# Engineering Analysis: Issue #1 (Giuseph-CT/ada-05-spec-driven-feature)

* **Issue Reference:** [Issue #1: Bug: El módulo de búsqueda de clientes no respeta la especificación de filtros en SPEC.md](https://github.com/Giuseph-CT/ada-05-spec-driven-feature/issues/1)
* **State:** OPEN | **Author:** Giuseph-CT | **Scope:** `Giuseph-CT/ada-05-spec-driven-feature` (Read-Only)

---

## 1. Problem / Requested Behavior

* **Facts directly from the Issue:**
  * **Title:** *"Bug: El módulo de búsqueda de clientes no respeta la especificación de filtros en SPEC.md"*
  * **Reported Behavior:** The issue states that in the customer search module (`customer_search`), passing an invalid value in the `status` filter parameter (such as `STATUS_INVALID` or `INVALID_STATUS`) results in the system failing to validate the input against the specification, returning an HTTP `200 OK` status with an empty list (`[]`).
  * **Reproduction Steps:**
    1. Execute customer search passing `status = "INVALID_STATUS"`.
    2. Observe the response returned by the function/endpoint.

* **Engineering Inferences & Codebase Verification:**
  * The actual codebase on `main` does not expose a function named `customer_search`, but rather the class `CustomerService.search(query: str)` and the CLI entry point `src/cli.py`.
  * On `main`, calling `CustomerService.search()` with a `status` keyword argument raises a Python `TypeError` (*unexpected keyword argument 'status'*), rather than returning `200 OK` or `[]`.
  * There are no HTTP REST endpoints in this codebase; it is strictly a local Python module and CLI application.

---

## 2. Expected Behavior

* **Facts directly from the Issue:**
  * According to the issue's reference to `SPEC.md` (*"Sección 3: Criterios de Búsqueda"*), the customer `status` filter parameter must only accept three specific values: `ACTIVE`, `INACTIVE`, and `PENDING`.
  * When receiving any value outside this set, the system must validate the input and either raise a validation exception or return an HTTP `400 Bad Request` error.

* **Engineering Inferences & Codebase Verification:**
  * The issue mixes HTTP semantics (`400 Bad Request`) with Python library semantics (*lanzar una excepción de validación*).
  * In this application's architecture (`ARCHITECTURE.md`), the domain standard for invalid inputs is raising a `ValidationError` in `src/service.py`, which `src/cli.py` intercepts to output to `sys.stderr` with exit code `1`.
  * The claim that `SPEC.md` specifies this expected behavior is **factually inaccurate** (see Section 8).

---

## 3. Acceptance Information Explicitly Present

* **Facts directly from the Issue:**
  Under the section *"Criterios de Aceptación"*, the issue lists three explicit checklist items:
  1. [ ] Implementar la validación estricta de parámetros según `SPEC.md`.
  2. [ ] Retornar el código/excepción de error correspondiente cuando el filtro sea inválido.
  3. [ ] Agregar o actualizar las pruebas unitarias para cubrir el escenario de filtro de estado inválido.

* **Engineering Inferences:**
  * **Criterion 1** assumes `SPEC.md` defines this validation rule, creating a blocking circular dependency because `SPEC.md` contains no such rule.
  * **Criterion 2** leaves ambiguous whether the target contract is an HTTP response code, a CLI exit code, or a Python exception.
  * **Criterion 3** requires unit test coverage for invalid status inputs. *(Note: PR #2, which attempted to resolve this issue, failed to add any unit tests).*

---

## 4. Ambiguities or Missing Information

* **Engineering Inferences:**
  1. **Fictitious Specification Section:** The issue references *"SPEC.md (Sección 3: Criterios de Búsqueda)"*. No such section or wording exists in `SPEC.md`.
  2. **Protocol & Interface Discrepancy:** The issue references HTTP responses (`400 Bad Request`, `200 OK`) and a generic endpoint, but the project is strictly a command-line script and local Python library. HTTP REST endpoints are explicitly designated **Out of Scope** in `SPEC.md` (lines 20–24).
  3. **Case Sensitivity & Normalization:** The issue specifies values `ACTIVE`, `INACTIVE`, `PENDING`, but does not clarify whether inputs like `"active"` or `" Active "` should be normalized via `.strip().upper()` or rejected as invalid.
  4. **Functional Behavior of Valid Statuses:** The issue only describes what happens on an invalid status. It leaves completely undefined what should happen when a valid status is passed (e.g., Does the repository filter records? How are existing customers mapped to a status when the model has no `status` attribute?).
  5. **CLI Integration:** The issue does not specify whether a CLI flag (e.g., `--status`) must be exposed in `src/cli.py`.

---

## 5. Relevant Code Areas in the Repository

If this feature/change were to be incorporated, the following code areas would be directly impacted:

* **`src/service.py` (`CustomerService`):**
  * Requires updating `CustomerService.search()` to accept a `status: str | None = None` parameter.
  * Requires defining valid status values (`VALID_STATUSES = {"ACTIVE", "INACTIVE", "PENDING"}`) and raising `ValidationError`.
* **`src/models.py` (`Customer`):**
  * Currently contains only `id: str`, `name: str`, `email: str`. A `status: str` attribute would be needed to store and evaluate status.
* **`src/repository.py` (`CustomerRepository`):**
  * `DEFAULT_CUSTOMERS` seed data lacks status properties.
  * `search_by_text()` only filters on name and email; status filtering logic would need to be added.
* **`src/cli.py` (`main`):**
  * `argparse` configuration currently only accepts positional query. Requires `--status` option to be usable from CLI.
* **`src/exceptions.py`:**
  * Standard exception class `ValidationError` used for domain validation errors.

---

## 6. Existing Tests Related to the Issue

* **`tests/test_service.py`:**
  * Tests search query validation rules (`test_service_short_query_raises_validation_error`, `test_service_empty_query_raises_validation_error`, etc.).
  * **Status:** There are zero existing tests related to status, as it is not part of the current specification.
* **`tests/test_cli.py`:**
  * Tests CLI argument handling and stderr output for validation errors.
  * **Status:** No tests for any `--status` flag.
* **`tests/test_repository.py`:**
  * Tests in-memory matching by name and email.
  * **Status:** No tests for status-based filtering.

---

## 7. Risks or Edge Cases

* **Engineering Inferences:**
  1. **Direct Violation of Spec-Driven Rules in `AGENTS.md`:**
     * Project Rule: *"Do not invent business requirements."*
     * Project Rule: *"Do not modify REQUIREMENTS.md or SPEC.md to make tests pass."*
     * Project Rule: *"Stop and ask for clarification if requirements conflict."*
     * Implementing Issue #1 as written introduces an unapproved requirement that directly conflicts with the project's specification documents.
  2. **Incomplete / Disconnected Implementation Risk (demonstrated in PR #2):**
     * If validation is added to `CustomerService.search()` without updating `Customer`, `CustomerRepository`, and `src/cli.py`, the validation checks an argument that is subsequently ignored during search execution, creating dead logic.
  3. **Input Edge Cases for Status:**
     * Missing or `None` value (must be permitted to avoid breaking existing searches).
     * Case variants (`"active"` vs `"ACTIVE"`).
     * Trailing/leading whitespace (`" ACTIVE "`).
     * Non-string types passed programmatically.
  4. **Test Suite & Coverage Regression:**
     * Introducing conditional validation branches without comprehensive test coverage violates **NFR-02** ($\ge 90\%$ test coverage, currently at 100%).

---

## 8. Alignment with REQUIREMENTS.md and SPEC.md

* **Direct Facts from Project Documentation:**
  1. **`SPEC.md`:**
     * **Out of Scope (Lines 20–24):** Explicitly designates REST APIs out of scope:
       > *"HTTP REST API endpoints / FastAPI framework (reserved for future iterations)."*
     * **Domain Model (Lines 26–36):** Defines `Customer` exclusively with `id`, `name`, and `email`.
     * **Validation Rules (Lines 44–47):** Only contains rules for query length ($\ge 2$) and non-empty/whitespace query.
     * **Conclusion:** There is no status filter, no enum `ACTIVE`/`INACTIVE`/`PENDING`, and no *"Sección 3: Criterios de Búsqueda"*.
  2. **`REQUIREMENTS.md`:**
     * **Functional Requirements (FR-01 to FR-06):** Focus exclusively on name and email searching.
     * **Open Questions / Clarifications (Section Q-02, Line 25):**
       > *"Q-02: N/A - Should deleted/inactive customers be included in search results? (No, all in-memory seed records are active)."*
     * **Conclusion:** Customer status filtering was deliberately considered and excluded from the feature requirements.
  3. **`results/agent-report.md` (Human Review Phase 10, Lines 69–71):**
     * The post-implementation audit explicitly notes:
       > *"¿Se inventaron reglas? No. Durante la generación inicial, la IA propuso incluir paginación y filtros por estado de cliente, pero fueron descartados en la revisión humana por no pertenecer al alcance de la especificación."*

---

## Conclusion

From a software engineering and spec-driven perspective:

* **Issue #1 is a hallucinated/invalid bug report.** It asserts the existence of a specification section and requirement that does not exist in `SPEC.md` or `REQUIREMENTS.md`, and was previously explicitly rejected during human review.
* Per the project governance rules in `AGENTS.md`, **this issue should not be implemented** without an official revision and formal sign-off on `REQUIREMENTS.md` and `SPEC.md`.