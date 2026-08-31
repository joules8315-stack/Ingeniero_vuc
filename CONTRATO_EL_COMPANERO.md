# CONTRATO — SIEMPRE SE TRABAJA CON CONTINUE

**Julio, 2026-08-31:**

> "a partir de ahora trabajaras con continue, no con cline"
>
> "De ahora en adelante todo es con continue, es lo mejor, mas economico"
>
> "solo si se bloquea continue, solo si eso pasa, o falla, no responde como es, trabajas
> nuevamente con cline"
>
> "Crea los mecanismos de comunicacion continua, fluida, eficiente con continue"

## 1. EL COMPANERO ES CONTINUE. SIEMPRE.

Todo el trabajo en equipo va a **`continue`**: las tareas, el segundo ojo, la supervision.
No es una preferencia: es la regla. Y es la mas barata, que es lo que Julio busca.

## 2. CLINE ES EL REEMPLAZO, Y SOLO EN TRES CASOS

Se acude a `cline` **unicamente** cuando Continue:

| Caso | Que significa |
|---|---|
| **se bloquea** | no arranca, se queda colgado, no acepta el encargo |
| **falla** | contesta pero su trabajo esta mal y no lo corrige |
| **no responde como es** | contesta cualquier cosa, o no contesta |

Y aun asi: **se declara el motivo y queda apuntado**. No se acude a Cline por costumbre ni por
comodidad, y jamas en silencio.

Esto no es blandura. Es una leccion ya pagada, escrita en la memoria de fallos:

> *"no hacer un candado sin una forma honrada de satisfacerlo: empuja a saltarselo, y eso es peor
> que no tenerlo"*

Un candado que prohibiera el reemplazo sin salida acabaria apagado el dia que Continue fallara.

## 3. ESTA ESCRITO EN UN SOLO SITIO

Quien es el companero vive en `arnes/companero.py` y `memoria/COMPANERO.json`.
**Nunca escrito a mano dentro de otra pieza.**

**Por que, medido el mismo dia:** al cambiar de companero, el candado del buzon siguio exigiendo
leer el buzon de Cline, porque tenia su nombre escrito a mano dentro. Un nombre repetido por diez
sitios obliga a acordarse de diez sitios, y **lo que depende de acordarse no se cumple**.

## 4. EL BUZON: LA COMUNICACION ES CONTINUA, FLUIDA Y NO DEPENDE DE JULIO

- Continue tiene **su propio buzon**, creado al ponerlo como companero. No hereda el de nadie.
- **Al empezar a trabajar se lee el buzon del companero activo**, y si hay algo sin contestar,
  se contesta ANTES de seguir. Lo vigila un candado, no la buena memoria.
- **Al terminar una tarea se avisa por el canal.** Sin aviso, el otro no sabe que puede seguir.
- **Nada de esperar a que Julio haga de mensajero.** Si el companero tiene que abrir su ventana
  para leer, se le dice a Julio de una vez, no se calla fingiendo que se avanzo.

## 5. CAMBIAR DE COMPANERO DEJA RASTRO

Se apunta **quien entra, quien sale, cuando y por que**. El que entra **sale de la reserva**:
nadie figura a la vez como activo y como reemplazo.

## 6. NINGUNA TAREA VIVA SE QUEDA CON EL QUE SALE

Trabajo mandado a quien ya no esta es **trabajo muerto que ademas parece avance**. Lo que
estuviera vivo se traspasa **con todo el material** y con el motivo apuntado.

## 7. AL COMPANERO NUEVO SE LE DICEN LAS REGLAS

No se le tira una tarea encima sin mas. Se le dice como se trabaja aqui: vigia roja primero, dos
ojos siempre, nunca senalar por numero de renglon, no tocar los proyectos de Julio, y avisar por
el canal al terminar. **Lo que no se dice, no se cumple.**

## QUIEN LO HACE CUMPLIR

- `arnes/companero.py` — dice quien es el activo y quien el reemplazo, en un solo sitio.
- `arnes/candado_companero.py` — frena mandarle trabajo al reemplazo por costumbre.
- `arnes/candado_buzon.py` — obliga a leer y contestar el buzon del **activo** antes de seguir.
- `vigias/test_vigia_el_companero_es_continue.py` — mide que todo esto se cumple de verdad.
