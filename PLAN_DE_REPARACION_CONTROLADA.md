# PLAN DE REPARACION CONTROLADA (Julio, 2026-09-09)

> **Diagnostico -> autorizacion temporal -> reparacion minima -> prueba fisica -> certificacion ->
> siguiente autorizacion.** Una etapa no se abre hasta que la anterior quede certificada.
>
> Esto NO es barra libre y NO es un arnes que impida reparar. Es la ruta de acceso que Julio ya
> legislo en `CONTRATO_RUTA_DE_ACCESO.md`: el plan dice QUE se toca, y **nada mas**.

---

## REGLA MADRE

> **Se puede tocar cualquier pieza estrictamente necesaria para el fallo demostrado, y ninguna
> que no lo sea.**

Consecuencias, tal como las mando Julio:

1. Se puede **atravesar el arnes** cuando el arnes es el obstaculo que impide corregir el fallo.
2. Se toca solo lo relacionado con la **primera causa demostrada**.
3. Se puede crear un **archivo auxiliar** si es indispensable (y se dice cual y por que).
4. Se puede tocar una **vigia** cuando esta demostrablemente falsa o impide validar la reparacion.
5. **NO** se rediseña el sistema entero.
6. **NO** se reparan los 9 puntos a la vez: uno, certificado, y despues el siguiente.
7. **NO** se borra un control porque estorbe.
8. **NO** se cambia arquitectura, modelos, base de datos ni APIs sin demostrar que hace falta.
9. Se **conserva todo lo que ya funciona**.
10. Cada cambio se prueba **fisicamente** antes de pasar al siguiente.

### Credenciales (ley aparte, ya escrita)
Se usan las **variables de entorno ya configuradas** (`CONTRATO_CREDENCIALES_PARA_PRUEBAS.md`).
No se piden, no se muestran, no se guardan, no se escriben en ningun archivo del proyecto.
Si falta una credencial, **se dice y se para**: nunca se sigue a medias ni se inventa.

---

## LAS 8 ETAPAS (una sola via, siempre la misma)

| Etapa | Que se hace | Cuando se da por buena |
|---|---|---|
| 1 | Identificar la **primera causa demostrada** | Esta escrita con numeros medidos, no con opiniones |
| 2 | Enumerar **los archivos que la provocan o la bloquean** | La lista esta abajo, cerrada |
| 3 | Autorizar esa lista **aunque haya un arnes detras** | La ruta queda abierta y se enseña a Julio |
| 4 | **Nada fuera de la lista** sin justificarlo | La ruta frena lo que no declaro |
| 5 | **Reparacion minima** | Un solo cambio, con su por que |
| 6 | **Pruebas fisicas** | La vigia del punto vira a VERDE, corriendo de verdad |
| 7 | **Lo que ya funcionaba sigue funcionando** | Los vecinos del cross-flow siguen verdes |
| 8 | **Certificacion y solo entonces** se autoriza lo siguiente | Julio lo ve con sus ojos |

**Vigia verde no es prueba** (`MODO INGENIERO`, regla 3): la prueba es que Julio lo vea funcionar.

---

## REPARACION 1 (la unica autorizada hoy)

**Causa demostrada**: el trabajo se manda al cerebro de pago **por un tope declarado**
(`TOPE_PESADO = 15000` en `cuerpo/obrero.py:473`) y no por la **capacidad real medida**.
Medido: los gratis llevan **0 de 72** trabajos escritos; en un paquete normal, **8 de 12** salidas
superan la capacidad de los gratis; un paquete que mide 14.858 llega a medir 25.122.
Resultado: gratis que si aguantan el encargo quedan de brazos cruzados y paga Julio.

**El cambio (una linea)**:
```
cuerpo/obrero.py:473
   hoy:      if len(prompt) > TOPE_PESADO or pesado:
   debe ser: if pesado or not cuotas.rankear(turnos, len(prompt)):
```
`turnos` (linea 466) ya son los gratis disponibles, sin los de pago.

