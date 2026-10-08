# AI Usage Log — Customer Search Feature

This log documents the AI pair-programming interactions, architectural decisions, human oversight, task progressions, and verification results throughout the implementation of the Customer Search feature.

---

## Session Summary

- **Development Paradigm**: Specification-driven development guided by `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, and strict `AGENTS.md` instructions.
- **Model / Agent**: Gemini 3.8 Flash / Antigravity Agent.
- **Outcome**: All 6 tasks (T-01 to T-06) successfully completed with 100% test coverage and zero regression.

---

## Key Human-AI Decision Entries (Spec-Driven Workflow)

### Entry 1: Specification & Boundary Definition (Spec Phase)
- **AI Proposal**: The AI suggested adding pagination parameters (`page`, `limit`) and an `is_active` filter flag to `CustomerRepository.search_by_text()`.
- **Human Decision / Review**: **Rejected**. The requirement (`REQUIREMENTS.md`) and specification (`SPEC.md`) only mandate partial text search with a hard cap of 50 results (`MAX_RESULTS = 50`). Adding pagination would violate the YAGNI principle and introduce unrequested complexity.
- **Impact on Product**: Enforced strict adherence to scope; kept repository methods lean and matching `SPEC.md`.

### Entry 2: Exception Strategy & Error Handling (Design Phase)
- **AI Proposal**: The AI proposed catching validation errors in `CustomerService` and returning an empty list `[]` when the search query was invalid or shorter than 2 characters.
- **Human Decision / Review**: **Corrected**. According to `SPEC.md`, queries with `len(trimmed_query) < 2` or empty strings must explicitly raise a custom `ValidationError`.
- **Impact on Product**: Created `src/exceptions.py` with `ValidationError` and ensured proper exception throwing in `src/service.py`.

### Entry 3: CLI Error Output & Exit Codes (Implementation Phase)
- **AI Proposal**: The AI initially printed error messages for `ValidationError` using standard `print()` (stdout) and exited with code `0`.
- **Human Decision / Review**: **Corrected**. Standard CLI conventions and `SPEC.md` require printing error messages to `sys.stderr` and exiting with a status code of `1` without dumping internal traceback logs.
- **Impact on Product**: Refactored `src/cli.py` to direct error outputs to `stderr` and set `sys.exit(1)`.

### Entry 4: NFR-01 Performance Testing & Data Fixtures (Testing Phase)
- **AI Proposal**: The AI created a unit test for performance using a mock repository containing only 10 static records.
- **Human Decision / Review**: **Adjusted**. Requirement `NFR-01` specifies response times under 200ms when querying across at least 1,000 customer records.
- **Impact on Product**: Implemented a dynamic dataset fixture generating 1,000 `Customer` instances in `tests/test_service.py` with `time.perf_counter()` assertion.

---

## Chronological Task Progression

### Task 1: T-01 Project Setup
- **Prompt**:
  > Read REQUIREMENTS.md, SPEC.md, ARCHITECTURE.md, TASKS.md, AGENTS.md. Inspect repository, identify next incomplete task, propose approach, implement T-01, run tests, report.
- **Actions & Decisions**:
  - Inspected fresh repository containing only documentation.
  - Initialized Python virtual environment (`.venv`) and installed `pytest` + `pytest-cov`.
  - Created `requirements.txt` and `pyproject.toml` with `pythonpath = ["."]` and `testpaths = ["tests"]`.
  - Created package initializers `src/__init__.py` and `tests/__init__.py`.
  - Added `.gitignore` to prevent tracking of `.venv/`, `.pytest_cache/`, `__pycache__/`, `.coverage`.
  - Added smoke test in `tests/test_setup.py` ensuring clean pytest discovery.
- **Verification**: `pytest` executed with 1 passed test (exit code 0).

### Task 2: T-02 Domain Model
- **Prompt**:
  > Proceed with T-02 Domain model. Propose approach, implement Customer dataclass and ValidationError, add tests in `tests/test_models.py`, run pytest.
- **Actions & Decisions**:
  - Implemented `Customer` dataclass in `src/models.py` with `id`, `name`, and `email` string fields.
  - Implemented custom `ValidationError` in `src/exceptions.py` inheriting from standard `Exception`.
  - Added unit tests in `tests/test_models.py` verifying instantiation, field integrity, dataclass equality, and exception message propagation.
- **Verification**: `pytest tests/test_models.py` passed (3 tests). Full suite passed (4 tests).

### Task 3: T-03 Search Logic
- **Prompt**:
  > Proceed with T-03 Search logic. Implement `CustomerRepository` in `src/repository.py` with seed data and search filtering logic (case-insensitive partial match on name or email). Add unit tests in `tests/test_repository.py`.
- **Actions & Decisions**:
  - Implemented `CustomerRepository` in `src/repository.py` initialized with seed dataset reflecting test scenarios (`"John Doe"`, `"Johnny Smith"`, `"Alice Wonderland"`, `"Alex Johnson"`, `"Jane Doe"`, `"Bob Builder"`, `"Diana Prince"`, `"Ana Garcia"`).
  - Provided support for custom dataset injection in constructor for decoupled testing.
  - Implemented `search_by_text(query)` applying whitespace trimming, lowercase partial matching against `name` and `email`, and capping results to `MAX_RESULTS = 50`.
  - Implemented `find_by_query` interface alias and `get_all` utility.
  - Added 10 unit tests in `tests/test_repository.py` covering seed retrieval, partial matches, case insensitivity, whitespace queries, empty queries, non-matching queries, and max results limit.
- **Verification**: `pytest tests/test_repository.py` passed (10 tests). Full suite passed (14 tests), 100% coverage.

### Task 4: T-04 Validation and Errors
- **Prompt**:
  > Proceed with T-04 Validation and errors. Implement `CustomerService` in `src/service.py` ensuring whitespace is stripped before checking minimum length (len < 2). Delegate valid queries to repository. Add unit tests in `tests/test_service.py`.
- **Actions & Decisions**:
  - Implemented `CustomerService` in `src/service.py`.
  - Applied strict validation sequencing:
    1. Null check / empty check: query stripped of leading and trailing whitespace. If empty, raises `ValidationError("Search query cannot be empty.")`.
    2. Length check: if `len(trimmed_query) < 2`, raises `ValidationError("Search query must be at least 2 characters long.")`.
  - Forwarded validated trimmed query to `repository.search_by_text()`.
  - Added 10 unit tests in `tests/test_service.py` covering valid name/email searches, whitespace padding, non-existent queries, short queries, empty/whitespace-only queries, None query, and dependency injection.
- **Verification**: `pytest --cov=src` passed (24 tests), 100% coverage.

### Task 5: T-05 Tests & Performance
- **Prompt**:
  > Proceed with T-05 Tests. Implement NFR-01 performance test (<200 ms with 1,000 records). Implement CLI entry point in `src/cli.py`. Add CLI integration tests in `tests/test_cli.py`. Run `pytest --cov=src`.
- **Actions & Decisions**:
  - Added performance test `test_service_performance_with_1000_records` in `tests/test_service.py` evaluating elapsed time with `time.perf_counter()`.
  - Implemented `src/cli.py` with `argparse`, formatting structured output on stdout for matches, friendly `"No customers found."` output for empty results, and catching `ValidationError` to print to `stderr` with exit code `1` (without stack traces).
  - Created `tests/test_cli.py` covering successful output, no results, validation errors (stderr + exit code 1), and subprocess invocations.
- **Verification**: `pytest --cov=src` passed (32 tests), 100% total coverage across all source files.

### Task 6: T-06 Documentation
- **Prompt**:
  > Update `README.md` with overview, setup, execution, testing. Create `AI_USAGE_LOG.md`. Mark tasks in `TASKS.md` as complete. Run `pytest --cov=src` final verification.
- **Actions & Decisions**:
  - Generated comprehensive `README.md` with CLI examples and testing guides.
  - Documented complete interaction and architectural history in `AI_USAGE_LOG.md`.
  - Updated `TASKS.md` with completion status for all tasks T-01 through T-06.
  - Verified green test suite and test coverage.

---

# AI Usage Log — ADA-06

| Entrada | Etapa | Evidencia / Descripción |
| :---: | :--- | :--- |
| **1** | **MCP Configuration** | Se configuró el servidor `github-readonly` mediante un Fine-Grained PAT de mínimo privilegio limitado a `Giuseph-CT/ada-05-spec-driven-feature` con permisos excluyentes de lectura (`Contents`, `Issues`, `Pull requests`). El estudiante tomó la decisión de deshabilitar explícitamente cualquier toolset de escritura para garantizar el aislamiento operativo. |
| **2** | **Repository Analysis** | El agente utilizó las herramientas `repository_read` y `issue_read` para inspeccionar la estructura del proyecto y leer el archivo `SPEC.md`. El estudiante validó manualmente que el agente identificara correctamente los componentes en capas (`cli`, `service`, `repository`) y la tasa de cobertura de pruebas inicial. |
| **3** | **Issue / PR Analysis** | El agente detectó que la Issue #1 citaba una sección de `SPEC.md` inexistente y que el PR #2 introducía código muerto sin pruebas. El estudiante verificó ejecutando `pytest` localmente que la cobertura de pruebas efectivamente caía en la rama del PR #2, confirmando el hallazgo del agente. |
| **4** | **Permission / Security Review** | Se evaluó el riesgo de *Prompt Injection* y fuga de credenciales. El estudiante inspeccionó el inventario de herramientas disponible en la sesión MCP, confirmando la ausencia total de capacidades de escritura (`create_issue`, `comment_pr`, etc.) y ratificó la coherencia entre el Token PAT, la política MCP y la autenticación. |

---

## AI Usage Log (ADA-07)

### Stage 1: Workflow observation
- **Prompt/Interacción:** Análisis manual guiado por IA del diff de la rama `fix/customer-search-validation`.
- **Decisión Humana:** Se aceptó el orden de pasos (diff -> pytest -> clasificación -> reporte) y se descartó la auto-aprobación del PR.

### Stage 2: Skill authoring
- **Prompt/Interacción:** Ajuste del frontmatter y descripción de `SKILL.md`.
- **Decisión Humana:** Se forzó el patrón de nombres con guiones medios (`reviewing-pull-requests`) para asegurar compatibilidad con el linter de VS Code.

### Stage 3: Script/reference design
- **Prompt/Interacción:** Separación de la lógica de evaluación y plantillas.
- **Decisión Humana:** Se movió la guía de severidad a `references/severity_guide.md` y el checklist a `references/review_checklist.md` aplicando Progressive Disclosure para mantener compacto el `SKILL.md`.

### Stage 4: Evaluation/refinement
- **Prompt/Interacción:** Validación del artefacto `results/pr-readiness-review.md`.
- **Decisión Humana:** Se verificó que `validate_review_report.py` retornara exit code 0 únicamente cuando las secciones estandarizadas estuvieran presentes.

### Stage 5: Third-party audit
- **Prompt/Interacción:** Inspección del script de validación determinista antes de su ejecución.
- **Decisión Humana:** Se validó que el script fuera seguro, de solo lectura sobre el reporte local y sin llamadas de red o comandos de modificación.

### Stage 6: Professional skill comparison
- **Prompt/Interacción:** Comparación entre dar instrucciones generales vs encapsular know-how en una Agent Skill.
- **Decisión Humana:** Se confirmó que separar triggers, scripts deterministas y conocimiento especializado en `references/` reduce sustancialmente las alucinaciones del LLM y garantiza reportes consistentes.