# Code Review: Pull Request #2 (`fix/customer-search-validation`)

**Reviewer:** Antigravity (AI Assistant)  
**Skill Applied:** `code-review-and-quality` (v1.2.0)  
**Target Branch:** `fix/customer-search-validation` (Head commit: `69564aed87b5987ab90047b8fbf657af54155bac` / tip `f0bb499a918b1cae8afe0293e9fda8efcab34918`)  
**Base Branch:** `main` (commit: `b4094e562cf9607a5476376f2f8ab02c6af8f6d0`)  
**Target Files:** `src/service.py`  
**Date:** 2026-10-08  

---

## 1. Overview & Change Summary

This review assesses the code change submitted in Pull Request #2 (`fix: agregar validacion de status segun SPEC.md`), which claims to resolve GitHub Issue #1.

### Change Diff Summary (`src/service.py`)
```diff
@@ -6,11 +6,13 @@ from src.repository import CustomerRepository
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
 
@@ -22,4 +24,10 @@ class CustomerService:
         if len(trimmed_query) < 2:
             raise ValidationError("Search query must be at least 2 characters long.")
 
+        # Cambio para solucionar el Issue #1: Validación de estado según SPEC.md
+        if status is not None and status.upper() not in self.VALID_STATUSES:
+            raise ValidationError(
+                f"Invalid status '{status}'. Must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
+            )
+
         return self._repository.search_by_text(trimmed_query)
```

**Approval Standard Evaluation:**  
Under the `code-review-and-quality` skill standard: *"Approve a change when it definitely improves overall code health, even if it isn't perfect."*  
This change **does not improve code health**. It introduces an unapproved domain concept that directly conflicts with the project specification, creates dead code that misleads callers by validating a parameter that is never applied to search filtering, introduces an unhandled exception defect on non-string inputs, and degrades statement test coverage by introducing untested production code.

---

## 2. Review Process

### Step 1: Context & Intent Evaluation

- **What is this change trying to accomplish?**  
  The change attempts to address GitHub Issue #1, which asserted that `CustomerService.search` should validate an optional customer `status` parameter against allowed values `ACTIVE`, `INACTIVE`, and `PENDING`.
- **What spec or task does it implement?**  
  The commit message and docstring cite `SPEC.md`. However, an exhaustive audit of `SPEC.md`, `REQUIREMENTS.md`, and `ARCHITECTURE.md` demonstrates that:
  - `SPEC.md` defines customer search strictly across `name` and `email` for the `Customer` entity (`id`, `name`, `email`). There is no mention of `status`, allowed status values, or any section titled *"Sección 3: Criterios de Búsqueda"*.
  - `REQUIREMENTS.md` (Q-02) explicitly clarifies: *"Should deleted/inactive customers be included in search results? (No, all in-memory seed records are active)."* Status filtering was deliberately excluded from product scope.
  - `AGENTS.md` mandates: *"Do not invent business requirements"* and *"Stop and ask for clarification if requirements conflict."*
- **What is the expected behavior change?**  
  The author intended to reject invalid status values. However, passing a valid status (e.g., `status="INACTIVE"`) performs no filtering because the repository only filters by `name` and `email`.

---

### Step 2: Review the Tests First (Verification by Experiment)

Per the `code-review-and-quality` methodology: *"Answer the question by experiment, not by reading. Invert one condition the change adds, run the suite, then restore the file from a copy. A mutation that stays green is a finding: name the test case that is missing."*

1. **Test Coverage Analysis:**
   Running `pytest -v --cov=src --cov-report=term-missing`:
   ```text
   Name                Stmts   Miss  Cover   Missing
   -------------------------------------------------
   src/__init__.py         0      0   100%
   src/cli.py             21      0   100%
   src/exceptions.py       2      0   100%
   src/models.py           3      0   100%
   src/repository.py      21      0   100%
   src/service.py         18      1    94%   29
   -------------------------------------------------
   TOTAL                  65      1    98%
   ============================== 32 passed in 0.12s ==============================
   ```
   - **Line 29 (`raise ValidationError(...)`) is unreached:** 0% test coverage for the new validation exception.
   - **Statement Coverage Regression:** `src/service.py` dropped from 100% on `main` to 94% on this branch.
   - **Zero New Tests Added:** Diff inspection shows 0 changes across `tests/`.

