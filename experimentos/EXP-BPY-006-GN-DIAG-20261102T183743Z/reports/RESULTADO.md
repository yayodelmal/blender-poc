# Diagnóstico mínimo Geometry Nodes — unión de cubos

**Estado: INCONCLUSIVE — se detuvo al fallar el validador antes de informar mediciones geométricas.**  
**Run ID:** `EXP-BPY-006-GN-DIAG-20261102T183743Z`  
**Fecha:** 2026-11-02 (UTC).

## Alcance

Se crearon dos `.blend` independientes con Geometry Nodes `Mesh Boolean / UNION`. Cada uno contiene dos cubos cerrados de 10 × 10 × 10 mm. El cubo A ocupa X=[0,10] mm; el cubo B ocupa X=[9,8,19,8] mm; comparten 10 × 10 mm de sección y se solapan 0,2 mm en X. Resultado esperado: envolvente 19,8 × 10 × 10 mm, volumen 1.980 mm³, una componente cerrada y manifold. Se construyeron ambas permutaciones de `Mesh 1` y `Mesh`.

## Entorno y antecedentes

- Repositorio verificado en `/Users/yayo/Projects/blender-poc`, rama `main`, limpio al inicio, remoto `origin` configurado.
- Ejecutable: `/Applications/Blender.app/Contents/MacOS/Blender`.
- Versión: Blender 5.4.0 Alpha, build `745ab9a3e3c5` (branch `main`), macOS arm64.
- SHA-256 del ejecutable: `732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80`.
- El resultado histórico de EXP-BPY-001 documenta Blender 5.2.3 LTS con tres fallos de arranque background, código 139 asociado en los logs a Metal. Se conserva esa evidencia; no se volvió a probar ni se instaló/actualizó Blender. El usuario autorizó expresamente continuar con la Alpha por esta limitación.
- Cada ejecución usó `--background --factory-startup --disable-autoexec --python-exit-code 1` y `HOME`, config, scripts, data y temporales separados bajo `profiles/<label>/`.

## Ejecuciones y evidencia

| Variante | `Mesh 1` | `Mesh` (entrada 2) | Generación | Validación separada |
|---|---|---|---|---|
| A_FIRST | Input A | Input B | Exit code 0; guardó `.blend` | Exit code 1; INCONCLUSIVE |
| B_FIRST | Input B | Input A | Exit code 0; guardó `.blend` | Exit code 1; INCONCLUSIVE |

Los logs de generación y sus metadatos están en `logs/build_A_FIRST.*` y `logs/build_B_FIRST.*`. Registran el comando, el perfil aislado, versión, SHA del ejecutable, duración y el orden configurado de los inputs.

En ambos validadores, un proceso Blender independiente abrió el `.blend` esperado. El validador redirigió en memoria la salida del grupo para inspeccionar A y B individualmente; luego se detuvo al intentar conectar la salida final: buscó `boolean.outputs['Geometry']`, pero el socket de salida del nodo Boolean en esta build se llama `Mesh`. El error es `KeyError` y quedó registrado en `logs/validate_A_FIRST.log` y `logs/validate_B_FIRST.log`. El archivo abierto no se guardó. Como el programa no emitió su registro JSON de mediciones, no hay resultados independientes persistidos para las entradas ni para la unión.

**No se declara que las variantes de este diagnóstico hayan producido un único operando.** El resultado de la unión es desconocido por la interrupción del validador. Según la condición indicada, no se corrigió el script ni se repitió el test.

## Comparación con la evidencia Alpha anterior

Los logs históricos `experimentos/EXP-BPY-006/logs/probe_gn_boolean.log` y `probe_gn_boolean_reverse.log` sí emitieron mediciones:

- Orden anterior A→B: 15 × 7 × 1,2 mm, 8 vértices, 6 caras; corresponde al ladrillo, no a la unión placa+ladrillo.
- Orden anterior B→A: aproximadamente 80 × 60 × 4 mm, 8 vértices, 6 caras; corresponde a la base, no a la unión.

Esto respalda que **aquella prueba Alpha** conservó un operando distinto al invertir el orden. Era una prueba de placa y ladrillo de tamaños diferentes, no esta prueba nueva de dos cubos iguales. No se generaliza ese resultado al diagnóstico actual, cuya validación quedó inconclusa.

## Artefactos sellados

El registro `registro_artefactos.jsonl`, creado solo para este diagnóstico mediante `herramientas/sellar_artefacto.py`, contiene:

| Artefacto | Tamaño | SHA-256 | Estado |
|---|---:|---|---|
| `artifacts/union_Afirst.blend` | 60.750 B | `bbc5359b5045396f5fbbf33e1e7b96fba4925ebc21a36b68fc5f5cd82a57e9b6` | INCONCLUSIVE |
| `artifacts/union_Bfirst.blend` | 60.749 B | `863d752ad3bfc09d8e575a6a1629fec4ae2ebd313852ca4a942c61adabcba710` | INCONCLUSIVE |
| `logs/validate_A_FIRST.log` | 4.142 B | `b672519eaf2f66b22412abf2759c380ec023aaa66388b622a52886740ea761d3` | Evidencia del error |
| `logs/validate_B_FIRST.log` | 4.142 B | `9bdd3482df4d3f3b8052610c6b1494f7ee90c25e7763945d6d7dd5b919297a72` | Evidencia del error |

## Dictamen y recomendación

El experimento mínimo no confirmó ni refutó en la nueva ejecución el comportamiento de la unión: la causa inmediata de la inconclusión fue un nombre de socket incorrecto en el validador. La evidencia Alpha anterior indica que la unión no combinó los operandos bajo los dos órdenes probados allí, pero no identifica la causa raíz. Geometry Nodes no queda validado para sólidos conectados ni recomendado para CU-01 en este momento.

No se tocaron EXP-BPY-003 ni otros experimentos históricos. No se exportó STL, no se abrió Creality Print ni se imprimió. No hubo reparación de geometría. El siguiente paso requeriría corregir el validador y repetir solo este diagnóstico; esta ejecución termina aquí según la condición de parada.
