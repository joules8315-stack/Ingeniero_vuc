@echo off
REM ============================================================================
REM  REPARA  -  el comando de una palabra que Julio pidio el 2026-09-30.
REM
REM  CORREGIDO esa misma noche: la primera version solo PREPARABA el material y
REM  no reparaba nada. Julio lo corrio y se quedo en el paquete. Ahora SI repara:
REM  lanza las rondas de equipo del plan, en orden, una tras otra.
REM
REM  El proyecto es 'ingeniero', la herramienta, tal como figura en la libreta de
REM  direcciones proyectos.config. No es ninguna aplicacion de Julio.
REM
REM  El plan esta en PLAN_DOS_PASOS.md, en esta misma carpeta.
REM  Los encargos de cada ronda estan en memoria\encargos.
REM
REM  Se usa asi, en su terminal:
REM      cd C:\Ingeniero_VUC
REM      .\REPARA
REM
REM  Cada ronda tarda unos minutos. No hay que hacer nada mientras: al final de
REM  cada una se ve el veredicto del equipo.
REM ============================================================================

cd /d "C:\Ingeniero_VUC"

echo.
echo ============================================================
echo   PASO 1a  -  LA VIGIA DE LA LIBRETA DE FRENOS, nace ROJA
echo ============================================================
echo.
python ingeniero.py equipo ingeniero --crear --encargo-archivo "memoria\encargos\paso_1a_vigia_libreta.txt"

echo.
echo ============================================================
echo   FIN DE LA PRIMERA RONDA
echo ============================================================
echo.
echo Si arriba dice APROBADO Y APLICADO, la vigia ya esta escrita y
echo nace roja, que es lo correcto. La pieza que vigila va en la
echo ronda siguiente.
echo.
echo Si dice RECHAZADO o SIN VEREDICTO, no se perdio nada: el trabajo
echo quedo archivado y hay que mirar el motivo que aparece arriba.
echo.
