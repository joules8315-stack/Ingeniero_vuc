# -*- coding: utf-8 -*-
"""Renueva el permiso de una hora de las pruebas reales de Foto Informe.

Julio lo pidio a mano el 2026-08-24. Su opcion C sigue en pie: el sistema NO renueva solo,
lo manda Julio. No se guarda nada nuevo de larga vida, no se muestra la clave ni el permiso,
y solo se toca la variable del permiso, que caduca en una hora.

Todo lo que puede fallar va envuelto: a Julio no le llega nunca un error crudo, le llega una
frase que dice que paso y que hacer.
"""
import json
import urllib.request
import winreg

MVP = "http://127.0.0.1:8000"


def leer(nombre):
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment")
        v, _ = winreg.QueryValueEx(k, nombre)
        return str(v or "")
    except Exception:
        return ""


def guardar(nombre, valor):
    k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(k, nombre, 0, winreg.REG_SZ, valor)
    winreg.CloseKey(k)


def main():
    correo, clave = leer("FOTO_INFORME_TEST_EMAIL"), leer("FOTO_INFORME_TEST_PASSWORD")
    if not correo or not clave:
        print("No estan guardados el correo y la clave, asi que no puedo renovar por mi cuenta.")
        print("Julio: corre en tu ventana el bloque que te pide la clave, y avisame.")
        return 1

    cuerpo = json.dumps({"email": correo, "password": clave}).encode("utf-8")
    pet = urllib.request.Request(MVP + "/login", data=cuerpo,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(pet) as r:
            resp = json.loads(r.read())
    except Exception as e:
        print("No se pudo pedir el permiso: " + str(e)[:120])
        print("Comprueba que el programa este encendido y vuelve a intentarlo.")
        return 1

    token = str(resp.get("access_token") or "")
    if not token:
        print("El programa no devolvio permiso. No se toco nada.")
        return 1

    guardar("FOTO_INFORME_TEST_BEARER", token)

    # No basta con guardarlo: se comprueba que de verdad abre la puerta.
    try:
        prueba = urllib.request.Request(MVP + "/reports",
                                        headers={"Authorization": "Bearer " + token})
        with urllib.request.urlopen(prueba) as r:
            sirve = (r.status == 200)
    except Exception:
        sirve = False

    if not sirve:
        print("Se guardo el permiso pero NO abre la puerta. Mejor renovalo tu a mano.")
        return 1

    print("PERMISO RENOVADO Y COMPROBADO. Dura una hora. No se guardo nada mas.")
    print("Aviso: tu clave sigue guardada en el equipo. Eso es justo lo que tu opcion C")
    print("queria evitar; cuando terminemos hoy conviene borrarla.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
