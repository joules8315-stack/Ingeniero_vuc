import os
import subprocess
from datetime import datetime, date

def _leer_proyectos_config():
    ruta_config = os.path.join(os.path.dirname(__file__), '..', 'proyectos.config')
    proyectos = {}
    try:
        with open(ruta_config, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith('#') or '=' not in linea:
                    continue
                apodo, ruta = linea.split('=', 1)
                proyectos[apodo.strip()] = ruta.strip()
    except FileNotFoundError:
        return {}
    return proyectos

def _git_info(ruta_proyecto):
    try:
        # último commit
        ultimo = subprocess.check_output(['git', '-C', ruta_proyecto, 'log', '-1', '--format=%ci'],
                                         stderr=subprocess.DEVNULL, text=True).strip()
        # commits de hoy
        hoy = date.today().isoformat()
        commits_hoy = subprocess.check_output(['git', '-C', ruta_proyecto, 'log', '--since=' + hoy + ' 00:00:00', '--until=' + hoy + ' 23:59:59', '--oneline'],
                                              stderr=subprocess.DEVNULL, text=True).strip().splitlines()
        return ultimo, len(commits_hoy)
    except subprocess.CalledProcessError:
        return None, 0

def _dias_sin_commit(ultimo_commit):
    if not ultimo_commit:
        return None
    try:
        fecha_commit = datetime.strptime(ultimo_commit, '%Y-%m-%d %H:%M:%S %z')
        hoy = datetime.now(fecha_commit.tzinfo)
        return (hoy - fecha_commit).days
    except ValueError:
        return None

def _hay_prueba_real():
    ruta_pruebas = os.path.join(os.path.dirname(__file__), '..', 'memoria', 'pruebas_real')
    if not os.path.isdir(ruta_pruebas):
        return False
    return any(os.path.isfile(os.path.join(ruta_pruebas, f)) for f in os.listdir(ruta_pruebas))

def medir():
    proyectos = _leer_proyectos_config()
    foto_informe = proyectos.get('foto_informe')
    ingeniero = proyectos.get('ingeniero')
    if not foto_informe or not ingeniero:
        return {'error': 'NO_ENCONTRADO: apodo faltante en proyectos.config'}
    ultimo_foto, commits_hoy_foto = _git_info(foto_informe)
    ultimo_ing, commits_hoy_ing = _git_info(ingeniero)
    dias_foto = _dias_sin_commit(ultimo_foto)
    dias_ing = _dias_sin_commit(ultimo_ing)
    return {
        'foto_informe': {'ultimo_commit': ultimo_foto, 'dias_sin_commit': dias_foto, 'commits_hoy': commits_hoy_foto},
        'ingeniero': {'ultimo_commit': ultimo_ing, 'dias_sin_commit': dias_ing, 'commits_hoy': commits_hoy_ing},
        'prueba_real': _hay_prueba_real()
    }

def informe():
    datos = medir()
    if 'error' in datos:
        print(datos['error'])
        return
    foto = datos['foto_informe']
    ing = datos['ingeniero']
    puede_trabajar = foto['dias_sin_commit'] is not None and foto['dias_sin_commit'] <= 1
    print('JULIO PUDO TRABAJAR HOY: ' + ('SI' if puede_trabajar else 'NO'))
    if not puede_trabajar:
        print('Dias parado el proyecto foto_informe: ' + str(foto['dias_sin_commit']))
        print('Movimiento de la herramienta ingeniero hoy: ' + str(ing['commits_hoy']) + ' commits')
    print('Prueba real apuntada: ' + ('SI' if datos['prueba_real'] else 'NO'))