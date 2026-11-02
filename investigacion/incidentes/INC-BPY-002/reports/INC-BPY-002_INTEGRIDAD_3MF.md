# INC-BPY-002 — Sobrescritura de proyecto 3MF durante la selección de perfil

**Estado:** contenido actual preservado; ningún archivo restaurado.  
**Fecha de revisión:** 2026-11-02 15:51 UTC.  
**Experimento en pausa:** EXP-BPY-004 y EXP-BPY-005.  
**Alcance:** inspección de archivos locales, hashes y contenido estático del 3MF. No se laminó ni se envió a la impresora.

## Resumen del incidente

El archivo alterado es la copia de trabajo creada para la repetición de EXP-BPY-004:

`experimentos/EXP-BPY-004/artifacts/EXP-BPY-004-20261102T154038Z_working_copy.3mf`

El manifiesto previo registraba esa copia con 24.292 bytes y SHA-256 `659b0890553a1e30087d3c6d329520179306767597938d45d705c3d919a2b5a4`. El archivo actual tiene 23.873 bytes y SHA-256 `1a67df633765254308be33262862609f78e0520b405a95fb7593dc0c6d42d50f`. Su modificación local figura a las 12:50:04 -0300 del 2026-11-02.

La copia 3MF actual se preservó sin alteraciones en:

`investigacion/incidentes/INC-BPY-002/evidencias/EXP-BPY-004_working_copy_CURRENT_20261102T155123Z.3mf`

La copia de evidencia mide 23.873 bytes y su SHA-256 es también `1a67df633765254308be33262862609f78e0520b405a95fb7593dc0c6d42d50f`.

## Comparación con el artefacto histórico

El proyecto original de EXP-BPY-004 no fue sobrescrito:

| Archivo | Tamaño actual | Hash actual | Hash registrado | Estado |
|---|---:|---|---|---|
| `...121521-0300_slice_project.3mf` | 24.292 bytes | `659b0890553a1e30087d3c6d329520179306767597938d45d705c3d919a2b5a4` | Igual | `MATCH` |
| `...154038Z_working_copy.3mf` | 23.873 bytes | `1a67df633765254308be33262862609f78e0520b405a95fb7593dc0c6d42d50f` | `659b0890553a1e30087d3c6d329520179306767597938d45d705c3d919a2b5a4` | `MISMATCH — ALTERADO` |
| Copia de custodia del estado actual | 23.873 bytes | `1a67df633765254308be33262862609f78e0520b405a95fb7593dc0c6d42d50f` | Creada durante este incidente | `MATCH` con archivo actual |

El working copy había sido registrado con el mismo hash que el proyecto original antes de la sobrescritura. Por ello, su estado binario anterior está representado íntegramente por el proyecto histórico intacto. No se reemplazó el working copy por ese archivo.

## Perfil y parámetros guardados en el 3MF actual

La lectura estática de `Metadata/project_settings.config` en la copia preservada muestra:

- `default_print_profile`: `0.20mm Standard @Creality K1C 0.4 nozzle`.
- Impresora: `Creality K1C`; perfil `Creality K1C 0.4 nozzle`; boquilla `0.4` / `Standard`.
- Filamento: `Hyper PLA @Creality K1C 0.4 nozzle`, tipo `PLA`.
- Temperaturas serializadas: boquilla 220 °C; cama 50 °C.
- Altura de capa: 0,20 mm.
- Paredes: 2; relleno: 15 %, patrón `grid`; soportes desactivados; brim automático de 5 mm.

La diferencia de paredes y relleno respecto de la configuración personalizada previamente observada (4 paredes, 18 % gyroid) es consistente con el cambio solicitado al preset Standard. La etiqueta `default_print_profile` y estos valores confirman que el **proyecto guardado contiene configuración Standard**. No se afirma equivalencia con una configuración de fábrica verificada externamente ni se ha comprobado el panel de la interfaz después de guardar.

El archivo contiene una geometría de 241 vértices y 478 triángulos con límites aproximados 80 × 60 × 5 mm. No contiene entradas `.gcode` ni `Metadata/plate_1.json`; `Metadata/slice_info.config` solo identifica Creality Print 7.3.0.6157. Por lo tanto, este archivo acredita el proyecto y sus ajustes, pero no aporta una salida de laminado nueva, una vista previa persistente de trayectorias ni nuevas estimaciones de impresión.

## STL aprobado

El STL fuente de EXP-BPY-003 sigue intacto: 23.984 bytes, SHA-256 `c6342d689ef70742ae0f9b3d6bbbf32b4f0f542ef7a5b6be2645f3205755b3d3`. La copia de entrada de EXP-BPY-004 también está registrada con ese mismo hash. No se escribieron en ellos.

## Búsqueda de copias recuperables

La búsqueda se limitó a `experimentos/EXP-BPY-004`, `experimentos/EXP-BPY-005` y registros del incidente. Se encontraron dos 3MF relevantes:

1. El proyecto histórico `...121521-0300_slice_project.3mf`, que coincide exactamente con el hash previo del working copy y permanece intacto.
2. El working copy actual `...154038Z_working_copy.3mf`, ahora con configuración Standard, preservado en `evidencias/`.

No se encontraron otros `.3mf`, snapshots, `.bak` ni copias `~` en esos directorios. No se consultó historial de versiones externo, Time Machine ni almacenamiento en nube.

## Qué cambió y qué se conserva

- **Cambió:** el working copy `...154038Z_working_copy.3mf` fue guardado con contenido distinto al hash anotado en el manifiesto.
- **Se conserva:** el estado Standard guardado, en su ruta actual y en una copia de custodia independiente con hash verificado.
- **Se conserva:** el estado binario anterior del working copy en el proyecto original `...121521-0300_slice_project.3mf`, que ya tenía el mismo hash antes de la repetición.
- **No se perdió:** el artefacto maestro del proyecto original de EXP-BPY-004 ni el STL aprobado.
- **No se hizo:** restauración, reescritura de hashes históricos, nuevo laminado, envío o impresión.

## Continuación segura

Mantener congelados tanto el proyecto histórico como la copia de custodia. Para continuar EXP-BPY-004, crear otra copia nueva del 3MF con perfil Standard ya guardado, verificar su hash y laminar solamente esa copia en un run nuevo. Guardar el 3MF resultante de ese run con nombre nuevo y persistir las capturas de perfil, Preview y resumen. EXP-BPY-005 permanece `NOT RUN`; Fase 1 permanece `PENDIENTE_VALIDACION_FISICA`.
