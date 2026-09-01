# MODO INGENIERO — reglas fijas de Cline en este proyecto (las pone el Ingeniero VUC).

Toda orden que Julio de aqui arranca por el MODO INGENIERO. El Ingeniero es el arnes de cualquier
IA: toma la orden y repara. No es una sugerencia: asi, y solo asi debe trabajar.

0. NUNCA TRABAJAR A SOLAS (lo mas importante). Para tocar CODIGO, PRIMERO se corre el equipo:
     cd C:\Ingeniero_VUC; python ingeniero.py equipo ingeniero "<la tarea>"
   Uno GENERA, OTRO distinto AUDITA (nadie se aprueba a si mismo). Si el candado te bloquea,
   NO lo rodees ni lo ignores: pasa por el equipo. No se escribe codigo a solas en ningun proyecto.
1. NUNCA ASUMIR. Si algo no esta escrito, se PREGUNTA (PREGUNTA_REQUERIDA) o se escribe NO_ENCONTRADO.
   Jamas se adivina.
2. NO LEER EL PROYECTO ENTERO. Se pide el paquete minimo:
     cd C:\Ingeniero_VUC; python ingeniero.py trabaja ingeniero "<el problema>"
   Lo que falte se pide con NECESITO_LEER. El candado de lectura frena lo demas.
3. VIGIA VERDE NO ES PRUEBA: la prueba es que Julio lo vea funcionar con sus ojos. Ninguna IA se
   autocertifica.
4. NO ROMPER VECINOS. Antes de tocar se mira "A QUIEN PUEDE DANAR" del paquete.
5. A JULIO SE LE HABLA SIMPLE, sin jerga, y el comando siempre listo para PowerShell (`;`, no `&&`).
6. SI SE PIERDE EL CONTEXTO, NO SE SIGUE A CIEGAS. Se para y se dice que hacer para retomar.

Cuando Julio mande algo: se arranca por el Ingeniero (paquete + equipo), no por cuenta propia.
