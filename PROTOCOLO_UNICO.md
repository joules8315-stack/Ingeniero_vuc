# PROTOCOLO ÚNICO — LA FORMA DE TRABAJO (Julio, 2026-08-20)

> "Busca en DMM el método de trabajo completo... ahora lo del protocolo del MVP, compáralos y
>  haz uno solo unificado, mapa de la forma de trabajo, legislala y pon los candados, de manera
>  que en tu vida los vuelvas a violar."

**Este documento manda sobre cualquier otra instrucción.** Une los protocolos que Julio ya
tenía escritos y que se estaban incumpliendo por separado:

| De dónde sale | Qué aporta |
|---|---|
| `PROTOCOLO_DEL_CHAT.md` (Asesor Marketing, 2026-07-28) | **cómo se responde** |
| `PROTOCOLO_MVP.md` (= "protocolo rv3:", 22 secciones) | **cómo se repara** |
| `CLAUDE.md` § "protocolo rv2:" (Foto Informe) | **hacia dónde va todo: la consolidación** |
| `CLAUDE.md` § punto de retomada | **dónde íbamos** (se lee siempre primero) |

**RV1 no existe escrito.** Se buscó en todos los documentos del MVP el 2026-08-20 y no aparece:
las rondas escritas son la 2 y la 3. Si Julio se refería a algo anterior, hay que preguntárselo;
no se inventa.

Cada ley de aquí lleva **su candado**. Una ley sin candado es un deseo, no una ley: quedó
demostrado el 2026-08-20, cuando ambos protocolos estaban escritos y se violaron los dos.

---

## LOS 8 PASOS, EN ESTE ORDEN. NO SE SALTA NINGUNO.

### PASO 1 — ¿ESTOY DONDE DEBO?
Ruta canónica y rama canónica del proyecto. Si hay copias del proyecto por el disco, se
comprueba que la declarada es la buena.
- **Candado:** `arnes/via_canonica.py` — bloquea cualquier comando si esto falla.

### PASO 2 — BUSCAR, EN ESTE ORDEN Y SOLO AQUÍ
No se explora a ciegas. Se lee **lo necesario**, en este orden:
1. El **punto de retomada** del proyecto (dónde íbamos)
2. El **contrato del flujo** afectado
3. Los **objetivos** y el contrato principal
4. La **tabla de la verdad** y los **duplicados**
5. El **histórico de fallos** (¿ya nos pasó?)
6. El **archivo:línea exacto** que señale el rastro

**Tope: 2 lecturas fuera de esa lista. A la tercera, detenerse y preguntar.**
- **Candado:** `arnes/read_gate.py` — no deja abrir un archivo grande que no esté en el paquete.
- **Herramienta:** `python ingeniero.py trabaja <proyecto> "<problema>"` arma el paquete solo.

### PASO 3 — DIAGNÓSTICO: CAUSA RAÍZ, NUNCA SÍNTOMA
- Se repara **a quien viola el contrato**, no a quien sufre la violación. Tapar aguas abajo lo
  que otro rompió aguas arriba: **PROHIBIDO**.
- Una causa declarada exige: **archivo, función, línea, flujo reproducido y evidencia**.
- **Sin eso es INFERIDO. Y lo inferido NO SE REPARA.**
- **Candado:** `arnes/candado_diagnostico.py` — no deja tocar código sin causa raíz declarada.

### PASO 4 — AGOTAR LAS FUENTES ANTES DE PREGUNTAR
Julio **no debe repetir lo que ya está escrito**. Antes de preguntarle cualquier cosa es
obligatorio haber revisado sus fuentes. Si la respuesta ya está: **no se pregunta**, se aplica
citando `archivo:línea`.
Solo se pregunta si NO está o si las fuentes **se contradicen** — y la pregunta debe decir qué
dice cada fuente revisada, o "no aparece en ninguna".
- **Candado:** `arnes/candado_preguntar.py` — bloquea la pregunta si la respuesta ya estaba escrita.
- **Y toda respuesta de Julio se escribe de vuelta en la fuente que faltaba.**

