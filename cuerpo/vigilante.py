"""Vigilante de tareas que pasan su tiempo limite.

Directriz de Julio A-44 del 2026-09-21:
si una tarea pasa su tiempo limite se revisa si sigue trabajando o se dano;
si avanza se espera; si no, se detiene para buscar la causa.

Este modulo expone una sola funcion, esperar(), que aplica esa directriz
sobre un proceso ya lanzado. La funcion no decide que hacer con el
resultado: solo devuelve el motivo por el que dejo de esperar.
"""

import time


def esperar(proceso, limite, sin_avance, tope_duro, avance,
            dormir=time.sleep, reloj=time.monotonic):
    """Espera a que un proceso termine o haya que detenerlo.

    Parametros:
        proceso: objeto con .poll() y .kill() (por ejemplo subprocess.Popen).
        limite: segundos desde el arranque a partir de los cuales se empieza
            a mirar si la tarea sigue avanzando.
        sin_avance: segundos sin avance que se toleran una vez pasado el
            limite antes de darla por colgada.
        tope_duro: segundos maximos desde el arranque, se avance o no.
        avance: funcion sin argumentos que devuelve una marca de progreso
            (numero, cadena, lo que sea comparable).
        dormir: funcion para pausar entre comprobaciones (por defecto
            time.sleep).
        reloj: funcion de reloj monotono (por defecto time.monotonic).

    Devuelve:
        'termino'    si el proceso acabo por su cuenta.
        'tope_duro'  si se paso el tope duro y hubo que matarlo.
        'colgada'    si paso el limite y llevaba demasiado sin avanzar.

    Si avance() lanza una excepcion, se toma como que no hubo avance.
    """
    inicio = reloj()
    ultimo = avance()
    momento_ultimo_avance = inicio

    while True:
        if proceso.poll() is not None:
            return 'termino'

        if reloj() - inicio > tope_duro:
            proceso.kill()
            return 'tope_duro'

        try:
            ahora = avance()
        except Exception:
            ahora = ultimo

        if ahora != ultimo:
            ultimo = ahora
            momento_ultimo_avance = reloj()

        if (reloj() - inicio > limite
                and reloj() - momento_ultimo_avance > sin_avance):
            proceso.kill()
            return 'colgada'

        dormir(5)
