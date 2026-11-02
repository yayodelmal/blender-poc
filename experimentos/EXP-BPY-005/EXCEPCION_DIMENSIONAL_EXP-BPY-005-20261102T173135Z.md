# Excepción dimensional — EXP-BPY-005, run `EXP-BPY-005-20261102T173135Z`

**Registrado:** 2026-11-02T17:45Z. Archivo nuevo; no modifica ningún informe, manifiesto ni artefacto. Decisión del proyecto: [ADR-0003](../../docs/05_decisiones/ADR-0003_cierre_fase1_con_excepcion_dimensional.md).

## Decisión del responsable

El responsable decidió **no realizar las mediciones físicas con pie de metro**, por considerar suficiente la inspección visual para el alcance exploratorio de esta prueba de concepto. La decisión es consciente. No es una medición realizada.

## Cuatro hechos distintos

| Hecho | Estado | Respaldo |
|---|---|---|
| Impresión física completada | **Sí (declarada)**, con 3 fotos coherentes | Declaración del responsable; `evidencias/` (3 fotos selladas en `registro_artefactos.jsonl`); tiempo "~30 min" sin medir |
| Inspección visual | **Favorable** | Declaración y `EVALUACION_CALIDAD_PARCIAL_…md` (27 relieves, juntas definidas, sin defectos evidentes a simple vista) |
| Medición dimensional física | **NOT RUN — omitida por decisión del usuario** | `MEDICIONES_FISICAS.md` sin datos; no se inventan |
| Aceptación del usuario para continuar | **Sí**, para el alcance exploratorio | Esta decisión |

## Verificaciones y su estado

| Criterio | Estado |
|---|---|
| Tolerancia ±0,5 mm por eje (X 80, Y 60, Z 5 mm; base 4 mm informativa) | **NOT RUN — omitida por decisión del usuario.** No se declara cumplida ni incumplida |
| Tres medidas por eje, instrumento, resolución y verificación de cero | NOT RUN |
| Adhesión entre capas, resistencia, deformación cuantificada | NOT RUN / INCONCLUSIVE |
| Adhesión a cama | Declarada buena (pegamento en barra); sin foto de cama ni primera capa |
| Cara de la PEI montada, hora de inicio y fin, archivo abierto en el laminador, estado de la boquilla | NO MEDIDO |
| Conteo de 27 relieves, definición de juntas, acabado | PASS visual (cualitativo) |

## Veredicto técnico de EXP-BPY-005

**No es PASS.** El protocolo (`PROTOCOLO_IMPRESION.md`, "Medición y aceptación") y `CIERRE_FASE_1` §9 exigen mediciones reales para aceptar. Estado: **impresión completada y evaluada visualmente; verificación dimensional NOT RUN por decisión del usuario; aceptado por el usuario para el alcance exploratorio.** Las estimaciones del laminador (30 min 36 s, 14,45 g) siguen siendo estimaciones.

## Implicaciones

- **Calidad dimensional:** un error de unas décimas de milímetro (el umbral aprobado es 0,5 mm sobre 80 mm, ~0,6 %) no es detectable a simple vista. La exactitud dimensional de la K1C con este perfil queda **sin caracterizar**. No hay datos de encogimiento, ni de "pata de elefante" en la primera capa.
- **Reproducibilidad:** hay una sola impresión y ningún dato cuantitativo de la pieza. Quedan registrados el STL, el 3MF, la ficha de laminado y las fotos, así que el proceso es repetible, pero su resultado físico no es comparable con otro run.
- **Tolerancia ±0,5 mm:** sigue siendo la aprobada para este cupón. No tiene respaldo empírico y no debe reutilizarse en CU-01 sin medición.
- **Alcance de la excepción:** solo este cupón y su propósito exploratorio. No se extiende a CU-01 ni a ninguna pieza funcional.
- **Reversibilidad:** si la pieza se conserva, las medidas pueden tomarse después y registrarse como adenda, sin reescribir este documento.
