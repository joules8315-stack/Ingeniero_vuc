import contextlib

def mirando(objeto, nombre):
    """
    Es una pieza reutilizable para usar con 'with' que sirve para demostrar si una pieza fue llamada DE VERDAD, ejecutando el camino real.

    Al salir del with, lo que devuelve tiene exactamente dos cosas: la_llamaron (si o no) y veces (cuantas veces la llamaron dentro del with).
    Antes de entrar valen falso y cero.

    Tiene que valer igual para las dos formas que hay en la casa: para un metodo de un objeto (le pasas el objeto) y para una funcion suelta de un modulo (le pasas el modulo entero).

    Reglas que no se pueden romper:
    1. No puede cambiar lo que la pieza vigilada devuelve: el espia mira, no toca el resultado.
    2. No puede dejarla enganchada al terminar: al salir del with todo tiene que quedar como estaba, y una llamada de DESPUES no se puede contar.
    3. No puede tragarse ni cambiar las excepciones que salten dentro del with.
    4. No implementes la clase del objeto (Python no admite tocar clases de C): para el modulo y para el objeto de la casa vale con cambiar el atributo por uno envuelto, guardando el de antes para devolverlo al salir.
    """

    class Espia:
        def __init__(self, objeto, nombre):
            self.objeto = objeto
            self.nombre = nombre
            self.la_llamaron = False
            self.veces = 0
            self._original = None
            self._es_modulo = hasattr(objeto, '__dict__') and not hasattr(objeto, '__class__') # Heurística para detectar módulo

        def __enter__(self):
            self.la_llamaron = False
            self.veces = 0

            if self._es_modulo:
                # Si es un módulo, buscamos la función directamente en su diccionario
                if hasattr(self.objeto, self.nombre):
                    self._original = getattr(self.objeto, self.nombre)
                    setattr(self.objeto, self.nombre, self._envuelto)
                else:
                    # Si la función no existe en el módulo, no podemos espiarla
                    pass
            else:
                # Si es un objeto, buscamos el método
                if hasattr(self.objeto, self.nombre):
                    self._original = getattr(self.objeto, self.nombre)
                    setattr(self.objeto, self.nombre, self._envuelto)
                else:
                    # Si el método no existe en el objeto, no podemos espiarlo
                    pass
            return self

        def _envuelto(self, *args, **kwargs):
            self.la_llamaron = True
            self.veces += 1
            # Llamamos a la función original y devolvemos su resultado
            if self._original:
                return self._original(*args, **kwargs)
            else:
                # Si _original es None, significa que la pieza no existía al entrar
                # Esto podría ser un caso a manejar, pero por ahora devolvemos None
                # o lanzamos una excepción si se considera un error.
                # Para este caso, asumimos que si no existía, no se puede llamar.
                pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            # Restauramos el atributo original
            if self._es_modulo:
                if self._original is not None:
                    setattr(self.objeto, self.nombre, self._original)
            else:
                if self._original is not None:
                    setattr(self.objeto, self.nombre, self._original)

            # No suprimir excepciones
            return False

    return Espia(objeto, nombre)
