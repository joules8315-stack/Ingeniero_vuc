# CONTRATO_LEGISLACION_TOTAL — TODAS las leyes de Julio (consolidado)

> Fecha: 2026-08-24 · Proyecto: Ingeniero VUC (aplica a TODOS los proyectos) · Estado: LEY VIGENTE
>
> Aquí quedan **TODAS** las leyes que Julio ha dado. Cada una con su candado (lo que frena) y su
> vigía (lo que comprueba). Nada se habla sin legislar, sin candado y sin vigía.

---

## PARTE 1 — LEYES DE TRABAJO (equipo y pruebas)

### L1 — SIEMPRE EN EQUIPO, SIN SALTO (aplica a TODAS las IA)
El candado de equipo aplica a Claude, Cline y ChatGPT por igual. Para saltarlo se pide permiso y
la respuesta es **SIEMPRE "denegado"**. Se trabaja siempre en equipo.
- **Candado:** `arnes/candado_equipo.py` + `arnes/edit_gate_universal.py`.
- **Vigía:** `vigias/test_vigia_equipo_total.py`.

### L2 — PROBAR DE VERDAD ANTES DE PEDIRLE A JULIO
Antes de pedirle a Julio que pruebe con sus ojos se corre, con el equipo, una **prueba real
(Playwright)** que demuestre que el objetivo se cumple. Se verifica si el resultado se logró o fue
**autovalidación** (una autovalidación no abre la puerta). Si se logró, se avisa; si no, se aprende
y se reinicia el ciclo, sin excusas.
- **Candado:** `arnes/candado_prueba_real.py`.
- **Vigía:** `vigias/test_vigia_prueba_real.py`.

### L3 — SOLO SE PREGUNTA DESPUÉS DE HABER BUSCADO
Nunca se pregunta a Julio antes de buscar. Se busca primero en: el repositorio, los objetivos, la
legislación, las tablas de verdad, la matriz y la tabla de errores — todo debe estar **indexado**.
Solo si allí no está la respuesta, se pregunta. Nunca antes.
- **Candado:** `arnes/candado_preguntar.py` (PASO 4).
- **Vigía:** `vigias/test_vigia_dudas.py`.

### L4 — SIEMPRE EL EQUIPO PARA LO PESADO (4 ojos)
El volumen lo hace el equipo (DeepSeek genera, OTRO distinto audita). Nadie se aprueba a sí mismo.
- **Candado:** `arnes/candado_equipo.py` + `cuerpo/cruzado.py`.
- **Vigía:** `vigias/test_vigia_equipo_sirve.py`.

## PARTE 2 — LEYES DE CALIDAD DEL TRABAJO

### L5 — TODO LO QUE SE HABLA SE LEGISLA
Toda orden de Julio se legisla: analizar → legislar → tabla/matriz → bloques → indexar → vigías →
arnés → cross-flow (no romper lo que sirve). Un candado sin vigía es un deseo.
- **Candado:** este contrato + `cerebro/protocolo.py`.
- **Vigía:** `vigias/test_vigia_legislar_todo.py`.

### L6 — TODO QUEDA LIMPIO Y EN COMMIT
Nada se queda sin guardar ni ensuciando el repo. Todo lo nuevo se ANOTA EN EL ÍNDICE.
- **Candado:** `hooks/pre-commit` → `arnes/guardia_de_guardado.py` (lo ejecuta GIT).
- **Vigía:** `vigias/test_vigia_commit_limpio.py`.

### L7 — LAS PRUEBAS SON REALES, NO AUTOVALIDACIÓN
Las pruebas Playwright abren el navegador y comprueban el comportamiento de verdad (no son
simulacros ni solo leer el texto del código).
- **Candado:** `arnes/candado_prueba_real.py`.
- **Vigía:** `vigias/test_vigia_pruebas_reales.py`.

### L8 — NO GASTAR TOKENS AL PEDO
DeepSeek (de pago) solo para lo pesado y de último; los gratis para lo liviano. Sin encargo, el
bucle no trabaja. Tope y PARAR.
- **Candado:** `arnes/cuotas.py` (DE_PAGO) + `arnes/loop.py` (tope/PARAR).
- **Vigía:** `vigias/test_vigia_equipo_sirve.py`.

## PARTE 3 — LEYES DE SEGURIDAD

