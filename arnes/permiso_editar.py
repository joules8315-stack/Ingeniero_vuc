# -*- coding: utf-8 -*-
"""arnes/permiso_editar.py — RETIRADO. NO ES UNA PUERTA.

Julio, 2026-08-26: la salida de emergencia NECESITO_EDITAR se volvio la ENTRADA PRINCIPAL —
todas las IA se salieron por ahi y trabajaron a solas, que es justo lo que el candado de equipo
existe para impedir. Queda RETIRADA de raiz:

  · candado_equipo y edit_gate_universal ya NO la honran (se les quito el bypass).
  · `hay_permiso` siempre responde False: aunque algo lo llame, NUNCA abre.
  · `dar` responde error: ya no se puede fabricar una llave.
  · el comando `necesito-editar` se quito de ingeniero.py.

El UNICO que autoriza tocar codigo a solas es Julio (autorizacion), o el veredicto del equipo.
Si un archivo grande no cabe en el paquete, la cura es arreglar el repartidor (diccionario/router),
no volver a abrir esta puerta.
"""
import json, os, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(AQUI, "memoria", "PERMISOS_EDICION.json")
REGISTRO = os.path.join(AQUI, "memoria", "permisos_edicion.log")
VIGENCIA_MIN = 30


def dar(archivo, motivo, vigia="", dana=""):
    """RETIRADO (Julio, 2026-08-26): ya no se puede abrir la puerta."""
    return {"_error": "RETIRADO: el permiso de edicion (NECESITO_EDITAR) ya no existe. "
                      "El unico que autoriza tocar codigo a solas es Julio, o el veredicto del equipo."}


def hay_permiso(archivo):
    """RETIRADO (Julio, 2026-08-26): nunca abre. El candado de equipo ya no lo consulta."""
    return False


def texto():
    return ("PERMISOS DE EDICION: RETIRADOS (Julio, 2026-08-26). "
            "La salida de emergencia se volvio entrada principal y se cerro de raiz. "
            "El unico que autoriza tocar codigo a solas es Julio, o el veredicto del equipo.")
