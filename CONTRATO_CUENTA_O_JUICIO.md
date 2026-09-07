# CONTRATO — ¿ESTO ES UNA CUENTA O UN JUICIO? (la pregunta que se hace SIEMPRE)

**Julio, 2026-09-07:**

> *"Sigue buscando qué se puede programar, qué tareas, que son muchas, esa debe ser una
> pregunta recurrente: ¿esta tarea es para programar, o para una IA?, y obrar en consecuencia
> en su construcción."*

Y el mismo día:

> *"En cuanto a lo de la copia, que lo haga por completo un programa."*

**Esta ley NO toca los tiempos de espera.** Julio decidió el 2026-09-07 dejarlos como estaban
y no legislar nada sobre minutos.

---

## LA LEY

**Antes de mandarle nada a un cerebro, y antes de construir cualquier pieza nueva en
CUALQUIER proyecto, se responde esta pregunta y se deja escrita:**

| | Qué es | Quién lo hace |
|---|---|---|
| **CUENTA** | Con reglas fijas da SIEMPRE lo mismo. No hay nada que decidir. | **Un programa. Gratis.** |
| **JUICIO** | Hay que decidir algo que no está escrito en ninguna ley ni material. | Un cerebro. |

**Si es una CUENTA y se le manda a un cerebro, se está pagando por una fotocopiadora.**

---

## POR QUÉ NACE ESTA LEY (el hecho medido, no una impresión)

De las **8 rondas pagadas del 2026-09-06**, en **5** el encargo ya llevaba dentro el
`TEXTO_VIEJO` y el `TEXTO_NUEVO` exactos. El cerebro de pago solo los copió. Lo único que
aportó fue la revisión — **y la revisión la hace un cerebro gratis**.

Cinco vueltas pagadas por una fotocopia.

---

## LA TABLA DE VERDAD — una vuelta completa del equipo, paso por paso

| # | Paso | Qué es | Quién debe hacerlo | Estado |
|---|---|---|---|---|
| 1 | Encontrar el flujo y las piezas del problema | CUENTA | programa (`cerebro/router.py`) | ✅ ya |
| 2 | Sacar la función entera por su NOMBRE | CUENTA | programa (`cerebro/piezas.py::funcion_completa`) | ✅ ya |
| 3 | Sacar a quién puede dañar (vecinos por el grafo) | CUENTA | programa | ✅ ya |
| 4 | Pesar el encargo y ver quién lo aguanta | CUENTA | programa (`cuerpo/cuotas.py`) | ✅ ya |
| 5 | Elegir quién escribe y quién revisa | CUENTA | programa (`cuotas.rankear`) | ✅ ya |
| 6 | **Decidir QUÉ está mal y qué hay que cambiar** | **JUICIO** | **cerebro** | ✅ correcto |
| 7 | **Escribir el texto nuevo cuando hay que decidir CÓMO** | **JUICIO** | **cerebro** | ✅ correcto |
| 8 | Escribir el texto nuevo **cuando ya está decidido** | CUENTA | programa | ❌ **lo hace un cerebro DE PAGO** |
| 9 | Copiar el texto viejo tal cual del material | CUENTA | programa | ❌ **lo hace un cerebro DE PAGO** |
| 10 | Comprobar que el texto viejo está literal y es único | CUENTA | programa | ✅ ya |
| 11 | Comprobar que no inventó archivos | CUENTA | programa (`_validar_en_paquete`) | ✅ ya |
| 12 | Aplicar el cambio al disco | CUENTA | programa (`cuerpo/aplicador.py`) | ✅ ya |
| 13 | Comprobar que el archivo no quedó roto | CUENTA | programa | ✅ ya |
| 14 | Correr las vigías | CUENTA | programa | ✅ ya |
| 15 | **Juzgar si el cambio es correcto y no rompe vecinos** | **JUICIO** | cerebro (gratis) | ✅ correcto |
| 16 | Entender una respuesta mal formada | CUENTA | programa | ❌ **se pierde la vuelta pagada** |
| 17 | Reintentar si el revisor contesta roto | CUENTA | programa | ✅ ya |

**17 pasos. Solo 3 son JUICIO (6, 7 y 15). De los 14 que son CUENTA, 11 ya los hace un
programa. Faltan tres: el 8, el 9 y el 16.**

