# CONTRATO — EL SITIO SE BUSCA POR NOMBRE, NUNCA POR NUMERO

**Julio, 2026-08-31**, despues de repetirlo muchas veces sin que se reparara:

> "Lo que borra todo, que cuenta por lineas, por que no lo reemplazas, por que lo busque por
> funcion y nombre, para que asi identifique las lineas correctas. Si en definitiva no se puede
> buscar por numero, que se elimine esa instruccion y quede buscando por funcion y nombre, ya que
> dices que el numero esta constantemente cambiando."

## LO QUE MANDA

**1. Un sitio del codigo se senala por su NOMBRE y por su TEXTO. Nunca por un numero de renglon.**
   - Se dice: *que archivo*, *que funcion*, *que texto hay ahora* y *que texto debe quedar*.
   - No se dice: *"de la 97 a la 136"*.

**2. Un tramo de renglones esta PROHIBIDO como forma de reparar.**
   Un tramo de 40 renglones **es la funcion entera**. Aunque solo haya que cambiar una palabra, al
   aplicarlo se borra todo. Eso es lo que "borra todo".

**3. Los numeros de renglon solo valen para MIRAR, jamas para TOCAR.**
   Se pueden imprimir para que un humano se oriente. En cuanto sirven para decidir que se
   sustituye, estan prohibidos: se corren solos en cuanto alguien anade un renglon mas arriba.

**4. Prohibido escribir en el codigo un numero de renglon a mano para encontrar algo.**
   Nada de `desde, hasta = 87, 227`. Se pregunta por el nombre.

**5. El texto que se dice sustituir tiene que aparecer PALABRA POR PALABRA y ser UNICO.**
   Si se repite en el archivo, se alarga hasta que sea unico. Si no aparece literal, se rechaza y
   no se toca nada. Pararse en seco es correcto; destrozar el archivo no.

## POR QUE (lo que costo)

Medido el 2026-08-31, en un solo dia:

| Lo que paso | Cuanto |
|---|---|
| Vueltas del equipo rechazadas por esto | 3 ese dia, 8 el anterior |
| Renglones que le llegaban al equipo de un archivo de 116 | **40** |
| Piezas de ese archivo que llegaban enteras (de 6) | **2** |
| Veces que el revisor dijo "no veo ese texto" teniendolo delante | **3** |

Se le pedia al equipo que aprobara un cambio **sobre lo que no podia ver**, y se discutia sobre
renglones que nadie tenia delante.

## QUIEN LO HACE CUMPLIR

- **La ley**: este documento.
- **El candado**: `arnes/candado_por_nombre.py` — frena la escritura antes de que ocurra.
- **Las vigias**:
  - `vigias/test_vigia_la_pieza_se_busca_por_nombre.py` — que exista y funcione la busqueda por nombre.
  - `vigias/test_vigia_se_busca_por_nombre.py` — que el candado frene de verdad.

## LO QUE NO SE NEGOCIA

- No se deja nada "pendiente" por estar en rojo. **Se repara hasta verde, y recien entonces se
  pasa al siguiente.** Un paso en rojo no se guarda ni se avanza.
- Si el equipo rechaza, **se comprueba con los ojos si el rechazo es cierto** antes de darlo por
  bueno. Un revisor que dice "no veo ese texto" teniendolo delante se esta equivocando, y su
  rechazo no vale.
