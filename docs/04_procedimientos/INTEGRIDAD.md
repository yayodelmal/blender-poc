# Procedimiento de integridad de artefactos

**Vigente desde:** 2026-11-02. Convierte INC-006 (`INTEGRIDAD_INC-006_copia.md`) en regla de trabajo. Cada identificador de la lista siguiente es un campo del registro.

## Reglas

1. **Nunca teclear un hash o un tamaño.** Se calculan con `herramientas/sellar_artefacto.py`.
2. **Sellar después de que cierre el proceso que escribió el archivo**, comprobando su código de salida.
3. **Un registro por artefacto**, con ruta y `run_id` en la misma línea: así un hash no puede asociarse al archivo de otra ejecución.
4. **Revisiones aceptadas inmutables.** Un cambio crea un archivo nuevo con su propio registro.
5. **Rehashear tras la validación** (`--verify`). Si difiere del sellado, el artefacto no se promueve.
6. **Archivos que puede guardar una aplicación GUI** (3MF de Creality Print): se trabaja siempre sobre una copia, y su registro lleva `mutable: true`. Antes y después de la sesión se verifica el original.
7. **Los informes no se hashean en el registro.** Solo artefactos (`.blend`, STL, 3MF, capturas, scripts).
8. Las correcciones a registros históricos van en [ERRATAS](../06_estado/ERRATAS.md), nunca sobre el original.
9. Formato de `run_id` hacia adelante: `EXP-BPY-NNN-AAAAMMDDTHHMMSSZ` (UTC). Lo histórico no se renombra.

## Registro (una línea JSON por artefacto, `registro_artefactos.jsonl` en la carpeta del experimento)

| Campo | Contenido |
|---|---|
| `run_id` | Ejecución que produjo o utilizó el artefacto |
| `artifact_id` | Identificador propio del artefacto (por ejemplo `master`, `snapshot_A`, `stl`); distinto del `run_id` |
| `path` | Ruta relativa al repositorio |
| `size_bytes`, `sha256` | Calculados por la herramienta |
| `sealed_at_utc` | Instante del cálculo |
| `role` | `produced`, `input` o `evidence` |
| `producer_script`, `producer_script_sha256` | Script que lo generó (si aplica) |
| `blender` | Versión/build y hash del ejecutable (opcional) |
| `exit_code` | Del proceso productor |
| `mutable` | `true` si una aplicación puede reescribirlo |
| `expected` / `observed` | Parámetros esperados y mediciones (opcional, texto o JSON) |
| `validation` | `PASS`, `FAIL`, `INCONCLUSIVE` o `NOT RUN` |
| `approval` | Quién y cuándo lo aprobó, o `null` |

La herramienta rellena `size_bytes`, `sha256`, `sealed_at_utc` y la ruta; el resto lo aporta quien invoca.

## Uso

```
python3 -I herramientas/sellar_artefacto.py seal \
    --registro experimentos/EXP-BPY-006/registro_artefactos.jsonl \
    --run-id EXP-BPY-006-20261102T180000Z --artifact-id master \
    --path experimentos/EXP-BPY-006/artifacts/….blend --role produced \
    --producer-script experimentos/EXP-BPY-006/scripts/build.py --exit-code 0

python3 -I herramientas/sellar_artefacto.py verify \
    --registro experimentos/EXP-BPY-006/registro_artefactos.jsonl
```

`seal` se niega a registrar dos veces el mismo `run_id` + `artifact_id` y a sellar un archivo inexistente. `verify` recalcula todo y sale con código distinto de cero si algo difiere.

## Límite

El sellado detecta cambios posteriores al sellado, no los anteriores. Los permisos de archivo ayudan contra accidentes, no son una garantía criptográfica.
