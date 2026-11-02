# SEC-007 — Comparación MCP y bpy directo

**MCP:** árbol fijado a SHA 992233bb258975a05eec8b5691465c50c2831e34. **bpy directo:** alternativa conceptual; no implementada ni probada.

| Criterio | MCP for Blender | Blender + bpy directo |
|---|---|---|
| Seguridad/superficie | Añade servidor, socket TCP, parser, tools e integraciones. localhost reduce el alcance de red usual, no autentica procesos locales. | Elimina listener/dispatch MCP si Blender se invoca como proceso. Python y Blender conservan permisos del usuario. |
| Ejecución Python | execute_blender_code llega a exec. Safe mode es opt-in y permite cambios/escritura. | --python también ejecuta en Blender. No es sandbox; solo es más acotado con operaciones/entradas definidas. |
| Edición paramétrica | Herramientas de escena e interacción viva disponibles; herramienta genérica permite cambios amplios. | bpy controla geometría, modificadores y parámetros; requiere definir operaciones del laboratorio. |
| Persistencia .blend | Se puede guardar desde la sesión; safe mode permite guardado. | Puede guardar copias y revisiones con rutas controladas; exige diseñar el flujo. |
| Inspección geométrica | get_scene_info y herramientas de inspección reducen trabajo; readOnlyHint no es permiso del socket. | Consultas bpy pueden devolver medidas/topología; los validadores los mantiene el laboratorio. |
| Recuperación | Timeout puede dejar estado incierto; stop() cierra sockets, sin rollback transaccional acreditado. | Proceso/exit code separados; timeout también es incierto. Copia candidata y promoción tras validar facilita rollback. |
| Trazabilidad | Logs MCP/addon y trajectory posibles; falta vincular cada operación a revisiones y decisión final. | stdout/stderr, exit code y hashes controlables; el esquema de registro debe construirse. |
| Complejidad | Reutiliza integración comunitaria; requiere alinear server/addon, socket y allowlist. | Menos puente externo, más responsabilidad de crear lanzador y validadores. |
| macOS ARM64 | Wheel Python universal no demuestra compatibilidad funcional local. | Depende de Blender ARM y bpy instalados; prueba local pendiente. |
| Mantenimiento | Proyecto PyPI/comunidad activo; cambios de protocolo externos. | bpy parte de Blender; el laboratorio mantiene la orquestación propia. |

MCP aporta interacción y tools listas, pero conserva un socket anónimo y ruta a exec. La allowlist Codex limita lo que invoca ese agente, no el socket de otros procesos. bpy directo quita superficie de red, pero solo mejora seguridad si las operaciones se acotan; script arbitrario mantiene el riesgo de ejecución con permisos de usuario.

Ambas opciones pueden satisfacer edición, persistencia, validación, exportación y recuperación. Sin prueba local no hay conclusión de compatibilidad ARM64 ni de calidad imprimible. Para MVP, MCP condicionado reduce trabajo propio; si no se acepta el socket anónimo, evaluar bpy mediante entradas limitadas antes de implementar.

Fuentes: [socket y handlers](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/addon.py#L1116-L1455), [exec](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/addon.py#L2129-L2154), [safe mode](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/safe_mode.py), [Codex MCP config](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [Blender CLI](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html).

