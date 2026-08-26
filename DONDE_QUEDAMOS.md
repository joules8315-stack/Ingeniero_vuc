# DONDE QUEDAMOS — cierre del 2026-08-25

## LO PRIMERO DE MAÑANA: LA PRUEBA DE JULIO

Foto Informe esta **reparado, probado y GUARDADO**. El guardia del repo lo aprobo en verde
(replay verde sobre el codigo actual + vigia en el commit). Ya no falta nada de mi lado.

**Falta la ley 3: que Julio lo vea con sus ojos.** Hasta eso, nada se sella.

Las cinco cosas que Julio tiene que comprobar en su programa:

1. **Al abrir, que sus 25 informes esten ahi** sin tener que entrar a Revisar.
2. **Colocar unos pocos, dejar otros sueltos, y dar a Generar**: debe avisarle y, si acepta,
   salir SOLO con los que coloco.
3. **Borrar la colocacion de filas**, colocar dos o tres, y ver que los demas SIGUEN sueltos.
4. **Ordenar ascendente** y abrir el documento: el mas antiguo arriba. Descendente al reves.
5. **Escribir en las casillas** y ver que cada texto sale donde lo escribio.

Cuando lo confirme: `python ingeniero.py probado foto_informe "<lo que vio>"`.

---

## LO REPARADO EN FOTO INFORME (todo medido contra su cuenta real)

| Que le pasaba a Julio | Estado |
|---|---|
| Pulsaba Generar y no pasaba NADA si quedaba algun informe sin colocar | Reparado. Sale la ventana, acepta, y genera. |
| El informe final salia con los 25 aunque hubiera escogido 19 | Reparado. Salen los 19; los sueltos quedan fuera y se borran igual al descargar. |
| Borraba la colocacion de filas y se le deshacia sola | Reparado. Medido: base 0 y pantalla 0. |
| Abria el programa y la lista salia VACIA (parecia que se perdieron) | Reparado. Vuelven solos. |
| Reemplazar la plantilla no hacia nada | Reparado por Cline (el cuaderno servia el camino viejo). |

**Dos leyes dictadas por Julio y escritas**, con su vigia:
`CONTRATO_ORDENAR_FILAS.md` y `CONTRATO_BORRAR_ASIGNACION_FILAS.md`.

---

## LA SERIE METODICA DE PRUEBAS (lo que pidio el 2026-08-25)

Cuatro verdes, siguiendo el plan que ya trae el mapa del MVP (seccion 6):

- **El documento corresponde con lo colocado** — sus 19 informes, cada uno EN SU CASILLA, con su
  objetivo, su nombre y las 49 fotos. Mira celda por celda, no busca en todo el texto.
- **El documento respeta ascendente y descendente** — las dos direcciones.
- **La escritura manual llega a su casilla** — las 8 filas.
- **Borrar un rol** — se borra, se ve, aguanta recargar y no toca a los otros tres.

---

## LO QUE FALTA (por orden)

1. **EL CAPSTONE: descargar de verdad -> borrado real.** NO se corre sin permiso explicito de
   Julio. El mapa es tajante: la prueba crea su PROPIO juego de datos, y los 11 informes reales
   de Julio se usan como fotos de entrada, **nunca como blanco del borrado**.
2. **La matriz exhaustiva de roles** (escenario 3 del mapa). Lo que ya existe cubre borrar y
   cambiar de columna; falta cada rol contra cada columna.
3. **La prueba de las 10 vueltas de Cline** sigue sin sus tres arreglos (escribir el texto
   tecleando y esperando la rehidratacion, pulsar de verdad el boton de borrar, y que las
   comprobaciones puedan fallar). Ya se le recordo por el canal.

---

## DOS AVISOS QUE NO HAY QUE PERDER

**Una alarma grita en falso.** `rv3_prueba_4_roles.py` dice que borrar el rol de evidencia no
borra, y es mentira: usa un cero creyendo que borra y el programa lo convierte en 1, o sea que
mueve. Ya estaba investigado y escrito, pero la prueba vieja sigue gritando. Una alarma que suena
sin motivo ensena a ignorarla, y el dia que suene de verdad nadie mirara.

