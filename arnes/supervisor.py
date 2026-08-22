# -*- coding: utf-8 -*-
"""arnes/supervisor.py — EL SUPERVISOR POR DEFECTO (DeepSeek), la norma inquebrantable.

Julio, 2026-08-21:
  "trabaja de la mano con deepseek, que si tu eres las manos el supervisa, y si el es las manos
   tu supervisas, eso como norma inquebrantable."
  "no es openrouter, es deepseek."

POR QUE EXISTE ESTO Y NO SE HACE CON LA FILA NORMAL: la fila de cerebros gratis se quedo sin
poder auditar. Con el encargo real (26.821 letras) los dos de Groq devuelven "demasiado grande",
el de tu PC no le cabe, y los de Gemini contestan roto. Resultado: el que propone se aprobaba
solo, que es exactamente lo que Julio prohibio. DeepSeek si traga ese tamano.

Se le habla a SU casa (api.deepseek.com), no a traves de intermediarios.
La llave va SOLA en las variables de Windows (DEEPSEEK_API_KEY). Nunca se le pide por el chat y
nunca se escribe aqui.

    python arnes/supervisor.py "<lo que hay que auditar>"

OJO: DeepSeek es de PAGO. Cada llamada gasta saldo de Julio. Por eso esto NO se llama solo en
bucle: se llama cuando hace falta un segundo par de ojos y no hay ninguno gratis que pueda.
"""
import os
import sys


def preguntar(prompt, modelo=None, temperatura=0.2, espera=300):
    """Le pregunta a DeepSeek y devuelve su respuesta tal cual. Sin red que tape errores."""
    import json
    import urllib.request

    llave = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not llave:
        raise RuntimeError("no hay llave de DeepSeek en las variables de Windows "
                           "(DEEPSEEK_API_KEY)")
    cuerpo = json.dumps({
        "model": modelo or os.environ.get("DEEPSEEK_MODELO", "deepseek-chat"),
        "temperature": temperatura,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    pet = urllib.request.Request("https://api.deepseek.com/chat/completions",
                                 data=cuerpo, method="POST")
    pet.add_header("Content-Type", "application/json")
    pet.add_header("Authorization", "Bearer " + llave)
    with urllib.request.urlopen(pet, timeout=espera) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"]


def saldo():
    """Lo que le QUEDA a Julio, preguntado a la casa de DeepSeek. No se estima: se pregunta.

    Julio, 2026-08-21: "quiero saber para cuantas tareas sirve". Inventarse el precio seria
    justo lo que esta prohibido (ley 2: nunca inventar); el saldo de verdad lo dice DeepSeek.
    """
    import json
    import urllib.request

    llave = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not llave:
        raise RuntimeError("no hay llave de DeepSeek en las variables de Windows")
    pet = urllib.request.Request("https://api.deepseek.com/user/balance")
    pet.add_header("Authorization", "Bearer " + llave)
    with urllib.request.urlopen(pet, timeout=30) as r:
        return json.load(r)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "saldo":
        try:
            d = saldo()
            for s in d.get("balance_infos", []):
                print("SALDO: %s %s (recargado %s, de regalo %s)"
                      % (s.get("total_balance"), s.get("currency"),
                         s.get("topped_up_balance"), s.get("granted_balance")))
            if not d.get("is_available", True):
                print("AVISO: la cuenta figura SIN saldo utilizable")
        except Exception as e:
            print("NO SE PUDO CONSULTAR EL SALDO: %s" % e)
            sys.exit(1)
        sys.exit(0)
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    try:
        print(preguntar(" ".join(sys.argv[1:])))
    except Exception as e:
        # El error se ve tal cual: si es de saldo o de llave, Julio tiene que enterarse.
        print("DEEPSEEK NO CONTESTO: %s" % e)
        sys.exit(1)
