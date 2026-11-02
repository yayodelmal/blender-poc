# PREP-005 — Runbook propuesto para EXP-001

Estado: borrador para revisión. Ninguno de los pasos de preparación de entorno o experimento se ha ejecutado. Por el bloqueo de PREP-003, no se debe iniciar el runbook hasta resolver el alcance de ejecución Python y obtener autorización explícita.

## Secuencia propuesta

1. **Autorización y congelación del alcance.** Aprobar por escrito el experimento y sus límites, incluyendo aceptación o resolución del riesgo de Python arbitrario. EXP-001 debe usar únicamente una escena desechable, sin datos privados ni geometría de producción.
2. **Respaldo.** Copiar de forma segura la configuración existente de Codex y preferencias pertinentes de Blender antes de cualquier cambio. Proteger y redactar secretos en las evidencias. Registrar hashes de respaldo y ubicación local.
3. **Aislamiento.** Crear un directorio de prueba dedicado con permisos restringidos, separado de proyectos y documentos de usuario. La creación del directorio requiere autorización de ejecución.
4. **Adquisición aprobada, si faltan componentes.** Instalar solo artefactos que el responsable apruebe, fijados por versión y SHA; documentar fuente. Requisito de servidor Python >=3.10. El Python de sistema observado, 3.9.6, no satisface ese mínimo. No usar una actualización mutable de main.
5. **Integridad y versiones.** Registrar macOS, Codex, Blender, Python/uv, commit, versiones servidor/addon/protocolo, rutas cargadas y SHA-256. No continuar si addon y servidor no corresponden exactamente al candidato revisado.
6. **Addon.** Instalar/activar el addon correspondiente solo en la instancia y perfil de prueba acordados. Confirmar manualmente que la escena contiene exclusivamente contenido desechable.
7. **Codex MCP.** Respaldar y luego modificar configuración únicamente tras resolver PREP-003. No presentar enabled_tools como control del socket. Excluir herramientas de escritura/ejecución y verificar la lista expuesta; si una herramienta de lectura puede invocar execute_code, detenerse hasta aprobación y control compensatorio explícito.
8. **Listener.** Antes de cualquier llamada MCP, observar endpoint, familia, puerto, propietario y ausencia de exposición externa/túneles pertinentes. No enviar conexiones de prueba. Detenerse si el bind excede loopback o el propietario no es el esperado.
9. **Conectividad acotada.** Solo tras las comprobaciones anteriores, consultar estado y metadatos de la escena desechable según el protocolo aprobado. Guardar solicitudes, respuesta, hora, versiones y registros redactados. Dado el comportamiento interno observado, la consulta de escena no es estrictamente solo lectura a nivel de ejecución.
10. **Desconexión controlada.** Cerrar la sesión MCP de forma prevista, observar errores/desconexión en cliente y servidor y confirmar que el socket desaparece al cerrar Blender. No provocar fallos fuera de los límites aprobados.
11. **Cierre y reversión.** Cerrar procesos, confirmar listener ausente, restaurar configuración y preferencias respaldadas, retirar componentes temporales solo si fueron instalados para el ensayo y estaba aprobada su retirada. Verificar hashes/estado restaurado y registrar cualquier desviación.
12. **Informe.** Clasificar PASS/FAIL/INCONCLUSIVE/NOT RUN y adjuntar evidencia con datos sensibles redactados. No interpretar logs como entrenamiento automático del modelo.

## Autorización explícita requerida

Requieren aprobación del responsable: instalar software/artefactos; crear directorios de trabajo; modificar configuración Codex o preferencias; instalar/activar addon; iniciar Blender o MCP; abrir listener; conectar Codex; consultar la escena; escribir logs fuera de esta documentación; cerrar procesos ajenos a la sesión; retirar componentes; restaurar configuraciones. Este documento no autoriza ninguno de esos actos.

## Recuperación ante estado incierto

Si ocurre timeout, no repetir automáticamente una llamada cuyo resultado no se conoce. Primero observar estado del proceso, socket y escena por una vía autorizada. Si hay cambio humano durante la sesión, detener llamadas, conservar evidencia, no restaurar sobre cambios ajenos y pedir resolución del responsable. Si no se puede demostrar la reversión, informar INCONCLUSIVE y preservar respaldos.

## Condición para pasar a EXP-002

EXP-001 debe terminar con identidad de artefactos acreditada, herramientas efectivamente acotadas al alcance aprobado, listener limitado y cerrado, registros completos y configuración restaurada. La ejecución de Python interna de herramientas de inspección requiere resolución explícita antes de iniciar.
