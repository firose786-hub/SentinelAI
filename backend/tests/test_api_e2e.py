from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.samples.sample_data import SAMPLES

client = TestClient(app)
banking_sample = next(s for s in SAMPLES if s["id"] == "python-banking")
clean_sample = next(s for s in SAMPLES if s["id"] == "python-clean")
java_sample = next(s for s in SAMPLES if s["id"] == "java-login")


def test_api_validate_endpoint():
    res = client.post("/api/validate", json={
        "code": banking_sample["code"],
        "filename": banking_sample["filename"],
        "language": "Auto-detect",
    })
    assert res.status_code == 200
    data = res.json()
    assert data["language"] == "Python"
    assert data["syntaxValid"] is True


def test_api_analyze_banking_sample():
    res = client.post("/api/analyze", json={
        "code": banking_sample["code"],
        "filename": banking_sample["filename"],
        "language": "Python",
    })
    assert res.status_code == 200
    record = res.json()
    assert record["submission"]["filename"] == "banking_service.py"
    assert len(record["securityFindings"]) > 0
    assert record["summary"]["verdict"] in ("Block", "Request changes")
    assert "metrics" in record
    assert record["metrics"]["securityScore"] < 100

    # Test fetching the analysis
    record_id = record["id"]
    get_res = client.get(f"/api/analyses/{record_id}")
    assert get_res.status_code == 200

    # Test PDF download endpoint
    pdf_res = client.get(f"/api/reports/{record_id}/pdf")
    assert pdf_res.status_code == 200
    assert pdf_res.content.startswith(b"%PDF")


def test_api_analyze_clean_sample():
    res = client.post("/api/analyze", json={
        "code": clean_sample["code"],
        "filename": clean_sample["filename"],
        "language": "Python",
    })
    assert res.status_code == 200
    record = res.json()
    assert len(record["securityFindings"]) == 0
    assert record["metrics"]["securityScore"] == 100
    assert record["summary"]["verdict"] == "Approve"


def test_api_analyze_java_sample():
    res = client.post("/api/analyze", json={
        "code": java_sample["code"],
        "filename": java_sample["filename"],
        "language": "Java",
    })
    assert res.status_code == 200
    record = res.json()
    assert record["submission"]["language"] == "Java"
    assert len(record["securityFindings"]) > 0


def test_api_chat_endpoint():
    res = client.post("/api/chat", json={
        "question": "What is SQL injection?",
        "history": [],
    })
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert "citations" in data
    assert len(data["citations"]) > 0


def test_api_stats_endpoint():
    res = client.get("/api/stats")
    assert res.status_code == 200
    stats = res.json()
    assert "totalAnalyses" in stats
    assert "security" in stats


def test_html_routes_serving():
    routes = [
        "/",
        "/dashboard.html",
        "/analysis.html",
        "/findings.html",
        "/assistant.html",
        "/knowledge-base.html",
        "/reports.html",
        "/history.html",
    ]
    for r in routes:
        res = client.get(r)
        assert res.status_code == 200, f"Route {r} failed with status {res.status_code}"
        assert len(res.content) > 100

