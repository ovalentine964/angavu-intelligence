"""
Plan-and-Execute Pattern for Angavu Intelligence.

WHY: Complex tasks (like loan applications, market stall setup, or
supplier negotiations) need multi-step planning before execution.
A single-shot approach fails on multi-step workflows because it can't
adapt when intermediate steps fail or produce unexpected results.

HOW: Plan → Execute → Observe → Replan loop.
1. Planner breaks the task into ordered steps
2. Executor runs each step sequentially
3. Observer checks if results match expectations
4. Replanner adjusts the plan based on observed results

WHERE: angavu-intelligence-backend/app/agents/loops/plan_execute.py

Pattern borrowed from: LangGraph Plan-and-Execute + ORPA loop (XMPro)
Alignment: NIST AI RMF — predictable, auditable agent behavior
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ── Plan Step States ─────────────────────────────────────────


class StepStatus(str, Enum):
    """Lifecycle states for a plan step."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    REPLANNED = "replanned"


class PlanStatus(str, Enum):
    """Lifecycle states for an overall plan."""
    CREATED = "created"
    EXECUTING = "executing"
    REPLANNING = "replanning"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ── Data Structures ──────────────────────────────────────────


@dataclass
class PlanStep:
    """
    A single step in a plan.

    Each step has a clear description, the tool/action to execute,
    expected outcome, and a status tracker. Steps are ordered and
    executed sequentially (with possible replanning between steps).
    """
    step_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str = ""
    action: str = ""  # Tool name or action type
    parameters: dict[str, Any] = field(default_factory=dict)
    expected_outcome: str = ""
    status: StepStatus = StepStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retries: int = 0
    max_retries: int = 2

    def mark_in_progress(self) -> None:
        self.status = StepStatus.IN_PROGRESS
        self.started_at = datetime.utcnow()

    def mark_completed(self, result: Any) -> None:
        self.status = StepStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.utcnow()

    def mark_failed(self, error: str) -> None:
        self.status = StepStatus.FAILED
        self.error = error
        self.completed_at = datetime.utcnow()

    def can_retry(self) -> bool:
        return self.retries < self.max_retries

    @property
    def duration_seconds(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


@dataclass
class ExecutionPlan:
    """
    A complete execution plan with ordered steps.

    The plan is the output of the Planner. It contains all the steps
    needed to accomplish the task, along with metadata for tracking
    and auditing (NIST AI RMF compliance).
    """
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    task_description: str = ""
    steps: list[PlanStep] = field(default_factory=list)
    status: PlanStatus = PlanStatus.CREATED
    current_step_index: int = 0
    replan_count: int = 0
    max_replans: int = 3
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    context: dict[str, Any] = field(default_factory=dict)
    audit_trail: list[dict[str, Any]] = field(default_factory=list)

    @property
    def current_step(self) -> Optional[PlanStep]:
        if 0 <= self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None

    @property
    def progress(self) -> float:
        """Progress as a fraction (0.0 to 1.0)."""
        if not self.steps:
            return 0.0
        completed = sum(1 for s in self.steps if s.status == StepStatus.COMPLETED)
        return completed / len(self.steps)

    @property
    def is_complete(self) -> bool:
        return all(
            s.status in (StepStatus.COMPLETED, StepStatus.SKIPPED)
            for s in self.steps
        )

    @property
    def has_failures(self) -> bool:
        return any(s.status == StepStatus.FAILED for s in self.steps)

    def add_audit_entry(self, action: str, details: dict[str, Any]) -> None:
        """Append to audit trail for NIST AI RMF compliance."""
        self.audit_trail.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "step_index": self.current_step_index,
            **details,
        })


# ── Planner ──────────────────────────────────────────────────


