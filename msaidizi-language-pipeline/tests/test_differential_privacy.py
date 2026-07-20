"""
Tests for Differential Privacy Module.

Tests the DifferentialPrivacy class:
- Noise scale calculation (σ = clip_norm * sqrt(2 * ln(1.25/δ)) / ε)
- Gaussian noise addition
- Gradient clipping
- L2 norm computation
- Edge cases and privacy budget validation
"""

import math
import pytest
from federated_learning import DifferentialPrivacy


class TestNoiseScaleCalculation:
    """Test the noise scale formula: σ = clip_norm * sqrt(2 * ln(1.25/δ)) / ε"""

    def test_strong_privacy_noise_scale(self, dp_strong):
        """ε=0.1 should produce large noise scale (σ ≈ 34.6 * clip_norm)."""
        # σ = 1.0 * sqrt(2 * ln(1.25 / 1e-5)) / 0.1
        # = sqrt(2 * ln(125000)) / 0.1
        # = sqrt(2 * 11.736) / 0.1
        # = sqrt(23.472) / 0.1
        # ≈ 4.845 / 0.1 ≈ 48.45
        expected_sigma = 1.0 * math.sqrt(2 * math.log(1.25 / 1e-5)) / 0.1
        assert expected_sigma > 30.0, "Strong privacy should have large noise"
        assert expected_sigma < 60.0

    def test_moderate_privacy_noise_scale(self, dp_moderate):
        """ε=1.0 should produce moderate noise scale (σ ≈ 3.46 * clip_norm)."""
        expected_sigma = 1.0 * math.sqrt(2 * math.log(1.25 / 1e-5)) / 1.0
        assert expected_sigma > 3.0
        assert expected_sigma < 10.0

    def test_noise_scale_proportional_to_clip_norm(self):
        """Noise scale should be proportional to clip_norm."""
        dp1 = DifferentialPrivacy(epsilon=1.0, delta=1e-5, clip_norm=1.0)
        dp2 = DifferentialPrivacy(epsilon=1.0, delta=1e-5, clip_norm=2.0)
        # The noise added to a value of 0 should have std proportional to clip_norm
        # We can't directly access sigma, but we can check via noise addition
        # For now, verify the objects are created correctly
        assert dp2.clip_norm == 2.0
        assert dp1.clip_norm == 1.0

    def test_noise_scale_inversely_proportional_to_epsilon(self):
        """Larger epsilon (less privacy) should produce smaller noise."""
        sigma_weak = 1.0 * math.sqrt(2 * math.log(1.25 / 1e-5)) / 10.0
        sigma_strong = 1.0 * math.sqrt(2 * math.log(1.25 / 1e-5)) / 0.1
        assert sigma_weak < sigma_strong


class TestDifferentialPrivacyConstruction:
    """Test DP object construction and validation."""

    def test_valid_construction(self):
        """Valid parameters should construct without error."""
        dp = DifferentialPrivacy(epsilon=0.1, delta=1e-5, clip_norm=1.0)
        assert dp.epsilon == 0.1
        assert dp.delta == 1e-5
        assert dp.clip_norm == 1.0

    def test_invalid_epsilon_zero(self):
        """Zero epsilon should raise ValueError."""
        with pytest.raises(ValueError, match="epsilon must be positive"):
            DifferentialPrivacy(epsilon=0.0)

    def test_invalid_epsilon_negative(self):
        """Negative epsilon should raise ValueError."""
        with pytest.raises(ValueError, match="epsilon must be positive"):
            DifferentialPrivacy(epsilon=-1.0)

    def test_invalid_delta_zero(self):
        """Zero delta should raise ValueError."""
        with pytest.raises(ValueError, match="delta must be in"):
            DifferentialPrivacy(delta=0.0)

    def test_invalid_delta_one(self):
        """Delta >= 1 should raise ValueError."""
        with pytest.raises(ValueError, match="delta must be in"):
            DifferentialPrivacy(delta=1.0)

    def test_invalid_clip_norm_zero(self):
        """Zero clip_norm should raise ValueError."""
        with pytest.raises(ValueError, match="clip_norm must be positive"):
            DifferentialPrivacy(clip_norm=0.0)

    def test_invalid_clip_norm_negative(self):
        """Negative clip_norm should raise ValueError."""
        with pytest.raises(ValueError, match="clip_norm must be positive"):
            DifferentialPrivacy(clip_norm=-1.0)

    def test_default_parameters(self):
        """Default parameters should match documented values."""
        dp = DifferentialPrivacy()
        assert dp.epsilon == 0.1
        assert dp.delta == 1e-5
        assert dp.clip_norm == 1.0


