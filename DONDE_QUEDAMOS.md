# DONDE QUEDAMOS — cierre del 2026-08-26

## LO PRIMERO DE MAÑANA

**1. Hay UNA prueba en rojo en Foto Informe, y no es de las nuestras.** El guardia del repo corre
una tanda de 92 y ve 1 roja; las 37 comprobaciones nuestras estan VERDES, y las otras 42 que se
probaron a mano tambien. Esta en el resto del proyecto (probablemente `test_table_search_unit` o
`test_template_session_family`). Por eso quedo sin guardar un archivo de RESULTADOS (no codigo).
Hay que encontrarla y decidir: ¿venia roja de antes, o la rompio alguien hoy?

**2. Julio tiene que contestar UNA pregunta** para poder reparar lo del Word sellado (abajo).

---

## LO QUE JULIO PREGUNTO Y LO QUE SE MIDIO (2026-08-26)

| Su pregunta | Respuesta MEDIDA |
|---|---|
| ¿Puedo poner cualquier orden y va a su casilla? | **Si.** Medido con navegador: fila 5 -> orden 2. Fila y orden son distintos, como manda el contrato. |
| ¿Reparte equitativo si hay mas informes que casillas? | **Si.** 25 informes en 10 filas: 5 filas de 3 y 5 de 2, ascendente y descendente, y el Word lo respeta. |
| ¿Varios en una casilla comparten orden? | **Si.** Los dos que fueron a la fila 5 comparten el orden 2. |
| ¿Si escojo pocos, solo esos salen? | **Si.** 19 escogidos de 25: el Word salio con 19 y los 6 sueltos fuera. |
| ¿Las fotos al final, con su nombre? | **Si, y Julio tenia razon.** El nombre va en el ENCABEZADO de cada bloque: "Evidencia 2 \| Pruebas 360", "Julio 1 \| prueba de fotos rapidas". 15 de 21 con etiqueta; los otros 6 llevan nombre PROPIO (Julio, Karen), que es la ley L22. |
| ¿Existe el boton de los titulos? | **NO. Hay que construirlo.** |
| ¿Se puede editar el Word? | **En el archivo, SI**: 0 controles de contenido, 0 bloqueos, 0 proteccion, y los 31 textos de Julio FUERA de cualquier caja. Pero el dice que no puede. Falta su dato. |

**COMO FUNCIONA EL ORDEN (confirmado por Julio):** el no escribe un numero. Escribe la FILA, y el
MVP pone el orden segun la SECUENCIA de colocacion; si la fila ya tiene otro informe, reutiliza su
orden. Julio: "es asi como esta en los contratos, parece que ya funciona asi".

---

## LO QUE FALTA

**A. EL BOTON DE LOS TITULOS** — hay que legislarlo y construirlo. Julio lo dicto con sus palabras:
  · Va en la pagina donde se configuran las 4 columnas.
  · Texto literal: **"¿Quieres que los Titulos se guarden dentro de la tabla?  SI    No"**
  · Hoy funciona como el "SI". El "No" es lo nuevo.

**B. EL WORD SELLADO** — el archivo dice que TODO es editable, y Julio dice que no puede.
La pregunta que falta, y solo el la puede contestar: al intentar cambiar lo que escribio la
aplicacion, **¿que pasa exactamente?**
  · ¿Sale una barra amarilla de "Vista protegida / Habilitar edicion"? -> es Windows con los
    archivos bajados de internet, no el programa.
  · ¿Deja escribir pero se pierde al regenerar? -> no esta sellado: se reescribe encima.
  · ¿No deja ni seleccionar, como si fuera imagen? -> esa parte no es texto, es foto.
Son tres causas y tres reparaciones distintas. Sin su respuesta seria adivinar.

**C. LOS ENLACES QUE NO SALTAN** — el documento tiene 35 marcadores y 25 enlaces internos, pero
Julio dice que en NINGUNO de sus informes funcionan ("ni siquiera alumbran"). Medir por que.

**D. UN INFORME COLOCADO QUE NO SE GUARDO** — en la prueba del orden, "Montaje terminado" se
coloco en la fila 2 y quedo en fila 0. Los otros dos (a la fila 5) si se guardaron. Sin aviso.
**Aislar antes de acusar**: puede ser la prueba o puede ser el MVP.

**E. EL CAPSTONE (borrado real)** — sigue esperando permiso explicito de Julio.

---

## LOS SEIS FLUJOS QUE SIGUEN SIN PROBAR (de los 13 del mapa)

Entrar y ruteo · fuente unica de verdad · **crear informes y tomar fotos** · **marca de agua** ·
modo sin internet · dictado por voz.

Los dos en negrita son los que Julio usa a diario.

---

## LO QUE APRENDIMOS HOY (y duele)

**TRES medidas mias fueron correctas y sus interpretaciones equivocadas.** El patron es siempre el
mismo: el numero esta bien, la conclusion no.

  1. "111 celdas centradas" -> iba a decir que el fallo historico del alineado seguia vivo y a
     tocar el motor del Word. FALSO: lo centrado eran las fotos (correcto) y las etiquetas de la
     plantilla. Los 24 objetivos y los 7 textos de Julio salen ARRIBA.
  2. "los 22 informes de Julio estan mal" -> con el criterio afinado, 11 salen limpios y el resto
     tiene 1 o 2 celdas, que pueden ser legitimas.
  3. "el nombre no aparece junto a la foto" -> SI aparece. Mire dos veces en el sitio equivocado.

**Las tres las corto Julio preguntando**, no un candado. Sigue sin haber nada que vigile si una
explicacion se sostiene. La pregunta de criterio (¿que cambio? ¿cuantos de cuantos?) es el primer
paso, pero no cubre "mediste bien y concluiste mal".

**Y su otra correccion, aceptada:** las pruebas de CONDUCTA van con navegador o son
autovalidacion. Mirar dentro del Word si es abrir el archivo — ahi no hay navegador que valga —
pero leer la base por atajo para juzgar conducta, no.

---

**Estado de la cuenta de Julio:** sus informes y fotos intactos; la colocacion, devuelta.
**Vigias:** Ingeniero 399 verdes · Foto Informe 37 verdes.
