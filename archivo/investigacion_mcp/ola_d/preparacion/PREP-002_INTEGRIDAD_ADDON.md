# PREP-002 — Integridad y correspondencia del addon

## Resultado

La referencia de código prevista es el commit completo 992233bb258975a05eec8b5691465c50c2831e34 del repositorio ahujasid/mcp-for-blender. El árbol auditado declara versión de servidor 2.2.6 y el addon empaquetado declara versión 1.8/protocolo 15, según SEC-005/006. No se encontró una instalación local verificable del servidor, Blender o addon. La correspondencia local servidor-addon queda BLOCKED.

## Evidencia documental del candidato

- [pyproject.toml, SHA fijado](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/pyproject.toml) es el manifiesto del servidor.
- [Addon empaquetado, SHA fijado](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/bundled/addon.py) pertenece al mismo árbol Git al fijar el mismo SHA.
- El código del manager del servidor espera protocolo del addon; la compatibilidad declarada en el commit es protocolo 15. Esto acredita correspondencia del árbol fuente, no del artefacto efectivamente instalado en el equipo.
- No se debe sustituir el SHA fijado por main, ni utilizar un instalador que descargue una rama mutable, sin revisar nuevamente procedencia y contenido.

## Artefactos publicados y hashes conocidos

SEC-005 registró metadatos de PyPI para MCP for Blender 2.2.6, sin procedencia verificable que establezca equivalencia con el commit auditado:

| Artefacto | SHA-256 publicado | Limitación |
|---|---|---|
| wheel 2.2.6 | 6f47cef6a5b5e2084269fcdec027fa8c6fb097157f1bf32cd922a711e59d738c | No se verificó que su contenido sea idéntico al árbol Git fijado |
| sdist 2.2.6 | 0b4f306804267be804cf315744aa55d010485dd6d919d4bb7270ec3f51b6efd9 | No se verificó que su contenido sea idéntico al árbol Git fijado |

No se conoce aún el hash esperado del addon extraído, porque no se descargó ni examinó el artefacto durante esta preparación. Un hash solo demuestra identidad de bytes contra una referencia conocida; no demuestra por sí mismo que la fuente sea confiable.

## Registro requerido si se autoriza la preparación de artefactos

1. Registrar SHA de Git y URL permanente de cada archivo fuente usado.
2. Registrar versión del servidor, versión del addon y protocolo MCP/addon observado.
3. Obtener únicamente el artefacto aprobado; calcular SHA-256 de wheel/sdist y del addon instalado o extraído.
4. Comparar bytes o diff del addon contra el archivo del commit fijado, documentando cualquier diferencia de empaquetado.
5. Registrar ruta del addon que Blender realmente carga y metadatos del archivo; no asumir que una copia con el mismo nombre corresponde al candidato.
6. Descartar para el experimento cualquier copia de origen desconocido o rama mutable.

## Estado y acciones pendientes

| Comprobación | Estado | Acción futura |
|---|---|---|
| Commit fuente identificado | READY documental | Mantener SHA completo en el expediente |
| Manifiesto y addon en un mismo árbol Git | READY documental | Usar enlaces permanentes al SHA |
| Versiones declaradas compatibles | READY documental, no runtime | Confirmar handshake solo en fase autorizada |
| Instalación local correspondiente | BLOCKED | No hay Blender/MCP local detectado; acreditar artefactos antes de activar |
| Copias locales desconocidas | UNKNOWN | Inspeccionar rutas reales de Blender después de instalar/identificar Blender |
| Hash de addon local | UNKNOWN | Calcular y comparar solo después de obtener autorización para preparación de componentes |

Fuentes: SEC-005_REVISION_REPRODUCIBLE.md, SEC-006_SOCKET_Y_EJECUCION.md y enlaces permanentes al commit indicados arriba. No se modificó ni activó ningún archivo.
