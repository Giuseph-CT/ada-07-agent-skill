# Requirements — Customer Search

## User Story
As a user,
I want to search customers by name or email,
so that I can quickly find the customer record I need.

## Functional Requirements
FR-01: The system MUST allow searching for customers by name or email address.
FR-02: The search MUST support case-insensitive partial matching (e.g., searching "ana" matches "Ana", "Diana", or "ana@example.com").
FR-03: The search query MUST contain at least 2 characters to execute a search.
FR-04: The system MUST return a structured list of matching customer records containing ID, full name, and email.
FR-05: The system MUST return an empty result list when no matching records are found.
FR-06: The system MUST validate the query input and return a clear error message for invalid inputs (e.g., query too short or whitespace-only).

## Non-Functional Requirements
NFR-01: The search operation MUST complete in less than 200 ms for datasets up to 1,000 in-memory records.
NFR-02: The codebase MUST achieve at least 90% unit test coverage using pytest.
NFR-03: The project MUST run on Python 3.11+ using standard library and minimal external dependencies (pytest).

## Open Questions
Q-01: N/A - Is pagination required for large search results? (No, for this scope a maximum limit of 50 records is sufficient).
Q-02: N/A - Should deleted/inactive customers be included in search results? (No, all in-memory seed records are active).

## Constraints / Assumptions
C-01: The implementation MUST run locally via CLI/Script interface using Python 3.11+.
A-01: Customer data is stored in-memory or loaded from a local static JSON file.