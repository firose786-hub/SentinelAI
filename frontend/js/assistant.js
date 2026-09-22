/**
 * Conversational Assistant Controller
 */

let chatHistory = [];

const SUGGESTIONS = [
  "Why is string concatenation in SQL dangerous?",
  "How do I fix the embedded credential finding?",
  "Explain OWASP A01 broken access control",
  "What should replace MD5 for password hashing?",
];

async function initAssistant() {
  const container = document.getElementById("chat-messages");
  const suggestionsContainer = document.getElementById("suggestions-chips");
  const current = await getCurrentAnalysis();

  const contextNote = document.getElementById("assistant-context-note");
  if (contextNote) {
    if (current) {
      contextNote.textContent = `Grounded in knowledge base & current analysis of ${current.submission.filename}.`;
    } else {
      contextNote.textContent = "Grounded in the indexed OWASP & secure coding knowledge base.";
    }
  }

  // Load stored API key indicator & input
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
        toast.success("Gemini API key saved! Real-time AI enabled.");
        if (apiKeyPanel) apiKeyPanel.style.display = "none";
      } else {
        localStorage.removeItem("sentinel_gemini_api_key");
        toast.info("Using default local RAG engine.");
      }
      updateApiKeyBadge();
    });
  }

  if (clearKeyBtn && inlineInput) {
    clearKeyBtn.addEventListener("click", () => {
      localStorage.removeItem("sentinel_gemini_api_key");
      inlineInput.value = "";
      toast.info("Gemini API key removed. Using local RAG.");
      updateApiKeyBadge();
    });
  }

  if (suggestionsContainer) {
    suggestionsContainer.innerHTML = SUGGESTIONS.map(s => `
      <button type="button" class="btn btn-outline suggestion-btn" style="border-radius: 9999px; font-size: 12px; padding: 6px 14px;">
        ${s}
      </button>
    `).join("");

    document.querySelectorAll(".suggestion-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const text = btn.textContent.trim();
        document.getElementById("chat-input").value = text;
        sendQuestion();
      });
    });
  }

  const form = document.getElementById("chat-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      sendQuestion();
    });
  }

  const clearBtn = document.getElementById("clear-chat-btn");
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      chatHistory = [];
      renderChat();
    });
  }
}

function updateApiKeyBadge() {
  const badge = document.getElementById("gemini-status-badge");
  if (!badge) return;
  const stored = localStorage.getItem("sentinel_gemini_api_key");
  if (stored) {
    badge.innerHTML = `<span style="color: var(--forest); font-weight: 600; background-color: var(--forest-soft); padding: 2px 8px; border-radius: 9999px;">● Gemini Real-Time Active</span>`;
  } else {
    badge.innerHTML = `<span style="color: var(--fg-muted); background-color: var(--bg-surface-2); padding: 2px 8px; border-radius: 9999px;">● Local Knowledge Base RAG</span>`;
  }
}

async function sendQuestion() {
  const input = document.getElementById("chat-input");
  const question = input.value.trim();
  if (!question) return;

  input.value = "";
  chatHistory.push({ role: "user", content: question });
  renderChat(true);

  const current = await getCurrentAnalysis();
  let analysisContext = null;
  if (current) {
    analysisContext = `File ${current.submission.filename} (${current.submission.language}). Verdict: ${current.summary.verdict}. Security findings: ${current.securityFindings.map(f => f.title).join(", ")}.`;
  }

  const apiKey = localStorage.getItem("sentinel_gemini_api_key") || undefined;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        history: chatHistory.slice(-8).map(m => ({ role: m.role, content: m.content })),
        analysisContext,
        apiKey,
      }),
    });

    if (!res.ok) throw new Error("Assistant response failed");
    const data = await res.json();

    chatHistory.push({
      role: "assistant",
      content: data.answer,
      citations: data.citations || [],
      engine: data.engine || "RAG Knowledge Base",
    });
  } catch (err) {
    chatHistory.push({
      role: "assistant",
      content: `Sorry, could not complete the request: ${err.message}`,
      citations: [],
    });
  } finally {
    renderChat(false);
  }
}

function renderChat(isLoading = false) {
  const container = document.getElementById("chat-messages");
  const suggestionsBox = document.getElementById("suggestions-box");
  if (!container) return;

  if (chatHistory.length === 0 && !isLoading) {
    if (suggestionsBox) suggestionsBox.style.display = "block";
    container.innerHTML = "";
    return;
  }

  if (suggestionsBox) suggestionsBox.style.display = "none";

  container.innerHTML = chatHistory.map(m => {
    const isUser = m.role === "user";
    return `
      <div style="display: flex; justify-content: ${isUser ? 'flex-end' : 'flex-start'}; margin-bottom: 14px;">
        <div style="max-width: 82%; padding: 12px 16px; border-radius: ${isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px'}; background-color: ${isUser ? 'var(--primary)' : 'var(--bg-surface-2)'}; color: ${isUser ? 'var(--primary-fg)' : 'var(--fg-main)'}; border: 1px solid ${isUser ? 'transparent' : 'var(--border)'}; font-size: 13.5px; line-height: 1.5;">
          ${m.engine && !isUser ? `
            <div style="font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--fg-muted); margin-bottom: 4px; font-weight: 600;">
              ${m.engine}
            </div>
          ` : ''}
          <div>${formatMessageMarkdown(m.content)}</div>
          ${m.citations && m.citations.length ? `
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid var(--border); font-size: 11px; color: var(--fg-muted);">
              <p style="font-weight: 600; margin-bottom: 2px;">Retrieved Sources:</p>
              <ul style="padding-left: 14px;">
                ${m.citations.map(c => `<li>${c}</li>`).join("")}
              </ul>
            </div>
          ` : ''}
        </div>
      </div>
    `;
  }).join("");

  if (isLoading) {
    container.innerHTML += `
      <div style="display: flex; justify-content: flex-start; margin-bottom: 14px;">
        <div style="padding: 10px 14px; border-radius: 16px; background-color: var(--bg-surface-2); color: var(--fg-muted); border: 1px solid var(--border); font-size: 13px; display: flex; align-items: center; gap: 8px;">
          <svg style="width: 14px; height: 14px; animation: spin 1s linear infinite;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line></svg>
          Retrieving knowledge & generating answer…
        </div>
      </div>
    `;
  }

  container.scrollTop = container.scrollHeight;
}

function formatMessageMarkdown(text) {
  let formatted = text.replace(/```([a-zA-Z]*)\n([\s\S]*?)```/g, (match, lang, code) => {
    return `<div class="code-container"><div class="code-header"><span>${lang || 'CODE'}</span></div><div class="code-body">${escapeHtml(code.trim())}</div></div>`;
  });
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");
  formatted = formatted.replace(/\n\n/g, "<br/><br/>").replace(/\n/g, "<br/>");
  return formatted;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

document.addEventListener("DOMContentLoaded", initAssistant);
