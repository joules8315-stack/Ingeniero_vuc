# -*- coding: utf-8 -*-
# juez_de_la_prueba.py
#
# PARA QUE SIRVE:
# La prueba roja antes y verde despues es la unica manera barata de saber que un cambio
# hace de verdad lo que se pidio. Eso es CUENTA, no JUICIO: se puede decidir corriendo la
# prueba tres veces (antes, despues y al deshacer), asi que NO se paga una IA para saberlo.
#
# Este juez corre la prueba con el mismo python que esta corriendo, con pytest en modo
# callado, con la raiz como carpeta de trabajo, con tope de 300 segundos, con
# PYTHONDONTWRITEBYTECODE=1 y quitando del entorno toda variable que empiece por PYTEST
# (igual que arnes/sabotaje.py), porque si no se corre pytest dentro de pytest y se cuelga.
#
# PASO 1: corre la prueba tal como esta todo ahora -> antes_roja (True si NO pasa).
# PASO 2: lee el archivo, comprueba que el texto viejo aparece, guarda copia y escribe el
#         texto viejo cambiado por el nuevo UNA sola vez.
# PASO 3: corre la prueba otra vez -> despues_verde (True si SI pasa).
# PASO 4: devuelve el archivo a su contenido original, corre la prueba una tercera vez
#         -> vuelve_roja (True si vuelve a NO pasar); despues deja el cambio nuevo puesto.
#
# ok es True solo si las tres son True. razon es un texto en castellano sencillo que dice
# que paso en cada uno de los tres momentos. Si el texto viejo no aparece, o si algo
# revienta, se devuelve todo en falso y la razon lo explica, sin lanzar ningun error.

import os
import subprocess
import sys


TOPE_SEGUNDOS = 300


def _entorno_limpio():
    """Entorno sin variables PYTEST* y sin escribir codigo compilado."""
    entorno = dict(os.environ)
    for clave in list(entorno.keys()):
        if clave.startswith('PYTEST'):
            del entorno[clave]
    entorno['PYTHONDONTWRITEBYTECODE'] = '1'
    return entorno


def _correr_prueba(raiz, ruta_prueba):
    """Corre pytest en modo callado sobre la prueba. Devuelve True si pasa."""
    orden = [
        sys.executable,
        '-m',
        'pytest',
        '-q',
        str(ruta_prueba),
    ]
    try:
        proceso = subprocess.run(
            orden,
            cwd=str(raiz),
            env=_entorno_limpio(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=TOPE_SEGUNDOS,
        )
    except subprocess.TimeoutExpired:
        return False, 'la prueba se paso del tope de %d segundos' % TOPE_SEGUNDOS
    except Exception as error:
        return False, 'no se pudo correr la prueba: %s' % error
    if proceso.returncode == 0:
        return True, 'la prueba paso'
    return False, 'la prueba no paso (codigo %s)' % proceso.returncode


def _alguna_esta_roja(raiz, rutas_pruebas):
    """Corre pytest UNA sola vez sobre todas las rutas juntas.

    Devuelve True si alguna no paso, y False si pasaron todas o si no se pudo correr.
    """
    orden = [
        sys.executable,
        '-m',
        'pytest',
        '-q',
    ]
    orden.extend(str(ruta) for ruta in rutas_pruebas)
    try:
        proceso = subprocess.run(
            orden,
            cwd=str(raiz),
            env=_entorno_limpio(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=TOPE_SEGUNDOS,
        )
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False
    return proceso.returncode != 0


def juzgar(raiz, ruta_prueba, ruta_archivo, texto_viejo, texto_nuevo, dejar_el_cambio=True):
    """Decide por programa si el cambio hace lo pedido.

    Devuelve un diccionario con antes_roja, despues_verde, vuelve_roja, ok y razon.
    Nunca lanza error: si algo revienta, todo en falso y la razon lo explica.

    Si dejar_el_cambio es falso, al terminar el archivo se queda con su contenido
    original, tal como estaba antes de todo.
    """
    resultado = {
        'antes_roja': False,
        'despues_verde': False,
        'vuelve_roja': False,
        'ok': False,
        'razon': '',
    }

    ruta_archivo = str(ruta_archivo)
    ruta_prueba = str(ruta_prueba)
    raiz = str(raiz)

    # PASO 1: la prueba tal como esta todo ahora.
    try:
        pasa_antes, detalle_antes = _correr_prueba(raiz, ruta_prueba)
    except Exception as error:
        resultado['razon'] = 'al correr la prueba antes de tocar nada, revento: %s' % error
        return resultado
    resultado['antes_roja'] = not pasa_antes

    # PASO 2: leer el archivo, comprobar el texto viejo y escribir el cambio.
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido_original = f.read()
    except Exception as error:
        resultado['razon'] = (
            'antes de tocar nada: %s. No se pudo leer el archivo que se cambia: %s'
            % (detalle_antes, error)
        )
        return resultado

    if texto_viejo not in contenido_original:
        resultado['razon'] = (
            'antes de tocar nada: %s. El texto viejo no aparece en el archivo, '
            'asi que no hay nada que cambiar.' % detalle_antes
        )
        return resultado

    contenido_nuevo = contenido_original.replace(texto_viejo, texto_nuevo, 1)
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_nuevo)
    except Exception as error:
        resultado['razon'] = (
            'antes de tocar nada: %s. No se pudo escribir el cambio en el archivo: %s'
            % (detalle_antes, error)
        )
        return resultado

    # PASO 3: la prueba otra vez, ya con el cambio puesto.
    try:
        pasa_despues, detalle_despues = _correr_prueba(raiz, ruta_prueba)
    except Exception as error:
        detalle_despues = 'revento al correr la prueba con el cambio puesto: %s' % error
        pasa_despues = False
    resultado['despues_verde'] = bool(pasa_despues)

    # PASO 4: devolver el archivo a su contenido original y correr la prueba otra vez.
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_original)
        pasa_vuelta, detalle_vuelta = _correr_prueba(raiz, ruta_prueba)
    except Exception as error:
        detalle_vuelta = 'revento al deshacer el cambio: %s' % error
        pasa_vuelta = True
    resultado['vuelve_roja'] = not pasa_vuelta

    # Dejar el archivo como pide la tarea: el cambio nuevo si dejar_el_cambio es
    # verdadero, y el contenido original si es falso.
    if dejar_el_cambio:
        contenido_a_dejar = contenido_nuevo
        que_se_queria_dejar = 'el cambio nuevo puesto'
    else:
        contenido_a_dejar = contenido_original
        que_se_queria_dejar = 'el archivo como estaba'
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_a_dejar)
    except Exception as error:
        resultado['razon'] = (
            'antes de tocar nada: %s. Despues del juicio no se pudo dejar %s: %s'
            % (detalle_antes, que_se_queria_dejar, error)
        )
        return resultado

    resultado['ok'] = bool(
        resultado['antes_roja']
        and resultado['despues_verde']
        and resultado['vuelve_roja']
    )

    resultado['razon'] = (
        'antes de tocar nada: %s. Con el cambio puesto: %s. Al deshacer el cambio: %s.'
        % (detalle_antes, detalle_despues, detalle_vuelta)
    )
    return resultado


