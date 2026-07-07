# 🛡️ Task Decomposition Skill — Prevention System #7

> **Purpose:** Break large tasks into swarm-sized chunks that can complete within timeout.
> **Prevents:** Timeouts, incomplete work, overly broad tasks, unclear deliverables.

---

## The Problem

A swarm given "implement the entire model routing system" will:
1. Run out of time
2. Produce incomplete work
3. Miss edge cases
4. Have no clear "done" state

---

## Decomposition Rules

### Rule 1: 3-5 Files Per Swarm
If a task touches more than 5 files, decompose it.

### Rule 2: 10-Minute Scope
If a task takes more than 10 minutes, decompose it. Estimate: ~100 lines of code per 2 minutes.

### Rule 3: Single Responsibility
Each swarm task should do ONE thing well. If you can't describe it in one sentence, it's too broad.

### Rule 4: Clear Deliverables
Each task must produce specific, verifiable files. No "improve the codebase."

### Rule 5: Testable Completion
Each task must have a bash command that verifies it's done.

---

## Decomposition Process

### Step 1: List All Files

```
Original task: "Implement model routing system"

Files involved:
- src/services/model_router.py (new)
- src/services/providers/huggingface.py (new)
- src/services/providers/ollama.py (new)
- src/services/providers/local.py (new)
- src/services/fallback_chain.py (new)
- config/providers.json (modify)
- tests/test_model_router.py (new)
- tests/test_providers.py (new)
- tests/test_fallback.py (new)
- docs/model_routing.md (new)

Total: 10 files → TOO MANY for one swarm
```

### Step 2: Group by Dependency

```
Group A (Core - no dependencies):
  - src/services/model_router.py
  - config/providers.json

Group B (Providers - depends on A):
  - src/services/providers/huggingface.py
  - src/services/providers/ollama.py
  - src/services/providers/local.py

Group C (Fallback - depends on A, B):
  - src/services/fallback_chain.py

Group D (Tests - depends on A, B, C):
  - tests/test_model_router.py
  - tests/test_providers.py
  - tests/test_fallback.py

Group E (Docs - depends on all):
  - docs/model_routing.md
```

### Step 3: Create Task Sequence

```
IMPL-18a: Core Router (Group A)
  Files: src/services/model_router.py, config/providers.json
  Time: ~5 min
  Verify: python -m py_compile src/services/model_router.py

IMPL-18b: Provider Implementations (Group B)
  Files: src/services/providers/huggingface.py, ollama.py, local.py
  Depends: IMPL-18a
  Time: ~8 min
  Verify: python -m py_compile src/services/providers/*.py

IMPL-18c: Fallback Chain (Group C)
  Files: src/services/fallback_chain.py
  Depends: IMPL-18a, IMPL-18b
  Time: ~5 min
  Verify: python -m py_compile src/services/fallback_chain.py

IMPL-18d: Tests (Group D)
  Files: tests/test_model_router.py, test_providers.py, test_fallback.py
  Depends: IMPL-18a, IMPL-18b, IMPL-18c
  Time: ~8 min
  Verify: python -m pytest tests/ -v

IMPL-18e: Documentation (Group E)
  Files: docs/model_routing.md
  Depends: IMPL-18d
  Time: ~3 min
  Verify: test -s docs/model_routing.md
```

### Step 4: Write Task Definitions

Each task gets the full SWARM_TASK_TEMPLATE format:

```markdown
# SWARM TASK: IMPL-18a — Core Router

## META
- Task ID: IMPL-18a
- Owner: [assigned at runtime]
- Dependencies: None
- Timeout: 5 minutes

## WHY
The model router is the central dispatch for all AI inference requests.
Without it, no other component can route to free models.

## WHAT
- [ ] Create `src/services/model_router.py` — main routing logic
- [ ] Update `config/providers.json` — list of free providers

## HOW
1. Create ModelRouter class with `route(request) -> provider` method
2. Define provider interface: `Provider.get_models()`, `Provider.infer(request)`
3. Add provider registry loading from config/providers.json
4. Ensure only FREE providers are included

## WHERE
```
src/services/model_router.py  # CREATE
config/providers.json          # MODIFY
```

## VERIFY
```bash
python -m py_compile src/services/model_router.py
python -c "import json; json.load(open('config/providers.json'))"
! grep -ri "openai\|anthropic\|google" src/services/model_router.py
```

## COST: $0
```

