# DONDE QUEDAMOS — cierre del 2026-08-21

> Julio: **"guarda todo para manana"**.
> Esto es lo primero que hay que leer al volver. No hace falta que Julio cuente nada otra vez.

---

## LO PRIMERO QUE HAY QUE HACER MANANA (por orden)

**1. Julio corre la prueba integral de Foto Informe.** Es lo unico que falta para poder guardar
la reparacion. Su propio arnes la exige y la ultima verde es de hace un mes.

Ventana 1, el motor:
```powershell
cd "C:\Users\USER\dev\Foto_info_repo\Foto_informe--main"; .\start_backend_8000.bat
```

Ventana 2, la prueba (la clave nunca se ve ni se guarda):
```powershell
cd "C:\Users\USER\dev\Foto_info_repo\Foto_informe--main"
$env:FOTO_INFORME_TEST_EMAIL = "tu-correo-de-PRUEBA"
$s = Read-Host "Clave de la cuenta de PRUEBA (no se vera)" -AsSecureString
$b = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)
$env:FOTO_INFORME_TEST_PASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringAuto($b)
[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($b)
.\.venv\Scripts\python.exe rv3_prueba_integral.py
.\.venv\Scripts\python.exe rv3_prueba_real_velocidad.py
```

**2. Con esa verde, se guarda la reparacion de Foto Informe** (hoy quedo preparada pero el arnes
la retuvo).

**3. Julio lo ve con sus ojos.** Vigia verde NO es prueba. Abre Foto Informe, toma fotos con el
celular con el informe abierto en el computador, y comprueba que aparecen y que la pantalla
responde de una vez.

---

## LO QUE QUEDO HECHO HOY

### Foto Informe — las 4 fugas de velocidad, tapadas (SIN GUARDAR todavia)
Lo escribio DeepSeek, lo audito otro cerebro distinto (caza una variable fuera de sitio que
habria tumbado la pantalla), y se comprobo renglon a renglon antes de aplicar.

1. **Guardar ya no borra la memoria entera.** Olvida solo lo que ese guardado toca. Los otros
   tres sitios que si borran todo se quedan igual (al entrar, al salir, al pedir limpiar).
2. **El reloj corre solo en la pantalla de las fotos, cada 5 segundos.** En las demas, cero.
   Antes despertaba cada 12 segundos en todas, se mirara o no.
3. **Con la ventana escondida no llama.** Al volver, revive solo si estas en la de fotos.
4. **Leer espera 10 segundos** en vez de 25. Guardar, subir (60 s) y generar (120 s) NO se
   tocaron: acortarlas cortaria un guardado y Julio perderia el borrador.

**Comprobado:** la vigia nacio ROJA con 6 fallos antes de tocar y quedo verde. 19 vigias verdes.
El codigo de la pantalla sigue siendo valido (comprobado aparte: un error ahi la dejaria en
blanco sin avisar).

**COPIA DE SEGURIDAD** (por si algo se pierde), en `memoria/rescate/`:
- `foto_informe_velocidad_2026-08-21.patch` — el cambio entero, se puede volver a aplicar
- `app_web_reparada_2026-08-21.html` — la pantalla ya reparada
- la vigia y la prueba de navegador, copiadas tambien

### El taller — GUARDADO (punto de reparacion `c3f65a8`)
- **Lo pesado siempre lo hace DeepSeek.** Generar va a el; auditar sigue gratis. Repartir por
  tamano no bastaba: tres veces el mismo dia los gratis se rindieron por debajo del tope.
- **La libreta del candado, al reves:** ahora apunta cada vez que FRENA, con el motivo.
- **Los 51 fallos ya avisan de verdad.** Habia 24 mudos y otros 7 con el aviso escrito como
  frase (que no coincide con nada). Cero mudos ahora.
- **Las llaves, protegidas.** El archivo de llaves estaba sin proteger.
- 250 vigias verdes.

---

## LO QUE ESTA PENDIENTE Y ES DECISION DE JULIO

**1. Las credenciales estan dentro del repositorio de Foto Informe Y SUBIDAS a internet.**
Comprobado: estan en la rama principal y en la rama de trabajo. El repositorio parece privado
(no responde a quien no tenga permiso), asi que no esta a la vista de cualquiera. Pero **esta en
el historial**: borrar el archivo hoy no lo quita. Hay que reescribir el historial, y eso es
delicado. **No se ha tocado nada.** Se trata aparte, con su ley y su prueba.

**2. El aviso de fallos no distingue** entre cometer un fallo y trabajar sobre el propio
registro de fallos. Freno varias veces al escribir su propia ley. No es grave, pero es el mismo
patron que ya esta apuntado dos veces (un candado que depende de lo que protege).

**3. Hay una copia congelada de Foto Informe** en el Escritorio de OneDrive, declarada como
respaldo. No se toca. Si algun dia se abre esa por error, se estaria reparando la equivocada.

---

## LO QUE JULIO DIJO HOY Y NO SE OLVIDA

- "el equipo que haga siempre lo pesado deepseek, no lo olvides nunca" — **ya es ley del codigo**
- "repara usando tu equipo, ellos reparan, tu vigilas, no seas tonto"
- "que todo quede en un commit, cosa que si lo danan, se pueda reparar"
- "siempre protegiendo contrasena" — nunca se pide ni se escribe una clave por el chat
- Trabaja **mixto**: fotos desde el celular, informe desde el computador, a la vez
- "que haga solo las llamadas que necesite, nada mas, en el tiempo que necesite"
