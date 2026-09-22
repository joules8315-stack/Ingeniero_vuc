"""Vigia: si Big Pickle falla al auditar, revisa grok47.

Vigila cuerpo/obrero.py::auditar cuando se le pide auditor='bigpickle'.

Reglas que comprueba:
  1. Si bigpickle.preguntar devuelve ('', ['timeout']), el relevo lo hace grok
     y el veredicto es APROBADO con quien_reviso == 'grok47'.
  2. En ese caso NO se llama a obrero._preguntar_con_relevo.
  3. Si grok.preguntar tambien devuelve ('', ['timeout']), entonces SI se llama
     a obrero._preguntar_con_relevo, como hoy.

Nunca se llama a Claude: obrero._claude_directo se monkeypatchea para que
lance AssertionError si alguien lo invoca.
"""

from cuerpo import obrero
from cuerpo import bigpickle
from cuerpo import grok


PAQUETE = ''
PROPUESTA = {'archivo': 'x.py'}


def _claude_prohibido(*args, **kwargs):
    raise AssertionError('no se debe llamar a Claude en esta vigia')


def _preparar(monkeypatch, grok_respuesta, apuntes):
    """Deja los dobles puestos. apuntes es un dict donde se anotan las llamadas."""
    monkeypatch.setattr(obrero, '_claude_directo', _claude_prohibido)

    def _bp_preguntar(*args, **kwargs):
        apuntes['bigpickle'] = apuntes.get('bigpickle', 0) + 1
        return ('', ['timeout'])

    def _grok_preguntar(*args, **kwargs):
        apuntes['grok'] = apuntes.get('grok', 0) + 1
        return grok_respuesta

    def _relevo_preguntar(*args, **kwargs):
        apuntes['relevo'] = apuntes.get('relevo', 0) + 1
        return ('', None, [])

    monkeypatch.setattr(bigpickle, 'preguntar', _bp_preguntar)
    monkeypatch.setattr(grok, 'preguntar', _grok_preguntar)
    monkeypatch.setattr(obrero, '_preguntar_con_relevo', _relevo_preguntar)


def test_si_big_pickle_falla_revisa_grok(monkeypatch):
    apuntes = {}
    _preparar(
        monkeypatch,
        ('{"veredicto": "APROBADO", "resumen_para_el_jefe": "ok"}', []),
        apuntes,
    )

    auditoria, quien, avisos = obrero.auditar(
        '', {'archivo': 'x.py'}, auditor='bigpickle', evitar='deepseek')

    assert quien == 'grok47', 'deberia revisar grok47, reviso %r' % (quien,)
    assert auditoria is not None, 'la auditoria no puede ser None'
    assert auditoria.get('veredicto') == 'APROBADO', (
        'el veredicto deberia ser APROBADO, fue %r' % (auditoria.get('veredicto'),))
    assert apuntes.get('grok', 0) >= 1, 'grok deberia haber sido llamado'


def test_no_se_llama_al_relevo_si_grok_contesta(monkeypatch):
    apuntes = {}
    _preparar(
        monkeypatch,
        ('{"veredicto": "APROBADO", "resumen_para_el_jefe": "ok"}', []),
        apuntes,
    )

    auditoria, quien, avisos = obrero.auditar(
        '', {'archivo': 'x.py'}, auditor='bigpickle', evitar='deepseek')

    assert apuntes.get('relevo', 0) == 0, (
        'no se debe llamar a obrero._preguntar_con_relevo cuando grok contesta; '
        'se llamo %d veces' % (apuntes.get('relevo', 0),))


def test_si_grok_tambien_falla_si_se_llama_al_relevo(monkeypatch):
    apuntes = {}
    _preparar(monkeypatch, ('', ['timeout']), apuntes)

    auditoria, quien, avisos = obrero.auditar(
        '', {'archivo': 'x.py'}, auditor='bigpickle', evitar='deepseek')

    assert apuntes.get('relevo', 0) >= 1, (
        'si grok tambien falla, se debe llamar a obrero._preguntar_con_relevo; '
        'se llamo %d veces' % (apuntes.get('relevo', 0),))
