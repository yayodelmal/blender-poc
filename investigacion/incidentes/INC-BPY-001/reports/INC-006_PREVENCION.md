# INC-006 — Prevención mínima de divergencias

## Registro por revisión

Para cada archivo aceptado, guardar un manifiesto local pequeño (Markdown o JSON) con:

| Campo | Valor que debe capturarse |
|---|---|
| revision_id | ID único e inmutable de la revisión |
| artifact_path | Ruta exacta del archivo, sin alias ambiguos |
| sha256 / size_bytes | Huella completa y tamaño del mismo archivo |
| blender | Versión completa, branch/build hash, arquitectura y ruta del ejecutable |
| generator_script | Ruta y SHA-256 del script que produjo esa revisión |
| parameters_expected | Parámetros, unidades y contrato/invariantes |
| measurements_observed | Valores medidos, tolerancia, método, objeto/mesh ID |
| validation_state | PASS/FAIL/INCONCLUSIVE/NOT RUN por check |
| accepted_at / accepted_by | Timestamp con offset y actor responsable |

## Momento de sellado

Calcular tamaño y SHA-256 **después** de que el proceso generador termine, verificar código de salida, cerrar el archivo y calcular la huella del path final que se entregará. Repetir el hash después de la reapertura de validación y comparar contra el valor sellado. El validador debe ser de solo lectura y no guardar. Asociar cada hash a ruta e ID explícitos en la misma línea de salida; no copiar valores entre runs.

Registrar el manifiesto junto al artefacto, pero mantener el artefacto aceptado inmutable. Cualquier cambio crea un archivo/revisión nueva con su propio hash; no actualizar el archivo aprobado in-place. El snapshot se copia, se hashea y se reabre/verifica antes de mutar una copia de trabajo.

## Integridad operativa

- Usar nombres únicos con revision ID, sin reutilizar nombres ni aceptar `overwrite`.
- Si es práctico, almacenar maestros como artefactos content-addressed o en directorio de solo lectura de trabajo; los permisos ayudan contra accidentes, pero no son una garantía criptográfica ni sustituyen controles de proceso.
- Mantener resultados de generación, validación y checksum en logs separados con horas UTC y local offset.
- En el reporte final, insertar el manifest de la revisión como referencia única; no volver a teclear hash/tamaño desde otra ejecución.
- Revisar que el SHA calculado corresponda exactamente al path del `run_id` incluido en el informe.

No se implementó este mecanismo. Los informes históricos de EXP-BPY-001 y EXP-BPY-002 se conservaron sin cambios.