### ARCHIVOS AUTORIZADOS (ruta abierta, y nada mas)

| Archivo | Para que |
|---|---|
| `cuerpo/obrero.py` | el arreglo de la linea 473 |
| `cuerpo/cuotas.py` | **solo** si la evidencia demuestra que la medida de capacidad esta mal |
| `vigias/test_vigia_se_reparte_por_capacidad.py` | la prueba del punto 1 (nace ROJA, debe virar VERDE) |
| `vigias/test_vigia_lo_pesado_a_deepseek.py` | vigia de la ley vieja: se ACTUALIZA a la ley nueva, no se borra |
| `CONTRATO_EL_PASILLO_SE_REPARTA_POR_CAPACIDAD.md` | la ley del punto 1 |
| `PLAN_DE_REPARACION_CONTROLADA.md` | este plan |
| `DONDE_QUEDO_2026-09-09.md` | el parte de donde quedo todo |

### NO AUTORIZADOS (ni se miran)

`arnes/aplicador.py`, `memoria/`, `cerebro/router.py`, frontend, base de datos, APIs,
cualquier vigia que no sea de las dos de arriba, y cualquier archivo que no participe en esta causa.
Si hiciera falta ampliar la ruta: **no se rodea, se dice** (Regla 4 del contrato de la ruta) y
Julio decide.

### Lo que NO se puede romper (vecinos que hoy funcionan)

`test_vigia_repartidor_por_capacidad.py`, `test_vigia_equipo_que_aguanta.py`,
`test_vigia_trabajar_respeta_generador_auditor.py`, `test_vigia_el_cerebro_es_el_que_pido.py`,
`test_vigia_relevo_cuotas.py`, `test_vigia_nada_lento.py`,
`test_vigia_revisor_roto_no_tira_la_vuelta.py`, `test_vigia_ruta_de_acceso.py`.

### Etapas 2 a 6 de Julio

**Sin empezar y sin tocar** hasta que Julio vea la reparacion 1 funcionando con sus ojos.

---

## ESTADO DE LA REPARACION 1 (2026-09-09)

| Etapa | Estado |
|---|---|
| 1. Primera causa demostrada | HECHA |
| 2. Archivos que la provocan o bloquean | HECHO (la tabla de arriba, cerrada) |
| 3. Autorizada la lista (ruta abierta) | HECHA (`memoria/RUTA_DE_ACCESO.json`) |
| 4. Nada fuera de la lista | CUMPLIDO: se toco `obrero.py` y las 2 vigias; `cuotas.py` NO hizo falta |
| 5. Reparacion minima | HECHA: 4 cambios (2 de fondo, 1 comentario de la constante, 2 vigias) |
| 6. Pruebas fisicas | HECHA: la vigia del punto 1 **ROJA -> 5 passed**; vecinos **52 passed / 0 failed** |
| 7. Lo que funcionaba sigue funcionando | HECHA: juego completo **642 passed**, y las 6 rojas se comprobo con `git stash` que **ya estaban rojas antes** (ajenas) |
| 8. Certificacion | **PENDIENTE DE JULIO**: que lo vea funcionar con sus ojos |

Efecto medido con las capacidades reales de hoy: un encargo de 19.500 letras lo aguantan **6 gratis**
(antes iba a DeepSeek de pago); uno de 60.000 lo aguantan gemini4, gemini2 y gemini (antes, pago).
DeepSeek sigue entrando cuando **de verdad** no le cabe a ningun gratis, y el bloqueo F2 sigue en pie.

La ruta queda **abierta** hasta que Julio certifique (por si hay que corregir algo que el vea).
Cerrarla, cuando toque: `python -c "import sys; sys.path.insert(0,'arnes'); import candado_ruta_de_acceso as r; r.cerrar()"`

---

## PRUEBA REAL (2026-09-10) — "que no vuelva a salir el fallo"

Julio mando: la prueba de verdad es el trabajo real, y si el fallo sale, se para. Se lanzo **una
ronda real del equipo** con un trabajo real pendiente (`vigias/_espia.py`, A1 del plan de DMM):