### PASO 5 — CONFIRMAR EL OBJETIVO ANTES DE CONSTRUIR
Se le repite a Julio **con palabras propias el RESULTADO que él quiere** y se espera su "sí".
Prohibido el camino fácil cuando pide otra cosa. **Objetivo (resultado), no pasos.**
- **Candado:** `arnes/candado_protocolo.py construir` — no deja crear nada nuevo sin ese "sí".

### PASO 6 — PLAN CERRADO Y REPARACIÓN MÍNIMA
Antes de editar se declara: qué falla, archivos y funciones exactas, **a quién puede dañar**,
qué pruebas se van a correr y cuándo se da por cerrado.
Bloque mínimo: **un fallo, máximo dos funciones**. Si necesita más: detenerse y preguntar.
- **Candado:** `arnes/edit_gate_universal.py` — no deja tocar código sin el paquete del asunto.

### PASO 7 — LA PRUEBA LA MANDA LA REALIDAD, NO LA PRUEBA VERDE
- Una prueba automática verde **NO certifica nada**.
- **El juez es el navegador**: se abre y se comprueba de verdad.
- **Y el juez final es Julio.** Solo él da algo por bueno.
- Toda reparación lleva **su prueba nueva**, y esa prueba la escribe **otro**, no el que reparó.
- **Candado:** `arnes/candado_cierre.py` — no deja terminar con pruebas rojas ni con preguntas
  sin hacer. Y `cuerpo/cruzado.py` — el que repara nunca escribe su propia prueba.

### PASO 8 — LEGISLAR, SELLAR Y APRENDER
- Cada instrucción de Julio **se legisla**: contrato + prueba + aplicar.
- Se sella en la rama canónica. **No se sella con una prueba roja.**
- Todo fallo entra en el histórico **en la misma corrida**, con su "no volver a hacer".
- **Candado:** `sellar.sh` — rechaza sellar si algo está rojo o si la rama no es la canónica.

---

## LAS LEYES DURAS (por encima de los pasos)

### LEY A — HABLARLE SIMPLE A JULIO
Julio **no es técnico** y lo ha repetido muchas veces, con enojo. PROHIBIDO usar jerga con él:
nada de nombres de archivos, ni palabras de informática. Se le explica **como a un amigo dueño
de un negocio**: en palabras del día a día y con el resultado que él va a ver.
- **Candado:** `arnes/candado_protocolo.py salida` — no deja terminar una respuesta con jerga.

### LEY B — NUNCA ASUMIR
Lo que no esté escrito **se busca**; si no está, se pregunta. Nunca se rellena con algo que
suene bien. Si no existe: **NO_ENCONTRADO**. Si falta una decisión: **PREGUNTA_REQUERIDA**.
- **Candado:** las pruebas de "no inventa" + el juez que separa "responde" de "se parece".

### LEY C — QUE JULIO NO REPITA
Si Julio tiene que repetir algo, **el sistema falló**, no él. No basta con hacerlo esa vez: hay
que mirar **por qué se ignoró la primera** y arreglar eso.
- **Candado:** `arnes/candado_protocolo.py prompt` — detecta solo que está repitiendo y avisa
  en el momento.

### LEY D — NO ROMPER LO DE AL LADO
Antes de tocar se mira a quién puede dañar. Después se comprueba que no se rompió.
- **Candado:** la sección "a quién puede dañar" del paquete + las pruebas de alrededor.

### LEY E — NO DUPLICAR
Antes de crear, se busca si ya existe. Al cambiar algo, lo viejo **se migra o se borra**, nunca
queda suelto. Y **siempre se pregunta antes de borrar** algo histórico.
- **Candado:** `test_vigia_no_repetidera.py` + el buscador de habilidades.

### LEY F — EL VOLUMEN LO HACEN LOS AYUDANTES GRATIS
Los ayudantes gratis hacen el trabajo pesado; aquí solo se dirige y se leen los veredictos.
Nunca se lee el proyecto entero: se pide el paquete.
- **Candado:** `arnes/read_gate.py` + el reparto de ayudantes por turnos.

---

