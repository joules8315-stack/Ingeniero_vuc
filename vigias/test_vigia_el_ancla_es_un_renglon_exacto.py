def test_el_candado_frena_un_ancla_de_varios_renglones():
    """Comprueba que el candado arnes/candado_ancla.py rechaza un fragmento de varios renglones
    y acepta uno de un solo renglón que aparece una única vez en el archivo."""
    candado_path = Path(__file__).parents[1] / "arnes" / "candado_ancla.py"
    assert candado_path.is_file(), f"Falta el candado {candado_path}"
    # ... resto del código ...