# -*- coding: utf-8 -*-
"""arnes/revisor_de_programa.py — EL OJO 2. Caza lo mecanico SIN gastar ni una IA.

SOLO HACE CUENTAS. El JUICIO sigue siendo del auditor de IA: si un cambio esta bien pensado,
si rompe a un vecino o si es una regresion, eso NO lo mira este programa. Se suma, no
sustituye. Lo que cambia es que lo mecanico deja de depender de que un cerebro se fije.

POR QUE NACE (dos fallos medidos el 2026-09-08, los dos con DOS cerebros delante):
  1. El equipo escribio una prueba que REVENTABA en la primera linea: usaba re sin haberlo
     importado. La aprobo un cerebro DISTINTO con "confianza alta". Se corrio y fallo.
  2. El equipo RECHAZO por invento las constantes que el propio encargo mandaba definir.

De lo que el auditor rechazo en un dia, casi todo era CUENTA, no juicio:
    "texto viejo y nuevo son identicos"  -> comparar
    "usa un nombre que no existe"        -> leer el codigo
    "no implementa lo que se pidio"      -> buscar un nombre
    "es una regresion total"             -> ESO SI es juicio: se queda para la IA

LEY: CONTRATO_CUENTA_O_JUICIO.md y CONTRATO_MENOS_IA_MAS_PROGRAMA.md (Julio).

Se usa asi:
    from arnes import revisor_de_programa
    fallos = revisor_de_programa.revisar(propuesta, tarea)
"""
import ast
import builtins
import os
import re
import sys
import textwrap

# Palabras con las que empieza un PEDAZO que vive dentro de otro bloque. Un texto que empieza
# asi no es un archivo entero y no se puede leer suelto, por mucho que este perfecto.
EMPIEZOS_DE_PEDAZO = ("else", "elif", "except", "finally", "case")


def es_un_pedazo(texto):
    """El texto es un PEDAZO de dentro de otro bloque, no un archivo entero?

    Se sabe por la forma, que es una cuenta: o viene sangrado desde el primer renglon, o
    empieza por una palabra que solo existe colgando de algo de mas arriba.
    """
    for linea in str(texto or "").splitlines():
        if not linea.strip():
            continue
        if linea[:1] in (" ", "\t"):
            return True
        primera = linea.strip().split()[0].rstrip(":") if linea.strip().split() else ""
        return primera in EMPIEZOS_DE_PEDAZO
    return False

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Los nombres propios de Python (round, len, print...). No son invento de nadie.
PROPIOS_DE_PYTHON = set(dir(builtins))
# Los duendes de MODULO: en todo .py existen (__file__, __name__, __package__...), como
# en el propio modulo builtins. dir(builtins) trae algunos pero NO __file__ (builtins no
# tiene archivo), y un .py normal SI: frenar por eso era una frenada en falso (2026-09-10).
PROPIOS_DE_PYTHON |= {"__file__", "__cached__", "__builtins__", "__annotations__",
                      "__package__", "__loader__", "__name__", "__doc__",
                      "__spec__", "__path__", "__debug__"}


def _quitar_comentario(linea):
    """Corta la linea en el primer numeral que este FUERA de comillas.

    Recorre caracter por caracter llevando si esta dentro de comillas simples o dobles,
    respetando la barra invertida que escapa la siguiente letra. Un numeral dentro de una
    cadena NO es un comentario y no se toca (freno en falso nº12, orden de Julio A-38 punto 3).
    """
    dentro = None
    i = 0
    while i < len(linea):
        c = linea[i]
        if c == "\\" and dentro is not None:
            i += 2
            continue
        if dentro is None:
            if c == "#":
                return linea[:i]
            if c == "'" or c == '"':
                dentro = c
        elif c == dentro:
            dentro = None
        i += 1
    return linea


def no_carga(contenido):
    """Devuelve la lista de textos con lo que impide cargar el modulo. Vacia = carga.

    Es CUENTA con ast, sin ejecutar nada. Mira, en orden, cada nodo del cuerpo del modulo:
    primero los nombres que se LEEN al cargar y despues los que DEFINE. Un nombre leido que
    no este definido ni importado arriba impide cargar el modulo.
    """
    import ast
    import builtins
    try:
        if contenido[:1] == chr(0xFEFF):
            contenido = contenido[1:]
        try:
            arbol = ast.parse(contenido)
        except SyntaxError as e:
            return ['EL ARCHIVO NO CARGA: error de sintaxis en la linea %s' % e.lineno]
        definidos = set(dir(builtins)) | {'__file__', '__name__', '__doc__'}
        fallos = []
        ya_dicho = set()
        for nodo in arbol.body:
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                partes = list(nodo.decorator_list)
                partes.extend(nodo.args.defaults)
                partes.extend(d for d in nodo.args.kw_defaults if d is not None)
            elif isinstance(nodo, ast.ClassDef):
                partes = list(nodo.decorator_list)
                partes.extend(nodo.bases)
                partes.extend(nodo.keywords)
            else:
                partes = [nodo]
                for n in ast.walk(nodo):
                    if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                        definidos.add(n.id)
                    elif isinstance(n, ast.ExceptHandler) and n.name:
                        definidos.add(n.name)
                    elif isinstance(n, ast.Import):
                        for a in n.names:
                            definidos.add((a.asname or a.name).split('.')[0])
                    elif isinstance(n, ast.ImportFrom):
                        for a in n.names:
                            definidos.add(a.asname or a.name.split('.')[0])
                    elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        definidos.add(n.name)
            for parte in partes:
                for n in ast.walk(parte):
                    if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                        if n.id not in definidos and n.id not in ya_dicho:
                            ya_dicho.add(n.id)
                            fallos.append('EL ARCHIVO NO CARGA: ' + n.id +
                                          ' se usa al cargar el modulo y no esta definido ni importado arriba')
            if isinstance(nodo, ast.Import):
                for a in nodo.names:
                    definidos.add((a.asname or a.name).split('.')[0])
            elif isinstance(nodo, ast.ImportFrom):
                for a in nodo.names:
                    definidos.add(a.asname or a.name.split('.')[0])
            elif isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                definidos.add(nodo.name)
            else:
                for n in ast.walk(nodo):
                    if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                        definidos.add(n.id)
        return fallos
    except Exception:
        return []


