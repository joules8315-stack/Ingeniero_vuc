# PAQUETE MINIMO — dmm — 2026-09-10
> **Problema:** Enchufar cuerpo/traductor.py y cuerpo/aprobacion.py al chat real que atiende al dueno
> **Flujo(s) detectado(s):** aprobacion (6), traductor (6), real (6)
> **Raiz:** `C:\Users\USER\dev\Asesor Marketing`

**REGLA DE ESTE PAQUETE:** esto es TODO lo que hace falta. No abras nada mas.
Si de verdad necesitas otra cosa, PIDELA con el formato del final. No la leas por tu cuenta.

## 1. LA LEY QUE MANDA AQUI
- `CONTRATO_EL_TRADUCTOR_DE_PETICIONES.md` (85 lineas) — CONTRATO — EL TRADUCTOR: de lo que pide el cliente a un encargo profesional
- `CONTRATO_PRUEBA_REAL_DOGFOOD.md` (38 lineas) — CONTRATO_PRUEBA_REAL_DOGFOOD — la web DMM se crea a sí misma + campaña real + seguimiento
- `CONTRATO_WEB_DMM_PRUEBA_REAL.md` (17 lineas) — CONTRATO — PRUEBA REAL: DMM DISEÑA SU PROPIA WEB DE AGENCIA DE MARKETING
- `CONTRATO_A1_VOZ_MARCA.md` (42 lineas) — CONTRATO — Página A1: Voz de Marca (el "traductor")
- `CONTRATO_CAMPANAS_Y_CLIENTES.md` (121 lineas) — CONTRATO — CAMPAÑAS, APROBACIÓN, MAESTRA-ESCLAVA y MODELO DE CLIENTES
- `CONTRATO_CONECTAR_META.md` (66 lineas) — CONTRATO — CONECTAR LA PÁGINA REAL DE FACEBOOK (SolarDemo) al Marketing Manager
- `CONTRATO_CUERPO_Y_RAG.md` (59 lineas) — CONTRATO DE LA BASE — el CUERPO + la MEMORIA (RAG) del Asesor

### Texto de la ley que manda aqui (primera de la lista):
```
# CONTRATO — EL TRADUCTOR: de lo que pide el cliente a un encargo profesional

**Julio, 2026-09-09:**

> *"Que exista un creador de prompts, para que el pedido del cliente se convierta en prompt, y
> crear la herramienta para que ese prompt llegue a su sitio: sea búsqueda, sea mejorar una
> foto, o un video, una idea para el podcast. Para comunicarse de manera profesional con cada
> IA necesitamos, para ejecutar trabajos que no parezcan de niño estúpido, un MEDIADOR que
> convierta las palabras del cliente en diseños profesionales. Por lo cual se debe dotar el
> programa con estas habilidades: de marketing, de fotografía, de creación de campañas."*

---

## EL PROBLEMA, EN UNA FRASE

**El cliente dice "ponme una foto bonita del pan". Eso, mandado tal cual, devuelve una foto de
niño estúpido.**

Un fotógrafo profesional no oye "una foto bonita": oye **luz lateral de mañana, fondo
desenfocado, vapor saliendo del pan recién partido, sobre madera vieja**. Esa traducción es la
que separa un anuncio que vende de uno que da vergüenza.

> **DMM tiene que saber traducir. Y esa traducción es un oficio, no una frase.**

---

## LA LEY

**Ninguna petición del cliente llega tal cual a una IA. Pasa por el TRADUCTOR.**

```
"ponme una foto bonita del pan"
            ↓
       EL TRADUCTOR  (sabe de marketing, de fotografía y de campañas)
            ↓
un encargo profesional, con luz, encuadre, estilo, formato y para qué red
            ↓
       A SU SITIO: imagen, vídeo, búsqueda, podcast, texto
