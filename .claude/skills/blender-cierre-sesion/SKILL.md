---
name: blender-cierre-sesion
description: Use when en blender-poc termina un run, una revisión o un diagnóstico y hay que dejar el estado coherente: actualizar el estado de las fases, el índice de experimentos, las erratas o la memoria, o cuando un documento quedó viejo respecto a lo ejecutado.
---

# blender-cierre-sesion

Después de cada run, el repo debe poder leerse sin recordar la sesión. Se **añade**, no se reescribe.

## Checklist

1. **Informe del run** como archivo nuevo: `RUN/reports/RESULTADO.md`. Debe separar lo medido, lo declarado por el responsable y lo no ejecutado (`NOT RUN`). Un PASS digital no es pieza imprimible. Si hubo intentos fallidos, listarlos con su carpeta.
2. **Sellado** (`blender-integridad`) hecho y verificado antes de citar hashes.
3. **Estado vigente**: `docs/06_estado/ESTADO_FASES.md`. Actualizar la fila del experimento, los pendientes del responsable y el «próximo experimento». Es la fuente canónica.
4. **Índice**: `experimentos/INDEX.md`. Una fila por run con su resultado y el estado vigente.
5. **Erratas**: si un informe anterior resulta incorrecto, entrada nueva en `docs/06_estado/ERRATAS.md` (afirmación original, mejor respaldo, fuentes, límite). No editar el informe original.
6. **Lecciones**: si hubo un fallo reutilizable, fila en `docs/04_procedimientos/APRENDIZAJES.md` (síntoma, causa, regla, verificación, estado).
7. **Decisiones**: si el responsable aceptó un riesgo o una excepción, ADR en `docs/05_decisiones/` (los tres actuales son ADR-0001 a 0003).
8. **Memoria**: actualizar `blender-poc-estado-y-reglas.md` solo con lo que no se deduce del repo (estado de fase, pendientes del responsable, motivos).

## Tabla de destinos

| Qué pasó | Dónde se anota |
|---|---|
| Resultado de un run | `RUN/reports/RESULTADO.md` (nuevo) |
| Cambió el estado de una fase | `ESTADO_FASES.md` |
| Informe previo incorrecto | `ERRATAS.md` (nunca editar el original) |
| Aprendizaje reutilizable | `APRENDIZAJES.md` |
| Decisión o excepción del responsable | `docs/05_decisiones/ADR-000N` |

## Errores frecuentes

- Marcar «cerrado» algo que el responsable solo declaró. Escribir qué se midió y qué no.
- Dejar el índice sin la fila del run, lo que hace que el estado parezca más atrasado de lo real.
- Dar una excepción por heredada: la dimensional de la Fase 1 (ADR-0003) **no** se hereda a CU-01.
