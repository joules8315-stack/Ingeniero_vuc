import json
import os
import sys
import time
import pytest
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "arnes"))
import candado_equipo
import guardia_de_guardado

# LO ORDENA JULIO (2026-09-12): "Ninguna IA, ninguna, puede pasar a trabajar en estos proyectos sin equipo, arnes y vigias. Obligalo, que no le quede opcion." Y sobre el guardia: "que se acuerde de todo".

# ESTA VIGIA NACE ROJA en las pruebas marcadas ROJA. Las demas pueden nacer verdes: protegen que no se afloje.

# LO QUE YA EXISTE (nombres exactos, comprobados en el codigo):
#   arnes/candado_equipo.py:
#      guardar_veredicto(tarea, archivos, obrero, auditor, veredicto)   -> escribe el veredicto en la ruta de la variable de entorno INGENIERO_VEREDICTO_TEST (si esta puesta) y un renglon en el cuaderno de la variable INGENIERO_BALANCE_EQUIPO (si esta puesta).
#      _fallos_mecanicos(tarea, archivos)  -> lee la memoria real; EN LA VIGIA SE SUSTITUYE con monkeypatch por una funcion que devuelve [] para no tocar la memoria de verdad.
#   arnes/guardia_de_guardado.py:
#      _cubierto_por_equipo(archivos)  -> True si todo el codigo que se guarda lo aprobo el equipo, False si no, None si no hay codigo. Lee la ruta de INGENIERO_VEREDICTO_TEST.
#      main()  -> devuelve 0 si deja guardar, 1 si frena. Por dentro llama a _lo_que_se_va_a_guardar(raiz), _hay_llaves(raiz, archivos), _vigias(raiz), _apuntar(raiz, texto) y _apuntar_balance(raiz, tipo, archivos). Lee la variable de entorno JULIO_LO_AUTORIZA (la llave de Julio: vale si trae 20 letras o mas).
#  Para importar:  AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(AQUI, "arnes")); import candado_equipo; import guardia_de_guardado

# EL CUADERNO NUEVO (lo que la reparacion va a crear, y esta vigia exige):
#   Se llama .veredictos_recientes.jsonl y vive EN LA MISMA CARPETA que el archivo de veredicto (os.path.dirname de INGENIERO_VEREDICTO_TEST). Un veredicto por renglon, en JSON, con al menos: cuando (numero de time.time()), archivos (lista), veredicto (texto), reviso_a_si_mismo (verdadero o falso).

# FIXTURE autouse (todo en la carpeta de mentira tmp_path, NUNCA la memoria real):
#   monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
#   monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
#   monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
#   monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])


# LAS PRUEBAS (nombres de archivo de mentira que no existen en ningun proyecto):

# 1. test_dos_aprobaciones_seguidas_cubren_las_dos   (ROJA)
def test_dos_aprobaciones_seguidas_cubren_las_dos(monkeypatch, tmp_path):
    """El guardia olvida la primera aprobacion y frenaria trabajo bueno."""
    import subprocess
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo)
    os.makedirs(repo / "web", exist_ok=True)
    with open(repo / "web" / "bloque_crm_de_prueba.py", "w") as f:
        f.write("# crm de prueba\n")
    with open(repo / "web" / "bloque_agenda_de_prueba.py", "w") as f:
        f.write("# agenda de prueba\n")
    subprocess.run(["git", "add", "-A"], cwd=repo)
    monkeypatch.chdir(repo)

    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    candado_equipo.guardar_veredicto("pantalla de clientes", ["web/bloque_crm_de_prueba.py"], "groq", "deepseek", "APROBADO")
    candado_equipo.anotar_huella(str(repo), "web/bloque_crm_de_prueba.py")
    candado_equipo.guardar_veredicto("pantalla de agenda", ["web/bloque_agenda_de_prueba.py"], "groq", "deepseek", "APROBADO")
    candado_equipo.anotar_huella(str(repo), "web/bloque_agenda_de_prueba.py")

    assert guardia_de_guardado._cubierto_por_equipo(["web/bloque_crm_de_prueba.py", "web/bloque_agenda_de_prueba.py"]) is True

    # SABOTAJE: lo cambiado a mano despues de la aprobacion NO entra (A-34)
    with open(repo / "web" / "bloque_crm_de_prueba.py", "w") as f:
        f.write("# crm de prueba CAMBIADO A MANO\n")
    subprocess.run(["git", "add", "-A"], cwd=repo)
    assert guardia_de_guardado._cubierto_por_equipo(["web/bloque_crm_de_prueba.py", "web/bloque_agenda_de_prueba.py"]) is False, 'lo cambiado a mano despues de la aprobacion NO entra (A-34)'


