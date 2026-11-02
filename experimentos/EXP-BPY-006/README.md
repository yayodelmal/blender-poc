# EXP-BPY-006

Ensayo de parametricidad y edición incremental. Los scripts y candidatos pertenecen solo a este directorio, salvo el maestro EXP-BPY-003 que se leyó y verificó sin escribir.

## Ejecución registrada

- `run_id`: `EXP-BPY-006-20261102T175526Z`
- Blender: `/Applications/Blender.app/Contents/MacOS/Blender`, 5.4.0 Alpha, Python 3.13.13.
- Integridad: usar `python3 herramientas/sellar_artefacto.py verify --registro experimentos/EXP-BPY-006/registro_artefactos.jsonl` desde la raíz del repositorio.
- Cada proceso de Blender corrió con `--background --factory-startup --disable-autoexec --python-exit-code 1` y perfil aislado bajo `profiles/`.

## Reproducción

Los comandos ejecutados aparecen completos en cada `logs/*.meta.json`. No los repitas sobre los nombres de salida existentes: el generador rehúsa sobrescribir. Para una repetición, el responsable debe asignar otro `run_id`, directorios de perfil y nombres de salida.

Ejemplos de los comandos originales (desde la raíz del repositorio):

```sh
python3 experimentos/EXP-BPY-006/scripts/run_blender.py build_A_v2 -- --background --factory-startup --disable-autoexec --python-exit-code 1 --python experimentos/EXP-BPY-006/scripts/build_candidates.py -- A experimentos/EXP-BPY-006/artifacts/EXP-BPY-006-20261102T175526Z_A_bpy_v2.blend
python3 experimentos/EXP-BPY-006/scripts/run_blender.py validate_A_v2 -- --background --factory-startup --disable-autoexec --python-exit-code 1 --python experimentos/EXP-BPY-006/scripts/validate_candidate.py -- experimentos/EXP-BPY-006/artifacts/EXP-BPY-006-20261102T175526Z_A_bpy_v2.blend
```

La ejecución B se detuvo después de observar una salida booleana no contractual. Consultar `reports/RESULTADO.md`; los candidatos fallidos y los errores se conservaron. No se ejecutaron los controles negativos restantes ni C. Este README documenta resultados, no autoriza repetir Blender ni avanzar a CU-01.

## Archivos

- `scripts/`: inspección, generación, validación y probes diagnósticos propios del experimento.
- `artifacts/`: candidatos independientes, incluidos fallidos.
- `snapshots/`: copia byte-idéntica del maestro.
- `logs/`: salida, comando, versiones, duración y código de salida por proceso.
- `registro_artefactos.jsonl`: sello de integridad existente del proyecto.
