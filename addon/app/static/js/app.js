"use strict";

function apiUrl(path) {
  const meta = document.querySelector('meta[name="rptm-api-base"]');
  const base = (meta?.content || "/api").replace(/\/$/, "");
  const cleanPath = path.replace(/^\//, "");
  return `${base}/${cleanPath}`;
}

async function readJson(response) {
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || `HTTP ${response.status}`);
  }

  return data;
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

    const health = await readJson(healthResponse);
    const settings = await readJson(settingsResponse);

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
      "Add-on-Verbindung fehlgeschlagen";
  }
}

function setSpoolmanLoading(isLoading) {
  const button = document.getElementById("spoolman-sync");
  button.disabled = isLoading;
  button.textContent = isLoading
    ? "Spoolman wird abgeglichen …"
    : "Spoolman abgleichen";
}

function renderLocations(locations) {
  const container = document.getElementById("location-list");
  container.replaceChildren();

  if (!locations.length) {
    const empty = document.createElement("span");
    empty.className = "location-chip muted-chip";
    empty.textContent = "Noch keine Lagerorte vorhanden";
    container.appendChild(empty);
    return;
  }

  for (const location of locations) {
    const chip = document.createElement("span");
    chip.className = "location-chip";
    chip.textContent = location;
    container.appendChild(chip);
  }
}

async function loadSpoolmanStatus(method = "GET") {
  const message = document.getElementById("spoolman-message");
  const status = document.getElementById("spoolman-status");

  setSpoolmanLoading(true);
  message.classList.remove("is-error");

  try {
    const endpoint = method === "POST"
      ? "spoolman/sync"
      : "spoolman/status";

    const response = await fetch(apiUrl(endpoint), {
      method,
      cache: "no-store",
    });
    const data = await readJson(response);

    status.textContent = data.health === "healthy"
      ? "Verbunden"
      : data.health;
    document.getElementById("spoolman-version").textContent =
      data.version || "Unbekannt";
    document.getElementById("spool-count").textContent =
      data.spool_count;
    document.getElementById("filament-count").textContent =
      data.filament_count;
    document.getElementById("vendor-count").textContent =
      data.vendor_count;
    document.getElementById("location-count").textContent =
      data.location_count;

    message.textContent = `Verbunden mit ${data.url}`;
    renderLocations(data.locations);
  } catch (error) {
    console.error("Spoolman status could not be loaded:", error);
    status.textContent = "Nicht erreichbar";
    message.textContent = error.message;
    message.classList.add("is-error");
    renderLocations([]);
  } finally {
    setSpoolmanLoading(false);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  loadRuntimeStatus();
  loadSpoolmanStatus();

  document
    .getElementById("spoolman-sync")
    .addEventListener("click", () => loadSpoolmanStatus("POST"));
});
