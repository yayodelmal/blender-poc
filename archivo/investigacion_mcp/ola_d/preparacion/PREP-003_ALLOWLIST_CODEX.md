# PREP-003 — Allowlist de herramientas de Codex

## Dictamen: BLOCKED para EXP-001 completo

No se recomienda ni se presenta una allowlist como garantía de lectura únicamente. La inspección estática del commit 992233bb258975a05eec8b5691465c50c2831e34 muestra que varias herramientas nominalmente informativas pueden invocar ejecución Python genérica dentro de Blender.

## Evidencia en el código fijado

- [server.py, función _run_script](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/server.py#L528-L535) envía el comando execute_code al addon con el script construido por el servidor.
- [get_scene_info](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/server.py#L558-L617) llama _run_script en la ruta principal; ante error dispone de una ruta de respaldo directa. Por tanto, habilitar get_scene_info no garantiza no ejecutar código Python genérico.
- [look y su fallback](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/server.py#L1493-L1535) pueden recurrir a la ruta scripted, que llama _run_script y execute_code.
- [get_addon_status](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/server.py#L414-L457) usa handshake y consultas directas de estado; el código inspeccionado no muestra execute_code en esa ruta. Sin embargo, solo informa estado y no satisface la inspección de escena exigida en EXP-001.
- El argumento read_only del comando no constituye una barrera de autorización de Python; SEC-006 documenta que no limita de forma efectiva todas las operaciones.

## Discrepancia con documentos previos

SEC-008 y el diseño EXP-001 consideraron el filtrado enabled_tools de Codex como mitigación de exposición para el experimento. Este trazado de llamadas revela que filtrar por nombre de herramienta no elimina la ejecución Python interna de get_scene_info ni de ciertos recorridos de look. El filtrado de Codex tampoco controla procesos locales que se conecten al socket sin autenticación. Se registra la discrepancia para revisión expresa de SEC-008/EXP-001; no se alteran aquí decisiones previamente aprobadas.

La documentación oficial de Codex describe la configuración de herramientas del servidor MCP, pero la compatibilidad y efecto exactos de enabled_tools deben cotejarse con la versión local y con el esquema MCP concreto: [documentación MCP de Codex](https://learn.chatgpt.com/docs/extend/mcp?surface=cli). La configuración local no contiene un servidor Blender y no se modificó.

## Herramientas

No hay lista permitida válida para el EXP-001 completo en este momento. No se debe habilitar execute_blender_code ni herramientas de creación/modificación, importación, exportación, ejecución genérica o guardado. get_addon_status podría ser una consulta acotada de estado en un experimento distinto, pero no es suficiente para verificar inspección de escena y no se propone como autorización implícita.

Para desbloquear:

1. Revisar el código exacto de cada herramienta candidata y demostrar que toda ruta, incluidos fallbacks, evita execute_code.
2. Si no existe esa capacidad, decidir mediante revisión humana si se acepta un experimento explícitamente expuesto a ejecución Python o posponerlo hasta contar con una barrera técnica verificable.
3. Confirmar cómo aplica enabled_tools Codex CLI 0.166.0 y demostrar la lista visible en interfaz sin conectar a Blender en esta fase.
4. Mantener explícito que el control de Codex limita herramientas expuestas al agente; no autentica el listener ni protege de otros procesos locales.

Estado: BLOCKED. No se aplicó configuración ni se conectó servidor alguno.