### L9 — LAS CLAVES NO SE LEEN DESDE LA TERMINAL
Las claves de pago viven en las variables de entorno; NINGÚN agente las lee por el chat ni por la
terminal. Solo el código interno las usa.
- **Candado:** `arnes/candado_terminal.py` (bloquea leer variables de entorno).
- **Vigía:** `vigias/test_vigia_claves_protegidas.py`.

## PARTE 4 — LEYES DEL CEREBRO (DMM)

### L10 — EL CEREBRO OPERA CON LA INFO INDEXADA
El modelo que genera NO inventa: se le pasa la info de la empresa INDEXADA y cada parte crea lo que
debe crear (campaña, imagen, video, web, música, podcast).
- **Candado:** la creación SIEMPRE recibe el perfil/index.
- **Vigía:** `vigias/test_vigia_cerebro_operativo.py`.

### L11 — DMM SIEMPRE APRENDE Y CORRIGE
DMM aprende y corrige en campañas, imágenes, videos, web, música, podcast y todo lo que lo conforma.
Cada pieza deja su aprendizaje. Crear sin aprender es un fallo.
- **Candado:** toda creación registra su aprendizaje.
- **Vigía:** `vigias/test_vigia_aprendizaje_total.py`.

## PARTE 5 — LEY DE FILAS (Foto Informe)

### L12 — SOLO SE GUARDAN LAS FILAS ASIGNADAS
La plantilla puede tener más filas; solo se gestionan las que el usuario asigna. Asignar MÁS filas
de las que tiene la plantilla ES error.
- **Candado:** `rv3_prueba_8_texto.py` (regla de filas).
- **Vigía:** `test_vigia_filas_asignadas.py` (en Foto).

## PARTE 6 — LEY DE LA MEMORIA (el repartidor y el paquete)

### L13 — LA MEMORIA NO MIENTE NI OLVIDA (Julio, 2026-08-27)
El paquete que arma el repartidor (tipo Obsidian) tiene que ser COMPLETO para la pieza que se va a
tocar: su flujo, con quién se relaciona, las rutas que ya se tomaron (cuáles reparaciones acertaron
y cuáles no) y su historial. El repartidor trae la información **veraz, completa, medida y necesaria**
para evaluar cada pieza y repararla — sin especular, sin alucinar, sin inventar qué buscar. Y se MIDE
si la memoria sirve: cada `NECESITO_LEER` (paquete incompleto) cuenta como fallo de la fragmentación.
- **Regla madre:** si el sistema no puede trabajar (círculo: el repartidor no trae su propio material
  y el equipo no aprueba), **se REPARA la causa de fondo de la herramienta antes de pedir llaves**.
  La herramienta se repara/afina mientras construye.
- **Candado:** que el repartidor no entregue un trozo sin la pieza/función completa a la que
  pertenece (`cerebro/router.py` + `cerebro/trozos.py`).
- **Vigía:** `vigias/test_vigia_memoria_completa.py`.

## PARTE 7 — LEY DE LA DECISIÓN DE REPARAR

### L14 — ANTES DE REPARAR SE RESPONDEN LAS 5 PREGUNTAS (Julio, 2026-08-27)
Antes de tocar código se responde, y queda escrito, **las cinco preguntas**: ¿Qué voy a reparar?
¿Dónde? ¿Por qué? ¿Cuándo? ¿Cómo lo voy a reparar? Si **todo es positivo** (se sabe todo con
precisión) se **legisla y se repara**. Si algo no se sabe, se **investiga**, se vuelven a responder
las 5 preguntas y recién se repara. Nada de reparar sin saber qué, dónde, por qué, cuándo y cómo.
- **Candado:** `arnes/candado_diagnostico.py` (exige archivo/función/línea/evidencia/cambio/alcance)
  + el paso 3 "Causa raíz, nunca síntoma" del protocolo.
- **Vigía:** `vigias/test_vigia_decision_reparar.py`.

### L15 — LA LLAVE ÚNICA DE JULIO ABRE SOLO LO NECESARIO (Julio, 2026-08-27)
Cuando Julio pone su llave, **no se abren los 12 candados de golpe**. Se abren **solo** los que la
tarea necesita, ni más ni menos. Y antes de abrir, se le dice exactamente **cuáles** candados se abren
y **por qué** (qué protege cada uno). La llave es una, pero su efecto es quirúrgico: autoriza lo que
hace falta y nada más.
- **Candado:** `arnes/autorizacion.py` (la llave) + `arnes/candado_equipo.py` (cómo decide abrir).
- **Vigía:** `vigias/test_vigia_llave_unica.py`.