class Planner:
    """
    Breaks complex tasks into ordered, executable steps.

    The Planner receives a task description and context (worker profile,
    market conditions, etc.) and produces an ExecutionPlan.

    This is the "think before you act" component. In the ORPA loop
    (Observe → Reason → Plan → Act), this handles the Plan phase.

    For the MVP, the planner uses template-based planning.
    In production, it will call the LLM to generate plans.
    """

    # Template plans for common task types
    PLAN_TEMPLATES: dict[str, list[dict[str, str]]] = {
        "loan_application": [
            {"action": "validate_input", "description": "Validate loan application data"},
            {"action": "check_eligibility", "description": "Check if worker meets basic eligibility criteria"},
            {"action": "assess_credit", "description": "Run creditworthiness assessment using transaction history"},
            {"action": "calculate_terms", "description": "Calculate loan amount, interest rate, and repayment schedule"},
            {"action": "generate_offer", "description": "Generate loan offer with terms and conditions"},
            {"action": "present_to_worker", "description": "Present offer to worker for confirmation"},
        ],
        "price_comparison": [
            {"action": "identify_markets", "description": "Identify relevant markets for the commodity"},
            {"action": "fetch_prices", "description": "Fetch current prices from each market"},
            {"action": "calculate_transport", "description": "Calculate transport costs to each market"},
            {"action": "compare_total_cost", "description": "Compare total cost (price + transport) across markets"},
            {"action": "recommend", "description": "Recommend best option with reasoning"},
        ],
        "market_setup": [
            {"action": "check_availability", "description": "Check market stall availability"},
            {"action": "register", "description": "Register for market stall"},
            {"action": "arrange_transport", "description": "Arrange transport to market"},
            {"action": "setup_payment", "description": "Set up M-Pesa payment for stall"},
            {"action": "notify_customers", "description": "Notify regular customers of new location"},
        ],
        "restock_inventory": [
            {"action": "check_stock", "description": "Check current inventory levels"},
            {"action": "analyze_sales", "description": "Analyze recent sales patterns"},
            {"action": "forecast_demand", "description": "Forecast demand for next period"},
            {"action": "find_suppliers", "description": "Find suppliers with best prices"},
            {"action": "place_order", "description": "Place restocking order"},
        ],
        "daily_planning": [
            {"action": "check_weather", "description": "Check weather forecast"},
            {"action": "check_prices", "description": "Check current market prices"},
            {"action": "analyze_traffic", "description": "Analyze traffic conditions"},
            {"action": "recommend_schedule", "description": "Recommend daily schedule"},
        ],
    }

    def plan(self, task_type: str, context: dict[str, Any]) -> ExecutionPlan:
        """
        Generate an execution plan for a given task type.

        Args:
            task_type: The type of task (e.g., "loan_application", "price_comparison")
            context: Additional context (worker_id, market_id, etc.)

        Returns:
            ExecutionPlan with ordered steps
        """
        plan = ExecutionPlan(
            task_description=f"Execute {task_type}",
            context=context,
        )

        template = self.PLAN_TEMPLATES.get(task_type)
        if template is None:
            # Unknown task type — create a generic plan
            plan.steps.append(PlanStep(
                description=f"Execute unknown task: {task_type}",
                action="generic_execute",
                parameters={"task_type": task_type, **context},
                expected_outcome="Task completed",
            ))
        else:
            for i, step_def in enumerate(template):
                plan.steps.append(PlanStep(
                    description=step_def["description"],
                    action=step_def["action"],
                    parameters={**context, "step_index": i},
                    expected_outcome=f"Step {i + 1} completed successfully",
                ))

        plan.add_audit_entry("plan_created", {
            "task_type": task_type,
            "step_count": len(plan.steps),
        })

        return plan

    def replan(
        self,
        plan: ExecutionPlan,
        failed_step: PlanStep,
        reason: str,
    ) -> ExecutionPlan:
        """
        Generate a revised plan after a step failure.

        The replanner considers what went wrong and adjusts
        remaining steps accordingly. It may:
        - Retry the failed step with different parameters
        - Skip the step if non-critical
        - Add alternative steps
        - Abort the plan if unrecoverable

        Args:
            plan: The current plan
            failed_step: The step that failed
            reason: Why the step failed

        Returns:
            Updated ExecutionPlan (modified in-place)
        """
        if plan.replan_count >= plan.max_replans:
            plan.status = PlanStatus.FAILED
            plan.add_audit_entry("plan_aborted", {
                "reason": f"Max replans ({plan.max_replans}) exceeded",
                "last_failure": reason,
            })
            return plan

        plan.replan_count += 1
        plan.status = PlanStatus.REPLANNING

        # Strategy 1: Retry if retries available
        if failed_step.can_retry():
            failed_step.retries += 1
            failed_step.status = StepStatus.PENDING
            failed_step.error = None
            plan.add_audit_entry("step_retry", {
                "step_id": failed_step.step_id,
                "retry_count": failed_step.retries,
                "reason": reason,
            })
            plan.status = PlanStatus.EXECUTING
            return plan

        # Strategy 2: Skip non-critical steps
        critical_actions = {"validate_input", "check_eligibility", "assess_credit", "present_to_worker"}
        if failed_step.action not in critical_actions:
            failed_step.status = StepStatus.SKIPPED
            plan.add_audit_entry("step_skipped", {
                "step_id": failed_step.step_id,
                "reason": f"Non-critical step failed: {reason}",
            })
            plan.status = PlanStatus.EXECUTING
            return plan

        # Strategy 3: Add alternative step
        alternative = PlanStep(
            description=f"Alternative: {failed_step.description} (fallback approach)",
            action=f"{failed_step.action}_fallback",
            parameters=failed_step.parameters,
            expected_outcome=failed_step.expected_outcome,
        )
        insert_index = plan.steps.index(failed_step) + 1
        failed_step.status = StepStatus.REPLANNED
        plan.steps.insert(insert_index, alternative)

        plan.add_audit_entry("step_replanned", {
            "original_step_id": failed_step.step_id,
            "alternative_step_id": alternative.step_id,
            "reason": reason,
        })

        plan.status = PlanStatus.EXECUTING
        return plan


