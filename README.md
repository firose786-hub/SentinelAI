# SentinelAI: Agentic AI-Based Smart Compliance Auditor & AI Security Validation Platform for Enterprise LLM Systems

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.110-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit%201.32-FF4B4B.svg)](https://streamlit.io/)
[![OWASP LLM](https://img.shields.io/badge/Security-OWASP%20Top%2010%20LLM-critical.svg)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
[![ISO/NIST](https://img.shields.io/badge/Compliance-ISO%2027001%20%26%20NIST%20CSF-informational.svg)](https://www.nist.gov/cyberframework)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Table of Contents

1. [Executive Abstract](#-executive-abstract)
2. [Problem Statement & Research Gap](#-problem-statement--research-gap)
3. [Proposed System Overview](#-proposed-system-overview)
4. [Novel & Unique Contributions](#-novel--unique-contributions)
5. [System & Multi-Agent Architecture](#-system--multi-agent-architecture)
6. [Agent Specifications & Responsibilities](#-agent-specifications--responsibilities)
7. [The AI Debate Engine Mechanism](#-the-ai-debate-engine-mechanism)
8. [Standards Compliance & OWASP LLM Validation](#-standards-compliance--owasp-llm-validation)
9. [Mathematical Models: Forecast, Memory & Financial Exposure](#-mathematical-models)
10. [Technology Stack](#-technology-stack)
11. [Database Design & Schemas](#-database-design--schemas)
12. [REST API Documentation](#-rest-api-documentation)
13. [Installation & Quickstart Guide](#-installation--quickstart-guide)
14. [Streamlit 9-Tab Dashboard Walkthrough](#-streamlit-9-tab-dashboard-walkthrough)
15. [Experimental Test Organizations & Empirical Results](#-experimental-test-organizations--empirical-results)
16. [Research Limitations & Compliance Disclaimers](#-research-limitations--compliance-disclaimers)
17. [Ethical & Safety Considerations](#-ethical--safety-considerations)
18. [Future Enhancements & Roadmap](#-future-enhancements--roadmap)
19. [Conclusion](#-conclusion)

---

## 🔬 Executive Abstract

The rapid enterprise adoption of Artificial Intelligence (AI) and Large Language Model (LLM)-based agents has introduced complex cybersecurity vulnerabilities alongside strict regulatory compliance requirements. Organizations must satisfy established frameworks such as **ISO/IEC 27001:2022** and the **NIST Cybersecurity Framework (CSF) 2.0** while simultaneously defending production LLM applications against novel attack surfaces including prompt injection, jailbreaking, sensitive credential leakage, and autonomous agent privilege escalation.

Traditional compliance auditing tools and AI application security scanners operate in isolated silos, failing to provide unified governance, collaborative multi-agent reasoning, predictive improvement forecasting, or plain-English executive translation.

**SentinelAI** bridges this research gap by proposing an **Agentic AI-Based Smart Compliance Auditor & AI Security Validation Platform**. The platform integrates:
- Automated ISO/IEC 27001 and NIST CSF compliance checking.
- Adversarial AI security validation grounded in the **OWASP Top 10 for LLM Applications (2025/2026)**.
- A transparent, multi-turn **AI Debate Engine** where Red Team (Skeptic) and Blue Team (Advocate) agents contest findings under an impartial Judge Agent.
- A **Compliance Forecast Agent** modeling 30/60/90-day trajectory gains.
- A longitudinal **Memory Agent** tracking score evolution and recurring persistent vulnerabilities across audit cycles.
- A **CEO Mode & Business Impact Engine** translating complex telemetry into plain English and quantitative financial exposure models.

The system is implemented in Python using **FastAPI**, **Streamlit**, **SQLite**, **ReportLab**, and **Google Gemini API** with robust deterministic offline fallbacks.

---

## 🎯 Problem Statement & Research Gap

### Problem Statement
Enterprise LLM deployments present dual challenges:
1. **Regulatory Compliance Uncertainty**: Traditional IT audits do not account for probabilistic, non-deterministic generative AI interfaces.
2. **Emergent Adversarial Attack Vectors**: Prompt injections, tool abuse, and vector database poisoning bypass legacy network firewalls.
3. **Communication Friction**: Technical CVSS scores fail to communicate actionable business risk or financial exposure to C-suite executives.

### Research Gap in Existing Solutions
| Existing Paradigm | Typical Limitation | SentinelAI Contribution |
| :--- | :--- | :--- |
| **Traditional GRC Platforms** (e.g., ServiceNow, OneTrust) | Static checklists; no LLM threat awareness; manual evidence collection. | Real-time automated ISO/NIST control evaluation combined with active LLM validation. |
| **Standalone LLM Red-Teaming Tools** (e.g., Garak, PyRIT) | Focus purely on attack simulation; lack regulatory mapping or governance verdicts. | Integrates adversarial red-teaming directly into ISO/NIST compliance scoring and debate. |
| **Single-Agent Auditing Scripts** | Prone to LLM hallucination and single-perspective bias. | Adversarial **AI Debate Engine** (Red vs. Blue vs. Judge) ensuring balanced consensus. |
| **Static PDF Review Tools** | Point-in-time snapshot with no temporal learning across audits. | **Memory Agent** detecting recurring vulnerabilities across audit history with longitudinal diffs. |
| **Technical Vulnerability Scanners** | Jargon-heavy outputs inaccessible to executive decision makers. | **CEO Mode** with plain English synthesis, downtime estimation, and financial exposure ranges. |

---

## 💡 Proposed System Overview

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Enterprise Profile & LLM Ingest                 │
│         (Fintech, HealthCare, Retail SaaS, Defense, Custom Submissions)│
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        Multi-Agent Governance Pipeline                 │
│  [Policy Agent] ──► [Compliance Agent (ISO/NIST)] ──► [Risk Agent]     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Adversarial Security Validation                   │
│  [Red Team Agent: OWASP LLM Attacks] ◄──► [Blue Team Agent: Guardrails]│
│                                   │                                    │
│                                   ▼                                    │
│                    [Judge Agent: OWASP LLM Classifier]                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Collaborative Consensus Layer                     │
│  [AI Debate Engine (Skeptic vs. Advocate)] ──► [Decision Agent]        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Predictive & Longitudinal Insights                │
│  [Forecast Agent]  │  [Roadmap Agent]  │  [Memory Agent]  │  [CEO Mode]│
│  (30/60/90 Days)   │   (P1/P2/P3 Plan) │ (Audit Delta &)  │ (Impact &) │
│                    │                   │ (Recurrence)     │ (Downtime) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    Executive Presentation & Export                     │
│  • 9-Tab Streamlit SaaS Dashboard   • ReportLab PDF Report             │
│  • RESTful FastAPI OpenAPI Engine   • Structured JSON & Markdown       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Novel & Unique Contributions

1. **Multi-Agent Compliance Checking**: Evaluates operational evidence against simplified **ISO/IEC 27001:2022** controls and **NIST Cybersecurity Framework 2.0** categories.
2. **Adversarial AI Debate Engine**: Unique 3-party debate mechanism where Red Team (Skeptic) and Blue Team (Advocate) contest each finding, moderated by an impartial Judge Agent to issue binding verdicts (`APPROVED`, `APPROVED WITH REMEDIATION`, `HIGH RISK`, `CRITICAL RISK`).
3. **Safe Simulated OWASP LLM Attack Validation**: Automated probing for Prompt Injection (LLM01), Sensitive Data Disclosure (LLM02), Supply Chain Poisoning (LLM03), Output Handling (LLM05), Excessive Agency (LLM06), System Prompt Leakage (LLM07), Vector Weaknesses (LLM08), and Model DoS (LLM10).
4. **Compliance Forecast Agent**: Predictive model projecting organizational posture at 30, 60, and 90-day milestones with confidence intervals based on remediation velocity.
5. **Automated Remediation Roadmap**: Prioritized action plan categorizing engineering actions into **P1 (1-14 days)**, **P2 (15-45 days)**, and **P3 (46-90 days)** with assigned teams and expected point gains.
6. **Audit Memory Agent**: SQLite-backed longitudinal intelligence calculating score deltas ($+X$ points) and tracking persistent, recurring vulnerabilities across consecutive audit cycles.
7. **CEO Mode & Quantitative Business Impact Engine**: Jargon-free executive synthesis paired with an empirical financial exposure model (estimated downtime hours and revenue-scaled liability range).
8. **Deterministic Offline Architecture**: Fully operable in isolated, air-gapped environments with offline rule engines, while seamlessly leveraging Google Gemini 2.5 Flash when API credentials are provided.

---

## 🏛️ System & Multi-Agent Architecture

```
                                  ORGANIZATION PROFILE
                                           │
                                           ▼
                                 ┌───────────────────┐
                                 │   Policy Agent    │
                                 └─────────┬─────────┘
                                           ▼
                                 ┌───────────────────┐
                                 │ Compliance Agent  │ ──► [ISO 27001 Score]
                                 └─────────┬─────────┘ ──► [NIST CSF Score]
                                           ▼
                                 ┌───────────────────┐
                                 │    Risk Agent     │ ──► [Risk Score 0-100]
                                 └─────────┬─────────┘
                                           ▼
                 ┌───────────────────────────────────────────────────┐
                 │       ADVERSARIAL SECURITY VALIDATION ENGINE      │
                 │                                                   │
                 │   ┌───────────────────┐   ┌───────────────────┐   │
                 │   │  Red Team Agent   ├──►│  Blue Team Agent  │   │
                 │   │ (OWASP LLM Atks)  │   │ (Defenses & WAF)  │   │
                 │   └─────────┬─────────┘   └─────────┬─────────┘   │
                 │             │                       │             │
                 │             └───────────┬───────────┘             │
                 │                         ▼                         │
                 │               ┌───────────────────┐               │
                 │               │    Judge Agent    │ ──► [AI Sec Score]
                 │               └───────────────────┘               │
                 └─────────────────────────┬─────────────────────────┘
                                           ▼
                                 ┌───────────────────┐
                                 │ AI Debate Engine  │ (Skeptic vs Advocate)
                                 └─────────┬─────────┘
                                           ▼
                                 ┌───────────────────┐
                                 │  Decision Agent   │ ──► [Formal Verdict]
                                 └─────────┬─────────┘
        ┌──────────────────┬───────────────┼───────────────┬──────────────────┐
        ▼                  ▼               ▼               ▼                  ▼
┌───────────────┐  ┌───────────────┐ ┌───────────┐ ┌───────────────┐  ┌───────────────┐
│Forecast Agent │  │ Roadmap Agent │ │Memory Agt │ │ CEO & Impact  │  │ Report Agent  │
│(30/60/90 Days)│  │ (P1-P3 Matrix)│ │(Hist Diff)│ │(Plain English)│  │ (PDF/JSON/MD) │
└───────────────┘  └───────────────┘ └───────────┘ └───────────────┘  └───────────────┘
```

---

## 🤖 Agent Specifications & Responsibilities

| Agent Name | Primary Responsibility | Input Payload | Output Artifact | Rationale for Existence |
| :--- | :--- | :--- | :--- | :--- |
| **Policy Agent** | Interprets security charters and system boundaries | Organization Profile & Docs | Structured standard scopes | Establishes in-scope baseline requirements |
| **Compliance Agent** | Evaluates controls against ISO 27001 & NIST CSF 2.0 | Policy mappings & telemetry | Control status, Evidence, Gaps, Scores | Quantifies formal governance compliance |
| **Risk Agent** | Models multi-dimensional cyber exposure | Control gaps & AI findings | Risk Score (0-100), Risk Tier, Drivers | Synthesizes threat likelihood and impact |
| **Red Team Agent** | Simulates adversarial OWASP LLM attack vectors | LLM System config & interfaces | Attack findings & bypass observations | Discovers empirical security vulnerabilities |
| **Blue Team Agent** | Assesses guardrails, DLP, and compensating controls | Red findings & existing controls | Defensive arguments & residual risks | Prevents false positives by evaluating defenses |
| **Judge Agent** | Impartial arbiter mapping findings to OWASP LLM | Red attacks & Blue defenses | OWASP LLM findings & AI Security Score | Provides standardized objective adjudication |
| **AI Debate Engine** | Coordinates adversarial multi-turn reasoning | Red findings, Blue defenses, Judge | Multi-turn debate transcripts | Eliminates single-agent bias via debate |
| **Decision Agent** | Authorizes final regulatory & governance verdict | Debate outcome & scores | Verdict & Deployment Clearance Mandate | Produces definitive compliance determination |
| **Forecast Agent** | Projects 30/60/90-day posture trajectories | Current score & Roadmap items | Predicted scores & confidence metrics | Enables proactive resource planning |
| **Roadmap Agent** | Produces step-by-step P1/P2/P3 mitigation matrix | Gaps & Confirmed vulnerabilities | Prioritized engineering action plan | Translates findings into technical fixes |
| **Memory Agent** | Tracks audit history and recurring vulnerabilities | Current audit & SQLite records | Longitudinal score delta & recurring flaws | Detects persistent unpatched security risks |
| **CEO Agent** | Translates technical telemetry to plain English | Audit findings & annual revenue | Executive summary & financial exposure | Bridges communication gap for C-suite |
| **Report Agent** | Compiles multi-format documentation | Full Audit Record payload | ReportLab PDF, Markdown, JSON | Generates formal auditable artifacts |

---

## ⚖️ The AI Debate Engine Mechanism

The **AI Debate Engine** is a signature capability of SentinelAI. Rather than relying on a single heuristic or static threshold, the platform stages an adversarial dialogue:

```
[Round 1: Red Team (Skeptic)]
  • Asserts why the enterprise LLM system is UNSAFE.
  • Highlights active Critical/High exploits (e.g., unmitigated Prompt Injection or Excessive Agency).
  • Argues for deployment rejection or severe operational restrictions.

[Round 2: Blue Team (Advocate)]
  • Defends the organization's existing baseline controls (MFA, encryption, audit logs).
  • Highlights compensating mechanisms that contain blast radius.
  • Argues for conditional approval with targeted remediation.

[Round 3: Judge Agent (Moderator)]
  • Weighs empirical exploit evidence against demonstrated defenses.
  • Formulates final ruling based on severity weighting.
  • Issues one of four binding verdicts:
      1. APPROVED (Score > 85%, 0 Critical/High vulns)
      2. APPROVED WITH REMEDIATION (Score > 65%, 0 Critical vulns, minor gaps)
      3. HIGH RISK (Score < 65% or >= 1 Critical vuln)
      4. CRITICAL RISK (Score < 40% or >= 2 Critical vulns)
```

---

## 🛡️ Standards Compliance & OWASP LLM Validation

### 1. ISO/IEC 27001:2022 Control Coverage
- **ISO-A.5.1**: Policies for Information Security & AI Governance
- **ISO-A.5.8**: Information Security in Project Management & AI Development
- **ISO-A.5.15**: Access Control & Role-Based Permissions for LLMs
- **ISO-A.5.23**: Information Security for Cloud Services & Hosted AI APIs
- **ISO-A.8.7**: Protection Against Malware & Prompt Injection Attacks
- **ISO-A.8.12**: Data Leakage Prevention (DLP) & Output Filtering
- **ISO-A.8.24**: Use of Cryptography & API Key Management Vaults
- **ISO-A.8.28**: Secure Coding & Guardrail Engineering

### 2. NIST Cybersecurity Framework (CSF) 2.0 Coverage
- **GV.OC**: Organizational Context & AI Governance Oversight
- **ID.RA**: Risk Assessment & LLM Threat Modeling
- **PR.AC**: Identity Management, Authentication & Access Control
- **PR.DS**: Data Security & Sensitive Output Redaction
- **PR.PS**: Platform Security & Automated Guardrail Enforcement
- **DE.CM**: Continuous Monitoring & Token Anomaly Detection
- **RS.MA**: Incident Management & Adversarial Prompt Response
- **RC.RP**: Recovery Planning & Deterministic Model Fallback Resilience

### 3. OWASP Top 10 for LLM Applications (2025/2026 Edition)
- **LLM01**: Prompt Injection & Jailbreak Vulnerability (CWE-77, CVSS 9.3)
- **LLM02**: Sensitive Information Disclosure & Credential Leakage (CWE-200, CVSS 8.4)
- **LLM03**: Supply Chain & Third-Party Plugin Abuse (CWE-1357, CVSS 7.8)
- **LLM04**: Data and Model Poisoning via RAG Ingestion (CWE-1407, CVSS 6.8)
- **LLM05**: Improper Output Handling & Markdown XSS / SQLi (CWE-79, CVSS 8.1)
- **LLM06**: Excessive Agency & Autonomous Tool Execution (CWE-250, CVSS 9.1)
- **LLM07**: System Prompt Leakage & IP Extraction (CWE-200, CVSS 6.2)
- **LLM08**: Vector & Embedding Inversion Weaknesses (CWE-310, CVSS 5.9)
- **LLM10**: Unbounded Consumption & Model Denial of Service (CWE-400, CVSS 6.5)

---

## 📐 Mathematical Models

### 1. Overall Compliance Score Formulation
The Overall Compliance Score ($C_{\text{overall}}$) is the arithmetic mean of the weighted ISO 27001 score ($S_{\text{ISO}}$) and NIST CSF score ($S_{\text{NIST}}$):
$$C_{\text{overall}} = \text{round}\left(\frac{S_{\text{ISO}} + S_{\text{NIST}}}{2}\right)$$
Where each framework score is computed over control weights $w_i$ and control scores $s_i \in [0, 100]$:
$$S = \frac{\sum_{i=1}^{N} w_i \cdot s_i}{\sum_{i=1}^{N} w_i}$$

### 2. AI Security Score & Risk Quantification
The AI Security Score ($S_{\text{AI}}$) deducts weighted penalties for active vulnerabilities:
$$S_{\text{AI}} = \max\left(5, 100 - \sum_{v \in V_{\text{active}}} P(v)\right)$$
Where penalty $P(v)$ is defined as:
$$P(v) = \begin{cases} 22, & \text{Severity} = \text{Critical} \\ 14, & \text{Severity} = \text{High} \\ 8, & \text{Severity} = \text{Medium} \\ 4, & \text{Severity} = \text{Low} \end{cases}$$

The Aggregate Cyber Risk Score ($R_{\text{cyber}}$) combines compliance deficiency and vulnerability impact:
$$R_{\text{cyber}} = \min\left(100, \max\left(5, \text{round}\left(0.5 \cdot (100 - C_{\text{overall}}) + 0.5 \cdot \text{Penalty}_{\text{vuln}}\right)\right)\right)$$

### 3. Compliance Forecast Trajectory Model
Future compliance score at milestone $t \in \{30, 60, 90\}$ days is modeled as:
$$\hat{S}(t) = \min\left(100, S_{\text{current}} + \sum_{k \in \text{Roadmap}(t)} \Delta G_k\right)$$
Where $\Delta G_k$ represents the verified point gain for completed roadmap action $k$.

### 4. Longitudinal Memory Diff & Recurrence Formulation
For consecutive audits $A_t$ and $A_{t-1}$:
$$\Delta C = C(A_t) - C(A_{t-1}), \quad \Delta S_{\text{AI}} = S_{\text{AI}}(A_t) - S_{\text{AI}}(A_{t-1}), \quad \Delta R = R(A_t) - R(A_{t-1})$$
A vulnerability $v$ is classified as **Persistent** if:
$$\text{Occurrences}(v) \ge 2 \quad \text{and} \quad \text{Status}(v, A_t) = \text{Vulnerable}$$

### 5. Illustrative Financial Exposure Model
Financial liability exposure range is modeled as a function of annual enterprise revenue ($R_{\text{annual}}$) and severity tier multiplier ($\mu$):
$$E_{\text{financial}} = R_{\text{annual}} \times \mu$$
$$\text{Range} = \left[ 0.7 \times E_{\text{financial}}, \; 1.3 \times E_{\text{financial}} \right]$$
Where $\mu = 0.045$ for Critical Risk, $\mu = 0.022$ for High Risk, and $\mu = 0.008$ for Medium Risk.

---

## 💻 Technology Stack

- **Core Runtime**: Python 3.11+ / Python 3.13
- **API Framework**: FastAPI 0.110+, Uvicorn (ASGI)
- **Interactive UI**: Streamlit 1.32+, Plotly Express / Graph Objects
- **Data Validation & Schemas**: Pydantic v2
- **Persistence**: SQLite 3 (`backend/data/analyses.db`)
- **PDF Generation**: ReportLab 4.1+
- **AI / LLM Layer**: Official Google Gemini SDK (`google-genai`), deterministic fallback engine
- **Automated Testing**: Pytest 8.0+, FastAPI TestClient

---

## 🗄️ Database Design & Schemas

The platform maintains persistent SQLite tables:

### 1. `compliance_audits` Table Schema
```sql
CREATE TABLE compliance_audits (
    audit_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    organization_name TEXT NOT NULL,
    industry TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    date_formatted TEXT NOT NULL,
    iso_score INTEGER NOT NULL,
    nist_score INTEGER NOT NULL,
    overall_compliance INTEGER NOT NULL,
    ai_security_score INTEGER NOT NULL,
    overall_risk_score INTEGER NOT NULL,
    verdict TEXT NOT NULL,
    record_json TEXT NOT NULL
);
```

### 2. `analyses` Table Schema (Legacy Code Inspection)
```sql
CREATE TABLE analyses (
    id TEXT PRIMARY KEY,
    created_at INTEGER NOT NULL,
    filename TEXT NOT NULL,
    language TEXT NOT NULL,
    code TEXT NOT NULL,
    verdict TEXT NOT NULL,
    overall_health INTEGER NOT NULL,
    security_score INTEGER NOT NULL,
    quality_score INTEGER NOT NULL,
    maintainability_score INTEGER NOT NULL,
    complexity TEXT NOT NULL,
    record_json TEXT NOT NULL
);
```

---

## 🌐 REST API Documentation

SentinelAI provides a fully documented FastAPI OpenAPI interface accessible at `http://localhost:8000/docs`.

| Method | Endpoint | Description | Query / Body Params | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | Healthcheck & agent subsystem telemetry | None | Status JSON |
| `GET` | `/organizations` | List all pre-configured dummy enterprise profiles | None | `List[OrganizationProfile]` |
| `POST` | `/audit/{org_id}` | Run full multi-agent compliance & security audit | `api_key` (optional) | `AuditRecord` |
| `POST` | `/audit/custom` | Run audit on user-submitted organization JSON | `OrganizationProfile` body | `AuditRecord` |
| `GET` | `/history` | Retrieve all historical audits sorted by recency | None | `List[AuditRecord]` |
| `GET` | `/history/{org_id}` | Retrieve historical audits for a specific org | None | `List[AuditRecord]` |
| `GET` | `/audit/{audit_id}` | Fetch specific audit record by ID | None | `AuditRecord` |
| `DELETE`| `/audit/{audit_id}` | Delete audit record from SQLite database | None | Success confirmation |
| `GET` | `/report/{audit_id}/pdf` | Generate & download publication-grade PDF report | None | `application/pdf` stream |
| `GET` | `/report/{audit_id}/markdown` | Download formatted Markdown report | None | `text/markdown` |
| `GET` | `/report/{audit_id}/json` | Export structured JSON audit payload | None | `application/json` |

---

## 🚀 Installation & Quickstart Guide

### 1. Prerequisites
- Python 3.11 or Python 3.13 installed
- Git

### 2. Clone and Install Dependencies
```bash
git clone <repository-url>
cd smart-code-inspection-platform-group2

# Install required packages
py -m pip install -r requirements.txt
```

### 3. Environment Configuration (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optional: Add `GEMINI_API_KEY=your_key_here` to enable Google Gemini reasoning. If omitted, SentinelAI operates deterministically offline).*

### 4. Launching Backend & Dashboard

**Option A: Start FastAPI Backend (Port 8000)**
```bash
py -m uvicorn backend.app.main:app --reload --port 8000
```
*Access interactive Swagger documentation at `http://localhost:8000/docs`.*

**Option B: Start Streamlit SaaS Dashboard**
```bash
py -m streamlit run frontend/app.py
```
*Opens interactive cybersecurity dashboard at `http://localhost:8501`.*

### 5. Running Automated Pytest Suite
```bash
py -m pytest backend/tests -v
```

---

## 🖥️ Streamlit 9-Tab Dashboard Walkthrough

1. **Tab 1: 👔 CEO Mode & Executive Summary**
   - Jargon-free executive narrative explaining overall organizational risk.
   - Top 3 Critical Business Risks.
   - Top 3 Immediate Recommended Actions.
   - 30 / 60 / 90-Day Executive Strategic Outlook.
2. **Tab 2: 📋 Standards Compliance Audit**
   - Side-by-side evaluation of ISO/IEC 27001:2022 and NIST CSF 2.0 controls.
   - Evidence telemetry, identified gaps, severity badges, and specific remediation actions.
3. **Tab 3: 🛡️ AI Security Validation (OWASP Top 10 LLM)**
   - Simulated adversarial attacks across 9 OWASP LLM categories.
   - Expandable findings displaying Simulated Payload, Red Team Observation, Blue Team Defense, and Judge Ruling.
4. **Tab 4: ⚖️ AI Debate Engine & Decision**
   - Live transcript of multi-turn debate between Red Team (Skeptic) and Blue Team (Advocate).
   - Binding decision badge (`APPROVED`, `APPROVED WITH REMEDIATION`, `HIGH RISK`, `CRITICAL RISK`) and decision rationale.
5. **Tab 5: 📈 Compliance Forecast (30/60/90 Days)**
   - Interactive Plotly trajectory curve modeling expected score gains over time.
   - Milestone cards with confidence ratings and residual risk analysis.
6. **Tab 6: 🗺️ Remediation Roadmap**
   - Actionable engineering plan prioritized by **P1 (1-14 Days)**, **P2 (15-45 Days)**, and **P3 (46-90 Days)**.
   - Displays responsible teams, target timelines, and anticipated point gains.
7. **Tab 7: 🧠 Audit Memory & Longitudinal Learning**
   - Audit-to-audit comparison with $+/- X$ point delta indicators.
   - Multi-audit recurring flaw tracker identifying persistent unpatched vulnerabilities.
8. **Tab 8: 💰 Quantitative Business Impact**
   - Estimated potential operational downtime hours.
   - Revenue-scaled illustrative financial exposure range ($USD$).
   - Most impacted business units.
9. **Tab 9: 🏗️ Multi-Agent Architecture & Report Export**
   - Full pipeline architecture flow diagram.
   - Per-agent execution telemetry (ms).
   - One-click downloads for ReportLab PDF, JSON, and Markdown reports.

---

## 📊 Experimental Test Organizations & Empirical Results

| Organization Profile | Industry | ISO Score | NIST Score | Overall Compliance | AI Security Score | Risk Score | Debate Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Apex Wealth & FinTech Global** | Financial Services | 70% | 75% | **73%** | **56%** | 46 / 100 | `HIGH RISK` |
| **BioCare Health Systems** | Healthcare & EHR | 46% | 36% | **41%** | **38%** | 68 / 100 | `CRITICAL RISK` |
| **OmniRetail AI Commerce** | E-Commerce Retail | 24% | 15% | **20%** | **22%** | 82 / 100 | `CRITICAL RISK` |
| **AeroDefense Cyber Solutions** | Aerospace Defense | 100% | 100% | **100%** | **100%** | 5 / 100 | `APPROVED` |
| **NexusFlow Enterprise SaaS** | B2B Cloud SaaS | 88% | 85% | **86%** | **78%** | 22 / 100 | `APPROVED WITH REMEDIATION` |

---

## ⚠️ Research Limitations & Compliance Disclaimers

> [!IMPORTANT]
> 1. **Research-Oriented Simplified Controls**: The evaluated ISO/IEC 27001:2022 and NIST CSF 2.0 controls represent simplified academic benchmarks and do not constitute formal legal compliance determination or official third-party certification.
> 2. **Simulated Adversarial Security Tests**: All AI security probing vectors (prompt injections, jailbreaks, data probing) are safe, non-destructive simulated tests executed within controlled test harness environments. No live exploitation or unauthorized network scanning is performed.
> 3. **Illustrative Financial & Forecast Models**: Compliance forecast curves and financial liability figures are illustrative estimation models for research and demonstration purposes.
> 4. **Human Review Requirement**: Real-world enterprise production deployments require manual human-in-the-loop review by qualified cybersecurity and legal governance professionals.

---

## 🔒 Ethical & Safety Considerations

- **No Live Model Tampering**: Probing runs against mock parameters and sandboxed environments.
- **Privacy First**: Sensitive credentials and customer PII are strictly simulated and never transmitted externally.
- **Defensive Focus**: Attack payloads are strictly derived from open-source OWASP Top 10 educational benchmarks designed to harden defenses.

---

## 🔮 Future Enhancements & Roadmap

- [ ] **Real-Time CI/CD Pull Request Gatekeeper**: Automated GitHub Action scanning AI prompt templates and agent tools upon every pull request.
- [ ] **Dynamic Vector Inversion Scanner**: Live mathematical probing of embedding vector distances to test for differential privacy leakage.
- [ ] **EU AI Act & NIST AI RMF Modules**: Dedicated assessment tabs for European Union AI Act high-risk classification requirements.
- [ ] **Active Honeypot Tokens**: Automated canary token injection to trace RAG corpus leakage across downstream inferences.

---

## 🏁 Conclusion

**SentinelAI** demonstrates an integrated, research-ready cybersecurity platform unifying ISO/IEC 27001, NIST CSF, and OWASP Top 10 for LLM security auditing. By employing a collaborative multi-agent architecture with an adversarial AI Debate Engine, temporal compliance forecasting, longitudinal audit memory, and plain-English CEO translation, SentinelAI establishes a robust foundation for modern enterprise AI governance and security assurance.

---
*Created as part of the Advanced Agentic AI & Cybersecurity Research Initiative.*
