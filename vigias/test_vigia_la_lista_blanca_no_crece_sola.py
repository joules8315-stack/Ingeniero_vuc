import os
import sys
import importlib.util
import pytest

# Ruta base del proyecto (dos niveles arriba de este archivo)
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Añadir al path para que otros imports del proyecto funcionen
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

# Cargar el módulo que contiene la lista blanca sin usar su nombre de paquete
ruta_lista = os.path.join(AQUI, "skills", "lista_blanca.py")
spec = importlib.util.spec_from_file_location("lista_blanca_por_su_sitio", ruta_lista)
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)

# Obtener la lista de entradas (cada una es un dict con claves 'ruta', 'porque' y 'quien')
entradas = modulo.listadas()

# ---------------------------------------------------------------------------
# Constantes de la vigía (no dependen de configuración externa)
# ---------------------------------------------------------------------------
TOPE_MAXIMO = 3  # Máximo permitido de piezas en la lista blanca
# Ruta(s) que Julio autorizó realmente. Por ahora solo el compilador del mapa del negocio.
RUTAS_AUTORIZADAS_JULIO = {"cuerpo/compilar_mapa.py"}

# ---------------------------------------------------------------------------
# 1. La lista no debe superar el tope definido
# ---------------------------------------------------------------------------
def test_la_lista_no_pasa_del_tope():
    """Comprueba que la lista blanca no supera el número máximo permitido.
    Si falla, Julio pierde la garantía de que la lista sea una excepción y se
    convierte en una puerta trasera que él prohibió.
    """
    cantidad = len(entradas)
    assert cantidad <= TOPE_MAXIMO, (
        f"Julio: la lista blanca tiene {cantidad} piezas, pero solo se permiten {TOPE_MAXIMO}. "
        "Una lista que crece sola deja de ser una excepción y se convierte en la puerta trasera que Julio prohibió."
    )

# ---------------------------------------------------------------------------
# 2. Ninguna entrada debe atribuir a Julio sin que la ruta esté autorizada
# ---------------------------------------------------------------------------
def test_ninguna_entrada_dice_que_la_metio_Julio_sin_que_conste():
    """Asegura que solo las rutas explícitamente autorizadas aparecen con 'quien' == 'Julio'.
    Si falla, Julio aparece como autor de piezas que él no aprobó.
    """
    violadores = [e["ruta"] for e in entradas if e.get("quien") == "Julio" and e["ruta"] not in RUTAS_AUTORIZADAS_JULIO]
    assert not violadores, (
        f"Julio: las siguientes rutas están atribuidas a Julio sin autorización: {', '.join(violadores)}. "
        "Una pieza sin permiso de Julio deja de contarse como dormida y nadie la va a enchufar nunca."
    )

# ---------------------------------------------------------------------------
# 3. Cada entrada debe contener un motivo suficientemente descriptivo
# ---------------------------------------------------------------------------
def test_cada_entrada_dice_por_que_de_verdad():
    """Verifica que el campo 'porque' tenga al menos 20 caracteres y más de dos palabras.
    Si falla, el motivo es demasiado corto o poco claro, lo que impide que Julio
    confíe en que la pieza está justificada.
    """
    deficientes = []
    for e in entradas:
        motivo = e.get("porque", "")
        # al menos 20 letras y al menos 3 palabras
        if len(motivo) < 20 or len(motivo.split()) < 3:
            deficientes.append(e["ruta"])
    assert not deficientes, (
        f"Julio: las siguientes piezas tienen un motivo demasiado corto o insuficiente: {', '.join(deficientes)}. "
        "Sin un motivo claro la pieza no se cuenta como dormida y nadie la va a enchufar nunca."
    )
