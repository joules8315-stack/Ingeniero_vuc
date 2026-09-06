# CONTRATO — UNA SOLA VIA, PARA ABRIR Y PARA GUARDAR

**Julio, 2026-09-05:**

> *"Mira si los commit estan quedando en la via canonica, o rama canonica, dependiendo del caso,
> que no haya mas de una version, verifica esto, si existe mas de una version, unifica en una
> unica via canonica, tanto para abrir, como para commit, nunca otra version fuera de via
> canonica."*

**Julio lo preciso el mismo dia:**

> *"Una sola rama, o via canonica, para ABRIR, TRABAJAR y GUARDAR. Nunca un duplicado, o via
> alterna. Si existe mas de una via o rama, unificala."*

**YA SE UNIFICO (2026-09-05).** Se le enseño a Julio que la segunda copia no tenia nada propio
(cero cambios sin guardar, cero guardados que la principal no tuviera). El dio la orden y se
retiro: la copia de trabajo sobrante, su rama y su carpeta. Queda **una carpeta y una rama**.

**Ya paso antes y costo caro:** habia 3 copias de Foto Informe en el disco y se estuvo
reparando la de mayo. Se curo asi: Julio confirmo cual era la buena, las otras dos se
respaldaron y se borraron (2026-08-20). Este contrato es para que no vuelva a pasar, y ahora
tambien para las ramas, no solo para las carpetas.

---

## LO QUE SE ENCONTRO AL MEDIRLO (2026-09-05, no es opinion)

1. **No existe rama principal.** Ni `main` ni `master`. Todo lo que se guarda desde hace semanas
   va a una rama de trabajo, y nadie lo habia comprobado.
2. **Hay una segunda copia completa del proyecto en el disco** (9,3 MB), parada desde el
   2026-09-01, con **cero** cosas que la copia principal no tenga.
3. **El guardian de la via canonica NO la ve.** Solo comprueba las carpetas registradas; no mira
   ramas, ni copias de trabajo de git. Por eso la segunda version llevaba dias ahi sin que nadie
   se enterara.

---

## LA LEY

**Hay UNA sola via. La misma para abrir y para guardar. Todo lo demas es una version fuera de
la ley y se unifica o se retira.**

### Regla 1 — Una sola carpeta viva por proyecto
Un proyecto tiene UNA carpeta donde se trabaja. Las demas copias solo pueden existir si estan
**declaradas como respaldo congelado**, y entonces no se editan nunca.

### Regla 2 — Una sola rama viva por proyecto
Se guarda SIEMPRE en la rama canonica del proyecto. No se abre una rama nueva para trabajar sin
que Julio lo pida. Si aparece otra rama:
- si **no tiene nada** que la canonica no tenga, se retira;
- si **tiene algo**, se pasa a la canonica ANTES de retirarla, y se le dice a Julio que se paso.

### Regla 3 — Antes de guardar se comprueba donde se guarda
Ningun guardado se da por bueno sin haber comprobado que cae en la via canonica. Guardar en otra
rama o en otra copia es guardar en un sitio que Julio no mira: es trabajo perdido con aspecto de
trabajo hecho.

### Regla 4 — El guardian tiene que mirar las tres cosas
El aviso de via canonica no vale si solo mira carpetas. Tiene que mirar:
- **la carpeta** (donde se trabaja),
- **la rama** (donde se guarda),
- **las copias de trabajo de git** (las que no se ven al abrir la carpeta).

### Regla 5 — Nada se retira a espaldas de Julio
Una copia o una rama sobrante **no se borra sola**. Se le enseña a Julio que no tiene nada
unico, se respalda, y el dice si se retira. Borrar sin enseñar es lo mismo que perder.

---

## A QUIEN PUEDE DANAR

- Al guardian de la via canonica: hay que ampliarlo, no cambiarlo de sitio.
- Al candado que obliga a guardar antes de terminar: ahora ademas tiene que decir **donde**
  quedo guardado.

---

## COMO SE COMPRUEBA QUE SE CUMPLE

Una vigia que, con un proyecto de mentira:
1. crea una segunda rama y comprueba que el aviso **la nombra**;
2. crea una segunda copia de trabajo y comprueba que el aviso **la nombra**;
3. comprueba que el aviso dice **en que rama** se esta guardando, no solo en que carpeta.

**Vigia verde no es prueba.** La prueba es que Julio vea el aviso nombrando la copia sobrante.
