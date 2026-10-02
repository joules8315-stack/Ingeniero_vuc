# PAQUETE MINIMO — ingeniero — 2026-09-10
> **Problema:** Puerta trasera: se trabajo sin el equipo (sin ley 6). Prohibido abrir candados sin permiso. Crear comando para encriptar la carpeta de candados. Tarea: sustituir con programas las funciones que no necesitan IA.
> **Flujo(s) detectado(s):** equipo (6)
> **Raiz:** `C:\Ingeniero_VUC`

**REGLA DE ESTE PAQUETE:** esto es TODO lo que hace falta. No abras nada mas.
Si de verdad necesitas otra cosa, PIDELA con el formato del final. No la leas por tu cuenta.

## 1. LA LEY QUE MANDA AQUI
- `CONTRATO_EL_EQUIPO_ESCRIBE.md` (112 lineas) — CONTRATO — EL EQUIPO GRATIS ESCRIBE, EL DE PAGO ES EL ÚLTIMO RECURSO
- `CONTRATO_EQUIPO_QUE_AGUANTA.md` (88 lineas) — CONTRATO — EL EQUIPO QUE AGUANTA EL TAMAÑO
- `CONTRATO_UNA_SOLA_VIA.md` (86 lineas) — CONTRATO — UNA SOLA VIA, PARA ABRIR Y PARA GUARDAR
- `PLAN_CANDADOS_QUE_NO_SE_VIOLAN.md` (225 lineas) — PLAN — CANDADOS QUE NO SE PUEDEN VIOLAR, Y QUE NO TE PIDEN PERMISO
- `CONTRATO_AUDITORIA_DE_PROYECTO.md` (150 lineas) — CONTRATO — EL INVENTARIO PARA UNA SEGUNDA OPINION
- `CONTRATO_AUTONOMIA_CLINE.md` (57 lineas) — CONTRATO_AUTONOMIA_CLINE — Cline actúa AUTÓNOMO en el bucle, sin pedir autorización a Julio

