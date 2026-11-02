# Resultado — EXP-BPY-002

## Estado global: PASS

Ejecución `EXP-BPY-002-20261102T112024-0300`, 2026-11-02, Blender 5.4.0 Alpha (build hash `745ab9a3e3c5`), Python integrado 3.13.13, macOS Apple Silicon. `PASS` aplica solamente a este protocolo y a ese entorno Alpha; no valida una versión estable.

## Historial del bloqueo y resolución

### Registro histórico preservado

El primer intento terminó `NOT RUN` antes de abrir Blender. El informe histórico registró 51.802 bytes y SHA-256 `6a23e9e28bfa30043059184d21744b13416b9303da99f0a60a9f056d86eb5141`, mientras que el archivo designado ya observaba 51.810 bytes y SHA-256 `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3`. Ese informe no se ha reescrito.

### Investigación INC-BPY-001

La investigación concluyó dictamen B — nueva línea base candidata, con validación semántica satisfactoria. No se encontró una copia binariamente idéntica a la huella histórica ni una causa raíz concluyente; se identificó una probable asociación incorrecta de huella/artefacto. Los documentos del incidente conservan la divergencia y las limitaciones.

### Aprobación actual

La autorización explícita aprobó el artefacto `105936` en su tamaño actual (51.810 bytes) y SHA-256 `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3` únicamente como entrada de EXP-BPY-002. La decisión y su alcance constan en [APROBACION_LINEA_BASE.md](APROBACION_LINEA_BASE.md). El maestro no se alteró.

## Resultados

| Verificación | Estado | Evidencia |
|---|---|---|
| Preflight del maestro aprobado | PASS | `logs/preflight_20261102T112024-0300.txt`: regular, 51.810 bytes, SHA exacto aprobado |
| Versión y ejecutable | PASS | `logs/blender_version_20261102T112024-0300.log`; Blender 5.4.0 Alpha, Python 3.13.13 |
| Snapshot íntegro | PASS | Snapshot de 51.810 bytes con SHA idéntico al maestro; `logs/snapshot_copy_...txt` |
| Reapertura y validación del snapshot | PASS | `logs/snapshot_validation_20261102T112024-0300.log` |
| Edición del objeto existente | PASS | `logs/edit_B_20261102T112024-0300.log`; punteros de objeto/malla y conteo de vértices conservados |
| Persistencia y validación independiente de B | PASS | `logs/revision_B_validation_20261102T112024-0300.log` |
| Control negativo X=55 mm | PASS (rechazado) | `logs/negative_binarybase_validation_20261102T112024-0300.log`: dimensiones y parámetro X fallan el contrato; exit 1 esperado |
| Restauración desde B | PASS | Copia restaurada con SHA binario idéntico a B y reabierta; `logs/restored_validation_...log` |
| Conflicto de revisión optimista | PASS | Guard corregido: base intacta elegible; copia base divergente produce `CONFLICT_BLOCKED`, promoción false; logs `revision_guard_no_conflict_...` y `revision_guard_conflict_...` |
| Maestro sin cambios | PASS | Hash final idéntico a línea base aprobada; tamaño 51.810 bytes |

## Medidas

- Snapshot A: 50.000000745 × 50.000000745 × 50.000000745 mm, centro [0,0,0], escala [1,1,1].
- Revisión B/restaurada: 50.000000745 × 50.000000745 × 70.000000298 mm, centro [0,0,0], escala [1,1,1]. Desviación máxima frente a parámetros esperados: menos de 0,000001 mm, dentro de ±0,01 mm.
- Topología B: 8 vértices, 12 aristas, 6 caras, un componente, todas las aristas manifold.
- Parámetros conservados en propiedades del objeto (`parameters_mm`); no son reactivos por sí mismos. La operación explícita de edición escaló coordenadas existentes del mesh sobre Z y actualizó esos metadatos.

## Controles y anomalías de ejecución

- El control negativo correcto se rechazó según lo esperado. Los artefactos de prueba quedaron separados de B.
- Una primera pasada del guard comparó por error el hash semántico con el checksum binario; detectó conflicto pero reportó falsamente que B estaba alterada. Luego una primera corrección comparó el archivo candidato con el hash de su base, una comparación inválida. Se conservan scripts, candidatos y logs de esas pasadas para trazabilidad; no se usan como evidencia de aprobación.
- El control definitivo separó la huella observada de la base del checksum del candidato y verificó también el hash de base declarado por este. En base intacta permitió elegibilidad; ante una copia divergente de la base bloqueó promoción. No se promovió ningún candidato concurrente.
- Blender emitió `ARCH_WARN: ARCH_CACHE_LINE_SIZE != Arch_ObtainCacheLineSize()` durante los procesos background. No impidió las lecturas/escrituras previstas; queda registrado como advertencia del entorno.
- Blender generó miniaturas dentro de los perfiles `HOME` experimentales ubicados bajo `experimentos/EXP-BPY-002/logs/`. No se observaron escrituras fuera del directorio experimental durante esta ejecución.

## Artefactos principales

Los hashes y tamaños completos por ejecución están en [MANIFIESTO_ARTEFACTOS.json](../MANIFIESTO_ARTEFACTOS.json). Evidencia detallada en `logs/`; scripts propios de la ejecución en `scripts/`.

| Artefacto | Tamaño | SHA-256 |
|---|---:|---|
| Maestro aprobado (solo lectura) | 51.810 | `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3` |
| Snapshot A | 51.810 | `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3` |
| Revisión B | 52.084 | `08a85ae9c8c413c24bc06fcfed0296b962e02dc3bc6a44af7373ee80c2b3a194` |
| Restaurada desde B | 52.084 | `08a85ae9c8c413c24bc06fcfed0296b962e02dc3bc6a44af7373ee80c2b3a194` |

## Conclusión

EXP-BPY-002 obtuvo `PASS`: editó el mesh existente sin sustituir su objeto/datos, conservó invariantes, persistió y reabrió B, rechazó la geometría inválida, recuperó B y bloqueó un conflicto base simulado. El archivo maestro conservó la huella aprobada. No se exportó STL ni se ejecutó EXP-BPY-003.

Se recomienda diseñar EXP-BPY-003 (relieve geométrico, validación/topología y exportación STL) como siguiente fase, manteniendo la validación separada y sin ejecutar hasta autorización.

## Limitación de observabilidad

Los códigos de salida y estados por operación se consolidaron en `logs/resumen_operaciones_20261102T112024-0300.txt`. Blender dejó duraciones internas en los logs, pero el tiempo de pared individual de cada invocación no quedó persistido durante esta ejecución interactiva; no se estiman como mediciones. Para futuras ejecuciones conviene envolver cada proceso en un registro que capture inicio/fin y código de salida. Esta limitación no altera los criterios geométricos ni de recuperación aprobados.
