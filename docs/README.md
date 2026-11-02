# docs/ — documentación vigente

Estado de la consolidación documental: **completa hasta el paso 8** (2026-11-02). Respaldo previo: `/Users/yayo/Projects/blender-poc-backup-20261102T172320Z/` (tar + SHA-256 de los 241 archivos originales; todos verificados idénticos después de las migraciones).

| Carpeta | Documento | Contenido |
|---|---|---|
| `01_vision/` | `META.md` | Visión, fases, CU-01 (decisión MCP sustituida por bpy) |
| `02_arquitectura/` | `ARQ.md` | Arquitectura vigente (bpy directo), diagrama y estado por componente |
| `03_contratos/` | `CON-001.md`, `VAL-001.md` | Contrato de diseño y estrategia de validación (copias literales; sin aprobar) |
| | `TRAZABILIDAD.md` | R → V → experimento, con estado real |
| `04_procedimientos/` | `EJECUCION_BLENDER.md` | Cómo ejecutar Blender en background |
| | `INTEGRIDAD.md` | Reglas de sellado y verificación (herramienta en `../herramientas/`) |
| | `CREALITY.md` | Uso de Creality Print |
| | `RECUPERACION_FLU-001.md` | Errores y recuperación (actualizado a bpy) |
| | `APRENDIZAJES.md` | L-001 a L-007 (copia literal; ver E-002 en ERRATAS) |
| | `INTEGRIDAD_INC-006_copia.md` | Diseño original de prevención (INC-006) |
| `05_decisiones/` | `ADR-0001`, `ADR-0002`, `ADR-0003` | bpy directo (aceptada, motivo por documentar); política de la Alpha (aceptada, opción C); cierre de Fase 1 con excepción dimensional (aceptada) |
| `06_estado/` | `ESTADO_FASES.md` | **Estado vigente** |
| | `RECONCILIACION_EXP-BPY-004.md`, `ERRATAS.md` | Notas sobre contradicciones; no reescriben informes |
| | `CIERRE_FASE_1_copia_2026-11-02.md` | Informe anterior (histórico) |

## Fuera de `docs/`

- `experimentos/` y `investigacion/incidentes/`: evidencia, sin mover. Cada uno tiene un `INDEX.md`.
- `archivo/documentos_originales/` y `archivo/investigacion_mcp/`: documentación e investigación anteriores, sin cambios. Los mapas de rutas antiguas están en `documentos/LEEME_MOVIDO.md` e `investigacion/LEEME_MOVIDO.md`.
- `herramientas/sellar_artefacto.py`: sellado y verificación de hashes.

## Cómo evitar pérdida de referencias

Los informes de experimentos y manifiestos solo citan rutas de `experimentos/` e `investigacion/incidentes/`, que no se movieron. Los mapas de migración listan cada ruta anterior con su ruta actual.
