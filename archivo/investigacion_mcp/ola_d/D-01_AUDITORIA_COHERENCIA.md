# D-01 — Auditoría de coherencia CON-001 / VAL-001
**Estado:** completada documentalmente; propuestas corregidas IN PROGRESS. **No se ejecutó Blender.**

## Hallazgos y correcciones trazables

| Hallazgo | Antes | Corrección | Trazabilidad |
|---|---|---|---|
| R02 (pared) asignaba V05 sin alcance explícito | Referencia válida, pero implícita | V05 mide pared; sigue bloqueada por selección 2/20 mm | CON-001 R02; VAL-001 V05 |
| R03/R04 no separaban presencia geométrica de función de drenaje | V05 genérica y R04 también referenciaba V03 | V05 cubre presencia/espesor/conducto; flujo requiere ensayo separado | CON-001 R03/R04; VAL-001 V05 |
| R05 apuntaba a V03/V04 sin topología explícita | V08 cubría topología pero no estaba enlazada desde requisito | Añadido V08 para topología y V03 para geometría de relieve/esquinas | CON-001 R05; VAL-001 V03/V08 |
| R06 apuntaba a V06 (recuperación) como prueba de edición | Confundía rollback con edición incremental | V04 prueba cambio; V02 mide; V03 verifica patrón | CON-001 R06; VAL-001 V02–V04/V06 |
| R07 omitía reapertura y compartía V06/V09 | Editabilidad y laminado mezclados | V04 prueba editabilidad/reapertura; V06 solo snapshot/recuperación | CON-001 R07; VAL-001 V04/V06 |
| R08 apuntaba V07/V08 y omitía laminado | No cubría Creality Print | Añadido V09 (laminado) y enlaces V07 exportación/V08 topología | CON-001 R08; VAL-001 V07–V09 |
| R09 apuntaba a V08 (topología) | El perfil de impresora no se prueba en topología | R09 enlaza V09; V10 solo protocolo físico si se acuerda | CON-001 R09; VAL-001 V09/V10 |
| Estado ACEPTADO DIGITAL ambiguo | Parecía incluir laminado e impresión | Definido como V02–V08 aplicables; laminado V09 puerta separada; V10 física aparte | CON-001 estados; VAL-001 secuencia |
| Snapshot/restauración se describían como existencia de archivo | No verificaba apertura ni recuperación real | V06 exige reapertura, revisión, invariantes; fallo bloquea mutación/reintentos | CON-001 precondición; VAL-001 V06 |
| Sin barrera para ediciones concurrentes | Un snapshot viejo podía sobrescribir cambio humano | Revisar revisión/estado observado antes de promover/restaurar | CON-001; SYN-02 regla 8 |

## Referencias cruzadas consolidadas

R01→V02; R02/R03/R04→V05; R05→V03/V08; R06→V02/V03/V04; R07→V04/V06; R08→V07/V08/V09; R09→V09 y opcional V10. Las verificaciones V01 y controles de ejecución (snapshot, estado incierto, etc.) son precondiciones/procedimiento, no requisitos geométricos adicionales.

## Ambigüedades que se conservan para aprobación

No se resolvieron pared, base, drenaje, si 150×150 incluye relieve, tolerancia, tamaño/profundidad/juntas de ladrillo ni definición de prueba física. R01 incluye relieve solo como propuesta provisional. ±0,10 mm y 0,05 mm son umbrales de ensayo propuestos, no estándares ni valores aprobados.

**Estados acordados en borrador:** `PASS`, `FAIL`, `INCONCLUSIVE`, `NOT RUN`; ninguna condición incierta se interpreta como PASS. El estado de ejecución de herramienta permanece separado del veredicto de cada verificación.
