# Agent Report

## Agent / Version
* **Agente:** agy (CLI Coding Agent)
* **Modelo:** Gemini

## Initial Context
El proyecto inició con los requerimientos (`REQUIREMENTS.md`), la especificación (`SPEC.md`), la arquitectura (`ARCHITECTURE.md`) y el desglose de tareas (`TASKS.md`).

## Task Sequence

### T-01: Project Setup
* **What the agent did:** Creó la estructura de archivos, `pyproject.toml` y `requirements.txt`.
* **Human review:** Verificado que la configuración de pytest y coverage fuera correcta.
* **Tests:** `tests/test_setup.py` PASSED.

### T-02: Domain Model
* **What the agent did:** Implementó el modelo `Customer` y la excepción `ValidationError`.
* **Human review:** Confirmado que no se agregaran atributos innecesarios fuera de la especificación.
* **Tests:** `tests/test_models.py` PASSED.

### T-03: Search Logic
* **What the agent did:** Implementó `CustomerRepository` con filtrado por nombre y correo.
* **Human review:** Verificado que las búsquedas fueran insensibles a mayúsculas/minúsculas.
* **Tests:** `tests/test_repository.py` PASSED (10 tests).

### T-04: Validation and Errors
* **What the agent did:** Implementó `CustomerService` realizando la limpieza con `.strip()` y validando longitud mínima.
* **Human review:** Confirmado el orden correcto de validación (espacios antes de validar caracteres mínimos).
* **Tests:** `tests/test_service.py` PASSED (10 tests).

### T-05: Tests & CLI Integration
* **What the agent did:** Creó `src/cli.py`, pruebas de integración de CLI y prueba de rendimiento NFR-01 con 1,000 registros.
* **Human review:** Revisado el manejo de errores en CLI (`stderr` y salida con código 1).
* **Tests:** `tests/test_cli.py` y `tests/test_service.py` PASSED. Cobertura al 100%.

### T-06: Documentation
* **What the agent did:** Actualizó `README.md`, `AI_USAGE_LOG.md` y `TASKS.md`.
* **Human review:** Aprobada la documentación de uso e instalación.
* **Tests:** Suite completa de 32 tests PASSED.

## Problems Encountered
Ninguno crítico. Las decisiones sobre el manejo de espacios en blanco y mensajes de error fueron aclaradas en `SPEC.md`.

## Human Interventions
Supervisión paso a paso por cada tarea (T-01 a T-06), validando los resultados de `pytest` antes de aprobar la siguiente fase.

## Requirement / Specification Changes
No hubo cambios en los requerimientos originales.

## Final Verification
* **Total Tests:** 32 passed.
* **Code Coverage:** 100%.
* **NFR-01 Performance:** $< 200\text{ ms}$ cumplido.

## Lessons Learned
El enfoque spec-driven evita que el agente o el desarrollador asuman requerimientos inexistentes, manteniendo el código limpio y enfocado exclusivamente en lo especificado.

# Fase 10 — Revisión Humana y Sección 18 — Reflexión

## 14. Fase 10 — Revisión humana

* **¿La implementación cumple REQUIREMENTS.md y SPEC.md?**
  Sí. La funcionalidad de búsqueda de clientes permite coincidencias parciales por nombre y correo electrónico, requiere una longitud mínima de 2 caracteres tras la limpieza con `.strip()`, es insensible a mayúsculas/minúsculas y lanza una excepción de tipo `ValidationError` en caso de consultas inválidas.

* **¿SPEC.md referencia requisitos existentes sin redefinirlos?**
  Sí. El archivo `SPEC.md` cita explícitamente los identificadores estables `FR-01` a `FR-06`, `NFR-01` y `NFR-02` en sus secciones de *Requirements Covered*, sin redefinir la intención original del negocio.

* **¿Se inventaron reglas?**
  No. Durante la generación inicial, la IA propuso incluir paginación y filtros por estado de cliente, pero fueron descartados en la revisión humana por no pertenecer al alcance de la especificación.

