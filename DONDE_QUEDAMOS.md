# DÓNDE QUEDAMOS — 2026-09-09

**Para retomar sin releer nada. Esto es el estado, no un resumen bonito.**

---

## LO QUE SE ESTABA HACIENDO

**Construyendo la aplicación de marketting, despertando sus piezas dormidas.**

De 82 piezas, **22 estaban construidas, probadas y sin que nadie las llamara**. El plan las daba
por *"departamentos que faltan"*. **No faltaban: estaban desenchufadas.**

### Van 12 despertadas. Todas gratis, sin una sola llamada a IA

| Lo que ahora hace y antes no |
|---|
| Dice **cuánto cuesta cada clic** |
| Apunta a **quién escribió** |
| Cada campaña **cuelga de una meta** que no se pierde |
| **Reparte** cada pregunta a su departamento |
| Guarda lo aprendido **con su fuente y su caducidad** |
| Saca **dos versiones** del mensaje para comparar |
| Deja **rastro** de todo, y sobrevive al apagón |
| Sabe **qué sale mañana** |
| Dice **qué red funciona mejor** |
| Sabe **qué campaña trajo a qué cliente** |
| **No paga dos veces** por calcular lo mismo |
| **Avisa si una red cambia sus reglas** |

**Cuatro de ellas no guardaban nada** y se les reparó la raíz antes de enchufarlas: las metas,
el historial, el calendario y el grafo. *Enchufar algo que pierde lo que guarda es enchufar humo.*

---

## POR DÓNDE SEGUIR — quedan 10

### Necesitan una IA de verdad (6). Una ronda del equipo cada una
`video` (el guion cronometrado) · `perfilador_clientes` (a quién hablarle) ·
`motor_preguntas` (preguntar solo lo que falta) · `director` (de una idea, el plan entero) ·
`skills` (que elija su herramienta) · `rotacion` (repartir entre cerebros)

**Empezar por `video`:** es la de más valor visible.

### Esperan las credenciales de Julio (3). **Van al final, por orden suya**
| Pieza | Qué hace falta |
|---|---|
| Entrar con contraseña | Cuenta de Supabase |
| Memoria en la nube | **La misma llave** |
| Leer los boletines de las redes | Una cuenta de correo **aparte, no la personal** |

**Son dos llaves, no tres.**

### Y una suelta
`cola_autonoma` — la lista para que trabaje solo.

---

## LO QUE FALTA PARA CERRAR EL CICLO

**Publicar de verdad · recoger los datos · el análisis que dice si funcionó.**

Sin esos tres, el ciclo se corta después de las dos versiones y **nunca se aprende nada**. Su
vigía **no finge que están**: se marca en amarillo y dice que publicar de verdad depende de las
credenciales.

---

## EL MÉTODO, QUE NO SE SALTA

1. Mirar qué hace de verdad, no lo que promete su nombre.
2. **¿Guarda lo que produce?** Si no, se repara la raíz **antes** de enchufar.
3. **La vigía primero, y nace roja.** Con las dos caras: que sale con datos, y que **sin datos
   no se inventa nada**.
4. Si es una cuenta, la aplica el copista. **Gratis.**
5. Correr **todas** las vigías, no solo la nueva.
6. Guardar contando **también lo que salió mal**.

Está escrito en `CONTRATO_ENCHUFAR_UNA_PIEZA_DORMIDA.md`.

---

## CÓMO ESTÁ LA HERRAMIENTA

- **636 vigías verdes.** La aplicación: **493 verdes**, 1 marcada a propósito.
- **Sin instrucciones pendientes de legislar.**
- El contador de huérfanas **ya existe y ya no miente**: 23 huérfanas reales, 24 candados
  reconocidos. *Era él mismo el primer huérfano.*
- **El bucle está roto:** ya no se le pide a un cerebro que juzgue trabajo ya hecho y verde. Lo
  comprueba un programa en 0,18 segundos y gratis.
- Al cerebro **solo le llega lo suyo**: de 27.785 letras a que le quepa a uno gratis.

## LOS COMANDOS

```
cd C:\Ingeniero_VUC; python ingeniero.py arranca
cd C:\Ingeniero_VUC; python skills/nace_conectada.py
cd C:\Ingeniero_VUC; python skills/nace_conectada.py --raiz "C:\Users\USER\dev\Asesor Marketing"
```
