# CONTRATO — LA BASCULA VA EN LA ULTIMA PUERTA, NO EN LA PRIMERA

**Fecha:** 2026-09-12
**Lo pidio Julio, con estas palabras:**

> "Debes asegurarte que solo ese codigo llegue a los cerebros, asi que pon un copista alli, o un
> blindaje de modo que no se le pueda poner nada mas, lo que deja el filtro es lo unico que debe
> llegar. Pon un programa, algo que no le anada a lo filtrado."

---

## EL FALLO QUE LO ORIGINA (medido, no opinado)

El 2026-09-12 Julio pregunto por que el paquete salia tan grande, y si habian vuelto a fallar los
filtros que ya se habian reparado. **Los filtros no fallaron.** Se midio el camino entero:

| | letras |
|---|---|
| Lo que entra (objetivo de Julio 7.575 + material 34.460) | 42.035 |
| **Lo que deja el filtro** (`asignador.armar_encargo`) | **11.359** — cumple su tope de 15.000 |
| + el objetivo **otra vez**, pegado por `obrero._prompt_obrero` | +7.575 |
| + las reglas fijas | +2.689 |
| **Lo que le llega al cerebro** | **21.623** |

Y groq (GPT-OSS 120B), que es **el que mejor escribe del equipo con un 65% de acierto**, aguanta
19.042. Se le saltaba por 2.581 letras. Esas 2.581 letras eran basura repetida.

## LA CAUSA DE FONDO, QUE ES LO QUE HAY QUE GUARDAR

**El filtro mide SU parte y se da por bueno. Nadie mide el sobre cerrado.**

`armar_encargo` dijo "11.359, cabe" y tenia razon en lo suyo. Despues **otra mano** le metio
10.264 letras mas, y en esa puerta no habia bascula. La bascula estaba **antes** de la ultima mano
que mete cosas.

Este es un patron, no un caso: es el mismo fallo que el contador de repeticiones que habia que
subir a mano y que el medidor de frenos en falso que nadie usaba. **Lo que se mide en un sitio y
se modifica en otro, no esta medido.**

## LA LEY

1. **LA BASCULA VA DONDE SE CIERRA EL SOBRE, NO DONDE SE EMPIEZA A LLENAR.** Lo que se pesa es lo
   ULTIMO que sale hacia el cerebro, no un paso intermedio.

2. **NADA VIAJA DOS VECES.** Si un texto ya va dentro del material, no se vuelve a pegar fuera.
   La repeticion no es redundancia util: es basura que echa fuera al mejor escritor.

3. **LO DEL FILTRO LLEGA ENTERO.** Lo que el filtro decidio que hacia falta, llega. Nadie lo
   recorta despues por su cuenta.

4. **LO UNICO QUE SE PUEDE ANADIR DESPUES DEL FILTRO SON LAS REGLAS FIJAS.** Son las instrucciones
   que le dicen al cerebro que hacer (no inventes, no asumas, contesta en este formato). Sin ellas
   el cerebro recibe material y ningun encargo. Son un texto FIJO y CONOCIDO: se puede medir de
   antemano. Cualquier otra cosa que alguien quiera anadir despues del filtro, **no pasa**.

5. **SI NO CABE, SE DICE EN VOZ ALTA.** Prohibido saltarse un cerebro en silencio por tamano. Si
   el sobre no le cabe al que lo iba a recibir, queda escrito: quien, cuanto pesaba, cuanto
   aguantaba. Un salto silencioso es como perdimos al mejor escritor sin enterarnos.

6. **ES UN PROGRAMA, NO UN CRITERIO.** Contar letras y comparar con un techo es cuenta, no juicio.
   Lo hace un programa gratis, siempre, sin preguntarle a ninguna IA. (CONTRATO_MENOS_IA_MAS_PROGRAMA)

## COMO SE PRUEBA QUE SE CUMPLE

Se EJECUTA el camino de verdad — el filtro y despues el que arma el sobre — con una marca rara
metida en el objetivo, y se CUENTA cuantas veces sale. No se busca una palabra en el codigo: se
corre el camino. (CONTRATO_ENCHUFADO_SE_PRUEBA_EJECUTANDO)

**Guardian:** `vigias/test_vigia_el_objetivo_no_va_dos_veces.py`

## LO QUE ESTA LEY NO TOCA

El tope del filtro (15.000) se queda como esta: ese numero es suyo y hace su trabajo. Aqui no se
toca cuanto material entra; se toca **quien pesa el sobre y en que puerta**.
