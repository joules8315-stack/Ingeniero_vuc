from cuerpo import vigilante


def _reloj_falso(inicio=0.0):
    """Reloj falso: una lista con el tiempo actual.

    Se avanza cuando se llama a dormir con los segundos que se le pasen.
    """
    class _Reloj(list):
        def __call__(self):
            return self[0]

    return _Reloj([float(inicio)])


def _dormir_falso(reloj):
    """Devuelve una funcion dormir que avanza el reloj falso."""
    def dormir(segundos):
        reloj[0] += float(segundos)
    return dormir


def _proceso_falso(reloj, termina_en=None):
    """Proceso falso.

    poll() devuelve None hasta que el reloj falso alcanza termina_en;
    a partir de ahi devuelve 0. Si termina_en es None, nunca termina.
    kill() apunta que se le llamo.
    """
    estado = {"matado": False}

    class ProcesoFalso:
        def poll(self):
            if termina_en is None:
                return None
            if reloj[0] >= termina_en:
                return 0
            return None

        def kill(self):
            estado["matado"] = True

    return ProcesoFalso(), estado


def _avance_que_sube():
    """Funcion avance que devuelve un numero que sube cada vez."""
    caja = {"n": 0}

    def avance():
        caja["n"] += 1
        return caja["n"]

    return avance


def _avance_quieto():
    """Funcion avance que devuelve siempre el mismo numero."""
    def avance():
        return 7

    return avance


def test_proceso_termina_antes_del_limite():
    """(1) Si el proceso termina a los 50, devuelve 'termino' y no se llamo a kill."""
    reloj = _reloj_falso()
    proceso, estado = _proceso_falso(reloj, termina_en=50)
    resultado = vigilante.esperar(
        proceso=proceso,
        limite=100,
        sin_avance=30,
        tope_duro=1000,
        avance=_avance_que_sube(),
        dormir=_dormir_falso(reloj),
        reloj=reloj,
    )
    assert resultado == "termino"
    assert estado["matado"] is False


def test_proceso_termina_pasado_el_limite_si_avanza():
    """(2) Si termina a los 300 y avance sube, devuelve 'termino' y no se llamo a kill."""
    reloj = _reloj_falso()
    proceso, estado = _proceso_falso(reloj, termina_en=300)
    resultado = vigilante.esperar(
        proceso=proceso,
        limite=100,
        sin_avance=30,
        tope_duro=1000,
        avance=_avance_que_sube(),
        dormir=_dormir_falso(reloj),
        reloj=reloj,
    )
    assert resultado == "termino"
    assert estado["matado"] is False


def test_proceso_colgado_sin_avance():
    """(3) Si nunca termina y avance no sube, devuelve 'colgada', se mato y el reloj no paso de 100+30+10."""
    reloj = _reloj_falso()
    proceso, estado = _proceso_falso(reloj, termina_en=None)
    resultado = vigilante.esperar(
        proceso=proceso,
        limite=100,
        sin_avance=30,
        tope_duro=1000,
        avance=_avance_quieto(),
        dormir=_dormir_falso(reloj),
        reloj=reloj,
    )
    assert resultado == "colgada"
    assert estado["matado"] is True
    assert reloj[0] <= 100 + 30 + 10


def test_proceso_tope_duro():
    """(4) Si nunca termina pero avance sube siempre, devuelve 'tope_duro', se mato y el reloj llego al menos a 1000."""
    reloj = _reloj_falso()
    proceso, estado = _proceso_falso(reloj, termina_en=None)
    resultado = vigilante.esperar(
        proceso=proceso,
        limite=100,
        sin_avance=30,
        tope_duro=1000,
        avance=_avance_que_sube(),
        dormir=_dormir_falso(reloj),
        reloj=reloj,
    )
    assert resultado == "tope_duro"
    assert estado["matado"] is True
    assert reloj[0] >= 1000
