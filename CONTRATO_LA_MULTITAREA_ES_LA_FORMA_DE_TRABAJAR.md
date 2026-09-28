# CONTRATO: LA MULTITAREA ES LA FORMA DE TRABAJAR

**Orden de Julio del 2026-09-28. MAXIMA PRIORIDAD.**

Trabajar de una en una es lo que hace que esto se demore demasiado, y eso es inaceptable.
A partir de hoy lo normal es trabajar en varias tareas al tiempo. Esta ley se legisla y se
verifica: no basta con escribirla, hay que comprobar que se cumple.

---

## LA LEY, EN POCAS FRASES

1. Lo normal es EN PARALELO. De una en una es la excepcion, y la excepcion se justifica por
   escrito.
2. Cuantas van a la vez lo decide LA COLA, no la memoria de nadie ni un numero escrito a mano.
3. Lo unico que va en fila es escribir en el disco y guardar, y se resuelve con turnos con tope.
4. Esperar NUNCA va en fila: mientras uno espera a una IA, los demas siguen.
5. La misma comprobacion no se repite: se corre una vez por ronda y su resultado se reusa.
6. La comprobacion se hace sobre las VECINAS de la pieza tocada, no sobre la bateria entera.
7. Ir en paralelo no es ir a lo loco: una reparacion que deja en rojo a una vecina no se sella.
8. Esto tambien manda en como trabaja quien dirige: las rondas que no dependen una de otra se
   lanzan a la vez.

---

## LAS REGLAS, UNA POR UNA

### Uno. Lo normal es EN PARALELO

El estado por defecto del taller es tener varias tareas corriendo a la vez. Trabajar de una en
una es la excepcion, y esa excepcion hay que justificarla con una razon escrita: quien la pida
tiene que decir por que esa tarea no puede ir acompanada. No vale el silencio ni la costumbre.

### Dos. Cuantas van a la vez lo decide LA COLA

El numero de tareas simultaneas NO lo decide la memoria de nadie ni un numero escrito a mano.
Lo decide la cola, que ya sabe lo que puede correr sin pisarse. La cola garantiza la coherencia
sola, y eso ya funciona hoy:

- no toma dos ordenes de la misma pieza a la vez;
- no toma ninguna orden cuya dependencia no este hecha.

Si la cola dice que dos pueden ir juntas, van juntas. Si dice que no, no van. No hay numero
magico que respetar.

### Tres. Lo unico en fila es escribir en el disco y guardar

Dos guardados a la vez se pisan. Eso es lo unico que va en fila, y se resuelve con TURNOS:

- el que llega primero guarda;
- el que llega segundo espera su turno con un tope de tiempo;
- si el tope se pasa, es FALLO, no espera eterna.

**Evidencia medida hoy:** dos guardados a la vez dejaron el indice de git bloqueado y se vieron
dos procesos peleando por el mismo archivo.

### Cuatro. Esperar NUNCA va en fila

Mientras uno espera la respuesta de una IA, los demas siguen trabajando. Nadie se queda
parado mirando una llamada. Esto se apoya en la ley hermana que ya existe,
`CONTRATO_TOPE_MEDIDO_Y_CORTE_A_MINIMA_EXPRESION`: toda espera tiene disparador y tope medido,
y lo que ocurra primero manda.

### Cinco. La misma comprobacion no se repite

Una prueba se corre UNA vez por ronda y su resultado se reusa. Hoy la misma vigia la corre el
que guarda, el que juzga si la tarea esta terminada y el que sabotea: tres veces la misma
cuenta. Ahi esta el 85 por ciento del reloj.

### Seis. La comprobacion se hace sobre las VECINAS, no sobre todo

Se comprueba la pieza tocada y sus VECINAS, no la bateria entera, y con tope de tiempo medido.
Correr todo para cambiar una pieza es lo que convierte cada guardado en minutos.

### Siete. En paralelo no es a lo loco

