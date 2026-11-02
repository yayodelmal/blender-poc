# Resultado — EXP-BPY-003

## Resultado global: PASS

Ejecución `EXP-BPY-003-20261102T144300Z`, 2026-11-02, macOS Apple Silicon, Blender 5.4.0 Alpha (build `745ab9a3e3c5`) y Python integrado 3.13.13. El resultado se limita a esta build Alpha y a este patrón de ensayo; no valida versiones estables, CU-01, laminado ni impresión física.

## Geometría aceptada

Se generó una placa editable de 80 × 60 × 5 mm, con base de 4 mm y 27 ladrillos en filas alternadas. La malla se construyó como una base y un conjunto de sólidos que se unen con Boolean Exact; cada ladrillo se solapa 0,5 mm con la base. El booleano quedó aplicado al objeto principal. El relieve es geometría poligonal real, no textura.

Los parámetros se centralizan en `scripts/build_relief_plate.py` y se guardan en propiedades personalizadas del objeto. Son metadatos de reconstrucción, no parámetros reactivos. El script permite reconstruir la pieza desde cero; no se usaron Geometry Nodes.

La revisión aceptada es `artifacts/EXP-BPY-003-20261102T144300Z_relief_plate_master.blend`. Se copió un snapshot en `snapshots/` y se reabrió en proceso independiente antes de exportar. El snapshot y el maestro tienen SHA-256 idéntico.

## Validación geométrica

La malla evaluada del maestro y del snapshot pasó:

- Bounds: 80.000005662 × 60.000002384 × 5.000000354 mm; dentro de ±0,01 mm.
- Centro XY: (0, 0) mm; plano inferior Z=0 mm.
- Relieve máximo: 1.000000354 mm; 27 islas superiores y área superior 3679.199872 mm² (esperada 3679,2 mm²).
- Una componente conectada; 241 vértices, 389 aristas y 150 caras.
- Todas las aristas manifold; caras orientadas coherentemente; volumen firmado positivo de 22879.203712 mm³.
- Sin aristas/caras degeneradas según umbrales del validador ni pares de caras no adyacentes detectados por BVHTree.
- No quedaron modificadores sin aplicar. Los 27 ladrillos se fusionaron físicamente con la base.

La prueba de intersecciones usa BVHTree sobre pares de caras y excluye pares que comparten algún vértice. Es una detección estática acotada, no una garantía general de ausencia de toda autointersección. La unión booleana exacta, la conectividad, manifold, orientación y volumen aportan comprobaciones complementarias.

## STL y reimportación

El STL válido se exportó desde el objeto seleccionado con Blender `bpy.ops.wm.stl_export`, escala 1000, `use_scene_unit=False`, forward Y, up Z y evaluación de viewport. Esto escribe coordenadas numéricas en milímetros. STL no codifica universalmente las unidades.

En un proceso background separado, `bpy.ops.wm.stl_import` reimportó el archivo con escala 0,001 para convertir los números mm a coordenadas Blender en metros. La reimportación pasó: 80.000013113 × 60.000006109 × 5.000000820 mm, una componente, manifold, volumen positivo, normales coherentes y los 27 islotes del relieve con área 3679.200758 mm². El STL está triangulado (241 vértices, 717 aristas y 478 caras en esta importación); sus dimensiones y rasgos geométricos comparados cumplen tolerancia.

El STL no conserva propiedades paramétricas. La prueba acredita transferencia de forma bajo la convención de escala indicada, no propiedades de laminado ni imprimibilidad física.

## Controles negativos

| Control | Resultado observado | Dictamen del control |
|---|---|---|
| Ladrillo separado 0,5 mm sobre la placa | 2 objetos y 2 componentes totales; el validador reportó FAIL | PASS: defecto detectado |
| Dimensión X alterada a 80,05 mm | Desviación +0,0500065 mm; falla dimensiones, área superior y volumen contra parámetros | PASS: defecto detectado |
| Exportación STL con `global_scale=1` en lugar de 1000 | Reimportada bajo la convención acordada como 0,080000 × 0,060000 × 0,005000 mm | PASS: escala incorrecta detectada y rechazada |

