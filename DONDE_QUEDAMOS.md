# DONDE QUEDAMOS — cierre del 2026-08-25

## LO PRIMERO DE MAÑANA

**1. Terminar de enganchar el contador de candados.** Esta conectado a UNO solo
(`candado_commit.py`) de unos quince. La cuenta sigue VACIA. Si se deja asi, la revision de los
8 dias que pidio Julio mirara una tabla de ceros y concluira que ningun candado sirve — lo
contrario de la verdad.

> Y una debilidad MIA que hay que corregir con eso: la vigia
> `test_vigia_candados_medicion.py::test_ALGUIEN_lo_llama` se conforma con que **uno** llame al
> contador. Deberia exigir que lo llamen los candados que de verdad frenan. Tal como esta, pasa
> en verde estando el trabajo a medias. Es exactamente el tipo de comprobacion floja que
> llevamos todo el dia cazando.

**2. La prueba de Julio en Foto Informe.** Esta reparado, probado y guardado; falta la ley 3: que
lo vea con sus ojos. Las cinco cosas a comprobar estan abajo.

---

## FOTO INFORME — reparado, probado y GUARDADO

El guardia del repo lo aprobo en verde (replay verde sobre el codigo actual + vigia).

| Que le pasaba a Julio | Estado |
|---|---|
| Pulsaba Generar y no pasaba NADA si quedaba algun informe sin colocar | Reparado |
| El informe final salia con los 25 aunque hubiera escogido 19 | Reparado: salen los 19 |
| Borraba la colocacion de filas y se le deshacia sola | Reparado |
| Abria el programa y la lista salia VACIA | Reparado |
| Reemplazar la plantilla no hacia nada | Reparado por Cline |

**Las cinco cosas que Julio tiene que comprobar con sus ojos:**

1. Al abrir, que sus 25 informes esten ahi sin entrar a Revisar.
2. Colocar unos pocos, dejar otros sueltos, dar a Generar: debe avisarle y salir SOLO con los que
   coloco.
3. Borrar la colocacion, colocar dos o tres, y ver que los demas SIGUEN sueltos.
4. Ordenar ascendente: el mas antiguo arriba. Descendente al reves.
5. Escribir en las casillas y ver que cada texto sale donde lo escribio.

Cuando lo confirme: `python ingeniero.py probado foto_informe "<lo que vio>"`.

**Pruebas nuevas, cuatro verdes:** el documento corresponde con lo colocado (celda por celda),
respeta ascendente y descendente, la escritura manual llega a su casilla, y borrar un rol
funciona.

**Falta de Foto Informe:** la matriz exhaustiva de roles, y el capstone del borrado real — ese
**no se corre sin permiso explicito de Julio**, y debe crear su PROPIO juego de datos: los
informes reales de Julio son fotos de entrada, nunca blanco del borrado.

---

## EL METODO — lo afinado hoy (lo que pidio Julio)

**1. La pregunta que ningun candado hacia** (la hizo Cline, dentro de `candado_diagnostico`).
Al declarar una causa hay que decir QUE CAMBIO entre las dos mediciones. Si nombra mas de una
cosa, avisa: *eso no es aislar, es una coincidencia*. **Ya cazo a Claude en caliente**, en la
primera causa que declaro despues de proponerla.

**2. El diccionario de las palabras de Julio al codigo** (`arnes/diccionario.py`).
Se cosecha SOLO de las causas declaradas, donde ya existen las dos mitades probadas. Probado en
vivo: se declaro la causa real del arranque y luego se pregunto con OTRAS palabras — contesto
`app_web.html`, `enterApp`, linea 2092.
**Su limite, dicho sin adornos:** no entiende el significado; encuentra si comparten al menos una
palabra que distinga. Lo que si hace es aprender la forma de hablar de Julio: cada descripcion
nueva del mismo sitio se suma. **No es el repartidor que pidio Julio: es el escalon anterior.**
**Falta (de Cline):** conectarlo al router con su vigia de uso. Sin eso es papel viejo — su
correccion, aceptada entera.

**3. El contador de candados** (Cline), con las DOS cuentas que decidio Julio: cazadas y frenadas
en falso. **Revision cada 8 dias, no cada mes.**

**4. Dos leyes nuevas:**
- `CONTRATO_DOS_TRABAJANDO.md` — nacio de un choque real: Claude y Cline construyeron la misma
  pieza a la vez. Quien propone **pregunta y ESPERA**; antes de crear se busca tambien lo que el
  otro acaba de hacer; al terminar se dice que quedo y donde; y el que descubre que su pieza
  sobra la retira el mismo (Claude retiro la suya).
- `CONTRATO_EQUIPO_QUE_AGUANTA.md` — a quien no le cupo, no se le vuelve a pedir lo mismo.

---

## LA CUENTA HONESTA DEL AVISO QUE MAS ESTORBA

El aviso de la memoria de fallos salto **unas veinte veces sin motivo** y se llevo cerca de un
tercio del dia. Pero cazo **tres cosas caras**:

1. La trampa que iba a borrar los textos manuales de Julio.
2. Que al contador de candados **no lo llamaba nadie** (habria hecho nacer muerta la revision de
   los 8 dias).
3. Que se estaba por reportar SIN_AUDITAR sin intentar con el cerebro de pago. Se repitio, y esa
   vez si hubo auditor.

**Ese es justo el dato que Julio va a mirar cada 8 dias**, y ahora existe. La señal esta mal
puesta (mira el nombre del comando, no el peligro) y eso se arregla; el candado en si vale.

---

## HALLAZGOS ABIERTOS, apuntados y visibles (ninguno apagado)

- El repartidor no llega del problema en palabras de Julio al codigo comprimido en ingles.
  Marcado como pendiente conocido: el dia que se arregle, la vigia avisa.
- `rv3_prueba_4_roles.py` **grita en falso**: dice que borrar el rol de evidencia no borra, y es
  mentira (usa un cero creyendo que borra, y el codigo lo convierte en 1: mueve). Ya estaba
  investigado y escrito, pero la prueba vieja sigue gritando. Una alarma que suena sin motivo
  ensena a ignorarlas todas.
- La pantalla de Revisar a veces tarda mas de 2 minutos en cargar la lista, y a veces no carga.
  Corto tres corridas.
- La prueba de las 10 vueltas de Cline sigue sin sus tres arreglos. Recordado por el canal.

---

**Estado de la cuenta de Julio:** 25 informes diarios, 19 colocados, 6 sueltos, 68 fotos.
Igual que como se encontro.

**Vigias:** Ingeniero 384 verdes · Foto Informe 37 verdes · Marketing 425 verdes.
