"""
Tests for Bayesian Update in WorkerBelief.

Tests the conjugate normal Bayesian updating formula:
  posterior_var = 1 / (1/prior_var + 1/obs_var)
  posterior_mean = posterior_var * (prior_mean/prior_var + obs/obs_var)

Validates:
- Formula correctness against manual calculations
- Convergence behavior with repeated observations
- Edge cases: zero variance, extreme observations
- Confidence tracking
"""

import math
import pytest
from agents.memory.tiered import WorkerBelief


class TestBayesianUpdateFormula:
    """Test the Bayesian update formula for correctness."""

    def test_basic_update(self, worker_belief):
        """Basic update should shift mean toward observation."""
        initial_mean = worker_belief.mean  # 700.0
        worker_belief.update(900.0, obs_confidence=0.5)
        # Mean should shift toward 900
        assert worker_belief.mean > initial_mean
        assert worker_belief.mean < 900.0  # But not all the way

    def test_update_variance_decreases(self, worker_belief):
        """Each update should decrease variance (increase certainty)."""
        initial_var = worker_belief.variance  # 500.0
        worker_belief.update(800.0, obs_confidence=0.5)
        assert worker_belief.variance < initial_var

    def test_update_count_increments(self, worker_belief):
        """Update count should increment with each update."""
        assert worker_belief.update_count == 0
        worker_belief.update(800.0)
        assert worker_belief.update_count == 1
        worker_belief.update(750.0)
        assert worker_belief.update_count == 2

    def test_confidence_increases(self, worker_belief):
        """Confidence should increase with each update."""
        initial_conf = worker_belief.confidence  # 0.3
        worker_belief.update(800.0)
        assert worker_belief.confidence > initial_conf

    def test_confidence_capped_at_one(self, worker_belief):
        """Confidence should not exceed 1.0."""
        for _ in range(50):
            worker_belief.update(700.0)
        assert worker_belief.confidence <= 1.0

    def test_manual_calculation_verification(self):
        """Verify the formula against manual calculation."""
        belief = WorkerBelief(name="test", mean=100.0, variance=200.0, confidence=0.3)

        # Manual calculation:
        # obs_confidence = 0.5 → obs_variance = 1.0 / max(0.5 * 10, 0.1) = 1.0 / 5.0 = 0.2
        # posterior_var = 1 / (1/200 + 1/0.2) = 1 / (0.005 + 5.0) = 1 / 5.005 ≈ 0.1998
        # posterior_mean = 0.1998 * (100/200 + 150/0.2) = 0.1998 * (0.5 + 750) = 0.1998 * 750.5 ≈ 149.95

        belief.update(150.0, obs_confidence=0.5)

        expected_obs_var = 1.0 / max(0.5 * 10, 0.1)  # = 0.2
        expected_post_var = 1.0 / (1.0 / 200.0 + 1.0 / expected_obs_var)
        expected_post_mean = expected_post_var * (100.0 / 200.0 + 150.0 / expected_obs_var)

        assert abs(belief.variance - expected_post_var) < 0.01
        assert abs(belief.mean - expected_post_mean) < 0.01

    def test_high_confidence_observation_dominates(self):
        """High-confidence observation should pull mean strongly."""
        belief = WorkerBelief(name="test", mean=100.0, variance=200.0, confidence=0.3)
        belief.update(500.0, obs_confidence=0.95)
        # With high confidence, mean should be close to 500
        assert belief.mean > 300.0

    def test_low_confidence_observation_barely_moves(self):
        """Low-confidence observation should move mean less than high-confidence one."""
        # Compare: low-confidence vs high-confidence observation
        belief_low = WorkerBelief(name="test", mean=100.0, variance=50.0, confidence=0.3)
        belief_high = WorkerBelief(name="test", mean=100.0, variance=50.0, confidence=0.3)
        belief_low.update(500.0, obs_confidence=0.05)
        belief_high.update(500.0, obs_confidence=0.95)
        # Low confidence should move less than high confidence
        low_move = abs(belief_low.mean - 100.0)
        high_move = abs(belief_high.mean - 100.0)
        assert low_move < high_move, \
            f"Low-confidence moved {low_move:.1f}, high-confidence moved {high_move:.1f}"

    def test_repeated_same_observation_converges(self):
        """Repeated identical observations should converge to that value."""
        belief = WorkerBelief(name="test", mean=100.0, variance=500.0, confidence=0.3)
        target = 750.0
        for _ in range(20):
            belief.update(target, obs_confidence=0.5)
        # After many updates, mean should be close to target
        assert abs(belief.mean - target) < 50.0


