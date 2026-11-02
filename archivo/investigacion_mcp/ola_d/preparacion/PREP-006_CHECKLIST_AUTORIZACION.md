# PREP-006 — Checklist previo a solicitud de autorización

Fecha de revisión: 2026-11-02. Estados: READY = evidencia suficiente para el punto documental/local; BLOCKED = condición pendiente que impide el experimento; UNKNOWN = no comprobado; NOT APPLICABLE = no aplica al alcance actual. UNKNOWN nunca se convierte implícitamente en READY.

| Requisito | Estado | Evidencia / pendiente |
|---|---|---|
| Commit candidato identificado | READY | SHA completo 992233bb258975a05eec8b5691465c50c2831e34 en SEC-005 y enlaces permanentes |
| Addon correspondiente al commit | BLOCKED | El árbol candidato contiene addon empaquetado correspondiente; no hay instalación local detectada ni hash local que lo demuestre |
| Versiones locales registradas | BLOCKED | macOS, Codex CLI, Python y uv registrados; Blender, addon y MCP no están identificados localmente |
| Configuración Codex MCP de Blender | READY para estado actual | Se inspeccionó sin mostrar secretos; no existe servidor Blender configurado |
| enabled_tools soportado/verificado en Codex local | UNKNOWN | No se modificó ni probó configuración; Codex CLI es 0.166.0 |
| Herramientas de escena limitadas técnicamente a lectura | BLOCKED | get_scene_info y ciertos caminos de look invocan execute_code; get_addon_status no basta para EXP-001 |
| Riesgo residual del socket documentado | READY | Loopback no autentica procesos locales; ejecución puede ocurrir dentro de Blender |
| Bind real solo loopback | UNKNOWN | No hay instancia candidata activa; requiere observación autorizada durante EXP-001 |
| Directorio/escena desechable aislados | BLOCKED | No existe directorio dedicado detectado y no se creó durante esta fase |
| Política de telemetría revisada | UNKNOWN | No hay instalación local del candidato; configuración efectiva no verificada |
| Evidencias y logs definidos | READY | Runbook y D-06 describen registro local; falta confirmar rutas efectivas al ejecutar |
| Plan de reversión definido | READY | PREP-005 define respaldo, cierre, restauración y tratamiento de estado incierto |
| EXP-001 ejecutado | NOT APPLICABLE | Sigue NOT RUN; esta tarea es preparación |
| Autorización explícita | BLOCKED | Pendiente del responsable y solo después de resolver los bloqueos técnicos |

## Discrepancia relevante para decisión

El supuesto anterior de que la allowlist de Codex bastaría para obtener una sesión de inspección solamente de lectura no se sostiene para todas las rutas de get_scene_info/look en el commit auditado: el servidor puede ejecutar internamente Python en Blender. Esta discrepancia debe revisarse explícitamente en SEC-008 y EXP-001 antes de pedir autorización. El filtro de herramientas tampoco protege el socket frente a otro proceso local.

## Decisión de preparación

**NOT READY.** No solicitar todavía autorización de EXP-001. Primero se debe resolver el bloqueo de ejecución interna Python, determinar el mecanismo técnico de inspección acotada o redefinir formalmente el riesgo y alcance; además, acreditar el addon instalado y preparar aislamiento y versiones. La autorización futura deberá cubrir instalaciones/configuración, activación, inicio del listener, conexiones MCP, escritura de evidencias y reversión.

Documentos de apoyo: PREP-001 a PREP-005, SEC-005 a SEC-008 y EXP-001_CONECTIVIDAD.md. Ningún experimento se ejecutó.