# ── Executor ─────────────────────────────────────────────────


class Executor:
    """
    Executes individual plan steps.

    The Executor takes a PlanStep and runs its action using the
    registered tool handlers. It handles:
    - Tool invocation
    - Error handling and retry logic
    - Result capture
    - Timeout management

    In production, tool handlers will call actual Angavu agents.
    For MVP, they're registered as callable functions.
    """

    def __init__(self) -> None:
        self._tool_handlers: dict[str, Callable] = {}

    def register_tool(self, action: str, handler: Callable) -> None:
        """Register a handler for a specific action type."""
        self._tool_handlers[action] = handler

    def execute_step(self, step: PlanStep) -> PlanStep:
        """
        Execute a single plan step.

        Args:
            step: The step to execute

        Returns:
            The updated step with result or error
        """
        step.mark_in_progress()

        handler = self._tool_handlers.get(step.action)
        if handler is None:
            step.mark_failed(f"No handler registered for action: {step.action}")
            return step

        try:
            result = handler(**step.parameters)
            step.mark_completed(result)
        except Exception as e:
            step.mark_failed(str(e))

        return step

    def execute_plan(self, plan: ExecutionPlan) -> ExecutionPlan:
        """
        Execute all steps in a plan sequentially.

        Args:
            plan: The plan to execute

        Returns:
            The updated plan with step results
        """
        plan.status = PlanStatus.EXECUTING

        for i, step in enumerate(plan.steps):
            if step.status in (StepStatus.COMPLETED, StepStatus.SKIPPED):
                continue  # Already done

            plan.current_step_index = i
            plan.add_audit_entry("step_started", {
                "step_id": step.step_id,
                "action": step.action,
            })

            self.execute_step(step)

            plan.add_audit_entry("step_completed" if step.status == StepStatus.COMPLETED else "step_failed", {
                "step_id": step.step_id,
                "status": step.status.value,
                "duration_seconds": step.duration_seconds,
            })

            if step.status == StepStatus.FAILED:
                # Don't continue — let the observer/replanner handle this
                break

        if plan.is_complete:
            plan.status = PlanStatus.COMPLETED
            plan.completed_at = datetime.utcnow()

        return plan


# ── Observer ─────────────────────────────────────────────────


class Observer:
    """
    Observes execution results and determines next actions.

    The Observer is the "quality check" in the Plan-and-Execute loop.
    After each step completes, the Observer:
    1. Checks if the result matches expected outcomes
    2. Identifies any anomalies or errors
    3. Recommends whether to continue, replan, or abort

    This maps to the ORPA loop's Observe phase.
    """

    def observe_step(self, step: PlanStep) -> ObservationResult:
        """
        Observe the result of a completed step.

        Args:
            step: The completed step to observe

        Returns:
            ObservationResult with recommendation
        """
        if step.status == StepStatus.COMPLETED:
            return ObservationResult(
                step_id=step.step_id,
                status="success",
                should_continue=True,
                should_replan=False,
                notes=f"Step completed in {step.duration_seconds:.1f}s",
            )

        if step.status == StepStatus.FAILED:
            return ObservationResult(
                step_id=step.step_id,
                status="failure",
                should_continue=False,
                should_replan=step.can_retry(),
                notes=f"Step failed: {step.error}",
                failure_reason=step.error,
            )

        return ObservationResult(
            step_id=step.step_id,
            status=step.status.value,
            should_continue=False,
            should_replan=False,
            notes=f"Unexpected status: {step.status.value}",
        )

    def observe_plan(self, plan: ExecutionPlan) -> PlanObservation:
        """
        Observe the overall state of a plan.

        Args:
            plan: The plan to observe

        Returns:
            PlanObservation with overall assessment
        """
        completed = sum(1 for s in plan.steps if s.status == StepStatus.COMPLETED)
        failed = sum(1 for s in plan.steps if s.status == StepStatus.FAILED)
        skipped = sum(1 for s in plan.steps if s.status == StepStatus.SKIPPED)
        pending = sum(1 for s in plan.steps if s.status == StepStatus.PENDING)

        return PlanObservation(
            plan_id=plan.plan_id,
            total_steps=len(plan.steps),
            completed=completed,
            failed=failed,
            skipped=skipped,
            pending=pending,
            progress=plan.progress,
            is_complete=plan.is_complete,
            recommendation=self._recommend(plan),
        )

    def _recommend(self, plan: ExecutionPlan) -> str:
        """Generate a recommendation based on plan state."""
        if plan.is_complete:
            return "Plan completed successfully. All steps executed."
        if plan.replan_count >= plan.max_replans:
            return "Plan failed after maximum replanning attempts. Manual intervention required."
        if plan.has_failures:
            return "Plan has failed steps. Replanning recommended."
        return "Plan in progress. Continue execution."


