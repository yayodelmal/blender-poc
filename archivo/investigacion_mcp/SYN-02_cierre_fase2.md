# SYN-02 — Coherencia y criterios de salida de Fase 2
**Fecha:** 2026-11-02. **Estado:** IN PROGRESS; revisión documental, no cierre de Fase 2.

## Revisión de coherencia

| Entregable | Estado | Ajuste o brecha para consolidación |
|---|---|---|
| META | Fase 1 abierta | Mantener selección tecnológica provisional hasta evidencia de punta a punta |
| ARQ-001 | Borrador anticipado | Mantener el diagrama candidato; aclarar medición incluyendo relieve, congelar versiones y describir fallback GUI |
| CAP-001 | Guía didáctica | Candidatos existen, pero compatibilidad/eficacia no probada; corregir claims como hechos solo tras vincular INV |
| FLU-001 | Propuesta conceptual | Reusar logs y snapshot nativos donde sirvan; fallo de snapshot/restauración o conflicto concurrente debe detener cambios |
| CON-001 | Borrador nuevo | R01 medida con relieve es provisional; resolver espesor, base, drenaje, detalles/tolerancias antes de ensayo final |
| VAL-001 | Borrador nuevo | Matriz de chequeos propuesta; umbrales digitales son experimentales y requieren acuerdo |

Revisé README, los documentos existentes, plan y plantilla. Los documentos de proyecto son intenciones, no registros de una instalación ya validada. Toda afirmación sobre proyectos se apoya en INV-01…05/08; fuentes `main`, `master`, `current` y recuentos comunitarios conservan límites temporales consignados allí. La investigación delegada fue un medio de ejecución documental; no altera la preferencia de un Codex único para el pipeline de producción.

## Correcciones transversales recomendadas

1. Distinguir objeto completo de envolvente exterior final. Si 150 mm incluye relieve, medir geometría evaluada del patrón, no el cuerpo base.
2. Representar los valores desconocidos como pendientes; no traducir 2/20 mm a un supuesto ni añadir base/drenaje.
3. Separar ejecución MCP, validez geométrica, laminado, aceptación digital e impresión física.
4. Conservar maestro `.blend`; STL es derivado sin editabilidad paramétrica. Probar reabrir snapshot antes de confiar en restauración.
5. Registrar tolerancias junto con unidad, método y versión. La boquilla de 0,4 mm no define todas las tolerancias FDM.
6. Tratar `INCONCLUSIVE`/`NOT RUN` como no aceptado. Reparación automática exige validación desde cero.
7. Aclarar que CLI Creality está documentado, pero el reporte adverso localizado #634 es Windows y #645 es petición. No extrapolar a K1C/macOS.
8. Si snapshot no se escribe/verifica antes de mutar, detener. Si no se restaura el estado conocido, detener y escalar. Si una persona modifica la escena concurrentemente, reconciliar revisión antes de aceptar o restaurar; no sobrescribir cambios posteriores.

## Dependencias y salida por olas

| Ola | Estado | Resultado/condición |
|---|---|---|
| A: INV-01,02,03,04,05,08 | Investigación documental entregada | Hallazgos accesibles en Markdown; pruebas propias = 0; ARM64 integral desconocida |
| B: INV-06 / CON-001 | Borrador entregado | Pendiente revisar parámetros geométricos y reglas de conflicto/rollback |
| B: INV-07 / VAL-001 | Borrador entregado | Pendiente acordar tolerancias, criterios de relieve, espesor y condiciones de impresión |
| C1: SYN-01 | Candidata provisional redactada | No seleccionar instalación hasta experimento documentado |
| C2: SYN-02 | Este documento | Fase 2 no cerrada |
| D: CU-01 experimental | No iniciado | Requiere completar decisiones de diseño, versions/políticas y autorización de fase siguiente |

## Criterios de salida de Fase 2

- [ ] Aprobar alcance de 150×150×60 (incluye o excluye relieve).
- [ ] Confirmar pared, base, drenaje y parámetros físicos relevantes.
- [ ] Acordar tolerancia digital de ensayo y método reproducible.
- [ ] Fijar versiones objetivo para Codex, Blender, MCP, skill QA, validadores y Creality Print.
- [ ] Definir requisitos de seguridad/localidad y revisar versiones de puente concretas.
- [ ] Aprobar contrato de operación, revisión, evidencia y manejo de estado concurrente.
- [ ] Aprobar VAL-001 y controles negativos, separando lo digital de una futura prueba física.
- [ ] Hacer revisión final de coherencia entre ARQ/CAP/FLU/CON/VAL y actualizar estado de cada uno.

Hasta cumplir esas condiciones, mantener Fase 1 y Fase 2 IN PROGRESS. Los experimentos de fase posterior deben comenzar en alcance desechable y no enviar impresión sin una decisión explícita. La siguiente actividad más útil es que el usuario resuelva los parámetros abiertos del CU-01; mientras tanto, se puede revisar fuentes/criterios sin tocar el equipo.
