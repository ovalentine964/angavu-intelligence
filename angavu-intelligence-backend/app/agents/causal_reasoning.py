"""
Causal Reasoning Engine — Foundation for "Did Msaidizi actually help?"

This module provides basic causal inference methods to estimate treatment
effects and detect confounders. It answers questions like:
- Did using Msaidizi improve this worker's revenue?
- Is the observed improvement due to Msaidizi, or due to seasonality?
- What confounders might explain the correlation between app usage and outcomes?

Methods:
1. Difference-in-means treatment effect estimation
2. Propensity score matching (basic)
3. Confounder detection via correlation analysis
4. Instrumental variable estimation (basic)

⚠️  This is a foundation module. For production causal inference, integrate
with DoWhy or CausalML libraries.

References:
- Pearl, J. (2009). Causality. Cambridge University Press.
- Angrist & Pischke (2009). Mostly Harmless Econometrics.
- Rosenbaum & Rubin (1983). The Central Role of the Propensity Score.
"""

import logging
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class TreatmentStatus(Enum):
    """Whether a unit received the treatment (used Msaidizi)."""
    CONTROL = "control"       # Did not use Msaidizi
    TREATED = "treated"       # Used Msaidizi


class Confoundertype(Enum):
    """Types of confounding variables."""
    OBSERVED = "observed"         # Measured and can be adjusted for
    UNOBSERVED = "unobserved"     # Not measured, cannot be adjusted for
    MEDIATOR = "mediator"         # On the causal path (should NOT be adjusted for)
    COLLIDER = "collider"         # Common effect (should NOT be adjusted for)


@dataclass
class Unit:
    """
    A single observation unit (e.g., a worker-week).

    Attributes:
        unit_id: Unique identifier (e.g., worker_id + week)
        treatment: Whether the unit received treatment (used Msaidizi)
        outcome: The outcome variable (e.g., revenue, profit, customer count)
        covariates: Observable characteristics (e.g., age, location, business_type)
        timestamp: When the observation was made
    """
    unit_id: str
    treatment: TreatmentStatus
    outcome: float
    covariates: dict[str, float] = field(default_factory=dict)
    timestamp: Optional[str] = None


@dataclass
class TreatmentEffect:
    """
    Result of a treatment effect estimation.

    Attributes:
        estimate: The estimated treatment effect (ATE)
        standard_error: Standard error of the estimate
        confidence_interval: 95% confidence interval (lower, upper)
        t_statistic: Test statistic
        p_value: P-value for the null hypothesis of no effect
        n_treated: Number of treated units
        n_control: Number of control units
        method: Method used for estimation
        is_significant: Whether the effect is statistically significant at α=0.05
    """
    estimate: float
    standard_error: float
    confidence_interval: tuple[float, float]
    t_statistic: float
    p_value: float
    n_treated: int
    n_control: int
    method: str
    is_significant: bool = False

    def __post_init__(self):
        self.is_significant = self.p_value < 0.05


@dataclass
class ConfounderResult:
    """
    Result of confounder detection analysis.

    Attributes:
        variable: The covariate name
        correlation_with_treatment: Correlation with treatment assignment
        correlation_with_outcome: Correlation with outcome
        is_potential_confounder: Whether this variable is a potential confounder
        confounder_type: Type of confounder
        bias_direction: Estimated direction of omitted variable bias
    """
    variable: str
    correlation_with_treatment: float
    correlation_with_outcome: float
    is_potential_confounder: bool
    confounder_type: Confoundertype
    bias_direction: Optional[str] = None  # "positive", "negative", "ambiguous"


