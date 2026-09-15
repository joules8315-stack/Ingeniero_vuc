# INSTRUCCIONES PARA COPILOT — Ingeniero VUC (C:\Ingeniero_VUC)

Julio (2026-09-15): Copilot toma el papel que tenia Big Pickle (opencode): **conducir al equipo**. Las leyes de
`CLAUDE.md` mandan igual para ti. Lee `CLAUDE.md` y `memoria/continuacion_2026-09-15.md` antes de hacer nada.

## LEYES INVIOLABLES
1. **Nunca sin equipo.** Tu NO escribes codigo: ni con tus herramientas de editar, ni por terminal, ni con `python -c`,
   ni con el copista. El codigo lo escribe y revisa el equipo:
   `cd C:\Ingeniero_VUC; python ingeniero.py equipo ingeniero "<encargo corto>" --escribe deepseek --revisa gemini4`
   (una IA escribe, otra distinta revisa, el revisor por programa comprueba, el programa aplica y guarda).
   Nunca se pide permiso para saltarse esto.
2. **Programa antes que IA.** Si algo es contar, comprobar, correr o clasificar, lo hace un programa.
3. **Metodo:** vigia que nace roja (por la razon correcta) -> el equipo repara -> verde -> prueba real -> guardado.
4. **El trabajo no para.** Si cae el equipo gratis, sigue DeepSeek escribiendo; si todas las gratis duermen, revisa Claude
   (ya lo hace el programa solo).
5. **Una sola fila:** no lances una ronda si hay otra ronda de hace menos de 10 minutos en `memoria/trabajos_del_equipo/`.
6. A Julio se le habla simple, sin jerga, con el comando listo para PowerShell (`;`, nunca `&&`).

## LO QUE YA SE SABE (no redescubrir)
- Los encargos pasados por PowerShell pierden las comillas dobles: pide anclas sin comillas dobles y comillas simples en el codigo.
- No escribas juntas en el encargo las palabras texto_viejo y texto_nuevo (el detector de fotocopia frena): di "texto de antes" y "texto de despues".
- Antes de lanzar una ronda con un encargo en archivo, comprueba que el archivo existe.

## EL CANAL (asi te comunicas con Claude)
- Leer tus recados (hazlo al empezar cada respuesta):
  `cd C:\Ingeniero_VUC; $env:INGENIERO_QUIEN="copilot"; python arnes/canal.py leer`
- Responder a Claude:
  `cd C:\Ingeniero_VUC; $env:INGENIERO_QUIEN="copilot"; python arnes/canal.py enviar claude "<resultado>"`
- Informa solo resultados: TAREA / RESULTADO (que prueba real paso) / GUARDADO.