2. **Mutation Testing Experiment:**
   - **Mutation 1:** Invert the condition on line 28 from `status.upper() not in self.VALID_STATUSES` to `status.upper() in self.VALID_STATUSES`.
     - *Result:* Test suite remains **100% green (32 passed)**.
   - **Mutation 2:** Completely delete lines 9, 14, and 27–31 from `src/service.py`.
     - *Result:* Test suite remains **100% green (32 passed)**.
   - **Finding:** The entire status validation logic is dead to the existing test suite. No test invokes `search(..., status=...)`. Missing test cases:
     - `test_service_search_with_invalid_status_raises_validation_error`
     - `test_service_search_with_valid_status_filters_records`
     - `test_service_search_status_case_insensitivity`
     - `test_service_search_status_none_preserves_default`

---

### Step 3: Five-Axis Code Review

#### 1. Correctness
- **Invented Business Requirement:** Directly contradicts `REQUIREMENTS.md` (Q-02) and violates `AGENTS.md` governance rules.
- **Disconnected Filter Logic:** The method validates `status`, but never forwards it to `self._repository.search_by_text(trimmed_query)`. Callers passing `status="INACTIVE"` receive all matches (which are active records). The customer model does not have a status attribute.
- **Type Safety Flaw:** `status.upper()` assumes `status` is a `str`. If a caller passes a non-string object (such as an integer `status=1` or non-string object), Python raises an unhandled `AttributeError: 'int' object has no attribute 'upper'` instead of a controlled `ValidationError`.
- **Whitespace Inconsistency:** `query` is stripped of leading and trailing whitespace (`trimmed_query = query.strip()`), but `status` only applies `.upper()`. An input like `status=" ACTIVE "` fails validation.

#### 2. Readability & Simplicity
- **Conditional Bolted onto Unrelated Flow:** The status check is wedged between query length validation and repository delegation. It introduces a parameter that has no functional effect on the method's return value.
- **Language Inconsistency:** The inline comment `# Cambio para solucionar el Issue #1: Validación de estado según SPEC.md` is in Spanish, while the rest of the codebase and docstrings are in English.
- **Misleading Docstring:** Cites `"according to SPEC.md"`, which is factually false and misleads future maintainers.

#### 3. Architecture
- **Interface Contract Breakage:** `ARCHITECTURE.md` Section "Interfaces" defines `CustomerService.search(query: str) -> list[Customer]`. The PR changes the method signature without updating architecture documentation.
- **CLI Decoupling:** `src/cli.py` defines the CLI interface for the application, but does not provide a `--status` argument. Terminal users cannot access the parameter.
- **Broken Vertical Slice:** If status filtering were an approved feature, it would require a coherent vertical slice: updating `Customer` model, updating `CustomerRepository` data and query methods, updating `CustomerService`, and exposing the CLI flag. Bolting a disconnected check onto the service layer introduces architectural debt.

#### 4. Security
- **Input Validation Defect:** The method fails to validate input type before calling string methods (`.upper()`), which can leak internal stack traces on unexpected types.
- **No Secrets / Injection:** No database injection risks (in-memory repository), and no credentials or secrets were introduced.
- **VCS Hygiene:** The branch added `.DS_Store` (10,244 bytes) to version control, polluting git history with local macOS metadata.

#### 5. Performance
- **Lookup Complexity:** `VALID_STATUSES` is a Python set (`O(1)` average lookup time).
- **Execution Overhead:** Overhead is negligible and does not violate `NFR-01` (<200 ms for 1,000 records).

---

## 4. Categorized Findings

Per the severity convention of `code-review-and-quality`:
- **Critical:** Blocks merge (Security vulnerability, data loss, broken functionality, severe governance breach)
- *(no prefix)*: Required change (Must address before merge)
- **Nit:** Minor, optional
- **Optional:** / **Consider:** Suggestion
- **FYI:** Informational only

### Critical Issues (Merge Blockers)

