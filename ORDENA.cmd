@echo off
REM ============================================================================
REM  ORDENA  -  manda la orden de reparacion a la otra IA, 2026-09-30.
REM
REM  Hace dos cosas de una sola vez:
REM    1) SUBE el plan y todo lo guardado, porque la otra IA lee lo subido,
REM       no el disco de Julio. Si no se sube, no lo ve.
REM    2) DEJA LA ORDEN en el canal, con las cinco respuestas de la ley de
REM       Julio: que, como, donde, por que y cuando.
REM
REM  Se usa asi, en su terminal:
REM      cd C:\Ingeniero_VUC
REM      .\ORDENA
REM ============================================================================

cd /d "C:\Ingeniero_VUC"

echo.
echo ===== 1 de 2: SUBIENDO, para que la otra IA pueda verlo =====
git push origin main
echo.
echo Si ahi arriba pidio usuario y clave y no entro, avisale a Julio:
echo la otra IA NO va a ver el plan hasta que esto suba.
echo.

echo ===== 2 de 2: DEJANDO LA ORDEN EN EL CANAL =====
python arnes/canal.py enviar opencode "ORDEN DE REPARACION, de Julio por medio de Claude, 2026-09-30. Empieza ya y no esperes respuesta de nadie. DONDE ESTA LA CARPETA: C:\Ingeniero_VUC, en la rama main. Es el proyecto 'ingeniero', la herramienta, no una aplicacion de Julio. Si lees desde fuera, el mismo contenido esta subido en el repositorio. QUE CONTIENE Y QUE LEER PRIMERO: en la raiz hay un documento llamado PLAN_DOS_PASOS.md. Ese documento MANDA: trae los dos pasos, los numeros medidos y un capitulo de lo que el plan NO arregla. No se improvisa nada que no este ahi. Las leyes de la casa estan en CLAUDE.md, tambien en la raiz. Las piezas estan en arnes (los candados), cuerpo (los obreros), cerebro (el reparto de material) y vigias (las pruebas). La memoria y los registros estan en memoria. QUE HAY QUE REPARAR, en orden: PASO 1, la via del diagnostico, va PRIMERO. 1a, crear arnes/libreta_de_frenos.py: cada freno anota por programa tres datos, cuando freno, el nombre exacto del que freno y la instruccion que fallo con su texto; un freno que no deja esos tres datos es un FRENO MUDO. 1b, crear arnes/lo_que_hay_que_corregir.py: al que escribe se le devuelven los fallos concretos del intento anterior en un bloque SEPARADO del encargo, que se REEMPLAZA en cada intento y no se acumula. 1c, poner verdes las seis pruebas rojas de quien fallo, en vigias/test_vigia_el_metodo_manda_en_la_puerta.py y vigias/test_vigia_fallos_de_verdad_avisan.py. PASO 2, el paquete completo pero pequeno, va DESPUES. 2a, el tope del pasillo usa hoy la capacidad del cerebro mas pequeno y tiene que usar la del que de verdad va a escribir; su prueba ya existe y esta roja, es vigias/test_vigia_el_pasillo_no_corta_al_que_escribe.py. 2b, que el recorte no parta una pieza por la mitad. 2c, quitar el solape duplicado del paquete. 2d, el dato pegado que se confunde con una pieza: la ley ya esta escrita con cinco casos en vigias/test_vigia_el_codigo_pegado_no_pide_funciones.py y dos siguen rojos desde el 2026-09-29; la regla es que una palabra conocida cuenta como pieza SOLO si el texto la nombra como pieza, detras de def o detras de la palabra funcion, y las que empiezan por raya baja siguen contando como hasta hoy. COMO SE REPARA: nunca a solas, cada arreglo por ronda de equipo, uno escribe y otro revisa, con el comando python ingeniero.py equipo ingeniero y el encargo en un archivo si es largo. La vigia va PRIMERO y nace ROJA por su propio motivo; el arreglo va en la ronda siguiente. Nada nace huerfano: una pieza nueva deja puesto quien la llama en su MISMA ronda. Si el material no trae la pieza, se pega el trozo literal DENTRO del encargo. El ancla de un cambio es UN SOLO renglon, exacto, que aparezca UNA sola vez en el archivo. Todas las rondas con el de pago: son centavos y el gratis quemo 25,9 horas fallando 4 de cada 10 veces. POR QUE SE REPARA ESTO Y NO OTRA COSA: hay 2.824 frenos apuntados y solo 5 acabaron sabiendo quien fallo. El sistema tuvo 2.824 oportunidades de aprender y aprovecho cinco. Por eso los mismos tres problemas vuelven cada semana con otra cara y Julio lleva meses sin avanzar. Ademas el pasillo recorta cada encargo casi a la mitad, de 26.838 letras a 14.843, para que le quepa a un ayudante gratis: eso causo 3 de los 4 rechazos de hoy. CUANDO: ahora, sin esperar a nadie. Si algo te frena, apunta el texto exacto del freno y pasa al punto siguiente de la lista; cuando acabes, vuelve al primero que dejaste frenado. Se avisa cuando CADA paso queda verde, no al final; si un paso se tranca dos veces seguidas, se avisa en el momento con la causa medida: archivo, funcion, renglon y evidencia. NO SE EMPIEZA LA MULTITAREA hasta que los dos pasos esten verdes y Julio lo haya visto con sus ojos. DOS AVISOS MEDIDOS QUE TE VAN A MORDER: uno, los doce candados estan escritos con la direccion de Windows y no funcionan si trabajas desde la nube; no es tu culpa cuando falle. Dos, el registro de legislacion parte un mensaje pegado en tantas ordenes como renglones tenga, asi que no pegues informes largos en el chat de Julio."

echo.
echo ===== LISTO =====
echo La orden quedo en el canal con las cinco respuestas: que, como, donde, por que y cuando.
echo.
