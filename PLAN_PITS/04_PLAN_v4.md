# PLAN v4 — Máquina de pits: el equipo construye DMM en loop, Claude sin manos
> Reemplaza al v3 (en `reciclado/`). Base: 01_ACUERDOS · 02_FORENSE · 03_REVISION.
> **APROBADO por Julio el 2026-09-18, tal como está (A-30). Cualquier cambio se le consulta antes.**

## 1. Método con Julio
- Julio aprueba **una vez**, con su llave. La máquina trabaja en loop hasta terminar.
- Al final, **un informe**. **Julio prueba una sola vez**, con DMM terminado.
- **El loop se detiene solo en tres casos:**
  1. DMM terminado, según el plan vigente de DMM;
  2. un frente parado por 3 fallos del mismo tipo;
  3. se agota el saldo de DeepSeek (ya no queda quien haga lo pesado). Sin tope en dólares:
     cada IA de pago se usa hasta que se agote (A-42, orden de Julio 2026-09-21).
  Lo que quede pendiente va en el informe.

## 2. Garantía de trabajar con el equipo (mecanismo, no voluntad)
- **Claude sin manos.** La lista de permisos de la plataforma solo le deja leer. La activa Julio con su llave. Cuando el programa lo llama, Claude trabaja en solo-lectura y contesta en JSON.
- **El pit trae sus propias reglas en su código.** No depende de los candados de Claude:
  - sin un revisor de otra familia no se monta nada;
  - sin etiqueta no se acepta ninguna respuesta;
  - una tarea con una huella que ya falló no se vuelve a enviar.
- Cada regla tiene su **vigía de sabotaje**: se la intenta romper a propósito y tiene que frenar.
- **Los 21 candados existentes no se quitan.** Los que frenan en falso (según el forense) se reparan como tareas del pit, midiendo antes y después.

## 3. Los puestos
```
[0] PORTERO ......... programa: carpeta y rama canónicas, nada sin guardar; si algo falla, no arranca
[A] RECEPCIÓN ....... programa: guarda la instrucción textual + commit (entrada)
[B] ALMA ............ Claude arquitecto, una vez por proyecto (A-29). Ficha: qué es, qué no es, qué no se puede romper, cómo se sabe que está listo
                      + MATRIZ y TABLA DE VERDAD del proyecto
[C] PLANIFICADOR .... programa: parte la ficha en tareas usando el MAPA DE FLUJOS
                      etiqueta de cada tarea: nº, origen, qué repara, pieza, dependencias,
                      PROGRAMA o IA (con razón)
[D] DESPACHADOR ..... programa: varias tareas a la vez; archivos distintos → en paralelo;
                      el mismo archivo → en fila; la IA se elige ANTES según datos reales;
                      si no está disponible, ENTRA LA OTRA (relevo en cadena: Claude→Codex,
                      Big Pickle→Codex; A-40, corregido con el sí de Julio 2026-09-21)
[E] PIT ............. pedazo listo → DeepSeek escribe (solo el cambio)
                      → Big Pickle revisa (JSON) → revisión de forma → monta
                      → prueba pieza y vecinas → vigía "nace conectado"
                      → FILA DE COMMITS (trabajo + cierre)
[F] FORENSE ......... si falla: expediente del programa → análisis con citas (JSON)
                      → Big Pickle verifica las citas → se vuelve atrás
                      → libro de fallos → ley + vigía → tarea NUEVA
[G] CIERRE .......... batería completa de pruebas + commit final + informe
```

**Bibliotecario (la memoria grafo, parte del equipo):**
- Busca en este orden: nombre → función → significado → si no encuentra, dice "no existe".
- **Filtro de salida:** cada pedazo va completo, sin cortes y sin sobras.
- El mapa de flujos lo genera un programa leyendo el código. Una pieza suelta (que nadie usa) se marca en rojo.

