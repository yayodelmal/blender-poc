# Cierre de Fase 1 — Laboratorio de Modelado 3D Agéntico

**Estado:** `PENDIENTE_VALIDACION_FISICA`  
**Fecha de actualización:** 2026-11-02  
**Alcance de este informe:** cierre provisional documental; la fase no está cerrada.

## 1. Objetivo

Demostrar un flujo local reproducible donde Codex genera/edita geometría Blender con `bpy`, valida el modelo, exporta STL y prepara su laminado para una Creality K1C. La primera fase debe terminar con contraste contra una impresión física, no solo con resultados digitales.

## 2. Arquitectura utilizada

Flujo funcional demostrado hasta ahora: Codex → procesos locales Blender background → `bpy` → archivos `.blend` revisados → validación geométrica → STL → Creality Print. MCP for Blender no se utilizó en los experimentos funcionales; la ruta elegida fue `bpy` directo por el dictamen de seguridad previo. La prueba física propuesta deja a la persona responsable como operador de la impresora.

## 3. Experimentos

| Experimento | Estado | Qué demuestra |
|---|---|---|
| EXP-BPY-001 | PASS | Generación de cubo, guardado, reapertura independiente y medición en Blender 5.4.0 Alpha |
| EXP-BPY-002 | PASS | Edición del objeto existente, revisión/snapshot, validación, control negativo y recuperación |
| EXP-BPY-003 | PASS | Relieve físico, topología, controles negativos, exportación y reimportación STL |
| EXP-BPY-004 | INCONCLUSIVE | Importación y laminado observados; configuración guardada ahora legible, pero conflicto de identidad de preset pendiente de resolver |
| EXP-BPY-005 | NOT RUN | Protocolo físico preparado; impresión y mediciones pendientes |

## 4. Capacidades y evidencia digital

Los tres experimentos Blender pasaron en la misma versión experimental: Blender 5.4.0 Alpha, build `745ab9a3e3c5`, Python integrado 3.13.13. EXP-BPY-003 creó una placa de 80 × 60 × 5 mm con 27 relieves, evaluó topología y transfirió la forma al STL bajo convención mm documentada. El STL tiene SHA-256 `c6342d689ef70742ae0f9b3d6bbbf32b4f0f542ef7a5b6be2645f3205755b3d3`; EXP-BPY-004 y una nueva lectura de integridad confirman que el artefacto sigue coincidiendo.

Hashes principales observados el 2026-11-02:

- EXP-BPY-001 maestro: `a5f0aa70db10127c973b69254c6f76a3f2656becfcf0a7b5104ffaaee16ecbc3`.
- EXP-BPY-002 revisión B: `08a85ae9c8c413c24bc06fcfed0296b962e02dc3bc6a44af7373ee80c2b3a194`.
- EXP-BPY-003 maestro: `09f7ee7c1ac207df00b1e8494e41b39a0c1eec4e048edbfcac61b71fd998495b`.
- EXP-BPY-003 STL: `c6342d689ef70742ae0f9b3d6bbbf32b4f0f542ef7a5b6be2645f3205755b3d3`.
- EXP-BPY-004 3MF: `659b0890553a1e30087d3c6d329520179306767597938d45d705c3d919a2b5a4`.

## 5. Evidencia física

No existe evidencia de impresión física. No se ha declarado que la placa se haya impreso. Las 37 min 20 s y 19,30 g (6,47 m) son estimaciones de laminador de la sesión anterior. No hay tiempo real, material real, fotografías ni mediciones de la pieza.

## 6. Incidentes y correcciones

- INC-BPY-001: se detectó divergencia entre la huella histórica y la del `.blend`. La investigación concluyó nueva línea base candidata; se aprobó explícitamente para EXP-BPY-002, preservando el registro previo.
- En EXP-BPY-001 se aisló `HOME`/temporales tras un intento de miniatura externa; la ejecución final aprobada no registró dicha escritura.
- EXP-BPY-003 requirió correcciones al generador/validador; las revisiones rechazadas se conservaron.
- EXP-BPY-004 conserva una diferencia entre el preset de proceso observado en UI (`Macetero PLA 0.20mm K1C`) y `default_print_profile` del 3MF (`0.20mm Standard @Creality K1C 0.4 nozzle`). No se resuelve por inferencia.

## 7. Limitaciones y reproducibilidad

La evidencia Blender se limita a una build Alpha; no valida una versión estable. STL no lleva unidad física universal; se documentó la convención numérica. El laminado tuvo inspección visual previa, pero no persistió capturas y quedaron dudas de configuración/aviso de adhesivo. Ninguno de los resultados digitales valida resistencia, adhesión real, acabado ni dimensiones de una impresión.

Los scripts, logs, manifiestos y hashes de los experimentos proporcionan reproducción del flujo digital en esa máquina/build. La repetibilidad física está pendiente de registrar material, superficie, perfil, entorno, tiempo y pieza.

## 8. Recomendaciones para Fase 2

1. Completar EXP-BPY-004 en una copia del proyecto, resolviendo y evidenciando el preset efectivo y el aviso de adhesivo.
2. Imprimir el cupón de EXP-BPY-003 bajo supervisión de la persona responsable y completar EXP-BPY-005.
3. Aprobar explícitamente tolerancias físicas y criterios visuales antes de evaluar la pieza.
4. Solo tras evidencia suficiente, cerrar Fase 1 y decidir si CU-01 pasa a definición paramétrica.
5. Mantener revisiones inmutables con manifiesto, hash posterior a cierre del proceso y evidencias ligadas a IDs de revisión.

## 9. Estado de cierre

**PENDIENTE_VALIDACION_FISICA.** La fase sigue abierta mientras EXP-BPY-004 tenga aspectos de configuración sin resolver y EXP-BPY-005 no tenga impresión, fotos y medidas reales. No se ha iniciado CU-01 ni se considera aprobada una pieza imprimible físicamente.
