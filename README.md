# Laboratorio de Modelado 3D Agéntico

**Estado (2026-11-03):** Fase 1 **cerrada por decisión del responsable, con excepción dimensional documentada** (ADR-0003; no se midió la pieza física, y eso no equivale a cumplir el criterio). Flujo digital demostrado en un proxy (80×60×5 mm) con Blender 5.4.0 Alpha: crear, editar, validar, snapshot, STL y laminado en Creality Print. Impresión física del proxy hecha, con inspección visual favorable y sin medición dimensional. CU-01 (macetero 150 × 150 × 60 mm): hay tres revisiones digitales con PASS (paredes de 20, 10 y 5 mm), un soporte para sensor SHT31 y dos variantes de color; ninguna se ha exportado a STL ni impreso (ver [`docs/06_estado/ESTADO_FASES.md`](docs/06_estado/ESTADO_FASES.md)).

**Entorno:** MacBook Apple Silicon, Codex, Blender (ejecución directa con `bpy`), Creality Print, Creality K1C, PLA, boquilla 0,4 mm.

## Dónde mirar

- **Estado vigente:** [`docs/06_estado/ESTADO_FASES.md`](docs/06_estado/ESTADO_FASES.md)
- **Arquitectura:** [`docs/02_arquitectura/ARQ.md`](docs/02_arquitectura/ARQ.md)
- **Qué está probado y qué no:** [`docs/03_contratos/TRAZABILIDAD.md`](docs/03_contratos/TRAZABILIDAD.md)
- **Procedimientos:** [`docs/04_procedimientos/`](docs/04_procedimientos/) (ejecución de Blender, integridad, Creality)
- **Decisiones:** [`docs/05_decisiones/`](docs/05_decisiones/)
- **Índice de la documentación:** [`docs/README.md`](docs/README.md)
- **Evidencia:** [`experimentos/INDEX.md`](experimentos/INDEX.md) y [`investigacion/incidentes/INDEX.md`](investigacion/incidentes/INDEX.md)
- **Histórico:** `archivo/` (investigación con MCP y documentos originales, sin cambios)

## Reglas

1. Los informes históricos no se reescriben; las correcciones van en [`docs/06_estado/ERRATAS.md`](docs/06_estado/ERRATAS.md).
2. Todo hash y tamaño lo calcula `herramientas/sellar_artefacto.py`; nunca se teclean ([INTEGRIDAD](docs/04_procedimientos/INTEGRIDAD.md)).
3. Se escribe siempre un archivo nuevo; no se sobrescriben revisiones aceptadas ni proyectos que una aplicación pueda guardar.
4. Distinguir hipótesis, protocolo preparado, experimento ejecutado e incidente.
5. Un PASS digital no equivale a una pieza imprimible ni a CU-01.
6. No exponer claves, credenciales ni datos privados.

## Próximo paso

EXP-BPY-006 quedó INCONCLUSIVE: `bpy` regenerando la geometría pasó, Geometry Nodes falló en la única variante medida y la edición in-place no se ejecutó (ver `experimentos/EXP-BPY-006/reports/CIERRE_ADITIVO_20261102.md`). Para CU-01 falta elegir la revisión y el drenaje, exportar a STL, imprimir y medir la pieza; la medición física es exigible.

## Material predeterminado para modelos nuevos

Los modelos de producto nuevos usan `herramientas/hyper_pla_marmol.py` por defecto, salvo indicación distinta del responsable. Desde un generador `bpy`, importa `aplicar_material_por_defecto(obj)` y llámalo después de crear la malla. El material procedural replica el acabado blanco con motas negras y grises de la variante PLA marmoleada; solo modifica apariencia. Los experimentos y revisiones históricas permanecen intactos.
