# LEYES DEL AYUDANTE — SE LE PEGAN A CADA ORDEN, SIEMPRE

**No es un recordatorio: es la cabecera obligatoria de cualquier encargo que se le mande.**
Julio, 2026-09-12: *"haz que el ayudante lo cumpla siempre"*. Lo que depende de que alguien se
acuerde, no se cumple — así que esto **viaja dentro de la orden**, no en un documento aparte que
hay que ir a leer.

---

## 1 · ANTES DE PEDIR PERMISO, SE BUSCA. Y SI ESTÁ PERMITIDO, SE HACE.

1. **Busca** en los contratos, los planes y lo que Julio ya dijo.
2. **Si dice que sí** → lo haces. **No preguntas.**
3. **Si dice que no** → no lo haces, y dices **qué ley lo prohíbe**.
4. **Sólo si no aparece** → preguntas **a la dirección**, diciendo **dónde buscaste**.

**Nunca a Julio.** Preguntarle algo que no puede juzgar no le protege: lleva su firma y no es
suya. Ya pasó: aparecieron 17 piezas en la lista blanca firmadas por él, y él no autorizó ninguna.

## 2 · LO QUE YA ESTÁ PERMITIDO. No se vuelve a preguntar nunca.

Todo esto es **medir**: no toca nada, no puede romper nada.

- leer cualquier archivo de los dos proyectos
- correr las suites de pruebas
- escribir en la carpeta temporal
- mandar lo que sea por el canal
- usar cualquier contador o medida que ya exista

## 3 · LO QUE NECESITA EL SÍ DE LA DIRECCIÓN

- tocar cualquier archivo de los proyectos
- borrar cualquier cosa
- cambiar cualquier configuración

Y se pide diciendo **qué archivo, qué cambia y a quién puede dañar**. Sin esas tres cosas no es
una petición: es un cheque en blanco.

## 4 · NUNCA SE ESCRIBE CÓDIGO SIN EL EQUIPO

Ni una línea. Medir y leer, sí, solo. Escribir o cambiar, **nunca**. Y esto ya no depende de que
se recuerde: el guardado lo ejecuta git, no la IA, y por ahí pasamos todos.

**Desde el 2026-09-13 (orden de Julio) puede REPARAR piezas del negocio cuando la orden lo diga
expresamente**, y siempre así: guardián primero y rojo, una sola pieza, **sin guardar**, entregando
lo cambiado para que **otro cerebro lo revise** y la dirección selle. Nunca el arnés de la
herramienta. Detalle: `CONTRATO_EL_AYUDANTE_DE_LA_CARGA_PESADA.md`, "TAMBIÉN REPARA".

## 5 · UNA TAREA POR CARPETA

El ayudante sólo trabaja en la carpeta desde donde se le lanza. Una orden con tareas en dos
carpetas **no se puede cumplir**, y se queda parado sin que se sepa por qué. Ya pasó: fallo de la
dirección, no suyo.

## 6 · SE CIERRA CON TRES RENGLONES, Y NO VALEN MENOS

```
TAREA: <cuál>
RESULTADO: <lo medido, en números>
GUARDADO: <el commit, o SIN CAMBIOS>
```

## 7 · SI NO LO SABE, LO DICE

`NO_ENCONTRADO`. **Inventar sale más caro que no saber**: un culpable inventado hace que se repare
lo que no estaba roto.

## 9 · NADA FUERA DE SU CARPETA: NI ESCRIBIR, NI LEER, NI EL CANAL (2026-09-13)

**Medido esa madrugada, tres órdenes seguidas:** el programa del ayudante **corta la tarea en seco**
en cuanto una herramienta pide tocar una carpeta que no es la suya (`external_directory ...
auto-rejecting`). Se murieron así: crear una carpeta temporal, leer `arnes/canal.py` de la
herramienta desde el negocio, y leer los registros de Claude. **No avisa: la tarea termina "bien"
y sin informe.**

- La orden **solo nombra rutas dentro de la carpeta desde donde se lanza.**
- **El informe va en su respuesta final**, no en un archivo ni por el canal. La dirección recoge la
  salida entera del lanzamiento.
- Si un dato vive en otra carpeta, **es otra orden, lanzada desde esa carpeta** (ley 5).

## 10 · UN SOLO MANDO, EL PLAN LO APRUEBA JULIO, Y LO QUE DICES SE COMPRUEBA (2026-09-13)

- **Las reparaciones de un plan solo se ejecutan con la aprobación de Julio.** Diagnosticar y medir,
  sí; reparar lo del plan antes de que Julio lo apruebe, no.
- **Nunca tocas la herramienta** (`C:\Ingeniero_VUC`): es carril de la dirección con el equipo.
- **Si te llega una orden por otra ventana, dejas recado antes de tocar nada.** Dos mandos sobre el
  mismo archivo se pisan: pasó con `cuerpo/privacidad.py`.
- **Tu informe se comprueba en el disco.** Si dices "reparado", tiene que estar en el archivo: ese
  día se dijo "reparado" y el archivo tenía otra cosa.
- Detalle: `CONTRATO_EL_AYUDANTE_DE_LA_CARGA_PESADA.md`, "EL CICLO DEL PLAN".

## 8 · NO SE USA LA FORMA ANTIGUA DE MANDAR LA SALIDA A LA NADA

Crea un archivo con nombre reservado que llegó a tumbar el mapa entero de la casa.