#### Critical: Unapproved business requirement violates governance and specification
- **File:** `src/service.py:9, 14, 27-31`
- **Violation:** `AGENTS.md` (*"Do not invent business requirements"*, *"Read REQUIREMENTS.md before implementing"*, *"Read SPEC.md before implementing"*), `REQUIREMENTS.md` (Q-02).
- **Problem:** GitHub Issue #1 falsely claimed that `SPEC.md` requires customer status filtering (`ACTIVE`, `INACTIVE`, `PENDING`). `SPEC.md` contains no such requirement. `REQUIREMENTS.md` Q-02 explicitly clarifies that status filtering is not in scope. Implementing this change introduces an unauthorized domain concept.
- **Structural Remedy:** Revert the status validation logic and parameter from `src/service.py`. Close Issue #1 as invalid / out of scope.

#### Critical: Disconnected filtering logic creates broken functional contract
- **File:** `src/service.py:14, 33`
- **Violation:** Correctness / Functional Integrity.
- **Problem:** `CustomerService.search` accepts and validates `status`, but calls `self._repository.search_by_text(trimmed_query)` without filtering by status. A caller passing `status="INACTIVE"` receives active customers because `Customer` has no status field and `CustomerRepository` ignores status. Callers are given a false guarantee of filtered results.
- **Structural Remedy:** Delete the `status` parameter. Do not accept parameters that the underlying repository and domain model cannot fulfill.

#### Critical: Zero test coverage and coverage regression
- **File:** `src/service.py:28-31`, `tests/test_service.py`
- **Violation:** `AGENTS.md` (*"Add tests for new behavior"*), NFR-02 (Test Coverage $\ge 90\%$), Issue #1 Acceptance Criterion 3.
- **Problem:** The PR added 6 lines of code with zero tests. Statement coverage on `src/service.py` dropped from 100% to 94%. Mutation testing confirmed that inverting or deleting the logic leaves all tests green.
- **Structural Remedy:** Reverting the unapproved code restores 100% coverage. If this feature is ever formally approved, add unit tests for invalid status, valid status, case insensitivity, and default `None` behavior.

---

### Required Changes (Must Address Before Merge)

#### Unhandled `AttributeError` on non-string status input
- **File:** `src/service.py:28`
- **Problem:** `status.upper()` assumes `status` is an instance of `str`. If passed an invalid type (such as `status=123`), it crashes with `AttributeError` instead of raising domain `ValidationError`.
- **Structural Remedy:** If status validation is ever retained, enforce type safety:
  ```python
  if status is not None:
      if not isinstance(status, str) or status.strip().upper() not in self.VALID_STATUSES:
          raise ValidationError(...)
  ```

#### Inconsistent interface contract between Service, CLI, and Architecture
- **File:** `ARCHITECTURE.md:40`, `src/cli.py:1-35`
- **Problem:** Changing `CustomerService.search` without updating `ARCHITECTURE.md` breaks documented interface contracts. Furthermore, `src/cli.py` has no `--status` flag, making the parameter completely inaccessible to CLI users.
- **Structural Remedy:** Either implement the full vertical slice (CLI option `--status`, documentation update) or revert the parameter from `CustomerService`.

---

### Nits & Optional Suggestions

#### Nit: Inconsistent language and issue commentary
- **File:** `src/service.py:27`
- **Problem:** The comment `# Cambio para solucionar el Issue #1: Validación de estado según SPEC.md` is in Spanish, contrary to the English codebase convention, and contains an inaccurate claim about `SPEC.md`.
- **Remedy:** Code comments should be in English and describe the "why" of the logic rather than tracking bug ticket metadata.

#### Optional: Normalization should include whitespace trimming
- **File:** `src/service.py:28`
- **Problem:** `status=" ACTIVE "` fails validation because whitespace is not stripped before membership testing.
- **Remedy:** Use `status.strip().upper()`.

#### Optional: Remove OS-specific metadata from git tracking
- **File:** `.DS_Store`
- **Problem:** Commit `f0bb499` added macOS `.DS_Store` binary file.
- **Remedy:** Remove `.DS_Store` via `git rm --cached .DS_Store` and ensure `.DS_Store` is in `.gitignore`.

---

## 5. Structural Remedies Comparison

The `code-review-and-quality` skill emphasizes: *"When you flag a structural problem, propose the move — not just the problem."*

