# Coordinación técnica — ejecución por olas

**Fecha:** 2026-11-02. **Alcance:** investigación documental y borradores; sin instalación, auditoría del equipo, ejecución de scripts ni implementación.

## Insumos y criterio

Se revisaron README.md, los cinco archivos originales de documentos/, PLAN_TAREAS_AGENTICAS.md y PLANTILLA_HALLAZGO.md. Los originales se conservan como antecedentes; SYN-02 registra las correcciones necesarias. Prioridad: simplicidad, reutilización, reproducibilidad y geometría fabricable; Codex como único agente del pipeline operativo. Los investigadores paralelos de esta sesión no son una decisión de arquitectura multiagente.

## Dependencias y asignación real

| Ola | Tareas | Responsable | Dependencia y salida |
|---|---|---|---|
| A | INV-01 → INV-02 | Investigador mcp_skills | Fuentes primarias y dos hallazgos separados |
| A | INV-03 → INV-04 | Investigador validacion | Fuentes primarias y dos hallazgos separados |
| A | INV-05 → INV-08 | Investigador estado_observabilidad | Fuentes primarias y dos hallazgos separados |
| B | INV-06 / CON-001 | Coordinador | INV-05; contraste de formatos y contrato provisional |
| B | INV-07 / VAL-001 | Coordinador | INV-03 e INV-04; criterios y pruebas propuestas |
| C1 | SYN-01 | Coordinador | Seis hallazgos + CON y VAL; matriz y arquitectura candidata |
| C2 | SYN-02 | Coordinador y revisión delegada | SYN-01; coherencia y puertas de salida |
| D futura | Experimentos autorizados | Codex único + revisión humana | Requisitos resueltos, versiones fijadas y autorización posterior |

Se confirmó disponibilidad de tres investigadores concurrentes, no seis. Ola A se ejecuta en tres líneas paralelas con dos tareas secuenciales por línea. La limitación de plazas no crea dependencias técnicas nuevas.

## Reglas de evidencia

- Cada hallazgo usa PLANTILLA_HALLAZGO.md y separa documentación primaria, declaraciones del autor, código/issues, testimonios y pruebas propias.
- Consulta web no equivale a prueba de instalación o funcionamiento; en esta entrega hay **cero pruebas propias del pipeline**.
- Fecha de consulta no equivale a fecha de publicación ni confirma actividad reciente. Registrar versiones cuando sean observables y desconocidas cuando no.
- Una fuente inaccesible o un enlace fallido no demuestra inexistencia del proyecto. No sustituir silenciosamente identidades.
- No aprobar compatibilidad de la cadena por compatibilidad aislada de sus componentes.
- «Finalizado» en investigación significa informe entregado; Fases 1/2 siguen IN PROGRESS si quedan condiciones de salida abiertas.

## Puertas entre olas

1. A → B: evidencia suficiente para especificar capacidades y límites; incertidumbres visibles.
2. B → C: contrato y validación con correspondencia requisito–medición–resultado, sin rellenar decisiones del usuario.
3. C → D: revisión de versiones/licencias, resolución de requisitos bloqueantes y autorización explícita para el alcance experimental. Esta entrega no autoriza instalar ni ejecutar.

## Entregables

- [INV-01](INV-01_mcp_blender.md), [INV-02](INV-02_skills.md), [INV-03](INV-03_validacion_fdm.md), [INV-04](INV-04_validadores.md), [INV-05](INV-05_edicion_estado.md), [INV-08](INV-08_observabilidad.md).
- [CON-001](CON-001_IN_PROGRESS.md), [VAL-001](VAL-001_IN_PROGRESS.md).
- [SYN-01](SYN-01_decision_arquitectura.md), [SYN-02](SYN-02_cierre_fase2.md).
- Ola D (preparación, no ejecución): [auditoría](ola_d/D-01_AUDITORIA_COHERENCIA.md), [compatibilidad/seguridad](ola_d/D-02_COMPATIBILIDAD_SEGURIDAD.md), [EXP-001](ola_d/EXP-001_CONECTIVIDAD.md), [EXP-002](ola_d/EXP-002_EDICION_PERSISTENCIA.md), [EXP-003](ola_d/EXP-003_GEOMETRIA_STL.md), [observabilidad](ola_d/D-06_OBSERVABILIDAD.md), [matriz](ola_d/MATRIZ_TRAZABILIDAD.md), [plan](ola_d/PLAN_EJECUCION_EXPERIMENTAL.md).

Ola D está autorizada solo para preparar documentos; ninguna prueba se ejecutó ni esta coordinación concede autorización para EXP-001. La revisión documental estática del socket es paso previo recomendado.
