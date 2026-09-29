# -*- coding: utf-8 -*-
"""cuerpo/aplicador.py — Aplica los cambios aprobados al disco, con respaldo temporal y validacion de sintaxis."""
import ast
import os
import tempfile
from datetime import datetime


def _apuntar_log(ok, archivo, funcion, detalle):
    """Apuntar en memoria/APLICACIONES.log. Si falla, no revienta."""
    try:
        ruta = os.environ.get("INGENIERO_APLICACIONES") or os.path.join(os.path.dirname(os.path.dirname(__file__)), "memoria", "APLICACIONES.log")
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} | {'OK' if ok else 'FALLO'} | {archivo} | {funcion} | {detalle}\n")
    except Exception:
        pass  # no debe tumbar la aplicacion


# Ley: CONTRATO_VARIOS_CAMBIOS_EN_UNA_RONDA.md (Julio 2026-09-14): varios pedazos en una sola ronda, se aplican TODOS o NINGUNO.
def aplicar_propuesta(propuesta, raiz=None):
    """Decide sola entre aplicar_cambios y aplicar_cambio. Devuelve (ok, mensaje).

    Si la propuesta es un diccionario y trae la clave 'cambios' con una lista no vacia,
    arma una copia donde cada trozo que no traiga su propia clave 'archivo' recibe el
    archivo de la propuesta, y llama a aplicar_cambios con esa copia. Si no trae
    'cambios', llama a aplicar_cambio con la propuesta tal cual. Devuelve lo que
    devuelva la que llamo.
    """
    if isinstance(propuesta, dict) and propuesta.get('cambios'):
        copia = dict(propuesta)
        archivo = propuesta.get('archivo')
        copia['cambios'] = [
            ({**pedazo, 'archivo': archivo} if isinstance(pedazo, dict) and not pedazo.get('archivo') else pedazo)
            for pedazo in propuesta['cambios']
        ]
        return aplicar_cambios(copia, raiz=raiz)
    return aplicar_cambio(propuesta, raiz=raiz)


def aplicar_cambios(propuesta, raiz=None):
    pedazos = propuesta.get('cambios') if isinstance(propuesta, dict) else []
    if not pedazos:
        return False, 'No hay cambios que aplicar.'
    contenidos = {}
    for pedazo in pedazos:
        ruta = pedazo['archivo']
        if raiz and not os.path.isabs(ruta):
            ruta = os.path.normpath(os.path.join(raiz, ruta))
        if ruta not in contenidos:
            if os.path.exists(ruta):
                # 2026-09-29: ingeniero.py empieza con la marca BOM (EF BB BF); leida con utf-8
                # queda como U+FEFF dentro del texto y ast.parse revienta con 'invalid
                # non-printable character U+FEFF' en el renglon 1, tirando todo cambio aprobado.
                # Se lee con utf-8-sig para que la marca no entre en el texto. Lo vigila
                # vigias/test_vigia_aplicador.py
                with open(ruta, 'r', encoding='utf-8-sig') as f:
                    contenidos[ruta] = f.read()
            else:
                contenidos[ruta] = ''
        viejo = pedazo.get('texto_viejo', '')
        nuevo = pedazo.get('texto_nuevo', '')
        if contenidos[ruta] == '' and viejo == '':
            contenidos[ruta] = nuevo
        else:
            if not viejo or contenidos[ruta].count(viejo) != 1:
                return False, f'El texto de antes no aparece exactamente una vez en {ruta}; no se aplico nada.'
            contenidos[ruta] = contenidos[ruta].replace(viejo, nuevo, 1)
    for ruta, texto in contenidos.items():
        if ruta.endswith('.py'):
            try:
                ast.parse(texto)
            except SyntaxError as e:
                return False, f'Sintaxis rota en {ruta} (renglon {e.lineno}); no se aplico nada.'
    for ruta, texto in contenidos.items():
        dir_archivo = os.path.dirname(ruta) or '.'
        fd, tmp_path = tempfile.mkstemp(dir=dir_archivo, suffix='.tmp')
        try:
            # 2026-09-29: la marca BOM tiene que quedar como estaba: no se agrega a los archivos
            # que no la tienen ni se le quita a los que si. Se lee la marca del original y se
            # escribe con utf-8-sig solo si el original la tenia. Lo vigila
            # vigias/test_vigia_aplicador.py
            tenia_bom = False
            if os.path.exists(ruta):
                with open(ruta, 'rb') as fb:
                    tenia_bom = fb.read(3) == b'\xef\xbb\xbf'
            with os.fdopen(fd, 'w', encoding='utf-8-sig' if tenia_bom else 'utf-8') as f:
                f.write(texto)
            os.replace(tmp_path, ruta)
            _apuntar_log(True, ruta, '?', 'cambio aplicado en ronda')
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            _apuntar_log(False, ruta, '?', f'error al aplicar: {e}')
            return False, f'Error al aplicar el cambio en {ruta}: {e}'
    return True, f'Se aplicaron {len(pedazos)} pedazos en {len(contenidos)} archivos.'


