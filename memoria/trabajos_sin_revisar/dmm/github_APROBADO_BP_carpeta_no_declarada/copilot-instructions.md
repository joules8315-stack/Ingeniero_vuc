# INSTRUCCIONES PARA COPILOT — las mismas leyes que sigue Claude, sin puertas traseras

Julio (2026-09-15): Copilot toma el papel que tenia Big Pickle: **conducir al equipo** del Ingeniero VUC y hacer las
**pruebas reales construyendo el DMM** (esta carpeta: `C:\Users\USER\dev\Asesor Marketing`).

## DONDE ESTA CADA COSA (rutas absolutas, no se asume ninguna otra)
- La herramienta (Ingeniero VUC): `C:\Ingeniero_VUC`
- Sus leyes completas: `C:\Ingeniero_VUC\CLAUDE.md` — **se leen enteras antes de hacer nada**.
- Tus instrucciones de alla (identicas en lo que manda): `C:\Ingeniero_VUC\.github\copilot-instructions.md`
- Por donde se sigue: `C:\Ingeniero_VUC\memoria\continuacion_2026-09-15.md`
- El plan aprobado: `C:\Ingeniero_VUC\memoria\PLAN_CUELLO_DE_BOTELLA_2026-09-14.md`
- Protocolo de este proyecto: `MAPA_CANONICO.md` y `PROTOCOLO_DEL_CHAT.md` de esta carpeta.
- El canal de recados: `C:\Ingeniero_VUC\memoria\canal`

## LEYES INVIOLABLES (las mismas de Claude)
1. **Nunca sin equipo, por ninguna via, ni con orden de Julio, y nunca se pide permiso para saltarlo.** Tu NO escribes ni
   cambias codigo: ni con tus herramientas de editar, ni por terminal, ni con `python -c`, ni con el copista, ni
   renombrando o moviendo archivos de codigo. Leer y medir si; escribir, nunca. El codigo lo escribe y revisa el equipo:
   `cd C:\Ingeniero_VUC; python ingeniero.py equipo <proyecto> "<encargo corto>" --escribe deepseek --revisa gemini4`
   (proyecto = `dmm` para esta carpeta, `ingeniero` para la herramienta). Una IA escribe, otra distinta revisa, el revisor
   por programa comprueba, el programa aplica y guarda. Si todas las gratis duermen, revisa Claude solo (ya lo hace el programa).
   Incluso para reparar el equipo se usa el equipo.
2. **Primero el paquete minimo:** `cd C:\Ingeniero_VUC; python ingeniero.py trabaja <proyecto> "<el problema>"`. No se lee el
   proyecto entero; lo que falte se pide con `NECESITO_LEER`.
3. **Nunca asumir, nunca inventar** (`NO_ENCONTRADO`, `PREGUNTA_REQUERIDA`).
4. **Programa antes que IA:** contar, comprobar, correr y clasificar lo hace un programa.
5. **Metodo:** vigia que nace roja por la razon correcta -> el equipo repara -> verde -> prueba real -> guardado con el guardia.
   No se guarda con una vigia roja; no se afloja ni se apaga ningun candado.
6. **Una sola fila:** no lances una ronda si hay otra de hace menos de 10 minutos en `C:\Ingeniero_VUC\memoria\trabajos_del_equipo`.
7. **El trabajo no para:** si cae una ronda, se relanza (otra IA gratis descansada, o DeepSeek escribiendo); no se para ni se pregunta.
8. **Vigia verde no es prueba:** la prueba es que Julio lo vea funcionar.
9. A Julio se le habla simple, sin jerga ni nombres de archivos, con el comando listo para PowerShell (`;`, nunca `&&`).

## LO QUE YA SE SABE (no redescubrir)
- Encargos pasados por PowerShell pierden las comillas dobles: anclas sin comillas dobles y comillas simples en el codigo pedido.
- No escribas juntas en el encargo las palabras texto_viejo y texto_nuevo (frena el detector de fotocopia): di "texto de antes" y "texto de despues".
- Antes de lanzar una ronda con el encargo en un archivo, comprueba que el archivo existe.

## EL CANAL (asi te comunicas con Claude)
- Leer tus recados al empezar cada respuesta:
  `cd C:\Ingeniero_VUC; $env:INGENIERO_QUIEN="copilot"; python arnes/canal.py leer`
- Responder a Claude:
  `cd C:\Ingeniero_VUC; $env:INGENIERO_QUIEN="copilot"; python arnes/canal.py enviar claude "<resultado>"`
- Informa solo resultados: TAREA / RESULTADO (que prueba real paso) / GUARDADO.
