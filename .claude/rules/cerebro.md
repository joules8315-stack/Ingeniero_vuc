---
paths:
  - "cerebro/**/*.py"
---
# Reglas del CEREBRO (las 4 capas)

Orden de las capas, no se salta ninguna:
`piezas.py` (archivos) -> `enlaces.py` (hilos) -> `flujos.py` (asuntos) -> `trozos.py` (pedazos) -> `grafo.py` (junta) -> `router.py` (entrega).

- Una ficha **nunca** guarda el contenido del archivo. Guarda como encontrarlo. Si empieza a guardar
  contenido, el cerebro se vuelve tan caro como el problema que resuelve.
- Un trozo **siempre** lleva su direccion real `archivo:desde-hasta`. Nunca `archivo#3`.
- La FUERZA de un hilo no se toca sin correr `vigias/test_vigia_trae_la_pieza_correcta.py`:
  ahi esta legislado que `CONTRATO_PRECIOS.md` gana sobre `MAPA_CANONICO.md` para `precios.py`.
- Al tocar el router: correr `vigias/test_vigia_paquete_no_lee_repo_entero.py`. Es la unica vigia
  del sistema que mira el GASTO.
