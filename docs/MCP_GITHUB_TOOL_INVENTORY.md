# MCP GitHub Tool Inventory

| Tool / capacidad | Toolset | Read/Write | Uso en el ADA | Riesgo |
| :--- | :--- | :--- | :--- | :--- |
| `get_file_contents`, `get_commit`, `get_directory_structure` | repos | Read | Leer archivos de código fuente, historial de commits y estructura del repositorio. | Bajo |
| `search_code`, `search_repositories` | repos | Read | Localizar archivos, funciones o clases específicas dentro del proyecto. | Bajo |
| `get_issue`, `list_issues`, `get_issue_comments` | issues | Read | Consultar el reporte de bug o requerimiento del Issue #1. | Medio: contenido proveniente de texto libre no confiable (*prompt injection*). |
| `get_pull_request`, `get_pull_request_files`, `get_pull_request_diff` | pull_requests | Read | Obtener los cambios de código, archivos modificados y diffs del PR #1. | Medio: contenido proveniente de código/comentarios externos. |
| Write tools (`create_issue`, `push_files`, `create_pull_request_comment`) | N/A | No disponibles | Ninguno. Deshabilitadas deliberadamente por la política `X-MCP-Readonly: true`. | Alto si estuvieran habilitadas (modificación no autorizada del repo). |