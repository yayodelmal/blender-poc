# Índice de incidentes

Archivo nuevo de la consolidación. No modifica ningún informe.

| Incidente | Qué ocurrió | Mejor respaldo | Estado | Abierto |
|---|---|---|---|---|
| INC-BPY-001 | El informe de EXP-BPY-001 asoció a su run `105936` el tamaño (51.802 B) y SHA-256 (`6a23e9e2…`) del archivo del run `105833` | INC-001 a INC-005: error de asociación, confianza alta (H5). No se puede excluir una edición posterior con timestamps preservados | Cerrado con dictamen B: nueva línea base candidata (`a5f0aa70…`, 51.810 B), aprobada por el responsable para EXP-BPY-002 | Prevención (INC-006) sin implementar |
| INC-BPY-002 | Una copia de trabajo 3MF de EXP-BPY-004 (`…154038Z_working_copy.3mf`) quedó guardada con contenido distinto al hash registrado (24.292 B `659b0890…` → 23.873 B `1a67df63…`) | Archivo actual y copia de custodia con hash verificado | Contenido actual preservado; sin restauración; EXP-BPY-004 se rehízo con copia nueva (run `155417Z`) | El manifiesto de EXP-BPY-005 aún cita el hash anterior; causa del guardado no establecida |
