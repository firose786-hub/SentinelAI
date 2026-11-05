"""
SentinelAI - Unit Tests for Individual Compliance & Security Agents
Verifies inputs, outputs, scoring logic, and edge cases for each of the 12 agents.
"""

import pytest
from backend.app.data.dummy_organizations import get_organization_by_id
from backend.app.agents.policy_agent import PolicyAgent
from backend.app.agents.compliance_agent import ComplianceAgent
from backend.app.agents.red_team_agent import RedTeamAgent
from backend.app.agents.blue_team_agent import BlueTeamAgent
from backend.app.agents.judge_agent import JudgeAgent
from backend.app.agents.debate_engine import AIDebateEngine
from backend.app.agents.decision_agent import DecisionAgent
from backend.app.agents.risk_agent import RiskAgent
from backend.app.agents.forecast_agent import ForecastAgent
from backend.app.agents.roadmap_agent import RoadmapAgent
from backend.app.agents.memory_agent import MemoryAgent
from backend.app.agents.ceo_agent import CEOAgent

@pytest.fixture
def sample_org():
    return get_organization_by_id("org-fintech-01")

def test_policy_agent(sample_org):
    agent = PolicyAgent()
    result = agent.analyze_policies(sample_org)
    assert result["agent"] == "Policy & Governance Agent"
    assert "policy_coverage_percent" in result
    assert 0 <= result["policy_coverage_percent"] <= 100
    assert result["governance_maturity"] in ["High", "Moderate", "Deficient"]
    assert len(result["in_scope_standards"]) >= 2

def test_compliance_agent(sample_org):
    agent = ComplianceAgent()
    assessments, iso_score, nist_score, overall_score = agent.evaluate_compliance(sample_org)
    assert len(assessments) > 0
    assert 0 <= iso_score <= 100
    assert 0 <= nist_score <= 100
    assert 0 <= overall_score <= 100
    for a in assessments:
        assert a.standard in ["ISO/IEC 27001:2022", "NIST CSF 2.0"]
        assert a.status in ["Compliant", "Partially Compliant", "Non-Compliant", "Not Applicable"]

def test_red_team_agent(sample_org):
    agent = RedTeamAgent()
    findings = agent.execute_simulated_attacks(sample_org)
    assert len(findings) == 10  # All 10 OWASP LLM 2025 vectors
    for f in findings:
        assert f["owasp_id"].startswith("LLM")
        assert f["status"] in ["Vulnerable", "Partially Mitigated", "Protected"]
        assert "simulated_observation" in f

def test_blue_team_agent(sample_org):
    red_agent = RedTeamAgent()
    blue_agent = BlueTeamAgent()
    raw_attacks = red_agent.execute_simulated_attacks(sample_org)
    defensive_findings = blue_agent.analyze_defenses(sample_org, raw_attacks)
    assert len(defensive_findings) == len(raw_attacks)
    for df in defensive_findings:
        assert "defensive_posture" in df
        assert "remediation" in df

def test_judge_agent(sample_org):
    red = RedTeamAgent().execute_simulated_attacks(sample_org)
    blue = BlueTeamAgent().analyze_defenses(sample_org, red)
    judge = JudgeAgent()
    final_findings, ai_security_score = judge.adjudicate_findings(blue)
    assert len(final_findings) == len(blue)
    assert 0 <= ai_security_score <= 100
    for ff in final_findings:
        assert "RULING:" in ff.judge_verdict

def test_debate_engine(sample_org):
    assessments, iso_s, nist_s, comp_s = ComplianceAgent().evaluate_compliance(sample_org)
    red = RedTeamAgent().execute_simulated_attacks(sample_org)
    blue = BlueTeamAgent().analyze_defenses(sample_org, red)
    final_findings, sec_s = JudgeAgent().adjudicate_findings(blue)
    
    debate = AIDebateEngine()
    result = debate.conduct_debate(
        org=sample_org,
        overall_compliance_score=comp_s,
        ai_security_score=sec_s,
        controls=assessments,
        ai_findings=final_findings
    )
    assert len(result.rounds) >= 3
    assert result.verdict in ["APPROVED", "APPROVED WITH REMEDIATION", "HIGH RISK", "CRITICAL RISK"]
    assert 0.0 <= result.decision_confidence <= 1.0

def test_decision_agent():
    decision_agent = DecisionAgent()
    verdict, rationale, tier = decision_agent.determine_final_verdict(
        compliance_score=75,
        ai_security_score=68,
        risk_score=42,
        critical_vulnerabilities=1
    )
    assert verdict in ["APPROVED", "APPROVED WITH REMEDIATION", "HIGH RISK", "CRITICAL RISK"]
    assert len(rationale) > 10

def test_risk_agent():
    risk_agent = RiskAgent()
    risk_score, tier, narrative = risk_agent.calculate_overall_risk(
        compliance_score=70,
        ai_security_score=65,
        vulnerable_findings_count=3,
        critical_count=1
    )
    assert 0 <= risk_score <= 100
    assert tier in ["Critical", "High", "Medium", "Low", "Informational"]

def test_forecast_and_roadmap(sample_org):
    assessments, _, _, comp_s = ComplianceAgent().evaluate_compliance(sample_org)
    red = RedTeamAgent().execute_simulated_attacks(sample_org)
    blue = BlueTeamAgent().analyze_defenses(sample_org, red)
    findings, _ = JudgeAgent().adjudicate_findings(blue)

    roadmap = RoadmapAgent().generate_roadmap(controls=assessments, ai_findings=findings)
    assert len(roadmap) > 0

    forecast = ForecastAgent().generate_forecast(current_overall_score=comp_s, roadmap=roadmap, ai_findings=findings)
    assert len(forecast.milestones) == 3
    assert forecast.milestones[0].days == 30
    assert forecast.milestones[1].days == 60
    assert forecast.milestones[2].days == 90
    assert forecast.milestones[0].predicted_score <= forecast.milestones[2].predicted_score

def test_memory_agent(sample_org):
    memory_agent = MemoryAgent()
    # Test first audit (no historical audits)
    comparison = memory_agent.compare_with_previous(
        org_id=sample_org.id,
        current_compliance_score=70,
        current_ai_security_score=60,
        current_risk_score=45,
        current_findings=[]
    )
    assert comparison.has_previous_audit is False
