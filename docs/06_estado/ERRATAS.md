# Erratas sobre informes históricos

Los informes históricos **no se editan**. Cada entrada conserva la afirmación original, la que tiene mejor respaldo y las fuentes. No se recalculan ni sustituyen valores históricos como si siempre hubieran sido correctos.

## E-001 — Hash y tamaño del maestro de EXP-BPY-001

- **Afirmación original** (`experimentos/EXP-BPY-001/reports/RESULTADO.md`, sección Artefactos): el `.blend` del run `105936` mide 51.802 B y tiene SHA-256 `6a23e9e28bfa30043059184d21744b13416b9303da99f0a60a9f056d86eb5141`.
- **Mejor respaldo**: ese tamaño y hash pertenecen al archivo del run `105833`. El archivo del run `105936` mide 51.810 B y tiene SHA-256 `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3`. Confirmado por recálculo propio (2026-11-02, auditoría) de ambos archivos.
- **Fuentes**: `investigacion/incidentes/INC-BPY-001/reports/INC-001` a `INC-005`; `experimentos/EXP-BPY-002/reports/APROBACION_LINEA_BASE.md`.
- **Límite**: no hay hash sellado en el instante de generación; una edición posterior con timestamps preservados no puede descartarse criptográficamente.

## E-002 — Descripción de L-001 en APRENDIZAJES_OPERATIVOS

- **Afirmación original** (`experimentos/EXP-BPY-005/APRENDIZAJES_OPERATIVOS.md`, L-001): "Hash de maestro .blend divergió por 8 bytes… Causa raíz no establecida".
- **Mejor respaldo**: los 8 bytes son la diferencia de tamaño entre dos runs distintos (INC-002), no una modificación del mismo archivo. La explicación más probable es un error de asociación (INC-004, H5, confianza alta); la ausencia de un hash contemporáneo impide una prueba definitiva.
- **Fuentes**: INC-002, INC-004, INC-005.

## E-003 — Hash del 3MF de trabajo de EXP-BPY-004 en el manifiesto de EXP-BPY-005

- **Afirmación original** (`experimentos/EXP-BPY-005/MANIFIESTO_ARTEFACTOS.json`): `…/EXP-BPY-004/artifacts/EXP-BPY-004-20261102T154038Z_working_copy.3mf` con SHA-256 `659b0890553a1e30087d3c6d329520179306767597938d45d705c3d919a2b5a4`.
- **Mejor respaldo**: ese hash corresponde al estado anterior del archivo, que coincide con el proyecto original `…121521-0300_slice_project.3mf`. El archivo actual mide 23.873 B y tiene `1a67df633765254308be33262862609f78e0520b405a95fb7593dc0c6d42d50f`; hay copia de custodia con el mismo hash.
- **Fuentes**: `investigacion/incidentes/INC-BPY-002/` (informe y manifiesto). Confirmado por recálculo propio en la auditoría.

## E-004 — Hash del informe en el manifiesto de EXP-BPY-005

- `experimentos/EXP-BPY-005/MANIFIESTO_ARTEFACTOS.json` registra `reports/RESULTADO.md` con `e9fad6aa77d0…`; el archivo actual (8.773 B) da `6ff4a097128b…`.
- **Explicación**: el informe se editó después de calcular el hash. No indica manipulación. Es una deuda de diseño: los manifiestos deben cubrir artefactos inmutables y no informes que se siguen editando.

## E-005 — Estado de EXP-BPY-004 en CIERRE_FASE_1, README de 004 y matriz de EXP-BPY-005

Ver [RECONCILIACION_EXP-BPY-004](RECONCILIACION_EXP-BPY-004.md).

## E-006 — Variante marmoleada de CU-01 modificada después de sellarse

- **Afirmación original** (`experimentos/CU-01/CU-01-COLOR-PLA-MARBLE-20261103T024738Z/registro_artefactos.jsonl`, `marbled_variant`): `artifacts/CU01_REV002_pla_marble.blend` mide 104.100 B y tiene SHA-256 `d13a02f0bae9…`, sellado a las 2026-11-03T02:48:10Z.
- **Mejor respaldo**: el archivo actual mide 120.245 B y da `0f43365c5017…`, así que `sellar_artefacto.py verify` lo marca `CAMBIADO`. Blender guardó encima del sellado y dejó `artifacts/CU01_REV002_pla_marble.blend1`, cuyo hash y tamaño coinciden con lo sellado: es la versión original. No se sabe quién guardó ni qué se cambió. Hipótesis sin confirmar: se guardó desde Blender con interfaz al ajustar el material que `herramientas/hyper_pla_marmol.py` declara replicar.
- **Acción**: la versión original se conserva sin cambios como `artifacts/CU01_REV002_pla_marble_sellado_original.blend` (copia byte a byte del `.blend1`; hash y tamaño idénticos a lo sellado, comprobados con la herramienta). El archivo modificado y el registro original no se tocan; el informe del run sigue describiendo la versión sellada.
- **Fuentes**: el registro del run y `herramientas/sellar_artefacto.py verify --registro experimentos/CU-01/CU-01-COLOR-PLA-MARBLE-20261103T024738Z/registro_artefactos.jsonl`.
- **Límite**: la copia original no está en el registro sellado (no se reescriben registros). Su identidad con lo sellado se apoya en esta entrada y en el recálculo. El `.blend1` sigue en disco pero está ignorado por git.