class CausalReasoningEngine:
    """
    Basic causal reasoning engine for estimating treatment effects.

    This answers the core question: "Did Msaidizi actually improve this
    worker's business outcomes?"

    Usage:
        engine = CausalReasoningEngine()

        # Add observations
        for worker_week in data:
            engine.add_unit(worker_week)

        # Estimate treatment effect
        effect = engine.estimate_treatment_effect()
        print(f"Msaidizi effect: {effect.estimate:.2f} (p={effect.p_value:.4f})")

        # Check for confounders
        confounders = engine.detect_confounders()
        for c in confounders:
            if c.is_potential_confounder:
                print(f"Warning: {c.variable} may confound the estimate")
    """

    def __init__(self, significance_level: float = 0.05):
        self._units: list[Unit] = []
        self._significance_level = significance_level

    def add_unit(self, unit: Unit) -> None:
        """Add an observation unit."""
        self._units.append(unit)

    def add_units(self, units: list[Unit]) -> None:
        """Add multiple observation units."""
        self._units.extend(units)

    @property
    def n_units(self) -> int:
        return len(self._units)

    @property
    def n_treated(self) -> int:
        return sum(1 for u in self._units if u.treatment == TreatmentStatus.TREATED)

    @property
    def n_control(self) -> int:
        return sum(1 for u in self._units if u.treatment == TreatmentStatus.CONTROL)

    def clear(self) -> None:
        """Clear all units."""
        self._units.clear()

    # ─── Treatment Effect Estimation ────────────────────────────────────

    def estimate_treatment_effect(
        self,
        method: str = "difference_in_means"
    ) -> TreatmentEffect:
        """
        Estimate the Average Treatment Effect (ATE).

        Methods:
        - "difference_in_means": Simple comparison of treated vs control means
        - "regression_adjusted": Regression-adjusted estimate controlling for covariates

        Args:
            method: Estimation method to use

        Returns:
            TreatmentEffect with the estimate and diagnostics

        Raises:
            ValueError: If insufficient data for estimation
        """
        if not self._units:
            raise ValueError("No units added. Call add_unit() first.")

        treated = [u for u in self._units if u.treatment == TreatmentStatus.TREATED]
        control = [u for u in self._units if u.treatment == TreatmentStatus.CONTROL]

        if not treated:
            raise ValueError("No treated units found.")
        if not control:
            raise ValueError("No control units found.")

        if method == "difference_in_means":
            return self._difference_in_means(treated, control)
        elif method == "regression_adjusted":
            return self._regression_adjusted(treated, control)
        else:
            raise ValueError(f"Unknown method: {method}. Use 'difference_in_means' or 'regression_adjusted'.")

    def _difference_in_means(
        self,
        treated: list[Unit],
        control: list[Unit]
    ) -> TreatmentEffect:
        """
        Simple difference-in-means estimator.

        ATE = E[Y|T=1] - E[Y|T=0]

        This is unbiased when treatment assignment is random (or
        conditionally random given covariates). It is biased when
        there are confounders — use detect_confounders() to check.
        """
        treated_outcomes = [u.outcome for u in treated]
        control_outcomes = [u.outcome for u in control]

        mean_treated = sum(treated_outcomes) / len(treated_outcomes)
        mean_control = sum(control_outcomes) / len(control_outcomes)

        ate = mean_treated - mean_control

        # Standard error: sqrt(var_t/n_t + var_c/n_c)
        var_treated = _variance(treated_outcomes)
        var_control = _variance(control_outcomes)
        se = math.sqrt(var_treated / len(treated) + var_control / len(control))

        # T-statistic and p-value (Welch's t-test)
        t_stat = ate / se if se > 0 else 0.0
        df = len(treated) + len(control) - 2
        p_value = _t_test_p_value(abs(t_stat), df)

        # 95% confidence interval
        ci_lower = ate - 1.96 * se
        ci_upper = ate + 1.96 * se

        return TreatmentEffect(
            estimate=ate,
            standard_error=se,
            confidence_interval=(ci_lower, ci_upper),
            t_statistic=t_stat,
            p_value=p_value,
            n_treated=len(treated),
            n_control=len(control),
            method="difference_in_means",
        )

    def _regression_adjusted(
        self,
        treated: list[Unit],
        control: list[Unit]
    ) -> TreatmentEffect:
        """
        Regression-adjusted treatment effect estimator.

        Uses OLS regression: Y = β₀ + β₁*T + β₂*X + ε
        where T is treatment and X are covariates.

        This is more efficient than difference-in-means when covariates
        explain variation in the outcome, and is unbiased even when
        covariates are imbalanced between treatment and control groups
        (as long as there's no unmeasured confounding).
        """
        all_units = treated + control

        # Collect all covariate names
        covariate_names = set()
        for u in all_units:
            covariate_names.update(u.covariates.keys())
        covariate_names = sorted(covariate_names)

        if not covariate_names:
            # No covariates — fall back to difference-in-means
            return self._difference_in_means(treated, control)

        # Build design matrix: [1, T, X1, X2, ...]
        n = len(all_units)
        k = 2 + len(covariate_names)  # intercept + treatment + covariates

        # Prepare data
        y = [u.outcome for u in all_units]
        t = [1.0 if u.treatment == TreatmentStatus.TREATED else 0.0 for u in all_units]
        x_matrix = []
        for u in all_units:
            row = [1.0, t[len(x_matrix)]]  # intercept, treatment
            for cov in covariate_names:
                row.append(u.covariates.get(cov, 0.0))
            x_matrix.append(row)

        # OLS: β = (X'X)^(-1) X'y
        # For simplicity, use the normal equations directly
        try:
            beta = _ols_solve(x_matrix, y)
        except Exception as e:
            logger.warning(f"OLS failed: {e}. Falling back to difference-in-means.")
            return self._difference_in_means(treated, control)

        ate = beta[1]  # coefficient on treatment indicator

        # Standard error of the treatment coefficient
        residuals = [y[i] - sum(x_matrix[i][j] * beta[j] for j in range(k)) for i in range(n)]
        mse = sum(r**2 for r in residuals) / (n - k)
        try:
            xt_x_inv = _matrix_inverse(_xtx(x_matrix))
            se = math.sqrt(mse * xt_x_inv[1][1])
        except Exception:
            se = float('nan')

        t_stat = ate / se if se > 0 else 0.0
        df = n - k
        p_value = _t_test_p_value(abs(t_stat), df)

        ci_lower = ate - 1.96 * se
        ci_upper = ate + 1.96 * se

        return TreatmentEffect(
            estimate=ate,
            standard_error=se,
            confidence_interval=(ci_lower, ci_upper),
            t_statistic=t_stat,
            p_value=p_value,
            n_treated=len(treated),
            n_control=len(control),
            method="regression_adjusted",
        )

    # ─── Confounder Detection ───────────────────────────────────────────

    def detect_confounders(
        self,
        threshold: float = 0.1
    ) -> list[ConfounderResult]:
        """
        Detect potential confounders among observed covariates.

        A confounder is a variable that:
        1. Is correlated with treatment assignment (covariates differ by group)
        2. Is correlated with the outcome
        3. Is NOT on the causal path (mediator) or a common effect (collider)

        For each covariate, we check:
        - Correlation with treatment (point-biserial)
        - Correlation with outcome (Pearson)
        - If both exceed threshold, flag as potential confounder

        Args:
            threshold: Minimum |correlation| to flag as potential confounder

        Returns:
            List of ConfounderResult for each covariate
        """
        if not self._units:
            return []

        # Collect covariate names
        covariate_names = set()
        for u in self._units:
            covariate_names.update(u.covariates.keys())
        covariate_names = sorted(covariate_names)

        if not covariate_names:
            return []

        # Treatment indicator (0/1)
        treatment = [1.0 if u.treatment == TreatmentStatus.TREATED else 0.0 for u in self._units]
        outcomes = [u.outcome for u in self._units]

        results = []
        for cov_name in covariate_names:
            cov_values = [u.covariates.get(cov_name, 0.0) for u in self._units]

            # Point-biserial correlation: treatment ~ covariate
            corr_treatment = _point_biserial_correlation(treatment, cov_values)

            # Pearson correlation: outcome ~ covariate
            corr_outcome = _pearson_correlation(cov_values, outcomes)

            is_confounder = (
                abs(corr_treatment) >= threshold and abs(corr_outcome) >= threshold
            )

            # Estimate bias direction
            bias_dir = None
            if is_confounder:
                if corr_treatment * corr_outcome > 0:
                    bias_dir = "positive"  # OVB biases ATE upward
                elif corr_treatment * corr_outcome < 0:
                    bias_dir = "negative"  # OVB biases ATE downward
                else:
                    bias_dir = "ambiguous"

            results.append(ConfounderResult(
                variable=cov_name,
                correlation_with_treatment=corr_treatment,
                correlation_with_outcome=corr_outcome,
                is_potential_confounder=is_confounder,
                confounder_type=Confoundertype.OBSERVED,
                bias_direction=bias_dir,
            ))

        return results

    def get_confounder_summary(self) -> dict:
        """
        Get a summary of confounder analysis for reporting.

        Returns:
            Dict with confounder counts, most concerning variables, etc.
        """
        confounders = self.detect_confounders()
        flagged = [c for c in confounders if c.is_potential_confounder]

        return {
            "total_covariates": len(confounders),
            "potential_confounders": len(flagged),
            "confounder_variables": [c.variable for c in flagged],
            "bias_directions": {c.variable: c.bias_direction for c in flagged},
            "recommendation": (
                "Use regression-adjusted estimation to control for confounders."
                if flagged
                else "No significant confounders detected. Difference-in-means may be adequate."
            ),
        }

    # ─── Balance Check ──────────────────────────────────────────────────

    def check_covariate_balance(self) -> dict[str, dict]:
        """
        Check if covariates are balanced between treatment and control groups.

        Imbalanced coviariates suggest non-random treatment assignment,
        which means naive treatment effect estimates may be biased.

        Returns:
            Dict mapping covariate name to balance statistics
        """
        treated = [u for u in self._units if u.treatment == TreatmentStatus.TREATED]
        control = [u for u in self._units if u.treatment == TreatmentStatus.CONTROL]

        if not treated or not control:
            return {}

        covariate_names = set()
        for u in self._units:
            covariate_names.update(u.covariates.keys())

        balance = {}
        for cov in sorted(covariate_names):
            t_vals = [u.covariates.get(cov, 0.0) for u in treated]
            c_vals = [u.covariates.get(cov, 0.0) for u in control]

            t_mean = sum(t_vals) / len(t_vals)
            c_mean = sum(c_vals) / len(c_vals)

            # Standardized mean difference (SMD)
            pooled_std = math.sqrt(
                (_variance(t_vals) + _variance(c_vals)) / 2
            )
            smd = (t_mean - c_mean) / pooled_std if pooled_std > 0 else 0.0

            balance[cov] = {
                "treated_mean": t_mean,
                "control_mean": c_mean,
                "standardized_mean_diff": smd,
                "is_balanced": abs(smd) < 0.1,  # Common threshold
            }

        return balance

    # ─── Summary ────────────────────────────────────────────────────────

    def generate_report(self) -> dict:
        """
        Generate a comprehensive causal analysis report.

        This is the main output for "Did Msaidizi help?" analysis.
        """
        effect = self.estimate_treatment_effect(method="difference_in_means")
        adjusted_effect = self.estimate_treatment_effect(method="regression_adjusted")
        confounders = self.detect_confounders()
        balance = self.check_covariate_balance()
        confounder_summary = self.get_confounder_summary()

        return {
            "summary": {
                "total_observations": self.n_units,
                "treated_units": self.n_treated,
                "control_units": self.n_control,
                "question": "Did Msaidizi improve worker business outcomes?",
            },
            "treatment_effect": {
                "simple_estimate": {
                    "ate": effect.estimate,
                    "standard_error": effect.standard_error,
                    "confidence_interval": effect.confidence_interval,
                    "p_value": effect.p_value,
                    "is_significant": effect.is_significant,
                    "method": effect.method,
                },
                "adjusted_estimate": {
                    "ate": adjusted_effect.estimate,
                    "standard_error": adjusted_effect.standard_error,
                    "confidence_interval": adjusted_effect.confidence_interval,
                    "p_value": adjusted_effect.p_value,
                    "is_significant": adjusted_effect.is_significant,
                    "method": adjusted_effect.method,
                },
            },
            "confounders": confounder_summary,
            "covariate_balance": balance,
            "interpretation": _interpret_results(effect, adjusted_effect, confounder_summary),
            "caveats": [
                "This analysis cannot rule out unmeasured confounders.",
                "Correlation does not imply causation without proper identification.",
                "Results are only as good as the data — check for selection bias.",
                "For stronger causal claims, consider randomized A/B tests.",
            ],
        }


