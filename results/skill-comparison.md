# Comparative Analysis: Custom Skill vs. Professional Skill

## Matrix Comparison

| Dimensión | Tu Skill (`reviewing-pull-requests`) | Skill Profesional (`code-review-and-quality`) | Conclusión |
| :--- | :--- | :--- | :--- |
| **Trigger / routing** | Enfocado en entrega de tareas/PRs para el curso (`PR readiness`). | Genérico, intensivo en intención de revisión de calidad de código. | Ambos evitan falsos positivos; el profesional cubre más sinónimos de intención. |
| **Scope / boundaries** | Estricto *Draft-Only* con archivo estandarizado de salida. | Estricto *Draft-Only* con Quality Gates de pase/fallo. | La profesional define gates explícitos de bloqueo (*Blocker/Critical*). |
| **Workflow depth** | Flujo secuencial lineal de 10 pasos guiados. | Análisis exhaustivo multinivel basado en 5 ejes de calidad. | La profesional analiza arquitectura y performance a mayor profundidad. |
| **Correctness** | Enfocado en requisitos/especificaciones del proyecto. | Enfocado en requisitos + patrones de diseño + edge cases. | La profesional detectó la excepción de tipo en runtime (`AttributeError`). |
| **Architecture** | Valida fronteras del sistema e interfaces. | Audita acoplamiento, cohesión, abstracción y desacoplamiento. | La profesional analizó la desconexión entre Service, Repository y CLI. |
| **Security** | Revisa secretos, credenciales e inyecciones básicas. | Revisa sanitización, excepciones no manejadas e inmutabilidad. | La profesional fue más exhaustiva en análisis defensivo contra tipos. |
| **Performance** | Básico (evaluación cualitativa). | Analiza complejidad algorítmica ($O(N)$) y consumo de recursos. | La profesional aporta mayor rigor en optimización y límites. |
| **Tests / verification** | Ejecuta `pytest` y revisa evidencia de cobertura. | Exige métricas de regresión y prueba de branch coverage / mutaciones. | Ambas detectaron la falta de coverage en la línea 29 de `src/service.py`. |
| **Severity model** | 3 niveles: MUST FIX, SHOULD FIX, OPTIONAL. | 4 niveles: Blocker, Critical, Major, Minor. | La profesional permite diferenciar errores fatales de problemas de calidad. |
| **Human review** | Diseñada para asistente interactivo con aprobación final. | Diseñada para auditoría autónoma o asistida por desarrollador. | Ambas respetan que el desarrollador toma la decisión final de merge. |
| **References / composition**| Uso de `references/` para checklists y guías de formato. | Uso de archivos de referencia para Quality Gates y convenciones. | Estructura de progressive disclosure equivalente. |
| **Reusability** | Alta en el contexto académico del curso ADA-07. | Alta para cualquier repositorio Python/software comercial. | La profesional es completamente agnóstica al proyecto. |

---

## Hallazgos Específicos y Accionables

1. **Ejemplo Hallazgo Único - Skill Profesional:**
   - **Hallazgo:** Excepción no controlada (`AttributeError`) en `src/service.py:28` al invocar `status.upper()` sin verificar si `status` es una cadena de texto (`isinstance(status, str)`).
   - **Valor:** Detectó un problema defensivo de calidad de código en tiempo de ejecución que no estaba explícito en las especificaciones del curso.

2. **Ejemplo Hallazgo Único - Tu Skill:**
   - **Hallazgo:** Validación determinista del formato del reporte mediante el script Python `validate_review_report.py`.
   - **Valor:** Garantizó que el reporte final cumpliera exactamente con la plantilla y el esquema requerido antes de presentarlo al usuario.

---

## Preguntas de Análisis Comparativo

### ¿Qué hace la Skill profesional que tu Skill no contempló?
Incorpora **Quality Gates explícitos** (Correctness, Security, Testing, Architecture) con un modelo de severidad de 4 niveles (*Blocker, Critical, Major, Minor*) y realiza análisis defensivo de tipos en tiempo de ejecución.

### ¿Qué elementos de tu Skill son más específicos al curso/proyecto y conviene conservar?
El **script determinista de validación** (`validate_review_report.py`), ya que garantiza que la salida cumpla de manera estricta con el esquema y plantilla del proyecto antes de guardarlo.

### ¿Qué agregarías a una versión 2 de tu Skill?
- Matriz de severidades de 4 niveles (*Blocker/Critical/Major/Minor*).
- Quality Gates de pase/fallo explícitos en el resumen ejecutivo.
- Verificación defensiva contra tipos de datos no válidos en el código revisado.

### ¿Qué NO copiarías y por qué?
No eliminaría el script determinista de validación. La skill profesional confía completamente en el LLM para estructurar la salida, lo cual puede generar ligeras variaciones de formato entre ejecuciones.

### ¿Cuál produjo hallazgos más accionables?
La **Skill Profesional**, porque además de identificar que la regla de `status` no estaba en la especificación, demostró que el parámetro ni siquiera se pasaba al repositorio (código muerto) y que crasheaba si se enviaba un entero.