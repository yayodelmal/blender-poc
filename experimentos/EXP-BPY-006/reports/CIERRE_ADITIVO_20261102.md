# EXP-BPY-006 — Cierre aditivo de estrategias

**Estado global de EXP-BPY-006: INCONCLUSIVE.** Este cierre consolida resultados ya registrados; no reemplaza ni modifica `RESULTADO.md`, `MATRIZ_COMPARATIVA.md`, experimentos, artefactos ni decisiones históricas.

## Matriz comparativa consolidada

| Estrategia | Resultado observado | Qué demuestra | Limitaciones y entorno |
|---|---|---|---|
| **A — `bpy`** | **PASS geométrico** para el candidato A de parámetros contractuales; el canario separado también pasó | A v2 cumple 80 × 60 × 5 mm, base de 4 mm, 27 ladrillos de 15 × 7 mm, una componente cerrada/manifold y volumen positivo. El canario 14,8 × 7 mm con paso X 16 mm produjo 27 relieves con las dimensiones cambiadas y mantuvo la envolvente, base y juntas. | A regenera la geometría completa desde parámetros del script; no es edición incremental ni parametrización reactiva dentro del `.blend`. Validado en Blender 5.4.0 Alpha, no en versión estable. El canario no cambia el contrato de 15 × 7 mm. |
| **B — Geometry Nodes** | **FAIL** en la única variante A→B cuya geometría multi-input se midió | La salida tuvo envolvente aproximada de 19,8 × 10 × 10 mm y una componente, pero volumen de ≈2.000 mm³ frente a 1.980 mm³ y `all_edges_manifold=false`. | La variante B→A no se construyó porque la validación de A→B activó la condición de parada. No se determina el efecto de invertir el orden y no se atribuye causa raíz. |
| **C — in-place** | **INCONCLUSIVE / NOT RUN** | La inspección del maestro identifica islas de caras superiores correspondientes a los relieves. | La malla fusionada no conserva regiones volumétricas inequívocas por ladrillo. No se ejecutó una edición incremental ni se reconstruyó el modelo para simularla. |

## Entorno Blender y alcance de la evidencia

La evidencia del proyecto registra tres fallos de arranque background con **Blender 5.2.3 LTS** en Apple Silicon, con código 139 y fallo asociado a Metal. El intento con `--gpu-backend opengl` fue rechazado por esa build, que declaraba admitir solo Metal. Las fuentes incluyen `experimentos/EXP-BPY-001/reports/RESULTADO.md`, los metadatos `experimentos/EXP-BPY-001/logs/background_probe_*.meta` y los logs de probe/crash.

No se verificó otra versión estable disponible que arranque en background. Por tanto, **Blender 5.4.0 Alpha es el único entorno background disponible y probado en este registro**. La build fijada por ADR-0002 es Blender 5.4.0 Alpha, build `745ab9a3e3c5`, Python 3.13.13, ejecutable `/Applications/Blender.app/Contents/MacOS/Blender`, SHA-256 `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`. Los resultados PASS en esta Alpha no constituyen validación de una versión estable.

## Registros de integridad consultados

Se ejecutó `python3 herramientas/sellar_artefacto.py verify --registro <ruta>` en modo de solo lectura. Todas las entradas de cada registro indicado devolvieron `OK`; no se alteraron registros, sellos ni artefactos.

| Registro | Resultado de verificación |
|---|---|
| `experimentos/EXP-BPY-006/registro_artefactos.jsonl` | 6 entradas OK: maestro/snapshot y candidatos A/B |
| `experimentos/EXP-BPY-006-A-CANARY-20261102T212457Z/registro_artefactos.jsonl` | 14 entradas OK: referencias, copia del generador, scripts, candidato, evidencia, logs y reporte |
| `experimentos/EXP-BPY-006-GN-DIAG-20261102T183743Z/registro_artefactos.jsonl` | 4 entradas OK |
| `experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/registro_artefactos.jsonl` | 4 entradas OK |
| `experimentos/EXP-BPY-006-GN-MULTI-20261102T210408Z/registro_artefactos.jsonl` | 2 entradas OK |
| `experimentos/EXP-BPY-006-GN-SORTID-20261102T211127Z/registro_artefactos.jsonl` | 2 entradas OK |
| `experimentos/EXP-BPY-006-GN-MULTIORDER-20261102T211540Z/registro_artefactos.jsonl` | 6 entradas OK |

## Artefactos y evidencias principales

### A — candidato contractual y canario