**La pantalla de Revisar a veces no carga.** Mas de dos minutos, o nunca. No siempre. Corto tres
corridas. Si le pasa a Julio, es de las cosas que mas rabia dan.

---

## LO REPARADO EN EL PROPIO INGENIERO

- **Los avisos ya no tapian.** La primera vez frenan y ensenan la leccion; si se insiste con la
  misma accion, pasa. Antes un aviso dejaba tapiado el protocolo entero.
- **El paso de las alarmas ya se puede cumplir** en proyectos que no las tienen en carpeta.
- **La llave del equipo abre lo que el equipo tuvo delante** (buscaba las piezas con un nombre
  que el paquete no usa: abria 1 archivo inutil, ahora 28).
- **El mando ya no se muere por un caracter** que la consola no sabe dibujar, y **guarda antes de
  ensenar**: un caracter invisible costaba la llamada entera al equipo.
- **El repartidor ya no se devuelve a si mismo**: las pruebas que citan el problema de Julio ya no
  tapan al codigo.
- **Nueva ley**: a quien no le cupo, no se le vuelve a pedir lo mismo
  (`CONTRATO_EQUIPO_QUE_AGUANTA.md`), con su vigia.

**HALLAZGO ABIERTO, apuntado y visible**: en Foto Informe el repartidor no llega del problema en
palabras de Julio al codigo, porque el codigo esta en ingles y comprimido y nunca se parecen.
Marcado como pendiente conocido: el dia que se arregle, la vigia avisa.

---

---

## AGREGADO AL CIERRE (2026-08-25, tarde) — CAPACIDAD, PRECISION y el modelo local

**Capacidad real medida** (`memoria/CAPACIDADES.json`): la cuota GRATIS de Groq es **8.000 tokens/min
y 200.000/día POR MODELO** (doc oficial de Groq, confirmado en vivo). Los de Groq (groq/groq20b/qwen)
aguantan ~8.000 letras por tarea y luego la cuota los frena. gemini2 (3-flash-preview) ~16.000 letras
(el más capaz gratis hoy). gemini (3.5) agotado hoy; gemini3 inestable; deepseek >=80.000 (pago, sin cuota).

**Precisión real EN TERRENO** (`arnes/medir_precision.py`, `memoria/PRECISION.json`): tarea de análisis
de campañas con los datos reales de SolarDemo, 4 comprobaciones objetivas (usa_datos, detecta_problema,
canales_marca, medible). Sirven (4/4): groq20b, qwen, gemini2, deepseek; groq 3/4 (no detectó las 0 ventas).
A descansar para análisis: gemini (agotado), gemini3 (inestable), local (1.5b, alucina). Regla: se asigna
por capacidad + precisión, y CADA tarea va con su vigía que la verifica (la vigía es la que los hace
precisos). Vigía: `test_vigia_precision.py`.

**El modelo local**: se descargó Qwen2.5-7B-Instruct (4.4 GB, listo en LM Studio) para que sea el cerebro
local de análisis, pero **NO carga en 8 GB de RAM** (el motor se cae por falta de memoria: exitCode 322).
Necesita 16 GB. El 1.5B queda de red de seguridad. Opción para hoy con 8 GB: bajar un 3B/4B que sí cabe.

**Fallo 45 (la señal de Claude)**: confirmado que la señal mira el comando y no el proyecto; Claude lo va
a arreglar (legislar -> alarma primero -> reparar); yo superviso.

**MAÑANA (por orden):**
1. Probar un 3B/4B local (si Julio lo quiere) con `python arnes/medir_precision.py local`.
2. Revisar lo de Claude (fallo 45) cuando avise.
3. Re-medir Gemini cuando su cuota se refresque.
4. Opcional: subir a 16 GB de RAM y activar el 7B.

---

**Estado de la cuenta de Julio al cerrar:** 25 informes diarios, 19 colocados, 6 sueltos,
68 fotos. Igual que como se encontro.
