/**
 * Analysis Submission Controller
 */

let validationTimer = null;

function updateApiKeyBadge() {
  const badge = document.getElementById("gemini-status-badge");
  if (!badge) return;
  const stored = localStorage.getItem("sentinel_gemini_api_key");
  if (stored) {
    badge.innerHTML = `<span style="color: var(--forest); font-weight: 600; background-color: var(--forest-soft); padding: 2px 7px; border-radius: 9999px;">● Real-Time AI Active</span>`;
  } else {
    badge.innerHTML = `<span style="color: var(--fg-muted); background-color: var(--bg-surface-2); padding: 2px 7px; border-radius: 9999px;">● Static Multi-Agent</span>`;
  }
}

function initApiKeyPanel() {
  updateApiKeyBadge();

  const apiKeyBtn = document.getElementById("api-key-btn");
  const apiKeyPanel = document.getElementById("api-key-panel");
  const saveKeyBtn = document.getElementById("save-inline-key-btn");
  const clearKeyBtn = document.getElementById("clear-inline-key-btn");
  const inlineInput = document.getElementById("inline-gemini-key");

  if (apiKeyBtn && apiKeyPanel) {
    apiKeyBtn.addEventListener("click", () => {
      const isHidden = apiKeyPanel.style.display === "none";
      apiKeyPanel.style.display = isHidden ? "block" : "none";
      if (isHidden && inlineInput) {
        inlineInput.value = localStorage.getItem("sentinel_gemini_api_key") || "";
        inlineInput.focus();
      }
    });
  }

  if (saveKeyBtn && inlineInput) {
    saveKeyBtn.addEventListener("click", () => {
      const val = inlineInput.value.trim();
      if (val) {
        localStorage.setItem("sentinel_gemini_api_key", val);
        toast.success("Gemini API key saved! Real-time deep AI inspection enabled.");
        if (apiKeyPanel) apiKeyPanel.style.display = "none";
      } else {
        localStorage.removeItem("sentinel_gemini_api_key");
        toast.info("Using local static multi-agent rules.");
      }
      updateApiKeyBadge();
    });
  }

  if (clearKeyBtn && inlineInput) {
    clearKeyBtn.addEventListener("click", () => {
      localStorage.removeItem("sentinel_gemini_api_key");
      inlineInput.value = "";
      toast.info("Gemini API key removed. Using local static multi-agent rules.");
      updateApiKeyBadge();
    });
  }
}

async function loadSamples() {
  const container = document.getElementById("samples-container");
  if (!container) return;

  try {
    const res = await fetch("/api/samples");
    const samples = await res.json();

    container.innerHTML = samples.map(s => `
      <button type="button" class="btn btn-outline sample-chip" data-id="${s.id}" style="border-radius: 9999px; padding: 6px 12px; font-size: 12px;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 13px; height: 13px;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
        ${s.label}
      </button>
    `).join("");

    document.querySelectorAll(".sample-chip").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        const sample = samples.find(s => s.id === id);
        if (sample) {
          document.getElementById("code-input").value = sample.code;
          document.getElementById("filename-input").value = sample.filename;
          document.getElementById("language-select").value = "Auto-detect";
          toast.success(`Loaded sample: ${sample.filename}`);
          runLiveValidation();
        }
      });
    });
  } catch (e) {}
}

