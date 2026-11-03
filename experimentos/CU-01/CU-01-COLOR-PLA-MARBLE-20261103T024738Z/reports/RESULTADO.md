# CU-01 — Variante PLA marmoleada

**Resultado: PASS.** Se creó una copia visual blanca con motas negras y grises pequeñas, usando un patrón procedural tipo Voronoi y acabado mate. La geometría coincide exactamente con CU-01 REV-002.

## Apariencia

- Base blanca; paleta de motas entre negro y gris.
- Patrón procedural 3D con Voronoi, escala 1000 y máscara de distancia 0,20–0,27.
- Rugosidad 0,8 para un acabado mate.
- Material único aplicado a todo el modelo. La vista 3D se guarda en modo Material Preview.

## Validación independiente

- Huella de geometría fuente/copia idéntica: `e0ef2049a63a2fc155458d7af82cca167886549aa32f7c6960e421d0d392e376`.
- Envolvente: 150,000021 × 150,000021 × 60,000002 mm.
- Una componente cerrada y manifold.
- Presencia de nodos Voronoi, paleta blanco/negro/gris, rugosidad y marcador de acabado comprobados.
- Blender 5.4.0 Alpha, build `745ab9a3e3c5`; ejecutable SHA-256 `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`.

## Archivos

- `artifacts/CU01_REV002_pla_marble.blend` — modelo con motas.
- `evidencias/validation.json` — validación independiente.
- `registro_artefactos.jsonl` — hashes y referencias.

Es una apariencia de material para previsualización en Blender; no modifica la geometría ni garantiza la apariencia exacta de una impresión real en PLA. No se exportó STL ni se imprimió.
