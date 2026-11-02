# EXP-BPY-004 — Resultado

**Estado global: PASS**  
**run_id:** `EXP-BPY-004-20261102T121521-0300`  
**Fecha:** 2026-11-02 (America/Santiago)

> **Histórico preservado:** la primera ejecución queda documentada sin cambios en las secciones siguientes. Las repeticiones de 15:40 y 15:54 son runs adicionales; ninguna reemplaza resultados o hashes históricos.

## Resumen

Creality Print 7.3.0.6157 (Apple Silicon arm64) importó la copia verificada del STL y la laminó en una sesión gráfica supervisada. La interfaz identificó Creality K1C y boquilla `0.4-Standard`; mostró 80 × 60 × 5 mm, 478 triángulos y un volumen de 22.879,2 mm³. En vista previa, a Z=5 mm, se distinguió el patrón alternado completo de ladrillos (27 huellas: filas de 5 y 4 alternadas); a Z=4 mm se observó la transición del relieve sobre la base. El laminador completó el cálculo y estimó 37 min 20 s, 19,30 g y 6,47 m de filamento. No se envió el trabajo ni se inició impresión.

El resultado global queda `INCONCLUSIVE` porque la sesión ya traía seleccionado un proceso personalizado llamado **“Macetero PLA 0.20mm K1C”** y filamento **“Hyper PLA”**. No se verificó que ese proceso personalizado equivalga a un perfil PLA estándar de Creality, y no se pudo documentar el conjunto completo de temperaturas, paredes, relleno, velocidades, soportes y adhesión desde el perfil efectivo. La placa también mostraba el aviso del laminador “please apply glue before print”. La preparación digital se ejecutó, pero no satisface todavía la trazabilidad de configuración pedida para aprobar el experimento.

## Resultados por criterio

| Verificación | Estado | Evidencia/nota |
|---|---|---|
| STL original coincide con manifiesto | PASS | 23.984 bytes; SHA-256 `c6342d689ef70742ae0f9b3d6bbbf32b4f0f542ef7a5b6be2645f3205755b3d3`. |
| Copia experimental coincide con original | PASS | Mismo tamaño y SHA-256. |
| Creality Print disponible/versionado | PASS | 7.3.0.6157, ejecutable arm64. |
| Importación | PASS | La interfaz mostró nombre de copia, dimensiones, volumen y triángulos. |
| Perfil K1C y boquilla 0,4 mm | PASS | Interfaz: `Creality K1C`; `0.4-Standard`. |
| Dimensiones tras importar | PASS | La interfaz mostró 80 × 60 × 5,00 mm. |
| Material/proceso requerido | INCONCLUSIVE | Filamento observado `Hyper PLA`; proceso `Macetero PLA 0.20mm K1C` es personalizado. No se estableció si existe/está seleccionado el perfil estándar de PLA solicitado. |
| Laminado completado | PASS | Creality Print pasó a `Preview` y mostró resumen de G-code. No se observó un diálogo de error bloqueante. |
| 27 relieves en trayectorias | PASS (inspección visual) | En la capa superior se vieron filas alternadas de 5 y 4 huellas; en Z=4,00 mm el patrón se distinguía sobre las trayectorias de la base. Conteo visual, no extracción automatizada. |
| Base/capas coherentes | PASS (inspección visual) | Base continua visible; 25 capas, altura de capa 0,20 mm; Z final mostrado 5,00 mm. |
| Advertencias revisadas | INCONCLUSIVE | Se observó la indicación de cama `please apply glue before print`; no se recopiló un inventario completo de avisos del slicer. |
| Configuración efectiva completa registrada | INCONCLUSIVE | Se capturaron algunos campos visibles; faltan temperaturas, número de paredes, densidad de relleno, velocidades detalladas y soportes/adhesión. |
| Evidencia gráfica persistente | INCONCLUSIVE | La inspección visual ocurrió en la interfaz; no se consiguió guardar capturas mediante la interfaz de control disponible. El proyecto 3MF se guardó. |
| Maestro y STL fuente intactos | PASS | Hash final del STL original igual al aprobado; hash de la copia igual. No se editó el maestro. |
| Envío/impresión física | PASS | No se pulsó `Send print`, no se conectó ni controló una impresora, no se imprimió. |

## Tiempos y consumo estimados por el laminador

- Tiempo: **37 min 20 s**.
- Filamento: **19,30 g**, **6,47 m**.
- Coste mostrado por la aplicación: **0,58** (moneda no verificada; no se interpreta como cotización).
- Capas: **25**, con altura nominal observada **0,20 mm** y Z final **5,00 mm**.

## Avisos y limitaciones

- La cama configurada se mostraba como `Smooth PEI Plate / Hig...` y la escena incluía el mensaje `please apply glue before print`. Se registra como aviso de preparación superficial del perfil seleccionado; no se comprobó adhesión física.
- Se usó el preset que ya aparecía seleccionado. No se guardó ni modificó un perfil global ni se alteraron parámetros manualmente.
- El valor `Hyper PLA` es lo que la aplicación mostraba como filamento; no se verificaron fabricante, lote ni propiedades físicas del material.
- El éxito del laminado y la presencia de trayectorias no validan impresión física, adhesión, acabado ni resistencia.
- No se exportó G-code. Se guardó el proyecto 3MF local para conservar el estado del laminador.
- Las vistas y los valores de la interfaz no se archivaron como capturas; las observaciones constan en `logs/ui_observaciones.txt` y en este informe.

## Recomendación histórica de la primera ejecución

Esta recomendación corresponde a la ejecución inicial y queda superada por el run final Standard documentado abajo.

## Run adicional: `EXP-BPY-004-20261102T155417Z`

La repetición se hizo desde una copia nueva de la configuración Standard preservada tras INC-BPY-002. El preflight confirmó el hash esperado tanto para el 3MF de custodia (`1a67df...d50f`) como para el STL aprobado (`c6342d...b3d3`). Creality Print 7.3.0.6157 mostró el preset Standard activo; la laminación concluyó y el resumen mostró 30m36s, 14,45 g y 4,84 m. La vista previa mostró el patrón de 27 ladrillos y persistió el aviso `please apply glue before print`.

La configuración guardada registra 220 °C de boquilla, 50 °C de cama, 0,20 mm, dos paredes, grid al 15 %, soportes desactivados, brim automático de 5 mm y velocidades según el manifiesto. En una inspección intermedia, la posición seleccionada del deslizador indicaba capa 20 / Z=4,00 mm; la malla mide 80,0000076 × 60,0000038 × 5,00000048 mm. La captura incorporada confirma que la barra llega hasta capa 25 / Z=5,00 mm. Se conserva la lectura intermedia como historial, no como altura final. El 3MF no incluye G-code.

El usuario aclaró que el control mostraba la posición del deslizador, no su extremo, y reportó una captura donde la última capa es 25 / Z=5,00 mm. La captura ya está guardada en `evidencias/`, se inspeccionó visualmente y se registró su SHA-256 en el manifiesto. El run final cumple los criterios de validación digital y el resultado global es `PASS`. No se tocó `Send print`; no hubo conexión ni impresión física.
