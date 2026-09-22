"""
Integration tests for SentinelAI FastAPI REST API endpoints and longitudinal Memory Agent.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "SentinelAI" in data["platform"]
    assert data["agents_active"] >= 11

def test_organizations_endpoint():
    resp = client.get("/organizations")
    assert resp.status_code == 200
    orgs = resp.json()
    assert len(orgs) >= 4
    org_ids = [o["id"] for o in orgs]
    assert "org-fintech-01" in org_ids
    assert "org-health-02" in org_ids

def test_run_audit_endpoint():
    resp = client.post("/audit/org-fintech-01")
    assert resp.status_code == 200
    audit = resp.json()
    assert audit["organization_id"] == "org-fintech-01"
    assert "audit_id" in audit
    assert "overall_compliance_score" in audit
    assert "ai_security_score" in audit
    assert "debate_result" in audit
    assert "roadmap" in audit
    assert "forecast" in audit
    assert "memory_comparison" in audit

def test_audit_history_and_memory_learning():
    # Run first audit
    resp1 = client.post("/audit/org-health-02")
    assert resp1.status_code == 200
    audit1 = resp1.json()

    # Run second audit on same org to trigger memory comparison & delta
    resp2 = client.post("/audit/org-health-02")
    assert resp2.status_code == 200
    audit2 = resp2.json()

    # Verify memory comparison
    mem = audit2["memory_comparison"]
    assert mem["has_previous_audit"] is True
    assert mem["previous_audit_id"] == audit1["audit_id"]
    assert "summary_of_progress" in mem
    assert len(mem["recurring_findings"]) > 0
    assert any(rf["occurrences_count"] >= 2 for rf in mem["recurring_findings"])

def test_get_audit_by_id():
    resp = client.post("/audit/org-retail-03")
    assert resp.status_code == 200
    audit_id = resp.json()["audit_id"]

    resp_get = client.get(f"/audit/{audit_id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["audit_id"] == audit_id

def test_download_pdf_report():
    resp = client.post("/audit/org-fintech-01")
    audit_id = resp.json()["audit_id"]

    resp_pdf = client.get(f"/report/{audit_id}/pdf")
    assert resp_pdf.status_code == 200
    assert resp_pdf.headers["content-type"] == "application/pdf"
    assert resp_pdf.content.startswith(b"%PDF")

def test_download_json_and_markdown_reports():
    resp = client.post("/audit/org-fintech-01")
    audit_id = resp.json()["audit_id"]

    resp_json = client.get(f"/report/{audit_id}/json")
    assert resp_json.status_code == 200
    assert resp_json.json()["audit_id"] == audit_id

    resp_md = client.get(f"/report/{audit_id}/markdown")
    assert resp_md.status_code == 200
    assert "# SentinelAI Audit Report" in resp_md.text

def test_custom_organization_audit():
    custom_profile = {
        "id": "org-custom-test",
        "name": "Acme AI Corp",
        "industry": "Autonomous Logistics",
        "size": "500 Employees",
        "annual_revenue_usd": 50000000.0,
        "description": "Logistics optimization agent using LLMs for dispatch planning.",
        "llm_system_description": "DispatchOptimizer AI Assistant",
        "llm_capabilities": ["Autonomous Route Generation", "API Dispatch Tooling"],
        "existing_controls": {
            "has_security_policy": True,
            "has_rbac_and_mfa": True,
            "has_prompt_firewall": False,
            "has_output_dlp": False,
            "has_human_in_the_loop_for_tools": False
        },
        "policy_documents": {}
    }
    resp = client.post("/audit/custom", json=custom_profile)
    assert resp.status_code == 200
    data = resp.json()
    assert data["organization_name"] == "Acme AI Corp"
    assert data["verdict"] in ["HIGH RISK", "CRITICAL RISK", "APPROVED WITH REMEDIATION"]