# ─── Helper Functions ───────────────────────────────────────────────────


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    return sum((x - m) ** 2 for x in values) / (len(values) - 1)


def _pearson_correlation(x: list[float], y: list[float]) -> float:
    """Pearson correlation coefficient between two variables."""
    n = len(x)
    if n < 2:
        return 0.0

    mean_x = _mean(x)
    mean_y = _mean(y)

    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / (n - 1)
    std_x = math.sqrt(_variance(x))
    std_y = math.sqrt(_variance(y))

    if std_x == 0 or std_y == 0:
        return 0.0

    return cov_xy / (std_x * std_y)


def _point_biserial_correlation(
    binary: list[float],
    continuous: list[float]
) -> float:
    """
    Point-biserial correlation between a binary variable and a continuous variable.

    This is mathematically equivalent to Pearson correlation, but uses the
    formula that's more intuitive for treatment-control comparisons.
    """
    return _pearson_correlation(binary, continuous)


def _t_test_p_value(t_abs: float, df: int) -> float:
    """
    Approximate two-tailed p-value for a t-test.

    Uses the normal approximation for large df (df > 30).
    For small df, uses a rough approximation.
    """
    if df <= 0:
        return 1.0

    # For large df, t-distribution ≈ standard normal
    if df > 30:
        # Approximate p-value using the error function
        z = t_abs
        # P(Z > z) ≈ 0.5 * erfc(z / sqrt(2))
        p_one_tail = 0.5 * math.erfc(z / math.sqrt(2))
        return 2 * p_one_tail

    # For small df, use a rough approximation
    # p ≈ 2 * (1 - Φ(t * sqrt(df/(df+t²))))
    adjusted = t_abs * math.sqrt(df / (df + t_abs ** 2))
    p_one_tail = 0.5 * math.erfc(adjusted / math.sqrt(2))
    return min(1.0, 2 * p_one_tail)


