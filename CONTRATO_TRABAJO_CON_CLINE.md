# CONTRATO — SE TRABAJA CON CLINE, Y ALGUIEN RESPONDE POR ELLO

**Julio, 2026-08-31:** *"Trabaja con cline y haz la reparacion... Una vez termine la tarea cline,
superviza, si es correcta, dale otra tarea, sino, dile que corrija, y me informas si falla."*

## 0. EL FOCO: SE AFINA LA HERRAMIENTA, NO EL PRODUCTO

**Julio, 2026-08-31:** *"no vas a reparar a hacer pruebas del ingeniero reparando el MVP,
seguimos afinando el ingeniero"*.

Mientras esta orden siga en pie, **no se toca ningun proyecto de Julio para probar la
herramienta**. Ni foto_informe, ni dmm, ni ninguno. La herramienta se prueba **contra si misma**,
que es lo que se hizo el 2026-08-31 y funciono: la busqueda por nombre se uso para reparar el
diccionario, y ahi mismo destapo su propio fallo.

Solo Julio levanta este foco. Nadie lo levanta "porque venia bien para probar".

### FOCO VIGENTE: PROYECTOS

**Julio lo levanto el 2026-09-11, con estas palabras:**

> *"Asignale todos los problemas por resolver, lo pesado, lo que cuesta, a opencode, que
> investigue, que repare todos los danos de raiz."*

> *"Crea el plan de reparaciones y construccion de todo el DMM, y terminalo con opencode, entre
> ustedes dos."*

**Que cambia:** desde hoy SI se trabaja sobre el DMM. El plan que manda es `PLAN_DMM_COMPLETO.md`,
en la raiz del DMM, y las tareas estan repartidas en el reparto de verdad.

**Que NO cambia:** el foco no es una excusa. Sigue prohibido tocar un proyecto de Julio **para
probar la herramienta**; lo que se levanta es trabajar en el DMM **porque Julio lo ha mandado**,
con su plan y con sus guardianes.

**Como se vuelve atras:** lo dice Julio, y se cambia esta linea a `FOCO VIGENTE: HERRAMIENTA`.
Nadie mas la toca.

---

**POR QUE ESTO ESTA ESCRITO AQUI Y NO DENTRO DE UNA PRUEBA (2026-09-11):** el foco estaba
CONGELADO dentro del guardian, asi que cuando Julio lo levanto, el guardian siguio defendiendo una
orden de hacia once dias y freno trabajo que Julio acababa de mandar. Un guardian que defiende una
orden vieja contra una nueva no protege: estorba. **Ahora el guardian LEE esta linea.** Y si no la
encuentra, se pone en lo mas estricto (la herramienta), para que borrarla no sea la forma de
apagarlo.

## 1. LA TAREA SE ASIGNA, NO SE OFRECE

**Julio, 2026-08-31:** *"asignale tarea a cline"*.

Nunca se le manda una lista para que elija. **Se le asigna UNA tarea concreta**, con:

- **Que hay que conseguir**, dicho como resultado, no como programacion.
- **El pedazo de codigo DENTRO del encargo**, no solo nombrado.
- **Lo que ya esta hecho y en verde**, para que no lo repita ni lo pise.
- **Lo que NO debe tocar** (lo que tiene el otro).
- **Lo medido**: numeros, no impresiones.

## 2. NO SE PISAN

Cada tarea tiene **un solo dueno**. El reparto vive en `memoria/REPARTO_IA.json` y lo lleva
`arnes/reparto.py`. Dos IA con la misma tarea es trabajo pagado dos veces y un choque al guardar.

## 3. LO QUE UNO NO PUEDE CERRAR, SE LE PASA AL OTRO

**Julio, 2026-08-31:** *"asignale tarea a cline, esa que no has podido resolver y despues la
supervisas"*.

Una tarea atascada **no se queda parada esperando**. Se le pasa a la otra IA, y se le pasa
**con todo el material**: el codigo dentro, lo ya medido, lo que se intento, por que no salio, y
las trampas conocidas. Pasarla sin el material es tirarle el problema encima, no repartir.

Y **quien la pasa la supervisa**. No se pasa para quitarsela de encima.

## 4. SE SUPERVISA LO QUE ENTREGA. SIEMPRE.

Cuando dice que termino, **no se da por bueno**. Se comprueba:

| Se comprueba | Como |
|---|---|
| Que hizo lo que se le pidio | corriendo su vigia, y que este **verde** |
| Que no rompio a los vecinos | corriendo las demas vigias |
| Que lo que dice es cierto | **mirando el codigo**, no creyendo su palabra |

Y despues, una de tres:
- **Correcto** → se le da la siguiente tarea.
- **Incorrecto** → se le dice **que corrija**, con el fallo concreto y medido.
- **Falla y no sale** → **se le informa a Julio**. No se esconde ni se maquilla.

## 5. LA PALABRA DE OTRA IA NO ES PRUEBA

Medido el 2026-08-31, dos veces el mismo dia:

- Cline afirmo que faltaba poner una llave que **ya estaba puesta**.
- El revisor del equipo rechazo **tres veces** diciendo que no veia un texto que **si tenia
  delante** (comprobado letra por letra en el papel que recibe).

**Antes de repetirle a Julio lo que dijo otra IA, se comprueba en el codigo.** Si no se comprobo,
se dice que no se comprobo. Y al reves: **antes de echarle la culpa a la otra IA, se comprueba**.
Ese mismo dia se le echo en cara a Cline un fallo que era del limpiador propio.

## 6. EL CANAL ES UN BUZON, NO UN TELEFONO

Dejar el recado funciona. Al dejarle una tarea, **se le dice a Julio** si hace falta que abra la
otra IA. Callarselo es dejar la tarea muerta y aparentar que se avanzo.

## 7. NADA QUEDA PENDIENTE

La vigia nace roja, se repara, queda verde, y recien entonces la siguiente. **Un paso en rojo no
se guarda ni se avanza.**

## QUIEN LO HACE CUMPLIR

- `arnes/reparto.py` — lleva quien tiene que tarea y en que estado.
- `vigias/test_vigia_reparto_con_cline.py` — mide el reparto y la supervision.
- `vigias/test_vigia_lo_atascado_se_pasa.py` — mide los puntos 0, 1 y 3.
