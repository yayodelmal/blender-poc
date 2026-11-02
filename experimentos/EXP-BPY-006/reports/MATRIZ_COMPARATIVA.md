# EXP-BPY-006 — Matriz comparativa observada

| Criterio | A — Script `bpy` | B — Geometry Nodes | C — Edición *in-place* |
|---|---|---|---|
| Estado del candidato | PASS geométrico (v2); primera revisión FAIL | FAIL en las dos variantes | INCONCLUSIVE / NOT RUN |
| Representación inicial | Malla nueva construida desde parámetros declarados | Parámetros persistentes en nodos; base de ensayo como operand de malla | Maestro EXP-BPY-003: malla única horneada, sin modificadores |
| Reproducibilidad | Script con parámetros centralizados; se reconstruye la pieza completa | El patrón persiste tras reabrir, pero unión con base no validada | No hay grupos u objetos por ladrillo que puedan editarse directamente |
| Editabilidad persistente | Malla editable; parámetros son metadatos no reactivos | Sockets `Relieve`, `Ladrillo X/Y`, `Paso X/Y` sobreviven; no se acreditó sólido completo | No demostrada para regiones volumétricas completas |
| Conservación de invariantes | Observada PASS en validación independiente: 80×60×5, base 4, 27 relieves, 1 componente | FAIL: salida no incluye la placa; 9/27 componentes según variante | No ejecutado |
| Complejidad observada | Moderada; unión booleana exacta al generar | Alta para patrón + instancias + unión; nodo Boolean observado conservando un operando | Alta por topología fusionada y caras compartidas |
| Recuperación | Artefacto nuevo separado; maestro/snapshot intactos | Variantes separadas y selladas; sin promoción | No se hicieron cambios ni recuperación |
| Validación independiente | PASS en proceso Blender distinto del generador | FAIL en proceso Blender distinto del generador | No disponible |
| Adecuación para CU-01 | Candidata provisional si se aceptan revisiones regeneradas y se versionan | No recomendable aún; comportamiento booleano bloqueante | No recomendable con el maestro horneado actual |
| Limitación principal | No es edición incremental ni modelo reactivo dentro del `.blend` | Sólido conectado base+relieve no obtenido | Top-islas identificables; volumen completo de cada ladrillo no aislado |

## Recomendación

Para el siguiente experimento de CU-01, la alternativa de menor riesgo técnico observado es **A como generador de revisiones inmutables**: modifica el script fuente, genera un archivo nuevo y valida el resultado por separado. Debe llamarse generación paramétrica reproducible, no edición *in-place*. Recomendación provisional, confianza media-baja: depende de Blender 5.4 Alpha y aún no pasó controles negativos de EXP-BPY-006.

No avanzar todavía a CU-01. Primero conviene un experimento pequeño para aislar la unión de sólidos en Geometry Nodes en una versión estable soportada. La estrategia C necesita conservar estructuras por ladrillo o probar una identificación topológica no ambigua en otra copia; no se forzó una simulación mediante reconstrucción.
