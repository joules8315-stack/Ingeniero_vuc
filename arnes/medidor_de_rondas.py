# -*- coding: utf-8 -*-
"""Medidor de rondas del equipo.

Para que sirve: mide cuanto se pierde en cada ronda del equipo. Una ronda es
un renglon del registro memoria/TRABAJOS_DEL_EQUIPO.log. De cada ronda se
mira si salio APROBADA y si su cambio llego a guardarse en la historia de
git ese mismo dia.

La meta que puso Julio es que de cada diez rondas se guarden nueve. Esta
pieza es la que dice, dia por dia, si eso se esta cumpliendo o no.

La funcion principal es contar(raiz, dia):
    - Si no existe memoria/TRABAJOS_DEL_EQUIPO.log dentro de la raiz,
      devuelve todo en cero y NO llama a git.
    - Si existe, lo lee en utf-8 y se queda solo con los renglones que
      empiezan por el dia pedido (ano-mes-dia).
    - El veredicto de cada renglon NO se busca por texto con espacios
      fijos: se parte el renglon por la barra vertical, se le quitan los
      espacios a cada pedazo, y el renglon cuenta como aprobado si alguno
      de esos pedazos es exactamente la palabra APROBADO.
    - Los guardados se piden a git con subprocess, corriendo en la raiz,
      con log --since y --until del dia y formato de una sola linea con
      el asunto, contando cuantos asuntos empiezan por
      'EQUIPO APROBADO Y APLICADO'. Todo dentro de un try: si git no esta
      o falla, guardados queda en cero.

Devuelve un diccionario con: rondas, aprobados, guardados, la parte que
salio bien (guardados / rondas, o cero si no hubo rondas) y una entrada
'razon' con un texto en castellano sencillo que nombra el dia pedido y
dice cuantas rondas hubo, cuantas se aprobaron y cuantas se guardaron.
"""

import os
import subprocess
import sys
from datetime import date


# Ruta relativa del registro dentro de la raiz del proyecto.
RUTA_REGISTRO = os.path.join('memoria', 'TRABAJOS_DEL_EQUIPO.log')

# Prefijo exacto del asunto de un cambio guardado por el equipo.
PREFIJO_GUARDADO = 'EQUIPO APROBADO Y APLICADO'

# Palabra exacta que marca un renglon aprobado.
PALABRA_APROBADO = 'APROBADO'


def _renglones_del_dia(raiz, dia):
    """Devuelve la lista de renglones del registro que empiezan por el dia.

    Si el registro no existe, devuelve None para que quien llama sepa que
    hay que devolver todo en cero sin llamar a git.
    """
    ruta = os.path.join(raiz, RUTA_REGISTRO)
    if not os.path.isfile(ruta):
        return None
    with open(ruta, 'r', encoding='utf-8') as f:
        todos = f.readlines()
    return [linea for linea in todos if linea.startswith(dia)]


def _es_aprobado(renglon):
    """Mira si el renglon trae la palabra APROBADO como pedazo exacto.

    No se busca un texto con espacios fijos: se parte el renglon por la
    barra vertical, se le quitan los espacios a cada pedazo, y cuenta como
    aprobado si alguno de esos pedazos es exactamente 'APROBADO'.
    """
    pedazos = renglon.split('|')
    for pedazo in pedazos:
        if pedazo.strip() == PALABRA_APROBADO:
            return True
    return False


def _contar_guardados(raiz, dia):
    """Cuenta los cambios guardados en la historia de git ese dia.

    Se pide a git con subprocess, corriendo en la raiz, el comando log con
    since y until del dia y formato de una sola linea con el asunto. Se
    cuentan los asuntos que empiezan por 'EQUIPO APROBADO Y APLICADO'.
    Todo dentro de un try: si git no esta o falla, devuelve cero.
    """
    try:
        comando = [
            'git',
            'log',
            '--since=%s 00:00:00' % dia,
            '--until=%s 23:59:59' % dia,
            '--pretty=format:%s',
        ]
        resultado = subprocess.run(
            comando,
            cwd=raiz,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if resultado.returncode != 0:
            return 0
        salida = resultado.stdout.decode('utf-8', errors='replace')
        guardados = 0
        for linea in salida.splitlines():
            if linea.startswith(PREFIJO_GUARDADO):
                guardados += 1
        return guardados
    except Exception:
        return 0


def contar(raiz, dia):
    """Cuenta las rondas del equipo de un dia y cuanto se guardo.

    Recibe la carpeta raiz y un dia escrito como ano-mes-dia. Devuelve un
    diccionario con rondas, aprobados, guardados, la parte que salio bien
    y una razon en castellano sencillo.
    """
    renglones = _renglones_del_dia(raiz, dia)

    if renglones is None:
        # El registro no existe: todo en cero y sin llamar a git.
        return {
            'rondas': 0,
            'aprobados': 0,
            'guardados': 0,
            'parte_bien': 0.0,
            'razon': (
                'El dia %s no hay registro de rondas: cero rondas, '
                'cero aprobadas y cero guardadas.' % dia
            ),
        }

    rondas = len(renglones)
    aprobados = 0
    for renglon in renglones:
        if _es_aprobado(renglon):
            aprobados += 1

    guardados = _contar_guardados(raiz, dia)

    if rondas > 0:
        parte_bien = guardados / rondas
    else:
        parte_bien = 0.0

    razon = (
        'El dia %s hubo %d rondas, se aprobaron %d y se guardaron %d.'
        % (dia, rondas, aprobados, guardados)
    )

    return {
        'rondas': rondas,
        'aprobados': aprobados,
        'guardados': guardados,
        'parte_bien': parte_bien,
        'razon': razon,
    }


def main():
    """Uso: python arnes/medidor_de_rondas.py [ano-mes-dia].

    Toma el dia del primer argumento o usa el de hoy. Llama a contar con la
    carpeta que esta un nivel arriba de la del propio archivo e imprime la
    razon.
    """
    if len(sys.argv) > 1:
        dia = sys.argv[1]
    else:
        dia = date.today().isoformat()

    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    resultado = contar(raiz, dia)
    print(resultado['razon'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
