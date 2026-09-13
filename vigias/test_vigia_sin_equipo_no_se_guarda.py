import os
import sys
import importlib.util
import pytest

# Declaración de revisión de cross-flow obligatorio:
# Se ha revisado arnes/guardia_de_guardado.py y vigias/test_vigia_equipo_siempre.py

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
arnes_path = os.path.join(AQUI, "arnes")
if arnes_path not in sys.path:
    sys.path.insert(0, arnes_path)

def _obtener_funcion_guardia():
    ruta_guardia = os.path.join(AQUI, "arnes", "guardia_de_guardado.py")
    spec = importlib.util.spec_from_file_location("guardia_de_guardado", ruta_guardia)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "se_puede_guardar_sin_equipo")

def test_con_veredicto_del_equipo_se_guarda():
    """
    Si esta prueba falla, Julio corre el riesgo de que el código legítimo,
    revisado y aprobado por el equipo, sea bloqueado injustamente en la puerta,
    lo que paralizaría el desarrollo colaborativo y seguro.
    """
    try:
        se_puede_guardar_sin_equipo = _obtener_funcion_guardia()
    except AttributeError:
        pytest.fail(
            "La función se_puede_guardar_sin_equipo no existe en guardia_de_guardado.py. "
            "Si esto falla, cualquiera podría guardar código a solas sin que nadie lo revise, "
            "dañando el DMM de Julio."
        )
    
    permitido, explicacion = se_puede_guardar_sin_equipo(True, "")
    assert permitido is True, (
        f"Error: El código aprobado por el equipo debería poder guardarse siempre. "
        f"Explicación recibida: {explicacion}"
    )

def test_SIN_EQUIPO_NO_SE_GUARDA():
    """
    Esta es la prueba principal que responde a la orden directa de Julio.
    Si falla, significa que un programador o una IA trabajando a solas
    puede guardar código sin revisión del equipo, saltándose el arnés
    y destruyendo la estabilidad del sistema.
    """
    try:
        se_puede_guardar_sin_equipo = _obtener_funcion_guardia()
    except AttributeError:
        pytest.fail(
            "La función se_puede_guardar_sin_equipo no existe en guardia_de_guardado.py. "
            "Sin ella, el código sin equipo se guardará sin control."
        )
    
    permitido, explicacion = se_puede_guardar_sin_equipo(False, "")
    assert permitido is False, (
        "¡PELIGRO! Se permitió guardar código sin que el equipo lo revise. "
        "Esto viola la orden directa de Julio de que nadie trabaje sin equipo."
    )
    assert "equipo" in explicacion.lower(), (
        f"La explicación del rechazo debe mencionar explícitamente al 'equipo'. "
        f"Explicación actual: {explicacion}"
    )

def test_lo_que_no_es_codigo_pasa():
    """
    Si esta prueba falla, Julio no podrá guardar notas, documentación,
    configuraciones o archivos que no son código fuente, paralizando tareas
    administrativas que no requieren la revisión técnica del equipo.
    """
    try:
        se_puede_guardar_sin_equipo = _obtener_funcion_guardia()
    except AttributeError:
        pytest.fail("La función se_puede_guardar_sin_equipo no existe en guardia_de_guardado.py.")
    
    permitido, explicacion = se_puede_guardar_sin_equipo(None, "")
    assert permitido is True, (
        f"Error: Los archivos que no son código (cubierto=None) no deberían requerir equipo. "
        f"Explicación recibida: {explicacion}"
    )

def test_la_llave_de_Julio_abre_pero_EXIGE_MOTIVO():
    """
    Si esta prueba falla, la llave de Julio podría usarse como una puerta trasera
    fácil sin dar explicaciones, o bien Julio no podría saltarse el candado
    en una emergencia real aportando un motivo justificado de peso (mínimo 20 letras).
    """
    try:
        se_puede_guardar_sin_equipo = _obtener_funcion_guardia()
    except AttributeError:
        pytest.fail("La función se_puede_guardar_sin_equipo no existe en guardia_de_guardado.py.")
    
    # Con llave muy corta (menos de 20 letras) -> No debe permitir guardar
    permitido_corto, explicacion_corto = se_puede_guardar_sin_equipo(False, "ok")
    assert permitido_corto is False, (
        "¡PELIGRO! Se permitió guardar con un motivo demasiado corto. "
        "Debe exigir al menos 20 letras para evitar que sea una puerta trasera fácil."
    )
    
    # Con llave de 20 letras o más -> Debe permitir guardar
    motivo_valido = "Emergencia de produccion corregida por Julio directamente"
    assert len(motivo_valido) >= 20
    permitido_largo, explicacion_largo = se_puede_guardar_sin_equipo(False, motivo_valido)
    assert permitido_largo is True, (
        f"Error: No se permitió guardar a pesar de que Julio proporcionó un motivo de más de 20 letras. "
        f"Explicación recibida: {explicacion_largo}"
    )

def test_la_funcion_existe_en_el_guardia_de_verdad():
    """
    Si esta prueba falla, significa que la función se_puede_guardar_sin_equipo
    no está implementada en el archivo arnes/guardia_de_guardado.py, por lo que
    el sistema de guardado real ignorará esta protección y permitirá que cualquiera
    guarde código sin equipo.
    """
    ruta_guardia = os.path.join(AQUI, "arnes", "guardia_de_guardado.py")
    assert os.path.exists(ruta_guardia), f"No existe el archivo del guardia en {ruta_guardia}"
    
    spec = importlib.util.spec_from_file_location("guardia_de_guardado", ruta_guardia)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        pytest.fail(f"No se pudo cargar el módulo guardia_de_guardado: {e}")
        
    assert hasattr(mod, "se_puede_guardar_sin_equipo"), (
        "La función 'se_puede_guardar_sin_equipo' NO existe en arnes/guardia_de_guardado.py. "
        "Si esto no se cumple, el guardia de la puerta dejará pasar código escrito a solas "
        "y se dañará el DMM de Julio."
    )
