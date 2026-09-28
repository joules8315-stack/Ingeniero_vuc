# CONTRATO DEL TOPE MEDIDO Y DEL CORTE A LA MINIMA EXPRESION

**Fecha:** 2026-09-28
**Quien lo manda:** Julio
**Que es esto:** dos ordenes que Julio dio hoy y que no estaban escritas en ninguna de las 66 leyes.
Por no estar escritas se repetian cada semana. Aqui quedan escritas, con lo que se midio hoy.

---

## LA LEY, en pocas frases

1. Ninguna espera se escribe de memoria: el tope sale de lo que se midio en el cuaderno de llamadas.
2. Toda espera se cierra con dos cosas, y vale la que llegue primero: el disparador y el tope de tiempo.
3. Pasarse del tope no es esperar mas: es fallo, se apunta como fallo y el trabajo sigue por otro lado.
4. Si contesta, la respuesta no se cree: la comprueban los programas que ya existen.
5. El corte del material no se mide contra ninguna IA: se mide contra la tarea. Primero se corta a la
   minima expresion completa y que funcione; despues se busca la IA a la que le quepa y este disponible,
   lo gratis primero.

---

## ORDEN UNO — TOPE MEDIDO, DISPARADOR Y CORTE A FALLO

### Regla 1. El tope sale de lo medido, no de la memoria

Ninguna espera se escribe de memoria. El tope de tiempo de una espera sale de lo que se MIDIO antes en el
cuaderno de llamadas. El documento dice donde se mide:

    memoria/CUADERNO_DE_LLAMADAS.jsonl

Esa es la unica ruta que se nombra. No se inventa ninguna otra ni se nombran carpetas que el encargo no
diga. Cada renglon del cuaderno trae: cuando, quien, tamano, clase, resultado y segundos.

### Regla 2. Dos cosas cierran la espera, y vale la que llegue primero

Una espera no se cierra solo por tiempo. Se cierra por dos cosas:

- el **disparador**: llego la respuesta, o llego la senal que se esperaba;
- el **tope de tiempo**: el maximo medido para esa labor.

Vale la que llegue primero. Si llega el disparador antes, la espera termina bien y se sigue. Si llega el
tope antes, la espera termina mal.

### Regla 3. Pasarse del tope es fallo, no es esperar mas

Pasarse del tope NO es esperar mas. Es fallo. Se apunta como fallo y el trabajo sigue por otro lado. No se
abre una espera nueva para el mismo asunto sin cambiar algo.

### Regla 4. Si contesta, la respuesta no se cree: se comprueba

Si la espera termina porque llego la respuesta, esa respuesta no se cree. La comprueban los programas que
ya existen:

- el revisor por programa;
- las vigias vecinas de la pieza tocada.

Esos son los que dicen si se rompio algo que ya servia.

### Regla 5. Los topes tienen que ser coherentes

El tope de fuera tiene que ser mayor que la suma de los topes de dentro. Si el de fuera es menor, la espera
de fuera corta antes de que las de dentro puedan terminar, y el fallo se apunta contra quien no lo merece.
Esto ya costo un fallo real apuntado en la memoria de fallos.

### Evidencia medida hoy, 2026-09-28

Tres hechos medidos hoy, que van aqui como prueba:

1. El guardia de guardado corrio la bateria de vecinas con tope de 600 segundos mientras el indice de git
   estaba bloqueado. Se midieron 7 minutos a las 12:30. En ese rato nada mas pudo avanzar.
2. A Codex se le pidio una palabra y no contesto en 120 segundos.
3. A mano tardo 245 segundos y acabo sin cupo, gastando 21.726 unidades esperando una ronda del equipo sin
   entregar nada.

---

## ORDEN DOS — CORTE A LA MINIMA EXPRESION COMPLETA

### Regla 6. El corte se mide contra la tarea, no contra la IA

El corte NO se mide contra la capacidad de ninguna IA, ni de la de pago ni de la de la gratis. Se mide
contra la tarea: entra lo que la tarea nombra y lo que eso usa, y se para ahi. Primero se corta el material
a su minima expresion completa y que funcione. Despues se busca la IA a la que le quepa y este disponible,
lo gratis primero.

### Regla 7. El presupuesto de letras es UNO y es para el paquete COMPLETO

Hay un solo presupuesto de letras, y es para el paquete COMPLETO, no solo para los pedazos de codigo. Los
pedazos pueden respetar su tope y el paquete entero pasarse igual.

Evidencia medida hoy: los pedazos respetaban su tope de 19.000, pero el paquete entero salio con 28.062
letras y al cerebro le viajaron 33.655, cuando el gratis aguanta 19.042.

### Regla 8. Las leyes no pesan: viaja la ley que habla del problema

No viaja una ley entera por venir primera en el abecedario. Viaja la ley que habla del problema, y solo el
trozo que aplica.

