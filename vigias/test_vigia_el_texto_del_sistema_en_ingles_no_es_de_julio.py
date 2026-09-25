def test_el_texto_del_sistema_en_ingles_no_es_de_julio():
    assert not parece_una_orden('Generate a concise, single-line task title of at most 36 characters and under five words where possible')
    assert not parece_una_orden('Write a brief catch-up for a user returning to this Codex task')
    assert parece_una_orden('Busca donde esta toda la informacion que necesitas para reparar el equipo')
