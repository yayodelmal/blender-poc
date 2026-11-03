---
name: blender-ruta-completa
description: Use when en blender-poc hay que crear o modificar geometría con scripts bpy (revisiones de CU-01, experimentos EXP-BPY), ejecutar Blender en background, validar una malla, o un build o validate falla y se está por reintentar o reescribir un lanzador o validador.
---

# blender-ruta-completa

Todo cambio que toque forma, dimensiones o lo que se imprime. Si solo cambia color o material, usar `blender-color`.

**Regla de oro:** no escribir lanzador ni validador. Existen en `herramientas/`. Solo se escribe el script que construye el modelo.

## Flujo

1. Leer `docs/06_estado/ESTADO_FASES.md`. CU-01 necesita decisiones del responsable (pared, base, drenaje, si 150 mm incluye el relieve) antes de modelar; si faltan, preguntar.
2. Carpeta de run nueva: `experimentos/<EXP>/<NOMBRE>-<AAAAMMDDTHHMMSSZ>/` con `artifacts/ evidencias/ scripts/ logs/ reports/`. El nombre de la carpeta es el `run_id`.
3. Escribir `scripts/build_model.py`. Unidades: 1 unidad Blender = 1 m, dimensiones en mm sobre la malla evaluada. Al terminar la geometría, llamar `aplicar_material_por_defecto(obj)` de `herramientas.hyper_pla_marmol` (AGENTS.md), salvo que el usuario pida otro acabado. Añadir la raíz del repo a `sys.path` antes del import.
4. Construir:
   `python3 herramientas/lanzar_blender.py RUN build RUN/scripts/build_model.py RUN/artifacts/NOMBRE.blend`
5. Validar **en otro proceso**:
   `python3 herramientas/lanzar_blender.py RUN validate herramientas/validar_malla.py RUN/artifacts/NOMBRE.blend RUN/evidencias/validation.json --dims 150,150,60 --volumen 423761.6 --cavidad 128,128,56`
   Comprueba mesh único, envolvente, componentes, manifold, orientación, volumen, degenerados y, con `--cavidad`, el hueco interior (paredes, piso y tapa abierta, con rayos). Sale con 2 si falla. Repetir con una cavidad equivocada debe fallar: es el control negativo.
6. Sellar con `blender-integridad`, escribir `reports/RESULTADO.md` como archivo nuevo y cerrar con `blender-cierre-sesion`.

## Cuando algo falla

- Leer `logs/<etiqueta>.log` antes de tocar nada. Corregir la causa, no probar variantes al azar.
- Cada reintento va en una **carpeta nueva**. El intento fallido se conserva; no se borra ni se sobrescribe.
- Segundo fallo con la misma pinta: parar y aislar con un ensayo en memoria (carpeta `DIAG-<tema>-<UTC>/`) en vez de un tercer build. En CU-01 REV-001 fueron 2 builds fallidos, 4 ensayos y un tercer build que pasó.
- Uniones booleanas o Geometry Nodes con resultado raro: `blender-geometry-nodes`.

## Errores frecuentes

| Error | Corrección |
|---|---|
| Dar por bueno un `exit 0` | Blender sale con 0 con geometría rota. Solo vale el validador. |
| Comparar un float de Blender sin tolerancia | `0.8` se guarda como `0.8000000119`. Usar tolerancia. |
| Copiar `run_blender.py` a cada carpeta | Usar `herramientas/lanzar_blender.py`. |
| Reutilizar etiqueta de log | El lanzador se niega. Usar etiqueta nueva. |
| Decir "listo para imprimir" tras un PASS digital | Un PASS digital no es una pieza imprimible. Ver `blender-exportar-imprimir`. |
