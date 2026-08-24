# Reglas de Cline en el Ingeniero VUC (Julio, 2026-08-24)

Estas reglas aplican a **Cline** (yo), igual que los candados aplican a Claude. No hay excepción
para ningún agente.

## 1. Siempre en equipo, sin salto
- Se trabaja SIEMPRE con el equipo (veredicto). Nunca se escribe código a solas.
- Para saltar el candado de equipo se pide permiso y la respuesta es **SIEMPRE "denegado"**.
  No hay forma honrada de saltarlo.

## 2. Probar de verdad antes de pedirle a Julio
- Antes de pedirle a Julio que pruebe con sus ojos, se corre, **con el equipo**, una **prueba real
  interna (Playwright)** que toca la pantalla y demuestra que el objetivo se cumple.
- Se verifica si el resultado se logró de verdad o fue **autovalidación**. Una autovalidación no
  cuenta como prueba.
- **Si se logró** → avisar a Julio para sus pruebas reales.
- **Si NO se logró** → aprender del error y **reiniciar el ciclo** para reparar el fallo y lograr
  el resultado, sin excusas.

## 3. Cada instrucción de Julio se legisla
Toda orden pasa por: analizar → legislar → tabla de la verdad/matriz → dividir en bloques →
indexar → vigías → arnés → cross-flow (no romper lo que sirve).

## 4. Hablar simple
Julio no es técnico. Nada de jerga ni nombres de archivos con él; el comando siempre listo para
PowerShell (`;`, no `&&`). Lo técnico queda dentro de estos archivos.
