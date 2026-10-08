# Engineering Analysis: Giuseph-CT/ada-05-spec-driven-feature

This is a read-only architectural and engineering analysis of the repository [Giuseph-CT/ada-05-spec-driven-feature](https://github.com/Giuseph-CT/ada-05-spec-driven-feature) conducted exclusively using the GitHub MCP Server with scope strictly limited to this repository.

---

## 1. Repository Purpose

The repository implements a **Customer Search Feature** using a strict **Spec-Driven Development methodology** in Python.

* **Primary Objective:** Provide a reliable, validated, case-insensitive partial substring search mechanism to locate customer records by name or email via both a local CLI entry point and an importable domain service module.
* **Methodology & Traceability:** The repository strictly follows a spec-first workflow where business needs in `REQUIREMENTS.md` map directly to formal acceptance criteria and technical contracts in `SPEC.md`, architectural specifications in `ARCHITECTURE.md`, and verifiable execution tasks in `TASKS.md`.
* **Scope Boundaries:** Operates on an in-memory repository without external database drivers or HTTP framework dependencies (REST APIs are explicitly designated out of scope for this iteration).

---

## 2. Main Directories and Important Files

ada-05-spec-driven-feature/
├── docs/
│   └── traceability.md          # Traceability matrix mapping FRs/NFRs to tests & files
├── results/
│   └── agent-report.md          # Human-AI review, audit notes, and DoD verification
├── src/
│   ├── init.py
│   ├── cli.py                   # Terminal CLI interface (argparse, exit code handling)
│   ├── exceptions.py            # ValidationError custom domain exception
│   ├── models.py                # Customer dataclass entity definition
│   ├── repository.py            # In-memory customer repository and seed data
│   └── service.py               # CustomerService validation and search orchestrator
├── tests/
│   ├── init.py
│   ├── test_cli.py              # CLI integration tests (stdout, stderr, exit codes)
│   ├── test_models.py           # Customer model instantiation tests
│   ├── test_repository.py       # In-memory substring filtering & case-insensitivity tests
│   ├── test_service.py          # Validation rules, error handling & performance tests
│   └── test_setup.py            # Pytest environment verification
├── AGENTS.md                    # Agent guardrails and project ground rules
├── AI_USAGE_LOG.md              # Interaction audit log recording prompts & human review
├── ARCHITECTURE.md              # 3-layer architecture, sequence diagram & interfaces
├── pyproject.toml               # Build system and pytest configuration
├── README.md                    # Setup, execution guide and CLI usage examples
├── REQUIREMENTS.md              # Business requirements (FR-01..FR-06, NFR-01..NFR-03)
├── requirements.txt             # Direct dependencies (pytest, pytest-cov)
├── SPEC.md                      # Technical contract, search/validation rules, test scenarios
└── TASKS.md                     # Task breakdown (T-01 through T-06)


---

## 3. Application Entry Point(s)

1. **Command-Line Interface (CLI):**
   * **File:** `src/cli.py` via function `main(argv=None)`.
   * **Invocation:**
     ```bash
     python -m src.cli "<query>"
     ```
   * **Behavior:** Parses a single positional query argument using `argparse`.
     * On match: Prints formatted customer rows to `stdout` and returns exit code `0`.
     * On empty results: Prints `"No customers found."` to `stdout` and returns exit code `0`.
     * On validation failure: Catches `ValidationError`, prints `Error: <message>` to `sys.stderr`, and returns exit code `1`.

2. **Programmatic / Service Entry Point:**
   * **File:** `src/service.py` via `CustomerService.search(query: str)`.
   * **Behavior:** Allows external Python consumers or integration harnesses to instantiate `CustomerService` (with optional dependency-injected `CustomerRepository`) to validate and execute search queries returning `list[Customer]`.

---

## 4. Main Components / Modules

The codebase enforces a clean **3-layer separation of concerns**:

* **`Customer` (`src/models.py`):** Standard Python dataclass containing `id: str`, `name: str`, and `email: str`.
* **`ValidationError` (`src/exceptions.py`):** Custom exception for domain and input validation failures.
* **`CustomerRepository` (`src/repository.py`):** Maintains in-memory records (seeded from `DEFAULT_CUSTOMERS`). Performs case-insensitive substring matching against `name` and `email` fields. Limits output to a maximum of 50 records (`MAX_RESULTS = 50`).
* **`CustomerService` (`src/service.py`):** Coordinates business logic:
  * Validates query is not `None` and not empty after `.strip()`.
  * Enforces minimum query length of 2 characters (`len(trimmed) >= 2`).
  * Calls `CustomerRepository.search_by_text()`.
* **`cli.py` (`src/cli.py`):** Handles argument parsing, standard I/O streams, and process exit code propagation.

---

## 5. Test Organization

Tests are consolidated in the `tests/` directory using `pytest`:

* `test_setup.py`: Baseline test confirming pytest is correctly operational.
* `test_models.py`: Tests creation, attribute values, and equality semantics of the `Customer` dataclass.
* `test_repository.py`: Validates case-insensitivity, partial matching on name/email, query trimming, `MAX_RESULTS` truncation at 50 records, and repository initialization.
* `test_service.py`: Tests validation rules (empty query, query length < 2, whitespace-only, `None`), repository dependency injection, and performance requirement NFR-01 (verifies that searching 1,000 synthetic records executes in < 200 ms).
* `test_cli.py`: Tests CLI invocations capturing stdout/stderr via `capsys` and validating exit code 0 on success and exit code 1 on `ValidationError`.
* **Coverage Status:** 32 automated tests with 100% statement coverage on all modules in `src/`.

---

## 6. Relevant Documentation

* **`REQUIREMENTS.md`:** User story, functional requirements (FR-01 to FR-06), and non-functional requirements (NFR-01 to NFR-03).
* **`SPEC.md`:** Detailed technical contract specifying input validation constraints, search rules, domain model, and acceptance criteria.
* **`ARCHITECTURE.md`:** Architectural patterns, sequence diagram, module boundaries, interfaces, and trade-offs.
* **`traceability.md`:** Complete requirement-to-code-to-test matrix.
* **`TASKS.md`:** Linear progression of implementation tasks (T-01 to T-06).
* **`AGENTS.md`:** Explicit agent governance rules (e.g., *"Do not invent business requirements"*, *"Do not modify REQUIREMENTS.md or SPEC.md to make tests pass"*).
* **`agent-report.md`:** Audit report reflecting on design decisions, human interventions, and lessons learned.

---

## 7. Potential Areas Affected by the Selected Issue / PR

Through GitHub inspection, we identified Issue #1 and its associated Pull Request #2:

| Item | Identifier / Branch | Title | State |
| :--- | :--- | :--- | :--- |
| **Issue #1** | `#1` | Bug: El módulo de búsqueda de clientes no respeta la especificación de filtros en SPEC.md | OPEN |
| **PR #2** | `#2` (`fix/customer-search-validation`) | fix: agregar validacion de status segun SPEC.md | OPEN |

### Detailed Findings & Impact Analysis

#### 1. Specification Mismatch (Hallucinated Requirement)
* **Claim in Issue #1:** Claims that according to `SPEC.md` (*"Sección 3: Criterios de Búsqueda"*), customer status filtering must accept only `ACTIVE`, `INACTIVE`, `PENDING` and return `400 Bad Request` otherwise.
* **Reality in SPEC.md and REQUIREMENTS.md:**
  * Neither `SPEC.md` nor `REQUIREMENTS.md` contains a customer status filter or HTTP 400 Bad Request errors.
  * In `REQUIREMENTS.md:25`, Question Q-02 explicitly clarifies: *"Should deleted/inactive customers be included in search results? (No, all in-memory seed records are active)."*
  * In `agent-report.md:70`, the human audit explicitly documented:
    > *"¿Se inventaron reglas? No. Durante la generación inicial, la IA propuso incluir paginación y filtros por estado de cliente, pero fueron descartados en la revisión humana por no pertenecer al alcance de la especificación."*
  * Therefore, Issue #1 is an invalid bug report attempting to introduce an unapproved requirement that violates the project rule: *"Do not invent business requirements"* (`AGENTS.md:11`).

#### 2. Areas Impacted by PR #2
* **`src/service.py`:**
  * PR #2 modifies `CustomerService.search()` to accept `status: str | None = None` and adds validation against `VALID_STATUSES = {"ACTIVE", "INACTIVE", "PENDING"}`.
* **Architectural & Design Inconsistencies Introduced:**
  * **Model Inconsistency:** The `Customer` dataclass has no `status` field (`id`, `name`, `email` only).
  * **Repository Inconsistency:** The repository `CustomerRepository` has no logic to filter by status, rendering the parameter ineffective after validation.
  * **CLI Inconsistency:** `src/cli.py` does not expose any `--status` CLI argument, making the feature inaccessible from the primary application entry point.
  * **Testing & Coverage Regression:** PR #2 modified code in `src/service.py` without adding any tests to `tests/test_service.py` covering the new branches, which breaks the 100% test coverage and fails acceptance criteria.

---

## GitHub MCP Capabilities Used

In compliance with instructions, every GitHub MCP operation was restricted to `Giuseph-CT/ada-05-spec-driven-feature`:

1. `search_repositories`: Inspected repository metadata, default branch (`main`), repository settings, and open issue counts.
2. `list_branches`: Identified repository branches (`main`, `fix/customer-search-validation`).
3. `list_issues`: Retrieved active issues on the repository (found Issue #1).
4. `issue_read`: Queried the complete body, author metadata, acceptance criteria, and linked PR references for Issue #1.
5. `list_pull_requests`: Retrieved all pull requests (found PR #2).
6. `pull_request_read`:
   * Method `get`: Inspected PR #2 metadata and base/head branches.
   * Method `get_files`: Listed modified files (`src/service.py`).
   * Method `get_diff`: Extracted the exact unified patch for PR #2.
7. `list_commits` & `get_commit`: Inspected recent commit history and specific commit `69564ae` on branch `fix/customer-search-validation`.
8. `get_file_contents`: Listed directory structures (`/`, `src/`, `tests/`, `docs/`, `results/`) and inspected file contents (`README.md`, `SPEC.md`, `REQUIREMENTS.md`, `ARCHITECTURE.md`, `TASKS.md`, `src/service.py`, `src/cli.py`, `src/repository.py`, `src/models.py`, `src/exceptions.py`, `tests/test_service.py`, `docs/traceability.md`).
9. `search_code`: Queried code index symbols within the repository scope.