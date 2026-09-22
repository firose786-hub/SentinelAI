/**
 * Findings & Analysis Results Controller
 */

let currentRecord = null;
let currentTab = "summary";

async function loadFindings() {
  const container = document.getElementById("findings-content");
  if (!container) return;

  const urlParams = new URLSearchParams(window.location.search);
  const idFromUrl = urlParams.get("id");
  if (idFromUrl) {
    try {
      const res = await fetch(`/api/analyses/${idFromUrl}`);
      if (res.ok) currentRecord = await res.json();
    } catch (e) {}
  }

  if (!currentRecord) {
    currentRecord = await getCurrentAnalysis();
  }

  if (!currentRecord) {
    container.innerHTML = `
      <div class="panel" style="padding: 48px; text-align: center;">
        <svg style="width: 36px; height: 36px; color: var(--border-strong); margin: 0 auto 12px auto;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
          <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
        </svg>
        <h2 style="font-size: 18px; margin-bottom: 8px;">No analysis selected</h2>
        <p style="color: var(--fg-subtle); max-width: 400px; margin: 0 auto 20px auto; font-size: 13.5px;">
          Submit code for multi-agent inspection to inspect findings, remediations, and code health.
        </p>
        <a href="/analysis.html" class="btn btn-primary">Run an analysis</a>
      </div>
    `;
    return;
  }

  setCurrentAnalysis(currentRecord);
  renderFindingsView();
}

function renderFindingsView() {
  const container = document.getElementById("findings-content");
  const a = currentRecord;

  const securityCount = a.securityFindings.length;
  const qualityCount = a.qualityFindings.length;
  const remediationCount = a.remediations.length;

  container.innerHTML = `
    <!-- Top Overview Header -->
    <section class="panel" style="margin-bottom: 18px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; flex-wrap: wrap;">
        <div>
          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 6px;">
            <h2 style="font-family: var(--font-mono); font-size: 16px;">${a.submission.filename}</h2>
            <span class="badge-tag">${a.submission.language}</span>
            <span class="badge-tag">${a.submission.lineCount} lines</span>
            <span class="badge-tag">complexity: ${a.metrics.complexity}</span>
          </div>
          <p style="color: var(--fg-subtle); font-size: 13.5px; line-height: 1.5; max-width: 700px;">
            ${a.summary.executiveOverview}
          </p>
        </div>
        <div>
          ${getVerdictBadge(a.summary.verdict)}
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 16px; margin-top: 18px; padding-top: 18px; border-top: 1px solid var(--border);">
        <div style="display: flex; align-items: center; gap: 12px;">
          ${renderScoreGauge(a.metrics.securityScore, 48)}
          <div>
            <p style="font-size: 11px; color: var(--fg-muted);">Security</p>
            <p style="font-weight: 700; font-size: 16px;">${a.metrics.securityScore}</p>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
          ${renderScoreGauge(a.metrics.qualityScore, 48)}
          <div>
            <p style="font-size: 11px; color: var(--fg-muted);">Quality</p>
            <p style="font-weight: 700; font-size: 16px;">${a.metrics.qualityScore}</p>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
          ${renderScoreGauge(a.metrics.maintainabilityScore, 48)}
          <div>
            <p style="font-size: 11px; color: var(--fg-muted);">Maintainability</p>
            <p style="font-weight: 700; font-size: 16px;">${a.metrics.maintainabilityScore}</p>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
          ${renderScoreGauge(a.metrics.overallHealth, 48)}
          <div>
            <p style="font-size: 11px; color: var(--fg-muted);">Code Health</p>
            <p style="font-weight: 700; font-size: 16px;">${a.metrics.overallHealth}</p>
          </div>
        </div>
      </div>

      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--border);">
        ${a.agentTimings.map(t => `
          <span class="badge-tag" style="display: flex; align-items: center; gap: 4px;">
            <svg style="width: 11px; height: 11px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
            ${t.agent}: ${(t.ms / 1000).toFixed(1)}s
          </span>
        `).join("")}
      </div>
    </section>

    <!-- Tabs Navigation -->
    <div class="tabs-nav">
      <button type="button" class="tab-btn ${currentTab === 'summary' ? 'active' : ''}" onclick="switchTab('summary')">
        <svg style="width: 15px; height: 15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
        PR summary
      </button>
      <button type="button" class="tab-btn ${currentTab === 'security' ? 'active' : ''}" onclick="switchTab('security')">
        <svg style="width: 15px; height: 15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
        Security (${securityCount})
      </button>
      <button type="button" class="tab-btn ${currentTab === 'quality' ? 'active' : ''}" onclick="switchTab('quality')">
        <svg style="width: 15px; height: 15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        Quality (${qualityCount})
      </button>
      <button type="button" class="tab-btn ${currentTab === 'remediation' ? 'active' : ''}" onclick="switchTab('remediation')">
        <svg style="width: 15px; height: 15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
        Remediation (${remediationCount})
      </button>
    </div>

    <!-- Tab Contents -->
    <div id="tab-content-area">
      ${renderTabContent()}
    </div>
  `;
}

