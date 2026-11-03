# Diagnóstico Geometry Nodes — unión mínima

**Resultado global: FAIL.** Las dos variantes se abrieron en procesos independientes y el validador resolvió la salida geométrica antes de medir. Cada entrada individual pasó, pero la salida UNION fue solamente uno de los cubos; ambas variantes incumplieron dimensiones y volumen esperados. No se hicieron correcciones ni reintentos.

## Ejecución

- `run_id`: `EXP-BPY-006-GN-DIAG-20261102T190420Z`
- Blender: 5.4.0 Alpha, build `745ab9a3e3c5`, branch `main`.
- Ejecutable: `/Applications/Blender.app/Contents/MacOS/Blender`
- SHA-256: `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`
- Python: 3.13.13.
- Repositorio: `/Users/yayo/Projects/blender-poc`, rama `main`; el árbol ya contenía el diagnóstico anterior como untracked y este ensayo se creó en un directorio distinto.
- La documentación de EXP-BPY-001 registra Blender 5.2.3 LTS con tres fallos de arranque background, código 139, durante inicialización de Metal. Por autorización del usuario, se usó la Alpha instalada; no se instaló ni actualizó Blender.
- Todos los procesos usaron `--background --factory-startup --disable-autoexec --python-exit-code 1`, `HOME`, config, scripts, data y temporales propios bajo `profiles/<label>/`.

## Inspección de API previa

La inspección se ejecutó antes de generar los candidatos. `evidencias/api_socket_inventory.json` y `logs/api_inspection.log` registran la API de `GeometryNodeMeshBoolean` para `UNION`:

| Tipo | Índice | Nombre | Identificador | Tipo socket | Multi-input | Enabled |
|---|---:|---|---|---|---|---|
| Entrada | 0 | Mesh 1 | Mesh 1 | GEOMETRY | no | no |
| Entrada | 1 | Mesh | Mesh 2 | GEOMETRY | sí | sí |
| Entrada | 2 | Self Intersection | Self Intersection | BOOLEAN | no | no |
| Entrada | 3 | Hole Tolerant | Hole Tolerant | BOOLEAN | no | no |
| Salida | 0 | Mesh | Mesh | GEOMETRY | — | sí |
| Salida | 1 | Intersecting Edges | Intersecting Edges | BOOLEAN | — | no |

Se detectó exactamente una salida habilitada de tipo `GEOMETRY`; se resolvió como `Mesh` (identificador `Mesh`). Ambos validadores comprobaron que la salida en el archivo abierto coincidía con el inventario y que la cantidad de candidatas era uno **antes de evaluar cualquier geometría**. La resolución pasó en las dos variantes.

## Procedimiento y comandos

Cada generación y validación se ejecutó como un proceso Blender distinto. Los comandos completos, la versión, el hash del ejecutable, los perfiles aislados, las marcas de tiempo, duración, código de salida y rutas de log están en los `logs/*.meta.json` y `logs/*.log`.

Generación (se ejecutó una vez por variante):

```text
python3 experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/scripts/run_isolated.py build_A_FIRST -- --background --factory-startup --disable-autoexec --python-exit-code 1 --python experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/scripts/build_union_variant.py -- A_FIRST experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/artifacts/union_Afirst.blend
python3 experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/scripts/run_isolated.py build_B_FIRST -- --background --factory-startup --disable-autoexec --python-exit-code 1 --python experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/scripts/build_union_variant.py -- B_FIRST experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/artifacts/union_Bfirst.blend
```

Validación independiente (un proceso distinto por `.blend`, solo lectura; el validador no invocó ningún operador de guardado):

```text
python3 experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/scripts/run_isolated.py validate_A_FIRST -- --background --factory-startup --disable-autoexec --python-exit-code 1 --python experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/scripts/validate_union_variant.py -- experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/artifacts/union_Afirst.blend experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/evidencias/validation_A_FIRST.json
python3 experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/scripts/run_isolated.py validate_B_FIRST -- --background --factory-startup --disable-autoexec --python-exit-code 1 --python experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/scripts/validate_union_variant.py -- experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/artifacts/union_Bfirst.blend experimentos/EXP-BPY-006-GN-DIAG-20261102T190420Z/evidencias/validation_B_FIRST.json
```

## Resultados medidos

Entradas individuales esperadas: A mide 10 × 10 × 10 mm, centro (5,5,5) mm; B mide 10 × 10 × 10 mm, centro (14,8,5,5) mm. Volumen esperado por cubo: 1.000 mm³.

