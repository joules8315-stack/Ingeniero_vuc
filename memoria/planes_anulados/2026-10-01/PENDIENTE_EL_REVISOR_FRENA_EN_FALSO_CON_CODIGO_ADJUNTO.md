# CORREGIDO — NO ERA UN FRENO EN FALSO. ERA UN ERROR MIO, DOS VECES

**Escrito el 2026-09-12 de noche, y CORREGIDO esa misma noche antes de darlo por bueno.**

## LO QUE ESCRIBI PRIMERO, Y ESTABA MAL

Escribi que el revisor frenaba en falso cuando el encargo lleva codigo adjunto, y que eso chocaba
con la regla de adjuntar siempre el codigo. **Era una conclusion apresurada.** Se apunto un freno
en falso en el medidor y ese apunte hay que quitarlo o corregirlo.

## LO QUE PASABA DE VERDAD

Para pedirle al equipo una pieza NUEVA existe una marca: `--crear`. **Yo no la puse. Dos veces.**

Sin esa marca, al obrero le llega el encargo de REPARAR, que exige decir "el texto de antes" y "el
texto de despues". Pero un archivo que todavia no existe **no tiene texto de antes**. Asi que el
obrero rellenaba ese hueco con lo mismo que ponia en el de despues, y entonces saltaban dos
guardianes, los dos con razon:

- el que aplica: "el archivo no existe en esa ruta" — porque si viene un texto de antes, entiende
  que se queria cambiar algo que ya estaba, y **no crea nada por su cuenta**. Correcto.
- el revisor: "el texto nuevo es igual al viejo, eso no repara nada" — correcto tambien, porque
  eran identicos.

Y las quejas de "esta palabra no aparece" eran consecuencia de lo mismo: si lo entregado esta
vacio, **ninguna** palabra del encargo aparece. No era que sobraran palabras del codigo adjunto.

## Y LO PEOR: ESTABA ESCRITO Y AVISADO

En `ingeniero.py`, junto a esa marca, hay un comentario del 2026-09-06 que describe exactamente lo
que me paso:

> "pedir crear un archivo nuevo acababa SIEMPRE en el encargo de reparar, que exige un texto_viejo
> que no existe, y el obrero se rendia."

Ya estaba cazado, ya estaba reparado, y ya estaba explicado. **Yo no lo lei y culpe al arnes.**

## LA LECCION, QUE ES LA QUE VALE

Cuando un guardian frena tres veces seguidas, la primera sospecha tiene que ser **que el que pide
lo esta pidiendo mal**, no que el guardian este roto. Acusar al guardian es la salida comoda y
lleva a romper la proteccion que funciona. Es la misma ley que Julio exige desde el principio:
**causa raiz antes que reparacion**, y la causa raiz aqui era el que mandaba el encargo.

## LO QUE SI QUEDA EN PIE DE LA NOTA ANTERIOR

Una sola cosa, y esa si esta medida:

    GPT-OSS 120B no le cabe (20762 letras, aguanta 19042) -> se le salta
    GPT-OSS 20B  no le cabe (20762 letras, aguanta 20169) -> se le salta

El encargo para reparar el objetivo duplicado no le cupo a ninguno de los dos **por el propio
objetivo duplicado**. Eso sigue siendo cierto y sigue sin reparar: la averia estorba a quien viene
a arreglarla. Se esquiva recortando el encargo, pero la reparacion sigue haciendo falta.
