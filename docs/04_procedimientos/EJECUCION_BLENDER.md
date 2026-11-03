# Ejecución de Blender en background

**Vigente desde:** 2026-11-02. Sintetiza lo practicado en EXP-BPY-001 a 003. Es el procedimiento observado, no una especificación nueva. El lanzador de referencia es `experimentos/EXP-BPY-003/scripts/run_blender.py`.

## Antes de ejecutar

1. Verificar que el ejecutable sea `/Applications/Blender.app/Contents/MacOS/Blender` y que su SHA-256 sea `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80` ([ADR-0002](../05_decisiones/ADR-0002_politica_blender_alpha.md)). Si cambia, es una build distinta y hay que registrarlo.
2. Verificar el hash de cada entrada con `herramientas/sellar_artefacto.py verify`.
3. Elegir una ruta de salida **nueva** que no exista.

## Cómo ejecutar

- Flags usados: `--background --factory-startup --disable-autoexec --python-exit-code 1 --python SCRIPT -- ARGS`.
- Un perfil aislado por proceso: `HOME`, `BLENDER_USER_CONFIG`, `BLENDER_USER_SCRIPTS`, `BLENDER_USER_DATAFILES` y `TMPDIR` dentro de la carpeta del experimento (en EXP-BPY-003: `logs/profile_LABEL`). Motivo: en EXP-BPY-001 Blender intentó escribir una miniatura en `~/.thumbnails` (L-006).
- Registrar por proceso: comando, inicio y fin en UTC, duración, código de salida, y stdout/stderr en un log propio. El lanzador de EXP-BPY-003 genera un `.meta.json` por proceso. En 001 y 002 no existía y los tiempos de pared no se guardaron.
- No escribir en `/tmp` ni fuera del árbol del experimento. En EXP-BPY-003 hubo una escritura puntual en `/tmp` (`exp003_run_probe.sh`).

## Después de ejecutar

1. Comprobar el código de salida. Código 0 no demuestra que la geometría sea correcta.
2. Sellar el artefacto con `herramientas/sellar_artefacto.py seal`.
3. Validar en **otro proceso**, abriendo el archivo sin guardarlo, con el contrato JSON del experimento.
4. Volver a verificar el hash tras la validación.

## Convenciones geométricas

- Escena en métrica, una unidad de Blender = 1 m. Las dimensiones se miden en mm sobre la malla evaluada.
- STL: se exporta con escala 1000 (coordenadas numéricas en mm) y se reimporta con escala 0,001. Un control de escala incorrecta debe fallar (EXP-BPY-003).

## Fallos conocidos

- Blender 5.2.3 LTS: código 139 por Metal en background. Sin solución verificada.
- `ARCH_WARN: ARCH_CACHE_LINE_SIZE` de la dependencia USD: se observa en todos los procesos de la Alpha, sin efecto detectado.

## Herramientas compartidas (desde 2026-11-03)

Sustituyen la copia de `run_blender.py` por experimento. Los experimentos anteriores conservan la suya; no se tocan.

| Herramienta | Uso |
|---|---|
| `herramientas/lanzar_blender.py CARPETA_RUN ETIQUETA SCRIPT [args]` | Lanza Blender con los flags de este documento, hash del ejecutable verificado, perfil aislado en `CARPETA_RUN/profiles/ETIQUETA` y log + `.meta.json` por proceso. No sobrescribe un log existente. |
| `herramientas/validar_malla.py` (vía el lanzador) | Valida en otro proceso: mesh único, envolvente en mm, componentes, manifold, orientación, volumen y degenerados; con `--cavidad X,Y,Z` mide también el hueco interior (paredes, piso, tapa abierta). Sale con código 2 si falla. |
| `herramientas/sellar_carpeta.py CARPETA_RUN --validation PASS` | Sella `artifacts/`, `evidencias/`, `scripts/` y `logs/` con `sellar_artefacto.py` y verifica. No se reescribe un registro existente. |
| `herramientas/exportar_stl.py export\|verify` (vía el lanzador) | STL con escala 1000 y verificación por reimportación; `--import-scale 0.01` es el control negativo y debe fallar. |
| `herramientas/aplicar_material.py` | Ruta corta para cambios solo de apariencia. |

Skills de proyecto que las usan: `.claude/skills/blender-*`.

