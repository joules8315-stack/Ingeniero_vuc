# LAS CUATRO PIEZAS QUE TE PIDIERON

Copiadas del disco tal cual, sin recortes ni retoques.
Fecha: 2026-09-01.

---

## 1. `ingeniero.py` — el bloque del mando `equipo` (donde guarda el veredicto)

```python
    if cmd == "equipo" and len(sys.argv) >= 4:
        # SIEMPRE EL EQUIPO (Julio, 2026-08-21, tras repetirlo tres veces y pagarlo).
        # Uno genera, OTRO distinto audita. Claude dirige y lee el veredicto: nada mas.
        # Deja la llave que abre el candado de escribir codigo.
        import sys as _s
        import json as _json
        import re as _re
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        from cerebro import router as _r
        from cuerpo import obrero as _o
        import candado_equipo as _ce
        proy, tarea = sys.argv[2], " ".join(sys.argv[3:])
        paq = _r.armar(proy, tarea)
        # el TEXTO, no la caja: trabajar espera el texto del paquete (fix 2026-08-24)
        res = _o.trabajar(_r.a_texto(paq), tarea)
        # ENCARGO A (2026-09-02): el trabajo pagado NO se tira. Se guarda SIEMPRE el
        # resultado ENTERO que contesto el equipo, ANTES de imprimir nada, pase lo que pase
        # (aprobado, rechazado o sin revisar: un rechazo tambien dice algo y vale dinero). Se
        # guarda antes de mostrar porque ya paso que la pantalla reventaba con una letra rara y
        # se perdia todo.
        try:
            _ult = os.path.join(AQUI, "memoria", "ULTIMO_TRABAJO_DEL_EQUIPO.json")
            os.makedirs(os.path.dirname(_ult), exist_ok=True)
            with open(_ult, "w", encoding="utf-8") as _f:
                _json.dump(res, _f, ensure_ascii=False, indent=1)
        except Exception:
            pass    # guardar es la prueba, pero no puede tumbar el trabajo
        # PRIMERO SE GUARDA, DESPUES SE ENSENA (fallo real 2026-08-25).
        # Antes se imprimia justo aqui y la llave se guardaba al final. El equipo contesto, el
        # print murio por un caracter que la consola de Windows no sabia dibujar, y el trabajo YA
        # PAGADO se perdio entero: no se guardo nada y hubo que volver a llamar. Lo que cuesta
        # dinero se asegura ANTES de ensenarlo. Mostrar es lo ultimo y ya no puede tumbar nada.
        if "_error" in res:
            print(_o.veredicto_corto(res))
            return 1
        prop = res.get("propuesta") or {}
        tocados = prop.get("archivo") or prop.get("archivos") or []
        if isinstance(tocados, str):
            tocados = [tocados]
        # tambien valen las piezas que el paquete trajo: es lo que el equipo tuvo delante.
        # FALLO REAL (2026-08-24): esto buscaba "piezas" y el paquete NO usa ese nombre, usa
        # "fichas" (medido: fichas=39, piezas=None). Como el obrero gratis casi siempre devuelve
        # NO_ENCONTRADO en proyectos grandes, la llave quedaba en ['NO_ENCONTRADO'] y no abria
        # nada: no se podia tocar ni una vigia recien escrita del mismo proyecto. El candado del
        # equipo se volvia un muro en vez de una puerta con llave.
        for clave in ("fichas", "piezas"):
            for pz in (paq.get(clave) if isinstance(paq, dict) else []) or []:
                pid = pz.get("id") if isinstance(pz, dict) else str(pz)
                if pid and pid not in tocados:
                    tocados.append(pid)
        _ce.guardar_veredicto(tarea, tocados, res.get("obrero"), res.get("auditor"),
                              (res.get("auditoria") or {}).get("veredicto", "?"))
        # Ya esta a salvo. AHORA se ensena, y si mostrar falla, no se pierde nada.
        try:
            print(_o.veredicto_corto(res))
        except Exception as _e:
            print("(el veredicto llego y quedo guardado, pero no se pudo mostrar entero: %s)"
                  % str(_e)[:90])
        print()
        # EL MENSAJE NO MIENTE (Julio, 2026-08-27): antes "LLAVE GUARDADA" salia SIEMPRE, incluso
        # cuando el equipo habia RECHAZADO. El candado NO abria (ya esta probado), pero el mensaje
        # decia "guarda llave" y enganaba. Ahora se dice la verdad: la llave SOLO abre con APROBADO.
        v_final = ((res.get("auditoria") or {}).get("veredicto", "?") or "?").strip().upper()
        # ENCARGO A (parte 2): cuando el equipo APROBO y la propuesta trae un archivo NUEVO con su
        # texto completo, y ese archivo NO EXISTE todavia, se crea. Si ya existe NO se toca, ni se
        # sobrescribe ni se le anade: solo se crean archivos nuevos. Y si el texto viene envuelto
        # entre lineas de tres tildes, se le quita la envoltura antes de guardar o queda roto.
        if v_final == "APROBADO" and isinstance(prop, dict):
            _nuevo_archivo = prop.get("archivo") or (prop.get("archivos") or [None])[0]
            _texto = prop.get("codigo") or prop.get("texto_nuevo") or ""
            if _nuevo_archivo and isinstance(_texto, str) and _texto.strip() \
                    and not os.path.exists(str(_nuevo_archivo)):
                _texto_limpio = _texto.lstrip()
                if _texto_limpio.startswith("```"):
                    _salto = _texto_limpio.find("\n")
                    _texto_limpio = _texto_limpio[_salto + 1:] if _salto >= 0 else ""
                if _texto_limpio.rstrip().endswith("```"):
                    _texto_limpio = _texto_limpio.rstrip()[:-3].rstrip("\n")
                try:
                    _destino = os.path.abspath(str(_nuevo_archivo))
                    os.makedirs(os.path.dirname(_destino), exist_ok=True)
                    with open(_destino, "w", encoding="utf-8") as _f:
                        _f.write(_texto_limpio + "\n")
                    print("CREADO (lo escribio el equipo): %s (%d letras)"
                          % (_nuevo_archivo, len(_texto_limpio)))
                except Exception as _e:
                    print("no se pudo crear %s: %s" % (_nuevo_archivo, str(_e)[:90]))
        if v_final == "APROBADO":
            print("LLAVE GUARDADA: se puede escribir en %d archivo(s) durante %d min."
                  % (len(tocados), _ce.VIGENCIA_MIN))
        else:
            print("EL EQUIPO NO APROBO (%s): NO se guardo llave, no se puede tocar codigo."
                  % v_final)
        return 0
