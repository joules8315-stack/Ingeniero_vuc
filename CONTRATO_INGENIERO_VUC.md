# CONTRATO — INGENIERO VUC (la constitucion de esta herramienta)
> Julio (2026-08-20): "necesito una red neuronal tipo Obsidian que solo le de lo necesario del codigo
> a la IA, para no volver a leerlo todo y no gastar token a lo pendejo". Este contrato es la ley de
> esa herramienta. Nace de `CONTRATO_MAESTRO_AHORRO.md` y `CONTRATO_AHORRO_DE_TOKENS.md` de DMM.

## LEY 0 — QUE ES Y DONDE VIVE
- El Ingeniero vive en `C:\Ingeniero_VUC`. **No pertenece a ningun proyecto.**
- Atiende a los proyectos declarados en `proyectos.config`. Para atender uno nuevo: una linea mas.
- Se enchufa a un proyecto con `python arnes/instalar.py <apodo>` y se desenchufa con `--quitar`.

## LEY 1 — NO SE LEE EL PROYECTO, SE LEE EL PAQUETE
- Todo trabajo empieza con `python ingeniero.py trabaja <proy> "<problema>"`.
- El paquete es TODO el material permitido. Lo que falte se PIDE con `NECESITO_LEER`.
- **Candado:** `arnes/read_gate.py` (hook PreToolUse). Bloquea abrir entero cualquier archivo de mas
  de 300 lineas que el paquete no declare. La documentacion oficial es clara: el CLAUDE.md es
  contexto, **el hook es lo que obliga**.
- **Vigia:** `vigias/test_vigia_paquete_no_lee_repo_entero.py` (tope 400 lineas, ahorro minimo 90%).

## LEY 2 — LAS 4 CAPAS DEL CEREBRO (ninguna se elimina)
| Capa | Pieza | Que aporta |
|---|---|---|
| 1 FLUJOS | `cerebro/flujos.py` | junta por ASUNTO lo que el texto no enlaza |
| 2 PIEZAS | `cerebro/piezas.py` | la ficha de cada archivo (que es, que boca tiene) |
| 3 TROZOS | `cerebro/trozos.py` | el pedazo exacto `archivo:desde-hasta` (el "chunk") |
| + HILOS | `cerebro/enlaces.py` | quien toca a quien, CON FUERZA |
| = GRAFO | `cerebro/grafo.py` | las junta y se acuerda (cache por huella) |
| = BOCA | `cerebro/router.py` | entrega el paquete minimo |
- Regla dura: **ninguna capa se elimina** sin actualizar este contrato y su vigia.

## LEY 3 — NUNCA ASUMIR, NUNCA INVENTAR
- Lo que el contrato no decide: `PREGUNTA_REQUERIDA:` y se le pregunta a Julio. No se adivina.
- Lo que no existe en disco: `NO_ENCONTRADO`. Jamas se rellena con algo verosimil.
- **Vigia:** `vigias/test_vigia_no_inventa.py` (todo lo que el paquete nombra debe existir; las
  lineas de los trozos deben caber en el archivo real).

## LEY 4 — NO REPARAR ALGO Y DANAR LO OTRO
- Todo paquete lleva la seccion "A QUIEN PUEDE DANAR" (los vecinos del grafo por IMPORTA/VIGILA).
- Antes de sellar se declara cual de esos vecinos se reviso.
- **Vigia:** `vigias/test_vigia_cross_flow.py`.

## LEY 5 — VIGIA VERDE NO ES PRUEBA
- La prueba es que **Julio lo vea funcionar con sus ojos**. `ESTADO.json` guarda `prueba_humana`
  y solo Julio la pone en HECHA. Ninguna IA la marca por su cuenta.
- **Meta-prueba (leccion de DMM LEY 5):** al tocar un candado hay que **sabotearlo a proposito** y
  comprobar que la vigia se pone ROJA. Un candado fantasma es peor que ninguno.

## LEY 6 — NO REPETIDERA
- Antes de crear una pieza se busca en `mapa/MAPA_INGENIERO.json` si ya existe.
- Antecedente real: `C:\vigias` tenia 52 vigias duplicadas; se comprobo una por una, se rescataron
  las 2 pruebas unicas a `memoria/rescate/` y el resto se desecho el 2026-08-20.
