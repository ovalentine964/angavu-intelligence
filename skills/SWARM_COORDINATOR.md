# 🛡️ Swarm Coordinator Skill — Prevention System #5

> **Purpose:** Prevents duplicate work, tracks ownership, ensures verification, manages dependencies.
> **Use when:** Orchestrating multiple swarms/sub-agents for a project.

---

## Core Concept

The Coordinator is the **single source of truth** for all swarm work. It maintains:

1. **Task Registry** — What needs to be done
2. **Ownership Registry** — Who owns what component
3. **Dependency Graph** — What must happen in what order
4. **Completion State** — What's actually verified done

---

## 1. Task Registry

Create and maintain `swarm_registry.json` in the project root:

```json
{
  "tasks": {
    "IMPL-18": {
      "name": "Model Router",
      "status": "pending",
      "owner": null,
      "dependencies": [],
      "files": ["src/services/model_router.py"],
      "created": "2026-07-07T10:00:00Z",
      "started": null,
      "completed": null,
      "verified": false,
      "verification_results": null
    },
    "FIX-6": {
      "name": "Remove Paid APIs",
      "status": "completed",
      "owner": "swarm-alpha",
      "dependencies": [],
      "files": ["src/services/model_router.py", "config/providers.json"],
      "created": "2026-07-07T09:00:00Z",
      "started": "2026-07-07T09:05:00Z",
      "completed": "2026-07-07T09:12:00Z",
      "verified": true,
      "verification_results": {
        "cost_check": "pass",
        "syntax_check": "pass"
      }
    }
  },
  "component_ownership": {
    "src/services/model_router.py": "swarm-alpha",
    "src/services/academic_framework.py": "swarm-beta",
    "config/providers.json": "swarm-alpha"
  }
}
```

---

## 2. Coordinator Workflow

### Before Starting a Swarm

```python
def start_task(task_id: str, swarm_name: str):
    """Pre-flight checks before assigning a task to a swarm."""

    # 1. Check task exists in registry
    task = registry["tasks"].get(task_id)
    if not task:
        raise ValueError(f"Task {task_id} not in registry")

    # 2. Check dependencies are complete
    for dep in task["dependencies"]:
        dep_task = registry["tasks"][get(dep)]
        if dep_task["status"] != "completed" or not dep_task["verified"]:
            raise ValueError(f"Dependency {dep} not verified complete")

    # 3. Check no other swarm is working on it
    if task["status"] == "in_progress":
        raise ValueError(f"Task {task_id} already in progress by {task['owner']}")

    # 4. Check component ownership — no conflicts
    for filepath in task["files"]:
        current_owner = registry["component_ownership"].get(filepath)
        if current_owner and current_owner != swarm_name:
            raise ValueError(f"File {filepath} owned by {current_owner}")

    # 5. Assign task
    task["status"] = "in_progress"
    task["owner"] = swarm_name
    task["started"] = now()

    for filepath in task["files"]:
        registry["component_ownership"][filepath] = swarm_name

    return task
```

### After Swarm Completes

```python
def complete_task(task_id: str, verification_results: dict):
    """Mark task as complete after verification."""

    task = registry["tasks"][task_id]

    # 1. Run verification
    verify_script = "scripts/verify_code.py"
    result = run_verify(verify_script, task["files"])

    # 2. Check verification passed
    if not result["passed"]:
        task["status"] = "failed"
        task["verification_results"] = result
        raise ValueError(f"Verification failed: {result['errors']}")

    # 3. Mark complete
    task["status"] = "completed"
    task["verified"] = True
    task["completed"] = now()
    task["verification_results"] = result

    # 4. Release component ownership (optional — depends on workflow)
    # for filepath in task["files"]:
    #     del registry["component_ownership"][filepath]

    return task
```

---

## 3. Preventing Duplicate Work

### The Rule
**No two swarms may work on the same file simultaneously.**

### Implementation

```python
def check_file_available(filepath: str) -> bool:
    """Check if a file is available for modification."""
    owner = registry["component_ownership"].get(filepath)
    if owner:
        # Check if the owning task is still in progress
        for task in registry["tasks"].values():
            if task["owner"] == owner and task["status"] == "in_progress":
                if filepath in task["files"]:
                    return False
    return True

def claim_files(swarm_name: str, files: List[str]):
    """Claim ownership of files for a swarm."""
    for filepath in files:
        if not check_file_available(filepath):
            raise ValueError(f"File {filepath} already claimed")
        registry["component_ownership"][filepath] = swarm_name
```

---

## 4. Dependency Management

### Rules

1. **No circular dependencies** — Check before adding
2. **Dependencies must be verified** — Not just "completed" but verified
3. **Max chain depth: 5** — If deeper, decompose differently

### Dependency Check

