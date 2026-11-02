# Declaración de impresión — EXP-BPY-005

**Run:** `EXP-BPY-005-20261102T173135Z`. **Registrado:** 2026-11-02T17:34Z. Archivo nuevo; no modifica documentos con hash en el manifiesto.

## Declaración del responsable (no verificada)

El responsable informa que **ya imprimió la pieza** (placa de relieve de EXP-BPY-003), que el resultado fue "excelente y perfecto" y que "los ladrillos se ven bien".

## Qué es y qué no es esto

- Es una **declaración humana de inspección visual**. No hay fotografías, mediciones ni registro en el repositorio.
- **No se declara PASS.** El criterio aprobado es ±0,5 mm por eje (X 80, Y 60, Z 5 mm; base 4 mm informativa), con tres medidas por eje y registro del instrumento (`MEDICIONES_FISICAS.md`). Sin esos datos, la comprobación dimensional está `NOT RUN`.
- Una inspección visual no acredita adhesión de capas, deformación, acabado ni dimensiones (`EVALUACION_CALIDAD.md`).

## Datos que no se indicaron (siguen `NO MEDIDO`)

Hora de inicio y fin, tiempo real, material real consumido, archivo abierto en el laminador (copia o proyecto distinto), preset efectivo al imprimir, decisión sobre el adhesivo y superficie de la cama, estado de la boquilla, incidencias durante la impresión, fotos, pie de metro y medidas.

## Estado

| Elemento | Estado |
|---|---|
| Impresión realizada | Declarada por el responsable; 3 fotos coherentes con la declaración |
| Evaluación visual | Declarada positiva; 3 fotos sin defectos evidentes a simple vista (cualitativo) |
| Mediciones físicas (V10) | `NOT RUN` |
| EXP-BPY-005 | **Impreso, evidencia pendiente.** No cerrado |
| Fase 1 | Sigue `PENDIENTE_VALIDACION_FISICA` hasta tener datos |

## Para cerrarlo

1. ~~Fotos de la pieza~~ (recibidas; ver abajo). Falta la foto de la superficie de impresión.
2. Tres medidas por eje con pie de metro, e instrumento y resolución.
3. Los datos de la lista anterior.
4. La captura del preset al imprimir, si la guardaste.

## Evidencia fotográfica (agregada)

Tres fotos aportadas por el responsable, en `evidencias/`, selladas en `registro_artefactos.jsonl` (rol `evidence`). Los nombres originales eran `Imagen de ChatGPT 2 nov 2026, 02_35_xx p.m.jpg`; el EXIF no incluye cámara. La procedencia (foto tomada por el responsable de la pieza impresa) se toma de su declaración; el archivo por sí solo no la acredita.

| Archivo | SHA-256 | Qué se ve (observación del asistente) |
|---|---|---|
| `EXP-BPY-005-20261102T173135Z_foto_1_lateral_oblicua.jpg` | `5fe6fe17a40f7f1b050d4d833a6860e031ab802cd57bf614d71fbad6f069e55d` | Vista oblicua de una placa blanca con motas oscuras y ladrillos en relieve sobre una encimera de granito. Bordes de ladrillo y de placa rectos y definidos; relieve visible sobre una base |
| `EXP-BPY-005-20261102T173135Z_foto_2_cara_plana.jpg` | `f68a36a07d4e43818293d3968f5ae9bb7da784c4b40de3d0a887ca8bcaf63b6a` | Cara plana sin relieve (presumiblemente la inferior; la foto no lo indica). Superficie lisa y uniforme, esquinas rectas, sin deformación evidente a simple vista |
| `EXP-BPY-005-20261102T173135Z_foto_3_superior_relieve.jpg` | `430b1302d25741eadfab275704534554f2cefcb635482d1d714d2abd0b63aa3c` | Vista superior: filas de 5, 4, 5, 4, 5 y 4 ladrillos, es decir 27, igual al diseño. Juntas visibles con textura de trayectorias diagonales; sin ladrillos ausentes ni fusionados a simple vista |

**Límites:** las fotos no permiten medir dimensiones, ni la altura del relieve, ni evaluar adhesión de capas o resistencia. No hay regla ni pie de metro en el encuadre. La inspección es cualitativa y coincide con lo que el responsable declaró, pero no sustituye a `MEDICIONES_FISICAS.md`.

Un archivo duplicado de la foto 1 (mismo SHA-256) apareció en `archivo/investigacion_mcp/ola_d/` con nombre `Imagen de ChatGPT 2 nov 2026, 02_35_32 p.m.jpg`. Se eliminó a petición del responsable, tras confirmar que el hash coincidía con la foto 1 conservada.

## Datos de la impresión declarados (agregado)

Declarados por el responsable; ninguno está medido ni respaldado por un registro.

| Campo | Declaración | Estado del dato |
|---|---|---|
| Adhesivo | Usó **pegamento en barra** sobre la superficie de la cama | Declarado |
| Resultado de adhesión a la cama | "Bueno y uniforme" | Declarado; no hay foto de la cama ni de la primera capa |
| Duración | **Aproximadamente 30 minutos** | Estimación del responsable, **no medida**. La estimación del laminador era 30 min 36 s; que se parezcan no la convierte en medición |
| Cara de la PEI montada y su limpieza | No indicado | `NO MEDIDO` |
| Hora de inicio y fin, material real consumido, estado de la boquilla, incidencias | No indicado | `NO MEDIDO` |
| Archivo abierto en Creality Print | No indicado | `NO MEDIDO` |

Con esto queda resuelta la decisión sobre el adhesivo que figuraba pendiente (usar adhesivo en barra), salvo la identificación de la cara de la PEI.
