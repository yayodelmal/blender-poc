# Diagnóstico Geometry Nodes — multi-input `Mesh`

**Resultado: INCONCLUSIVE — detenido antes de construir candidatos.**  
**run_id:** `EXP-BPY-006-GN-MULTI-20261102T210408Z`

## Preflight

- Repositorio accesible: `/Users/yayo/Projects/blender-poc`, `main`, remoto `origin` presente.
- El registro sellado del diagnóstico anterior `EXP-BPY-006-GN-DIAG-20261102T190420Z` se verificó correctamente antes de iniciar.
- Blender coincide con ADR-0002: `/Applications/Blender.app/Contents/MacOS/Blender`, Blender 5.4.0 Alpha, build `745ab9a3e3c5`, SHA-256 `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`.
- El maestro EXP-BPY-003 midió el mismo hash que su manifiesto histórico, `09f7ee7c1ac207df00b1e8494e41b39a0c1eec4e048edbfcac61b71fd998495b`, antes de crear este ensayo.
- No se abrió ni escribió el maestro, no se cambiaron los diagnósticos anteriores, ni se instaló/actualizó Blender.

## Inspección de la API

La inspección se ejecutó en Blender background con perfil aislado, sin evaluar geometría ni guardar `.blend`. Encontró:

| Socket | Identificador | Tipo | Activo | Multi-input |
|---|---|---|---:|---:|
| `Mesh 1` (entrada 0) | `Mesh 1` | GEOMETRY | no | no |
| `Mesh` (entrada 1) | `Mesh 2` | GEOMETRY | sí | sí |
| `Self Intersection` | `Self Intersection` | BOOLEAN | no | no |
| `Hole Tolerant` | `Hole Tolerant` | BOOLEAN | no | no |
| `Mesh` (salida 0) | `Mesh` | GEOMETRY | sí | — |
| `Intersecting Edges` | `Intersecting Edges` | BOOLEAN | no | — |

Hay exactamente un socket multi-input GEOMETRY activo, `Mesh`, y una salida GEOMETRY activa, `Mesh`. Por tanto, la identificación del socket fue inequívoca.

La comprobación API también probó la enumeración del orden de enlaces. Al llamar `links.new(A)` y luego `links.new(B)`, Blender enumeró los enlaces como **B,A**; al llamar `links.new(B)` y luego `links.new(A)`, los enumeró como **A,B**. El enlace expone `multi_input_sort_id` (0 y 1). La inversión por orden de inserción no coincide con el orden solicitado. La inspección quedó clasificada como inconclusa y devolvió código 2 antes de cualquier construcción.

No se trató de ambigüedad del socket: fue incertidumbre del mecanismo de orden requerido para las dos variantes. Según la instrucción de detenerse y no corregir sobre la marcha, no se asignaron sort IDs, no se guardaron candidatos y no se ejecutaron validadores.

## Evidencia y procesos

La inspección se ejecutó con:

```text
python3 experimentos/EXP-BPY-006-GN-MULTI-20261102T210408Z/scripts/run_isolated.py api_inspection -- --background --factory-startup --disable-autoexec --python-exit-code 1 --python experimentos/EXP-BPY-006-GN-MULTI-20261102T210408Z/scripts/inspect_boolean_multi_api.py -- experimentos/EXP-BPY-006-GN-MULTI-20261102T210408Z/evidencias/api_socket_inventory.json
```

`logs/api_inspection.meta.json` registra versión, SHA de Blender, perfil aislado, inicio/fin UTC, duración y código de salida 2. El log completo es `logs/api_inspection.log`. Se sellaron mediante `herramientas/sellar_artefacto.py`:

| Evidencia | Tamaño | SHA-256 | Estado |
|---|---:|---|---|
| `evidencias/api_socket_inventory.json` | 1.889 B | `2bdc89eb40a640a8106da9287af447b7e496aca1d847e8093891240734b1a65b` | INCONCLUSIVE |
| `logs/api_inspection.log` | 4.522 B | `9174eae73d2d0aa7fa59e17a4eefe9c718c49bfc9dfeb4e6376a943b41bd07cb` | INCONCLUSIVE |

La verificación del registro nuevo devolvió `OK` para ambas evidencias.

## Comparación con pruebas anteriores

Las pruebas anteriores `EXP-BPY-006-GN-DIAG-20261102T190420Z` conectaron un cubo a `Mesh 1` (deshabilitado) y el otro a `Mesh` (multi-input habilitado); sus validadores midieron como salida solo el operando conectado a `Mesh`. Este ensayo nuevo confirmó que el multi-input activo existe y que `Mesh 1` está deshabilitado, pero **no evaluó si conectar ambos cubos a `Mesh` produce la unión**. Por eso la hipótesis no se confirma ni se descarta.

## Dictamen y siguiente paso

**Hipótesis: INCONCLUSA.** No hay medidas de una unión nueva. No se atribuye causa raíz ni se recomienda todavía Geometry Nodes para CU-01.

Una siguiente ejecución independiente podría fijar explícitamente `multi_input_sort_id` para obtener dos órdenes distintos, volver a comprobar el orden efectivo antes de guardar y luego validar las uniones en procesos separados. Ese procedimiento no se ejecutó en este `run_id`; cualquier repetición debe usar un directorio y `run_id` nuevos.

No se exportó STL, no se utilizó Creality Print y no se imprimió.
