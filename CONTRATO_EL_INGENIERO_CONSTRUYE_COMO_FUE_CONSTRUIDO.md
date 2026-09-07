# CONTRATO — EL INGENIERO CONSTRUYE COMO EL FUE CONSTRUIDO

**Julio, 2026-09-07, enfadado y con razon:**

> *"el ingeniero se supone que debe construir todo, eso incluye los candados, la memoria, el
> arnes, los vigias, los skills, los scripts python, los helpers, todo... Se supone que es un
> ingeniero de software."*

> *"Yo di una instruccion clara, que el ingeniero sea capaz de copiar su arquitectura: que
> construyera, como el es construido."*

---

## EL AGUJERO, MEDIDO (2026-09-07)

La capacidad de enchufar el Ingeniero a un proyecto **ya existe** desde el principio: la ley
madre lo dice en su linea 9 (`python arnes/instalar.py <apodo>`). Pero al mirar QUE instala:

| Lo que `instalar.py` deja hoy en un proyecto | |
|---|---|
| Un aviso en `CLAUDE.md` | texto |
| Un recordatorio en `.claude/rules/` | texto |
| El candado de LECTURA en `.claude/settings.json` | **el unico que frena** |

Su propio comentario lo dice con todas las letras: *"Deja en el proyecto tres cosas, **sin tocar
su codigo**"*.

**No instala la arquitectura. Instala una nota.**

Y el resultado se ve en DMM:

| El arnes de DMM | Estado real medido |
|---|---|
| `arnes/edit_gate.py` (su candado de edicion) | escrito y **NO enganchado** |
| `arnes/recordatorio_arranque.py` | escrito y **NO enganchado** |
| `hooks/pre-commit` | escrito y **NO instalado** |
| `.claude/settings.json` | **`{}` vacio** |

DMM tiene candados escritos que **nunca se disparan**. Es la misma enfermedad que esta casa ya
tiene diagnosticada: *una ley escrita sin disparador no se cumple*. Solo que aqui le pasa al
proyecto que el Ingeniero tenia que haber construido.

---

## LAS CINCO RESPUESTAS

| | |
|---|---|
| **QUE** | que `instalar.py` **construya** la arquitectura en el proyecto, no que deje un aviso |
| **DONDE** | `arnes/instalar.py` del Ingeniero. Lo construido vive **dentro del proyecto**, suyo |
| **COMO** | genera para el proyecto sus propias piezas y **las engancha**; y comprueba que quedaron enganchadas |
| **POR QUE ASI** | se descarto **prestarle** las piezas del Ingeniero: eso crea dependencia de EJECUCION y Julio la prohibio expresamente. Y se descarto dejarlo en un aviso: es lo que hay hoy y no frena nada |
| **CUANDO** | ahora. Cada dia que pasa, el proyecto se construye sin red |

---

## LA LEY

### Regla 1 — Construir, no avisar
Enchufar un proyecto **no es dejarle un texto**. Es dejarle piezas que **funcionan y frenan**.
Si al terminar la instalacion nada frena, la instalacion **no se hizo**.

### Regla 2 — Lo construido es DEL PROYECTO, no prestado
Todo lo que se instala vive **dentro del proyecto** y le pertenece. El proyecto tiene que seguir
funcionando aunque la carpeta del Ingeniero desaparezca del disco.

**El Ingeniero CONSTRUYE el proyecto. El proyecto NO depende del Ingeniero para funcionar.**
La primera relacion se quiere; la segunda esta prohibida (Julio, 2026-09-07).

### Regla 3 — Lo que se instala
Como esta construido el Ingeniero, asi construye:

| Pieza | Que es |
|---|---|
| **arnes** | los candados del proyecto, en su carpeta |
| **enganches** | lo que hace que esos candados se disparen de verdad |
| **memoria** | donde el proyecto guarda su estado y sus fallos, para no repetirlos |
| **vigias** | las pruebas que protegen lo que se construye |
| **skills / scripts / helpers** | lo rutinario, programado y no pedido a la IA |
| **mapa** | el inventario de sus piezas, que se regenera |

### Regla 4 — No se pisa lo que el proyecto ya tiene
Si el proyecto **ya tiene** su candado de edicion (como DMM), **no se le escribe otro**: se
**engancha el suyo**. Duplicar es el fallo que esta casa mas persigue. Primero se busca en su
mapa; solo lo que falte se construye.

### Regla 5 — Se comprueba que quedo enganchado, no que quedo escrito
Al terminar, la instalacion **verifica y dice** cuantos candados quedaron **disparandose**. Un
candado escrito y no enganchado cuenta como **NO instalado**, y se dice asi.

---

## A QUIEN PUEDE DANAR

- `arnes/instalar.py` — cambia de raiz lo que hace.
- Los proyectos ya enchufados: al reinstalar les aparecen enganches que antes no tenian. Es lo
  que se busca, pero **hay que decirlo antes**, no despues.
- `--quitar` tiene que seguir dejando el proyecto **como estaba**. Si instalar construye mas,
  desinstalar tiene que saber retirar mas.

## COMO SE COMPRUEBA QUE SE CUMPLE

Una vigia que, sobre un proyecto de mentira:
1. instala y comprueba que **hay al menos un candado enganchado que de verdad frena**;
2. comprueba que el proyecto **sigue arrancando** si se borra la carpeta del Ingeniero (Regla 2);
3. le pone al proyecto un candado propio ANTES de instalar y comprueba que **no se le escribe
   otro encima**: se engancha el suyo (Regla 4);
4. comprueba que `--quitar` lo deja **igual que estaba**;
5. comprueba que el informe final dice **cuantos quedaron enganchados**, no cuantos escritos.

**Vigia verde no es prueba.** La prueba es que Julio toque DMM y le salte un candado de DMM.
