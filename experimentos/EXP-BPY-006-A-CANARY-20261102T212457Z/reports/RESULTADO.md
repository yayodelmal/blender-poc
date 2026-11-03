# EXP-BPY-006-A-CANARY — Respuesta del generador A a parámetros

**Resultado: PASS — el generador A reconstruye el relieve a partir de los parámetros canario y conserva las invariantes geométricas verificadas.**  
**Run ID:** `EXP-BPY-006-A-CANARY-20261102T212457Z`  
**Alcance:** diagnóstico aislado; no es una revisión contractual ni una aprobación para CU-01.

## Preflight e integridad

- Repositorio: `/Users/yayo/Projects/blender-poc`, rama `main`; directorio nuevo creado para esta ejecución.
- Registro histórico EXP-BPY-006 verificado con `herramientas/sellar_artefacto.py verify`: seis registros `OK`.
- Blender: `/Applications/Blender.app/Contents/MacOS/Blender`, Blender 5.4.0 Alpha, build `745ab9a3e3c5`, SHA-256 `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`; coincide con ADR-0002.
- Maestro EXP-BPY-003: SHA-256 antes y después `09f7ee7c1ac207df00b1e8494e41b39a0c1eec4e048edbfcac61b71fd998495b`.
- Candidato A de referencia: `A_bpy_v2.blend`, SHA-256 antes y después `d01c9f2c87e37e5e69b51a1f7b8704f78480243b8a12c15b9ae8e0da07b05239`; su registro histórico lo clasifica como PASS geométrico.
- Generador original SHA-256: `3c5b9068cc6d549418008dca6f6d3a0d5442d2dc8ab78cb3626710fe6626bf1a`. La copia diagnóstica tiene SHA-256 `119aecafd65cfe7dabda7b0cc6df631c89c7baae234ab95f479c0f4ab27369b0`. La comparación de archivos mostró solo el cambio de `RUN`, `brick_x_mm` y `pitch_x_mm`.

El preflight detallado se conserva en [`preflight.json`](../evidencias/preflight.json). Los hashes y metadatos de cada artefacto están en `registro_artefactos.jsonl`.

## Parámetros canario

| Parámetro | A de referencia | Canario | Resultado |
|---|---:|---:|---|
| Ladrillo X | 15 mm | 14,8 mm | Cambiado deliberadamente |
| Ladrillo Y | 7 mm | 7 mm | Invariante |
| Junta | 1,2 mm | 1,2 mm | Invariante |
| Paso X | 16,2 mm | 16,0 mm | Cambiado deliberadamente |
| Paso Y | 8,2 mm | 8,2 mm | Invariante |
| Filas / distribución | 6 / 5-4 alternadas | 6 / 5-4 alternadas | Invariante; 27 relieves |
| Base / relieve | 80 × 60 × 4 / 1 mm | Igual | Invariante |

La geometría evaluada demuestra el cambio respecto de la referencia: los 27 relieves miden aproximadamente 14,8 × 7 mm frente a los 15 × 7 mm registrados para A. La reducción de ancho de 0,2 mm y del paso X de 0,2 mm conserva la junta X en 1,2 mm.

## Ejecución reproducible

Se usaron dos procesos Blender separados. Cada proceso tuvo `HOME`, configuración, scripts de usuario, datafiles, extensiones y temporales bajo `profiles/<label>/`; no se usó un perfil global.

- Construcción: `python3 experimentos/EXP-BPY-006-A-CANARY-20261102T212457Z/scripts/run_isolated.py build build_canary /Users/yayo/Projects/blender-poc/experimentos/EXP-BPY-006-A-CANARY-20261102T212457Z/artifacts/EXP-BPY-006-A-CANARY-20261102T212457Z_A_canary.blend`
- Validación independiente, de solo lectura: `python3 experimentos/EXP-BPY-006-A-CANARY-20261102T212457Z/scripts/run_isolated.py validate validate_canary /Users/yayo/Projects/blender-poc/experimentos/EXP-BPY-006-A-CANARY-20261102T212457Z/artifacts/EXP-BPY-006-A-CANARY-20261102T212457Z_A_canary.blend /Users/yayo/Projects/blender-poc/experimentos/EXP-BPY-006-A-CANARY-20261102T212457Z/evidencias/validation_canary.json`

Los comandos exactos invocados por Blender, la versión y su hash, rutas de perfiles, inicio/fin UTC, duración, código de salida y log se registran en `logs/build_canary.meta.json` y `logs/validate_canary.meta.json`. Ambos procesos tuvieron código de salida 0. Los logs contienen el aviso `ArchWarn: ARCH_CACHE_LINE_SIZE != Arch_ObtainCacheLineSize()` de la build Alpha; no impidió construcción ni validación.

## Mediciones independientes

El validador abrió el `.blend` en un proceso nuevo, evaluó la malla con sus modificadores, escribió únicamente el JSON de evidencia y no guardó el archivo Blender.

| Verificación | Esperado | Observado | Estado |
|---|---|---|---|
| Envolvente evaluada | 80 × 60 × 5 mm | 79,999998 × 59,999999 × 5,000000 mm | PASS, ±0,01 mm |
| Base | 80 × 60 × 4 mm | 79,999998 × 59,999999 × 4,000000 mm | PASS |
| Relieves superiores | 27 de 14,8 × 7 mm | 27; X 14,799999–14,800001 mm, Y 6,999999–7,000000 mm | PASS |
| Juntas X | 1,2 mm | 1,1999998–1,2000008 mm | PASS |
| Juntas Y | 1,2 mm | 1,1999998–1,2000017 mm | PASS |
| Distribución | seis filas, 5/4 alternadas | `[5, 4, 5, 4, 5, 4]` | PASS |
| Componente / manifold | 1 / cerrado | 1 / todas las aristas manifold y contiguas | PASS |
| Volumen | 21.997,2 mm³ | 21.997,200293 mm³ | PASS |
| Elementos degenerados | 0 | 0 aristas, 0 caras | PASS |
| Parámetros persistidos | canario autorizado | coinciden exactamente con el diccionario canario | PASS |

Volumen esperado recalculado para esta variante: `80 × 60 × 4 + 27 × 14,8 × 7 × 1 = 21.997,2 mm³`. El validador usó una tolerancia numérica de 0,01 mm³ para esta comprobación; la desviación observada fue aproximadamente 0,000293 mm³.

## Dictamen y límites

El resultado confirma que **el generador A responde a estos cambios de parámetros**: el ancho de los ladrillos cambió en la geometría evaluada, el paso X cambió en los datos persistidos y la separación X permaneció en 1,2 mm. Las invariantes de envolvente, base, cantidad de relieves, separación Y y topología también pasaron.

Esta prueba demuestra una **regeneración completa reproducible**, no edición incremental del `.blend` existente ni parametrización reactiva dentro del archivo. La variante canario no cambia el contrato aprobado de 15 × 7 mm, no se promueve y no autoriza CU-01.

No se exportó STL, no se abrió Creality Print y no se imprimió. No se modificaron el maestro ni los artefactos históricos.