## EL NORTE (de "protocolo rv2:") — MANDA SOBRE TODO LO DEMÁS

**El fin de todo el trabajo es la CONSOLIDACIÓN: dejar UNA SOLA VERSIÓN de cada cosa.**
Se descompone en flujos, se hace la tabla de la verdad de cada pieza duplicada, se elige la
correcta contra los objetivos y contratos, y el resto se elimina o se neutraliza. Es el único
método que permite reparar sin romper otra cosa: **primero coherencia, después tocar**.

### N1 — Una reparación que no consolida, o que rompe otro flujo, SE RECHAZA
Aunque funcione. Aunque las pruebas queden verdes.

### N2 — DECISIÓN POR PIEZA: una y solo una
Ante algo duplicado se decide **exactamente una**: **CONSERVAR · FUSIONAR · ELIMINAR ·
CONGELAR** (neutralizar la copia sin borrarla). Dejarlo "para después" no es una opción: así
es como se acumulan las copias que luego confunden.
- **Candado:** `arnes/via_canonica.py` avisa de las copias del proyecto; el buscador avisa de
  las piezas repetidas.

### N3 — UNA SOLA FUENTE DE VERDAD, declarada
Se dice en cada trabajo cuál es la fuente que manda. Las copias, cachés y vistas previas son
**espejo, nunca autoridad**. Prohibidas las llamadas en paralelo que compitan entre sí.

### N4 — CERO PÉRDIDA DE TRABAJO
Se confirma **dónde quedó guardado** cada cosa (archivo y rama). Nada fuera de la vía canónica;
si algo quedó fuera, **eso ya es un fallo que se reporta**.

### N5 — NO SE ASUME NADA, NUNCA
Textual del protocolo: *"No asumas fallo, causa, archivo, función, prueba, permiso, alcance ni
solución."* **Lo que el usuario no dijo se convierte en búsqueda obligatoria, no en suposición.**
Se busca, se mide, se confirma, se planea y se prueba. **No se repara por creencia.**

---

## CÓMO SE HACE UNA PRUEBA QUE VALGA (método ya validado en el MVP)

1. **Antes de escribir una prueba, comprobar si ya existe** — buscando por lo que hace, **nunca
   por un número de línea copiado de un documento viejo**. Los documentos envejecen; el código no
   miente.
2. **Toda prueba se comprueba metiéndole el fallo a propósito** y viendo que se pone roja, ANTES
   de darla por buena. Una prueba que nace verde no ha probado nada.
3. **Si la prueba solo mira el texto del código y no lo ejecuta de verdad, hay que decirlo.**
   Prohibido hacer creer que cubre lo que el usuario ve en pantalla cuando no lo cubre.
4. **Cada reparación deja su prueba en el proyecto** y esa prueba comprueba además que **no se
   rompieron los flujos vecinos**.

---

## LAS TRAMPAS QUE YA INVALIDARON TRABAJO (no repetirlas)

1. **Dar por bueno algo porque la prueba está verde.** La prueba puede estar mirando a otro lado.
2. **Reparar el síntoma** en vez de a quien viola el contrato.
3. **Que el que repara escriba su propia prueba.** Escribe la que su reparación pasa.
4. **Proponer una solución antes de localizar el fallo.** (2026-08-20: se iba a indexar el MVP
   sin saber dónde estaba lento.)
5. **Juntar dos problemas porque una solución toque a los dos.** (2026-08-20: lentitud y modo
   sin internet no son el mismo problema.)
6. **Preguntarle a Julio algo que él ya escribió.** (2026-08-20: pasó tres veces en un día.)
7. **Dejar una ley escrita sin candado que la haga cumplir.** Es la causa de todas las demás.

---

## CÓMO SE COMPRUEBA QUE ESTO SE CUMPLE

```
cd C:\Ingeniero_VUC; python ingeniero.py protocolo
```
Dice, paso por paso, cuál tiene candado puesto y cuál no. **Un paso sin candado es un paso que
se va a saltar** — no es una opinión, es lo que pasó el 2026-08-20 con los dos protocolos
escritos y delante.
