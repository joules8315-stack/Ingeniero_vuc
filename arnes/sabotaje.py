# -*- coding: utf-8 -*-
"""SABOTAJE — el sabotaje de cada regla lo hace un PROGRAMA, no una mano.

Aplica una lista de sabotajes a los archivos, corre la vigia despues de cada
uno y deja SIEMPRE los archivos como estaban. Si la vigia se queda verde con
un sabotaje puesto, ese sabotaje no vale: la regla no esta guardada.
"""
import json
import os
import shutil
import subprocess
import sys


def _entorno_limpio():
    """Copia el entorno del proceso sin las variables PYTEST_ y sin bytecode."""
    entorno = {}
    for nombre, valor in os.environ.items():
        if nombre.startswith('PYTEST_'):
            continue
        entorno[nombre] = valor
    entorno['PYTHONDONTWRITEBYTECODE'] = '1'
    return entorno


def _correr_vigia(raiz, vigia):
    """Corre SOLO ese archivo de vigia. Devuelve True si paso (returncode 0)."""
    entorno = _entorno_limpio()
    resultado = subprocess.run(
        [sys.executable, '-m', 'pytest', vigia, '-q', '-p', 'no:cacheprovider'],
        cwd=raiz,
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        timeout=600,
        env=entorno,
    )
    return resultado.returncode == 0


def sabotear(raiz, vigia, sabotajes):
    """Aplica cada sabotaje, corre la vigia y restaura los archivos.

    sabotajes es una lista de dicts con 'archivo' (ruta relativa a raiz),
    'viejo' (texto exacto) y 'nuevo' (texto que lo reemplaza).
    Devuelve un dict con 'sana', 'devuelta', 'resultados' y 'ok'.
    """
    sana = _correr_vigia(raiz, vigia)

    resultados = []
    for sabotaje in sabotajes:
        archivo = sabotaje['archivo']
        viejo = sabotaje['viejo']
        nuevo = sabotaje['nuevo']
        ruta = os.path.join(raiz, archivo)
        copia = ruta + '.sabotaje_bak'
        shutil.copy2(ruta, copia)
        estado = None
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                texto = f.read()
            if viejo not in texto:
                estado = 'no_encontrado'
            else:
                texto_nuevo = texto.replace(viejo, nuevo, 1)
                with open(ruta, 'w', encoding='utf-8') as f:
                    f.write(texto_nuevo)
                # Python reusa su copia compilada si el archivo tiene la misma
                # fecha y el mismo tamano. Un sabotaje de igual largo en el
                # mismo segundo corria el codigo viejo y daba verde falso.
                m = os.path.getmtime(copia) + 10
                os.utime(ruta, (m, m))
                if _correr_vigia(raiz, vigia):
                    estado = 'verde'
                else:
                    estado = 'roja'
        finally:
            shutil.move(copia, ruta)
        resultados.append({'archivo': archivo, 'estado': estado})

    devuelta = _correr_vigia(raiz, vigia)

    ok = (
        sana
        and devuelta
        and len(resultados) > 0
        and all(r['estado'] == 'roja' for r in resultados)
    )
    return {
        'sana': sana,
        'devuelta': devuelta,
        'resultados': resultados,
        'ok': ok,
    }


def main():
    """Uso: python arnes/sabotaje.py <vigia> <archivo_json_con_la_lista>."""
    if len(sys.argv) != 3:
        print('uso: python arnes/sabotaje.py <vigia> <archivo_json_con_la_lista>')
        return 1
    vigia = sys.argv[1]
    archivo_json = sys.argv[2]
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(archivo_json, 'r', encoding='utf-8') as f:
        sabotajes = json.load(f)
    salida = sabotear(raiz, vigia, sabotajes)
    for resultado in salida['resultados']:
        print('%s: %s' % (resultado['archivo'], resultado['estado']))
    if salida['ok']:
        print('SABOTAJE OK')
        return 0
    print('SABOTAJE FALLO')
    return 1


if __name__ == '__main__':
    sys.exit(main())