def sin_ruido(texto):
    """Quita comentarios, textos entre triples comillas y lineas en blanco.

    La misma idea que ya usan skills/cazar_el_humo.py y cuerpo/aplicador.py: no se duplica el
    criterio, se reusa. Sirve para comparar dos textos por lo que de verdad hacen.
    """
    t = str(texto or "")
    t = re.sub(r'(?m)^\s*[rRbBuUfF]*"""(?:.|\n)*?"""', " ", t)
    t = re.sub(r"(?m)^\s*[rRbBuUfF]*'''(?:.|\n)*?'''", " ", t)
    fuera = []
    for linea in t.splitlines():
        linea = _quitar_comentario(linea).strip()
        if linea:
            fuera.append(linea)
    return "\n".join(fuera)


def _conocidos(arbol):
    """Todo nombre que en ese texto SI existe: lo importado, lo definido, lo asignado, los
    argumentos, los de except y los de global. Mas los nombres propios de Python."""
    if arbol is None:
        return set()
    vistos = set(PROPIOS_DE_PYTHON)
    for n in ast.walk(arbol):
        if isinstance(n, ast.Import):
            for a in n.names:
                vistos.add((a.asname or a.name).split(".")[0])
        elif isinstance(n, ast.ImportFrom):
            for a in n.names:
                vistos.add(a.asname or a.name)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            vistos.add(n.name)
        elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            vistos.add(n.id)
        elif isinstance(n, ast.ExceptHandler) and n.name:
            vistos.add(n.name)
        elif isinstance(n, ast.arg):
            vistos.add(n.arg)
        elif isinstance(n, (ast.Global, ast.Nonlocal)):
            for nombre in n.names:
                vistos.add(nombre)
    return vistos


def _leidos(arbol):
    """Los nombres que el texto LEE: los que tienen que existir de antes."""
    if arbol is None:
        return []
    fuera = []
    for n in ast.walk(arbol):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
            fuera.append(n.id)
    return fuera


def _piezas(arbol):
    """Los nombres de funcion y de clase que hay en ese texto, en el orden en que salen.

    Es la cuenta que faltaba. Comparando esta lista antes y despues se ve, sin gastar ni una
    IA, si un cambio se lleva por delante algo que ya estaba. Se miran tambien las de dentro
    (los metodos de una clase), porque el 2026-09-11 lo que desaparecio fue justo eso.
    """
    if arbol is None:
        return []
    fuera = []
    for n in ast.walk(arbol):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if n.name not in fuera:
                fuera.append(n.name)
    return fuera