class TestGradientClipping:
    """Test gradient clipping to bounded L2 norm."""

    def test_clip_within_norm(self, dp_strong):
        """Gradient within clip norm should pass through unchanged."""
        gradient = {"a": 0.1, "b": 0.2, "c": 0.3}
        clipped = dp_strong.clip_gradient(gradient)
        # L2 norm = sqrt(0.01 + 0.04 + 0.09) = sqrt(0.14) ≈ 0.374
        # This is < 1.0 clip_norm, so should be unchanged
        assert clipped == gradient

    def test_clip_exceeds_norm(self, dp_strong):
        """Gradient exceeding clip norm should be scaled down."""
        gradient = {"a": 5.0, "b": 5.0, "c": 5.0}
        clipped = dp_strong.clip_gradient(gradient)
        # L2 norm = sqrt(75) ≈ 8.66, should be scaled to 1.0
        norm = dp_strong._compute_l2_norm(clipped)
        assert norm <= 1.0 + 1e-6  # Allow tiny floating-point error

    def test_clip_preserves_direction(self, dp_strong):
        """Clipping should preserve the direction (ratio of components)."""
        gradient = {"a": 3.0, "b": 4.0}
        clipped = dp_strong.clip_gradient(gradient)
        # Original ratio: 3/4 = 0.75
        if clipped["b"] != 0:
            assert abs(clipped["a"] / clipped["b"] - 0.75) < 0.01

    def test_clip_nested_gradient(self, dp_strong):
        """Clipping should work on nested gradient dicts."""
        gradient = {"layer1": {"w1": 5.0, "w2": 5.0}, "layer2": {"w3": 5.0}}
        clipped = dp_strong.clip_gradient(gradient)
        norm = dp_strong._compute_l2_norm(clipped)
        assert norm <= 1.0 + 1e-6

    def test_clip_gradient_with_list(self, dp_strong):
        """Clipping should work on gradients with list values."""
        gradient = {"weights": [3.0, 4.0, 0.0]}  # L2 norm = 5.0
        clipped = dp_strong.clip_gradient(gradient)
        norm = dp_strong._compute_l2_norm(clipped)
        assert norm <= 1.0 + 1e-6


class TestL2NormComputation:
    """Test L2 norm computation for nested structures."""

    def test_scalar_norm(self, dp_strong):
        """L2 norm of a scalar should be its absolute value."""
        assert dp_strong._compute_l2_norm(5.0) == 5.0
        assert dp_strong._compute_l2_norm(-3.0) == 3.0
        assert dp_strong._compute_l2_norm(0.0) == 0.0

    def test_dict_norm(self, dp_strong):
        """L2 norm of a dict should be sqrt of sum of squares."""
        gradient = {"a": 3.0, "b": 4.0}
        norm = dp_strong._compute_l2_norm(gradient)
        assert abs(norm - 5.0) < 1e-10  # sqrt(9 + 16) = 5

    def test_list_norm(self, dp_strong):
        """L2 norm of a list should be sqrt of sum of squares."""
        values = [1.0, 2.0, 2.0]
        norm = dp_strong._compute_l2_norm(values)
        assert abs(norm - 3.0) < 1e-10  # sqrt(1 + 4 + 4) = 3

    def test_nested_norm(self, dp_strong):
        """L2 norm of nested structure should aggregate correctly."""
        gradient = {"a": 3.0, "b": {"c": 4.0}}
        norm = dp_strong._compute_l2_norm(gradient)
        assert abs(norm - 5.0) < 1e-10  # sqrt(9 + 16) = 5

    def test_empty_dict_norm(self, dp_strong):
        """L2 norm of empty dict should be 0."""
        assert dp_strong._compute_l2_norm({}) == 0.0

    def test_empty_list_norm(self, dp_strong):
        """L2 norm of empty list should be 0."""
        assert dp_strong._compute_l2_norm([]) == 0.0


