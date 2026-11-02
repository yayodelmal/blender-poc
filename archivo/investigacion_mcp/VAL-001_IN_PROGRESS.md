# VAL-001 / INV-07 — Estrategia de validación
**Fecha:** 2026-11-02. **Responsable:** coordinador técnico. **Estado:** borrador IN PROGRESS; ninguna prueba ejecutada.

## Pregunta investigada

¿Qué evidencia mínima permite afirmar que una edición cumple el CU-01 desde la escena editable hasta Creality Print?

## Evidencia

| Afirmación | Fuente/URL | Fecha/versión | Tipo de evidencia | Confianza |
|---|---|---|---|---|
| BMesh expone propiedades topológicas; usar malla evaluada cuando haya modificadores | [API indexada Blender 5.1](https://docs.blender.org/api/5.1/bmesh.types.html), [Depsgraph 3.6](https://docs.blender.org/api/3.6/bpy.types.Depsgraph.html) | Consulta 2026-11-02 | Documentación primaria; extractos indexados, acceso directo 402 | Alta documental, sin prueba |
| Trimesh separa watertight, winding consistente e is_volume | [API](https://trimesh.org/trimesh.base.html) | Docs 5.2.0, consultada 2026-11-02 | Documentación primaria abierta | Alta documental |
| Toolbox tiene checks y registro de una reparación problemática retirada | [INV-03](INV-03_validacion_fdm.md) | Evidencia secundaria de investigación primaria; consulta 2026-11-02 | Documentación/changelog | Media-alta |
| Creality documenta CLI, releases ARM64 y existe un reporte de fallo en Windows | [INV-04](INV-04_validadores.md), [issue #634](https://github.com/CrealityOfficial/CrealityPrint/issues/634) | 7.3.0; Windows 11/K2 Plus en issue | Documentación del autor e issue comunitario | Alta para lo documentado; macOS no probado |

No se realizaron pruebas propias. La matriz siguiente define pruebas propuestas, no resultados.

## Capacidades confirmadas y limitaciones

Cada chequeo debe registrar valor esperado, observado, unidad, tolerancia, método, versión, evidencia y resultado `PASS / FAIL / INCONCLUSIVE / NOT RUN`. Resultado general solo `PASS` si todos los obligatorios pasan; una herramienta que no arranca produce `INCONCLUSIVE`, no pase.

| ID | Requisito y evidencia | Criterio propuesto | Método candidato | Límite/estado |
|---|---|---|---|---|
| V01 | Contrato completo | No quedan requisitos bloqueantes sin resolver | Revisión CON-001 | Falla cerrada; pared, base/drenaje aún pendientes |
| V02 | Exterior nominal 150×150×60 mm, referencia incluye relieve por decisión provisional | Error digital ≤±0,10 mm por eje | Bounds world-space de geometría evaluada; repetir sobre STL | Umbral de ensayo propuesto, no tolerancia de impresora; semántica pendiente de confirmar |
| V03 | Relieve físico en cuatro caras y esquinas continuas | Geometría sobresaliente conectada al cuerpo; sin cara ausente ni corte accidental | Secciones/mesh evaluada, componentes, inspección renderizada | Vista visual sola no basta; definir profundidad y criterio de junta |
| V04 | Editabilidad e incrementalidad | Cambiar tamaño de ladrillo conserva parámetros del cuerpo y abre desde `.blend` | Cambiar patrón, guardar, reabrir, comparar mediciones e inputs | Requiere experimento; STL no acredita editabilidad |
| V05 | Espesor, base y drenaje (R02–R04) | Valores confirmados; presencia/espesor/aberturas geométricamente medibles; flujo solo si se establece ensayo | Medición local de pared/base, secciones y revisión de conductos | Bloqueada por decisiones humanas; ensayo de flujo requiere protocolo aparte |
| V06 | Estado y recuperación (R07) | Snapshot previo y restaurado abre; coincide con revisión aceptada e invariantes; revisión candidata se promueve solo sin conflicto concurrente | Guardar copia, reabrir, introducir cambio inválido, recuperar y comparar revisión/mediciones | Guardado no es transacción; fallo de snapshot/restauración bloquea mutación/reintentos |
| V07 | Exportación STL (R08) | Escala mm, orientación conocida; bounds y relieve coinciden con candidato dentro de tolerancia; archivo legible | Exportar derivado y reimportar/leer; medir con herramientas disponibles | Verificar opciones por versión; no sobrescribir maestro. No se exige Trimesh como dependencia |
| V08 | Topología y conectividad (R05/R08) | Sin aristas wire/boundary inesperadas ni degeneradas; winding y componentes según diseño; sólido imprimible según geometría prevista | BMesh/Toolbox y comprobación independiente opcional; inspección de vacíos intencionales | Ninguna métrica basta sola; no convertir huecos funcionales en fallos ciegos |
| V09 | Laminado Creality Print (R08/R09) | Perfil K1C + PLA + boquilla 0,4 mm elegido, escala y orientación correctas, laminado sin advertencias no resueltas; guardar proyecto/evidencia | GUI inicialmente; CLI experimental con control de retorno/salida | Laminable ≠ imprimible con éxito; automatización pendiente |
| V10 | Impresión física | Dimensiones/deformación/función dentro de criterios acordados | Impresión controlada y medición | Fuera del alcance documental; futura fase y material requerido |

**Nota de envolvente:** bounds del cuerpo solo subestiman dimensiones si el relieve sobresale. Definir si 150 mm incluye ladrillos; este borrador usa provisionalmente la envolvente final. Las caras superior/interior no se confunden con bordes abiertos topológicamente de la superficie sólida. Drenajes funcionales no se deben tapar para lograr un conteo simple de agujeros.

### Controles negativos propuestos

1. Escala alterada; 2. ladrillo reducido a textura/material sin volumen; 3. una cara sin patrón; 4. ladrillo separado o esquina con brecha; 5. shell abierto, normales inconsistentes o cara degenerada; 6. pieza próxima pero desconectada; 7. pared bajo el umbral confirmado; 8. STL en escala incorrecta; 9. snapshot ausente o corrupto; 10. timeout después de mutación; 11. laminador abre sin generar salida; 12. warning o perfil equivocado. Un validador útil debe detectar sus casos asignados y marcar inconcluso los demás.

### Flujo de decisión

Contrato resuelto → snapshot previo verificado → medir escena evaluada → pruebas geométricas y relieve → exportar derivado sin alterar maestro → releer STL y comparar → aceptar geometría digital → revisar Creality Print con perfil declarado → registrar laminado. La impresión física es V10 y una puerta posterior. Si una verificación V02–V08 falla o es inconclusa, no promover revisión digital; guardar evidencia/candidato y corregir o restaurar. V09 no retroactivamente cambia la validez geométrica, pero sí condiciona declarar el artefacto preparado para imprimir. Tras fallo de restauración: detener, no continuar reintentos sobre estado incierto.

## Compatibilidad Codex / macOS Apple Silicon

Blender tiene soporte Apple Silicon documentado; la cadena Codex/MCP/validador y el CLI de Creality no han sido ejecutados aquí. BMesh reutiliza Blender; Toolbox necesita casar release; Trimesh es una dependencia adicional que solo se recomienda si aporta comprobación independiente. Codex debe registrar resultados observados, no convertir mensajes del agente en prueba. Véanse INV-01 a INV-04.

## Comunidad y mantenimiento

Toolbox y Trimesh tienen proyectos públicos mantenidos con evidencia puntual descrita en INV-03/04. Creality publica un CLI y DMG ARM64, pero #634 advierte de una distribución Windows distinta; no inferir fallo o éxito macOS. Ningún caso comunitario revisado acredita todo CU-01 en Apple Silicon. Sin costo local adicional para BMesh; dependencias y licencias están en informes citados. Sin costos monetarios verificados.

## Aplicación al CU-01

Primera edición de aceptación: crear macetero resuelto, medir; cambiar solo tamaño/paso de ladrillo; repetir V02–V09, comparar con revisión base y mostrar que el maestro sigue editable. Los requisitos pendientes no se declaran aprobados. Impresión física se planifica solo tras revisión de laminado y criterios de prueba.

## Riesgos y preguntas abiertas

Bloquean cerrar protocolo: espesor 2/20 mm, base y drenaje; confirmar referencia de 150 mm; tolerancia digital propuesta; profundidad/tamaño mínimo del relieve y criterio de continuidad. Faltan versiones exactas y efectividad de automatización CLI. Ninguna métrica de topología garantiza fuerza, estanqueidad o extrusión correcta. V10 requiere un protocolo físico independiente.

## Recomendación y próximos experimentos (sin ejecutarlos)

Reutilizar primero BMesh/Toolbox; comparar STL con Trimesh si la dependencia se justifica; usar Creality Print GUI como evidencia de laminado, con CLI como experimento separado. Hacer una prueba por control negativo y registrar falsos positivos/negativos. Congelar versiones, conservar snapshots y repetir la edición incremental. **Confianza alta** en estructura general, **media/baja** en umbrales y eficacia local hasta prueba.
