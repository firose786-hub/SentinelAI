# SentinelAI — System Architecture & Multi-Agent Design Document

**Project**: *SentinelAI — Agentic AI-Based Smart Compliance Auditor & AI Security Validation Platform for Enterprise LLM Systems*  
**Architecture Version**: v3.0 Enterprise SOC  
**Batch**: `AIML-B05` · Major Project · 2026–2027  
**Supervisor**: Dr. Mahammad Firose Shaik (`firose786-hub`)  

---

## 1. High-Level Architectural Topology

SentinelAI follows an Enterprise Hybrid Layered Architecture composed of 5 distinct tiers:

```mermaid
graph TD
    subgraph Tier 1: Presentation Layer
        UI["Streamlit Command Center (13 Pages)<br>Obsidian Falcon Dark Glass Theme"]
        RoleRouter["RBAC Persona Gatekeeper<br>(CISO, Compliance, AI Engineer, SOC, Auditor, Admin)"]
    end

    subgraph Tier 2: Ingress & API Gateway Layer
        FastAPI["FastAPI REST API Service (:8000)<br>CORS, Input Validation & Security Gate"]
    end

    subgraph Tier 3: Agentic Intelligence & Orchestration Layer
        Orch["ComplianceOrchestrator Pipeline"]
        PolicyAgent["Policy & Governance Agent"]
        CompAgent["Compliance Agent (ISO 27001 & NIST CSF)"]
        RedAgent["Adversarial Red Team Agent"]
        BlueAgent["Defensive Blue Team Agent"]
        JudgeAgent["Impartial Judge Agent"]
        Debate["Adversarial AI Debate Engine"]
        DecisionAgent["Final Decision Agent"]
        RiskAgent["Quantitative Risk & Severity Agent"]
        ForecastAgent["30/60/90-Day Forecast Agent"]
        RoadmapAgent["Actionable Remediation Roadmap Agent"]
        MemoryAgent["Longitudinal Multi-Audit Memory Agent"]
        CEOAgent["CEO Business Impact & Financial Exposure Agent"]
        ReportAgent["ReportLab PDF & Multi-Sheet Excel Agent"]
    end

    subgraph Tier 4: Knowledge Base & RAG Services
        RAG["8-Step Hybrid RAG Engine<br>(Cosine Vector + BM25 Keywords)"]
        SPEP["Secure Prompt Engineering Patterns (SPEP Framework)"]
        M1Cat["Module 1: NIST SP 800-53 & ISO OLIR Catalogue"]
        EvidChain["Unified Compliance-and-Security Evidence Chain"]
    end

    subgraph Tier 5: Persistence & Verification Layer
        SQLite[("SQLite 7-Table Relational Schema<br>+ security_logs SIEM Trail")]
        Hasher["SHA-256 Cryptographic Hash Engine"]
    end

    UI --> RoleRouter
    RoleRouter --> FastAPI
    FastAPI --> Orch
    Orch --> PolicyAgent --> CompAgent --> RedAgent --> BlueAgent --> JudgeAgent --> Debate --> DecisionAgent --> RiskAgent --> ForecastAgent --> RoadmapAgent --> MemoryAgent --> CEOAgent --> ReportAgent
    CompAgent -.-> M1Cat
    RedAgent -.-> SPEP
    Debate -.-> EvidChain
    Orch --> RAG
    Orch --> SQLite
    ReportAgent --> Hasher
```

---

## 2. Multi-Agent Collaboration Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User as Enterprise Auditor
    participant Orch as Compliance Orchestrator
    participant Pol as Policy Agent
    participant Comp as Compliance Agent
    participant Red as Red Team Agent
    participant Blue as Blue Team Agent
    participant Judge as Judge Agent
    participant Debate as AI Debate Engine
    participant Dec as Decision Agent
    participant Risk as Risk & CEO Agent
    participant Rep as Report Agent
    participant DB as SQLite Database

    User->>Orch: Submit Audit Request (OrganizationProfile)
    Orch->>Pol: Ingest Policy Charters & Scope
    Pol-->>Orch: Governance Maturity & Standard Scope
    Orch->>Comp: Evaluate ISO 27001 & NIST CSF Controls
    Comp-->>Orch: Controls Assessment & Compliance Scores
    Orch->>Red: Execute OWASP LLM 2025 Adversarial Attacks
    Red-->>Orch: Raw Exploit Telemetry & Simulated Observations
    Orch->>Blue: Cross-Examine Defenses (SPEP Patterns)
    Blue-->>Orch: Mitigating Evidence & Defensive Findings
    Orch->>Judge: Adjudicate Vulnerabilities vs Defenses
    Judge-->>Orch: Final Security Findings & AI Security Score
    Orch->>Debate: Conduct Adversarial Debate (Skeptic vs Advocate)
    Debate-->>Orch: Debate Transcript & Binding Consensus Ruling
    Orch->>Dec: Synthesize Final Audit Verdict
    Dec-->>Orch: Audit Verdict & Rationale
    Orch->>Risk: Model Financial Liability & Trajectory
    Risk-->>Orch: Business Impact & 30/60/90-Day Forecast
    Orch->>DB: Persist AuditRecord & Findings (7 Tables)
    Orch->>Rep: Generate PDF & Signed Certificate (SHA-256)
    Rep-->>User: Return Complete Audit Dashboard & PDF Download
```

---

## 3. Core Architectural Subsystems

### 3.1 Dual-Runtime Operational Architecture
To ensure high availability in restricted defense, banking, or air-gapped enterprise environments:
1. **Google Gemini LLM Cloud Mode**: When `GEMINI_API_KEY` is present, agents dynamically use `gemini-2.5-flash` for multi-turn adversarial reasoning, natural language summary synthesis, and compliance gap interpretations.
2. **Deterministic Offline Fallback Mode**: When the API key is not configured, the system operates completely offline using AST syntactic analysis, regex token matching, cosine similarity trigger scoring, and grounded SQLite rule matrices. Zero degradation in audit completeness occurs.

### 3.2 Unified Evidence Chain Architecture (Innovation 1)
Connects disparate security scanner findings into regulatory governance failures:
- Exploit detected in **OWASP LLM01 (Prompt Injection)**
- Automatically degrades **NIST SI-10 (Information Input Validation)**
- Automatically degrades **ISO/IEC 27001:2022 Control A.8.28 (Secure Coding)**
- Subtracts calculated penalty points from overall compliance score.
- Propagates directly into CISO financial exposure calculation.

### 3.3 Cryptographic Integrity Verification Subsystem
Every finalized compliance audit record generates a canonical payload string:
`audit_id:org_name:compliance_score:verdict:timestamp:SENTINEL_AI_CLEARANCE`
This payload is hashed using **SHA-256** and embedded into:
- The PDF Certificate of Clearance (with QR verification block).
- The Excel audit workbook metadata.
- The SQLite `audits` database table for non-repudiation and external auditor verification.
