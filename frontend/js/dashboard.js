/**
 * Dashboard Controller
 */

async function loadDashboard() {
  const container = document.getElementById("dashboard-content");
  if (!container) return;

  try {
    const [statsRes, historyRes] = await Promise.all([
      fetch("/api/stats"),
      fetch("/api/analyses"),
    ]);

    const stats = await statsRes.json();
    const history = await historyRes.json();

    if (!stats || stats.totalAnalyses === 0) {
      container.innerHTML = `
        <div class="panel" style="padding: 48px; text-align: center;">
          <svg style="width: 36px; height: 36px; color: var(--border-strong); margin: 0 auto 12px auto;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          <h2 style="font-size: 18px; margin-bottom: 8px;">No inspections yet</h2>
          <p style="color: var(--fg-subtle); max-width: 440px; margin: 0 auto 20px auto; font-size: 13.5px;">
            Submit a Python or Java file and the multi-agent pipeline will produce severity-scored findings, remediation examples and a pull-request review.
          </p>
          <a href="/analysis.html" class="btn btn-primary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
            Run your first analysis
          </a>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div class="grid-4" style="margin-bottom: 20px;">
        <div class="panel" style="display: flex; align-items: center; gap: 16px; padding: 18px;">
          ${renderScoreGauge(stats.security, 54)}
          <div>
            <p style="font-size: 12px; color: var(--fg-muted);">Avg security score</p>
            <p style="font-family: var(--font-display); font-size: 22px; font-weight: 700;">${stats.security}</p>
          </div>
        </div>
        <div class="panel" style="display: flex; align-items: center; gap: 16px; padding: 18px;">
          ${renderScoreGauge(stats.quality, 54)}
          <div>
            <p style="font-size: 12px; color: var(--fg-muted);">Avg code quality</p>
            <p style="font-family: var(--font-display); font-size: 22px; font-weight: 700;">${stats.quality}</p>
          </div>
        </div>
        <div class="panel" style="display: flex; align-items: center; gap: 16px; padding: 18px;">
          ${renderScoreGauge(stats.maintainability, 54)}
          <div>
            <p style="font-size: 12px; color: var(--fg-muted);">Avg maintainability</p>
            <p style="font-family: var(--font-display); font-size: 22px; font-weight: 700;">${stats.maintainability}</p>
          </div>
        </div>
        <div class="panel" style="display: flex; align-items: center; gap: 16px; padding: 18px;">
          ${renderScoreGauge(stats.health, 54)}
          <div>
            <p style="font-size: 12px; color: var(--fg-muted);">Overall code health</p>
            <p style="font-family: var(--font-display); font-size: 22px; font-weight: 700;">${stats.health}</p>
          </div>
        </div>
      </div>

      <div class="grid-split">
        <section class="panel">
          <div class="panel-header">
            <h2 class="panel-title">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
              Recent inspections
            </h2>
          </div>
          <div style="display: flex; flex-direction: column; divide-y: 1px solid var(--border);">
            ${history.slice(0, 6).map(h => `
              <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border);">
                <div>
                  <a href="/findings.html?id=${h.id}" onclick="localStorage.setItem('sentinel_current_id', '${h.id}')" style="font-weight: 600; font-family: var(--font-mono); font-size: 13.5px;">${h.submission.filename}</a>
                  <span style="font-size: 12px; color: var(--fg-muted);"> · ${h.submission.language}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                  ${getVerdictBadge(h.summary.verdict)}
                  <a href="/findings.html?id=${h.id}" onclick="localStorage.setItem('sentinel_current_id', '${h.id}')" class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;">View</a>
                </div>
              </div>
            `).join("")}
          </div>
        </section>

        <section class="panel">
          <div class="panel-header">
            <h2 class="panel-title">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
              Severity distribution
            </h2>
          </div>
          <div style="display: flex; flex-direction: column; gap: 12px;">
            ${stats.counts.map(c => {
              const total = stats.totalFindings || 1;
              const pct = stats.totalFindings ? Math.round((c.count / total) * 100) : 0;
              let barColor = "#2F7A59";
              if (c.severity === "Critical" || c.severity === "High") barColor = "#BD3429";
              else if (c.severity === "Medium") barColor = "#B36B15";

              return `
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; font-size: 12px;">
                    ${getSeverityBadge(c.severity)}
                    <span style="font-family: var(--font-mono); color: var(--fg-subtle);">${c.count}</span>
                  </div>
                  <div style="height: 6px; background-color: var(--bg-surface-2); border-radius: 9999px; overflow: hidden;">
                    <div style="height: 100%; width: ${pct}%; background-color: ${barColor}; border-radius: 9999px;"></div>
                  </div>
                </div>
              `;
            }).join("")}
          </div>
          <p style="margin-top: 20px; font-size: 13px; color: var(--fg-subtle); line-height: 1.45;">
            ${stats.totalFindings} findings raised across ${stats.totalAnalyses} inspection${stats.totalAnalyses > 1 ? "s" : ""}.
          </p>
          <div style="display: flex; gap: 8px; margin-top: 18px;">
            <a href="/analysis.html" class="btn btn-primary" style="flex: 1;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
              New analysis
            </a>
            <a href="/knowledge-base.html" class="btn btn-outline" title="Knowledge base">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
            </a>
          </div>
        </section>
      </div>
    `;
  } catch (err) {
    container.innerHTML = `<p style="color: var(--destructive);">Failed to load dashboard: ${err.message}</p>`;
  }
}

document.addEventListener("DOMContentLoaded", loadDashboard);
