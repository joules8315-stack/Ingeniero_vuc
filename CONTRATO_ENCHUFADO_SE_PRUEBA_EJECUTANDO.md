# CONTRATO — ENCHUFADO SE PRUEBA EJECUTANDO, NUNCA LEYENDO

**Julio, 2026-09-09**, después de parar el trabajo por el mismo fallo una vez más:

> *"¿Cómo se repara de raíz, para que no vuelvan a salir los mismos putos fallos?"*

---

## EL FALLO QUE ESTA LEY MATA

Una vigía comprobaba que al cerebro solo le llegara lo suyo así:

```
assert "asignador" in ingeniero.py
```

**Buscaba la palabra en todo el archivo.** Como el mando `equipo` sí lo llamaba, la palabra
aparecía y la vigía se ponía **verde**. Pero `resolver` — el otro camino que manda trabajo a un
cerebro — abría el paquete entero y lo entregaba tal cual.

**Resultado medido:** se mandaron 7.575 letras y llegaron 35.845. No le cupo a ninguno de los
cuatro cerebros gratis, contestó el de pago y **se juzgó a sí mismo**.

**Verde de mentira. Y así veintiuna veces.**

---

## POR QUÉ PASA — la causa, no el síntoma

**Porque comprobar por palabra es lo fácil.** *"¿Aparece el nombre?"* son dos líneas.
*"¿El camino real la usa?"* cuesta pensar. **Mientras lo fácil esté permitido, se hará.**

Y detrás hay algo más gordo: **qué cuenta como "hecho"**.

| | |
|---|---|
| Hoy "hecho" significa | el archivo existe y hay una vigía verde |
| **Y eso se puede fingir sin querer** | ha pasado 21 veces |

---

## LA LEY

**Una vigía que comprueba que una pieza ESTÁ ENCHUFADA no lee texto: EJECUTA el camino real con
un espía puesto en la pieza, y comprueba que la llamaron.**

**Eso no se puede fingir.** No hay palabra que colar ni comentario que engañe: **o se ejecutó o
no se ejecutó.**

### Regla 1 — Ejecutar primero, leer solo si no queda otra
Si el camino se puede correr en una prueba, **se corre**. Leer el código es el último recurso,
no el primero.

### Regla 2 — Cuando de verdad no se pueda ejecutar, se mira LA FUNCIÓN, nunca el archivo
Es la Regla 5 de `CONTRATO_SE_BUSCA_POR_FUNCION.md`: *el nombre vale como pista, nunca como
criterio*. Un archivo con varios caminos **no prueba nada**: basta que uno la llame para que la
palabra aparezca.

### Regla 3 — Un archivo con varios caminos NO es prueba de nada
`assert "algo" in <archivo con varias funciones>` queda **prohibido**. Se nombra la función.

### Regla 4 — El espía es UNO SOLO para toda la casa
Si cada vigía se escribe su propio espía, en dos días vuelven a divergir: **es el mismo fallo
con otra cara**. Vive en `vigias/_espia.py` y se reusa.

### Regla 5 — Si al repararla nace ROJA, es que mentía
No se ablanda la vigía para que pase. **Se repara lo que estaba tapando.**

---

## ESTO NO ES TEORÍA: YA EXISTE HECHO EN ESTA CASA

`vigias/test_vigia_no_se_paga_dos_veces_por_lo_mismo.py`, escrita el mismo día, cuenta
**llamadas reales** con un contador espía:

```
e.vectorizar(["pan", "pasteles"])      → cuenta 2
e.vectorizar(["pan", "pasteles"])      → tiene que seguir contando 2
```

**Esa vigía no se puede engañar.** Las otras veinte sí. **Ese es el molde.**

---

## A QUIÉN PUEDE DAÑAR

- A las 21 vigías que comprueban por palabra: **varias nacerán rojas al repararlas**, y eso es
  correcto — demuestra que mentían.
- A quien escriba vigías a partir de ahora: **cuesta más pensarlas**. Ese es el precio, y es
  barato comparado con parar el trabajo por el mismo fallo una y otra vez.

## CÓMO SE COMPRUEBA QUE SE CUMPLE

`vigias/test_vigia_una_vigia_no_miente_por_el_nombre.py`: caza cualquier vigía que compruebe
por palabra sobre un archivo con varios caminos, **antes de que muerda**.

Es hermana de la que ya cazó los sitios que contaban una vigía recién nacida como avería.

**Y la prueba de verdad:** se le quita el recorte a `resolver` a propósito y la vigía **tiene
que ponerse roja**. Si sigue verde, la vigía no sirve.