```

### Regla 1 — El traductor sabe de oficio, no de palabras bonitas
Tiene que saber **marketing** (qué hace que algo venda), **fotografía** (luz, encuadre, formato)
y **creación de campañas** (qué pieza va en qué red y por qué).

### Regla 2 — Cada encargo va A SU SITIO
No es lo mismo pedir una imagen que pedir una búsqueda, un vídeo o una idea de podcast. **El
traductor decide a dónde va y le da la forma que ese sitio entiende.**

### Regla 3 — El cliente sigue hablando como habla
**El cliente no aprende a hablar en técnico. El traductor aprende a entenderle.** Si hace falta
que el cliente escriba como un experto, el traductor no sirve.

### Regla 4 — Lo que no se sabe, se pregunta; no se rellena
Si falta un dato que cambia el resultado — el formato, la red, si sale gente — **se pregunta al
cliente en su móvil**. No se inventa un valor por defecto que después le sorprenda.

### Regla 5 — Se guarda lo que funcionó
Cuando una traducción da un buen resultado, **se guarda como lo que es: algo que funcionó, con
su fuente y su caducidad**. Eso enlaza con el ciclo que aprende.

---

## LO QUE HAY HOY, MEDIDO (2026-09-09)

| | Estado |
|---|---|
| Una pieza que traduzca peticiones a encargos profesionales | **NO EXISTE. Ninguna** |
| Textos de imagen dentro del generador de vídeo | existen, pero **solo para vídeo** |
| Textos de imagen en la campaña | existen, pero **son una frase fija**, no un encargo pensado |
| Habilidades de fotografía, marketing y campañas como tales | **NO EXISTEN** |

**Es de las cosas que faltan de verdad, no de las que estaban dormidas.**

---

## CÓMO SE COMPRUEBA QUE SE CUMPLE

`vigias/test_vigia_el_traductor_de_peticiones.py`, comprobando lo que importa:
1. que una petición en palabras normales **sale convertida en un encargo profesional**;
2. que **va al sitio correcto** según lo que se pide;
3. que si falta algo que cambia el resultado, **se pregunta en vez de inventarlo**;
4. y que **el cliente nunca tiene que hablar en técnico**.

**Y la prueba de verdad: que Julio pida "una foto bonita del pan" y lo que salga no dé vergüenza.**

```

## 2. LAS PIEZAS (su boca, sin abrirlas)
### `cuerpo/aprobacion.py` — 232 lineas
  cuerpo/aprobacion.py - EL CLIENTE APRUEBA DESDE SU MOVIL, Y NADA SALE SIN SU SI. LEY: CONTRATO_EL_CLIENTE_APRUEBA_DESDE_SU_MOVIL.md (Julio, 2026-09-09), la que 
  Funciones: `pedir_visto_bueno`:120, `leer_respuesta`:153, `almacen_log`:199, `pendientes`:228

### `cuerpo/traductor.py` — 161 lineas
  cuerpo/traductor.py - EL TRADUCTOR: de lo que pide el cliente a un encargo profesional. LEY: CONTRATO_EL_TRADUCTOR_DE_PETICIONES.md (Julio, 2026-09-09). EL PROB
  Funciones: `traducir`:97

