# CONTRATO — SE APUNTA PARA REPARAR, NO PARA MIRAR

**Fecha:** 2026-09-12
**Lo dijo Julio, con enfado y con razon:**

> "Se apunta para repararlo enseguida, o terminando la tarea si el fallo no la afecta. No para
> verlo despues por alguien mas o el azar. Para que me sirve tener algo apuntado, si no es para
> repararlo de una vez. Repara, repara. Apunta y repara."

---

## EL FALLO QUE LO ORIGINA

La noche del 2026-09-12 se cazaron dos averias de la casa y se dejaron **apuntadas y sin reparar**,
con la excusa de que pedian paquete y veredicto. Julio lo corto en seco: un apunte que nadie
repara **no es trabajo, es una lista de deudas**. Y peor: da la falsa sensacion de que algo se
hizo. El fallo sigue vivo exactamente igual que antes de apuntarlo.

## LA LEY (es un orden, no una sugerencia)

**Estas en una tarea y sale un fallo:**

1. **Se apunta.** Siempre. Con su causa raiz medida y sus soluciones posibles.
2. **Se pregunta una sola cosa: este fallo me deja terminar la tarea?**
   - **SI me deja** entonces se termina la tarea, y **acto seguido se repara el fallo apuntado**.
     No al dia siguiente, no cuando alguien lo vea, no si sobra tiempo. **Acto seguido.**
   - **NO me deja** entonces **se repara el fallo PRIMERO**, y despues se sigue con la tarea.
3. **Un apunte no cierra nada.** La tarea no esta terminada mientras su fallo apuntado siga vivo.

## LO QUE ESTA PROHIBIDO

- Dejar un fallo apuntado "para que lo vea alguien" o "para manana", sin haberlo intentado.
- Usar el apunte como sustituto de la reparacion en el informe a Julio.
- Cerrar una vuelta diciendo "queda apuntado" cuando se podia haber reparado.

Si de verdad no se puede reparar (hace falta una decision de Julio, o una llave que no existe),
**se dice EXACTAMENTE que falta y de quien depende**. Eso no es un apunte: es una pregunta con
nombre y apellido.

## POR QUE ESTA LEY EXISTE

Porque Julio lleva tres dias repitiendo lo mismo, y cada repeticion suya es un fallo de este
sistema. Su frase: *"sigo repitiendo cosas y el trabajo estancado"*. Encontrar fallos sin
repararlos **parece trabajo y no lo es**: es el mismo movimiento que un contador que mide y nadie
mira, o una ley escrita sin guardian.

**Encontrar un fallo es la mitad barata. La mitad que vale es cerrarlo.**

## COMO SE COMPRUEBA QUE SE CUMPLE, SIN QUE NADIE SE ACUERDE

Esto NO se mide con un contador que alguien tenga que subir a mano: asi murio el contador de
repeticiones de Julio. Se mide solo, mirando lo que ya queda escrito por si mismo.

Al cerrar cualquier vuelta, por cada archivo de apunte que exista tiene que haber **una de estas
tres**, y las tres se comprueban leyendo, sin preguntarle a nadie:

- el commit que lo repara (esta en el historial, se lee solo),
- la vigia que lo va a cerrar (el archivo existe o no existe, se mira solo),
- o la pregunta concreta a Julio escrita dentro del propio apunte, diciendo que falta y de quien
  depende (la palabra PREGUNTA_REQUERIDA esta o no esta, se cuenta sola).

Un apunte sin ninguna de las tres es una deuda escondida, y el guardian lo saca a la luz.

**Guardian:** `vigias/test_vigia_apunta_y_repara.py`
