# EXP-BPY-001 — Codex + Blender local con bpy

Resultado más reciente: **PASS en Blender 5.4.0 Alpha**, ID EXP-BPY-001-20261102T105936-0300. Blender 5.2.3 LTS falló en background con Metal; se conserva esa evidencia y las ejecuciones anteriores. El run Alpha aislado generó el cubo, guardó el .blend y lo reabrió en un proceso independiente. Ver reports/RESULTADO.md.

## Ejecución registrada

- ID PASS: EXP-BPY-001-20261102T105936-0300
- Blender: /Applications/Blender.app/Contents/MacOS/Blender
- Build: Blender 5.4.0 Alpha, commit corto 745ab9a3e3c5, branch main
- Python: 3.13.13
- Script de generación: scripts/generate_20261102T105936-0300.py
- Script de validación: scripts/reopen_validate_20261102T105936-0300.py
- Artefacto: artifacts/EXP-BPY-001-20261102T105936-0300.blend
- Logs y metadatos de procesos: logs/*20261102T105936-0300.*
- Informe: reports/RESULTADO.md

Las ejecuciones anteriores con Blender 5.2.3 fallaron en inicialización Metal. Una ejecución intermedia Alpha intentó guardar una miniatura fuera de esta carpeta y la escritura falló. El run PASS final definió HOME, perfil y temporales dentro del directorio experimental; úsese ese patrón para futuras ejecuciones.

## Reproducción después de resolver el fallo de arranque

Este bloque documenta los comandos de esta prueba. No constituye autorización para reintentar hasta que se revise el crash. Mantener el perfil, temporal y artefactos dentro de esta carpeta.

Desde la raíz del proyecto:

1. Definir RUN como la ruta absoluta a experimentos/EXP-BPY-001.
2. Usar BLENDER_USER_CONFIG=$RUN/artifacts/blender_profile/config, BLENDER_USER_SCRIPTS=$RUN/artifacts/blender_profile/scripts, BLENDER_USER_DATAFILES=$RUN/artifacts/blender_profile/data y TMPDIR=$RUN/artifacts/tmp.
3. Generación: definir HOME=$RUN/artifacts/retry_$ID/profile/home junto con BLENDER_USER_CONFIG, BLENDER_USER_SCRIPTS, BLENDER_USER_DATAFILES y TMPDIR bajo el árbol experimental; ejecutar Blender --background --factory-startup --python $RUN/scripts/generate_$ID.py -- $RUN/artifacts/EXP-BPY-001-$ID.blend y guardar stdout/stderr en un log nuevo.
4. Solo si la generación finaliza y el archivo existe, iniciar un segundo proceso independiente con las mismas variables aisladas: Blender --background $RUTA_BLEND --python $RUN/scripts/reopen_validate_$ID.py; capturar stdout/stderr en un log nuevo.
5. Revisar el objeto, mediciones JSON, topología, resultado del proceso y criterios en reports/RESULTADO.md; un exit code 0 por sí solo no basta.

Los nombres de ejecución de esta carpeta no se deben reutilizar si se repite el experimento. Crear una nueva ejecución identificada dentro de las mismas subcarpetas y conservar evidencia de fallos anteriores. La versión 5.4 utilizada fue Alpha; el PASS funcional no la convierte en versión estable recomendada.

## Qué construyen los scripts si el runtime puede iniciarse

El script fuente declara centralmente dimensiones 50 × 50 × 50 mm, configura escena métrica con una unidad Blender igual a un metro, crea vértices de malla alrededor del origen, aplica transformación identidad y escribe propiedades personalizadas. El validador está diseñado para correr en un proceso independiente, comprobar reapertura, cantidad/nombre de objetos, parámetros, unidades, transformación, dimensiones de malla evaluada en milímetros, centro, manifoldidad y componente conectado. Tolerancia experimental dimensional: ±0,01 mm, exclusiva de este ensayo.

No se exporta STL ni se altera ningún proyecto .blend existente.
