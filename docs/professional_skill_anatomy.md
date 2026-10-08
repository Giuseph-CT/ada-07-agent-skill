# Professional Skill Study — ADA-07

## Source
- **Repository:** `https://github.com/addyosmani/agent-skills`
- **Skill:** `code-review-and-quality`
- **Version / commit:** `main` (commit `c4f8d1a` / v1.2.0)
- **Installed path:** `.agents/skills/code-review-and-quality/`

---

## Why this skill was selected
Se seleccionó por ser una Skill de referencia en la industria para revisión y auditoría de código, diseñada por Addy Osmani (Google). Destaca por aplicar estándares rigurosos de revisión en 5 ejes transversales, Quality Gates explícitos y un modelo formal de severidad.

---

## Anatomy observations

### Routing & Triggers
La `description` del frontmatter actúa como un algoritmo de enrutamiento basado en intención. Utiliza verbos de acción específicos ("review code", "audit diff", "assess code quality") y explicita anti-triggers claros ("Do NOT use to refactor code or auto-merge PRs") para evitar falsos positivos durante la selección por el LLM.

### Workflow & Quality Gates
El workflow implementa un pipeline estricto de 5 fases:
1. **Context Gathering:** Inspección del diff, archivos de requerimientos y especificaciones.
2. **Multi-Axis Analysis:** Evaluación sistemática dividida en los 5 ejes de calidad.
3. **Evidence Verification:** Ejecución de pruebas locales para verificar regresiones.
4. **Gate Evaluation:** Comparación contra `quality_gates.md` (0 Blockers, 0 Criticals).
5. **Report Generation:** Producción del artefacto en Markdown estructurado.

### Review Axes
- **Correctness:** Mapeo exacto entre comportamiento modificado y especificación/requisito.
- **Readability / Simplicity:** Ausencia de complejidad innecesaria, nombres descriptivos y principio YAGNI.
- **Architecture:** Respeto a las fronteras de módulos, patrones de diseño y dependencias.
- **Security:** Inyección de datos, sanitización, manejo de secretos y permisos.
- **Performance:** Algoritmos ineficientes, fugas de memoria o consultas no optimizadas.

### Severity Model
Diferencia los hallazgos en cuatro niveles bien definidos:
- **Blocker / Critical:** Viola especificación, rompe la compilación/tests, o introduce vulnerabilidades de seguridad (bloquea el merge de forma obligatoria).
- **Major:** Deuda técnica significativa, degrada la mantenibilidad o cobertura.
- **Minor / Informational:** Sugerencias de estilo o micro-optimizaciones no bloqueantes.

### Verification & Boundaries
- **Evidencia requerida:** Todo hallazgo debe citar el archivo exacto, línea de código y la prueba o requisito que lo sustenta.
- **Límites de autoridad:** Es una Skill *Draft-Only*. Prohíbe explícitamente realizar modificaciones sobre el código fuente analizado, publicar comentarios remotos vía API o aprobar/fusionar el PR.

---

## Execution
- **PR / diff reviewed:** Rama `fix/customer-search-validation`
- **Prompt used:** `"Aplica la skill instalada code-review-and-quality para revisar el diff actual de fix/customer-search-validation y genera results/professional-skill-review.md"`
- **Artifacts produced:** `results/professional-skill-review.md`

---

## Findings unique to the professional skill
1. **Detección de `AttributeError` por falta de validación de tipo:** Identificó una vulnerabilidad de robustez en `src/service.py:28` al invocar `status.upper()` sin verificar previamente si `status` es una cadena (`isinstance(status, str)`).
2. **Desconexión entre capas y código muerto:** Evidenció que la regla de negocio para `status` se validaba en el Service pero no se propagaba ni persistía en el Repository, además de resaltar que la interfaz CLI no expone dicho parámetro.

---

## Findings unique to my skill
1. **Validación determinista con script Python:** Inclusión y ejecución del script `validate_review_report.py` para garantizar sintácticamente que el reporte generado cumpla con todas las secciones exigidas con un exit code `0`.
2. **Alineación con la rúbrica del curso ADA-07:** Plantilla de salida y checklists directamente orientados a los criterios de evaluación del proyecto académico y trazabilidad de requerimientos.

---

## Security / dependency audit
- **Modo de operación:** Estrictamente *Draft-Only* y de solo lectura (*read-only*).
- **Permisos y comandos:** Limitado a inspección local de archivos (`git diff`) y ejecución de la suite de pruebas del proyecto (`pytest`).
- **Secretos y red:** No solicita ni expone credenciales/tokens; no realiza peticiones a red ni exfiltra datos.
- **Pinning:** Copia local fijada en el commit `c4f8d1a` (v1.2.0).

---

## What I would adopt in v2 of my skill
1. **Quality Gates explícitos:** Incorporar un criterio cuantitativo de aprobación/rechazo del PR basado en la presencia de fallos *Blocker* o *Critical*.
2. **Modelo de severidad de 4 niveles:** Reemplazar el esquema de 3 niveles por la matriz de *Blocker, Critical, Major, Minor*.
3. **Análisis defensivo de tipos de datos:** Añadir en la guía de inspección la comprobación de manejo seguro de tipos en parámetros de funciones principales.

---

## Human conclusion
La Skill profesional `code-review-and-quality` destaca por la profundidad metodológica de sus 5 ejes de revisión y su modelo de Quality Gates. No obstante, combinar la rigurosidad de análisis de la Skill profesional con el script de validación determinista en Python desarrollado en nuestra Skill propia produce el entorno de revisión más seguro, accionable y libre de errores de formato.