# 2. test_guardar_el_veredicto_lo_apunta_en_el_cuaderno   (ROJA)
def test_guardar_el_veredicto_lo_apunta_en_el_cuaderno(monkeypatch, tmp_path):
    """El cuaderno no registra el veredicto."""
    veredicto_file = tmp_path / ".veredictos_recientes.jsonl"
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    candado_equipo.guardar_veredicto("tarea", ["x_de_prueba.py"], "groq", "deepseek", "APROBADO")

    assert veredicto_file.exists()
    with open(veredicto_file, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["veredicto"] == "APROBADO"
        assert "x_de_prueba.py" in data["archivos"]


# 3. test_un_aprobado_de_hace_mas_de_24_horas_no_vale
def test_un_aprobado_de_hace_mas_de_24_horas_no_vale(monkeypatch, tmp_path):
    """Un permiso de ayer no vale para hoy."""
    veredicto_file = tmp_path / ".veredictos_recientes.jsonl"
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    # Escribir A MANO en tmp_path / ".veredictos_recientes.jsonl" un renglon
    with open(veredicto_file, 'w') as f:
        f.write(json.dumps({
            "cuando": time.time() - 25*3600,
            "archivos": ["viejo_de_prueba.py"],
            "veredicto": "APROBADO",
            "reviso_a_si_mismo": False
        }) + '\n')

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    assert guardia_de_guardado._cubierto_por_equipo(["viejo_de_prueba.py"]) is False


# 4. test_un_rechazado_no_vale
def test_un_rechazado_no_vale(monkeypatch, tmp_path):
    """Un veredicto de RECHAZADO no deberia ser valido."""
    veredicto_file = tmp_path / ".veredictos_recientes.jsonl"
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    with open(veredicto_file, 'w') as f:
        f.write(json.dumps({
            "cuando": time.time(),
            "archivos": ["viejo_de_prueba.py"],
            "veredicto": "RECHAZADO",
            "reviso_a_si_mismo": False
        }) + '\n')

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    assert guardia_de_guardado._cubierto_por_equipo(["viejo_de_prueba.py"]) is False


# 5. test_quien_se_reviso_a_si_mismo_no_abre
def test_quien_se_reviso_a_si_mismo_no_abre(monkeypatch, tmp_path):
    """Uno escribe y OTRO distinto revisa; revisarse a si mismo no es equipo."""
    veredicto_file = tmp_path / ".veredictos_recientes.jsonl"
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    with open(veredicto_file, 'w') as f:
        f.write(json.dumps({
            "cuando": time.time(),
            "archivos": ["viejo_de_prueba.py"],
            "veredicto": "APROBADO",
            "reviso_a_si_mismo": True
        }) + '\n')

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    assert guardia_de_guardado._cubierto_por_equipo(["viejo_de_prueba.py"]) is False


# 6. test_renglones_rotos_no_tumban_al_guardia
def test_renglones_rotos_no_tumban_al_guardia(monkeypatch, tmp_path):
    """Renglones rotos o vacios en el cuaderno no deben lanzar errores."""
    import subprocess
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo)
    with open(repo / "bueno_de_prueba.py", "w") as f:
        f.write("# bueno de prueba\n")
    subprocess.run(["git", "add", "-A"], cwd=repo)
    monkeypatch.chdir(repo)

    veredicto_file = tmp_path / ".veredictos_recientes.jsonl"
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    with open(veredicto_file, 'w') as f:
        f.write("esto no es json\n")
        f.write("\n")
        f.write(json.dumps({
            "cuando": time.time(),
            "archivos": ["bueno_de_prueba.py"],
            "veredicto": "APROBADO",
            "reviso_a_si_mismo": False
        }) + '\n')

    huellas_file = tmp_path / ".huellas_aprobadas.jsonl"
    with open(huellas_file, 'w') as f:
        f.write("esto no es json\n")
        f.write("\n")

    candado_equipo.guardar_veredicto("tarea", ["bueno_de_prueba.py"], "obrero", "auditor", "APROBADO")
    candado_equipo.anotar_huella(str(repo), "bueno_de_prueba.py")

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    assert guardia_de_guardado._cubierto_por_equipo(["bueno_de_prueba.py"]) is True


# 7. test_sin_codigo_sigue_sin_pedir_equipo
def test_sin_codigo_sigue_sin_pedir_equipo(monkeypatch, tmp_path):
    """Si no hay codigo que guardar, _cubierto_por_equipo debe devolver None."""
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    assert guardia_de_guardado._cubierto_por_equipo(["NOTAS_de_prueba.md"]) is None


# 8. test_el_guardado_a_solas_se_FRENA   (ROJA)
def test_el_guardado_a_solas_se_FRENA(monkeypatch, tmp_path):
    """El guardado a solas paso; la ley de Julio no se esta cumpliendo."""
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    # Monkeypatch para simular el comportamiento de las funciones internas de guardia_de_guardado
    monkeypatch.setattr(guardia_de_guardado, "_lo_que_se_va_a_guardar", lambda raiz: ["web/a_solas_de_prueba.py"])
    monkeypatch.setattr(guardia_de_guardado, "_hay_llaves", lambda raiz, archivos: [])
    monkeypatch.setattr(guardia_de_guardado, "_vigias", lambda raiz: (True, "todo verde de mentira"))
    monkeypatch.setattr(guardia_de_guardado, "_apuntar", lambda raiz, texto: None)
    monkeypatch.setattr(guardia_de_guardado, "_apuntar_balance", lambda raiz, tipo, archivos: None)

    # Sin ningun veredicto, main() tiene que devolver 1 (frena)
    assert guardia_de_guardado.main() == 1


