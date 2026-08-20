---
paths:
  - "arnes/**"
---
# Reglas del ARNES (los candados)

Leccion de Foto Informe (Julio, 2026-07-23): **un recordatorio se ignora; solo un candado que FRENA se cumple.**
Y de la documentacion oficial: el CLAUDE.md es contexto, no obligacion. Lo que obliga es el hook.

- `read_gate.py` es un hook **PreToolUse**. Salida 2 = bloquea. Salida 0 = deja pasar.
- Un candado que no muerde es peor que ninguno: da falsa seguridad. Al tocarlo, **sabotealo a
  proposito** y comprueba que la vigia se pone ROJA (LEY 5 del protocolo de DMM).
- No aflojar el candado para que "no estorbe". Si estorba, se ajusta `lectura.config`, no el codigo.
- Fallo real ya corregido (2026-08-20): comprobar el nombre del archivo "de pasada" en el texto del
  paquete abria la puerta a leer 10.818 lineas. Solo vale lo DECLARADO como `### \`pieza\``.
