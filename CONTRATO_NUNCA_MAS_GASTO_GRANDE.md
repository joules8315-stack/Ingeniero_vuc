# CONTRATO — NUNCA MAS UN GASTO GRANDE

**Julio, 2026-09-02, despues de una manana entera quemada:**
> *"legisla fuerte, nunca mas, nunca mas vuelves a hacer gasto grande"*

## LO QUE PASO, MEDIDO

Una sola manana consumio el 90% de la sesion. Y **el equipo no fue lo caro: fui yo.**
El equipo es lo barato — dos cerebros gratis por reparacion. Lo caro es la IA que dirige,
y esa manana hizo mas de cien idas y venidas para cerrar diez reparaciones.

**A donde se fue el dinero, por orden:**

1. **Repetir cada orden dos veces.** Un aviso del propio sistema frenaba la accion, y habia
   que repetirla identica para que pasara. Cada reparacion costaba el DOBLE de vueltas.
2. **Reformular sin medir.** Se mandaba un encargo, lo rechazaban, se reescribia a ojo, otra
   vez rechazado. Ocho vueltas seguidas en un caso.
3. **Descubrir a mitad de camino que faltaba material**, en vez de comprobarlo antes.
4. **Encadenar reparacion tras reparacion sin parar a contar.** Nadie llevaba la cuenta.

## LA LEY

**1. HAY UN TOPE, Y CUANDO SE LLEGA SE PARA.**
No se sigue "un poquito mas". Se para, se le cuenta a Julio lo hecho y lo que falta, y **el
decide** si se sigue. Gastar sin que el lo sepa es gastar a sus espaldas.

**2. SE AVISA POR EL CAMINO, NO AL FINAL.**
A mitad del tope se le dice cuanto se lleva. Julio no puede decidir sobre un gasto que no ve.

**3. TRES VUELTAS Y SE PARA.**
Si un encargo se rechaza tres veces, NO se intenta una cuarta. Tres rechazos seguidos no son
mala suerte: es que el encargo esta mal planteado o falta algo. Se para y se le dice.

**4. LO BARATO ANTES QUE LO CARO.**
El que dirige NO escribe codigo: lo escribe el equipo. Cada vez que la IA cara hace el trabajo
de la barata, se tira dinero. Ya esta legislado y ahora tambien se mide.

**5. SE COMPRUEBA ANTES DE PEDIR.**
Antes de mandar un encargo se comprueba que el material le LLEGA de verdad. Una comprobacion
barata evita una vuelta cara. Medido: eso solo ahorro ocho vueltas en un caso.

**6. UNA COSA POR ENCARGO.**
Pedir tres cambios a la vez acaba en rechazo y en tres vueltas. Uno por uno aprueba a la primera.

## QUIEN LO HACE CUMPLIR

- `arnes/candado_gasto.py` — cuenta las acciones de la tanda, avisa a mitad y **FRENA** al llegar
  al tope. No es un recordatorio: frena.
- `vigias/test_vigia_nunca_mas_gasto_grande.py` — comprueba que el candado muerde de verdad.

## LO QUE NO ES ESTA LEY

No es trabajar menos ni peor. Es **no gastar a espaldas de Julio**. Si hace falta seguir, se
le pide y el decide: el dinero es suyo y la decision tambien.
