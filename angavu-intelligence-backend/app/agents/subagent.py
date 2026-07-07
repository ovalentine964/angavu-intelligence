"""
Sub-Agent Orchestrator — OpenClaw-style push-based sub-agent completion.

This module implements the parent/child sub-agent pattern from OpenClaw:
- Parent agent spawns isolated child agents
- Children work independently and push completion events back
- Parent processes results as they arrive (non-blocking)
- Timeout handling for stuck agents
- Parent-child relationship tracking

Pattern Source: OpenClaw Gateway — sessions_spawn / sessions_yield
Academic Basis: STA (Software Technology & Architecture) — multi-agent coordination

Architecture:
    ParentAgent
        ├── spawn(task_1) → ChildAgent_1 → push(completion) ──┐
        ├── spawn(task_2) → ChildAgent_2 → push(completion) ──┤
        └── spawn(task_3) → ChildAgent_3 → push(completion) ──┘
                                                              │
                                                     Parent processes
                                                     results as they arrive

For Angavu's 33-agent system, this enables the IntentRouter to fan out
complex queries to specialist agents in parallel, collecting results
as each agent finishes.

@author Angavu Intelligence — Impl Swarm 13 (Sub-Agent Orchestration)
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Coroutine, Dict, List, Optional

logger = logging.getLogger(__name__)


# ─── Data Models ────────────────────────────────────────────────────────


class AgentStatus(Enum):
    """Lifecycle status of a sub-agent."""
    PENDING = "pending"         # Created, not yet started
    RUNNING = "running"         # Actively executing
    COMPLETED = "completed"     # Finished successfully
    FAILED = "failed"           # Finished with error
    TIMED_OUT = "timed_out"     # Exceeded timeout
    CANCELLED = "cancelled"     # Cancelled by parent


@dataclass
class SubTask:
    """A discrete unit of work assigned to a sub-agent."""
    task_id: str
    description: str
    agent_type: str                   # e.g. "finance", "inventory", "market"
    priority: str = "normal"          # "low", "normal", "high", "urgent"
    context: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 300                # seconds
    depends_on: List[str] = field(default_factory=list)  # task_ids this depends on
    model_hint: Optional[str] = None  # "on_device", "cloud_light", "cloud_full"


@dataclass
class AgentResult:
    """
    Result pushed back by a completed sub-agent.

    This is the push-based completion event — the child writes this,
    the parent reads it.
    """
    agent_id: str
    task_id: str
    status: AgentStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: float = 0.0
    completed_at: float = 0.0
    model_used: Optional[str] = None
    cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration_seconds(self) -> float:
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return 0.0

    @property
    def success(self) -> bool:
        return self.status == AgentStatus.COMPLETED


@dataclass
class ChildAgent:
    """Tracks a spawned child agent's lifecycle."""
    agent_id: str
    task: SubTask
    status: AgentStatus = AgentStatus.PENDING
    result: Optional[AgentResult] = None
    spawned_at: float = field(default_factory=time.time)
    parent_id: Optional[str] = None
    _task_handle: Optional[asyncio.Task] = field(default=None, repr=False)


# ─── Agent Handler Registry ─────────────────────────────────────────────

# Type alias: an agent handler takes a SubTask and returns an AgentResult
AgentHandler = Callable[[SubTask], Coroutine[Any, Any, AgentResult]]


class AgentRegistry:
    """
    Registry mapping agent_type strings to handler coroutines.

    Each specialist agent (FinanceAgent, InventoryAgent, etc.) registers
    its handler here. The orchestrator dispatches sub-tasks by agent_type.

    Usage:
        registry = AgentRegistry()
        registry.register("finance", finance_agent_handler)
        registry.register("inventory", inventory_agent_handler)
    """

    def __init__(self):
        self._handlers: Dict[str, AgentHandler] = {}

    def register(self, agent_type: str, handler: AgentHandler) -> None:
        """Register a handler for an agent type."""
        self._handlers[agent_type] = handler
        logger.info(f"Registered agent handler: {agent_type}")

    def get(self, agent_type: str) -> Optional[AgentHandler]:
        """Get handler for an agent type, or None."""
        return self._handlers.get(agent_type)

    def has(self, agent_type: str) -> bool:
        return agent_type in self._handlers

    @property
    def registered_types(self) -> List[str]:
        return list(self._handlers.keys())


# ─── Sub-Agent Orchestrator ─────────────────────────────────────────────


