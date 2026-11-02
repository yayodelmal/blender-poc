# Laboratorio de Modelado 3D Agéntico
**Documento maestro — versión 1.1 | 2 de noviembre de 2026**

**Estado:** Fase 1 en curso — investigación y selección tecnológica.  
**Entorno de referencia:** MacBook con Apple Silicon (macOS, ARM64).  
**Agente seleccionado:** Codex.  
**Integración de referencia:** [MCP for Blender — ahujasid](https://github.com/ahujasid/mcp-for-blender).  
**Caso de uso:** CU-01 — Macetero con ladrillos en relieve.

## 1. Visión y meta
Trabajar con Codex en una ventana y Blender en otra. Mediante instrucciones en español, crear y modificar modelos 3D de forma interactiva y observar los resultados en Blender. Cuando el modelo esté destinado a impresión 3D, sus detalles físicos deben estar representados mediante geometría real y exportarse correctamente a STL para prepararlo en Creality Print.

**Meta verificable:** crear un modelo, modificarlo incrementalmente sin perder requisitos anteriores y verificar su geometría antes de exportarlo. No basta con que se vea bien en pantalla.

## 2. Decisiones acordadas
- **Codex es el agente principal.** No se prioriza comparar Claude Code u OpenCode mientras Codex sea suficiente.
- **MCP for Blender (ahujasid) es la base de referencia**, por su ecosistema y compatibilidad declarada con Codex; no se asume que por sí solo garantice buenos resultados.
- La **Fase 1 se desarrolla para macOS Apple Silicon**, priorizando ejecución local y dependencias compatibles con ARM64.
- Evitar dependencias innecesarias de Docker o servicios externos; mantener portabilidad futura hacia Linux cuando sea posible.
- **Investigar soluciones existentes antes de programar componentes propios.**
- No realizar todavía una auditoría de la instalación ni cambios en el entorno.
- La impresión objetivo es **Creality K1C**, material **PLA**, boquilla **0,4 mm**, laminador **Creality Print**.
- Orca como entorno de agentes es opcional; OrcaSlicer no es requisito.

## 3. Fase 1 — Investigación y selección tecnológica
**Objetivo:** justificar una arquitectura mínima reutilizando herramientas existentes y evidencia de uso real.

**Líneas de investigación:**
1. Capacidades de MCP for Blender y alternativas relevantes: creación de geometría, edición incremental, Python API, inspección y retroalimentación visual.
2. Skills, documentación y buenas prácticas de geometría y fabricación FDM aplicables a Codex.
3. Validación geométrica independiente: mallas cerradas/manifold, dimensiones, intersecciones y preservación de detalles.
4. Compatibilidad de dependencias con macOS ARM64 y portabilidad futura a Linux.
5. Salud de comunidades: mantenimiento, issues, discusiones, contribuciones y experiencias verificables de usuarios.
6. Integración con exportación STL y preparación en Creality Print.

**Candidatos para estudiar (no seleccionados como dependencias):**
- [MCP for Blender](https://github.com/ahujasid/mcp-for-blender) — referencia principal.
- [MCP Printable](https://github.com/AaronGoldsmith/mcp-printable) — ideas de reglas FDM y validación.
- [Blender MCP Ultra](https://github.com/carlosh7/blender-mcp) — amplitud de operaciones.
- [Blender AI Agent](https://github.com/ahmedsayed1911/Blender-AI-Agent) — referencia de planificación y revisión.
- Blender Python API, BMesh y Trimesh — candidatos de ejecución/validación; compatibilidad concreta por verificar.

**Criterios para cerrar la fase:**
- Matriz comparativa de capacidades, comunidad, mantenimiento y compatibilidad macOS ARM64.
- Identificación de componentes reutilizables y brechas no resueltas.
- Arquitectura candidata justificada y riesgos explícitos.
- Plan de pruebas del CU-01 y criterios de aceptación.
- Decisión informada de qué instalar o desarrollar en la fase siguiente.

**No se considera completada la Fase 1** solo por elegir Codex y MCP for Blender.

## 4. Caso de uso CU-01 — Macetero con ladrillos
**Escenario:** Codex y Blender abiertos simultáneamente. El usuario describe el objeto, observa su construcción y solicita modificaciones posteriores.

| Atributo | Requisito |
|---|---|
| Forma exterior | Cuadrada, 150 × 150 mm |
| Altura | 60 mm |
| Espesor de pared | **Pendiente: 20 mm o 2 mm** |
| Decoración | Patrón de ladrillos tipo castillo en las cuatro caras |
| Naturaleza del patrón | **Relieve geométrico real**, no textura visual |
| Material | PLA |
| Impresora / boquilla | Creality K1C / 0,4 mm |
| Exportación / laminado | STL / Creality Print |

**Secuencia de aceptación:**
1. Crear el macetero con medidas verificables.
2. Agregar ladrillos en relieve geométrico en las cuatro caras.
3. Modificar el tamaño o distribución de los ladrillos mediante una nueva instrucción.
4. Mantener dimensiones y continuidad geométrica, incluidas las esquinas.
5. Validar topología, dimensiones y presencia del relieve en el STL.
6. Abrir y laminar el archivo en Creality Print.

**Criterio de calidad:** el agente debe distinguir textura visual de geometría fabricable, conservar editabilidad y comunicar verificaciones y limitaciones. Un STL válido y laminable **no garantiza** por sí solo una impresión física exitosa.

**Datos por confirmar:** espesor de paredes; presencia de base y drenaje.

## 5. Hipótesis arquitectónica — pendiente de validación
Instrucción natural → interpretación y plan geométrico → Codex + MCP for Blender + Python API → inspección visual y validación geométrica → corrección iterativa → exportación STL → Creality Print.

Las skills especializadas, una representación intermedia del diseño y una memoria de errores son **hipótesis de mejora**, no decisiones de implementación. Un solo agente es suficiente como punto de partida.

## 6. Fases previstas
- **Fase 1 — Investigación y selección tecnológica:** en curso.
- **Fase 2 — Diseño de la solución:** contratos, herramientas, flujos y validaciones.
- **Fase 3 — Implementación del laboratorio:** configuración e integración en MacBook.
- **Fase 4 — Validación experimental:** ejecutar CU-01 y medir cumplimiento, fallos, iteraciones, tiempo y costo.
- **Fase 5 — Optimización:** corregir brechas e incorporar memoria técnica si aporta valor.

## 7. Registro de decisiones y pendientes
**Decisiones confirmadas:** Codex; MCP for Blender como referencia; macOS Apple Silicon; Creality K1C/PLA/Creality Print; investigar antes de desarrollar.

**Pendientes:** evidencia comunitaria sobre modelado imprimible; evaluación de skills; validadores reutilizables; compatibilidad ARM64; espesores y detalles del macetero.

**Próximo hito:** completar una comparación fundamentada de las herramientas existentes y proponer una arquitectura mínima, sin instalar ni programar todavía.
