# RESCATADO de C:igias\test_vigia_cerebro_gemini.py el 2026-08-20, antes de desechar esa copia vieja.
# Esta prueba NO existia en la carpeta buena. Pegar en C:\Users\USER\dev\Asesor Marketing\vigias\test_vigia_cerebro_gemini.py si sigue haciendo falta.

def test_sin_llave_error_claro_no_silencio():
    from cuerpo import cerebro
    _limpiar()
    assert cerebro.proveedor() == ""
    try:
        cerebro.preguntar("hola")
        assert False, "no avisó que falta la llave"
    except RuntimeError as e:
        assert "GEMINI_API_KEY" in str(e) and "GROQ_API_KEY" in str(e)