async function runLiveValidation() {
  const code = document.getElementById("code-input").value;
  const filename = document.getElementById("filename-input").value;
  const language = document.getElementById("language-select").value;
  const valContainer = document.getElementById("validation-result");
  const submitBtn = document.getElementById("run-analysis-btn");

  if (!code.trim()) {
    if (valContainer) {
      valContainer.innerHTML = `<p style="font-size: 13px; color: var(--fg-muted);">Paste or upload code to see language detection and syntax validation.</p>`;
    }
    if (submitBtn) submitBtn.disabled = true;
    return;
  }

  try {
    const res = await fetch("/api/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, filename, language }),
    });

    if (!res.ok) return;
    const data = await res.json();

    if (valContainer) {
      valContainer.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 8px; font-size: 13px;">
          <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 6px;">
            <span style="color: var(--fg-muted);">Language:</span>
            <span style="font-weight: 600;">${data.language} ${data.languageAutoDetected ? '<span style="color: var(--fg-muted); font-size: 11px;">(auto-detected)</span>' : ''}</span>
          </div>
          <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 6px;">
            <span style="color: var(--fg-muted);">Lines:</span>
            <span style="font-family: var(--font-mono);">${data.lineCount}</span>
          </div>
          <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 6px;">
            <span style="color: var(--fg-muted);">Characters:</span>
            <span style="font-family: var(--font-mono);">${data.charCount}</span>
          </div>
          <div style="margin-top: 6px; padding: 10px 12px; border-radius: var(--radius-md); background-color: ${data.syntaxValid ? 'var(--forest-soft)' : 'var(--warning-soft)'}; color: ${data.syntaxValid ? 'var(--forest)' : 'var(--warning)'};">
            <div style="font-weight: 600; display: flex; align-items: center; gap: 6px;">
              ${data.syntaxValid 
                ? '<svg style="width: 16px; height: 16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> Syntax Valid'
                : `<svg style="width: 16px; height: 16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg> ${data.syntaxErrors.length} syntax notice(s)`}
            </div>
            ${data.syntaxErrors.length ? `
              <ul style="margin-top: 6px; padding-left: 18px; font-size: 12px; line-height: 1.4;">
                ${data.syntaxErrors.map(e => `<li>${e}</li>`).join("")}
              </ul>
            ` : ''}
          </div>
        </div>
      `;
    }

    if (submitBtn) {
      submitBtn.disabled = !code.trim();
    }
  } catch (err) {}
}

async function handleAnalyze() {
  const code = document.getElementById("code-input").value;
  const filename = document.getElementById("filename-input").value;
  const language = document.getElementById("language-select").value;
  const submitBtn = document.getElementById("run-analysis-btn");

  if (!code.trim()) {
    toast.error("Please paste code or upload a file first.");
    return;
  }

  submitBtn.disabled = true;
  submitBtn.innerHTML = `<svg style="width: 15px; height: 15px; animation: spin 1s linear infinite;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line></svg> Agents running…`;

  const stepperItems = document.querySelectorAll(".orchestration-step");
  let currentStep = 0;
  const interval = setInterval(() => {
    if (currentStep < stepperItems.length) {
      stepperItems[currentStep].classList.add("active");
      if (currentStep > 0) {
        stepperItems[currentStep - 1].classList.remove("active");
        stepperItems[currentStep - 1].classList.add("done");
      }
      currentStep++;
    }
  }, 1200);

  const apiKey = localStorage.getItem("sentinel_gemini_api_key") || undefined;

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, filename, language, apiKey }),
    });

    clearInterval(interval);

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Analysis failed");
    }

    const record = await res.json();
    setCurrentAnalysis(record);
    toast.success("Analysis complete!");
    setTimeout(() => {
      window.location.href = `/findings.html?id=${record.id}`;
    }, 600);
  } catch (e) {
    clearInterval(interval);
    toast.error(e.message);
    submitBtn.disabled = false;
    submitBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg> Run multi-agent analysis`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initApiKeyPanel();
  loadSamples();

  const codeInput = document.getElementById("code-input");
  const filenameInput = document.getElementById("filename-input");
  const languageSelect = document.getElementById("language-select");
  const runBtn = document.getElementById("run-analysis-btn");
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");

  if (codeInput) {
    codeInput.addEventListener("input", () => {
      clearTimeout(validationTimer);
      validationTimer = setTimeout(runLiveValidation, 400);
    });
  }

  if (filenameInput) {
    filenameInput.addEventListener("input", () => {
      clearTimeout(validationTimer);
      validationTimer = setTimeout(runLiveValidation, 400);
    });
  }

  if (languageSelect) {
    languageSelect.addEventListener("change", runLiveValidation);
  }

  if (runBtn) {
    runBtn.addEventListener("click", handleAnalyze);
  }

  if (dropzone && fileInput) {
    dropzone.addEventListener("click", () => fileInput.click());
    dropzone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    });
    dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
    dropzone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
      if (e.dataTransfer.files.length) {
        const file = e.dataTransfer.files[0];
        const reader = new FileReader();
        reader.onload = () => {
          codeInput.value = reader.result;
          filenameInput.value = file.name;
          languageSelect.value = "Auto-detect";
          toast.success(`Loaded file: ${file.name}`);
          runLiveValidation();
        };
        reader.readAsText(file);
      }
    });

    fileInput.addEventListener("change", (e) => {
      if (e.target.files.length) {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = () => {
          codeInput.value = reader.result;
          filenameInput.value = file.name;
          languageSelect.value = "Auto-detect";
          toast.success(`Loaded file: ${file.name}`);
          runLiveValidation();
        };
        reader.readAsText(file);
      }
    });
  }
});
