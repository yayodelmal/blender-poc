# Uso de Creality Print

**Vigente desde:** 2026-11-02. Basado en EXP-BPY-004, INC-BPY-002 y L-005 y L-007 de [APRENDIZAJES](APRENDIZAJES.md). Versión observada: Creality Print 7.3.0.6157, arm64.

## Reglas

1. **Nunca abrir el 3MF original.** Crear una copia con nombre nuevo, registrar su hash y abrir solo la copia. Creality Print puede guardar sobre el archivo abierto: eso ocurrió con `…154038Z_working_copy.3mf` (INC-BPY-002). Registrar la copia con `--mutable`.
2. Verificar el hash del STL de entrada antes y después de la sesión.
3. **Registrar el preset exacto** antes de laminar (nombre completo del selector de proceso). Un preset personalizado no se asume equivalente a uno estándar (EXP-BPY-004, primer run).
4. **Guardar una captura persistente** (archivo `.png` en `evidencias/`, con hash en el registro) de: impresora, boquilla, filamento, cama, preset, deslizador de capas en su extremo y resumen de G-code. Si no se puede guardar, el criterio queda INCONCLUSIVE; no se sustituye con una descripción.
5. Leer la posición del deslizador de capas con cuidado: en el run `155417Z` una lectura "20 / 4,00 mm" era la posición del control, no su extremo (25 / 5,00 mm).
6. Guardar el proyecto laminado con nombre nuevo por run.
7. No pulsar `Send print` ni conectar la impresora durante un experimento digital.
8. El aviso `please apply glue before print` es una advertencia del perfil. Decide un humano tras identificar la superficie física montada (el manual de la K1C indica que la cara A de la PEI lisa es sensible a aceite y sudor).

## Qué demuestra y qué no

El laminado completado demuestra que el modelo se importa con las dimensiones correctas y genera trayectorias con los ajustes registrados. No demuestra adhesión, acabado, resistencia ni dimensiones de la pieza impresa. El 3MF guardado no incluye G-code; las estimaciones (por ejemplo 30m36s, 14,45 g, 4,84 m) son del laminador, no mediciones.

## Pendiente

La CLI de Creality Print no está probada en esta máquina.
