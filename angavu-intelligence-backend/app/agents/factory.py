"""
Agent Factory — Wire up Angavu's 33-agent system with sub-agent orchestration.

This module creates and configures the full agent runtime:
- AgentRegistry with all specialist handlers
- SubAgentOrchestrator for parent/child coordination
- TaskDecomposer for query decomposition
- Integration with IntelligencePipeline

Usage:
    factory = AgentFactory()
    result = await factory.handle_query(
        query="How is my business? Should I restock?",
        worker_id="worker_123",
        context={"language": "sw", "business_type": "mama_mboga"}
    )

@author Angavu Intelligence — Impl Swarm 13 (Sub-Agent Orchestration)
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

from .subagent import (
    AgentRegistry,
    AgentResult,
    AgentStatus,
    SubAgentOrchestrator,
    SubTask,
)
from .task_decomposition import (
    DecompositionPlan,
    ExecutionStrategy,
    TaskDecomposer,
)
from .intelligence_pipeline import IntelligencePipeline, PipelineRequest

logger = logging.getLogger(__name__)


# ─── Default Agent Handlers ─────────────────────────────────────────────
# These are placeholder handlers. In production, each handler would
# invoke the actual specialist agent (LLM call, on-device model, etc.)


async def _default_agent_handler(task: SubTask) -> AgentResult:
    """
    Default handler that simulates agent execution.

    In production, replace with actual agent implementations:
    - FinanceAgent: calls financial analysis model
    - InventoryAgent: queries stock database + demand model
    - MarketAgent: fetches market prices + trend analysis
    - etc.
    """
    start = time.time()

    # Simulate processing time based on agent type
    latency_map = {
        "finance": 0.1,
        "credit": 0.15,
        "inventory": 0.08,
        "market": 0.12,
        "tax": 0.1,
        "formalization": 0.05,
        "anomaly": 0.2,
        "supplier": 0.1,
        "health": 0.05,
        "regulatory": 0.08,
        "forecast": 0.15,
        "savings": 0.08,
    }
    latency = latency_map.get(task.agent_type, 0.1)
    await asyncio.sleep(latency)

    return AgentResult(
        agent_id=f"handler_{task.agent_type}",
        task_id=task.task_id,
        status=AgentStatus.COMPLETED,
        result={
            "agent_type": task.agent_type,
            "analysis": f"[{task.agent_type}] Analysis for: {task.description[:100]}",
            "query": task.context.get("query", ""),
            "relevance": task.context.get("relevance_score", 0.0),
        },
        started_at=start,
        completed_at=time.time(),
        model_used=task.model_hint or "on_device",
        cost=0.0001,
    )


# ─── Agent Factory ──────────────────────────────────────────────────────


class AgentFactory:
    """
    Factory that wires up the full agent system.

    Creates:
    - AgentRegistry with all 33 agent handlers
    - SubAgentOrchestrator for spawning and coordinating children
    - TaskDecomposer for breaking queries into sub-tasks
    - Integration with IntelligencePipeline for single-agent queries

    This is the main entry point for the sub-agent orchestration system.
    """

    def __init__(
        self,
        enable_causal: bool = True,
        max_concurrent: int = 10,
        default_timeout: int = 300,
    ):
        # Create registry and register all agent handlers
        self._registry = AgentRegistry()
        self._register_default_handlers()

        # Create decomposer
        self._decomposer = TaskDecomposer()

        # Create pipeline for single-agent queries
        self._pipeline = IntelligencePipeline(
            enable_causal_reasoning=enable_causal,
        )

        # Orchestrator config (created per-query for isolation)
        self._max_concurrent = max_concurrent
        self._default_timeout = default_timeout

        # Stats
        self._query_count = 0
        self._total_cost = 0.0

        logger.info(
            f"AgentFactory initialized with {len(self._registry.registered_types)} "
            f"agent handlers"
        )

    def _register_default_handlers(self) -> None:
        """Register default handlers for all known agent types."""
        agent_types = [
            "finance", "credit", "inventory", "market", "tax",
            "formalization", "anomaly", "supplier", "health",
            "regulatory", "forecast", "savings",
        ]
        for agent_type in agent_types:
            self._registry.register(agent_type, _default_agent_handler)

    def register_handler(self, agent_type: str, handler) -> None:
        """Register a custom handler for an agent type (override default)."""
        self._registry.register(agent_type, handler)

    @property
    def registry(self) -> AgentRegistry:
        return self._registry

    @property
    def decomposer(self) -> TaskDecomposer:
        return self._decomposer

    # ─── Main Query Handler ─────────────────────────────────────────────

    async def handle_query(
        self,
        query: str,
        worker_id: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Handle a worker query through the full agent system.

        Flow:
        1. Decompose query into sub-tasks
        2. If simple (single agent) → use IntelligencePipeline directly
        3. If complex (multiple agents) → spawn sub-agents via orchestrator
        4. Collect results and merge into unified response

        Args:
            query: Worker's query text
            worker_id: Worker identifier
            context: Optional context (language, business_type, etc.)

        Returns:
            Merged response dict with all agent results
        """
        self._query_count += 1
        start = time.time()

        # Step 1: Decompose
        plan = self._decomposer.decompose(query, context)

        # Step 2: Simple query → single agent pipeline
        if plan.complexity.value == "trivial":
            return await self._handle_simple(query, worker_id, context, plan)

        # Step 3: Complex query → sub-agent orchestration
        return await self._handle_parallel(query, worker_id, context, plan)

    async def _handle_simple(
        self,
        query: str,
        worker_id: str,
        context: Optional[Dict[str, Any]],
        plan: DecompositionPlan,
    ) -> Dict[str, Any]:
        """Handle a simple single-agent query."""
        pipeline_request = PipelineRequest(
            request_id=f"req_{self._query_count}",
            worker_id=worker_id,
            query=query,
            context=context or {},
        )

        pipeline_response = self._pipeline.process(pipeline_request)

        return {
            "query": query,
            "worker_id": worker_id,
            "mode": "single_agent",
            "agent": plan.sub_tasks[0].agent_type if plan.sub_tasks else "health",
            "response": pipeline_response.response,
            "confidence": pipeline_response.confidence,
            "cost": 0.0001,
            "duration_ms": 100,
            "plan": {
                "plan_id": plan.plan_id,
                "complexity": plan.complexity.value,
                "strategy": plan.strategy.value,
            },
        }

    async def _handle_parallel(
        self,
        query: str,
        worker_id: str,
        context: Optional[Dict[str, Any]],
        plan: DecompositionPlan,
    ) -> Dict[str, Any]:
        """
        Handle a complex multi-agent query using sub-agent orchestration.

        Spawns sub-agents according to the decomposition plan's strategy,
        collects results, and merges into a unified response.
        """
        start = time.time()

        # Create orchestrator for this query
        orchestrator = SubAgentOrchestrator(
            registry=self._registry,
            parent_id=f"factory_{self._query_count}",
            max_concurrent=self._max_concurrent,
            default_timeout=self._default_timeout,
        )

        # Execute based on strategy
        if plan.strategy == ExecutionStrategy.PARALLEL:
            results = await self._execute_parallel(orchestrator, plan)
        elif plan.strategy == ExecutionStrategy.SEQUENTIAL:
            results = await self._execute_sequential(orchestrator, plan)
        else:  # MIXED
            results = await self._execute_mixed(orchestrator, plan)

        duration_ms = int((time.time() - start) * 1000)
        total_cost = sum(r.cost for r in results)
        self._total_cost += total_cost

        # Merge results
        merged = self._merge_results(results, plan)

        return {
            "query": query,
            "worker_id": worker_id,
            "mode": "multi_agent",
            "response": merged["response"],
            "confidence": merged["confidence"],
            "agent_results": merged["agent_results"],
            "cost": total_cost,
            "duration_ms": duration_ms,
            "agents_used": len(results),
            "plan": {
                "plan_id": plan.plan_id,
                "complexity": plan.complexity.value,
                "strategy": plan.strategy.value,
                "reasoning": plan.reasoning,
            },
            "orchestrator_stats": orchestrator.get_stats(),
        }

    async def _execute_parallel(
        self,
        orchestrator: SubAgentOrchestrator,
        plan: DecompositionPlan,
    ) -> List[AgentResult]:
        """Execute all sub-tasks in parallel."""
        await orchestrator.spawn_many(plan.sub_tasks)
        return await orchestrator.wait_for_all(timeout=self._default_timeout)

    async def _execute_sequential(
        self,
        orchestrator: SubAgentOrchestrator,
        plan: DecompositionPlan,
    ) -> List[AgentResult]:
        """Execute sub-tasks sequentially (respecting dependencies)."""
        results = []
        for task in plan.sub_tasks:
            agent_id = await orchestrator.spawn(task)
            result = await orchestrator.wait_for(agent_id)
            results.append(result)

            # If a dependency failed, skip dependent tasks
            if not result.success:
                for remaining in plan.sub_tasks:
                    if task.task_id in remaining.depends_on:
                        results.append(AgentResult(
                            agent_id=f"skipped_{remaining.agent_type}",
                            task_id=remaining.task_id,
                            status=AgentStatus.CANCELLED,
                            error=f"Dependency {task.task_id} failed",
                        ))
        return results

    async def _execute_mixed(
        self,
        orchestrator: SubAgentOrchestrator,
        plan: DecompositionPlan,
    ) -> List[AgentResult]:
        """
        Execute mixed strategy: parallel group first, then sequential chain.

        1. Spawn all independent tasks in parallel
        2. Wait for them to complete
        3. Spawn dependent tasks sequentially (they may need results from step 2)
        """
        all_results = []

        # Phase 1: Parallel group (no dependencies)
        parallel_tasks = [
            t for t in plan.sub_tasks if not t.depends_on
        ]
        if parallel_tasks:
            await orchestrator.spawn_many(parallel_tasks)
            parallel_results = await orchestrator.wait_for_all(
                timeout=self._default_timeout
            )
            all_results.extend(parallel_results)

        # Phase 2: Sequential chain (dependent tasks)
        sequential_tasks = [
            t for t in plan.sub_tasks if t.depends_on
        ]
        for task in sequential_tasks:
            # Check if dependencies succeeded
            dep_results = {
                r.task_id: r for r in all_results
                if r.task_id in task.depends_on
            }
            all_deps_ok = all(r.success for r in dep_results.values())

            if not all_deps_ok:
                all_results.append(AgentResult(
                    agent_id=f"skipped_{task.agent_type}",
                    task_id=task.task_id,
                    status=AgentStatus.CANCELLED,
                    error="Dependency failed",
                ))
                continue

            # Inject dependency results into task context
            task.context["dependency_results"] = {
                tid: r.result for tid, r in dep_results.items()
            }

            agent_id = await orchestrator.spawn(task)
            result = await orchestrator.wait_for(agent_id)
            all_results.append(result)

        return all_results

    # ─── Result Merging ─────────────────────────────────────────────────

    def _merge_results(
        self,
        results: List[AgentResult],
        plan: DecompositionPlan,
    ) -> Dict[str, Any]:
        """
        Merge multiple agent results into a unified response.

        Combines insights from all specialist agents into a coherent
        response for the worker.
        """
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        # Build agent-specific results
        agent_results = {}
        for r in results:
            agent_results[r.task_id] = {
                "agent_type": next(
                    (t.agent_type for t in plan.sub_tasks if t.task_id == r.task_id),
                    "unknown"
                ),
                "status": r.status.value,
                "result": r.result,
                "error": r.error,
                "duration_ms": int(r.duration_seconds * 1000),
                "cost": r.cost,
            }

        # Build merged response text
        response_parts = []
        for r in successful:
            if r.result and isinstance(r.result, dict):
                analysis = r.result.get("analysis", "")
                if analysis:
                    response_parts.append(analysis)

        # Calculate confidence based on success rate
        success_rate = len(successful) / len(results) if results else 0
        confidence = success_rate * 0.9  # Max 0.9 for multi-agent

        merged_response = "\n\n".join(response_parts) if response_parts else (
            "I analyzed your request from multiple angles. "
            f"{len(successful)} of {len(results)} analyses completed successfully."
        )

        if failed:
            failed_types = [
                agent_results[r.task_id]["agent_type"]
                for r in failed
            ]
            merged_response += (
                f"\n\nNote: {', '.join(failed_types)} analysis "
                f"{'was unavailable' if len(failed) == 1 else 'were unavailable'}."
            )

        return {
            "response": merged_response,
            "confidence": confidence,
            "agent_results": agent_results,
        }

    # ─── Stats ──────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_queries": self._query_count,
            "total_cost": self._total_cost,
            "registered_agents": len(self._registry.registered_types),
            "agent_types": self._registry.registered_types,
        }


# ─── Convenience Constructor ────────────────────────────────────────────


def create_default_factory(**kwargs) -> AgentFactory:
    """Create an AgentFactory with default configuration."""
    return AgentFactory(**kwargs)