function switchTab(tabName) {
  currentTab = tabName;
  renderFindingsView();
}

function renderTabContent() {
  const a = currentRecord;

  if (currentTab === "summary") {
    return `
      <div class="grid-split">
        <div class="panel">
          <h3 style="font-size: 15px; font-weight: 600; margin-bottom: 12px;">Prioritised fix list</h3>
          <ol style="padding-left: 0; list-style: none; display: flex; flex-direction: column; gap: 10px;">
            ${a.summary.prioritizedFixes.map((fix, idx) => `
              <li style="display: flex; gap: 10px; font-size: 13.5px;">
                <span style="display: flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 50%; background-color: var(--accent); color: var(--accent-fg); font-family: var(--font-mono); font-size: 11px; font-weight: 700; flex-shrink: 0;">${idx + 1}</span>
                <span style="color: var(--fg-subtle);">${fix}</span>
              </li>
            `).join("")}
          </ol>
        </div>

        <div style="display: flex; flex-direction: column; gap: 16px;">
          <div class="panel">
            <h3 style="font-size: 15px; font-weight: 600; margin-bottom: 12px;">Severity breakdown</h3>
            <div style="display: flex; flex-direction: column; gap: 8px;">
              ${["Critical", "High", "Medium", "Low"].map(sev => `
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
                  ${getSeverityBadge(sev)}
                  <span style="font-family: var(--font-mono); font-weight: 600;">${a.summary.severityBreakdown[sev] || 0}</span>
                </div>
              `).join("")}
            </div>
          </div>

          <div class="panel">
            <h3 style="font-size: 15px; font-weight: 600; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
              <svg style="width: 15px; height: 15px; color: var(--primary);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
              Knowledge grounding
            </h3>
            <ul style="padding-left: 16px; font-size: 12px; color: var(--fg-subtle); display: flex; flex-direction: column; gap: 4px;">
              ${a.knowledgeCitations.map(c => `<li>${c}</li>`).join("")}
            </ul>
          </div>
        </div>
      </div>
    `;
  }

  if (currentTab === "security") {
    if (!a.securityFindings.length) {
      return `<div class="panel" style="padding: 32px; text-align: center; color: var(--fg-muted);">No security vulnerabilities detected in this submission.</div>`;
    }
    return a.securityFindings.map(f => renderFindingCard(f, true)).join("");
  }

  if (currentTab === "quality") {
    if (!a.qualityFindings.length) {
      return `<div class="panel" style="padding: 32px; text-align: center; color: var(--fg-muted);">No code quality issues detected in this submission.</div>`;
    }
    return a.qualityFindings.map(f => renderFindingCard(f, false)).join("");
  }

  if (currentTab === "remediation") {
    if (!a.remediations.length) {
      return `<div class="panel" style="padding: 32px; text-align: center; color: var(--fg-muted);">No remediation items generated.</div>`;
    }
    return a.remediations.map((r, idx) => `
      <div class="panel" style="margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
          <svg style="width: 16px; height: 16px; color: var(--primary);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
          <h3 style="font-size: 15px; font-weight: 600;">${r.title}</h3>
          <span class="badge-tag">${r.findingId}</span>
        </div>
        <p style="font-size: 13.5px; color: var(--fg-subtle); line-height: 1.45;">
          ${r.recommendation}
        </p>
        ${r.bestPractice ? `
          <div style="margin-top: 10px; padding: 10px 14px; border-radius: var(--radius-md); background-color: var(--forest-soft); color: var(--forest); font-size: 12.5px; line-height: 1.45;">
            <b>Best practice:</b> ${r.bestPractice}
          </div>
        ` : ''}
        ${r.correctedCode ? renderRemediationCodeBox(r.correctedCode, idx) : ''}
      </div>
    `).join("");
  }

  return "";
}

