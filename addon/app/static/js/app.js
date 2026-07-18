"use strict";

function relativeUrl(path) {
  return new URL(path, new URL(".", window.location.href));
}

async function loadRuntimeStatus() {
  const statusElement = document.getElementById("global-status");
  const backendElement = document.getElementById("backend-status");
  const accessElement = document.getElementById("access-mode");

  try {
    const [healthResponse, settingsResponse] = await Promise.all([
      fetch(relativeUrl("api/health"), { cache: "no-store" }),
      fetch(relativeUrl("api/settings"), { cache: "no-store" }),
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
