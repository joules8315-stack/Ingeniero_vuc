# 🧭 PLAN PARA LA SIGUIENTE IA — terminar DMM sin contratiempos

> Julio dirá **"arranca todo" / "sigue" / "continúa" / "continúa por donde terminó"**. Este archivo es la
> primera lectura ante esas frases. Objetivo: terminar el trabajo sin repetirle nada a Julio y guiándolo en
> lo que le toca a él. Vive junto a [[MAPA_CANONICO]] (dónde está todo) y [[PROTOCOLO_DEL_CHAT]] (cómo trabajar).

## 0) AL ARRANCAR (haz esto SIEMPRE, en orden)
1. Lee: `MAPA_CANONICO.md` (Nivel 0), este `PLAN_SIGUIENTE_IA.md`, la memoria `punto-de-retomada`, y `git log --oneline -8`.
2. Confirma verde: `cd "C:\Users\USER\dev\Asesor Marketing"; python -m pytest -q vigias/` → deben pasar TODAS (~319).
3. Trabaja UNA tarea a la vez (abajo), con el arnés: semáforo → construir con el EQUIPO → vigía → `bash sellar.sh "msg"`.
4. **NO subas a GitHub** (LEY 3). Solo Julio autoriza (ver §4).

## 1) ESTADO ACTUAL (probado en vivo, funciona)
Campaña con prompt de imagen · ventana **Asesor IA** (chat grounded, persiste) · **pantallazo/manual de métricas**
→ la web analiza con el cerebro · **web nivel agencia** (dogfood DMM, con paleta+copy de Gemini, cacheada) ·
**búsqueda de competencia real** (brazos, sin anuncios) · **perfil editable** (prellena) · respaldo GitHub hecho
(pero congelado: no más push sin permiso). Arranque: `python web/servidor.py` → http://127.0.0.1:8200.

---

# ⚠️ ESTE ES EL ÚNICO PLAN DE DMM (Julio, 2026-09-08)

> Julio: *"verifica antes los planes que ya están y mira si nos acogemos a uno de ellos o creamos
> otro nuevo, por lo cual los viejos deben quedar obsoletos, de modo que no te confundas a la hora
> de mirar si se está siguiendo el plan. Que este sea el correcto."*
>
> **Se acoge ESTE**, porque `PROTOCOLO_DEL_CHAT.md` ya lo declara la primera lectura ante "sigue".
> **QUEDAN OBSOLETOS:** `PLAN_DE_ATAQUE.md` y `PENDIENTES.md`. No se leen ni se siguen.
> `MATRIZ_FALTANTES.md` y `CONTRATO_MAESTRO_DMM_AGENCIA.md` **no son planes**: son el inventario de
> lo que falta, y alimentan a este. Si algo no está aquí, no se hace.

## ESTADO MEDIDO EL 2026-09-08 (probado USANDO la aplicación, no leyendo código)

Se arrancó DMM, se dio de alta una panadería de barrio y se recorrieron sus **24 pantallas** como
un cliente. **Las 24 sirven.** La página de ventas escribió copy propio del negocio, no plantilla:
*"Pan que sabe a hogar, no a fábrica. Aquí el tiempo no corre, se deja fermentar."*

**Pero contra su propio mapa de departamentos: 1 terminado, 12 a medias, 4 que no existen.**

| | Cuenta |
|---|---|
| Departamentos terminados | **1** de 17 (solo Branding) |
| Piezas de programa | 83 (50 programa puro · 33 llaman a una IA) |
| Habilidades sueltas | **0** (el Ingeniero tiene 11; DMM ninguna) |
| Vigías | 149 |

### Lo que Julio preguntó, contestado con los documentos de DMM

| Pregunta | Respuesta honesta |
|---|---|
| ¿Se mejora a sí mismo? | **NO** — "solo se audita" (matriz B7) |
| ¿Crea podcast? | **NO existe** — faltan podcast, voz, avatar, animación |
| ¿Le dice al cliente cómo mejorar? | **NO existe** — falta entero el departamento de inteligencia de negocio |
| ¿CRM? | **A medias** — la pieza está, sin canales reales |
| ¿Busca la huella digital? | **A medias** — capta el dato, **no sale a buscarla en internet** |
| ¿Analiza campañas? | **NO existe** el departamento de publicidad |