def aplicar_cambio(propuesta, raiz=None):
    """Aplica la propuesta del obrero al disco. Devuelve (ok, mensaje).

    RAIZ (2026-09-06): la carpeta del proyecto al que pertenece la propuesta. El obrero
    devuelve rutas RELATIVAS ("cuerpo/memoria.py") y sin esto se resolvian contra la carpeta
    del Ingeniero, que solo acierta cuando el proyecto ES el Ingeniero. Fallo real medido hoy:
    una reparacion de dmm quedo APROBADA y sin aplicar por eso. Si no se pasa raiz, se
    comporta igual que siempre, asi que nadie de los que ya llamaban se entera.
    """
    # Si no es diccionario o no trae archivo, no se toca nada.
    if not isinstance(propuesta, dict) or not propuesta.get("archivo"):
        _apuntar_log(False, "?", "?", "propuesta invalida: no es dict o no trae archivo")
        return False, "Propuesta invalida: no es un diccionario o no trae 'archivo'."

    archivo = propuesta["archivo"]
    funcion = propuesta.get("funcion", "?")
    texto_viejo = propuesta.get("texto_viejo", "")
    texto_nuevo = propuesta.get("texto_nuevo", "")
    codigo = propuesta.get("codigo", "")
    # 2026-09-13: se perdieron dos rondas ya aprobadas por esto. Lo vigila vigias/test_vigia_aplicador.py.
    # La marca NO_ENCONTRADO la pone el obrero cuando no hay trozo: no es texto.
    if texto_viejo.strip().upper() == "NO_ENCONTRADO":
        texto_viejo = ""
    if texto_nuevo.strip().upper() == "NO_ENCONTRADO":
        texto_nuevo = ""
    # La ruta del obrero es relativa al PROYECTO, no al Ingeniero. Si nos dieron la carpeta del
    # proyecto y la ruta no es absoluta, se resuelve contra ella. Una ruta absoluta se respeta
    # tal cual: si el obrero ya dijo donde exactamente, no se le corrige.
    if raiz and not os.path.isabs(archivo):
        archivo = os.path.normpath(os.path.join(raiz, archivo))

    # Si el archivo NO existe y la propuesta trae texto_viejo, es un cambio sobre algo que deberia existir: no se crea nada.
    if not os.path.exists(archivo):
        if texto_viejo:
            _apuntar_log(False, archivo, funcion, "archivo no existe en esa ruta")
            return False, "El archivo no existe en esa ruta; probablemente la ruta este mal resuelta o falte la carpeta del proyecto."
        contenido = codigo if codigo else texto_nuevo
        if not contenido:
            _apuntar_log(False, archivo, funcion, "archivo no existe y no trae texto")
            return False, "El archivo no existe y la propuesta no trae texto para crearlo."

    # Comprobacion de humo: si el texto nuevo solo se diferencia del viejo en comentarios
    # con almohadilla o lineas en blanco, no se aplica nada. Un trozo suelto no dice si
    # empieza dentro de un texto de ayuda, asi que aqui no se manejan textos de ayuda.
    def _quitar_ruido(texto):
        lineas = []
        for linea in texto.splitlines():
            tira = linea.strip()
            if not tira:
                continue
            if tira.startswith('#'):
                continue
            lineas.append(tira)
        return "\n".join(lineas)

    # El bloque que CREA el archivo nuevo pertenece al caso "el archivo no existe" y estaba
    # quedando dentro de la comprobacion de humo: asi no se podia crear ni un archivo nuevo.
    # Se devuelve a su sitio (Julio, 2026-09-05: la reparacion no puede romper al vecino).
    if not os.path.exists(archivo):
        # 2026-09-27: un .py nuevo y roto no debe llegar al disco. Antes de escribir nada,
        # si termina en .py se comprueba la sintaxis con ast.parse, igual que la rama que
        # reescribe un archivo que ya existe. Lo vigila
        # vigias/test_vigia_un_archivo_nuevo_roto_no_llega_al_disco.py.
        if archivo.endswith(".py"):
            try:
                ast.parse(contenido)
            except SyntaxError as e:
                _apuntar_log(False, archivo, funcion, f"sintaxis rota: {e}")
                return False, f"El cambio deja el codigo roto (renglon {e.lineno}): {e.msg}"
        try:
            # la carpeta de un archivo nuevo se crea si falta (medido 2026-09-22, orden 176)
            os.makedirs(os.path.dirname(archivo) or ".", exist_ok=True)
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(contenido)
            _apuntar_log(True, archivo, funcion, "archivo creado")
            return True, "Archivo creado."
        except Exception as e:
            _apuntar_log(False, archivo, funcion, f"no se pudo crear: {e}")
            return False, f"No se pudo crear el archivo: {e}"

    # 2026-09-13, el obrero pide anadir al final poniendo el mismo renglon de ancla antes y despues y lo nuevo en codigo; se tomaba por humo y se perdia una ronda ya aprobada; lo vigila vigias/test_vigia_aplicador.py.
    if os.path.exists(archivo) and texto_viejo and texto_viejo == texto_nuevo and codigo:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        nuevo_contenido = contenido
        if not nuevo_contenido.endswith("\n"):
            nuevo_contenido += "\n"
        nuevo_contenido += "\n" + codigo
        if not codigo.endswith("\n"):
            nuevo_contenido += "\n"

        # Sustituir en un temporal al lado.
        dir_archivo = os.path.dirname(archivo) or "."
        fd, tmp_path = tempfile.mkstemp(dir=dir_archivo, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(nuevo_contenido)

            # Si termina en .py, validar sintaxis con ast.parse.
            if archivo.endswith(".py"):
                try:
                    with open(tmp_path, "r", encoding="utf-8") as f:
                        ast.parse(f.read())
                except SyntaxError as e:
                    os.remove(tmp_path)
                    _apuntar_log(False, archivo, funcion, f"sintaxis rota: {e}")
                    return False, f"El cambio deja el codigo roto (renglon {e.lineno}): {e.msg}"

            # Mover el temporal encima del original.
            os.replace(tmp_path, archivo)
            _apuntar_log(True, archivo, funcion, "codigo anadido al final")
            return True, "Codigo anadido al final."
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            _apuntar_log(False, archivo, funcion, f"error al aplicar: {e}")
            return False, f"Error al aplicar el cambio: {e}"

    if texto_viejo and texto_nuevo:
        if _quitar_ruido(texto_viejo) == _quitar_ruido(texto_nuevo):
            _apuntar_log(False, archivo, funcion, "cambio humo: solo toca comentarios")
            return False, "HUMO: el cambio solo toca comentarios, no repara nada."

    # Si el archivo YA existe, se busca texto_viejo.
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
    except Exception as e:
        _apuntar_log(False, archivo, funcion, f"no se pudo leer: {e}")
        return False, f"No se pudo leer el archivo: {e}"

    # 2026-09-22: contenido entero (codigo o texto_nuevo) y sin texto_viejo sobre un archivo
    # que YA existe: si es identico no se toca el disco; si difiere se sobreescribe entero
    # (validando .py). La marca 'crear' ya no es obligatoria: el obrero puede mandar el
    # documento entero sin texto_viejo y se re-escribe igual. Lo vigila
    # vigias/test_vigia_aplicador.py.
    if not texto_viejo and (codigo or texto_nuevo):
        contenido_propuesto = codigo if codigo else texto_nuevo
        if not contenido_propuesto:
            _apuntar_log(False, archivo, funcion, "crear sin contenido")
            return False, "La propuesta no trae contenido para crear."
        if contenido == contenido_propuesto:
            _apuntar_log(True, archivo, funcion, "archivo ya existe identico")
            return True, "El archivo ya existe identico; nada que aplicar."
        dir_archivo = os.path.dirname(archivo) or "."
        fd, tmp_path = tempfile.mkstemp(dir=dir_archivo, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(contenido_propuesto)
            if archivo.endswith(".py"):
                try:
                    with open(tmp_path, "r", encoding="utf-8-sig") as f:
                        ast.parse(f.read())
                except SyntaxError as e:
                    os.remove(tmp_path)
                    _apuntar_log(False, archivo, funcion, f"sintaxis rota: {e}")
                    return False, f"El cambio deja el codigo roto (renglon {e.lineno}): {e.msg}"
            os.replace(tmp_path, archivo)
            _apuntar_log(True, archivo, funcion, "archivo recreado")
            return True, "Archivo recreado."
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            _apuntar_log(False, archivo, funcion, f"error al aplicar: {e}")
            return False, f"Error al aplicar el cambio: {e}"

    if not texto_viejo:
        _apuntar_log(False, archivo, funcion, "texto_viejo vacio")
        return False, "La propuesta no trae 'texto_viejo'."

    veces = contenido.count(texto_viejo)
    if veces == 0:
        _apuntar_log(False, archivo, funcion, "texto_viejo no encontrado")
        return False, "El texto_viejo no aparece en el archivo."
    if veces > 1:
        try:
            if funcion and funcion != "?" and archivo.endswith(".py"):
                import ast as _ast
                arbol = _ast.parse(contenido)
                nodo_encontrado = None
                for nodo in _ast.walk(arbol):
                    if isinstance(nodo, (_ast.FunctionDef, _ast.AsyncFunctionDef)) and nodo.name == funcion:
                        nodo_encontrado = nodo
                        break
                if nodo_encontrado is not None:
                    lineas = contenido.splitlines(keepends=True)
                    ini = nodo_encontrado.lineno - 1
                    fin = nodo_encontrado.end_lineno
                    trozo = "".join(lineas[ini:fin])
                    if trozo.count(texto_viejo) == 1:
                        trozo_nuevo = trozo.replace(texto_viejo, texto_nuevo, 1)
                        nuevo_contenido = "".join(lineas[:ini]) + trozo_nuevo + "".join(lineas[fin:])
                        dir_archivo = os.path.dirname(archivo) or "."
                        fd, tmp_path = tempfile.mkstemp(dir=dir_archivo, suffix=".tmp")
                        try:
                            with os.fdopen(fd, "w", encoding="utf-8") as f:
                                f.write(nuevo_contenido)
                            if archivo.endswith(".py"):
                                try:
                                    with open(tmp_path, "r", encoding="utf-8-sig") as f:
                                        _ast.parse(f.read())
                                except SyntaxError as e:
                                    os.remove(tmp_path)
                                    _apuntar_log(False, archivo, funcion, f"sintaxis rota: {e}")
                                    return False, f"El cambio deja el codigo roto (renglon {e.lineno}): {e.msg}"
                            os.replace(tmp_path, archivo)
                            _apuntar_log(True, archivo, funcion, "cambio aplicado en funcion")
                            return True, "Cambio aplicado."
                        except Exception as e:
                            if os.path.exists(tmp_path):
                                os.remove(tmp_path)
                            _apuntar_log(False, archivo, funcion, f"error al aplicar: {e}")
                            return False, f"Error al aplicar el cambio: {e}"
        except Exception:
            pass
        _apuntar_log(False, archivo, funcion, f"texto_viejo aparece {veces} veces")
        return False, f"El texto_viejo aparece {veces} veces; no se sabe cual es."

    # Sustituir en un temporal al lado.
    nuevo_contenido = contenido.replace(texto_viejo, texto_nuevo, 1)
    dir_archivo = os.path.dirname(archivo) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_archivo, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)

        # Si termina en .py, validar sintaxis con ast.parse.
        if archivo.endswith(".py"):
            try:
                # 2026-09-13: ingeniero.py tiene la marca BOM y ast.parse la tomaba por error: se tiraba todo cambio aprobado. Lo vigila vigias/test_vigia_aplicador.py
                with open(tmp_path, "r", encoding="utf-8-sig") as f:
                    ast.parse(f.read())
            except SyntaxError as e:
                os.remove(tmp_path)
                _apuntar_log(False, archivo, funcion, f"sintaxis rota: {e}")
                return False, f"El cambio deja el codigo roto (renglon {e.lineno}): {e.msg}"

        # Mover el temporal encima del original.
        os.replace(tmp_path, archivo)
        _apuntar_log(True, archivo, funcion, "cambio aplicado")
        return True, "Cambio aplicado."
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        _apuntar_log(False, archivo, funcion, f"error al aplicar: {e}")
        return False, f"Error al aplicar el cambio: {e}"

