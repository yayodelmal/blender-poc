# CU-01 — REV-003 — Pared de 5 mm

**Resultado: PASS para validación geométrica digital independiente.** Esta revisión cambia el grosor de pared de 10 mm (REV-002) a 5 mm, a pedido del responsable. REV-001 y REV-002 no se tocaron.

## Especificación

- Envolvente total: 150 × 150 × 60 mm, incluido el relieve.
- Cuerpo abierto arriba, paredes de **5 mm**, base cerrada de 4 mm, sin drenaje.
- Cavidad esperada: 138 × 138 × 56 mm (cuerpo liso 148 × 148 mm; (148 − 138) / 2 = 5 mm por lado).
- Ladrillo nominal 15 × 7 mm, relieve 1 mm, juntas 1,2 mm, aparejo alternado. 264 parches (66 por cara).
- Acabado por defecto del proyecto (`AGENTS.md`): material Hyper PLA Marmol, comprobado en el archivo guardado. No cambia la geometría.

## Cómo se hizo

Copia del generador de REV-002 con un solo parámetro cambiado (`wall_mm` 10 → 5), más la llamada al acabado por defecto. Diferencias respecto al original en `scripts/build_model.py`: identificadores de revisión, `wall_mm` y 3 líneas del material. Lanzador y validador compartidos de `herramientas/`.

## Validación (proceso Blender separado del de construcción)

- Envolvente 150,000021 × 150,000021 × 60,000002 mm, dentro de ±0,01 mm.
- Una componente cerrada y manifold, orientación coherente, sin elementos degenerados.
- Volumen medido 274.801,765 mm³; esperado 274.801,6 mm³ (diferencia 0,165 mm³, tolerancia 1 mm³). El esperado se calculó como en REV-001 y REV-002: cuerpo liso menos cavidad más 27.025,6 mm³ de relieve.

## Límite de esta validación

El validador base **no mide la cavidad ni las paredes por separado**: la pared de 5 mm se respalda por el volumen y por el parámetro del generador, no por planos interiores ni rayos como en REV-001 y REV-002. Falta ese control si se quiere equivalencia con las revisiones anteriores.

## Alcance

PASS del modelo digital en Blender 5.4.0 Alpha. No se exportó STL, no se usó Creality Print y no se imprimió. **Una pared de 5 mm con boquilla de 0,4 mm no se ha evaluado para impresión ni resistencia**; la medición física sigue siendo exigible en CU-01.

## Historial

Un solo build y una sola validación, ambos sin fallos. Sin intentos fallidos ni diagnósticos.

## Archivos

- `artifacts/CU01_REV003_planter_*.blend` — modelo.
- `evidencias/validation.json` — mediciones.
- `registro_artefactos.jsonl` — 10 artefactos sellados con `herramientas/sellar_carpeta.py`; verificación posterior sin diferencias.
- Run: `REV-003-20261103T033342Z`.