---

## Decomposition Patterns

### Pattern: Horizontal Split (Parallel)
When tasks don't depend on each other:

```
Task A: Implement HuggingFace provider
Task B: Implement Ollama provider
Task C: Implement local model provider

→ Can run in parallel (different files, no dependencies)
```

### Pattern: Vertical Split (Sequential)
When tasks build on each other:

```
Task A: Create data models
Task B: Create service layer (uses data models)
Task C: Create API layer (uses service layer)

→ Must run sequentially (each depends on prior)
```

### Pattern: Core + Extensions
When there's a central module with plugins:

```
Task A: Core module + plugin interface
Task B: Plugin 1
Task C: Plugin 2
Task D: Plugin 3

→ A first, then B/C/D in parallel
```

### Pattern: Implement + Test
When implementation and testing can be separated:

```
Task A: Implementation (3 files)
Task B: Tests for A (2 files)
Task C: Integration test (1 file)

→ A first, then B, then C
```

---

## Anti-Patterns

### ❌ Too Broad
```
"Implement the entire authentication system"
→ 15 files, 2000 lines, 30+ minutes
```

### ✅ Properly Decomposed
```
AUTH-1: User model and database schema (2 files)
AUTH-2: Password hashing and verification (1 file)
AUTH-3: JWT token generation (1 file)
AUTH-4: Login endpoint (1 file)
AUTH-5: Registration endpoint (1 file)
AUTH-6: Auth middleware (1 file)
AUTH-7: Tests (3 files)
```

### ❌ Too Granular
```
"Create the User class"
"Add the email field to User"
"Add the password field to User"
"Add the created_at field to User"
→ Each is 2 minutes of work, overhead dominates
```

### ✅ Right-Sized
```
"Create User model with all fields and validation"
→ 1 file, 5 minutes, clear deliverable
```

### ❌ No Verification
```
"Make the code better"
→ How do you know when it's done?
```

### ✅ Verifiable
```
"Add error handling to model_router.py:fetch()
 - Verify: no bare except clauses
 - Verify: all exceptions logged
 - Verify: test_error_handling.py passes"
```

---

## Quick Decomposition Checklist

Before assigning a task to a swarm, verify:

- [ ] **≤ 5 files** to create/modify
- [ ] **≤ 10 minutes** estimated work time
- [ ] **Single responsibility** — one clear purpose
- [ ] **Specific deliverables** — exact file paths listed
- [ ] **Verification command** — bash command to check completion
- [ ] **Dependencies listed** — what must complete first
- [ ] **No conflicts** — files not claimed by another swarm
- [ ] **Context included** — relevant info from prior work

If any check fails → decompose further.

---

## Decomposition Template

```markdown
## Task Decomposition: [Original Task Name]

### Original Scope
- Files: [count]
- Estimated time: [minutes]
- Description: [one sentence]

### Why Decompose
- [ ] More than 5 files
- [ ] More than 10 minutes
- [ ] Multiple responsibilities
- [ ] No clear verification

### Decomposed Tasks

| ID | Name | Files | Time | Depends On |
|----|------|-------|------|------------|
| X-1 | [name] | [files] | [min] | None |
| X-2 | [name] | [files] | [min] | X-1 |
| X-3 | [name] | [files] | [min] | X-1 |
| X-4 | [name] | [files] | [min] | X-2, X-3 |

### Dependency Graph
```
X-1 → X-2 → X-4
X-1 → X-3 ↗
```

### Parallelization
- X-2 and X-3 can run in parallel (after X-1)
- X-4 must wait for both X-2 and X-3
```

---

*This skill prevents the #1 cause of swarm failure: tasks too large to complete.*
