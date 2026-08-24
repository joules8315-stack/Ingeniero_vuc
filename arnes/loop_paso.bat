@echo off
rem LOOP AUTOMATICO (Ingeniero VUC, 2026-08-24). La tarea de Windows lo llama cada minuto.
rem Si no hay encargo, no hace nada (casi gratis). Si hay, procesa una ronda con el equipo
rem y le responde al otro por el canal. Tiene tope de vueltas y se frena con `loop.py parar`.
"C:\Users\USER\AppData\Local\Programs\Python\Python310\python.exe" "C:\Ingeniero_VUC\arnes\loop.py" paso
