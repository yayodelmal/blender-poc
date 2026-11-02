# SEC-008 — Dictamen y decisión

**Fecha:** 2026-11-02. **Código:** ahujasid/mcp-for-blender, SHA 992233bb258975a05eec8b5691465c50c2831e34. **EXP-001/002/003:** NOT RUN.

## Dictamen

**APTO CON CONDICIONES**, únicamente para una prueba local acotada. No es certificación ni cubre procesos locales adversariales o el artefacto instalado no verificado.

- Addon enlaza localhost:9876 por defecto en AF_INET/SOCK_STREAM. Resolución efectiva no probada.
- No se observa autenticación o autorización por operación en el socket.
- execute_blender_code conduce a execute_code y exec dentro de Blender con sus permisos.
- Safe mode es opt-in, solo cubre la ruta MCP y permite mutaciones, guardado e import/export.
- Codex permite limitar herramientas mediante enabled_tools; se puede excluir el tool genérico para el agente, sin proteger el socket de otros clientes locales.
- El issue #404 sigue abierto, declara versión 1.6.0 y no demuestra por sí solo el estado de esta revisión. El SHA actual conserva la misma clase de riesgo: socket sin autenticación y ejecución Python. El issue no muestra rama ni PR de corrección, y no se identificó un parche que elimine ambos comportamientos. [Issue #404](https://github.com/ahujasid/mcp-for-blender/issues/404).

## Decisión recomendada

**B. Mantener MCP for Blender únicamente con mitigaciones verificables.**

Para Codex como agente único y prueba local de usuario único, la allowlist del cliente puede limitar la capacidad del agente y conservar la reutilización del puente. Esta recomendación requiere aceptación expresa del riesgo de que otros procesos locales puedan alcanzar el endpoint. No recomienda MCP para un entorno multiusuario o con procesos locales no confiables.

Si ese riesgo no es aceptable, evaluar C (bpy directo) con operaciones y entradas limitadas, archivos candidatos y validación. Python arbitrario por bpy no sería una mitigación.

## Condiciones antes de solicitar EXP-001

1. Aceptar por escrito que un proceso local podría alcanzar el socket y emitir comandos con permisos de Blender.
2. Fijar artefactos. PyPI 2.2.6 tiene hashes publicados, pero comparar contenido con Git y registrar hash del addon cargado.
3. No aceptar actualización del addon desde main durante el ensayo.
4. Configurar enabled_tools con las herramientas mínimas de inspección; excluir execute_blender_code y tools de escritura. Capturar la lista efectiva visible antes de consultar Blender.
5. Usar Blender desechable, sin archivos sensibles ni claves API, sin túneles; comprobar bind efectivo cuando haya autorización.
6. Desactivar telemetría explícitamente y registrar el estado. Safe mode no es read-only ni sandbox.
7. Definir evidencia, logs, cierre y recuperación; tras timeout no repetir hasta verificar el estado.
8. Solicitar autorización separada. Este dictamen no autoriza la ejecución.

## Siguiente secuencia

1. EXP-001 con allowlist Codex de solo lectura.
2. Revisar herramientas, logs, bind/cierre y aceptar o rechazar el riesgo residual.
3. EXP-002 después de aprobación separada para escritura.
4. EXP-003 tras validar recuperación y geometría.

**Riesgo residual:** alto frente a proceso local adversarial; moderado para sesión aislada de usuario único con aceptación explícita. localhost limita la red usual, pero no autentica. Codex allowlist limita solo el cliente Codex.

## Respuestas

| Pregunta | Respuesta |
|---|---|
| Código exacto | Árbol Git con SHA completo arriba. Wheel PyPI 2.2.6 tiene digest, aún no comparado byte a byte. |
| Bind | localhost:9876 por defecto, IPv4 TCP; resolución macOS pendiente. |
| Quién conecta | Cualquier proceso que alcance listener; sin auth/ACL identificadas. |
| Python arbitrario | Sí, execute_code llama exec() en Blender. |
| EXP-001 lectura | Sí para Codex con enabled_tools verificado; no para clientes locales externos. |
| #404 | Pertinente como clase de riesgo, aunque reportó 1.6.0. |
| MCP o bpy | MCP con condiciones; bpy acotado si no se acepta socket sin auth. |

## Actualización trazable respecto a SEC-001 / D-02

SEC-001 no tenía SHA ni inspección del socket. Este informe fija la fuente y confirma bind, dispatch, exec y safe mode. PyPI 2.2.6 sí tiene artefactos con hashes, aunque no se probó identidad con Git. SEC-001 se conserva como registro histórico; SEC-008 actualiza esos puntos.

Fuentes: [commit](https://github.com/ahujasid/mcp-for-blender/commit/992233bb258975a05eec8b5691465c50c2831e34), [socket](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/addon.py#L1116-L1455), [exec](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/addon.py#L2129-L2154), [safe mode](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/safe_mode.py), [PyPI digests](https://pypi.org/pypi/mcp-for-blender/2.2.6/json), [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [issue #369](https://github.com/ahujasid/mcp-for-blender/issues/369).

