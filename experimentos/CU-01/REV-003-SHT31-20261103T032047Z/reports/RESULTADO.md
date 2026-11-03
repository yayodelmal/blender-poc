# CU-01 REV-003 — Soporte removible para SHT31

**Resultado: PASS para validación geométrica digital independiente.** Se añadió a una copia de REV-002 un soporte separado y removible para la placa SHT31. La geometría de la maceta coincide con la fuente; las revisiones anteriores siguen intactas.

## Diseño

- Broche en U escalonado sobre la pared norte: canal nominal de 10,6 mm para la pared de 10 mm; holgura digital de 0,1 mm en el lado interior y 0,5 mm respecto al relieve exterior.
- Las patas del broche bajan 11,1 mm desde el borde. El montante eleva la parte superior de la cuna a z=90 mm, 30 mm sobre el borde de la maceta.
- Cuna abierta por detrás, orientada en paisaje para una placa aproximada de 13,1 × 10,4 mm. Deja libre una zona frontal central para el sensor y un corredor posterior para los pines.
- La maceta y el soporte son dos objetos MESH distintos. Ambos usan el material predeterminado Hyper PLA Marmol.

## Validación digital

La validación se ejecutó en un proceso Blender separado del constructor. Confirmó:

- Malla de la maceta idéntica a la de REV-002 y envolvente de 150 × 150 × 60 mm dentro de ±0,01 mm.
- Soporte en una componente cerrada, manifold y de volumen positivo.
- Extremo superior del soporte a 30 mm sobre el borde.
- Cero pares de triángulos intersectados entre el soporte y la maceta.
- Zona frontal central y corredor posterior digital libres según las áreas de resguardo definidas en el validador.
- Hyper PLA Marmol asignado a ambos objetos.

La evidencia completa está en `evidencias/validation_final.json`; los comandos, versiones, perfiles aislados y códigos de salida están en `logs/`.

## Límites

Las dimensiones 10,4 × 13,1 mm provienen de la imagen de referencia y son aproximadas. No se proporcionó espesor de placa ni altura/proyección de los pines; la cuna usa 1,6 mm como supuesto. La validación de los pines se limita a un corredor digital y no modela la placa o el header real. Este PASS no confirma el encaje físico, la flexión o retención del broche ni resistencia de impresión.

No se exportó STL, no se usó Creality Print y no se imprimió.

## Archivos

- `artifacts/CU01_REV003_SHT31_clip_support_20261103T032047Z.blend` — maceta y soporte como objetos separados.
- `evidencias/overview_final.png` y `evidencias/detail_final.png` — vistas de referencia.
- `evidencias/validation_final.json` — mediciones y controles.
- `registro_artefactos.jsonl` — huellas verificables de entradas, generadores, modelo, validación, logs y vistas.
