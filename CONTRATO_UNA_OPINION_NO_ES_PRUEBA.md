# CONTRATO — UNA OPINIÓN NO ES PRUEBA, Y UNA PIEZA SIN GUARDIÁN NO ESTÁ HECHA

**Julio, 2026-09-10/11.** Cinco instrucciones que nacen del mismo sitio.

---

## 1 · NINGUNA IA DECLARA FALLADO UN TRABAJO SIN COMPROBARLO

> *"Ninguna IA puede declarar fallado un trabajo sin comprobación real: opinión de una IA no es
> prueba."*

**Ya pasó y costó caro:** dos cerebros avisaron de un peligro **falso** y casi se le repite a
Julio como cierto. Se fue a mirar el código y **los dos se equivocaban**.

**La ley:** para decir que algo falló hay que **correrlo y enseñar la salida**. Un cerebro
opinando sobre código que no ejecutó **no prueba nada**, por muy seguro que suene.

| Dice | Vale como prueba |
|---|---|
| *"esto tiene errores graves"* sin correrlo | **No** |
| La salida de haberlo corrido | **Sí** |

---

## 2 · LAS PRUEBAS MIDEN LO QUE DE VERDAD LLEGA, NO QUE LA PIEZA EXISTA

> *"Las pruebas tienen que medir lo que de verdad recibe la IA, no que la función exista."*

Es hermana de la ley de **probar ejecutando**. Que una pieza exista no dice nada de lo que
recibe el que trabaja. **Se mide el encargo real, con sus letras contadas.**

---

## 3 · SI NO LE CABE A NINGÚN GRATIS, SE PARTE EL TRABAJO

> *"El divisor de verdad tiene que existir, no solo la regla escrita."*

**Una regla escrita sin la pieza que la hace no es una regla: es un deseo.** Si el encargo no le
cabe a nadie gratis, o **se parte de verdad**, o se dice y no se gasta. Lo que no vale es
mandarlo igual y que acabe pagándolo el caro.

---

## 4 · LOS REINTENTOS NO ENGORDAN EL ENCARGO

> *"El segundo intento lleva solo el fallo concreto."*

Cada reintento arrastraba lo anterior y el encargo crecía hasta no caberle a nadie. **El segundo
intento lleva el fallo y nada más.** Se repara lo que falló, no se cuenta la historia otra vez.

---

## 5 · EL PASILLO PRINCIPAL SE REPARA DE A UN PUNTO

> *"Primero el reparto por capacidad, comprobarlo de verdad, y después el siguiente."*

Por donde pasa todo el trabajo **no se tocan dos cosas a la vez**. Se repara una, **se comprueba
de verdad**, y solo entonces la siguiente. Si se rompe algo, así se sabe cuál fue.

---

## LO QUE ACABA DE PASAR, Y POR QUÉ ESTAS LEYES NO BASTAN (2026-09-11)

El jefe que coordina la aplicación **perdió la parte que lleva el presupuesto y pide el permiso
de Julio para lo caro**. De 81 renglones a 56.

**Y las 526 pruebas siguieron verdes.** Ninguna se enteró.

> **Una pieza que puede desaparecer sin que nada se ponga rojo es una pieza sin guardián.
> Y una pieza sin guardián NO ESTÁ HECHA, por mucho que exista.**

### Regla 6 — Lo que se enchufa nace con su guardián, y el guardián prueba que SIGUE ahí
No basta con probar que funciona hoy. **Tiene que ponerse rojo si mañana desaparece.** La prueba
es la de siempre: **se borra a propósito y la vigía tiene que gritar.**

---

## CÓMO SE COMPRUEBA QUE SE CUMPLE

`vigias/test_vigia_una_opinion_no_es_prueba.py`:
1. que ningún camino dé por fallado un trabajo **sin la salida de haberlo corrido**;
2. que al medir el encargo **se cuenten las letras que de verdad salen**;
3. y que **exista** el que parte el trabajo, no solo la regla escrita.

**Y la prueba de verdad:** se borra a mano una parte de una pieza enchufada y **alguna vigía
tiene que ponerse roja**. Si ninguna lo hace, esa pieza está sin guardián.
