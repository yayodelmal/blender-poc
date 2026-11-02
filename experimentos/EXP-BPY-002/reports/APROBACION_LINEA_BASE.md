# Aprobación de línea base — EXP-BPY-002

Registro creado: 2026-11-02T11:20:24-0300 (America/Santiago).

## Decisión nueva

- Incidente relacionado: INC-BPY-001.
- Dictamen de integridad: **B — NUEVA LÍNEA BASE CANDIDATA**.
- Artefacto/run aprobado como entrada de EXP-BPY-002: `105936`.
- Ruta relativa al proyecto: `experimentos/EXP-BPY-001/artifacts/EXP-BPY-001-20261102T105936-0300.blend`.
- Tamaño esperado: 51.810 bytes.
- SHA-256 aprobado: `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3`.

## Motivo y trazabilidad

INC-BPY-001 reconstruyó que el digest histórico `6a23e9e28bfa30043059184d21744b13416b9303da99f0a60a9f056d86eb5141` y el tamaño de 51.802 bytes pertenecían a un artefacto de otro run (`105833`), mientras que el artefacto `105936` tenía tamaño 51.810 y digest `a5f0aa70…`. Una copia inspeccionada con `--disable-autoexec` pasó las invariantes geométricas y paramétricas. El dictamen recomendó tratar `105936` con `a5f0…` como candidata y requerir decisión del responsable antes de usarla.

El responsable aprueba ahora explícitamente ese artefacto y esa huella como línea base de entrada para EXP-BPY-002. El valor histórico anterior queda documentado como discrepancia de asociación; no se presenta como si nunca hubiera existido y no se editan informes históricos.

Referencias:

- `investigacion/incidentes/INC-BPY-001/reports/INC-001_RECONSTRUCCION.md`
- `investigacion/incidentes/INC-BPY-001/reports/INC-003_VALIDACION_SEMANTICA.md`
- `investigacion/incidentes/INC-BPY-001/reports/INC-005_DICTAMEN.md`
- `experimentos/EXP-BPY-001/reports/RESULTADO.md` (registro histórico conservado)
- `experimentos/EXP-BPY-002/reports/RESULTADO.md` (bloqueo previo conservado)

## Alcance autorizado y restricción

Se autoriza usar el archivo únicamente como entrada verificada de EXP-BPY-002. No se autoriza modificar, sobrescribir, sustituir ni alterar el maestro. Cualquier apertura se hará sobre una copia de snapshot, con `--disable-autoexec` y perfil/HOME/temporales aislados. Las mutaciones se guardarán solo como artefactos nuevos dentro de `experimentos/EXP-BPY-002/`.

Esta decisión no altera el resultado histórico de EXP-BPY-001, no corrige sus documentos históricos y no implica que Blender 5.4.0 Alpha sea estable o apto para producción.
