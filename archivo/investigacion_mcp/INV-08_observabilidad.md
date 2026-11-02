# INV-08 — Observabilidad, errores y recuperación
**Fecha de investigación:** 2026-11-02 (fecha de sesión; fuentes consultadas durante esta sesión).  
**Responsable/agente:** estado_observabilidad.  
**Estado:** finalizado documentalmente; decisiones y validación IN PROGRESS.

## Pregunta investigada
¿Cuánto del registro y diagnóstico de FLU-001 puede reutilizarse de Blender, MCP for Blender y Codex, y qué falta para distinguir ejecución exitosa, modelo válido y recuperación comprobada?

Insumos: README, todos los documentos base, plan y plantilla; [INV-05](INV-05_edicion_estado.md). Investigación de lectura y web, **sin pruebas propias**, configuración, instalaciones ni ejecución de Blender. Se utilizó la skill OpenAI Docs para consultar fuentes oficiales de Codex; no se inspeccionaron credenciales ni historiales locales. La búsqueda de archivos de documentación Codex en el proyecto no encontró material aplicable.

## Evidencia
Todas las filas fueron consultadas el 2026-11-02. `main` y páginas actuales son referencias móviles: no se obtuvo SHA del puente ni se identificó versión instalada. El acceso al índice GitHub de issues por `timeout` falló; no se infiere ausencia de problemas. Las tres filas de Blender (CLI, recuperación e issue) son **fuente primaria, acceso parcial mediante extracto indexado**. MCP y Codex se abrieron y se leyeron sus secciones pertinentes; el código GitHub se abrió y se inspeccionaron fragmentos pertinentes, sin auditoría completa de archivos.

