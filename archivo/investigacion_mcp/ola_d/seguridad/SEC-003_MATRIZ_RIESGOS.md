# SEC-003 — Matriz de riesgos y mitigaciones
Escala cualitativa: crítica = ejecución/cambio de datos con permisos del proceso; alta = exposición relevante condicionada; media = privacidad/operación. Confianza mide evidencia recuperada, no certeza de explotación local.

| ID | Riesgo / evidencia | Severidad | Confianza | Mitigación y clase | Residual / condición |
|---|---|---:|---:|---|---|
| S-01 | Socket del addon sin autenticación y Python `exec`, reportado en 1.6.0 (#404) | Crítica si presente | Alta para 1.6.0; baja para 2.2.6 | No usar puente hasta identificar código corregido. Auth/allowlist probablemente requiere upstream/código si no existe. | No EXP-001 hasta revisar tag/SHA y solución. |
| S-02 | Cliente `localhost` default; `--host`/`BLENDER_HOST` pueden cambiar destino; bind addon no confirmado | Alta condicional | Media | Configurar loopback solo si addon lo soporta y revisión lo confirma; no túneles ni LAN | Loopback no autentica procesos locales. |
| S-03 | `execute_blender_code` reenvía Python a Blender | Crítica | Alta en `main`, release incierta | Tool read-only efectiva no acreditada; bloqueo técnico del sink o no uso del puente | Prompt del agente no es control de acceso. |
| S-04 | Código Python corre con permisos del proceso Blender | Crítica | Alta si #404 aplica; candidato pendiente | Usuario/carpeta aislados y mínimo privilegio; requiere configuración, no sandbox MCP | Reduce radio de impacto, no evita abuso del proceso local. |
| S-05 | Integraciones de assets llaman servicios externos y pueden usar claves | Alta condicional | Media en `main` | No invocar ni proporcionar keys; deshabilitar tool si la versión lo soporta | Revisar paquete exacto y llamadas de arranque. |
| S-06 | Telemetría mínima reportada activa por defecto; contenido opt-in según README | Media privacidad | Media para README actual, no candidata | `DISABLE_TELEMETRY=true` documentado; requiere config y validar en hash fijado | Sin análisis de tráfico no se confirma alcance. |
| S-07 | Timeout/cierre podría dejar estado incierto | Media | Media/estática parcial | Cierre normal como procedimiento; confirmar stop/unregister exacto antes de prueba | No probado dinámicamente. |
| S-08 | Safe mode/`read_only` puede confundirse con autorización real | Alta | Media-baja | Revisar implementación completa; no tratar como límite hasta demostrarlo | La tool genérica sigue siendo el problema. |

## Mitigaciones por capacidad

| Medida | Estado | Observación |
|---|---|---|
| Bind loopback | No verificable en addon exacto; el cliente usa `localhost` por defecto | Issue #369 dice que en su contexto addon solo escuchaba localhost; no acredita versión actual/IP precisa. |
| Sesión/privilegios mínimos | Requiere configuración/operación | Reduce blast radius; no es sandbox. |
| Allowlist/solo lectura | No verificada nativamente | `_run_script(... read_only=True)` es parámetro del wrapper; tool Python general disponible. |
| Desactivar telemetría | README actual documenta configuración | `DISABLE_TELEMETRY=true`; confirmar código por hash. |
| Evitar túneles/LAN | Medida operativa | No protege de proceso local con acceso al listener. |
| Cerrar servidor | Procedimiento, implementación no confirmada | Verificar stop/unregister y cierre en fase autorizada. |
| Restaurar config | Procedimiento | Nada se modificó en esta auditoría. |

## Riesgo residual

No puede aceptarse formalmente mientras la versión/addon no sean identificables. No hay evidencia suficiente para llamar 2.2.6 vulnerable ni corregida. Loopback no autentica procesos locales. La política conversacional puede reducir errores accidentales, pero no constituye control de acceso.
