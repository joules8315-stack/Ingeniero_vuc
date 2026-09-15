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
      ["arnes\\canal.py", "leer"],
      { cwd: INGENIERO, encoding: "utf-8", timeout: 15000,
        env: { ...process.env, INGENIERO_QUIEN: QUIEN } },
    );
    const texto = (out || "").trim();
    if (!texto) return "";
    try {
      const j = JSON.parse(texto);
      const ctx = j.hookSpecificOutput && j.hookSpecificOutput.additionalContext;
      return typeof ctx === "string" ? ctx : "";
    } catch {
      return "";
    }
  } catch {
    return "";
  }
}

export const CanalBuzonPlugin = async ({ client }) => {
  let sessionID = "";
  let lastActivity = Date.now();
  let inyectadas = 0;

  const inyectar = async (ctx) => {
    if (!sessionID) {
      log("sin sesion conocida, no inyecto");
      return;
    }
    inyectadas += 1;
    try {
      await client.session.promptAsync({
        path: { id: sessionID },
        body: {
          parts: [{ type: "text", text: ctx, synthetic: true }],
        },
      });
      log("inyectado #" + inyectadas + " a sesion " + sessionID);
    } catch (e) {
      log("fallo inyeccion: " + String((e && e.message) || e).slice(0, 160));
    }
  };

  const vigilante = () => {
    try {
      if (Date.now() - lastActivity < IDLE_MS) {
        log("vigilante: actividad reciente, espero");
        return;
      }
      if (inyectadas >= MAX_INYECTADAS) {
        log("vigilante: tope diario alcanzado (" + inyectadas + ")");
        return;
      }
      const ctx = leerCanal();
      if (!ctx) return;
      log("vigilante: hay recados, inyecto");
      inyectar(ctx);
    } catch (e) {
      log("vigilante error: " + String((e && e.message) || e).slice(0, 160));
    }
  };

  setInterval(vigilante, POLIZA_MS);
  log("plugin canal_buzon cargado (QUIEN=" + QUIEN + ", poliza " + POLIZA_MS + "ms)");

  return {
    "chat.message": async (input, output) => {
      sessionID = input && input.sessionID ? input.sessionID : sessionID;
      lastActivity = Date.now();
      const ctx = leerCanal();
      if (!ctx) return;
      output.parts.push({
        id: "canal-" + Date.now(),
        sessionID,
        messageID: input && input.messageID ? input.messageID : "user",
        type: "text",
        text: ctx,
        synthetic: true,
      });
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