### Texto de la ley que manda aqui (primera de la lista):
```
# CONTRATO — EL EQUIPO GRATIS ESCRIBE, EL DE PAGO ES EL ÚLTIMO RECURSO

**Julio, 2026-09-07:**

> *"Si se comprueba que el equipo sí puede escribir — antes no lo hacía porque lo hacía mal,
> pero si se corrige el fallo de por qué lo hacía mal, ahora sí puede escribir — y que lo
> copie un programa. **Esa es la petición desde el principio.** Pasé a realizar todo con
> DeepSeek porque el equipo no servía; una vez reparado esto, que siga el equipo gratis y
> DeepSeek se deje para cuando el equipo falle, pasando a ser la última instancia. Luego de
> una hora se verifica si el equipo se recuperó y vuelve el equipo a trabajar. Esto se debe
> medir ahora cuando se comience a crear DMM: cuánto demora el equipo en recuperarse, cada
> IA, para delegar así, rotarlos de modo que tengan el tiempo suficiente de respuesta y de
> recuperación."*

---

## LA LEY, Y SU CONDICIÓN

**El equipo gratis vuelve a escribir. El de pago pasa a ser el último recurso.**

**PERO la orden es CONDICIONAL, y así se cumple:** *"si se comprueba que el equipo sí puede
escribir"*. Primero se reparan los fallos, después **se mide**, y **solo si la medida dice que
sí**, se invierte el reparto. La prohibición del 2026-08-24 no se levanta por decreto: se
levanta con datos.

### Regla 1 — ÚLTIMO RECURSO NO SIGNIFICA QUE NO SE LE LLAME

**Confirmado por Julio el 2026-09-07.** Es un fallo ya cometido: se dio por cerrado un *"no hay
quien audite"* **sin haber llamado al de pago**, estando disponible y documentado justo para
eso. Al invertir el reparto, **DeepSeek sigue entrando SIEMPRE que el equipo falle**. No se
convierte en un adorno.

**Si un trabajo se queda sin hacer y no se le llamó, eso es un fallo, no un ahorro.**

### Regla 2 — La hora de gracia
Si el equipo falla y el de pago toma el relevo, **a la hora se vuelve a probar al equipo con
una tarea corta**. Si contesta bien, recupera el trabajo. No se le entierra por un mal rato.

### Regla 3 — Se rota, no se amontona
El trabajo se reparte **espaciando las llamadas**, para no volver a tocar el límite por minuto
de cada uno. Cada IA tiene su tiempo de respuesta y su tiempo de recuperación, **medidos**, y
se delega según eso.

### Regla 4 — Se mide con trabajo de verdad
La medición de cuánto tarda cada IA en recuperarse **se hace construyendo DMM**, no con
pruebas de laboratorio. Lo pidió Julio así.

### Regla 5 — Lo que NO cambia
- El bloqueo **F2** (nunca trabajar solo) sigue en pie.
- Quien revisa es **siempre otro distinto** del que escribió.
- Los **tiempos de espera por llamada** se quedan como estaban (Julio, 2026-09-07).

---

## LA TABLA DE VERDAD — las tres razones de la prohibición, y su estado

Julio anotó el 2026-08-24, con la medida delante:

> *"Medido tres veces el mismo día, con encargos POR DEBAJO del tope, los gratis devolvieron
> **propuesta vacía**, un **error de tamaño**, y **texto ilegible**. Se rendían igual."*

Son **tres causas distintas que nunca se aislaron**. La ley se levanta cuando estén las tres
resueltas y medidas:

| Razón | Cómo se quita | Estado |
|---|---|---|
| **Texto ilegible** | El traductor: rescata la respuesta rota y, si no puede, pide lo mismo en texto normal | pendiente |
| **Error de tamaño** | Rotación y espaciado: no volver a tocar el límite por minuto | pendiente |
| **Propuesta vacía** | El cuaderno de llamadas dirá si sigue pasando y cuándo | pendiente |

**Mientras quede una viva, la prohibición se queda, y se dice CUÁL sigue viva.**

---

## LA MATRIZ — qué hay que tener antes de invertir

| Hace falta | Para qué | Estado |
|---|---|---|
| `arnes/copista.py` | Que lo mecánico no lo escriba ningún cerebro | **HECHO y probado (2026-09-07)** |
| `vigias/test_vigia_copista.py` | Que el copista no deje de frenar nunca | en marcha |
| El traductor de respuestas rotas | Quitar la 3ª razón | pendiente |
| El cuaderno de llamadas | Saber POR QUÉ falla cada una. **Sin esto no se puede decidir nada** | pendiente |
| La rotación medida | Dejar de llamar cada minuto y medio | pendiente |

---

## LO QUE SE MIDIÓ Y OBLIGA A ESTO (fechas incluidas)

- **2026-09-06:** de 8 rondas pagadas, en **5** el encargo ya llevaba el texto de antes y el de
  después exactos. El cerebro de pago solo copió.
- **2026-09-06 / 07, 15 horas:** **40 siestas, 35 de tipo "minuto"**. Un cerebro que toca su
  límite duerme 90 segundos y vuelve a la fila; se le llama otra vez y vuelve a caer. **Cada
  vuelta de esa noria le cuenta como un fallo suyo.** Por eso Gemini figura con 96 % de fallos:
  no es que sea malo, es que se le llama a la puerta cada minuto y medio.

---

## A QUIÉN PUEDE DAÑAR

- A `cuerpo/obrero.py` (el orden de la fila) y a `cuerpo/cuotas.py` (las siestas y el reparto).
- A `CONTRATO_MAESTRO_AHORRO`, que se actualiza cuando la inversión ocurra.
- **A nadie más**: mientras la medida no lo permita, todo sigue exactamente como hoy.

## CÓMO SE COMPRUEBA

**La prueba no es una vigía verde. Es esta:** que en el veredicto de un trabajo real aparezca
**un cerebro GRATIS como obrero, no DeepSeek** — y que cuando ese gratis falle, **el de pago
entre igual** y el trabajo salga.

Su vigía comprueba lo que sí es determinista: que el de pago **siga estando en la fila** aunque
vaya el último, y que nunca se devuelva "no se pudo hacer" sin haberle llamado.

```

## 2. LAS PIEZAS (su boca, sin abrirlas)
### `skills/medir_al_equipo.py` — 137 lineas
  HABILIDAD — MEDIR AL EQUIPO. Sin gastar ni una llamada a ninguna IA. Julio, 2026-09-05: "crea las putas skills, habilidades, justo para que hagan lo repetitivo,
  Funciones: `medir`:70, `informe`:111

## 3. LOS TROZOS EXACTOS (aqui esta el problema, ve directo)
### `skills/medir_al_equipo.py:1-40`  (relevancia 2.46)
```
# -*- coding: utf-8 -*-
"""HABILIDAD — MEDIR AL EQUIPO. Sin gastar ni una llamada a ninguna IA.

Julio, 2026-09-05: "crea las putas skills, habilidades, justo para que hagan lo
repetitivo, sin necesidad de usar IA".

Esto es lo que el 5 de septiembre se hizo A MANO con seis ordenes de terminal para
saber si los cerebros gratis sirven o no. Es una cuenta, no un juicio: por eso lo
hace un programita y no un cerebro.

Contesta, con el registro que ya existe en disco:
  - quien ESCRIBE de verdad y quien solo REVISA
  - que trabajo fue real y que trabajo fue de practica
  - cuanto de lo aprobado llego DE VERDAD al codigo

Se usa asi:
    cd C:\\Ingeniero_VUC; python skills/medir_al_equipo.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRABAJOS = os.path.join(AQUI, "memoria", "TRABAJOS_DEL_EQUIPO.log")
APLICADO = os.path.join(AQUI, "memoria", "APLICACIONES.log")

if os.environ.get("PYTEST_CURRENT_TEST"):
    import tempfile
    _tmp = tempfile.mkdtemp()
    TRABAJOS = os.path.join(_tmp, "TRABAJOS_DEL_EQUIPO.log")
    APLICADO = os.path.join(_tmp, "APLICACIONES.log")


def _lineas(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, encoding="utf-8", errors="ignore") as f:
        return [ln.rstrip("\n") for ln in f if ln.strip()]


def _trozos(linea):
```