```

---

## 2. `arnes/guardia_de_guardado.py` — COMPLETO (208 renglones)

```python
# -*- coding: utf-8 -*-
"""arnes/guardia_de_guardado.py — EL CANDADO QUE NO DEPENDE DE QUIEN ESCRIBA.

Julio, 2026-08-24:
  "Crea candado para que cline use el candado, y siempre trabaje modo ingeniero, que no se
   pueda salir por ningun lado."

EL AGUJERO QUE TAPA: todos los candados de este taller son de Claude. Cline no los tiene. Y las
reglas escritas (.clinerules, CLAUDE.md) son CONTEXTO: se pueden ignorar. Ya paso con el
protocolo entero, escrito desde julio y saltado durante un dia completo.

ESTE ES DISTINTO: lo ejecuta GIT, no la IA. Da igual quien escriba el codigo — Claude, Cline,
otra IA o Julio a mano: para GUARDAR hay que pasar por aqui. No hay version educada de saltarselo.

QUE EXIGE, en este orden:
  1. Las VIGIAS del proyecto en VERDE. Guardar algo roto es lo que mas dano hace.
  2. Que no se guarden LLAVES. Un archivo de claves subido no se puede desubir.

LO QUE NO ESTORBA (o el candado se vuelve un muro y se acaba apagando, que es peor):
  - si el proyecto no tiene vigias, no se inventa una excusa: se deja pasar y se avisa
  - si las vigias no se pueden correr (falta pytest), se avisa y se deja pasar: no se atrapa
    a Julio por un problema de instalacion

LA UNICA SALIDA es `git commit --no-verify`, que es de git y no se puede quitar. Por eso cada
vez que este guardia FRENA queda apuntado, y cada vez que alguien pasa sin el, se nota: el
apunte no aparece.
"""
import os
import subprocess
import sys
import time
import json

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOSPECHOSOS = ("credencial", "credenciales", ".env", "secret", "password", ".key", ".pem")
LIBRETA = os.path.join("memoria", "GUARDIA.log")


