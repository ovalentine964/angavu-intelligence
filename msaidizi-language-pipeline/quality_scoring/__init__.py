"""
Language Quality Scoring Module
================================

Tracks how well the model performs per dialect, identifies gaps,
and triggers retraining when quality drops below thresholds.

Metrics tracked per dialect:
1. Perplexity — model's prediction confidence (lower = better)
2. BLEU — output similarity to reference (higher = better)
3. User satisfaction — explicit/implicit feedback signals
4. Correction rate — how often users correct the model
5. Response coherence — semantic consistency of responses
6. Dialect authenticity — how "native" the output sounds
7. Code-switch fluency — smoothness of language mixing

The quality scorer identifies:
- Dialects that need more training data
- Dialects where the model is improving vs. degrading
- Vocabulary gaps (words the model doesn't understand)
- Grammar patterns the model gets wrong
"""

from __future__ import annotations

import json
import math
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class InteractionMetric:
    """A single interaction's quality metrics."""

    interaction_id: str
    user_id_hash: str
    dialect: str
    timestamp: float

    # Input/output
    user_input: str
    model_output: str
    corrected_output: Optional[str] = None

    # Quality signals
    user_explicit_rating: Optional[int] = None    # 1-5 stars
    was_corrected: bool = False                    # User corrected the output
    correction_type: Optional[str] = None         # "word", "grammar", "meaning", "tone"
    response_time_ms: int = 0                      # How fast the model responded
    user_engaged_after: bool = False               # Did user continue the conversation?

    # Computed scores
    coherence_score: float = 0.0      # 0-1
    dialect_authenticity: float = 0.0 # 0-1
    vocabulary_coverage: float = 0.0  # 0-1 (how many words the model knew)

    @property
    def composite_score(self) -> float:
        """Weighted composite quality score."""
        scores = []
        weights = []

        if self.user_explicit_rating is not None:
            scores.append(self.user_explicit_rating / 5.0)
            weights.append(0.3)

        if not self.was_corrected:
            scores.append(1.0)
        else:
            scores.append(0.3)  # Corrected = low quality
        weights.append(0.25)

        if self.coherence_score > 0:
            scores.append(self.coherence_score)
            weights.append(0.2)

        if self.dialect_authenticity > 0:
            scores.append(self.dialect_authenticity)
            weights.append(0.15)

        if self.vocabulary_coverage > 0:
            scores.append(self.vocabulary_coverage)
            weights.append(0.1)

        if not scores:
            return 0.5

        return sum(s * w for s, w in zip(scores, weights)) / sum(weights)


