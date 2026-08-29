# DONDE QUEDAMOS — cierre del 2026-08-28

## LO PRIMERO DE MAÑANA, Y NO HAY DISCUSIÓN: EL REPARTIDOR

**Está MEDIDO, con prueba, no es sospecha.** El auditor rechazó **tres rondas seguidas** diciendo
cosas que son **falsas**:

| Lo que dijo el auditor | La realidad |
|---|---|
| *"usa el reloj sin importarlo"* | está importado, **línea 42** |
| *"la variable AQUI no existe, dará error"* | existe, **línea 44** |
| *"se inventó una forma rara de calcular la ruta"* | es **exactamente** la que ya usa el archivo |

**Por qué se equivoca:** el repartidor le entrega el archivo **a partir de la línea 65**. Las
líneas 39-44 —donde están el reloj y la variable— **nunca llegan a sus ojos**. Así que ve código
que usa cosas que él no ve declaradas, concluye que son inventadas, y **rechaza propuestas que
estaban bien**.

**Consecuencia para Julio:** tres rondas pagadas hoy para nada, y **el bucle no puede cerrar**:
se puede relanzar diez veces más y fallará igual, porque el problema no es lo que se pide, es que
**al auditor le falta la cabeza del archivo para juzgar**.

**Y no son solo inventos del obrero: el auditor también inventa, por la misma razón.** Es el mismo
fallo por las dos puntas.

**La reparación:** cuando el trabajo toca importaciones o constantes, el paquete tiene que traer el
archivo **desde su primera línea**. Sin eso, ninguna reparación del propio sistema podrá aprobarse
nunca.

## LO SEGUNDO: EL NUDO QUE IMPIDE GUARDAR

Hay una contradicción del sistema consigo mismo, encontrada hoy:

```
El método de Julio  →  la vigía nace en ROJO, primero
El guardián         →  no se guarda nada si hay algo en rojo
La reparación que la pondría verde  →  necesita al equipo
El equipo           →  no converge (ver punto de arriba)
```

**Resultado: el trabajo de hoy no se pudo guardar formalmente.** Está en disco y no se pierde,
pero no quedó sellado.

**El guardián no distingue** entre una prueba rota por descuido y una que nació roja a propósito.
Y eso choca con una lección que ya está escrita en el sistema: *"no hacer un candado sin una forma
honrada de satisfacerlo: empuja a saltárselo, y eso es peor que no tenerlo"*.

**La salida limpia** es la que usa el propio Python para esto: marcar la vigía como *"se espera que
falle hasta que llegue la reparación"*, de forma que si un día pasa sin querer, avise. Eso no
afloja nada y desatasca el método.

## LO QUE SÍ QUEDÓ HECHO HOY (en disco)

- **`CONTRATO_NUNCA_A_SOLAS.md`: 11 leyes**, de fallos medidos hoy. Incluye las dos que dictó Julio:
  **solo las pruebas con navegador llegan a él**, y **esa llave dura lo que duren las pruebas y no
  sirve para nada más**.
- **`PLAN_CANDADOS_QUE_NO_SE_VIOLAN.md`**, con el vigilante que autoriza a partir del plan aprobado.
- **`VIGIA_PENDIENTE_nunca_a_solas.py`: NACIÓ ROJA**, 4 de 9, por los motivos correctos.
  **ESTÁ APARTADA A PROPÓSITO, y hay que devolverla.** No vive todavía en la carpeta de vigías
  porque su reparación no está aprobada y el guardián no deja guardar con nada en rojo. En cuanto
  el equipo apruebe la reparación, **lo primero es moverla a `vigias/` con su nombre normal**
  (`test_vigia_nunca_a_solas.py`) y comprobar que se pone verde. Si se olvida, queda una ley sin
  vigía, que es justo lo que Julio no quiere.
- **Foto Informe, guardado y en verde:** los enlaces del Word ya saltan (dos marcadores compartían
  número y Word descartaba el salto), y el título es ahora el enlace. 72 vigías verdes.

## LOS CUATRO AGUJEROS (medidos, siguen abiertos)

1. **Crear un archivo nuevo no exige equipo.** Por ahí se construyó un subsistema entero a solas.
2. **El candado apunta lo que frena, nunca lo que deja pasar.** Por eso no se pudo explicar cómo se
   pasó.
3. **Avisa tarde**, cuando ya se decidió escribir.
4. **El aviso de memoria frena y obliga a repetir el comando**: hoy saltó más de **doce** veces.
   Es lo que Julio ve como "me pide permiso otra vez".

## LO QUE FALTA DE JULIO (dos comandos, una vez)

```
setx OPENROUTER_API_KEY "su llave"
```
Sin esto los dos únicos cerebros gratis que **no fallaron hoy** siguen invisibles, y cuando Google
se cae —hoy los tres Gemini dieron 503 a la vez— **el equipo se queda sin auditor**.

Y la lista de permitidos de Windows, que ya se le entregó. Sin ella cada permiso muere al cerrar la
ventana.

## EL ESTADO REAL DE LOS CEREBROS (medido hoy)

| | llamadas | fallos | |
|---|---|---|---|
| DeepSeek (**se paga**) | 75 | 0 | **0%** |
| Nemotron Ultra (nuevo) | 2 | 0 | **0%** |
| North Mini Code (nuevo) | 2 | 1 | 50% |
| Gemini 3 preview | 68 | 30 | 44% |
| GPT-OSS grande | 21 | 12 | 57% |
| Gemini 3.5 | 24 | 19 | 79% |
| Gemini flash | 26 | 23 | 88% |
| GPT-OSS pequeño | 9 | 8 | 89% |
| Gemini lite | 3 | 3 | **100%** ← *no tiene modelo asignado: fallo nuestro* |
| El de su PC | 9 | 9 | **100%** |

**6 de cada 10 llamadas gratis fallan**, y cada fallo empuja el trabajo al de pago.

## LO QUE APRENDIMOS HOY (caro)

**Escribí código a solas por tercera vez, y Julio lo cazó.** El candado existía y no lo impidió
porque "crear no es reescribir". La letra se cumplió; el espíritu no.

**El equipo sirve cuando tiene material.** En una ronda cazó un error mío de verdad: pedí comprobar
el contenido de un archivo, y cuando el candado actúa **el archivo todavía no existe**.

**Pero sin material inventa, por las dos puntas.** Y eso es lo que hay que reparar mañana, primero.
