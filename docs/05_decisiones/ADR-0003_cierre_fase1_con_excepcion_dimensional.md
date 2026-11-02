# ADR-0003 — Cierre de Fase 1 con excepción dimensional documentada

**Estado: ACEPTADA por el responsable (2026-11-02T17:45Z).** Evidencia del experimento: [`EXCEPCION_DIMENSIONAL_…md`](../../experimentos/EXP-BPY-005/EXCEPCION_DIMENSIONAL_EXP-BPY-005-20261102T173135Z.md).

## Contexto

- `archivo/documentos_originales/CIERRE_FASE_1_LABORATORIO_CAD.md` §1 y §9 y `PROTOCOLO_IMPRESION.md` exigen que Fase 1 termine con contraste físico: "impresión, fotos y medidas reales".
- EXP-BPY-001 a 004 tienen su estado final (ver [ESTADO_FASES](../06_estado/ESTADO_FASES.md)). En EXP-BPY-005 hay impresión, 3 fotos y evaluación visual favorable. No hay mediciones.
- El responsable decidió no medir, por considerar suficiente la inspección visual para una prueba de concepto exploratoria.

## Decisión

Declarar **Fase 1: CERRADA POR DECISIÓN DEL RESPONSABLE, CON EXCEPCIÓN DIMENSIONAL DOCUMENTADA.**

Esta denominación **no** significa que se cumpliera el criterio de cierre. El criterio dimensional físico queda **NOT RUN — omitida por decisión del usuario**. El veredicto técnico de EXP-BPY-005 se conserva sin forzar un PASS, y la autorización del responsable para continuar se registra por separado.

## Qué sí está y qué no está verificado

| Verificado | No verificado |
|---|---|
| Flujo digital en un proxy: crear, editar, snapshot, STL, laminado (EXP-BPY-001 a 004) | Dimensiones físicas frente a ±0,5 mm |
| Impresión completada (declarada, con 3 fotos) | Adhesión entre capas, resistencia, deformación cuantificada |
| Inspección visual favorable (27 relieves, juntas definidas) | Exactitud dimensional de la K1C con este perfil |
| Ficha de laminado aprobada y registrada | Repetibilidad física (una sola impresión) |

## Consecuencias

1. Se puede avanzar al siguiente experimento digital sin esperar medidas.
2. **La excepción no se hereda.** Antes de dar por válida cualquier pieza de CU-01 en lo dimensional hay que medirla (V10 de [VAL-001](../03_contratos/VAL-001.md)). La tolerancia ±0,5 mm no puede reutilizarse sin medición previa.
3. Cualquier afirmación sobre exactitud dimensional del proceso físico debe citar este ADR como limitación.
4. Si se miden las piezas más adelante, se registra una adenda; no se reescribe este ADR ni los informes.

## Siguiente experimento

Demostrar que el patrón de ladrillos se modifica de forma paramétrica conservando las dimensiones e invariantes del modelo (R06). Ver [ESTADO_FASES](../06_estado/ESTADO_FASES.md).
