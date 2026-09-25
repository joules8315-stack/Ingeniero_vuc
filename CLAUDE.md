# INGENIERO VUC — instrucciones fijas

Herramienta de Julio para **crear y reparar cualquier proyecto sin gastar tokens de mas**.
Vive en `C:\Ingeniero_VUC`, no pertenece a ningun proyecto, atiende a los de `proyectos.config`.

## PRIORIDAD UNO EN CURSO (aprobada por Julio el 2026-09-25)
**Lo primero que se lee al empezar: [`PLAN_PRIORIDAD_UNO.md`](PLAN_PRIORIDAD_UNO.md).**
No se pasa a ninguna otra prioridad hasta terminarlo. Orden: R0 el cierre atascado → R1 el trabajo
aprobado llega al disco + R2 el material completo → recoger los 14 trabajos frenados → R3/R4/R5
velocidad → R6 paralelo + R7 la llave por partes → R8 el comando `plan`.
El estado vive en `memoria/ORDENES.json`, no en el chat.

## LA REGLA QUE MANDA SOBRE TODAS
**No se lee el proyecto. Se lee el PAQUETE MINIMO.**

Ante cualquier problema, lo PRIMERO es:
```
cd C:\Ingeniero_VUC; python ingeniero.py trabaja <proyecto> "<el problema en palabras de Julio>"
```
Eso deja un paquete en `memoria/paquetes/`. Ese paquete es TODO el material permitido.
Si falta algo, se PIDE (formato `NECESITO_LEER` al final del paquete). No se abre por cuenta propia.

## LAS 5 LEYES DE JULIO (no se negocian)
1. **Nunca asumir.** Si el contrato no lo dice, se escribe `PREGUNTA_REQUERIDA:` y se le pregunta a Julio.
2. **Nunca inventar.** Si un archivo/funcion/linea no existe, se escribe `NO_ENCONTRADO`. Jamas se rellena.
3. **Vigia verde NO es prueba.** La prueba es que Julio lo vea funcionar con sus ojos.
4. **No romper vecinos.** Antes de tocar, se lee la seccion "A QUIEN PUEDE DANAR" del paquete.
5. **Hablarle en simple.** Julio no es tecnico. Nada de jerga; el comando siempre listo para PowerShell (`;`, no `&&`).

## LAS 2 LEYES DEL 2026-08-24 (se suman a las 5, no se negocian)
6. **Siempre en equipo, sin salto, en TODAS las IA** (Claude, Cline, ChatGPT). Para saltar el candado de equipo se pide permiso y la respuesta es SIEMPRE **denegado**.
7. **Probar de verdad antes de pedirle a Julio.** Antes de pedirle que pruebe con sus ojos se corre, con el equipo, una prueba real interna (Playwright) que demuestre que el objetivo se cumple. Si se logro, se le avisa; si no, se aprende del error y se reinicia el ciclo para lograr el resultado, sin excusas.

## LA LEY DEL 2026-08-27 (LA MEMORIA NO MIENTE NI OLVIDA)
El paquete del repartidor trae la pieza **COMPLETA**: su flujo, con quién se relaciona, las rutas que
ya se tomaron (cuáles acertaron y cuáles no) y su historial. Se mide si la memoria sirve (cada
`NECESITO_LEER` cuenta como fallo de fragmentación). **Regla madre:** si el sistema no puede trabajar,
se **repara la causa de fondo de la herramienta antes de pedir llaves**; la herramienta se repara/
afina mientras construye.

## LA LEY DE LA DECISIÓN DE REPARAR (2026-08-27)
Antes de tocar código se responden las **5 preguntas**: qué, dónde, por qué, cuándo y cómo. Si todo
es positivo (se sabe todo con precisión), se legisla y se repara. Si algo no se sabe, se investiga,
se vuelve a responder y recién se repara.

## LA LEY DE LA LLAVE ÚNICA (2026-08-27)
Cuando Julio pone su llave, **no se abren los 12 candados de golpe**. Se abren **solo** los que la
tarea necesita, ni más ni menos. Y antes de abrir, se le dice exactamente **cuáles** se abren y **por
qué**.

## COMO SE TRABAJA (el protocolo, no hay que repetirselo a nadie)
```
python ingeniero.py arranca                 # donde ibamos (el estado NO vive en el chat)
python ingeniero.py trabaja <proy> "<problema>"
python ingeniero.py vigias <proy> antes     # de que color estan ANTES
   ... reparar SOLO con el paquete ...
python ingeniero.py vigias <proy> despues   # no romper nada
   ... Julio prueba con sus ojos ...        # sin esto no se sella
```

## LO QUE ESTA PROHIBIDO
- Abrir un archivo entero de mas de 300 lineas (el candado `arnes/read_gate.py` lo frena).
- Reparar sin paquete vigente.
- Sellar con una vigia roja.
- Crear una pieza nueva que duplique una existente: primero se busca en el mapa.

## DONDE ESTA CADA COSA
- `cerebro/` — piezas, enlaces, flujos, trozos, grafo, router. El grafo tipo Obsidian.
- `arnes/`   — los candados (`read_gate.py` = candado de LECTURA, el que cuida el dinero).
- `vigias/`  — las pruebas del propio Ingeniero. Se corren con `python -m pytest -q vigias/`.
- `memoria/` — ESTADO.json (donde ibamos), paquetes/, grafos/, rescate/.
- `mapa/`    — el inventario de TODOS los proyectos. Se regenera, no se edita a mano.

<!-- INGENIERO_VUC:INICIO -->
## AHORRO DE TOKENS — lo pone el Ingeniero VUC (C:\Ingeniero_VUC)

**No se lee este proyecto entero. Se pide el paquete minimo.**

Ante cualquier problema, PRIMERO:
```
cd C:\Ingeniero_VUC; python ingeniero.py trabaja ingeniero "<el problema en palabras de Julio>"
```
Eso entrega la ley que manda, las piezas con su boca, los trozos exactos (`archivo:linea-linea`),
las vigias que protegen y a quien se puede danar. Ese paquete es TODO el material permitido.

Si falta algo, se PIDE asi (no se abre por cuenta propia):
```
NECESITO_LEER:
  archivo: <ruta>   motivo: <que responde>   decide: <que desbloquea>   riesgo: <si no lo leo>
```

Leyes: nunca asumir · nunca inventar (`NO_ENCONTRADO`) · vigia verde NO es prueba (la prueba es
que Julio lo vea) · no romper vecinos · hablarle simple y con el comando listo para PowerShell.
<!-- INGENIERO_VUC:FIN -->

