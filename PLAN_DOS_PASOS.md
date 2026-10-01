# EL PLAN EN DOS PASOS — que el Ingeniero deje de trancarse

> **Escrito el 2026-09-30 para que no vuelva a perderse.** Hasta hoy este plan vivía repartido en
> mensajes del canal y en el guardado de las 10:57. Dos IA distintas lo reconstruyeron por separado
> y llegaron a lo mismo; esto es ese acuerdo, en un solo sitio.
>
> **Lo aprueba Julio en el chat. No se pide ni se teclea ninguna clave a nadie, nunca.**

---

## POR QUÉ ESTE PLAN Y NO OTRO — los números, no una opinión

| Qué | Número | De dónde |
|---|---|---|
| Frenos apuntados | **2.824** | `memoria/CANDADOS_MEDICION.json` |
| Frenos con culpable identificado | **5** | ídem |
| Pruebas en rojo | **73** | batería completa, 2026-09-30 |
| Trabajos aprobados y frenados, en el disco | **73** | `memoria/trabajos_sin_revisar/` |
| Minutos por orden | **90,1** | `memoria/CUADERNO_DE_LLAMADAS.jsonl` |
| Horas quemadas en el ayudante gratis | **25,9**, fallando 40,6 % | `memoria/BIGPICKLE.log` |
| Segundos del ayudante de pago | **5,06** de media | `memoria/GASTO_USD.jsonl` |

**De los 78 fallos aprendidos, el origen se reparte así** (suma más de 100 % porque un fallo puede
tener varios orígenes):

| Origen | % |
|---|---|
| La herramienta | 37 % |
| El razonamiento de una IA | 36 % |
| La información que llegó | 33 % |
| Quien reparte | 6 % |

**Lo que grita el cuadro:** no hay un culpable único. Pero **nunca se supo cuál era** en el momento
del freno. 2.824 oportunidades de aprender, 5 aprovechadas.

---

# PASO 1 · LA VÍA DEL DIAGNÓSTICO — que cada freno diga quién falló

**La ley de Julio, 2026-09-30:** *"el que frena tiene que vigilar un aspecto específico, así que con
saber el nombre del vigía, y que quede apuntado, por programa, no a mano, en una lista, sabremos qué
está fallando. La lista debe tener la instrucción que se le dio y falló, de modo que podamos
corregir."*

### 1a · La libreta de frenos — `arnes/libreta_de_frenos.py` · NO EXISTE

Cada freno anota, **por programa y en el momento**, tres datos:

1. **cuándo** frenó
2. **el nombre exacto** del que frenó
3. **la instrucción que falló**, con su texto

Un freno que no deja esos tres datos escritos es un **FRENO MUDO**, y es el primer defecto a
reparar. El contador que ya existe (`memoria/CANDADOS_MEDICION.json`) lee esa libreta.

**Su vigía nace ROJA** y comprueba que el renglón queda escrito.

### 1b · Devolver la causa al que escribe — `arnes/lo_que_hay_que_corregir.py` · NO EXISTE

Hoy, cuando una ronda se rechaza, **se le repite al ayudante el mismo encargo y se espera otra
cosa**. Así no aprende: vuelve a fallar igual.

Lo que hace esta pieza: al que escribe se le devuelven **los fallos concretos del intento anterior**,
en un bloque **separado del encargo**, que **se reemplaza en cada intento en vez de acumularse**. Así
el encargo no engorda, no se corta, y el código no se daña.

**Medido hoy:** con los rechazos escritos a mano dentro del encargo, el equipo pasó de RECHAZADO a
DUDOSO a RECHAZADO-por-otra-cosa en tres vueltas. Iba acercándose. Hecho por programa, sin que nadie
se acuerde, eso se cierra en una vuelta.

### 1c · Las seis pruebas en rojo de "quién falló"

Todas en `vigias/test_vigia_el_metodo_manda_en_la_puerta.py` y
`vigias/test_vigia_fallos_de_verdad_avisan.py`:

- ningún fallo puede quedarse mudo
- el disparador tiene que ser una señal, no una frase suelta
- cada frase tiene que decir quién falló
- el octavo rótulo es obligatorio
- la cuenta sube a ocho
- el método se consulta antes que a cualquier ayudante

---

# PASO 2 · EL PAQUETE COMPLETO PERO PEQUEÑO — que el encargo no se corte nunca

**Este paso no estaba en las cinco vueltas del plan de las 10:57, y es el que más tiempo come hoy.**

