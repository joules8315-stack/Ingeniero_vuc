# RESCATADO de C:igias\test_vigia_credenciales_env.py el 2026-08-20, antes de desechar esa copia vieja.
# Esta prueba NO existia en la carpeta buena. Pegar en C:\Users\USER\dev\Asesor Marketing\vigias\test_vigia_credenciales_env.py si sigue haciendo falta.

def test_carga_llaves_del_env_sin_pisar_las_existentes():
    from cuerpo import config
    d = tempfile.mkdtemp()
    ruta = os.path.join(d, ".env")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("# comentario\nGROQ_API_KEY=gsk_desde_env\nGEMINI_API_KEY=AIza_desde_env\n")
    os.environ.pop("GROQ_API_KEY", None)
    os.environ["GEMINI_API_KEY"] = "ya_estaba"  # esta NO se debe pisar
    n = config.cargar_env(ruta)
    assert os.environ.get("GROQ_API_KEY") == "gsk_desde_env", "no cargó la llave del .env"
    assert os.environ.get("GEMINI_API_KEY") == "ya_estaba", "pisó una llave existente"
    assert n >= 1
    os.environ.pop("GROQ_API_KEY", None)
    os.environ.pop("GEMINI_API_KEY", None)