- Candidato A geométrico validado: `experimentos/EXP-BPY-006/artifacts/EXP-BPY-006-20261102T175526Z_A_bpy_v2.blend`.
- Generador fuente A/B: `experimentos/EXP-BPY-006/scripts/build_candidates.py`.
- Validación independiente de A: `experimentos/EXP-BPY-006/logs/validate_A_v2.log` y `experimentos/EXP-BPY-006/registro_artefactos.jsonl` (`A_bpy_rebuild_pass`).
- Informe del canario: `experimentos/EXP-BPY-006-A-CANARY-20261102T212457Z/reports/RESULTADO.md`.
- Candidato canario: `experimentos/EXP-BPY-006-A-CANARY-20261102T212457Z/artifacts/EXP-BPY-006-A-CANARY-20261102T212457Z_A_canary.blend`.
- Medición independiente del canario: `experimentos/EXP-BPY-006-A-CANARY-20261102T212457Z/evidencias/validation_canary.json`.
- Copia diagnóstica del generador: `experimentos/EXP-BPY-006-A-CANARY-20261102T212457Z/scripts/build_A_canary.py`; no se modificó el generador histórico.

### B — Geometry Nodes

- Comparativa de EXP-BPY-006: `experimentos/EXP-BPY-006/reports/MATRIZ_COMPARATIVA.md` y `experimentos/EXP-BPY-006/reports/RESULTADO.md`.
- Variante medida A→B: `experimentos/EXP-BPY-006-GN-MULTIORDER-20261102T211540Z/artifacts/union_A_before_B.blend`.
- Evidencia de medición: `experimentos/EXP-BPY-006-GN-MULTIORDER-20261102T211540Z/evidencias/validation_A_BEFORE_B.json`.
- Resultado y condición de parada: `experimentos/EXP-BPY-006-GN-MULTIORDER-20261102T211540Z/reports/RESULTADO.md`. Allí se documenta que B→A quedó sin ejecutar.
- Antecedentes de sockets y orden: `experimentos/EXP-BPY-006-GN-DIAG-20261102T183743Z/reports/RESULTADO.md`, `experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/reports/RESULTADO.md`, `experimentos/EXP-BPY-006-GN-MULTI-20261102T210408Z/reports/RESULTADO.md` y `experimentos/EXP-BPY-006-GN-SORTID-20261102T211127Z/reports/RESULTADO.md`.

### C — in-place y versión

- Inspección del maestro y topología: `experimentos/EXP-BPY-006/scripts/inspect_base.py` y `experimentos/EXP-BPY-006/reports/RESULTADO.md`.
- Decisión y pin de versión: `docs/05_decisiones/ADR-0002_politica_blender_alpha.md`.
- Evidencia del intento Blender 5.2.3 LTS: `experimentos/EXP-BPY-001/reports/RESULTADO.md`, `experimentos/EXP-BPY-001/logs/background_probe_20261102T104904.meta`, `experimentos/EXP-BPY-001/logs/background_probe_20261102T105207-0300.meta` y los logs/crash referenciados desde ese informe.

## Discrepancia documental observada

ADR-0002 presenta una inconsistencia interna: su encabezado indica **“Estado: ACEPTADA — opción C”**, pero en el contexto dice que EXP-BPY-001 dejó pendiente decidir si se acepta la Alpha y que no hay registro de esa decisión. Este cierre no interpreta ni corrige la discrepancia; el responsable debe resolverla en una actualización documental posterior si corresponde.

También queda una limitación de trazabilidad señalada en el informe histórico de EXP-BPY-006: el hash exacto de `build_candidates.py` no se selló en el instante en que se generó A v2. El mismo informe registra que el código de la sección A se mantuvo igual por inspección; el artefacto A sí está sellado y su validación pasa. El canario aporta una copia de fuente con hash y cambios delimitados, pero no convierte esa evidencia histórica en una captura contemporánea del generador original.

## Recomendación

**A — `bpy` es la estrategia provisional mejor respaldada para generar revisiones completas e inmutables:** los parámetros centralizados producen una malla nueva que pudo validarse en un proceso independiente; el canario confirma que los parámetros ensayados repercuten en las dimensiones de la geometría. Hay que describirla como regeneración completa, no como edición incremental.

Usar A para CU-01 requeriría una **decisión explícita del responsable** de aceptar la limitación de ejecutar Blender 5.4.0 Alpha mientras no se verifique una versión estable apta para background. Este informe no constituye esa aprobación. No inicia CU-01 ni promueve el canario al contrato.

## Estado de este cierre

Este documento es aditivo y resume evidencia existente. No se modificaron el maestro, los experimentos anteriores, ADR-0002, informes ni matrices históricas. No se generó geometría, STL, laminado ni impresión.
