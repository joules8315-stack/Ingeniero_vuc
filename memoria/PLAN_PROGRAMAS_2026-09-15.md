# PLAN 2026-09-15 — LOS PROGRAMAS HACEN EL TRABAJO, LAS IA SOLO LO QUE EXIGE PENSAR

Orden de Julio (2026-09-15): prioridad 1 = reemplazar por programas lo que hoy hacen las IA (lista del 14-sep).
Claude se ausenta ~3 dias: todo debe quedar funcionando sin el. Nada de esto afloja un candado.

## PAPELES (fijos)
| Quien | Hace | No hace |
|---|---|---|
| **DeepSeek** | Escribe TODO el codigo (`--escribe deepseek`) | No revisa lo suyo |
| **Big Pickle** | Revisa: corre las vigias y da veredicto (en cuanto exista su puerta, punto 0) | No escribe codigo |
| **Copilot** | Dirige la fila: lanza las rondas en orden, hace las pruebas reales con el DMM, mide e informa | No escribe codigo |
| **Claude** | Arquitecto: lee los informes del canal y vigila que se cumpla el plan. Gasto minimo | No escribe codigo ni lanza rondas |
| **Programas** | Todo lo mecanico (lista de abajo) | — |

Revisor del programa, en este orden y sin esperar: 1 pasada por una gratis despierta -> si todas duermen, Big Pickle
(punto 0) -> si no, Claude por linea de comandos. Nunca revisa quien escribio.

## METODO (sin excepcion)
Paquete -> vigia que nace roja por la razon correcta -> DeepSeek repara -> revisa otro -> verde -> prueba real -> guardado.
Una sola fila (nadie lanza si hay ronda de menos de 10 min). Si una ronda cae, se relanza; no se para ni se pregunta.

## LA LISTA, EN ORDEN (estado a 2026-09-15 08:10)
### 0. Que el trabajo no espere a nadie (lo que frena todo)
- [en curso] `auditar`: una sola pasada por las gratis y luego Claude (vigia puesta).
- [falta] Puerta de Big Pickle como revisor (igual que la de Claude: `opencode run`), solo si todas las gratis duermen.
- [falta] Terminar el programita de recados de Big Pickle (marca `prt_`, no marcar leido antes de entregar). 2 vigias rojas.
- [falta] Varios cambios en una ronda enchufado al comando equipo y al formato del obrero (la funcion ya existe).
### 1. El capataz (programa que garantiza que se cumpla)
- [a medias] Lista de ordenes, siguiente pendiente, lanzar, marcar estado, comprobar pasos. FALTA: vigia, prueba real.
- [falta] Solo el capataz marca HECHO: vigia roja -> aprobada por 2 distintos -> aplicada -> verde -> prueba real -> guardada.
- [falta] Vigilante de caidas: detecta por huella en los registros, aplica la cura conocida, abre orden si es nueva.
- [falta] Informe de cada hora (Windows lo corre solo): hecho de verdad, rondas caidas y motivo, HORA EN CERO.
- [falta] **Medir a cada IA, tambien a Copilot**: rondas que dirige o escribe, cuantas llegan guardadas, tiempo por pieza.
### 2. El revisor por programa (lo mecanico que hoy opina una IA)
- [hecho] Caza pruebas con simuladores.
- [falta] Caza imports o definiciones repetidas (1c).
- [falta] Caza cambios en archivos que el encargo no nombra (1d).
- [falta] Corre la vigia de verdad: nace roja por la razon correcta y luego verde (1e).
- [falta] Revisa el arreglo completo, no pedazo por pedazo; arreglar sus frenos falsos medidos (texto de antes vacio; "desaparece lo que ya estaba" sin salida).
### 3. Plantillas (la IA solo llena los casos)
- [falta] Esqueleto de vigia y esqueleto de ley generados por programa.
### 4. Candados que deciden por palabras pasan a comprobar
- [falta] Aviso de memoria (92% de frenos inutiles): las lecciones van en el paquete; solo frena lo comprobable.
- [falta] Detector de fotocopia por palabras.
- [falta] Lenguaje tecnico: saber a quien se habla (a Julio simple; entre IA exacto).
- [falta] Textos del sistema tomados como ordenes de Julio y "Julio repite" (registros limpios) + bucle de guardado.
### 5. Programas de apoyo
- [falta] Decidir que equipo toca (programa / gratis / 3 IA).
- [falta] Buscar si algo ya existe y si Julio ya lo decidio antes de preguntar.
- [falta] Plan y "donde ibamos" al dia solos.

## PRUEBA REAL DE TODO
Construir el DMM (tarea pendiente: las 5 pantallas que se quedan colgadas) con esto funcionando, y medir contra el 14-sep:
rondas, sin revisar, aprobadas que llegan guardadas, minutos por pieza. Copilot lo informa por el canal a Claude.
