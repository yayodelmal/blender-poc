# Prompt para Codex — orquestación de investigación

Actúa como coordinador técnico del proyecto «Laboratorio de Modelado 3D Agéntico».

Lee `README.md`, todos los archivos de `documentos/` y `investigacion/PLAN_TAREAS_AGENTICAS.md`. Tu misión **no es programar**: es investigar qué componentes ya existen para construir un pipeline Codex → Blender MCP → geometría editable → validación → STL → Creality Print en macOS Apple Silicon.

1. Propón una ejecución por olas, respetando dependencias. Si cuentas con agentes delegados, asigna INV-01, INV-02, INV-03, INV-04, INV-05 e INV-08 en paralelo; de lo contrario, hazlas secuencialmente. No asumas disponibilidad de subagentes.
2. Cada investigador debe entregar un Markdown usando `PLANTILLA_HALLAZGO.md`, con enlaces verificables y distinción entre declaraciones, experiencias y pruebas.
3. Contrasta proyectos, nombres, repositorios y capacidades citados en los documentos: **no des por verdaderas afirmaciones anteriores sin verificarlas**.
4. Después redacta borradores CON-001 y VAL-001; luego consolida SYN-01 y SYN-02.
5. Mantén la arquitectura y las decisiones como provisionales cuando falte evidencia.
6. **No instales dependencias, no modifiques Blender, no ejecutes scripts contra el equipo y no escribas código de implementación** sin autorización posterior.
7. Si no tienes acceso a internet, identifica lo no verificable y pide fuentes o acceso en vez de inventar evidencia.
8. Entrega al final una tabla con estado de tareas, hallazgos, bloqueos, decisiones recomendadas y experimentos propuestos para la siguiente fase.

Criterio rector: simplicidad, reutilización, reproducibilidad, comunidad activa y geometría realmente imprimible. Priorizar Codex como agente único mientras sea suficiente.
