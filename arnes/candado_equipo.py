# -*- coding: utf-8 -*-
"""arnes/candado_equipo.py — NO SE ESCRIBE CODIGO A SOLAS. SIEMPRE EL EQUIPO.

Julio, 2026-08-21, despues de tener que repetirlo otra vez:
  "pon candado de modo que siempre tengas que trabajar con equipo, y vigias para el arnes, que
   te frene cuando no lo hagas."
  "pon candado para que siempre actues con equipo, modo ingeniero y economico, sin excusa."
  "por no trabajar en equipo ya has gastado 19."

EL AGUJERO QUE TAPA: la regla estaba escrita, en la memoria y en el protocolo, y aun asi se
escribio a solas un guardia entero, tres vigias y cuatro reparaciones. Escrito no es cumplido.
Julio lo pago de su bolsillo. Una regla que depende de que yo me acuerde NO es una regla.

LO QUE EXIGE: para tocar CODIGO tiene que haber un veredicto del equipo RECIENTE que cubra ese
archivo. Uno genera, OTRO distinto audita (4 ojos: nadie se aprueba a si mismo).

  cd C:\\Ingeniero_VUC; python ingeniero.py equipo <proyecto> "<la tarea>"

LO QUE NO ESTORBA (o el candado se vuelve un muro y se acaba apagando, que es peor):
  · los documentos .md          — escribir la ley no es programar
  · archivo nuevo que no existe — crear no es reescribir
  · el propio arnes             — si el candado se rompe, hay que poder arreglarlo

FORTALECIDO (Julio, 2026-08-21): ya NO se deja pasar cuando no hay cerebros. Antes, si los
cerebros estaban agotados, se podia escribir a solas (quedaba apuntado en SIN_EQUIPO.log) y eso
dejaba a foto_informe y a cualquier proyecto SIN VIGILAR. Ahora SIEMPRE se exige el veredicto del
equipo para tocar codigo; si no hay, se BLOQUEA y Julio decide si aprueba. No se escribe a solas,
jamas, en ningun proyecto.

LA LIBRETA, AL REVES (Julio, 2026-08-21): antes se apuntaba lo que se COLABA sin equipo. Con la
puerta de escape cerrada ya no se cuela nada, asi que esa libreta se quedaria vacia para siempre
y no serviria de nada (medido: el archivo no llego a existir NUNCA). Ahora se apunta lo
contrario: CADA VEZ QUE EL CANDADO FRENA. Queda el dia, la hora, el archivo y por que se freno.
Asi Julio ve al final de la semana cuantas veces hubo que pararse y por que, en vez de creerselo.

INVIOLABLE no es que no haya salida: es que TODO deje rastro. La salida a mano sigue siendo suya
(INGENIERO_OFF) y hay una vigia que comprueba que nunca se la quiten.
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "arnes"))  # para importar autorizacion.py (Julio, 2026-08-24)

VEREDICTO = os.path.join(AQUI, "memoria", ".veredicto_equipo.json")
SIN_EQUIPO = os.path.join(AQUI, "memoria", "SIN_EQUIPO.log")
VIGENCIA_MIN = 90          # un veredicto vale hora y media: lo que dura una tanda de trabajo
CODIGO = (".py", ".js", ".html", ".ts", ".jsx", ".tsx", ".css", ".sql")


def _es_temporal(p):
    """¿Es un borrador temporal? En PRODUCCION NO hay exencion temporal: fuera de la casa siempre
    se exige veredicto (Julio, 2026-09-02: la IA no escribe codigo a solas en ningun lado).

    La exencion SOLO existe para la prueba, desviada con INGENIERO_TEMP_TEST: asi la vigia mide
    que el candado sabe distinguir un borrador sin abrirle a la IA una puerta real de salida."""
    ov = os.environ.get("INGENIERO_TEMP_TEST", "").strip()
    if ov:
        return p.lower().startswith(ov.replace("\\", "/").lower())
    return False


def _ruta_veredicto():
    return os.environ.get("INGENIERO_VEREDICTO_TEST") or VEREDICTO


def _ruta_sin_equipo():
    return os.environ.get("INGENIERO_SIN_EQUIPO_TEST") or SIN_EQUIPO


def _fallos_mecanicos(tarea, archivos=None):
    """EL OJO 2 (Julio, 2026-09-08). Antes de guardar la llave, un PROGRAMA mira lo mecanico.

    POR QUE AQUI: el trabajo del equipo ya esta guardado en disco cuando se llama a esta
    funcion, asi que se puede leer sin pedirselo a nadie. Y aqui es donde se decide si se abre
    la puerta de escribir: si el programa encuentra un fallo mecanico, la puerta NO se abre.

    NACE DE DOS FALLOS MEDIDOS ESE DIA, los dos con DOS cerebros delante y ninguno los vio:
      · el equipo entrego codigo que reventaba en la primera linea (usaba re sin importarlo) y
        lo aprobo un auditor DISTINTO con confianza alta;
      · y un auditor rechazo un cambio bueno diciendo que tres nombres no existian: se
        comprobo en el codigo y los tres SI existian.
    Las dos cosas son CUENTAS, no juicios. Un programa las responde en un segundo y sin fallar.

    NO SUSTITUYE AL AUDITOR DE IA: el juicio (si esta bien pensado, si rompe a un vecino) sigue
    siendo suyo y sigue siendo obligatorio. Esto solo anade un freno mas, gratis.

    NUNCA lanza: si no se puede comprobar, se deja todo exactamente como estaba.
    """
    try:
        sys.path.insert(0, os.path.join(AQUI, "arnes"))
        import revisor_de_programa as _rp
        ruta = os.path.join(AQUI, "memoria", "ULTIMO_TRABAJO_DEL_EQUIPO.json")
        if not os.path.exists(ruta):
            return []
        with open(ruta, encoding="utf-8") as f:
            guardado = json.load(f)
        prop = guardado.get("propuesta") if isinstance(guardado, dict) else None
        if not isinstance(prop, dict):
            return []
        # QUE SEA EL TRABAJO DE ESTA RONDA, NO EL DE OTRA (Julio lo cazo el 2026-09-08:
        # "esto no se convertira en otro problema por buscar atajos?"). Ese archivo se PISA en
        # cada ronda: si se leyera el de una ronda anterior, se estaria juzgando un trabajo que
        # no es, y eso seria un fallo nuevo y de los feos. Por eso se comprueba que el archivo
        # que toca la propuesta guardada sea uno de los que este veredicto abre. Si no cuadra,
        # no se juzga nada.
        suyo = str(prop.get("archivo") or "").replace("\\", "/").split("/")[-1]
        de_ahora = [str(a).replace("\\", "/").split("/")[-1] for a in (archivos or [])]
        if not suyo or (de_ahora and suyo not in de_ahora):
            return []
        return _rp.revisar(prop, tarea) or []
    except Exception:
        return []       # si no se puede comprobar, no se estorba


def guardar_veredicto(tarea, archivos, obrero, auditor, veredicto):
    """Lo llama `ingeniero.py equipo` cuando el equipo termina. Es la llave."""
    fallos_del_programa = _fallos_mecanicos(tarea, archivos) if veredicto == "APROBADO" else []
    if fallos_del_programa:
        # El programa caza lo que a las IA se les escapa. La llave NO se guarda.
        sys.stderr.write("\nEL REVISOR DE PROGRAMA FRENA (gratis, sin ninguna IA):\n")
        for f in fallos_del_programa:
            sys.stderr.write("   - %s\n" % f)
        sys.stderr.write("NO se abre la puerta de escribir. El trabajo queda guardado.\n")
        veredicto = "RECHAZADO_POR_EL_PROGRAMA"
    d = {"cuando": time.time(), "tarea": tarea, "archivos": list(archivos or []) if veredicto == "APROBADO" else [],
         "obrero": obrero, "auditor": auditor, "veredicto": veredicto,
         "reviso_a_si_mismo": (obrero == auditor),
         "fallos_del_programa": fallos_del_programa}
    os.makedirs(os.path.dirname(_ruta_veredicto()), exist_ok=True)
    json.dump(d, open(_ruta_veredicto(), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # EL CUADERNO DEL EQUIPO (Julio, 2026-09-02, preguntandolo por tercera vez: "que pasa con el
    # equipo, que no lo veo trabajando?"). Y tenia razon aunque el equipo SI trabajase: el
    # veredicto de arriba se SOBRESCRIBE en cada trabajo, asi que solo sobrevivia el ultimo. De
    # diez reparaciones aprobadas en un dia quedaba rastro de UNA. Julio tenia que creerme en vez
    # de mirarlo, que es justo lo que no quiere.
    # La ruta va ABSOLUTA: una relativa depende de desde donde se lance y falla en silencio.
    try:
        _cuaderno = os.environ.get("INGENIERO_BALANCE_EQUIPO") or os.path.join(AQUI, "memoria", "TRABAJOS_DEL_EQUIPO.log")
        os.makedirs(os.path.dirname(_cuaderno), exist_ok=True)
        with open(_cuaderno, "a", encoding="utf-8") as f:
            fecha = time.strftime("%Y-%m-%d %H:%M", time.localtime(d["cuando"]))
            archivos_txt = ", ".join(os.path.basename(str(a)) for a in list(archivos or [])[:3])
            trozos = [fecha, "escribio " + obrero, "reviso " + auditor, veredicto, archivos_txt,
                      "abre puertas" if veredicto == "APROBADO" else "NO abre puertas"]
            if obrero == auditor:
                trozos.append("se reviso a si mismo: hay que comprobarlo con los ojos")
            f.write(" | ".join(trozos) + "\n")
    except Exception:
        pass    # dejar constancia es la prueba, pero no puede tumbar el trabajo
    return d


def veredicto_vigente():
    """El veredicto del equipo si sigue fresco, o None."""
    try:
        d = json.load(open(_ruta_veredicto(), encoding="utf-8"))
    except Exception:
        return None
    if (time.time() - float(d.get("cuando", 0))) > VIGENCIA_MIN * 60:
        return None
    return d


def cubre(d, fp):
    """¿El veredicto es una APROBACION REAL de ESTE archivo?

    La puerta solo abre con dos cosas juntas:
      1) el veredicto es APROBADO de verdad (hubo 4 ojos: uno genero, OTRO distinto audito), y
      2) ese veredicto habla de ESTE archivo.

    Por que el veredicto tambien: un veredicto que NO es aprobacion no abre. Antes, un SIN_AUDITAR
    (no quedo segundo cerebro) o un RECHAZADO (el equipo dijo que no) abrian igual por solo nombrar
    el archivo. Eso era un sello de goma: se le decia a Julio que hubo equipo cuando no lo hubo.
    CONTRATO_EQUIPO_QUE_AGUANTA.md ya lo dice como ley: "Un SIN_AUDITAR no es una aprobacion.
    No se le dice a Julio 'el equipo lo aprobo'." Ahora la ley la cumple el candado, no la memoria.
    Un veredicto sobre otra cosa tampoco vale de llave: si abriera todo, bastaria llamar al equipo
    una vez y ya.
    """
    if not d:
        return False
    if d.get("reviso_a_si_mismo"):
        return False
    v = str(d.get("veredicto", "")).strip().upper()
    if v != "APROBADO":
        return False
    base = os.path.basename(fp).lower()
    for a in d.get("archivos", []):
        if os.path.basename(str(a)).lower() == base:
            return True
    return False


def _hay_cerebros():
    try:
        from cuerpo import obrero
        return bool(obrero.quienes_hay())
    except Exception:
        return False


def _apuntar_frenada(fp, por_que):
    """La libreta AL REVES (Julio, 2026-08-21): se apunta cada vez que el candado FRENA.

    Antes se apuntaba lo que se colaba sin equipo; con la puerta de escape cerrada eso ya no
    pasa nunca y la libreta quedaba vacia. Lo util ahora es lo contrario: que Julio pueda ver
    cuantas veces hubo que pararse y por que.

    A prueba de fallos a proposito: si la libreta no se puede escribir, el candado NO se cae.
    Frenar es lo importante; apuntarlo es la prueba, pero no puede tumbar al guardia.
    """
    try:
        os.makedirs(os.path.dirname(_ruta_sin_equipo()), exist_ok=True)
        with open(_ruta_sin_equipo(), "a", encoding="utf-8") as f:
            f.write("%s  %s  (%s)\n" % (time.strftime("%Y-%m-%d %H:%M"), fp[:120], por_que))
    except Exception:
        pass
    # EL REGISTRO DE DECISIONES (Julio, 2026-09-02): aqui queda TODO lo que decide el candado,
    # lo que frena Y lo que deja pasar, con cuatro datos separados por barra: cuando, que
    # archivo, que decidio y por que. Antes solo se apuntaba lo frenado, asi que nadie podia
    # auditar POR DONDE se colo algo: Julio tenia que creerme en vez de mirarlo.
    try:
        _dec = os.path.join(AQUI, "memoria", "DECISIONES_CANDADO.log")
        _texto = str(por_que or "")
        _que = "DEJO PASAR" if _texto.upper().startswith("DEJO PASAR") else "FRENO"
        _motivo = _texto.split(":", 1)[1].strip() if ":" in _texto else _texto
        os.makedirs(os.path.dirname(_dec), exist_ok=True)
        with open(_dec, "a", encoding="utf-8") as f:
            f.write("%s | %s | %s | %s\n"
                    % (time.strftime("%Y-%m-%d %H:%M"), fp[:160], _que, _motivo))
    except Exception:
        pass


MENSAJE = (
    "BLOQUEADO: NO SE ESCRIBE CODIGO A SOLAS\n\n"
    "  {fp}\n\n"
    "  Julio tuvo que repetirlo tres veces y le costo dinero. Uno GENERA, otro distinto AUDITA;\n"
    "  yo dirijo y leo el veredicto. Escribirlo yo mismo gasta lo caro para hacer lo barato.\n\n"
    "  Que hacer:\n"
    "     cd C:\\Ingeniero_VUC; python ingeniero.py equipo <proyecto> \"<la tarea>\"\n\n"
    "  Eso deja el veredicto, y con el veredicto este archivo se abre. Los documentos .md,\n"
    "  los archivos nuevos y el propio arnes se pueden tocar siempre.\n")


def main():
    import autorizacion
    # Solo Julio apaga, por comando (autorizar-off) y con autorizacion escrita: candados abiertos.
    if autorizacion.autorizada():
        _apuntar_frenada("(llave de Julio)", "DEJO PASAR: llave de Julio puesta")
        return 0
    # El interruptor viejo INGENIERO_OFF ya NO basta para apagar: sin autorizacion de Julio,
    # se deja constancia y se sigue bloqueando (Julio, 2026-08-24).
    if os.environ.get("INGENIERO_OFF", "").strip():
        _apuntar_frenada("(INGENIERO_OFF)", "interruptor encendido sin autorizacion previa de Julio")
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        _apuntar_frenada("(peticion ilegible)", "no se pudo leer la peticion: %s" % e)
        sys.stderr.write(MENSAJE.format(fp="(peticion ilegible)"))
        return 2
    fp = str((data.get("tool_input") or {}).get("file_path") or "")

    # EL EQUIPO VIGILA TAMBIEN FUERA DE LA CASA (Julio, 2026-09-02).
    # Agujero medido: antes esto devolvia 0 ("no es de esta casa: no se vigila") para TODO lo que
    # no estuviera dentro de `proyectos.config`. La mesa de Julio esta FUERA (MVP y sus proyectos),
    # asi que la IA podia escribir codigo A SOLAS ahi y nadie lo veia. Ahora:
    #   · dentro de una casa            -> se vigila como siempre
    #   · FUERA de toda casa            -> se exige veredicto IGUAL (se cierra la puerta de fuera)
    #   · temporal del sistema          -> no se vigila (un borrador no debe frenar, leccion 2026-09-01)
    #   · documento (.md) fuera         -> no se vigila (no es codigo)
    _fuera_de_casa = False
    if fp:
        _abs = os.path.abspath(fp).replace("\\", "/").lower()
        _casas = [AQUI.replace("\\", "/").lower()]
        # Las pruebas desvian la casa a su carpeta de mentira, igual que hace el resto del
        # arnes con sus cuadernos. Asi miden al candado DE VERDAD sin tocar el proyecto.
        _otra_casa = os.environ.get("INGENIERO_CASA_TEST", "").strip()
        if _otra_casa:
            _casas.append(_otra_casa.replace("\\", "/").lower())
        try:
            _cfg = os.path.join(AQUI, "proyectos.config")
            with open(_cfg, "r", encoding="utf-8") as _f:
                for _linea in _f:
                    _linea = _linea.strip()
                    if not _linea or _linea.startswith("#"):
                        continue
                    if "=" not in _linea or "|" not in _linea:
                        continue
                    _ruta = _linea.split("=", 1)[1].split("|", 1)[0].strip()
                    if _ruta:
                        _casas.append(_ruta.replace("\\", "/").lower())
        except Exception:
            pass
        _en_casa = any(_abs.startswith(c) for c in _casas if c)
        if not _en_casa:
            if _es_temporal(_abs):
                return 0                    # borrador (solo via la exencion de prueba): no se vigila
            _fuera_de_casa = True           # FUERA de la casa y no es temporal: se exige veredicto
    if not fp:
        _apuntar_frenada("(peticion vacia)", "la peticion no trae archivo")
        sys.stderr.write(MENSAJE.format(fp="(peticion vacia)"))
        return 2
    if os.path.splitext(fp)[1].lower() not in CODIGO:
        _apuntar_frenada(fp, "documento libre")
        return 0                                    # documentos: libres
    rel = fp.replace("\\", "/").lower()
    if "/arnes/" in rel:
        _apuntar_frenada(fp, "DEJO PASAR: es el propio arnes")
        if os.path.exists(fp):                       # solo si el candado YA existe (reparar, no crear)
            return 0                                    # hay que poder arreglar el propio candado
    # VIGIA NUEVA (Julio, 2026-09-02): crear una vigia nueva (por carpeta /vigias/ o por
    # nombre test_vigia_) NO exige veredicto: es la prueba que protege una reparacion y
    # debe nacer ANTES que ella. Si no existe, se deja pasar y se apunta. REESCRIBIR una
    # vigia que ya existe sigue exigiendo veredicto.
    #
    # EL ORDEN IMPORTA Y AQUI SE PAGO: este trozo estaba DESPUES del freno de "crear codigo
    # nuevo", asi que era codigo muerto al que no se llegaba nunca. Una vigia nueva, por
    # definicion, todavia no existe. Toda excepcion va ANTES del freno o no sirve de nada.
    # Y NO BASTA CON LLAMARSE VIGIA: hay que SERLO. Se mira el contenido que se va a escribir,
    # y solo pasa si de verdad es una prueba (trae pytest y algun def test_). Si no, seria la
    # trampa mas facil del mundo: llamar test_vigia_ a cualquier cosa y colar codigo entero sin
    # que nadie lo revise. Cumplir la letra y saltarse el espiritu ya paso una vez aqui.
    # Y sin contenido que mirar tampoco se abre: una excepcion que no se puede comprobar deja
    # de ser excepcion y se convierte en una puerta.
    _loquesea = str((data.get("tool_input") or {}).get("content") or
                    (data.get("tool_input") or {}).get("new_string") or "")
    _es_vigia_de_verdad = ("pytest" in _loquesea and "def test_" in _loquesea)
    if (("/vigias/" in rel) or
            os.path.basename(fp).lower().startswith("test_vigia_")):
        if not os.path.exists(fp) and _es_vigia_de_verdad:
            _apuntar_frenada(fp, "DEJO PASAR: vigia nueva de verdad")
            return 0
    # CERRADO (Julio, 2026-08-27): crear archivos de codigo tambien exige veredicto.
    # Antes se colaba por aqui y se construia un subsistema entero a solas.
    if not os.path.exists(fp):
        _apuntar_frenada(fp, "FRENO: crear codigo nuevo sin veredicto del equipo")
        _m = MENSAJE.format(fp=fp)
        if _fuera_de_casa:
            _m += ("\n  (OJO: este archivo esta FUERA de las rutas registradas de proyectos.config.\n"
                   "   Para trabajar ahi hay que registrar el proyecto (agregar su ruta a "
                   "proyectos.config)\n   o trabajar en uno ya registrado.)\n")
        sys.stderr.write(_m)
        return 2
    # FORTALECIDO (Julio, 2026-08-21): ya NO se deja pasar sin veredicto aunque no haya cerebros.
    # Antes se escapaba por aqui y dejaba a foto_informe y a cualquier proyecto SIN VIGILAR.
    # Ahora SIEMPRE se exige el veredicto del equipo; si no hay, se BLOQUEA y Julio decide.
    d = veredicto_vigente()
    if cubre(d, fp):
        _apuntar_frenada(fp, "veredicto del equipo cubre el archivo")
        return 0                                    # el equipo ya lo miro: adelante
    # SIN PUERTA (Julio, 2026-08-26): la salida de emergencia NECESITO_EDITAR / permiso_editar
    # se volvio la ENTRADA PRINCIPAL — todas las IA se salieron por ahi y trabajaron a solas,
    # que es justo lo que este candado existe para impedir. Se quito de raiz. El UNICO que
    # autoriza tocar codigo a solas es Julio (autorizacion), o el veredicto del equipo.
    # Si un archivo grande no cabe en el paquete, la cura NO es una llave: es arreglar el
    # repartidor (diccionario/router) para que el veredicto SI nombre el archivo.
    # LA LIBRETA, AL REVES: queda constancia de CADA frenada, con el motivo exacto.
    _apuntar_frenada(fp, "sin veredicto del equipo" if not d else
                     "el veredicto vigente no habla de este archivo")
    _m = MENSAJE.format(fp=fp)
    if _fuera_de_casa:
        _m += ("\n  (OJO: este archivo esta FUERA de las rutas registradas de proyectos.config.\n"
               "   Para trabajar ahi hay que registrar el proyecto (agregar su ruta a "
               "proyectos.config)\n   o trabajar en uno ya registrado.)\n")
    sys.stderr.write(_m)
    # MEDICION (Julio, 2026-08-25): este candado cazo algo real: freno escribir a solas.
    try:
        import candados_medicion
        candados_medicion.cazado("equipo")
    except Exception:
        pass
    return 2


if __name__ == "__main__":
    sys.exit(main())
