/**
 * Reports Controller
 */

let currentRecord = null;

async function loadReportView() {
  const container = document.getElementById("report-content");
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
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
        </svg>
        <h2 style="font-size: 18px; margin-bottom: 8px;">No report available</h2>
        <p style="color: var(--fg-subtle); max-width: 400px; margin: 0 auto 20px auto; font-size: 13.5px;">
          Submit and analyze code to generate comprehensive PDF, Markdown, and JSON inspection reports.
        </p>
        <a href="/analysis.html" class="btn btn-primary">Run an analysis</a>
      </div>
    `;
    return;
  }

  const a = currentRecord;
  const allFindings = [...a.securityFindings, ...a.qualityFindings];
  const createdDate = new Date(a.createdAt).toLocaleString();

  container.innerHTML = `
    <div style="display: flex; gap: 10px; margin-bottom: 18px; flex-wrap: wrap;">
      <a href="/api/reports/${a.id}/markdown" class="btn btn-primary" download>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        Markdown Report
      </a>
      <a href="/api/reports/${a.id}/json" class="btn btn-outline" download>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        JSON Export
      </a>
      <a href="/api/reports/${a.id}/pdf" class="btn btn-secondary" download>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="15" y2="15"></line></svg>
        Download PDF Report
      </a>
      <button type="button" class="btn btn-outline" onclick="window.print()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Print / PDF
      </button>
    </div>

    <article class="panel" style="padding: 28px;">
      <header style="border-bottom: 1px solid var(--border); padding-bottom: 18px; margin-bottom: 20px;">
        <p style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-muted);">Code review report</p>
        <h2 style="font-family: var(--font-mono); font-size: 22px; margin-top: 4px;">${a.submission.filename}</h2>
        <div style="display: flex; gap: 12px; align-items: center; margin-top: 8px; font-size: 13px; color: var(--fg-subtle); flex-wrap: wrap;">
          ${getVerdictBadge(a.summary.verdict)}
          <span><b>Language:</b> ${a.submission.language}</span>
          <span><b>Lines:</b> ${a.submission.lineCount}</span>
          <span><b>Generated:</b> ${createdDate}</span>
        </div>
      </header>

      <section style="margin-bottom: 22px;">
        <h3 style="font-size: 15px; font-weight: 600; margin-bottom: 8px;">Executive overview</h3>
        <p style="font-size: 13.5px; color: var(--fg-subtle); line-height: 1.55;">${a.summary.executiveOverview}</p>
      </section>

      <section class="grid-4" style="margin-bottom: 22px;">
        <div class="panel" style="background-color: var(--bg-surface-2); padding: 14px;">
          <p style="font-size: 11px; color: var(--fg-muted);">Security Score</p>
          <p style="font-family: var(--font-display); font-size: 20px; font-weight: 700;">${a.metrics.securityScore}/100</p>
        </div>
        <div class="panel" style="background-color: var(--bg-surface-2); padding: 14px;">
          <p style="font-size: 11px; color: var(--fg-muted);">Code Quality</p>
          <p style="font-family: var(--font-display); font-size: 20px; font-weight: 700;">${a.metrics.qualityScore}/100</p>
        </div>
        <div class="panel" style="background-color: var(--bg-surface-2); padding: 14px;">
          <p style="font-size: 11px; color: var(--fg-muted);">Maintainability</p>
          <p style="font-family: var(--font-display); font-size: 20px; font-weight: 700;">${a.metrics.maintainabilityScore}/100</p>
        </div>
        <div class="panel" style="background-color: var(--bg-surface-2); padding: 14px;">
          <p style="font-size: 11px; color: var(--fg-muted);">Overall Health</p>
          <p style="font-family: var(--font-display); font-size: 20px; font-weight: 700;">${a.metrics.overallHealth}/100</p>
        </div>
      </section>

      <section style="margin-bottom: 22px;">
        <h3 style="font-size: 15px; font-weight: 600; margin-bottom: 8px;">Severity breakdown</h3>
        <div style="display: flex; gap: 14px; flex-wrap: wrap;">
          ${["Critical", "High", "Medium", "Low"].map(sev => `
            <div style="display: flex; align-items: center; gap: 6px;">
              ${getSeverityBadge(sev)}
              <span style="font-family: var(--font-mono); font-weight: 700;">${a.summary.severityBreakdown[sev] || 0}</span>
            </div>
          `).join("")}
        </div>
      </section>

      <section style="margin-bottom: 22px;">
        <h3 style="font-size: 15px; font-weight: 600; margin-bottom: 12px;">Findings (${allFindings.length})</h3>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          ${allFindings.map(f => `
            <div style="padding: 12px 14px; border-radius: var(--radius-md); border: 1px solid var(--border); background-color: var(--bg-surface-2);">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <span style="font-weight: 600; font-size: 14px;">${f.title}</span>
                ${getSeverityBadge(f.severity)}
              </div>
              <p style="font-size: 13px; color: var(--fg-subtle);">${f.detail}</p>
              <p style="font-size: 11px; font-family: var(--font-mono); color: var(--fg-muted); margin-top: 4px;">
                ${f.owaspCategory ? `${f.owaspCategory} · ${f.cwe} · ` : `${f.category} · `}
                ${f.line ? `line ${f.line}` : 'file-level'} · ${f.agent}
              </p>
            </div>
          `).join("")}
        </div>
      </section>

      <section style="margin-bottom: 22px;">
        <h3 style="font-size: 15px; font-weight: 600; margin-bottom: 8px;">Remediation roadmap</h3>
        <ol style="padding-left: 18px; font-size: 13.5px; color: var(--fg-subtle); display: flex; flex-direction: column; gap: 6px;">
          ${a.summary.prioritizedFixes.map(fix => `<li>${fix}</li>`).join("")}
        </ol>
      </section>

      <footer style="padding-top: 14px; border-top: 1px solid var(--border); font-size: 11px; color: var(--fg-muted);">
        Generated by Smart Code Inspection Platform with Vulnerability Detection System — Group 2. Grounded in: ${a.knowledgeCitations.join("; ")}
      </footer>
    </article>
  `;
}

document.addEventListener("DOMContentLoaded", loadReportView);
