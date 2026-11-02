# Protocolo — EXP-BPY-005

## Estado y alcance

Prueba de impresión física de una placa de ensayo, dependiente de resolución de EXP-BPY-004. La fase física está `NOT RUN`. No se realiza conexión ni control remoto de la Creality K1C.

## Artefacto

Modelo: placa de relieve EXP-BPY-003, revisión exportada `20261102T144300Z`.  
STL: `experimentos/EXP-BPY-003/artifacts/EXP-BPY-003-20261102T144300Z_relief_plate.stl`.  
SHA-256 aprobado: `c6342d689ef70742ae0f9b3d6bbbf32b4f0f542ef7a5b6be2645f3205755b3d3`.  
Dimensiones nominales: 80 × 60 × 5 mm; 27 ladrillos en relieve.

## Ficha de laminado disponible

Fuente de esta tabla: lectura estática de `Metadata/project_settings.config` dentro del 3MF guardado y observaciones consignadas en EXP-BPY-004. No es una captura nueva de la interfaz. Los datos serializados acreditan el contenido del proyecto guardado; no demuestran por sí solos qué controles estaban activos en pantalla al laminar.

| Campo | Valor encontrado | Estado/evidencia |
|---|---|---|
| Creality Print | 7.3.0.6157, arm64 | Registrado en EXP-BPY-004 |
| Impresora | Creality K1C | Confirmada expresamente por el usuario; proyecto `printer_model=Creality K1C` |
| Boquilla | 0,4 mm, `Standard` | Confirmada expresamente por el usuario; interfaz muestra `0.4-Standard` |
| Perfil de proceso serializado | `0.20mm Standard @Creality K1C 0.4 nozzle` | 3MF, clave `default_print_profile` |
| Perfil de proceso observado anteriormente | `Macetero PLA 0.20mm K1C` | Informe de EXP-BPY-004; personalizado, identidad frente al preset serializado sin resolver |
| Filamento de perfil | Creality Hyper PLA; tipo PLA | 3MF: `filament_settings_id`, `filament_vendor`, `filament_type` |
| Filamento físico cargado | Creality Hyper PLA | Confirmado expresamente por el usuario; perfil visible `Hyper PLA` |
| Temperatura de boquilla | 220 °C inicial y normal | 3MF: `nozzle_temperature_initial_layer`, `nozzle_temperature` |
| Cama | 50 °C inicial y normal | 3MF: temperaturas para `High Temp Plate`; UI mostró aviso de adhesivo |
| Altura de capa | 0,20 mm; primera capa 0,20 mm | 3MF y observación previa; 25 capas para 5 mm |
| Paredes | 4 (`wall_loops`) | 3MF |
| Relleno | 18 %, gyroid | 3MF |
| Velocidades | pared exterior 200; pared interior 250; relleno disperso 270; primera capa 60; relleno primera capa 60; superficie superior 200; viaje 500 mm/s | Valores serializados del 3MF; confirmar unidades/valor mostrado en UI antes de aceptar el job |
| Soportes | Desactivados (`enable_support=0`) | 3MF |
| Adhesión | `auto_brim`, ancho 5 mm; perfil de cama `Smooth PEI Plate / High Temp…` | Proyecto/interfaz; sigue visible el aviso “please apply glue before print”; decisión de adhesivo no asumida |
| Orientación | XY 80 × 60, Z 5 mm; base apoyada sobre cama según vista previa descrita | Importación y vista previa registradas; revisar al abrir proyecto |
| Tiempo estimado | 37 min 20 s | Observado en sesión anterior; no recalculado en esta revisión |
| Filamento estimado | 19,30 g; 6,47 m | Observado en sesión anterior; no recalculado en esta revisión |

Los ajustes serializados describen el proyecto; si al abrirlo Creality Print los valores difieren, no imprimir hasta investigar y registrar la discrepancia. No guardar cambios sobre el proyecto histórico: crear una copia nueva con identificador de ejecución.

## Confirmaciones humanas registradas — 2026-11-02

- Impresora física: Creality K1C.
- Boquilla instalada: 0,4 mm.
- Filamento físico cargado: Creality Hyper PLA.
- Superficie: cama original de Creality K1C.
- Tolerancia experimental aprobada: ±0,5 mm por eje para X, Y y Z.

Son declaraciones del usuario, no mediciones independientes del agente.

## Paso de control humano para el laminado

Antes de autorizar una preparación final:

1. Abrir una copia del proyecto 3MF en Creality Print 7.3.0.6157. Hecho para `EXP-BPY-004-20261102T154038Z`.
2. Confirmar K1C/0,4 y seleccionar `0.20mm Standard @Creality K1C 0.4 nozzle`. El perfil figura en el 3MF, pero la sesión muestra activo `Macetero PLA 0.20mm K1C`; el selector no abrió su lista. Pendiente de resolver antes de laminar.
3. Confirmar temperaturas, capa, paredes, relleno, velocidades, soportes y adhesión leyendo los valores activos en UI. Valores serializados documentados; comprobación UI completa pendiente.
4. Confirmar orientación, dimensiones y 27 relieves en vista previa por capas. Dimensiones y patrón visibles en Prepare; trayectorias no verificadas en una nueva ejecución porque aún no se laminó.
5. El usuario confirmó la cama original de la K1C. UI muestra `Smooth PEI Plate / High Temp…` y `please apply glue before print`. Registrar la decisión de adhesivo del usuario; no asumirla.
6. Filamento confirmado por el usuario: Creality Hyper PLA.
7. Persistir capturas de perfil, parámetros, capas y resultado. Las capturas CUA se observaron en la sesión, pero no existe una operación disponible para escribirlas en `evidencias/`; persistencia pendiente.
8. Presentar ficha y solicitar revisión humana antes de considerar aprobada la preparación de impresión.

La persona responsable decide e inicia la impresión manualmente y permanece supervisándola. No conectar, enviar, ni iniciar la K1C desde este agente.

## Registro durante la impresión

Usar `REGISTRO_IMPRESION.md`. Anotar comienzo/fin, incidencias y estado real, sin estimar lo no medido. Guardar fotos sin edición engañosa y con escala/contexto cuando sea posible.

## Medición y aceptación

Usar `MEDICIONES_FISICAS.md` y `EVALUACION_CALIDAD.md`. Tolerancia experimental aprobada por el usuario: **±0,5 mm por eje en X, Y y Z** para este cupón; no es un estándar universal de K1C. Registrar instrumento, resolución, exactitud declarada y verificación de cero. Si no puede discriminar el umbral, informar la limitación.

Para Z registrar tanto el espesor de base en zona sin relieve como el espesor total desde la cara de apoyo hasta la cima de los ladrillos, con medidas en distintos puntos. La comparación nominal de 5 mm es el espesor total.

## Resultados y cierre

Hasta recibir evidencia del usuario, imprimir = `NOT RUN`; mediciones físicas = `NOT RUN`; resultado global = `NOT RUN`; cierre de Fase 1 = `PENDIENTE_VALIDACION_FISICA`. Un resultado de laminado no equivale a resultado físico.