Evidencia medida hoy: la ley se elegia ordenando por nombre y se copiaba entera la primera, asi que
viajaron 2.087 letras de una ley que no tenia nada que ver con el problema.

### Regla 9. Si se pide una funcion, viaja esa funcion completa, no el vecindario

Si la tarea nombra una funcion, viaja esa funcion completa. No viaja el vecindario de alrededor.

Evidencia medida hoy: viajaron 220 renglones (15.206 letras) cuando la tarea nombraba 30.

### Regla 10. Un pedazo contenido dentro de otro no viaja dos veces

Si un pedazo esta contenido dentro de otro, no viaja dos veces. Se manda el que contiene y se quita el
contenido.

### Regla 11. La tijera al final del pasillo es ultimo freno, y si se usa es fallo del armado

Recortar con tijera al final del pasillo es un parche que puede cortar lo que hacia falta. Se permite solo
como ultimo freno. Si hace falta usarlo, es senal de que el paquete se armo mal, asi que queda apuntado
como fallo del armado.

### Regla 12. El formato del paquete y el de la respuesta son compactos y ontologicos

El formato del paquete y el de la respuesta son compactos y ontologicos. Dicen:

- que se pide;
- que resultado se espera;
- que material hay y donde.

Sin prosa repetida. Que no de pie a malas interpretaciones.

---

## COMO SE COMPRUEBA

Comandos listos para PowerShell, desde la raiz del proyecto.

**1. Que el cuaderno de llamadas existe y se puede leer:**

```powershell
Test-Path memoria/CUADERNO_DE_LLAMADAS.jsonl
Get-Content memoria/CUADERNO_DE_LLAMADAS.jsonl -TotalCount 3
```

**2. Que cada renglon trae cuando, quien, tamano, clase, resultado y segundos:**

```powershell
Get-Content memoria/CUADERNO_DE_LLAMADAS.jsonl |
  ForEach-Object { $_ | ConvertFrom-Json } |
  Select-Object -First 5 cuando, quien, tamano, clase, resultado, segundos
```

**3. Que el tope de una espera sale de lo medido (no de la memoria):**

```powershell
Get-Content memoria/CUADERNO_DE_LLAMADAS.jsonl |
  ForEach-Object { $_ | ConvertFrom-Json } |
  Where-Object { $_.clase -eq 'guardado' } |
  Measure-Object -Property segundos -Maximum -Average
```

**4. Que el tope de fuera es mayor que la suma de los de dentro:**

```powershell
# Se leen los topes declarados y se comprueba la suma a mano en el contrato de la pieza.
Select-String -Path arnes/guardia_de_guardado.py -Pattern 'TOPE|timeout|segundos'
Select-String -Path cuerpo/codex.py -Pattern 'TOPE|timeout|segundos'
```

**5. Que el paquete entero no pasa del presupuesto de letras:**

```powershell
Get-ChildItem memoria/paquetes -Filter *.json |
  ForEach-Object { [pscustomobject]@{ archivo=$_.Name; letras=(Get-Content $_.FullName -Raw).Length } } |
  Sort-Object letras -Descending | Select-Object -First 5
```

**6. Que no viaja una ley entera por venir primera en el abecedario:**

```powershell
Select-String -Path cerebro/router.py -Pattern 'ley|abecedario|sort|orden'
```

**7. Que un pedazo contenido dentro de otro no viaja dos veces:**

```powershell
Select-String -Path cerebro/router.py -Pattern 'quitar_contenidos|contenido'
```

**8. Que la tijera al final del pasillo queda apuntada como fallo del armado:**

```powershell
Select-String -Path cerebro/router.py -Pattern 'tijera|recort|fallo'
```

---

## PIEZAS QUE HOY INCUMPLEN CADA REGLA

Estas son las piezas que hoy incumplen, nombradas por su ruta, para que quien venga a repararlas sepa
donde mirar. No se inventa ninguna: las tres ya estan medidas.

| Pieza | Que regla incumple |
|---|---|
| `arnes/guardia_de_guardado.py` | Reglas 1, 2, 3 y 5: la espera del guardado. Corre la bateria de vecinas con tope de 600 segundos sin sacar el tope de lo medido, y bloquea el indice de git mientras espera. |
| `cuerpo/codex.py` | Reglas 1, 2 y 3: la espera de Codex. Se le pidio una palabra y no contesto en 120 segundos, y no habia disparador ni corte a fallo apuntado. |
| `cerebro/router.py`, funcion `armar` | Reglas 6, 7, 8, 9, 10 y 11: el presupuesto del paquete y la eleccion de la ley. El paquete entero salio con 28.062 letras, la ley se eligio por abecedario y viajaron 220 renglones cuando la tarea nombraba 30. |

---

## LO QUE ESTE CONTRATO NO HACE

Este contrato no toca ningun archivo `.py`. Es un documento de ley. Las reparaciones de las tres piezas de
arriba van en otra ronda, y quien las haga tiene que citar este contrato.
