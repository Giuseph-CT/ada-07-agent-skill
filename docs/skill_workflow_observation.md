# Workflow Observation

## Trigger
- Cuando un usuario o desarrollador solicita verificar si una rama (`fix/customer-search-validation`) o Pull Request está listo para revisión humana.
- Cuando se requiere una evaluación previa de calidad, cumplimiento de especificación y estado de pruebas antes de autorizar el merge.

## Inputs
- El nombre de la rama actual (`fix/customer-search-validation`) o ID del PR.
- Acceso de lectura al código fuente, especificaciones (`SPEC.md` / `REQUIREMENTS.md`) y la suite de pruebas.

## Steps Performed
1. Inspeccionar documentos de especificación (`SPEC.md` o similares en el repositorio) para entender los criterios de aceptación.
2. Extraer los cambios realizados mediante `git diff main`.
3. Ejecutar la suite de pruebas determinista utilizando `pytest -v`.
4. Evaluar si los cambios en el código cumplen la especificación y si todas las pruebas pasan.
5. Clasificar cada observación o hallazgo en MUST FIX, SHOULD FIX u OPTIONAL.
6. Redactar el reporte estructurado de readiness para el revisor humano.

## Decisions
- Evaluar la alineación semántica entre el código implementado y los requerimientos especificados en los documentos del proyecto.
- Determinar la severidad justa de un fallo o deuda técnica (categorizar en MUST FIX, SHOULD FIX u OPTIONAL).

## Deterministic Work
- Obtención de métricas e historial de cambios mediante comandos de Git (`git diff main --stat`).
- Ejecución de la suite automatizada de pruebas unitarias (`pytest -v`).

## Reference Knowledge
- Criterios de severidad para clasificación de hallazgos (`finding_severities.md`).
- Formato y estructura estandarizada para el reporte de revisión (`report_template.md`).

## Output
- Archivo de reporte en Markdown guardado en `results/pr_readiness_report.md`.

## Stop Conditions
- Si el flujo intenta realizar operaciones de escritura o modificación en GitHub (comentar, aprobar PR, hacer merge).
- Si existen inconsistencias graves en la especificación que impidan evaluar la solución de manera objetiva.

## Skill Iteration
Version: 1.0.0 -> 1.0.1
Observed failure: VS Code Linter y el parser de skills rechazaron la propiedad name en SKILL.md por usar guiones bajos (`reviewing_pull_requests`).
Root cause: Trigger / Frontmatter Metadata Rule (convención estricta de nombres con guiones medios).
Change: Se modificó la metadata name a `reviewing-pull-requests` manteniendo la ruta de directorios requerida.
Evidence after change: El agente cargó la skill correctamente al solicitar "Perform a PR readiness review for the current branch".
Result: PASS