---
paths:
  - "vigias/**/*.py"
---
# Reglas de las VIGIAS del Ingeniero

- **Test-first**: la vigia se escribe ANTES de la reparacion, y debe ponerse ROJA primero.
  Una vigia que nace verde no probo nada.
- Cada vigia debe probar el **caso que Julio de verdad vive**, no un caso de laboratorio
  (leccion C25/C26: fallos P0 "cubiertos" por vigias que probaban datos que nadie usa).
- Si el proyecto de un caso no esta en esta maquina: `pytest.skip`, nunca falsear un verde.
- Los casos nuevos salen de fallos REALES y se apunta la fecha del fallo en el docstring.