def _apuntar(raiz, texto):
    """Deja rastro. A prueba de fallos: si no se puede escribir, el guardia NO se cae."""
    try:
        ruta = os.path.join(raiz, LIBRETA)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M") + "  " + texto + "\n")
    except Exception:
        pass


def _lo_que_se_va_a_guardar(raiz):
    try:
        r = subprocess.run(["git", "diff", "--cached", "--name-only"],
                           cwd=raiz, capture_output=True, text=True, timeout=60)
        return [l.strip() for l in (r.stdout or "").splitlines() if l.strip()]
    except Exception:
        return []


import re

# Como es una llave DE VERDAD. Se mira el CONTENIDO, no el nombre: un documento que HABLA de
# claves no lleva ninguna dentro, y frenarlo por el nombre es ruido. Paso el mismo dia que se
# escribio este guardia: freno el contrato que explica como se piden las claves.
PINTA_DE_LLAVE = re.compile(
    r"sk-[A-Za-z0-9]{16,}"
    r"|AIza[A-Za-z0-9_\-]{20,}"
    r"|gsk_[A-Za-z0-9]{20,}"
    r"|eyJ[A-Za-z0-9_\-]{30,}\.[A-Za-z0-9_\-]{20,}"
    r"|(password|contrasena|clave|secret)\s*[:=]\s*[\"']?[A-Za-z0-9!@#%^&*_\-]{8,}",
    re.IGNORECASE)

# Por el NOMBRE solo se frena lo que EXISTE para guardar llaves: la terminacion del archivo.
# Nada de frenar por que la palabra "credenciales" aparezca en el nombre: asi se freno el
# contrato que EXPLICA como se piden las claves, que no lleva ninguna. Una senal que salta con
# todo se vuelve ruido y se acaba ignorando, que es peor que no tenerla.
TERMINACIONES_DE_LLAVES = (".env", ".key", ".pem", ".pfx", ".p12")


def _hay_llaves(raiz, archivos):
    """Frena solo si de verdad hay una llave. Ya paso: el archivo de claves de Foto Informe
    esta subido a internet y no hay forma de desubirlo.

    DOS CAMINOS, a proposito:
      - por el NOMBRE: los archivos que solo existen para guardar llaves. No hace falta abrirlos.
      - por el CONTENIDO: cualquier otro donde asome algo con pinta de llave de verdad.
    Un documento que EXPLICA como se piden las claves no lleva ninguna: ese pasa.
    """
    malos = []
    for a in archivos:
        n = a.lower()
        if n.endswith(TERMINACIONES_DE_LLAVES) or "/.env" in n or n.startswith(".env"):
            malos.append(a + "   (archivo de llaves)")
            continue
        ruta = os.path.join(raiz, a.replace("/", os.sep))
        try:
            if os.path.getsize(ruta) > 2 * 1024 * 1024:
                continue                       # demasiado grande para ser un archivo de claves
            with open(ruta, encoding="utf-8", errors="ignore") as f:
                if PINTA_DE_LLAVE.search(f.read()):
                    malos.append(a + "   (lleva algo con pinta de llave DENTRO)")
        except Exception:
            continue                           # si no se puede leer, no se frena por eso
    return malos


