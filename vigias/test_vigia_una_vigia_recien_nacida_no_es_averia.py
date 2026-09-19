# -*- coding: utf-8 -*-
"""VIGIA — UNA VIGIA RECIEN NACIDA NO ES UNA AVERIA. EN NINGUN SITIO.

JULIO, 2026-09-09, y lo tuvo que repetir varias veces, la ultima gritando:
"Como putas le vas a dar a una IA un fallo que es A PROPOSITO. Mira ese fallo en TODOS los
vigias y reparalo de una vez por todas."

EL FALLO, y es de los que envenenan todo el metodo:
El metodo de esta casa MANDA escribir la vigia PRIMERO y que NAZCA ROJA. Una vigia que nace
verde no probo nada. Pero varios sitios que corren las vigias contaban esa roja como algo ROTO:
  - arnes/candado_cierre.py no dejaba cerrar nunca
  - ingeniero.py, el mando vigias, devolvia fallo
Resultado: el propio metodo se castigaba a si mismo. Y esta casa ya tiene escrito que un
candado sin forma honrada de satisfacerlo EMPUJA A SALTARSELO, y eso es peor que no tenerlo.

LA CURA, QUE YA EXISTIA Y NO SE COPIABA: arnes/guardia_de_guardado.py le pregunta al guardado
si esa vigia es NUEVA (nunca guardada) o si ya estaba. Si ya estaba y ahora esta roja, ESO SI es
romper algo que estaba verde y hay que frenar. Si es nueva, es el paso 1 del metodo.

ESTA VIGIA VIGILA A LOS VIGILANTES: comprueba que TODO el que corre vigias y decide sepa
distinguirlo. Si manana alguien anade otro sitio que corra vigias sin distinguir, esta vigia lo
caza antes de que vuelva a morder.
"""
import os
import re

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Los que corren las vigias DE VERDAD y deciden con el resultado.
LOS_QUE_DECIDEN = [
    "arnes/candado_cierre.py",
    "arnes/guardia_de_guardado.py",
    "ingeniero.py",
]

# ESTOS SI DEBEN FRENAR SIEMPRE, y por eso NO distinguen: no es un olvido, es su oficio.
# arnes/guard_pasado.py corre las vigias que protegen reparaciones YA HECHAS. Si una de esas
# se cae, no hay ninguna "recien nacida" que valga: es una reparacion vieja que se rompio, o
# una prueba que desaparecio dejando la reparacion sin nada que la proteja. Ahi frenar es lo
# correcto. Esta lista existe para que nadie "arregle" manana lo que no esta roto: la vigia de
# abajo los deja en paz, pero deja escrito POR QUE.
FRENAN_SIEMPRE_A_PROPOSITO = [
    "arnes/guard_pasado.py",
]


def _vivo(rel):
    ruta = os.path.join(AQUI, *rel.split("/"))
    if not os.path.exists(ruta):
        return ""
    with open(ruta, encoding="utf-8") as f:
        codigo = f.read()
    codigo = re.sub(r'"""(?:.|\n)*?"""', " ", codigo)
    codigo = re.sub(r"'''(?:.|\n)*?'''", " ", codigo)
    return "\n".join(re.sub(r"#.*$", "", ln) for ln in codigo.splitlines())


def test_todos_los_que_deciden_distinguen_una_vigia_recien_nacida():
    """El que corre vigias y decide TIENE que preguntarle al guardado si son nuevas."""
    fallan = [rel for rel in LOS_QUE_DECIDEN if "ls-files" not in _vivo(rel) and "cat-file" not in _vivo(rel)]
    assert not fallan, (
        "ESTOS CUENTAN UNA VIGIA RECIEN NACIDA COMO SI FUERA UNA AVERIA: %s. El metodo manda "
        "que la vigia nazca ROJA, y estos la castigan por hacerlo. El metodo se castiga a si "
        "mismo, y un candado que no se puede satisfacer honradamente empuja a saltarselo."
        % ", ".join(fallan))


def test_ninguno_se_queda_a_medias_dejando_pasar_lo_que_si_se_rompio():
    """Distinguir no puede convertirse en dejar pasar TODO: si ya estaba verde y se rompio, se frena."""
    for rel in LOS_QUE_DECIDEN:
        vivo = _vivo(rel)
        if "ls-files" not in vivo and "cat-file" not in vivo:
            continue
        assert "ya_estaban" in vivo or "guardados" in vivo, (
            "%s distingue las nuevas pero NO frena cuando una vigia que YA ESTABA VERDE se "
            "rompe. Eso seria abrir la puerta de par en par: cualquier rotura pasaria "
            "disfrazada de vigia nueva." % rel)


def test_no_aparecen_sitios_nuevos_sin_distinguir():
    """Si manana alguien anade otro que corra vigias, se caza aqui antes de que muerda."""
    sospechosos = []
    for carpeta in ("arnes", "cuerpo"):
        d = os.path.join(AQUI, carpeta)
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.endswith(".py"):
                continue
            rel = carpeta + "/" + f
            if rel in LOS_QUE_DECIDEN or rel in FRENAN_SIEMPRE_A_PROPOSITO:
                continue
            vivo = _vivo(rel)
            if '"-m", "pytest"' in vivo and "returncode" in vivo and "ls-files" not in vivo:
                sospechosos.append(rel)
    assert not sospechosos, (
        "SITIOS NUEVOS QUE CORREN VIGIAS Y NO DISTINGUEN UNA RECIEN NACIDA: %s. O se les anade "
        "la distincion, o se les mete en la lista de arriba si de verdad deben frenar siempre."
        % ", ".join(sospechosos))
