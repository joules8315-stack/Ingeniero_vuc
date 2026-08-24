# CONTRATO — LEGISLACIÓN 2026-08-24 (equipo total + prueba real antes de pedirle a Julio)

> Fecha: 2026-08-24 · Proyecto: Ingeniero VUC · Estado: LEY VIGENTE
>
> Julio, textual (2026-08-24):
> **"Revisa como se esta llevando a cabo lo de la legislación, quedo dentro del protocolo, que con
> cada instruccion que yo de, primero debe analizarla, legislar, agragarlo a tabla de la verdad,
> matriz, despues dividirla por bloques, indexarla, crearle vigias, aplicar arnes, para que lo que
> repara no destruya algo que sirva, de modo que cuando se trabaje, con el equipo, logre el
> resultado, realice, con el equipo, pruebas reales, playwright, y verifique si en realidad se
> logro el resultado, o fue una autovalidacion. 1) Si logro el resultado, que me avise para pruebas
> reales. 2) Si no se logro el resultado, que aprenda del error, y comience nuevamente el proceso,
> para reparar el fallo y lograr el resultado solicitado, sin excusas."**

Esta instrucción **es** parte de la ley, no el prólogo. Por eso va arriba y textual.

---

## 1. EL CICLO DE LEGISLACIÓN (se aplica a CADA instrucción de Julio)

Toda orden de Julio se legisla así, en este orden, y cada paso deja rastro en disco:

1. **Analizarla** — qué pide de verdad, sin asumir.
2. **Legislarla** — escribir la ley (contrato), con su candado.
3. **Agregarla a la tabla de la verdad y a la matriz** — ver `MATRIZ_LEGISLACION.md`.
4. **Dividirla en bloques** — piezas mínimas, cada una con su ley.
5. **Indexarla** — para que el sistema la encuentre por lo que hace (`cerebro/protocolo.py`).
6. **Crearle vigías** — que comprueben la ley y muerdan al sabotearla.
7. **Aplicar el arnés** — el candado que frena, no un recordatorio.
8. **Cross-flow** — que lo que repara no destruya algo que sirve (no romper vecinos).

Y el ciclo de trabajo que esa instrucción ordena:
- Trabajar **con el equipo** para lograr el resultado.
- Con el equipo, correr **pruebas reales (Playwright)**.
- **Verificar** si el resultado se logró de verdad o fue **autovalidación**.
  - **Si se logró** → avisarle a Julio para sus pruebas reales.
  - **Si NO se logró** → aprender del error y **reiniciar el ciclo** para reparar el fallo y lograr
    el resultado, sin excusas.

---

## 2. LOS BLOQUES DE ESTA INSTRUCCIÓN

### B1 — Equipo total, sin salto (aplica a TODAS las IA)
- **Ley:** el candado de equipo aplica a Claude, Cline y ChatGPT por igual. Para saltarlo se pide
  permiso y la respuesta es **SIEMPRE "denegado"**. Se trabaja siempre en equipo.
- **Candado:** `arnes/candado_equipo.py` (no ofrece salto: exige veredicto del equipo para tocar
  código) + `arnes/edit_gate_universal.py`.
- **Vigía:** `vigias/test_vigia_equipo_total.py`.

### B2 — Probar de verdad antes de pedirle a Julio
- **Ley:** antes de pedirle a Julio que pruebe con sus ojos, hay que correr, **con el equipo**, una
  **prueba real interna (Playwright)** que toca la pantalla y demuestra que el objetivo se cumple.
  Se verifica si el resultado se logró o fue autovalidación. Una autovalidación no abre la puerta.
- **B2.1** — Si se logró → avisarle a Julio para sus pruebas reales (`pedir-prueba`).
- **B2.2** — Si NO se logró → aprender del error y **reiniciar el ciclo** para reparar, sin excusas.
- **Candado:** `arnes/candado_prueba_real.py` (bloquea pedirle a Julio sin evidencia fresca, verde
  y con equipo).
- **Vigía:** `vigias/test_vigia_prueba_real.py`.

### B3 — Legislar cada instrucción así
- **Ley:** toda orden de Julio pasa por el ciclo del punto 1. Una orden no legislada es un deseo.
- **Candado:** este contrato + `vigias/test_vigia_legislacion_ciclo.py`.
- **Vigía:** `vigias/test_vigia_legislacion_ciclo.py`.

### B4 — Solo se pregunta después de haber buscado
- **Ley:** nunca se pregunta a Julio antes de buscar. Se busca primero en el repositorio, los
  objetivos, la legislación, las tablas de verdad, la matriz y la tabla de errores — todo debe
  estar **indexado**. Solo si allí no está la respuesta, se pregunta. Nunca antes.
- **Candado:** `arnes/candado_preguntar.py` (PASO 4) + LEY I del protocolo.
- **Vigía:** `vigias/test_vigia_dudas.py`.

---

## 3. LO QUE NO SE HACE

- **No se le pide a Julio que pruebe sin prueba real interna, con equipo y en verde.**
- **No se acepta una autovalidación como prueba** de que el objetivo se cumple.
- **No se salta el candado de equipo** ("denegado" es la única respuesta a un salto).
- **No se legislan dos instrucciones en un solo apunte** cuando son independientes.
- **No se relajan estas vigías para que pasen.** Si estorban, se dice; no se quitan.
