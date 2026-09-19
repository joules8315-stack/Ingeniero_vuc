> # ⛔ JUBILADO — y esta vez CON la prueba delante (2026-09-08)
>
> Julio pidio datos, no decisiones. Se comprobo punto por punto: **sus 16 pendientes de marketing
> son los mismos A1-A17 de `MATRIZ_FALTANTES.md`, y sus 7 del Ingeniero son los mismos B1-B7.**
> No aporta ni un hueco que la matriz no tenga ya, con mas detalle y con quien depende de quien.
> Es un duplicado completo, asi que se jubila sin perder nada.
>
> **El unico plan de DMM es `PLAN_SIGUIENTE_IA.md`.** El inventario de lo que falta vive en
> `MATRIZ_FALTANTES.md`. Esto se guarda solo como historia.

# PENDIENTES — arrancar mañana (según contratos). Cierre 2026-07-26 — OBSOLETO
> Lista de lo que FALTA en DMM (Marketing) e INGENIERO, con su contrato. Ver estado pieza-por-pieza en `MATRIZ_DE_VERDAD.md`. Leyenda: ⏳ construir · 🔌 conectar/operar · 👤 paso de Julio (externo).

## CÓMO ARRANCAR MAÑANA
1. `python mvp2_check.py` (puerta/arnés) → debe decir "ARNÉS SANO".
2. Leer este archivo + `MATRIZ_DE_VERDAD.md`.
3. Confirmar cerebros: `.env` con Gemini+Groq; LM Studio en Running.
4. Decir "sigue" y retomar por el pendiente #1 (índice fuerte semántico).

---

## A) DMM — MARKETING (pendientes por contrato)
1. ⏳🔌 **Login seguro** (`CONTRATO_ACCESO_Y_GOOGLE`, Ley 1): wire de **Supabase Auth** (form POST + `SUPABASE_ANON_KEY`) O activar **Google Sign-In** (credencial Google). El login propio es dev/inseguro.
2. 🔌 **Captador de políticas fase 2** (`CONTRATO_CAPTADOR_POLITICAS`): enganchar **buzón real** (IMAP, `joules8315@gmail.com`) + **monitoreo web con cron** + confirmar URLs oficiales.
3. ⏳ **Tendencias/viral** (Ley 6 `CAPTADOR`): buscar lo viral y adaptarlo a la marca (legislado, NO construido).
4. 🔌👤 **Contestadora fase 2** (`CONTRATO_CONTESTADORA_OMNICANAL`): **canales WhatsApp/FB por API oficial de Meta** + historial de conversación. (El chat web y las reglas LC1-LC11 ya están.)
5. 🔌 **Ventas/inteligencia comercial** (Ley): conectar la **contestadora → registrar preguntas**; registro de ventas real. (Módulo `ventas.py` hecho, sin datos.)
6. 🔌 **Medir/Publicar real** (`CONTRATO_CAMPANAS`): **insights reales por publicación** de Meta; activar **envío real** (mecanismo con confirmación ya hecho).
7. ⏳ **Branding dinámico** (`CONTRATO_BRANDING_MM`): **extraer color del logo** (Pillow) + guardar paleta en el perfil (legislado, NO construido).
8. ⏳ **Análisis de la huella digital** (Ley de Perfil Vivo): el campo se captura; falta el **análisis profundo** (buscar la huella en la red + competencia). El sugeridor de redes ya está.
9. ⏳👤 **Video real** (`CONTRATO_MODELOS`): storyboard hecho; **render Flux→Wan por escenas en GPU** = fase final.
10. ⏳ **Ciclo semanal automático** (Leyes Ciclo Semanal + Estrategia Adaptativa + Revisión de Políticas): reorganizar la agenda por datos, cierre jueves/publica viernes, horario de audiencia (legislado, NO automatizado).
11. 🔌 **Propagación de precios** (Ley): subir lista → propaga a **todos los canales + recicla fotos** (hoy: web/generadores sí; redes/fotos falta).
12. 🔌👤 **Persistencia en Supabase real** (`CONTRATO_SUPABASE`): poner `SUPABASE_URL/KEY` (nube); **llaves cifradas a Supabase Vault**; **RLS por cuenta**.
13. ⏳ **Multi-empresa** (maestra-esclava): guardar/buscar por **NIT/cédula** (futuro).
14. ⏳ **Cobro/suscripción** (`CONTRATO_PRODUCTO_Y_PLAN`, Plan 50k): construir el plan Base/Premium y el cobro (límites de Gemini ya verificados).
15. 👤 **Desplegar** (FastAPI + hosting https) + **App Review de Meta** (pasos de Julio).
16. 👤 **Pruebas reales de Julio** (no-ship) con las llaves puestas, del bloque ya listo (parrilla, generadores, contestadora, web, precios, medir).

## B) INGENIERO DE SOFTWARE AUTÓNOMO (pendientes por contrato)
Hecho: 11 roles + Director + auditor + bucle + constructor + 3 cerebros + Playwright. Falta:
1. ⏳ **Índice FUERTE semántico** (`CONTRATO_MEMORIA` cap.2): **pgvector en Supabase** (hoy es bolsa de palabras).
2. ⏳ **Grafo (GRM)** (`CONTRATO_MEMORIA` cap.3): 5ª capa de memoria (relaciones).
3. ⏳ **Memoria/índice de los OTROS MVP** (Foto Informe): para comunicación rápida al trabajarlos.
4. 🔌 **Correr el Ingeniero VIVO** con Gemini (auditar de verdad) — probado con local (flojo) y una corrida Gemini; falta uso sostenido + que Julio juzgue.
5. ⏳ **Playwright integrado** al flujo (que "pulse los botones" en cada cambio, no solo a mano).
6. ⏳ **Aplicar el Ingeniero** a terminar DMM y Foto Informe (que CONSTRUYA de verdad, validado por Playwright).
7. ⏳ **Bootstrapping**: el Ingeniero construyéndose/mejorándose a sí mismo (hoy solo se audita).

## PRIORIDAD SUGERIDA MAÑANA
1) Índice fuerte semántico (pgvector) + grafo + memoria otros MVP → **comunicación barata** (base de todo).
2) Login Supabase Auth (seguridad) + enganchar captador al correo real.
3) Correr el Ingeniero vivo y aplicarlo a terminar piezas de DMM.
