#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""arnes/llamar.py — EL LLAMADO: que la otra IA 'sienta' que le escribieron.

`python arnes/llamar.py <para> "<asunto>"`

Deja una MARCA visible (memoria/canal/llamados/<para>.txt) y dispara un AVISO de Windows
(toast) para que el llamado se note. Asi, cada vez que alguien deja una instruccion en el
canal, la IA destinataria 'siente el llamado' en cuanto su sesion haga cualquier cosa.

Si el toast no puede salir (PowerShell bloqueado, etc.), queda la marca: el aviso no debe
poder tumbar el canal entero, asi que todo es a prueba de fallos (best effort).
"""
import os, sys, subprocess, time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LLAMADOS = os.path.join(AQUI, "memoria", "canal", "llamados")


def marcar(para, asunto):
    os.makedirs(LLAMADOS, exist_ok=True)
    marca = os.path.join(LLAMADOS, para + ".txt")
    try:
        with open(marca, "w", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M") + " | " + asunto)
    except Exception:
        pass
    return marca


def _toast(para, asunto):
    """Aviso visual en Windows. APAGADO por Julio (2026-08-26): el popup de PowerShell salia una y
    otra vez y molestaba. La MARCA (memoria/canal/llamados/<para>.txt) sigue siendo lo que la IA
    lee, asi que el llamado no se pierde. Para volver a encender el popup: INGENIERO_LLAMAR_TOAST=1.
    """
    if os.environ.get("INGENIERO_LLAMAR_TOAST", "").strip() != "1":
        return
    titulo = "CANAL: llamado para " + para
    texto = (asunto or "")[:120].replace("'", "")
    ps = ("Add-Type -AssemblyName System.Windows.Forms;"
          "Add-Type -AssemblyName System.Drawing;"
          "$n=New-Object System.Windows.Forms.NotifyIcon;"
          "$n.Icon=[System.Drawing.SystemIcons]::Information;"
          "$n.Visible=$true;"
          "$n.BalloonTipTitle='" + titulo + "';"
          "$n.BalloonTipText='" + texto + "';"
          "$n.ShowBalloonTip(6000);"
          "Start-Sleep -Seconds 6;$n.Dispose()")
    try:
        flags = 0x08000000 if os.name == "nt" else 0   # CREATE_NO_WINDOW: no abrir consola al notificar
        subprocess.Popen(["powershell", "-NoProfile", "-Command", ps],
                         creationflags=flags, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    except Exception:
        pass


def llamar(para, asunto):
    marca = marcar(para, asunto)
    _toast(para, asunto)
    return marca


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        print("LLAMADO a '" + sys.argv[1] + "': " + llamar(sys.argv[1], " ".join(sys.argv[2:])))
    else:
        print(__doc__)
