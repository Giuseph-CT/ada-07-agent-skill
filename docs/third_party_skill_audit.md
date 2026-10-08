# Third-Party Skill Pre-Install Audit & Supply Chain Hygiene

- **Repository:** `https://github.com/addyosmani/agent-skills`
- **Selected skill:** `code-review-and-quality`
- **Version / Commit inspected:** `main` (commit `c4f8d1a` / v1.2.0)
- **Installed path:** `.agents/skills/code-review-and-quality/`

---

## Purpose
Realizar revisiones integrales de código y calidad de software sobre diffs o PRs, evaluando corrección (*correctness*), legibilidad, arquitectura, seguridad y rendimiento, antes de proceder al merge.

---

## Supply Chain Control Matrix 

| Control | Evidencia / Estado |
| :--- | :--- |
| **Source** | Autor y repositorio identificados públicamente (`addyosmani/agent-skills`). |
| **Pinning** | Commit fijado en `c4f8d1a` (v1.2.0) localmente para evitar deriva o actualizaciones no controladas. |
| **Audit** | `SKILL.md` y archivos de referencia (`references/`) inspeccionados previo a la ejecución. |
| **Secrets** | No contiene ni solicita credenciales, tokens o API keys embebidas. |
| **Commands** | Ejecución restringida exclusivamente a la suite de pruebas (`pytest`) y lectura de diffs (`git diff`). |
| **Permissions** | Acceso estrictamente en modo lectura (*read-only*) sobre el workspace local. No obtiene más acceso del necesario. |
| **Change control** | Copia estática fijada localmente; no se actualiza silenciosamente durante la evaluación. |

---

## Trigger / Description
- **Triggers:** Solicitudes explícitas de code review, análisis de calidad de código, revisión de diffs/PRs, verificación de refinamientos o solicitudes de auditoría de arquitectura/seguridad sobre cambios de código.
- **Out of scope:** Implementación directa de código, refactorización automática de archivos sin solicitud, ejecución de escrituras en Git/GitHub (commits, merges, comentarios remotos) o explicaciones genéricas de sintaxis.

---

## Supporting References
- `references/checklist.md` (Puntos de inspección por eje temático)
- `references/quality_gates.md` (Criterios de paso/fallo para merge)
- `references/severity_rubric.md` (Matriz de severidad Blocker/Critical/Major/Minor)

---

## Tools / Commands / Permissions
- **Herramientas de inspección:** Read-only sobre el sistema de archivos (`git diff`, `git status`, lectura de archivos).
- **Comandos permitidos:** Comandos de solo lectura y suites de pruebas del proyecto (`pytest`, `npm test`, linter checks).
- **Permisos requeridos:** Lectura de repositorio. No requiere tokens con permiso de escritura en GitHub.

---

## Potential Risks
- **Supply Chain:** Inyección de instrucciones no verificadas (Prompt Injection) en archivos `references/`.
- **Ejecución de código:** Los comandos de test sugeridos por la Skill deben ser monitoreados para evitar ejecución de scripts maliciosos arbitrarios.
- **Exposición de datos:** Posible lectura e inclusión accidental de variables de entorno o credenciales locales en los reportes de salida.

---

## Decision & Trust Rationale
[X] Install
[ ] Do not install

**Reason:** La Skill se mantiene bajo un esquema puramente *read-only*, no incluye scripts ejecutables opacos (`.sh` o `.py` compilados) y sus referencias son archivos Markdown transparentes. No requiere acceso a red externa ni exfiltra información, por lo que es completamente segura para entornos locales y de evaluación académica.