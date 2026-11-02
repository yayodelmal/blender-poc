# Configuración observada del laminado

**run_id:** `EXP-BPY-004-20261102T121521-0300`  
**Aplicación:** Creality Print 7.3.0.6157 (arm64)  
**Impresora:** `Creality K1C`  
**Boquilla:** `0.4-Standard`  
**Proceso activo:** `Macetero PLA 0.20mm K1C` (preset personalizado; correspondencia con perfil estándar no verificada)  
**Filamento activo:** `Hyper PLA`  
**Cama:** texto visible truncado `Smooth PEI Plate / Hig...`; no se completa por inferencia.

## Valores observados directamente

| Parámetro | Valor mostrado |
|---|---:|
| Altura de capa | 0,20 mm |
| Altura primera capa | 0,20 mm |
| Ancho de línea por defecto | 0,42 mm |
| Ancho de línea primera capa | 0,50 mm |
| Ancho de pared externa | 0,42 mm |
| Ancho de pared interna | 0,45 mm |
| Ancho de superficie superior | 0,42 mm |
| Ancho de relleno disperso | 0,45 mm |
| Ancho de relleno sólido interno | 0,42 mm |
| Ancho de línea de soporte | 0,42 mm |
| Capas/resultante | 25 capas; Z=5,00 mm |
| Tiempo estimado | 37 min 20 s |
| Filamento estimado | 19,30 g; 6,47 m |
| Coste calculado por la aplicación | 0,58; moneda no verificada |

## No observados o no documentados

Temperatura de boquilla, temperatura de cama, número de paredes, porcentaje/patrón de relleno, velocidades por tipo de trayectoria, estado y cantidad de soportes, brim/adhesión, estrategia de costura y todos los avisos del laminador. No se completan esos datos con valores genéricos.

En la cama apareció el texto `please apply glue before print`; se conserva literalmente como aviso mostrado. No se validó adhesión física.

## Evidencia

La observación fue visual en Creality Print tras laminar. El proyecto se guardó como `artifacts/EXP-BPY-004-20261102T121521-0300_slice_project.3mf`. La interfaz CUA de esta ejecución no permitió persistir capturas de pantalla; no se presentan capturas inexistentes.
# Configuración del laminado — run `EXP-BPY-004-20261102T155417Z`

Estado final EXP-BPY-004: `PASS`. La captura persistente verifica la barra completa de 1 / Z=0,20 mm a 25 / Z=5,00 mm y las trayectorias. El run intermedio anotó capa 20 / Z=4,00 mm como posición seleccionada; se conserva esa lectura histórica y queda explicada por el deslizador.

| Ajuste | Valor observado/guardado |
|---|---|
| Aplicación | Creality Print 7.3.0.6157 arm64 |
| Impresora | Creality K1C |
| Boquilla | 0.4-Standard (0,4 mm) |
| Superficie | Smooth PEI Plate / High Temp; gráfica Creality Smooth PEI Plate |
| Filamento | Hyper PLA (tipo PLA) |
| Proceso activo en interfaz | 0.20mm Standard @Creality K1C 0.4 nozzle |
| Boquilla / primera capa | 220 / 220 °C |
| Cama / primera capa | 50 / 50 °C |
| Altura de capa / primera capa | 0,20 / 0,20 mm |
| Paredes | 2 |
| Relleno | grid, 15 % |
| Soportes | desactivados |
| Adhesión | brim automático, 5 mm |
| Velocidades (mm/s, ajustes serializados) | exterior 200; interior 250; relleno 270; primera capa 60; relleno primera capa 60; superficie superior 200; viaje 500 |
| Estimación de laminador | 30 min 36 s; 14,45 g; 4,84 m |
| Lectura inicial del control | 20 / Z=4,00 mm, posición seleccionada (historial conservado) |
| Rango de capas verificado | 1 / Z=0,20 mm hasta 25 / Z=5,00 mm, evidencia en captura persistente |
| Aviso | please apply glue before print |

Fuente de valores serializados: `artifacts/EXP-BPY-004-20261102T155417Z_slice_project.3mf`, `Metadata/project_settings.config`. Evidencia de la selección y Preview observada en la sesión de Creality Print; no hay captura persistente. La miniatura del proyecto se conserva en `evidencias/EXP-BPY-004-20261102T155417Z_project_thumbnail.png` y solo muestra la pieza, no el laminado.

El usuario explica que el control inicial mostraba una posición intermedia; la captura incorporada confirma el máximo de 25 / Z=5,00 mm, perfil Standard, material, estimaciones y patrón de trayectorias. El manual oficial de K1C indica limpiar o recubrir con adhesivo la cara A de PEI lisa por su susceptibilidad al aceite/sudor. Antes de imprimir, comprobar qué superficie está montada y su limpieza; no se comprobó físicamente aquí.

No se envió el trabajo ni se inició impresión. EXP-BPY-004 queda `PASS`; la impresión física requiere revisión del usuario y comprobación presencial de la cama.

