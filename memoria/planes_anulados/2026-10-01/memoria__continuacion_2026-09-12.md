# DONDE QUEDAMOS — 2026-09-12 (tanda 2 nocturna: guardado para limpieza)

## ESTADO TRAS LA TANDA (verificado con pruebas reales)
- **Guardián del `nul` HECHO**: `cerebro/piezas.py` (RESERVADOS_WINDOWS, es_nombre_reservado, barrer_reservados en escanear), `mapa/inventario.py` (mismo patrón), `skills/nace_conectada.py` (copia autónoma local, sin importar cerebro). Borra SOLO archivos con nombre reservado (nul, con, aux, prn, com1-9, lpt1-9) usando ruta larga `\\?\`. Verificado en lab con un `nul` real. `medir_las_nueve_puertas.py:209` NO vulnerable (usa marco.filename); DMM protegido y NO tocado.
- **Lista blanca HECHA**: `memoria/lista_blanca.json` con las 17 de mano (anotadas vía `lb.anotar(ruta, porque, 'Julio')`). Se añadió `if __name__ == "__main__":` a `skills/medir_acciones.py` y `skills/medir_navegador.py` (exigido por el candado de anotar).
- **nace_conectada ↔ lista_blanca CONECTADO**: `_leer_lista_blanca(raiz)` (respeta INGENIERO_LISTA_BLANCA), `huerfanas()`/`informe()` excluyen blancas. Resultado: **HUERFANAS: 6 de 86 (17 de mano no cuentan)**. La 6 restantes = las del plan ENCHUFAR.
- **Hook git INSTALADO**: `git config core.hooksPath hooks` → `hooks/pre-commit` corre `arnes/guardia_de_guardado.py`. El guardia corre pytest completo (verde). OJO: los "cuelgues" de pytest eran procesos python huérfanos del guardia; con limpieza corre en ~152s.
- **Suite completa VERDE**: `python -m pytest -q vigias/` → 697 passed, 1 skipped.
- **CORRECCIÓN AL PLAN (confirmada con vigía)**: `arnes/permiso_editar.py` **NO se borra**. `vigias/test_vigia_equipo_total.py:59-61` lo importa y exige `hay_permiso(...) is False`. Queda como llave retirada que la vigía prueba.

## DECISIONES DE JULIO (tomadas vía pregunta esta tanda)
- `candado_archivo_del_veredicto.py` → conectarlo en `candado_equipo.guardar_veredicto` (patrón revisor_de_programa: tumbar el APROBADO si el archivo reparado no es del encargo).
- `limpiar_credenciales.py` → conectarlo al cierre de sección en `candado_prueba_real`.
- Julio pidió PARAR para limpiar: los enchufes NO se tocan aún, quedan anotados abajo.

## ENCHUFES PENDIENTES (de los 6; decisión de Julio ya tomada)
1. `candado_archivo_del_veredicto.py` → enganchar en `arnes/candado_equipo.py::guardar_veredicto` (import + revisar_veredicto; vigía test_vigia_archivo_del_veredicto conforme).
2. `limpiar_credenciales.py` → llamar `limpiar()` al final de `candado_prueba_real.marcar()`.
3. `cuerpo/lecciones.py` → `apuntar()` no se llama en ningún flujo; **sigue esperando que Julio diga dónde** (al sellar / flujo paquete / a mano). PREGUNTA_REQUERIDA vigente.
4. Hechos ya: nace_conectada↔lista_blanca, guardia_de_guardado→hook git. `permiso_editar.py` NO se borra (ver arriba).

## COMO SE REANUDA
```
cd C:\Ingeniero_VUC
python -m pytest -q vigias/
python skills\nace_conectada.py            # ver 6 de 86
```
Siguiente trabajo real: los enchufes 1 y 2 (según decisión de Julio), y preguntar lo de lecciones.

---
## ANTES DE LA TANDA — lo que quedaba de ayer (2026-09-12, "guarda todo, seguimos mañana")

## EL PLAN QUE VA (aprobado por Julio)
Descargar a Claude de la carga. opencode (esta herramienta) hace: 3 dormidas del negocio (DMM), correr/reportar suites, 24 dormidas de la herramienta (incluyen partes del arnés que no funcionan). Claude hace: 26 leyes sin guardián, dirigir al equipo, comprobarlo suyo, causa raíz. Carriles separados, aviso al cerrar, tres preguntas.

## ESTADO VERIFICADO (hechos ya medidos)
- Suite herramienta (C:\Ingeniero_VUC): `python -m pytest -q vigias/` → 688 passed, 1 skipped (143.90s).
- Suite DMM: `python -m pytest -q vigias/` → 688 passed, 1 skipped (171.96s).
- Espía A1 ya construido y verde: `vigias/_espia.py` existe, `test_vigia_el_espia.py` 4/4.
- Contador de huérfanas: herramienta **24 de 86**; DMM **5 de 105**.
- DMM git: rama `integration/mvp2-asesor`, 74 commits por delante de origin, único cambio sin guardar `.salud_almacen.json`. NO subir a GitHub (LEY 3).
- `ESTADO.json`: prueba_humana PENDIENTE (solo Julio la pone en HECHA); vigias_antes limpiado 2026-09-12 10:21.

## PAQUETE VIGENTE DE LA HERRAMIENTA
`memoria/paquetes/ingeniero__descargar_a_claude_de_la_carga__correr_l.md` (flujos piezas(6), equipo(6), medir(6)). Toda reparación SOLO con ese paquete.

## CLASIFICACIÓN DE LAS 24 HUÉRFANAS DE LA HERRAMIENTA (paso 1 COMPLETO)

### BORRAR (1)
- `arnes/permiso_editar.py` — RETIRADO (Julio 2026-08-26). `hay_permiso` siempre False, `dar()` devuelve error. Código muerto, nadie lo llama. OJO: antes de borrar, revisar que ninguna vigía lo exija (`test_vigia_legislar_todo.py`, `test_vigia_llave_unica.py` lo mencionan).

### LISTA BLANCA — herramienta de mano (17) → van a `memoria/lista_blanca.json`
- skills (11): cazar_el_humo, falta_en_el_material, frenos_con_culpable, julio_pudo_trabajar, leyes_sin_vigia, medir_acciones, medir_al_equipo, medir_navegador, orden_o_texto_pegado, quien_sirve_de_verdad, via_unica
- arnes (5): loop, medir_precision, mirada_completa, renovar_permiso_pruebas, supervisor
- mapa (1): auditoria_proyecto

### ENCHUFAR (6) — el foco real del "arnés que no funciona"
- `skills/nace_conectada.py` → RAÍZ: el contador NO lee la lista blanca; hay que conectarlo con `skills/lista_blanca.py` para que las 17 de mano dejen de contar.
- `skills/lista_blanca.py` → nadie la consume; queda muerta hasta que `nace_conectada` la lea.
- `arnes/candado_archivo_del_veredicto.py` → no está enganchado en `.claude/settings.json`; cablearlo (existe su vigía `vigias/test_vigia_archivo_del_veredicto.py` → existe).
- `arnes/guardia_de_guardado.py` → debe ejecutarlo git como hook `pre-commit`, pero `.git/hooks/` solo tiene `.sample` → instalar el hook.
- `arnes/limpiar_credenciales.py` → el paquete dice que la llama `candado_prueba_real`, pero grep: NO la llama nadie → cablearla a `candado_prueba_real`/cierre.
- `cuerpo/lecciones.py` → `apuntar()` no se llama en ningún flujo (F8 punto h muerto). Decide Julio dónde: al sellar, en flujo de paquete, o a mano.

## PASO 2 (próximo a ejecutar)
1. Escribir `memoria/lista_blanca.json` con las 17 de mano.
2. Borrar `arnes/permiso_editar.py` (verificando vigías primero).
3. Enchufar las 6: `nace_conectada`↔`lista_blanca`, candado del veredicto en settings, hook git, `limpiar_credenciales`, y el punto de llamada de `lecciones.py` (decisión de Julio).
4. Correr suites + `nace_conectada` para ver el número real bajar.

## PENDIENTES DEL NEGOCIO DMM (decisión de Julio, no bloquean lo de la herramienta)
- 3 dormidas de opencode: `cuerpo/imagenes.py`, `cuerpo/captador_correo.py`, `cuerpo/auth_supabase.py` (dependen de decisiones de Julio).
- `arnes/compilar_mapa.py` se corre desde `sellar.sh` → candidata lista blanca.
- `cuerpo/skills.py` = B7 catálogo, la necesita el fabricante, no es de opencode.

## HECHOS DEL ARNÉS YA REUNADOS
- Candados enganchados hoy en `.claude/settings.json`: candado_legislar, candado_buzon, candado_por_nombre, candado_companero, candado_ruta_de_acceso, candado_gasto, candado_comunicacion, candado_supervisor, candado_no_repetir, candado_commit. (`candado_archivo_del_veredicto` NO está entre ellos.)
- `obrero.py` (947 líneas) trae `_deepseek_directo` (DeepSeek pago, API propia), `_gemini_directo`, `_openrouter_directo` como puertas reales. Su docstring aclara: DeepSeek = CEREBRO de pago; Cline = ENCARGADO (canal 4ojos). Son dos cosas distintas.