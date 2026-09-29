"""arnes/metodo.py

El metodo de Julio, obligado por un programa y no por la memoria de la IA.

Una sola funcion publica: revisar(encargo, raiz).

Recibe el texto del encargo y la carpeta del proyecto. Devuelve una LISTA de
frases cortas con lo que le FALTA al encargo. Lista VACIA quiere decir que esta
completo y se puede lanzar.

Cada frase dice QUE falta Y COMO escribirlo, en palabras simples, y tiene mas
de quince letras. Nunca revienta: si le llega algo vacio, None, o que no es
texto, devuelve la lista de las siete.

Los siete rotulos que se exigen, exactamente estos:

  1. PROBLEMA:      el problema con las palabras de quien lo reporto
  2. EVIDENCIA:     que se midio, con que, y que contesto
  3. CAMINO:        que se comprobo que no repite un camino que ya fallo
  4. PUEDE DANAR:   a quien puede danar y el flujo
  5. VIGIA:         la prueba declarada, y la promesa de sabotaje
  6. NO SE TOCA:    lo que se queda igual
  7. MANO:          quien es la mano mas barata que puede hacerlo

Se compara sin distinguir mayusculas de minusculas y sin tildes. Un rotulo
cuenta como puesto solo si detras de los dos puntos hay al menos tres letras
que no sean espacios: un rotulo vacio es como si no estuviera.

El parametro raiz se recibe y se guarda para lo que viene despues (consultar
los caminos que ya fallaron), pero en esta ronda NO se usa para nada mas. No
se lee ningun archivo todavia.
"""

import unicodedata


# Los siete rotulos, en el orden en que se exigen. Cada uno con su frase de
# freno: dice QUE falta y COMO escribirlo, para que quien lea pueda arreglarlo
# sin preguntar a nadie.
ROTULOS = (
    (
        "PROBLEMA",
        "Falta el PROBLEMA con las palabras de quien lo reporto. Escribe un "
        "renglon que empiece por PROBLEMA: y cuenta el fallo tal como lo dijo "
        "la persona que lo sufrio, sin traducirlo a tecnicismos.",
    ),
    (
        "EVIDENCIA",
        "Falta la EVIDENCIA medida. Escribe un renglon que empiece por "
        "EVIDENCIA: y di que mediste, con que comando, y que contesto.",
    ),
    (
        "CAMINO",
        "Falta el CAMINO ya probado. Escribe un renglon que empiece por "
        "CAMINO: y di que comprobaste que este arreglo no repite un camino "
        "que ya fallo antes.",
    ),
    (
        "PUEDE DANAR",
        "Falta a quien PUEDE DANAR. Escribe un renglon que empiece por "
        "PUEDE DANAR: y di a quien le puede hacer dano y por que flujo del "
        "programa pasa ese dano.",
    ),
    (
        "VIGIA",
        "Falta la VIGIA declarada. Escribe un renglon que empiece por VIGIA: "
        "y di que prueba lo vigila y promete que la vas a sabotear para ver "
        "que se pone roja.",
    ),
    (
        "NO SE TOCA",
        "Falta lo que NO SE TOCA. Escribe un renglon que empiece por NO SE "
        "TOCA: y di que partes del programa se quedan igual y no se van a "
        "cambiar en esta ronda.",
    ),
    (
        "MANO",
        "Falta la MANO mas barata. Escribe un renglon que empiece por MANO: "
        "y di quien es la mano mas barata que puede hacer este trabajo, sin "
        "gastar de mas.",
    ),
)


# Minimo de letras no-espacio que tiene que haber detras de los dos puntos
# para que un rotulo cuente como puesto.
MINIMO_DETRAS = 3


def _sin_tildes(texto):
    """Devuelve el texto en minusculas y sin tildes, para comparar rotulos.

    Se separa cada caracter en su forma base y se tiran los acentos. Asi
    'EVIDENCIA', 'evidencia' y 'Evidéncia' se comparan igual.
    """
    if not isinstance(texto, str):
        return ""
    descompuesto = unicodedata.normalize("NFD", texto)
    limpio = "".join(
        c for c in descompuesto if not unicodedata.combining(c)
    )
    return limpio.lower()


def _rotulo_puesto(texto_plano, rotulo):
    """Dice si el rotulo aparece con al menos tres letras detras de los dos puntos.

    texto_plano ya viene sin tildes y en minusculas. Se busca el rotulo seguido
    de ':' y se cuentan las letras no-espacio que hay detras, hasta el final de
    la linea (o del texto). Si hay menos de MINIMO_DETRAS, el rotulo esta vacio
    y cuenta como si no estuviera.
    """
    aguja = _sin_tildes(rotulo) + ":"
    inicio = 0
    while True:
        pos = texto_plano.find(aguja, inicio)
        if pos == -1:
            return False
        detras = texto_plano[pos + len(aguja):]
        # Solo cuenta lo que va en la misma linea que el rotulo.
        fin_linea = detras.find("\n")
        if fin_linea != -1:
            detras = detras[:fin_linea]
        letras = [c for c in detras if not c.isspace()]
        if len(letras) >= MINIMO_DETRAS:
            return True
        inicio = pos + len(aguja)


def revisar(encargo, raiz):
    """Devuelve la lista de frases con lo que le FALTA al encargo.

    Lista vacia quiere decir que el encargo esta completo y se puede lanzar.
    Nunca revienta: si encargo es None, vacio o no es texto, devuelve la lista
    de las siete frases.

    El parametro raiz se recibe y se guarda para lo que viene despues
    (consultar los caminos que ya fallaron), pero en esta ronda no se usa para
    nada mas. No se lee ningun archivo todavia.
    """
    # raiz se recibe y se guarda para lo que viene despues. Aqui no se usa.
    _ = raiz

    if not isinstance(encargo, str) or not encargo.strip():
        return [frase for _rotulo, frase in ROTULOS]

    texto_plano = _sin_tildes(encargo)

    falta = []
    for rotulo, frase in ROTULOS:
        if not _rotulo_puesto(texto_plano, rotulo):
            falta.append(frase)
    return falta
