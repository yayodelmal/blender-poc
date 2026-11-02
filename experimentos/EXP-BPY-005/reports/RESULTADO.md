# EXP-BPY-005 — Resultado provisional

**Resultado de impresión:** `NOT RUN`  
**Preparación:** perfil Standard no está seleccionado/verificado; no se repitió el laminado.  
**Cierre de Fase 1:** `PENDIENTE_VALIDACION_FISICA`.

## Actualización de laminado Standard (2026-11-02)

Un run adicional `EXP-BPY-004-20261102T155417Z` confirmó el preset Standard en la interfaz y laminó una copia del proyecto. La configuración efectiva serializada es K1C/0,4 mm, Hyper PLA, 220/50 °C, capa 0,20 mm, dos paredes, grid al 15 %, soportes apagados y brim automático de 5 mm. Estimaciones nuevas: 30 min 36 s, 14,45 g y 4,84 m. Se vio el aviso `please apply glue before print`.

La preparación para impresión sigue pendiente de recibir la captura como archivo verificable. El usuario aclaró que Preview mostraba un punto intermedio del deslizador (capa 20 / Z=4,00 mm) y reportó que el extremo es capa 25 / Z=5,00 mm. Se conserva la observación previa; la explicación está registrada como declaración hasta verificar la captura. El aviso de adhesivo es una recomendación para preparar la cama, no un error de laminado conocido. El manual oficial indica que la cara A de PEI lisa es sensible a aceite/sudor y debe limpiarse o recubrirse con adhesivo; antes de imprimir hay que identificar la superficie física montada y confirmar su limpieza ([manual oficial K1C, sec. 5.2.2](https://wiki.creality.com/products/fully-enclosed/k1c-2025/%E5%A4%9A%E8%AF%AD%E7%A7%8D%E8%AF%B4%E6%98%8E%E4%B9%A6/k1c-sm-001_user_manual%28en%29.pdf)). No se inspeccionó físicamente la cama. No se envió ni inició impresión; resultado de EXP-BPY-005: `NOT RUN`; cierre Fase 1: `PENDIENTE_VALIDACION_FISICA`.

### Ficha de laminado reportada para revisión (no aprobada todavía)

Creality Print 7.3.0.6157; K1C, boquilla 0,4 mm, Hyper PLA, Smooth PEI Plate / High Temp; perfil Standard 0.20mm; boquilla/cama 220/50 °C; capas 0,20 mm; 2 paredes; grid 15 %; soportes desactivados; brim automático 5 mm. El usuario reporta última capa 25 / Z=5,00 mm, tiempo 30m36s, material 14,45 g / 4,84 m y 27 relieves visibles. Falta incorporar la captura para hacer persistente esa evidencia. El usuario confirma material físico y cama original y mantiene aprobada la tolerancia experimental ±0,5 mm por eje. La advertencia `please apply glue before print` debe tratarse con la comprobación de limpieza/superficie del protocolo; no se ha inspeccionado la cama físicamente.

## Verificaciones de esta etapa

| Comprobación | Estado | Evidencia |
|---|---|---|
| STL aprobado presente y tamaño 23.984 bytes | PASS | Inspección de solo lectura, 2026-11-02 |
| SHA-256 STL coincide con EXP-BPY-003 | PASS | `c6342d689ef70742ae0f9b3d6bbbf32b4f0f542ef7a5b6be2645f3205755b3d3` |
| Copia EXP-BPY-004 coincide con STL aprobado | PASS | Mismo tamaño y hash |
| 3MF existente y hash coincide con manifiesto | PASS | 24.292 bytes; `659b0890553a1e30087d3c6d329520179306767597938d45d705c3d919a2b5a4` |
| Configuración serializada legible | PASS | `Metadata/project_settings.config` leído sin ejecutar componentes del archivo |
| Perfil del proceso inequívoco entre UI y 3MF | INCONCLUSIVE | Informe UI anterior dice `Macetero PLA 0.20mm K1C`; 3MF serializa `0.20mm Standard @Creality K1C 0.4 nozzle` |
| Valores efectivos revisados en sesión gráfica actual | INCONCLUSIVE | UI confirma impresora/boquilla/filamento/cama/dimensiones; el preset y los ajustes completos siguen sin comprobarse |
| Filamento físico y perfil Hyper PLA | PASS (confirmación humana + UI) | El usuario confirmó Hyper PLA cargado; la interfaz muestra Hyper PLA |
| Confirmaciones humanas de impresora, boquilla, filamento, cama y tolerancia | PASS (declaración recibida) | K1C, 0,4 mm, Creality Hyper PLA, cama original y ±0,5 mm por eje; no equivalen a medición independiente |
| Abrir copia de proyecto en Creality Print | PASS | `EXP-BPY-004-20261102T154038Z_working_copy.3mf` abierta; hash igual al proyecto anterior |
| Seleccionar el preset Standard | BLOCKED | UI mantiene `Macetero PLA 0.20mm K1C`; el control del preset no abrió su lista. No se asumió el cambio |
| Nuevo laminado y nuevas estimaciones | NOT RUN | Detenido antes de `Slice plate` para no producir resultado con preset no confirmado |
| Capturas persistentes en el repositorio | BLOCKED | Capturas CUA observadas en la sesión; API disponible no expone guardado de bytes a archivo |
| Impresión física | NOT RUN | No iniciada; debe iniciarla y supervisarla el usuario |

## Configuración que serializa el proyecto

K1C, boquilla 0,4 mm Standard, perfil `0.20mm Standard @Creality K1C 0.4 nozzle`, filamento Creality Hyper PLA (tipo PLA), boquilla 220 °C, cama High Temp Plate 50 °C, capa 0,20 mm, cuatro paredes, relleno gyroid 18 %, soportes desactivados y brim automático de 5 mm. Velocidades guardadas: exterior 200, interior 250, relleno disperso 270, primera capa 60, relleno de primera capa 60, superficie superior 200, viaje 500 mm/s.

La interfaz en la ejecución anterior mostró un preset de proceso personalizado distinto. Esa discrepancia impide afirmar qué preset produjo el G-code asociado al resumen de 37 min 20 s / 19,30 g. Las cifras siguen siendo estimaciones históricas de laminador, no métricas físicas.

## Matriz de trazabilidad

| Requerimiento | Experimento | Evidencia | Resultado | Limitación |
|---|---|---|---|---|
| Crear y reabrir geometría | EXP-BPY-001 | Informe, scripts, logs y `.blend`; hash actual verificado `a5f0aa70…ecbc3` | PASS | Blender 5.4.0 Alpha, no versión estable |
| Editar estado, persistir y recuperar | EXP-BPY-002 | Informe, snapshots y manifest; revisión B hash `08a85ae9…a194` verificado | PASS | Solo cupo geométrico simple; mismo entorno Alpha |
| Relieve real, malla y STL | EXP-BPY-003 | Informe/manifest; maestro hash `09f7ee7c…8495b`, STL hash completo arriba | PASS | Validación digital del proxy, no laminado/fabricación |
| Importar, configurar y laminar en Creality Print | EXP-BPY-004 | Informe histórico, proyecto 3MF, repetición UI y log | INCONCLUSIVE | Preset Standard no se pudo seleccionar; no hubo nuevo slice y faltan capturas persistentes de preview |
| Pieza física conforme | EXP-BPY-005 | Plantillas creadas; sin fotos ni mediciones | NOT RUN | Espera resolución de perfil, aprobación humana y evidencia física |

## Criterio de avance

Para continuar EXP-BPY-004: seleccionar manualmente en Creality Print el perfil Standard indicado, confirmar que el preset cambia y aportar evidencia persistente o dejar la aplicación en ese estado para volver a verificar; después revisar parámetros, laminar y guardar una copia nueva. La persona responsable debe decidir sobre adhesivo ante el aviso. La tolerancia física de ±0,5 mm por eje ya fue aprobada por el usuario.

Una vez recibida evidencia de impresión, completar los registros. No se cierra Fase 1 por la preparación documental.

## Estado posterior a la aclaración de Preview

El usuario reporta que la vista previa llega a capa 25 / Z=5,00 mm, con 27 relieves visibles, y aclara que la lectura 20 / Z=4,00 mm anotada en el run era la posición actual del deslizador. Se conserva esa observación antigua como historial. El perfil Standard y la configuración efectiva están respaldados por el proyecto 3MF guardado y por las observaciones de la interfaz del run. El STL vuelve a coincidir con el hash aprobado.

La captura descrita no está disponible en los archivos de esta sesión. Se necesita adjuntarla para incorporarla a `experimentos/EXP-BPY-004/evidencias/`, calcular su SHA-256 y cerrar la verificación persistente. Por ello la ficha siguiente es para revisión humana, pero todavía no se considera aprobada para imprimir:

| Campo | Configuración reportada/registrada |
|---|---|
| Impresora / boquilla | Creality K1C / 0,4 mm (`0.4-Standard`) |
| Perfil / filamento | `0.20mm Standard @Creality K1C 0.4 nozzle` / Creality Hyper PLA |
| Superficie | `Smooth PEI Plate / High Temp`; el usuario confirma cama original K1C |
| Temperaturas | Boquilla 220 °C; cama 50 °C |
| Capas / paredes / relleno | 0,20 mm / 2 / grid 15 % |
| Soportes / brim | Soportes desactivados / automático 5 mm |
| Modelo / Preview | 80 × 60 × 5 mm; usuario reporta capa máxima 25 / Z=5,00 mm y patrón de 27 ladrillos |
| Estimación | 30 min 36 s; 14,45 g / 4,84 m |
| Advertencia | `please apply glue before print`: revisar superficie física, confirmar que corresponda a cara lisa PEI y que esté limpia; seguir manual/perfil aplicable y decisión del operador |

El usuario ya aprobó ±0,5 mm por eje para medición física y confirmó Hyper PLA y cama original. No se envió ni inició impresión: EXP-BPY-005 continúa `NOT RUN`; Fase 1 `PENDIENTE_VALIDACION_FISICA`.
