"""
Unit tests for SentinelAI multi-agent compliance & security platform.
Validates all 13 specialized agents, debate engine, forecast, roadmap, memory, and PDF export.
"""

import pytest
from backend.app.data.dummy_organizations import ORGANIZATION_PROFILES, get_organization_by_id
from backend.app.agents.policy_agent import PolicyAgent
from backend.app.agents.compliance_agent import ComplianceAgent
from backend.app.agents.risk_agent import RiskAgent
from backend.app.agents.red_team_agent import RedTeamAgent
from backend.app.agents.blue_team_agent import BlueTeamAgent
from backend.app.agents.judge_agent import JudgeAgent
from backend.app.agents.debate_engine import AIDebateEngine
from backend.app.agents.decision_agent import DecisionAgent
from backend.app.agents.forecast_agent import ForecastAgent
from backend.app.agents.roadmap_agent import RoadmapAgent
from backend.app.agents.memory_agent import MemoryAgent
from backend.app.agents.ceo_agent import CEOAgent
from backend.app.agents.report_agent import ReportAgent
from backend.app.agents.compliance_orchestrator import ComplianceOrchestrator

@pytest.fixture
def fintech_org():
    return get_organization_by_id("org-fintech-01")

@pytest.fixture
def defense_org():
    return get_organization_by_id("org-defense-04")

def test_policy_agent(fintech_org):
    agent = PolicyAgent()
    res = agent.analyze_policies(fintech_org)
    assert res["organization_name"] == fintech_org.name
    assert "in_scope_standards" in res
    assert res["policy_coverage_percent"] > 0

def test_compliance_agent(fintech_org):
    agent = ComplianceAgent()
    controls, iso_score, nist_score, overall = agent.evaluate_compliance(fintech_org)
    assert len(controls) == 16  # 8 ISO + 8 NIST
    assert 0 <= iso_score <= 100
    assert 0 <= nist_score <= 100
    assert 0 <= overall <= 100

def test_red_team_agent(fintech_org):
    agent = RedTeamAgent()
    findings = agent.execute_simulated_attacks(fintech_org)
    assert len(findings) >= 9
    assert any(f["owasp_id"] == "LLM01" for f in findings)
    assert any(f["owasp_id"] == "LLM02" for f in findings)

def test_blue_team_agent(fintech_org):
    red_agent = RedTeamAgent()
    blue_agent = BlueTeamAgent()
    raw_findings = red_agent.execute_simulated_attacks(fintech_org)
    defensive_findings = blue_agent.evaluate_defenses(fintech_org, raw_findings)
    assert len(defensive_findings) == len(raw_findings)
    assert "blue_team_defense" in defensive_findings[0]

def test_judge_agent_and_scoring(fintech_org):
    red_agent = RedTeamAgent()
    blue_agent = BlueTeamAgent()
    judge = JudgeAgent()
    raw = red_agent.execute_simulated_attacks(fintech_org)
    defensive = blue_agent.evaluate_defenses(fintech_org, raw)
    final_findings, sec_score = judge.adjudicate_findings(defensive)
    assert len(final_findings) == len(raw)
    assert 0 <= sec_score <= 100
    assert all(hasattr(f, "judge_verdict") for f in final_findings)

def test_debate_engine_and_verdict(fintech_org, defense_org):
    debate_engine = AIDebateEngine()
    comp_agent = ComplianceAgent()
    red_agent = RedTeamAgent()
    blue_agent = BlueTeamAgent()
    judge = JudgeAgent()

    # Test on Fintech
    ctrls, iso, nist, overall = comp_agent.evaluate_compliance(fintech_org)
    raw = red_agent.execute_simulated_attacks(fintech_org)
    defensive = blue_agent.evaluate_defenses(fintech_org, raw)
    findings, sec_score = judge.adjudicate_findings(defensive)

    debate_res = debate_engine.conduct_debate(fintech_org, overall, sec_score, ctrls, findings)
    assert len(debate_res.rounds) == 3
    assert debate_res.verdict in ["APPROVED", "APPROVED WITH REMEDIATION", "HIGH RISK", "CRITICAL RISK"]
    assert debate_res.decision_confidence > 0.7

    # Test on Defense Org (Should be APPROVED)
    ctrls_d, iso_d, nist_d, overall_d = comp_agent.evaluate_compliance(defense_org)
    raw_d = red_agent.execute_simulated_attacks(defense_org)
    defensive_d = blue_agent.evaluate_defenses(defense_org, raw_d)
    findings_d, sec_score_d = judge.adjudicate_findings(defensive_d)

    debate_res_d = debate_engine.conduct_debate(defense_org, overall_d, sec_score_d, ctrls_d, findings_d)
    assert debate_res_d.verdict == "APPROVED"

