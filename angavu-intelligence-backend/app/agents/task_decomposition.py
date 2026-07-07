"""
Task Decomposer — Break complex queries into sub-agent tasks.

This module decomposes a worker's complex query into discrete sub-tasks
that can be dispatched to specialist agents in parallel or sequence.

Pattern: IntentRouter identifies need → TaskDecomposer breaks it down →
         SubAgentOrchestrator spawns children → results collected and merged.

Academic Basis: ECO 321 (Mechanism Design) — optimal task allocation
across agents with heterogeneous capabilities and costs.

For Angavu's informal economy context:
- A mama mboga asking "How is my business doing?" triggers:
  finance (cash flow analysis) + inventory (stock check) + market (price trends)
- A boda rider asking "Should I buy a new bike?" triggers:
  finance (affordability) + market (bike prices) + health (revenue forecast)
- These can run in PARALLEL since they're independent analyses

@author Angavu Intelligence — Impl Swarm 13 (Sub-Agent Orchestration)
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from .subagent import SubTask

logger = logging.getLogger(__name__)


# ─── Task Complexity Classification ─────────────────────────────────────


class TaskComplexity(Enum):
    """How complex is the decomposed task?"""
    TRIVIAL = "trivial"       # Single agent, no decomposition needed
    SIMPLE = "simple"         # 2-3 agents, parallel
    MODERATE = "moderate"     # 3-5 agents, some dependencies
    COMPLEX = "complex"       # 5+ agents, mixed parallel/sequential


class ExecutionStrategy(Enum):
    """How should sub-tasks be executed?"""
    PARALLEL = "parallel"         # All independent, run simultaneously
    SEQUENTIAL = "sequential"     # Dependencies, run in order
    MIXED = "mixed"              # Some parallel, some sequential


@dataclass
class DecompositionPlan:
    """Result of decomposing a complex task."""
    plan_id: str
    original_query: str
    complexity: TaskComplexity
    strategy: ExecutionStrategy
    sub_tasks: List[SubTask]
    parallel_groups: List[List[str]]   # Groups of task_ids that can run in parallel
    sequential_chain: List[str]        # Ordered task_ids for sequential execution
    estimated_cost: float = 0.0
    reasoning: str = ""


# ─── Agent Capability Map ───────────────────────────────────────────────
# Maps agent types to what they can handle, their typical cost, and speed.


@dataclass
class AgentCapability:
    """Describes what an agent type can do and its cost profile."""
    agent_type: str
    description: str
    keywords: List[str]           # Query keywords that trigger this agent
    typical_cost: float = 0.0     # Estimated cost in USD
    typical_latency_ms: int = 500 # Expected response time
    can_parallel: bool = True     # Can run alongside other agents?
    model_hint: str = "on_device" # Default model to use


# Default capability map for Angavu's 33-agent system
DEFAULT_CAPABILITIES: Dict[str, AgentCapability] = {
    "finance": AgentCapability(
        agent_type="finance",
        description="Cash flow, revenue, expenses, profit analysis",
        keywords=["cash", "flow", "revenue", "income", "expense", "profit",
                  "pesa", "mapato", "gharama", "faida", "money", "pesa"],
        typical_cost=0.0003,
        typical_latency_ms=800,
    ),
    "credit": AgentCapability(
        agent_type="credit",
        description="Credit scoring, loan eligibility, debt management",
        keywords=["credit", "loan", "borrow", "lend", "debt", "mkopo",
                  "deni", "score", "eligibility"],
        typical_cost=0.0005,
        typical_latency_ms=1200,
        model_hint="cloud_light",
    ),
    "inventory": AgentCapability(
        agent_type="inventory",
        description="Stock levels, reorder points, demand forecasting",
        keywords=["inventory", "stock", "reorder", "demand", "bidhaa",
                  "hifadhi", "存货", "level"],
        typical_cost=0.0002,
        typical_latency_ms=600,
    ),
    "market": AgentCapability(
        agent_type="market",
        description="Market prices, competitor analysis, demand trends",
        keywords=["market", "price", "competitor", "demand", "soko",
                  "bei", "ushindani", "trend"],
        typical_cost=0.0004,
        typical_latency_ms=1000,
        model_hint="cloud_light",
    ),
    "tax": AgentCapability(
        agent_type="tax",
        description="Tax compliance, KRA filing, VAT management",
        keywords=["tax", "kra", "vat", "return", "filing", "kodi",
                  "tozo", "compliance"],
        typical_cost=0.0003,
        typical_latency_ms=700,
    ),
    "formalization": AgentCapability(
        agent_type="formalization",
        description="Business registration, licensing, permits",
        keywords=["formal", "register", "license", "permit", "biashara",
                  "usajili", "leseni"],
        typical_cost=0.0002,
        typical_latency_ms=500,
    ),
    "anomaly": AgentCapability(
        agent_type="anomaly",
        description="Fraud detection, error identification, unusual patterns",
        keywords=["fraud", "error", "unusual", "suspicious", "strange",
                  "udanganyifu", "kosa"],
        typical_cost=0.0006,
        typical_latency_ms=1500,
        model_hint="cloud_light",
    ),
    "supplier": AgentCapability(
        agent_type="supplier",
        description="Supplier matching, vendor comparison, sourcing",
        keywords=["supplier", "vendor", "source", "buy", "stockist",
                  "muuzaji", "chanzo"],
        typical_cost=0.0003,
        typical_latency_ms=900,
    ),
    "health": AgentCapability(
        agent_type="health",
        description="Overall financial health, business overview, reports",
        keywords=["health", "report", "summary", "overview", "hali",
                  "ripoti", "jumla"],
        typical_cost=0.0002,
        typical_latency_ms=400,
    ),
    "regulatory": AgentCapability(
        agent_type="regulatory",
        description="Regulatory compliance, legal requirements, policy changes",
        keywords=["regulation", "compliance", "law", "rule", "sheria",
                  "kanuni", "taratibu"],
        typical_cost=0.0003,
        typical_latency_ms=800,
    ),
    "forecast": AgentCapability(
        agent_type="forecast",
        description="Revenue forecasting, seasonal predictions, growth projections",
        keywords=["forecast", "predict", "future", "projection", "growth",
                  "utaratibu", "mbinu"],
        typical_cost=0.0005,
        typical_latency_ms=1200,
        model_hint="cloud_light",
    ),
    "savings": AgentCapability(
        agent_type="savings",
        description="Savings goals, investment advice, financial planning",
        keywords=["save", "savings", "invest", "goal", "akiba",
                  "wekeza", "mpango"],
        typical_cost=0.0003,
        typical_latency_ms=700,
    ),
}


# ─── Task Decomposer ────────────────────────────────────────────────────


class TaskDecomposer:
    """
    Decompose complex worker queries into sub-agent tasks.

    The decomposer analyzes a query, identifies which specialist agents
    are needed, determines execution order (parallel vs sequential),
    and produces a DecompositionPlan.

    Academic basis: ECO 321 (Mechanism Design) — optimal task allocation
    across agents with heterogeneous capabilities.

    Usage:
        decomposer = TaskDecomposer()
        plan = decomposer.decompose(
            query="How is my business doing? Should I restock tomatoes?",
            worker_context={"language": "sw", "business_type": "mama_mboga"}
        )

        # plan.sub_tasks has the tasks to dispatch
        # plan.strategy tells the orchestrator how to run them
    """

    def __init__(
        self,
        capabilities: Optional[Dict[str, AgentCapability]] = None,
    ):
        self._capabilities = capabilities or DEFAULT_CAPABILITIES

    def decompose(
        self,
        query: str,
        worker_context: Optional[Dict[str, Any]] = None,
    ) -> DecompositionPlan:
        """
        Break a complex query into sub-agent tasks.

        Steps:
        1. Identify which agents are needed (keyword matching)
        2. Determine dependencies between agents
        3. Choose execution strategy (parallel/sequential/mixed)
        4. Estimate cost
        5. Build sub-tasks

        Args:
            query: The worker's query
            worker_context: Optional context (language, business_type, etc.)

        Returns:
            DecompositionPlan with sub-tasks and execution strategy
        """
        context = worker_context or {}
        query_lower = query.lower()

        # Step 1: Identify needed agents
        matched_agents = self._match_agents(query_lower)

        # If no agents matched, default to health (overview)
        if not matched_agents:
            matched_agents = [("health", 1.0)]

        # Step 2: Determine complexity
        n_agents = len(matched_agents)
        complexity = self._classify_complexity(n_agents, matched_agents)

        # Step 3: Build sub-tasks
        sub_tasks = []
        for agent_type, relevance in matched_agents:
            task_id = f"task_{agent_type}_{uuid.uuid4().hex[:6]}"
            capability = self._capabilities[agent_type]

            sub_task = SubTask(
                task_id=task_id,
                description=f"{capability.description} for query: {query[:80]}",
                agent_type=agent_type,
                priority=self._estimate_priority(query_lower, agent_type),
                context={
                    "query": query,
                    "relevance_score": relevance,
                    "worker_context": context,
                },
                timeout=300,
                model_hint=capability.model_hint,
            )
            sub_tasks.append(sub_task)

        # Step 4: Determine execution strategy
        strategy, parallel_groups, sequential_chain = self._plan_execution(
            sub_tasks, matched_agents
        )

        # Step 5: Estimate cost
        estimated_cost = sum(
            self._capabilities.get(st.agent_type, AgentCapability(
                agent_type=st.agent_type, description="", keywords=[]
            )).typical_cost
            for st in sub_tasks
        )

        plan = DecompositionPlan(
            plan_id=f"plan_{uuid.uuid4().hex[:8]}",
            original_query=query,
            complexity=complexity,
            strategy=strategy,
            sub_tasks=sub_tasks,
            parallel_groups=parallel_groups,
            sequential_chain=sequential_chain,
            estimated_cost=estimated_cost,
            reasoning=self._explain_plan(matched_agents, strategy, complexity),
        )

        logger.info(
            f"Decomposed query into {len(sub_tasks)} sub-tasks "
            f"(complexity={complexity.value}, strategy={strategy.value}, "
            f"est_cost=${estimated_cost:.4f})"
        )

        return plan

    # ─── Agent Matching ─────────────────────────────────────────────────

    def _match_agents(self, query_lower: str) -> List[Tuple[str, float]]:
        """
        Match query keywords to agent capabilities.

        Returns list of (agent_type, relevance_score) sorted by relevance.
        """
        scores: Dict[str, float] = {}

        for agent_type, cap in self._capabilities.items():
            score = 0.0
            matched_keywords = []
            for kw in cap.keywords:
                if kw in query_lower:
                    score += 1.0
                    matched_keywords.append(kw)

            if score > 0:
                # Normalize by number of keywords (prevents bias toward
                # agents with many keywords)
                normalized = score / len(cap.keywords)
                # Boost for multiple keyword matches
                boosted = normalized * (1 + 0.3 * (len(matched_keywords) - 1))
                scores[agent_type] = min(boosted, 1.0)

        # Sort by relevance descending
        sorted_agents = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Return top agents (cap at 6 to avoid over-decomposition)
        return sorted_agents[:6]

    def _classify_complexity(
        self,
        n_agents: int,
        matched: List[Tuple[str, float]],
    ) -> TaskComplexity:
        """Classify task complexity based on agent count and types."""
        if n_agents <= 1:
            return TaskComplexity.TRIVIAL
        elif n_agents <= 3:
            return TaskComplexity.SIMPLE
        elif n_agents <= 5:
            return TaskComplexity.MODERATE
        else:
            return TaskComplexity.COMPLEX

    # ─── Execution Planning ─────────────────────────────────────────────

    def _plan_execution(
        self,
        sub_tasks: List[SubTask],
        matched: List[Tuple[str, float]],
    ) -> Tuple[ExecutionStrategy, List[List[str]], List[str]]:
        """
        Determine execution strategy: parallel, sequential, or mixed.

        Rules:
        - Most financial analysis tasks are independent → parallel
        - Credit scoring depends on cash flow analysis → sequential
        - Forecast depends on historical data from finance → sequential
        - Market analysis and inventory are independent → parallel
        """
        task_ids = [st.task_id for st in sub_tasks]
        agent_types = {st.task_id: st.agent_type for st in sub_tasks}

        # Define dependency rules
        # key: agent_type that depends on → value: list of agent_types it needs first
        dependencies = {
            "credit": ["finance"],      # Credit needs cash flow data
            "forecast": ["finance"],    # Forecast needs revenue history
            "anomaly": ["finance"],     # Anomaly detection needs transaction data
            "savings": ["finance"],     # Savings advice needs income data
        }

        # Check if any dependencies exist
        has_deps = False
        for task in sub_tasks:
            deps = dependencies.get(task.agent_type, [])
            for dep_type in deps:
                for other_task in sub_tasks:
                    if other_task.agent_type == dep_type and other_task.task_id != task.task_id:
                        task.depends_on.append(other_task.task_id)
                        has_deps = True

        if not has_deps:
            # All independent — parallel execution
            return (
                ExecutionStrategy.PARALLEL,
                [task_ids],  # One group = all parallel
                [],
            )

        # Has dependencies — determine mixed execution
        # Build parallel groups: tasks with no deps run first, then dependent tasks
        no_deps = [t for t in sub_tasks if not t.depends_on]
        has_deps_list = [t for t in sub_tasks if t.depends_on]

        parallel_groups = []
        sequential_chain = []

        if no_deps:
            parallel_groups.append([t.task_id for t in no_deps])

        # Order dependent tasks by dependency depth
        for task in has_deps_list:
            sequential_chain.append(task.task_id)

        if no_deps and has_deps_list:
            return ExecutionStrategy.MIXED, parallel_groups, sequential_chain
        elif has_deps_list:
            return ExecutionStrategy.SEQUENTIAL, [], task_ids
        else:
            return ExecutionStrategy.PARALLEL, [task_ids], []

    # ─── Helpers ────────────────────────────────────────────────────────

    def _estimate_priority(self, query_lower: str, agent_type: str) -> str:
        """Estimate task priority based on query urgency and agent type."""
        urgent_keywords = ["urgent", "emergency", "now", "immediately", "haraka"]
        high_keywords = ["important", "asap", "quickly", "soon", "haraka"]

        if any(kw in query_lower for kw in urgent_keywords):
            return "urgent"
        if any(kw in query_lower for kw in high_keywords):
            return "high"
        if agent_type == "anomaly":
            return "high"  # Anomaly detection is always high priority
        return "normal"

    def _explain_plan(
        self,
        matched: List[Tuple[str, float]],
        strategy: ExecutionStrategy,
        complexity: TaskComplexity,
    ) -> str:
        """Generate human-readable explanation of the decomposition plan."""
        agents = [f"{m[0]} (relevance={m[1]:.2f})" for m in matched]
        return (
            f"Identified {len(matched)} relevant agents: {', '.join(agents)}. "
            f"Complexity: {complexity.value}. "
            f"Execution: {strategy.value}. "
            f"{'All tasks run in parallel — no dependencies.' if strategy == ExecutionStrategy.PARALLEL else ''}"
            f"{'Some tasks have dependencies — parallel first, then sequential.' if strategy == ExecutionStrategy.MIXED else ''}"
            f"{'Sequential execution required — tasks depend on each other.' if strategy == ExecutionStrategy.SEQUENTIAL else ''}"
        )

    # ─── Single-Agent Shortcut ──────────────────────────────────────────

    def is_simple_query(self, query: str) -> bool:
        """
        Check if this query can be handled by a single agent (no decomposition).

        Simple queries: "What's my balance?", "How much tax do I owe?"
        Complex queries: "How is my business? Should I restock? What about prices?"
        """
        query_lower = query.lower()
        matched = self._match_agents(query_lower)
        return len(matched) <= 1

    def get_primary_agent(self, query: str) -> str:
        """
        Get the single best agent for a simple query.

        Returns the agent_type with the highest relevance score.
        """
        query_lower = query.lower()
        matched = self._match_agents(query_lower)
        if matched:
            return matched[0][0]
        return "health"  # Default fallback
