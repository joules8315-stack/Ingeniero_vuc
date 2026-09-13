import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)

from cuerpo import obrero

"""VIGIA: NADIE REVISA SU PROPIO TRABAJO.

Protege la ley "uno escribe y OTRO distinto revisa".
Medido el 2026-09-13: de 102 rondas reales aprobadas en 7 dias, 40 las reviso
EL MISMO cerebro que las escribio. Por ley esas no se aplican, asi que se
quedaban esperando y la ronda siguiente las borraba.

La causa estaba en cuerpo/obrero.py, funcion auditar: cuando ningun revisor
contesto, hacia un ultimo intento con el cerebro de pago (pesado=True) SIN
pasarle 'evitar', asi que el que escribio acababa revisandose a si mismo.

LEY QUE SE MANTIENE (Julio): el ultimo intento con el cerebro de pago
(pesado=True) SE SIGUE HACIENDO SIEMPRE; lo vigila
vigias/test_vigia_lo_pesado_a_deepseek.py. Lo unico que cambia es que en ese
intento TAMBIEN se aparta al que escribio. La prueba 4 lo comprueba.
"""


propuesta = {"archivo": "vigias/de_prueba.py", "diagnostico": "prueba", "codigo": "x = 1\n"}


def test_el_ultimo_intento_tambien_aparta_al_que_escribio(monkeypatch):
    llamadas = []

    def espia(prompt, temperatura, evitar=None, primero=None, pesado=False, clase=None, vuelta=None, **resto):
        llamadas.append({"evitar": evitar, "pesado": pesado, "vuelta": vuelta})
        if evitar is None:
            # si nadie aparta al que escribio, contesta EL MISMO que escribio, aprobando
            return ('{"veredicto": "APROBADO", "resumen": "me reviso a mi mismo"}', "deepseek", [])
        return ("", None, [])  # con el que escribio apartado, no queda ningun revisor disponible

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", espia)
    obrero.auditar("material de prueba", propuesta, auditor="gemini4", evitar="deepseek")
    assert all(c["evitar"] == "deepseek" for c in llamadas), (
        "el ultimo intento no aparto al que escribio y se reviso a si mismo; "
        "asi se quedaron 40 rondas aprobadas sin aplicar"
    )


def test_sin_otro_revisor_no_sale_aprobado_por_si_mismo(monkeypatch):
    llamadas = []

    def espia(prompt, temperatura, evitar=None, primero=None, pesado=False, clase=None, vuelta=None, **resto):
        llamadas.append({"evitar": evitar, "pesado": pesado, "vuelta": vuelta})
        if evitar is None:
            return ('{"veredicto": "APROBADO", "resumen": "me reviso a mi mismo"}', "deepseek", [])
        return ("", None, [])

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", espia)
    auditoria, quien, avisos = obrero.auditar("material de prueba", propuesta, auditor="gemini4", evitar="deepseek")
    assert quien != "deepseek", (
        "quien escribio no puede aprobarse a si mismo; sin otro revisor el trabajo queda pendiente de revision"
    )
    assert (auditoria or {}).get("veredicto") != "APROBADO", (
        "quien escribio no puede aprobarse a si mismo; sin otro revisor el trabajo queda pendiente de revision"
    )


def test_con_otro_revisor_si_se_aprueba(monkeypatch):
    def espia(prompt, temperatura, evitar=None, primero=None, pesado=False, clase=None, vuelta=None, **resto):
        return ('{"veredicto": "APROBADO", "resumen": "ok"}', "gemini4", [])

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", espia)
    auditoria, quien, _ = obrero.auditar("material de prueba", propuesta, auditor="gemini4", evitar="deepseek")
    assert quien == "gemini4" and auditoria["veredicto"] == "APROBADO"


def test_el_intento_pesado_se_sigue_haciendo(monkeypatch):
    llamadas = []

    def espia(prompt, temperatura, evitar=None, primero=None, pesado=False, clase=None, vuelta=None, **resto):
        llamadas.append({"evitar": evitar, "pesado": pesado, "vuelta": vuelta})
        if evitar is None:
            return ('{"veredicto": "APROBADO", "resumen": "me reviso a mi mismo"}', "deepseek", [])
        return ("", None, [])

    monkeypatch.setattr(obrero, "_preguntar_con_relevo", espia)
    obrero.auditar("material de prueba", propuesta, auditor="gemini4", evitar="deepseek")
    assert any(c["pesado"] is True for c in llamadas), (
        "se quito el ultimo intento con el cerebro de pago, y Julio ordeno que lo pesado siempre se intente con el"
    )
