---
name: blender-exportar-imprimir
description: Use when en blender-poc se va a exportar un modelo a STL o 3MF, laminarlo en Creality Print, preparar o registrar una impresión en la K1C, o cuando el tamaño del modelo importado sale 10, 100 o 1000 veces distinto del esperado.
---

# blender-exportar-imprimir

Un PASS digital no es una pieza imprimible. Esta skill cubre el paso de `.blend` validado a archivo para el laminador.

## Exportar y verificar el STL

Escena en mm sobre una unidad Blender = 1 m. El STL no declara unidad, así que se fija la escala.

```
python3 herramientas/lanzar_blender.py RUN stl_export herramientas/exportar_stl.py export RUN/artifacts/MODELO.blend RUN/artifacts/MODELO.stl
python3 herramientas/lanzar_blender.py RUN stl_verify herramientas/exportar_stl.py verify RUN/artifacts/MODELO.stl RUN/evidencias/stl_verify.json --dims 150,150,60
python3 herramientas/lanzar_blender.py RUN stl_verify_neg herramientas/exportar_stl.py verify RUN/artifacts/MODELO.stl RUN/evidencias/stl_verify_neg.json --dims 150,150,60 --import-scale 0.01
```

- Exporta con `global_scale=1000` y reimporta con 0,001 en **otro proceso**.
- El tercer comando es el control negativo: **debe terminar en exit 2**. Si pasa, el control no sirve.
- Un STL no conserva el material del modelo.
- Sellar con `blender-integridad` después de verificar.

## Creality Print (versión observada 7.3.0.6157)

1. Nunca abrir el 3MF original: crear copia con nombre nuevo, registrarla con `--mutable` y abrir solo la copia (INC-BPY-002).
2. Verificar el hash del STL de entrada antes y después de la sesión.
3. Registrar el nombre completo del preset antes de laminar. Un preset personalizado no equivale a uno estándar.
4. Guardar capturas `.png` en `evidencias/` (impresora, boquilla, filamento, cama, preset, deslizador de capas al extremo, resumen de G-code) y sellarlas. Sin captura, el criterio queda INCONCLUSIVE.
5. El deslizador de capas: leer su extremo, no la posición del control.
6. Proyecto laminado con nombre nuevo por run.
7. No pulsar `Send print` ni conectar la impresora en un experimento digital.
8. El aviso `please apply glue before print` lo resuelve una persona tras identificar la superficie montada.

## Qué demuestra y qué no

El laminado demuestra que el modelo entra con las dimensiones correctas y genera trayectorias. No demuestra adhesión, acabado, resistencia ni dimensiones de la pieza. Las estimaciones de tiempo y filamento son del laminador, no mediciones.

## CU-01

La medición física con calibre **es exigible**. La excepción dimensional de la Fase 1 (ADR-0003) no se hereda. Mientras no se mida, escribir `NOT RUN` y nunca PASS.

## Errores frecuentes

| Síntoma | Causa |
|---|---|
| Modelo diminuto o gigante en el laminador | Escala de exportación incorrecta (L-004) |
| El 3MF original aparece modificado | Se abrió el original en Creality Print |
| «Laminado OK» sin evidencia | Faltan capturas persistentes (L-007) |
