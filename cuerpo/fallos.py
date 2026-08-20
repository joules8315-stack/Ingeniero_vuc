# -*- coding: utf-8 -*-
"""cuerpo/fallos.py — LA MEMORIA DE FALLOS (orden 6.1 de Julio, 2026-08-20).

  "que haya siempre memoria de fallos, que se actualice constantemente para que siempre sepa
   el ingeniero que hacer y que no."

Un fallo que no se apunta se repite. Aqui queda cada uno con: que paso, por que paso (causa
raiz), como se curo, y QUE NO SE DEBE VOLVER A HACER. Antes de reparar cualquier cosa, el
Ingeniero mira si ya se tropezo con esa piedra.

No se borra nada: un fallo viejo sigue enseñando. Se marca `curado` y se queda.
Vive en `memoria/FALLOS.json` -> sobrevive a que se cierre la sesion o se acabe el saldo.
"""
import os, sys, json, re, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "FALLOS.json")


def _leer():
    try:
        d = json.load(open(RUTA, encoding="utf-8"))
        return d if isinstance(d, list) else d.get("fallos", [])
    except Exception:
        return []


def _guardar(fallos):
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    json.dump(fallos, open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def apuntar(que_paso, causa_raiz, cura, no_volver_a, proyecto="", piezas=None,
            quien_lo_caza="", contar=True):
    """Apunta un fallo REAL. `no_volver_a` es lo mas valioso: la leccion en una frase."""
    fallos = _leer()
    nuevo = {
        "id": len(fallos) + 1,
        "fecha": datetime.date.today().isoformat(),
        "proyecto": proyecto,
        "que_paso": que_paso,
        "causa_raiz": causa_raiz,
        "cura": cura,
        "no_volver_a": no_volver_a,
        "piezas": piezas or [],
        "quien_lo_caza": quien_lo_caza,   # que vigia/agente lo detecta ahora
        "veces": 1,
    }
    # si ya estaba apuntado el mismo, se sube el contador en vez de duplicar (Ley 6)
    for f in fallos:
        if f["que_paso"].lower()[:60] == que_paso.lower()[:60]:
            # `contar=False` para la siembra: volver a sembrar NO significa que el fallo se
            # repitiera. Fallo real 2026-08-20: la memoria decia "x4" sobre fallos que pasaron
            # UNA vez. Un dato falso en la memoria de fallos es peor que no tener memoria.
            if contar:
                f["veces"] = f.get("veces", 1) + 1
                f["fecha"] = nuevo["fecha"]
            if quien_lo_caza and not f.get("quien_lo_caza"):
                f["quien_lo_caza"] = quien_lo_caza
            _guardar(fallos)
            return f
    fallos.append(nuevo)
    _guardar(fallos)
    return nuevo


def _palabras(t):
    return {w for w in re.split(r"[^\wáéíóúñ]+", (t or "").lower()) if len(w) > 3}


def parecidos(problema, proyecto="", k=4):
    """¿Ya nos tropezamos con esta piedra? Devuelve los fallos que se parecen."""
    q = _palabras(problema)
    if not q:
        return []
    out = []
    for f in _leer():
        if proyecto and f.get("proyecto") and f["proyecto"] != proyecto:
            continue
        texto = " ".join([f["que_paso"], f["causa_raiz"], f["no_volver_a"]] + f.get("piezas", []))
        comunes = q & _palabras(texto)
        if comunes:
            out.append((len(comunes), f))
    return [f for _, f in sorted(out, key=lambda x: -x[0])[:k]]


def aviso_para_el_paquete(problema, proyecto=""):
    """El texto que se mete en el paquete minimo. Vacio si no hay nada parecido."""
    ps = parecidos(problema, proyecto)
    if not ps:
        return ""
    L = ["## LO QUE YA NOS PASO AQUI (memoria de fallos — no tropezar dos veces)"]
    for f in ps:
        veces = f" (paso {f['veces']} veces)" if f.get("veces", 1) > 1 else ""
        L.append(f"- **{f['que_paso']}**{veces}")
        L.append(f"  - causa raiz : {f['causa_raiz']}")
        L.append(f"  - se curo con: {f['cura']}")
        L.append(f"  - NO VOLVER A: {f['no_volver_a']}")
        if f.get("quien_lo_caza"):
            L.append(f"  - lo vigila  : {f['quien_lo_caza']}")
    return "\n".join(L)


def texto():
    fallos = _leer()
    if not fallos:
        return "MEMORIA DE FALLOS: vacia todavia."
    L = [f"MEMORIA DE FALLOS ({len(fallos)} apuntados) — lo que el Ingeniero ya aprendio:"]
    for f in sorted(fallos, key=lambda x: -x.get("veces", 1)):
        veces = f" x{f['veces']}" if f.get("veces", 1) > 1 else ""
        L.append(f"  [{f['fecha']}]{veces} {f['que_paso'][:80]}")
        L.append(f"        NO VOLVER A: {f['no_volver_a'][:90]}")
    return "\n".join(L)


# ─── Los fallos REALES del 2026-08-20 quedan sembrados de entrada ──────────────────
SEMILLA = [
    dict(que_paso="El paquete traia el motor (cuerpo/perfil.py) pero NO la cara (web/), donde esta "
                  "el formulario que de verdad guarda",
         causa_raiz="el flujo se armaba solo por el NOMBRE del archivo, y web/servidor.py no se "
                    "llama 'onboarding'",
         cura="quien IMPORTA una pieza del flujo pertenece al flujo (llamadores por el grafo)",
         no_volver_a="armar un flujo mirando solo nombres de archivo; hay que seguir los hilos",
         proyecto="dmm", piezas=["cerebro/router.py", "web/servidor.py"],
         quien_lo_caza="vigias/test_vigia_paquete_trae_la_cara.py"),
    dict(que_paso="El candado de lectura dejaba abrir app.py entero (10.818 lineas)",
         causa_raiz="bastaba que el nombre del archivo apareciera 'de pasada' en un comentario "
                    "del paquete para darlo por declarado",
         cura="solo vale lo declarado como cabecera `### `pieza`` en el paquete",
         no_volver_a="comprobar pertenencia con 'esta el nombre en el texto'; hay que exigir "
                     "la declaracion formal",
         proyecto="ingeniero", piezas=["arnes/read_gate.py"],
         quien_lo_caza="prueba manual de los 3 casos del candado"),
    dict(que_paso="El buscador de habilidades decia 'ya lo escribiste' sobre cosas que Julio "
                  "nunca escribio (telegram, QR)",
         causa_raiz="se exigia 'cualquiera' de las palabras y las cortas (qr) o comunes (canal) "
                    "colaban cualquier trozo; ademas las no indexadas parecian rarisimas",
         cura="exigir SOLO la palabra mas rara, y si no queda ninguna que distinga, devolver vacio",
         no_volver_a="afirmar que algo existe sin una palabra que de verdad lo distinga",
         proyecto="ingeniero", piezas=["cuerpo/skills.py"],
         quien_lo_caza="vigias/test_vigia_skills_no_miente.py"),
    dict(que_paso="Un trozo de un problema de PLANTILLA traia el codigo del LOGIN",
         causa_raiz="la palabra 'sesion' aparecia en los dos asuntos",
         cura="filtro `exigir`: el trozo debe hablar del asunto, no compartir una palabra suelta",
         no_volver_a="buscar por palabras sueltas sin exigir el asunto",
         proyecto="foto_informe", piezas=["cerebro/trozos.py"],
         quien_lo_caza="vigias/test_vigia_trae_la_pieza_correcta.py"),
    dict(que_paso="Import del cerebro de DMM agarraba el paquete equivocado",
         causa_raiz="el Ingeniero y DMM tienen los dos un paquete llamado `cuerpo`",
         cura="cargar por RUTA con importlib y nombre propio (dmm_cerebro)",
         no_volver_a="importar por nombre cuando dos proyectos comparten nombre de paquete",
         proyecto="ingeniero", piezas=["cuerpo/obrero.py"],
         quien_lo_caza="cuerpo/obrero.py::disponible()"),
]


def sembrar():
    """Deja apuntados los fallos ya vividos. Idempotente: no duplica."""
    for f in SEMILLA:
        apuntar(contar=False, **f)
    return len(_leer())


if __name__ == "__main__":
    if "--sembrar" in sys.argv:
        print("fallos apuntados:", sembrar())
    print(texto())
