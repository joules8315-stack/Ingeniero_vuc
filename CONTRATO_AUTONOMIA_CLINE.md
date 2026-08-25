# CONTRATO_AUTONOMIA_CLINE — Cline actúa AUTÓNOMO en el bucle, sin pedir autorización a Julio

> Fecha: 2026-08-24 · Proyecto: Ingeniero VUC (aplica a TODOS) · Estado: LEY VIGENTE

Julio, textual (2026-08-24): "tu participación debe ser en algo que no necesite mi aprobación y que
puedas comunicarte sin mí, que no dependa de mí. Porque en un loop, donde yo no esté pendiente,
pararías el proceso."

## EL FALLO QUE TAPA
En el chat, Cline (yo) le pidió a Julio **más de 10 autorizaciones** en un solo trabajo. Eso está bien
cuando Julio está delante, pero **en el bucle automático (Claude ↔ Cline ↔ DeepSeek) nadie va a estar
delante**: si para cada paso hace falta que Julio apruebe, **el proceso se detiene**. Un sistema que
depende de que Julio apruebe cada paso NO puede correr solo. Y la idea es que corra solo.

## LEY — CLINE TRABAJA SIN PEDIRLE AUTORIZACIÓN A JULIO
1. **En el bucle, Cline NO le pregunta ni le pide aprobación a Julio.** Se comunica con Claude y con
   DeepSeek por el **canal** (`arnes/canal.py`), usa el **equipo** para generar y auditar, y avanza.
2. **Julio entra SOLO al final**, para la **prueba humana con sus ojos** (ley L2 / paso H). Nunca como
   aprobador intermedio del proceso.
3. **El equipo resuelve sus dudas del código y del contexto indexado**, no le pregunta a Julio. Si al
   equipo le falta contexto, lo pide por `NECESITO_LEER` (a otra IA), no a Julio.
4. **Los candados se satisfacen con veredictos del equipo (autónomos)**, no con aprobación humana.
   Un candado que solo pueda abrirse con aprobación de Julio es un candado que **para el bucle**.
5. **Las preguntas a Julio solo se reservan para lo que SOLO Julio decide** (objetivos, gustos, "sí"
   final a lo construido). Nunca para "cómo hago esto" ni "¿lo hago o no?".

## Candado
`arnes/candado_autonomia.py` — detecta si Cline/Claude está esperando una aprobación de Julio en el
bucle y lo avisa/bloquea para que el trabajo no se detenga (o lo resuelve por el canal/equipo).

## Vigía
`vigias/test_vigia_autonomia.py` — comprueba que el flujo del bucle no depende de una aprobación de
Julio en el medio, y que las preguntas solo van a Julio al final (prueba humana).

## Consecuencia de comportamiento (para Cline)
Dejar de preguntarle a Julio cosas que puedo resolver yo (leyendo el código, usando el equipo, o
preguntándole a Claude/DeepSeek por el canal). Preguntar a Julio solo lo que es SU decisión.
