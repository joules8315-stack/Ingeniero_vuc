@echo off
REM ============================================================================
REM  BUCLE  -  todos los pasos del plan, de corrido, sin parar.
REM
REM  Julio lo pidio asi el 2026-09-30: "necesito que haga todo, en loop, todos
REM  los pasos del plan". Antes se le daba un paso por vez y eso no servia.
REM
REM  QUE HACE: lanza la ronda de equipo de CADA paso del plan, tres intentos por
REM  paso. Si un paso no entra en tres intentos, lo deja y PASA AL SIGUIENTE: no
REM  se queda parado esperando a nadie. Nada se pierde: cada intento queda
REM  archivado con su motivo en memoria\trabajos_del_equipo.
REM
REM  El plan esta en PLAN_DOS_PASOS.md. Los encargos en memoria\encargos.
REM
REM  CUANTO TARDA: cada intento son unos minutos. El bucle entero puede llevar
REM  una hora o mas. No hay que hacer nada mientras: al final sale el parte.
REM
REM  Se usa asi, en su terminal:
REM      cd C:\Ingeniero_VUC
REM      .\BUCLE
REM
REM  LO QUE ESTE BUCLE TODAVIA NO HACE SOLO, y hay que decirlo: no lee el motivo
REM  del rechazo para pegarlo dentro del encargo. Eso es justo lo que construye
REM  el paso 1b del plan, y por eso el paso 1b va primero en la lista. Mientras
REM  no exista, los reintentos son a ciegas.
REM ============================================================================

cd /d "C:\Ingeniero_VUC"

echo.
echo ############################################################
echo #  BUCLE DEL PLAN  -  todos los pasos, tres intentos cada uno
echo ############################################################

call :UN_PASO "memoria\encargos\paso_1a_vigia_libreta.txt"         "PASO 1a - la prueba de la libreta de frenos"
call :UN_PASO "memoria\encargos\paso_1b_vigia_devolver_la_causa.txt" "PASO 1b - la prueba de devolver la causa"

echo.
echo ############################################################
echo #  PARTE FINAL
echo ############################################################
echo.
echo Mira arriba el veredicto de cada paso. Donde diga APROBADO Y
echo APLICADO, esa prueba ya esta escrita y nace roja, que es lo
echo correcto: la pieza que la pone verde va en la ronda siguiente.
echo.
echo Donde diga RECHAZADO, nada se perdio: el intento quedo guardado
echo con su motivo en memoria\trabajos_del_equipo.
echo.
echo PRUEBA HUMANA: PENDIENTE. Prueba verde NO es prueba: la prueba
echo es que Julio lo vea funcionar con sus ojos.
echo.
goto :FIN


:UN_PASO
REM  %~1 = el archivo del encargo     %~2 = como se llama en palabras
echo.
echo ============================================================
echo   %~2
echo ============================================================
echo.
echo   --- intento 1 de 3 ---
python ingeniero.py equipo ingeniero --crear --encargo-archivo "%~1"
echo.
echo   --- intento 2 de 3 ---
python ingeniero.py equipo ingeniero --crear --encargo-archivo "%~1"
echo.
echo   --- intento 3 de 3 ---
python ingeniero.py equipo ingeniero --crear --encargo-archivo "%~1"
echo.
echo   Fin de %~2. Se pasa al siguiente.
goto :EOF


:FIN
