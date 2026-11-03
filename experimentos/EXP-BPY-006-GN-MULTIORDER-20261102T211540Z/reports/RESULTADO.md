# Diagnóstico Geometry Nodes — multi-input por orden de enlace

**Resultado global: FAIL — la primera variante no cumplió el contrato geométrico y se detuvo antes de construir B_BEFORE_A.**  
**run_id:** `EXP-BPY-006-GN-MULTIORDER-20261102T211540Z`.

## Preflight e integridad

- Repositorio accesible: `/Users/yayo/Projects/blender-poc`, rama `main`, remoto `origin`.
- Los registros de `EXP-BPY-006-GN-SORTID-20261102T211127Z` y `EXP-BPY-006-GN-MULTI-20261102T210408Z` verificaron `OK` antes de empezar.
- Blender: `/Applications/Blender.app/Contents/MacOS/Blender`, 5.4.0 Alpha, build `745ab9a3e3c5`, SHA-256 `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`, igual a ADR-0002.
- Maestro EXP-BPY-003 antes del ensayo: SHA-256 `09f7ee7c1ac207df00b1e8494e41b39a0c1eec4e048edbfcac61b71fd998495b`, coincidente con su manifiesto.
- Perfiles `HOME`, Blender config/scripts/data y temporales aislados por proceso. Versiones, SHA, comandos exactos, tiempos UTC, duración y códigos de salida están en `logs/*.meta.json` y `logs/*.log`.

## API y orden efectivo

Para `UNION`, la API reportó un único socket GEOMETRY multi-input habilitado, `Mesh` (índice 1, identificador `Mesh 2`); `Mesh 1` estaba deshabilitado; la única salida GEOMETRY habilitada se llamaba `Mesh`.

El preflight comprobó, sin asignar `multi_input_sort_id`, que:

| Secuencia al crear enlaces | Orden efectivo enumerado |
|---|---|
| A y luego B | B, A |
| B y luego A | A, B |

El generador usó la secuencia B y luego A para exigir y confirmar el orden efectivo **A,B** antes de guardar `union_A_before_B.blend`. No conectó nada a `Mesh 1`. El validador independiente abrió el archivo, resolvió los sockets y volvió a confirmar el orden A,B antes de evaluar geometría.

## Geometría medida

Los dos cubos de entrada estaban cerrados y fueron medidos por separado en el proceso validador:

| Entrada | Dimensiones observadas | Centro (mm) | Volumen | Componentes / manifold | Resultado |
|---|---|---|---:|---|---|
| A | 9,9999998 × 9,9999998 × 9,9999998 mm | (5,0000; 5,0000; 5,0000) | 999,999933 mm³ | 1 / sí | PASS |
| B | 9,9999998 × 9,9999998 × 9,9999998 mm | (14,8000; 5,0000; 5,0000) | 999,999933 mm³ | 1 / sí | PASS |

En el orden A,B, el resultado evaluado fue:

| Medida | Esperado | Observado | Estado |
|---|---:|---:|---|
| Dimensiones | 19,8 × 10 × 10 mm | 19,7999999 × 9,9999998 × 9,9999998 mm | PASS dimensional |
| Volumen | 1.980 mm³ | 1.999,999866 mm³ | FAIL |
| Componentes conectadas | 1 | 1 | PASS |
| Cerrada/manifold | Sí | No; `all_edges_manifold=false` | FAIL |
| Elementos degenerados | 0 | 0 aristas, 0 caras | PASS |

La variante A_BEFORE_B queda **FAIL**. La variante B_BEFORE_A no se construyó ni validó: la condición de parada se activó tras fallar la validación de la primera variante. Por tanto, esta ejecución no determina si invertir el orden cambia el resultado.

## Evidencias selladas

El registro `registro_artefactos.jsonl` contiene seis sellos, todos verificados al cierre:

| Artefacto | Tamaño | SHA-256 | Estado |
|---|---:|---|---|
| `evidencias/api_order_preflight.json` | 2.103 B | `607fc300b157da25f2ed68cf16febf91f540045909125732eab1046adfd8af1c` | PASS API/order preflight |
| `logs/api_order_preflight.log` | 4.640 B | `d1ad32856955341d9d6cedb17d61a0edfd45a49acb058c039e4b61a1feaeb60c` | PASS API/order preflight |
| `artifacts/union_A_before_B.blend` | 60.692 B | `1817f1aa63a54e6bb9fe6ec9d51d5e821b6464c66bf2c50d7d10b6ced521a181` | FAIL geometry |
| `logs/build_A_BEFORE_B.log` | 4.117 B | `f387bcde76b0fbac2114dcbe54bf6683338b77a20fc0ce479a8f2dde8f439c10` | PASS saved with order A,B |
| `evidencias/validation_A_BEFORE_B.json` | 5.132 B | `c9a926bd7f7f53f80cf597fac33d34b61bfb36eda0a105e8db7d98684f09681a` | FAIL geometry |
| `logs/validate_A_BEFORE_B.log` | 6.964 B | `c9ff0e9fd6bba9b5ddfa790ed689549dd8170aa1fdb3e5bb50476da8fab10726` | FAIL geometry |

## Comparación con diagnósticos anteriores

- `...DIAG-20261102T190420Z`: las geometrías se conectaron a sockets separados; el validador midió un solo operando.
- `...MULTI-20261102T210408Z`: se confirmó el socket multi-input y se vio que el orden efectivo se invierte respecto de la secuencia de creación; no se construyó geometría.
- `...SORTID-20261102T211127Z`: `multi_input_sort_id` resultó de solo lectura.
- Esta ejecución controló y confirmó el orden efectivo A,B usando únicamente la secuencia de creación. Aunque las dimensiones, una componente y la ausencia de degenerados pasaron, el volumen y manifold fallaron. No se infiere causa raíz.

## Dictamen

El `UNION` multi-input de esta build no produjo, en la única variante validada, el sólido cerrado esperado. La hipótesis de que el problema se resolvía conectando ambos cubos al socket activo `Mesh` **no queda confirmada**. No se evaluó el orden opuesto por la condición de parada.

Se recomienda mantener **A como generador provisional** para CU-01 y no usar Geometry Nodes para afirmar sólidos conectados en esta build. El maestro conserva su SHA histórico al cierre. No se modificaron diagnósticos anteriores; no se exportó STL, no se usó Creality Print y no se avanzó a CU-01.
