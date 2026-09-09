# CONTRATO — AL CEREBRO SOLO LE LLEGA LO SUYO

**Julio, 2026-09-09**, después de repetirlo varias veces y con razón:

> *"Quedamos que se dividiría, para que solo la parte que le toque al cerebro llegue al cerebro,
> lo que es de programar, a programar. Y otra vez la misma cosa: que llega completo todo el
> llamado. Crea vigía fuerte, legisla bien, pon candados que sirvan, y asegúrate de que no se
> vuelva a olvidar."*

Y después, la pregunta que llevó a la raíz:

> *"Averigua por qué el sistema le pega encima esos datos de más. Quién los pega, y por qué."*

---

## LA RAÍZ, EN UNA FRASE

> **Se le pedía buscar material para un encargo que ya traía el material dentro.**

Es como pedir pan teniéndolo en la mano: te traen otro, y encima pesa.

**Nadie hizo nada mal.** El buscador que arma el paquete **hacía bien su trabajo**: se le da un
problema en palabras normales y trae lo relacionado. En la medición trajo 6 leyes, 12 fichas, 7
piezas de código, 14 trozos, 3 vigías y 7 vecinos. **Para eso existe.**

El fallo fue de quien le pidió ayuda cuando no hacía falta.

---

## LA LEY QUE MANDA SOBRE TODAS, Y ROMPE EL BUCLE (Julio, 2026-09-09)

> *"Ese es el punto: está mal el flujo. Por qué se le pide que juzgue algo que ya está. Eso es
> estúpido. Debe pasar a EJECUTAR, no que lo juzguen. Lo que debe hacer, a lo sumo, es con un
> PROGRAMA verificar que el pedido esté bien hecho y lleve lo que se le pidió. Para romper el
> bucle."*

**A UN CEREBRO NO SE LE PIDE QUE JUZGUE TRABAJO YA HECHO Y EN VERDE.** La vigía YA dijo si
funciona. Eso es el comparador, y su palabra vale más que una opinión.

**EL BUCLE QUE SE ROMPE, y ocurrió de verdad tres veces seguidas el 2026-09-09:**
se manda el trabajo a juzgar -> el cerebro, ahogado en relleno, dice "tiene errores de sintaxis"
-> se comprueba y es FALSO (compila, y sus vigías pasan) -> se vuelve a mandar -> otra vez lo
mismo. Cada vuelta cuesta dinero y no aporta nada.

**LO QUE SE HACE EN SU LUGAR: un PROGRAMA comprueba que el pedido esté bien hecho.** Gratis, al
instante y sin opinar. Mira tres cosas:
1. que el encargo **diga qué se quería conseguir**;
2. que **lleve dentro lo que se pidió** (el código, el trozo, lo que sea);
3. que **quepa** en un cerebro gratis.

Si las tres están, **a ejecutar**. Sin preguntarle a nadie.

### Y el equipo NO se salta: cambia de momento
El equipo sigue siendo obligatorio **para ESCRIBIR código**, que es donde hay juicio de verdad
(qué hay que cambiar y cómo). Lo que se acaba es pedirle que opine sobre algo **ya aplicado y
verde**, porque ahí ya no queda nada que decidir.

---

## LA OTRA MITAD: qué material se le manda

**Antes de mandarle nada a un cerebro se responde: ¿esto ya trae dentro lo que necesita?**

| Lo que se pide | ¿Hace falta buscar material? |
|---|---|
| **"Repara esto"** — no se sabe dónde está el fallo | **SÍ.** El buscador es imprescindible |
| **"Juzga esto"** — el código ya va dentro del encargo | **NO.** Buscar solo añade peso |

**Son dos cosas distintas y se estaban tratando igual.**

### Regla 1 — El tope cuenta lo que LLEGA, no lo que se manda
Un tope que no cuenta lo que se añade después **no es un tope**. Medido: con el tope en 19.000,
lo que llegaba de verdad eran 19.209 y se pasaba por **167 letras** del cerebro más pequeño. Se
le saltaba igual.

### Regla 2 — Nada viaja dos veces
Medido el mismo día: el encargo iba en el encargo **y otra vez** dentro del diagnóstico.
**Recortar por un lado y duplicar por otro no sirve de nada.**

### Regla 3 — Al recortar, primero se guarda lo necesario
Recortar por lo bruto es trampa: si se cae justo el trozo que hay que reparar, **el encargo cabe
y no sirve para nada**. Se conserva lo necesario y se recorta el relleno.

### Regla 4 — Si no le cabe a nadie, se dice y NO se gasta
Callarse es lo que hacía el sistema viejo: se les saltaba a todos **en silencio**, contestaba el
de pago, y como no quedaba nadie más **se juzgaba a sí mismo**.

---

## LO MEDIDO (2026-09-09), ANTES Y DESPUÉS

| | Antes | Después |
|---|---|---|
| Lo que se mandaba | 7.447 letras | 7.447 letras |
| Lo que le llegaba | **27.785 letras** | **le cabe a un gratis** |
| Del total, el encargo real era | **el 27%** | casi todo |
| Quién contestaba | el de pago, **solo** | **un cerebro gratis** |
| ¿Se juzgaba a sí mismo? | **sí** | **no** |
| Coste | dinero | **cero** |

Y juzgaba mal: dijo *"errores de sintaxis graves"* sobre un archivo **que compila y cuyas vigías
pasan**. Un cerebro ahogado en relleno no juzga: adivina.

---

## POR QUÉ SE OLVIDABA UNA Y OTRA VEZ

**La cura ya existía y nadie la llamaba.** `arnes/asignador.py`, construido el día anterior,
sabe recortar dejando lo necesario y sabe elegir un cerebro al que le quepa. **Cero
invocaciones.**

Es la misma enfermedad de las 22 piezas dormidas de la aplicación de marketing: **legislado,
construido, y sin enchufar.**

> **Por eso esta ley no se conforma con estar escrita.**

---

## CÓMO SE HACE CUMPLIR

`vigias/test_vigia_al_cerebro_solo_llega_lo_suyo.py` **no comprueba que la ley esté escrita.
Comprueba que se cumple:**

1. que quien manda trabajo a un cerebro **llama al asignador**;
2. que lo que sale **nunca pasa del tope** que aguantan los gratis;
3. que al recortar **no se tira lo que hace falta**;
4. y que si no le cabe a nadie, **se dice y no se gasta**.

**Y la comprobación de verdad no es la vigía: es medir lo que LLEGA al cerebro**, no lo que se
manda. Así se cazaron los tres fallos, uno detrás de otro.
