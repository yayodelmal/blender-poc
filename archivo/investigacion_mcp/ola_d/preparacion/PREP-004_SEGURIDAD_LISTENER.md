# PREP-004 — Seguridad del listener local

## Hechos estáticos del candidato

El addon del commit 992233bb258975a05eec8b5691465c50c2831e34 usa un socket TCP IPv4 (AF_INET/SOCK_STREAM), con host predeterminado localhost y puerto 9876, según SEC-006 y el código fijado [addon.py](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/bundled/addon.py). Esto describe la configuración del candidato; no demuestra la dirección efectiva en una futura ejecución. El cliente que usa localhost no determina por sí solo dónde escucha el addon.

El socket no incorpora autenticación ni autorización identificada. Loopback reduce exposición de red, pero no distingue Codex de otro proceso local con acceso al puerto. Un cliente local podría intentar enviar operaciones admitidas por el protocolo; execute_code amplía el impacto potencial al contexto de permisos del proceso Blender.

## Observación de esta preparación

La consulta local no encontró listener en 9876 en el instante de inspección. No se abrió ni sondeó el socket. No se inspeccionaron túneles activos con alcance concluyente, pues Blender no está presente y el listener candidato no se inició. La observación no acredita la configuración futura.

## Procedimiento observacional para una fase autorizada

Durante una sesión aprobada, registrar antes de conectar el estado de sockets y procesos mediante herramientas locales de inspección de solo lectura (por ejemplo, lsof y netstat disponibles en macOS), junto con PID, usuario y nombre de proceso propietario. Observar direcciones IPv4 e IPv6, puerto efectivo, y si la dirección corresponde exclusivamente a loopback o a interfaces más amplias. Revisar proxies/túneles configurados y redirecciones relevantes con herramientas del sistema, sin crear conexiones de prueba. Repetir la captura al cerrar Blender y confirmar que desapareció el listener y terminó el proceso previsto.

No registrar argumentos de procesos que puedan contener secretos; limitar la evidencia a PID, usuario, ejecutable, endpoint y hora. Una discrepancia entre dirección configurada y socket observado debe detener el experimento.

## Criterios observacionales

- PASS de exposición de red solo si el endpoint real está limitado a loopback, se identifica el propietario, no hay túnel/redirección relevante y el socket desaparece al cierre.
- FAIL si escucha en una interfaz externa, el proceso propietario no corresponde a la sesión prevista o permanece activo después del cierre controlado.
- INCONCLUSIVE si no se puede observar IPv4/IPv6, identificar propietario, descartar túnel relevante o demostrar el cierre.

La observación no sustituye autenticación. Riesgo residual: proceso local no confiable puede alcanzar un socket loopback no autenticado; la allowlist de Codex no limita ese proceso. También permanece riesgo de ejecución arbitraria dentro del proceso Blender si se alcanza la herramienta correspondiente.

Estado: procedimiento preparado; no ejecutado y no constituye autorización para abrir el listener.
