@echo off
REM ============================================================================
REM  BUCLE  -  los pasos del plan, de corrido. UN intento por paso.
REM
REM  CORREGIDO el 2026-09-30 de noche, cazado por Julio: la version anterior
REM  reintentaba TRES VECES EL MISMO ENCARGO. Eso va contra su propio metodo:
REM
REM    Regla 2 - un camino que ya fallo NO se vuelve a intentar.
REM    Regla 3 - el avance se mide en hechos nuevos, no en intentos. Un intento
REM              que falla sin dejar un hecho nuevo es morderse la cola: se para.
REM    Regla 5 - si varios caminos distintos fallan sobre el mismo problema, lo
REM              que esta mal es la CAUSA, no el arreglo: se vuelve a medir.
REM
REM  Reintentar el mismo texto tres veces no deja ningun hecho nuevo. Era
REM  morderse la cola, escrito en un archivo. Por eso ahora va UN solo intento
REM  por paso: si un paso no entra, se para ahi y se mira el motivo, que es
REM  justamente el hecho nuevo con el que se arma el camino siguiente.
REM
REM  OJO, APUNTADO Y NO REPARADO: si el auditor contesta roto, la ronda se da
REM  por perdida aunque el obrero haya trabajado bien. Eso ya se cazo y esta
REM  apuntado: hay que reintentar AL AUDITOR dentro de la ronda. Mientras no se
REM  repare, un RECHAZADO con veredicto raro puede no ser culpa del obrero.
REM
REM  El plan esta en PLAN_DOS_PASOS.md. Los encargos en memoria\encargos.
REM
REM  Se usa asi, en su terminal:
REM      cd C:\Ingeniero_VUC
REM      .\BUCLE
REM ============================================================================

cd /d "C:\Ingeniero_VUC"

echo.
echo ############################################################
echo #  BUCLE DEL PLAN  -  un intento por paso, sin reintentos ciegos
echo ############################################################

call :UN_PASO "memoria\encargos\paso_1a_vigia_libreta.txt"                "PASO 1a - la prueba de la libreta de frenos"
call :UN_PASO "memoria\encargos\paso_0a_vigia_del_bucle_que_aprende.txt"  "PASO 0a - la prueba del bucle que aprende del rechazo"
call :UN_PASO "memoria\encargos\paso_1b_vigia_devolver_la_causa.txt"      "PASO 1b - la prueba de devolver la causa al que escribe"

echo.
echo ############################################################
echo #  PARTE FINAL
echo ############################################################
echo.
echo Donde diga APROBADO Y APLICADO, esa prueba ya esta escrita y
echo nace roja, que es lo correcto: la pieza que la pone verde va en
echo la ronda siguiente.
echo.
echo Donde diga RECHAZADO, NO se reintenta el mismo camino. El motivo
echo que aparece arriba es el hecho nuevo: con el se arma otro camino.
echo Cada intento quedo guardado en memoria\trabajos_del_equipo.
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
python ingeniero.py equipo ingeniero --crear --encargo-archivo "%~1"
echo.
echo   Fin de %~2.
goto :EOF


:FIN
