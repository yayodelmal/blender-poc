# EXP-BPY-002 — instrucciones reproducibles

Esta ejecución se identifica como `EXP-BPY-002-20261102T112024-0300`. El protocolo se ejecutó con Blender 5.4.0 Alpha, Python integrado 3.13.13, mediante procesos background aislados. La evidencia de preflight y de cada operación está en `logs/`; resultados en `reports/RESULTADO.md`.

## Artefactos

- Entrada autorizada: `../EXP-BPY-001/artifacts/EXP-BPY-001-20261102T105936-0300.blend`, solo lectura.
- Snapshot verificado: `snapshots/EXP-BPY-002-20261102T112024-0300-snapshot_A.blend`.
- Revisión aceptada B: `artifacts/EXP-BPY-002-20261102T112024-0300-revision_B.blend`.
- Candidato negativo, restauración y copias de conflicto: `artifacts/`.
- Scripts específicos: `scripts/`.
- Manifiesto de archivos y hashes: `MANIFIESTO_ARTEFACTOS.json`.

## Repetición

1. Consultar `reports/APROBACION_LINEA_BASE.md` y verificar antes de abrir Blender que el maestro siga siendo archivo regular de 51.810 bytes con SHA-256 `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3`.
2. Usar únicamente el ejecutable documentado en `logs/blender_version_20261102T112024-0300.log` y verificar que reporta Blender 5.4.0 Alpha.
3. Para cada proceso crear `HOME`, `BLENDER_USER_CONFIG`, `BLENDER_USER_SCRIPTS`, `BLENDER_USER_DATAFILES` y `TMPDIR` únicos dentro de `logs/`.
4. Ejecutar Blender con `--background --factory-startup --disable-autoexec --python-exit-code 1`; abrir como entrada el snapshot o la revisión/copia concreta y pasar el contrato JSON al validador mediante `--`.
5. Para editar, invocar `edit_mesh_parameter_20261102T112024-0300.py` con una especificación JSON, usar una entrada verificada y una ruta de salida nueva que aún no exista. El script escala vértices existentes alrededor del centro, comprueba identidad y guarda únicamente el nuevo candidato.
6. Cerrar el proceso escritor; calcular tamaño y SHA-256 del archivo de salida; reabrirlo en otro proceso independiente con `validate_state_20261102T112024-0300.py`.
7. Para comprobar restauración, copiar B a un nombre de salida nuevo y validar la copia en otro proceso. No guardar desde el validador.
8. Para control de revisión, comparar el SHA-256 observado de la base con el esperado y comprobar que la candidata registra el mismo SHA de base usando `revision_guard_corrected_20261102T112024-0300.py`. Probar una ruta base intacta y una copia divergente. Un conflicto debe devolver `CONFLICT_BLOCKED` y `promotion_allowed: false`.
9. Registrar comandos, salidas, códigos, hashes, resultados y advertencias. No sobreescribir maestros, snapshots ni revisiones aceptadas.

Los comandos exactos y resultados de esta ejecución están preservados en los logs; el control de concurrencia inicial defectuoso también se mantiene como evidencia y está descrito en el informe. La tolerancia ±0,01 mm es experimental para esta prueba, no una tolerancia de CU-01.
