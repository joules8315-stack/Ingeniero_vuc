# DONDE QUEDAMOS — cierre del 2026-08-24

> Esto es lo PRIMERO que hay que leer al volver. Julio no tiene que contar nada otra vez.

---

## LO PRIMERO AL VOLVER

**1. Encender Foto Informe** (si no esta ya):
```powershell
cd "C:\Users\USER\dev\Foto_info_repo\Foto_informe--main"; .\.venv\Scripts\python.exe run_backend.py
```
Se comprueba abriendo `http://127.0.0.1:8000/` — tiene que responder.

**2. La base de Supabase se DUERME sola.** Si el MVP dice "no autorizado" al entrar, no es la
clave: es que el proyecto de Supabase esta pausado. Julio entra y le da a reanudar. Costo media
hora descubrirlo el 2026-08-24.

**3. Las credenciales de prueba ya estan guardadas** en las variables de usuario de Windows
(`FOTO_INFORME_TEST_EMAIL`, `FOTO_INFORME_TEST_PASSWORD`, `FOTO_INFORME_TEST_BEARER`).
Julio pidio **dejarlas hasta terminar las pruebas**. Al acabar, se le ofrece borrarlas: su
propia regla dice "nada de larga vida".
El pase (`BEARER`) caduca; se renueva entrando con correo y clave y guardando el nuevo.

**4. El siguiente paso tecnico:** desatascar el guardado de la reparacion de velocidad.

---

## FOTO INFORME — reparacion de velocidad: HECHA y PROBADA, pero SIN GUARDAR

### Lo que quedo reparado (4 fugas)
1. Al guardar ya no se borra la libreta entera: se olvida **solo lo que ese guardado toca**.
2. El reloj corre **solo en la pantalla 4 (fotos), cada 5 segundos**. En las demas, cero.
3. Con la ventana escondida no llama. Al volver, revive solo si estas en la 4.
4. Leer espera **10 segundos**; guardar (25), subir (60) y generar (120) **intactos**.

### Probado de verdad, con navegador
| | Pantalla vieja | Reparada |
|---|---|---|
| Quieto en el menu | 1 llamada | **0** |
| Pantalla de fotos | 2 en 20 s | **4** (una cada 5) |
| Ventana escondida | 0 | **0** |
| Al guardar | borra la libreta entera | **olvida solo lo tocado** |
| Resultado | **ROJO, 3 fallos** | **VERDE** |

La misma prueba, sin tocarla, contra las dos versiones. **Con la vieja se pone roja**: eso
demuestra que no es autovalidacion.

**La prueba con navegador CAZO UN FALLO GRAVE** que la de texto no vio: en la pantalla de fotos
se hacian 0 llamadas, o sea que las fotos del celular NO habrian aparecido en el computador.
Se reparo (nadie encendia el reloj al ENTRAR en la 4) y quedo verde.

### POR QUE NO ESTA GUARDADO
El guardian del propio proyecto lo rechaza: exige una **prueba integral verde reciente** y la
ultima es de hace un mes. Hace bien su trabajo. Para desatascarlo hay que hacer que la cadena de
pruebas 8 → 9 termine.

### TODO A SALVO en `memoria/rescate/`
- `foto_informe_velocidad_2026-08-24.patch` — el cambio entero, se puede volver a aplicar
- `app_web_reparada_2026-08-24.html` — la pantalla ya reparada
- `rv3_prueba_real_velocidad.py` — la prueba con navegador que mide las llamadas
- `test_vigia_solo_las_llamadas_necesarias.py` — la vigia de texto
- `rv3_prueba_8_reporte_2026-08-24.json` — los hallazgos de la prueba 8

---

## LO QUE PREGUNTO JULIO: al borrar asignaciones, ¿queda algun registro?

**SI, y esta MEDIDO** (prueba 8, corrida el 2026-08-24):

- **"Hay texto manual atado a un informe que no existe"** — **2 casos**. Se borra un informe
  diario y su texto escrito a mano se queda colgado. Nadie lo ve, nadie lo limpia.
- **Los textos no cuadran con su fila.** La prueba escribio "Fila 3 · Julio" y la base tiene
  "Fila 6 · Prueba Real".