@dataclass
class ObservationResult:
    """Result of observing a single step."""
    step_id: str
    status: str
    should_continue: bool
    should_replan: bool
    notes: str
    failure_reason: Optional[str] = None


@dataclass
class PlanObservation:
    """Result of observing an entire plan."""
    plan_id: str
    total_steps: int
    completed: int
    failed: int
    skipped: int
    pending: int
    progress: float
    is_complete: bool
    recommendation: str


# ── Replanner ────────────────────────────────────────────────


class Replanner:
    """
    Adjusts plans based on observed results.

    The Replanner sits between the Observer and the Executor.
    When the Observer reports a failure, the Replanner decides
    how to adjust the plan:
    - Retry with different parameters
    - Skip and continue
    - Add alternative steps
    - Abort the entire plan

    This maps to the ORPA loop's Plan phase (re-entry).
    """

    def __init__(self, planner: Planner) -> None:
        self._planner = planner

    def replan(
        self,
        plan: ExecutionPlan,
        observation: ObservationResult,
    ) -> ExecutionPlan:
        """
        Adjust the plan based on an observation.

        Args:
            plan: The current plan
            observation: The observation that triggered replanning

        Returns:
            Updated plan
        """
        failed_step = None
        for step in plan.steps:
            if step.step_id == observation.step_id:
                failed_step = step
                break

        if failed_step is None:
            return plan  # Can't find the failed step — shouldn't happen

        return self._planner.replan(
            plan=plan,
            failed_step=failed_step,
            reason=observation.failure_reason or "Unknown failure",
        )


# ── Orchestrator ─────────────────────────────────────────────


class PlanExecuteOrchestrator:
    """
    Top-level orchestrator for the Plan-and-Execute pattern.

    Combines Planner → Executor → Observer → Replanner into
    a single cohesive loop. This is the entry point for any
    complex multi-step task in Angavu.

    Usage:
        orchestrator = PlanExecuteOrchestrator()
        orchestrator.executor.register_tool("check_eligibility", my_handler)
        result = orchestrator.run("loan_application", {"worker_id": "abc123"})
    """

    def __init__(self) -> None:
        self.planner = Planner()
        self.executor = Executor()
        self.observer = Observer()
        self.replanner = Replanner(self.planner)

    def run(self, task_type: str, context: dict[str, Any]) -> ExecutionPlan:
        """
        Run the full Plan-and-Execute loop.

        Args:
            task_type: Type of task to execute
            context: Task context and parameters

        Returns:
            Completed or failed ExecutionPlan
        """
        # 1. PLAN
        plan = self.planner.plan(task_type, context)

        # 2. EXECUTE → OBSERVE → REPLAN loop
        max_iterations = 10  # Safety limit
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # EXECUTE
            plan = self.executor.execute_plan(plan)

            # OBSERVE
            plan_obs = self.observer.observe_plan(plan)

            if plan_obs.is_complete:
                plan.status = PlanStatus.COMPLETED
                plan.completed_at = datetime.utcnow()
                break

            if plan.status == PlanStatus.FAILED:
                break

            # Check last failed step for replanning
            if plan.has_failures:
                failed_step = next(
                    (s for s in reversed(plan.steps) if s.status == StepStatus.FAILED),
                    None,
                )
                if failed_step:
                    obs = self.observer.observe_step(failed_step)
                    if obs.should_replan:
                        plan = self.replanner.replan(plan, obs)
                    else:
                        plan.status = PlanStatus.FAILED
                        break
                else:
                    break
            else:
                break  # No failures, no pending steps — done

        return plan
