# Plan de investigación agéntica — Backlog inicial

**Modo:** solo investigación, documentación y propuestas; sin instalaciones ni cambios de código. Cada tarea entrega un Markdown independiente con fuentes y fecha de consulta.

| ID | Prioridad | Tarea | Insumos | Entregable | Dependencias |
|---|---|---|---|---|---|
| INV-01 | Alta | Verificar MCP for Blender de ahujasid: herramientas reales, soporte Codex, edición iterativa, límites, mantenimiento y comunidad | META, ARQ | `INV-01_mcp_blender.md` | Ninguna |
| INV-02 | Alta | Investigar skills existentes para Blender/Codex, licencias, soporte ARM64, comunidad y ejemplos verificables | CAP | `INV-02_skills.md` | Ninguna |
| INV-03 | Alta | Verificar MCP Printable y otras alternativas de validación FDM; distinguir claims de funciones demostradas | FLU, CAP | `INV-03_validacion_fdm.md` | Ninguna |
| INV-04 | Alta | Investigar validadores de malla/topología/dimensiones y posibilidades de automatizar revisión en Creality Print | ARQ, FLU | `INV-04_validadores.md` | Ninguna |
| INV-05 | Media | Investigar persistencia de modelos editables: Geometry Nodes, modificadores, convenciones y snapshots/restauración | ARQ, FLU | `INV-05_edicion_estado.md` | Ninguna |
| INV-06 | Alta | Diseñar contrato CON-001: invariantes, parámetros, cambios, trazabilidad y estados, comparando formatos y soluciones existentes | META, ARQ, CAP | `CON-001_IN_PROGRESS.md` | INV-05 deseable |
| INV-07 | Alta | Diseñar VAL-001: pruebas de dimensiones, geometría real, malla, FDM, exportación y resultados inconclusos | FLU, ARQ | `VAL-001_IN_PROGRESS.md` | INV-03 e INV-04 deseables |
| INV-08 | Media | Investigar logging, categorización de errores, métricas y recuperación; reutilización frente a código nuevo | FLU | `INV-08_observabilidad.md` | Ninguna |
| SYN-01 | Alta | Consolidar matriz de decisión: comunidad, compatibilidad, capacidades, riesgos, brechas y arquitectura mínima | Todos los hallazgos | `SYN-01_decision_arquitectura.md` | INV-01 a INV-08 |
| SYN-02 | Alta | Revisar coherencia ARQ/CAP/FLU/CON/VAL y definir criterios de salida de Fase 2 | Todos | `SYN-02_cierre_fase2.md` | SYN-01, INV-06, INV-07 |

## Ejecución sugerida
- **Ola A, en paralelo:** INV-01, INV-02, INV-03, INV-04, INV-05, INV-08.
- **Ola B:** INV-06 e INV-07 usando hallazgos relevantes; pueden avanzar como borradores sin esperar todo.
- **Ola C:** SYN-01 y SYN-02; no cerrar fase con referencias no verificadas.

## Criterios de aceptación de cada tarea
- Fuente primaria enlazada, fecha de consulta, versión/commit si aplica.
- Evidencia separada en **verificado documentalmente**, **declarado por el proyecto**, **experiencia comunitaria** y **pendiente de probar**.
- Compatibilidad Codex y macOS ARM64 evaluada explícitamente; decir «desconocida» si no hay evidencia.
- Problemas abiertos, riesgos, costos y dependencias.
- Recomendación: reutilizar / experimentar / descartar, con nivel de confianza.
- No modificar el entorno local.

## CU-01 — Escenario común
Crear un macetero exterior de 150×150×60 mm; agregar ladrillos geométricos (no textura), modificarlos manteniendo medidas, validar malla, exportar STL y revisar en Creality Print. **No asumir** espesor de pared ni drenaje. La evaluación documental no sustituye una prueba ejecutada.
