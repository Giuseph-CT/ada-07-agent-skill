# Traceability Matrix: Issue → PR → Code → Test

| Issue / Need | PR | Code / Files | Test / Evidence | Estado |
| :--- | :--- | :--- | :--- | :--- |
| **Issue #1**: Validar filtro de `status` (`ACTIVE`, `INACTIVE`, `PENDING`) según supuesta especificación | **PR #2**: `fix: agregar validacion de status segun SPEC.md` *(Closes #1)* | `src/service.py` | `tests/test_service.py` | **Gap** (El código valida en `service.py` pero no filtra en `repository.py`; no hay pruebas unitarias añadidas en `tests/`) |
| **FR-01 a FR-06**: Búsqueda por coincidencia parcial de texto en `name` y `email` | N/A *(Parte del release inicial en `main`)* | `src/service.py`<br>`src/repository.py`<br>`src/models.py`<br>`src/cli.py` | `tests/test_service.py`<br>`tests/test_repository.py`<br>`tests/test_cli.py` | **Covered** (100% Cobertura de pruebas en la rama `main`) |
| **NFR-02**: Cobertura de pruebas unitarias $\ge 90\%$ | **PR #2** *(Introduce regresión de cobertura)* | `src/service.py` | Ninguno añadido para el nuevo flujo condicional | **Gap** (La adición de ramas no probadas en PR #2 degrada la cobertura global de la rama `fix/customer-search-validation`) |

---

### Notas sobre Infecciones y Evidencia Remota

* **Relación Explicita:** La vinculación entre **Issue #1** y **PR #2** es **explícita** en los metadatos de GitHub (`Closes #1` en el cuerpo del PR #2).
* **Inferencia de Código y Pruebas (PR #2):**
  * *Evidencia Directa:* El diff de git en PR #2 muestra modificaciones **únicamente** en `src/service.py`.
  * *Fact:* Cero archivos fueron modificados dentro del directorio `tests/`.
  * *Inferencia:* El parámetro `status` introducido en `CustomerService.search` es **código muerto (*dead code*)**, ya que tras pasar la validación, el valor de `status` se descarta y no se transfiere a `CustomerRepository.search_by_text()`.
* **Inferencia de Especificación:** La Issue #1 cita la *"Sección 3: Criterios de Búsqueda"* de `SPEC.md`. Inspeccionando el archivo remoto `SPEC.md` vía MCP, se confirma que **dicha sección no existe**, por lo que la necesidad descrita en Issue #1 es una **hallucinated rule / unapproved requirement**.