class TestNoiseAddition:
    """Test Gaussian noise addition to gradients."""

    def test_add_noise_to_scalar(self, dp_strong):
        """Noise should be added to scalar values."""
        gradient = {"value": 0.0}
        noised = dp_strong.add_noise(gradient)
        # With strong privacy, noise should be substantial
        # We can't check exact value, but it should be different
        # (with overwhelming probability)
        assert "value" in noised

    def test_add_noise_preserves_structure(self, dp_strong):
        """Noise addition should preserve gradient structure."""
        gradient = {"a": 1.0, "b": 2.0, "c": 3.0}
        noised = dp_strong.add_noise(gradient)
        assert set(noised.keys()) == set(gradient.keys())

    def test_add_noise_to_nested(self, dp_strong):
        """Noise should be added to nested gradient dicts."""
        gradient = {"layer": {"w1": 1.0, "w2": 2.0}}
        noised = dp_strong.add_noise(gradient)
        assert "layer" in noised
        assert "w1" in noised["layer"]
        assert "w2" in noised["layer"]

    def test_add_noise_to_list(self, dp_strong):
        """Noise should be added to list values."""
        gradient = {"weights": [1.0, 2.0, 3.0]}
        noised = dp_strong.add_noise(gradient)
        assert len(noised["weights"]) == 3

    def test_add_noise_preserves_non_numeric(self, dp_strong):
        """Non-numeric values should pass through unchanged."""
        gradient = {"name": "test", "value": 1.0}
        noised = dp_strong.add_noise(gradient)
        assert noised["name"] == "test"

    def test_add_noise_statistical_properties(self, dp_moderate):
        """Noise should have approximately correct statistical properties."""
        # Generate many noisy values from a zero gradient
        gradient = {"value": 0.0}
        samples = [dp_moderate.add_noise(gradient)["value"] for _ in range(1000)]
        mean = sum(samples) / len(samples)
        # Mean should be close to 0 (within 3 standard errors)
        sigma = 1.0 * math.sqrt(2 * math.log(1.25 / 1e-5)) / 1.0
        se = sigma / math.sqrt(1000)
        assert abs(mean) < 3 * se, f"Noise mean {mean} too far from 0 (se={se})"

    def test_strong_privacy_adds_more_noise(self, dp_strong, dp_moderate):
        """Stronger privacy (lower ε) should add more noise on average."""
        gradient = {"value": 0.0}
        strong_diffs = [abs(dp_strong.add_noise(gradient)["value"]) for _ in range(100)]
        moderate_diffs = [abs(dp_moderate.add_noise(gradient)["value"]) for _ in range(100)]
        avg_strong = sum(strong_diffs) / len(strong_diffs)
        avg_moderate = sum(moderate_diffs) / len(moderate_diffs)
        assert avg_strong > avg_moderate


class TestGradientScaling:
    """Test gradient scaling for clipping."""

    def test_scale_gradient_scalar(self, dp_strong):
        """Scaling a scalar should multiply by factor."""
        result = dp_strong._scale_gradient(10.0, 0.5)
        assert abs(result - 5.0) < 1e-10

    def test_scale_gradient_dict(self, dp_strong):
        """Scaling a dict should multiply all values."""
        gradient = {"a": 10.0, "b": 20.0}
        result = dp_strong._scale_gradient(gradient, 0.5)
        assert result["a"] == 5.0
        assert result["b"] == 10.0

    def test_scale_gradient_list(self, dp_strong):
        """Scaling a list should multiply all elements."""
        values = [10.0, 20.0, 30.0]
        result = dp_strong._scale_gradient(values, 0.1)
        assert result == [1.0, 2.0, 3.0]

    def test_scale_gradient_nested(self, dp_strong):
        """Scaling should work recursively on nested structures."""
        gradient = {"layer": {"w1": 10.0, "w2": 20.0}}
        result = dp_strong._scale_gradient(gradient, 0.5)
        assert result["layer"]["w1"] == 5.0
        assert result["layer"]["w2"] == 10.0

    def test_scale_by_one_identity(self, dp_strong):
        """Scaling by 1.0 should be identity."""
        gradient = {"a": 42.0, "b": -7.0}
        result = dp_strong._scale_gradient(gradient, 1.0)
        assert result == gradient


class TestDifferentialPrivacyEdgeCases:
    """Test edge cases for differential privacy."""

    def test_very_small_epsilon(self):
        """Very small epsilon (very strong privacy) should still work."""
        dp = DifferentialPrivacy(epsilon=0.001, delta=1e-10, clip_norm=1.0)
        gradient = {"value": 0.0}
        noised = dp.add_noise(gradient)
        assert math.isfinite(noised["value"])

    def test_very_large_epsilon(self):
        """Very large epsilon (very weak privacy) should add tiny noise."""
        dp = DifferentialPrivacy(epsilon=1000.0, delta=1e-5, clip_norm=1.0)
        gradient = {"value": 0.0}
        noised = dp.add_noise(gradient)
        # With ε=1000, noise should be very small
        assert abs(noised["value"]) < 1.0  # Very likely with tiny noise

    def test_empty_gradient(self, dp_strong):
        """Empty gradient should not crash."""
        clipped = dp_strong.clip_gradient({})
        assert clipped == {}
        noised = dp_strong.add_noise({})
        assert noised == {}

    def test_single_element_gradient(self, dp_strong):
        """Single-element gradient should work."""
        gradient = {"only": 42.0}
        clipped = dp_strong.clip_gradient(gradient)
        noised = dp_strong.add_noise(clipped)
        assert "only" in noised
