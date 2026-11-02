# EXP-BPY-006 — Resultado de ejecución

**Estado global: INCONCLUSIVE — ejecución detenida por comportamiento no fiable de la unión en Geometry Nodes.**  
**run_id:** `EXP-BPY-006-20261102T175526Z`  
**Entorno:** Blender 5.4.0 Alpha, Python 3.13.13, macOS Apple Silicon, modo background, perfiles aislados por ejecución.  
**Alcance:** candidatos A, B y C; no se exportó STL ni se utilizó Creality Print.

## Decisión de parada

La evaluación de B no produjo de forma consistente un sólido con la base. La unión Geometry Nodes de dos sólidos superpuestos conservó solamente uno de sus operandos en una prueba aislada; al invertir las entradas conservó el otro. Una variante con un modificador Boolean externo tampoco añadió la base al patrón evaluado. Es una discrepancia observada en Blender 5.4.0 Alpha, no una atribución de causa raíz al producto.

Como el resultado de una operación geométrica central no es fiable en el entorno probado, se detuvo la fase antes de controles negativos adicionales y antes de modificar C. Se preservaron los candidatos y los logs parciales. No se promovió ninguna revisión.

## Integridad y punto de partida

| Elemento | SHA-256 | Tamaño | Estado |
|---|---|---:|---|
| Maestro EXP-BPY-003, antes | `09f7ee7c1ac207df00b1e8494e41b39a0c1eec4e048edbfcac61b71fd998495b` | 57.035 B | Verificado en registro |
| Snapshot EXP-BPY-006 | `09f7ee7c1ac207df00b1e8494e41b39a0c1eec4e048edbfcac61b71fd998495b` | 57.035 B | Copia idéntica, inspección de solo lectura PASS |
| Maestro EXP-BPY-003, después | `09f7ee7c1ac207df00b1e8494e41b39a0c1eec4e048edbfcac61b71fd998495b` | 57.035 B | Coincide con preflight |

La verificación final con `herramientas/sellar_artefacto.py verify` devolvió `OK` para el maestro, snapshot y los cuatro candidatos sellados. El maestro no se abrió en modo escritura ni se guardó.

## Resultados por estrategia

### A — Script paramétrico `bpy`

El primer candidato `A_bpy.blend` registró dimensiones correctas y 27 superficies superiores, pero tenía **28 componentes desconectados**: las cajas se habían concatenado sin unión. Se conservó como control fallido.

La revisión `A_bpy_v2.blend` fue generada con un script centralizado en parámetros y una unión booleana exacta de las cajas con la base. Un proceso Blender independiente abrió el archivo y validó:

- Dimensiones evaluadas: 79,999998 × 59,999999 × 5,000000 mm; desviación máxima < 0,000003 mm, dentro de ±0,01 mm.
- Base desde Z=0, espesor de base 4 mm y escala de objeto (1,1,1).
- 27 islas superiores de 15 × 7 mm.
- Una componente conectada, aristas manifold, orientación coherente, volumen positivo de 22.035,000311 mm³ y cero elementos degenerados.
- Parámetros guardados como metadatos y fuente generadora conservada.

**Resultado del candidato geométrico: PASS.** La estrategia vuelve a construir toda la geometría. No demuestra edición incremental del maestro ni que el metadato cambie la malla reactivamente; el cambio paramétrico se expresa en el script y genera una nueva malla/revisión.

### B — Geometry Nodes

Los sockets paramétricos sobrevivieron a guardar y reabrir. Sin embargo, este criterio no basta:

- `B_geometry_nodes.blend`: la evaluación tuvo dimensiones 79,800002 × 31,599998 × 1,199999 mm y 27 componentes separados; no incorporó la base ni produjo la envolvente contractual.
- `B_geometry_nodes_v2.blend`: el patrón GN y sus valores persistieron, pero el modificador Boolean externo no incorporó la base; el resultado medido siguió siendo 79,800002 × 31,599998 × 1,199999 mm y 9 componentes.
- La prueba aislada de la unión GN informó 15 × 7 × 1,2 mm con una componente al conectar base primero, y 80 × 60 × 4 mm con una componente al invertir los operandos. En ambos casos el resultado observado correspondió a un solo operando, no a la unión esperada.

**Resultado: FAIL para los candidatos construidos; estrategia general INCONCLUSIVE en Blender 5.4 Alpha.** Los valores persistentes y la geometría evaluada conectada al patrón están demostrados; la unión del patrón con la placa no. No se recomienda usar esta variante para CU-01 sin aislar la causa y repetirla.

