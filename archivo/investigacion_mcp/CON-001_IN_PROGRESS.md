# CON-001 / INV-06 — Contrato de diseño
**Fecha de investigación:** 2026-11-02.  
**Responsable/agente:** coordinador técnico / Codex.  
**Estado:** en curso — borrador IN PROGRESS, sin implementación ni aprobación de parámetros abiertos.

## Pregunta investigada

¿Cómo conservar requisitos y trazabilidad durante ediciones del CU-01, reutilizando formatos y mecanismos existentes?

## Evidencia

| Afirmación | Fuente/URL | Fecha/versión | Tipo de evidencia | Confianza |
|---|---|---|---|---|
| Python incluye lectura/escritura JSON en su biblioteca estándar | [json](https://docs.python.org/3/library/json.html) | Consulta 2026-11-02; página mutable, no versión local | Documentación primaria | Alta documental |
| JSON Schema permite declarar propiedades obligatorias y controlar campos adicionales | [Object](https://json-schema.org/understanding-json-schema/reference/object) | Consulta 2026-11-02 | Documentación primaria | Alta documental |
| YAML admite estructuras legibles y comentarios; necesita un procesador | [YAML](https://yaml.org/spec/1.2.2/) | 1.2.2, 2021-10-01; consulta 2026-11-02 | Documentación primaria | Alta documental |
| GN, propiedades y guardados nativos son reutilizables, pero no constituyen un contrato transaccional | [INV-05 y sus fuentes](INV-05_edicion_estado.md) | Consulta 2026-11-02; manuales de varias versiones | Documentación primaria y síntesis de investigación | Alta para existencia; media para aplicación |
| Separar contrato, maestro y salida puede reducir pérdida de requisitos | Propuesta de este documento | Borrador 0.1 | Hipótesis | Media; sin prueba propia |

No hay pruebas propias ni testimonios comunitarios específicos de este contrato. Los incidentes de persistencia se conservan en INV-05 con su contexto.

## Capacidades confirmadas y limitaciones

### Comparación de representaciones

| Alternativa | Ventaja | Límite | Recomendación provisional |
|---|---|---|---|
| Markdown con tablas | Revisión humana y cambios fáciles de explicar | Sin validación estructural automática | Usar ahora para acordar requisitos |
| JSON + esquema JSON Schema | Tipos explícitos, herramientas existentes, lectura JSON estándar Python | Esquema y validador adicional por elegir; validar estructura no verifica geometría | Preferido para futura automatización mínima |
| YAML | Comentarios y edición manual cómoda | Parser y reglas de resolución adicionales; aporta poco si escribe el agente | Alternativa si prima edición humana frecuente |
| Propiedades de `.blend` y entradas GN | Parámetros cerca del modelo | No sustituyen evidencia, historial ni invariantes verificadas | Guardar ID/revisión y parámetros; evitar dos contratos autoritativos |
| Solo conversación | Ninguna infraestructura nueva | Requisitos y estado difíciles de reproducir | No usar como única persistencia |

**Propuesta del coordinador:** contrato Markdown en esta fase; JSON versionado si la siguiente fase necesita comprobación automática. No se creó esquema, parser ni sincronizador. Si se adopta JSON, será la fuente autoritativa; Markdown será una vista y `.blend` guardará su referencia de revisión. Una discrepancia impide aceptar el cambio. Los formatos no resuelven por sí solos esa sincronización.

### Campos del contrato propuesto

| Grupo | Contenido mínimo | Regla |
|---|---|---|
| Identidad | ID CU-01, revisión, fecha, autor de decisión, estado | Revisiones aceptadas inmutables; cambios crean revisión nueva |
| Requisitos | ID, descripción, valor, unidad, origen, confirmado/propuesto/pendiente | Un valor pendiente no equivale a cero, falso ni requisito opcional |
| Medición | Referencia geométrica, tolerancia, método, evidencia requerida | Cada requisito apunta a una comprobación VAL |
| Modelo | Ruta `.blend`, revisión, IDs lógicos, parámetros GN/modificadores | Nombre visible no es identidad suficiente |
| Entorno | Versiones exactas Blender/addon/servidor/Codex/validadores/slicer, ARM64, macOS | Registrar en fase autorizada; hoy desconocido |
| Operación | ID, solicitud original, revisión base, parámetros permitidos, invariantes | Rechazar operación sobre revisión obsoleta |
| Resultado | Estado de llamada, de geometría, de validación y decisión | Mantener separados éxito técnico y aceptación |
| Artefactos | Snapshot previo, candidato, STL, reporte, proyecto de laminado | Asociar a revisión y, en ejecución futura, checksum |

### Instancia conceptual CU-01 (no ejecutable)

| ID | Requisito | Estado | Verificación |
|---|---|---|---|
| R01 | Exterior 150 × 150 × 60 mm | Confirmado por antecedentes; referencia del relieve pendiente | V02 |
| R02 | Pared 2 mm **o** 20 mm | Pendiente del usuario; sin valor por defecto | V05 (medición física/digital de espesor) |
| R03 | Base: presencia y espesor | Pendiente del usuario | V05 (inspección de presencia y medición) |
| R04 | Drenaje: presencia, cantidad, diámetro y ubicación | Pendiente del usuario | V05 (geometría y, si se requiere, ensayo de flujo) |
| R05 | Ladrillos geométricos en cuatro caras, continuidad en esquinas | Confirmado; tamaño, profundidad, juntas y criterio de continuidad pendientes | V03 (relieve/caras/esquinas) y V08 (topología) |
| R06 | Cambiar tamaño/distribución del patrón sin alterar dimensiones ni otros requisitos | Confirmado; operación concreta debe definir nuevos valores | V04 (edición), V02 (dimensiones), V03 (relieve) |
| R07 | Conservar maestro editable y reabrible | Confirmado como objetivo | V04 (edición/reapertura) y V06 (snapshot/restauración) |
| R08 | STL validado y revisado en Creality Print | Confirmado como objetivo | V07 (exportación/relectura), V08 (topología), V09 (laminado) |
| R09 | K1C, PLA, boquilla 0,4 mm | Confirmado; perfil/material/altura de capa y calibración pendientes | V09 (perfil de laminado); V10 solo si se acuerda prueba física |

**Decisión propuesta, aún no acordada:** medir la envolvente final incluyendo ladrillos. Si 150 mm describe solo el cuerpo, las dimensiones finales serán distintas y hay que revisar R01. No compensar silenciosamente reduciendo paredes o cavidad. Proponer un sólido conectado, con los ladrillos unidos físicamente al cuerpo; múltiples piezas requerirían un contrato distinto.

**Tolerancias propuestas para el experimento digital:** ±0,10 mm por dimensión exterior; diferencia máxima 0,05 mm por eje entre malla evaluada y STL reimportado. Son umbrales de ensayo del coordinador, no precisión garantizada de K1C ni estándar FDM. No quedan aceptados hasta revisión. Espesor mínimo, profundidad del relieve, ancho de junta y tolerancias físicas siguen pendientes de diseño/perfil; no derivarlos automáticamente de la boquilla.

### Cambio y aceptación

1. Resolver requisitos bloqueantes; registrar revisión base y pedido. «Más pequeños» requiere definir un nuevo valor o una propuesta explícita antes de aceptarla.
2. Comprobar que escena, contrato y snapshot corresponden a esa revisión. Guardar copia previa; no sobrescribir último aceptado.
3. Modificar solo parámetros permitidos. Para reducir ladrillos: tamaño/paso/distribución; preservar cuerpo, envolvente, espesor, base y drenaje acordados.
4. Medir candidato con VAL. Estados de prueba: PASS, FAIL, INCONCLUSO o NO EJECUTADO. No aceptar si una comprobación obligatoria no es PASS.
5. Si pasa, crear nueva revisión aceptada y enlazar evidencias. Si falla, conservar candidato separado, restaurar y volver a verificar.
6. Ante timeout: estado INCIERTO; inspeccionar antes de repetir. Proponer máximo dos intentos correctivos por operación, más el intento inicial. Agotado el límite, detener y reportar; no es una capacidad incorporada de MCP.

**Precondición de mutación:** si el snapshot no pudo escribirse y reabrirse/verificarse, no iniciar la operación. Si falla la restauración, no reintentar mutaciones: conservar evidencia, marcar estado incierto y escalar. Antes de promover o restaurar, comparar revisión/estado observado para detectar ediciones humanas concurrentes; detener y reconciliar si difieren.

Estado del diseño: BORRADOR → LISTO PARA ENSAYO → CANDIDATO → ACEPTADO DIGITAL / RECHAZADO / INCONCLUSO. «Aceptado digital» requiere V02–V08 aplicables en PASS y revisión documentada del maestro/snapshot. La preparación de laminado es una puerta separada V09; si falla o queda inconclusa, el modelo puede conservar aceptación geométrica digital, pero el artefacto no se declara listo para imprimir. V10 (impresión física) es otra etapa y requiere criterios propios; no se infiere de malla ni laminado.

No llamar “snapshot restaurado” a encontrar el archivo: V06 exige abrir la copia, comparar revisión e invariantes y volver a validarla. Un fallo de snapshot previo bloquea mutación; fallo de restauración bloquea nuevos intentos. La promoción de una revisión exige que contrato, maestro y candidato sean la misma revisión, sin edición humana concurrente pendiente.

## Compatibilidad Codex / macOS Apple Silicon

Markdown y JSON no dependen de CPU. Su consumo automático dentro de Blender/Codex no está probado. No se presupone un validador JSON Schema instalado. INV-01 e INV-05 separan soporte documental y cadena real pendiente.

## Comunidad y mantenimiento

Se reutilizan formatos documentados y capacidades Blender, no un framework nuevo. La salud de los componentes se evalúa en INV-01/05. Este contrato es específico del laboratorio: responsable propuesto Codex, aprobación de requisitos por el usuario. Costos: mantenimiento de revisión y almacenamiento; sin dependencia nueva en esta fase.

## Aplicación al CU-01

La prueba clave es editar ladrillos y demostrar simultáneamente conservación de R01–R04, continuidad R05 y editabilidad R07. Un material de ladrillo o un render no satisface R05. El archivo STL no reemplaza el maestro parametrizado.

## Riesgos y preguntas abiertas

Bloquean la aceptación final: pared, base, drenaje, alcance de las medidas, parámetros de relieve y tolerancias. También falta elegir versiones exactas y comprobar recuperación. No se encontró un contrato existente específico para CU-01 que haga innecesario acordar estos campos. La búsqueda no demuestra que no exista otro.

## Recomendación y próximos experimentos (sin ejecutarlos)

Reutilizar archivos y propiedades nativas; aprobar primero la semántica. Después ensayar un cambio válido, un cambio accidental de escala, una revisión obsoleta, un timeout y reapertura del maestro. Registrar qué requisitos detecta cada prueba. Automatizar solo las brechas demostradas; sin base de datos, gestor de agentes ni servicio de contratos por ahora.