## 3. LOS TROZOS EXACTOS (aqui esta el problema, ve directo)
### `cuerpo/aprobacion.py:1-40`  (relevancia 5.2)
```
# -*- coding: utf-8 -*-
"""cuerpo/aprobacion.py - EL CLIENTE APRUEBA DESDE SU MOVIL, Y NADA SALE SIN SU SI.

LEY: CONTRATO_EL_CLIENTE_APRUEBA_DESDE_SU_MOVIL.md (Julio, 2026-09-09), la que el mismo llamo
"parte cardinal de DMM".

POR QUE ES LO MAS IMPORTANTE: un dueno de negocio no se sienta delante de un ordenador. Esta
amasando pan a las cinco de la manana o atendiendo el mostrador. SU OFICINA ES EL MOVIL. Una
herramienta que le obliga a entrar a una web para aprobar cada cosa no se usa; y una que publica
sin preguntarle da miedo, porque es su marca y su dinero.

EL CANAL (aclaracion de Julio, 2026-09-09): la idea NO es depender de WhatsApp (los permisos son
complicados y ese no es el objetivo). Lo que quiere Julio es que la PROPIA APLICACION mande la
notificacion, igual que mandaria WhatsApp, para que el cliente apruebe, descarte o proponga
cambios usando el chat O el microfono (el microfono dicta texto; aqui se entiende igual). Por eso
este modulo es de la APP (guarda en el buzon via cuerpo/almacen.py) y WhatsApp es SOLO un canal
opcional enchufable, nunca la puerta.

EL CICLO QUE ESTA PIEZA PROTEGE:
  DMM prepara -> se lo ENSENA al cliente -> el ELIGE o PIDE CAMBIOS -> APRUEBA
  -> se AGENDA solo -> se publica -> EMPIEZA A MEDIR.

Reglas que cumple (NO se salta ninguna):
  1. NADA se publica sin el si del cliente (es su marca y su dinero).
  2. Se le ensena lo que va a salir tal cual (texto + imagenes + carrusel), no un resumen.
  3. "Pide cambios" es respuesta valida: se rehace SOLO eso y se vuelve a ensenar. Queda guardado
     (ensena sus gustos).
  4. Al aprobar se agenda solo (mismo acto), reusando cuerpo/automatizacion.py.
  5. Publicado significa empezar a medir (enlaza con el ciclo que aprende).
"""
import re
from datetime import datetime

_TABLA = "aprobaciones"

PENDIENTE = "pendiente_aprobacion"   # recien notificado, esperando su si
APROBADO = "aprobado"                # dio el si -> se agenda solo y puede publicarse en su fecha
CAMBIOS = "cambios"                  # pidio cambios -> DMM rehace solo eso
DESCARTADO = "descartado"            # la descarto

```

### `cuerpo/traductor.py:1-40`  (relevancia 4.97)
```
# -*- coding: utf-8 -*-
"""cuerpo/traductor.py - EL TRADUCTOR: de lo que pide el cliente a un encargo profesional.

LEY: CONTRATO_EL_TRADUCTOR_DE_PETICIONES.md (Julio, 2026-09-09).

EL PROBLEMA EN UNA FRASE: el cliente dice "ponme una foto bonita del pan". Eso, mandado tal cual a
una IA, devuelve una foto de nino estupido. Un fotografo profesional no oye "una foto bonita": oye
luz lateral de manana, fondo desenfocado, vapor saliendo del pan recien partido, sobre madera
vieja. Esa traduccion separa un anuncio que vende de uno que da verguenza.

ESTA PIEZA ES EL MEDIADOR: sabe de marketing, de fotografia y de campanas. Ninguna peticion del
cliente llega tal cual a una IA; primero pasa por aqui, que la convierte en un encargo profesional
(con luz, encuadre, estilo y formato) y decide A QUE SITIO va: imagen, video, busqueda o podcast.

REGLAS QUE CUMPLE:
  * el cliente sigue hablando como habla (el traductor entiende, no le hace aprender tecnico);
  * cada encargo va a su sitio y con la forma que ese sitio entiende;
  * lo que no se sabe y cambia el resultado SE PREGUNTA (nunca se inventa un valor por defecto);
  * lo que funciona se guarda (via cuerpo/almacen.py) para que no se pierda al apagar.

Se usa cuerpo/almacen.py para guardar (mismo sitio que el resto de la app): guardar una
traduccion que se pierde al apagar es guardar humo.
"""
import re

_TABLA = "traductor_log"

# Cada destino sabe de un oficio distinto: el encargo ya profesional (aterrizado en la empresa,
# sin rellenar datos que el cliente no dio).
_OFICIO_IMAGEN = (
    "luz lateral suave de la manana que marque la textura, fondo limpio y desenfocado para que el "
    "ojo vaya al producto, plano cercano, encuadre directo y honesto, sin cliches ni "
    "exageraciones. Estilo de fotografia comercial que vende por apetito, confianza y verdad."
)
_OFICIO_VIDEO = (
    "un arranque que enganche en los primeros 3 segundos, ritmo que no aburre, una sola idea "
    "clara y un cierre que invite a actuar sin presion. La forma exacta (formato, red y duracion) "
    "no se decide aqui si el cliente no la pidio: se pregunta antes de producir."
)
_OFICIO_BUSQUEDA = (
```

## 4. LAS VIGIAS QUE PROTEGEN ESTO
- `vigias/test_vigia_el_traductor_de_peticiones.py`
- `vigias/test_vigia_envio_real.py`

