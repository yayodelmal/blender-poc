# Aprendizajes operativos reutilizables

Estos registros preservan procedimientos y decisiones verificables. No son entrenamiento automático del modelo ni cambios de pesos; una regla se reutiliza solo después de revisar que aplica al contexto.

| ID | Experimento | Síntoma / evidencia | Causa | Corrección o regla | Verificación | Estado |
|---|---|---|---|---|---|---|
| L-001 | INC-BPY-001 / EXP-BPY-002 | Hash de maestro .blend divergió por 8 bytes; tamaño/hashes históricos preservados | Causa raíz no establecida; investigación encontró cambio y validación semántica satisfactoria | Aprobar línea base nueva mediante autorización explícita; no reescribir historia; guardar maestro inmutable y generar revisiones | EXP-BPY-002 preflight/snapshot y hash final PASS | Cerrado para esa entrada |
| L-002 | EXP-BPY-002 | Debía recuperarse estado aceptado después de candidato inválido | Snapshot/revisión inmutable separa estado candidato de accepted | Validar copia reabierta independientemente; recuperación requiere equivalencia geométrica y paramétrica | Restauración B y conflicto optimista PASS | Verificado en ensayo |
| L-003 | EXP-BPY-003 | Generador/validador iniciales tuvieron fallos de dimensión, escala/componente y área/volumen | Errores en conversión unidades, construcción y matriz de transformación | Validar evaluado, componentes, manifold, normales, volumen y dimensión antes de exportar | Revisiones rechazadas conservadas; controles negativos detectados | Verificado en proxy |
| L-004 | EXP-BPY-003/004 | STL no declara universalmente unidad; exportación mal escalada produjo modelo diminuto | STL guarda geometría triangulada y el receptor necesita convención de unidad/escala | Registrar escala y convención explícitamente; verificar dimensiones tras reimportación | Controles de escala de EXP-BPY-003 y dimensiones importadas en EXP-BPY-004 | Verificado digitalmente |
| L-005 | EXP-BPY-004 | Configuración del slicer incompleta en informe; 3MF revela valores, pero nombre del perfil contradice UI | La observación de UI y metadata del proyecto no quedaron ligadas a una captura persistente de la misma ejecución | Registrar preset, campos activos y captura antes/después de slice; archivar proyecto nuevo por revisión | No resuelto hasta reconciliar `Macetero PLA 0.20mm K1C` con el perfil serializado `0.20mm Standard...` | Pendiente |
| L-006 | EXP-BPY-001 | OpenImageIO intentó miniatura fuera de árbol de experimento | Blender usó HOME de usuario | Aislar HOME, configuración y temporales bajo experimento; inspeccionar rutas externas al final | Run final 001 y runs 002/003 registraron perfiles aislados | Verificado para esos runs; no sandbox completo |
| L-007 | EXP-BPY-004 | Observación visual del laminado no produjo capturas persistentes | La interfaz de control disponible no persistió screenshots | Guardar capturas normales de UI dentro de evidencias y ligar a run/config; si no se puede, criterio inconcluso | Falta captura de la sesión previa | Regla definida; pendiente aplicar |

## Regla de integridad

Calcular el SHA-256 definitivo del artefacto exacto que se entrega después de terminar el proceso que lo escribió, ligarlo en el manifiesto a una ruta inequívoca y no sobrescribir revisiones aceptadas. Esto no diagnostica por sí solo cambios semánticos.
