import os
import sys

# Añadir el directorio raíz del proyecto y el paquete 'arnes' al sys.path
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))

# Importar la función a probar
from arnes import candado_legislar


def test_un_aviso_de_maquina_NO_es_una_orden():
    """Los mensajes generados por la máquina no deben ser considerados órdenes."""
    avisos = [
        '<summary>Background command "Pedir la reparacion con la funcion adjunta" completed (exit code 0)</summary>',
        '<summary>Monitor event: "esperar la reparacion del equipo"</summary>',
        '<summary>Monitor "esperar la reparacion del equipo" stream ended</summary>',
        '<event>TODO GUARDADO: d1d8786 LA AVERIA SE DEFIENDE SOLA: el encargo para repararla no le cupo a ningun cerebro</event>',
    ]
    for aviso in avisos:
        assert not candado_legislar.parece_una_orden(aviso), f"Aviso de máquina detectado como orden: {aviso}"


def test_una_orden_de_verdad_de_Julio_SIGUE_entrando():
    """Las órdenes reales de Julio deben seguir siendo reconocidas como órdenes."""
    ordenes = [
        "Repara el registro que se traga los avisos de la maquina, ponle candado y vigilalo",
        "Deja todo lo que estas haciendo en el canal del ayudante para que continue",
        "Sigue construyendo y reparando el negocio hasta terminarlo",
    ]
    for orden in ordenes:
        assert candado_legislar.parece_una_orden(orden), f"Orden real de Julio no reconocida: {orden}"
