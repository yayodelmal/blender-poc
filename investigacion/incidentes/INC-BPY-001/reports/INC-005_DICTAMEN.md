# INC-005 — Dictamen de integridad

## Dictamen: B — NUEVA LÍNEA BASE CANDIDATA

El archivo designado `EXP-BPY-001-20261102T105936-0300.blend` existe, tiene SHA-256 actual `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3`, mide 51.810 bytes, concuerda en ruta/ID/tiempo con el log de generación y pasó inspección semántica de lectura sobre una copia. No se encontró una copia histórica independiente de ese run con una huella preexistente verificable.

La huella publicada anteriormente (`6a23e9e2…`, 51.802 bytes) coincide exactamente con el artefacto de otro run (`105833`). No se usa esa copia como reemplazo del maestro `105936`, aunque coincide con el digest escrito en el informe. La evidencia indica con confianza alta un error de asociación en el informe; no prueba que el maestro jamás se modificara conservando timestamps.

El dictamen A no aplica porque el candidato `105833` tiene otro run ID, nombre de objeto y procedencia; no es una copia del artefacto designado `105936`. El dictamen B aplica como candidata porque el archivo actual pasa invariantes, conserva identidad semántica y concuerda con su log de generación. La decisión final de línea base pertenece al responsable.

## Evidencia clave

- Esperado registrado en EXP-BPY-001: SHA-256 `6a23e9e28bfa30043059184d21744b13416b9303da99f0a60a9f056d86eb5141`, tamaño 51.802 bytes.
- Observado para el maestro designado: SHA-256 `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3`, tamaño 51.810 bytes.
- El primero pertenece al archivo `105833`; el segundo al archivo `105936` y su copia forense.
- La inspección semántica de la copia `105936` obtuvo PASS para objeto, parámetros, dimensiones, centro, escala, unidades y topología.
- El SHA del maestro `105936` permaneció igual antes y después de la investigación.

## Estado de EXP-BPY-002

**Sigue bloqueado.** No se modificó ninguna referencia histórica ni se restauró/aprobó el archivo. Para reanudar se requiere autorización explícita que:

1. Apruebe como nueva línea base candidata el path `experimentos/EXP-BPY-001/artifacts/EXP-BPY-001-20261102T105936-0300.blend`, tamaño 51.810 y SHA-256 `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3`.
2. Autorice continuar EXP-BPY-002 usando exactamente esa huella, conservando los informes históricos sin reescribirlos y creando un nuevo snapshot/run ID.

Una aprobación puede rechazar esta candidata y pedir otra evidencia. Este dictamen no sustituye dicha aprobación.
