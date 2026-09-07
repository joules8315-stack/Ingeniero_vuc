# CONTRATO — EL INVENTARIO PARA UNA SEGUNDA OPINION

**Julio, 2026-09-07:**

> *"necesito me des esta información urgente, para pedir una segunda opinión y crear un plan
> para crear DMM"*

Y su condicion, literal:

> *"no quiero que el equipo rellene esto a mano inventando estados. Si pueden generarlo
> automáticamente desde el repositorio, mejor. Las afirmaciones como 'esto existe' deben poder
> rastrearse hasta un archivo, función, contrato, test o commit."*

---

## LAS CINCO RESPUESTAS

| | |
|---|---|
| **QUE** | una pieza que LEE un proyecto entero y escribe un inventario en la forma exacta que pidio Julio, para que otro pueda auditarlo sin tener el disco delante |
| **DONDE** | `mapa/auditoria_proyecto.py` del Ingeniero VUC. El resultado va a `memoria/auditorias/<APODO>_AUDITORIA_PROYECTO.json`, **fuera** del proyecto auditado |
| **COMO** | reusando el censo que YA existe (`cerebro/grafo.py`: piezas, enlaces, flujos) y anadiendole lo que el censo no mira: git, duplicados por contenido y recuento de pruebas. Nada se escribe de memoria: todo sale de leer |
| **POR QUE ASI Y NO DE OTRO MODO** | se descarto **(a)** que el equipo lo rellenara a mano — es justo lo que Julio prohibio, y ademas lo rellenaria inventando; y **(b)** hacer un censo nuevo — ya hay uno probado y duplicarlo va contra la ley de no crear piezas repetidas |
| **CUANDO** | ahora. Julio lo pidio urgente para pedir una segunda opinion y armar el plan de DMM |

---

## LA LEY

### Regla 1 — Solo lectura, y por escrito
Al proyecto auditado **se le lee y nada mas**: no se modifica, no se crea, no se borra, no se
hace commit. El informe se escribe **fuera**, en la carpeta del Ingeniero. Si el informe se
escribiera dentro, la propia auditoria ensuciaria lo auditado.

### Regla 2 — Lo que no se puede comprobar leyendo, no se rellena
Todo campo que exija correr, llamar o preguntar sale como **`no_verificado`**, nunca vacio a
secas y nunca adivinado. Es la Ley 2 de Julio (nunca inventar) aplicada a un informe.

### Regla 3 — Cada afirmacion lleva su rastro
Al lado de cada cosa dudosa va un campo **`_como_se_sabe`** que dice de donde salio: la ruta
del archivo, la funcion con su linea, el commit, o la razon por la que no se puede saber.
Un informe sin rastro no se puede auditar: solo se puede creer.

### Regla 4 — Leer no es probar
Ningun archivo entra en `funciona` por haberlo leido. `estado_funcional.funciona` solo se
llena **corriendo** las pruebas y la prueba real. Hasta entonces todo el codigo esta como no
verificado. Es la Ley 3 de Julio: vigia verde no es prueba.

### Regla 5 — Ni un secreto en el informe
Antes de escribir nada se pasa el detector que ya protege lo que se manda a la nube
(`cuerpo/privacidad.py`). Si un archivo huele a secreto, se dice **cual archivo** y **cuantos**,
y **jamas el valor**. Un informe que se comparte con otro es exactamente el sitio donde una
clave se escapa.

### Regla 6 — La integridad se mide, no se opina
Julio pidio detectar *"versiones paralelas, código huérfano, duplicaciones, contratos que se
contradicen, candados que no se ejecutan y componentes que el equipo cree que existen pero
realmente no funcionan"*. De esa lista:

| Lo que pidio | Como se responde |
|---|---|
| duplicaciones | **se mide**: misma huella del contenido = copia identica |
| rutas paralelas | **se mide**: mismo nombre de archivo en dos sitios |
| funciones duplicadas | **se mide** por nombre, y se dice que **no** se comparo el cuerpo |
| candados que no se ejecutan | **se listan** los que existen; si estan enganchados no se sabe leyendo, y se dice |
| contratos que se contradicen | **no se afirma**: comparar dos leyes es leerlas enteras. Se entrega la lista para que la segunda opinion lo juzgue |
| componentes que se creen que existen | **se responde solo con `existe`** = hay un archivo que lo respalda. Nunca con `funciona` |

**No se rellena un juicio con una medida.** Que dos archivos tengan el mismo nombre es un dato;
que sean un conflicto es una opinion, y la opinion la pone quien audita, no el recolector.

### Regla 7 — El esquema lo manda Julio
El informe sale con **estas llaves y en este orden**, aunque alguna vaya vacia. Si falta una,
el informe esta mal aunque el contenido sea bueno: quien lo audita espera esta forma.

```
proyecto · reglas_de_recoleccion · estructura_proyecto · arquitectura · dos_cerebros ·
agentes · skills · mcp · plugins · herramientas · memoria · motor_dmm · flujos · leyes ·
contratos · candados · arneses · guardas · tablas_de_verdad · matrices · ontologia ·
versionado_y_canon · duplicacion_y_conflictos · pruebas · rendimiento · costos · seguridad ·
estado_funcional · deuda_tecnica · objetivos_futuros · preguntas_abiertas · resumen_equipo
```

