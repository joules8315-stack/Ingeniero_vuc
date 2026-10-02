# MAÑANA SE SIGUE POR AQUÍ (guardado el 2026-08-20, noche)

> Julio: "guarda todo mañana seguimos". Esto es para no repetir nada de lo de hoy.

## LO PRIMERO AL VOLVER

```powershell
cd C:\Ingeniero_VUC; python ingeniero.py arranca
```

## LA TAREA: reparar el MVP (Foto Informe)

Julio pidió dos cosas **distintas** (no son el mismo problema, y confundirlas ya fue un fallo):

### 1) LA LENTITUD — diagnóstico TERMINADO, falta reparar

**Ya está medido y probado. No hay que volver a investigarlo.**

| Qué se midió | Resultado |
|---|---|
| El servidor en sí | **3 milisegundos** → el programa NO es lento |
| Abrir la pantalla de inicio | medio segundo, 2 peticiones |
| Intentar entrar | 2 centésimas (ni llega a la nube) |
| Cada viaje a la nube | **~550 ms** (medido el 2026-07-10) |

**Viajes seguidos por acción** (contados por `.execute()` en `app.py`):
| Acción | Viajes | Espera |
|---|---|---|
| Crear informe (`app.py:13616`) | 4 | ~2,2 s |
| Añadir diario (`app.py:14282`) | 3 | ~1,7 s |
| Subir foto (`app.py:14705`) | 3 | ~1,7 s |
| Asignar (`app.py:14919`) | 2 | ~1,1 s |
| Generar informe (`app.py:16427`) | 2 | ~1,1 s |

Y la pantalla llama al servidor **desde 50 sitios**, 16 de ellos a `/reports/`.

**CAUSA RAÍZ:** no es el código, es el **número de idas y vueltas seguidas** a la nube.
**CURA PENDIENTE:** agrupar los viajes de cada acción en vez de hacerlos uno detrás de otro.

**FALTA MEDIR** (y es lo único que bloquea): guardar, asignar y generar **desde dentro**.
Para eso Julio tiene que añadir a `C:\Users\USER\dev\Foto_info_repo\Foto_informe--main\.env`:
```
FOTO_INFORME_TEST_EMAIL=<un correo que ya funcione>
FOTO_INFORME_TEST_PASSWORD=<su contraseña>
```
(Las de `CREDENCIALES_MVP.txt` **no valen**: dan "no autorizado".)
La herramienta ya está hecha: `C:\Ingeniero_VUC\skills\medir_acciones.py`.

### 2) EL MODO SIN INTERNET — diagnóstico TERMINADO, falta reparar

**2.1 — El círculo vicioso (probado en el código Y en pantalla):**
- `app_web.html:376` exige tener el **complemento** descargado para entrar sin internet.
- El complemento solo se descarga **dentro** del MVP → hace falta login → hace falta internet.
- **Comprobado con navegador:** en la pantalla de inicio solo hay "Entrar" y "Vigía interno".
  De modo sin internet **no hay nada, ni escondido**.
- **"El complemento" es el término del propio contrato de Julio** (`OBJETIVO_MVP.md:2975`), y el
  fallo ya estaba descrito en la línea 2983: *"al abrir sin red el celular se quedaba llamando a
  Render en vez de abrir offline"*.
- **CURA:** botón de modo sin internet **en la pantalla de inicio**.

**Las DOS aplicaciones instaladas:** el manifiesto (`app.py:10216`) **no tiene campo `id`** y su
dirección de arranque es `/` (el MVP con login). Según la documentación de Chrome, sin `id` el
navegador identifica la app por esa dirección y **crea una segunda instalación fantasma**.
**CURA:** añadir `id` fijo al manifiesto.

**2.2 — Las fotos se descargan solas.** SIN INVESTIGAR TODAVÍA.

**2.3 — "Dice que está completo".** NO es falta de memoria: es un tope de **4 fotos por informe**
(`offline.html:79`, `MAX_FOTOS = 4`, mensaje *"Máximo 4 fotos por informe"*).
El contrato dice "máximo 4 fotos por registro" (`OBJETIVO_MVP.md:802`), ligado a la maqueta del
documento final (alineación de 1, 2, 3 o 4 fotos por hoja).
**Julio ordenó: en el modo sin internet el tope debe ser la memoria del celular, no un número.**
Hay que legislar ese cambio antes de tocarlo, porque choca con el contrato de la parte online.

## ESTADO DEL INGENIERO

- **125 comprobaciones en verde**, todo sellado en su rama.
- **28 fallos aprendidos**, con su "no volver a hacer".
- **16 cerrojos activos**. Hoy me frenaron de verdad: el de lectura, el de edición, el de vía
  canónica y el de "confirmar el objetivo antes de construir".
- El protocolo único con sus 8 pasos: `python ingeniero.py ruta`

## LO QUE HICE MAL HOY (para no repetirlo)

1. Iba a **indexar sin saber dónde estaba lento** → ya hay cerrojo (paso 3, causa raíz).
2. Dije que **lentitud y modo sin internet eran el mismo problema**. No lo son.
3. Le pregunté a Julio **tres cosas que él ya había escrito** → ya hay cerrojo (paso 4).
4. Le hice creer que iba a **borrar el botón del Organizador de tareas**. No toqué nada.
5. Le hablé **con jerga** todo el día, estando prohibido por su protocolo → ya hay cerrojo.

## EL PROYECTO DE JULIO QUEDÓ INTACTO

Cero archivos suyos modificados. Las herramientas de medir se guardaron en
`C:\Ingeniero_VUC\skills\`. El servidor del MVP quedó apagado.
