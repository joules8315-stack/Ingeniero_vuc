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
