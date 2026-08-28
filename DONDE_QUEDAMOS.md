# DONDE QUEDAMOS — cierre del 2026-08-27 (tarde)

## LO PRIMERO DE MAÑANA

**0. QUITAR LOS AVISOS QUE FASTIDIAN A JULIO.** Su `settings.json` no tiene lista de PERMITIDOS
(solo `deny`), así que cada comando le pide confirmación y los permisos que da mueren al cerrar la
ventana. **Claude NO puede arreglarlo**: las líneas 8-9 de ese archivo le prohíben editarlo, y esa
regla se respeta. El comando ya está redactado y entregado a Julio (hace respaldo, añade `allow`
solo para leer / correr pruebas / guardar, y comprueba que el archivo quede válido). **Sin esto no
se puede trabajar seguido.**

**1. EL BOTÓN DE LOS TÍTULOS — falta UNA cosa y está medida.**
```
SI  -> 21 de 21 titulos en la tabla de trabajo   CORRECTO
NO  -> 16 de 21 siguen saliendo                  FALLA
```
El cambio hecho quita 5. Los otros **16 salen por otro camino que aún no se ha encontrado**.
La prueba ya está preparada para decir **en qué columna** están (se añadió el desglose por columna),
pero **esa corrida quedó sin ejecutar**. Es el siguiente comando:
```
cd "C:\Users\USER\dev\Foto_info_repo\Foto_informe--main"; python rv3_prueba_boton_titulos.py
```
**Julio pidió que esto se resuelva CON CLINE.** Preguntarle por dónde salen esos 16.

## LO QUE SE HIZO HOY (todo guardado salvo lo que se dice abajo)

- **LAS DOS LLAVES** (`CONTRATO_DOS_LLAVES.md`): se separó la llave de TRABAJO de la de CANDADOS.
  `rv3_portero.py` guarda la clave SOLO en memoria, la pide UNA vez por jornada y renueva el permiso
  solo. Se descubrió que la clave de Julio estaba GUARDADA en texto plano en las variables de usuario
  y el programa solo AVISABA; ahora PARA. El gate pasó de 1 h a 12 h (la comprobación del hash del
  código NO se tocó). 20 vigías verdes, comprobadas con sabotaje. **PROBADO EN VIVO: el portero
  funciona y entregó permisos reales.**
- **`getpass` mostraba la clave** aunque dijera que no (queja de Julio). Reemplazado por lectura con
  `msvcrt` que muestra asteriscos, y si NO puede ocultarla **PARA en vez de mentir**.
- **OpenRouter en el Ingeniero**: 8 -> 11 cerebros. Se cazó una trampa cerrada: un cerebro sin
  capacidad declarada entra con CERO y `rankear` lo salta SIEMPRE, así que nunca mide y queda de
  adorno. Vigía nueva para eso y otra que impide colar un modelo de pago de OpenRouter.
- **LA ROTACIÓN DE CEREBROS en DMM** (`CONTRATO_ROTACION_DE_CEREBROS.md`): relevos de verdad —
  contesta uno, los demás ni se enteran. 437 vigías verdes.

## LO QUE NO ESTÁ GUARDADO EN GIT (está en disco, no se pierde)

`app.py` y `app_web.html` de Foto Informe llevan el botón construido **sin commitear**: el gate exige
un ensayo integral fresco y no se corrió. Para guardarlos:
```
cd "C:\Users\USER\dev\Foto_info_repo\Foto_informe--main"; python rv3_prueba_integral.py
```
(el portero debe estar encendido).

## LO QUE JULIO DEJÓ DICHO Y HAY QUE CUMPLIR

- **"Apóyate siempre en Cline."** Hoy el botón sí fue con equipo (3 rondas, 2 rechazos con razón),
  pero **el portero y los arreglos del medidor se hicieron SIN equipo**, porque su llave de candados
  estaba puesta y nada frenaba. Se le dijo. Mañana: con equipo.
- **"No más autorizaciones."** Ver punto 0.
- **DMM de principio a fin.** Se encontró el mapa (`MATRIZ_FALTANTES.md`, 24 piezas) y se midió el
  estado real con navegador: **10 de 15 pasan; /parrilla, /voz-branding, /anuncios y /contenido NO
  ABREN**, y el botón "Aprobar" no se puede pulsar. Julio dijo que la web "parece de niño de
  primaria". Hay 6 piezas que no necesitan ninguna llave suya: el grafo, indexar Foto Informe,
  preguntas-contra-ventas, color de marca, ciclo semanal y precios a las redes.

## LO QUE APRENDIMOS HOY (caro)

**Medir bien y concluir mal, otra vez — dos veces seguidas en el mismo asunto.**
 1. "16 títulos salen mal" -> se contaban TODAS las tablas juntas.
 2. Se separó por "tiene fotos" -> **también estaba mal**: la tabla de trabajo lleva fotos dentro,
    así que dio 0 títulos y 0 Anexos, algo que Julio ve con sus ojos que es falso.
 3. Lo correcto: identificar la tabla **por los encabezados que pegó Julio** (`work_headers`),
    que es como la identifica el propio programa. Ya está así.

**Una promesa que no se cumple es peor que no prometer.** Se le dijo a Julio "no se ve al teclear" y
sí se veía. Escribió su clave con la pantalla a la vista. De ahí la ley: si no se puede ocultar, se
PARA y se dice.