- **Vigia:** `vigias/test_vigia_no_repetidera.py`.

## LEY 7 — QUE JULIO NO REPITA
- El estado NO vive en el chat: vive en `memoria/ESTADO.json`. `python ingeniero.py arranca` dice
  donde ibamos y cual es el siguiente paso, aunque se cierre la sesion o se acabe el saldo.
- A Julio se le habla simple, sin jerga, y el comando siempre listo para PowerShell (`;`, no `&&`).

## ESTADO HONESTO (2026-08-20)
- Hecho y probado: mapa, las 4 capas, router, candado de lectura, instalador, ESTADO, 7 vigias.
- Probado contra si mismo y contra DMM/Foto Informe: ahorro 99.0% y 99.4%.
- **Falta la prueba de Julio.** Hasta que el lo vea, esto NO esta certificado.

---

# AMPLIACION (Julio, 2026-08-20, segunda tanda de ordenes)

## LEY 8 — NADIE SE AUTOVALIDA (vigia cruzada)
- El que REPARA no escribe la prueba. Otro cerebro escribe la vigia **a ciegas**, sin ver la
  reparacion, y un tercero juzga si la reparacion pasa esa vigia.
- Motivo: si el mismo repara y prueba, escribe la prueba que su reparacion pasa. Verde de mentira.
- **Pieza:** `cuerpo/cruzado.py`. **Vigia:** el propio ciclo deja constancia de quien hizo que.
- El juez pregunta siempre: ¿invento algo? ¿pasa la vigia de verdad? ¿ataca la CAUSA RAIZ o tapa
  el sintoma? Si rechaza, se reintenta con lo aprendido, hasta 3 rondas.

## LEY 9 — NADA LENTO
- Ningun proceso hace esperar a Julio. Topes: **120s por llamada**, **300s el ciclo entero**.
- Medido el 2026-08-20 con un paquete de 388 lineas:
  `qwen3.6-27b` >300s TIMEOUT · `llama-3.3-70b-versatile` 30s · `gemini-2.0-flash` 40s.
- **Pieza:** `arnes/velocidad.config`. **Vigia:** `test_vigia_nada_lento.py`, que se pone ROJA si
  alguien vuelve a poner un modelo de los lentos.
- Lo que no depende uno de otro va EN PARALELO (reparador y vigilante a la vez).

## LEY 10 — EL RELEVO DE CEREBROS (critico)
- Orden textual de Julio: "gaste los token gratis de Qwen y despues los de gemini, cuando se
  repongan los de Qwen continue con el".
- Lo critico no es cambiar de cerebro: es **VOLVER** al primero cuando repone.
- **Pieza:** `cuerpo/cuotas.py`. **Vigia:** `test_vigia_relevo_cuotas.py`.
- "Lento" NO es lo mismo que "agotado": tardar una vez no manda a nadie a dormir una hora.
- En el trabajo cruzado los cerebros SE REPARTEN: si compiten por el mismo, se bloquean entre si.

## LEY 11 — MEMORIA DE FALLOS
- Todo fallo real se apunta con: que paso · causa raiz · como se curo · **QUE NO VOLVER A HACER**.
- Antes de reparar, el paquete avisa si ya se tropezo con esa piedra.
- **Pieza:** `cuerpo/fallos.py` -> `memoria/FALLOS.json`. No se borra nada: lo viejo sigue enseñando.

## LEY 12 — NADA SE DA POR HECHO SIN MIRAR EL DISCO
- Cada orden de Julio vive en `ORDENES.md`, textual, con su comprobacion.
- `verificar.py` la comprueba una por una contra el disco. Nadie puede decir "ya esta" sin prueba.
- Lo que solo Julio puede dar por bueno sale marcado `[JULIO]` y **ninguna IA lo marca jamas**.
- **Comando:** `python ingeniero.py verificar`

## LEY 13 — EL VOLUMEN NO ENTRA EN LA VENTANA DE CLAUDE
- El trabajo pesado corre en proceso APARTE (`cuerpo/subagentes.py`): se traga las 20.000 letras
  del paquete y devuelve ~600 de veredicto. Claude decide igual de bien viendo el 3%.
- Si el proceso aparte se cuelga, NO se lleva por delante la sesion de Julio.
