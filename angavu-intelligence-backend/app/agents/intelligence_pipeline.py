"""
Intelligence Pipeline — Core agent orchestration for Angavu Intelligence.

This module orchestrates the intelligence agents that serve Msaidizi workers.
It integrates:
- Financial analysis agents
- Causal reasoning (did Msaidizi actually help?)
- Model routing and cost management
- Human-in-the-loop decision making

Architecture:
    Worker Query → ModelRouter → Agent Pipeline → Response
                                     ↓
                              Causal Reasoning
                              (treatment effects,
                               confounder detection)
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

logger = logging.getLogger(__name__)


class PipelineStage(Enum):
    """Stages in the intelligence pipeline."""
    INTAKE = "intake"           # Parse and validate input
    ROUTING = "routing"         # Select model/agent
    ANALYSIS = "analysis"       # Run financial analysis
    CAUSAL = "causal"          # Causal reasoning (did Msaidizi help?)
    SYNTHESIS = "synthesis"     # Combine results
    DELIVERY = "delivery"       # Format and deliver response


@dataclass
class PipelineRequest:
    """A request through the intelligence pipeline."""
    request_id: str
    worker_id: str
    query: str
    context: dict[str, Any] = field(default_factory=dict)
    priority: str = "normal"  # "low", "normal", "high", "urgent"


@dataclass
class PipelineResponse:
    """A response from the intelligence pipeline."""
    request_id: str
    response: str
    confidence: float
    stage_results: dict[str, Any] = field(default_factory=dict)
    causal_analysis: Optional[dict] = None
    warnings: list[str] = field(default_factory=list)


class IntelligencePipeline:
    """
    Main intelligence pipeline for Angavu/Msaidizi.

    This orchestrates the full flow from worker query to response,
    including causal reasoning about Msaidizi's impact.

    Usage:
        pipeline = IntelligencePipeline()
        response = pipeline.process(request)
    """

    def __init__(
        self,
        enable_causal_reasoning: bool = True,
        max_cost_per_query: float = 0.001,  # $0.001 per query
    ):
        self._enable_causal = enable_causal_reasoning
        self._max_cost = max_cost_per_query
        self._causal_engine = None

        if enable_causal_reasoning:
            # Lazy import to avoid circular dependencies
            try:
                from .causal_reasoning import CausalReasoningEngine
                self._causal_engine = CausalReasoningEngine()
                logger.info("Causal reasoning engine initialized")
            except ImportError:
                logger.warning("Causal reasoning module not available")
                self._enable_causal = False

    def process(self, request: PipelineRequest) -> PipelineResponse:
        """
        Process a request through the full intelligence pipeline.

        Stages:
        1. INTAKE: Parse and validate the request
        2. ROUTING: Select the best model/agent
        3. ANALYSIS: Run financial analysis
        4. CAUSAL: Estimate treatment effects if relevant
        5. SYNTHESIS: Combine all results
        6. DELIVERY: Format the response
        """
        stage_results = {}
        warnings = []

        # Stage 1: INTAKE
        intake_result = self._stage_intake(request)
        stage_results[PipelineStage.INTAKE.value] = intake_result

        if not intake_result.get("valid", False):
            return PipelineResponse(
                request_id=request.request_id,
                response=intake_result.get("error", "Invalid request"),
                confidence=0.0,
                stage_results=stage_results,
                warnings=warnings,
            )

        # Stage 2: ROUTING
        routing_result = self._stage_routing(request, intake_result)
        stage_results[PipelineStage.ROUTING.value] = routing_result

        # Stage 3: ANALYSIS
        analysis_result = self._stage_analysis(request, routing_result)
        stage_results[PipelineStage.ANALYSIS.value] = analysis_result

        # Stage 4: CAUSAL REASONING
        causal_result = None
        if self._enable_causal and self._should_run_causal(request):
            causal_result = self._stage_causal(request, analysis_result)
            stage_results[PipelineStage.CAUSAL.value] = causal_result

            if causal_result and causal_result.get("warnings"):
                warnings.extend(causal_result["warnings"])

        # Stage 5: SYNTHESIS
        synthesis_result = self._stage_synthesis(
            request, analysis_result, causal_result
        )
        stage_results[PipelineStage.SYNTHESIS.value] = synthesis_result

        # Stage 6: DELIVERY
        delivery_result = self._stage_delivery(request, synthesis_result)
        stage_results[PipelineStage.DELIVERY.value] = delivery_result

        return PipelineResponse(
            request_id=request.request_id,
            response=delivery_result.get("response", ""),
            confidence=delivery_result.get("confidence", 0.0),
            stage_results=stage_results,
            causal_analysis=causal_result,
            warnings=warnings,
        )

    def _stage_intake(self, request: PipelineRequest) -> dict[str, Any]:
        """Parse and validate the incoming request."""
        if not request.query or not request.query.strip():
            return {"valid": False, "error": "Empty query"}

        if not request.worker_id:
            return {"valid": False, "error": "Missing worker_id"}

        return {
            "valid": True,
            "query_type": self._classify_query(request.query),
            "language": request.context.get("language", "en"),
        }

    def _stage_routing(
        self, request: PipelineRequest, intake: dict
    ) -> dict[str, Any]:
        """Select the best model and agent for this query."""
        query_type = intake.get("query_type", "general")

        # Map query types to agents
        agent_map = {
            "credit": "CreditScoringAgent",
            "cash_flow": "CashFlowForecastAgent",
            "market": "MarketAnalysisAgent",
            "tax": "TaxComplianceAgent",
            "formalization": "FormalizationAgent",
            "anomaly": "AnomalyDetectionAgent",
            "supplier": "SupplierMatchingAgent",
            "inventory": "InventoryOptimizationAgent",
            "health": "FinancialHealthAgent",
            "regulatory": "RegulatoryIntelligenceAgent",
            "general": "FinancialHealthAgent",
        }

        agent = agent_map.get(query_type, "FinancialHealthAgent")

        return {
            "selected_agent": agent,
            "query_type": query_type,
            "model": "on_device",  # Start with on-device for cost
            "estimated_cost": 0.0,
        }

    def _stage_analysis(
        self, request: PipelineRequest, routing: dict
    ) -> dict[str, Any]:
        """Run the selected agent's analysis."""
        agent_name = routing.get("selected_agent", "FinancialHealthAgent")

        # In production, this would invoke the actual agent
        # For now, return a structured placeholder
        return {
            "agent": agent_name,
            "analysis_type": routing.get("query_type", "general"),
            "result": f"Analysis from {agent_name} for worker {request.worker_id}",
            "metrics": {
                "revenue_trend": "increasing",
                "risk_level": "low",
                "recommendations": [],
            },
        }

    def _should_run_causal(self, request: PipelineRequest) -> bool:
        """
        Determine if causal reasoning is relevant for this request.

        Causal reasoning runs when:
        1. The query is about Msaidizi's impact or effectiveness
        2. The worker has enough historical data for comparison
        3. The query involves outcome evaluation
        """
        impact_keywords = [
            "impact", "effect", "improve", "better", "worse",
            "help", "benefit", "compare", "before", "after",
            "growth", "increase", "decrease", "change",
            "result", "outcome", "performance",
        ]
        query_lower = request.query.lower()
        return any(kw in query_lower for kw in impact_keywords)

    def _stage_causal(
        self, request: PipelineRequest, analysis: dict
    ) -> dict[str, Any]:
        """
        Run causal reasoning analysis.

        This answers: "Did Msaidizi actually improve this worker's business?"
        """
        if not self._causal_engine:
            return {"available": False, "reason": "Causal engine not initialized"}

        # In production, load worker's historical data here
        # For now, return the engine's capabilities
        engine = self._causal_engine

        result = {
            "available": True,
            "engine_status": "ready",
            "methods_available": [
                "difference_in_means",
                "regression_adjusted",
            ],
            "confounder_detection": True,
            "covariate_balance_check": True,
            "warning": (
                "Causal analysis requires historical data. "
                "No worker data loaded — showing engine capabilities only."
            ),
            "warnings": [
                "No historical data loaded for this worker. "
                "Causal estimates will be computed when data is available."
            ],
        }

        # If we had real data, we'd do:
        # engine.add_units(worker_data)
        # report = engine.generate_report()
        # result["report"] = report

        return result

    def _stage_synthesis(
        self,
        request: PipelineRequest,
        analysis: dict,
        causal: Optional[dict],
    ) -> dict[str, Any]:
        """Combine analysis results and causal reasoning into a coherent response."""
        synthesis = {
            "analysis_summary": analysis.get("result", ""),
            "metrics": analysis.get("metrics", {}),
            "has_causal_analysis": causal is not None and causal.get("available", False),
        }

        if causal and causal.get("available"):
            synthesis["causal_insight"] = (
                "Causal reasoning engine is active. "
                "When historical data is available, we can estimate whether "
                "Msaidizi's interventions caused measurable improvements in "
                "your business outcomes."
            )

        return synthesis

    def _stage_delivery(
        self, request: PipelineRequest, synthesis: dict
    ) -> dict[str, Any]:
        """Format the final response for delivery to the worker."""
        response_parts = []

        # Main analysis
        if synthesis.get("analysis_summary"):
            response_parts.append(synthesis["analysis_summary"])

        # Causal insight
        if synthesis.get("has_causal_analysis"):
            response_parts.append(synthesis.get("causal_insight", ""))

        response = "\n\n".join(response_parts) if response_parts else "I'm analyzing your request..."

        return {
            "response": response,
            "confidence": 0.8,
            "format": "text",
        }

    def _classify_query(self, query: str) -> str:
        """Classify the query type for routing."""
        query_lower = query.lower()

        keyword_map = {
            "credit": ["credit", "loan", "borrow", "lend", "debt", "mkopo"],
            "cash_flow": ["cash", "flow", "revenue", "income", "expense", "pesa"],
            "market": ["market", "price", "competitor", "demand", "soko"],
            "tax": ["tax", "kra", "vat", "return", "filing", "kodi"],
            "formalization": ["formal", "register", "license", "permit", "biashara"],
            "anomaly": ["fraud", "error", "unusual", "suspicious", "strange"],
            "supplier": ["supplier", "vendor", "source", "buy", "stockist"],
            "inventory": ["inventory", "stock", "reorder", "demand", "bidhaa"],
            "health": ["health", "report", "summary", "overview", "hali"],
            "regulatory": ["regulation", "compliance", "law", "rule", "sheria"],
        }

        for qtype, keywords in keyword_map.items():
            if any(kw in query_lower for kw in keywords):
                return qtype

        return "general"

    # ─── Causal Analysis API ────────────────────────────────────────────

    def get_causal_engine(self):
        """Get the causal reasoning engine for direct use."""
        return self._causal_engine

    def run_causal_analysis(self, worker_data: list) -> Optional[dict]:
        """
        Run a full causal analysis on worker data.

        Args:
            worker_data: List of Unit objects with treatment, outcome, covariates

        Returns:
            Causal analysis report dict, or None if causal reasoning is disabled
        """
        if not self._causal_engine:
            logger.warning("Causal reasoning engine not available")
            return None

        from .causal_reasoning import Unit, TreatmentStatus

        # Convert raw data to Unit objects if needed
        units = []
        for item in worker_data:
            if isinstance(item, Unit):
                units.append(item)
            elif isinstance(item, dict):
                units.append(Unit(
                    unit_id=item.get("unit_id", "unknown"),
                    treatment=(
                        TreatmentStatus.TREATED
                        if item.get("treated", False)
                        else TreatmentStatus.CONTROL
                    ),
                    outcome=item.get("outcome", 0.0),
                    covariates=item.get("covariates", {}),
                    timestamp=item.get("timestamp"),
                ))

        self._causal_engine.clear()
        self._causal_engine.add_units(units)

        return self._causal_engine.generate_report()
