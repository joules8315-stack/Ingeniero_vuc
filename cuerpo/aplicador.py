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


def aplicar_cambio(propuesta):
    """Aplica la propuesta del obrero al disco. Devuelve (ok, mensaje)."""
    # Si no es diccionario o no trae archivo, no se toca nada.
    if not isinstance(propuesta, dict) or not propuesta.get("archivo"):
        _apuntar_log(False, "?", "?", "propuesta invalida: no es dict o no trae archivo")
        return False, "Propuesta invalida: no es un diccionario o no trae 'archivo'."

    archivo = propuesta["archivo"]
    funcion = propuesta.get("funcion", "?")
    texto_viejo = propuesta.get("texto_viejo", "")
    texto_nuevo = propuesta.get("texto_nuevo", "")
    codigo = propuesta.get("codigo", "")

    # Si el archivo NO existe y la propuesta trae texto_viejo, es un cambio sobre algo que deberia existir: no se crea nada.
    if not os.path.exists(archivo):
        if texto_viejo:
            _apuntar_log(False, archivo, funcion, "archivo no existe en esa ruta")
            return False, "El archivo no existe en esa ruta; probablemente la ruta este mal resuelta o falte la carpeta del proyecto."
        contenido = codigo if codigo else texto_nuevo
        if not contenido:
            _apuntar_log(False, archivo, funcion, "archivo no existe y no trae texto")
            return False, "El archivo no existe y la propuesta no trae texto para crearlo."

    # Comprobacion de humo: si el texto nuevo solo se diferencia del viejo en comentarios,
    # cadenas de documentacion o lineas en blanco, no se aplica nada.
    def _quitar_ruido(texto):
        lineas = []
        dentro_docstring = False
        for linea in texto.splitlines():
            tira = linea.strip()
            if not tira:
                continue
            if dentro_docstring:
                if '"""' in tira:
                    dentro_docstring = False
                continue
            if tira.startswith('"""'):
                if tira.count('"""') < 2:
                    dentro_docstring = True
                continue
            if tira.startswith('#'):
                continue
            lineas.append(tira)
        return "\n".join(lineas)

    # El bloque que CREA el archivo nuevo pertenece al caso "el archivo no existe" y estaba
    # quedando dentro de la comprobacion de humo: asi no se podia crear ni un archivo nuevo.
    # Se devuelve a su sitio (Julio, 2026-09-05: la reparacion no puede romper al vecino).
    if not os.path.exists(archivo):
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(contenido)
            _apuntar_log(True, archivo, funcion, "archivo creado")
            return True, "Archivo creado."
        except Exception as e:
            _apuntar_log(False, archivo, funcion, f"no se pudo crear: {e}")
            return False, f"No se pudo crear el archivo: {e}"

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

    if not texto_viejo:
        _apuntar_log(False, archivo, funcion, "texto_viejo vacio")
        return False, "La propuesta no trae 'texto_viejo'."

    veces = contenido.count(texto_viejo)
    if veces == 0:
        _apuntar_log(False, archivo, funcion, "texto_viejo no encontrado")
        return False, "El texto_viejo no aparece en el archivo."
    if veces > 1:
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
                with open(tmp_path, "r", encoding="utf-8") as f:
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

