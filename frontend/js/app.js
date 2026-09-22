/**
 * Sentinel Frontend Application Core
 */

// Theme Management
function initTheme() {
  const saved = localStorage.getItem("sentinel_theme");
  const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  const theme = saved || (prefersDark ? "dark" : "light");
  document.documentElement.setAttribute("data-theme", theme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "light";
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("sentinel_theme", next);
}

// Toast Notifications
const toast = {
  show(message, type = "info") {
    let container = document.getElementById("toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "toast-container";
      document.body.appendChild(container);
    }
    const item = document.createElement("div");
    item.className = `toast toast-${type}`;
    item.textContent = message;
    container.appendChild(item);
    setTimeout(() => {
      item.style.opacity = "0";
      setTimeout(() => item.remove(), 250);
    }, 3200);
  },
  success(msg) {
    this.show(msg, "success");
  },
  error(msg) {
    this.show(msg, "error");
  },
  info(msg) {
    this.show(msg, "info");
  },
};

// Score Gauge SVG Generator
function renderScoreGauge(value, size = 64) {
  const strokeWidth = 5;
  const radius = (size - strokeWidth * 2) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  let strokeColor = "#2F7A59"; // success
  if (value < 60) strokeColor = "#BD3429"; // destructive
  else if (value < 80) strokeColor = "#B36B15"; // warning

  return `
    <div class="score-gauge-wrap" style="width: ${size}px; height: ${size}px;">
      <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
        <circle cx="${size / 2}" cy="${size / 2}" r="${radius}" fill="none" stroke="var(--bg-surface-3)" stroke-width="${strokeWidth}" />
        <circle cx="${size / 2}" cy="${size / 2}" r="${radius}" fill="none" stroke="${strokeColor}" stroke-width="${strokeWidth}"
          stroke-dasharray="${circumference}" stroke-dashoffset="${offset}" stroke-linecap="round" />
      </svg>
      <span class="score-gauge-val" style="font-size: ${Math.round(size * 0.28)}px;">${value}</span>
    </div>
  `;
}

// Helper to format severity badge
function getSeverityBadge(severity) {
  const s = severity.toLowerCase();
  return `<span class="badge badge-${s}">${severity}</span>`;
}

// Helper to format verdict badge
function getVerdictBadge(verdict) {
  let cls = "verdict-approve";
  if (verdict === "Block") cls = "verdict-block";
  else if (verdict === "Request changes") cls = "verdict-request";
  else if (verdict === "Approve with suggestions") cls = "verdict-approve-sugg";
  return `<span class="verdict-badge ${cls}">${verdict}</span>`;
}

// Current Analysis Cache
function setCurrentAnalysis(record) {
  if (record && record.id) {
    localStorage.setItem("sentinel_current_id", record.id);
  }
}

async function getCurrentAnalysis() {
  const currentId = localStorage.getItem("sentinel_current_id");
  if (currentId) {
    try {
      const res = await fetch(`/api/analyses/${currentId}`);
      if (res.ok) return await res.json();
    } catch (e) {}
  }
  // Fallback to latest
  try {
    const listRes = await fetch("/api/analyses");
    if (listRes.ok) {
      const list = await listRes.json();
      if (list && list.length > 0) {
        localStorage.setItem("sentinel_current_id", list[0].id);
        return list[0];
      }
    }
  } catch (e) {}
  return null;
}

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  const toggleBtn = document.getElementById("theme-toggle-btn");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", toggleTheme);
  }
});