## 4. LAS VIGIAS QUE PROTEGEN ESTO
- `vigias/test_vigia_deepseek_en_el_equipo.py`
- `vigias/test_vigia_equipo_no_cae.py`
- `vigias/test_vigia_equipo_que_aguanta.py`
- `vigias/test_vigia_equipo_siempre.py`
- `vigias/test_vigia_equipo_sirve.py`
- `vigias/test_vigia_equipo_total.py`
- `vigias/test_vigia_siempre_con_equipo.py`

Correlas ANTES de tocar (para ver de que color estan) y DESPUES (para no romper):
```
cd "C:\Ingeniero_VUC"; python -m pytest -q vigias/test_vigia_deepseek_en_el_equipo.py vigias/test_vigia_equipo_no_cae.py vigias/test_vigia_equipo_que_aguanta.py vigias/test_vigia_equipo_siempre.py vigias/test_vigia_equipo_sirve.py vigias/test_vigia_equipo_total.py vigias/test_vigia_siempre_con_equipo.py
```

## 5. A QUIEN PUEDE DANAR TOCAR ESTO (cross-flow obligatorio)
- Nadie depende de estas piezas. Reparacion aislada.

## LO QUE YA NOS PASO AQUI (memoria de fallos — no tropezar dos veces)
- **Julio tuvo que decir TRES veces que se trabaja en equipo, y me dijo 'por no trabajar en equipo ya has gastado 19'. El arnes solo guarda UN permiso de edicion a la vez, asi que pedir el segundo borra el primero y hay que repetir la peticion.**
  - causa raiz : El permiso se guarda en un solo hueco. Con un trabajo que toca dos archivos, obliga a pedir permiso una y otra vez y empuja a apagar el arnes.
  - se curo con: APUNTADO, no reparado aun: hace falta que el permiso guarde varios archivos a la vez.
  - NO VOLVER A: pedir dos permisos seguidos creyendo que valen los dos
- **El Ingeniero creia elegir cerebro y SIEMPRE contestaba el mismo. Un modelo inventado, 'pepito-grillo-9000', contesto tan tranquilo (y en italiano). Kimi K2 y K3 'funcionaban' a 7 segundos: era mentira, era Gemini disfrazado. Julio pidio Kimi creyendo que hacia falta descargarlo, y ni siquiera esta en su llave.**
  - causa raiz : La puerta comoda del cerebro prestado hacia DOS cosas a escondidas: a Gemini le quitaba el modelo pedido y usaba el suyo fijo; y si el modelo no existia, en vez de avisar caia CALLANDO en otro proveedor. Un error tapado es peor que un error: hace tomar decisiones sobre datos falsos. Encima los dos modelos fijos de Gemini (2.0-flash y respaldo 1.5-flash) llevaban MUERTOS: 404 los dos. Por eso Gemini fallaba 4 de 7 veces y el trabajo caia en la IA cara, o sea Julio pagando.
  - se curo con: El Ingeniero llama a cada cerebro DIRECTO, con el modelo que el elige, y un modelo que no existe da error a la vista. Se comprobo uno por uno contra la llave real: en Groq solo viven gpt-oss-120b y gpt-oss-20b (0.9s); en Gemini el bueno es gemini-3.5-flash (3.3s). Kimi y los Llama dan 404: no estan en su llave.
  - NO VOLVER A: fiarse de una medida de velocidad o de disponibilidad sin comprobar QUIEN contesto de verdad; y dejar que un fallo de modelo caiga callando en otro
  - lo vigila  : vigias/test_vigia_el_cerebro_es_el_que_pido.py
- **El candado de lectura dejaba abrir app.py entero (10.818 lineas)**
  - causa raiz : bastaba que el nombre del archivo apareciera 'de pasada' en un comentario del paquete para darlo por declarado
  - se curo con: solo vale lo declarado como cabecera `### `pieza`` en el paquete
  - NO VOLVER A: comprobar pertenencia con 'esta el nombre en el texto'; hay que exigir la declaracion formal
  - lo vigila  : prueba manual de los 3 casos del candado
- **Dos IA quedaron con la MISMA tarea porque cada una la tenia escrita con otras palabras: 'el guardian deja de ensuciarse solo' y 'el guardian deja de gritar por sus propios cuadernos'**
  - causa raiz : arnes/reparto.py compara las tareas letra por letra. Dos formas de decir lo mismo no coinciden, asi que no las ve como la misma y deja que dos las cojan. Es justo lo que el reparto existe para impedir
  - se curo con: comparar las tareas por las palabras que comparten, no letra por letra, y avisar cuando se parecen demasiado antes de asignarlas a dos
  - NO VOLVER A: dar por distinta una tarea solo porque este escrita con otras palabras: Julio habla de la misma cosa de diez maneras y todas son la misma cosa
  - lo vigila  : vigias/test_vigia_reparto_con_cline.py

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