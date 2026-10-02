# ANEXO — Prueba de punta a punta en el PC de Julio (resultado medido)
Corrige y completa `ESTUDIO_FORENSE_2026-10-02.md`. Fuente: pantalla de Julio, programa `punta.py` (read-only salvo la etapa 4).
La prueba escribió **9 señales en el cuaderno** (`quien = PRUEBA_PUNTA_A_PUNTA`): el cuaderno sí recibe. `MEDIDO`

## Datos
**Etapa 1 — la cadena (0,1 s).** `MEDIDO`
- Estados: fallida 33, pendiente 173, hecha 167, corriendo 2, archivada 18, esperando 17.
- De las 173 pendientes: **96 pueden correr ya**; 77 esperan a otra orden.
- Las que esperan: la orden de la que dependen está `pendiente` en 68 casos, `corriendo` en 2 y `fallida` en 7.
- Desde las 22:03: **+9 fallidas y 0 hechas** (24 → 33; 167 → 167).

**Etapa 2 — el cierre (0,1 s).** `MEDIDO`
- Fallidas por paso: `no_aprobo` 23, `sabotaje` 6, `guardia` 3, `no_aplico` 1.
- Las 6 de `sabotaje` (H2, R27, 197, 199, 193, 175) no traen razón en `nota` (solo H2 trae una nota que habla de otra cosa) y **no hay ninguna línea `SABOTAJE` en las salidas guardadas**: la razón del sabotaje no se guarda en ningún archivo.

**Etapa 3 — la selección del guardia (1,4 s).** `MEDIDO`
- Hoy el guardia correría **TODAS**. 229 archivos cambiados; 3 son código fuera de `vigias/`.
- Archivos que fuerzan TODAS por "código sin vigía vecina": **`crear_las_ordenes.py` y `poner_el_orden.py`** (están sueltos en la carpeta del Ingeniero). Ayudantes de pruebas que fuercen TODAS: ninguno.
- Si solo se guardara 1 archivo típico: `cuerpo/obrero.py` → 85 vigías; `cuerpo/capataz.py` → 40; `arnes/vecinas.py` → 11; `arnes/guardia_de_guardado.py` → 17; `ingeniero.py` → 56.

**Etapa 4 — el guardia real (602,0 s).** `MEDIDO`
- Resultado: **deja guardar (True)**, tras 602 s, con 13 vigías rojas toleradas ("ya rojas antes / esperando su arreglo").
- 602 s es casi el tope de 600 s por grupo: `DEDUCIDO` que algún grupo llegó al tope. `NO SE SABE` si hubo grupos cortados (el mensaje no lo dice).

## Qué corrige esto del estudio
1. **La cadena de dependencias NO es el cuello principal.** Hay 96 órdenes listas para correr; solo 7 esperan a una fallida. Mi §3 (A1–A3) sigue siendo cierto como estructura del plan, pero **no explica** que no avance: lo que no avanza es la **conversión de órdenes corridas en órdenes hechas**.
2. **Cuello medido:** 23 de 33 fallidas (70 %) son `no_aprobo`; 0 hechas nuevas en la última ventana.
3. **La causa de `TODAS` es medida:** dos scripts sueltos sin vigía vecina (`crear_las_ordenes.py`, `poner_el_orden.py`). Sin ellos, la selección sería la de `ingeniero.py` (56 vigías) más las vigías nuevas.
4. **La lista de rojas conocidas funciona:** con ella, 13 rojas se toleran y el guardia deja guardar. Queda sin explicar por qué a las 22:03 frenó por 4 que estaban en la lista (cambió la lista entre medias: `NO SE SABE`).
5. **Observabilidad:** la razón del sabotaje no queda registrada. Es un hueco a cerrar.

## Pendiente de medir
Razón de cada `no_aprobo` (las salidas guardadas traen líneas `fallo :`); razón de cada `sabotaje`; si el guardia pasa con grupos cortados.