Una reparacion que deja en rojo a una vecina NO se sella. Esto vale igual cuando van varias
tareas a la vez: la coherencia no se relaja por ir mas rapido. Ir rapido y romper no es ir
rapido, es volver a empezar.

### Ocho. Esto tambien manda en como trabaja quien dirige

Las rondas que no dependen una de otra se lanzan a la vez, no en fila. Las que dependen siguen
su orden. Y quien dice que depende de que es LA COLA, no la memoria del que dirige.

---

## LA EVIDENCIA MEDIDA (2026-09-28)

La cadena corrio de verdad, 41 minutos seguidos, del 13:05 al 13:46. En ese rato:

| Que se midio | Cuanto |
|---|---|
| Reloj total de la cadena | 41 minutos (13:05 a 13:46) |
| Llamadas a las IA | 31 llamadas |
| Tiempo DENTRO de las IA | 6,2 minutos = **15 por ciento** del reloj |
| Rondas del equipo | 5, de las que solo 1 quedo aprobada |
| Tiempo que NO fue de las IA | unos 35 minutos = **85 por ciento** del reloj |

Ese 85 por ciento no fue trabajo de las IA: fue la propia maquina comprobando, de una en una.

Y una sola de esas comprobaciones ya estaba medida antes:

- el guardia de guardado corre la bateria de las vecinas con tope de 600 segundos mientras el
  indice de git esta bloqueado;
- 7 minutos medidos a las 12:30, con todo lo demas parado.

Conclusion: el cuello de botella no son las IA. Es la maquina comprobando en fila lo que ya
esta comprobado.

---

## COMO SE COMPRUEBA QUE SE CUMPLE

Julio lo pidio expresamente. Estos cuatro comandos se corren tal cual, sin cambiarlos:

**1. Cuantas tareas a la vez le pasa el mando que lanza la cadena** (si aparece el nombre del
proyecto solo, le esta pasando una):

```
cd C:\Ingeniero_VUC; Select-String -Path ingeniero.py -Pattern bucle\(
```

**2. La vigia de la multitarea, que es la que manda aqui:**

```
cd C:\Ingeniero_VUC; python -m pytest -q vigias/test_vigia_la_cadena_trabaja_en_varias_a_la_vez.py
```

**3. Cuanto del reloj se fue DENTRO de las IA** (hoy salio 15 por ciento; se cambia la hora del
principio por la del tramo que se quiera medir):

```
cd C:\Ingeniero_VUC; python -c import json; tot=0; n=0;
 [ (globals().__setitem__('tot', tot+float(d.get('segundos') or 0)), globals().__setitem__('n', n+1))
 for d in (json.loads(l) for l in open('memoria/CUADERNO_DE_LLAMADAS.jsonl',encoding='utf-8'))
 if d.get('cuando','') >= '2026-09-28 13:05' ]; print(n, 'llamadas', round(tot/60,1), 'minutos dentro de las IA')
```

**4. Si de verdad hubo dos trabajos a la vez** (en el cuaderno, dos llamadas de la misma clase
con la misma hora al minuto son dos trabajos solapados, y de una en una eso no puede pasar):

```
cd C:\Ingeniero_VUC; Select-String -Path memoria\CUADERNO_DE_LLAMADAS.jsonl -Pattern 'clase: reparar' | Select-Object -Last 10
```

El cuaderno de llamadas vive en `memoria/CUADERNO_DE_LLAMADAS.jsonl` y cada renglon trae cuando,
quien, tamano, clase, resultado y segundos.

---

## PIEZAS QUE HOY INCUMPLEN

- `ingeniero.py` — en el mando que lanza la cadena: le pasa una sola tarea.
- `cuerpo/capataz.py` — en la funcion `bucle`: ya sabe correr varias a la vez, recibe cuantas y
  usa un grupo de hilos. El motor existe y esta sin usar.
- `arnes/guardia_de_guardado.py` — la bateria con tope de 600 segundos mientras el guardado esta
  bloqueado.
