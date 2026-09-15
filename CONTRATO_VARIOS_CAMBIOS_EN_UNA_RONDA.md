# CONTRATO — VARIOS CAMBIOS EN UNA SOLA RONDA, TODOS O NINGUNO

**Julio, 2026-09-14** (plan aprobado, paso 1): *"si, aprobado el plan, haz asi segun el plan, mira que no se desvie."*
Base medida: `memoria/PLAN_CUELLO_DE_BOTELLA_2026-09-14.md`, secciones A2 y A3.

## LA LEY
Una aprobacion del equipo puede traer **la lista completa de pedazos** de un arreglo (uno o varios archivos).
El programa los aplica **todos juntos o ninguno**: si un solo pedazo no se puede aplicar, **ningun archivo cambia**.
Un arreglo de 4 pedazos cuesta **1 ronda**, no 4.

## POR QUE (medido)
- No habia ley que pidiera un cambio por ronda: se construyo asi (el aplicador recibe un pedazo; el comando equipo lo llama una vez).
- El 54% de los frenos del revisor de programa ("no hace lo que se pidio") nace de eso: el encargo describe el arreglo
  completo y la ronda lleva un pedazo, asi que las palabras de los otros pedazos "faltan".

## LO QUE NO CAMBIA
- El revisor de IA y el revisor de programa siguen revisando **cada pedazo** (humo, sintaxis, nombres que no existen).
- Quien escribe y quien revisa siguen siendo distintos. El guardado al momento sigue igual.
- Una propuesta de un solo pedazo (como hoy) sigue funcionando exactamente igual.

## TABLA DE VERDAD
| Caso | Resultado |
|---|---|
| Propuesta de 1 pedazo (formato de hoy) | Se aplica como siempre |
| Lista de 3 pedazos en 2 archivos, todos validos | Se aplican los 3; cambian los 2 archivos; 1 sola ronda |
| Lista donde 1 pedazo tiene texto viejo que no esta o esta repetido | NO cambia ningun archivo; dice cual pedazo y por que |
| Lista donde 1 pedazo deja codigo roto | NO cambia ningun archivo; dice cual pedazo y el renglon |
| Encargo que nombra una palabra que esta en OTRO pedazo de la misma lista | El revisor NO frena por "no hace lo que se pidio" |
| Encargo que nombra una palabra que no esta en NINGUN pedazo | El revisor sigue frenando |
| Dos pedazos sobre el mismo archivo | Se aplican en orden sobre el mismo contenido |

## MATRIZ — que se toca (y nada mas)
| Pieza | Que cambia |
|---|---|
| `cuerpo/aplicador.py` | nueva funcion `aplicar_cambios` (todos o ninguno), usando la validacion que ya existe |
| `cuerpo/obrero.py` | el formato de respuesta acepta `cambios: [ {archivo, funcion, texto_viejo, texto_nuevo}, ... ]` y la validacion lo acepta |
| `ingeniero.py` (comando equipo) | la llave abre todos los archivos de la lista; se llama `aplicar_cambios`; se guarda con todos los archivos |
| `arnes/candado_equipo.py` (`_fallos_mecanicos`) | revisa cada pedazo de la lista |
| `arnes/revisor_de_programa.py` (`revisar`) | con lista: humo/sintaxis/nombres por pedazo; "no hace lo que se pidio" sobre la lista entera |

## A QUIEN PUEDE DANAR
`arnes/copista.py` (importa del aplicador), `vigias/test_vigia_aplicador.py`, `vigias/test_vigia_revisor_de_programa.py`,
`vigias/test_vigia_no_se_aplica_lo_frenado.py`, `vigias/test_vigia_lo_aprobado_se_guarda_al_momento.py`.

## VIGIA
`vigias/test_vigia_varios_cambios_en_una_ronda.py` — **nace ROJA** (la funcion aun no existe), se pone verde con la reparacion.
Comprueba cada renglon de la tabla de verdad con archivos de prueba en carpeta temporal (nunca los de verdad).

## COMO SE COMPRUEBA DE VERDAD
Una ronda real del equipo con un arreglo de 2 o mas pedazos: **1 ronda, APROBADO, APLICADO, GUARDADO AL MOMENTO**.
El primer uso real sera el **paso 0** del plan (anotar por que frena cada candado), que toca muchos sitios a la vez.
