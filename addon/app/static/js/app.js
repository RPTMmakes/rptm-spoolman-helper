"use strict";

function apiUrl(path) {
  const meta = document.querySelector('meta[name="rptm-api-base"]');
  const base = (meta?.content || "/api").replace(/\/$/, "");
  const cleanPath = path.replace(/^\//, "");
  return `${base}/${cleanPath}`;
}

async function loadRuntimeStatus() {
  const statusElement = document.getElementById("global-status");
  const backendElement = document.getElementById("backend-status");
  const accessElement = document.getElementById("access-mode");

  try {
    const [healthResponse, settingsResponse] = await Promise.all([
      fetch(apiUrl("health"), { cache: "no-store" }),
      fetch(apiUrl("settings"), { cache: "no-store" }),
    ]);

    if (!healthResponse.ok || !settingsResponse.ok) {
      throw new Error("Status request failed");
    }

    const health = await healthResponse.json();
    const settings = await settingsResponse.json();

    backendElement.textContent =
      health.status === "ok" ? `Online · ${health.version}` : "Fehler";

    accessElement.textContent = settings.ingress
      ? "Home Assistant Ingress"
      : "Direkter Portzugriff";

    statusElement.classList.add("is-online");
    statusElement.querySelector("span:last-child").textContent =
      "Add-on ist erreichbar";
  } catch (error) {
    console.error("Runtime status could not be loaded:", error);
    backendElement.textContent = "Nicht erreichbar";
    accessElement.textContent = "Unbekannt";
    statusElement.classList.add("is-error");
    statusElement.querySelector("span:last-child").textContent =
      "Verbindung fehlgeschlagen";
  }
}

window.addEventListener("DOMContentLoaded", loadRuntimeStatus);
