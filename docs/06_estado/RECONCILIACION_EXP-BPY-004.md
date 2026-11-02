# Reconciliación del estado de EXP-BPY-004

**Fecha:** 2026-11-02. **Tipo:** nota nueva; no reescribe ningún informe histórico. Origen: auditoría documental previa a la consolidación.

## Problema

Cuatro documentos dan estados distintos para EXP-BPY-004. La diferencia viene de mezclar el estado **por run** con el estado **del experimento**.

## Runs de EXP-BPY-004

| run_id | Qué pasó | Estado propio del run | Fuente |
|---|---|---|---|
| `EXP-BPY-004-20261102T121521-0300` | Laminado con el preset ya activo `Macetero PLA 0.20mm K1C` (personalizado); 37m20s, 19,30 g | INCONCLUSIVE (preset sin equivalencia verificada, sin capturas persistentes) | `reports/RESULTADO.md` (secciones históricas) |
| `EXP-BPY-004-20261102T154038Z` | Copia de trabajo del 3MF; el 3MF terminó guardado con configuración Standard (12:50:04 -0300). Sin nuevo laminado | Interrumpido; archivo alterado, ver INC-BPY-002 | `INC-BPY-002_INTEGRIDAD_3MF.md`, `reports/REPETICION_20261102T154038Z.md` |
| `EXP-BPY-004-20261102T155417Z` | Laminado desde copia nueva del 3MF Standard custodiado; 30m36s, 14,45 g, 4,84 m | PASS (digital) | `reports/REPETICION_20261102T155417Z.md`, manifiesto |

## Declaraciones en conflicto

| Documento | Dice | Se refiere realmente a |
|---|---|---|
| `experimentos/EXP-BPY-004/reports/RESULTADO.md` (encabezado) y `MANIFIESTO_ARTEFACTOS.json` (`status`) | PASS | Cierre con el run 155417Z (`closure_run_id`) |
| `experimentos/EXP-BPY-004/README.md` (párrafo final) | INCONCLUSIVE por capa 20/Z=4,00 y falta de captura | Una lectura intermedia del run 155417Z, luego explicada |
| `archivo/documentos_originales/CIERRE_FASE_1_LABORATORIO_CAD.md` (antes `documentos/`) §3 y §6 | INCONCLUSIVE, conflicto de preset pendiente | Estado anterior al run 155417Z; no menciona INC-BPY-002 |
| `experimentos/EXP-BPY-005/reports/RESULTADO.md` (matriz) | INCONCLUSIVE | Misma situación anterior; su sección final sí recoge el run Standard |

## Evidencia que decide

- `experimentos/EXP-BPY-004/evidencias/Captura de pantalla 2026-11-02 a la(s) 1.08.30 p.m..png`, SHA-256 `618f70d7d0ac9843a667a203a2c727153556a6c4d1f0618c43553506388a30be` (igual al del manifiesto). Se inspeccionó visualmente. Título de ventana `EXP-BPY-004-20261102T155417Z_slice_project`. Muestra:
  - preset `0.20mm Standard @Creality K1C 0.4 nozzle`;
  - K1C, `0.4-Standard`, Hyper PLA, `Smooth PEI Plate / Hig…`;
  - deslizador de capas 25 / 5.00 mm y 1 / 0.20 mm;
  - 30m36s, 14.45 g, 4.84 m;
  - patrón de ladrillos en Preview.
- `Metadata/project_settings.config` del 3MF custodiado (leído en INC-BPY-002): 220/50 °C, capa 0,20 mm, 2 paredes, grid 15 %, soportes desactivados, brim automático de 5 mm.
- Recálculo de SHA-256 (auditoría): los 7 artefactos del manifiesto de 004 coinciden.

## Veredicto (confirmado por el responsable, 2026-11-02)

1. **Run 155417Z: PASS digital.** Es la afirmación mejor respaldada. Debe leerse con estas limitaciones:
   - el conteo de 27 relieves es visual, no automatizado;
   - no hay G-code en el repositorio;
   - no se vio ni se registró la superficie física;
   - la advertencia `please apply glue before print` sigue abierta como decisión humana.
2. **Run 121521-0300: INCONCLUSIVE.** No cambia y se conserva.
3. **Experimento EXP-BPY-004: cerrado digitalmente por el run 155417Z.** Los demás runs quedan como historial.
4. Los tres documentos que siguen diciendo INCONCLUSIVE describen estados anteriores. No se editan; esta nota los reemplaza como referencia de estado vigente.
5. **Esto no cierra la Fase 1.** Sigue `PENDIENTE_VALIDACION_FISICA` hasta ejecutar EXP-BPY-005.

## Contradicción adicional

- `EXP-BPY-005/reports/RESULTADO.md` dice que seleccionar el preset Standard quedó `BLOCKED` y que "no se asumió el cambio".
- INC-BPY-002 muestra que el 3MF de la copia de trabajo se guardó a las 12:50:04 con configuración Standard.
- El archivo es evidencia objetiva de que el contenido cambió. Quién disparó el guardado no está establecido por ninguna fuente leída; no se afirma una causa.

## Deuda de manifiesto asociada

`EXP-BPY-005/MANIFIESTO_ARTEFACTOS.json` sigue registrando `EXP-BPY-004-20261102T154038Z_working_copy.3mf` con `659b0890…`. El archivo actual mide 23.873 B con `1a67df63…` (alterado). La corrección va como errata nueva (paso 7 del plan), no editando el manifiesto histórico.
