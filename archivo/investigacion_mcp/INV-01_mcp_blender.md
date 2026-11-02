# INV-01 — MCP for Blender y alternativas
**Fecha de investigación:** 2026-11-02 (fecha de sesión; consulta documental web).
**Responsable/agente:** Codex / mcp_skills.
**Estado:** finalizado (investigación documental); adopción e integración IN PROGRESS.

## Pregunta investigada

¿Qué integración permite a Codex inspeccionar y editar Blender para CU-01, con evidencia suficiente para un experimento posterior en macOS ARM64?

## Evidencia

Todas las fuentes se consultaron el 2026-11-02. Las ramas `main` y páginas web son mutables; no constituyen una captura histórica inmutable. Se intentó consultar commits por GitHub/API, pero no se recuperó un SHA verificable. Las versiones siguientes proceden de manifiestos, no de una instalación ni de una release comprobada.

| Afirmación | Fuente/URL | Fecha/versión | Tipo de evidencia | Confianza |
|---|---|---|---|---|
| `ahujasid/blender-mcp` redirige a `ahujasid/mcp-for-blender`; el mantenedor explica el cambio de nombre y el wrapper antiguo | [Repositorio](https://github.com/ahujasid/blender-mcp), [issue 366](https://github.com/ahujasid/mcp-for-blender/issues/366) | Anuncio 2026-09-16; 2.0.0 en anuncio | documentación primaria / código o issue | Alta para identidad; continuidad declarada, no probada |
| Paquete `mcp-for-blender` 2.2.6; Python ≥3.10; `mcp>=1.26.0,<2`, `httpx>=0.27.0` | [pyproject](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/pyproject.toml) | main consultada | código o issue | Alta documental |
| Licencia MIT | [LICENSE](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/LICENSE) | main; copyright 2025 | documentación primaria | Alta |
| Expone estado, inspección, ejecución Python, vistas e integración de assets | [server.py](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/src/blender_mcp/server.py) | main; sin SHA | código o issue | Alta sobre presencia; ejecución pendiente |
| Documenta Codex, Blender ≥3.0, Python ≥3.10 y uv; incluye telemetría mínima por defecto y contenido opt-in | [README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md) | main | documentación primaria (declarado por proyecto) | Media para compatibilidad real |
| Codex permite servidores STDIO y HTTP; configuración MCP por CLI o TOML | [OpenAI: MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) | Documentación consultada; sin versión fijada | documentación primaria | Alta documental |
| Reporte abierto de socket sin autenticación que ejecuta Python | [issue 404](https://github.com/ahujasid/mcp-for-blender/issues/404) | 2026-10-21; reporta 1.6.0 | código o issue / testimonio comunitario | Alta para existencia; no reproducido ni extrapolado a 2.2.6 |
| Ultra declara herramientas de modelado, nodos, impresión y STL; números de herramientas inconsistentes | [README Ultra](https://raw.githubusercontent.com/carlosh7/blender-mcp/main/README.md) | main | documentación primaria (claim) | Media; no valida calidad |
| Ultra 3.2.0, MIT, Python ≥3.10; depende de MCP, requests, PyYAML y NumPy | [pyproject Ultra](https://raw.githubusercontent.com/carlosh7/blender-mcp/main/pyproject.toml) | main | código o issue | Alta documental |
| Blender AI Agent propone planificación, revisión visual, rollback y GLB/MP4; se declara experimental | [README AI Agent](https://raw.githubusercontent.com/ahmedsayed1911/Blender-AI-Agent/main/README.md) | main; versión desconocida | documentación primaria (claim) | Media |
| AI Agent muestra licencia GPL-3.0 y dependencias externas MCP/FastMCP | [Repositorio](https://github.com/ahmedsayed1911/Blender-AI-Agent), [requirements](https://raw.githubusercontent.com/ahmedsayed1911/Blender-AI-Agent/main/requirements.txt) | main | documentación primaria / código o issue | Alta documental |

**Pruebas propias:** ninguna. **Verificado documentalmente** significa que se leyó la fuente, no que funcionó en el Mac del laboratorio. Los testimonios no equivalen a auditorías independientes.

## Capacidades confirmadas y limitaciones

En `server.py` se observan `get_addon_status`, `get_scene_info`, `execute_blender_code`, `look`, `search_assets`, `import_asset` y `generate_3d`. Python se envía al Blender vivo; permite plantear cambios incrementales mediante `bpy`/`bmesh`. El servidor utiliza socket, por defecto localhost:9876. Algunas herramientas de UI se filtran según capacidades del cliente. Esto no demuestra que todas las interfaces de Codex reciban la misma experiencia visual. [Código](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/src/blender_mcp/server.py).

La edición paramétrica, restauración fiable y cumplimiento de invariantes deben diseñarse y probarse. Ejecutar Python puede crear geometría o exportar mediante Blender, pero no prueba que el resultado sea manifold, dimensionalmente correcto o imprimible. No se encontró una demostración reproducida por nosotros del CU-01.

Ultra merece comparación puntual: su README menciona 239 y 248 herramientas, mientras la descripción del repositorio dice 223. No utilizar un recuento como criterio de superioridad. Sus imágenes de escenas y Geometry Nodes son demos del autor, no ensayos FDM. AI Agent se orienta a generación procedural, animación y estudio web; no acredita aquí un flujo STL/K1C. [Ultra](https://github.com/carlosh7/blender-mcp), [AI Agent](https://raw.githubusercontent.com/ahmedsayed1911/Blender-AI-Agent/main/README.md).

## Compatibilidad Codex / macOS Apple Silicon

| Componente | Codex | macOS ARM64 |
|---|---|---|
| ahujasid | Receta explícita `codex mcp add blender -- uvx mcp-for-blender`; protocolo STDIO admitido oficialmente | README ofrece macOS; no se verificó matriz ARM64 ni ejecución local |
| Ultra | Declara cualquier cliente MCP/STDIO; integración concreta con Codex pendiente | Declara macOS y Blender ≥4.2; dependencias nativas y wheel ARM64 pendientes |
| AI Agent | Capa MCP descrita, pero no se verificó receta Codex directa | Desconocida; no se verificó combinación ARM64/Ollama/Qwen/Blender |

La compatibilidad del protocolo no certifica la del add-on, Python embebido, visor ni arquitectura. No se inspeccionó la instalación local. Docker no es necesario para plantear el experimento del candidato principal.

## Comunidad y mantenimiento

La página de ahujasid mostraba aproximadamente 33,1 mil estrellas, 3 mil forks y 32 issues abiertos; son indicadores mutables de difusión. Hay issues fechados en octubre de 2026, pero su existencia no prueba velocidad de resolución. [Repositorio](https://github.com/ahujasid/mcp-for-blender), [issues](https://github.com/ahujasid/mcp-for-blender/issues).

Los manifiestos 2.2.6 y 3.2.0 aportan referencias de versión; no se obtuvo último commit ni cadencia verificable para los tres proyectos. Ultra incluye documentación y CI en el repositorio; no se verificó su historial de ejecuciones. No se obtuvo evidencia comunitaria independiente de CU-01 para ninguna alternativa. Evitar traducir insignias, estrellas o claims de seguridad en estabilidad demostrada.

## Aplicación al CU-01

Propuesta: inspeccionar escena y estado del add-on; construir cuerpo y patrón con parámetros persistentes; cambiar únicamente el tamaño de los ladrillos; comprobar volumen exterior final de 150×150×60 mm, incluidas esquinas y relieve. Guardar `.blend` antes/después y validar STL con la estrategia de INV-03/04 y VAL-001. Es una hipótesis de uso, no un resultado observado. Pared, base y drenaje permanecen pendientes; no elegir entre 2 y 20 mm.

## Riesgos y preguntas abiertas

- Ejecución Python amplia y reporte de socket sin autenticación: comprobar alcance y mitigaciones en la versión fijada antes del prototipo; el issue 404 se refiere a 1.6.0, no prueba automáticamente un fallo actual.
- El README distingue telemetría mínima de uso y telemetría de contenido. Para un experimento local propone desactivación completa con `DISABLE_TELEMETRY=true`; no se cambió configuración. [README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md).
- Costos: licencia abierta no elimina consumo de Codex ni posibles cargos de generación externa. `generate_3d` advierte costo por llamada; CU-01 no requiere esos proveedores. Tarifas no investigadas. [Código](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/src/blender_mcp/server.py).
- Un timeout deja incierto el estado; no repetir mutaciones sin inspección. Una imagen correcta no acredita medidas o malla.
- Versiones y fechas recuperadas pueden depender del índice/caché; no se atribuye actividad posterior al 2026-11-02 ni se inventa un commit.

## Recomendación y próximos experimentos (sin ejecutarlos)

**Experimentar primero con ahujasid**: confianza alta en existencia e integración documentada; media en ajuste arquitectónico; compatibilidad práctica ARM64 y CU-01 pendientes. Reutilizar el transporte antes de escribir otro puente.

1. Fijar release/commit y versiones de Blender, Python, uv y Codex; revisar add-on y dependencias del artefacto exacto.
2. Probar conexión, inventario y vista sobre escena desechable; registrar herramientas realmente expuestas.
3. Crear y modificar patrón paramétrico con invariantes; verificar por separado restauración y estado tras timeout.
4. Validar/exportar CU-01 una vez aclarados parámetros; comparar Ultra únicamente si aparece una brecha concreta.
5. Mantener AI Agent como referencia de diseño de revisiones/rollback, sin incorporarlo al stack inicial por ahora (confianza media).
