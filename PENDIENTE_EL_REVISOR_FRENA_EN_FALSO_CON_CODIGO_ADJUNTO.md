# PENDIENTE — EL REVISOR FRENA EN FALSO CUANDO EL ENCARGO LLEVA CODIGO ADJUNTO

**Cazado el 2026-09-12 por la noche. Apuntado como freno en falso. NO se reparo.**

## QUE PASO, EN ORDEN

Se le pidio al equipo la vigia que tiene que cazar el objetivo duplicado. El equipo **la APROBO**:

    VEREDICTO: APROBADO
    resumen: Se crea el archivo de vigia pedido con pruebas que cubren el diagnostico, sin
             modificar ni danar codigo existente.

Y aun asi **no se escribio**, porque el revisor de programa la freno con esto:

    - NO HACE LO QUE SE PIDIO: el encargo habla de 'NECESITO_LEER' y esa palabra no aparece
    - NO HACE LO QUE SE PIDIO: el encargo habla de 'TOPE_LETRAS' y esa palabra no aparece
    - NO HACE LO QUE SE PIDIO: el encargo habla de '_sitio_obj' y esa palabra no aparece

**Las tres son falsas.** Esas palabras estan en el **codigo que se adjunto** al encargo para que
el obrero pudiera trabajar. No son cosas que la vigia nueva tenga que contener. El revisor
compara las palabras del encargo entero contra el archivo nuevo, y cuando el encargo lleva codigo
pegado dentro — que es justo lo que manda hacer el candado de memoria — **todas las palabras de
ese codigo se convierten en exigencias falsas**.

## POR QUE ES GRAVE Y NO UN DETALLE

Choca con una regla que el propio sistema obliga a cumplir:

> "NO VUELVAS A mandar al equipo un encargo que nombra renglones de un archivo sin comprobar
> ANTES que ese trozo va adjunto."

O sea: **si adjuntas el codigo como manda una regla, la otra te frena.** Cuanto mejor se prepara
el encargo, mas probable es el freno. Es una trampa que se cierra sola.

Ya esta apuntado en el medidor de frenos en falso: `revisor_de_programa -> (0 cazadas, 1 freno
falso)`. Esa cuenta existe precisamente para esto y llevaba muerta hasta el 11 de septiembre.

## Y ALGO MAS, QUE ES EL COLMO: EL FALLO SE MORDIO A SI MISMO

En ese mismo intento quedo escrito:

    GPT-OSS 120B no le cabe (20762 letras, aguanta 19042) -> se le salta
    GPT-OSS 20B  no le cabe (20762 letras, aguanta 20169) -> se le salta

El encargo para reparar el objetivo duplicado **salio de 20.762 letras y no le cupo a ninguno de
los dos**, por el mismo objetivo duplicado que iba a reparar. Si la reparacion estuviera hecha,
habria cabido en los dos. La averia se defiende sola: bloquea al que viene a arreglarla.

## LO QUE SE PROPONE (pendiente del si de Julio)

Que el revisor mire solo **lo que se pide de nuevo**, no el material adjunto. Lo mas simple y sin
IA: que el encargo separe con una marca clara la parte de "codigo adjunto, esto es material" de la
parte de "esto es lo que tienes que escribir", y que el revisor compare solo contra la segunda.

Es cuenta, no juicio: lo hace un programa gratis.

## LO QUE NO SE HIZO Y POR QUE

No se reparo esta noche: Julio dijo de parar, y tocar el revisor pide paquete y veredicto. Se
apunta con su medicion para que manana no haya que volver a descubrirlo.
