# EXP-BPY-003 — relieve, topología y STL

Ejecución `EXP-BPY-003-20261102T144300Z`; Blender 5.4.0 Alpha, Python 3.13.13. El resultado y alcance se describen en `reports/RESULTADO.md`; rutas, tamaños, hashes y metadatos de proceso en `MANIFIESTO_ARTEFACTOS.json`.

## Archivos principales

- Maestro editable validado (vista original): `artifacts/EXP-BPY-003-20261102T144300Z_relief_plate_master.blend`.
- Copia recomendada para abrir en Blender: `artifacts/EXP-BPY-003-20261102T144300Z_relief_plate_open_ready.blend` (misma geometría, encuadre guardado).
- Snapshot reabierto: `snapshots/EXP-BPY-003-20261102T144300Z_relief_plate_A_snapshot.blend`.
- STL en milímetros numéricos: `artifacts/EXP-BPY-003-20261102T144300Z_relief_plate.stl`.
- Scripts: `scripts/build_relief_plate.py`, `validate_relief_blend.py`, `make_negative_candidate.py`, `export_stl.py`, `validate_stl.py` y `run_blender.py`.
- Negativos aislados: `artifacts/*negative*`.

## Reproducción

1. Usar el ejecutable `/Applications/Blender.app/Contents/MacOS/Blender` y confirmar Blender 5.4.0 Alpha; el experimento no establece compatibilidad con otras versiones.
2. Ejecutar cada comando con `scripts/run_blender.py LABEL -- ...`. El lanzador crea `HOME`, configuración, scripts, datos y temporales separados dentro de `logs/profile_LABEL`, y guarda log y `.meta.json` con código y duración.
3. Construir a una ruta nueva inexistente con `build_relief_plate.py`; no sobrescribir ningún artefacto.
4. Reabrir mediante otro proceso y validar usando `validate_relief_blend.py`, pasando un contrato JSON después de `--`. Contrato usado: bounds 80×60×5 mm, 27 ladrillos, área superior 3679,2 mm², tolerancia ±0,01 mm.
5. Copiar el modelo verificado al snapshot, calcular SHA-256 y reabrir/validar también esa copia antes de exportar.
6. Ejecutar los controles negativos desde una copia del maestro. Cada validador debe producir `FAIL` y código distinto de cero para el candidato rechazado.
7. Exportar únicamente el objeto principal con `export_stl.py`, `global_scale=1000`, `use_scene_unit=False`, forward Y/up Z. Nunca exportar un candidato no validado.
8. En un proceso Blender recién iniciado, importar con `validate_stl.py` y `import_global_scale=0.001`. Comparar bounds, topología, componentes, volumen y 27 regiones superiores. El STL contiene números interpretados como mm por la convención del experimento; no almacena esa unidad de manera universal.
9. Calcular los hashes después de que el proceso escritor cierre y verificar cada ruta de forma individual. No sobrescribir maestro ni snapshot.

Las primeras revisiones fallidas y sus logs se conservan para diagnóstico; la revisión v3 y los archivos `relief_plate_master.blend` / `relief_plate_open_ready.blend` tienen la geometría validada. El generador centra la vista 3D en el objeto y la guarda a una distancia útil para abrir archivos nuevos. No se ejecutó Creality Print ni impresión física.
