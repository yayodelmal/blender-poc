# Plan de ejecución experimental — Ola D
**Estado:** preparación únicamente. EXP-001 está pendiente de autorización explícita; ningún protocolo se ha ejecutado.

## Puertas de entrada

Antes de conectividad: verificar fuente/hash y seguridad de versión MCP; decidir exposición aceptable del socket #404; recoger versiones existentes solo si se autoriza lectura local. La presente ola no inspeccionó la máquina. Aprobar evidencia a retener y telemetría. Preparar carpeta de ensayo aislada y criterios de limpieza. No instalar ni tocar preferencias sin alcance aprobado.

## Secuencia

| Orden | Experimento | Entrada/condición | Salida exigida | Avance |
|---|---|---|---|---|
| 0 | Aprobación de diseño y seguridad | Resolver D-02; autorización explícita EXP-001 | Versiones candidatas, threat decision, scope firmado/revisado | Si no, detener |
| 1 | [EXP-001](EXP-001_CONECTIVIDAD.md) Conectividad lectura | Seguridad MCP aceptada; servidor/addon disponibles | Status, inventario comparado con UI, escena intacta, logs error/desconexión, PASS | Requiere nueva autorización antes de ejecución; FAIL/INCONCLUSIVE detiene |
| 2 | [EXP-002](EXP-002_EDICION_PERSISTENCIA.md) Estado y edición | EXP-001 PASS; tolerancia de proxy y snapshot acordados | `.blend` reabre, modificación incremental, negativo detectado y restore medido | PASS para dependencias de maestro |
| 3 | [EXP-003](EXP-003_GEOMETRIA_STL.md) Geometría/relieve/STL | EXP-002 PASS; herramientas disponibles versionadas | relieve en malla evaluada y STL, controles, dimensiones/topología | PASS permite diseño de laminado |
| 4 | EXP-004 (por diseñar) Creality Print | EXP-003 PASS, versión/profile aprobado | GUI y quizá CLI verificados por separado; escala y trayectorias registradas | No se envía a impresora automáticamente |
| 5 | CU-01 macetero | Todas previas; espesor/base/drenaje, tolerancias y relieve acordados | aceptación V02–V09; versión y artefactos reproducibles | Decisión específica antes de prototipar |
| 6 | Impresión física controlada | CU-01 laminado revisado y prueba física autorizada | dimensiones/función/defectos medidos conforme protocolo nuevo | No inferir de fase digital |

## Reglas de avance y detención

- Un PASS solo se declara con artefactos y criterio cumplido; documentación no es resultado experimental.
- FAIL: corregir causa en diseño aislado y repetir experimento pertinente; registrar versión y cambios.
- INCONCLUSIVE: resolver medición/instrumentación sin aumentar alcance; no promocionar.
- NOT RUN: registrar motivo (sin autorización, dependencia o recursos).
- Snapshot previo no comprobado, restauración fallida o edición humana concurrente: detener mutaciones y reconciliar estado.
- Solo un Codex controla operaciones de la arquitectura del pipeline. La persona revisa decisiones, excepciones y resultados.

## Primera acción recomendada

**No EXP-001 todavía:** primero revisión documental estática del release/commit candidato del MCP para responder si socket se enlaza a localhost y si #404 es aplicable; después llevar al responsable la matriz de versiones y riesgo. La primera acción experimental, si es autorizada posteriormente, será EXP-001 de solo lectura en escena desechable. En esta entrega queda **NOT RUN**.