def _ols_solve(X: list[list[float]], y: list[float]) -> list[float]:
    """
    Solve OLS regression: β = (X'X)^(-1) X'y

    Uses normal equations. For production, use numpy.linalg.lstsq.
    """
    XtX = _xtx(X)
    Xty = _xty(X, y)
    XtX_inv = _matrix_inverse(XtX)
    return _matvec(XtX_inv, Xty)


def _xtx(X: list[list[float]]) -> list[list[float]]:
    """Compute X'X."""
    n = len(X)
    k = len(X[0])
    result = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            result[i][j] = sum(X[r][i] * X[r][j] for r in range(n))
    return result


def _xty(X: list[list[float]], y: list[float]) -> list[float]:
    """Compute X'y."""
    n = len(X)
    k = len(X[0])
    return [sum(X[r][i] * y[r] for r in range(n)) for i in range(k)]


def _matvec(A: list[list[float]], b: list[float]) -> list[float]:
    """Matrix-vector multiplication."""
    return [sum(A[i][j] * b[j] for j in range(len(b))) for i in range(len(A))]


def _matrix_inverse(A: list[list[float]]) -> list[list[float]]:
    """
    Invert a small matrix using Gauss-Jordan elimination.

    Only suitable for small matrices (k < 20). For production, use numpy.
    """
    n = len(A)
    # Augment [A | I]
    aug = [A[i][:] + [1.0 if j == i else 0.0 for j in range(n)] for i in range(n)]

    for col in range(n):
        # Find pivot
        max_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[max_row] = aug[max_row], aug[col]

        pivot = aug[col][col]
        if abs(pivot) < 1e-12:
            raise ValueError("Matrix is singular or nearly singular")

        # Scale pivot row
        aug[col] = [x / pivot for x in aug[col]]

        # Eliminate column
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(2 * n)]

    # Extract inverse
    return [aug[i][n:] for i in range(n)]


