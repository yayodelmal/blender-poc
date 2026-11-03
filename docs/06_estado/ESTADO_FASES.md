# Estado de las fases

**Fecha:** 2026-11-02. **Fuente canónica del estado vigente.** `CIERRE_FASE_1_copia_2026-11-02.md` (misma carpeta) es el informe anterior, con EXP-BPY-004 desactualizado; se conserva como histórico. Reconciliación en [RECONCILIACION_EXP-BPY-004](RECONCILIACION_EXP-BPY-004.md).

## Fase 1 — **CERRADA POR DECISIÓN DEL RESPONSABLE, CON EXCEPCIÓN DIMENSIONAL DOCUMENTADA**

**Esto no significa que se cumpliera el criterio de cierre.** `CIERRE_FASE_1` §9 y el protocolo de EXP-BPY-005 exigen impresión, fotos y medidas reales; las medidas no se tomaron por decisión del responsable (verificación dimensional física: `NOT RUN — omitida por decisión del usuario`). El veredicto técnico se conserva y la autorización para continuar se registra por separado: [ADR-0003](../05_decisiones/ADR-0003_cierre_fase1_con_excepcion_dimensional.md). Estado anterior: `PENDIENTE_VALIDACION_FISICA`.

| Experimento | Estado vigente | Detalle |
|---|---|---|
| EXP-BPY-001 | PASS | Línea base `a5f0aa70…`, aprobada tras INC-BPY-001 |
| EXP-BPY-002 | PASS | Con salvedades (conflicto simulado, sin tiempos de pared) |
| EXP-BPY-003 | PASS | Proxy 80×60×5 mm, STL `c6342d68…` |
| EXP-BPY-004 | PASS (digital) | Run `155417Z`; el run `121521-0300` queda INCONCLUSIVE como histórico |
| EXP-BPY-005 | **Impresión completada · inspección visual favorable · medición dimensional NOT RUN (omitida por decisión del usuario) · aceptado por el usuario para el alcance exploratorio** | **No es PASS.** Cuatro hechos separados en `experimentos/EXP-BPY-005/EXCEPCION_DIMENSIONAL_EXP-BPY-005-20261102T173135Z.md`. Respaldo: declaración, 3 fotos selladas y `EVALUACION_CALIDAD_PARCIAL_…md` |

Entorno de todos los PASS: Blender 5.4.0 Alpha (ver ADR-0002), Creality Print 7.3.0.6157, macOS Apple Silicon.

## Incidentes

| Incidente | Estado | Abierto |
|---|---|---|
| INC-BPY-001 | Cerrado (dictamen B) | Prevención por sellado automático: herramienta implementada (`herramientas/sellar_artefacto.py`) y usada en EXP-BPY-005 |
| INC-BPY-002 | Contenido preservado, sin restaurar | Manifiesto de EXP-BPY-005 con hash desfasado (ver [ERRATAS](ERRATAS.md)) |

## Decisiones

| Decisión | Estado |
|---|---|
| Ejecución directa con bpy ([ADR-0001](../05_decisiones/ADR-0001_bpy_directo.md)) | Aceptada; el motivo y la aceptación del riesgo de MCP quedan por documentar |
| Política de la Alpha ([ADR-0002](../05_decisiones/ADR-0002_politica_blender_alpha.md)) | Aceptada: opción C |
| Reconciliación de EXP-BPY-004 | Confirmada |
| Cierre de Fase 1 con excepción dimensional ([ADR-0003](../05_decisiones/ADR-0003_cierre_fase1_con_excepcion_dimensional.md)) | Aceptada; el criterio dimensional físico sigue sin verificar |

## Pendientes del responsable

1. EXP-BPY-005: ficha de laminado aprobada; adhesivo declarado (pegamento en barra, resultado bueno). Siguen sin registrar: cara de la PEI montada, hora de inicio/fin, archivo abierto en el laminador, estado de la boquilla. Ver `experimentos/EXP-BPY-005/APROBACIONES_…md` y `DECLARACION_IMPRESION_…md`.
2. Para CU-01: espesor de pared (2 o 20 mm), base, drenaje, si los 150 mm incluyen el relieve.
3. Motivo documentado del pivote a bpy y aceptación del riesgo de MCP (ADR-0001).

## CU-01 — revisiones digitales (macetero 150 × 150 × 60 mm)

Solo modelo digital en Blender 5.4.0 Alpha. **Ninguna revisión se ha exportado a STL ni impreso**; la medición física sigue siendo exigible.

| Revisión | Cambio | Resultado | Carpeta |
|---|---|---|---|
| REV-001 | Pared 20 mm, base 4 mm, sin drenaje (3 intentos; los 2 primeros fallaron) | PASS digital | `experimentos/CU-01/REV-001-20261102T220906Z` |
| REV-002 | Pared 10 mm | PASS digital | `experimentos/CU-01/REV-002-20261103T023400Z` |
| REV-003 (pared 5 mm) | Pared 5 mm; acabado Hyper PLA Marmol por defecto | PASS digital; cavidad 138 × 138 × 56 mm medida en un run complementario | `experimentos/CU-01/REV-003-20261103T033342Z` y `…/REV-003-CAVIDAD-20261103T033612Z` |
| REV-003-SHT31 | Copia de REV-002 (pared 10 mm) con soporte removible para placa SHT31, como objeto aparte (trabajo de otro agente) | PASS digital según su informe; sus 16 artefactos sellados verifican OK. Sin STL ni impresión | `experimentos/CU-01/REV-003-SHT31-20261103T032047Z` |

Variantes visuales de REV-002 (no cambian la geometría): blanco mate y PLA marmoleado, en `experimentos/CU-01/CU-01-COLOR-*`. Pendiente del responsable: elegir la revisión, drenaje y la medición física.

## Fase 2 y siguientes

No cerrada. CON-001 y VAL-001 son borradores sin aprobar. No se ha iniciado CU-01. **La excepción dimensional no se hereda a CU-01**: allí V10 (medición física) vuelve a ser exigible.

## Criterios que permanecen sin verificar

- Dimensiones físicas frente a ±0,5 mm por eje (X 80, Y 60, Z 5 mm; base 4 mm).
- Exactitud dimensional de la K1C con este perfil; repetibilidad (una sola impresión).
- Adhesión entre capas, resistencia y deformación cuantificada.
- Tiempos reales y datos operativos de la impresión (`NO MEDIDO`).
- Estabilidad de Blender: todo el trabajo digital usa una build Alpha (ADR-0002).

## Próximo experimento

**EXP-BPY-006 (propuesto): modificación paramétrica del patrón de ladrillos conservando dimensiones e invariantes (R06).** Debe cambiar el tamaño o la distribución de los ladrillos sin reconstruir ni alterar la envolvente (80×60×5 mm), la base de 4 mm ni la conectividad, y comparar tres estrategias: script paramétrico, Geometry Nodes y edición in-place. Controles negativos: dimensión alterada, ladrillo desconectado, conteo erróneo. Validar en proceso separado y sellar con `herramientas/sellar_artefacto.py`. Sin STL nuevo ni impresión hasta que pase. CU-01 solo tras decidir pared, base y drenaje.

Si el responsable toma las medidas más adelante, se registran como adenda en `MEDICIONES_FISICAS.md`/nuevo archivo, sin reescribir lo anterior.
