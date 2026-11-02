# Resultado — EXP-BPY-001

## Resumen

**Resultado de la repetición con Blender 5.4.0 Alpha: PASS.** La ejecución limpia EXP-BPY-001-20261102T105936-0300 completó el probe, generó el cubo, guardó el .blend y lo reabrió en un segundo proceso independiente. Las nueve verificaciones geométricas pasaron. La ejecución previa con Blender 5.2.3 LTS falló al inicializar Metal; ese resultado se conserva como antecedente y no se sobrescribe.

La aprobación aplica únicamente al flujo mínimo de esta prueba en Blender 5.4.0 Alpha (build main), con perfil aislado y sin exportar STL. No valida estabilidad de versión, impresión ni los experimentos EXP-001/002/003. Una ejecución intermedia de la Alpha generó el archivo pero intentó escribir una miniatura en una ruta fuera del experimento y la escritura falló. La ejecución PASS final aisló además HOME dentro del experimento y no mostró ese intento.

## Entorno observado

| Dato | Resultado |
|---|---|
| ID aprobado | EXP-BPY-001-20261102T105936-0300 |
| Fecha local | 2026-11-02, zona -0300 |
| Fecha de procesos fallidos 5.2.3 | 2026-11-02T13:49:44Z, 13:49:56Z y 13:52:12Z |
| macOS | 27.0.1, build 26A434 |
| Arquitectura de equipo | arm64 |
| Ruta Blender | /Applications/Blender.app/Contents/MacOS/Blender |
| Bundle version de la ejecución aprobada | 5.4.0 |
| Versión informada por CLI | Blender 5.4.0 Alpha |
| Commit corto | 745ab9a3e3c5, branch main |
| SHA-256 ejecutable | 732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80 |
| Python integrado / bpy | Python 3.13.13; bpy importable y ejecutado |
| Addon/MCP | No usado |
| Perfil/temporales ejecución aprobada | artifacts/retry_20261102T105936-0300/profile y artifacts/retry_20261102T105936-0300/tmp |

## Matriz de verificaciones

| Verificación | Estado | Evidencia |
|---|---|---|
| Blender instalado y ruta exacta | PASS | Bundle y ejecutable en /Applications/Blender.app |
| Versión y arquitectura arm64 | PASS | Info.plist, file, lipo y salida --version |
| Ejecutable 5.4 Alpha corre con --version | PASS | Salida identifica Blender 5.4.0 Alpha; aparece advertencia ARCH_WARN de dependencia USD |
| Arranque background 5.2.3 LTS | FAIL | Generación y probes de 2026-11-02 terminaron en código 139 en Metal |
| Arranque background 5.4.0 Alpha | PASS | Probe con bpy importable, código 0 |
| Generación por bpy en ejecución aprobada | PASS | Log JSON confirma bpy, parámetros y save_result FINISHED |
| Cubo 50 × 50 × 50 mm | PASS | Malla creada desde vértices métricos centrados |
| Guardado de .blend | PASS | Archivo 51,802 bytes; SHA-256 registrado abajo |
| Proceso independiente de reapertura | PASS | Segundo proceso reportó Read blend del artefacto esperado |
| Cantidad/nombre de objetos | PASS | Un único objeto con nombre e ID de ejecución esperados |
| Medidas, centro, escala y unidades | PASS | Dimensiones evaluadas, centro cero, escala identidad y unidades METRIC |
| Topología y componentes | PASS | 8 vértices, 12 aristas, 6 caras, un componente, aristas manifold |
| Parámetros personalizados después de reabrir | PASS | JSON 50/50/50 mm e ID persistieron |
| Evidencia reproducible | PASS | Scripts, logs, metadatos, checksums y este informe |

## Evidencia de proceso

La ejecución aprobada usó Blender 5.4.0 Alpha, Python 3.13.13, factory startup y perfil/temporales bajo artifacts/retry_20261102T105936-0300. Probe: 13:58:37Z–13:58:38Z, código 0. Generación: 13:59:42Z, código 0. Reapertura/validación: 13:59:47Z–13:59:48Z, código 0.

