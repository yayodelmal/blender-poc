# D-06 — Registro mínimo y mejora operativa
**Estado:** diseño de preparación; sin configuración, ejecución o framework nuevo.

## Fuentes y reutilización

INV-08 documenta logs de Blender; logger/context JSONL opt-in/trajectory del MCP; y eventos JSONL de Codex CLI/OTel opcional. Ninguna capa cubre el ciclo completo ni valida geometría. En particular, `world_state` snapshots MCP no son `.blend` probados ni restauración. Se recomienda un manifiesto por operación que apunte a logs existentes, no un colector nuevo. Fuentes: [Codex modo no interactivo](https://learn.chatgpt.com/docs/non-interactive-mode), [Codex config](https://learn.chatgpt.com/docs/config-file/config-advanced), [MCP logging](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/logging), [MCP repo y privacidad/telemetría](https://github.com/ahujasid/mcp-for-blender).

## Registro mínimo por operación

Usar Markdown local para la primera ejecución revisada; JSONL solo si se precisa agregar datos automáticamente y tras aprobar formato. Un evento contiene:

| Campo | Contenido |
|---|---|
| `operation_id` | UUID aleatorio, único entre operaciones |
| `request` | Solicitud original saneada, idioma y timestamp TZ |
| `base_revision` / `candidate_revision` | IDs de contrato, `.blend` y ruta snapshot/candidato |
| `tools` | Herramienta MCP invocada, transporte, argumentos relevantes saneados, duración |
| `versions` | Codex app/CLI y modelo, Blender/build/arquitectura, addon/servidor, Python/uv, validador, Creality si aplica |
| `execution_status` | SUCCESS / ERROR / UNCERTAIN; error de protocolo separado del error de tool |
| `measurements` | ID check, valor esperado/observado, unidad, tolerancia, objeto evaluado y método |
| `validation_results` | PASS / FAIL / INCONCLUSIVE / NOT RUN por Vxx |
| `errors_retries` | clase FLU, error saneado, intento, acción y motivo para repetir |
| `recovery` | snapshot verificado, restauración intentada/abierta, mediciones antes/después y resultado |
| `final_decision` | candidato aceptado digital, rechazado, laminado registrado o pendiente; actor que decide |
| `evidence` | Rutas, checksums cuando el mecanismo esté aprobado, capturas/logs referenciados |

No guardar credenciales, prompts ajenos, datos personales ni código completo salvo requisito explícito; redactar rutas sensibles. Acordar retención antes de activar trajectory remoto u OTel. Telemetría opcional no se habilita por defecto.

## Reconciliación entre logs

Ordenar por `operation_id` y timestamp UTC/local con offset. Como las herramientas no necesariamente propagan un ID común, registrar el inicio/fin de turno, llamada MCP y revisión visible en una ficha del agente. Si una fuente no produce correlation ID, asociar por timestamps y secuencia como inferencia, marcar confianza, no inventar unión exacta. La escena y sus mediciones son evidencia de resultado; texto de Codex o logs solos no lo son.

## Aprendizaje operativo

1. Clasificar fallo (INT/EXE/GEO/FDM/STA/VAL) y reproducirlo con versión y entrada conocidas.
2. Formular causa como hipótesis; definir un caso controlado y métrica previa.
3. Cambiar procedimiento/selección de herramienta, no el modelo aprendido; volver a ejecutar mismo control y casos vecinos.
4. Aceptar la corrección solo si el fallo objetivo deja de ocurrir, invariantes conservadas y no aparecen regresiones; guardar evidencia.
5. Añadir nota/versionado de procedimiento; marcar alcance y casos donde no aplica. Retirar o revertir si falla una repetición.

Registrar un fallo no significa que Codex lo recuerde o se entrene. Memoria consultable requeriría recuperación explícita de notas; actualización de pesos no está propuesta. Métricas iniciales: aceptación al primer intento con denominador/exclusiones; intentos por operación; restauraciones intentadas/comprobadas; V inconclusas/no ejecutadas; tiempo hasta STL/lámina revisados; recurrencia por causa/versión.

**Recomendación:** registro local manual con referencias a logs de las capas ya existentes; evaluar automatización solo si tres o más pruebas demuestran una carga de correlación repetida. No sumar base de datos, OTel collector, backend cloud o multiagentes para esta fase.
