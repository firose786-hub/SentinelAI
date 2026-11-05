"""
SentinelAI - End-to-End Compliance Orchestrator Integration Test
Tests the complete multi-agent audit execution pipeline across all 12 agents.
"""

import pytest
from backend.app.agents.compliance_orchestrator import ComplianceOrchestrator
from backend.app.data.dummy_organizations import get_organization_by_id, ORGANIZATION_PROFILES
from backend.app.models.compliance_schemas import AuditRecord, AuditVerdict

def test_compliance_orchestrator_initialization():
    orchestrator = ComplianceOrchestrator()
    assert orchestrator.policy_agent is not None
    assert orchestrator.compliance_agent is not None
    assert orchestrator.risk_agent is not None
    assert orchestrator.red_team_agent is not None
    assert orchestrator.blue_team_agent is not None
    assert orchestrator.judge_agent is not None
    assert orchestrator.debate_engine is not None
    assert orchestrator.decision_agent is not None
    assert orchestrator.forecast_agent is not None
    assert orchestrator.roadmap_agent is not None
    assert orchestrator.memory_agent is not None
    assert orchestrator.ceo_agent is not None
    assert orchestrator.report_agent is not None

def test_full_audit_execution_fintech():
    orchestrator = ComplianceOrchestrator()
    org = get_organization_by_id("org-fintech-01")
    assert org is not None

    # Execute audit in offline deterministic mode (api_key=None)
    record: AuditRecord = orchestrator.run_full_audit(org=org, api_key=None)

    assert record.audit_id.startswith("AUDIT-")
    assert record.organization_name == org.name
    assert record.industry == org.industry
    assert 0 <= record.iso_compliance_score <= 100
    assert 0 <= record.nist_compliance_score <= 100
    assert 0 <= record.overall_compliance_score <= 100
    assert 0 <= record.ai_security_score <= 100
    assert 0 <= record.overall_risk_score <= 100
    assert record.verdict in ["APPROVED", "APPROVED WITH REMEDIATION", "HIGH RISK", "CRITICAL RISK"]

    # Verify agent outputs
    assert len(record.controls_assessment) > 0
    assert len(record.ai_security_findings) > 0
    assert record.debate_result is not None
    assert len(record.debate_result.rounds) >= 3
    assert record.forecast is not None
    assert len(record.forecast.milestones) == 3
    assert len(record.roadmap) > 0
    assert record.ceo_summary is not None
    assert record.business_impact is not None
    assert record.business_impact.estimated_financial_exposure_usd > 0
    assert record.llm_reasoning_used is False  # Confirms offline fallback worked

def test_full_audit_execution_healthcare():
    orchestrator = ComplianceOrchestrator()
    org = get_organization_by_id("org-health-02")
    assert org is not None

    record = orchestrator.run_full_audit(org=org)
    assert record.organization_id == "org-health-02"
    assert record.overall_compliance_score > 0
    assert len(record.roadmap) > 0

def test_audit_timings_recorded():
    orchestrator = ComplianceOrchestrator()
    org = ORGANIZATION_PROFILES[0]
    record = orchestrator.run_full_audit(org=org)
    
    assert "policy_analysis" in record.agent_execution_times
    assert "compliance_evaluation" in record.agent_execution_times
    assert "red_team_attacks" in record.agent_execution_times
    assert "judge_adjudication" in record.agent_execution_times
    assert "total_pipeline" in record.agent_execution_times
    assert record.agent_execution_times["total_pipeline"] >= 0.0
