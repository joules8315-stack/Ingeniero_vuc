# -*- coding: utf-8 -*-
"""CANDADO — un APROBADO sobre OTRO archivo no vale como aprobado.

QUE FRENA: que el equipo firme APROBADO cuando el archivo que dice haber reparado NO es
ninguno de los que traia el encargo.

FALLO REAL QUE LO TRAE (2026-08-24, Foto Informe): el encargo era reparar una prueba concreta.
El reparador diagnostico bien los defectos y luego dijo tocar OTRA prueba, que estaba sana. Las
tres rondas apuntaron al archivo equivocado y el juez firmo APROBADO. Aplicarlo habria
reescrito lo que funciona y dejado lo roto igual, con el sello del equipo encima.

POR QUE ES UN CANDADO Y NO UN AVISO AL JUEZ: el juez SI caza esto a veces (ese mismo dia, en
DMM, escribio "existe una discrepancia de ubicacion") y otras veces no. Comparar dos nombres es
mecanico. Lo mecanico no se deja a que un cerebro se acuerde.
Ley de Foto Informe (2026-07-23): "un recordatorio se ignora; solo un candado que FRENA se cumple".

QUE **NO** HACE (a proposito):
  · no asciende a nadie: lo que no venia APROBADO se queda como estaba;
  · no juzga si la reparacion es buena — eso sigue siendo del juez;
  · no frena cuando el archivo SI es el del encargo. Un freno que frena siempre tapia la puerta,
    y eso ya nos costo la tarde del 2026-08-24.

Lo protege: vigias/test_vigia_archivo_del_veredicto.py
"""
import os

APROBADO = "APROBADO"
NO_ENCONTRADO = "NO_ENCONTRADO"


def _nombre(ruta):
    """Solo el nombre del archivo, sin carpeta, sin barras y en minusculas.

    El reparador escribe la ruta como le da la gana: a secas, con './' delante, o con la ruta
    entera de Windows. El freno no puede caerse por eso, ni dejar pasar por eso.
    """
    if not ruta:
        return ""
    t = str(ruta).strip().strip('"').strip("'")
    if not t or t == NO_ENCONTRADO:
        return ""
    t = t.replace("\\", "/")
    return os.path.basename(t).strip().lower()


def se_equivoco_de_archivo(archivo_reparado, archivos_del_encargo):
    """Devuelve el MOTIVO en palabras si se reparo otro archivo, o "" si esta bien.

    Devuelve motivo (o sea: FRENA) tambien cuando no se puede comprobar:
      · el reparador no dijo que archivo toca, o dijo NO_ENCONTRADO;
      · el encargo no trajo ningun archivo con que comparar.
    Ley 2 de Julio: nunca inventar. Sin con que comparar, no se aprueba a ciegas.
    """
    tocado = _nombre(archivo_reparado)
    if not tocado:
        return ("El reparador no dijo que archivo toca, asi que no se puede comprobar que "
                "haya reparado lo que se pidio.")

    esperados = [a for a in (_nombre(x) for x in (archivos_del_encargo or [])) if a]
    if not esperados:
        return ("El encargo no trae ningun archivo con que comparar, asi que no se puede "
                "comprobar que se haya reparado lo que se pidio.")

    if tocado in esperados:
        return ""

    return ("Se reparo %s, y el encargo era sobre %s. Un arreglo sobre otro archivo no vale, "
            "aunque el juez lo haya aprobado." % (_nombre(archivo_reparado),
                                                  ", ".join(esperados)))


def revisar_veredicto(veredicto, archivo_reparado, archivos_del_encargo):
    """(veredicto_final, motivo). Solo tumba APROBADOS; nunca asciende a nadie."""
    if str(veredicto or "").strip().upper() != APROBADO:
        return veredicto, ""
    motivo = se_equivoco_de_archivo(archivo_reparado, archivos_del_encargo)
    if motivo:
        # MEDICION (Julio, 2026-08-25): freno un APROBADO sobre el archivo equivocado.
        try:
            import candados_medicion
            candados_medicion.cazado("archivo_del_veredicto")
        except Exception:
            pass
        return "RECHAZADO_ARCHIVO_EQUIVOCADO", motivo
    return APROBADO, ""


def texto(motivo):
    """Como se le cuenta a Julio, sin jerga."""
    return ("EL APROBADO NO VALE: se arreglo un archivo que no era.\n  " + motivo +
            "\n  Se vuelve a lanzar el encargo nombrando el archivo, y no se aplica nada.")