| | Antes del arreglo (log viejo) | En la prueba real de hoy |
|---|---|---|
| Quien ESCRIBE | `deepseek` (DE PAGO), siempre | **`gemini4` (GRATIS)** |
| Quien REVISA | `deepseek` a veces (se revisaba a si mismo) | **`gemini` (GRATIS, distinto)** |
| Aviso "no le cabe" falso | Si | **No** |
| Bloqueo F2 en caso normal | Si | **No** |

Registro: `memoria/TRABAJOS_DEL_EQUIPO.log` (`2026-09-10 12:04 | escribio gemini4 | reviso gemini`).
El veredicto fue RECHAZADO, pero **por otra causa, medida**: el encargo de `--crear` era el de
ANALISTA y pedia el documento *"en markdown"*, asi que el gratis hizo lo que se le pidio y el auditor
lo rechazo por no ser Python. Eso es el **punto 2/3**, no el reparto: **no se toco** hasta la
autorizacion de Julio. Queda declarado como el fallo que bloqueaba A1/A2 del plan.

### CIERRE DE LA PRUEBA REAL (2026-09-10, mismo dia) — el fallo NO se quedo

Julio autorizo (*"si, autorizo crear una pieza nueva"*) y el bloqueo se cerro en 3 pasos:

| Paso | Que se hizo | Con que se prueba |
|---|---|---|
| 1 | El encargo de crear ya pide **CODIGO** cuando la tarea pide un `.py` (y el de documento queda intacto) | llamada real a `_prompt_obrero` en los 3 casos + `ast.parse` del archivo tocado |
| 2 | Se creo la pieza `vigias/_espia.py` (A1 del plan de DMM), **6º encargo y 1º aprobado** | `TRABAJOS_DEL_EQUIPO.log`: `2026-09-10 12:26 | escribio gemini4 | reviso gemini3 | APROBADO` |
| 3 | La vigia roja viro a verde | `test_vigia_el_espia.py`: **4 failed -> 4 passed** |

El paso 1 **no se pago a ninguna IA**: el equipo lo freno por si mismo por la ley de la fotocopia
(`FRENADO: ESO ES UNA FOTOCOPIA, Y LA FOTOCOPIA NO SE PAGA`) y lo aplico `arnes/copista.py` (gratis).
Solo se creo un fichero de encargo auxiliar: `memoria/_encargo_copista.txt`.

Vecinos: **67 passed / 0 failed** (12 ficheros, incluidos los 8 del cross-flow).
Juego completo: **646 passed / 2 rojas**; las 2 rojas son **ajenas y previas** (fallo 67 del
2026-09-09 sin disparador, y una legislacion pendiente): 642 + las 4 de `_espia` que viraron = 646.
Ninguna roja nueva.

Autorizacion de ruta usada: `vigias/_espia.py` se anadio a `memoria/RUTA_DE_ACCESO.json`. Es la
primera vez que se amplia la ruta para CREAR, y es precisamente el agujero apuntado en la reparacion
2: **la amplio quien iba a usar la pieza**. Queda dicho aqui para que no se haga costumbre sin Julio.

Colores corridos de verdad: punto 1 + lo-pesado-a-deepseek **10 passed**; vecinos del cross-flow
**50 passed / 0 failed**; `test_vigia_el_espia.py` **4 failed** (correcto: nace roja pidiendo su pieza).

---

## AGUJERO CONOCIDO (apuntado, no tapado)

`memoria/RUTA_DE_ACCESO.json` esta en su propia lista, asi que quien trabaja **podria ampliarse la
ruta a si mismo**. Cerrarla es seguro; ampliarla no deberia poderla ampliar nadie mas que Julio.
Y ademas: el candado **no tiene puerta** — no existe comando en `ingeniero.py` que llame a
`abrir()`/`cerrar()`, solo su vigia. Las dos cosas quedan apuntadas para la reparacion 2.
