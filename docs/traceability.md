# Matriz de Trazabilidad — ADA-05

| Requirement | SPEC / AC | Task | Files | Test | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-01** | Búsqueda por coincidencia parcial en nombre | T-03 | `src/repository.py`, `src/service.py` | `tests/test_repository.py`, `tests/test_service.py` | OK | Búsqueda case-insensitive implementada. |
| **FR-02** | Búsqueda por coincidencia parcial en email | T-03 | `src/repository.py`, `src/service.py` | `tests/test_repository.py`, `tests/test_service.py` | OK | Permite encontrar por dominio o usuario. |
| **FR-03** | Longitud mínima de 2 caracteres después de `.strip()` | T-04 | `src/service.py` | `tests/test_service.py`, `tests/test_cli.py` | OK | Lanza `ValidationError` si `len(trimmed) < 2`. |
| **FR-04** | Búsqueda insensible a mayúsculas/minúsculas | T-03, T-04 | `src/repository.py`, `src/service.py` | `tests/test_repository.py`, `tests/test_service.py` | OK | Convierte a minusculas antes de comparar. |
| **FR-05** | Eliminación de espacios en blanco al inicio y final | T-04 | `src/service.py` | `tests/test_service.py`, `tests/test_cli.py` | OK | Se aplica `.strip()` antes de validar longitud. |
| **FR-06** | Excepción `ValidationError` para consultas inválidas | T-02, T-04 | `src/exceptions.py`, `src/service.py`, `src/cli.py` | `tests/test_service.py`, `tests/test_cli.py` | OK | `cli.py` la captura y muestra en `stderr` con exit code 1. |
| **NFR-01** | Tiempo de respuesta $< 200\text{ ms}$ en 1,000 registros | T-05 | `src/service.py`, `src/repository.py` | `tests/test_service.py` | OK | Verificado mediante `test_service_performance_with_1000_records`. |
| **NFR-02** | Cobertura de pruebas $\ge 90\%$ | T-05 | `src/*` | Toda la suite en `tests/` | OK | Cobertura alcanzada: **100%**. |