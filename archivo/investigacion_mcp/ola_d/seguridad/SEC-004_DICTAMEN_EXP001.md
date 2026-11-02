# SEC-004 — Dictamen de seguridad y puerta EXP-001
**Dictamen:** **INCONCLUSO** para candidato `mcp-for-blender` 2.2.6.

## Respuesta ejecutiva

| Pregunta | Dictamen |
|---|---|
| Versión exacta auditada | No fue posible fijar versión reproducible. Servidor consultado desde `main`; pyproject declara 2.2.6; SHA/tag/artefacto no verificados. Addon exacto no verificado. |
| Interfaz de socket | `main` cliente usa `localhost:9876` por defecto y permite `--host`/`BLENDER_HOST`. Bind del listener addon candidato sin confirmar. |
| ¿Autenticación? | #404 reporta que no existía en 1.6.0. No se puede responder para candidato. Localhost no equivale a auth. |
| Capacidad conectada | Wrapper `execute_blender_code` en `main` envía código al comando `execute_code`; el reporte describe `exec` en Blender. Versión candidata pendiente. |
| ¿#404 aplica? | No establecido. Reporte es 1.6.0; no se identificó fix ni se enlazó 2.2.6 a código. |
| Mitigaciones posibles | No-LAN/no túnel, sesión y permisos aislados, cierre normal, telemetría-off configurada según README. Read-only, bind exacto, autenticación y corrección del sink no acreditados. |
| Riesgo residual | Alto/indeterminado mientras tool Python y socket se ejecuten con permisos de Blender sin control de acceso verificado. |
| ¿Apto? | **INCONCLUSO**, no APTO. EXP-001 no autorizado ni ejecutado. |

## Condiciones mínimas antes de reconsiderar autorización

1. Obtener tag/commit completo y artefactos reproducibles de servidor y addon; registrar hashes y correspondencia.
2. Revisar en ese SHA bind, accept, parser, auth, handler, cleanup y dispatch; comparar con 1.6.0 y cualquier parche/PR del mantenedor.
3. Resolver si el laboratorio acepta sink Python arbitrario accesible a procesos locales. Loopback y usuario separado reducen superficie, pero no autenticación.
4. Demostrar control técnico que excluya `execute_blender_code`/escritura para EXP-001; de otro modo declarar que la lectura depende solo de política de llamada y no cumple aislamiento.
5. Confirmar bind loopback, sin configuración LAN/túnel; usar escena/carpeta desechable y permisos mínimos.
6. Revisar telemetría en artefacto exacto; sin claves de APIs externas; verificar cierre y restauración de configuración.
7. Actualizar dictamen con evidencia suficiente. Solo entonces solicitar autorización separada para correr EXP-001 de lectura.

No se otorga autorización aquí. EXP-001, EXP-002 y EXP-003 permanecen `NOT RUN`.
