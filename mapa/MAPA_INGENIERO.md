# MAPA DEL INGENIERO VUC — paso 1 (inventario real, sin suposiciones)
> Generado por `mapa/inventario.py` + `mapa/compilar_mapa.py`. NO se edita a mano: se regenera.
> Regla: aqui solo entra lo que EXISTE en disco. Lo que no aparece, no existe.

**Universo:** 2245 piezas · 609,425 lineas · 4 proyectos.

## 1. Cuanto hay en cada proyecto

| Proyecto | Piezas |
|---|---|
| foto_informe | 1179 |
| Ingeniero VUC (esta herramienta) | 671 |
| dmm | 395 |

## 2. Que tipo de piezas hay

| Rol | Cuantas |
|---|---|
| DATO/CONFIG | 1194 |
| VIGIA | 319 |
| DOC | 190 |
| CODIGO | 160 |
| CONTRATO | 114 |
| CUERPO (modulo) | 99 |
| ARNES/CANDADO | 65 |
| OTRO | 45 |
| LANZADOR/SCRIPT | 22 |
| PROTOCOLO/MAPA | 17 |
| MATRIZ/TABLA_VERDAD | 11 |
| WEB | 8 |
| SKILL | 1 |

## 3. EL CUERPO que ya existe (no se vuelve a construir)

Ruta: `C:\Users\USER\dev\Asesor Marketing\cuerpo`

| Modulo | Lineas | Que hace | Boca (API publica) |
|---|---|---|---|

## 4. LAS 5 CAPAS DE MEMORIA que ya estan (base del cerebro tipo Obsidian)

| Capa | Pieza | Estado |
|---|---|---|
| 1. RAG semantico | `cuerpo/rag.py` | NO EXISTE |
| 2. Indice | `cuerpo/indice.py` | NO EXISTE |
| 2b. Indice semantico | `cuerpo/indice_semantico.py` | NO EXISTE |
| 2c. Embeddings | `cuerpo/embeddings.py` | NO EXISTE |
| 3. Grafo (dependencias) | `cuerpo/grafo.py` | NO EXISTE |
| 3b. Grafo de negocio | `cuerpo/grafo_negocio.py` | NO EXISTE |
| 4. Persistencia | `cuerpo/almacen.py` | NO EXISTE |
| 5. Aprendizaje | `cuerpo/memoria.py` | NO EXISTE |

## 5. EL ARNES que ya existe (metodo de trabajo a copiar y mejorar)

| Pieza | Lineas | Que hace |
|---|---|---|

## 6. CONTRATOS (las leyes ya escritas)

Son **0** contratos. Los que mandan sobre el Ingeniero:


## 7. MATRIZ Y TABLA DE LA VERDAD


## 8. LOS ARCHIVOS MONSTRUO (los que queman tokens al releerlos)

| Proyecto | Archivo | Lineas |
|---|---|---|
| foto_informe | `app.py` | 16,918 |
| foto_informe | `COMPARTIR_IA_CODIGO/app.py` | 15,109 |
| foto_informe | `test_template_session_family.py` | 12,693 |
| foto_informe | `validate_mvp.py` | 7,160 |
| foto_informe | `app_web.html` | 2,463 |
| Ingeniero VUC (esta herramienta) | `memoria/rescate/app_web_reparada_2026-08-24.html` | 2,382 |
| Ingeniero VUC (esta herramienta) | `memoria/rescate/app_web_reparada_2026-08-21.html` | 2,373 |
| foto_informe | `supervisor_full.py` | 1,585 |
| foto_informe | `COMPARTIR_IA_CODIGO/app_web.html` | 1,424 |
| foto_informe | `rv3_prueba_integral.py` | 1,307 |
| foto_informe | `test_table_search_unit.py` | 967 |
| dmm | `web/servidor.py` | 823 |

## 9. REPETIDERA DETECTADA

- Copias con contenido identico en 2+ lugares: **7**
- Mismo nombre de archivo en 2+ lugares: **78**
- `C:\vigias` (52 vigias): comparada una por una contra la carpeta buena.
  **Nada unico. Solo 2 pruebas rescatables:**
  - `test_vigia_cerebro_gemini.py::test_sin_llave_error_claro_no_silencio`
  - `test_vigia_credenciales_env.py::test_carga_llaves_del_env_sin_pisar_las_existentes`
  El resto es copia vieja -> se desecha DESPUES de rescatar esas dos.

## 10. LO QUE **NO** EXISTE (lo que hay que construir)

| Falta | Por que importa |
|---|---|
| `router_contexto.py` | Nadie arma el paquete minimo. El grafo existe pero nadie lo usa para eso. Busqueda: 0 resultados. |
| `guard_alcance.py` (candado de LECTURA) | El arnes frena EDITAR, no frena LEER. El gasto esta en la lectura. |
| Vigias anti-token | De 190 vigias, NINGUNA vigila el gasto ni el alcance de lectura. |
| `CLAUDE.md` + `.claude/rules/` | Ningun proyecto los tiene. Sin eso, la IA entra a ciegas y lee entero. |
| `STATE.json` del Ingeniero | El estado vive en el chat; al cerrarse, se pierde y hay que repetir. |
| Cerebro propio del Ingeniero | `cuerpo/` es el cuerpo de DMM (marketing), no el del Ingeniero. |
| HULK | Julio lo nombro. Busqueda en los 4 proyectos: **NO EXISTE**. Falta que Julio diga que es. |
