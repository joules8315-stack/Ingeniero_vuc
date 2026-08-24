# CONTRATO — COMO SE PIDEN LAS CREDENCIALES PARA UNA PRUEBA REAL

> Fecha: 2026-08-22 · Proyecto: Ingeniero VUC (vale para TODOS los proyectos) · Estado: LEY
>
> Julio, textual:
> **"abre la variable de entorno en ps, yo pongo las credenciales, abre de manera segura, de
> alli en adelante trabajas tu. Legisla, y guardalo como metodo de trabajo, siempre"**

---

## 1. EL METODO. UNA SOLA FORMA, SIEMPRE

Cuando una prueba real necesite entrar a un sitio con correo y contrasena:

**PASO 1 — Se le ABRE la ventana. No se le explica, se le abre.**
```powershell
Start-Process rundll32.exe -ArgumentList "sysdm.cpl,EditEnvironmentVariables"
```

**PASO 2 — Se le dice EXACTAMENTE que escribir, en dos lineas y nada mas:**
```
   Nombre : <NOMBRE_DE_LA_VARIABLE>
   Valor  : la contrasena
```
Se le indica el cuadro **de arriba** (Variables de usuario) y el boton **Nueva...**. Nada mas.

**PASO 3 — Julio escribe. Ahi termina su parte.**

**PASO 4 — De ahi en adelante trabaja el Ingeniero.** Lee la credencial del usuario de Windows
y se la pasa al proceso, sin mostrarla:
```powershell
$env:LA_VARIABLE = [Environment]::GetEnvironmentVariable("LA_VARIABLE","User")
```

## 2. LO QUE NUNCA SE HACE

- **NUNCA se le pide una clave por el chat.** Ni se escribe, ni se repite, ni se enseña.
- **NUNCA se escribe una clave dentro de un archivo del proyecto.** Ahi es donde acaban
  subidas a internet: ya paso en Foto Informe.
- **NUNCA se le suelta a Julio un bloque de ordenes largo para que lo entienda.** Julio no es
  tecnico y lo ha dicho con enojo. Se le ABRE la ventana y se le dicen DOS lineas.
- **NUNCA se le pide dos veces lo mismo.** Si no aparece, se mira en el usuario, en la maquina
  y con otros nombres ANTES de volver a molestarle.

## 3. POR QUE ESTA LEY EXISTE (lo que costo el 2026-08-22)

Se le pidio la misma credencial **cuatro veces**. Cada vez con un bloque de ordenes distinto
que el no entendia. Julio contesto "listo" dos veces y la clave no estaba, porque la habia
escrito en SU ventana y el Ingeniero trabaja en otra: **una variable escrita en una ventana no
la ve nadie mas**. Eso no se le explico a tiempo.

Ademas se le ofrecio "crear una cuenta nueva" cuando la que habia ya era de pruebas, y se le
hizo perder mas tiempo todavia. Julio: *"no entiendo un puto culo"*, *"busca otra puta forma"*.

**La leccion:** cuando algo depende de que Julio haga algo tecnico, **el trabajo es del
Ingeniero, no suyo**. Lo unico suyo es escribir el dato en un hueco que ya esta abierto delante.

## 4. LO QUE SE HACE AL TERMINAR

- Se le ofrece **borrar** la credencial guardada. No se deja una clave viviendo en su Windows
  para siempre sin decirselo.
- Se **borran las que ya no sirven**. El 2026-08-22 habia un pase de entrada caducado ahi
  guardado que no valia para nada.

```powershell
[Environment]::SetEnvironmentVariable("LA_VARIABLE", $null, "User")
```

## 5. COMO SE COMPRUEBA QUE ESTA LEY SE CUMPLE

`vigias/test_vigia_credenciales_se_piden_bien.py`:

1. Ninguna prueba real trae una clave escrita dentro.
2. Toda prueba real lee sus credenciales del entorno, nunca de un archivo del proyecto.
3. Toda prueba real, si le faltan, **lo dice claro y para**: nunca sigue a medias ni las inventa.
