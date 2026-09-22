import json
from backend.app.agents.orchestrator import Orchestrator
from backend.app.report.generator import (
    generate_markdown_report,
    generate_json_report,
    generate_pdf_report,
)
from backend.app.samples.sample_data import SAMPLES

banking_sample = next(s for s in SAMPLES if s["id"] == "python-banking")


def test_markdown_report_generation():
    orch = Orchestrator()
    record = orch.run_pipeline(banking_sample["code"], banking_sample["filename"], "Python")

    md = generate_markdown_report(record)
    assert "# Code Review Report — banking_service.py" in md
    assert "CWE-89" in md
    assert "Executive overview" in md
    assert "Security" in md


def test_json_report_generation():
    orch = Orchestrator()
    record = orch.run_pipeline(banking_sample["code"], banking_sample["filename"], "Python")

    raw_json = generate_json_report(record)
    data = json.loads(raw_json)
    assert data["submission"]["filename"] == "banking_service.py"
    assert len(data["securityFindings"]) > 0


def test_pdf_report_generation():
    orch = Orchestrator()
    record = orch.run_pipeline(banking_sample["code"], banking_sample["filename"], "Python")

    pdf_bytes = generate_pdf_report(record)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 1000