### C — Edición *in-place*

El maestro contiene una malla ya fusionada, sin modificadores. Se verifican 27 islas de cara superior, una por relieve, pero el volumen de cada ladrillo no está conservado como objeto, colección ni grupo paramétrico independiente; la cara superior no identifica por sí sola la región completa que habría que transformar. Modificar solo esos vértices alteraría también las caras laterales compartidas y no acredita la reubicación íntegra del ladrillo ni la invariancia de la base.

**Resultado: INCONCLUSIVE / NOT RUN.** No se creó copia mutable de C ni se intentó reconstruirla para simular una edición incremental.

## Controles, errores y recuperación

- El control de fuente (snapshot binariamente idéntico y hash del maestro posterior) pasó.
- El candidato A inicial es un control geométrico fallido conservado; el validador detectó los 28 componentes.
- Los fallos de implementación de los primeros intentos B quedaron en `logs/build_B*.log`; las ejecuciones posteriores produjeron candidatos sellados y fallos geométricos observados.
- **NOT RUN:** controles de envolvente, base, desconexión intencional, pérdida de relieve, parámetro no autorizado, editabilidad tras reabrir, mutación del maestro y base obsoleta. Se detuvo la secuencia antes de inyectar defectos, por la condición de parada del experimento.
- **Restauración:** no se necesitó restaurar geometría; ninguna mutación tocó el maestro. No se probó restauración de candidato en esta etapa.
- No se ejecutaron exportaciones STL, Creality Print ni impresión.

## Artefactos principales

- Maestro: `experimentos/EXP-BPY-003/artifacts/EXP-BPY-003-20261102T144300Z_relief_plate_master.blend`
- Snapshot: `snapshots/EXP-BPY-006-20261102T175526Z_source_snapshot.blend`
- A fallido desconectado: `artifacts/EXP-BPY-006-20261102T175526Z_A_bpy.blend`
- A validado: `artifacts/EXP-BPY-006-20261102T175526Z_A_bpy_v2.blend`
- B fallido v1: `artifacts/EXP-BPY-006-20261102T175526Z_B_geometry_nodes.blend`
- B fallido v2: `artifacts/EXP-BPY-006-20261102T175526Z_B_geometry_nodes_v2.blend`
- Registro de hashes: `registro_artefactos.jsonl`
- Validador independiente: `scripts/validate_candidate.py`
- Generador: `scripts/build_candidates.py`
- Bitácoras de procesos: `logs/`

El registro existente selló estos candidatos:

| ID en registro | Tamaño | SHA-256 | Validación registrada |
|---|---:|---|---|
| `A_bpy_failed_disconnected` | 55.495 B | `99e2324663b5b143103bc027cb4694af4ae0dd1f1c873608d9d23af90c1356ff` | FAIL |
| `A_bpy_rebuild_pass` | 56.883 B | `d01c9f2c87e37e5e69b51a1f7b8704f78480243b8a12c15b9ae8e0da07b05239` | PASS geométrico |
| `B_gn_failed_v1` | 58.377 B | `15a8bcef57c85e200150412c4b9f50857efc7b4a6af125ddf270688c777ade1e` | FAIL |
| `B_gn_failed_v2` | 57.571 B | `31e6c3f1c0aeda797bb9767a5b7cfe07e47795c2b62dd03648a7294d07913dc8` | FAIL |

**Límite de trazabilidad:** los metadatos sellados incluyen el SHA-256 del archivo `build_candidates.py` existente al sellar los candidatos. El script cambió en la sección B después de generar A v2; el procedimiento no registró el hash del script exactamente al momento de la generación. El código de A se mantuvo igual por inspección de esta sesión, pero no existe sello contemporáneo del script ejecutado. El registro no se reescribió; este límite se conserva aquí.

## Conclusión

EXP-BPY-006 **no cumple el criterio global de PASS**: A proporciona una malla correcta reproducible, pero reconstruye la pieza; B no logró una placa conectada en el entorno experimental; C no se ejecutó porque la identificación inequívoca de las regiones volumétricas no está demostrada. La recomendación provisional es conservar A como ruta de generación de revisiones nuevas, sin confundirla con edición incremental. Antes de CU-01, hace falta una repetición acotada de Geometry Nodes en una versión estable de Blender o un prototipo GN cuya salida se valide primero con una unión simple; para C se requeriría una representación fuente que conserve explícitamente cada volumen de ladrillo.
