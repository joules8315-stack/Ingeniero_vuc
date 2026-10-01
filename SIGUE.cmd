@echo off
REM ============================================================================
REM  SIGUE  -  terminar lo que quedo a medias HOY, antes de empezar nada nuevo.
REM
REM  El proyecto es 'ingeniero', la herramienta, tal como figura en la libreta de
REM  direcciones proyectos.config. No es ninguna aplicacion de Julio.
REM
REM  Julio lo pidio el 2026-09-30 de noche, despues de cazar que se le hablaba de
REM  empezar de cero sin contarle el avance que ya habia: entre las 10:08 y las
REM  18:52 el equipo cerro 26 reparaciones, con 42 pruebas verdes de 45.
REM
REM  Lo que quedo a medias son TRES pruebas rojas del candado que frena cuando
REM  una pieza nueva nace sin que nadie la llame. Esas tres son lo que hoy frena
REM  el cierre en cada vuelta.
REM
REM  QUE HACE: una sola ronda de equipo, con la causa YA MEDIDA escrita dentro
REM  del encargo. No es un reintento a ciegas: una de las tres lleva la causa
REM  exacta comprobada en el codigo, y de las otras dos lleva la evidencia
REM  literal de la prueba, sin inventarles causa.
REM
REM  POR QUE UN SOLO INTENTO: el metodo de Julio del 2026-09-29, regla 2, un
REM  camino que ya fallo no se vuelve a intentar; y regla 3, un intento que falla
REM  sin dejar un hecho nuevo es morderse la cola.
REM
REM  Se usa asi, en su terminal:
REM      cd C:\Ingeniero_VUC
REM      .\SIGUE
REM ============================================================================

cd /d "C:\Ingeniero_VUC"

echo.
echo ############################################################
echo #  ANTES: como estan las tres pruebas ahora mismo
echo ############################################################
echo.
python -m pytest -q --tb=no vigias/test_vigia_una_pieza_nueva_nace_enganchada.py

echo.
echo ############################################################
echo #  LA RONDA: terminar las tres rojas de hoy
echo ############################################################
echo.
python ingeniero.py equipo ingeniero --encargo-archivo "memoria\encargos\paso_hoy_las_tres_rojas_de_huerfanas.txt"

echo.
echo ############################################################
echo #  DESPUES: como quedaron las tres pruebas
echo ############################################################
echo.
python -m pytest -q --tb=no vigias/test_vigia_una_pieza_nueva_nace_enganchada.py

echo.
echo ############################################################
echo #  Y QUE NO SE ROMPIERON LAS VECINAS
echo ############################################################
echo.
python -m pytest -q --tb=no vigias/test_vigia_solo_frena_la_huerfana_recien_nacida.py vigias/test_vigia_la_huerfana_se_empareja_con_su_fecha.py

echo.
echo ############################################################
echo #  PARTE
echo ############################################################
echo.
echo Compara el ANTES y el DESPUES de arriba. Si el DESPUES dice
echo 6 passed, las tres rojas de hoy quedaron cerradas.
echo.
echo Si sigue habiendo rojas, NO se reintenta lo mismo: el motivo que
echo salio en la ronda es el hecho nuevo con el que se arma el camino
echo siguiente.
echo.
echo PRUEBA HUMANA: PENDIENTE. Prueba verde NO es prueba: la prueba es
echo que Julio lo vea funcionar con sus ojos.
echo.
