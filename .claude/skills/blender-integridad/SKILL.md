---
name: blender-integridad
description: Use when en blender-poc se va a registrar un hash o tamaño, sellar artefactos de un run, afirmar que un archivo es el validado, sobrescribir una revisión, o abrir un 3MF en Creality Print; también al pensar en teclear un SHA-256 a mano.
---

# blender-integridad

Dos incidentes (INC-BPY-001 e INC-BPY-002) vinieron de asociar un hash al archivo equivocado. La regla es mecánica: **los hashes los calcula una herramienta, nunca una persona ni un modelo.**

**Violar la letra de estas reglas es violar su espíritu.**

## Cómo sellar un run

```
python3 herramientas/sellar_carpeta.py RUN --validation PASS [--input ENTRADA.blend]
```

- Registra `artifacts/` (produced), `evidencias/`, `scripts/`, `logs/` (evidence) y cada `--input`. No incluye `reports/` (los informes no se hashean).
- Se detiene si `registro_artefactos.jsonl` ya existe y termina verificando todo.
- Para un solo archivo o casos especiales: `herramientas/sellar_artefacto.py seal|verify`. Detalle en `docs/04_procedimientos/INTEGRIDAD.md`.

Sellar **después** de que cierre el proceso que escribió el archivo y de comprobar su código de salida. Volver a verificar tras la validación: `sellar_artefacto.py verify --registro RUN/registro_artefactos.jsonl`. Si algo sale `CAMBIADO`, el artefacto no se promueve.

## Reglas que no se negocian

- Nunca teclear un hash o un tamaño, ni copiarlo de otro informe.
- Un archivo nuevo por run. No se sobrescribe una revisión aceptada ni un proyecto que una aplicación pueda guardar.
- Informes históricos no se reescriben: la corrección va a `docs/06_estado/ERRATAS.md`.
- 3MF de Creality Print: trabajar sobre una copia. `sellar_carpeta.py` registra los `*.3mf` como `mutable` solo; otros archivos que una aplicación pueda reescribir se marcan con `--mutable "*.ext"`.
- Un PASS de validación no cambia lo anterior: distinguir declaración del responsable de evidencia medida.

## Excusas habituales

| Excusa | Realidad |
|---|---|
| «Es el mismo archivo, copio el hash del informe» | Así nació INC-BPY-001. Recalcular con la herramienta. |
| «Solo cambié un detalle del .blend aceptado» | Cambio = archivo nuevo con su propio registro. |
| «El informe necesita el hash, lo escribo yo» | Citar el valor que imprimió la herramienta; no se teclea. |
| «Sello al final de la sesión, todos juntos» | Sellar justo tras cerrar cada proceso productor. |
| «Es solo un ensayo, no hace falta» | Los ensayos que se citan después también se sellan. |

## Límite

El sellado detecta cambios posteriores al sellado, no los anteriores. No es garantía criptográfica.
