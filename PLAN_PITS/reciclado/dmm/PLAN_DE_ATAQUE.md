> # ⛔ JUBILADO — pero SOLO despues de rescatar lo que seguia vivo (2026-09-08)
>
> **Primero se declaro obsoleto sin datos, y estaba MAL.** Julio lo cazo: *"¿tienes datos que asi
> lo comprueben, o solo lo decidiste?"*. Se midio uno por uno y **dos huecos seguian VIVOS**:
>
> | Hueco de este documento | Comprobado el 2026-09-08 |
> |---|---|
> | Quitar la marca del curso del codigo (derechos de autor) | **SEGUIA AHI**: `cuerpo/generadores.py:45` y `cuerpo/video.py:4`. Y el filtro de palabras prohibidas NO la caza (vigila "mertatitlan", mal escrito) |
> | Faltan validadores (correo, telefono, NIT, cedula) | **NO EXISTE NINGUNO** |
> | Falta el boton "Salir" | Ya resuelto: `web/menu.py:60` |
> | Falta recolector/analista de datos | Ya resuelto: `cuerpo/analista.py` |
> | Login, imagenes, publicar en Meta, metricas, canales | Ya recogidos en `MATRIZ_FALTANTES.md` |
>
> Los dos vivos se MIGRARON a `PLAN_SIGUIENTE_IA.md` (T14-a y T22), como manda la ley L9 de
> `CONTRATO_ESTADO_CANONICO`: lo viejo se migra o se borra, **nunca queda huerfano**.
> Ahora si: **el unico plan de DMM es `PLAN_SIGUIENTE_IA.md`.** Esto se guarda como historia.

# PLAN DE ATAQUE — huecos de DMM (Julio 2026-07-27) — OBSOLETO
> Lista de TODOS los huecos (bugs, faltantes, cosas a medias). Julio: buscar los huecos; los que el EQUIPO pueda reparar, a la cola (`cola_ingeniero.txt`); los que no, quedan listados aquí. Ley dura: la construcción la hace el EQUIPO (Qwen genera → Gemini audita → vigías) — Claude solo dirige y revisa JSON. Ver `CONTRATO_INGENIERO_AUTONOMO.md`.
> **Quién repara:** 🤖 = equipo (cola) · 🧠 = Claude integra (editar código real con arnés) · 👤 = Julio (plata/trámite externo).

## A) DERECHOS DE AUTOR / LIMPIEZA (urgente)
- 🧠 **"Mercatitlán" en `cuerpo/generadores.py`** (línea ~45, "MÉTODO OBLIGATORIO (Mercatitlán / Valor Antiventa)") → es la marca del curso, prohibida como "mertatitlan". Quitarla. **Además es la causa de que las generaciones salgan iguales** (método clavado a mano, no varía con el contexto).

## B) UI / UX (la página)
- 🧠 **No hay botón "Salir"** en los 4 bloques (no hay logout visible; la ruta `/logout` existe).
- 🧠 **Redundancia de "Adjuntar"** en Empresa (el "Choose File" del navegador + el botón "Adjuntar" se leen como dos). Aclarar el flujo.
- 🧠 **Diseño:** mejoró (oro/carbón) pero "no parece de agencia de marketing" — falta concepto visual (hero con propuesta de valor, ejemplos, no solo formularios).
- 🧠 **Generación repetitiva** (mismo resultado 4 veces) → causa raíz = el método clavado (A) + no inyecta bien el contexto/aprendizaje.

## C) FUNCIONAL (lo que no sirve todavía)
- 🧠+👤 **Login real:** hoy entra cualquier correo (dev). Cablear Google/Supabase (credencial existe).
- 👤 **Imágenes reales (Nano Banana):** código LISTO (`cuerpo/imagenes.py`); falta **cupo/billing** de Google (429). Sin esto no hay imagen.
- 🧠+👤 **Publicar en Meta (reel/post):** hoy SIMULADO (`_enviar_simulado` en `publicador.py`). Falta conectar página (OAuth listo) + construir el envío real.
- 🧠+👤 **Métricas reales:** falta leer insights de la página conectada.
- 🧠+👤 **Messenger / WhatsApp:** webhook listo; Meta no entrega mensajes reales hasta **publicar la app** (App Review).
- 🧠 **Bloques 3 y 4 (Campañas/Resultados):** esqueletos; no crean/miden campañas reales completas aún.

## D) PIEZAS LEGISLADAS PERO NO CONSTRUIDAS (parte 🤖 equipo)
- 🤖 **CRM base** (contactos: nombre/cédula/ciudad/correo/tel/dirección/producto + estado + venta).
- 🤖 **Recolector/analista de datos** (agregar métricas, qué se vende más).
- 🤖 **Evidence Manager / Reasoning / Hipótesis** ya existen; falta **integrarlos** al flujo real (🧠).
- 🤖 **Validadores/utilidades** (validar correo, teléfono colombiano, NIT, etc.).

## LO QUE EL EQUIPO ATACA YA (está en `cola_ingeniero.txt`)
Las tareas 🤖 de piezas AISLADAS van a la cola: el equipo (Qwen+Gemini+vigías) las construye en staging, deja JSON, y Claude las integra al volver. Corre **`trabajar.bat`**.

## HONESTO (límite real)
El equipo autónomo construye piezas AISLADAS bien. Los huecos 🧠 (integrar al código real con el arnés) y 👤 (plata/Meta) NO los hace el equipo solo — los hace Claude (integrando) o Julio (billing/trámites). Por eso la cola es corta: la mayoría de huecos hoy son integración/externos, no piezas nuevas.
