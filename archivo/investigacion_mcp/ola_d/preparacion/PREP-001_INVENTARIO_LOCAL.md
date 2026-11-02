# PREP-001 — Inventario local de solo lectura

Fecha de inspección: 2026-11-02. Alcance: metadatos y consultas locales no modificadoras. No se abrió Blender, no se inició MCP ni se conectó a sockets.

## Evidencia observada

| Componente | Estado | Evidencia observada | Límite |
|---|---|---|---|
| macOS | Detectado | sw_vers informa macOS 27.0.1, build 26A434 | No se validó compatibilidad de aplicaciones con esta versión del sistema |
| Arquitectura | Detectada | uname -m devuelve arm64 | sysctl hw.machine fue denegado por el entorno; no fue necesario para identificar arquitectura |
| Codex CLI | Instalado | /opt/homebrew/bin/codex; codex --version informa codex-cli 0.166.0 | La consulta mostró aviso de que no pudo crear alias de PATH por Operation not permitted; no se autorizó ni observó cambio de configuración |
| Codex Desktop | No verificado | No se encontró /Applications/Codex.app | ChatGPT.app está presente, versión 26.1027.30824, pero no se infiere que equivalga a Codex Desktop |
| Blender | No detectado | command -v blender vacío; no se encontró Blender.app en /Applications ni en ~/Applications; búsqueda local indexada sin resultado | La búsqueda no demuestra ausencia en ubicaciones no indexadas o volúmenes externos |
| Python | Detectado | /usr/bin/python3, versión 3.9.6 | La versión queda por debajo del requisito Python >=3.10 declarado por el árbol MCP candidato; el entorno operativo del servidor no está instalado/verificado |
| uv | Instalado | /opt/homebrew/bin/uv, versión 0.12.17, Homebrew 2026-09-18, aarch64-apple-darwin | No se comprobó la selección de intérprete que usaría una futura instalación |
| MCP for Blender | Desconocido | No se encontró comando mcp-for-blender; pip show no informó paquete | uv tool list no pudo leer su caché por acceso denegado; por ello no se declara ausente |
| Configuración MCP de Codex | Inspeccionada sin secretos | ~/.codex/config.toml existe; se encontraron secciones node_repl, computer-use (enabled=false) y onshape; no existe sección blender | Solo se registraron nombres de secciones y opciones relevantes, sin valores sensibles |
| Complemento Blender local | No detectado / ubicación desconocida | Búsqueda convencional de directorios de addons sin resultados | Blender no está detectado y las rutas alternativas no se pueden descartar exhaustivamente |
| Directorio aislado de pruebas | No disponible | No existían repo/tmp, repo/experiments, ~/Library/Application Support/blender-poc ni /private/tmp/blender-poc | La carpeta de documentos de preparación no se considera espacio experimental |
| Puerto 9876 | Sin listener observado en el instante | Consulta local de procesos/socket informó cero entradas para 9876 | No prueba que el candidato se haya iniciado antes, ni que una futura sesión esté aislada |

## Discrepancias y acciones pendientes

- El inventario local no confirma las versiones objetivo candidatas descritas por documentación previa; solo identifica Codex CLI 0.166.0 y uv 0.12.17.
- El Python de sistema es 3.9.6, insuficiente para el requisito del paquete candidato. No se buscó ni instaló otro Python.
- El hecho de que no aparezca Blender ni MCP en rutas consultadas es evidencia limitada, no prueba global de ausencia.
- Antes de EXP-001 se necesita un directorio aislado aprobado, Blender instalado y versionado, y evidencia del origen del addon.

## Fuentes

- Metadatos locales obtenidos con sw_vers, uname, command -v, --version, búsqueda de rutas y consulta de configuración redactada.
- Requisito Python del commit auditado: [pyproject.toml en 992233bb258975a05eec8b5691465c50c2831e34](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/pyproject.toml).

Estado del documento: preparado; no constituye autorización de ejecución.
