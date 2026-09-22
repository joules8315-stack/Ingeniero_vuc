import subprocess

from cuerpo import capataz
from cuerpo import vigilante


class PopenFalso:
    """Popen de mentira: escribe la salida en el archivo que le pasan y no cuelga."""

    llamadas = []

    def __init__(self, comando, **kw):
        self.comando = comando
        self.kw = kw
        PopenFalso.llamadas.append(kw)
        self.pid = 1
        self.returncode = 0
        salida = kw.get('stdout')
        if salida is not None:
            salida.write('salida del equipo')
            salida.flush()

    def poll(self):
        return 0

    def kill(self):
        return None

    def wait(self, timeout=None):
        return 0


def _preparar(monkeypatch, respuesta):
    """Deja el Popen falso y el vigilante falso en su sitio y devuelve el apuntador."""
    PopenFalso.llamadas = []
    monkeypatch.setattr(capataz.subprocess, 'Popen', PopenFalso)
    apuntes = []

    def esperar_falso(*args, **kw):
        apuntes.append({'args': args, 'kw': kw})
        return respuesta

    monkeypatch.setattr(vigilante, 'esperar', esperar_falso)
    return apuntes


def test_si_el_equipo_termina_la_salida_se_recoge(monkeypatch):
    apuntes = _preparar(monkeypatch, 'termino')
    resultado = capataz.lanzar_al_equipo('ingeniero', {'id': '1', 'encargo': 'x'})
    assert isinstance(resultado, dict)
    assert 'salida del equipo' in resultado['salida']
    assert len(apuntes) == 1
    limite = apuntes[0]['kw'].get('limite', apuntes[0]['kw'].get('tope_segundos'))
    assert limite == capataz.LIMITE_TAREA_SEGUNDOS


def test_si_el_equipo_se_cuelga_lo_que_dijo_no_se_pierde(monkeypatch):
    _preparar(monkeypatch, 'colgada')
    resultado = capataz.lanzar_al_equipo('ingeniero', {'id': '1', 'encargo': 'x'})
    assert isinstance(resultado, dict)
    assert resultado['salida'].startswith('COLGADA:')
    assert 'salida del equipo' in resultado['salida']


def test_al_popen_no_se_le_pasa_una_tuberia_sin_vaciar(monkeypatch):
    _preparar(monkeypatch, 'termino')
    capataz.lanzar_al_equipo('ingeniero', {'id': '1', 'encargo': 'x'})
    assert len(PopenFalso.llamadas) >= 1
    for kw in PopenFalso.llamadas:
        assert kw.get('stdout') != subprocess.PIPE


def test_el_tipo_de_fallo_reconoce_la_colgada():
    assert capataz.tipo_de_fallo('COLGADA: sin avance') == 'colgada'