def revisar(propuesta, tarea=""):
    """Las cuatro cuentas. Devuelve una LISTA de frases; vacia si no encuentra nada.

    NUNCA lanza: si algo raro pasa, lo dice como un fallo mas y sigue. Un revisor que revienta
    deja pasar todo, que es lo contrario de para lo que existe.
    """
    fallos = []
    try:
        p = propuesta if isinstance(propuesta, dict) else {}
        viejo = str(p.get("texto_viejo") or "")
        nuevo = str(p.get("texto_nuevo") or p.get("codigo") or "")
        tarea = str(tarea or "")
        # un cambio de varios trozos (lista cambios, ordenes 55-60) se revisa trozo a trozo con las mismas cuentas;
        # sin esto se miraban texto_viejo y texto_nuevo de arriba, vacios, y se acusaba en falso (medido 2026-09-21, orden 95).
        if isinstance(p.get("cambios"), list) and p.get("cambios"):
            todos = []
            for c in p.get("cambios"):
                if not isinstance(c, dict):
                    continue
                sub = dict(p)
                sub.pop("cambios", None)
                sub.pop("codigo", None)
                sub["archivo"] = c.get("archivo") or p.get("archivo")
                sub["texto_viejo"] = c.get("texto_viejo", "")
                sub["texto_nuevo"] = c.get("texto_nuevo", "")
                todos.extend(revisar(sub, tarea))
            # la palabra del encargo basta con que este en alguno de los trozos (medido 2026-09-22, orden 95)
            juntos = ""
            for p in (p.get("cambios") or []):
                if isinstance(p, dict):
                    juntos += str(p.get("texto_viejo") or "") + str(p.get("texto_nuevo") or "")
            todos = [f for f in todos if not (f.startswith('NO HACE LO QUE SE PIDIO') and f.split(chr(39))[1] in juntos)]
            return todos

        # Un cambio que SOLO BORRA es legitimo: quitar codigo que sobra y no poner nada en su
        # lugar es trabajo de verdad. Solo no hay nada que hacer cuando tampoco se dice que quitar.
        # Esta cuenta va PRIMERO porque es la mas barata de todas: si el texto viejo que dice
        # cambiar no aparece tal cual en el archivo, lo que se propone no existe y seguramente
        # se adivino lo que hay mas alla del pedazo que se mando. Hay que pedir el archivo
        # completo antes de proponer. Si algo falla aqui, no se dice nada y se sigue.
        try:
            _ruta_v = str(p.get("archivo") or "")
            if viejo.strip() and _ruta_v and os.path.isfile(_ruta_v):
                with open(_ruta_v, encoding="utf-8", errors="replace") as _fv:
                    _contenido_v = _fv.read()
                if viejo not in _contenido_v:
                    return ["EL TEXTO VIEJO NO ESTA EN EL ARCHIVO: lo que se dice cambiar no existe "
                            "tal cual. Seguramente se adivino lo que hay mas alla del pedazo que se "
                            "mando. Hay que pedir el archivo completo antes de proponer."]
        except Exception:
            pass

        if not nuevo.strip() and not viejo.strip():
            return ["La propuesta no trae texto nuevo: no hay nada que aplicar."]
        # 2c — SE QUEDA SIN CUERPO: una prueba que se queda con su docstring y nada mas
        # PASA SIEMPRE. El candado sigue en su sitio pero ya no vigila nada y nadie se entera.
        # Medido el 2026-09-20: un cambio del equipo se comio el cuerpo entero de una prueba
        # ya guardada. Es CUENTA: se comparan los cuerpos de las funciones test_ antes y
        # despues. Si algo falla aqui, no se agrega nada y se sigue como siempre.
        try:
            _ruta_c = str(p.get("archivo") or "")
            if (_ruta_c.lower().endswith(".py") and os.path.isfile(_ruta_c)
                    and viejo.strip()):
                with open(_ruta_c, encoding="utf-8-sig", errors="replace") as _fc:
                    _antes_c = _fc.read()
                if viejo in _antes_c:
                    _despues_c = _antes_c.replace(viejo, nuevo, 1)
                    _arbol_antes_c = ast.parse(_antes_c)
                    _arbol_despues_c = ast.parse(_despues_c)
                    # Se busca la funcion suelta del archivo a proposito: mas abajo se escribe
                    # una con el mismo nombre dentro de esta funcion y eso taparia a la de fuera.
                    # Se escribe entero aqui a proposito, sin llamar a ninguna funcion de
                    # fuera, porque mas abajo hay otra con el mismo nombre dentro de esta
                    # misma funcion y eso la taparia.
                    def _vacia_aqui(nodo):
                        cuerpo = list(nodo.body)
                        if (cuerpo and isinstance(cuerpo[0], ast.Expr)
                                and isinstance(cuerpo[0].value, ast.Constant)
                                and isinstance(cuerpo[0].value.value, str)):
                            cuerpo = cuerpo[1:]
                        if not cuerpo:
                            return True
                        if len(cuerpo) == 1 and isinstance(cuerpo[0], ast.Pass):
                            return True
                        return False
                    _sin_antes = {n.name for n in ast.walk(_arbol_antes_c)
                                  if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                                  and n.name.startswith("test_") and _vacia_aqui(n)}
                    _sin_despues = {n.name for n in ast.walk(_arbol_despues_c)
                                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                                    and n.name.startswith("test_") and _vacia_aqui(n)}
                    for _nombre in sorted(_sin_despues - _sin_antes):
                        fallos.append(
                            "SE QUEDA SIN CUERPO: la prueba '%s' tenia cuerpo antes y ahora "
                            "no tiene nada o solo pass. Una prueba sin cuerpo PASA SIEMPRE: "
                            "el candado sigue en su sitio pero deja de vigilar y nadie lo nota."
                            % _nombre)
        except Exception:
            pass

        if not nuevo.strip():
            # Solo se borra: las demas cuentas suponen que hay codigo nuevo que leer, asi que
            # se devuelve la lista de fallos tal como va, sin mirar mas cuentas.
            return fallos

        # 0 — SIMULADORES: una prueba con simuladores no prueba la pieza de verdad.
        if re.search(r'MagicMock|unittest\.mock|\bMock\w*', nuevo):
            fallos.append('USA SIMULADOR (Mock) EN VEZ DE LO REAL: una prueba con simuladores no prueba la pieza de verdad.')

        # 1 — HUMO: el cambio solo toca comentarios y no repara nada.
        if viejo.strip() and sin_ruido(viejo) == sin_ruido(nuevo):
            fallos.append("HUMO: quitando comentarios y lineas en blanco, el texto nuevo es "
                          "IGUAL al viejo. Ese cambio no repara nada.")

        # 2 — SINTAXIS: si queda roto, no se puede aplicar ni se puede seguir leyendo.
        #
        # OJO, FRENADA EN FALSO CAZADA EL 2026-09-08 la primera vez que este revisor se uso
        # con trabajo de verdad: el equipo entrego un PEDAZO que empieza a media altura
        # (dentro de otro bloque, con su sangria y empezando por else). No estaba roto: es un
        # pedazo, no un archivo entero. Y este revisor grito "el codigo queda roto".
        # Su propia vigia lo dice: un candado que frena lo legitimo es PEOR que no tenerlo,
        # porque ensena a ignorarlos todos. Por eso, si es un pedazo y no se deja leer entero,
        # NO se acusa de nada: no se puede comprobar, y callar es mas honrado que gritar.
        arbol = None
        _ruta_js = str(p.get('archivo') or '')
        _es_js = _ruta_js.lower().endswith(('.js', '.mjs', '.cjs'))
        if _es_js:
            _texto_js = None
            if es_un_pedazo(nuevo) and _ruta_js and os.path.isfile(_ruta_js) and viejo:
                try:
                    with open(_ruta_js, encoding='utf-8-sig', errors='replace') as _fj:
                        _todo_js = _fj.read()
                    if viejo in _todo_js:
                        _texto_js = _todo_js.replace(viejo, nuevo, 1)
                except Exception:
                    _texto_js = None
            elif not es_un_pedazo(nuevo):
                _texto_js = nuevo
            if _texto_js is not None:
                _sufijo = os.path.splitext(_ruta_js)[1] or '.js'
                if _sufijo == '.js' and re.search(r'(?m)^\s*(import|export)\b', _texto_js):
                    _sufijo = '.mjs'
                _tmp_js = None
                try:
                    import tempfile
                    import subprocess
                    _fd, _tmp_js = tempfile.mkstemp(suffix=_sufijo)
                    with os.fdopen(_fd, 'w', encoding='utf-8') as _ftmp:
                        _ftmp.write(_texto_js)
                    _flags = 0x08000000 if os.name == 'nt' else 0
                    _res = subprocess.run(['node', '--check', _tmp_js], capture_output=True, text=True, timeout=20, shell=False, creationflags=_flags)
                    if _res.returncode != 0:
                        fallos.append('EL CODIGO QUEDA ROTO (node): ' + (_res.stderr or '')[:200])
                        return fallos
                except FileNotFoundError:
                    pass
                except Exception:
                    pass
                finally:
                    if _tmp_js:
                        try:
                            os.remove(_tmp_js)
                        except Exception:
                            pass
        try:
            _es_py = (not _ruta_js) or str(_ruta_js).lower().endswith('.py')
            arbol = ast.parse(nuevo) if _es_py else None
        except SyntaxError as e:
            try:
                arbol = ast.parse(textwrap.dedent(nuevo))
            except SyntaxError:
                # FRENADA EN FALSO CAZADA EL 2026-09-14: un trozo que acababa donde empieza la funcion
                # siguiente no se dejaba leer suelto y se acuso de roto, aunque el archivo completo quedaba
                # bien. Antes de acusar, se lee el archivo tal como quedaria con el cambio.
                _completo = None
                try:
                    _ruta_s = str(p.get("archivo") or "")
                    if _ruta_s and os.path.isfile(_ruta_s) and viejo:
                        with open(_ruta_s, encoding="utf-8-sig", errors="replace") as _fs:
                            _todo = _fs.read()
                        if viejo in _todo:
                            _completo = _todo.replace(viejo, nuevo, 1)
                except Exception:
                    _completo = None
                if _completo is not None:
                    try:
                        arbol = ast.parse(_completo)
                    except SyntaxError as e2:
                        fallos.append("EL CODIGO QUEDA ROTO en el renglon %s del archivo completo: %s. Asi no arranca."
                                      % (getattr(e2, "lineno", "?"), e2.msg))
                        return fallos
                else:
                    if es_un_pedazo(nuevo):
                        return fallos       # pedazo suelto: no hay nada que se pueda comprobar
                    fallos.append("EL CODIGO QUEDA ROTO en el renglon %s: %s. Asi no arranca."
                                  % (getattr(e, "lineno", "?"), e.msg))
                    return fallos
        except Exception as e:
            fallos.append("No se pudo leer el codigo nuevo: %s" % str(e)[:120])
            return fallos

        # Lo que esta dentro de un texto entre comillas no es codigo de este archivo: juzgarlo
        # como codigo frena trabajo bueno.
        try:
            _ruta_txt = str(p.get("archivo") or "")
            if (_ruta_txt.lower().endswith(".py") and os.path.isfile(_ruta_txt)
                    and viejo.strip()):
                with open(_ruta_txt, encoding="utf-8-sig", errors="replace") as _ftx:
                    _todo_tx = _ftx.read()
                _pos_tx = _todo_tx.find(viejo)
                if _pos_tx >= 0:
                    _renglon_tx = _todo_tx.count("\n", 0, _pos_tx) + 1
                    _arbol_tx = ast.parse(_todo_tx)
                    for _nodo_tx in ast.walk(_arbol_tx):
                        if (isinstance(_nodo_tx, ast.Constant)
                                and isinstance(_nodo_tx.value, str)
                                and getattr(_nodo_tx, "lineno", None) is not None
                                and getattr(_nodo_tx, "end_lineno", None) is not None):
                            if _nodo_tx.lineno <= _renglon_tx <= _nodo_tx.end_lineno:
                                return fallos
        except Exception:
            pass

        # 3b — IMPORTA ARRIBA ALGO QUE NO EXISTE EN SU MODULO. Una prueba que hace
        # `from modulo import nombre` arriba del archivo, y ese nombre no existe en el modulo,
        # revienta la RECOGIDA de pytest: toda la bateria queda en un solo error y no se sabe
        # que estaba roto. Medido el 2026-09-20. Si el nombre SI existe, no se dice nada. Si el
        # modulo no se puede leer, no se dice nada: cuando no se puede comprobar, se calla.
        try:
            _ruta_mp = str(p.get("archivo") or "")
            if _ruta_mp.lower().endswith(".py") and os.path.isfile(_ruta_mp) and viejo.strip():
                with open(_ruta_mp, encoding="utf-8-sig", errors="replace") as _fmp:
                    _antes_mp = _fmp.read()
                if viejo in _antes_mp:
                    _despues_mp = _antes_mp.replace(viejo, nuevo, 1)
                    try:
                        _arbol_mp = ast.parse(_despues_mp)
                    except Exception:
                        _arbol_mp = None
                    if _arbol_mp is not None:
                        _dir_mp = os.path.dirname(_ruta_mp)
                        for _nodo_mp in ast.walk(_arbol_mp):
                            if not isinstance(_nodo_mp, ast.Call):
                                continue
                            _fn_mp = _nodo_mp.func
                            if not isinstance(_fn_mp, ast.Attribute):
                                continue
                            if _fn_mp.attr != "setattr":
                                continue
                            _base_mp = _fn_mp.value
                            if not isinstance(_base_mp, ast.Attribute):
                                continue
                            if _base_mp.attr != "monkeypatch":
                                continue
                            if len(_nodo_mp.args) < 2:
                                continue
                            _mod_arg = _nodo_mp.args[0]
                            _nom_arg = _nodo_mp.args[1]
                            if not isinstance(_mod_arg, ast.Constant) or not isinstance(_mod_arg.value, str):
                                continue
                            _nom_pedido = _nodo_mp.args[1]
                            if not isinstance(_nom_pedido, ast.Constant) or not isinstance(_nom_pedido.value, str):
                                continue
                            _mod_nombre = _mod_arg.value
                            _nom_pedido = _nom_pedido.value
                            _ruta_mod_mp = os.path.join(_dir_mp, *_mod_nombre.split(".")) + ".py"
                            if not os.path.isfile(_ruta_mod_mp):
                                continue
                            try:
                                with open(_ruta_mod_mp, encoding="utf-8-sig", errors="replace") as _fmod_mp:
                                    _fuente_mod_mp = _fmod_mp.read()
                                _arbol_mod_mp = ast.parse(_fuente_mod_mp)
                            except Exception:
                                continue
                            _nombres_mod_mp = set()
                            for _n_mp in _arbol_mod_mp.body:
                                if isinstance(_n_mp, ast.Import):
                                    for _a_mp in _n_mp.names:
                                        _nombres_mod_mp.add((_a_mp.asname or _a_mp.name).split(".")[0])
                                elif isinstance(_n_mp, ast.ImportFrom):
                                    for _a_mp in _n_mp.names:
                                        _nombres_mod_mp.add(_a_mp.asname or _a_mp.name)
                                elif isinstance(_n_mp, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                                    _nombres_mod_mp.add(_n_mp.name)
                                elif isinstance(_n_mp, ast.Assign):
                                    for _t_mp in _n_mp.targets:
                                        if isinstance(_t_mp, ast.Name):
                                            _nombres_mod_mp.add(_t_mp.id)
                            if _nom_pedido not in _nombres_mod_mp:
                                fallos.append(
                                    "MONKEYPATCH A UN NOMBRE QUE EL MODULO NO IMPORTA: la prueba "
                                    "hace monkeypatch.setattr('%s', '%s', ...) pero '%s' no se "
                                    "importa arriba de %s. Ese apartado revienta con "
                                    "AttributeError y la prueba no mediria nada. Hay que apartar "
                                    "la funcion en su propio modulo."
                                    % (_mod_nombre, _nom_pedido, _nom_pedido, _ruta_mod_mp))
                                continue
                            if not isinstance(_nom_arg, ast.Constant) or not isinstance(_nom_arg.value, str):
                                continue
                            _mod_nombre = _mod_arg.value
                            _nom_pedido = _nom_arg.value
                            if not _mod_nombre or not _nom_pedido:
                                continue
                            _ruta_mod_mp = os.path.join(_dir_mp, *_mod_nombre.split(".")) + ".py"
                            if not os.path.isfile(_ruta_mod_mp):
                                continue
                            try:
                                with open(_ruta_mod_mp, encoding="utf-8-sig", errors="replace") as _fmm:
                                    _arbol_mod_mp = ast.parse(_fmm.read())
                            except Exception:
                                continue
                            _nombres_mod_mp = set()
                            for _n_mp in ast.walk(_arbol_mod_mp):
                                if isinstance(_n_mp, ast.ImportFrom):
                                    for _al_mp in _n_mp.names:
                                        _nombres_mod_mp.add(_al_mp.asname or _al_mp.name)
                                elif isinstance(_n_mp, ast.Import):
                                    for _al_mp in _n_mp.names:
                                        _nombres_mod_mp.add(_al_mp.asname or _al_mp.name.split(".")[0])
                                elif isinstance(_n_mp, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                                    _nombres_mod_mp.add(_n_mp.name)
                                elif isinstance(_n_mp, ast.Assign):
                                    for _t_mp in _n_mp.targets:
                                        if isinstance(_t_mp, ast.Name):
                                            _nombres_mod_mp.add(_t_mp.id)
                            if _nom_pedido not in _nombres_mod_mp:
                                fallos.append(
                                    "MONKEYPATCH A UN NOMBRE QUE EL MODULO NO IMPORTA: la prueba "
                                    "hace monkeypatch.setattr('%s', '%s', ...) pero '%s' no se "
                                    "importa arriba de %s. Ese apartado revienta con "
                                    "AttributeError y la prueba no mediria nada. Hay que apartar "
                                    "la funcion en su propio modulo."
                                    % (_mod_nombre, _nom_pedido, _nom_pedido, _ruta_mod_mp))
        except Exception:
            pass

        try:
            _ruta_imp = str(p.get("archivo") or "")
            if _ruta_imp.lower().endswith(".py") and os.path.isfile(_ruta_imp) and viejo.strip():
                with open(_ruta_imp, encoding="utf-8-sig", errors="replace") as _fimp:
                    _antes_imp = _fimp.read()
                if viejo in _antes_imp:
                    _despues_imp = _antes_imp.replace(viejo, nuevo, 1)
                    try:
                        _arbol_imp = ast.parse(_despues_imp)
                    except Exception:
                        _arbol_imp = None
                    if _arbol_imp is not None:
                        _dir_imp = os.path.dirname(_ruta_imp)
                        for _nodo_imp in ast.walk(_arbol_imp):
                            if not isinstance(_nodo_imp, ast.ImportFrom):
                                continue
                            if _nodo_imp.level and _nodo_imp.level > 0:
                                continue
                            _mod_imp = _nodo_imp.module or ""
                            if not _mod_imp:
                                continue
                            _ruta_mod = os.path.join(_dir_imp, *_mod_imp.split(".")) + ".py"
                            if not os.path.isfile(_ruta_mod):
                                continue
                            try:
                                with open(_ruta_mod, encoding="utf-8-sig", errors="replace") as _fm:
                                    _arbol_mod = ast.parse(_fm.read())
                            except Exception:
                                continue
                            _nombres_mod = set()
                            for _n in ast.walk(_arbol_mod):
                                if isinstance(_n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                                    _nombres_mod.add(_n.name)
                                elif isinstance(_n, ast.Assign):
                                    for _t in _n.targets:
                                        if isinstance(_t, ast.Name):
                                            _nombres_mod.add(_t.id)
                                elif isinstance(_n, ast.AnnAssign) and isinstance(_n.target, ast.Name):
                                    _nombres_mod.add(_n.target.id)
                                elif isinstance(_n, (ast.Import, ast.ImportFrom)):
                                    for _a in _n.names:
                                        _nombres_mod.add(_a.asname or _a.name.split(".")[0])
                            for _alias in _nodo_imp.names:
                                if _alias.name == "*":
                                    continue
                                if _alias.name not in _nombres_mod:
                                    fallos.append(
                                        "IMPORTA ALGO QUE NO EXISTE: '%s' no esta en '%s'. "
                                        "Eso para la recogida de pytest y deja ciega a toda la "
                                        "bateria: hay que importarlo dentro de cada prueba."
                                        % (_alias.name, _mod_imp))
        except Exception:
            pass

        # 3 — USA UN NOMBRE QUE NO EXISTE. El fallo real del 2026-09-08: re sin importar.
        #
        # SOLO SI ES UN ARCHIVO ENTERO. Segunda frenada en falso cazada el mismo dia: se
        # reviso un PEDAZO del interior de una funcion y el revisor grito que perfil,
        # objetivo, camp, experimentos e hipotesis "no existen". Existen todos: son los datos
        # que recibe la funcion de mas arriba y lo que se importa al principio del archivo.
        # Mirando un pedazo suelto no se puede ver nada de eso, asi que acusar es mentir.
        # Cuando no se puede comprobar, se calla. Frenar lo bueno ensena a ignorar los frenos.
        # 2b — NO CARGA: si el archivo tal como quedaria no arranca, se dice aqui.
        # Es CUENTA con no_carga, sin ejecutar nada. Solo se avisa si ANTES cargaba y DESPUES
        # no: si antes ya no cargaba, no lo rompio este cambio y no se dice nada.
        try:
            _ruta_nc = str(p.get("archivo") or "")
            if (_ruta_nc.lower().endswith(".py") and os.path.isfile(_ruta_nc)
                    and viejo.strip()):
                with open(_ruta_nc, encoding="utf-8-sig", errors="replace") as _fnc:
                    _antes_nc = _fnc.read()
                if viejo in _antes_nc:
                    _despues_nc = _antes_nc.replace(viejo, nuevo, 1)
                    _fallos_antes = no_carga(_antes_nc)
                    _fallos_despues = no_carga(_despues_nc)
                    if not _fallos_antes and _fallos_despues:
                        fallos.append(
                            "NO CARGA: el archivo se queda sin arrancar. Primera razon: %s"
                            % _fallos_despues[0])
        except Exception:
            pass

        # 2c — SE QUEDA SIN CUERPO: una prueba que se queda con su docstring y nada mas
        # PASA SIEMPRE. El candado sigue en su sitio pero ya no vigila nada y nadie se entera.
        # Medido el 2026-09-20: un cambio del equipo se comio el cuerpo entero de una prueba
        # ya guardada. Es CUENTA: se comparan los cuerpos de las funciones test_ antes y
        # despues. Si algo falla aqui, no se agrega nada y se sigue como siempre.
        try:
            _ruta_c = str(p.get("archivo") or "")
            if (_ruta_c.lower().endswith(".py") and os.path.isfile(_ruta_c)
                    and viejo.strip()):
                with open(_ruta_c, encoding="utf-8-sig", errors="replace") as _fc:
                    _antes_c = _fc.read()
                if viejo in _antes_c:
                    _despues_c = _antes_c.replace(viejo, nuevo, 1)
                    _arbol_antes_c = ast.parse(_antes_c)
                    _arbol_despues_c = ast.parse(_despues_c)

                    def _cuerpo_vacio(_nodo):
                        _cuerpo = list(_nodo.body)
                        if (_cuerpo and isinstance(_cuerpo[0], ast.Expr)
                                and isinstance(_cuerpo[0].value, ast.Constant)
                                and isinstance(_cuerpo[0].value.value, str)):
                            _cuerpo = _cuerpo[1:]
                        if not _cuerpo:
                            return True
                        if len(_cuerpo) == 1 and isinstance(_cuerpo[0], ast.Pass):
                            return True
                        return False

                    def _pruebas_sin_cuerpo(_arbol):
                        _sin = set()
                        for _n in ast.walk(_arbol):
                            if (isinstance(_n, (ast.FunctionDef, ast.AsyncFunctionDef))
                                    and _n.name.startswith("test_")
                                    and _cuerpo_vacio(_n)):
                                _sin.add(_n.name)
                        return _sin

                    _sin_antes = _pruebas_sin_cuerpo(_arbol_antes_c)
                    _sin_despues = _pruebas_sin_cuerpo(_arbol_despues_c)
                    for _nombre in sorted(_sin_despues - _sin_antes):
                        fallos.append(
                            "SE QUEDA SIN CUERPO: la prueba '%s' tenia cuerpo antes y ahora "
                            "no tiene nada o solo pass. Una prueba sin cuerpo PASA SIEMPRE: "
                            "el candado sigue en su sitio pero deja de vigilar y nadie lo nota."
                            % _nombre)
        except Exception:
            pass

        if es_un_pedazo(nuevo):
            return fallos
        conocidos = set(_conocidos(arbol))
        # FRENADA EN FALSO CAZADA EL 2026-09-13: acusaba de no existir a os y sys, que estaban importados
        # mas arriba del archivo, fuera del trozo. Si el archivo existe y el trozo viejo esta en el, los
        # nombres se comprueban tambien sobre el archivo tal como quedaria despues del cambio.
        try:
            _ruta_total = str(p.get("archivo") or "")
            if _ruta_total and os.path.isfile(_ruta_total) and viejo:
                with open(_ruta_total, encoding="utf-8-sig", errors="replace") as _ft:
                    _contenido_total = _ft.read()
                if viejo in _contenido_total:
                    _arbol_total = ast.parse(_contenido_total.replace(viejo, nuevo, 1))
                    conocidos = conocidos | set(_conocidos(_arbol_total))
        except Exception:
            pass
        ya_dicho = set()
        for nombre in _leidos(arbol):
            if nombre not in conocidos and nombre not in ya_dicho:
                ya_dicho.add(nombre)
                fallos.append("USA UN NOMBRE QUE NO EXISTE: '%s'. No se importa, no se define "
                              "y no es de Python. En cuanto se corra, revienta." % nombre)

        # 4 — NO HACE LO QUE SE PIDIO. Solo se miran las palabras con guion bajo dentro: son
        # nombres de funcion o de dato. Las palabras normales del castellano se ignoran, porque
        # si no, "reparar" o "impuesto" darian frenadas en falso.
        # FRENADA EN FALSO CAZADA EL 2026-09-08, en la primera mordida de verdad: un encargo
        # nombra archivos (cuerpo/campana_flujo.py) y palabras del propio encargo
        # (texto_viejo, texto_nuevo). Esas NO son funciones que la reparacion deba tocar, y
        # contarlas frena trabajos buenos. Un candado que frena lo legitimo ensena a ignorar
        # todos los candados. Por eso se quitan antes de mirar.
        limpia = re.sub(r"[\w/\\.]+\.(?:py|md|json|txt|js|html|css|sql|cfg|config)\b", " ", tarea)
        for jerga in ("texto_viejo", "texto_nuevo"):
            limpia = limpia.replace(jerga, " ")
        # FRENADA EN FALSO CAZADA EL 2026-09-13: la ruta de la carpeta de la herramienta y el nombre del
        # plan frenaban rondas buenas. Se quitan las rutas de Windows y los nombres de archivo con guiones,
        # y si el archivo que se cambia EXISTE, solo cuentan las palabras que estan en ese archivo: las demas
        # son contexto del encargo. Si no existe, se sigue como antes. Lo vigila la vigia del revisor.
        limpia = re.sub(r"[A-Za-z]:\\[^\s,;]*", " ", limpia)
        limpia = re.sub(r"[\w/\\.-]+\.(?:py|md|json|txt|js|html|css|sql|cfg|config)\b", " ", limpia)
        contenido_archivo = None
        try:
            ruta_archivo = str(p.get("archivo") or "")
            if ruta_archivo and os.path.isfile(ruta_archivo):
                with open(ruta_archivo, encoding="utf-8-sig", errors="replace") as fa:
                    contenido_archivo = fa.read()
        except Exception:
            contenido_archivo = None
        # FRENADA EN FALSO CAZADA EL 2026-09-14: al CREAR un archivo nuevo contaba como obligatoria cualquier
        # palabra del encargo, aunque solo contara como esta hoy otro archivo, y tiro una vigia ya aprobada.
        # Al crear no se puede separar lo pedido del contexto: ese juicio es del revisor de IA.
        _creando_archivo_nuevo = contenido_archivo is None and not (viejo or "").strip()
        # FRENADA EN FALSO CAZADA EL 2026-09-30: el encargo nombra piezas dentro del apartado de lo
        # que NO SE TOCA, precisamente para protegerlas, y el revisor las exigia igual. Decir "esto
        # no se toca" hacia que el trabajo se rechazara, y hubo que renunciar a proteger al vecino
        # para que pasara. Se quita ese apartado del texto antes de buscar palabras obligatorias.
        limpia = re.sub(r"(?is)NO SE TOCA\s*:.*?(?=\n[A-Z][A-Z ]{2,}\s*:|\Z)", " ", limpia)
        for palabra in set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*_[A-Za-z0-9_]*\b", limpia)):
            if _creando_archivo_nuevo:
                break
            if contenido_archivo is not None and palabra not in contenido_archivo:
                continue
            if palabra not in viejo and palabra not in nuevo:
                fallos.append("NO HACE LO QUE SE PIDIO: el encargo habla de '%s' y esa palabra "
                              "no aparece ni en el texto viejo ni en el nuevo." % palabra)

        # 5 — DESAPARECE LO QUE YA ESTABA. EL AGUJERO MEDIDO EL 2026-09-11: este revisor
        # vigilaba que lo NUEVO estuviera bien y NO vigilaba que lo VIEJO siguiera ahi. Por
        # ese hueco se perdio la puerta del jefe que coordina del DMM (paso de 81 a 56
        # renglones sin guardar) y NINGUN guardia dijo nada: las 526 vigias siguieron verdes.
        # Ni el revisor, ni el que aplica los cambios, ni el copista miraban los borrados.
        #
        # Es una CUENTA, no un juicio: se listan los nombres de funcion y de clase de cada
        # texto y se dice cuales estaban y ya no estan. SI es querido borrarlos, se dice y se
        # sigue; lo que no puede pasar es que se pierdan en silencio.
        #
        # SOLO SI LOS DOS TEXTOS SON ARCHIVOS ENTEROS QUE SE DEJAN LEER. Con un pedazo suelto
        # no se puede comparar nada y acusar seria mentir: es la misma leccion de las dos
        # frenadas en falso del 2026-09-08. Cuando no se puede comprobar, se calla.
        if viejo.strip() and not es_un_pedazo(viejo):
            arbol_viejo = None
            try:
                arbol_viejo = ast.parse(viejo)
            except SyntaxError:
                try:
                    arbol_viejo = ast.parse(textwrap.dedent(viejo))
                except SyntaxError:
                    arbol_viejo = None
            except Exception:
                arbol_viejo = None
            if arbol_viejo is not None:
                quedan = _piezas(arbol)
                perdidas = [n for n in _piezas(arbol_viejo) if n not in quedan]
                # decirlo por escrito es que el propio encargo nombre la pieza que se va
                perdidas = [n for n in perdidas if n not in (tarea or '')]
                if perdidas:
                    fallos.append(
                        "DESAPARECE LO QUE YA ESTABA: el texto nuevo se lleva por delante %d "
                        "pieza(s) que si estaban en el viejo: %s. Si ese borrado es querido, "
                        "hay que decirlo por escrito; si no, es trabajo que se pierde en "
                        "silencio, que fue lo que paso el 2026-09-11."
                        % (len(perdidas), ", ".join(perdidas)))
    except Exception as e:      # un revisor que revienta deja pasar todo
        fallos.append("El revisor no pudo terminar la revision: %s" % str(e)[:140])
    return fallos


def informe(fallos):
    if not fallos:
        return ("REVISOR DE PROGRAMA: nada mecanico que objetar.\n"
                "  OJO: esto NO dice que el cambio sea bueno. El juicio (si esta bien pensado\n"
                "  y si rompe vecinos) sigue siendo del auditor de IA.")
    L = ["REVISOR DE PROGRAMA: %d fallo(s) cazados sin gastar ni una IA:" % len(fallos), ""]
    for f in fallos:
        L.append("   - " + f)
    return "\n".join(L)


if __name__ == "__main__":
    import json
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], encoding="utf-8") as f:
            datos = json.load(f)
        prop = datos.get("propuesta") if isinstance(datos, dict) else {}
        tar = (prop or {}).get("diagnostico", "") if isinstance(prop, dict) else ""
        print(informe(revisar(prop or {}, tar)))
    else:
        print(__doc__)
    sys.exit(0)
