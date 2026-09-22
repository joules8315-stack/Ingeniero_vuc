import json

from cuerpo import director


def _escribir_ordenes(raiz, ordenes):
    memoria = raiz / "memoria"
    memoria.mkdir(parents=True, exist_ok=True)
    (memoria / "ORDENES.json").write_text(
        json.dumps(ordenes, ensure_ascii=False), encoding="utf-8"
    )
    (memoria / "HUELLAS_QUE_FALLARON.jsonl").write_text("", encoding="utf-8")


def _leer_ordenes(raiz):
    return json.loads((raiz / "memoria" / "ORDENES.json").read_text(encoding="utf-8"))


def _ordenes_de_mentira():
    return [
        {
            "id": "7",
            "titulo": "Arreglar el medidor",
            "pieza": "cuerpo/medidor.py",
            "encargo": "que cuente bien",
            "vigia": "vigias/test_vigia_medidor.py",
            "estado": "fallo",
            "fallos_seguidos": 3,
        },
        {
            "id": "8",
            "titulo": "Orden que pasa",
            "pieza": "cuerpo/pieza_ocho.py",
            "encargo": "que pase",
            "vigia": "",
            "estado": "pendiente",
            "fallos_seguidos": 0,
        },
        {
            "id": "9",
            "titulo": "Orden que falla",
            "pieza": "cuerpo/pieza_nueve.py",
            "encargo": "que falle",
            "vigia": "",
            "estado": "pendiente",
            "fallos_seguidos": 0,
        },
        {
            "id": "10",
            "titulo": "Otra pendiente",
            "pieza": "cuerpo/pieza_diez.py",
            "encargo": "que siga pendiente",
            "vigia": "",
            "estado": "pendiente",
            "fallos_seguidos": 0,
        },
    ]


def test_estado_cuenta_por_estado_y_muestra_la_primera_pendiente(tmp_path):
    _escribir_ordenes(tmp_path, _ordenes_de_mentira())

    texto = director.estado(tmp_path)

    assert isinstance(texto, str)
    assert "pendiente: 3" in texto
    assert "fallo: 1" in texto
    assert "8" in texto
    assert "Orden que pasa" in texto


def test_orden_nueva_mete_la_orden_primera_y_pendiente(tmp_path):
    _escribir_ordenes(tmp_path, _ordenes_de_mentira())

    texto = json.dumps(
        {
            "id": "900",
            "titulo": "Orden nueva de mentira",
            "pieza": "cuerpo/pieza_nueva.py",
            "encargo": "que haga algo",
            "vigia": "vigias/test_vigia_pieza_nueva.py",
        },
        ensure_ascii=False,
    )

    ok, motivo = director.orden_nueva(tmp_path, texto)

    assert ok is True
    assert isinstance(motivo, str)
    ordenes = _leer_ordenes(tmp_path)
    assert ordenes[0]["id"] == "900"
    assert ordenes[0]["estado"] == "pendiente"
    assert ordenes[0]["titulo"] == "Orden nueva de mentira"


def test_orden_nueva_rechaza_id_repetido_y_texto_malo(tmp_path):
    _escribir_ordenes(tmp_path, _ordenes_de_mentira())
    antes = _leer_ordenes(tmp_path)

    repetida = json.dumps(
        {
            "id": "7",
            "titulo": "Otra con el mismo id",
            "pieza": "cuerpo/otra.py",
            "encargo": "que no entre",
            "vigia": "vigias/test_vigia_otra.py",
        },
        ensure_ascii=False,
    )
    ok, motivo = director.orden_nueva(tmp_path, repetida)
    assert ok is False
    assert isinstance(motivo, str)
    assert _leer_ordenes(tmp_path) == antes

    ok, motivo = director.orden_nueva(tmp_path, "esto no es json")
    assert ok is False
    assert isinstance(motivo, str)
    assert _leer_ordenes(tmp_path) == antes

    sin_encargo = json.dumps(
        {
            "id": "901",
            "titulo": "Sin encargo",
            "pieza": "cuerpo/pieza_nueva.py",
            "vigia": "vigias/test_vigia_pieza_nueva.py",
        },
        ensure_ascii=False,
    )
    ok, motivo = director.orden_nueva(tmp_path, sin_encargo)
    assert ok is False
    assert isinstance(motivo, str)
    assert _leer_ordenes(tmp_path) == antes

    sin_vigia = json.dumps(
        {
            "id": "902",
            "titulo": "Sin vigia",
            "pieza": "cuerpo/pieza_nueva.py",
            "encargo": "que haga algo",
        },
        ensure_ascii=False,
    )
    ok, motivo = director.orden_nueva(tmp_path, sin_vigia)
    assert ok is False
    assert isinstance(motivo, str)
    assert _leer_ordenes(tmp_path) == antes


def test_reintentar_deja_la_orden_pendiente_y_limpia_sus_huellas(tmp_path):
    _escribir_ordenes(tmp_path, _ordenes_de_mentira())
    huellas = tmp_path / "memoria" / "HUELLAS_QUE_FALLARON.jsonl"
    huellas.write_text(
        json.dumps({"id": "7", "huella": "algo fallo"}, ensure_ascii=False)
        + "\n"
        + json.dumps({"id": "9", "huella": "otra cosa fallo"}, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )

    ok, motivo = director.reintentar(tmp_path, "7")

    assert ok is True
    assert isinstance(motivo, str)
    ordenes = _leer_ordenes(tmp_path)
    orden_7 = [o for o in ordenes if o["id"] == "7"][0]
    assert orden_7["estado"] == "pendiente"
    assert orden_7["fallos_seguidos"] == 0

    lineas = [
        l for l in huellas.read_text(encoding="utf-8").splitlines() if l.strip()
    ]
    ids = [json.loads(l)["id"] for l in lineas]
    assert "7" not in ids
    assert "9" in ids


def test_hecha_marca_hecha_cuando_la_vigia_pasa(tmp_path):
    vigia_ok = tmp_path / "test_vigia_que_pasa.py"
    vigia_ok.write_text(
        "def test_ok():\n    assert True\n", encoding="utf-8"
    )

    ordenes = _ordenes_de_mentira()
    for o in ordenes:
        if o["id"] == "8":
            o["vigia"] = str(vigia_ok)
    _escribir_ordenes(tmp_path, ordenes)

    ok, motivo = director.hecha(tmp_path, "8")

    assert ok is True
    assert isinstance(motivo, str)
    ordenes = _leer_ordenes(tmp_path)
    orden_8 = [o for o in ordenes if o["id"] == "8"][0]
    assert orden_8["estado"] == "hecha"


def test_hecha_no_marca_hecha_cuando_la_vigia_falla(tmp_path):
    vigia_mal = tmp_path / "test_vigia_que_falla.py"
    vigia_mal.write_text(
        "def test_ok():\n    assert False\n", encoding="utf-8"
    )

    ordenes = _ordenes_de_mentira()
    for o in ordenes:
        if o["id"] == "9":
            o["vigia"] = str(vigia_mal)
    _escribir_ordenes(tmp_path, ordenes)

    ok, motivo = director.hecha(tmp_path, "9")

    assert ok is False
    assert isinstance(motivo, str)
    ordenes = _leer_ordenes(tmp_path)
    orden_9 = [o for o in ordenes if o["id"] == "9"][0]
    assert orden_9["estado"] != "hecha"
