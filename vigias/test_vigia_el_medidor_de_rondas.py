"""Vigia del medidor de rondas.

Prueba la pieza arnes/medidor_de_rondas.py, que todavia no existe y que se
crea en este mismo encargo. La pieza expone una funcion `contar(raiz, dia)`
que lee memoria/TRABAJOS_DEL_EQUIPO.log y devuelve un diccionario con al
menos: rondas, aprobados, guardados y la razon en palabras.

Formato de cada renglon del registro (separado por barras verticales):
    fecha y hora | quien escribio | quien reviso | veredicto | archivos

Si esta vigia se pone roja, se pierde: la unica comprobacion automatica de
que el medidor de rondas cuenta bien lo aprobado y lo rechazado de un dia.
Sin ella, el punto E del plan de raiz (cuantas rondas aprobadas llegan al
disco) vuelve a medirse a ojo.
"""

import sys
from pathlib import Path

import pytest


# La pieza vive en la carpeta arnes, igual que las demas vigias del arnes.
# Se anade la raiz del proyecto al sys.path para poder importarla como
# `arnes.medidor_de_rondas`, que es como la llaman las otras vigias.
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from arnes.medidor_de_rondas import contar  # noqa: E402


DIA_OBJETIVO = "2026-09-19"
DIA_AJENO = "2026-09-18"


# Cuatro renglones con el mismo formato que usa hoy el registro:
# fecha y hora | quien escribio | quien reviso | veredicto | archivos
# Tres del dia 2026-09-19 (dos APROBADO, uno RECHAZADO) y uno de otro dia.
RENGLONES = [
    "2026-09-19 09:15:00 | cline | opencode | APROBADO | arnes/medidor_de_rondas.py",
    "2026-09-19 10:40:00 | deepseek | opencode | APROBADO | vigias/test_vigia_el_medidor_de_rondas.py",
    "2026-09-19 11:05:00 | cline | opencode | RECHAZADO | arnes/otra_pieza.py",
    "2026-09-18 23:59:00 | cline | opencode | APROBADO | arnes/pieza_de_ayer.py",
]


def _armar_raiz_con_log(tmp_path: Path) -> Path:
    """Arma una carpeta raiz con memoria/TRABAJOS_DEL_EQUIPO.log dentro."""
    raiz = tmp_path / "raiz"
    memoria = raiz / "memoria"
    memoria.mkdir(parents=True, exist_ok=True)
    log = memoria / "TRABAJOS_DEL_EQUIPO.log"
    log.write_text("\n".join(RENGLONES) + "\n", encoding="utf-8")
    return raiz


def test_prueba_1_cuenta_las_rondas_del_dia(tmp_path):
    """PRUEBA 1: tres rondas del dia, dos aprobadas.

    Si esto falla se pierde: la garantia de que el medidor separa por dia y
    distingue aprobado de rechazado. Sin esa garantia, el punto E del plan
    de raiz (cuantas rondas aprobadas llegan al disco) se mide mal y nadie
    lo nota.
    """
    raiz = _armar_raiz_con_log(tmp_path)

    resultado = contar(raiz, DIA_OBJETIVO)

    assert isinstance(resultado, dict), (
        "contar debe devolver un diccionario con las cuentas del dia; "
        "si devuelve otra cosa, ninguna vigia ni informe puede leer el "
        "resultado y el punto E del plan de raiz queda ciego."
    )

    assert resultado.get("rondas") == 3, (
        "Se pierde la cuenta de rondas del dia: en el registro hay 3 "
        "renglones del 2026-09-19 y contar debe devolver rondas=3. Si "
        "devuelve otro numero, el medidor esta contando de mas (incluye "
        "otros dias) o de menos (se salta renglones), y el informe del "
        "dia miente."
    )

    assert resultado.get("aprobados") == 2, (
        "Se pierde la cuenta de aprobados del dia: de los 3 renglones del "
        "2026-09-19, 2 llevan veredicto APROBADO y contar debe devolver "
        "aprobados=2. Si falla, el punto E del plan de raiz (cuantas rondas "
        "aprobadas llegan al disco) se mide mal y las rondas perdidas "
        "vuelven a pasar sin que nadie las vea."
    )


def test_prueba_2_dia_sin_nada_no_revienta_y_da_cero(tmp_path):
    """PRUEBA 2: un dia sin renglones no revienta y da rondas=0.

    Si esto falla se pierde: la confianza de que el medidor se puede llamar
    cualquier dia, tambien los festivos y los dias sin trabajo. Un medidor
    que revienta con un dia vacio obliga a mirarlo a mano antes de usarlo.
    """
    raiz = _armar_raiz_con_log(tmp_path)

    resultado = contar(raiz, "2026-01-01")

    assert isinstance(resultado, dict), (
        "contar debe devolver un diccionario tambien cuando el dia no tiene "
        "renglones; si revienta o devuelve otra cosa, el informe del dia no "
        "se puede generar en los dias sin trabajo."
    )

    assert resultado.get("rondas") == 0, (
        "Se pierde la garantia de que un dia sin renglones da rondas=0. Si "
        "devuelve otra cosa, el medidor esta inventando rondas que no "
        "existen y el informe del dia deja de ser fiable."
    )


def test_prueba_3_la_razon_es_texto_y_nombra_el_dia(tmp_path):
    """PRUEBA 3: la razon en palabras es texto no vacio y nombra el dia.

    Si esto falla se pierde: la explicacion legible del resultado. Sin ella, "
    el numero de rondas aparece sin decir a que dia se refiere ni por que, y "
    quien lo lea no puede comprobar que se midio el dia que pidio.
    """
    raiz = _armar_raiz_con_log(tmp_path)

    resultado = contar(raiz, DIA_OBJETIVO)

    razon = resultado.get("razon")

    assert isinstance(razon, str) and razon.strip() != "", (
        "Se pierde la explicacion en palabras del resultado: contar debe "
        "devolver una razon que sea texto y no este vacia. Sin ella, el "
        "numero de rondas aparece sin justificacion y nadie puede auditar "
        "de donde sale."
    )

    assert DIA_OBJETIVO in razon, (
        "Se pierde la trazabilidad del dia medido: la razon en palabras debe "
        "nombrar el dia pedido (2026-09-19). Si no lo nombra, quien lea el "
        "informe no puede saber a que dia se refiere la cuenta y se pueden "
        "confundir los numeros de dos dias distintos."
    )


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
