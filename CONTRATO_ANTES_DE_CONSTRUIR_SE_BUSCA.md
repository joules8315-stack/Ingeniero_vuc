# CONTRATO — ANTES DE CONSTRUIR, SE BUSCA: ¿ya existe? ¿es habilidad o es programa?

**Julio, 2026-09-07:**

> *"Cuando estés reparando y creando el DMM, lo primero que vas a hacer es revisar el mapa y
> buscar todas las funciones, para buscar su skill, o crear su script. Ya la mayoría de ellos
> existe para agencia de marketing; lo que haga falta, construirlo."*

---

## LA LEY

**Antes de construir NADA en DMM (y en cualquier proyecto), se recorre el mapa y, función por
función, se responde en este orden:**

1. **¿Ya existe aquí?** → se usa. No se duplica.
2. **¿Existe como habilidad ya escrita?** → se instala y se usa.
3. **¿Existe fuera, hecho para agencias de marketing?** → se trae, no se reinventa.
4. **¿Es una CUENTA?** → se hace con un programa. Gratis. (`CONTRATO_CUENTA_O_JUICIO`)
5. **¿Es un JUICIO y no existe?** → **recién entonces** se construye, con el equipo.

**Solo se llega al paso 5 después de haber fallado los cuatro anteriores.** Construir sin haber
recorrido los cuatro es duplicar, y duplicar es el gasto que Julio lleva meses persiguiendo.

---

## POR QUÉ NACE ESTA LEY (hechos medidos, con fecha)

- **2026-09-06:** el plan escrito de DMM mandaba crear una memoria de historial. **Ya había
  dos funcionando.** Crearla habría sido duplicar. Se amplió lo que existía y el hueco real
  resultó ser mucho más pequeño de lo que decía el papel.
- **2026-09-06:** ese mismo plan daba por faltantes **tres piezas que ya existen**:
  `cuerpo/experimentos.py` (75 líneas, con su vigía), `cuerpo/crm.py` (60) y
  `cuerpo/compliance.py` (55). Seguirlo a ciegas habría hecho el trabajo dos veces.
- **El caso de `experimentos.py` es el aviso más caro que hay guardado:** figura como fallo
  repetido **CINCO veces** — cinco encargos seguidos para crear un módulo que **hoy existe en
  el disco**. Esta ley nace, sobre todo, de ese caso: **se mira el disco antes de creerle al
  papel.**
- **2026-09-06:** de 8 rondas pagadas, **5** fueron para copiar un texto ya escrito: trabajo de
  programa pagado a un cerebro.

**El papel escrito envejece. El mapa y el disco no mienten.**

---

## LA TABLA DE VERDAD — el orden de la búsqueda

| Paso | Pregunta | Con qué se responde | Si la respuesta es sí |
|---|---|---|---|
| 1 | ¿Ya existe en este proyecto? | `MAPA_CANONICO.md` de DMM **y el disco** | Se usa. **No se duplica** |
| 2 | ¿Existe como habilidad? | `python ingeniero.py buscar-skill "<lo que hace falta>"` | Se instala y se usa |
| 3 | ¿Existe fuera, para agencias? | Búsqueda por lo que HACE, no por su nombre | Se trae |
| 4 | ¿Es una CUENTA? | `CONTRATO_CUENTA_O_JUICIO` | **Lo hace un programa. Gratis** |
| 5 | ¿Es JUICIO y no existe? | Las 5 respuestas de `CONTRATO_CREAR_PIEZA_NUEVA` | Se construye con el equipo |

### Regla del disco por encima del papel
En el paso 1, **mirar el disco es obligatorio**, no basta con el mapa ni con un plan escrito.
Un documento puede decir que algo falta y estar equivocado: pasó con `experimentos.py`, y
costó cinco encargos.

### Regla de los dos caminos (obligatoria en los pasos 1, 2 y 3)
Se busca **por su nombre Y por lo que hace**. Un nombre que no aparece **no es una avería**:
casi siempre es otra forma de escribir lo mismo. Frenar ahí es un fallo falso.
(`CONTRATO_CUENTA_O_JUICIO`, Regla 4.)

---

## LA MATRIZ — cómo se recorre DMM

1. Se lee el **mapa canónico** de DMM y su **matriz de faltantes**. **NO** el plan escrito:
   está viejo y ya se comprobó que miente sobre cuatro piezas.
2. Se hace la **lista de funciones** del proyecto, una por una.
3. Por cada una se responden los 5 pasos y **se escribe la respuesta**.
4. Se trabaja **una tarea a la vez**, y **un encargo por archivo**
   (cura del 2026-08-31: un encargo que tocaba dos archivos lo rechazaron tres veces seguidas).
5. Lo que resulte CUENTA se va apartando a una lista: **eso es lo que deja de costar dinero**.

---

## A QUIÉN PUEDE DAÑAR

- A nadie. Es una ley de orden: **manda buscar antes de construir**.
- **No sustituye** a `CONTRATO_CREAR_PIEZA_NUEVA`: lo refuerza. Aquella pone las condiciones
  para crear; esta obliga a agotar la búsqueda antes de llegar a crear.
- **No toca** la vía canónica: cada proyecto se toca solo con su ruta y su rama comprobadas.

## CÓMO SE COMPRUEBA

`vigias/test_vigia_antes_de_construir_se_busca.py`, determinista y sin red: ante una pieza
nueva declarada, exige que estén escritas **las respuestas de los 5 pasos**. Si falta una,
**frena** y dice cuál falta.

**Vigía verde no es prueba.** La prueba es que Julio no vea aparecer dos piezas que hacen lo
mismo, y que la lista de "esto lo hace un programa" crezca en cada vuelta.