Cada negativo se generó desde el maestro a una ruta separada. No se modificó ni sobrescribió el maestro.

## Intentos de desarrollo conservados

Las primeras dos revisiones del generador se rechazaron antes de exportar: una trató milímetros como unidades internas de Blender; la siguiente aplicó una escala de cubo incorrecta, resultando en dimensiones reducidas y 28 componentes. Los logs `validate_master.log` y `validate_master_v2.log` preservan esos resultados. La revisión v3 corrigió ambas causas y pasó antes de ser copiada al artefacto maestro.

La primera validación STL midió bounds correctamente, pero no aplicó la escala del objeto al área y volumen locales; por eso fue rechazada. El validador se corrigió para incorporar la matriz de transformación y una ejecución nueva pasó. Los dos logs, el fallido y el corregido, quedan preservados.

La primera consulta de API STL también encontró una limitación del script de introspección: accedió a `default` en una propiedad RNA de tipo colección. El script de consulta fue ajustado; la build expuso las operaciones de exportación/importación y los parámetros usados. Blender mostró durante los procesos la advertencia `ARCH_WARN` de USD. No impidió estas operaciones. El probe de API emitió además avisos RNA de enum al inspeccionar metadatos, sin relación con la exportación.

## Integridad y escrituras

Los archivos anteriores de EXP-BPY-001 y EXP-BPY-002 permanecen con sus hashes registrados: el maestro aprobado de EXP-BPY-001 (`a5f0aa70…ecbc3`) y la revisión B de EXP-BPY-002 (`08a85ae9…a194`). No se utilizó MCP, no se instaló software, no se abrió Creality Print y no se imprimió.

Todas las ejecuciones Blender usaron `HOME`, configuración y temporales bajo `experimentos/EXP-BPY-003/logs/`. Blender generó perfiles/miniaturas dentro de esos perfiles. **Sí ocurrió una escritura fuera del directorio experimental:** durante la consulta inicial se creó temporalmente `/tmp/exp003_run_probe.sh`; se retiró al detectarse. No se observó otra escritura externa atribuible a Blender, aunque esto no constituye una auditoría forense de todo el sistema.

Cada proceso lanzado por `scripts/run_blender.py` tiene log y `.meta.json` con comando, inicio/fin UTC, duración monotónica y código de salida. Los hashes finales por archivo están vinculados en [MANIFIESTO_ARTEFACTOS.json](../MANIFIESTO_ARTEFACTOS.json). Las revisiones erróneas se mantienen como evidencia diagnóstica y no se promueven.

## Advertencia de alcance

`manifold`, volumen positivo, conectividad y transferencia STL no equivalen a laminado validado ni a impresión física validada. No se ejecutó Creality Print ni se comprobó perfil K1C, tolerancias funcionales, adhesión, resistencia, puentes o drenaje.

## Recomendación

EXP-BPY-003 obtuvo `PASS` para este proxy. Se recomienda preparar EXP-BPY-004 para revisar el laminado en Creality Print con perfil de Creality K1C y boquilla de 0,4 mm, pero mantenerlo sin ejecutar hasta autorización. No se ha inferido que el proxy valide CU-01.


## Corrección de vista al abrir

La causa de que pareciera vacío era el encuadre guardado: Layout tenía `view_distance=18.388` unidades Blender (metros) y el objeto mide 0,08 m de ancho. La pieza estaba en Scene Collection y no estaba oculta; el acercamiento con Home la mostró.

Creé `artifacts/EXP-BPY-003-20261102T144300Z_relief_plate_open_ready.blend` como copia separada con la vista centrada en el objeto a 0,20 m, objeto seleccionado y los workspaces 3D encuadrados. Se reabrió en Blender GUI y la pieza quedó visible sin pulsar Home; la validación geométrica volvió a dar PASS. El archivo original `relief_plate_master.blend` conserva su SHA-256 y no se modificó.

También ajusté `scripts/build_relief_plate.py` para que futuras escenas generadas en este laboratorio guarden un encuadre inicial centrado y visible. Esto no cambia las preferencias globales de Blender.
