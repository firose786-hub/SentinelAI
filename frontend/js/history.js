/**
 * History Controller
 */

async function loadHistory() {
  const container = document.getElementById("history-content");
  if (!container) return;

  try {
    const res = await fetch("/api/analyses");
    const analyses = await res.json();

    if (!analyses || analyses.length === 0) {
      container.innerHTML = `
        <div class="panel" style="padding: 48px; text-align: center;">
          <svg style="width: 36px; height: 36px; color: var(--border-strong); margin: 0 auto 12px auto;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></polyline>
            <polyline points="12 6 12 12 14 14"></polyline>
          </svg>
          <h2 style="font-size: 18px; margin-bottom: 8px;">No history yet</h2>
          <p style="color: var(--fg-subtle); max-width: 400px; margin: 0 auto 20px auto; font-size: 13.5px;">
            Your past code review runs and reports will be saved here in persistent local storage.
          </p>
          <a href="/analysis.html" class="btn btn-primary">Run an analysis</a>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <p style="font-size: 13px; color: var(--fg-muted);">${analyses.length} inspection record${analyses.length > 1 ? 's' : ''} stored in persistent database.</p>
        <button type="button" class="btn btn-outline" onclick="clearAllHistory()" style="font-size: 12px; padding: 6px 12px;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 13px; height: 13px;"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
          Clear all
        </button>
      </div>

      <div class="panel" style="padding: 0; overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13.5px;">
          <thead>
            <tr style="border-bottom: 1px solid var(--border); color: var(--fg-muted); font-size: 12px;">
              <th style="padding: 14px 18px; font-weight: 600;">File</th>
              <th style="padding: 14px 12px; font-weight: 600;">Language</th>
              <th style="padding: 14px 12px; font-weight: 600;">Findings</th>
              <th style="padding: 14px 12px; font-weight: 600;">Health</th>
              <th style="padding: 14px 12px; font-weight: 600;">Verdict</th>
              <th style="padding: 14px 18px; text-align: right; font-weight: 600;">Actions</th>
            </tr>
          </thead>
          <tbody>
            ${analyses.map(a => {
              const findingsCount = a.securityFindings.length + a.qualityFindings.length;
              const dateStr = new Date(a.createdAt).toLocaleString();
              return `
                <tr style="border-bottom: 1px solid var(--border); transition: background-color 0.15s ease;">
                  <td style="padding: 14px 18px;">
                    <a href="/findings.html?id=${a.id}" onclick="localStorage.setItem('sentinel_current_id', '${a.id}')" style="font-family: var(--font-mono); font-weight: 600; font-size: 13px; color: var(--fg-main);">${a.submission.filename}</a>
                    <p style="font-size: 11px; color: var(--fg-muted); margin-top: 2px;">${dateStr}</p>
                  </td>
                  <td style="padding: 14px 12px;">
                    <span class="badge-tag">${a.submission.language}</span>
                  </td>
                  <td style="padding: 14px 12px; font-family: var(--font-mono);">${findingsCount}</td>
                  <td style="padding: 14px 12px; font-family: var(--font-mono); font-weight: 600;">${a.metrics.overallHealth}/100</td>
                  <td style="padding: 14px 12px;">${getVerdictBadge(a.summary.verdict)}</td>
                  <td style="padding: 14px 18px; text-align: right;">
                    <div style="display: inline-flex; gap: 6px;">
                      <a href="/findings.html?id=${a.id}" onclick="localStorage.setItem('sentinel_current_id', '${a.id}')" class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;" title="View inspection">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 13px; height: 13px;"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                      </a>
                      <button type="button" class="btn btn-outline" onclick="deleteHistoryItem('${a.id}')" style="padding: 4px 8px; font-size: 12px; color: var(--destructive);" title="Delete inspection">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 13px; height: 13px;"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                      </button>
                    </div>
                  </td>
                </tr>
              `;
            }).join("")}
          </tbody>
        </table>
      </div>
    `;
  } catch (err) {
    container.innerHTML = `<p style="color: var(--destructive);">Failed to load history: ${err.message}</p>`;
  }
}

async function deleteHistoryItem(id) {
  if (!confirm("Are you sure you want to delete this analysis record?")) return;
  try {
    const res = await fetch(`/api/analyses/${id}`, { method: "DELETE" });
    if (res.ok) {
      toast.success("Analysis deleted");
      loadHistory();
    }
  } catch (err) {
    toast.error("Failed to delete analysis");
  }
}

async function clearAllHistory() {
  if (!confirm("Are you sure you want to clear all analysis history?")) return;
  try {
    const res = await fetch("/api/analyses", { method: "DELETE" });
    if (res.ok) {
      toast.success("History cleared");
      localStorage.removeItem("sentinel_current_id");
      loadHistory();
    }
  } catch (err) {
    toast.error("Failed to clear history");
  }
}

document.addEventListener("DOMContentLoaded", loadHistory);
