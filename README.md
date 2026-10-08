# Customer Search Feature

A reliable, validated, case-insensitive partial search mechanism to locate customer records by name or email via a local CLI and Python module.

---

## Architecture Overview

The project adheres to a 3-layer modular architecture:
- **CLI Interface Layer (`src/cli.py`)**: Handles command-line arguments via `argparse`, orchestrates user output, and captures validation errors gracefully.
- **Domain Service Layer (`src/service.py`)**: Applies input validation rules (whitespace trimming, minimum 2-character requirement, non-empty) and coordinates with repository.
- **In-Memory Repository Layer (`src/repository.py`)**: Stores customer records in memory, performs case-insensitive substring matching against customer `name` and `email`, and caps results at 50 records.
- **Domain Models & Exceptions (`src/models.py`, `src/exceptions.py`)**: Defines the `Customer` dataclass and custom `ValidationError`.

---

## Requirements

- Python 3.11+
- Virtual environment (`venv`)
- Standard library (`dataclasses`, `argparse`, `sys`, `typing`)
- Development dependencies (`pytest`, `pytest-cov`)

---

## Installation & Setup

1. **Clone or navigate to the repository:**
   ```bash
   cd ada-05-spec-driven-feature
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## CLI Execution

Search customer records by name or email using the module CLI entry point:

```bash
python -m src.cli "<query>"
```

### Examples

- **Search by customer name:**
  ```bash
  python -m src.cli "john"
  ```
  *Output:*
  ```text
  Found 2 matching customer(s):
  - ID: 1, Name: John Doe, Email: john.doe@example.com
  - ID: 2, Name: Johnny Smith, Email: johnny@gmail.com
  ```

- **Search by email domain:**
  ```bash
  python -m src.cli "gmail"
  ```
  *Output:*
  ```text
  Found 2 matching customer(s):
  - ID: 2, Name: Johnny Smith, Email: johnny@gmail.com
  - ID: 4, Name: Alex Johnson, Email: alex@gmail.com
  ```

- **No matches found:**
  ```bash
  python -m src.cli "xyz_nonexistent"
  ```
  *Output:*
  ```text
  No customers found.
  ```

- **Validation error handling (query too short):**
  ```bash
  python -m src.cli "a"
  ```
  *Stderr:*
  ```text
  Error: Search query must be at least 2 characters long.
  ```

- **Validation error handling (empty / whitespace-only query):**
  ```bash
  python -m src.cli "   "
  ```
  *Stderr:*
  ```text
  Error: Search query cannot be empty.
  ```

---

## Running Tests & Coverage

Run the test suite using `pytest`:
```bash
pytest
```

Run test suite with test coverage analysis:
```bash
pytest --cov=src
```
*(Expected coverage: 100%, exceeding the 90% NFR-02 requirement).*