* **¿Hay código innecesario?**
  No. La solución incluye únicamente los módulos necesarios (`models.py`, `repository.py`, `service.py`, `exceptions.py` y `cli.py`), respetando el principio YAGNI (*You Aren't Gonna Need It*).

* **¿Se modificaron archivos no relacionados?**
  No. Todos los cambios se limitaron estrictamente a las rutas dentro de `src/`, `tests/`, `docs/` y `results/`.

* **¿Los tests prueban comportamiento?**
  Sí. La suite de 32 pruebas automatizadas evalúa las respuestas del servicio, el lanzamiento de excepciones, el formato de salida y códigos de salida de la CLI, en lugar de validar detalles de implementación privada.

* **¿ARCHITECTURE.md coincide con el código?**
  Sí. Se mantuvo la arquitectura en capas (CLI → Service → Repository) con la inyección de dependencias definida en el diseño.

* **¿La documentación está actualizada?**
  Sí. Se actualizó el `README.md`, la matriz de trazabilidad en `docs/traceability.md`, el historial de interacción en `AI_USAGE_LOG.md` y el informe en `results/agent-report.md`.

---

## 18. Reflexión

1. **¿Qué diferencia hay entre requirement, specification y prompt?**
   * **Requirement:** Expresa la necesidad del negocio u objetivo final (el *qué*), por ejemplo: *"El sistema debe permitir buscar clientes por nombre o correo"*.
   * **Specification:** Define las reglas técnicas, límites, casos de borde y contratos de entrada/salida (el *cómo se comporta*), como especificar que la consulta requiere mínimo 2 caracteres tras `.strip()`.
   * **Prompt:** Es la instrucción contextualizada enviada a la IA para que ejecute una tarea específica basándose en la especificación.

2. **¿Qué información fue indispensable antes de programar?**
   Los criterios de aceptación explícitos, los atributos de la entidad `Customer`, el manejo de espacios en blanco, la excepción específica a lanzar (`ValidationError`) y los límites de resultados por consulta.

3. **¿Qué decisiones debieron resolverse antes de programar?**
   * El comportamiento del sistema ante cadenas compuestas únicamente por espacios en blanco.
   * La decisión de capturar excepciones en la CLI para retornar código de salida `1` escribiendo el mensaje en `stderr`.
   * La estructura de inyección de dependencias dentro de `CustomerService` para simplificar las pruebas unitarias.

4. **¿Qué errores evitó SPEC.md?**
   Evitó que la IA implementara persisencia en base de datos SQL no requerida, evitó el uso de excepciones genéricas (`ValueError` o `Exception`) y garantizó que se aplicara `.strip()` antes de validar la longitud mínima de caracteres.

5. **¿Qué problema evita separar REQUIREMENTS.md de SPEC.md?**
   Evita la duplicación y desincronización de las reglas de negocio. `REQUIREMENTS.md` se mantiene intacto como la visión del cliente, mientras que `SPEC.md` sirve como contrato técnico de implementación sin alterar el problema original.

6. **¿Qué papel tuvo AGENTS.md?**
   Sirvió como guía de conducta para el agente de IA (`agy`), restringiendo su autonomía a las tareas asignadas en `TASKS.md`, indicándole los archivos a consultar previamente y prohibiéndole modificar requerimientos sin aprobación explícita.

7. **¿Qué cambió durante la revisión humana?**
   Se descartaron métodos innecesarios en la capa de datos sugeridos por la IA, se corrigió la salida de error en `cli.py` hacia `stderr` y se ajustó la prueba de rendimiento para garantizar el cumplimiento de `NFR-01` ($< 200\text{ ms}$).

8. **¿La arquitectura coincidió con el código final?**
   Sí, la separación de responsabilidades entre la capa de interfaz (`cli.py`), la lógica del dominio (`service.py`) y la gestión de datos (`repository.py`) se implementó en exacta correspondencia con `ARCHITECTURE.md`.

9. **¿Qué requisito fue más difícil de probar?**
   `NFR-01` (Tiempo de respuesta $< 200\text{ ms}$ en 1,000 registros), ya que requirió implementar una fixture que poblara 1,000 objetos `Customer` en memoria para medir el tiempo real con `time.perf_counter()`.

10. **¿Qué mejorarías en tu proceso spec-driven?**
    Añadiría un paso de validación automática de estilo (linter tipo `flake8` o `ruff`) antes de ejecutar las pruebas unitarias y definiría desde la especificación el comportamiento ante consultas concurrentes.

11. **¿Por qué SPEC.md puede funcionar como contrato verificable sin duplicar los requisitos?**
    Porque asocia los identificadores estables de los requisitos (`FR-01`, `FR-02`, etc.) a criterios de aceptación estructurados (escenarios *Given-When-Then*), permitiendo verificar el comportamiento mediante código de prueba sin reescribir el requisito.

12. **¿Qué decisiones importantes aparecen en tu AI Usage Log y cómo cambió tu criterio después de revisar las sugerencias de la IA?**
    La decisión de rechazar la generación de métodos de filtrado adicionales no solicitados. Mi criterio evolucionó hacia un enfoque estricto de auditoría sobre el código generado por la IA, validando que cada archivo añadido cumpliera fielmente con la especificación del proyecto.