## EL ORDEN. NO SE SALTA NI SE REORDENA.

| Turno | Tarea | Por qué va ahí |
|---|---|---|
| **1** | **T13 Ciencia Experimental** | El propio DMM lo marca como el mayor faltante: *"es la diferencia entre un generador de contenido y un director de marketing basado en evidencia"*. Sin esto, DMM repite lo que ya sabe que no sirve |
| **2** | **T12 Ficha científica** en cada creativo | Es lo que hace útil al de arriba: sin ficha no hay qué medir |
| **3** | **T18 Inteligencia de negocio** *(nueva)* | Es "decirle al cliente cómo mejorar su negocio". Hoy no existe |
| **4** | **T19 Publicidad y análisis de campañas** *(nueva)* | Es "analizar campañas". Hoy no existe |
| **5** | **T20 Huella digital de verdad** *(nueva)* | Hoy solo capta el dato; falta salir a buscarla |
| **6** | **T14 Derechos de autor** | Transversal y obligatorio: publicar sin esto es un riesgo legal real |
| **7** | **T15 Calidad nivel agencia** | Hoy la web "parece de niños" (juicio de Julio) |
| **8** | **T17 Podcast y voz** *(nueva)* | Lo pidió Julio; el departamento creativo lo tiene declarado y sin construir |
| **9** | **T16 Orquestador CEO** | Coordina todo lo anterior: va después, no antes |
| **10** | **T7 Estado canónico** | Auditoría de bajo riesgo, no bloquea a nadie |
| **11** | **T21 Canales reales (CRM vivo)** *(nueva)* | Depende de trámites de Julio y de terceros |
| — | **T6 Imágenes** | **PARADA: depende de que Julio active el cobro de Google.** No se toca |

**Hechas y selladas:** T1, T2, T3, T4, T5 (2026-07-28).
**Sin cerrar de antes:** T8, T9, T11 — se revisan al llegar a su turno; si ya están, se marcan.

### ⚠️ TURNO 1 — LO QUE YA SE INTENTÓ Y FALLÓ **CINCO VECES** (léelo antes de tocar nada)

La memoria de fallos del Ingeniero tiene esto apuntado sobre **T13**, y dice *"te ha pasado 5 veces"*:

> **Qué se pidió:** crear el módulo de Ciencia Experimental que falta según el contrato científico
> creativo.
> **Por qué falló las 5 veces:** *"el módulo no existe y hay incompatibilidad de firmas entre lo que
> espera el contrato y lo que se puede implementar"*.
> **Cómo hacerlo (ya escrito en la cura):** crear `cuerpo/experimentos.py` con las funciones
> **`definir_test`**, **`recoger_resultados`** y **`aprender`**, **con las firmas compatibles con el
> flujo**, no con las que el contrato imagina. `definir_test` devuelve un diccionario con `id`.

**Si el turno 1 se ataca sin leer esto, será la sexta vez.** Primero se comprueba qué firma espera
de verdad el flujo (`asesor.disenar_campana`, `hipotesis.py`, `aprendizaje.py`) y se construye contra
ESA, no contra la del papel. Eso es una cuenta: se mira, no se adivina.

### Las tareas NUEVAS, en detalle

- **T18 — INTELIGENCIA DE NEGOCIO** (`cuerpo/negocio.py`): ganancia, retorno de lo invertido, cuánto
  cuesta traer un cliente, cuánto deja en toda su vida, el embudo y la previsión. **DONE cuando** DMM
  le dice al dueño, con números suyos, qué cambiar para ganar más. Base: `analista.py`, `ventas.py`.
- **T19 — PUBLICIDAD Y ANÁLISIS DE CAMPAÑAS** (`cuerpo/publicidad.py`): reparto de presupuesto,
  optimizador, y el análisis de qué campaña funcionó y **por qué**. **DONE cuando** DMM compara dos
  campañas y dice cuál repetir con la razón medida. Base: `campana_flujo`.
