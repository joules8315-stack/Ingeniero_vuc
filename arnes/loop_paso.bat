@echo off
rem LOOP AUTOMATICO (Ingeniero VUC, 2026-08-24). La tarea de Windows lo llama cada minuto.
rem Si no hay encargo, no hace nada (casi gratis). Si hay, procesa una ronda con el equipo
rem y le responde al otro por el canal. Tiene tope de vueltas y se frena con `loop.py parar`.
rem 2026-08-25: se lanza con powershell -WindowStyle Hidden para que NO salga la ventana de
rem consola que abria y cerraba cada minuto (ventana parpadeando).
powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "& 'C:\Users\USER\AppData\Local\Programs\Python\Python310\python.exe' 'C:\Ingeniero_VUC\arnes\loop.py' paso"