Dentro de cada llave, los campos que pidio Julio:

- **proyecto**: nombre, version, fecha_recoleccion, repo_canonico, branch_actual, commit_actual,
  commit_base_conocido, estado_actual, objetivo_del_mvp.
- **reglas_de_recoleccion**: no_modificar_codigo, no_crear_archivos, no_hacer_commit,
  no_eliminar_nada, solo_lectura, incluir_archivos_relevantes, excluir_secretos,
  excluir_credenciales, excluir_tokens_api, incluir_rutas_completas_de_archivos.
- **estructura_proyecto**: arbol_directorios, archivos_totales, y las listas archivos_codigo,
  archivos_configuracion, archivos_documentacion, archivos_pruebas, archivos_contratos,
  archivos_leyes, archivos_memoria, archivos_skills, archivos_agentes, archivos_harness,
  archivos_guardas, archivos_indice.
- **arquitectura**: frontend (tecnologia, ruta, entrypoints, paginas, componentes_principales),
  backend (tecnologia, ruta, entrypoints, apis, servicios, workers), base_datos (tecnologia,
  tablas, relaciones, indices, politicas), servicios_externos, modelos_ia (nombre, proveedor,
  uso, local_o_nube, costo, entrada, salida).
- **dos_cerebros**: ingeniero_software, dmm_marketing y kernel_compartido, cada uno con existe,
  archivos, agentes, roles, skills, herramientas, flujo, entrada, salida.
- **agentes**: nombre, archivo, rol, objetivo, modelo, herramientas, skills, entrada, salida,
  memoria, puede_decidir, puede_ejecutar, puede_modificar_codigo, puede_hacer_commit, estado.
- **skills**: nombre, archivo, objetivo, prompt_o_logica, herramientas, entrada, salida,
  validaciones, memoria_utilizada, agente_que_la_invoca, estado.
- **mcp / plugins / herramientas**: nombre, funcion, quien lo usa, costo, estado.
- **memoria**: arquitectura_general, rag, memoria_fragmentada, indice_canonico, grafo,
  memoria_de_razonamiento, memoria_de_evidencia, memoria_de_hipotesis, cache_semantica.
- **motor_dmm**: perfil_empresa, voz_marca, perfilador_cliente, productos_servicios,
  competencia, entorno_digital, recoleccion_datos, analitica, estrategia, campanas, contenido,
  publicacion, ventas, aprendizaje.
- **flujos**: nombre, objetivo, trigger, pasos, agentes, skills, herramientas, entradas,
  salidas, validaciones, guardas, candados, harness, commit, estado.
- **leyes / contratos / candados / arneses**: nombre, archivo, que hace, y su estado.
- **guardas**: entrada, salida, cross_flow, codigo, memoria, commit.
- **versionado_y_canon**: rama_canonica, commits_recientes, tags, branches, reglas_de_commit,
  proteccion_contra_versiones_huerfanas, fuente_de_verdad.
- **duplicacion_y_conflictos**: archivos_duplicados, funciones_duplicadas, skills_duplicadas,
  contratos_conflictivos, leyes_conflictivas, rutas_paralelas, versiones_paralelas.
- **pruebas**: frameworks, cantidad_total, tests_pasando, tests_fallando, tests_omitidos,
  tests_e2e, tests_integracion, tests_unitarios, tests_de_regresion, playwright.
- **rendimiento / costos / seguridad / estado_funcional / deuda_tecnica / objetivos_futuros /
  preguntas_abiertas / resumen_equipo**: tal como los escribio Julio.

### Regla 8 — `resumen_equipo` se queda vacio a proposito
Esa llave es opinion del equipo, no lectura del repositorio. **El recolector no la rellena.**
Rellenarla desde aqui seria exactamente lo que Julio prohibio.

---

## A QUIEN PUEDE DANAR

- A `cerebro/grafo.py`: se le pide el censo con `forzar=True`, o sea que lo recalcula. Solo lee.
- A nadie mas: la pieza es nueva y nadie la importa todavia.

---

## COMO SE COMPRUEBA QUE SE CUMPLE

Una vigia que:
1. corre el recolector sobre un proyecto de mentira y comprueba que **estan las 32 llaves**;
2. comprueba que **no se creo ni se modifico ningun archivo** dentro del proyecto auditado;
3. le mete un secreto de mentira a un archivo y comprueba que **el valor no aparece** en el informe;
4. comprueba que `estado_funcional.funciona` sale **vacio** aunque el codigo este sano
   (leer no es probar);
5. comprueba que un bloque sin archivos que lo respalden sale con `existe: false` y con su
   `_como_se_sabe`, y **nunca** con datos inventados.

**Vigia verde no es prueba.** La prueba es que Julio mande el informe, le den una segunda
opinion, y esa opinion no tenga que preguntarle nada que estuviera en el disco.
