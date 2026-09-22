import threading
import time
import requests
import uvicorn
from app.main import app

def run_srv():
    uvicorn.run(app, host="127.0.0.1", port=5056, log_level="warning")

def main():
    t = threading.Thread(target=run_srv, daemon=True)
    t.start()
    time.sleep(2.0)

    base = "http://127.0.0.1:5056"
    routes = [
        "/",
        "/dashboard.html",
        "/analysis.html",
        "/findings.html",
        "/assistant.html",
        "/knowledge-base.html",
        "/reports.html",
        "/history.html",
        "/css/style.css",
        "/js/app.js",
        "/api/stats",
        "/api/samples",
        "/api/knowledge",
    ]

    print("=== TESTING ALL ROUTES ON LIVE SERVER ===")
    all_ok = True
    for r in routes:
        res = requests.get(f"{base}{r}")
        status = res.status_code
        print(f"{r} -> status {status} (length {len(res.content)})")
        if status != 200:
            all_ok = False

    # Check Landing page title and text
    root_res = requests.get(f"{base}/")
    if "Smart Code Inspection" not in root_res.text or "Group 2" not in root_res.text:
        print("ERROR: Root page missing project title")
        all_ok = False
    else:
        print("PASS: Root landing page contains exact project title & Group 2 branding")

    # Test POST analyze
    samples = requests.get(f"{base}/api/samples").json()
    banking_sample = samples[0]
    an_res = requests.post(f"{base}/api/analyze", json={
        "code": banking_sample["code"],
        "filename": banking_sample["filename"],
        "language": banking_sample["language"],
    })
    print(f"POST /api/analyze -> status {an_res.status_code}")
    rec = an_res.json()
    print(f"Analysis record id: {rec['id']}")
    print(f"Security findings count: {len(rec['securityFindings'])}")
    print(f"Quality findings count: {len(rec['qualityFindings'])}")
    print(f"Verdict: {rec['summary']['verdict']}")
    print(f"Security score: {rec['metrics']['securityScore']}")

    # Test PDF report endpoint
    pdf_res = requests.get(f"{base}/api/reports/{rec['id']}/pdf")
    print(f"GET /api/reports/{rec['id']}/pdf -> status {pdf_res.status_code} (length {len(pdf_res.content)})")
    if not pdf_res.content.startswith(b"%PDF"):
        all_ok = False
        print("ERROR: PDF response does not start with %PDF header")

    # Test Chat endpoint
    chat_res = requests.post(f"{base}/api/chat", json={
        "question": "How does SQL injection occur?",
        "history": [],
    })
    print(f"POST /api/chat -> status {chat_res.status_code}")
    chat_data = chat_res.json()
    print(f"Chat answer snippet: {chat_data['answer'][:80]}...")
    print(f"Chat citations count: {len(chat_data['citations'])}")

    print(f"\nALL LIVE HTTP ENDPOINTS VERIFIED: {all_ok}")
    return all_ok

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
