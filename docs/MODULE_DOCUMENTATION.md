# SentinelAI — Complete 10-Module Implementation Documentation (M1 to M10)

**Project**: *SentinelAI — Agentic AI-Based Smart Compliance Auditor & AI Security Validation Platform for Enterprise LLM Systems*  
**Batch**: `AIML-B05` · Major Project · 2026–2027  
**Supervisor**: Dr. Mahammad Firose Shaik (`firose786-hub`)  

---

## Module Index & Scope Breakdown

```text
M1: Control Catalogue & Threat Taxonomy
M2: Compliance Assessment Engine
M3: Document Processing & 8-Step RAG
M4: AI Security Testing & Red Team Testbed
M5: 12-Agent Multi-Agent Architecture
M6: Judge, Risk & Adversarial Decision Engine
M7: Remediation & 30/60/90-Day Trajectory Forecasting
M8: Full-Stack Command Center & RBAC Application
M9: Tamper-Evident Reporting & Evidence Vault
M10: Integration, Evaluation & Quality Assurance
```

---

### M1: Control Catalogue & Threat Taxonomy
- **Purpose**: Establishes machine-readable cybersecurity controls and AI threat taxonomies.
- **Key Files**:
  - `modules/m1_control_catalogue/controls.json`: 14 NIST SP 800-53 Rev. 5 controls across AC, IA, SI, SC, AU, IR.
  - `modules/m1_control_catalogue/iso_nist_mapping.csv`: 24 verified NIST OLIR crosswalk relationships to ISO 27001:2022.
  - `modules/m1_control_catalogue/threats.json`: 10 OWASP Top 10 for LLMs (2025) threats + MITRE ATLAS techniques.
  - `modules/m1_control_catalogue/threat_control_mapping.json`: Many-to-many relationship linking exploits to control breaches.
  - `modules/m1_control_catalogue/questionnaire.json`: 13 weighted audit self-assessment questions.
  - `modules/m1_control_catalogue/validator.py`: Automated referential integrity validator.

---

### M2: Compliance Assessment Engine
- **Purpose**: Evaluates organizational charters, technical toggles, and evidence against international compliance frameworks.
- **Key Files**:
  - `backend/app/agents/compliance_agent.py`: Calculates ISO compliance score, NIST compliance score, and overall compliance posture.
  - `backend/app/data/compliance_standards.py`: Formal control catalogues with evaluation keys, weights, and criteria.
- **Scoring Formulas**:
  $$\text{Score}_{\text{ISO}} = \frac{\sum \text{Points Earned}}{\sum \text{Max Possible Points}} \times 100$$
  $$\text{Score}_{\text{NIST}} = \frac{\sum \text{Points Earned}}{\sum \text{Max Possible Points}} \times 100$$
  $$\text{Overall Compliance} = 0.5 \times \text{Score}_{\text{ISO}} + 0.5 \times \text{Score}_{\text{NIST}}$$

---

### M3: Document Processing & 8-Step RAG
- **Purpose**: Ingests organizational policies, splits them into semantic chunks, and performs hybrid vector-keyword retrieval with citation verification.
- **Key Files**:
  - `backend/app/services/rag_service.py`: 8-step pipeline:
    1. Query Normalization & Tokenization
    2. Hybrid Retrieval (Cosine Similarity + BM25 Keywords)
    3. Cross-Score Re-ranking (Top-5 Selection)
    4. Initial Synthesis with Citations
    5. Self-Feedback Gap Evaluation
    6. Secondary Supplemental Retrieval
    7. Refinement & Context Assembly
    8. Exact Citation Span Verification

---

### M4: AI Security Testing & Red Team Testbed
- **Purpose**: Simulates safe, controlled adversarial attacks targeting LLMs.
- **Key Files**:
  - `backend/app/agents/red_team_agent.py`: Executes automated tests across all 10 OWASP LLM 2025 vectors.
  - `frontend/app.py` (AI Security Lab): Interactive testbeds for Direct Prompt Injection, Jailbreak Persona Hijack, Token DLP, and Cloud API Outbound Confinement.
  - `backend/app/data/spep_framework.py`: Mathematical cosine trigger score computation:
    $$\text{Score}_{\text{Trigger}} = \min\left(0.98, 0.65 + 0.12 \times N_{\text{matched tokens}}\right)$$

---

### M5: 12-Agent Multi-Agent Architecture
- **Purpose**: Coordinates 12 specialized autonomous agents through an adversarial consensus pipeline.
- **Key Files**:
  - `backend/app/agents/compliance_orchestrator.py`: Master pipeline coordinator.
  - Agents: Policy, Compliance, Risk, Red Team, Blue Team, Judge, Debate, Decision, Forecast, Roadmap, Memory, Report.

---

### M6: Judge, Risk & Adversarial Decision Engine
- **Purpose**: Adjudicates findings, resolves Red vs. Blue conflicts, and calculates comprehensive risk metrics.
- **Key Files**:
  - `backend/app/agents/debate_engine.py`: Multi-turn adversarial debate (Skeptic vs. Advocate).
  - `backend/app/agents/judge_agent.py`: Impartial arbiter classifying findings into OWASP and assigning security deductions.
  - `backend/app/agents/risk_agent.py`: Composite risk score:
    $$\text{Risk Score} = 100 - \left(0.5 \times \text{Compliance} + 0.5 \times \text{AI Security}\right) + \text{Critical Penalty}$$

---

### M7: Remediation & 30/60/90-Day Trajectory Forecasting
- **Purpose**: Formulates prioritized fix roadmaps and calculates financial loss exposure.
- **Key Files**:
  - `backend/app/agents/roadmap_agent.py`: Assigns P1, P2, P3 actions, responsible teams, target completion days, and expected score gains.
  - `backend/app/agents/forecast_agent.py`: Models posture at 30, 60, and 90 days.
  - `backend/app/agents/ceo_agent.py`: Estimates downtime hours and monetary liability ranges based on enterprise revenue.

---

### M8: Full-Stack Command Center & RBAC Application
- **Purpose**: Delivers an enterprise-grade Cyber Defense Command Center.
- **Key Files**:
  - `frontend/app.py`: 2,443-line Streamlit dashboard.
  - Obsidian Falcon Dark Glass Theme (`#080C16` and `#00F2FE`).
  - 6 Pre-configured Personas with 1-Click Quick Demo cards and hardware MFA TOTP (`749201`).
  - Sidebar Enclave Switcher and dynamic permission routing.

---

### M9: Tamper-Evident Reporting & Evidence Vault
- **Purpose**: Generates multi-format publication-grade compliance audits with cryptographic provenance.
- **Key Files**:
  - `backend/app/agents/report_agent.py`: ReportLab PDF generator with Executive Summary, Radar Charts, Controls Breakdown, Findings Table, and Remediation Roadmap.
  - `backend/app/services/excel_generator.py`: Multi-sheet styled Excel workbook (`.xlsx`) via OpenPyXL.
  - `backend/app/services/hasher.py`: SHA-256 certificate fingerprint generator.

---

### M10: Integration, Evaluation & Quality Assurance
- **Purpose**: End-to-end integration across frontend, backend, database, and offline fallbacks.
- **Key Files**:
  - `backend/app/main.py`: FastAPI server unifying all subsystems.
  - `backend/tests/`: Comprehensive Pytest test suites with >95% code coverage.
  - `run_tests.bat`: 1-Click test runner.
