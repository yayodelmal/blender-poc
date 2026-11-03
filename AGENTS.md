# Instrucciones del repositorio

## Material por defecto para modelos nuevos

- Los modelos de producto nuevos generados en este proyecto deben usar `herramientas/hyper_pla_marmol.py` por defecto, salvo que el usuario elija otro acabado o que un ensayo geométrico requiera expresamente una malla neutral.
- Después de construir la geometría de un objeto MESH, los nuevos generadores deben llamar `aplicar_material_por_defecto(obj)` desde `herramientas.hyper_pla_marmol`.
- El acabado es procedural y visual. No cambia la geometría; un STL no conserva este material.
- No editar experimentos históricos, revisiones aceptadas o artefactos sellados para aplicar retroactivamente el acabado. Crear una revisión o run nuevo.
