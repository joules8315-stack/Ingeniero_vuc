# CONTRATO — EL PASILLO CENTRAL: SE REPARTE POR CAPACIDAD REAL

**Ley dictada por Julio el 2026-09-09**, despues de la auditoria de causa raiz del mismo dia:

> "El problema esta en como nuestro sistema prepara, reparte, entrega y posteriormente juzga ese
> codigo. [...] Reparar **unicamente el punto 1**, comprobarlo en funcionamiento real y, si queda
> demostrado, pasar al punto 2."

> "Actualmente: 'No me dijeron que generador usar' = 'trabajo pesado'. Eso esta mal.
> Debe ser: '¿cuanto ocupa realmente este trabajo y que IA puede manejarlo?' Y entonces elegir."

Fuente medida: `memoria/AUDITORIA_CAUSA_RAIZ_2026-09-09.json` (`status: ROOT_CAUSE_CONFIRMED`)
y `memoria/MEDICION_NUEVE_PUERTAS_2026-09-09.json`.

---

## 0. La causa raiz, medida (por que existe esta ley)

| Lo que se creia | Lo que se midio |
|---|---|
| "El trabajo normal va a los gratis; solo lo pesado al de pago" | Los gratis llevan **0 de 72 trabajos reales escritos** |
| "Si no le cabe a nadie, se parte" | La regla existe, **el divisor no existe** |
| "Se manda el paquete tal como se preparo" | Se preparo de **14.858** y llego al cerebro **25.122** |
| "Lo que no cabe se salta a los que no aguantan" | En un paquete normal, **8 de 12** salidas superan la capacidad real de los gratis |

**Primera divergencia (la que manda):** `cuerpo/obrero.py` -> `pesado_ahora = not generador`.
Cuando nadie pide generador (el caso normal), el sistema **asume "pesado"** y fuerza el cerebro de
pago ANTES de mirar cuanto mide el encargo. Los gratis nunca compiten. No falta un cerebro gratis:
**falta el reparto por capacidad en la puerta de generar.**

---

## 1. LAS SEIS REGLAS Y SU ORDEN (Julio, 2026-09-09)

Se reparan **de una en una**, en este orden. No se abre la siguiente sin cerrar la anterior.

| # | Regla | Estado al escribir esta ley |
|---|-------|------------------------------|
| 1 | **Se elige por capacidad real, no por suposicion** | **EN REPARACION AHORA** |
| 2 | Una sola entrega: lo preparado no se vuelve a inflar sin control | Ley escrita, NO reparado |
| 3 | El divisor tiene que existir de verdad (dar solo lo que necesita) | Ley escrita, NO reparado |
| 4 | El reintento lleva el fallo concreto, no todo el historial | Ley escrita, NO reparado |
| 5 | Ninguna IA declara fallado sin comprobacion real | Ley escrita, NO reparado |
| 6 | Las pruebas miden lo que de verdad recibe la IA | Ley escrita, NO reparado |

---

## 2. REGLA 1 — TABLA DE LA VERDAD (lo que HOY se repara)

Entrada: un encargo para GENERAR. `generador` = el cerebro que pidio el que llama (puede ser None).
`tamano` = **letras del prompt REAL que se va a mandar** (no del paquete preparado).

| Caso | Se pidio generador | Tamano | ¿Algun gratis aguanta de verdad? | ANTES (mal) | DEBE SER |
|---|---|---|---|---|---|
| A | Nadie | 3.000 | Si | De pago primero | **Gratis primero** (el mas eficiente que aguanta) |
| B | Nadie | 12.000 | Si | De pago primero | **Gratis primero** |
| C | Nadie | 19.500 | Si (el que aguanta) | De pago primero | **El gratis que aguanta, primero** |
| D | Nadie | 250.000 | No, ninguno | De pago primero | **De pago primero** (lo pesado de verdad sigue al de pago) |
| E | Un gratis concreto | 19.500 | Si | Se le ignoraba | **Ese gratis primero**, y si no puede, se AVISA |
| F | El de pago | cualquier | — | De pago | **De pago**, sin cambio |
| G | Nadie | 250.000 y **no hay de pago** | No | Se volcaba a los gratis | **SE PARA** (F2, nunca a solas) y se dice que hay que PARTIRLO |

