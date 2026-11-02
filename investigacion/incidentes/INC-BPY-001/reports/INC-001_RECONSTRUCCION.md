# INC-001 — Reconstrucción de la divergencia

Fecha de investigación: 2026-11-02, zona America/Santiago (-0300). Incidente de solo lectura sobre el maestro EXP-BPY-001.

## Conclusión resumida

La evidencia favorece con **confianza alta** un error de asociación en el informe de EXP-BPY-001: el hash y tamaño allí puestos bajo el run aprobado `105936` corresponden exactamente al artefacto de otro run, `105833`. El maestro de `105936` conserva su fecha de nacimiento/modificación de generación, coincide con el log y pasa inspección semántica de solo lectura. No hay evidencia observada de una escritura posterior del maestro, aunque no existe un hash contemporáneo y sellado para el instante de generación; por eso no se puede excluir absolutamente una modificación con timestamps preservados.

No se restauró ni aprobó ningún archivo. EXP-BPY-002 sigue bloqueado hasta autorización expresa de una nueva línea base.

## Línea de tiempo

| Hora local | Evento y evidencia | Interpretación |
|---|---|---|
| 2026-11-02 10:58:52–10:58:53 | Blender 5.4.0 Alpha genera `EXP-BPY-001-20261102T105833-0300.blend`; `logs/generate_20261102T105833-0300.meta` tiene UTC 13:58:52–53, código 0. | Artefacto válido de un run anterior, con ID/nombre de objeto propios de `105833`. |
| 10:59:10 | Proceso independiente valida y reabre `105833`; `logs/validate_20261102T105833-0300.meta`, código 0. El validador no contiene llamadas de guardado. | Se verificaron invariantes de ese run. |
| Después de 10:59:10 y antes de 10:59:42 | La secuencia de comandos local calcula stat/SHA-256 de `105833`: 51.802 bytes y `6a23e9e2…`. No se guardó timestamp separado del cálculo. | Es el valor que después aparece asociado por error a `105936`. El intervalo exacto no puede precisarse. |
| 10:59:42 | Blender guarda `105936`; log `generate_20261102T105936-0300.log` identifica ruta, run ID y `save_result FINISHED`. El birth/modify/change del maestro actual son 10:59:42. | Nombre, ID, log y metadatos del archivo concuerdan. El maestro actual mide 51.810 bytes, SHA `a5f0aa70…`. |
| 10:59:47–10:59:48 | Segundo proceso abre `105936`; `validate_20261102T105936-0300.log` registra `Read blend`. El script valida y termina; no tiene operador/API de guardado. | No se observa una escritura del maestro durante validación. |
| 10:59:42–10:59:48 | En el perfil aislado de `105936` hay una miniatura de 3.257 bytes en `artifacts/retry_20261102T105936-0300/profile/home/.thumbnails/large/…png`. | Auxiliar dentro del perfil de EXP-BPY-001; no es el maestro. El sistema de archivos no fija cuál de los dos procesos la creó. |
| 11:00:50 | `RESULTADO.md` de EXP-BPY-001 tiene mtime 11:00:50. Identifica como aprobado el run `105936`, pero enumera 51.802 bytes y SHA `6a23…`. | Hora observable de la última escritura del informe, no necesariamente del cálculo de hash. El informe mezcla identidad de `105936` con la huella de `105833`. |
| Antes de iniciar esta investigación | EXP-BPY-002 registra 51.810 bytes y SHA `a5f0…` en `source_integrity_check.txt`. | Corresponde al maestro actual de `105936`; EXP-BPY-002 no abrió Blender ni lo copió/modificó. |
| 11:07:54 | Copia forense de solo lectura se hace en `evidencias/`; hash de origen y copia `a5f0…`. | Evidencia desechable, no reemplazo. |
| 11:08:47–11:08:48 | Blender 5.4.0 Alpha abre solo la copia con `--disable-autoexec`; inspección propia de lectura, código 0. | Semántica PASS. Hash del maestro antes y después permanece `a5f0…`. |

Los timestamps de filesystem usan hora local y los logs de proceso UTC. El hash informado por EXP-BPY-001 no tiene un timestamp de captura independiente: solo queda la fecha de modificación del informe (11:00:50) y la secuencia anterior de comandos.

## Reconstrucción de guardados

- El generador `generate_20261102T105936-0300.py` crea el mesh/object y llama una vez a `bpy.ops.wm.save_as_mainfile` hacia el path de `105936`.
- El validador `reopen_validate_20261102T105936-0300.py` solo lee datos, mide la malla y emite JSON; la búsqueda de APIs de escritura no devolvió coincidencias.
- El log de generación reporta la ruta del artefacto, `save_result: FINISHED` y el ID `105936`.
- El log de validación reporta `Read blend` de esa ruta y las invariantes esperadas.
- El auxiliar thumbnail no prueba una escritura del `.blend`. Una ejecución anterior registró intento de thumbnail fuera de la carpeta que falló; la ejecución `105936` usó HOME aislado y el thumbnail encontrado queda bajo su perfil aislado.

## Versiones y ruta

- Ejecutable: `/Applications/Blender.app/Contents/MacOS/Blender`.
- Versión: Blender 5.4.0 Alpha, branch `main`, build hash `745ab9a3e3c5`, build 2026-10-30.
- SHA-256 del ejecutable: `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`.
- Python integrado: 3.13.13; arquitectura del host: arm64.

## Hechos, inferencias e incógnitas

**Hechos:** hay dos archivos `.blend` de los runs `105833` y `105936`; el primero tiene la huella documentada, el segundo la huella observada. Los nombres/IDs y tiempos de generación coinciden con sus logs. El validador no guarda. El actual y su copia forense pasaron inspección semántica. El SHA de origen no cambió durante la investigación.

**Inferencia fuerte:** el informe final trasladó tamaño/hash de `105833` al renglón del maestro `105936`. La exacta igualdad de ambos valores y los IDs distintos lo sustentan.

**Desconocido:** instante original de cálculo del hash listado en el informe; si el maestro `105936` fue modificado entre 10:59:42 y la primera medición de EXP-BPY-002 conservando timestamps; causa exacta de las diferencias internas de los dos contenedores comprimidos.

## Evidencia vinculada

- `../evidencias/inspect_copy_readonly_20261102T110754.py`
- `../evidencias/maestro_actual_copia_20261102T110754-0300.blend`
- `../logs/source_precheck_20261102T110754-0300.txt`
- `../logs/copy_precheck_20261102T110754-0300.txt`
- `../logs/semantic_readonly_20261102T110754-0300.log` y `.meta`
- `../logs/integrity_post_inspection_20261102T110754-0300.txt`
- `../logs/candidate_search_comparison_20261102T1110.txt`
