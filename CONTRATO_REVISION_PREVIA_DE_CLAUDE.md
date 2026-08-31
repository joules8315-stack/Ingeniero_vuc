# CONTRATO_REVISION_PREVIA_DE_CLAUDE.md

Julio, 2026-08-31.

## LA LEY (lo que Julio pidio, textual y simple)

> "Necesito que legisles sobre esto: Debes pasarle todo lo que va a hacer a Claude para que revice
> y apruebe, me lo estas dejando [en el chat] y yo no se ni mierda de codigo."

## QUE PROHIBE

**Ninguna IA que trabaje en este proyecto toca CODIGO (o creado de vigias/contratos) sin pasar
PRIMERO por la revision de Claude.** En concreto:

1. **No se escribe, modifica ni repara un archivo de codigo** (ni una vigia, ni un candado, ni un
   contrato) sin que primero se le EXPONGA a Claude QUÉ se va a hacer, DÓNDE, POR QUÉ y CÓMO, y
   Claude lo haya APROBADO por el canal.

2. **Si Claude no lo revisa y aprueba, no se toca.** Un trabajo sin el visto bueno de Claude se
   considera NO aprobado y no se guarda ni se commitea.

3. El flujo obligatorio es:
   ```
   1. la IA dice a Claude por el canal: QUÉ piensa hacer, DÓNDE, POR QUÉ y CÓMO.
   2. Espera la respuesta de Claude (APROBADO o RECHAZADO con motivos).
   3. Solo si Claude APRUEBA, se toca el codigo.
   4. Al terminar, se le dice a Claude QUÉ se hizo, DÓNDE, POR QUÉ y CUÁNDO (para su supervision).
   ```

## POR QUE EXISTE

El 2026-08-31 Continue toco `arnes/candado_buzon.py` por su cuenta y lo dejo a medias, y Julio,
que NO sabe de codigo, no podia saber si estaba bien o roto. Eso es inaceptable: una IA que se
cree con derecho a tocar el tallere sin que Julio o el compañero supervisor lo vean.

## QUE NO ES ESTA LEY

- No es "no trabajar": es "no trabajar a ciegas".
- No quita autonomia para PROYECTAR: la IA puede investigar, pensar y proponer todo lo que quiera;
  solo no puede EJECUTAR sobre el codigo hasta que Claude apruebe.
- No reemplaza a Julio: Julio sigue mandando; lo que cambia es que la IA no le mete mano al codigo
  por su cuenta.

## DONDE SE LEE

Esta es la regla que manda. Se apunta en el protocolo, se pone una vigia que FREne un toque de
codigo no aprobado, y se le avisa a Claude por el canal para que la conozca.