```python
def check_dependencies(task_id: str) -> Tuple[bool, List[str]]:
    """Check if all dependencies are satisfied."""
    task = registry["tasks"][task_id]
    unsatisfied = []

    for dep_id in task["dependencies"]:
        dep = registry["tasks"].get(dep_id)
        if not dep:
            unsatisfied.append(f"{dep_id}: not found")
        elif dep["status"] != "completed":
            unsatisfied.append(f"{dep_id}: status is {dep['status']}")
        elif not dep["verified"]:
            unsatisfied.append(f"{dep_id}: not verified")

    return len(unsatisfied) == 0, unsatisfied

def check_circular_deps(task_id: str, new_deps: List[str]) -> bool:
    """Check if adding new dependencies would create a cycle."""
    visited = set()

    def dfs(node: str) -> bool:
        if node in visited:
            return True  # Cycle found
        visited.add(node)
        task = registry["tasks"].get(node)
        if not task:
            return False
        for dep in task["dependencies"]:
            if dfs(dep):
                return True
        visited.remove(node)
        return False

    # Temporarily add new deps
    original = registry["tasks"][task_id]["dependencies"]
    registry["tasks"][task_id]["dependencies"] = original + new_deps
    has_cycle = dfs(task_id)
    registry["tasks"][task_id]["dependencies"] = original

    return has_cycle
```

---

## 5. Swarm Size Limits

### Rules

| Metric | Limit | Reason |
|--------|-------|--------|
| Files per swarm | 3-5 | Keeps scope manageable |
| Time per swarm | 10 min max | Prevents timeouts |
| Lines of code | ~500 max | Reviewable in one pass |
| Dependencies | 3 max | Keeps dependency chain short |

### Decomposition Trigger

If a task exceeds these limits, decompose it:

```
IMPL-18: "Implement model router" (8 files, 1200 lines)
    ↓ decompose into:
IMPL-18a: "Core routing logic" (2 files, 300 lines)
IMPL-18b: "Provider registry" (2 files, 200 lines)
IMPL-18c: "Fallback chain" (2 files, 200 lines)
IMPL-18d: "Integration tests" (2 files, 200 lines)
```

---

## 6. Verification Protocol

Every completed task MUST pass verification:

```bash
# Step 1: File existence AND content
python scripts/verify_code.py --checks content

# Step 2: Cost check
python scripts/cost_guard.py --root .

# Step 3: Academic completeness (if applicable)
python scripts/academic_completeness.py --root .

# Step 4: Syntax check
python scripts/verify_code.py --checks syntax

# Step 5: Test check
python scripts/verify_code.py --checks tests
```

Only after ALL checks pass can a task be marked `verified: true`.

---

## 7. Context Sharing Between Swarms

### The Problem
Each swarm works in isolation and doesn't know what others did.

### The Solution
Before starting a swarm, inject context:

```python
def prepare_context(task_id: str) -> str:
    """Prepare context document for a swarm."""
    task = registry["tasks"][task_id]
    context_parts = []

    # 1. Current task details
    context_parts.append(f"## Your Task: {task['name']}")
    context_parts.append(f"Task ID: {task_id}")
    context_parts.append(f"Files to modify: {task['files']}")

    # 2. Dependency outputs
    for dep_id in task["dependencies"]:
        dep = registry["tasks"][dep_id]
        context_parts.append(f"\n## Completed Dependency: {dep['name']}")
        context_parts.append(f"Files: {dep['files']}")
        if dep.get("summary"):
            context_parts.append(f"Summary: {dep['summary']}")

    # 3. Component ownership
    context_parts.append("\n## Component Ownership")
    for filepath in task["files"]:
        owner = registry["component_ownership"].get(filepath, "unclaimed")
        context_parts.append(f"  {filepath}: {owner}")

    # 4. Prior work summary
    context_parts.append("\n## Prior Work Summary")
    for tid, t in registry["tasks"].items():
        if t["status"] == "completed" and t["verified"]:
            context_parts.append(f"  ✅ {tid}: {t['name']} (by {t['owner']})")

    return "\n".join(context_parts)
```

---

## 8. Coordinator Commands

### For Human/Parent Agent

```bash
# Create a new task
python coordinator.py add-task --id IMPL-18 --name "Model Router" \
    --files src/services/model_router.py --deps FIX-6

# Start a task (assign to swarm)
python coordinator.py start --id IMPL-18 --swarm swarm-alpha

# Complete a task (runs verification)
python coordinator.py complete --id IMPL-18

# Show status
python coordinator.py status

# Show ownership
python coordinator.py ownership

# Show dependencies
python coordinator.py deps --id IMPL-18
```

---

## 9. Error Recovery

### If a Swarm Fails

1. Mark task as `failed`
2. Release file ownership
3. Log the error
4. Re-assign to a new swarm (optionally with more context)

### If Verification Fails

1. Don't mark as `completed`
2. Return to `in_progress` with error details
3. Swarm must fix and re-verify

### If Timeout Occurs

1. Mark task as `timed_out`
2. Release file ownership
3. Decompose into smaller tasks
4. Re-assign pieces

---

## Integration with OpenClaw

When using OpenClaw's sub-agent system:

1. **Create tasks** in the main session
2. **Start swarms** by spawning sub-agents with the task context
3. **Collect results** via `sessions_yield`
4. **Verify** in the main session
5. **Update registry** in the main session

The main session IS the coordinator.

---

*This skill is a living document. Update it as the swarm coordination patterns evolve.*
