# INV-05 — Persistencia de edición y estado
**Fecha de investigación:** 2026-11-02 (fecha de sesión; consulta web en esta sesión).  
**Responsable/agente:** estado_observabilidad.  
**Estado:** finalizado documentalmente; selección y pruebas IN PROGRESS.

## Pregunta investigada
¿Qué capacidades existentes permiten editar el patrón del CU-01, conservar requisitos y recuperar un estado anterior sin desarrollar un sistema de modelado nuevo?

Se leyeron README, los cinco documentos de `documentos/`, el plan y la plantilla. No se instaló software, ejecutó Blender ni realizó prueba propia. Las páginas `latest`, `dev`, repositorios y resultados indexados son evidencia temporal, no una versión instalada. Algunos accesos directos al manual devolvieron error de recuperación; se contrastaron extractos indexados de páginas oficiales versionadas. No se afirma haber inspeccionado un `.blend` real.

## Evidencia
**Alcance de lectura de las filas:** las fuentes Blender de esta tabla se leyeron mediante extractos indexados oficiales (incluidos requisitos, licencia e issues), no mediante descarga completa. Por tanto, el tipo de todas esas filas debe interpretarse como **documentación primaria/issue, acceso parcial**. “Alta” califica la afirmación concreta visible en el extracto, no una revisión completa de página, release ni implementación. “Verificado documentalmente” nunca significa probado.
| Afirmación | Fuente/URL | Fecha/versión | Tipo de evidencia | Confianza |
|---|---|---|---|---|
| Geometry Nodes modifica geometría mediante grupos conectados a un modificador | [Introducción GN](https://docs.blender.org/manual/en/4.3/modeling/geometry_nodes/introduction.html) | Manual 4.3; consulta 2026-11-02 | Documentación primaria, acceso parcial indexado | Alta para mecanismo; no prueba CU-01 |
| Modificadores conservan geometría base; aplicar fija el resultado; el orden afecta la salida | [Modificadores](https://docs.staging.blender.org/manual/en/latest/modeling/modifiers/introduction.html) | Página staging rotulada 5.2 LTS; consulta 2026-11-02 | Documentación primaria, acceso parcial indexado | Alta mecanismo; media versión |
| Cada modificador puede tener valores propios de entradas de un grupo compartido | [Geometry Nodes Modifier](https://docs.blender.org/manual/id/5.1/modeling/modifiers/geometry_nodes.html) | Manual 5.1; consulta 2026-11-02 | Documentación primaria, acceso parcial indexado | Alta |
| Custom properties almacenan datos en data-blocks; admiten tipos simples y acceso Python | [Custom Properties](https://docs.blender.org/manual/sl/4.5/files/custom_properties.html) | Manual 4.5 LTS; consulta 2026-11-02 | Documentación primaria, acceso parcial indexado | Alta |
| Realizar instancias convierte referencias en geometría y aumenta memoria/costo de procesamiento | [Instances](https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/instances.html) | Manual 4.5 LTS; consulta 2026-11-02 | Documentación primaria, acceso parcial indexado | Alta |
| Existen Save Incremental, Save As, Save Copy y recuperación | [Blender File](https://docs.blender.org/manual/sl/4.5/files/blend/index.html), [Recovering Data](https://docs.blender.org/manual/id/4.2/troubleshooting/recover.html) | Manuales 4.5/4.2; consulta 2026-11-02 | Documentación primaria, acceso parcial indexado | Alta |
| `.blend1`/`.blend2` son rotación de guardados; Auto Save escribe respaldos temporales | [Save & Load](https://docs.blender.org/UATEST/manual/en/dev/editors/preferences/save_load.html) | Página UATEST/dev rotulada 5.1; consulta 2026-11-02 | Documentación primaria, acceso parcial indexado; corroborada por Recovering Data | Media-alta |
| Empaquetar recursos incluye solo recursos elegibles; no todos los externos | [Packed Data](https://docs.blender.org/manual/de/4.5/files/blend/packed_data.html) | Manual 4.5 LTS; consulta 2026-11-02 | Documentación primaria, acceso parcial indexado | Alta |
| Crash al guardar asset GN con entrada menú sin conectar; reproducido y resuelto | [Issue #157947](https://projects.blender.org/blender/blender/issues/157947) | Linux, 5.2 Alpha `e3d8e8e05a83`; 2026-04-29; cerrado; consulta 2026-11-02 | Issue, acceso parcial indexado; experiencia externa | Alta existencia; no generalizable a estable/ARM |
| Archivo de GN con subtipo Pixel de 5.2 provocaba crash al abrir en 5.1.2 | [Issue #160212](https://projects.blender.org/blender/blender/issues/160212) | 5.2 Beta `2a1ca5553bac`; 2026-06-16; cerrado; consulta 2026-11-02 | Issue, acceso parcial indexado; experiencia externa | Alta caso concreto |
| Apple Silicon es plataforma soportada; GPL es licencia del software | [Requisitos](https://www.blender.org/download/requirements/), [Licencia](https://www.blender.org/about/license/), [Comunidad](https://www.blender.org/about/) | Páginas sin versión fija; consulta 2026-11-02 | Documentación primaria/declarado por proyecto, acceso parcial indexado | Alta |

## Capacidades confirmadas y limitaciones

| Reutilizable hoy según documentación | Límite | Propuesta del laboratorio, todavía no implementada |
|---|---|---|
| Malla base + modificadores | Aplicar la pila elimina esa vía de edición paramétrica; orden importa | Conservar maestro editable y generar derivado de exportación |
| GN con entradas expuestas | Un grafo no impone por sí mismo los requisitos de negocio | Exponer ancho/alto/espaciado/profundidad del ladrillo; separar parámetros del cuerpo |
| Custom properties | No son esquema validado, historial ni bloqueo de invariantes | Guardar identificador lógico, versión de contrato y rol; contrato completo con evidencia fuera del modelo |
| Guardado `.blend`, Save Copy/Incremental | Guardar no acredita geometría válida; recursos externos pueden faltar | Snapshot nombrado por revisión y operación, vinculado a resultados de validación |
| Undo, autosave, backups rotativos | No son una transacción entre MCP, escena y registro externo; rotación no conserva necesariamente el último estado aceptado | Restaurar snapshot aceptado y verificar reapertura antes de continuar |

No se encontró en estas capacidades un protocolo nativo de “cambio aceptado contra CON-001”. Esa coordinación es brecha de procedimiento, no razón suficiente para crear un servicio. Un archivo `.blend` conserva la representación editable; un STL debe tratarse como salida, no como repositorio del grafo y sus parámetros. Realizar instancias no une sólidos automáticamente ni demuestra manifoldness: comprobar unión física y topología en VAL-001.

Convenciones propuestas: roles `cuerpo`, `patron`, `exportacion`; identificadores lógicos persistentes distintos del nombre visible; unidades explícitas; versión del grafo, Blender y contrato. La unicidad de identificadores tras duplicar objetos requiere comprobación propia. No atribuir esta convención a Blender ni a MCP.

## Compatibilidad Codex / macOS Apple Silicon
Blender publica soporte Apple Silicon y mínimo soportado macOS 13 en su [página de requisitos](https://www.blender.org/download/requirements/). Las [notas de compatibilidad](https://developer.blender.org/docs/release_notes/compatibility/) diferencian soporte oficial y ejecutabilidad anterior, señalando 5.3 como endurecimiento del mínimo; por prudencia usar requisitos soportados y fijar release concreta después. No se inspeccionó macOS ni Blender local.

GN, custom properties y guardado son capacidades Blender, independientes del cliente Codex. Su operación por Codex requiere herramientas de inspección/edición y permisos que INV-01 debe confirmar. **Compatibilidad integral Codex → MCP → guardado/restauración en ARM64: pendiente de probar**. No extrapolar soporte de Blender a addons, dependencias Python o restablecimiento de conexión tras abrir un archivo.

## Comunidad y mantenimiento
Blender es proyecto comunitario coordinado por Blender Foundation, según su página institucional. Los issues enlazados muestran reportes reproducibles, interacción de mantenedores y cierres; no miden tasa de fiabilidad del CU-01. La [actividad pública](https://projects.blender.org/blender/blender/activity) registra cambios de octubre de 2026. No se hizo censo de issues ni se ofrece SLA.

Licencia: Blender GPL, con detalles de componentes en su página de licencia. Uso local sin costo de licencia; siguen existiendo costos de memoria, almacenamiento, tiempo de modelado y uso de Codex. Estas capacidades nativas no requieren Docker, nube, assets comerciales ni addon adicional. El puente MCP tiene sus dependencias/licencia propias (INV-01). No se cotizaron planes de Codex.

## Aplicación al CU-01
**Propuesta:** cuerpo paramétrico separado de patrón GN editable; maestro `.blend` conservado. “Ladrillos más pequeños” modifica distribución/tamaño del patrón, no escala del objeto completo. Las dimensiones exteriores **150 × 150 × 60 mm** deben medirse sobre geometría evaluada que incluya el relieve. Si ese criterio requiere reinterpretar una medida previa del cuerpo, resolverlo en CON-001 antes de aceptar modelo.

Invariantes: envolvente exterior, cuatro caras con relieve físico, continuidad en esquinas y persistencia de parámetros. Espesor (**2 o 20 mm**), base y drenaje continúan pendientes; no crear una supuesta revisión “válida final” inventándolos. Presencia de nodos no demuestra exportación del relieve. Verificar malla evaluada y STL con VAL-001; comprobar Creality Print por separado.

## Riesgos y preguntas abiertas
- Recursos externos, grupos compartidos y data-blocks vinculados pueden hacer que copia de escena no sea aislamiento suficiente. Elegir snapshot de archivo con dependencias conocidas.
- GN puede producir instancias o piezas separadas; no confundir visualización correcta con una carcasa fabricable.
- Guardado con versión nueva y apertura con antigua no garantiza compatibilidad; fijar versión y conservar original previo a migrar.
- Timeout después de guardar/cambiar deja resultado incierto: inspeccionar escena y archivo, no repetir creación ciegamente.
- ¿Reapertura conserva el servidor/addon y referencias? ¿Qué evidencia acredita restauración? Pendiente experimental.
- Tolerancias dimensionales y política de retención de snapshots necesitan acuerdo en CON/VAL; no se fijan arbitrariamente aquí.

## Recomendación y próximos experimentos (sin ejecutarlos)
**Reutilizar** GN/modificadores, custom properties y guardados nativos; confianza alta en su existencia, media en adecuación al CU-01. **Experimentar** con un procedimiento simple de snapshots y registro asociado, antes de programar transacciones o gestores propios. **Descartar como única recuperación** autosave/Undo y como prueba de aceptación el mero éxito de una herramienta.

1. En futura fase autorizada, crear CU-01 tras resolver espesor/base/drenaje; guardar y reabrir maestro con parámetros y versiones registrados.
2. Reducir ladrillos; comprobar dimensiones evaluadas, cuatro caras, esquinas y editabilidad tras reapertura.
3. Exportar derivado y verificar relieve, unidades, malla y laminado sin destruir el maestro.
4. Introducir cambio inválido controlado; restaurar snapshot y comparar invariantes, parámetros y evidencia previa. Probar también caída/desconexión y recursos faltantes.
5. Medir tamaño de snapshots, tiempos de guardado/restauración y memoria al realizar instancias. Adoptar mecanismo solo tras prueba reproducible en Apple Silicon/Codex.
