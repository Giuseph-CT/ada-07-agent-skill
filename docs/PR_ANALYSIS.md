# Engineering Analysis: Pull Request #2 (Giuseph-CT/ada-05-spec-driven-feature)

* **PR Reference:** [PR #2: fix: agregar validacion de status segun SPEC.md](https://github.com/Giuseph-CT/ada-05-spec-driven-feature/pull/2)
* **Linked Issue:** Closes [#1](https://github.com/Giuseph-CT/ada-05-spec-driven-feature/issues/1)
* **Author:** Giuseph-CT | **Status:** OPEN | **Scope:** `Giuseph-CT/ada-05-spec-driven-feature` (Read-Only)

> **API Mapping Note:** In GitHub's data model, ID #1 is an Issue (`Issue #1`). The corresponding Pull Request created to address Issue #1 is `Pull Request #2`.

---

## 1. PR Summary & Metadata

* **Base Branch:** `main` (SHA: `b4094e562cf9607a5476376f2f8ab02c6af8f6d0`)
* **Head Branch:** `fix/customer-search-validation` (SHA: `69564aed87b5987ab90047b8fbf657af54155bac`)
* **Commits:** 1 commit (`69564ae`: *"fix: agregar validacion de status segun SPEC.md"*)
* **Changed Files:** 1 file modified (`src/service.py`) — `+10` additions, `-2` deletions
* **Reviews / Comments:** 0 reviews, 0 comments
* **CI / Checks:** None configured

---

## 2. Code Diff

```diff
diff --git a/src/service.py b/src/service.py
index 049caad..1e41b78 100644
--- a/src/service.py
+++ b/src/service.py
@@ -6,11 +6,13 @@
 class CustomerService:
     """Service layer orchestrating customer search validation and execution."""
 
+    VALID_STATUSES = {"ACTIVE", "INACTIVE", "PENDING"}
+
     def __init__(self, repository: CustomerRepository | None = None) -> None:
         self._repository = repository if repository is not None else CustomerRepository()
 
-    def search(self, query: str) -> list[Customer]:
-        """Validate query and search customers through repository."""
+    def search(self, query: str, status: str | None = None) -> list[Customer]:
+        """Validate query and status according to SPEC.md, then search customers."""
         if query is None:
             raise ValidationError("Search query cannot be empty.")
 
@@ -22,4 +24,10 @@ def search(self, query: str) -> list[Customer]:
         if len(trimmed_query) < 2:
             raise ValidationError("Search query must be at least 2 characters long.")
 
+        # Cambio para solucionar el Issue #1: Validación de estado según SPEC.md
+        if status is not None and status.upper() not in self.VALID_STATUSES:
+            raise ValidationError(
+                f"Invalid status '{status}'. Must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
+            )
+
         return self._repository.search_by_text(trimmed_query)

## 3. Detailed Evaluation

### 1. What behavior changes?
* **Method Signature:** `CustomerService.search` accepts an optional `status: str | None = None` parameter in addition to `query: str`.
* **Validation:** If `status` is provided, it normalizes the input with `.upper()` and checks against `VALID_STATUSES = {"ACTIVE", "INACTIVE", "PENDING"}`. If invalid, it raises `ValidationError`.
* **Execution:** If `status` is valid (e.g., `"ACTIVE"`), the parameter is discarded after validation; the method continues to execute `self._repository.search_by_text(trimmed_query)` without filtering by status.

### 2. Which Issue / requirement appears to be addressed?
* The PR explicitly targets **Issue #1** (`Closes #1`).
* It addresses the purported requirement described in Issue #1 that input status must be constrained to `{"ACTIVE", "INACTIVE", "PENDING"}`.

### 3. Which files implement the change?
* Exclusively `src/service.py`. No models, repositories, CLI entry points, documentation, or tests were altered.

### 4. Are tests present for the behavior?
* **No.** No tests were added or modified anywhere in `tests/`. The new validation code path in `src/service.py` is entirely untested.

### 5. Are there obvious gaps between the Issue and implementation?
* **Missing Tests:** Acceptance Criterion 3 of Issue #1 (*"Agregar o actualizar las pruebas unitarias para cubrir el escenario de filtro de estado inválido"*) was omitted.
* **Incomplete Filter Implementation:** The PR validates status but does not perform any status-based filtering in the repository.
* **Lack of CLI Support:** The primary application interface in `src/cli.py` does not expose any `--status` argument.
* **Protocol Disconnect:** Issue #1 mentions returning `400 Bad Request`; this PR only raises Python `ValidationError`.

### 6. Is there unrelated scope?
* Within the git diff itself, there is no stray or unrelated code.
* At the architectural and domain level, however, the concept of customer status is entirely outside the approved scope defined in `REQUIREMENTS.md` and `SPEC.md`.

### 7. What should a human reviewer verify manually?
* Verify whether status filtering was ever an approved product requirement or if it was hallucinated.
* Check the project rule in `AGENTS.md` regarding inventing business requirements.
* Run `pytest --cov=src` locally to observe the test coverage regression caused by untested lines in `src/service.py`.
* Review `REQUIREMENTS.md` (Q-02) and `agent-report.md` confirming that status filtering was previously reviewed and explicitly rejected.

---

## 4. Classification of Findings

### [OBSERVATION]
* **GitHub Object Numbering:** PR #2 is the pull request linked to Issue #1. PR #1 does not exist on GitHub (404 Not Found).
* **Atomic Git Diff:** The pull request is contained within a single commit (`69564ae`) modifying a single file (`src/service.py`).
* **Case-Insensitive Input Handling:** The implementation uses `.upper()`, allowing `"active"`, `"Active"`, or `"ACTIVE"` to pass validation.

### [RISK]
* **Scope & Governance Violation:** The project's `AGENTS.md` dictates: *"Do not invent business requirements"* and *"Do not modify REQUIREMENTS.md or SPEC.md to make tests pass"*. Merging this PR establishes an unapproved domain concept that directly conflicts with `REQUIREMENTS.md` (Q-02).
* **Quality & Coverage Degradation:** The repository currently has 100% test coverage. Introducing 6 lines of branching logic without unit tests reduces statement coverage and risks violating non-functional requirement **NFR-02** ($\ge 90\%$ test coverage).
* **Dead Code / False Sense of Functionality:** A caller passing `status="INACTIVE"` will pass validation successfully, but will still receive active customer records because the repository layer does not filter by status.

### [POTENTIAL DEFECT]
* **Type Safety / Attribute Error on Non-String Inputs:** The code does `status.upper()` directly without checking `isinstance(status, str)`. If a non-string object (such as an integer or enum instance) is passed, it will raise an unhandled `AttributeError` instead of a `ValidationError`.
* **Incomplete Acceptance Criteria Fulfillment:** Acceptance Criterion #3 of Issue #1 explicitly mandates adding unit tests. This PR fails its own stated acceptance criteria.

### [QUESTION]
* **Product Intent:** Should the product requirements be formally revised to include customer status (requiring changes to `REQUIREMENTS.md`, `SPEC.md`, `src/models.py`, `src/repository.py`, and `src/cli.py`), or should Issue #1 and PR #2 be closed as invalid / out of scope?
* **CLI Surface:** If status filtering is accepted, should `src/cli.py` add an optional `--status` argument with choices `['ACTIVE', 'INACTIVE', 'PENDING']`?