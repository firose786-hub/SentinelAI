/**
 * Knowledge Base Controller
 */

let allDocs = [];
let activeDocId = null;

async function loadKnowledgeBase() {
  const listContainer = document.getElementById("kb-docs-list");
  const detailContainer = document.getElementById("kb-doc-detail");
  const searchInput = document.getElementById("kb-search-input");
  const countLabel = document.getElementById("kb-stats-count");

  if (!listContainer || !detailContainer) return;

  try {
    const res = await fetch("/api/knowledge");
    allDocs = await res.json();

    if (countLabel) {
      countLabel.textContent = `${allDocs.length} indexed documents · retrieved by the TF-IDF vector index at analysis and chat time.`;
    }

    if (allDocs.length > 0) {
      activeDocId = allDocs[0].id;
    }

    renderDocsList(allDocs);
    renderDocDetail();

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        const q = e.target.value.trim().toLowerCase();
        const filtered = allDocs.filter(d => 
          d.title.toLowerCase().includes(q) ||
          d.tags.some(t => t.toLowerCase().includes(q)) ||
          d.body.toLowerCase().includes(q)
        );
        renderDocsList(filtered);
        if (filtered.length > 0 && !filtered.some(d => d.id === activeDocId)) {
          activeDocId = filtered[0].id;
        }
        renderDocDetail();
      });
    }
  } catch (err) {
    listContainer.innerHTML = `<p style="color: var(--destructive); padding: 12px;">Failed to load knowledge base: ${err.message}</p>`;
  }
}

function renderDocsList(docs) {
  const container = document.getElementById("kb-docs-list");
  if (!container) return;

  if (docs.length === 0) {
    container.innerHTML = `<p style="padding: 16px; font-size: 13px; color: var(--fg-muted);">No documents match your query.</p>`;
    return;
  }

  container.innerHTML = docs.map(d => `
    <button type="button" class="kb-item-btn ${d.id === activeDocId ? 'active' : ''}" onclick="selectDoc('${d.id}')" style="width: 100%; text-align: left; padding: 12px 14px; border-radius: var(--radius-md); border: 1px solid ${d.id === activeDocId ? 'var(--primary)' : 'var(--border)'}; background-color: ${d.id === activeDocId ? 'var(--accent)' : 'var(--bg-surface)'}; margin-bottom: 6px; cursor: pointer; transition: all 0.15s ease;">
      <p style="font-size: 13.5px; font-weight: 600; color: ${d.id === activeDocId ? 'var(--accent-fg)' : 'var(--fg-main)'};">${d.title}</p>
      <p style="font-size: 11px; color: var(--fg-muted); margin-top: 3px;">${d.source}</p>
    </button>
  `).join("");
}

function selectDoc(id) {
  activeDocId = id;
  const searchInput = document.getElementById("kb-search-input");
  const q = searchInput ? searchInput.value.trim().toLowerCase() : "";
  const filtered = q ? allDocs.filter(d => 
    d.title.toLowerCase().includes(q) ||
    d.tags.some(t => t.toLowerCase().includes(q)) ||
    d.body.toLowerCase().includes(q)
  ) : allDocs;

  renderDocsList(filtered);
  renderDocDetail();
}

function renderDocDetail() {
  const container = document.getElementById("kb-doc-detail");
  if (!container) return;

  const doc = allDocs.find(d => d.id === activeDocId);
  if (!doc) {
    container.innerHTML = `<p style="padding: 24px; color: var(--fg-muted);">Select a document from the list.</p>`;
    return;
  }

  const paragraphs = doc.body.split("\n").filter(Boolean);

  container.innerHTML = `
    <article class="panel">
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
        <svg style="width: 20px; height: 20px; color: var(--primary);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
        <h2 style="font-size: 18px; font-weight: 700;">${doc.title}</h2>
      </div>
      <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 16px;">
        <span class="badge-tag" style="background-color: var(--accent); color: var(--accent-fg); font-weight: 600;">${doc.source}</span>
        ${doc.tags.map(t => `<span class="badge-tag">${t}</span>`).join("")}
      </div>
      <div style="display: flex; flex-direction: column; gap: 12px; font-size: 13.5px; line-height: 1.6; color: var(--fg-subtle);">
        ${paragraphs.map(p => `<p>${p}</p>`).join("")}
      </div>
    </article>
  `;
}

document.addEventListener("DOMContentLoaded", loadKnowledgeBase);