- **Lo que bloquea todo:** la pantalla rechaza el guardado con
  *"Completa Nº Fila y Anexos/Evidencias/Otros para todos los grupos antes de guardar"*.
  Ese es el primer hilo del que tirar.

**La prueba 9 NO llego a correr**: exige que la 8 termine bien, y la 8 fallo con 11 hallazgos.

**OJO, error que ya se cometio:** al leer el estado de la cuenta, `/reports` devuelve **1** — ese
es el informe CONTENEDOR, y siempre hay uno solo por diseno. Los informes diarios van dentro y
son **25**. Se le dijo a Julio que se habian borrado 24 y era **falso**. Antes de alarmarle, se
mira `daily_entries_count`.

---

## EL TALLER — lo que se construyo hoy

**EL GUARDIA DE GUARDADO** (`arnes/guardia_de_guardado.py`), orden de Julio: *"que cline use el
candado, que no se pueda salir por ningun lado"*.
- **No lo ejecuta la IA: lo ejecuta git.** Da igual quien escriba.
- Pruebas rojas → no guarda. Archivo con llaves → no guarda. Cada frenada queda apuntada.
- **Probado saboteandolo**: cazo unas rojas de verdad y cazo un archivo de llaves colado a mano.
- Instalado en **los tres proyectos** (antes solo Foto Informe tenia algo asi).
- **Unica salida:** `--no-verify`, que es de git y no se puede quitar. Se nota porque no aparece
  el apunte en la libreta.

**REGLAS DE CLINE** (`.clinerules/modo_ingeniero.md`) en los tres proyectos.

**CONTRATO DE CREDENCIALES PARA PRUEBAS** — como se piden sin que Julio sufra: se le ABRE la
ventana y se le dicen dos lineas. Nunca un bloque de ordenes largo.

---

## REVISION DEL TRABAJO DE CLINE EN DMM (2026-08-24)

**Bien:** las 7 piezas nuevas tienen vigia (4 a 7 pruebas cada una), y **las vigias sirven**
(al romper una pieza a proposito, 5 de 7 se pusieron rojas). **No duplica**: sigue un contrato
con tareas numeradas y hacen cosas distintas de sus hermanas.

**Mal:** **5 de las 7 piezas no las usa nadie** — existen, estan probadas y no estan conectadas
a nada, asi que Julio no ve ningun resultado. Y deja el proyecto en rojo mientras trabaja: cada
pieza nueva rompia dos comprobaciones del mapa (hubo que recompilarlo 5 veces).

**No ha visto:** que una pieza sin conectar no vale nada todavia; que hay que recompilar el mapa
en el mismo momento de crearla; y que hay otro trabajando a la vez y sus rojas bloquean al otro.

---

## PENDIENTE, DECISION DE JULIO

1. **Las credenciales estan en el historial del repositorio de Foto Informe y subidas.** El
   proyecto parece privado. **La clave de ese archivo esta MUERTA** (comprobado: el servidor la
   rechaza), asi que el riesgo real es bajo. Sacarla del historial es delicado. Sin tocar.
2. **Los 10 segundos de espera al leer no se han probado con conexion lenta de celular.** Es el
   mejor aviso que dio Cline y sigue sin medir.
3. **La pantalla de Foto Informe es un solo archivo enorme** (598.377 letras). Partirla es un
   proyecto en si.

---

## LO QUE JULIO YA DIJO Y NO SE OLVIDA

- "el equipo que haga siempre lo pesado deepseek, no lo olvides nunca" — **es ley del codigo**
- "repara usando tu equipo, ellos reparan, tu vigilas, no seas tonto"
- "el siguiente paso siempre es que realices pruebas con playwright" — **antes** de pedirle a el
- "siempre protegiendo contrasena" — nunca se pide ni se escribe una clave por el chat
- "no inventes ni mierda, solo via oficial"
- Trabaja **mixto**: fotos desde el celular, informe desde el computador, a la vez
- **No es tecnico.** Nada de jerga, nada de nombres de archivo, nada de bloques largos de
  ordenes. Se le ABRE lo que necesite y se le dicen dos lineas.
