# Índice de experimentos (EXP-BPY)

Archivo nuevo de la consolidación. No modifica ningún informe. Los estados son los de cada run, con el estado vigente del experimento a la derecha. Detalle de EXP-BPY-004 en `../docs/06_estado/RECONCILIACION_EXP-BPY-004.md`.

**Nombres:** `EXP-BPY-00x` son los experimentos con `bpy` directo. `EXP-001/002/003` (en `../archivo/investigacion_mcp/ola_d/`) son protocolos MCP **NOT RUN**; no son los mismos.

**Formato de run_id:** en 001, 002 y el primer run de 004 la hora está en -0300; desde 003 es UTC (`Z`). No se renombra lo histórico.

| Experimento | run_id | Resultado del run | Estado vigente | Entorno |
|---|---|---|---|---|
| EXP-BPY-001 | `…T104904`, `…T105207-0300` | FAIL (Blender 5.2.3 LTS, Metal, código 139) | histórico | 5.2.3 LTS |
| | `…T105833-0300` | Generó y validó; aviso de miniatura fuera del árbol | histórico (su hash `6a23e9e2…` fue citado por error bajo 105936: INC-BPY-001) | 5.4.0 Alpha |
| | `…T105936-0300` | PASS; archivo 51.810 B, `a5f0aa70…` | **PASS** (línea base aprobada para EXP-BPY-002) | 5.4.0 Alpha |
| EXP-BPY-002 | `…T112024-0300` | PASS | **PASS** (guard de revisión simulado; sin tiempos de pared) | 5.4.0 Alpha |
| EXP-BPY-003 | `…T144300Z` | PASS | **PASS** (proxy 80×60×5 mm; STL `c6342d68…`) | 5.4.0 Alpha |
| EXP-BPY-004 | `…T121521-0300` | INCONCLUSIVE (preset personalizado) | histórico | Creality Print 7.3.0.6157 |
| | `…T154038Z` | Interrumpido; 3MF alterado (INC-BPY-002) | histórico | |
| | `…T155417Z` | PASS digital | **PASS** (cierre del experimento) | |
| EXP-BPY-005 | `…T153524Z` | NOT RUN (preparación) | histórico | |
| | `…T173135Z` | Impresión declarada por el responsable; 3 fotos selladas; sin medidas | **Impresión completada, inspección visual favorable, medición dimensional NOT RUN (omitida por decisión del usuario)**; aceptado por el usuario para el alcance exploratorio. No es PASS. Ver ADR-0003 | |

Los hashes completos están en el `MANIFIESTO_ARTEFACTOS.json` de cada experimento. EXP-BPY-001 no tiene manifiesto; sus hashes están en prosa.