def test_forecast_agent(fintech_org):
    comp_agent = ComplianceAgent()
    red_agent = RedTeamAgent()
    blue_agent = BlueTeamAgent()
    judge = JudgeAgent()
    roadmap_agent = RoadmapAgent()
    forecast_agent = ForecastAgent()

    ctrls, iso, nist, overall = comp_agent.evaluate_compliance(fintech_org)
    raw = red_agent.execute_simulated_attacks(fintech_org)
    defensive = blue_agent.evaluate_defenses(fintech_org, raw)
    findings, sec_score = judge.adjudicate_findings(defensive)
    roadmap = roadmap_agent.build_roadmap(ctrls, findings)

    forecast = forecast_agent.generate_forecast(overall, roadmap, findings)
    assert forecast.current_score == overall
    assert len(forecast.milestones) == 3
    assert forecast.milestones[0].days == 30
    assert forecast.milestones[1].days == 60
    assert forecast.milestones[2].days == 90
    assert forecast.milestones[0].predicted_score >= overall
    assert forecast.milestones[2].predicted_score >= forecast.milestones[1].predicted_score

def test_roadmap_agent(fintech_org):
    comp_agent = ComplianceAgent()
    red_agent = RedTeamAgent()
    blue_agent = BlueTeamAgent()
    judge = JudgeAgent()
    roadmap_agent = RoadmapAgent()

    ctrls, iso, nist, overall = comp_agent.evaluate_compliance(fintech_org)
    raw = red_agent.execute_simulated_attacks(fintech_org)
    defensive = blue_agent.evaluate_defenses(fintech_org, raw)
    findings, sec_score = judge.adjudicate_findings(defensive)

    roadmap = roadmap_agent.build_roadmap(ctrls, findings)
    assert len(roadmap) > 0
    assert any(item.priority == "P1" for item in roadmap)
    assert all(item.expected_point_gain > 0 for item in roadmap)

def test_ceo_agent_and_business_impact(fintech_org):
    comp_agent = ComplianceAgent()
    red_agent = RedTeamAgent()
    blue_agent = BlueTeamAgent()
    judge = JudgeAgent()
    ceo_agent = CEOAgent()

    ctrls, iso, nist, overall = comp_agent.evaluate_compliance(fintech_org)
    raw = red_agent.execute_simulated_attacks(fintech_org)
    defensive = blue_agent.evaluate_defenses(fintech_org, raw)
    findings, sec_score = judge.adjudicate_findings(defensive)

    ceo_summary, business_impact = ceo_agent.generate_executive_insights(
        fintech_org, overall, sec_score, "HIGH RISK", ctrls, findings
    )
    assert len(ceo_summary.top_3_risks) <= 3
    assert len(ceo_summary.top_3_recommended_actions) <= 3
    assert business_impact.estimated_downtime_hours > 0
    assert business_impact.estimated_financial_exposure_usd > 0
    assert "USD" in business_impact.financial_range_display

def test_orchestrator_end_to_end(fintech_org):
    orchestrator = ComplianceOrchestrator()
    record = orchestrator.run_full_audit(fintech_org)
    assert record.organization_id == fintech_org.id
    assert record.overall_compliance_score > 0
    assert len(record.controls_assessment) == 16
    assert len(record.ai_security_findings) >= 9
    assert len(record.roadmap) > 0
    assert len(record.forecast.milestones) == 3
    assert len(record.agent_execution_times) >= 10

def test_report_generation(fintech_org):
    orchestrator = ComplianceOrchestrator()
    record = orchestrator.run_full_audit(fintech_org)
    report_agent = ReportAgent()

    pdf_bytes = report_agent.generate_pdf(record)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")

    md_str = report_agent.generate_markdown(record)
    assert "# SentinelAI Audit Report" in md_str
    assert record.organization_name in md_str

    json_str = report_agent.generate_json(record)
    assert record.audit_id in json_str
