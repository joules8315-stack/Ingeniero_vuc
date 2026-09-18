import { execFileSync } from "node:child_process";
import { appendFileSync } from "node:fs";

const PYTHON = "C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python310\\python.exe";
const INGENIERO = "C:\\Ingeniero_VUC";
const QUIEN = "opencode";
const LOG = "C:\\Users\\USER\\AppData\\Local\\Temp\\opencode\\canal_buzon.log";
const POLIZA_MS = 10000;
const IDLE_MS = 30000;
const MAX_INYECTADAS = 60;

function log(msg) {
  try {
    appendFileSync(LOG, new Date().toISOString() + "  " + msg + "\n");
  } catch {}
}

function leerCanal() {
  try {
    const out = execFileSync(
      PYTHON,
      ["arnes\\canal.py", "leer", "--sin-marcar"],
      { cwd: INGENIERO, encoding: "utf-8", timeout: 15000,
        env: { ...process.env, INGENIERO_QUIEN: QUIEN } },
    );
    const texto = (out || "").trim();
    if (!texto) return null;
    try {
      const j = JSON.parse(texto);
      const ctx = j.additionalContext;
      const rutas = j.rutas;
      if (typeof ctx === "string" && ctx) return { ctx, rutas };
      return null;
    } catch {
      return null;
    }
  } catch {
    return null;
  }
}

function marcarCanal(rutas) {
  try {
    if (!rutas || !rutas.length) return;
    execFileSync(
      PYTHON,
      ["arnes\\canal.py", "marcar", ...rutas],
      { cwd: INGENIERO, encoding: "utf-8", timeout: 15000,
        env: { ...process.env, INGENIERO_QUIEN: QUIEN } },
    );
  } catch (e) {
    log("marcarCanal fallo: " + e);
  }
}

export const CanalBuzonPlugin = async ({ client }) => {
  let sessionID = "";
  let lastActivity = Date.now();
  let inyectadas = 0;

  const inyectar = async (r) => {
    if (!sessionID) {
      log("sin sesion conocida, no inyecto");
      return;
    }
    inyectadas += 1;
    try {
      await client.session.promptAsync({
        path: { id: sessionID },
        body: {
          parts: [{ type: "text", text: r.ctx, synthetic: true }],
        },
      });
      log("inyectado #" + inyectadas + " a sesion " + sessionID);
      marcarCanal(r.rutas);
    } catch (e) {
      log("fallo inyeccion: " + String((e && e.message) || e).slice(0, 160));
    }
  };

  const vigilante = () => {
    try {
      if (!sessionID) {
        log("vigilante: sin sesion conocida, no leo");
        return;
      }
      if (Date.now() - lastActivity < IDLE_MS) {
        log("vigilante: actividad reciente, espero");
        return;
      }
      if (inyectadas >= MAX_INYECTADAS) {
        log("vigilante: tope diario alcanzado (" + inyectadas + ")");
        return;
      }
      const r = leerCanal();
      if (!r) return;
      log("vigilante: hay recados, inyecto");
      inyectar(r);
    } catch (e) {
      log("vigilante error: " + String((e && e.message) || e).slice(0, 160));
    }
  };

  setInterval(vigilante, POLIZA_MS);
  log("plugin canal_buzon cargado (QUIEN=" + QUIEN + ", poliza " + POLIZA_MS + "ms)");

  return {
    "chat.message": async (input, output) => {
      sessionID = (output && output.message && output.message.sessionID) || sessionID;
      lastActivity = Date.now();
      const messageID = (output && output.message && output.message.id) || (input && input.messageID);
      if (!messageID || String(messageID).indexOf("msg") !== 0) {
        log("chat.message: sin messageID real (msg...), no se agrega la parte ni se marca");
        return;
      }
      const r = leerCanal();
      if (!r) return;
      output.parts.push({
        id: "prt_" + Date.now() + "_" + Math.random().toString(36).slice(2, 8),
        sessionID,
        messageID,
        type: "text",
        text: r.ctx,
        synthetic: true,
      });
      marcarCanal(r.rutas);
    },
    event: async ({ event }) => {
      if (!event || !event.properties) return;
      const s = event.properties;
      sessionID = (s && (s.sessionID || (s.info && s.info.id))) || sessionID;
    },
    "shell.env": async (_input, output) => {
      output.env.INGENIERO_QUIEN = QUIEN;
    },
  };
};

export default CanalBuzonPlugin;