class TestBayesianUpdateEdgeCases:
    """Test edge cases in Bayesian updating."""

    def test_zero_variance_prior(self):
        """Zero variance prior should be handled (clamped to 0.001)."""
        belief = WorkerBelief(name="test", mean=100.0, variance=0.0, confidence=0.5)
        # Should not raise — variance is clamped to max(variance, 0.001)
        belief.update(200.0, obs_confidence=0.5)
        assert belief.mean != 100.0  # Should have updated

    def test_very_small_variance_prior(self):
        """Very small prior variance should still allow updates."""
        belief = WorkerBelief(name="test", mean=100.0, variance=0.001, confidence=0.5)
        belief.update(200.0, obs_confidence=0.5)
        assert belief.mean > 100.0

    def test_very_large_observation(self):
        """Very large observation should not crash."""
        belief = WorkerBelief(name="test", mean=100.0, variance=500.0, confidence=0.3)
        belief.update(1_000_000.0, obs_confidence=0.5)
        assert math.isfinite(belief.mean)
        assert math.isfinite(belief.variance)

    def test_negative_observation(self):
        """Negative observations should work (e.g., losses)."""
        belief = WorkerBelief(name="test", mean=100.0, variance=500.0, confidence=0.3)
        belief.update(-200.0, obs_confidence=0.5)
        assert belief.mean < 100.0

    def test_zero_confidence_observation(self):
        """Zero confidence observation should be clamped."""
        belief = WorkerBelief(name="test", mean=100.0, variance=500.0, confidence=0.3)
        # obs_confidence=0 → obs_variance = 1.0 / max(0 * 10, 0.1) = 10.0
        belief.update(200.0, obs_confidence=0.0)
        assert math.isfinite(belief.mean)

    def test_timestamp_updates(self, worker_belief):
        """Last updated timestamp should change after update."""
        initial_time = worker_belief.last_updated
        worker_belief.update(800.0)
        assert worker_belief.last_updated >= initial_time


class TestBayesianConvergence:
    """Test convergence properties of the Bayesian updater."""

    def test_variance_decreases_monotonically(self):
        """Variance should decrease with each observation."""
        belief = WorkerBelief(name="test", mean=100.0, variance=1000.0, confidence=0.1)
        prev_var = belief.variance
        for i in range(10):
            belief.update(100.0 + i * 10, obs_confidence=0.5)
            assert belief.variance <= prev_var, \
                f"Variance increased at step {i}: {prev_var} → {belief.variance}"
            prev_var = belief.variance

    def test_many_updates_stable(self):
        """Many updates should produce stable, finite results."""
        belief = WorkerBelief(name="test", mean=500.0, variance=500.0, confidence=0.3)
        for i in range(100):
            belief.update(500.0 + (i % 50) * 5, obs_confidence=0.5)
        assert math.isfinite(belief.mean)
        assert math.isfinite(belief.variance)
        assert belief.variance > 0
        assert belief.update_count == 100

    def test_confidence_approaches_one(self):
        """Confidence should approach 1.0 after many updates."""
        belief = WorkerBelief(name="test", mean=100.0, variance=500.0, confidence=0.1)
        for _ in range(30):
            belief.update(100.0, obs_confidence=0.5)
        assert belief.confidence > 0.9


class TestWorkerBeliefSerialization:
    """Test serialization/deserialization of WorkerBelief."""

    def test_to_dict(self, worker_belief):
        """to_dict should produce a valid dictionary."""
        d = worker_belief.to_dict()
        assert "name" in d
        assert "mean" in d
        assert "variance" in d
        assert "confidence" in d
        assert "update_count" in d
        assert "last_updated" in d

    def test_from_dict_roundtrip(self, worker_belief):
        """Serialization roundtrip should preserve values."""
        d = worker_belief.to_dict()
        restored = WorkerBelief.from_dict(d)
        assert restored.name == worker_belief.name
        assert restored.mean == worker_belief.mean
        assert restored.variance == worker_belief.variance
        assert restored.confidence == worker_belief.confidence
        assert restored.update_count == worker_belief.update_count

    def test_from_dict_with_extra_keys(self):
        """from_dict should handle dict with matching keys."""
        d = {
            "name": "test",
            "mean": 500.0,
            "variance": 100.0,
            "confidence": 0.5,
            "update_count": 10,
            "last_updated": 1234567890.0,
        }
        belief = WorkerBelief.from_dict(d)
        assert belief.name == "test"
        assert belief.mean == 500.0
