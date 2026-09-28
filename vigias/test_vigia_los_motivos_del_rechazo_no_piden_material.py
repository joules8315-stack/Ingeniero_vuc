import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuerpo import obrero


PROPUESTA_OK = json.dumps({"archivo": "x.py", "texto_viejo": "a", "texto_nuevo": "b"})
PAQUETE = "paquete"


# La tarea pide un archivo y una funcion que SI estan en el material de prueba.
ENCARGO = (
    "Cambia en cuerpo/obrero.py la funcion _prompt_obrero para que respete "
    "el generador pedido."
)

# El material de prueba SI trae el archivo y la funcion que pide la tarea.
MATERIAL_CON_PIEZA = (
    "# PAQUETE\n"
    "### cuerpo/obrero.py\n"
    "```\n"
    "def _prompt_obrero(...):\n"
    "    ...\n"
    "```\n"
)

# Material que NO trae el archivo que la TAREA nombra.
MATERIAL_SIN_PIEZA = (
    "# PAQUETE\n"
    "- cuerpo/otra_cosa.py (10 lineas)\n"
    "- cuerpo/y_otra.py (5 lineas)\n"
)

# Motivo de rechazo que nombra un archivo de codigo que NO esta en el material.
# Ese archivo solo aparece en el aviso del revisor, no en la tarea.
MOTIVO_RECHAZO = (
    "El cambio no toca cuerpo/archivo_que_solo_nombra_el_aviso.py y por eso "
    "no queda bien."
)


def _preparar(monkeypatch, material, veredictos):
    """Monta el molde de la prueba vecina: nadie llama a la IA de verdad.

    - _propuesta_cumple: dice que la propuesta cumple.
    - _validar_en_paquete: no encuentra inventos.
    - _filtrar_paquete: devuelve el material de prueba.
    - _preguntar_con_relevo: apunta los pedidos en una lista en vez de llamar.
    - auditar: devuelve el veredicto que la prueba quiera, en orden.
    """
    monkeypatch.setattr(obrero, "_propuesta_cumple", lambda p, c: (True, ""))
    monkeypatch.setattr(obrero, "_validar_en_paquete", lambda *a, **k: [])
    monkeypatch.setattr(obrero, "_filtrar_paquete", lambda paquete, **k: material)

    prompts = []

    def falsa_obrero(prompt, *a, **k):
        prompts.append(prompt)
        return (PROPUESTA_OK, "deepseek", [])

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", falsa_obrero)

    pendientes = list(veredictos)
    llamadas_auditar = []

    def aud(*a, **k):
        llamadas_auditar.append((a, k))
        if pendientes:
            veredicto = pendientes.pop(0)
        else:
            veredicto = {"veredicto": "APROBADO"}
        return (veredicto, "groq", [])

    monkeypatch.setattr(obrero, "auditar", aud)
    return prompts, llamadas_auditar


def test_los_motivos_del_rechazo_no_piden_material(monkeypatch):
    """La primera vuelta se rechaza nombrando un archivo que solo sale en el aviso.

    La segunda vuelta debe SI llegar a pedirle al cerebro: dos pedidos apuntados.
    No debe morir diciendo que falta el archivo que solo nombraba el aviso.
    """
    veredictos = [
        {"veredicto": "RECHAZADO", "motivo": MOTIVO_RECHAZO},
        {"veredicto": "APROBADO"},
    ]
    prompts, _ = _preparar(monkeypatch, MATERIAL_CON_PIEZA, veredictos)

    resultado = obrero.trabajar(PAQUETE, ENCARGO, generador="deepseek", auditor="bigpickle")

    # La segunda vuelta SI le pidio al cerebro: hay dos pedidos apuntados.
    assert len(prompts) >= 2

    # No murio por falta del archivo que solo nombraba el aviso.
    texto = json.dumps(resultado, ensure_ascii=False)
    assert "FALTA_MATERIAL" not in texto
    assert "archivo_que_solo_nombra_el_aviso" not in texto


def test_si_la_tarea_nombra_archivo_que_no_esta_se_muere_sin_llamar(monkeypatch):
    """Si es la TAREA la que nombra un archivo que el material no trae,
    se sigue muriendo sin llamar a nadie: eso no se afloja.
    """
    veredictos = [{"veredicto": "APROBADO"}]
    prompts, _ = _preparar(monkeypatch, MATERIAL_SIN_PIEZA, veredictos)

    resultado = obrero.trabajar(PAQUETE, ENCARGO, generador="deepseek", auditor="bigpickle")

    # Nadie le pregunto al cerebro.
    assert prompts == []

    texto = json.dumps(resultado, ensure_ascii=False)
    assert "FALTA_MATERIAL" in texto
    assert "NECESITO_LEER" in texto
    assert "cuerpo/obrero.py" in texto