# 9. test_lo_aprobado_por_el_equipo_si_se_guarda
def test_lo_aprobado_por_el_equipo_si_se_guarda(monkeypatch, tmp_path):
    """Si el equipo aprobo, el guardado debe permitirse."""
    import subprocess
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo)
    os.makedirs(repo / "web", exist_ok=True)
    with open(repo / "web" / "a_solas_de_prueba.py", "w") as f:
        f.write("# a solas de prueba\n")
    subprocess.run(["git", "add", "-A"], cwd=repo)
    monkeypatch.chdir(repo)

    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    # Simular el guardado de un veredicto aprobado
    candado_equipo.guardar_veredicto("tarea", ["web/a_solas_de_prueba.py"], "groq", "deepseek", "APROBADO")
    candado_equipo.anotar_huella(str(repo), "web/a_solas_de_prueba.py")

    # Monkeypatch para simular el comportamiento de las funciones internas de guardia_de_guardado
    monkeypatch.setattr(guardia_de_guardado, "_lo_que_se_va_a_guardar", lambda raiz: ["web/a_solas_de_prueba.py"])
    monkeypatch.setattr(guardia_de_guardado, "_hay_llaves", lambda raiz, archivos: [])
    monkeypatch.setattr(guardia_de_guardado, "_vigias", lambda raiz: (True, "todo verde de mentira"))
    monkeypatch.setattr(guardia_de_guardado, "_apuntar", lambda raiz, texto: None)
    monkeypatch.setattr(guardia_de_guardado, "_apuntar_balance", lambda raiz, tipo, archivos: None)

    # main() tiene que devolver 0 (permite guardar)
    assert guardia_de_guardado.main() == 0


# 10. test_un_documento_se_guarda_sin_equipo
def test_un_documento_se_guarda_sin_equipo(monkeypatch, tmp_path):
    """Los documentos que no son codigo deben guardarse sin pedir equipo."""
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    monkeypatch.delenv("JULIO_LO_AUTORIZA", raising=False)
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    # Monkeypatch para simular el comportamiento de las funciones internas de guardia_de_guardado
    monkeypatch.setattr(guardia_de_guardado, "_lo_que_se_va_a_guardar", lambda raiz: ["NOTAS_de_prueba.md"])
    monkeypatch.setattr(guardia_de_guardado, "_hay_llaves", lambda raiz, archivos: [])
    monkeypatch.setattr(guardia_de_guardado, "_vigias", lambda raiz: (True, "todo verde de mentira"))
    monkeypatch.setattr(guardia_de_guardado, "_apuntar", lambda raiz, texto: None)
    monkeypatch.setattr(guardia_de_guardado, "_apuntar_balance", lambda raiz, tipo, archivos: None)

    # main() devuelve 0 (permite guardar)
    assert guardia_de_guardado.main() == 0


# 11. test_la_llave_de_julio_con_motivo_abre
def test_la_llave_de_julio_con_motivo_abre(monkeypatch, tmp_path):
    """La llave de Julio con un motivo valido debe permitir el guardado."""
    monkeypatch.setenv("INGENIERO_VEREDICTO_TEST", str(tmp_path / "veredicto.json"))
    monkeypatch.setenv("INGENIERO_BALANCE_EQUIPO", str(tmp_path / "trabajos.log"))
    # La llave de Julio debe tener 20 letras o mas
    monkeypatch.setenv("JULIO_LO_AUTORIZA", "lo autorizo porque es una urgencia del cliente")
    monkeypatch.setattr(candado_equipo, "_fallos_mecanicos", lambda tarea, archivos=None: [])

    # Simular la importacion de guardia_de_guardado
    AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(AQUI, "arnes"))
    import guardia_de_guardado

    # Monkeypatch para simular el comportamiento de las funciones internas de guardia_de_guardado
    monkeypatch.setattr(guardia_de_guardado, "_lo_que_se_va_a_guardar", lambda raiz: ["web/a_solas_de_prueba.py"])
    monkeypatch.setattr(guardia_de_guardado, "_hay_llaves", lambda raiz, archivos: [])
    monkeypatch.setattr(guardia_de_guardado, "_vigias", lambda raiz: (True, "todo verde de mentira"))
    monkeypatch.setattr(guardia_de_guardado, "_apuntar", lambda raiz, texto: None)
    monkeypatch.setattr(guardia_de_guardado, "_apuntar_balance", lambda raiz, tipo, archivos: None)

    # main() devuelve 0 (permite guardar)
    assert guardia_de_guardado.main() == 0
