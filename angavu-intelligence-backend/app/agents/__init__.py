"""
Intelligence agents for Angavu Intelligence.

Provides:
- IntelligencePipeline: Main orchestration for worker queries
- CausalReasoningEngine: Estimate treatment effects and detect confounders
- SubAgentOrchestrator: OpenClaw-style push-based sub-agent coordination
- TaskDecomposer: Break complex queries into sub-agent tasks
- AgentFactory: Wire up the full 33-agent system
"""

from .causal_reasoning import CausalReasoningEngine, TreatmentEffect, ConfounderResult
from .intelligence_pipeline import IntelligencePipeline, PipelineRequest, PipelineResponse
from .subagent import (
    SubAgentOrchestrator,
    AgentResult,
    AgentStatus,
    AgentRegistry,
    SubTask,
    ChildAgent,
)
from .task_decomposition import (
    TaskDecomposer,
    DecompositionPlan,
    TaskComplexity,
    ExecutionStrategy,
)
from .factory import AgentFactory, create_default_factory

__all__ = [
    # Causal reasoning
    "CausalReasoningEngine",
    "TreatmentEffect",
    "ConfounderResult",
    # Intelligence pipeline
    "IntelligencePipeline",
    "PipelineRequest",
    "PipelineResponse",
    # Sub-agent orchestration
    "SubAgentOrchestrator",
    "AgentResult",
    "AgentStatus",
    "AgentRegistry",
    "SubTask",
    "ChildAgent",
    # Task decomposition
    "TaskDecomposer",
    "DecompositionPlan",
    "TaskComplexity",
    "ExecutionStrategy",
    # Factory
    "AgentFactory",
    "create_default_factory",
]
