# MATRIZ / TABLA DE LA VERDAD — LEGISLACIÓN 2026-08-24

> Fecha: 2026-08-24 · Proyecto: Ingeniero VUC · Estado: LEY VIGENTE
>
> Tabla de la verdad y matriz de la instrucción de Julio del 2026-08-24. Cada fila es un bloque;
> cada columna, la garantía de que ese bloque está legislado, tiene candado y tiene vigía. Se
> actualiza cuando algo cambia. No se escribe a mano: se comprueba contra el disco.

| Bloque | La ley (qué exige) | Candado (qué frena) | Vigía (qué comprueba) | Estado |
|---|---|---|---|---|
| B1 | Siempre en equipo, sin salto, en TODAS las IA (Claude, Cline, ChatGPT). Saltarlo se pide permiso y la respuesta es SIEMPRE "denegado". | `arnes/candado_equipo.py` + `arnes/edit_gate_universal.py` | `vigias/test_vigia_equipo_total.py` | LEGISLADO |
| B2 | Antes de pedirle a Julio que pruebe: prueba real interna (con equipo, Playwright) en verde que demuestre el objetivo. | `arnes/candado_prueba_real.py` | `vigias/test_vigia_prueba_real.py` | LEGISLADO |
| B2.1 | Si el resultado se logró → avisarle a Julio para pruebas reales. | comando `pedir-prueba` (solo pasa si hay evidencia) | `vigias/test_vigia_prueba_real.py` | LEGISLADO |
| B2.2 | Si NO se logró → aprender del error y reiniciar el ciclo para reparar, sin excusas. | candado de cierre (`candado_cierre.py`) | `vigias/test_vigia_legislacion_ciclo.py` | LEGISLADO |
| B3 | Toda instrucción de Julio se legisla: analizar → legislar → tabla/matriz → bloques → indexar → vigías → arnés → cross-flow. | este contrato + `cerebro/protocolo.py` | `vigias/test_vigia_legislacion_ciclo.py` | LEGISLADO |
| B4 | Solo se pregunta después de haber buscado (todo indexado); nunca antes. | `arnes/candado_preguntar.py` (PASO 4) | `vigias/test_vigia_dudas.py` | LEGISLADO |

## Comprobación real (no autovalidación)

Cada bloque de arriba solo cuenta como LEGISLADO si:
1. Existe el archivo del candado que dice la columna **y** está conectado (no es un deseo).
2. Existe la vigía que dice la columna **y** está verde.
3. La ley está escrita en `PROTOCOLO_UNICO.md` y en `CLAUDE.md` (la leen todas las IA).
4. La vigía nace ROJA al sabotear la cura (prueba de que muerde, no de que aparenta).

Se comprueba con: `python -m pytest -q vigias/test_vigia_equipo_total.py vigias/test_vigia_prueba_real.py vigias/test_vigia_legislacion_ciclo.py`
