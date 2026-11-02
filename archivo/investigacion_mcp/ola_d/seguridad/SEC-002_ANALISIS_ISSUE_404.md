# SEC-002 — Aplicabilidad del issue #404
**Consulta:** 2026-11-02. **Resultado:** reporte específico para 1.6.0; aplicabilidad a 2.2.6 no establecida.

## Reporte original

El [issue #404](https://github.com/ahujasid/mcp-for-blender/issues/404) se abrió el 21-oct-2026. Describe addon Blender escuchando TCP local por puerto default; JSON `type=execute_code`; despacho del handler a `exec(code, namespace)` sin autenticación. Indica además que MCP `execute_blender_code` reenvía el código al comando. El investigador reportó escribir un archivo marcador inocuo y enlaza la ruta de ejecución. El campo Version dice `1.6.0`. El panel visible de relación/development informa “No branches or pull requests”. El issue se observa abierto.

## Versión y trazabilidad

El manifiesto de rama actual [pyproject.toml](https://github.com/ahujasid/mcp-for-blender/blob/main/pyproject.toml) reporta paquete 2.2.6, Python ≥3.10. GitHub [Releases](https://github.com/ahujasid/mcp-for-blender/releases) dice que no hay releases. La consulta de tags/API no fue accesible; no se recuperó SHA completo. Por tanto no se puede mapear 1.6.0 a commit, comprobar tag 2.2.6, comparar código por diff ni enlazar servidor y addon instalados. La rama `main` no sustituye una versión identificable.

## Respuestas

| Pregunta | Respuesta basada en evidencia |
|---|---|
| ¿Qué reporta? | Socket sin autenticación que alcanza ejecución Python en Blender; reporte describe reproducción externa inocua y revisión estática. |
| ¿A qué versión/commit? | Issue declara 1.6.0; SHA no indicado/obtenido. |
| ¿Corrección identificable? | No en el issue consultado; no aparece rama/PR enlazada. No descarta fix fuera de la vista, pero no se presume. |
| ¿Release/commit donde aparece? | No identificada; repositorio no lista releases. |
| ¿Candidato corregido? | No determinable; 2.2.6 aparece en pyproject de `main`, sin tag/artefacto/commit verificable. |
| ¿Qué falta? | SHA/tag 2.2.6, addon correspondiente, bind exacto, parser/auth, diff/PR y defaults de safe mode. |

## Conclusión

#404 respalda un hallazgo reportado para 1.6.0, no para 2.2.6. `main` actual muestra una herramienta Python genérica y forwarding, pero no demuestra que el sink actual del addon sea igual. **Aplicabilidad a candidata INCONCLUSA**, impacto potencial crítico si listener y sink siguen presentes.
