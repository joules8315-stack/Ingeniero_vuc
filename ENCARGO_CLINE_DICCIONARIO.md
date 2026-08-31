# ENCARGO PARA CLINE — 2026-08-31 — EL DICCIONARIO ENVENENADO

Lo manda Julio: **no es a elegir, es tu tarea.** Claude coge otra y no toca la tuya.

## LO QUE YA ESTA HECHO Y EN VERDE (no lo repitas, no lo toques)

- `cerebro/piezas.py::funcion_completa(ruta, nombre)` — la pieza se busca **por su nombre** y
  llega entera, con su sitio real. Aprobada por el equipo.
- `cerebro/router.py` — el repartidor ya la usa: fuera los dos numeros escritos a mano.
- `CONTRATO_SE_BUSCA_POR_NOMBRE.md` — la ley.
- `arnes/candado_por_nombre.py` + `vigias/test_vigia_se_busca_por_nombre.py` — 10 en verde.

## DOS DATOS TUYOS QUE COMPROBE Y SON FALSOS

1. **"Falta poner la llave de OpenRouter"** → **ya esta puesta**. Verificado en el archivo de
   llaves privado. Si arrancas por ahi, pierdes una vuelta.
2. **"gemini2 tiene 100% de acierto"** → ese numero sale de una prueba de **marketing** de 4
   preguntas, no de revisar codigo. Hoy me rechazo **tres veces** diciendo que no veia un texto
   que si tenia delante; lo medi letra por letra en el papel que recibe.

## TU TAREA: EL DICCIONARIO ENVENENADO (esta medido, no supuesto)

`memoria/DICCIONARIO.json` tiene 6 entradas. **Una es basura**: archivo `a.py`, funcion `f`,
proyecto `p`. Lleva **535 apariciones y 27 formas distintas de decirlo**.

**Quien la mete:** `vigias/test_vigia_causa_cambio.py` y `vigias/test_vigia_decision_reparar.py`
llaman a `candado_diagnostico.declarar("p", "a.py", "f", "1", ...)`, y eso acaba escribiendo en la
memoria **de verdad**. Cada corrida de las vigias la engorda un poco mas.

**Por que hace dano:** en `arnes/diccionario.py` basta **una** palabra en comun para casar
(`MINIMO_PALABRAS_COMPARTIDAS = 1`). Con 27 formas de decirlo dentro, esa entrada falsa casa con
casi cualquier problema y **gana**, asi que el repartidor recibe un archivo que no existe. Por eso
"usa el diccionario" nunca funciono.

### LO QUE HAY QUE CONSEGUIR

1. `aprender()` **no guarda** un sitio cuyo archivo no exista de verdad en el disco. Su propio
   texto ya lo promete ("sin sitio probado no se guarda nada") pero **no lo comprueba**.
2. **Tope a las formas de decirlo**: un sitio que dice haberse aprendido de 500 maneras es un
   iman, no un sitio. Se queda con las ultimas y se descarta el resto.
3. Las **vigias dejan de escribir** en la memoria de verdad.
4. **Limpiar** el veneno que ya hay.

### METODO (no se negocia)

- La vigia **primero**, y que **nazca roja**. Despues reparas. **No se guarda hasta verde.**
- **Con el equipo**, sin saltar candados.
- Un paso a la vez. Nada queda "pendiente".

## DOS COSAS QUE APRENDI HOY Y TE AHORRAN VUELTAS

1. **Antes de mandar un encargo, comprueba que el texto que hay que tocar le llega de verdad al
   equipo.** Varias vueltas murieron por pedirle que aprobara lo que no podia ver: de un archivo
   de 116 renglones le llegaban 40, y de 6 piezas solo 2 enteras.
2. **Si no llega, mete el pedazo de codigo DENTRO del encargo.** Con eso aprobo a la primera,
   despues de ocho rechazos.

## CONTESTA POR EL CANAL

Para que Julio vea con sus ojos que el canal funciona:

```
cd C:\Ingeniero_VUC; python -c "import sys;sys.path.insert(0,'arnes');import canal;canal.enviar('claude','cojo el diccionario', de='cline')"
```