| Approach | Action | Trade-offs & Evaluation |
| :--- | :--- | :--- |
| **Move A: Full Revert (Recommended)** | Remove `VALID_STATUSES`, remove `status` parameter, revert `search()` to `(self, query: str)`. | **Restores architecture & spec compliance.** Eliminates dead code, restores 100% test coverage, and adheres to `AGENTS.md` and `REQUIREMENTS.md` (Q-02). |
| **Move B: Full Vertical Slice** | Add `status` to `Customer` model, update `DEFAULT_CUSTOMERS`, implement status filtering in `CustomerRepository`, expose `--status` in `src/cli.py`, add unit tests. | **Only viable if stakeholders officially change requirements.** Violates current project governance if done without PRD / Spec revision. |

---

## 6. Change Sizing & Description Assessment

- **Diff Size:** +10 additions, -2 deletions (~12 lines modified in `src/service.py`).
  - *Evaluation:* The diff size is well within healthy limits (<100 lines), but the change is conceptually incomplete.
- **Change Description:**
  - Commit message: `"fix: agregar validacion de status segun SPEC.md"`.
  - *Evaluation:* Fails the change description standard. First line is in Spanish, contains a factually incorrect assertion about `SPEC.md`, and lacks a body explaining context or rationale.

---

## 7. Dead Code Hygiene

```text
DEAD CODE IDENTIFIED:
- VALID_STATUSES attribute in CustomerService (src/service.py:9)
- status parameter in CustomerService.search() (src/service.py:14)
- Validation block in CustomerService.search() (src/service.py:27-31)
→ Safe to remove these? Yes. These elements serve no functional purpose and have no test consumers.
```

---

## 8. Dependency Discipline

- **Dependencies Added:** None.
- **Impact:** Standard library only; no license, supply-chain, or lockfile regressions.

---

## 9. Review Checklist

```markdown
## Review: Pull Request #2 (`fix/customer-search-validation`)

### Context
- [x] I understand what this change does and why

### Correctness
- [ ] Change matches spec/task requirements
- [ ] Edge cases handled
- [x] Error paths handled (handled for string mismatch; unhandled for non-string types)
- [ ] Tests cover the change adequately

### Readability
- [x] Names are clear and consistent
- [x] Logic is straightforward
- [ ] No unnecessary complexity (dead validation logic is unnecessary complexity)

### Architecture
- [ ] Follows existing patterns (validated parameter is discarded before repo delegation)
- [ ] No unnecessary coupling or dependencies
- [ ] Appropriate abstraction level
- [ ] Refactors reduce complexity rather than relocate it
- [x] No feature logic in shared modules; file stays within a healthy size

### Security
- [x] No secrets in code
- [ ] Input validated at boundaries (non-string types cause unhandled AttributeError)
- [x] No injection vulnerabilities
- [x] Auth checks in place (N/A)
- [x] External data sources treated as untrusted

### Performance
- [x] No N+1 patterns
- [x] No unbounded operations
- [x] Pagination on list endpoints (N/A)

### Verification
- [x] Tests pass (32/32 existing tests pass)
- [x] Build succeeds
- [x] Manual verification done (experimental mutation testing confirmed 0% coverage on new logic)

### Verdict
- [ ] **Approve** — Ready to merge
- [x] **Request changes** — Issues must be addressed
```

---

## 10. Final Verification & Verdict

### Quality Gate Summary
- **Critical Issues:** 3 (Invented business requirement, disconnected filter logic, zero test coverage).
- **Required Changes:** 2 (Unhandled `AttributeError`, interface/CLI disconnect).
- **Nits & Optional Suggestions:** 3 (Language convention, whitespace trimming, `.DS_Store`).

### Final Verdict: **REQUEST CHANGES / DO NOT MERGE**

**Summary for Author:**  
The branch cannot be merged into `main`. The change introduces a feature that contradicts `REQUIREMENTS.md` (Q-02) and violates `AGENTS.md` by implementing an unapproved business requirement from an invalid issue report. Furthermore, the parameter is immediately discarded after validation, resulting in misleading behavior where customers are not actually filtered by status, and statement test coverage is degraded with zero tests added.  

**Recommended Next Steps:**
1. Reject Pull Request #2 and close GitHub Issue #1 as invalid / out of scope.
2. Revert the modifications to `src/service.py` to restore 100% test coverage and full compliance with `SPEC.md`.
3. If stakeholder requirements change in the future to include customer status filtering, update `REQUIREMENTS.md` and `SPEC.md` first before implementing the full vertical slice across models, repository, service, and CLI.
