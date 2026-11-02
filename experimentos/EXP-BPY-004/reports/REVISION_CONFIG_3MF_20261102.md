# Revisión complementaria del proyecto EXP-BPY-004

**Fecha:** 2026-11-02 15:35 UTC  
**Método:** lectura estática de los archivos de configuración dentro del archivo ZIP 3MF. No se guardó ni alteró el proyecto.  
**Proyecto:** `artifacts/EXP-BPY-004-20261102T121521-0300_slice_project.3mf`  
**SHA-256 observado:** `659b0890553a1e30087d3c6d329520179306767597938d45d705c3d919a2b5a4` (24.292 bytes).

## Valores serializados

`Metadata/project_settings.config` contiene:

- Impresora `Creality K1C`; perfil de máquina `Creality K1C 0.4 nozzle`; variante 0,4; diámetro 0,4 mm; volumen/nozzle `Standard`.
- `default_print_profile`: `0.20mm Standard @Creality K1C 0.4 nozzle`.
- Filamento `Hyper PLA @Creality K1C 0.4 nozzle`, vendor `Creality`, tipo `PLA`.
- Temperatura de boquilla 220 °C, primera capa 220 °C.
- Perfil de cama `High Temp Plate`; temperatura 50 °C para las capas iniciales y normales.
- Altura de capa y primera capa 0,20 mm.
- Cuatro paredes; relleno gyroid 18 %.
- Soportes apagados.
- Adhesión/brim `auto_brim`, ancho 5 mm.
- Velocidad exterior 200, interior 250, relleno disperso 270, primera capa 60, relleno primera capa 60, top surface 200 y travel 500 (unidades serializadas mm/s).
- `filament_flow_ratio=0.95`; caudal máximo volumétrico 23 mm³/s.

`Metadata/plate_1.json` registra caja XY de 80 × 60 mm y altura de capa 0,20 mm; el proyecto informa diámetro 0,4 mm. La orientación y 27 relieves se observaron visualmente en la sesión registrada, no se vuelven a acreditar por la lectura del JSON.

## Discrepancia y alcance

El informe/UI de la sesión previa identifica el proceso activo como `Macetero PLA 0.20mm K1C`, mientras que `default_print_profile` en el proyecto serializa `0.20mm Standard @Creality K1C 0.4 nozzle`. La evidencia disponible no establece si el campo `default_print_profile` refleja exactamente el proceso que generó el laminado, si el proyecto fue reabierto/actualizado con otro preset o si la etiqueta visual anterior describe una configuración personalizada equivalente. No se declara equivalencia ni se elige uno por suposición.

Las estimaciones de 37 min 20 s y 19,30 g / 6,47 m son observaciones registradas en el informe original. Este 3MF no proporciona, en las entradas examinadas, evidencia persistente suficiente para vincular esas estimaciones inequívocamente a uno de los dos nombres de proceso.

## Estado

La revisión confirma que el archivo 3MF conserva los parámetros enumerados, pero no resuelve la identidad efectiva del preset de proceso de la ejecución que produjo la estimación. EXP-BPY-004 permanece `INCONCLUSIVE`. Para resolverlo hace falta abrir una copia del proyecto en Creality Print, capturar el perfil activo y, si se relamina, guardar proyecto y resumen bajo una revisión nueva.
