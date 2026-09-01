# DONDE QUEDAMOS — 2026-08-31

Julio: *"cuando todo este terminado, guarda todo, continuamos manana"*.
Esta todo guardado y en verde. Aqui esta lo que hicimos y por donde seguir.

---

## LO QUE SE CERRO HOY (todo con su ley, su candado y su prueba)

Todo lo de hoy es **la misma enfermedad con distintas caras**: el sistema decia
una cosa y hacia otra.

| Lo que decia | Lo que hacia de verdad |
|---|---|
| que buscaba el sitio del codigo | contaba renglones, que se corren solos, y borraba funciones enteras |
| que habia un ayudante disponible | no sabia ni como llamarle, y reventaba al intentarlo |
| que aceptaba la eleccion de revisor | la tiraba a la basura **en silencio** |
| que habia que contestar los recados | no daba ninguna forma de marcarlos como contestados |
| quien mandaba cada recado | los firmaba como "desconocido" y luego bloqueaba con ellos |
| que un fallo estaba protegido | apuntaba una prueba **que no existe** |

Las seis, cerradas.

### 1. El sitio se busca POR NOMBRE, nunca por numero de renglon
- `cerebro/piezas.py::funcion_completa` devuelve la pieza entera buscandola por su nombre.
- El repartidor ya no lleva los numeros 87 y 227 escritos a mano.
- El obrero entrega **texto viejo a texto nuevo**, no un tramo.
- Candado `arnes/candado_por_nombre.py`, enchufado y probado.

### 2. Con quien se trabaja lo dice Julio, y hay quien lo haga cumplir
- `arnes/companero.py`: **un solo sitio** dice quien es el companero.
- Distingue RESERVA (con salida honrada) de RETIRADO (sin ella).
- Candado `arnes/candado_companero.py`, enchufado.

### 3. El equipo dejo de tirar trabajo ya pagado
- Si el revisor contesta roto, **se le vuelve a preguntar**. Antes se tiraba la ronda.
- El informe ya no dice un simple interrogante: dice que el revisor contesto roto.

### 4. Las dos listas ya no se pueden separar — LA CURA DE FONDO DEL DIA
- Habia **dos listas que debian decir lo mismo y nadie comparaba nunca**: una decidia
  quien entra en la fila de cerebros, la otra sabia como llamarle.
- Un nombre entro en la primera sin estar en la segunda: reventaba, el relevo lo contaba
  como un fallo mas, y el ciclo se quedaba **SIN REVISOR**. Todo caia en el de PAGO.
- Ahora la segunda se construye de la **misma fuente** que la primera.
- **El hallazgo fue de Continue.** Fue el mejor diagnostico del dia.

### 5. Se puede elegir de verdad quien escribe y quien revisa
- Lo pesado ya no es fijo: se calcula, para que pedir un cerebro concreto no se lo pise.
- Si no se puede respetar lo pedido, **SE DICE**. Antes se ignoraba callando.
- El que revisa **nunca** puede ser el que escribio.

### 6. El buzon y los recados
- Contestar un recado **lo deja cerrado**, con quien y cuando.
- El sistema **ya sabe quien es quien** (antes firmaba todo como "desconocido").
- El vigilante que llevaba **seis dias muerto** sin que nadie lo notara.

---

## LO QUE HAY QUE DECIDIR MANANA

**Con que ayudante se sigue.** Los numeros de hoy, misma jornada:

| | Cline | Continue |
|---|---|---|
| Trabajos terminados | **4 de 4** | 0 de 1 |
| Comprobados en el codigo | **4** | 1 a medias |
| Dijo hecho sin estarlo | 0 | **3 veces** |
| Rompio algo | nunca | **2 veces el mismo archivo** |

**Recomendacion de Claude:** Cline vuelve a activo para EJECUTAR. Continue solo para
MIRAR Y OPINAR, que ahi acerto mejor que nadie, pero sin escribir mientras su
herramienta diga que guardo sin haber guardado.

Falta que Julio lo decida y que se legisle.

---

## LO QUE FALTA (por orden)

1. **Que Julio lo pruebe con sus ojos.** Vigia verde NO es prueba. Nada de hoy esta
   sellado hasta que el lo vea funcionar.
2. Decidir y legislar lo del ayudante (arriba).
3. La vigia de las 7 puertas del candado de equipo: escrita, nacio roja, apartada.
4. El vigilante que autoriza desde el plan aprobado: legislado, NO construido.
5. Pruebas con navegador del propio Ingeniero: no empezadas.
6. **Foto Informe, paso 6 de 8.** El producto de Julio, parado mientras se afina la
   herramienta. Es lo unico que da dinero: en cuanto la herramienta aguante, va esto.

---

## COMO EMPEZAR MANANA

    cd C:\Ingeniero_VUC; python ingeniero.py arranca

**512 comprobaciones en verde, ninguna roja, todo guardado.**
