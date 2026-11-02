# EXP-001 — Conectividad Codex ↔ Blender MCP
**Estado:** protocolo preparado; **NOT RUN**. Requiere autorización explícita del responsable. No configurar ni ejecutar en esta ola.

## Objetivo e hipótesis

Demostrar conexión de lectura entre Codex, MCP for Blender y Blender ARM64, y conservar evidencia de errores/desconexión. Hipótesis: una versión fijada puede informar estado y metadatos de escena desechable a Codex sin modificarla. No se acepta que “servidor conectado” pruebe operación válida.

## Dependencias y versiones

Versión Codex CLI o app (registrar cuál), Blender/macOS/arquitectura, MCP ahujasid release + SHA, Python/uv, versión addon y transporte según D-02. Toolbox, Printable, Trimesh y skills no son dependencias de esta prueba. Hash y licencias del paquete registrados antes de uso.

## Precondiciones

- Responsable aprueba alcance EXP-001 y cualquier configuración necesaria; respaldo de preferencias existentes y plan de reversión.
- Static review del tag candidato: confirmar bind loopback, puerto, autenticación, herramientas activadas y resultado de #404; si no es aceptable, detener.
- Sin otros servicios/addons en el puerto; acceso local exclusivo, sin túneles, LAN ni escena privada. No instalar software dentro de este protocolo.
- Blender abierto manualmente con escena vacía desechable, observación de objetos/contador inicial y ruta de evidencia. Consentimiento/telemetría revisados por responsable; nada se habilita por omisión.
- Codex workspace de prueba separado, límites de herramienta en lectura, registro de versión y configuración; no autorizar ejecución Python mutante.

## Procedimiento reproducible

1. Registrar fecha, macOS, arquitectura, Blender, addon, Codex (producto/versión/modelo), MCP commit, Python/uv, endpoint local, variables de telemetría (sin secretos).
2. Activar addon según documentación de la versión aprobada y observar el estado en Blender. No cambiar preferencias no relacionadas.
3. Iniciar el servidor MCP configurado por el responsable; revisar listado de herramientas en Codex y verificar nombre/transport. No realizar llamada de escritura.
4. Solicitar estado del addon/Blender; guardar respuesta íntegra saneada. Confirmar versión y conexión.
5. Pedir metadatos de escena desechable (objetos y unidades si el API los devuelve). Comparar con inspección manual en UI: conteo/nombres y valores visibles.
6. Repetir una llamada de solo lectura y demostrar ausencia de cambio en escena (comparación de conteo/estado; cualquier hash solo si no cambia archivos de estado volátiles).
7. En punto acordado, desconectar el addon o parar servidor de manera manual; intentar una llamada de lectura y registrar timeout/error. Reconectar y observar si recuperación de lectura funciona. No inducir crash ni mutaciones.
8. Confirmar que logs de Codex, MCP y Blender contienen timestamps/error; no exigir mismo almacenamiento si una capa solo expone stderr/eventos. Redactar rutas privadas/secrets.

## Resultados esperados y evidencias

Bundle: hoja de versiones/hashes; screenshot del complemento activo; captura/lista Codex de servidor/herramientas; salida de estado/escena; inspección manual comparativa; conteo antes/después; log de desconexión/recuperación por capa; registro de telemetry opt-in/out; checklist de limpieza. No capturar contenido de usuario no relacionado.

## Controles negativos

- MCP configurado con nombre incorrecto: debe detectarse servidor no conectado, no fabricar PASS.
- Addon apagado: consulta debe fallar o reportar inactivo.
- Servidor detenido durante llamada: resultado incierto/fallo registrado; no mutar automáticamente al reconectar.
- Escena con nombre de objeto conocido y uno distinto: lectura debe reflejar verdad observada sin cambio.
- Tool devuelta como texto con error sin bandera protocolaria: registrar capa de transporte y estado real.

## Criterios

- **PASS:** status, inventario y llamada read-only coinciden con Blender; escena intacta; desconexión queda como error/incertidumbre en log; versiones y configuración se reproducen.
- **FAIL:** herramienta reporta conectado pero datos son falsos; una llamada de lectura muta escena; endpoint accesible fuera del límite aprobado; seguridad #404 aplicable sin mitigación aceptada; logs exponen secretos.
- **INCONCLUSIVE:** no se puede determinar bind/alcance, la app no muestra inventario, falta capa de log, versiones inconsistentes o estado incierto no reconciliable.
- **NOT RUN:** falta autorización/precondición o experimento no iniciado.

## Riesgos, recuperación y limpieza

No enviar código arbitrario vía `execute_blender_code` en esta prueba; incluso lecturas por esa herramienta implican envío de código controlado. Si configuración de MCP requiere code execution para inspección, debe revisarse como riesgo del protocolo antes de autorizarlo. Ante estado incierto, cerrar llamada, inspeccionar UI, no reintentar operaciones mutantes. Al acabar detener servidor y addon de forma normal; restaurar configuración inicial según copia autorizada; cerrar Blender desechable sin guardarlo; confirmar que no quedó proceso/puerto ni telemetría activada. No modificar preferencias reales sin aprobación específica.

## Avance

EXP-002 puede prepararse documentalmente antes; su ejecución depende de PASS de seguridad/conectividad y autorización separada. EXP-001 no aprueba creación, exportación ni CU-01.