| Medición | A_FIRST: A→Mesh 1, B→Mesh | B_FIRST: B→Mesh 1, A→Mesh | Contrato de unión |
|---|---:|---:|---:|
| Input A | 9,9999998 × 9,9999998 × 9,9999998 mm; 999,999933 mm³; 1 componente manifold | Igual; PASS | 10 × 10 × 10 mm; 1.000 mm³ |
| Input B | 9,9999998 × 9,9999998 × 9,9999998 mm; 999,999933 mm³; 1 componente manifold | Igual; PASS | 10 × 10 × 10 mm; 1.000 mm³ |
| Salida UNION | 9,9999998 × 9,9999998 × 9,9999998 mm; 999,999933 mm³; centro X=14,8000000 mm | 9,9999998 × 9,9999998 × 9,9999998 mm; 999,999933 mm³; centro X=5,0000000 mm | 19,8 × 10 × 10 mm; 1.980 mm³ |
| Componentes, manifold, degenerados de salida | 1; manifold; 0 aristas y 0 caras degeneradas | 1; manifold; 0 aristas y 0 caras degeneradas | 1 componente, cerrado/manifold, cero degenerados |
| Resultado | **FAIL**: salida equivale al input B | **FAIL**: salida equivale al input A | No se obtuvo la unión |

El volumen contractual de 1.980 mm³ corresponde a `1000 + 1000 - (0,2 × 10 × 10)`. La salida fue un cubo válido, pero no la unión de los cubos solapados.

## Comparación con las ejecuciones Alpha anteriores

Los logs previos de `experimentos/EXP-BPY-006/logs/probe_gn_boolean.log` y `probe_gn_boolean_reverse.log` registraron que, al invertir el orden, la salida cambiaba entre los operandos (15 × 7 × 1,2 mm y 80 × 60 × 4 mm, respectivamente). En este diagnóstico mínimo se repitió ese patrón con cubos iguales: la salida correspondió a lo conectado a `Mesh`, no a una unión; invertir las conexiones cambió la posición del único cubo resultante.

El inventario también muestra que `Mesh 1` está deshabilitado para esta operación y `Mesh` es una entrada multi-input habilitada. Es una observación de la interfaz API que coincide con los resultados. **No se afirma que sea causa raíz** ni se ensayó una conexión alternativa, pues el alcance quedó limitado a las dos permutaciones solicitadas y debía detenerse ante un resultado inesperado.

## Integridad y artefactos sellados

Los cuatro artefactos solicitados se sellaron mediante `herramientas/sellar_artefacto.py`; la verificación final devolvió `OK` para todos:

| Artefacto | Tamaño | SHA-256 | Validación |
|---|---:|---|---|
| `artifacts/union_Afirst.blend` | 60.751 B | `3be43143b890c41c5cf20f075ff70168fd2e123d48481f0258bfc37d7ec6bfdc` | FAIL |
| `artifacts/union_Bfirst.blend` | 60.749 B | `4115bca7bbe5ac8b390af81724c704da4febadbb32282d18a85154089c849b76` | FAIL |
| `evidencias/validation_A_FIRST.json` | 5.087 B | `c05605248e9208499a2c24f753867ee67228cf73aaf314f88ef8f9110f1c385f` | FAIL |
| `evidencias/validation_B_FIRST.json` | 5.085 B | `ba3dd021b1cf4a7d2cab10203d23bf86fa2873912ee39082c6ccf82889400a85` | FAIL |

El maestro EXP-BPY-003 no se abrió ni escribió. Su hash comprobado al cierre coincide con el manifiesto histórico: `09f7ee7c1ac207df00b1e8494e41b39a0c1eec4e048edbfcac61b71fd998495b`. No se modificó el diagnóstico anterior ni documentación histórica.

## Conclusión y siguiente paso

El comportamiento inesperado se reprodujo: la salida de `UNION` conserva el operando conectado a `Mesh` y cambia cuando se invierte el orden. El experimento mínimo queda **FAIL** para la operación de unión esperada. Geometry Nodes no queda validado para sólidos conectados ni para CU-01.

Se detuvo después de registrar y sellar resultados. No se corrigieron scripts ni se repitió dentro de este `run_id`. El siguiente paso debería ser una investigación separada de la semántica documentada de las entradas para `UNION` en esta versión y, solo bajo un nuevo `run_id`, probar el modo de conexión que admita el API si el responsable lo autoriza. No se exportó STL, no se usó Creality Print y no se imprimió.
