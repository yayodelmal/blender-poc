# Laboratorio de Modelado 3D Agéntico

**Estado (2026-11-02):** Fase 1 **cerrada por decisión del responsable, con excepción dimensional documentada** (ADR-0003; no se midió la pieza física, y eso no equivale a cumplir el criterio). Flujo digital demostrado en un proxy (80×60×5 mm) con Blender 5.4.0 Alpha: crear, editar, validar, snapshot, STL y laminado en Creality Print. Impresión física del proxy hecha, con inspección visual favorable y sin medición dimensional. CU-01 (macetero) sin iniciar.

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

EXP-BPY-006: modificación paramétrica del patrón de ladrillos conservando dimensiones e invariantes (R06). CU-01 solo después, y necesita decisiones de pared, base y drenaje; allí la medición física vuelve a ser exigible.
