# ADR-0001 — Ejecución directa con `bpy` en lugar de MCP for Blender

**Estado: ACEPTADA en lo operativo (2026-11-02); motivo y aceptación de riesgo por documentar.** La ejecución directa es la arquitectura vigente. Este texto reconstruye la decisión desde la evidencia y no sustituye el motivo declarado por el responsable.

## Contexto

- META, ARQ-001, FLU-001 y SYN-01 definen la arquitectura con MCP for Blender (ahujasid).
- SEC-008 (SHA `992233bb…`, sin ejecución): socket TCP localhost:9876 sin autenticación por operación y `execute_code` → `exec` dentro de Blender. Dictamen **APTO CON CONDICIONES**, opción B (MCP con mitigaciones) o C (bpy directo con operaciones acotadas) si no se acepta el riesgo del socket.
- SEC-007 compara ambos: bpy elimina listener y dispatch, pero sigue ejecutando Python con permisos del usuario.
- EXP-BPY-001…005 se ejecutaron con bpy en procesos background. MCP no se usó en ningún experimento (`EXP-BPY-003/reports/RESULTADO.md`; `CIERRE_FASE_1` §2).
- Los protocolos MCP (EXP-001/002/003 en `archivo/investigacion_mcp/ola_d/`) siguen NOT RUN.

## Decisión propuesta

Adoptar ejecución directa: Codex genera scripts `bpy` versionados, se ejecutan con Blender en background con perfil/HOME/TMP aislados, y la validación corre en un proceso independiente. Cada edición escribe un archivo nuevo; no se sobrescriben revisiones aceptadas.

## Evidencia a favor (verificada en el repositorio)

- Cinco experimentos completados, incluyendo edición, snapshot, STL y reimportación.
- No hay socket ni servicio persistente.
- Cada proceso queda con log, exit code y metadatos (`run_blender.py` en EXP-BPY-003).

## Evidencia en contra / límites

- No hay comparación experimental con MCP: la ventaja es de seguridad y simplicidad, no una medición de rendimiento.
- bpy no es un sandbox. Un script arbitrario tiene los permisos del usuario; la mitigación real es acotar y revisar los scripts.
- Se pierde el bucle visual interactivo de META. Hoy se sustituye abriendo el `.blend` en la GUI.

## Cuándo reabrir

Reevaluar MCP solo si el bucle por lotes resulta demasiado lento o impide la revisión visual en CU-01. En ese caso aplicar las 8 condiciones de SEC-008 antes de cualquier EXP-001.

## Datos que faltan (los aporta el responsable)

- Motivo real del pivote: ¿seguridad (socket sin autenticación), simplicidad o disponibilidad? **[pendiente]**
- Aceptación o rechazo explícito del riesgo residual de MCP descrito en SEC-008. **[pendiente]**
- Fecha y responsable de la decisión. **[pendiente]**