def _cubierto_por_equipo(archivos):
    """Lo que se va a guardar lleva veredicto del equipo? (Julio, 2026-09-02)

    Asi el balance sabe, en cada guardado y sin que nadie lo cuente a mano, si esto fue del
    equipo o a mano. Devuelve True (equipo), False (a mano) o None (no toca codigo)."""
    codigo = [a for a in archivos
              if a.lower().endswith((".py", ".js", ".html", ".ts", ".jsx", ".tsx", ".css", ".sql"))]
    if not codigo:
        return None                                   # nada que atribuir: no toca codigo
    ruta = os.environ.get("INGENIERO_VEREDICTO_TEST") or \
        os.path.join(AQUI, "memoria", ".veredicto_equipo.json")
    try:
        d = json.load(open(ruta, encoding="utf-8"))
    except Exception:
        d = None
    if not d or str(d.get("veredicto", "")).upper() != "APROBADO":
        return False
    bases = set(os.path.basename(str(a)).lower() for a in d.get("archivos", []))
    return all(os.path.basename(a).lower() in bases for a in codigo)


def _apuntar_balance(raiz, tipo, archivos):
    """Deja una linea en el BALANCE.log: que hizo el equipo y que se hizo a mano. A prueba de
    fallos: si no se puede escribir, el guardia no se cae."""
    try:
        ruta = os.path.join(raiz, "memoria", "BALANCE.log")
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("%s | %s\n" % (tipo, ", ".join(archivos[:8])))
    except Exception:
        pass


def _vigias(raiz):
    """(paso, mensaje). Si no hay vigias o no se pueden correr, se DEJA PASAR con aviso."""
    carpeta = os.path.join(raiz, "vigias")
    if not os.path.isdir(carpeta):
        return True, "este proyecto no tiene vigias (se deja pasar)"
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "vigias/"],
                           cwd=raiz, capture_output=True, text=True, timeout=900)
    except Exception as e:
        return True, "no se pudieron correr las vigias (%s): se deja pasar" % str(e)[:60]
    salida = (r.stdout or "") + (r.stderr or "")
    ultima = [l for l in salida.splitlines() if l.strip()][-1:] or [""]
    if r.returncode == 0:
        return True, ultima[0].strip()
    if r.returncode == 5:
        return True, "no se recogio ninguna vigia (se deja pasar)"
    return False, ultima[0].strip()


