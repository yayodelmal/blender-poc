# INV-04 — Validadores geométricos y revisión en Creality Print
**Fecha de investigación:** 2026-11-02.  
**Responsable/agente:** validacion.  
**Estado:** finalizado documentalmente; integración, precisión y ejecución ARM64 IN PROGRESS.

## Pregunta investigada

¿Qué herramientas existentes permiten comprobar malla, dimensiones y exportación, y qué parte del laminado en Creality Print puede automatizarse con evidencia?

Insumos: README, cinco documentos base, plan, plantilla e INV-03. **Pruebas propias: ninguna.** Solo lectura web/local y escritura de Markdown. `current`, `main` y `master` son referencias móviles; no se capturaron SHAs. Parte de documentación Blender fue recuperada por resultados del buscador: aperturas directas devolvieron 402; se señala esa evidencia parcial.

## Evidencia

| Afirmación | Fuente/URL | Fecha/versión | Tipo de evidencia | Confianza |
|---|---|---|---|---|
| BMesh expone `is_manifold`, `is_contiguous`, `is_boundary`, `is_wire` y enlaces a caras. | [BMesh](https://docs.blender.org/api/5.1/bmesh.types.html) | API 5.1; consulta 2026-11-02 | Documentación primaria, extracto indexado | Alta para API, pendiente ejecución |
| `to_mesh()` sobre objeto evaluado incluye modificadores; sobre original no. | [Depsgraph](https://docs.blender.org/api/3.6/bpy.types.Depsgraph.html) | API 3.6 | Documentación primaria, extracto indexado | Alta para distinción; versión local desconocida |
| Trimesh distingue watertight, winding consistente e `is_volume`; no son sinónimos. | [API Trimesh](https://trimesh.org/trimesh.base.html) | Docs 5.2.0 | Documentación primaria abierta | Alta |
| Creality documenta entrada STL/OBJ, carga de presets y laminado CLI. | [README oficial](https://github.com/CrealityOfficial/CrealityPrint/blob/master/README.md) | master, consulta 2026-11-02 | Documentación primaria indexada | Alta para documentación; media para binario concreto |
| Código distingue modo CLI y despacha `CLI::run`. | [CrealityPrint.cpp](https://github.com/CrealityOfficial/CrealityPrint/blob/master/src/CrealityPrint.cpp) | master | Código indexado, no compilado | Media |
| Existen DMG Apple Silicon publicados. | [Releases](https://github.com/CrealityOfficial/CrealityPrint/releases) | 7.3.0.6157 ARM64, asset 2026-10-10 | Publicación primaria indexada | Alta para disponibilidad |
| Un usuario reporta CLI sin salida ni terminación en Windows 11/K2 Plus, build 7.3.0.6151. | [Issue #634](https://github.com/CrealityOfficial/CrealityPrint/issues/634) | 2026-10-09; abierto en consulta | Issue/testimonio comunitario | Alta para existencia del reporte; no prueba macOS |
| Solicitud de API local/MCP; no es documentación de API disponible. | [Issue #645](https://github.com/CrealityOfficial/CrealityPrint/issues/645) | 2026-10-31; abierto | Issue/testimonio comunitario | Alta para petición; no prueba ausencia universal de CLI |

## Capacidades confirmadas y limitaciones

**BMesh/API:** permite consultar topología, no certifica fabricación. Medir la malla original puede omitir el relieve de modificadores. La API de objeto evaluado cubre esa distinción; no se auditó el exportador instalado. [Depsgraph](https://docs.blender.org/api/3.6/bpy.types.Depsgraph.html).

**Propuesta derivada:** obtener vértices evaluados e instancias relevantes, llevarlos a coordenadas mundiales y calcular envolvente alineada con ejes contractuales. No basta la dimensión de un objeto del cuerpo si los ladrillos sobresalen. Repetir comparación sobre el STL reimportado con convención de milímetros y tolerancia explícita. Los detalles concretos de opciones STL de cada versión deben verificarse antes de implementar; no se logró fuente suficiente para fijar nombres de operadores actuales.

**Toolbox:** reutilizar los checks existentes de geometría y diagnóstico visual, antes de crear un validador equivalente. Análisis de intersecciones y espesores necesita comprobar alcance, escala y versión; la corrección Make Manifold puede cambiar intención. El historial 1.1.4 retiró una operación que introducía defectos, por lo que reparar exige volver a validar. [Historial](https://extensions.blender.org/add-ons/print3d-toolbox/versions/). Alcance, licencia y mantenimiento complementarios en INV-03.

**Trimesh:** `is_watertight` exige dos caras por arista; `is_winding_consistent` comprueba orientación de aristas compartidas; `is_volume` añade condiciones de volumen y orientación. Una intersección booleana puede usar motores externos. Ninguna de estas propiedades por sí sola verifica resolución FDM o todos los errores geométricos. [API](https://trimesh.org/trimesh.base.html).

Importación/triángulos, bounds y componentes permiten una segunda lectura del archivo. Debe registrarse si el loader procesó o fusionó vértices: una limpieza silenciosa puede ocultar el estado original. El informe debe separar geometría leída y reparaciones. No se ha construido ni ejecutado este procedimiento.

**Creality Print:** README documenta `--slice 0` para todas las placas, `--outputdir`, `--load_settings`, `--load_filaments`, `--debug` y `--logfile`; STL requiere ajustes externos que un proyecto puede contener. Los ejemplos son Windows. No equivalen a un comando macOS probado ni garantizan paridad de `master` con DMG 7.3.0. [README](https://github.com/CrealityOfficial/CrealityPrint/blob/master/README.md).

No se verificó API HTTP pública ni MCP oficial. #645 es una petición del usuario y su afirmación de control exclusivamente GUI entra en tensión con el README CLI; prevalece la distinción entre documentación de interfaz y funcionamiento de una distribución. #634 muestra un fallo concreto en Windows, **no evidencia de fallo macOS/K1C**. [#645](https://github.com/CrealityOfficial/CrealityPrint/issues/645), [#634](https://github.com/CrealityOfficial/CrealityPrint/issues/634).

## Compatibilidad Codex / macOS Apple Silicon

| Componente | Evaluación | Dependencias/costos |
|---|---|---|
| BMesh/Blender | API local integrada; soporte Apple Silicon de Blender documentado, integración con Codex depende del puente elegido y permisos. No probada aquí. | Blender; sin proceso adicional para BMesh. |
| Toolbox | Extensión Blender; no MCP por sí misma. Compatibilidad concreta exige casar versión de extensión y Blender. | GPL-3.0-or-later; sin tarifa identificada. |
| Trimesh | Python; ARM64 plausible, matriz concreta de wheels y extras no verificada. No MCP incluido. | MIT; NumPy es dependencia básica, extras pueden fallar al invocar funciones ausentes. |
| Creality Print | DMG ARM64 publicado; CLI vía Codex es hipótesis de integración local. | Descarga pública; repo muestra AGPL-3.0 y licencia adicional, sin auditoría de todas las dependencias. |

[Requisitos Blender](https://www.blender.org/download/requirements/), [Toolbox](https://extensions.blender.org/add-ons/print3d-toolbox/), [Trimesh instalación](https://trimesh.org/install.html), [Trimesh repo](https://github.com/mikedh/trimesh), [Creality repo](https://github.com/CrealityOfficial/CrealityPrint).

No hace falta proponer Docker ni compilar Creality para el primer experimento. Compilar agregaría Xcode, CMake y toolchain; no está autorizado ni justificado ahora. Costos relevantes: agente, integración, CPU/RAM, tiempo de laminado y material de futuras pruebas; no se cuantificaron.

## Comunidad y mantenimiento

Trimesh muestra 6.063 commits, 3,7k estrellas y 702 forks en la página consultada; además documentación versionada 5.2.0. No se obtuvo fecha exacta de último commit. Estas señales indican ecosistema, no precisión de un check específico. [Repositorio](https://github.com/mikedh/trimesh).

Creality muestra 587 estrellas y 152 forks; releases con assets ARM64 fechados y los issues #634/#645 prueban actividad pública puntual. No usar conteo de issues como tasa de defectos ni asumir corrección porque exista código posterior en `master`. [Repositorio](https://github.com/CrealityOfficial/CrealityPrint), [releases](https://github.com/CrealityOfficial/CrealityPrint/releases).

No se encontró en las fuentes revisadas una experiencia reproducible de Codex → Blender → STL → Creality Print en ARM64 para este CU-01.

## Aplicación al CU-01

Cadena propuesta para VAL-001:

1. Contrato: 150×150×60 mm exteriores; ladrillos reales y editables en cuatro caras; continuidad en esquinas. Pared 2/20 mm, base y drenaje INCONCLUSIVE hasta confirmar.
2. Escena: medir malla evaluada e inspeccionar secciones, unión del relieve y esquinas. Conservar original paramétrico.
3. Malla: bordes/manifold, orientación, degenerados, componentes e intersecciones; espesor con método y límites documentados. No aceptar solamente `is_watertight`.
4. STL: volver a cargar y comparar medidas, secciones y relieve; no confundir STL con archivo editable de autoría.
5. Creality: abrir STL, elegir K1C/PLA/0,4 mm explícitamente, verificar escala y orientación, laminar y revisar capas, paredes, base si corresponde, voladizos, trayectorias de ladrillos y advertencias. Guardar proyecto y evidencia de ajustes.

La boca y eventual drenaje son vacíos funcionales delimitados por superficies cerradas del material: no deben repararse tapándolos para alcanzar un contador. Es inferencia geométrica de diseño, no resultado obtenido. Editabilidad requiere prueba de cambio en `.blend`, no un check del STL.

## Riesgos y preguntas abiertas

- Tolerancias dimensionales, altura/profundidad mínima de ladrillo, pared, base y drenaje aún sin especificar.
- Los checks de espesor pueden muestrear y omitir detalles; ausencia de aviso no demuestra cumplimiento exhaustivo.
- Extras de Trimesh para colisión/proximidad/booleanas pueden tener requisitos nativos: verificar solo los necesarios antes de añadirlos.
- Un CLI documentado puede no estar funcional en el DMG elegido. Falta verificar códigos de salida, logs, archivos y terminación; evitar inferir éxito del lanzamiento del proceso.
- No se verificó extracción estructurada estable de todas las advertencias de Creality ni automatización completa de revisión visual.

## Recomendación y próximos experimentos (sin ejecutarlos)

**Reutilizar Blender/Toolbox para diagnóstico, añadir Trimesh si aporta independencia del exportador y mantener revisión GUI de Creality como paso explícito.** Confianza alta en capacidades básicas documentadas, media en integración y baja en validación FDM integral.

La CLI de Creality merece experimento acotado, no desarrollo de un MCP nuevo. Tras autorización: fijar DMG/versión; comprobar ayuda del binario; laminar un proyecto mínimo y STL con presets guardados; capturar salida, tiempo límite y G-code; comparar capas con GUI. Si falla, conservar revisión manual y marcar automatización INCONCLUSIVE. No enviar trabajos a impresora durante estas verificaciones. Después ejecutar los casos negativos de INV-03 y CU-01; solo una futura impresión evalúa desempeño físico.
