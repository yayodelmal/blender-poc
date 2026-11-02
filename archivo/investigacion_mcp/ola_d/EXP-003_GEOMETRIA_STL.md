# EXP-003 — Relieve físico, validación y STL
**Estado:** protocolo preparado; **NOT RUN**. No construir CU-01 ni imprimir durante este experimento.

## Objetivo e hipótesis

En una pieza intermedia de ensayo, demostrar que un relieve geométrico real puede parametrizarse/modificarse, medirse sobre geometría evaluada, detectar controles negativos, exportarse a STL sin destruir el maestro y recuperar dimensiones al releer archivo.

## Dependencias y versiones

EXP-001 y EXP-002 PASS; Blender/MCP/Python/uv/Codex fijados; Toolbox si está disponible de forma aprobada, versión anotada. No instalar Trimesh, MCP Printable ni skills como dependencias. Lectura STL puede hacerse con capacidad disponible ya aprobada; si no está disponible, marcar comparación independiente INCONCLUSIVE. Creality Print no necesario para este ensayo, salvo prueba adicional autorizada.

## Precondiciones y diseño

Contrato de experimento con tamaño/tolerancia aprobados; escena desechable; almacenamiento para maestro, exportación y reimportación; backup validado. Pieza propuesta: placa rectangular de tamaño moderado con filas de relieves prismáticos conectados en dos caras y una esquina; no se fijan dimensiones FDM ni valores en este protocolo. Anotar dimensiones del cuerpo, profundidad, paso, cuenta, unidades y componentes esperados.

## Procedimiento

1. Crear pieza paramétrica, guardar maestro revision A y medir bounds/inputs/objetos.
2. Verificar que relieve sobresale de la superficie y está físicamente unido (no textura; no superficies solo visuales). Inspeccionar secciones y componentes.
3. Cambiar un parámetro del patrón; medir bounding box de geometría evaluada que incluye modificadores y transformar a coordenadas acordadas. Confirmar dimensiones invariantes y cambio en relieve.
4. Ejecutar checks disponibles de topología: fronteras inesperadas, degenerados, orientación, componentes; interpretar vacíos diseñados según contrato. Ningún `watertight` único define aceptación.
5. Guardar maestro y exportar selección/derivado STL en archivo separado; verificar opciones/unidades de la versión. Confirmar maestro y nodos permanecen editables.
6. Reimportar STL en escena aislada; comparar bounds por eje dentro tolerancia aprobada, sección/perfil del relieve y número de componentes. Registrar diferencias de triangulación esperables.
7. Ejecutar controles negativos independientes y confirmar que check asignado produce FAIL; restaurar escena limpia desde maestro aceptado y medir de nuevo.

## Controles negativos

N1 relieve reemplazado solo por material/textura; N2 malla base medida sin evaluar modificador; N3 relieve separado apenas del cuerpo; N4 cara/superficie abierta inesperada; N5 dimensión de cuerpo alterada; N6 escala STL incorrecta; N7 exportación que aplica/destruye el maestro; N8 componente suelto; N9 modificador deshabilitado al exportar. No todos tienen detector automatizado: revisión se asigna por método y se anota si manual.

## Evidencias obligatorias

Versiones/hashes; contrato de ensayo; maestro antes/después; captura de grafo/modificador y geometría; medidas base/evaluada/STL; reporte de topología con método/unidad; STL separado; captura de reimportación y sección; logs de operaciones; negativo por negativo con estado esperado/observado; registro de revisión/restore. Si un resultado proviene solo de pantalla, etiquetarlo inspección visual.

## Criterios

- **PASS:** todas las invariantes cumplen tolerancia; relieve aparece en malla evaluada y STL, conectado según diseño; topología cumple los checks especificados; STL reimportado coincide; maestro conserva editabilidad.
- **FAIL:** cualquier dimensión fuera de tolerancia, relieve no físico/ausente/desconectado, defecto asignado no detectado, o exportación altera maestro.
- **INCONCLUSIVE:** modificadores/instancias no se incluyen o no se entiende escala; checker inaccesible; hueco funcional ambiguo; comparación no reproducible.
- **NOT RUN:** falta autorización, experimento anterior no pasa o condiciones no están fijadas.

## Riesgos y recuperación

STL triangulado no conserva parametricidad; exportar a ruta distinta. Unidad puede escalar por 1000; comparar bounds. Instancias requieren materialización en exportador, comprobar resultado sin alterar grafo. Si falla snapshot o restauración, detener, conservar archivos y no reexportar desde estado incierto. Limpiar solo directorio de ensayo tras registrar evidencia y autorización.

## Puerta de avance

PASS permite diseñar integración de laminado simple/GUI (candidata EXP-004); no aprueba automáticamente CU-01, Creality Print/CLI ni impresión física. CU-01 requiere cerrar decisiones humanas pendientes y repetir criterios específicos.