def main():
    raiz = AQUI
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, timeout=30)
        if (r.stdout or "").strip():
            raiz = (r.stdout or "").strip().replace("/", os.sep)
    except Exception:
        pass

    archivos = _lo_que_se_va_a_guardar(raiz)

    llaves = _hay_llaves(raiz, archivos)
    if llaves:
        _apuntar(raiz, "FRENADO: intento de guardar llaves -> " + ", ".join(llaves[:4]))
        sys.stderr.write(
            "\nGUARDIA: NO SE GUARDA. Ibas a subir un archivo de LLAVES:\n"
            + "".join("   " + x + "\n" for x in llaves[:6])
            + "\n  Una clave subida NO se puede desubir. Ya paso una vez.\n"
              "  Sacala del guardado y ponla en la lista de lo que nunca se sube.\n\n")
        return 1

    paso, mensaje = _vigias(raiz)
    if not paso:
        _apuntar(raiz, "FRENADO: vigias rojas -> " + mensaje)
        sys.stderr.write(
            "\nGUARDIA: NO SE GUARDA. Hay pruebas ROJAS:\n"
            "   " + mensaje + "\n\n"
            "  No se guarda dejando algo roto. Da igual quien haya escrito el codigo.\n"
            "  Arreglalo y vuelve a guardar.\n\n")
        return 1

    # EL BALANCE (Julio, 2026-09-02): cada guardado apunta si fue del equipo o a mano, para que
    # nadie tenga que contar a mano cuanto trabaja cada quien (memoria/BALANCE.log).
    try:
        cub = _cubierto_por_equipo(archivos)
        if cub is True:
            _apuntar_balance(raiz, "equipo", archivos)
        elif cub is False:
            _apuntar_balance(raiz, "a_mano", archivos)
    except Exception:
        pass

    _apuntar(raiz, "OK: %d archivo(s) | %s" % (len(archivos), mensaje))
    sys.stderr.write("GUARDIA: verde. " + mensaje + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**EL FALLO QUE HAY QUE REPARAR AQUI:** `_apuntar()` y `_apuntar_balance()` escriben dentro de la
carpeta `memoria/`, que ESTA dentro del repositorio. Como este guardia corre justo ANTES de cada
guardado, cada guardado deja archivos modificados nuevos, y el candado de commit vuelve a pedir
guardar. Se muerde la cola.

---

## 3. `cerebro/router.py` — la funcion `armar()`

**Aviso importante:** `armar()` NO llama a ningun cerebro. Solo arma el material. Quien llama a
los cerebros es `_preguntar_con_relevo()` en `cuerpo/obrero.py`, que va en el punto 4.

```python
def armar(apodo, problema, k_trozos=6, saltos=1):
    g = grafo.cargar(apodo)
    hits = flujos.buscar(g["flujos"], problema)[:3]
    nombres = [h[0] for h in hits]

    # piezas del flujo
    ids = []
    for n in nombres:
        ids += g["flujos"].get(n, {}).get("piezas", [])
    ids = sorted(set(ids))
    fichas = [p for p in g["piezas"] if p["id"] in ids]

    # Si el flujo no toco ningun codigo, se buscan las piezas que HABLAN DEL PROBLEMA.
    #
    # Antes se cogian las TRES MAS GRANDES, por numero de lineas. Eso es elegir por tamano, y el
    # archivo mas gordo no es el que tiene el fallo: en el MVP, un problema de LA PANTALLA traia
    # el servidor (16.845 lineas) y la pantalla (2.349) no entraba NUNCA. El equipo lo dijo tres
    # veces seguidas: "el archivo app_web.html no esta en el material". Fallo real 2026-08-21.
    # Es ademas lo contrario de la regla de Julio: se busca por lo que la cosa HACE, no por como
    # de grande es.
    codigo = [f for f in fichas if f["rol"] in ("CUERPO", "CODIGO", "WEB", "CEREBRO")]
    if not codigo:
        candidatas = _las_que_hablan_del_problema(g, problema)
        fichas += candidatas
        codigo = candidatas

    # LO QUE EL PROBLEMA NOMBRA, ENTRA (Julio, 2026-08-27, ley L13/L14).
    # Cuando Julio (o el encargo) dice el nombre exacto de una parte del programa, esa parte DEBE
    # entrar al material. Hoy se ignora: se nombra "app_web.html" y el repartidor devuelve solo las
    # pruebas o vigias, no la pantalla; el equipo no puede revisar ni aprobar, y todo se atasca.
    # Regla general: se detectan en el texto del problema las rutas/archivos que existen en el grafo
    # del proyecto (p.ej. app_web.html, app.py, rv3_prueba_x.py), y se agregan al material. Aplica a
    # TODOS los proyectos: el ingeniero es el central y transmite a los demas. Es el pedazo que hace
    # falta, no el archivo entero (los hay de 16 mil renglones: ni caben ni sirven).
    # Se guarda en _nombrados para que su trozo se agregue despues de que exista `pedazos`.
    _nombrados = []
    try:
        import re as _re
        for m in _re.finditer(r"([A-Za-z0-9_\\/.\-]+\.(?:py|html|js|css|ts|json|md))", problema):
            pieza = m.group(1).replace("\\", "/")
            base = pieza.split("/")[-1]
            ficha = next((p for p in g["piezas"]
                          if p["id"].replace("\\", "/").endswith(pieza)
                          or p["id"].split("/")[-1] == base), None)
            if not ficha or ficha in codigo:
                continue
            codigo.append(ficha)
            if ficha not in fichas:
                fichas.append(ficha)
            _nombrados.append(ficha["id"])
    except Exception:
        _nombrados = []

    # LA CARA TAMBIEN ES DEL FLUJO (fallo real 2026-08-20, cazado por Qwen y Gemini).
    # El paquete del onboarding traia `cuerpo/perfil.py` (el motor) pero NO `web/` (la cara,
    # donde esta el formulario que de verdad guarda). Qwen: "no veo el codigo que invoca a
    # guardar_perfil". Ninguna de las 26 vigias lo vio: verde sobre un caso que no se vive.
    # Cura: QUIEN LLAMA a una pieza del flujo pertenece al flujo, aunque su nombre no lo diga.
    _, entra = enlaces.indexar(g["enlaces"])
    ya = {f["id"] for f in codigo}
    llamadores = []
    for f in list(codigo):
        for e in entra.get(f["id"], []):
            if e["tipo"] != "IMPORTA" or e["de"] in ya:
                continue
            fv = grafo.ficha(g, e["de"])
            if fv and fv["rol"] in ("WEB", "CODIGO", "CUERPO"):
                llamadores.append(fv)
                ya.add(fv["id"])
    # la cara primero: ahi suele estar el fallo que Julio ve con sus ojos
    llamadores.sort(key=lambda x: (x["rol"] != "WEB", -x["lineas"]))
    codigo += llamadores[:4]
    for f in llamadores[:4]:
        if f not in fichas:
            fichas.append(f)

    # EL DICCIONARIO (2026-08-25): si este problema YA se reparo antes, aqui esta
    # el sitio exacto del codigo, dicho en palabras de Julio. Es justo lo que la busqueda por
    # letras nunca logra (Julio habla espanol y de negocio; el codigo, ingles y comprimido). Se
    # agregan esos sitios PROBADOS al material, para que el paquete traiga el programa y no solo
    # las vigias recien escritas.
    diccionario_sitios = []
    try:
        sys.path.insert(0, AQUI)
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        from arnes import diccionario as _dic
        diccionario_sitios = _dic.buscar(problema, apodo)[:4]
        for sitio in diccionario_sitios:
            sufijo = str(sitio.get("archivo") or "").replace("\\", "/")
            if not sufijo:
                continue
            ficha = next((p for p in g["piezas"]
                          if p["id"].replace("\\", "/").endswith(sufijo)), None)
            if ficha and ficha not in codigo:
                codigo.append(ficha)
                if ficha not in fichas:
                    fichas.append(ficha)
    except Exception:
        pass

    # EL ROUTER SE CORRIGE SOLO (orden 3 de Julio, 2026-08-20).
    # Si en un problema del mismo flujo el paquete se quedo CORTO, el medidor apunto QUE falto.
    # Aqui se lee ese apunte y se mete esa pieza, para no repetir el mismo hueco dos veces.
    # Es lo que convierte el medidor en aprendizaje: medir sin corregir no sirve de nada.
    try:
        import re as _re
        sys.path.insert(0, AQUI)
        from cuerpo import medidor as _med
        for f in _med.lo_que_falto(apodo):
            if not (set(f.get("flujos", [])) & set(nombres)):
                continue
            for texto_falto in f.get("falto", []):
                for pieza in _re.findall(r"[\w/]+\.(?:py|html|js)", str(texto_falto)):
                    base = pieza.split("/")[-1]
                    extra = grafo.ficha(g, pieza) or next(
                        (p for p in g["piezas"] if p["id"].split("/")[-1] == base), None)
                    if extra and extra not in codigo:
                        codigo.append(extra)
                        if extra not in fichas:
                            fichas.append(extra)
    except Exception:
        pass

    claves = _claves_de(g, nombres)
    b = trozos.Buscador(codigo)
    # Se piden MAS candidatos de los que se van a entregar: los sobrantes son la materia prima
    # del re-ordenado por significado. Contar palabras es gratis; el significado se paga.
    pedazos = b.buscar(problema, k=k_trozos * 2, exigir=claves or None)
    if not pedazos:                       # el filtro de asunto puede ser muy duro: se afloja
        pedazos = b.buscar(problema, k=k_trozos * 2)

    # POR SIGNIFICADO, NO SOLO POR LETRAS (orden 4 de Julio, 2026-08-20).
    # Contar palabras no entiende sinonimos: el contrato dice "perfil" y el codigo "onboarding".
    # Se reordenan SOLO los candidatos que ya trajo el buscador (1 llamada, no 600), y si no
    # hay llave o cuota se queda el orden de siempre: nunca deja al Ingeniero sin buscador.
    if os.environ.get("INGENIERO_SIN_SIGNIFICADO", "").strip():
        pedazos = pedazos[:k_trozos]
    else:
        try:
            from . import semantico
            ...
```

A partir de ahi la funcion sigue unos 200 renglones mas del mismo estilo: reordena por
significado, monta las leyes que aplican, las vigias que protegen y la seccion "a quien puede
danar", y devuelve el paquete. Si hace falta ese trozo tambien, se pide aparte.

---

## 4. `cuerpo/obrero.py` — la funcion `_preguntar_con_relevo()` (aqui SI se llama a los cerebros)

```python
def _preguntar_con_relevo(prompt, temperatura, evitar=None, primero=None, pesado=False):
    """Pregunta respetando el orden de Julio: Qwen -> Gemini -> local, y VOLVIENDO a Qwen
    en cuanto despierte. Si uno se agota (429/cuota), se le marca la siesta y sigue el de al lado.
    Devuelve (texto, quien_contesto, avisos)."""
    c, _ = prestar_cerebro()
    if not c:
        return "", "", ["NO_ENCONTRADO: sin cerebro"]
    evitar_lista = evitar if isinstance(evitar, list) else [evitar] if evitar else []
    hay = [q for q in quienes_hay() if q not in evitar_lista]
    turnos = cuotas.fila(hay) or hay          # si todos duermen, se intenta igual (por si desperto ya)
    if primero and primero in turnos:         # el que reparte el trabajo cruzado manda
        turnos = [primero] + [q for q in turnos if q != primero]
    avisos = []
    vel = _velocidad()
    # DE UNA SOLA FUENTE, NUNCA A MANO (fallo real 2026-08-31, el que mas dinero costo ese dia).
    # Antes esta lista se escribia nombre por nombre, y quienes_hay() sacaba los suyos de otro
    # sitio: de `vel`. Dos listas que tenian que decir lo mismo y que nadie comparaba nunca.
    # Un nombre configurado entraba en la fila pero NO estaba aqui, asi que al hablarle el modelo
    # llegaba vacio, reventaba, el relevo lo contaba como un fallo mas y el ciclo se quedaba SIN
    # REVISOR: todo el trabajo caia en el cerebro de PAGO, pagandolo Julio, sin ninguna necesidad.
    # Anadir el nombre que faltaba habria tapado el caso de ese dia; manana se configura otro y
    # vuelve a pasar igual. Por eso ahora sale de la MISMA fuente: quien se configura, entra en la
    # fila Y se sabe como llamarle. No hay dos sitios que recordar.
    # Cada modelo de Groq es un cupo gratis distinto: Groq reparte POR MODELO, no por llave.
    modelos = {}
    for _quien in cuotas.ORDEN:
        # el de casa no se llama por internet: no tiene modelo que pedirle a nadie
        modelos[_quien] = None if _quien == "local" else vel.get("modelo_" + _quien)
    for k in vel:
        if k.startswith("modelo_router"):
            modelos[k[len("modelo_"):]] = vel[k]
    tope = float(vel.get("tope_segundos", 75))

    # EL DE PAGO NO ENTRA EN LA PREGUNTA A LA VEZ (auditoria de DeepSeek, 2026-08-21).
    # Abajo se les pregunta a TODOS A LA VEZ porque "son todos gratis, preguntar no cuesta".
    # Con DeepSeek dentro esa frase deja de ser cierta: se le pagaria una llamada en CADA
    # pregunta aunque contestase antes uno gratis. Lo cazo el propio DeepSeek al auditar esto.
    # Asi que se le aparta aqui y se le guarda para el ULTIMO RECURSO, a solas.
    de_pago = [q for q in turnos if q in cuotas.DE_PAGO]
    turnos = [q for q in turnos if q not in cuotas.DE_PAGO]
    # Salvo cuando el encargo es PESADO: ahi los gratis no aguantan y el de pago si entra.
    # SIEMPRE LO PESADO A DEEPSEEK (Julio, 2026-08-21): "el equipo que haga siempre lo pesado
    # deepseek, no lo olvides nunca." Repartir por TAMANO no bastaba: medido tres veces el mismo
    # dia, con encargos POR DEBAJO de TOPE_PESADO, los gratis devolvieron propuesta vacia, un 413
    # y texto ilegible. Se rendian igual. Por eso GENERAR (lo pesado) ya no se reparte por letras:
    # va a DeepSeek. AUDITAR (lo ligero) sigue siendo gratis, que es donde la ley de coste manda.
    if len(prompt) > TOPE_PESADO or pesado:
        turnos = de_pago + turnos
        de_pago = []
    # REPARTIDOR POR METRICAS (Julio, 2026-08-21): se asigna por eficiencia, no preguntando a
    # todos a la vez. `cuotas.rankear` ordena del mas eficiente al menos y SALTA a los que no
    # soportan el tamano. Asi no se gasta tokens en preguntar a quien no va a poder.
    turnos = cuotas.rankear(turnos, len(prompt))
    # DESPUES de rankear, nunca antes: rankear ordena por eficiencia y volveria a hundir al de
    # pago, deshaciendo la orden de Julio sin que se notara.
    # SI NO HAY LLAVE DE DEEPSEEK no pasa nada: no estara en `turnos`, esto no hace nada y el
    # relevo sigue con los gratis. Julio no se queda atrapado por no tener saldo.
    # SI DEEPSEEK FALLA tampoco pasa nada: comprobado en el bucle de abajo, cualquier fallo cae
    # en el `except` y PASA EL TURNO al siguiente. (Los dos cerebros avisaron de que aqui se
    # colgaria; se fue a mirar el codigo y los dos se equivocaban.)
    if pesado and "deepseek" in turnos:
        turnos = ["deepseek"] + [q for q in turnos if q != "deepseek"]
    # F2 (Julio 2026-08-24): NUNCA trabajar solo. Si la tarea es de VOLUMEN y DeepSeek (la mano
    # de pago) NO esta disponible, se BLOQUEA: no se cae a qwen/gemini para llenar el hueco.
    if pesado and "deepseek" not in [q for q in quienes_hay()]:
        return ("", "", [
            "BLOQUEADO F2 (Julio 2026-08-24): tarea de VOLUMEN y DeepSeek (la mano) no esta "
            "disponible. No se usa qwen/gemini para lo pesado. Habilita DeepSeek o reduce la tarea."])

    def _ultimo_recurso(avisos):
        """Se llama SOLO cuando ningun cerebro gratis pudo. Aqui empieza a costar dinero."""
        for quien in de_pago:
            try:
                txt = _con_tope(lambda: _pedirle_a(quien),
                                max(tope, cuotas.cuanto_esperarle(quien)))
                if not (txt or "").strip():
                    raise ValueError("contesto vacio")
                cuotas.apuntar_uso(quien, ok=True)
                avisos.append("no quedaba ningun cerebro gratis: contesto %s, que SE PAGA"
                              % cuotas.APODO[quien])
                return txt, quien, avisos
            except Exception as e:
                msg = str(e)
                cuotas.apuntar_uso(quien, ok=False)
                if cuotas.es_agote(msg):      # sin saldo cuenta como agotado: a dormir, no insistir
                    cuotas.dormir(quien, msg)
                avisos.append("%s fallo: %s" % (cuotas.APODO[quien], msg[:90]))
        return "", "", avisos + ["NO_ENCONTRADO: ningun cerebro pudo atender"]

    # SOLO CODIGO A LA NUBE (Julio, 2026-08-21). Se tapa AQUI, en el unico sitio por donde sale
    # todo, y no en cada sitio que llama: si depende de acordarse, un dia no se acuerda.
    # El cerebro de tu PC no cuenta: ahi no sale nada del ordenador.
    try:
        from cuerpo import privacidad as _pv
        prompt_nube, _tapados = _pv.limpiar(prompt)
        ...
```

A partir de ahi siguen unos 80 renglones mas: pregunta a todos los gratis A LA VEZ, el primero
que conteste gana, cada fallo apunta la siesta del que se agoto, y si ninguno puede se llama a
`_ultimo_recurso()`. Si hace falta ese trozo tambien, se pide aparte.

**EL FALLO QUE HAY QUE REPARAR AQUI:** existe una tabla medida de cuanto aguanta cada cerebro
(`memoria/CAPACIDADES.json`, con un dato `max` por cerebro). `cuotas.rankear` deberia saltarse a
los que no soportan el tamano, pero en la practica se les sigue llamando y devuelven vacio:
medido el 2026-09-01, cuatro cerebros seguidos sin contestar con un encargo grande.
