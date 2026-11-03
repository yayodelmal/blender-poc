---
name: blender-color
description: Use when en blender-poc se pide cambiar el color, la rugosidad o el material de un modelo que ya existe (blanco mate, un color liso, una variante visual) sin tocar su forma.
---

# blender-color: solo apariencia

Blender tarda menos de 1 s por proceso. El tiempo se pierde en reescribir scripts, validadores y carpetas. Elige la ruta primero.

## Ruta corta: solo apariencia

Aplica si el cambio es **únicamente** color, rugosidad o nombre de material y la geometría no se toca. No aplica a nada que cambie forma, dimensiones, STL o lo que se imprime.

```
python3 herramientas/aplicar_material.py RUTA.blend --color blanco --rugosidad 0.8
```

- `--color`: nombre (blanco, negro, gris, rojo, verde, azul, amarillo, naranja) o hex `RRGGBB`.
- `--objeto NOMBRE` si la escena tiene más de un mesh. `--salida` para elegir destino (def. `variantes/<fuente>_<color>.blend`).
- Un solo proceso: verifica el hash de Blender (ADR-0002), aplica el material, comprueba que la huella de geometría no cambió, guarda un `.blend` nuevo (nunca sobrescribe), reabre y verifica material, y añade una línea a `variantes/registro_variantes.jsonl`.
- Si dice `PASS`, terminaste. No crees carpeta de experimento, informe, scripts de validación ni sellado.
- Si falla, no dejes el candidato y reporta el error tal cual.

Esta ruta es una decisión del responsable (2026-11-03). Es solo para variantes visuales y no es evidencia de pieza imprimible ni de CU-01.

## Si el pedido no es solo apariencia

| Pedido | Skill |
|---|---|
| Crear o cambiar forma, dimensiones, validar una malla | `blender-ruta-completa` |
| Uniones booleanas o Geometry Nodes | `blender-geometry-nodes` |
| Sellar, hashes, revisiones aceptadas | `blender-integridad` |
| STL, 3MF, laminado, impresión | `blender-exportar-imprimir` |
| Cerrar un run y actualizar el estado | `blender-cierre-sesion` |

Esta herramienta aplica colores lisos. Una textura procedural (por ejemplo el marmoleado Voronoi) no entra aquí: el acabado por defecto de los modelos nuevos es `herramientas/hyper_pla_marmol.py` (ver `AGENTS.md`).

## Para no perder tiempo

- Comparar floats de Blender con tolerancia (~1e-5): guarda `0.8` como `0.8000000119`.
- Antes de reintentar un script que falló, lee el log del fallo anterior y corrige la causa.
