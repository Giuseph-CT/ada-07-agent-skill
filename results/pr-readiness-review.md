# PR Readiness Review

## Review Context
- **PR / Branch:** `fix/customer-search-validation` (linked to GitHub PR #2, targeting base `main`)
- **Reviewer Agent:** Antigravity (Advanced Agentic Assistant)
- **Date:** 2026-10-08
- **Commit Reviewed:** `69564aed87b5987ab90047b8fbf657af54155bac` (*"fix: agregar validacion de status segun SPEC.md"*) and branch tip `f0bb499a918b1cae8afe0293e9fda8efcab34918`
- **Target File:** `src/service.py` (and related repo artifacts)
- **Readiness Verdict:** **NOT READY / REJECT MERGE**

---

## Requirements / Acceptance Criteria Reviewed
The branch was evaluated against the project specification, governance rules, and linked issue claims:

1. **`AGENTS.md` (Project Governance Rules):**
   - *"Read REQUIREMENTS.md before implementing."*
   - *"Read SPEC.md before implementing."*
   - *"Do not invent business requirements."*
   - *"Do not modify REQUIREMENTS.md or SPEC.md to make tests pass."*
   - *"Do not delete or weaken tests."*
   - *"Add tests for new behavior."*
   - *"Stop and ask for clarification if requirements conflict."*

2. **`REQUIREMENTS.md`:**
   - **FR-01 through FR-06:** Define partial, case-insensitive customer search by name and email, minimum query length of 2 characters, structured output, and input validation.
   - **Q-02:** Explicitly documents: *"Should deleted/inactive customers be included in search results? (No, all in-memory seed records are active)."* Status filtering is not part of the functional requirements.
   - **NFR-02:** Requires at least 90% unit test coverage using pytest.

3. **`SPEC.md`:**
   - **Scope:** In-memory customer repository, core domain logic for name/email search, CLI entry point, and test suite.
   - **Domain Model:** `Customer` dataclass contains only `id: str`, `name: str`, and `email: str`.
   - **Validation Rules:** Only two rules exist: (1) `len(trimmed_query) < 2` raises `ValidationError`, (2) empty/whitespace query raises `ValidationError`.
   - **Note:** `SPEC.md` does **not** contain any status parameter, status enum, or "Sección 3: Criterios de Búsqueda".

4. **`ARCHITECTURE.md`:**
   - **Component Interface:** Defines `CustomerService.search(query: str) -> list[Customer]`.
   - **Data Flow:** CLI passes `query` to `CustomerService`, which validates length and delegates to `CustomerRepository.search_by_text(query)`.

5. **Linked GitHub Issue #1 Claims & Acceptance Criteria:**
   - AC-1: Implement strict parameter validation according to `SPEC.md`. *(Invalid premise: `SPEC.md` contains no such rule).*
   - AC-2: Return error exception when status filter is invalid.
   - AC-3: Add or update unit tests to cover invalid status filter scenario.

---

## Test Evidence
Automated test suite execution and statement coverage analysis were performed locally on branch `fix/customer-search-validation`:

### 1. Test Suite Execution (`pytest -v`)
```text
============================= test session starts ==============================
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/giuseph/Documents/Projects/ada-05-spec-driven-feature
configfile: pyproject.toml
testpaths: tests
plugins: cov-7.1.0
collected 32 items

tests/test_cli.py::test_cli_successful_search PASSED                     [  3%]
tests/test_cli.py::test_cli_no_results PASSED                            [  6%]
tests/test_cli.py::test_cli_short_query_error PASSED                     [  9%]
tests/test_cli.py::test_cli_whitespace_query_error PASSED                [ 12%]
tests/test_cli.py::test_cli_no_args_error PASSED                         [ 15%]
tests/test_cli.py::test_cli_subprocess_invocation PASSED                 [ 18%]
tests/test_cli.py::test_cli_subprocess_invocation_validation_error PASSED [ 21%]
tests/test_models.py::test_customer_instantiation PASSED                 [ 25%]
tests/test_models.py::test_customer_equality PASSED                      [ 28%]
tests/test_models.py::test_validation_error PASSED                       [ 31%]
tests/test_repository.py::test_repository_default_seed_data PASSED       [ 34%]
tests/test_repository.py::test_repository_custom_seed_data PASSED        [ 37%]
tests/test_repository.py::test_search_partial_match_by_name PASSED       [ 40%]
tests/test_repository.py::test_search_partial_match_by_email PASSED      [ 43%]
tests/test_repository.py::test_search_case_insensitivity PASSED          [ 46%]
tests/test_repository.py::test_search_with_leading_and_trailing_whitespace PASSED [ 50%]
tests/test_repository.py::test_search_no_matches_returns_empty_list PASSED [ 53%]
tests/test_repository.py::test_search_empty_or_whitespace_returns_empty_list PASSED [ 56%]
tests/test_repository.py::test_search_max_results_limit PASSED           [ 59%]
tests/test_repository.py::test_find_by_query_alias PASSED                [ 62%]
tests/test_service.py::test_service_successful_search_by_name PASSED     [ 65%]
tests/test_service.py::test_service_successful_search_by_email PASSED    [ 68%]
tests/test_service.py::test_service_search_with_padding_whitespace PASSED [ 71%]
tests/test_service.py::test_service_non_existent_query_returns_empty_list PASSED [ 75%]
tests/test_service.py::test_service_short_query_raises_validation_error PASSED [ 78%]
tests/test_service.py::test_service_short_query_with_whitespace_raises_validation_error PASSED [ 81%]
tests/test_service.py::test_service_empty_query_raises_validation_error PASSED [ 84%]
tests/test_service.py::test_service_whitespace_only_query_raises_validation_error PASSED [ 87%]
tests/test_service.py::test_service_none_query_raises_validation_error PASSED [ 90%]
tests/test_service.py::test_service_custom_repository_injection PASSED   [ 93%]
tests/test_service.py::test_service_performance_with_1000_records PASSED [ 96%]
tests/test_setup.py::test_package_import PASSED                          [100%]

============================== 32 passed in 0.12s ==============================
```

### 2. Statement Coverage Analysis (`pytest --cov=src --cov-report=term-missing`)
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
```

### 3. Key Test Evidence Findings:
- **Zero New Tests Added:** Diff inspection shows 0 test files modified or added in this branch.
- **Coverage Regression:** `src/service.py` statement coverage dropped from **100%** on `main` to **94%** on `fix/customer-search-validation`.
- **Missed Line 29:** The newly added `raise ValidationError(...)` on invalid status in `src/service.py` is completely untested.
- **Broken Acceptance Criterion 3 of Issue #1:** Issue #1 specifically mandated adding/updating unit tests for invalid status filtering; the PR completely omitted this requirement.

---

## MUST FIX

### RF-01
Requirement / AC: `AGENTS.md` (*"Do not invent business requirements"*, *"Read REQUIREMENTS.md before implementing"*, *"Read SPEC.md before implementing"*), `REQUIREMENTS.md` (Q-02), and `SPEC.md`
File: `src/service.py:9-10, 14, 27-31`
Evidence:
In `src/service.py`:
```python
VALID_STATUSES = {"ACTIVE", "INACTIVE", "PENDING"}
...
def search(self, query: str, status: str | None = None) -> list[Customer]:
...
    # Cambio para solucionar el Issue #1: Validación de estado según SPEC.md
    if status is not None and status.upper() not in self.VALID_STATUSES:
        raise ValidationError(
            f"Invalid status '{status}'. Must be one of: {', '.join(sorted(self.VALID_STATUSES))}"
        )
```
Problem:
This modification introduces an unapproved, invented business requirement. The author implemented this change to address GitHub Issue #1, which claimed that `SPEC.md` (*"Sección 3"*) required status filtering constrained to `ACTIVE`, `INACTIVE`, and `PENDING`. However, `SPEC.md` contains no such section or requirement, and `REQUIREMENTS.md` Q-02 explicitly clarifies that inactive/deleted statuses are not in scope because all records are active. Furthermore, `results/agent-report.md` documented that customer status filtering had already been evaluated and intentionally rejected during specification review. Merging this PR establishes an unauthorized domain rule in direct violation of `AGENTS.md`.
Recommended next step:
Reject PR #2 and revert the status validation changes in `src/service.py`. Close Issue #1 as invalid / out of scope. If status filtering is desired by stakeholders in the future, it must first be formally specified, approved, and added to `REQUIREMENTS.md` and `SPEC.md`.

### RF-02
Requirement / AC: `AGENTS.md` (*"Add tests for new behavior"*), NFR-02 (Test Coverage $\ge 90\%$), and Issue #1 AC-3 (*"Agregar o actualizar las pruebas unitarias para cubrir el escenario de filtro de estado inválido"*)
File: `src/service.py:28-31` and `tests/test_service.py`
Evidence:
Running `pytest --cov=src --cov-report=term-missing` demonstrates that line 29 of `src/service.py` is missed:
```text
src/service.py         18      1    94%   29
```
Git diff shows 0 changes in the `tests/` directory (`git diff main..fix/customer-search-validation -- tests/` returns empty).
Problem:
New code introducing conditional branching and validation logic was merged into `src/service.py` without any automated test evidence. This introduces untested production code, degrades statement coverage on `src/service.py` from 100% to 94%, and fails AC-3 of the issue the PR claims to close.
Recommended next step:
If this feature were ever approved, comprehensive unit tests must be added to `tests/test_service.py` covering: (1) invalid status raising `ValidationError`, (2) valid status accepted, (3) case-insensitivity (`"active"` vs `"ACTIVE"`), and (4) `status=None` preserving default behavior. Since the feature is unauthorized (RF-01), the recommended resolution is reverting lines 9, 14, and 27-31 to restore 100% clean test coverage.

### RF-03
Requirement / AC: `SPEC.md` (Domain Model & Scope) and `ARCHITECTURE.md` (Module Responsibilities)
File: `src/service.py:14, 28-33`, `src/models.py:1-9`, `src/repository.py:1-42`
Evidence:
In `src/service.py`:
```python
def search(self, query: str, status: str | None = None) -> list[Customer]:
    ...
    if status is not None and status.upper() not in self.VALID_STATUSES:
        raise ValidationError(...)

    return self._repository.search_by_text(trimmed_query)
```
In `src/models.py`:
```python
@dataclass
class Customer:
    id: str
    name: str
    email: str
```
In `src/repository.py`:
`search_by_text(self, query: str) -> list[Customer]` only filters on `name` and `email`. It does not accept or filter by `status`.
Problem:
The PR creates dead code and a misleading contract. If a client invokes `service.search("john", status="INACTIVE")`, the status passes validation, but the method executes `search_by_text(trimmed_query)` without filtering. All matching customer records are returned regardless of status, and the `Customer` entity does not even possess a `status` field. The implementation validates a parameter that is immediately discarded, giving callers a false sense of filtering functionality.
Recommended next step:
Revert the `status` parameter from `CustomerService.search()`. Full architectural alignment across models, repositories, and interfaces must occur if status filtering is officially adopted in the future.

---

## SHOULD FIX

### RF-04
Requirement / AC: Code Quality & Robustness / Error Handling
File: `src/service.py:28`
Evidence:
```python
if status is not None and status.upper() not in self.VALID_STATUSES:
```
Problem:
The check invokes `.upper()` directly on `status` without verifying that `status` is an instance of `str`. If a caller passes a non-string object (such as an integer `status=1`, a list, or a non-string enum), Python will raise an unhandled `AttributeError: 'int' object has no attribute 'upper'` instead of a controlled domain `ValidationError`.
Recommended next step:
If status validation is implemented in the future, validate type safety first:
```python
if status is not None:
    if not isinstance(status, str) or status.strip().upper() not in self.VALID_STATUSES:
        raise ValidationError(...)
```

### RF-05
Requirement / AC: `ARCHITECTURE.md` (Interfaces & CLI Entry Point)
File: `ARCHITECTURE.md:40` and `src/cli.py:1-42`
Evidence:
`ARCHITECTURE.md` documents:
```markdown
## Interfaces
- CustomerService.search(query: str) -> list[Customer]
```
In `src/cli.py`, the CLI parser only accepts:
```python
parser.add_argument("query", help="Search query string...")
```
Problem:
The PR changes the signature of `CustomerService.search` without updating `ARCHITECTURE.md`. Moreover, `src/cli.py` does not expose any `--status` flag, making the newly added parameter inaccessible to terminal users and decoupling the CLI interface from the service layer.
Recommended next step:
Maintain architectural coherence. If the service signature is modified, update `ARCHITECTURE.md` and expose the corresponding CLI flags in `src/cli.py`. Reverting the unapproved parameter in `src/service.py` resolves this discrepancy.

### RF-06
Requirement / AC: Repository Hygiene / Clean Git Tree
File: `.DS_Store`
Evidence:
`git diff --stat main..fix/customer-search-validation` shows `.DS_Store` added as a tracked binary file (10,244 bytes).
Problem:
Platform-specific metadata file `.DS_Store` was committed to the repository, polluting version control history and diffs.
Recommended next step:
Add `.DS_Store` to `.gitignore`, remove the file from git tracking using `git rm --cached .DS_Store`, and commit the removal.

---

## OPTIONAL

### RF-07
Requirement / AC: Input Normalization Consistency
File: `src/service.py:28`
Evidence:
The query string is normalized with `.strip()` (`trimmed_query = query.strip()`), but `status.upper()` does not strip leading or trailing whitespace.
Problem:
An input such as `status=" ACTIVE "` fails validation because `" ACTIVE "` is not in `VALID_STATUSES`.
Recommended next step:
Normalize status inputs using `status.strip().upper()` for consistency with query normalization.

### RF-08
Requirement / AC: Branch Scope / Separation of Concerns
File: `docs/ENGINEERING_ANALYSIS.md`, `docs/ISSUE_ANALYSIS.md`, `docs/MCP_GITHUB_PERMISSION_REVIEW.md`, `docs/MCP_GITHUB_TOOL_INVENTORY.md`, `docs/PR_ANALYSIS.md`, `docs/TRACEABILITY_MATRIX.md`, `results/github-mcp-review.md`
Evidence:
The branch contains multiple analytical documentation files alongside the single code change in `src/service.py`.
Problem:
While these analysis artifacts provide valuable context, committing internal audit and MCP analysis reports onto a feature branch dilutes the focus of the pull request.
Recommended next step:
Keep feature branches focused strictly on implementation code and tests. Maintain architectural audit reports in dedicated documentation branches or folders.

---

## Open Questions
1. **Product Management Clarification:** Does the product team plan to introduce customer status lifecycle management (`ACTIVE`, `INACTIVE`, `PENDING`) in an upcoming milestone?
   - If **NO**: Issue #1 and PR #2 should be closed immediately as invalid / out of scope.
   - If **YES**: A formal change request must update `REQUIREMENTS.md` and `SPEC.md` first, followed by coordinated updates to `Customer` entity, seed data in `CustomerRepository`, service filtering, CLI flags, and unit tests.

---

## Final Review Summary
- **MUST FIX count:** 3
- **SHOULD FIX count:** 3
- **OPTIONAL count:** 2
- **Human decision required:** YES

### Overall Readiness Verdict:
**NOT READY (REJECT / DO NOT MERGE)**

The branch `fix/customer-search-validation` cannot be merged into `main` in its current state. It violates the core project principle of Spec-Driven Development by implementing an unapproved business requirement from an invalid issue, degrades test coverage by omitting automated unit tests, and introduces dead code that does not actually filter customers by status.
