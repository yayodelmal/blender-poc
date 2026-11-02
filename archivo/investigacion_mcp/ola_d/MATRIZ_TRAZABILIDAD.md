# Matriz de trazabilidad de requisitos y experimentos
**Estado:** propuesta para revisión. Rxx/Vxx proceden de CON-001/VAL-001; EXP no ejecutados.

| Requisito | Fuente/estado | Verificación | Evidencia prevista | Experimento | Bloqueo/nota |
|---|---|---|---|---|---|
| R01 150×150×60 mm exterior | CU-01; referencia incluye relieve aún provisional | V02 | bounds world evaluados y STL | EXP-003 | Decidir cuerpo vs envolvente final |
| R02 espesor pared 2 o 20 mm | pendiente | V05 | mediciones y sección | CU-01 posterior | Responsable debe decidir; no se asume |
| R03 base/presencia/espesor | pendiente | V05 | inspección/medición | CU-01 posterior | Decidir |
| R04 drenaje | pendiente | V05; flujo físico aparte | geometría, dimensiones, eventualmente protocolo flujo | CU-01 posterior | Decidir parámetros; función de flujo no se prueba aquí |
| R05 ladrillos geométricos 4 caras/esquinas | confirmado con detalle pendiente | V03 y V08 | malla evaluada, secciones, componentes, capturas | EXP-003 pieza proxy; luego CU-01 | Profundidad, juntas y continuidad a acordar |
| R06 edición patrón preserva invariantes | confirmado | V02/V03/V04 | before/after y medidas | EXP-002 y EXP-003 | EXP-002 proxy simple |
| R07 maestro editable y restaurable | objetivo confirmado | V04/V06 | `.blend` A/B, reopen y restore comprobado | EXP-002 | snapshot fallido bloquea mutación |
| R08 STL y preparación en Creality | objetivo confirmado | V07/V08/V09 | STL reimportado, reporte, proyecto/capturas de laminado | EXP-003 para export; experimento laminado futuro | CLI no probado; laminado ≠ impresión |
| R09 K1C/PLA/0,4 mm | contexto confirmado; perfil pendiente | V09 (V10 si física) | captura del perfil/proyecto | futuro laminado/impresión | Definir perfil y parámetros si se imprime |
| MCP conexión/lectura | INV-01 capacidad documental; local desconocido | D-03 conectividad | versiones, tool list, status, inventario, logs | EXP-001 | Aprobación previa y revisión de #404 |
| snapshot/revisión sin conflicto | CON-001 precondición | V06 | archivo reabierto, ID/revisión e invariantes; registro de conflicto | EXP-002 | Resolver método de copia |
| topología no es impresión validada | VAL-001 | V08/V09/V10 separados | reportes topológicos, trayectorias, medición física | EXP-003/futuro | No prometer fuerza/función a partir de watertight |

**Estados:** PASS requiere criterio explícito y evidencia observada; FAIL incumple; INCONCLUSIVE no permite concluir; NOT RUN sin ejecución. Para arquitectura completa no hay R aceptado mediante pruebas propias a esta fecha.
