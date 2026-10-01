import importlib.util
import os
import sys
import tempfile
import shutil


# Esta vigia nace ROJA a proposito: la pieza arnes/libreta_de_frenos.py todavia no existe.
# Cuando se escriba con el contrato cerrado (apuntar y leer), los cuatro casos pasan a verde
# SIN TOCAR este archivo.


def _ruta_de_la_libreta():
    # Se arma la ruta partiendo de la carpeta de ESTA prueba, nunca por nombre de paquete:
    # hay dos proyectos con carpetas que se llaman igual y se agarraria la equivocada.
    aqui = os.path.dirname(os.path.abspath(__file__))
    raiz = os.path.dirname(aqui)
    return os.path.join(raiz, "arnes", "libreta_de_frenos.py")


def _cargar_libreta():
    # Carga la pieza por RUTA. Si no existe, revienta con un mensaje en palabras simples.
    ruta = _ruta_de_la_libreta()
    if not os.path.isfile(ruta):
        raise AssertionError(
            "la libreta de frenos no existe todavia en: " + ruta
            + " -- esta vigia nace ROJA a proposito"
        )
    spec = importlib.util.spec_from_file_location("libreta_de_frenos_bajo_prueba", ruta)
    if spec is None or spec.loader is None:
        raise AssertionError("no se pudo cargar la libreta de frenos desde: " + ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _carpeta_de_prueba():
    # La prueba SIEMPRE usa su propia carpeta. Nunca la memoria de verdad del proyecto.
    return tempfile.mkdtemp(prefix="libreta_de_frenos_prueba_")


def caso_1_la_libreta_existe_y_tiene_sus_dos_funciones():
    # Vigila: que la libreta exista y traiga apuntar y leer, y que se puedan llamar.
    libreta = _cargar_libreta()
    assert hasattr(libreta, "apuntar"), "la libreta no tiene la funcion apuntar"
    assert hasattr(libreta, "leer"), "la libreta no tiene la funcion leer"
    assert callable(libreta.apuntar), "apuntar no se puede llamar"
    assert callable(libreta.leer), "leer no se puede llamar"


def caso_2_un_freno_apuntado_deja_los_tres_datos_escritos():
    # Vigila: que un freno apuntado deje cuando, quien_freno e instruccion, y mudo falso.
    libreta = _cargar_libreta()
    carpeta = _carpeta_de_prueba()
    try:
        libreta.apuntar("candado_de_prueba", "hacer tal cosa", carpeta=carpeta)
        renglones = libreta.leer(carpeta=carpeta)
        assert isinstance(renglones, list), "leer no devolvio una lista"
        assert len(renglones) == 1, "se esperaba un solo renglon apuntado"
        renglon = renglones[0]
        assert isinstance(renglon, dict), "el renglon no es un diccionario"
        assert renglon.get("cuando"), "el renglon no trae cuando escrito"
        assert renglon.get("quien_freno") == "candado_de_prueba", "quien_freno no coincide"
        assert renglon.get("instruccion") == "hacer tal cosa", "instruccion no coincide"
        assert renglon.get("mudo") is False, "un freno con los tres datos no puede ser mudo"
    finally:
        shutil.rmtree(carpeta, ignore_errors=True)


def caso_3_un_freno_sin_los_tres_datos_sale_marcado_como_mudo():
    # Vigila: que falte quien_freno o falte instruccion marque mudo verdadero, y que al leer
    # se distinga cual fue mudo y cual no.
    libreta = _cargar_libreta()
    carpeta = _carpeta_de_prueba()
    try:
        libreta.apuntar("", "hacer tal cosa", carpeta=carpeta)
        libreta.apuntar("candado_de_prueba", "", carpeta=carpeta)
        renglones = libreta.leer(carpeta=carpeta)
        assert isinstance(renglones, list), "leer no devolvio una lista"
        assert len(renglones) == 2, "se esperaban dos renglones apuntados"
        primero, segundo = renglones[0], renglones[1]
        assert primero.get("mudo") is True, "el freno sin quien_freno debe salir mudo"
        assert segundo.get("mudo") is True, "el freno sin instruccion debe salir mudo"
        assert primero.get("quien_freno") == "", "el mudo por quien_freno debe traerlo vacio"
        assert primero.get("instruccion") == "hacer tal cosa", "el primero si traia instruccion"
        assert segundo.get("quien_freno") == "candado_de_prueba", "el segundo si traia quien_freno"
        assert segundo.get("instruccion") == "", "el mudo por instruccion debe traerla vacia"
    finally:
        shutil.rmtree(carpeta, ignore_errors=True)


def caso_4_la_libreta_no_escribe_en_la_memoria_de_verdad():
    # Vigila: que al pasarle la carpeta de la prueba, el archivo quede en ESA carpeta y no en
    # la carpeta memoria del proyecto. Esto ya costo caro dos veces.
    libreta = _cargar_libreta()
    carpeta = _carpeta_de_prueba()
    try:
        libreta.apuntar("candado_de_prueba", "hacer tal cosa", carpeta=carpeta)
        dentro = os.listdir(carpeta)
        assert dentro, "no quedo ningun archivo en la carpeta de la prueba"
        # La carpeta memoria del proyecto NO debe haber recibido nada de esta prueba.
        aqui = os.path.dirname(os.path.abspath(__file__))
        raiz = os.path.dirname(aqui)
        memoria = os.path.join(raiz, "memoria")
        if os.path.isdir(memoria):
            for nombre in os.listdir(memoria):
                ruta_memoria = os.path.join(memoria, nombre)
                if not os.path.isfile(ruta_memoria):
                    continue
                try:
                    with open(ruta_memoria, "r", encoding="utf-8", errors="ignore") as f:
                        contenido = f.read()
                except OSError:
                    continue
                assert "candado_de_prueba" not in contenido, (
                    "la prueba escribio en la memoria de verdad: " + ruta_memoria
                )
    finally:
        shutil.rmtree(carpeta, ignore_errors=True)


def main():
    casos = [
        ("CASO 1: la libreta existe y tiene sus dos funciones",
         caso_1_la_libreta_existe_y_tiene_sus_dos_funciones),
        ("CASO 2: un freno apuntado deja los tres datos escritos",
         caso_2_un_freno_apuntado_deja_los_tres_datos_escritos),
        ("CASO 3: un freno sin los tres datos sale marcado como mudo",
         caso_3_un_freno_sin_los_tres_datos_sale_marcado_como_mudo),
        ("CASO 4: la libreta no escribe en la memoria de verdad",
         caso_4_la_libreta_no_escribe_en_la_memoria_de_verdad),
    ]
    fallos = 0
    for nombre, funcion in casos:
        try:
            funcion()
            print("VERDE  " + nombre)
        except AssertionError as error:
            fallos += 1
            print("ROJO   " + nombre + " -> " + str(error))
        except Exception as error:
            fallos += 1
            print("ROJO   " + nombre + " -> " + type(error).__name__ + ": " + str(error))
    if fallos:
        print("")
        print("La libreta de frenos todavia no existe o no cumple el contrato.")
        print("Esta vigia nace ROJA a proposito: " + str(fallos) + " de " + str(len(casos)) + " casos fallan.")
        sys.exit(1)
    print("")
    print("Los " + str(len(casos)) + " casos pasan: la libreta de frenos cumple el contrato.")


if __name__ == "__main__":
    main()