| Afirmación | Fuente/URL | Fecha/versión | Tipo de evidencia | Confianza |
|---|---|---|---|---|
| MCP define mensajes de logging, niveles y declaración de capacidad; persistir queda al cliente | [MCP Logging](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/logging) | Especificación 2025-06-18 | Documentación primaria, verificado documentalmente | Alta para protocolo; desconocida implementación concreta |
| Error de protocolo y error de herramienta son mecanismos distintos; la herramienta puede señalar `isError` | [MCP Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) | 2025-06-18 | Documentación primaria | Alta |
| En stdio, stdout pertenece al protocolo; stderr puede llevar logs y el cliente puede ignorarlos | [MCP Transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) | 2025-06-18 | Documentación primaria | Alta |
| Blender dispone de categorías, niveles y salida a archivo; sintaxis cambia entre versiones | [CLI 4.5](https://docs.blender.org/manual/nl/4.5/advanced/command_line/arguments.html), [CLI 5.1](https://docs.blender.org/manual/id/5.1/advanced/command_line/arguments.html) | Manuales 4.5 LTS/5.1 | Documentación primaria | Alta existencia; comprobar release concreta |
| El puente configura logger con fecha/nombre/nivel, registra conexión/errores y convierte ciertos errores de ejecución en texto | [server.py](https://github.com/ahujasid/mcp-for-blender/blob/main/src/blender_mcp/server.py) | `main`, SHA no fijado | Código leído, no ejecutado | Alta código visible; media comportamiento integral |
| Existe registro local opt-in `BLENDER_MCP_CONTEXT_LOG`, nombres/tamaños sin contenido | [context_log.py](https://github.com/ahujasid/mcp-for-blender/blob/main/src/blender_mcp/context_log.py) | `main`; página indexada unas tres semanas antes de consulta | Código/documentación interna | Alta existencia; pendiente prueba |
| Decoradores incluyen duración, éxito/error y trayectoria antes/después; fallos de snapshot/registro no necesariamente interrumpen la operación | [telemetry_decorator.py](https://github.com/ahujasid/mcp-for-blender/blob/main/src/blender_mcp/telemetry_decorator.py) | `main`, SHA no fijado | Código leído | Alta existencia; alcance/activación pendiente |
| Codex CLI no interactivo emite JSONL con eventos de turnos, items y llamadas MCP | [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) | Página actual sin versión CLI fijada | Documentación primaria | Alta documental; sin prueba app/CLI |
| Codex ofrece exportación OTel opt-in y eventos de herramienta; no está habilitada por defecto | [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) | Página actual sin versión fija | Documentación primaria | Alta documental |
| Guardados y recuperación son mecanismos nativos, separados del log | [Recovering Data](https://docs.blender.org/manual/id/4.2/troubleshooting/recover.html) | Manual 4.2 LTS | Documentación primaria | Alta |
| Un fallo de guardado GN tuvo reproducción externa y corrección | [Blender #157947](https://projects.blender.org/blender/blender/issues/157947) | 5.2 Alpha; Linux; 2026-04-29; cerrado | Código o issue; experiencia comunitaria, no prueba propia | Alta caso puntual |

## Capacidades confirmadas y limitaciones

**Reutilización documentalmente respaldada:** logs Blender para diagnóstico interno; logger del puente para conexión y ejecución; registro local de contexto del puente para volumen de herramientas; eventos Codex CLI para secuencia del agente. MCP logging es una capacidad negociada, no una garantía de que cualquier servidor/cliente conserve archivo. Ninguna de estas capas acredita por sí sola dimensiones, relieve físico o FDM.

El archivo `context_log.py` declara escritura JSONL local en el directorio de datos BlenderMCP, con ruta específica para macOS bajo Application Support. Es opt-in y deliberadamente omite argumentos, código, prompts y resultados. Sirve para estudiar tamaños de contexto, no reconstruir el modelo ni demostrar aceptación. No se habilitó ni se leyó un registro local.

Los decoradores de telemetría/trajectory ya aportan instrumentación: conviene inspeccionarlos antes de construir duplicados. El código indica escrituras best effort y referencia Supabase; **no se recomienda activarlas todavía**: falta contrastar consentimiento, destino, retención y cobertura en la release elegida. Los snapshots de `world_state` no están acreditados como archivos `.blend` reabribles. No usar “trajectory” como sinónimo de rollback.

Codex `exec --json` documenta eventos `thread`, `turn`, `item` y errores, incluyendo llamadas MCP; el ejemplo oficial incluye consumo de tokens. Es una vía de captura para una futura prueba CLI, no evidencia de que la aplicación actual exponga idéntico archivo. `--output-schema` estructura la respuesta final, pero no certifica sus afirmaciones. Continuar una sesión conserva conversación; no restaura la escena de Blender.

OTel de Codex puede aportar duración, resultados y metadatos; exportar necesita un destino adicional. Mantenerlo como opción posterior, no requisito inicial. No adoptar Agents API ni un backend cloud solo para obtener registros de un laboratorio local.

### Taxonomía y recuperación propuestas para este laboratorio
La siguiente tabla es **propuesta propia derivada de FLU-001**, no funcionalidad nativa de MCP:

| Familia | Evidencia mínima | Decisión propuesta |
|---|---|---|
| INT | Solicitud y diferencia respecto de CON-001 | Reformular cambio; no aceptar geometría fuera de intención |
| EXE | Excepción, error de protocolo/herramienta o timeout | Si resultado incierto, inspeccionar escena y revisión antes de reintentar |
| GEO | Medición/topología/relieve que incumple | Conservar evidencia; corregir desde estado conocido o restaurar |
| FDM | Comprobación de fabricación o laminado fallida | Registrar perfil y criterio; distinguir fallo de malla de limitación de impresión |
| STA | Estado previo ausente, archivo no reabre o cambio ajeno sobrescrito | Detener promoción; recuperar revisión comprobable |
| VAL | Comprobador no disponible, error o dato insuficiente | Marcar inconcluso/no verificado; jamás convertirlo en pase |

Separar **resultado de ejecución** (`éxito/error/incierto`), **resultado por validación** (`pasa/falla/inconcluso/no ejecutada`) y **decisión** (`aceptar/corregir/restaurar/pendiente`). Un error textual del puente puede requerir inspección adicional aunque no exista `isError`; validar este caso en experimento. Una excepción capturada no prueba que ninguna mutación haya ocurrido.

Mínimo propuesto sin servicio nuevo: una ficha local por operación con identificador de ejecución y operación, fecha con zona horaria, solicitud, revisión del contrato, versiones de componentes, snapshot previo y candidato, intento, resultado técnico, verificaciones con mediciones/unidades/tolerancias y evidencia, decisión y duración. Vincular logs grandes por ruta, evitando copiarlos completos. El formato final pertenece a CON-001; Markdown sirve para la primera prueba manual y JSONL es candidato si se necesita cálculo. Versionar archivos no implica commits: este workspace no está inicializado como repositorio Git, según comprobación del orquestador.

El snapshot debe preceder una mutación importante. En un timeout, no reemitir creación o modificación a ciegas: primero reconciliar estado observado y esperado. Restaurar solo una revisión cuya validez esté documentada, luego volver a verificar. Limitar reintentos por operación y detenerse al repetir la misma causa sin nueva evidencia; cantidad exacta pendiente. Registrar fallo de restauración por separado del fallo original.

### Métricas propuestas, sin mediciones realizadas
| Métrica | Definición para no confundir ejecución con aceptación |
|---|---|
| Éxito al primer intento | Operaciones aceptadas con todas las verificaciones obligatorias concluyentes al primer intento / operaciones iniciadas elegibles; mostrar además excluidas/bloqueadas |
| Reintentos | Intentos adicionales por operación; informar también operaciones nunca aceptadas para evitar sesgo |
| Restauraciones | Restauraciones intentadas, completadas y verificadas; no contar solo llamada exitosa |
| Inconclusos | Verificaciones inconclusas / verificaciones requeridas, más no ejecutadas por separado |
| Tiempo hasta entrega | Desde requisitos confirmados hasta STL verificado y revisión Creality Print registrada; separar espera humana/cómputo |
| Recurrencia | Repeticiones de causa identificada, con versión/procedimiento; no agrupar únicamente por mensaje parecido |
| Uso/costo | Tokens observados si disponibles, duración y almacenamiento; no inventar costo monetario sin tarifa/modalidad |

Comparar el mismo CU-01, parámetros, criterios VAL, versiones y número de operaciones. Publicar tamaño de muestra; no interpretar una mejora de porcentaje si se omitieron verificaciones. Estas fórmulas no vienen implementadas por Blender/MCP/Codex.

## Compatibilidad Codex / macOS Apple Silicon
Blender [documenta Apple Silicon](https://www.blender.org/download/requirements/); véase INV-05 para diferencia entre soporte y compatibilidad de versiones. El módulo de contexto contempla explícitamente `darwin`, pero esto no prueba ejecución ARM64 del conjunto. Capturar texto/JSONL no exige por sí mismo librerías nativas nuevas; el servidor, addon y cliente sí necesitan validación conjunta.

Codex CLI y app deben evaluarse separadamente. La existencia documental de JSONL/OTel no demuestra permisos de archivos, transporte negociado ni captura de stderr en esta sesión. No se ejecutó un cliente ni se alteró configuración. El modo `exec` tiene condiciones propias de ejecución en repositorio según la documentación; no se inicializó Git ni se prepara una automatización aquí.

## Comunidad y mantenimiento
Blender dispone de documentación y tracker públicos; #157947 es evidencia de reporte/corrección real, no tasa de fallos ni prueba Apple Silicon. Los módulos del puente muestran instrumentación existente y cambios, pero páginas de `main` recuperadas en fechas distintas no forman una release reproducible. INV-01 debe fijar commit/versiones y comunidad del puente antes de adoptar capacidades. No se encontró en esta revisión un testimonio verificado de recuperación integral Codex/Blender/CU-01.

Licencia Blender: [GPL](https://www.blender.org/about/license/). La licencia y dependencias de la release MCP corresponden a INV-01; no se deduce permiso de redistribución de un fragmento visible. La especificación MCP es referencia de interoperabilidad, no un servicio ni licencia universal de sus implementaciones. No se añade código ni dependencia. Logs nativos no tienen costo de licencia adicional de Blender, pero consumen disco/tiempo; Codex depende de modalidad contratada, no cotizada. Exportación OTel añade destino/operación y posible costo; trayectoria remota puede añadir dependencia externa. No son necesarios para la primera prueba.

## Aplicación al CU-01
Operación ejemplo propuesta: reducir ladrillos manteniendo envolvente **150 × 150 × 60 mm**, cuatro caras con relieve físico, continuidad de esquinas y editabilidad. Registrar valores previos/nuevos del patrón y mediciones de geometría evaluada incluyendo relieve. Una captura visual es evidencia auxiliar; no demuestra medidas ni unión física. El STL y la revisión de Creality Print necesitan evidencias separadas.

Espesor **2 o 20 mm**, base y drenaje continúan pendientes. El registro debe distinguir requisito no confirmado de error de herramienta. No informar “modelo válido para imprimir” mientras los criterios obligatorios o las verificaciones no estén resueltos. Material PLA, K1C y boquilla 0,4 mm se conservan como contexto de fabricación, sin inventar parámetros de laminado.

## Riesgos y preguntas abiertas
- Correlación entre llamada Codex, socket del puente, escena y snapshot aún no probada; un timestamp aislado no identifica inequívocamente una operación.
- Retención, rotación, límites de tamaño, pérdida de logs al crash y timestamps con zona deben definirse. No confundir ausencia de error registrado con ausencia de fallo.
- El registro de contexto omite contenido; trayectoria puede capturarlo. Revisar campos y destino antes de activar, no copiar secretos ni datos personales innecesarios a reportes.
- Logs de éxito pueden describir solo retorno sin excepción. Validación geométrica/FDM sigue siendo tarea de VAL-001.
- Cambios humanos concurrentes requieren reconciliación: restaurar un snapshot viejo podría borrar cambios aceptados posteriores.
- La memoria de soluciones requiere evidencia reproducible y revisión; conservar logs no entrena automáticamente al modelo.

## Recomendación y próximos experimentos (sin ejecutarlos)
**Reutilizar**, confianza alta documental: diagnósticos Blender, logs del puente y eventos CLI cuando esa interfaz sea elegida. **Experimentar**, confianza media: registro local mínimo vinculado a snapshots y CON/VAL. **Posponer** OTel remoto, trajectory remota y base de conocimiento hasta demostrar necesidad y revisar configuración/licencia/costos. No desarrollar otro logger antes de comprobar los existentes.

1. En futura fase autorizada, fijar versiones y observar una operación válida, error Python controlado, pérdida de conexión y fallo geométrico sin excepción. Comparar eventos de cada capa.
2. Verificar si los errores de texto, `isError` y excepciones se distinguen en el cliente; comprobar que ningún éxito técnico promocione un modelo inválido.
3. Reabrir snapshot y validar restauración según INV-05, conservando evidencia del error y de la recuperación.
4. Repetir la misma modificación del CU-01 con criterios constantes; calcular métricas desde fichas antes de automatizar su agregación.
5. Promover una corrección a procedimiento/skill solo tras reproducción y validación; registrar también intentos fallidos, versiones y casos donde no aplica.
