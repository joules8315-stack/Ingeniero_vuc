# ENCARGO PARA CLINE — el obrero repara POR TEXTO, no por numero de renglon

**Lo manda Julio.** Claude no pudo cerrarla: se quedo sin revisor libre (los cerebros gratis
daban error de servidor y el de pago estaba haciendo de obrero). No es que falte saber que hacer:
esta todo medido y el material va aqui dentro.

## ESTO ES LO QUE JULIO LLEVA PIDIENDO DESDE EL PRINCIPIO

> "Lo que borra todo, que cuenta por lineas, por que no lo reemplazas, por que lo busque por
> funcion y nombre... si en definitiva no se puede buscar por numero, que se elimine esa
> instruccion y quede buscando por funcion y nombre."

La mitad ya esta hecha y en verde (la busqueda por nombre, el repartidor, la ley y el candado).
**Falta esta mitad: que el propio obrero deje de pedir tramos.**

## EL CODIGO QUE HAY AHORA (verbatim, sacado del archivo hace un segundo)

```python
def _prompt_obrero(paquete, tarea):
    return f"""Eres el OBRERO de un ingeniero de software. Trabajas SOLO con el material de abajo.

REGLAS DURAS (si las rompes, tu trabajo se descarta):
1. NO inventes archivos, funciones ni lineas. Si algo no esta en el material, escribe NO_ENCONTRADO.
2. NO decidas lo que el contrato no dice. Escribe PREGUNTA_REQUERIDA: <la pregunta en palabras simples>.
3. Cambia lo MINIMO. Nombra el archivo y la linea exacta de cada cambio. IMPORTANTE: al nombrar la
   linea, COPIAS el texto literal de esa linea tal como aparece en el material (no solo el numero).
   Un numero solo se confunde (ej: "7" se lee como "1"); el texto no. Si no copias el texto exacto,
   tu trabajo se descarta.
4. Antes de terminar, di a quien puedes danar (mira la seccion "A QUIEN PUEDE DANAR").
5. Trabaja SOLO con la memoria del PAQUETE de abajo (la informacion indexada). Si te falta material
   para responder, pidelo asi y nada mas: NECESITO_LEER: archivo / motivo / que decide / riesgo.
   No rechaces el trabajo ni te inventes excusas: el material es el suficiente para lo que se te pide.

TAREA: {tarea}

Responde SOLO un JSON valido, sin texto alrededor:
{{"diagnostico": "que esta mal, en una frase",
  "archivo": "ruta exacta del material",
  "lineas": "desde-hasta",
  "linea_texto": "el texto literal de la linea que vas a tocar, copiado tal cual del material",
  "cambio": "que hay que cambiar, concreto",
  "codigo": "el codigo nuevo, solo el pedazo",
  "vigia": "que prueba lo comprobaria",
  "puede_danar": ["pieza1", "pieza2"],
  "preguntas": ["si falta decidir algo"],
  "confianza": "alta|media|baja"}}

===== MATERIAL (esto es TODO lo que existe) =====
{paquete}
===== FIN DEL MATERIAL ====="""
```

## LO QUE HAY QUE CONSEGUIR — solo en `cuerpo/obrero.py`, y en ningun otro archivo

1. En la **regla numero 3**, que quede escrito que esta **PROHIBIDO dar numeros de renglon o
   tramos**, porque un tramo borra la funcion entera y los numeros se corren solos; que el sitio
   se senala **por NOMBRE** (que archivo, que funcion) y **copiando el texto literal** que hay
   ahora y el que debe quedar; y que ese texto tiene que aparecer **palabra por palabra** en el
   material y ser **UNICO** en el archivo (si se repite, se alarga hasta que lo sea).
   **CONSERVA la frase exacta** `COPIAS el texto literal`: otra vigia la exige y se pondria roja.

2. En las **casillas que el obrero rellena**, quitar la que pide el tramo (la de `desde-hasta`) y
   la que pide el texto de una sola linea, y poner **tres**:
   - el **nombre** de la funcion o seccion donde esta (nunca un numero),
   - el **texto literal que hay AHORA** y que se sustituye,
   - el **texto literal que debe quedar**.
   Las demas casillas siguen igual.

3. Se **conservan todos los comentarios**. Nada mas cambia.

## OJO CON ESTO (te ahorra rojas)

- `vigias/test_vigia_el_auditor_juzga_por_texto.py` y `vigias/test_vigia_memoria_completa.py`
  exigen hoy la palabra `linea_texto`. Al cambiarla tendras que **actualizar esas vigias al
  contrato nuevo**. No las aflojes: que **pidan mas**, no menos.
- El candado `arnes/candado_por_nombre.py` **frena** cualquier codigo que pida un tramo. Si te
  frena, es que lo estas haciendo bien al reves.

## COMO NO PERDER VUELTAS (aprendido hoy a base de ocho rechazos)

1. **Comprueba antes de mandar el encargo** que el pedazo de codigo le LLEGA al equipo.
2. Si no llega, **mete el codigo DENTRO del encargo**. Con eso aprueba a la primera.
3. **Un encargo, UN archivo.**
4. Saca una pieza entera por su nombre con `cerebro/piezas.py::funcion_completa`.
5. Si no hay revisor libre, **reparte a mano**: uno genera y otro revisa, con `evitar`.

## EL METODO, que no se negocia

Vigia primero y que **nazca roja** -> reparas -> **verde** -> recien entonces la siguiente.
Nada queda pendiente. Nada se guarda en rojo.

**Cuando termines, dilo por el canal. Julio mando que yo te lo supervise.**
