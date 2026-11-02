# EXP-BPY-004

Validación supervisada de importación y laminado del relieve EXP-BPY-003 en Creality Print. No se realizó impresión física.

## Artefactos

- Entrada aprobada, copia de trabajo: `artifacts/EXP-BPY-004-20261102T121521-0300_input.stl`
- Proyecto local de Creality Print: `artifacts/EXP-BPY-004-20261102T121521-0300_slice_project.3mf`
- Resultado: `reports/RESULTADO.md`
- Configuración observada: `reports/CONFIGURACION_LAMINADO.md`
- Manifiesto de integridad: `MANIFIESTO_ARTEFACTOS.json`
- Inventario, preflight y observaciones UI: `logs/`

## Reproducción

1. Confirmar el hash del STL original en `MANIFIESTO_ARTEFACTOS.json`.
2. Abrir la copia experimental con Creality Print 7.3.0.6157.
3. Seleccionar/confirmar K1C y boquilla 0,4 mm, registrar perfil de proceso y material realmente activos.
4. Laminar localmente y revisar capas superiores y la transición del relieve.
5. Guardar el proyecto 3MF en `artifacts/`.
6. Verificar de nuevo el hash del original y de la copia.

Esta ejecución utilizó el proceso que ya estaba activo (`Macetero PLA 0.20mm K1C`) y `Hyper PLA`; al ser personalizado y faltar varios parámetros efectivos, su resultado es `INCONCLUSIVE`. No se debe interpretar como aprobación de un perfil estándar ni como validación física.

No pulsar `Send print` ni conectar una impresora durante esta prueba.
# Run Standard `EXP-BPY-004-20261102T155417Z`

La repetición más reciente está descrita en `reports/REPETICION_20261102T155417Z.md`. Usa copias nuevas del STL aprobado y del 3MF Standard de custodia, conserva el proyecto laminado en `artifacts/EXP-BPY-004-20261102T155417Z_slice_project.3mf` y registra ajustes/resultados en el manifiesto. No se envió el trabajo a la K1C.

Estado: `INCONCLUSIVE`, porque el Preview mostró capa 20/Z=4,00 mm frente a 5,00 mm de altura del modelo, y no se pudo guardar una captura persistente de trayectorias. El thumbnail que se extrajo del 3MF solo documenta el modelo. Ver el manifiesto y `logs/run_20261102T155417Z.txt` antes de continuar.