**Regla de oro:** el "de pago" entra cuando **no le cabe a ningun gratis**, jamas por no saber
cuanto mide. Y el juicio de capacidad sale de `cuerpo/cuotas.py` (`_capacidad` / `rankear`), que es
el unico numero que **baja con la evidencia** (CONTRATO_EQUIPO_QUE_AGUANTA).

**Lo que NO cambia:** a quien pidio un cerebro se le respeta; sin llave de pago no se rompe nada
(se sigue con los gratis); el que de verdad no le cabe a nadie se PARA, no se cae a los gratis
para llenar el hueco.

---

## 3. MATRIZ — QUE SE TOCA Y A QUIEN PUEDE DANAR

| Se toca | Por que | **A quien puede danar** | Como se protege |
|---|---|---|---|
| `cuerpo/obrero.py` -> `trabajar()` | Es donde nace la decision equivocada | Al de pago: podria dejar de recibir trabajo que **si** le cabe a un gratis — es lo que Julio ordena | Se conserva: lo que NO le cabe a nadie gratis sigue yendo al de pago |
| idem | | A los gratis: podrian recibir lo que no aguantan | No se les manda: lo filtra `cuotas.rankear` (capacidad MEDIDA) |
| idem | | A la regla F2 "nunca a solas" | Se mantiene el BLOQUEO cuando de verdad no aguanta nadie y no hay de pago |
| `cuerpo/obrero.py` -> `_preguntar_con_relevo()` | El tope declarado (`TOPE_PESADO=15000`) decide sin medir | Los gratis de contexto grande (Gemini) | La decision pasa a la capacidad medida, que es la que ya usa el relevo para saltar |
| `vigias/test_vigia_lo_pesado_a_deepseek.py` | Vigilaba la ley vieja ("pesado = not generador") | El sistema entero, si se borra en vez de actualizar | Se **actualiza para vigilar la ley nueva**, no se borra ni se afloja |

**No se toca** (por orden de Julio): subir limites de contexto, anadir otro divisor, parchear otra
puerta, aceptar la vigia verde sin comprobar, ni aceptar "no le cabe al cerebro" sin medir lo que
de verdad se mando.

---

## 4. VIGIA (que si se rompe, se sepa)

`vigias/test_vigia_se_reparte_por_capacidad.py` (nace ROJA antes de la reparacion):

1. Con un encargo que **si** le cabe a un gratis y sin generador pedido, el de pago **NO** va
   primero (era el fallo: iba primero siempre).
2. Con un encargo que **no** le cabe a ningun gratis, el de pago **SI** va primero.
3. Sin llave de pago y sin gratis que aguante, se **PARA** y se dice (F2 intacto).
4. Al que pidio un generador concreto se le sigue respetando y, si no puede, se avisa.
5. La ley vieja ("pesado = not generador") **ya no puede volver** por descuido.

## 5. ARNES (que el candado este enchufado de verdad)

| Que | Donde |
|---|---|
| La decision de a quien le toca | `cuerpo/obrero.py` (`trabajar`, `_preguntar_con_relevo`) |
| La capacidad medida | `cuerpo/cuotas.py` (`_capacidad`, `rankear`, `apuntar_no_cupo`) |
| La ley escrita | este archivo |
| La vigia | `vigias/test_vigia_se_reparte_por_capacidad.py` |
| La prueba real | el espia que mide **lo que de verdad se manda**, sin gastar cuota |

## 6. CROSS-FLOW — VECINOS QUE NO SE PUEDEN ROMPER

Estas vigias ya existen y se corren al terminar; si alguna se pone roja, la reparacion no vale:

- `test_vigia_repartidor_por_capacidad.py` — no se le da trabajo al que no aguanta.
- `test_vigia_equipo_que_aguanta.py` — a quien no le cupo, no se le vuelve a pedir lo mismo.
- `test_vigia_trabajar_respeta_generador_auditor.py` — 4 ojos y generador/auditor pedidos.
- `test_vigia_el_cerebro_es_el_que_pido.py` — no se cambia el cerebro por detras.
- `test_vigia_lo_pesado_a_deepseek.py` — **actualizada** a la ley nueva.
- `test_vigia_relevo_cuotas.py`, `test_vigia_nada_lento.py`, `test_vigia_revisor_roto_no_tira_la_vuelta.py`.

---

**Estado al legislarla (2026-09-09):** los 6 puntos quedan ESCRITOS como ley. Solo el punto 1 se
repara ahora. Los puntos 2 a 6 **no se tocan hasta que Julio vea el punto 1 funcionando.**