class SubAgentOrchestrator:
    """
    OpenClaw-style sub-agent orchestrator.

    Parent spawns isolated children. Children push completion events
    back. Parent processes results as they arrive.

    Key features:
    - Push-based completion: children notify parent when done
    - Timeout handling: stuck agents are cancelled
    - Parent-child tracking: full lineage of agent spawns
    - Concurrent execution: multiple children run in parallel
    - Cost tracking: aggregate cost across all sub-agents

    Usage:
        registry = AgentRegistry()
        registry.register("finance", finance_handler)

        orchestrator = SubAgentOrchestrator(registry=registry)

        # Spawn children
        id1 = await orchestrator.spawn(SubTask(
            task_id="t1", description="Analyze cash flow",
            agent_type="finance", timeout=60
        ))
        id2 = await orchestrator.spawn(SubTask(
            task_id="t2", description="Check inventory",
            agent_type="inventory", timeout=30
        ))

        # Wait for all completions
        results = await orchestrator.wait_for_all()
    """

    def __init__(
        self,
        registry: Optional[AgentRegistry] = None,
        parent_id: Optional[str] = None,
        max_concurrent: int = 10,
        default_timeout: int = 300,
    ):
        self._registry = registry or AgentRegistry()
        self._parent_id = parent_id
        self._max_concurrent = max_concurrent
        self._default_timeout = default_timeout

        # Active children: agent_id → ChildAgent
        self._children: Dict[str, ChildAgent] = {}

        # Completion queue: push-based results arrive here
        self._completion_queue: asyncio.Queue[AgentResult] = asyncio.Queue()

        # Global completion callbacks (parent registers these)
        self._on_complete: List[Callable[[AgentResult], None]] = []

        # Semaphore for concurrency limiting
        self._semaphore = asyncio.Semaphore(max_concurrent)

        # Aggregate stats
        self._total_spawned = 0
        self._total_completed = 0
        self._total_failed = 0
        self._total_cost = 0.0

        logger.info(
            f"SubAgentOrchestrator initialized "
            f"(parent={parent_id}, max_concurrent={max_concurrent})"
        )

    # ─── Spawn ──────────────────────────────────────────────────────────

    async def spawn(self, task: SubTask) -> str:
        """
        Spawn an isolated sub-agent for the given task.

        Returns immediately with the agent_id. The child runs
        asynchronously and pushes its result to the completion queue.

        Args:
            task: The sub-task to execute

        Returns:
            agent_id: Unique identifier for the spawned child

        Raises:
            ValueError: If no handler registered for task.agent_type
        """
        handler = self._registry.get(task.agent_type)
        if handler is None:
            raise ValueError(
                f"No handler registered for agent_type='{task.agent_type}'. "
                f"Available: {self._registry.registered_types}"
            )

        agent_id = f"subagent:{uuid.uuid4().hex[:12]}"
        timeout = task.timeout or self._default_timeout

        child = ChildAgent(
            agent_id=agent_id,
            task=task,
            parent_id=self._parent_id,
        )
        self._children[agent_id] = child
        self._total_spawned += 1

        # Spawn the async task — runs independently
        child._task_handle = asyncio.create_task(
            self._run_child(child, handler, timeout)
        )

        logger.info(
            f"Spawned sub-agent {agent_id} for task '{task.description}' "
            f"(type={task.agent_type}, timeout={timeout}s)"
        )
        return agent_id

    async def spawn_many(self, tasks: List[SubTask]) -> List[str]:
        """Spawn multiple sub-agents. Returns list of agent_ids."""
        agent_ids = []
        for task in tasks:
            agent_id = await self.spawn(task)
            agent_ids.append(agent_id)
        return agent_ids

    # ─── Wait / Collect ─────────────────────────────────────────────────

    async def wait_for(self, agent_id: str) -> AgentResult:
        """
        Wait for a specific sub-agent to complete.

        Push-based: blocks until the child pushes its result.
        """
        child = self._children.get(agent_id)
        if child is None:
            return AgentResult(
                agent_id=agent_id,
                task_id="unknown",
                status=AgentStatus.FAILED,
                error=f"Unknown agent_id: {agent_id}",
            )

        if child.result is not None:
            return child.result

        # Wait on the child's task handle
        if child._task_handle is not None:
            await child._task_handle

        return child.result or AgentResult(
            agent_id=agent_id,
            task_id=child.task.task_id,
            status=AgentStatus.FAILED,
            error="No result produced",
        )

    async def wait_for_any(self) -> AgentResult:
        """
        Wait for the next sub-agent completion (push-based).

        Returns the first result that arrives from any child.
        """
        return await self._completion_queue.get()

    async def wait_for_all(self, timeout: Optional[int] = None) -> List[AgentResult]:
        """
        Wait for all spawned sub-agents to complete.

        Args:
            timeout: Max seconds to wait for all agents.
                     If None, waits indefinitely.

        Returns:
            List of AgentResult for all children.
        """
        if not self._children:
            return []

        # Wait for all child tasks
        tasks = [
            child._task_handle
            for child in self._children.values()
            if child._task_handle is not None
        ]

        if timeout:
            done, pending = await asyncio.wait(tasks, timeout=timeout)
            # Cancel any still-pending
            for t in pending:
                t.cancel()
        else:
            await asyncio.gather(*tasks, return_exceptions=True)

        return [
            child.result or AgentResult(
                agent_id=child.agent_id,
                task_id=child.task.task_id,
                status=AgentStatus.TIMED_OUT,
                error="No result produced",
            )
            for child in self._children.values()
        ]

    async def process_completions(
        self,
        callback: Callable[[AgentResult], Coroutine[Any, Any, None]],
    ) -> None:
        """
        Process completion events as they arrive (streaming mode).

        Calls the callback for each result as it arrives from any child.
        Returns when all children have completed.

        Usage:
            async def handle_result(result: AgentResult):
                print(f"Agent {result.agent_id} finished: {result.status}")

            await orchestrator.process_completions(handle_result)
        """
        remaining = len(self._children)
        while remaining > 0:
            result = await self._completion_queue.get()
            remaining -= 1
            try:
                await callback(result)
            except Exception as e:
                logger.error(f"Completion callback error: {e}")

    # ─── Cancellation ───────────────────────────────────────────────────

    async def cancel(self, agent_id: str) -> bool:
        """Cancel a running sub-agent."""
        child = self._children.get(agent_id)
        if child is None or child._task_handle is None:
            return False

        if child.status not in (AgentStatus.PENDING, AgentStatus.RUNNING):
            return False

        child._task_handle.cancel()
        child.status = AgentStatus.CANCELLED
        logger.info(f"Cancelled sub-agent {agent_id}")
        return True

    async def cancel_all(self) -> int:
        """Cancel all running sub-agents. Returns count cancelled."""
        count = 0
        for child in self._children.values():
            if await self.cancel(child.agent_id):
                count += 1
        return count

    # ─── Stats ──────────────────────────────────────────────────────────

    @property
    def active_count(self) -> int:
        return sum(
            1 for c in self._children.values()
            if c.status in (AgentStatus.PENDING, AgentStatus.RUNNING)
        )

    @property
    def total_cost(self) -> float:
        return self._total_cost

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_spawned": self._total_spawned,
            "total_completed": self._total_completed,
            "total_failed": self._total_failed,
            "active_count": self.active_count,
            "total_cost": self._total_cost,
            "children": {
                aid: {
                    "status": child.status.value,
                    "task": child.task.description,
                    "agent_type": child.task.agent_type,
                    "duration": child.result.duration_seconds if child.result else 0,
                }
                for aid, child in self._children.items()
            },
        }

    # ─── Internal ───────────────────────────────────────────────────────

    async def _run_child(
        self,
        child: ChildAgent,
        handler: AgentHandler,
        timeout: int,
    ) -> None:
        """
        Execute a child agent with timeout and push result to queue.

        This is the core of the push-based pattern:
        1. Acquire concurrency semaphore
        2. Run handler with timeout
        3. Wrap result in AgentResult
        4. Push to completion queue (parent receives it)
        5. Fire completion callbacks
        """
        async with self._semaphore:
            child.status = AgentStatus.RUNNING
            child.started_at = time.time()

            try:
                result = await asyncio.wait_for(
                    handler(child.task),
                    timeout=timeout,
                )
                child.status = AgentStatus.COMPLETED
                self._total_completed += 1

            except asyncio.TimeoutError:
                result = AgentResult(
                    agent_id=child.agent_id,
                    task_id=child.task.task_id,
                    status=AgentStatus.TIMED_OUT,
                    error=f"Sub-agent timed out after {timeout}s",
                    started_at=child.spawned_at,
                    completed_at=time.time(),
                )
                child.status = AgentStatus.TIMED_OUT
                self._total_failed += 1
                logger.warning(
                    f"Sub-agent {child.agent_id} timed out after {timeout}s"
                )

            except asyncio.CancelledError:
                result = AgentResult(
                    agent_id=child.agent_id,
                    task_id=child.task.task_id,
                    status=AgentStatus.CANCELLED,
                    error="Cancelled by parent",
                    started_at=child.spawned_at,
                    completed_at=time.time(),
                )
                child.status = AgentStatus.CANCELLED

            except Exception as e:
                result = AgentResult(
                    agent_id=child.agent_id,
                    task_id=child.task.task_id,
                    status=AgentStatus.FAILED,
                    error=str(e),
                    started_at=child.spawned_at,
                    completed_at=time.time(),
                )
                child.status = AgentStatus.FAILED
                self._total_failed += 1
                logger.error(f"Sub-agent {child.agent_id} failed: {e}")

            # Ensure result has timing info
            if result.started_at == 0.0:
                result.started_at = child.spawned_at
            if result.completed_at == 0.0:
                result.completed_at = time.time()

            # Track cost
            self._total_cost += result.cost

            # Store result on child
            child.result = result

            # PUSH completion event to queue (parent receives this)
            await self._completion_queue.put(result)

            # Fire registered callbacks
            for cb in self._on_complete:
                try:
                    cb(result)
                except Exception as e:
                    logger.error(f"Completion callback error: {e}")

            logger.info(
                f"Sub-agent {child.agent_id} finished: status={result.status.value} "
                f"duration={result.duration_seconds:.1f}s"
            )

    def on_complete(self, callback: Callable[[AgentResult], None]) -> None:
        """Register a callback for when any child completes."""
        self._on_complete.append(callback)
