# Revisión conjunta Claude + Codex — la primera tarea (acuerdo A-41)

> Orden de Julio del 2026-09-21, **prioridad sobre todo lo demás**: Codex verifica el plan de trabajo
> con **toda** la información, y Codex y Claude buscan **juntos** cómo perfeccionar la herramienta.
> Codex trabaja en **solo lectura**. Esta hoja es su encargo completo.

## 1. Qué es la herramienta y qué quiere Julio

El **Ingeniero VUC** (`C:\Ingeniero_VUC`) es la herramienta de Julio para **construir y reparar
cualquier proyecto gastando lo mínimo**. Julio no es técnico. El primer proyecto que tiene que
terminar es **DMM** (asesor de marketing, `C:\Users\USER\dev\Asesor Marketing`); la única prueba que
Julio acepta es **ver DMM funcionando con sus ojos**, empezando por la entrada al sistema.

Cómo trabaja hoy: una **máquina de pits** (programa) corre una lista de tareas etiquetadas en loop;
**DeepSeek** escribe, **Big Pickle** revisa (si falla, **Codex**), un **juez de la prueba** (programa)
decide lo que se puede contar, el **guardia** no deja guardar nada roto, y Claude (o Codex si Claude
no está) solo hace de **arquitecto** una vez por proyecto y de **perito** cuando algo falla.
Método de cada tarea: la prueba **nace roja**, después la pieza, después el **sabotaje** (se rompe el
arreglo a propósito y la prueba tiene que frenar).

La idea que manda: **más programa, menos IA**. La IA solo donde haga falta juicio de significado.

## 2. Lo que tienes que leer (todo en esta carpeta; ábrelo tú, en solo lectura)

| Archivo | Por qué |
|---|---|
| `PLAN_PITS/04_PLAN_v4.md` | El plan vigente, aprobado por Julio. **No se cambia sin consultarle** |
| `PLAN_PITS/01_ACUERDOS.md` | Todo lo que Julio decidió, numerado (A-1 … A-41). Gana el más nuevo |
| `PLAN_PITS/02_FORENSE.md` | El forense del 2026-09-18, medido con programas |
| `memoria/FORENSE_BIG_PICKLE_2026-09-14.md` | El forense anterior: 7 causas, 5 parejas de leyes que se pisan |
| `PLAN_PITS/03_REVISION.md` | La revisión del plan |
| `PLAN_PITS/07_INVENTARIO_CUENTA_O_JUICIO.md` | Qué paso es cuenta (programa) y cuál juicio (IA) |
| `PLAN_PITS/08_FICHA_DEL_PIT.md` | Lo construido y **todo lo aprendido soltando la máquina sola**, con sus fallos medidos |
| `memoria/ORDENES.json` | La lista de tareas de la máquina (60), con lo que repara cada una |
| `memoria/FALLOS.json` | El libro de fallos (causa, cura, lección) |
| `CLAUDE.md` y `AGENTS.md` | Las leyes duras (las tuyas son las mismas) |
| `memoria/LEYES_DEL_AYUDANTE.md` y los `CONTRATO_*.md` (66) | Las leyes escritas. Léelas según las necesites |
| `CONTRATO_COMO_EL_INGENIERO_CONSTRUYE_UN_PROYECTO.md`, `CONTRATO_ANALISIS_DE_FONDO.md`, `CONTRATO_CUENTA_O_JUICIO.md` | El **método de operar** del Ingeniero (punto 1.6) |
| `cerebro/` (`router.py`, `trozos.py`, `grafo.py`) | El repartidor y la memoria indexada (puntos 1.0 y 1.5) |
| `cuerpo/capataz.py`, `cuerpo/obrero.py`, `cuerpo/aplicador.py` | La máquina de pits, el equipo y el aplicador |
| `arnes/` | Los candados. `arnes/candado_legislar.py` es lo más parecido al "guardador" de 1.5 |

**Prohibido abrir:** cualquier archivo `.env` (llaves), `auth.json`, y el proyecto DMM entero en
esta primera vuelta (puede traer datos de clientes). Si necesitas algo de DMM, lo pides.

## 3. Los ocho puntos que hay que responder

- **1.0 La información que les llega a las IA.** Hoy el material se corta en trozos de 40 renglones
  elegidos por parecido de palabras; medido: rondas perdidas porque llegó la portada de un archivo y
  no la función. ¿Cómo lograr que llegue **solo lo necesario, completo, sin sobras ni textos largos,
  en archivos baratos de leer**?
- **1.1 Más rápida, precisa y económica.** ¿Qué pasos que hoy hace una IA puede hacer un programa?
  ¿Dónde se pierde tiempo y dinero? (El forense y la ficha traen números medidos.)
- **1.2 Que se autorrepare**, con la misma regla: más programa, menos IA.
- **1.3 Velocidad de entrega y recepción de información entre programas.**
- **1.4 Qué más se reemplaza por programas**, en **todos** los repositorios: la herramienta y lo que
  construye.
- **1.5 El programa guardador.** Cuando Julio da, pule o cambia una directriz: guardarla en los
  archivos que corresponden, saber si **repite**, si es **nueva** o si es **parte de una directriz
  principal**, y dejarla **completa en la memoria indexada**. Y cómo hacer esa memoria más rápida y
  mejor organizada. (Hoy hay un candado que recoge las órdenes de Julio, pero recoge mucho ruido de
  máquina; está medido en la ficha.)
- **1.6 El método de operar.** Ya está definido, pero repartido en varios documentos. Resáltalo y di
  cuál es **el mejor método**: entender al usuario, encontrar la esencia y la causa raíz, asignar
  objetivos, arquitectura, mapa y plan, tomar el equipo y las herramientas adecuadas, ejecutar con
  precisión.
- **1.7 Modo ingeniero automático.** Cuando Julio ordene trabajar en cualquier repositorio, **todas
  las IA sin excepción** trabajan en modo ingeniero, siempre. ¿Qué IA hay hoy (Claude, Codex, DeepSeek,
  Big Pickle, Groq, Gemini, Cline, Copilot…), cuál ya está obligada por mecanismo y cuál no?

## 4. Cómo contestas

**Solo JSON, sin texto alrededor.** Cada hallazgo con su prueba copiada literal (archivo y el texto),
o marcado como supuesto. Nada inventado: si no lo encuentras, `NO_ENCONTRADO`.

```json
{"puntos": [
  {"punto": "1.0",
   "hallazgos": [{"que": "...", "evidencia": {"archivo": "ruta", "texto": "copiado literal"}, "medido_o_supuesto": "medido"}],
   "propuestas": [{"que": "...", "como": "...", "programa_o_ia": "PROGRAMA", "por_que": "...",
                   "ahorro": "qué se ahorra y cómo se mediría", "riesgo": "a quién puede dañar",
                   "prioridad": 1, "toca_el_plan_v4": false}]}
 ],
 "contradicciones": [{"entre": ["ruta A", "ruta B"], "cual": "..."}],
 "preguntas_para_julio": ["en palabras simples, solo lo que es decisión suya"]}
```

Una propuesta que **cambie el plan v4** lleva `"toca_el_plan_v4": true`: esas se le consultan a Julio
antes (acuerdo A-30). Todo lo demás lo hace el equipo, con prueba roja, pieza y sabotaje.
