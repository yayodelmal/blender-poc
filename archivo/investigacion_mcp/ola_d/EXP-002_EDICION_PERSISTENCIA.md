# EXP-002 — Edición paramétrica y persistencia
**Estado:** protocolo preparado; **NOT RUN**. Dependencia lógica: EXP-001 PASS; ejecución con autorización propia.

## Objetivo e hipótesis

Con una escena desechable, demostrar que un parámetro editable cambia geometría sin reconstruir toda la escena, `.blend` guarda y reabre igual, dimensiones invariantes se mantienen, una revisión inválida puede descartarse y la última revisión aceptada recuperarse verificablemente.

## Dependencias y precondiciones

Blender/Codex/MCP fijados y EXP-001 PASS; estrategia de snapshot aceptada; almacenamiento desechable con espacio y política de versiones; criterios V02 y tolerancia aprobados para la pieza de prueba. No se usa el macetero. No asumir un valor numérico de tolerancia aquí. Solo un agente operativo Codex; operador humano no edita durante una transacción salvo en prueba concurrente controlada.

Antes de mutación: comprobar snapshot (guardar y reabrir/inspeccionar), revisión base y escena sin cambios concurrentes. Si cualquiera falla, detener.

## Pieza y procedimiento

Geometría simple: placa/cuerpo prismático parametrizado y un relieve rectangular unido físicamente como segundo parámetro (profundidad o paso); fijar valores de ensayo aprobados, sin convertirlos en requisitos CU-01. Guardar revisión A como `accepted` tras medir bounding box y contar geometrías/componentes conforme a modelo declarado.

1. Anotar ID de ensayo, versión, parámetro e invariante (largo/ancho/alto del cuerpo) y capturar escena A.
2. Guardar copia snapshot A; cerrarla/reabrirla o abrirla en proceso limpio; comparar objetos, entradas paramétricas y dimensiones.
3. Cambiar un parámetro de relieve por mecanismo editable (input GN/modificador) conservando identidad/cuerpo; medir escena evaluada. Guardar revisión B separada; reabrir y verificar cambio e invariantes.
4. Introducir un cambio inválido definido por control (p. ej. desplazar el relieve hasta separarlo intencionalmente). No promoverlo. Capturar medición que lo detecta y guardar como candidato fallido aislado.
5. Restaurar snapshot B aceptado a nueva copia de trabajo. Reabrirla y verificar revisión, parámetro, bounding box y condición de unión del relieve. Una copia presente sin comparación no es restauración probada.
6. Estado incierto: acordar timeout natural de llamada en operación no crítica; si no se puede generar sin acción insegura, documentar como NOT RUN. Nunca repetir create blindly; inspeccionar escena y archivos primero.
7. Conflicto concurrente: durante una pausa entre snapshot y commit, humano cambia un valor no destructivo; el agente debe detectar divergencia de revisión/escena y detener promoción/restauración. Resolver manualmente a cuál revisión corresponde continuar.

## Evidencias y controles negativos

Conservar A/B/candidato/restaurado `.blend`, capturas UI, registro de inputs/mediciones, timestamps y checksum de archivos si mecanismo aprobado; comparación antes/después, log de llamada y registro operación. Negativos: snapshot faltante, archivo corrupto/no abre, parámetro accidentalmente aplicado al objeto completo, dimensiones cambian, restore desde versión vieja, edición concurrente, timeout con mutación parcial. No guardar el candidato inválido sobre la última copia aceptada.

## Criterios

- **PASS:** A y B reabren; B solo cambia parámetro esperado; invariantes pasan tolerancia acordada; candidato inválido falla check; restore vuelve a B por medición y revisión; conflicto se detecta.
- **FAIL:** no preserva editable el parámetro, no reabre, se altera invariant sin detección, restore presenta archivo sin estado correcto, se sobrescribe cambio humano.
- **INCONCLUSIVE:** estado tras timeout no se puede reconciliar, API no permite medir parámetro o copia no tiene checksum/comparación acordada.
- **NOT RUN:** no autorizado o precondiciones faltantes.

## Riesgos, recuperación y puerta siguiente

Riesgo de reemplazar archivo o data-block enlazado; trabajar en carpeta desechable. Fallo de snapshot bloquea mutación; fallo de restore bloquea nuevos reintentos y escalar. Eliminar solo artefactos de prueba cuya ruta se haya revisado con operador; conservar evidencia mínima acordada. EXP-003 requiere PASS de edición/persistencia para conservar maestro.
