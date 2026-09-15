# POR DONDE SE SIGUE — 2026-09-15 (madrugada)

Todo guardado. Base: `memoria/PLAN_CUELLO_DE_BOTELLA_2026-09-14.md` + ordenes de Julio del 14 y 15.

## HECHO Y GUARDADO (equipo 2: DeepSeek escribe, IA gratis revisa, vigias verdes)
- Varios cambios en una ronda, todos o ninguno: `aplicador.aplicar_cambios` (vigia verde). FALTA enchufarlo al comando equipo y al formato del obrero.
- Revisor por programa caza pruebas con simuladores (1b).
- `cuotas.puede_revisar_claude` + `obrero._claude_directo` + en `auditar`: si TODAS las gratis duermen revisa Claude por linea de comandos; nunca quien escribio (ley de Julio con condicion).
- Capataz: solo 5 funciones sueltas, SIN vigia ni prueba real.
- Plugin de recados de Big Pickle movido tal cual a `.opencode/plugins/` (sigue sin reparar).
- Cerrojo viejo de git quitado (no se guardaba nada desde 14-sep 18:47).

## CAUSAS RAIZ MEDIDAS (no redescubrir)
- Rondas sin revisar: `auditar` pasa 3 veces seguidas por TODAS las gratis (2 intentos + vuelta pesada) y las duerme en segundos; y dos directores lanzando rondas a la vez queman las mismas cuotas. UNA SOLA FILA.
- Encargos pasados por PowerShell pierden las comillas dobles: usar anclas sin comillas dobles y comillas simples en el codigo pedido.
- El detector de fotocopia frena si el encargo trae juntas las palabras texto_viejo y texto_nuevo.
- El candado de memoria frena la primera escritura de cualquier archivo: repetir SIEMPRE y comprobar que el archivo existe antes de lanzar la ronda.
- El revisor por programa acusa en falso con archivo existente y texto de antes vacio; y 'DESAPARECE LO QUE YA ESTABA' ofrece una salida ('decirlo por escrito') que no existe.
- Plugin de recados: lee (marca leido) antes de conocer la sesion; al reiniciar opencode bota los recados.

## SIGUE, EN ESTE ORDEN (con el equipo, vigia roja -> verde -> prueba real -> guardado)
1. Que `auditar` no queme las gratis: una sola pasada por gratis descansadas, luego Claude si todas duermen, luego DeepSeek si no escribio el.
2. Prueba real de la revision por Claude con una ronda de construccion del DMM.
3. Capataz completo + vigilante de caidas + informe horario (Windows lo corre solo).
4. Reparar el plugin de recados (no marcar leido hasta entregar).
5. Enchufar varios cambios por ronda al comando equipo; revisor mira el arreglo completo.
6. Tanda 1: 1c imports repetidos, 1d archivos no nombrados, 1e vigia que falla por la razon correcta.
7. Tandas 3-5 del plan (medicion de frenos, candados por palabras, portero de equipo).
Prueba real de todo: construir el DMM con esto funcionando.
