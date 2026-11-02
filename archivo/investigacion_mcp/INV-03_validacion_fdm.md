# INV-03 — Validación FDM y MCP Printable
**Fecha de investigación:** 2026-11-02 (consulta documental; sin prueba local).  
**Responsable/agente:** validacion.  
**Estado:** finalizado como investigación documental; adopción y validación experimental IN PROGRESS.

## Pregunta investigada

¿MCP Printable aporta una validación FDM reutilizable para CU-01 y qué alternativas evitan confundir una malla cerrada con una pieza imprimible?

Se leyeron README, los cinco documentos de `documentos/`, el plan y la plantilla. No se instaló software, ejecutó scripts de proyectos, inspeccionó la instalación de Blender ni generó geometría. **Pruebas propias: ninguna.** Las ramas `main` consultadas son referencias móviles; no se obtuvo SHA reproducible. Las fechas relativas del buscador no se interpretan como actividad del proyecto.

## Evidencia

| Afirmación | Fuente/URL | Fecha/versión | Tipo de evidencia | Confianza |
|---|---|---|---|---|
| Printable existe; anuncia conexión con Codex y backends Blender/OpenSCAD. Se presenta como alpha y dice haber sido usado en impresiones reales. Esto último es declaración del autor. | [Repositorio/README](https://github.com/AaronGoldsmith/mcp-printable) | Consulta 2026-11-02; README dice 0.1.x | Documentación primaria / declarado | Alta para existencia; baja para resultados físicos generalizables |
| El manifiesto declara 0.2.3, Python ≥3.10, MIT y dependencias MCP, Pillow, Trimesh y NumPy. Difiere del estado 0.1.x del README. | [pyproject.toml](https://raw.githubusercontent.com/AaronGoldsmith/mcp-printable/main/pyproject.toml) | main, 0.2.3 | Código | Alta |
| Existe servidor FastMCP y wrapper de `blender_validate`; ofrece HEALTH, OVERHANGS, THIN_WALLS y CLEARANCE. La inspección del wrapper no demuestra precisión de los algoritmos. | [server.py](https://raw.githubusercontent.com/AaronGoldsmith/mcp-printable/main/server.py) | main consultado | Código | Alta para interfaz; pendiente para resultados |
| Addon 0.2.3 despacha comandos en hilo principal vía timers y TCP local 9876, con respuesta de versión. | [addon/__init__.py](https://raw.githubusercontent.com/AaronGoldsmith/mcp-printable/main/addon/__init__.py) | 0.2.3 | Código | Alta |
| Backend OpenSCAD documenta análisis STL con Trimesh, componentes, volumen, dimensiones y voladizos; no paridad completa con Blender. | [Backend OpenSCAD](https://raw.githubusercontent.com/AaronGoldsmith/mcp-printable/main/docs/openscad/README.md) | main consultado | Documentación primaria | Alta para alcance declarado |
| 3D Print Toolbox ofrece análisis, reparación y exportación; licencia GPL-3.0-or-later. | [Ficha oficial](https://extensions.blender.org/add-ons/print3d-toolbox/) | 1.5.0, changelog 2026-10-19 | Documentación primaria recuperada por buscador | Alta |
| Una reparación antigua producía non-manifolds en ciertos casos y se retiró. | [Historial Toolbox](https://extensions.blender.org/add-ons/print3d-toolbox/versions/) | 1.1.4, 2025-01-21 | Documentación primaria / changelog | Alta |
| Trimesh es alternativa Python MIT con operaciones de malla y STL. | [Repositorio Trimesh](https://github.com/mikedh/trimesh), [instalación](https://trimesh.org/install.html) | Consulta 2026-11-02 | Documentación primaria | Alta |

## Capacidades confirmadas y limitaciones

**Printable:** está comprobada documentalmente la existencia de herramientas, no un servicio de certificación. Reúne modelado, renders, cortes, validación y exportación. Las promesas de obtener mecanismos funcionales directamente de una petición no constituyen evidencia externa. El README incluso tiene conteos de herramientas distintos: no usarlos como criterio de calidad. [README](https://github.com/AaronGoldsmith/mcp-printable).

El servidor delega validación a Blender. No se consiguió leer la implementación interna de handlers: los intentos de acceso devolvieron `cache miss`. Quedan sin auditar muestreo de espesores, tolerancias, falsos negativos, tratamiento de modificadores e intersecciones. No presentar THIN_WALLS como medición exhaustiva. El control de versiones servidor/addon identifica posibles desajustes, pero no evita todos los fallos. [Servidor](https://raw.githubusercontent.com/AaronGoldsmith/mcp-printable/main/server.py).

OpenSCAD agrega otro programa y un intercambio por STL; no conserva el diseño editable de Blender mediante ese intercambio. Su documentación llama `is_winding_consistent` a normales que apuntan afuera: hay que distinguir consistencia local de orientación global y volumen positivo. No generalizar las advertencias del autor sobre rutas absolutas o unión de shells por laminadores sin reproducirlas. [Backend](https://raw.githubusercontent.com/AaronGoldsmith/mcp-printable/main/docs/openscad/README.md).

| Alternativa existente | Uso propuesto | Límite / decisión |
|---|---|---|
| 3D Print Toolbox | Diagnóstico dentro de Blender y revisión humana de geometría | Reutilizar antes de programar checks equivalentes; adaptar versión/API y verificar salida. No activar reparación automática como criterio de éxito. |
| BMesh y API Blender | Medidas, topología y comprobaciones sobre geometría evaluada | Primitivas reutilizables; no validador FDM listo. Detalle en INV-04. |
| Trimesh | Segunda lectura del STL exportado | Complementa Blender; no verifica editabilidad ni intención del patrón. Detalle en INV-04. |
| Creality Print | Interpretación final por perfiles y trayectorias de capas | Obligatorio en el escenario; CLI experimental según INV-04; laminar no garantiza impresión física. |

**Inferencia para el laboratorio:** watertight es insuficiente: no implica dimensiones correctas, espesor apropiado, ausencia de todas las autointersecciones, detalles resolubles por extrusión, adhesión, soportes adecuados o resistencia. Se requieren controles geométricos y revisión del laminado con parámetros explícitos. Una boquilla de 0,4 mm no fija por sí sola un umbral universal de detalle o pared.

## Compatibilidad Codex / macOS Apple Silicon

Printable menciona Codex; su transporte stdio y código Python hacen plausible integrarlo, pero **no se comprobó conexión con Codex ni ejecución ARM64**. Blender se declara ≥3.6 en el addon. No hay matriz de pruebas por combinación Blender/macOS/arquitectura en la evidencia leída. [README](https://github.com/AaronGoldsmith/mcp-printable), [addon](https://raw.githubusercontent.com/AaronGoldsmith/mcp-printable/main/addon/__init__.py).

Dependencias directas documentadas: Python, MCP, Pillow, Trimesh, NumPy; Blender y addon para ese backend, OpenSCAD para el otro. No se requiere Docker en el manifiesto. MIT no implica que todas las dependencias tengan esa licencia. No se observa tarifa de servicio del proyecto; persisten costos del agente, tiempo de integración, RAM/CPU y ensayos de impresión. [Manifiesto](https://raw.githubusercontent.com/AaronGoldsmith/mcp-printable/main/pyproject.toml).

## Comunidad y mantenimiento

La vista consultada del repositorio muestra 34 commits, 2 estrellas, 2 forks y 2 issues abiertos; es una fotografía, no una métrica de fiabilidad. No se obtuvo fecha del último commit ni evidencia independiente de CU-01 en Apple Silicon. La afirmación de impresiones reales procede del propio autor. [Repositorio](https://github.com/AaronGoldsmith/mcp-printable).

Toolbox muestra 53 reseñas y contribuciones de Erik Woods en correcciones 1.5.0; una reseña de rawknee sobre 1.4.1 describe corrección de geometría manifold. Es testimonio alojado en la ficha, no ensayo reproducible. Su historial ofrece evidencia concreta de mantenimiento, incluyendo la retirada de una reparación problemática. [Ficha](https://extensions.blender.org/add-ons/print3d-toolbox/), [historial](https://extensions.blender.org/add-ons/print3d-toolbox/versions/).

## Aplicación al CU-01

Propuesta, no resultado: conservar el `.blend` editable, medir envolvente exterior 150×150×60 mm **incluyendo ladrillos**, revisar cuatro caras y continuidad de esquinas, cambiar tamaño de ladrillos y repetir medidas. El resultado STL debe contener el relieve en sus triángulos; un render no prueba ese requisito.

Pared 2 o 20 mm, base y drenaje siguen **sin confirmar**. No asignar PASS a esos requisitos. Una abertura superior o drenaje diseñado puede existir en un sólido de paredes cerradas: no confundir cavidad con bordes topológicos abiertos. Revisar cortes y unión real entre ladrillos y cuerpo; objetos visualmente superpuestos no prueban un sólido aceptable.

## Riesgos y preguntas abiertas

- Precisión de espesores y colisiones de Printable pendiente; falta conjunto de casos positivos y negativos.
- La referencia actual es ahujasid; Printable añade otro puente y puerto. Comparar convivencia y conflictos antes de incorporarlo; no asumir interoperabilidad entre addons.
- Reglas FDM del servidor pueden imponer preferencias de diseño. Deben subordinarse al contrato del macetero.
- Falta fijar versiones/SHAs, probar instalación ARM64 y verificar que no se pierden modificadores ni geometría al exportar.
- No hay prueba física, ni validación específica K1C/PLA, ni ensayo de retención de agua; drenaje y uso exterior no autorizan inferir esos resultados.

## Recomendación y próximos experimentos (sin ejecutarlos)

**Reutilizar Toolbox y primitivas Blender como primera opción; experimentar con Printable, sin adoptarlo aún como validador obligatorio. Confianza media.** Trimesh queda como comprobación independiente de exportación. La elección se apoya en alcance documental y en evitar duplicar un puente antes de conocer el existente.

Después de autorización de la fase experimental: fijar versiones; ejecutar controles con escala errónea, pared fina, caras invertidas, cuerpos desconectados, intersección y relieve solo visual; comparar reportes contra casos conocidos. Comprobar si el addon usa malla evaluada y cómo estima espesores. Ejecutar CU-01 y su edición incremental, reimportar STL y revisar capas en Creality Print. Registrar PASS/FAIL/INCONCLUSIVE por requisito, tiempo, falsos negativos y costo. Ninguno de estos experimentos se realizó.
