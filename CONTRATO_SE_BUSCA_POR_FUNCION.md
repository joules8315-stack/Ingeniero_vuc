# CONTRATO — SE BUSCA POR FUNCION. NI POR PALABRA, NI POR NUMERO.

**Julio, 2026-09-08**, despues de repetirlo muchas veces:

> *"Quita eso de que busque por palabra, por numero y cosas que no sirven. Que busque por
> funcion."*

Es la continuacion natural de `CONTRATO_SE_BUSCA_POR_NOMBRE.md` (Julio, 2026-08-31), que ya
prohibio el numero de renglon. Ahora se prohibe tambien la palabra suelta.

## EL PORQUE, EN PALABRAS DE JULIO (2026-09-08)

> *"Si busca por numero, si corre una casilla, no sabe donde poner."*
>
> *"Si busca por palabra, o palabras, o palabra rara, es como adivinar, eso no sirve. Le sirve
> es saber el contexto, o que funcion cumple, o para que sirve, o que hace. De resto es pura
> estupidez."*

**Las dos razones, y no hay mas que discutir:**

| Como busca | Por que no sirve |
|---|---|
| Por **numero** | Si corre una casilla, ya no sabe donde poner. El numero se mueve solo. |
| Por **palabra** (o la mas rara) | **Es adivinar.** Una palabra puede estar por accidente y no dice nada de lo que la pieza hace. |
| Por **funcion / contexto** | Es SABER: que funcion cumple, para que sirve, que hace. Eso no se mueve y no se adivina. |

**Ojo con esto, que es lo que se hizo mal:** afinar la busqueda por palabras (quitar comunes,
exigir la mas rara) **NO arregla nada**, porque sigue siendo adivinar. Es la misma estupidez
con mejores modales. Se cambia la PREGUNTA, no el filtro.

---

## LA LEY

**Una pieza se elige por lo que HACE (sus funciones), no por las palabras que aparecen en su
nombre ni en su descripcion.**

El nombre y la descripcion son adorno: cambian, estan mal escritos, llevan palabras de relleno.
La funcion es un hecho: o existe o no existe.

### Regla 1 — Prohibido elegir por interseccion de palabras
Nada de "si alguna palabra de la necesidad aparece en el texto de la pieza". Una palabra puede
aparecer por accidente. Ni siquiera vale afinarlo quitando palabras comunes o exigiendo la mas
rara: **sigue siendo el mismo truco, solo que mas fino.**

### Regla 2 — Se pregunta por la funcion
La busqueda mira la **boca** de cada pieza: sus funciones publicas. Eso YA lo guarda el mapa
para todas las piezas (`mapa/inventario.py::apis` lo extrae y queda en `MAPA_INGENIERO.json`
dentro del campo `api` de cada pieza). **No hay que construir nada nuevo: hay que mirarlo.**

### Regla 3 — Varias candidatas es mejor que una equivocada
Si por funcion salen cuatro piezas, se devuelven las cuatro. **Ninguna se pierde y ninguna se
inventa.** Elegir entre ellas, si hace falta, es un JUICIO (o se le pregunta a Julio). Devolver
una sola con cara de certeza cuando es la equivocada es peor que devolver cuatro.

### Regla 4 — Si no hay funcion que lo cubra, se dice NO_ENCONTRADO
No se traen parecidos. Ley de siempre: si no se puede saber, se dice que no se sabe.

---

## EL FALLO REAL QUE LA HACE NACER (medido el 2026-09-08)

Necesidad: **"medir las acciones de cada IA"**.

El buscador de habilidades (`cuerpo/skills.py::buscar`, renglones 123-127) se queda con las
palabras de mas de 3 letras — `medir`, `acciones`, `cada` — y elige cualquier habilidad que
tenga alguna de ellas en su nombre o en su descripcion. Resultado medido:

| Habilidad | Que paso |
|---|---|
| `medir_navegador` | **GANA**, y no tiene nada que ver: su descripcion dice "cuanto tarda **cada** una". Gano por una palabra de relleno. |
| `quien_sirve_de_verdad` | **SE PIERDE**, siendo la correcta: su unica palabra de enlace es "IA", de 2 letras, descartada por el filtro `len(w) > 3`. |

**Y buscando por funcion no se pierde:** el mapa ya tiene apuntado que
`quien_sirve_de_verdad` expone una funcion llamada **`medir`**.

Fallo identico ya guardado el **2026-08-20** con otra palabra corta: *"generar un codigo QR"*,
donde "qr" tiene 2 letras y se descartaba igual. **Es la segunda vez.**

---

## QUE SE REPARA Y DONDE

`cuerpo/skills.py::buscar` deja de comparar palabras y pasa a preguntar por funcion, usando el
`api` que el mapa ya guarda de cada pieza. **No se crea ninguna pieza nueva.**

## COMO SE PRUEBA (la vigia tiene que nacer ROJA)

1. Con la necesidad "medir las acciones de cada IA", `quien_sirve_de_verdad` **tiene que salir**.
2. `medir_navegador` **no puede salir** por la palabra "cada".
3. Con una necesidad que ninguna funcion cubre, **tiene que decir NO_ENCONTRADO**, no parecidos.