---

## LA MATRIZ — qué falta y con qué se cura

| Falta | Pieza que lo cura | Qué se reusa (no se duplica) |
|---|---|---|
| Pasos 8 y 9 — la copia | `arnes/copista.py` | `cuerpo/aplicador.py::aplicar_cambio` |
| Paso 16 — respuesta mal formada | ampliar `cuerpo/obrero.py::_json_de` y pedir texto plano si falla | lo que ya rescata JSON |
| Saber POR QUÉ falla cada llamada | anotar quién · peso · tiempo · si contestó · si contestó MAL o NO contestó | `memoria/CUOTAS.json` |

---

## LAS REGLAS

**Regla 1 — La pregunta se escribe, no se piensa.** Toda pieza nueva, en cualquier proyecto,
lleva escrito si es CUENTA o JUICIO. Si es CUENTA y se le manda a un cerebro, se rechaza.

**Regla 2 — El copista no adivina.** Si el texto viejo no está literal, o está más de una vez,
**FRENA**. Nunca aplica a ciegas. Es la cura del fallo del 2026-08-21.

**Regla 3 — El equipo no se salta, cambia de oficio.** La Ley 6 de Julio sigue entera: el
equipo sigue metido en cada trabajo. Deja de teclear y pasa a **auditar**, que es JUICIO.
Ningún cerebro escribe una letra que no estuviera ya decidida.

**Regla 4 — Nunca se frena por no encontrar un nombre (Julio, 2026-09-07).**

> *"Hablas mucho de nombrar, y muchos de los fallos pasados fue por ello: no encontraba el
> nombre. Debes agregar 'por nombre o por función', para que si no la encuentra de una forma
> la encuentre por otra y no frene el trabajo por un fallo falso."*

**Toda búsqueda tiene DOS caminos, nunca uno:** primero por su **nombre**; si no aparece, por
**lo que hace**. Un nombre que no se encuentra **no es una avería**: casi siempre es otra
forma de escribir lo mismo.

**Frenar por eso es un fallo falso, y un fallo falso es peor que no tener aviso**, porque
enseña a ignorar los avisos de verdad. Solo se frena cuando **los dos caminos** fallan, y
entonces se dice **cuál se probó y con qué**.

Es la Regla 1 de `CONTRATO_CREAR_PIEZA_NUEVA` (*"primero se busca POR FUNCIÓN, no por
nombre"*) hecha obligatoria en TODA búsqueda: piezas, funciones, cerebros, modelos y archivos.

**Regla 5 — Cada pieza nueva deja su fallo anotado.** En `memoria/FALLOS.json`, con su
**disparador**, para que `arnes/candado_memoria.py` avise ANTES de repetirlo. Un fallo sin
disparador no avisa a nadie, y volver a pisarlo es cuestión de tiempo. (Es la instrucción 2 de
Julio del 2026-09-07: *"que nada se pierda, que los fallos siempre estén presentes para no
volver por esa ruta"*.)

---

## A QUIÉN PUEDE DAÑAR

- Al mando `equipo`: pasa de "el equipo escribe" a "el equipo audita" **solo** cuando el
  cambio ya viene decidido. Sin los dos bloques, todo sigue exactamente igual.
- A la **Ley 6** (siempre en equipo, sin salto): **no se toca**.
- A `CONTRATO_LA_IA_CARA_NUNCA_ESCRIBE`: **no se toca**. Quien hace lo mecánico es un
  programa, no la IA cara.
- A los **tiempos de espera**: **no se tocan**. Se quedan como estaban (Julio, 2026-09-07).

## CÓMO SE COMPRUEBA

`vigias/test_vigia_cuenta_o_juicio.py`:
1. encargo con los dos bloques → **no se llama a ningún cerebro para escribir**;
2. encargo sin los dos bloques → flujo de siempre, escribe el equipo;
3. texto viejo que no está, o que está dos veces → **frena y dice cuál**;
4. el paso 15 (auditar) **sigue llamando a un cerebro**: un juicio no se programa.

**Vigía verde no es prueba.** La prueba es rehacer una ronda de ayer con cero llamadas al
cerebro de pago, que el archivo quede idéntico, y que Julio lo vea.
