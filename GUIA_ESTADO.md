# GUIA_ESTADO.md

**Para que sirve:** Este documento te explica, en palabras simples y sin tecnicismos, qué significa cada casilla del cuaderno donde el Ingeniero apunta por dónde iba el trabajo. Así, cuando quieras saber en qué punto estamos, no necesitas leer un archivo de máquina lleno de símbolos raros.

---

## proyecto
Es el apodo corto que le ponemos al trabajo en el que se estaba avanzando. Sirve para identificar de un vistazo de qué asunto estamos hablando.

## problema
Es el problema o la petición exacta que tú le diste al Ingeniero, escrita con tus propias palabras. Aquí es donde queda registrado qué fue lo que pediste.

## flujos
Son las zonas o áreas del proyecto que ese problema toca. Es como decir: "este trabajo afecta a la parte de precios, a la de plantilla, etc.". Ayuda a saber qué otras cosas podrían verse afectadas.

## paquete
Es la ruta del "paquete mínimo" que está vigente. Esto es el material más pequeño y completo que el Ingeniero puede leer para entender y reparar el problema. Es la única pieza de información que se debe consultar para arreglar algo.

## decision_pendiente
Si esta casilla tiene algo escrito, significa que el trabajo está PARADO. No se puede avanzar porque hay una pregunta que solo tú, Julio, puedes responder. Es una señal de que necesitamos tu opinión para continuar.

## vigias_antes
Aquí se apunta de qué color estaban las pruebas automáticas (verde o rojo) ANTES de que el Ingeniero tocara nada. Sirve para saber el punto de partida.

## vigias_despues
Aquí se apunta de qué color quedaron esas mismas pruebas DESPUÉS del cambio. Si estaban verdes antes y ahora están rojas, significa que algo se rompió.

## prueba_humana
Esta casilla registra si tú, Julio, ya viste el resultado funcionar con tus propios ojos. Mientras diga PENDIENTE, el trabajo no se puede dar por terminado, sin importar lo que digan las pruebas automáticas.

## ultimo_sello
Es la fecha en la que se dio por cerrado el último trabajo. Sirve para saber cuándo fue la última vez que terminamos algo por completo.

## historial
Es la lista de todos los cambios que ha tenido este cuaderno. Cada cambio registra la fecha, qué casilla se modificó y de qué valor a qué valor pasó. Es como el historial de un documento, para saber cómo ha evolucionado.

---

**Nota final:** Recuerda que una prueba automática en verde (que todo funciona) no es la prueba definitiva. La única prueba real es que tú, Julio, lo veas funcionar con tus propios ojos.