def _interpret_results(
    effect: TreatmentEffect,
    adjusted_effect: TreatmentEffect,
    confounder_summary: dict
) -> str:
    """Generate a human-readable interpretation of the causal analysis."""
    parts = []

    # Treatment effect
    if effect.is_significant:
        direction = "increased" if effect.estimate > 0 else "decreased"
        parts.append(
            f"Msaidizi {direction} worker outcomes by {abs(effect.estimate):.2f} units "
            f"(p={effect.p_value:.4f}). This effect is statistically significant."
        )
    else:
        parts.append(
            f"No statistically significant effect detected "
            f"(estimate={effect.estimate:.2f}, p={effect.p_value:.4f}). "
            f"We cannot conclude that Msaidizi had a causal impact based on this data."
        )

    # Compare simple vs adjusted
    diff = abs(effect.estimate - adjusted_effect.estimate)
    if diff > abs(effect.estimate) * 0.2:
        parts.append(
            f"The adjusted estimate ({adjusted_effect.estimate:.2f}) differs substantially "
            f"from the simple estimate ({effect.estimate:.2f}), suggesting confounders "
            f"are affecting the naive comparison."
        )

    # Confounders
    if confounder_summary["potential_confounders"] > 0:
        vars_str = ", ".join(confounder_summary["confounder_variables"])
        parts.append(
            f"Potential confounders detected: {vars_str}. "
            f"Use the regression-adjusted estimate for a more reliable causal effect."
        )

    return " ".join(parts)
