# CU-01 — Variante blanca mate

**Resultado final: PASS.** Se creó una copia visual de la REV-002 con material blanco mate. La geometría se mantuvo exactamente igual.

## Apariencia aplicada

- Un material para todo el modelo: `CU01_White_Matte`.
- Color base RGBA: blanco puro `(1, 1, 1, 1)`.
- Rugosidad solicitada al material: 0,8 (mate; Blender lo conserva como `0.8000000119` por precisión de punto flotante).
- El archivo está preparado para mostrar el material en la vista de Blender.

## Comprobación independiente

- Huella de geometría de la fuente y de la copia: idéntica (`e0ef2049a63a2fc155458d7af82cca167886549aa32f7c6960e421d0d392e376`).
- Envolvente: 150,000021 × 150,000021 × 60,000002 mm.
- Una componente cerrada y manifold.
- Material blanco mate y marca de variante comprobados.
- Blender 5.4.0 Alpha, build `745ab9a3e3c5`; ejecutable SHA-256 `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`.

## Trazabilidad de la validación

El primer control de acabado dio `FAIL` porque exigía que la rugosidad coincidiera con 0,8 a una tolerancia menor que la precisión numérica que devuelve Blender. Las comprobaciones de geometría, dimensiones y componentes ya habían pasado. Se conserva ese resultado inicial en `evidencias/validation.json`. Con una tolerancia compatible con esa precisión, dos validaciones independientes posteriores devolvieron `PASS`; el resultado final está en `evidencias/validation_final.json`.

## Archivos

- `artifacts/CU01_REV002_white_matte.blend` — variante blanca.
- `evidencias/validation_final.json` — resultado final.
- `registro_artefactos.jsonl` — hashes y referencias.

Esta variante es solo visual; no cambia la geometría de pared de 10 mm. No se exportó STL ni se imprimió.
