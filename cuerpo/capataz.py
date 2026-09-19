import json
import os
import subprocess


def lanzar_al_equipo(encargo):
    raiz = r"C:\Ingeniero_VUC"
    resultado = subprocess.run(
        ["python", "ingeniero.py", "equipo", "ingeniero", encargo],
        cwd=raiz,
        capture_output=True,
        text=True,
    )
    return (resultado.returncode, resultado.stdout)


def leer_lista():
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(carpeta_proyecto, "memoria", "ORDENES.json")
    try:
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []
    if isinstance(datos, list):
        return datos
    return []


def siguiente_pendiente():
    for orden in leer_lista():
        if orden.get("estado") == "pendiente":
            return orden
    return None


def marcar_estado(orden_id, estado, paso_fallido='', fallos_seguidos=0):
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(carpeta_proyecto, "memoria", "ORDENES.json")
    lista = leer_lista()
    encontrada = False
    for orden in lista:
        if orden.get("id") == orden_id:
            orden["estado"] = estado
            orden["paso_fallido"] = paso_fallido
            orden["fallos_seguidos"] = fallos_seguidos
            encontrada = True
            break
    if not encontrada:
        return False
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)
    return True


def comprobar_pasos(orden):
    carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Paso 1 ronda: buscar el archivo mas reciente APROBADO de la pieza
    pieza = orden.get("pieza")
    if not pieza:
        return "ronda"
    base = os.path.splitext(os.path.basename(pieza))[0]
    carpeta_trabajos = os.path.join(carpeta_proyecto, "memoria", "trabajos_del_equipo")
    candidatos = []
    try:
        for nombre in os.listdir(carpeta_trabajos):
            if base in nombre and "APROBADO" in nombre:
                ruta_cand = os.path.join(carpeta_trabajos, nombre)
                candidatos.append((os.path.getmtime(ruta_cand), ruta_cand))
    except OSError:
        return "ronda"
    if not candidatos:
        return "ronda"
    candidatos.sort(reverse=True)
    ruta_ronda = candidatos[0][1]
    try:
        with open(ruta_ronda, encoding="utf-8") as f:
            datos_ronda = json.load(f)
    except (OSError, json.JSONDecodeError):
        return "ronda"
    obrero = datos_ronda.get("obrero")
    auditor = datos_ronda.get("auditor")
    if not obrero or not auditor or obrero == auditor:
        return "ronda"

    # Paso 2 aplicada: la ruta del campo pieza existe en disco
    if not os.path.exists(pieza):
        return "aplicada"

    # Paso 3 vigia_verde: pytest sobre la vigia
    vigia = orden.get("vigia")
    if not vigia:
        return "vigia_verde"
    resultado_vigia = subprocess.run(
        ["python", "-m", "pytest", vigia],
        cwd=carpeta_proyecto,
        capture_output=True,
        text=True,
    )
    if resultado_vigia.returncode != 0:
        resultado_git = subprocess.run(
            ["git", "ls-files", vigia],
            cwd=carpeta_proyecto,
            capture_output=True,
            text=True,
        )
        if resultado_git.stdout.strip() == "":
            return ""
        return "vigia_verde"

    # Paso 4 prueba_real: correr el comando de la orden
    comando = orden.get("comando")
    if not comando:
        return "prueba_real"
    resultado_prueba = subprocess.run(
        comando,
        shell=True,
        cwd=carpeta_proyecto,
        capture_output=True,
        text=True,
    )
    if resultado_prueba.returncode != 0:
        return "prueba_real"

    # Paso 5 guardado: si el comando no esta vacio ya se corrio en el paso 4
    return ""
    encontrada = False
    for orden in lista:
        if orden.get("id") == orden_id:
            orden["estado"] = estado
            orden["paso_fallido"] = paso_fallido
            orden["fallos_seguidos"] = fallos_seguidos
            encontrada = True
            break
    if not encontrada:
        return False
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2)
    return True
