# CU-01 — REV-002 — Pared de 10 mm

**Resultado: PASS para validación geométrica digital independiente.** Esta revisión cambia el grosor de pared de 20 mm a 10 mm. Conserva la envolvente exterior y los demás parámetros aprobados. La REV-001 se mantiene intacta.

## Especificación

- Envolvente total: 150 × 150 × 60 mm, incluido el relieve.
- Cuerpo abierto arriba, con paredes de **10 mm**.
- Base cerrada de 4 mm, sin drenaje.
- Cavidad resultante: **128 × 128 × 56 mm**. El cuerpo liso mide 148 × 148 mm bajo el relieve; `(148 − 128) / 2 = 10 mm` por lado.
- Ladrillos nominales de 15 × 7 mm, relieve de 1 mm, juntas de 1,2 mm y aparejo alternado con continuidad en las cuatro esquinas.

## Validación

- Medida exterior: 150,000021 × 150,000021 × 60,000002 mm; dentro de ±0,01 mm.
- Los cuatro planos interiores se encontraron a ±64 mm y abarcan 56 mm de altura útil.
- Cavidad 128 × 128 × 56 mm; tapa abierta y base cerrada a z≈4 mm, comprobada con siete rayos interiores.
- Una componente cerrada y manifold, orientación coherente, volumen positivo y cero elementos degenerados.
- 264 parches de ladrillo (66 por cara), juntas de aproximadamente 1,2 mm.
- Volumen firmado: 423.761,855 mm³; esperado: 423.761,6 mm³, diferencia dentro de 1 mm³.
- Validación realizada en un proceso Blender separado del proceso de construcción.
- Blender 5.4.0 Alpha, build `745ab9a3e3c5`; ejecutable SHA-256 `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`.

## Nota del patrón

Para cubrir cada cara de 148 mm manteniendo juntas de 1,2 mm y el aparejo, las piezas de extremo miden 16,7 mm en hiladas pares y 8,6 mm en impares. Las piezas interiores son nominalmente de 15 mm.

## Alcance

Este PASS corresponde al modelo digital validado en Blender Alpha. No evalúa impresión física, resistencia, tolerancias de fabricación ni Blender estable. No se exportó STL, no se usó Creality Print y no se imprimió.

## Archivos

- `artifacts/CU01_REV002_planter_20261103T023400Z.blend` — modelo de paredes de 10 mm.
- `evidencias/validation.json` — mediciones independientes.
- `registro_artefactos.jsonl` — hashes de modelo, informe y evidencias.