**Medido en las nueve rondas de hoy:** el pasillo recortó cada encargo **casi a la mitad** — de
26.838 letras a 14.843 — para que le cupiera a un ayudante gratis. Se le manda la ley completa, le
llega cortada, contesta a medias y el auditor lo rechaza con razón. **Eso causó 3 de los 4 rechazos
de hoy.**

### 2a · `tope_del_pasillo` · NO EXISTE

El recorte usa hoy **la capacidad del cerebro más pequeño**. Tiene que usar **la del que de verdad va
a escribir**. Si el que escribe aguanta 60.000 letras, no se recorta a 19.042 por si acaso.

Su vigía ya existe y está en rojo: `vigias/test_vigia_el_pasillo_no_corta_al_que_escribe.py`.

### 2b · Que el recorte no parta una función por la mitad

Hoy el corte es a ciegas por número de letras. Si cae en mitad de una pieza, el que escribe recibe
media función y se rinde. El corte tiene que respetar los límites de cada pieza.

### 2c · Quitar el solape duplicado

El mismo trozo viaja dos veces en el mismo paquete y gasta el sitio de otra pieza.

### 2d · El dato pegado que se confunde con una pieza

**La ley ya está escrita y en rojo desde el 2026-09-29**, con cinco casos, en
`vigias/test_vigia_el_codigo_pegado_no_pide_funciones.py`. Dos siguen rojos:

- un dato que va detrás de una coma se toma por pieza (no debería)
- una pieza declarada de verdad **no** se reconoce (sí debería)

**La regla que sale de los cinco casos:** una palabra conocida cuenta como pieza **solo cuando el
texto la nombra como pieza** — detrás de `def` o detrás de la palabra "función". Si solo aparece
dentro de un trozo pegado, no cuenta. Las que empiezan por raya baja siguen contando como hasta hoy.

**Esto es lo que tumbó 6 de las 13 rondas de hoy antes de que nadie pensara.**

---

# EL ORDEN, Y POR QUÉ

**Paso 1 primero.** Sin diagnóstico, cada arreglo del paso 2 se hace a ciegas y se vuelve a perder.
El paso 1 es lo que convierte cada tropiezo en información en vez de en un obstáculo.

**Paso 2 después, y cierra el bucle:** con el encargo entero llegando a quien puede con él, las
rondas dejan de morirse en la puerta.

---

# LO QUE ESTE PLAN **NO** ARREGLA — dicho sin maquillaje

Para que nadie espere de esto más de lo que da:

1. **Las 73 pruebas en rojo.** El plan arregla 8. Quedan 65, de antes.
2. **Los 73 trabajos aprobados y frenados** que esperan en el disco.
3. **Los doce candados que se trancan entre ellos.** Hay una orden apuntada de Julio que lo nombra
   —*"dos guardianes se contradicen: uno obliga a nombrar las piezas y el otro obliga a no
   nombrarlas"*— y está **sin empezar**. Hoy se perdió una sesión entera peleando eso.
4. **Las direcciones de los candados.** Los doce están escritos con la dirección de Windows. Julio
   trabaja desde la nube, donde la letra del disco no significa nada: ahí **no protegen nada**.
5. **Que el Ingeniero construya cualquier aplicación y se autorrepare.** Con estos dos pasos el
   Ingeniero **deja de trancarse**, que es la puerta de entrada. No es lo mismo que atravesarla.

---

# LA MULTITAREA VA DESPUÉS — y no es una opinión

**Medido hoy:** Codex y Claude escribieron el mismo archivo del grafo a la vez y Windows lo bloqueó;
la ronda de Codex murió con un error de permisos que no era de permisos. La multitarea existe a
medias en `cuerpo/capataz.py` y está **apagada**. Encenderla hoy multiplica los choques, no el
trabajo.

**Se enciende cuando los dos pasos estén verdes y Julio lo haya visto con sus ojos.**

---

# CÓMO SE TRABAJA ESTE PLAN

- **Todas las rondas con el de pago.** El dinero no es el problema: son centavos por ronda. El tiempo
  sí: el gratis quemó 25,9 horas fallando 4 de cada 10 veces.
- **La vigía va primero y nace ROJA** por su propio motivo; el arreglo va en la ronda siguiente.
- **Nada nace huérfano:** una pieza nueva deja puesto quién la llama en su misma ronda.
- **Se avisa cuando cada paso queda verde**, no al final. Si un paso se tranca dos veces seguidas, se
  avisa en el momento con la causa medida.

**PRUEBA HUMANA: PENDIENTE.** Vigía verde NO es prueba. La prueba es que Julio lo vea funcionar.