Correlas ANTES de tocar (para ver de que color estan) y DESPUES (para no romper):
```
cd "C:\Users\USER\dev\Asesor Marketing"; python -m pytest -q vigias/test_vigia_el_traductor_de_peticiones.py vigias/test_vigia_envio_real.py
```

## 5. A QUIEN PUEDE DANAR TOCAR ESTO (cross-flow obligatorio)
- Nadie depende de estas piezas. Reparacion aislada.

## LO QUE YA NOS PASO AQUI (memoria de fallos — no tropezar dos veces)
- **Aplicar el paquete dmm__enchufar_cuerpo_traductor_py_y_cuerpo_ap: enchufar cuerpo/traductor.py y cuerpo/aprobacion.py al chat real que atiende al dueno. Una peticion en palabras de persona se traduce a encargo; cuando la campana esta lista le llega una notificacion DENTRO de la app y el da el si / pide cambios / descarta por chat o microfono; al aprobar queda agendada sola. Sin romper vecinos. Despues prueba real de pantalla (Playwright).** (paso 5 veces)
  - causa raiz : El paquete pide enchufar cuerpo/traductor.py y cuerpo/aprobacion.py al chat real que atiende al dueno, pero el material no contiene el archivo del chat real ni la funcion que lo conecta, por lo que no se puede realizar la integracion sin inventar.
  - se curo con: No se puede realizar el cambio porque el material no incluye el archivo del chat real ni la funcion que lo conecta con cuerpo/traductor.py y cuerpo/aprobacion.py.
  - NO VOLVER A: La reparación propuesta no implementa la conexión del traductor y la aprobación al chat real de la aplicación. La prueba B requiere que la petición del usuario en el chat se traduzca y luego se apruebe dentro de la misma aplicación, lo cual no se aborda en la reparación.
  - lo vigila  : vigias/test_vigia_enchufar_traductor_aprobacion.py
- **crear el modulo de Ciencia Experimental (experimentos.py) que falta segun el contrato cientifico creativo: DMM define el test, recoge resultados y aprende. Usa SOLO la memoria del paquete.** (paso 5 veces)
  - causa raiz : El mÃ³dulo experimentos.py no existe y hay incompatibilidad de firmas entre lo que espera el contrato y lo que se puede implementar con el material disponible.
  - se curo con: Crear el mÃ³dulo cuerpo/experimentos.py con las funciones definir_test, recoger_resultados y aprender, usando las firmas compatibles con el flujo detectado (memoria, resultados, crear) y el material disponible.
  - NO VOLVER A: Escribir el cÃ³digo real del archivo cuerpo/experimentos.py. Debe implementar definir_test (que devuelva un dict con id), recoger_resultados y aprender (que debe llamar a cuerpo.memoria para persistir la lecciÃ³n).
  - lo vigila  : C:\Users\USER\dev\Asesor Marketing\vigias\test_vigia_experimentos.py
- **El paquete traia el motor (cuerpo/perfil.py) pero NO la cara (web/), donde esta el formulario que de verdad guarda**
  - causa raiz : el flujo se armaba solo por el NOMBRE del archivo, y web/servidor.py no se llama 'onboarding'
  - se curo con: quien IMPORTA una pieza del flujo pertenece al flujo (llamadores por el grafo)
  - NO VOLVER A: armar un flujo mirando solo nombres de archivo; hay que seguir los hilos
  - lo vigila  : vigias/test_vigia_paquete_trae_la_cara.py

## 6. SI NECESITAS ALGO MAS, PIDELO ASI (no lo leas por tu cuenta)
```
NECESITO_LEER:
  archivo:  <ruta exacta>
  motivo:   <que pregunta responde>
  decide:   <que decision desbloquea>
  riesgo:   <que pasa si no lo leo>
```

## 7. LO QUE NO SE HACE
- No inventar archivos, funciones ni lineas. Si no esta arriba, se escribe `NO_ENCONTRADO`.
- No decidir lo que el contrato no dice. Se escribe `PREGUNTA_REQUERIDA:` y se le pregunta a Julio.
- No sellar con una vigia roja.
- Una vigia verde NO es prueba. La prueba es que Julio lo vea funcionar.