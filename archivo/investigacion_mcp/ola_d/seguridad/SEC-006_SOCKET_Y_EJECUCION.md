# SEC-006 — Socket, controles de acceso y ejecución

**Código:** commit 992233bb258975a05eec8b5691465c50c2831e34. **Método:** revisión estática, sin ejecutar ni conectar.

## Listener y autenticación

El constructor BlenderMCPServer del addon recibe host localhost y puerto 9876 por defecto. start crea socket AF_INET/SOCK_STREAM, activa SO_REUSEADDR, enlaza (self.host, self.port) y llama listen(5) ([constructor/start](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/addon.py#L1116-L1238)). La escena permite cambiar el puerto; el código observado no presenta ajuste de host. El valor configurado es localhost, no IP numérica; resolución final depende de macOS y no fue comprobada.

El servidor MCP por separado tiene DEFAULT_HOST localhost y puerto 9876, con overrides CLI y BLENDER_HOST/BLENDER_PORT ([cliente](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/server.py#L53-L119)). Ese host configura connect y no determina el bind del addon.

_server_loop acepta clientes y _handle_client acumula JSON y mete órdenes en cola ([accept/handler](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/addon.py#L1302-L1389)). El dispatch resuelve los handlers base ([dispatch](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/addon.py#L1428-L1455)). No se observa token, secreto, autenticación mutua ni autorización por operación entre accept y dispatch. Cualquier proceso que alcance el socket puede enviar mensajes de protocolo; localhost no autentica a procesos locales.

## Ejecución

El servidor MCP registra execute_blender_code en la función de [server.py, líneas 732–778](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/server.py#L732-L778) y envía el comando execute_code. El addon incluye ese comando en handlers base y llama exec(code, namespace), con bpy disponible ([ejecución](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/addon.py#L2129-L2154)). Se ejecuta dentro del proceso Blender y con sus permisos efectivos. No hay separación de permisos de lectura y escritura en el socket.

safe_mode.py documenta un validador optativo activado mediante BLENDER_MCP_SAFE_MODE ([fuente](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/safe_mode.py#L0-L69)). Opera en la ruta MCP y no cubre llamadas directas al socket. Bloquea varias rutas de escape, pero permite modificaciones Blender, guardado/apertura e importación/exportación. No es solo lectura ni sandbox de proceso.

## Restricción de tools para EXP-001

No se identifica opción nativa para quitar execute_blender_code del servidor MCP. La documentación de Codex soporta enabled_tools para controlar las herramientas visibles al agente ([documentación](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)). Así Codex puede limitarse a tools de inspección y omitir ejecución, edición, exportación, generación e importación. Se debe verificar la lista efectiva antes de llamar a Blender.

El filtro es un control del cliente Codex, no del listener. No evita que otro cliente local hable con el socket. La anotación readOnlyHint tampoco impone autorización.

## Cierre

stop() cambia el estado, desregistra el timer, cierra sockets cliente y listener, vacía la cola y espera hasta un segundo al hilo ([cierre](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/addon.py#L1250-L1300)). Implementación estática no demuestra cierre operativo en el Mac.

## Issue #404 y bind configurable

El [issue #404](https://github.com/ahujasid/mcp-for-blender/issues/404) permanece abierto, declara la versión 1.6.0 y explica la recepción sin auth de execute_code y el paso a exec; su panel de desarrollo indica que no hay ramas o PR asociados. No se atribuye automáticamente 1.6.0 a este SHA, pero el código fijado contiene el mismo patrón estructural. No se identificó un parche de autenticación/autorización ni un modo nativo para retirar el handler. El [issue #369](https://github.com/ahujasid/mcp-for-blender/issues/369) también está abierto y pide un bind configurable; el código auditado usa localhost de forma predeterminada y no presenta un control de host en el panel. Aunque localhost limite exposición de red, permanece el acceso de procesos locales y la ejecución en Blender.

| Control | Evaluación |
|---|---|
| Bind | localhost:9876 por defecto, IPv4 TCP; resolución efectiva sin verificar |
| Autenticación/ACL | No encontrada en el protocolo auditado |
| Python arbitrario | Sí, exec en Blender |
| Safe mode | Opt-in, MCP-path-only, permite escritura |
| Tool exclusion para Codex | Posible mediante enabled_tools; requiere configuración y verificación |
| Protección del socket a otros procesos | No identificada |

**Conclusión EXP-001:** puede restringirse técnicamente a lectura para las llamadas de Codex mediante allowlist comprobada. No se puede afirmar que ningún otro proceso local tenga acceso al listener. Si ese es un requisito, el diseño actual no lo cumple.