- **T20 — HUELLA DIGITAL DE VERDAD** (ampliar `brazos.py`): salir a buscar al cliente en internet
  (redes, reseñas, vídeo) y analizar a su competencia. **DONE cuando** con solo el nombre del negocio
  DMM trae su huella real y la compara con dos competidores.
- **T17 — PODCAST Y VOZ** (`cuerpo/podcast.py`): guion, voz y montaje. **DONE cuando** de una campaña
  sale un episodio escuchable. Cuidado con T14: la música y las voces tienen dueño.
- **T21 — CANALES REALES (CRM vivo)**: WhatsApp, Facebook e Instagram por la vía oficial + calendario.
  **Depende de trámites de Julio y de Meta**, por eso va al final.

### RESCATADO DE `PLAN_DE_ATAQUE.md` antes de jubilarlo (Julio, 2026-09-08)

Julio preguntó si tenía datos para declararlo obsoleto. **No los tenía: lo decidí.** Al medirlo,
dos huecos suyos seguían VIVOS y no estaban en ningún otro documento. Se migran aquí (ley L9 de
`CONTRATO_ESTADO_CANONICO`: lo viejo se migra o se borra, nunca queda huérfano):

- **T14-a — QUITAR LA MARCA DEL CURSO DEL CÓDIGO (derechos de autor, URGENTE).**
  Comprobado el 2026-09-08: sigue en `cuerpo/generadores.py` renglón 45 ("MÉTODO OBLIGATORIO
  (Mercatitlán / Valor Antiventa)") y en `cuerpo/video.py` renglón 4. **Y el filtro de palabras
  prohibidas de `cuerpo/cerebro.py` NO la caza**, porque solo vigila "mertatitlan", mal escrito y
  sin tilde. Es la marca de un curso ajeno metida en el producto. El plan de ataque además apuntaba
  que ese método clavado a mano **es la causa de que las generaciones salgan iguales**. Va dentro
  del turno 6 (T14, derechos de autor) y es lo primero de ese turno.
  **Su vigía tiene que NACER ROJA**: se comprueba que hoy el filtro deja pasar "Mercatitlán" con
  tilde, y solo se da por curado cuando al quitar el arreglo la vigía se pone roja otra vez.
- **T22 — VALIDADORES** (`cuerpo/validadores.py`): correo, teléfono colombiano, NIT y cédula.
  Comprobado: **no existe ninguno**. Son cuentas puras, así que las hace un programa, no una IA.
  Va al final, con T21.

**Comprobado y ya resuelto** (por eso NO se migra): el botón "Salir" ya existe
(`web/menu.py` renglón 60) y el analista de datos ya existe (`cuerpo/analista.py`). El resto de sus
huecos (login, imágenes, publicar en Meta, métricas, canales) ya está recogido en `MATRIZ_FALTANTES`
y en los turnos de arriba.

## CÓMO SE HACE CADA TURNO (las cinco pruebas, sin excepción)
1. **Primero la vigía, y tiene que nacer ROJA.** Una vigía que nace verde no probó nada.
2. **Lo construye el EQUIPO**, no la IA a solas. Uno escribe, **otro distinto** revisa.
3. **Si es una cuenta, la hace un programa**, no una IA (`CONTRATO_CUENTA_O_JUICIO`).
4. **Se prueba USANDO la aplicación**, no mirando vigías. Una vigía verde NO es prueba.
5. **Se sella** y no se pasa al siguiente turno hasta que este esté verde y usado.

> **AVISO HONESTO:** este orden, escrito aquí, es un documento — y en esta casa ya está medido que
> *"lo que depende de acordarse, no se cumple"*. Mientras no exista un candado que frene al que se
> salta el turno, esta tabla depende de la buena voluntad. Ese candado está legislado en el Ingeniero
> (`CONTRATO_EL_PLAN_SE_SIGUE.md`, 2026-09-08) y **todavía no está construido**.

---

## 2) MANDATO — TAREAS DELEGADAS (obligatorio, SIN opciones)
Haces UNA tarea a la vez, EN ESTE ORDEN. Para cada una: quita su `@skip` en `vigias/test_vigia_PENDIENTES.py`,
constrúyela CON EL EQUIPO (§6), ponla VERDE, verifica en vivo con Playwright si es UI, y **sella** (`bash
sellar.sh`). NO inventes tareas nuevas, NO reordenes, NO pidas permiso para lo que ya está aquí escrito.

### T1 — WEB SIN REPETICIÓN (nivel agencia real)
- **QUÉ:** que la web (`/web-c`) NO repita el mismo párrafo entre secciones (hoy `características`, `nuestra
  experiencia`, `quiénes somos` reciclan el texto de `negocio` → se ve plantillero).
- **POR QUÉ:** Julio exige que parezca de una agencia real; la repetición es la señal #1 de amateur.
- **DÓNDE:** `web/web_c.py` (`copys_cerebro` y el ensamblado de secciones).
- **CÓMO (con el equipo):** amplía `copys_cerebro` para que Gemini escriba copy DISTINTA por sección
  (`caracteristicas`, `sobre-empresa`, `para-quien`), en UN solo JSON, respetando la CACHÉ (no gastar en cada
  carga). Cada sección usa su copy; si no hay, cae al texto del perfil (nunca vacío).
- **PROBARLO:** `test_web_secciones_no_repiten` en verde + `python web/servidor.py` y screenshot con
  `scratchpad/dmm_web.py` → que Julio apruebe la estética.
- **DONE cuando:** ningún párrafo >60 chars se repite y Julio dice "sí, parece de agencia".

### T2 — MULTI-INQUILINO (para alquilar)
- **QUÉ:** `empresas_guardadas()` es GLOBAL; aíslalo POR CUENTA (email del login). Cada usuario ve SOLO sus
  empresas; cupo de empresas por plan.
- **POR QUÉ:** Julio va a ALQUILAR DMM; sin aislamiento, un cliente vería las empresas de otro (inviable).
- **DÓNDE:** `cuerpo/perfil.py` (`empresas_guardadas`, `fijar_actual`, almacén por cuenta), `cuerpo/auth`.
- **CÓMO (con el equipo):** clave de almacén = cuenta+empresa; `empresas_guardadas(cuenta)` filtra por cuenta.
- **PROBARLO:** `test_empresas_aisladas_por_cuenta` verde (cuenta A no ve las de B).
- **DONE cuando:** dos cuentas distintas nunca ven las empresas de la otra.

### T3 — PRODUCTOS: AGREGAR/QUITAR UNO A UNO
- **QUÉ:** agregar o eliminar UN producto sin re-subir toda la lista, con botón **Aplicar** en Empresa.
- **POR QUÉ:** Julio lo pidió (cada producto que guarde, editable a mano); hoy solo se reemplaza la lista entera.
- **DÓNDE:** `cuerpo/precios.py` (añade `agregar_item`/`quitar_item`, REUSAR, no duplicar) + form en `web/bloque_empresa.py` + ruta.
- **CÓMO (con el equipo):** el motor genera `agregar_item`/`quitar_item` contra su vigía; Claude cablea la UI.
- **PROBARLO:** `test_agregar_quitar_producto` verde + Playwright (agrega/quita y persiste).
- **DONE cuando:** se agrega y se quita un producto y queda guardado y visible.

### T4 — SEGUIMIENTO DE PUBLICACIONES + AJUSTES DESDE LA WEB
- **QUÉ:** la web lleva el control de las publicaciones (Julio renovó 4) y sugiere ajustes.
- **POR QUÉ:** Julio quiere monitorear si sirven y corregir, TODO desde la web (no desde el chat con Claude).
- **DÓNDE:** nuevo `web/panel_seguimiento.py` + `cuerpo/campanas_registro` + `cuerpo/aprendizaje` + la ventana `/chat`.
- **CÓMO (con el equipo):** el cerebro interpreta métricas por publicación y devuelve el ajuste; se muestra en la web.
- **PROBARLO:** `test_seguimiento_publicaciones` verde + Playwright.
- **DONE cuando:** la web lista las publicaciones con su métrica y un ajuste sugerido, y persiste.

### T5 — CRM (base)
- **QUÉ:** `cuerpo/crm.py` mínimo: registrar contacto (nombre/ciudad/tel/producto/estado del embudo), el usuario
  marca la VENTA, persiste.
- **POR QUÉ:** legislado en [[CONTRATO_CRM_Y_ANALISTA_DATOS]] (función cardinal), NO construido.
- **DÓNDE:** `cuerpo/crm.py` (nuevo) + almacén local + una pantalla simple.
- **CÓMO (con el equipo):** el motor genera `crm.py` contra `test_crm_base`.
- **PROBARLO:** `test_crm_base` verde.
- **DONE cuando:** se registra un contacto, se marca la venta y queda persistido.

### T6 — IMÁGENES REALES (depende de Julio)
- **QUÉ:** generar imágenes reales (no borrador) cuando haya cupo. **DÓNDE:** `cuerpo/imagenes.py` (Nano Banana).
- **CÓMO:** hasta que Julio active billing Google, la web ENTREGA los prompts (ya hecho); no gastes en esto.
- **DONE:** no bloquea; queda a la espera de que Julio active el pago (guíalo, §4).

### T8 — CIENTÍFICO CREATIVO + HISTÓRICO (lo que Julio EXIGE, 2026-07-28)
- **QUÉ:** que DMM deje de repetir cifras obvias y actúe como un profesional: (a) construya un **HISTÓRICO
  real** por publicación (serie en el tiempo, no números sueltos; Julio da métricas cada pocos días); (b)
  **hipotetice POR QUÉ** ganó la que ganó y **diseñe EXPERIMENTOS A/B** para confirmar/descartar y crear
  cada vez mejores campañas; (c) analice **el CREATIVO como un pro**: tono, colores, tipo de letra, imágenes
  y los ELEMENTOS dentro de la imagen.
- **POR QUÉ:** "el cerebro repite lo que ya veo; eso lo hace un niño de 5 años". Necesita pensar y probar.
- **DÓNDE:** `web/panel_resultados` (prompt ya subido a modo científico: hipótesis+experimento) es el paso 1;
  falta: histórico time-series (nuevo `cuerpo/historico.py`), y **alimentar el CREATIVO** (imagen+copy de cada
  post) al análisis — usar `cuerpo/vision.py` para describir tono/color/tipografía/elementos de la imagen
  ganadora. `hipotesis.py`+`aprendizaje.py`+`campanas_registro` ya existen para el bucle ensayo-error.
- **CÓMO (con el equipo):** Gemini vision describe el creativo → el cerebro formula hipótesis sobre esos
  atributos → propone A/B → se registra la hipótesis y se resuelve con las métricas de la próxima semana.
- **PROBARLO:** vigía nueva (el análisis cita atributos del creativo y propone un experimento medible).
- **DONE cuando:** ante una campaña ganadora, DMM explica POR QUÉ (atributos), propone un A/B concreto, y
  Julio dice "esto sí es un profesional".

### T9 — LAS VIGÍAS NO DEBEN BORRAR DATOS REALES (bug, 2026-07-28)
- **QUÉ:** `campanas_registro`/almacén de producción se **resetea al correr las vigías** (`reset()` en
  tests) → los datos reales de Julio se pierden al sellar. Aislar el almacén de TEST del de producción.
- **DÓNDE:** `vigias/conftest.py` (apuntar `almacen`/stores a un temp por sesión) o que los tests usen su
  propio path. **DONE cuando:** correr `pytest`/`sellar.sh` NO altera los datos reales guardados.

### T11 — CAPTURA AUTOMÁTICA de métricas Marketplace (Julio EXIGE automático)
- **QUÉ:** un Playwright que, usando la SESIÓN REAL de Julio (perfil de navegador persistente = sus cookies),
  entre a sus publicaciones de Marketplace → pestaña Estadísticas → screenshot de cada una → `cuerpo/vision.py`
  extrae los números → **`cuerpo/metricas_reales.guardar_manual`** (RUTA ÚNICA, LEY 6). Automático, bajo demanda.
- **POR QUÉ:** Marketplace es su MAYOR canal de ventas y NO tiene API; hoy captura manual = repetitivo.
- **DÓNDE:** nuevo `capturar_marketplace.py` (raíz) con `sync_playwright().chromium.launch_persistent_context(
  user_data_dir=<perfil de Julio>)`; guarda SIEMPRE por `metricas_reales` (LEY 6). CAVEAT ToS: automatizar FB
  va contra su ToS; con sesión propia baja el riesgo; correr solo cuando Julio lo pida. **Preguntar a Julio la
  ruta de su perfil de Chrome** antes de construir.
- **PROBARLO:** con un HTML de Estadísticas de ejemplo (fixture) → extrae y guarda por la ruta única.
- **DONE cuando:** Julio corre 1 comando y sus métricas de Marketplace entran solas al histórico.

### T12 — BUCLE CIENTÍFICO CREATIVO e2e (lo que Julio MÁS exige; [[CONTRATO_CIENTIFICO_CREATIVO]])
- **QUÉ:** que DMM CREE la imagen con su **FICHA** (objetivo + hipótesis + porqué de cada parámetro: imagen,
  texto, color, tipografía, elementos + qué métrica la mide), DEFINA el test ANTES de lanzar, y **a la semana
  recoja los resultados** para confirmar/descartar (aprendizaje). + **encuestas cortas** (2-3 preguntas, no
  obligatorias). + **HISTORIAL completo** de cada imagen y análisis (en pantalla solo la ÚLTIMA campaña).
- **DÓNDE:** `cuerpo/asesor.disenar_campana` (ya da mensaje+hipótesis+imagen_prompt → añadir la FICHA completa
  con el porqué de cada parámetro y la métrica-que-mide) · `hipotesis.py`/`aprendizaje.py` (recoger a la
  semana) · nuevo almacén de FICHAS con historial (serie) · `web/panel_resultados`/`bloque_resultados` (mostrar
  solo la última + acceso al historial) · encuestas cortas (nuevo). Con vision para analizar el creativo.
- **DONE cuando:** al crear una campaña, DMM entrega la ficha (por qué cada parámetro + qué métrica lo mide),
  define el test, y a la semana confirma/descarta con los datos; todo con historial; y Julio dice "esto sí es
  un profesional".
- **T12b — CALIDAD AGENCIA:** la web (propia y de clientes) debe verse nivel agencia, no "de niños" (juicio de
  Julio). Iterar diseño con Playwright+screenshot hasta que Julio apruebe.

### T13-T16 — DEPARTAMENTOS QUE FALTAN (visión agencia autónoma, [[CONTRATO_MAESTRO_DMM_AGENCIA]])
- **T13 Ciencia Experimental** `cuerpo/experimentos.py`: diseñar experimento + KPI + tamaño de muestra +
  validez estadística + sesgos + inferencia causal + extraer la REGLA aprendida y guardarla (que no repita lo
  que ya sabe que no sirve). Es el mayor faltante. Ata con `hipotesis.py`/`aprendizaje.py`.
- **T14 Cumplimiento — derechos de autor** `cuerpo/compliance.py`: verificar imágenes/música/fuentes/logos
  antes de publicar; + vigilar políticas de cada plataforma (extiende `reglero.py`). Transversal, obligatorio.
- **T15 Calidad nivel agencia**: auditor antes de publicar (ortografía/marca/SEO/enlaces/calidad visual) + la
  web deja de "parecer de niños" (juicio de Julio, iterar con Playwright).
- **T16 Orquestador CEO** `cuerpo/director` (ampliar): coordina departamentos, presupuesto, aprobación humana
  configurable (acciones de alto impacto piden OK de Julio o siguen sus reglas).
- Prioridad y estado de TODOS los departamentos: ver el mapa EXISTE/FALTA en [[CONTRATO_MAESTRO_DMM_AGENCIA]].

### T7 — AUDITAR ESTADO CANÓNICO (cero contaminación, ley Nivel 0)
- **QUÉ:** revisar TODOS los almacenes y garantizar UN estado activo por entidad; superseder lo viejo, sin fantasmas.
- **POR QUÉ:** el bug de Foto Informe (versiones viejas vivas que confunden). Ley [[CONTRATO_ESTADO_CANONICO]].
- **DÓNDE:** `cuerpo/perfil_datos` ✓, `cuerpo/precios` ✓, `web/web_c` caché ✓ (ya corregidos); AUDITAR
  `campanas_registro`, `metricas_reales`, `conversacion`, `almacen`, `indice*` y cualquier otro; donde una
  entidad pueda quedar con versión vieja activa, aplica `Clone→Migrate→Validate→Promote→Deactivate→Cleanup→Reindex`.
- **CÓMO (con el equipo):** el motor genera la corrección contra su vigía; Claude define qué es "una activa".
- **PROBARLO:** extiende `test_vigia_estado_canonico` con un caso por almacén auditado (no sirve estado superseded).
- **DONE cuando:** ningún almacén sirve una versión vieja; editar = crear estado nuevo que hereda lo válido y desactiva el anterior.

## 3) CÓMO EJECUTAR LAS PRUEBAS
- **Unidad/candados (rápido, siempre):** `python -m pytest -q vigias/`  (herméticas, sin red).
- **UI/real (navegador):** `python web/servidor.py` en una consola; en otra, un guion Playwright como
  `scratchpad/dmm_web.py` (login `/login?email=test@gmail.com`, crea perfil por el FORM que tiene
  `input[name='nombre_negocio']`, navega, screenshot). Ojo: usa `wait_until="domcontentloaded"` (las imágenes
  remotas cuelgan `load`). Reinicia el servidor tras editar código (no toma cambios en caliente).
- **Sellar:** `bash sellar.sh "mensaje"` — corre TODAS las vigías (no sella si hay roja) y recompila el mapa.

## 4) LO QUE LE TOCA A JULIO (guíalo, no lo hagas por él)
- **Autorizar push a GitHub** (cuando quiera respaldar): en PowerShell →
  `cd "C:\Users\USER\dev\Asesor Marketing"; "ok" | Out-File -Encoding ascii .push_autorizado; git push` y luego
  borrar el permiso: `Remove-Item .push_autorizado`.
- **Probar en vivo con su ojo** (ley: nada se da por bueno sin su prueba): `python web/servidor.py` → recorrer
  Empresa/Entorno/Campañas/Tu Web/Resultados/Asesor IA.
- **Generar las imágenes** con los prompts que le da la web (pégalos en Gemini/Nano Banana).
- **Billing de Google** (si quiere imágenes automáticas y más cuota de visión).
- **Meta/WhatsApp** (App Review) si quiere métricas automáticas en vez de pantallazo.

## 5) CÓMO OPERAR — obligatorio, NO hay opciones (opera como Claude)
Actúas ASÍ, no de ninguna otra manera:
1. **Una tarea a la vez**, en el orden de §2. Terminas y sellas antes de pasar a la siguiente.
2. **Test-first:** primero la vigía (quita el skip de `test_vigia_PENDIENTES`), luego el código hasta verde.
3. **Con el arnés:** semáforo `.mvp2_plan_aprobado` para tocar `cuerpo/`+`web/`; sellar con `bash sellar.sh "msg"`.
4. **Prueba humana:** para UI, corre Playwright, y NO cantes victoria hasta que Julio lo apruebe con su ojo.
5. **NO subes a GitHub** (LEY 3). NO asumes; si un dato no está, preguntas. Toda acción con botón **Aplicar**.
6. **No legislar sin aplicar. Anti-humo** (nada sin fundamento real). Sé económico (§6).

## 6) EL EQUIPO — obligatorio en cada construcción (ultraeconómico)
El token caro es el de Claude. Por eso construyes el CÓDIGO con el equipo, no a mano:
- **Qwen genera** → **pytest (la vigía) verifica** → **Gemini audita** → **Claude solo lee el veredicto JSON**.
- Herramienta: `cuerpo/motor.py` → `construir_pieza(vigia_path, instruccion, ruta_destino, auditar=True)`.
- Antes de gastar cerebro: mira la CACHÉ/lo que ya existe (no dupliques). El copy de la web ya se cachea.
- Claude pone lo FUERTE (las vigías, el juicio, el cableado); el equipo hace la mano de obra.
- Candado que exige el equipo: `vigias/test_vigia_motor.py`, `test_vigia_auditoria_economica`, `test_vigia_copys_cache`.
