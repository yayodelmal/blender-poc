---
name: blender-geometry-nodes
description: Use when en blender-poc se construye o modifica geometría con Geometry Nodes o uniones booleanas, o cuando una unión da varias componentes, malla no manifold, volumen distinto del esperado, o un KeyError en sockets del nodo Mesh Boolean.
---

# blender-geometry-nodes

Referencia de lo ya diagnosticado en Blender 5.4.0 Alpha (build `745ab9a3e3c5`). No es verdad general de Blender: son observaciones de esta build.

## Mesh Boolean (nodo Geometry Nodes), operación UNION

| Elemento | Observado |
|---|---|
| Salida de geometría | Se llama `Mesh`, no `Geometry`. Buscar `outputs['Geometry']` da `KeyError` |
| Entrada `Mesh 1` (índice 0) | Deshabilitada en UNION |
| Entrada `Mesh` (índice 1, id `Mesh 2`) | Multi-input, la única activa |
| Orden de enlaces | Crear A y luego B se enumera como **B,A**; B y luego A, como **A,B** |
| `NodeLink.multi_input_sort_id` | Solo lectura (`AttributeError`). No se puede fijar el orden a mano |

Antes de evaluar geometría, inspeccionar los sockets por API y comprobar que hay exactamente una salida GEOMETRY activa.

## Resultado de EXP-BPY-006

- **A, `bpy` con parámetros centralizados: PASS.** Regenera la malla completa y se valida en otro proceso. Es la estrategia mejor respaldada, no es edición incremental.
- **B, Geometry Nodes: FAIL.** Variante A→B: volumen ≈ 2.000 mm³ frente a 1.980 esperado, `all_edges_manifold=false`. B→A no se construyó (se aplicó la condición de parada); no se atribuye causa raíz.
- **C, edición in-place: INCONCLUSIVE / NOT RUN.** La malla fusionada no conserva regiones por ladrillo.

Usar GN en un modelo real requiere decisión del responsable. Por defecto, regenerar con `bpy`.

## Uniones booleanas con `bpy` (CU-01)

Observado: unir un lado o lados opuestos funciona; **incluir caras adyacentes en el mismo operando falló**. Lo que sí pasó: construir y unir **cada cara de forma secuencial**. Eso produjo 1 componente cerrada y manifold (REV-001, REV-002). No prueba una causa general de Blender.

## Si una unión da algo raro

1. Medir componentes, manifold, volumen y envolvente con `herramientas/validar_malla.py`.
2. Aislar en una carpeta `DIAG-<tema>-<UTC>/` con ensayos en memoria, sin guardar `.blend`.
3. Cambiar una sola cosa por ensayo (orden, agrupación de operandos, solape). Registrar qué falló y qué no.
4. Documentar solo lo observado. Nada de "causa raíz" sin evidencia.
5. Detenerse si el validador falla: no encadenar más variantes sobre un resultado FAIL.

Detalle: `experimentos/EXP-BPY-006/reports/CIERRE_ADITIVO_20261102.md` y las cinco carpetas `EXP-BPY-006-GN-*`.