# PARA QUE SIRVE:
# El juez encuentra solo la prueba que cubre lo que se cambio, para no tener que
# decirsela a mano. Recibe la raiz, la ruta relativa del archivo que se cambia (con
# barras normales), el texto viejo y el texto nuevo; busca las vigias que nombran ese
# archivo y devuelve un diccionario con ok, prueba y razon.
def juzgar_con_vecinas(raiz, ruta_relativa, texto_viejo, texto_nuevo, dejar_el_cambio=True):
    # dejar_el_cambio: si es falso, el archivo se queda como estaba (para cuando el juez se usa antes de aprobar el trabajo).
    """Busca sola la prueba que cubre el archivo y la juzga.

    Devuelve un diccionario con ok, prueba y razon. Nunca lanza error: si algo
    revienta, ok en None y la razon lo explica.
    """
    try:
        from pathlib import Path

        from arnes import vecinas

        raiz = str(raiz)
        ruta_relativa = str(ruta_relativa)

        ruta_archivo = str(Path(raiz) / ruta_relativa)
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido_original = f.read()
        except Exception:
            contenido_original = None

        try:
            vigias = vecinas._vigias_existentes(raiz)
            candidatas = vecinas._vecinas_por_stem([ruta_relativa], raiz, vigias)

            if not candidatas:
                return {
                    'ok': None,
                    'prueba': None,
                    'razon': (
                        'ninguna prueba nombra ese archivo, asi que no hay nada que '
                        'correr para comprobarlo'
                    ),
                }

            # No se prueban una por una todas las vecinas: cada una cuesta tres corridas
            # y un archivo con muchas vecinas tardaba tres minutos. Se mira de un vistazo
            # cuales estan rojas y solo esas se prueban.
            rutas_candidatas = [str(Path(raiz) / vigia) for vigia in candidatas]
            if not _alguna_esta_roja(raiz, rutas_candidatas):
                return {
                    'ok': None,
                    'prueba': None,
                    'razon': (
                        'ninguna de las pruebas que nombran ese archivo estaba roja, '
                        'asi que no habia nada que demostrar'
                    ),
                }

            for vigia in candidatas[:3]:
                ruta_vigia = str(Path(raiz) / vigia)
                resultado = juzgar(
                    raiz, ruta_vigia, ruta_archivo, texto_viejo, texto_nuevo,
                    dejar_el_cambio=False,
                )

                if not resultado.get('antes_roja'):
                    continue

                if resultado.get('despues_verde') and resultado.get('vuelve_roja'):
                    return {
                        'ok': True,
                        'prueba': vigia,
                        'razon': resultado.get('razon', ''),
                    }

                return {
                    'ok': False,
                    'prueba': vigia,
                    'razon': resultado.get('razon', ''),
                }

            return {
                'ok': None,
                'prueba': None,
                'razon': (
                    'ninguna de las pruebas que nombran ese archivo estaba roja, '
                    'asi que no habia nada que demostrar'
                ),
            }
        finally:
            if not dejar_el_cambio and contenido_original is not None:
                try:
                    with open(ruta_archivo, 'w', encoding='utf-8') as f:
                        f.write(contenido_original)
                except Exception:
                    pass
    except Exception as error:
        return {
            'ok': None,
            'prueba': None,
            'razon': 'al buscar la prueba que cubre el archivo, revento: %s' % error,
        }


def main():
    """Uso: python arnes/juez_de_la_prueba.py <raiz> <prueba> <archivo> <viejo> <nuevo>."""
    if len(sys.argv) != 6:
        print('uso: python arnes/juez_de_la_prueba.py <raiz> <prueba> <archivo> <viejo> <nuevo>')
        return 1
    raiz = sys.argv[1]
    ruta_prueba = sys.argv[2]
    ruta_archivo = sys.argv[3]
    texto_viejo = sys.argv[4]
    texto_nuevo = sys.argv[5]
    resultado = juzgar(raiz, ruta_prueba, ruta_archivo, texto_viejo, texto_nuevo)
    print(resultado['razon'])
    if resultado['ok']:
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
