# EXP-BPY-005 — Impresión física supervisada

**Estado:** `NOT RUN` (no hay evidencia de impresión física).  
**Preparación documental:** lista para revisión, con un bloqueo sobre la identidad del preset de proceso.  
**Run ID de preparación:** `EXP-BPY-005-20261102T153524Z`.

Esta ejecución cierra la cadena digital de la placa de EXP-BPY-003 y deja preparado su contraste físico en una Creality K1C, boquilla de 0,4 mm y PLA. La impresión la inicia y supervisa la persona responsable; este experimento no controla la impresora.

## Archivos

- [Protocolo de impresión](PROTOCOLO_IMPRESION.md)
- [Registro de impresión](REGISTRO_IMPRESION.md)
- [Mediciones físicas](MEDICIONES_FISICAS.md)
- [Evaluación de calidad](EVALUACION_CALIDAD.md)
- [Aprendizajes operativos](APRENDIZAJES_OPERATIVOS.md)
- [Resultado provisional](reports/RESULTADO.md)
- [Manifiesto](MANIFIESTO_ARTEFACTOS.json)

## Entrada aprobada

- STL fuente: `../EXP-BPY-003/artifacts/EXP-BPY-003-20261102T144300Z_relief_plate.stl`
- SHA-256: `c6342d689ef70742ae0f9b3d6bbbf32b4f0f542ef7a5b6be2645f3205755b3d3`
- Copia de EXP-BPY-004 verificada: `../EXP-BPY-004/artifacts/EXP-BPY-004-20261102T121521-0300_input.stl`
- SHA-256 de la copia: el mismo que la fuente.

No se copia ni se altera el STL en esta preparación. La configuración de laminado y su autorización deben resolverse antes de imprimir.

## Cómo completar después de autorización

1. Resolver la discrepancia de preset anotada en el protocolo y aprobar una ficha final.
2. Registrar que la persona responsable revisó impresora, material físico, cama, boquilla y laminado.
3. La persona responsable inicia y supervisa la impresión en la K1C.
4. Completar el registro de impresión, mediciones y evaluación con datos y fotos reales.
5. Actualizar el manifiesto y el resultado sin borrar el estado `NOT RUN` histórico.

No usar los valores estimados como mediciones físicas. Los criterios de tolerancia física siguen pendientes de aprobación.
