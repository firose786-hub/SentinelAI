# SentinelAI — End-to-End Enterprise User Guide & Command Center Walkthrough

**Project**: *SentinelAI — Agentic AI-Based Smart Compliance Auditor & AI Security Validation Platform for Enterprise LLM Systems*  
**Platform**: SentinelAI Enterprise SOC v3.0  
**Target URL**: `http://localhost:8501`  

---

## 1. Enterprise Login Gate & Persona Selection

Upon opening `http://localhost:8501`, SentinelAI enforces an **Enterprise Authentication Gatekeeper**.

### 1-Click Quick Demo Login Cards:
For frictionless faculty review and viva demonstrations, 6 pre-configured persona cards are provided directly on the login screen. Click any card to auto-fill credentials:

| Persona Role | User Account | Password | Hardware MFA TOTP | Authorized Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin` | `749201` | Full administrative control, user role management, system diagnostics. |
| **CISO Executive** | `ciso` | `ciso` | `749201` | Financial liability models ($5M–$12M), downtime risk, board PDF reports. |
| **Compliance Officer**| `compliance`| `compliance` | `749201` | ISO 27001 Annex A, NIST CSF 2.0 controls, gap analysis. |
| **AI Security Engineer**| `ai_engineer`| `engineer` | `749201` | 14 Defense toggles, Prompt Injection testbed, cloud API allowlists. |
| **SOC Analyst** | `soc_analyst`| `analyst` | `749201` | Real-time threat feed, Red vs Blue Arena, Judge rulings. |
| **External Auditor** | `auditor` | `auditor` | `749201` | Read-only evidence trail, SHA-256 certificate validation. |

---

## 2. Navigating the 13 Command Center Pages

Once authenticated, use the **Sidebar Enclave Persona Switcher** (`🎭 Switch Persona`) or the page dropdown to navigate:

### 1. 🛡️ Executive SOC Overview
- **Header**: Live SOC Pulse Beacon, Active Organization, Model Specification.
- **KPI Metrics**: Overall Compliance Score, AI Security Score, Composite Risk Score, Total Findings.
- **Visuals**: Radar Chart comparing ISO vs. NIST vs. OWASP dimensions; Financial Exposure Card ($5M–$12M range).

### 2. 👔 CISO Executive Dashboard
- **Target Audience**: Chief Information Security Officer & Board of Directors.
- **Features**: Plain-English executive synthesis, estimated downtime hours, financial liability breakdown, and instant 1-click **Download CISO Executive Board PDF**.

### 3. 📋 GRC Compliance Dashboard (ISO 27001 & NIST CSF)
- **Features**: Filter by framework (`ISO/IEC 27001:2022`, `NIST CSF 2.0`), search controls, view evidence trails, and identify regulatory gaps with color-coded status badges (`Compliant`, `Partially Compliant`, `Non-Compliant`).

### 4. 🧪 AI Security Lab & Attack Testbed (AI Engineer)
- **Interactive Defense Toggles**: 14 switches (Semantic Prompt Firewall, Output Token DLP, Human-in-the-Loop for Tools, Secrets KMS, SIEM Logging).
- **Testbed Tabs**:
  - `💉 Prompt Injection (LLM01)`: Input an adversarial prompt (e.g. *"System override..."*) -> Click **Simulate Attack Payload** -> View mathematical cosine trigger score and sanitized output.
  - `🔓 Jailbreak Persona Hijack`: Inspect DAN mode attack vectors and Red Team observations.
  - `🕵️ Sensitive Data Leakage (LLM06)`: Test PII redaction and PCI credit card token masking.
  - `⚙️ Insecure Plugin / Tool (LLM08)`: Test outbound URL against enterprise cloud API allowlists.

### 5. 🚨 SOC Operations & Red vs Blue Deliberation Arena (SOC Analyst)
- **Features**: Real-time threat feed, severity distribution charts, and the **AI Debate Arena** where the Red Team (Skeptic) and Blue Team (Advocate) contest findings round-by-round under the Judge Agent's binding ruling.

### 6. 📑 External Auditor Portal (External Auditor)
- **Features**: Read-only immutable view, Ground-Truth evidence trail, and cryptographic **SHA-256 Certificate Fingerprint** validation block ensuring reports cannot be forged or tampered with.

### 7. 🛠️ Admin Console & Diagnostics (Super Admin)
- **Features**: Manage user seats, assign RBAC roles (`Super Admin`, `CISO`, `Compliance Officer`, etc.), inspect 12-agent system health, and view live SIEM security logs.

### 8. 📄 Reports & Downloads
- **Features**:
  - **Download Publication-Grade PDF**: High-resolution ReportLab document with executive summary, radar charts, findings tables, and cryptographic certificate block.
  - **Download Styled Excel Workbook (`.xlsx`)**: Multi-sheet workbook formatted via OpenPyXL.
  - **Download JSON & Markdown**: Complete machine-readable audit datasets.

---

## 3. Running a Custom Audit on Your Own Organization

1. Navigate to **🏢 Organizations & Profiles**.
2. Select an existing enterprise (`Apex Wealth FinTech`, `BioCare Health Systems`, `RetailPulse E-Commerce`, `IronShield Aerospace Defense`) or click **"Create Custom Organization"**.
3. Fill in Organization Name, Industry, AI Model used (e.g. Gemini, GPT-4, Llama-3), and adjust the 14 security control toggles.
4. Click **"🚀 Apply Controls & Run 12-Agent Audit"**.
5. The 12 agents execute in sequence (Policy -> Compliance -> Red Team -> Blue Team -> Judge -> Debate -> Decision -> Risk -> Forecast -> Roadmap -> Memory -> CEO -> Report).
6. The entire Command Center refreshes dynamically with custom compliance scores, financial exposures, and downloadable reports!
