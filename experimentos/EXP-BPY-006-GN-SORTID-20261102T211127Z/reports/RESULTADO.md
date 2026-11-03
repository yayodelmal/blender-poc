# Diagnóstico Geometry Nodes — asignación explícita del orden multi-input

**Resultado: INCONCLUSIVE — detenido antes de construir los `.blend`.**  
**run_id:** `EXP-BPY-006-GN-SORTID-20261102T211127Z`

## Preflight de repositorio e integridad

- Repositorio accesible en `/Users/yayo/Projects/blender-poc`, rama `main`, remoto `origin`.
- Los registros de integridad de `EXP-BPY-006-GN-MULTI-20261102T210408Z` y `EXP-BPY-006-GN-DIAG-20261102T190420Z` verificaron `OK` antes de empezar.
- Blender en `/Applications/Blender.app/Contents/MacOS/Blender`: 5.4.0 Alpha, build `745ab9a3e3c5`, SHA-256 `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`, igual al pin de ADR-0002.
- El maestro EXP-BPY-003 coincidía con su SHA histórico antes del diagnóstico: `09f7ee7c1ac207df00b1e8494e41b39a0c1eec4e048edbfcac61b71fd998495b`.

## Inspección API y motivo de parada

En `UNION`, Blender reportó un único socket multi-input GEOMETRY activo, `Mesh` (índice 1, identificador `Mesh 2`), y una salida GEOMETRY activa única, `Mesh`. `Mesh 1` (índice 0) estaba deshabilitado.

El preflight creó enlaces de inspección sin evaluar geometría ni guardar modelos. Intentó asignar sort IDs explícitos para A→B y B→A y leer el orden resultante. La primera asignación falló con:

```text
AttributeError: bpy_struct: attribute "multi_input_sort_id" from "NodeLink" is read-only
```

No se pudo cumplir el requisito de asignar explícitamente el orden. El proceso terminó con código 2; no se construyeron archivos `.blend`, no se ejecutaron validadores y no se probaron ambas uniones. El procedimiento no se corrigió ni se repitió.

## Evidencia sellada

El comando completo, versión, hash de Blender, perfil aislado, tiempos UTC, código de salida y log están en `logs/api_sortid_preflight.meta.json` y `logs/api_sortid_preflight.log`.

| Evidencia | Tamaño | SHA-256 | Estado |
|---|---:|---|---|
| `evidencias/api_sortid_inventory.json` | 1.989 B | `7f92b586a09a0618b699883869deabc2425c41238c03812ce066ca197aee54a4` | INCONCLUSIVE |
| `logs/api_sortid_preflight.log` | 4.755 B | `436498205415a3a6c69268f663cb5b363a4545fcff0706c05175051f22d7d9c6` | INCONCLUSIVE |

Ambas evidencias quedaron selladas en `registro_artefactos.jsonl`. Este registro no contiene artefactos geométricos, porque no se construyeron candidatos.

## Comparación e hipótesis

- En `EXP-BPY-006-GN-DIAG-20261102T190420Z`, A y B se conectaron a entradas distintas (`Mesh 1` y `Mesh`); la salida medida fue un solo cubo y cambió al invertirlas.
- En `EXP-BPY-006-GN-MULTI-20261102T210408Z`, se identificó correctamente `Mesh` como multi-input activo, pero el orden enumerado fue inverso al orden de creación de enlaces; no se midió geometría.
- Esta ejecución confirma que `multi_input_sort_id` es de solo lectura desde la API Python en la build probada. No determina qué resultado produciría una unión si ambos cubos se conectan al socket activo `Mesh` con un orden efectivo comprobado por otro mecanismo.

**Hipótesis: INCONCLUSA.** No hay mediciones de los dos cubos, la unión ni su sensibilidad al orden. No se atribuye causa raíz.

## Estado del alcance

El maestro EXP-BPY-003 y las ejecuciones anteriores no se modificaron. No hubo archivos de modelo nuevos, exportación STL, uso de Creality Print ni impresión. CU-01 no se inició.

Una prueba futura tendría que definir el orden mediante el orden real de creación de enlaces —sin escribir `multi_input_sort_id`— y verificarlo inequívocamente antes de evaluar geometría. Requeriría un directorio y `run_id` nuevos.