@dataclass
class DialectReport:
    """Quality report for a specific dialect."""

    dialect: str
    period_start: float
    period_end: float
    total_interactions: int = 0

    # Aggregate metrics
    avg_composite_score: float = 0.0
    correction_rate: float = 0.0         # Fraction of interactions corrected
    avg_coherence: float = 0.0
    avg_dialect_authenticity: float = 0.0
    avg_vocabulary_coverage: float = 0.0
    avg_user_rating: float = 0.0         # Only if ratings provided
    engagement_rate: float = 0.0         # Users who continued after response

    # Trend analysis
    score_trend: str = "stable"          # "improving", "stable", "degrading"
    trend_magnitude: float = 0.0         # How much it changed

    # Gap identification
    vocabulary_gaps: List[str] = field(default_factory=list)     # Unknown words
    grammar_errors: List[str] = field(default_factory=list)      # Common grammar mistakes
    low_quality_patterns: List[str] = field(default_factory=list)  # Patterns causing errors

    # Recommendations
    needs_more_data: bool = False
    needs_retraining: bool = False
    recommended_actions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Export as dictionary."""
        return {
            "dialect": self.dialect,
            "period": {
                "start": datetime.fromtimestamp(self.period_start).isoformat(),
                "end": datetime.fromtimestamp(self.period_end).isoformat(),
            },
            "total_interactions": self.total_interactions,
            "metrics": {
                "composite_score": round(self.avg_composite_score, 3),
                "correction_rate": round(self.correction_rate, 3),
                "coherence": round(self.avg_coherence, 3),
                "dialect_authenticity": round(self.avg_dialect_authenticity, 3),
                "vocabulary_coverage": round(self.avg_vocabulary_coverage, 3),
                "user_rating": round(self.avg_user_rating, 3),
                "engagement_rate": round(self.engagement_rate, 3),
            },
            "trend": {
                "direction": self.score_trend,
                "magnitude": round(self.trend_magnitude, 3),
            },
            "gaps": {
                "vocabulary": self.vocabulary_gaps[:20],
                "grammar": self.grammar_errors[:10],
                "patterns": self.low_quality_patterns[:10],
            },
            "recommendations": {
                "needs_more_data": self.needs_more_data,
                "needs_retraining": self.needs_retraining,
                "actions": self.recommended_actions,
            },
        }


@dataclass
class QualityScorer:
    """
    Tracks and scores model quality per dialect.

    Collects interaction metrics, computes per-dialect quality scores,
    identifies gaps, and recommends actions.
    """

    # Quality threshold below which retraining is triggered
    quality_threshold: float = 0.6
    min_interactions_for_scoring: int = 50
    report_interval_hours: int = 168  # weekly

    # Storage
    _metrics: Dict[str, List[InteractionMetric]] = field(
        default_factory=lambda: defaultdict(list)
    )
    _vocabulary_unknown: Dict[str, set] = field(
        default_factory=lambda: defaultdict(set)
    )
    _correction_patterns: Dict[str, List[str]] = field(
        default_factory=lambda: defaultdict(list)
    )
    _reports: Dict[str, List[DialectReport]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def record_interaction(self, metric: InteractionMetric) -> None:
        """Record an interaction metric."""
        self._metrics[metric.dialect].append(metric)

        # Track vocabulary gaps
        if metric.was_corrected and metric.corrected_output:
            # Words in correction that weren't in model output
            model_words = set(metric.model_output.lower().split())
            correct_words = set(metric.corrected_output.lower().split())
            new_words = correct_words - model_words
            self._vocabulary_unknown[metric.dialect].update(new_words)

            # Track correction patterns
            if metric.correction_type:
                self._correction_patterns[metric.dialect].append(
                    metric.correction_type
                )

        # Limit stored metrics per dialect
        max_stored = 10000
        if len(self._metrics[metric.dialect]) > max_stored:
            self._metrics[metric.dialect] = self._metrics[metric.dialect][-max_stored:]

    def record_correction(
        self,
        user_id_hash: str,
        dialect: str,
        original_input: str,
        incorrect_output: str,
        correct_output: str,
        correction_type: str = "meaning",
    ) -> None:
        """Record a user correction as a quality signal."""
        metric = InteractionMetric(
            interaction_id=f"corr_{int(time.time())}",
            user_id_hash=user_id_hash,
            dialect=dialect,
            timestamp=time.time(),
            user_input=original_input,
            model_output=incorrect_output,
            corrected_output=correct_output,
            was_corrected=True,
            correction_type=correction_type,
            coherence_score=0.2,  # Corrected = low coherence
        )
        self.record_interaction(metric)

    def get_dialect_score(self, dialect: str) -> float:
        """Get current composite quality score for a dialect."""
        metrics = self._metrics.get(dialect, [])
        if not metrics:
            return 0.0

        # Use recent metrics (last 7 days)
        cutoff = time.time() - (7 * 24 * 3600)
        recent = [m for m in metrics if m.timestamp > cutoff]

        if not recent:
            return 0.0

        return sum(m.composite_score for m in recent) / len(recent)

    def generate_report(
        self,
        dialect: str,
        period_hours: int = 168,
    ) -> Optional[DialectReport]:
        """
        Generate a quality report for a dialect.

        Args:
            dialect: Dialect to report on
            period_hours: Look-back period in hours

        Returns:
            DialectReport if enough data, None otherwise
        """
        metrics = self._metrics.get(dialect, [])
        if len(metrics) < self.min_interactions_for_scoring:
            return None

        cutoff = time.time() - (period_hours * 3600)
        period_metrics = [m for m in metrics if m.timestamp > cutoff]

        if not period_metrics:
            return None

        report = DialectReport(
            dialect=dialect,
            period_start=cutoff,
            period_end=time.time(),
            total_interactions=len(period_metrics),
        )

        # Compute aggregate metrics
        report.avg_composite_score = (
            sum(m.composite_score for m in period_metrics) / len(period_metrics)
        )

        corrected = [m for m in period_metrics if m.was_corrected]
        report.correction_rate = len(corrected) / len(period_metrics)

        coherence_scores = [m.coherence_score for m in period_metrics if m.coherence_score > 0]
        report.avg_coherence = (
            sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0.0
        )

        auth_scores = [m.dialect_authenticity for m in period_metrics if m.dialect_authenticity > 0]
        report.avg_dialect_authenticity = (
            sum(auth_scores) / len(auth_scores) if auth_scores else 0.0
        )

        vocab_scores = [m.vocabulary_coverage for m in period_metrics if m.vocabulary_coverage > 0]
        report.avg_vocabulary_coverage = (
            sum(vocab_scores) / len(vocab_scores) if vocab_scores else 0.0
        )

        ratings = [m.user_explicit_rating for m in period_metrics if m.user_explicit_rating is not None]
        report.avg_user_rating = (
            sum(ratings) / len(ratings) / 5.0 if ratings else 0.0
        )

        engaged = [m for m in period_metrics if m.user_engaged_after]
        report.engagement_rate = len(engaged) / len(period_metrics)

        # Trend analysis
        report.score_trend, report.trend_magnitude = self._compute_trend(
            period_metrics
        )

        # Gap identification
        report.vocabulary_gaps = list(self._vocabulary_unknown.get(dialect, set()))[:20]

        # Correction pattern analysis
        patterns = self._correction_patterns.get(dialect, [])
        if patterns:
            from collections import Counter
            common = Counter(patterns).most_common(5)
            report.grammar_errors = [f"{p}: {c} occurrences" for p, c in common]

        # Recommendations
        self._generate_recommendations(report)

        # Store report
        self._reports[dialect].append(report)

        return report

    def generate_all_reports(self) -> Dict[str, DialectReport]:
        """Generate reports for all dialects with enough data."""
        reports = {}
        for dialect in self._metrics:
            report = self.generate_report(dialect)
            if report:
                reports[dialect] = report
        return reports

    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get dashboard-ready quality data across all dialects.

        Returns summary suitable for visualization.
        """
        dashboard = {
            "timestamp": time.time(),
            "dialects": {},
            "overall_health": "healthy",
            "critical_dialects": [],
            "improving_dialects": [],
        }

        for dialect, metrics in self._metrics.items():
            if len(metrics) < self.min_interactions_for_scoring:
                continue

            score = self.get_dialect_score(dialect)
            recent = [m for m in metrics if m.timestamp > time.time() - 86400]

            dialect_info = {
                "score": round(score, 3),
                "interactions_today": len(recent),
                "total_interactions": len(metrics),
                "correction_rate": round(
                    sum(1 for m in recent if m.was_corrected) / max(len(recent), 1),
                    3
                ),
            }

            dashboard["dialects"][dialect] = dialect_info

            if score < self.quality_threshold:
                dashboard["critical_dialects"].append(dialect)
                dashboard["overall_health"] = "needs_attention"
            elif score > 0.8:
                dashboard["improving_dialects"].append(dialect)

        return dashboard

    def _compute_trend(
        self, metrics: List[InteractionMetric]
    ) -> Tuple[str, float]:
        """Compute quality trend direction and magnitude."""
        if len(metrics) < 10:
            return "stable", 0.0

        # Split into halves
        mid = len(metrics) // 2
        first_half = metrics[:mid]
        second_half = metrics[mid:]

        avg_first = sum(m.composite_score for m in first_half) / len(first_half)
        avg_second = sum(m.composite_score for m in second_half) / len(second_half)

        diff = avg_second - avg_first

        if diff > 0.05:
            return "improving", diff
        elif diff < -0.05:
            return "degrading", diff
        else:
            return "stable", diff

    def _generate_recommendations(self, report: DialectReport) -> None:
        """Generate actionable recommendations based on report."""
        actions = []

        if report.correction_rate > 0.3:
            report.needs_retraining = True
            actions.append(
                f"High correction rate ({report.correction_rate:.1%}). "
                "Schedule priority retraining for this dialect."
            )

        if report.avg_composite_score < self.quality_threshold:
            report.needs_retraining = True
            actions.append(
                f"Quality score ({report.avg_composite_score:.2f}) below threshold "
                f"({self.quality_threshold}). Needs more training data."
            )

        if report.total_interactions < self.min_interactions_for_scoring * 2:
            report.needs_more_data = True
            actions.append(
                f"Only {report.total_interactions} interactions. "
                "Need more data for reliable quality assessment."
            )

        if report.vocabulary_gaps:
            actions.append(
                f"{len(report.vocabulary_gaps)} unknown vocabulary words detected. "
                "Update vocabulary and retrain."
            )

        if report.avg_dialect_authenticity < 0.5 and report.avg_dialect_authenticity > 0:
            actions.append(
                "Low dialect authenticity. Consider collecting more native speaker data."
            )

        if report.score_trend == "degrading":
            actions.append(
                f"Quality is degrading (change: {report.trend_magnitude:+.3f}). "
                "Investigate recent model updates or data distribution shifts."
            )

        report.recommended_actions = actions
