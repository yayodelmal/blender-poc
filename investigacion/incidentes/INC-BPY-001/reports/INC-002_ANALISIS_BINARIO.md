# INC-002 — Hashes, metadatos y comparación binaria

Capturas: 2026-11-02, zona America/Santiago (-0300). Ningún archivo fuente fue editado.

## Identidades observadas

| Candidato | Tamaño | SHA-256 completo | Fechas relevantes | Clasificación |
|---|---:|---|---|---|
| `experimentos/EXP-BPY-001/artifacts/EXP-BPY-001-20261102T105936-0300.blend` | 51.810 | `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3` | birth/modify/change 2026-11-02 10:59:42 -0300 | `HASH MISMATCH` contra huella listada en RESULTADO.md; identidad más consistente con run 105936 por ruta, log e ID interno |
| `experimentos/EXP-BPY-001/artifacts/EXP-BPY-001-20261102T105833-0300.blend` | 51.802 | `6a23e9e28bfa30043059184d21744b13416b9303da99f0a60a9f056d86eb5141` | birth/modify 2026-11-02 10:58:53 -0300 | `HASH MATCH` contra digest listado en RESULTADO.md; no es el artefacto `105936`, es otro run con distinto ID y nombre de objeto |
| `investigacion/incidentes/INC-BPY-001/evidencias/maestro_actual_copia_20261102T110754-0300.blend` | 51.810 | `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3` | copia capturada 11:07:54 -0300; copia binaria del candidato 105936 | `HASH MISMATCH` contra digest del informe; copia forense del maestro actual, no respaldo histórico independiente |

El informe final cita expresamente el ID aprobado `105936`, pero sus 51.802 bytes y SHA `6a23…` son exactamente los del archivo `105833`. Ese candidato no se considera respaldo auténtico del run designado: sus logs y propiedades internas prueban que corresponde a otro run.

## Búsqueda de copias

Se buscaron `.blend`, `.blend1` y `.blend2` dentro del proyecto (`find .` limitado al workspace). Solo aparecieron los dos artefactos de EXP-BPY-001 y la copia forense creada durante este incidente. No hay backup Blender `.blend1/.blend2`, snapshot de EXP-BPY-002 ni copia independiente del binario `105936` anterior a esta investigación.

## Comparación binaria entre los dos runs

Se comparó el artefacto `105833` (que coincide con la huella publicada por error) con el artefacto designado `105936`:

- Tamaños: 51.802 vs. 51.810 bytes; diferencia de tamaño +8 bytes.
- En las primeras 14.441 posiciones del rango común no se hallaron diferencias.
- Primera posición distinta (base 1): 14.442.
- Última posición distinta dentro del archivo más corto (base 1): 51.802.
- Posiciones con bytes distintos en el rango común: 37.154.
- Distribución: posiciones 1–12.950: 0; 12.951–25.901: 11.397; 25.902–38.851: 12.892; 38.852–51.802: 12.865.

La comparación es entre **dos generaciones diferentes**, no entre un original y su versión modificada. Ambos archivos están en contenedor comprimido Zstandard; sus bytes comprimidos no permiten inferir qué campos semánticos cambiaron. La distribución dispersa no demuestra alteración geométrica.

## Formato, permisos y atributos

- `file` reconoce el maestro como Zstandard comprimido; encabezado observado: `28 b5 2f fd …`. Blender 5.4.0 Alpha lo abrió como `.blend` sin volverlo a guardar.
- Modo: `-rw-r--r--`, propietario `yayo`, grupo `staff`; no se observó ACL adicional en `ls -leO@`. El propietario puede escribir, por lo que los permisos no hacen el artefacto inmutable.
- Atributo extendido observado: `com.apple.provenance` (11 bytes). No permite identificar por sí solo un autor ni atribuir la divergencia.
- Birth, modify y change del maestro actual coinciden con el instante de guardado del log, 10:59:42. Access time cambió al inspeccionarlo, como efecto normal de lectura; no equivale a modificación del contenido.

## Integridad durante el incidente

SHA-256 del maestro antes de copiar/inspeccionar: `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3`. SHA-256 después de inspeccionar la copia: mismo valor. La copia de inspección también mantuvo ese digest antes/después. Por tanto, no se detectó cambio del maestro durante esta investigación.

Evidencias: `../logs/source_precheck_20261102T110754-0300.txt`, `copy_precheck…`, `integrity_post_inspection…` y `candidate_search_comparison_20261102T1110.txt`.
