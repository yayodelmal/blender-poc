# ADR-0002 — Política sobre la build Alpha de Blender

**Estado: ACEPTADA — opción C (2026-11-02, responsable).** Aceptada tras la auditoría documental; se acepta la recomendación tal como está escrita.

## Contexto

- Blender 5.2.3 LTS falló en tres arranques background por Metal (código 139). Intentar `--gpu-backend opengl` fue rechazado porque esa build solo admite Metal (`EXP-BPY-001/reports/RESULTADO.md`).
- Todos los experimentos que pasaron usan Blender 5.4.0 Alpha, rama `main`, build `745ab9a3e3c5` (2026-10-30), ejecutable SHA-256 `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`, Python 3.13.13.
- Los informes aclaran que PASS "no valida una versión estable". La causa del arreglo no está establecida (el issue #163272 es solo plausible).
- EXP-BPY-001 dejó pendiente decidir si se acepta una Alpha como entorno temporal. No hay registro de esa decisión.

## Opciones

| Opción | Ventaja | Costo |
|---|---|---|
| A. Aceptar y fijar esta Alpha por hash de ejecutable | Continuidad inmediata y reproducible en esta máquina | Riesgo de deriva si se actualiza; sin soporte; no representa una versión estable |
| B. Repetir EXP-BPY-001 a 003 en una versión estable que arranque en background | Entorno defendible | Hay que encontrar una versión estable que no falle por Metal; trabajo adicional |
| C. A ahora, B antes de CU-01 | Equilibrio | Dos etapas |

## Recomendación (a decidir por el responsable)

**C**, con estas condiciones:
- no actualizar ni reemplazar la app `/Applications/Blender.app` sin registro;
- verificar el hash del ejecutable antes de cada experimento;
- repetir los controles críticos en una versión estable antes de cerrar CU-01.

## Datos que faltan

- ¿Existe en esta máquina otra versión de Blender que arranque en background? **[no verificado]**
