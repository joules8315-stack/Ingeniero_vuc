# PENDIENTE — DOS FALLOS DE LA CASA, CAZADOS LA NOCHE DEL 2026-09-12

Ninguno de los dos se reparo: los dos piden paquete y veredicto del equipo. Quedan apuntados con
su medicion para que manana no haya que volver a descubrirlos.

---

## FALLO 1 — EL REGISTRO DE ORDENES DE JULIO SE TRAGA AVISOS DEL SISTEMA

El registro que guarda lo que dice Julio, para que ninguna orden suya se pierda, apunto esa noche
**cinco textos que Julio no escribio nunca**. Eran avisos del propio sistema:

    <summary>Background command "Pedir la reparacion con la funcion adjunta" completed</summary>
    <summary>Monitor event: "esperar la reparacion del equipo"</summary>
    <summary>Monitor "esperar la reparacion del equipo" stream ended</summary>
    <event>TODO GUARDADO: d1d8786 LA AVERIA SE DEFIENDE SOLA...</event>

Son mensajes que dicen "una tarea termino". El registro los entendio como ordenes de Julio y
freno el cierre pidiendo que se legislaran.

**POR QUE IMPORTA Y NO ES UN DETALLE.** El registro es el que garantiza que a Julio no se le
olvide nada suyo. Si se llena de ruido pasan dos cosas, las dos malas:

1. **se pierde la senal entre el ruido**: una orden de verdad queda enterrada entre diez avisos
2. **se acostumbra uno a marcar sin leer**: y el dia que entre una orden de verdad, se marca
   igual, de carrerilla. Eso es exactamente como mueren estos registros.

**LO QUE SE PROPONE** (cuenta, no juicio; lo hace un programa gratis): que la puerta por donde
entra lo que Julio escribe **no admita texto que venga entre los signos de menor y mayor** ni que
empiece por "Background command", "Monitor event" o "stream ended". Un aviso de maquina tiene
forma de aviso de maquina y se reconoce sin preguntarle a nadie.

---

## FALLO 2 — UN ARCHIVO VACIO LLAMADO "nul" DEJA CIEGO AL MAPA

Esa noche aparecio dos veces, en la carpeta de la herramienta, un archivo vacio con ese nombre. En
Windows ese nombre esta reservado, y al intentar leerlo el escaner del mapa **revienta entero**:

    ValueError: path is on mount '\\\\.\\nul', start on mount 'C:'
    en cerebro/piezas.py, funcion escanear

Y cuando el mapa cae, **cae todo lo que depende de el**: el reparto no puede armar el paquete y
el equipo no puede trabajar. Eso tumbo un intento de reparacion esa misma noche.

**DE DONDE SALE:** lo mas probable es el ayudante de la carga pesada, corriendo sus mediciones en
esa carpeta: en Windows, una orden que manda su salida "a la nada" al estilo antiguo crea un
archivo con ese nombre en vez de tirarla. No esta confirmado, y no se afirma como cierto.

**LO QUE SE PROPONE:** que el escaner **salte** los nombres reservados de Windows (nul, con, prn,
aux, com1..com9, lpt1..lpt9) en vez de reventar. Es un archivo que no deberia existir, pero un
mapa que se cae entero por un archivo raro es fragil: **el mapa tiene que sobrevivir a la basura,
no depender de que no la haya.**

Y aparte, avisar al ayudante en su orden de trabajo de que no use esa forma antigua de mandar la
salida a la nada.

---

## LO QUE SI QUEDO HECHO ESA NOCHE, PARA NO CONFUNDIR

La vigia del objetivo duplicado **ya existe y nace roja**, con los numeros medidos:
`assert 21623 <= 19042` y la marca del objetivo apareciendo 2 veces. La reparacion esta pedida al
equipo. El guardian de guardado **no deja sellar mientras siga roja**, que es lo correcto.
