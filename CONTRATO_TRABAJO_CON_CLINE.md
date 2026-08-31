# CONTRATO — SE TRABAJA CON CLINE, Y ALGUIEN RESPONDE POR ELLO

**Julio, 2026-08-31:** *"Trabaja con cline y haz la reparacion... Una vez termine la tarea cline,
superviza, si es correcta, dale otra tarea, sino, dile que corrija, y me informas si falla."*

## 1. LA TAREA SE ASIGNA, NO SE OFRECE

Nunca se le manda a Cline una lista para que elija. **Se le asigna UNA tarea concreta**, con:

- **Que hay que conseguir**, dicho como resultado, no como programacion.
- **Lo que ya esta hecho y en verde**, para que no lo repita ni lo pise.
- **Lo que NO debe tocar** (lo que tiene el otro).
- **Lo medido**: numeros, no impresiones.

## 2. NO SE PISAN

Cada tarea tiene **un solo dueno**. El reparto vive en `memoria/REPARTO_IA.json` y lo lleva
`arnes/reparto.py`. Dos IA con la misma tarea es trabajo pagado dos veces y un choque al guardar.

## 3. SE SUPERVISA LO QUE ENTREGA. SIEMPRE.

Cuando Cline dice que termino, **no se da por bueno**. Se comprueba:

| Se comprueba | Como |
|---|---|
| Que hizo lo que se le pidio | corriendo su vigia, y que este **verde** |
| Que no rompio a los vecinos | corriendo las demas vigias |
| Que lo que dice es cierto | **mirando el codigo**, no creyendo su palabra |

Y despues, una de tres:
- **Correcto** → se le da la siguiente tarea.
- **Incorrecto** → se le dice **que corrija**, con el fallo concreto y medido.
- **Falla y no sale** → **se le informa a Julio**. No se esconde ni se maquilla.

## 4. LA PALABRA DE OTRA IA NO ES PRUEBA

Medido el 2026-08-31, dos veces el mismo dia:

- Cline afirmo que faltaba poner una llave que **ya estaba puesta**.
- El revisor del equipo rechazo **tres veces** diciendo que no veia un texto que **si tenia
  delante** (comprobado letra por letra en el papel que recibe).

**Antes de repetirle a Julio lo que dijo otra IA, se comprueba en el codigo.** Si no se comprobo,
se dice que no se comprobo.

## 5. EL CANAL ES UN BUZON, NO UN TELEFONO

Medido: dejar el recado funciona; **despertar a Cline no**. Cline solo lee su buzon cuando alguien
lo abre. Por eso, al dejarle una tarea, **se le dice a Julio** que tiene que abrir Cline y
mandarle leer su buzon. Callarselo es dejar la tarea muerta y aparentar que se avanzo.

## 6. NADA QUEDA PENDIENTE

Igual que para todo lo demas: la vigia nace roja, se repara, queda verde, y recien entonces la
siguiente. **Un paso en rojo no se guarda ni se avanza.**

## QUIEN LO HACE CUMPLIR

- `arnes/reparto.py` — lleva quien tiene que tarea y en que estado.
- `vigias/test_vigia_reparto_con_cline.py` — mide que esto se cumple de verdad.
