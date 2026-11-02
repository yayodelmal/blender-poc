# SEC-005 — Revisión reproducible

**Fecha:** 2026-11-02. **Alcance:** identificación de fuente y análisis estático; no se ejecutó ni instaló software.

## Identidad y publicación

Repositorio canónico: [ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender). El HEAD observado de la rama principal es **992233bb258975a05eec8b5691465c50c2831e34** ([commit permanente](https://github.com/ahujasid/mcp-for-blender/commit/992233bb258975a05eec8b5691465c50c2831e34), mensaje “docs: add badge to README”).

Fuentes consultadas en ese SHA: [pyproject.toml](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/pyproject.toml), [server.py](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/server.py), [addon_manager.py](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/addon_manager.py), [safe_mode.py](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/safe_mode.py), [addon.py raíz](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/addon.py) y [addon.py empaquetado](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/bundled/addon.py).

El manifiesto de este commit declara mcp-for-blender 2.2.6, Python >=3.10, mcp>=1.26.0,<2, httpx>=0.27.0 y el empaquetado de src/blender_mcp/bundled/addon.py.

La página de [releases de GitHub](https://github.com/ahujasid/mcp-for-blender/releases) no lista releases formales. La página y API de tags no se pudieron consultar con las fuentes disponibles; no afirmo que no existan tags ni cuál sería el último.

PyPI publica [mcp-for-blender 2.2.6](https://pypi.org/project/mcp-for-blender/2.2.6/). Su [JSON](https://pypi.org/pypi/mcp-for-blender/2.2.6/json) identifica wheel universal publicado el 2026-10-28, SHA-256 6f47cef6a5b5e2084269fcdec027fa8c6fb097157f1bf32cd922a711e59d738c; sdist SHA-256 0b4f306804267be804cf315744aa55d010485dd6d919d4bb7270ec3f51b6efd9. La ficha PyPI indica que los archivos se publicaron sin provenance. Hay artefactos identificables por hash, pero no se descargaron ni compararon con Git y no se encontró atestación que vincule sus hashes con el SHA anterior. La auditoría se refiere al árbol del commit, no certifica el wheel.

## Correspondencia del addon

Ambos archivos addon existen en el árbol del commit. addon_manager.get_bundled_addon_path selecciona primero bundled/addon.py y deja el archivo raíz como fallback del checkout editable ([líneas 162–175](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/addon_manager.py#L162-L175)). install_addon copia el archivo resuelto a la carpeta de Blender ([líneas 267–335](https://github.com/ahujasid/mcp-for-blender/blob/992233bb258975a05eec8b5691465c50c2831e34/src/blender_mcp/addon_manager.py#L267-L335)). En el mismo commit, el servidor y el addon empaquetado pertenecen a un árbol Git coherente.

No se obtuvo comparación integral ni hash blob para afirmar que la copia raíz y la copia bundled son idénticas byte a byte. El addon declara versión propia 1.8 y protocolo 15, distintos de la versión de paquete 2.2.6; manager y addon declaran protocolo 15. Tampoco se inspeccionó el archivo efectivamente instalado/cargado en Blender.

El addon consulta una URL mutable main para comprobar actualizaciones y permite instalar la descarga manualmente. No instala durante la comprobación. Si se acepta esa actualización, el código cargado ya no se identifica solo por el SHA auditado. En una prueba futura se debe registrar el hash del addon cargado.

| Elemento | Estado |
|---|---|
| Árbol fuente | SHA completo fijado; enlaces por archivo |
| Versión manifestada | 2.2.6 |
| Release/tag GitHub | Sin release listada; último tag no verificable |
| Artefactos PyPI | Wheel y sdist publicados con hashes; no comparados con Git |
| Addon en árbol | Versión 1.8, protocolo 15 |
| Hash instalado / dependencias locales | Desconocidos, no inspeccionados |

**Conclusión:** el commit auditado es reproducible como referencia fuente. La equivalencia del artefacto PyPI y addon instalado requiere comparación posterior autorizada.

