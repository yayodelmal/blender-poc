# INV-02 — Skills Blender para Codex
**Fecha de investigación:** 2026-11-02 (fecha de sesión; consulta documental web).
**Responsable/agente:** Codex / mcp_skills.
**Estado:** finalizado (investigación documental); selección y validación práctica IN PROGRESS.

## Pregunta investigada

¿Existen skills reutilizables para el modelado editable y revisión del CU-01, compatibles documentalmente con Codex y plausibles en macOS ARM64, sin confundir instrucciones, scripts y herramientas MCP?

## Evidencia

Fuentes consultadas el 2026-11-02. Se leyó `main`, no una versión inmutable: la consulta del historial no permitió recuperar SHA. Las fechas y versiones se atribuyen al proyecto; no se presume que una declaración de pruebas sea una ejecución independiente.

| Afirmación | Fuente/URL | Fecha/versión | Tipo de evidencia | Confianza |
|---|---|---|---|---|
| Existe EL4CTEO/blender-skills; declara 28 skills, Codex y Blender 5.2+ | [README](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/README.md) | main consultada | documentación primaria (claim del autor) | Alta para existencia; media para funcionamiento |
| Licencia MIT | [LICENSE](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/LICENSE) | Copyright 2026 | documentación primaria | Alta |
| Changelog 1.2.0 y declaración de verificación en Blender 5.2.3 | [CHANGELOG](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/CHANGELOG.md) | 2026-10-30 | documentación primaria (claim) | Alta sobre declaración; prueba no repetida |
| Las cinco skills propuestas existen y llevan metadato 1.2.0 | [core](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-core/SKILL.md), [scene-setup](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-scene-setup/SKILL.md), [hardsurface](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-hardsurface-modeling/SKILL.md), [geometry-nodes](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-geometry-nodes/SKILL.md), [asset-qa](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-asset-qa/SKILL.md) | main; metadata 1.2.0 | documentación primaria | Alta documental |
| QA implementa perfiles `game`, `render`, `print`, `roblox`; el perfil print eleva bordes abiertos/no manifold a error | [qa_check.py](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-asset-qa/scripts/qa_check.py) | main | código o issue | Alta para presencia de código; eficacia pendiente |
| Codex reconoce SKILL.md, instrucciones/recursos/scripts y rutas `.agents/skills` de repositorio y usuario | [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) | Documentación consultada | documentación primaria | Alta documental |
| Instalador tiene destino Codex y selección `--skills`; reemplaza destinos homónimos | [install.sh](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/install/install.sh) | main | código o issue | Alta por lectura; no ejecutado |
| Hay wrapper headless con detección de Blender en macOS y Python host ≥3.9 declarado | [run_in_blender.py](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-core/scripts/run_in_blender.py) | main | código o issue | Alta para ruta macOS; ARM64 no probado |
| El autor publica comparación con/sin skills de cinco tareas y especifica modelo/Blender | [Comparación](https://el4cteo.github.io/blender-skills/comparison/) | Página consultada; sin fecha fijada | documentación primaria (demo del autor) | Media; no benchmark independiente |

**Pruebas propias:** ninguna. **Experiencia comunitaria:** no se obtuvo una reproducción externa verificable de Codex + Apple Silicon + CU-01. La comparación del autor no se clasifica como testimonio independiente.

## Capacidades confirmadas y limitaciones

| Skill | Contenido verificado | Utilidad propuesta y límite |
|---|---|---|
| `blender-core` | Ruta MCP mediante `execute_blender_code`, ejecución headless, reporte de entorno y reglas de API | Orquestación y diagnóstico; no es otro agente ni instala un MCP por sí sola |
| `blender-scene-setup` | Auditoría, unidades métricas/escala 1, nombres y colecciones | Base de trazabilidad; aplicar escalas y purgar requiere revisar efectos sobre modelo editable |
| `blender-hardsurface-modeling` | Booleans, bevels, pila de modificadores y copia de exportación | Útil para cuerpo y relieve; sus normal maps/decals y floaters para baking no satisfacen geometría FDM |
| `blender-geometry-nodes` | Constructor JSON de nodos, inspección de sockets e inputs de modificador | Candidato para ladrillos paramétricos; no trae demostración de continuidad del macetero |
| `blender-asset-qa` | Revisión numérica/visual y perfil print | Reutilizable como control parcial; no certifica PLA/K1C/boquilla ni cumplimiento de CON-001 |

Fuentes de cada fila: los cinco `SKILL.md` enlazados en la tabla de evidencia.

El código de QA usa `bpy`, `bmesh`, BVH/KDTree y puede analizar malla evaluada con modificadores en coordenadas mundiales. Define tolerancias `eps=0.001`, `tol=0.002` y criterios por perfil. Hay que calibrar su significado en las unidades elegidas y comprobar falsos positivos/negativos: proximidad de piezas no demuestra unión fabricable. El conjunto examinado no demuestra medición de pared mínima, alcance completo de autointersecciones ni restricciones del laminador. [Código QA](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-asset-qa/scripts/qa_check.py).

Además, la skill QA sugiere separar superficies 2–5 mm para ciertos problemas visuales. Esa corrección puede violar dimensiones o continuidad del CU-01; no trasladarla automáticamente al contrato de fabricación. [Skill QA](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/skills/blender-asset-qa/SKILL.md).

Los otros candidatos de [INV-01](INV-01_mcp_blender.md) son servidores/pipelines, no sustitutos equivalentes de estas skills: Ultra agrega herramientas y guía integrada; AI Agent añade su propia planificación y revisión. No hay evidencia que justifique incorporar ambos al stack inicial.

## Compatibilidad Codex / macOS Apple Silicon

**Codex: compatibilidad documental favorable.** El formato de las skills coincide con el mecanismo oficial: metadatos `name`/`description`, carga de instrucciones cuando se seleccionan y recursos opcionales. Codex soporta `.agents/skills` y symlinks; el instalador del proyecto apunta a esas rutas. Esto acredita descubrimiento previsto, no resultados correctos de los scripts. [OpenAI](https://learn.chatgpt.com/docs/build-skills), [instalador](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/install/install.sh).

**Apple Silicon: sin verificación integral.** Markdown es independiente de arquitectura; el wrapper contempla `darwin` y rutas `/Applications/Blender*.app`. No se verificaron pruebas CI ARM64, arquitectura del binario ni todas las dependencias. El requisito documentado Blender 5.2+ es más restrictivo que el mínimo declarado por el MCP de ahujasid: elegir la versión común exige prueba. No se inspeccionó ni modificó el Blender local.

## Comunidad y mantenimiento

La página del repositorio mostraba 657 estrellas, 65 forks y ocho commits; el listado de issues abiertos mostraba cero. Son observaciones mutables, no indicadores suficientes de madurez o ausencia de fallos. [Repositorio](https://github.com/EL4CTEO/blender-skills), [issues](https://github.com/EL4CTEO/blender-skills/issues).

El changelog presenta entradas 0.1.0 (2026-10-14), 1.1.0 (2026-10-16) y 1.2.0 (2026-10-30). Indica desarrollo reciente según el autor; no se comprobó cadencia sostenida. El README declara 67 tests headless; no se ejecutaron ni se verificaron logs CI. [Changelog](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/CHANGELOG.md), [README](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/README.md).

La comparación publicada usa Opus 5.5 (medium), Blender 5.2 y una ejecución por tarea, según la página. Ilustra paredes PBR, simulación y assets animados; no demuestra resultados con Codex, repetibilidad estadística o impresión del macetero. [Demo](https://el4cteo.github.io/blender-skills/comparison/).

## Aplicación al CU-01

Propuesta de reutilización: `core` para entorno; `scene-setup` para escala/nombres; `hardsurface` para sólido editable; `geometry-nodes` para patrón; `asset-qa` perfil print para una parte de VAL-001. Mantener las medidas finales 150×150×60 mm como verificación independiente y medir el modelo evaluado después de reducir ladrillos. Las instancias deben materializarse cuando lo requiera la exportación, preservando el original paramétrico.

No incorporar recomendaciones de texturizado como sustitución de ladrillos reales. Las paredes de 2 o 20 mm, base y drenaje siguen pendientes. Guardar evidencia de esquinas, dimensiones y STL, además de imágenes.

## Riesgos y preguntas abiertas

- `install.sh` elimina la carpeta de destino de cada skill antes de crear symlink o copia. Antes de una eventual instalación, revisar colisiones y fijar alcance reducido; no se ejecutó el instalador. [Código](https://raw.githubusercontent.com/EL4CTEO/blender-skills/main/install/install.sh).
- Las instrucciones se diseñaron principalmente para assets visuales; QA no equivale a contrato dimensional ni validación completa FDM.
- Adaptar instrucciones puede ser suficiente; no escribir un nuevo framework antes de medir brechas. Revisar scripts auxiliares y APIs exactas de Blender en la versión fijada.
- Licencia MIT verificada; costos del agente y recursos de render/ejecución siguen existiendo. No se verificaron precios ni benchmark de consumo.
- Versiones y fechas son observaciones de fuentes actuales/caché. No se obtuvo SHA ni evidencia de soporte ARM64; no extrapolar fechas futuras ni historial inexistente.

## Recomendación y próximos experimentos (sin ejecutarlos)

**Reutilizar selectivamente y experimentar con las cinco skills**: confianza alta en existencia y contenido, media en adecuación al CU-01, funcionamiento local pendiente. Mantener Fase 1/Fase 2 IN PROGRESS hasta pruebas y contratos.

1. Fijar commit y revisar dependencias de las cinco skills antes de decidir instalación de alcance proyecto.
2. Medir descubrimiento explícito en Codex y una llamada de inspección; comprobar imports y resultados estructurados mediante MCP.
3. Ensayar QA con mallas conocidas: válida, abierta, normales invertidas, piezas próximas sin unión, pared demasiado fina y dimensión equivocada. Identificar qué casos no detecta.
4. Comparar CU-01 con/sin skills usando mismo modelo, requisitos y versiones; registrar invariantes, reintentos, tiempo y validaciones.
5. Adaptar únicamente las recomendaciones que contradigan el contrato FDM; mantener un validador independiente para medidas, pared y STL. No promover la demo visual del autor como aprobación del laboratorio.
