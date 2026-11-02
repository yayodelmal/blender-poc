# Trazabilidad vigente: requisito → verificación → experimento

**Fecha:** 2026-11-02. **Reemplaza como referencia vigente a:** `archivo/investigacion_mcp/ola_d/MATRIZ_TRAZABILIDAD.md`, que apuntaba a protocolos MCP nunca ejecutados. Requisitos Rxx de [CON-001](CON-001.md); verificaciones Vxx de [VAL-001](VAL-001.md).

Estados: PASS, FAIL, INCONCLUSIVE, NOT RUN según VAL-001. "Proxy" significa que se probó en una pieza de ensayo, no en CU-01.

## Verificaciones

| V | Qué verifica | Experimento | Estado | Alcance real |
|---|---|---|---|---|
| V01 | Contrato resuelto sin requisitos bloqueantes | — | **NOT RUN** | Pared, base, drenaje y alcance de 150 mm siguen pendientes |
| V02 | Dimensiones | EXP-BPY-001 (cubo 50 mm), EXP-BPY-002 (50×50×70 mm), EXP-BPY-003 (80×60×5 mm) | PASS (proxy) | Tolerancia ±0,01 mm experimental; no ±0,10 mm propuesta en CON-001 |
| V03 | Relieve físico en caras y esquinas | EXP-BPY-003 | PASS (proxy, placa plana) | 27 ladrillos sobre una cara; no cubre las 4 caras ni esquinas |
| V04 | Editabilidad e incrementalidad | EXP-BPY-002 | PASS (proxy) | Edición in-place de un cubo (escalar Z). No se cambió tamaño de ladrillo |
| V05 | Espesor, base y drenaje | — | **NOT RUN** | Bloqueado por decisiones humanas |
| V06 | Snapshot, restauración y conflicto | EXP-BPY-002, EXP-BPY-003 (snapshot) | PASS con salvedades | Conflicto simulado; guard corregido tras dos intentos defectuosos |
| V07 | Exportación STL y relectura | EXP-BPY-003 | PASS | Convención mm documentada; un control de escala errónea detectado |
| V08 | Topología y conectividad | EXP-BPY-001, 002, 003 | PASS | Manifold, un componente, volumen positivo; BVH acotado |
| V09 | Laminado en Creality Print | EXP-BPY-004 (run `155417Z`) | PASS (digital) | Sin G-code; 27 relieves por conteo visual; aviso de adhesivo abierto |
| V10 | Impresión física | EXP-BPY-005 | Impresión hecha y evaluada visualmente (PASS visual cualitativo); **medición dimensional NOT RUN — omitida por decisión del usuario** | Tolerancia ±0,5 mm aprobada para el cupón y sin verificar; excepción de [ADR-0003](../05_decisiones/ADR-0003_cierre_fase1_con_excepcion_dimensional.md), no heredable a CU-01 |

## Requisitos

| R | Requisito | Cubierto por | Estado |
|---|---|---|---|
| R01 | Exterior 150×150×60 mm | V02 (solo proxies) | Sin evidencia sobre CU-01 |
| R02 | Pared 2 o 20 mm | V05 | Pendiente del responsable |
| R03 | Base | V05 | Pendiente |
| R04 | Drenaje | V05 | Pendiente |
| R05 | Ladrillos geométricos en 4 caras, esquinas continuas | V03, V08 | Parcial (placa plana) |
| R06 | Cambiar el patrón sin reconstruir ni alterar dimensiones | V02, V03, V04 | **Sin evidencia**: no se ha cambiado el tamaño del ladrillo; parámetros no reactivos |
| R07 | Maestro editable y restaurable | V04, V06 | PASS en proxy |
| R08 | STL validado y laminado | V07, V08, V09 | PASS en proxy (digital) |
| R09 | K1C, PLA, 0,4 mm | V09 (y V10) | Laminado Standard hecho; impresión de proxy hecha con inspección visual favorable; sin medición dimensional |

## Lectura rápida

El pipeline digital tiene evidencia en un proxy. CU-01 tiene cero cobertura propia: faltan decisiones de diseño (V01, V05) y la prueba de R06.