function renderRemediationCodeBox(code, idx) {
  const codeLines = code.split("\n");
  const uniqueId = `rem-code-${idx}`;
  return `
    <div class="code-container" style="margin-top: 12px;" id="${uniqueId}">
      <div class="code-header" style="display: flex; justify-content: space-between; align-items: center;">
        <span>CORRECTED CODE</span>
        <button type="button" class="btn btn-outline" style="padding: 2px 8px; font-size: 11px; display: flex; align-items: center; gap: 4px;" onclick="copyCodeSnippet('${uniqueId}')">
          <svg style="width: 12px; height: 12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
          Copy
        </button>
      </div>
      <div class="code-body">
        ${codeLines.map((line, i) => `
          <div class="code-line">
            <span class="code-line-num">${i + 1}</span>
            <span>${escapeHtml(line || ' ')}</span>
          </div>
        `).join("")}
      </div>
      <textarea style="display:none;" class="raw-code-store">${escapeHtml(code)}</textarea>
    </div>
  `;
}

function copyCodeSnippet(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const textarea = container.querySelector(".raw-code-store");
  if (textarea) {
    navigator.clipboard.writeText(textarea.value).then(() => {
      toast.success("Corrected code copied to clipboard!");
    }).catch(() => {
      toast.info("Copied!");
    });
  }
}

function renderFindingCard(f, isSecurity) {
  const rem = currentRecord.remediations.find(r => r.findingId === f.id);
  const lines = currentRecord.code.split("\n");
  let snippetHtml = "";

  if (f.line && f.line > 0 && f.line <= lines.length) {
    const start = Math.max(0, f.line - 3);
    const end = Math.min(lines.length, f.line + 2);
    const slice = lines.slice(start, end);

    snippetHtml = `
      <div class="code-container" style="margin-top: 10px;">
        <div class="code-header"><span>FLAGGED LOCATION (LINE ${f.line})</span></div>
        <div class="code-body">
          ${slice.map((line, idx) => {
            const lineNo = start + idx + 1;
            const isTarget = lineNo === f.line;
            return `
              <div class="code-line ${isTarget ? 'code-line-highlight' : ''}">
                <span class="code-line-num">${lineNo}</span>
                <span>${escapeHtml(line || ' ')}</span>
              </div>
            `;
          }).join("")}
        </div>
      </div>
    `;
  }

  return `
    <article class="finding-card" id="card-${f.id}">
      <div class="finding-card-header" onclick="toggleCardDetail('${f.id}')">
        <span class="finding-dot dot-${f.severity.toLowerCase()}"></span>
        <div class="finding-content">
          <div class="finding-title-row">
            <h3 class="finding-title">${f.title}</h3>
            ${getSeverityBadge(f.severity)}
          </div>
          <p class="finding-detail">${f.detail}</p>
          <div class="finding-tags">
            ${isSecurity ? `<span class="badge-tag">${f.owaspCategory}</span><span class="badge-tag">${f.cwe}</span>` : `<span class="badge-tag">${f.category}</span>`}
            <span class="badge-tag">${f.line ? `line ${f.line}` : 'file-level'}</span>
            <span class="badge-tag">${f.agent}</span>
          </div>
        </div>
        <svg style="width: 16px; height: 16px; color: var(--fg-muted); transition: transform 0.2s;" id="chevron-${f.id}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
      </div>

      <div class="finding-details-collapsible" id="detail-${f.id}" style="display: none;">
        ${snippetHtml}
        ${rem ? `
          <div style="margin-top: 12px;">
            <p style="font-size: 12px; color: var(--fg-muted); margin-bottom: 4px; font-weight: 600;">Remediation Agent Recommendation:</p>
            <p style="font-size: 13.5px; color: var(--fg-subtle);">${rem.recommendation}</p>
            ${rem.bestPractice ? `<p style="font-size: 12.5px; color: var(--forest); margin-top: 4px;"><b>Best Practice:</b> ${rem.bestPractice}</p>` : ''}
            ${rem.correctedCode ? renderRemediationCodeBox(rem.correctedCode, f.id) : ''}
          </div>
        ` : ''}
      </div>
    </article>
  `;
}

function toggleCardDetail(id) {
  const el = document.getElementById(`detail-${id}`);
  const chev = document.getElementById(`chevron-${id}`);
  if (el) {
    if (el.style.display === "none") {
      el.style.display = "block";
      if (chev) chev.style.transform = "rotate(180deg)";
    } else {
      el.style.display = "none";
      if (chev) chev.style.transform = "none";
    }
  }
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

document.addEventListener("DOMContentLoaded", loadFindings);
