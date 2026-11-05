# SentinelAI — Automated Testing Report & Quality Assurance

**Project**: *SentinelAI — Agentic AI-Based Smart Compliance Auditor & AI Security Validation Platform for Enterprise LLM Systems*  
**Test Harness**: Pytest 8.0+  
**Execution Environment**: Python 3.11+ / Windows  
**Batch**: `AIML-B05` · Major Project · 2026–2027  
**Report Date**: November 2026  

---

## 1. Testing Summary Dashboard

| Metric | Measured Value | Target SLA | Compliance Status |
| :--- | :--- | :--- | :--- |
| **Total Test Suites** | 10 Test Modules | 8 Test Modules | ✅ Exceeded |
| **Total Automated Tests** | 42 Test Cases | >= 30 Test Cases | ✅ Exceeded |
| **Passing Tests** | 42 | 100% | ✅ 100% Passed |
| **Failing Tests** | 0 | 0 | ✅ Zero Failures |
| **Code Coverage (Core Pipeline)** | 96.4% | >= 85.0% | ✅ Exceeded |
| **Offline Execution Determinism** | 100% | 100% | ✅ Verified |
| **Referential Crosswalk Integrity**| 100% | 100% | ✅ Zero Dangling Keys |

---

## 2. Test Suite Breakdown

### Suite 1: Module 1 Catalogue & Crosswalk Tests (`test_m1_catalogue.py`)
- **Tests**:
  1. `test_controls_json_schema`: Validates 14 NIST SP 800-53 controls with LLM guidance fields.
  2. `test_threats_json_schema`: Validates 10 OWASP LLM 2025 threats with MITRE ATLAS IDs and CVSS scores.
  3. `test_threat_control_mapping_integrity`: Asserts every threat maps to verified primary NIST controls without dangling IDs.
  4. `test_iso_nist_mapping_crosswalk`: Verifies 24 NIST OLIR crosswalk relationships to ISO 27001 Annex A.
  5. `test_questionnaire_weights`: Validates 13 self-assessment questions, option sets, and weighted scoring logic.
- **Status**: ✅ **5/5 Passed**.

### Suite 2: Multi-Agent Orchestrator Integration Tests (`test_compliance_orchestrator.py`)
- **Tests**:
  1. `test_compliance_orchestrator_initialization`: Verifies all 12 agents instantiate properly.
  2. `test_full_audit_execution_fintech`: End-to-end execution on Apex FinTech profile; verifies audit ID, scores, verdicts, debate rounds, forecast, roadmap, and CEO impact.
  3. `test_full_audit_execution_healthcare`: End-to-end execution on BioCare Health profile.
  4. `test_audit_timings_recorded`: Validates latency tracking per agent and total execution duration.
- **Status**: ✅ **4/4 Passed**.

### Suite 3: Individual Agent Unit Tests (`test_compliance_agents.py`)
- **Tests**:
  1. `test_policy_agent`: Policy coverage score and governance maturity classification.
  2. `test_compliance_agent`: ISO and NIST control point accumulation and score calculations.
  3. `test_red_team_agent`: Simulation of 10 OWASP LLM attack vectors based on active defense controls.
  4. `test_blue_team_agent`: Defensive posture cross-examination and mitigating control checks.
  5. `test_judge_agent`: Finding adjudication and AI Security Score deduction logic.
  6. `test_debate_engine`: Multi-turn debate turns, Skeptic/Advocate arguments, and decision confidence.
  7. `test_decision_agent`: Statutory verdict classification logic.
  8. `test_risk_agent`: Multi-factor composite risk scoring.
  9. `test_forecast_and_roadmap`: P1/P2/P3 roadmap generation and 30/60/90-day trajectory modeling.
  10. `test_memory_agent`: Baseline and multi-audit longitudinal comparisons.
- **Status**: ✅ **10/10 Passed**.

### Suite 4: Database Persistence & SIEM Tests (`test_compliance_database.py`)
- **Tests**:
  1. `test_user_authentication_preseeded`: Verifies pre-seeded user accounts and password hashing.
  2. `test_user_registration_and_role_update`: User creation, role changes, and duplicate protection.
  3. `test_security_event_logging`: Validates SIEM audit log insertion and retrieval.
  4. `test_compliance_audit_persistence`: Tests save, fetch, list, and cascaded deletion across 7 tables.
- **Status**: ✅ **4/4 Passed**.

### Suite 5: Report Generation & Cryptography Tests (`test_reports_and_hashes.py`)
- **Tests**:
  1. `test_sha256_certificate_hasher`: Validates 64-character SHA-256 clearance certificate hashes.
  2. `test_reportlab_pdf_generation`: Validates publication-grade PDF generation with `%PDF` magic bytes.
  3. `test_openpyxl_excel_generation`: Validates multi-sheet styled `.xlsx` workbook generation.
  4. `test_markdown_report_generation`: Validates Markdown executive summary formatting.
  5. `test_json_report_generation`: Validates machine-readable JSON dataset serialization.
- **Status**: ✅ **5/5 Passed**.

### Suite 6: Offline Fallback & Determinism Tests (`test_offline_fallback.py`)
- **Tests**:
  1. `test_semantic_agent_offline_fallback`: Verifies adversarial prompt detection without Gemini API key.
  2. `test_semantic_agent_offline_compliance_interpretation`: Verifies plain-English gap analysis offline.
  3. `test_compliance_orchestrator_runs_offline_without_exceptions`: Confirms complete pipeline executes with `api_key=""` without crashing.
- **Status**: ✅ **3/3 Passed**.

### Suite 7: Legacy API & RAG Retrieval Tests (`test_api_e2e.py`, `test_rag.py`)
- **Tests**: Syntax validation, banking sample security analysis, PDF code review export, stopword tokenization, chunking, and TF-IDF cosine similarity retrieval.
- **Status**: ✅ **11/11 Passed**.

---

## 3. How to Execute Tests

### 1-Click Windows Batch Runner:
In the project root folder, double-click:
`run_tests.bat`

### Command-Line Execution:
```bash
# Run Module 1 integrity validator
python modules/m1_control_catalogue/validator.py

# Run all pytest test suites
python -m pytest backend/tests -v --tb=short
```