La reapertura reportó el mismo .blend y un único objeto. Dimensiones evaluadas: 50.00000074505806 × 50.00000074505806 × 50.00000074505806 mm; desviación por eje: +0.00000074505806 mm, menor que la tolerancia experimental de ±0.01 mm. Centro: (0,0,0) mm. Escala: (1,1,1). Unidades: METRIC, scale_length 1.0, display MILLIMETERS. Topología evaluada: 8 vértices, 12 aristas, 6 caras, un componente conectado y todas las aristas manifold.

Antecedente: Blender 5.2.3 LTS falló en tres arranques/probes con código 139. La pila señaló detección de Metal. El intento de `--gpu-backend opengl` fue rechazado porque esa build solo admite metal. El issue [Blender #163272](https://projects.blender.org/blender/blender/issues/163272) trata un crash de Metal en contexto no GUI/sandbox y figura resuelto en 5.3; la similitud es plausible, no una causa raíz demostrada. La 5.4 Alpha evita el crash en esta prueba, pero no establece cuál cambio lo resolvió.

La ejecución intermedia con Alpha 20261102T105833-0300 pasó generación y validación, pero su log reportó fallo de OpenImageIO al intentar escribir una miniatura en /Users/yayo/.thumbnails/large. La escritura no se abrió; se conserva el log. Para la ejecución PASS final se aisló HOME dentro del árbol experimental y no apareció esa operación. En todas las ejecuciones Alpha se vio la advertencia ARCH_WARN de dependencia USD, sin evidencia de que afecte el resultado.

## Artefactos

- Generador PASS: scripts/generate_20261102T105936-0300.py
- Validador independiente PASS: scripts/reopen_validate_20261102T105936-0300.py
- Archivo .blend PASS: artifacts/EXP-BPY-001-20261102T105936-0300.blend (51,802 bytes)
- SHA-256 .blend: 6a23e9e28bfa30043059184d21744b13416b9303da99f0a60a9f056d86eb5141
- SHA-256 generador: c6281c70736634bc425971281a0843782fbd14b2fa0e2b4f585c42c2880805a9
- SHA-256 validador: 406c88ad8d3ae2e42ce75e12a81314e447ad08292c67725e1ee7ed2dc15b120f
- Logs y metadatos del run PASS: logs/*20261102T105936-0300.*
- Probe Alpha: logs/background_probe_20261102T105833-0300.log y .meta
- Generación intermedia y warning de thumbnail: logs/generate_20261102T105833-0300.log
- Ejecuciones fallidas 5.2.3 y crash reports: logs/*104904*, logs/*105207* y artifacts/tmp/
- Tolerancia del cubo: ±0,01 mm, solo experimental, no aprobada para CU-01.

## Errores y advertencias

1. Blender 5.2.3 LTS: tres fallos de arranque background en Metal, código 139.
2. En un primer run de Blender Alpha, OpenImageIO no pudo escribir una miniatura fuera de la carpeta del experimento. Para el run final se aisló HOME dentro del experimento; el log final no reporta escritura externa.
3. Advertencia ARCH_WARN de la dependencia USD en Blender Alpha, sin fallo asociado en este ensayo.
4. No hubo errores de bpy ni de validación en el run PASS final.

## Clasificación y decisión

La clasificación de la ejecución 5.4.0 Alpha / 20261102T105936-0300 es **PASS**: se cumplieron todas las condiciones funcionales del ensayo y existen mediciones tras reapertura independiente. La ejecución 5.2.3 LTS permanece **FAIL** y documenta el problema inicial. La Alpha se debe tratar como runtime experimental, no como versión estable elegida para producción.

## Recomendación

La prueba demuestra que el flujo bpy directo de generación, guardado, reapertura y medidas puede funcionar en esta Mac bajo Blender 5.4.0 Alpha. Se puede preparar EXP-BPY-002 como prueba siguiente, pero recomiendo ejecutarlo solo después de decidir si se acepta una Alpha como entorno temporal de laboratorio o se repite esta prueba en una versión estable/LTS que arranque correctamente. EXP-BPY-002 no se ejecutó. Ninguna conclusión aquí aprueba EXP-001, EXP-002, EXP-003 ni exportación STL.
