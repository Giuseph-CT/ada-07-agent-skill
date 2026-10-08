# Tasks

## T-01 Project setup [Completed]
- Goal: Create project directory structure, initial files, and pytest setup.
- Files: `src/__init__.py`, `tests/__init__.py`, `pyproject.toml` or `requirements.txt`.
- Acceptance: `pytest` runs without errors.
- Verification: Execute `pytest` via terminal.
- Status: Completed.

## T-02 Domain model [Completed]
- Goal: Define `Customer` dataclass and custom `ValidationError` exception.
- Files: `src/models.py`, `src/exceptions.py`, `tests/test_models.py`.
- Acceptance: `Customer` object instantiates correctly with id, name, email.
- Verification: Run `pytest tests/test_models.py`.
- Status: Completed.

## T-03 Search logic [Completed]
- Goal: Implement `CustomerRepository` and search filtering logic.
- Files: `src/repository.py`, `tests/test_repository.py`.
- Acceptance: Repository filters records by partial name and email (case-insensitive).
- Verification: Run `pytest tests/test_repository.py`.
- Status: Completed.

## T-04 Validation and errors [Completed]
- Goal: Implement `CustomerService` with query validation rules (FR-03, FR-06).
- Files: `src/service.py`, `tests/test_service.py`.
- Acceptance: Raises `ValidationError` when query length < 2 or whitespace.
- Verification: Run `pytest tests/test_service.py`.
- Status: Completed.

## T-05 Tests [Completed]
- Goal: Ensure comprehensive test suite execution and high test coverage.
- Files: `tests/test_service.py`, `tests/test_repository.py`, `tests/test_cli.py`.
- Acceptance: Test coverage >= 90%.
- Verification: Run `pytest --cov=src`.
- Status: Completed (100% coverage achieved, 32 passing tests).

## T-06 Documentation [Completed]
- Goal: Create `README.md` explaining CLI execution and updates to `AI_USAGE_LOG.md`.
- Files: `README.md`, `AI_USAGE_LOG.md`.
- Acceptance: Clear usage instructions and completed AI interaction log.
- Verification: Manual review of documentation.
- Status: Completed.