**Estados de un trabajo:** *pasa pruebas* → *revisado por otra familia* → **HECHO solo con la prueba de Julio**.

## 4. Equipo (según los datos del forense)
| Papel | Quién | Nota |
|---|---|---|
| Escribir | DeepSeek | Falla 1%. Es el obrero principal |
| Revisar y lo semipesado analítico | Big Pickle (JSON) | **Primero hay que conectarla para que un programa la llame** (hoy tiene 0 rondas automáticas) |
| Tareas pequeñas / revisión de reserva | Groq 120b (encargos pequeños, con pausas de 3-4 min), Gemini 4 | Solo lo que cabe, medido antes de enviar |
| Eliminadas | Groq 20b, Gemini 1 y 3, LM Studio local, OpenRouter | Por datos |
| Arquitecto (una vez) y perito (cuando algo falla) | Claude solo-lectura | Llamado por el programa (A-29) |
| Reemplazo de Claude + revisor si Big Pickle falla | **Codex** solo-lectura, en JSON | **Añadido por Julio el 2026-09-21 (A-40)**. Mismas leyes duras que Claude. Cuenta personal: nunca llaves ni datos de clientes |

**Ahorro:**
- Instrucciones fijas siempre al principio, para abaratar lo que se repite.
- DeepSeek devuelve solo el cambio; Big Pickle solo JSON corto.
- Ninguna IA carga historial.
- El registro anota tiempo y etiqueta de cada llamada.

## 5. Guardar todo (sin volver lento el pit)
- Solo la rama canónica. **Fila de commits:** las tareas trabajan en paralelo, pero guardan de a una.
- En cada commit: la prueba de la pieza y sus vecinas (segundos). **La batería completa, al cierre.**
- Si falla: se vuelve atrás y se anota en el libro de fallos con su commit.
- El libro de acuerdos, el forense, el libro de fallos y la telemetría también van con commit.

## 6. Orden del loop
0. **Portero:** el equipo revisa los 101 cambios sin guardar y guarda los buenos (A-28). Subir esta carpeta con commit. Pasar a "reciclado" los planes jubilados de DMM.
1. **Conectar Big Pickle** por OpenCode, sin ventana, con respuesta en formato de datos y servidor abierto para que no demore. Medir su límite real. Se usa hasta que se agote; entonces revisa Codex (A-42, A-40). El filtro nunca le manda llaves ni datos de clientes (sus datos pueden usarse para entrenar). Limpiar el reparto de IA según el forense y agregar el reloj.
2. **Reemplazo por programa:** inventario "cuenta o juicio" de cada paso; lo que es cuenta pasa a programa y se prueba.
3. **Armar el pit** con las piezas que ya existen: obrero, cruzado, aplicador (varios cambios por tarea), cuotas (elegir antes), subagentes (en paralelo), trozos, router y grafo (pedazos), via_canonica (portero), autorizacion (llave). Esta primera vez Claude escribe **solo los encargos**; el código lo escriben DeepSeek y Big Pickle.
4. **Reglas del pit** con vigías de sabotaje. Reparar los candados que frenan en falso. Revisor de contradicciones de leyes.
5. **DMM:** ficha, matriz y tabla de verdad desde "Lo que falta para terminar el DMM" → loop de tareas hasta terminar.
6. **Ingeniero de Marketing:** un programa confirma que DMM no usa esas piezas para funcionar. El equipo copia al ingeniero lo que le falte y las quita de DMM (A-26).
7. **Cierre:** batería completa + informe → **prueba de Julio**.

## 7. Cómo se comprueba que el equipo funciona
- Claude intenta escribir y la plataforma lo rechaza.
- Se sabotea cada regla del pit (autorrevisión, sin etiqueta, huella repetida) y el pit frena.
- Varias tareas corren a la vez sin mezclarse; cada commit trae su etiqueta.
- Un fallo forzado produce un expediente, un forense con citas y una tarea distinta.
- **DMM terminado, probado por Julio.**
