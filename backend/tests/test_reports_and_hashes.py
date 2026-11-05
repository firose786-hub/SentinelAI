"""
SentinelAI - Reporting & Cryptographic Integrity Unit Tests
Verifies PDF generation, Excel workbook generation, Markdown synthesis, and SHA-256 hashes.
"""

import pytest
import hashlib
from backend.app.agents.compliance_orchestrator import ComplianceOrchestrator
from backend.app.agents.report_agent import ReportAgent
from backend.app.services.excel_generator import generate_excel_report
from backend.app.services.hasher import generate_certificate_hash, generate_sha256_hash
from backend.app.data.dummy_organizations import get_organization_by_id

@pytest.fixture(scope="module")
def audit_record():
    orchestrator = ComplianceOrchestrator()
    org = get_organization_by_id("org-fintech-01")
    return orchestrator.run_full_audit(org=org)

def test_sha256_certificate_hasher(audit_record):
    cert = generate_certificate_hash(
        audit_id=audit_record.audit_id,
        org_name=audit_record.organization_name,
        compliance_score=audit_record.overall_compliance_score,
        verdict=audit_record.verdict,
        timestamp=audit_record.timestamp
    )
    assert "certificate_id" in cert
    assert "sha256_hash" in cert
    assert len(cert["sha256_hash"]) == 64  # Valid SHA-256 hex string
    assert cert["verification_status"] == "CRYPTOGRAPHICALLY_VERIFIED"

def test_reportlab_pdf_generation(audit_record):
    report_agent = ReportAgent()
    pdf_bytes = report_agent.generate_pdf(audit_record)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")  # Valid PDF header magic bytes

def test_openpyxl_excel_generation(audit_record):
    excel_bytes = generate_excel_report(audit_record.model_dump())
    assert isinstance(excel_bytes, bytes)
    assert len(excel_bytes) > 500
    # PK zip header for xlsx
    assert excel_bytes.startswith(b"PK") or b"CSV" in excel_bytes

def test_markdown_report_generation(audit_record):
    report_agent = ReportAgent()
    md_content = report_agent.generate_markdown(audit_record)
    assert isinstance(md_content, str)
    assert f"# Executive AI Security & Compliance Audit Report" in md_content
    assert audit_record.organization_name in md_content
    assert "ISO/IEC 27001" in md_content
    assert "OWASP Top 10" in md_content

def test_json_report_generation(audit_record):
    report_agent = ReportAgent()
    json_bytes = report_agent.generate_json(audit_record)
    assert isinstance(json_bytes, bytes)
    assert b"audit_id" in json_bytes
    assert b"controls_assessment" in json_bytes
