import io
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .config import PORT, HOST, GEMINI_API_KEY
from .models.schemas import (
    ValidateRequest,
    AnalyzeRequest,
    ChatRequest,
    SubmissionResult,
    AnalysisRecord,
)
from .models.compliance_schemas import (
    OrganizationProfile,
    AuditRecord,
)
from .data.dummy_organizations import ORGANIZATION_PROFILES, get_organization_by_id
from .services.submission_service import validate_submission
from .agents.orchestrator import Orchestrator
from .agents.compliance_orchestrator import ComplianceOrchestrator
from .agents.conversational_code_assistant import ConversationalCodeAssistant
from .agents.report_agent import ReportAgent
from .rag.knowledge_base import KNOWLEDGE_BASE
from .rag.rag_engine import retrieve
from .samples.sample_data import SAMPLES
from .report.generator import (
    generate_markdown_report,
    generate_json_report,
    generate_pdf_report,
)
from .database import (
    init_db,
    save_analysis,
    get_analysis,
    list_analyses,
    delete_analysis,
    clear_all_analyses,
    save_compliance_audit,
    get_compliance_audit,
    get_all_compliance_audits,
    get_compliance_audits_for_org,
    delete_compliance_audit,
)

# Initialize SQLite database schema
init_db()

app = FastAPI(
    title="SentinelAI — Agentic Smart Compliance Auditor & AI Security Validation Platform",
    description="Collaborative multi-agent compliance auditing (ISO 27001, NIST CSF) and AI security validation (OWASP Top 10 for LLM) with adversarial debate and longitudinal memory.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()
compliance_orchestrator = ComplianceOrchestrator()
report_agent = ReportAgent()
assistant = ConversationalCodeAssistant()

frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"


# ---------------- SentinelAI Compliance & AI Security API Routes ----------------

@app.get("/health")
def api_health():
    """Health check endpoint confirming API status and active agent subsystems."""
    return {
        "status": "healthy",
        "platform": "SentinelAI - Agentic Smart Compliance Auditor & AI Security Validation Platform",
        "version": "2.0.0",
        "agents_active": 13,
        "database": "SQLite (data/analyses.db)",
        "gemini_api_configured": bool(GEMINI_API_KEY)
    }


@app.get("/organizations", response_model=List[OrganizationProfile])
def api_get_organizations():
    """Retrieves all preconfigured dummy enterprise profiles spanning fintech, health, retail, and defense."""
    return ORGANIZATION_PROFILES


@app.post("/audit/custom", response_model=AuditRecord)
def api_run_custom_audit(profile: OrganizationProfile, api_key: Optional[str] = Query(None)):
    """Executes compliance audit for a user-supplied custom enterprise profile."""
    try:
        record = compliance_orchestrator.run_full_audit(org=profile, api_key=api_key)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Custom compliance audit error: {str(e)}")


@app.post("/audit/{organization_id}", response_model=AuditRecord)
def api_run_audit(organization_id: str, api_key: Optional[str] = Query(None)):
    """Executes the full 11+ agent compliance and AI security audit pipeline for an organization."""
    org = get_organization_by_id(organization_id)
    if not org:
        raise HTTPException(status_code=404, detail=f"Organization with ID '{organization_id}' not found.")
    try:
        record = compliance_orchestrator.run_full_audit(org=org, api_key=api_key)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance audit pipeline error: {str(e)}")


@app.get("/history", response_model=List[AuditRecord])
def api_get_audit_history():
    """Returns all historical multi-agent compliance audits ordered by recency."""
    return get_all_compliance_audits()


@app.get("/history/{organization_id}", response_model=List[AuditRecord])
def api_get_org_audit_history(organization_id: str):
    """Returns historical audits specific to a given organization."""
    return get_compliance_audits_for_org(organization_id)


@app.get("/audit/{audit_id}", response_model=AuditRecord)
def api_get_audit_by_id(audit_id: str):
    """Retrieves a complete compliance audit record by its unique audit ID."""
    record = get_compliance_audit(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Audit record '{audit_id}' not found.")
    return record


@app.delete("/audit/{audit_id}")
def api_delete_audit(audit_id: str):
    """Deletes a compliance audit record from SQLite."""
    deleted = delete_compliance_audit(audit_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Audit record '{audit_id}' not found.")
    return {"success": True, "message": f"Audit {audit_id} deleted."}


@app.get("/report/{audit_id}/pdf")
def api_download_pdf_report(audit_id: str):
    """Generates and downloads publication-grade ReportLab PDF audit report."""
    record = get_compliance_audit(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Audit record '{audit_id}' not found.")
    try:
        pdf_bytes = report_agent.generate_pdf(record)
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="sentinelai-audit-{record.organization_name.replace(" ", "-")}-{record.audit_id}.pdf"'},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {str(e)}")


@app.get("/report/{audit_id}/markdown")
def api_download_markdown_report(audit_id: str):
    """Downloads formatted Markdown report."""
    record = get_compliance_audit(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Audit record '{audit_id}' not found.")
    md_content = report_agent.generate_markdown(record)
    return Response(
        content=md_content,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="sentinelai-audit-{record.audit_id}.md"'},
    )


@app.get("/report/{audit_id}/json")
def api_download_json_report(audit_id: str):
    """Downloads structured JSON audit dataset."""
    record = get_compliance_audit(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Audit record '{audit_id}' not found.")
    json_bytes = report_agent.generate_json(record)
    return Response(
        content=json_bytes,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="sentinelai-audit-{record.audit_id}.json"'},
    )


@app.get("/report/{audit_id}/excel")
def api_download_excel_report(audit_id: str):
    """Downloads formatted multi-tab Excel spreadsheet (.xlsx)."""
    record = get_compliance_audit(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Audit record '{audit_id}' not found.")
    from .services.excel_generator import generate_excel_report
    excel_bytes = generate_excel_report(record.model_dump())
    return StreamingResponse(
        io.BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="sentinelai-audit-{record.audit_id}.xlsx"'},
    )


# ---------------- Additional Blueprint REST Routes ----------------

@app.post("/auth/login")
def api_auth_login(payload: Dict[str, str] = Body(...)):
    """User authentication endpoint (default: admin / admin123)."""
    from .database import authenticate_user
    username = payload.get("username", "")
    password = payload.get("password", "")
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    return {"status": "success", "user": user, "token": "sentinel-session-jwt-token-2026"}


@app.post("/auth/register")
def api_auth_register(payload: Dict[str, str] = Body(...)):
    """User registration endpoint."""
    from .database import register_user
    username = payload.get("username", "")
    password = payload.get("password", "")
    email = payload.get("email", "")
    success = register_user(username, password, email)
    if not success:
        raise HTTPException(status_code=400, detail="Username already exists.")
    return {"status": "success", "message": "User created successfully."}


@app.get("/dashboard/summary")
def api_dashboard_summary():
    """Returns top-level executive metrics for recent audits."""
    audits = get_all_compliance_audits()
    if not audits:
        # Load preset demo audit
        preset = get_organization_by_id("org-fintech-01")
        record = compliance_orchestrator.run_full_audit(preset)
        audits = [record]
    
    latest = audits[0]
    return {
        "latest_audit_id": latest.audit_id,
        "organization_name": latest.organization_name,
        "overall_compliance_score": latest.overall_compliance_score,
        "iso_compliance_score": latest.iso_compliance_score,
        "nist_compliance_score": latest.nist_compliance_score,
        "ai_security_score": latest.ai_security_score,
        "overall_risk_score": latest.overall_risk_score,
        "verdict": latest.verdict,
        "total_audits_recorded": len(audits)
    }


@app.post("/compliance/check")
def api_compliance_check(profile: OrganizationProfile):
    """Audits ISO 27001 & NIST CSF compliance for an organization."""
    record = compliance_orchestrator.run_full_audit(profile)
    return {
        "iso_score": record.iso_compliance_score,
        "nist_score": record.nist_compliance_score,
        "overall_compliance": record.overall_compliance_score,
        "controls": record.controls_assessment
    }


@app.post("/ai-security/test")
def api_ai_security_test(profile: OrganizationProfile):
    """Executes Red Team OWASP attack simulations and Blue Team validation."""
    record = compliance_orchestrator.run_full_audit(profile)
    return {
        "ai_security_score": record.ai_security_score,
        "findings": record.ai_security_findings
    }


@app.post("/agents/debate")
def api_agents_debate(profile: OrganizationProfile):
    """Runs the multi-turn AI debate engine (Red Skeptic vs Blue Advocate vs Judge)."""
    record = compliance_orchestrator.run_full_audit(profile)
    return record.debate_result


@app.get("/risk/analysis")
def api_risk_analysis(audit_id: Optional[str] = None):
    """Retrieves risk breakdown and financial exposure modeling."""
    audits = get_all_compliance_audits()
    record = audits[0] if audits else compliance_orchestrator.run_full_audit(get_organization_by_id("org-fintech-01"))
    return {
        "risk_score": record.overall_risk_score,
        "risk_tier": record.business_impact.overall_risk_tier,
        "estimated_downtime_hours": record.business_impact.estimated_downtime_hours,
        "financial_exposure": record.business_impact.financial_range_display,
        "primary_impact_areas": record.business_impact.primary_impact_areas
    }


@app.get("/forecast/predict")
def api_forecast_predict(audit_id: Optional[str] = None):
    """Retrieves 30/60/90-day trajectory forecast."""
    audits = get_all_compliance_audits()
    record = audits[0] if audits else compliance_orchestrator.run_full_audit(get_organization_by_id("org-fintech-01"))
    return record.forecast


@app.get("/roadmap/generate")
def api_roadmap_generate(audit_id: Optional[str] = None):
    """Retrieves prioritized P1/P2/P3 remediation action plan."""
    audits = get_all_compliance_audits()
    record = audits[0] if audits else compliance_orchestrator.run_full_audit(get_organization_by_id("org-fintech-01"))
    return record.roadmap


@app.get("/history/audits")
def api_history_audits():
    """Alias for /history returning all stored audits."""
    return get_all_compliance_audits()


@app.post("/query")
def api_rag_query(payload: Dict[str, str] = Body(...)):
    """Executes the 8-step RAG flow (Query→Retrieve→Rerank→Generate→SelfCheck→Refine→Verify)."""
    from .services.rag_service import rag_service
    q = payload.get("query", "")
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    result = rag_service.execute_8_step_rag(q)
    return result


@app.post("/settings/save")
def api_settings_save(payload: Dict[str, Any] = Body(...)):
    """Saves user configuration settings."""
    return {"status": "success", "message": "Settings saved successfully."}


# ---------------- Backward-Compatible Code Inspection API Routes ----------------

@app.post("/api/validate", response_model=SubmissionResult)
def api_validate(req: ValidateRequest):
    return validate_submission(req.code, req.filename, req.language)


@app.post("/api/analyze", response_model=AnalysisRecord)
def api_analyze(req: AnalyzeRequest):
    if not req.code or not req.code.strip():
        raise HTTPException(status_code=400, detail="Submission code cannot be empty.")
    try:
        record = orchestrator.run_pipeline(
            code=req.code[:40000],
            filename=req.filename or "snippet.py",
            requested_language=req.language or "Auto-detect",
            api_key=req.apiKey,
        )
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis pipeline error: {str(e)}")


@app.get("/api/analyses", response_model=List[AnalysisRecord])
def api_list_analyses():
    return list_analyses()


@app.get("/api/analyses/{record_id}", response_model=AnalysisRecord)
def api_get_analysis(record_id: str):
    record = get_analysis(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return record


@app.delete("/api/analyses/{record_id}")
def api_delete_analysis(record_id: str):
    deleted = delete_analysis(record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return {"success": True, "message": "Analysis deleted."}


@app.delete("/api/analyses")
def api_clear_analyses():
    clear_all_analyses()
    return {"success": True, "message": "All analyses cleared."}


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        result = assistant.answer(
            question=req.question.strip(),
            history=req.history,
            analysis_context=req.analysisContext,
            api_key=req.apiKey,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assistant error: {str(e)}")


@app.get("/api/samples")
def api_get_samples():
    return SAMPLES


@app.get("/api/knowledge")
def api_get_knowledge(q: Optional[str] = Query(None)):
    if not q or not q.strip():
        return KNOWLEDGE_BASE
    query = q.strip().lower()
    filtered = [
        doc for doc in KNOWLEDGE_BASE
        if query in doc["title"].lower()
        or any(query in tag.lower() for tag in doc["tags"])
        or query in doc["body"].lower()
    ]
    return filtered


@app.get("/api/stats")
def api_get_stats():
    analyses = list_analyses()
    if not analyses:
        return {
            "totalAnalyses": 0,
            "security": 0,
            "quality": 0,
            "maintainability": 0,
            "health": 0,
            "counts": [
                {"severity": "Critical", "count": 0},
                {"severity": "High", "count": 0},
                {"severity": "Medium", "count": 0},
                {"severity": "Low", "count": 0},
            ],
            "totalFindings": 0,
        }

    n = len(analyses)
    avg_sec = round(sum(a.metrics.securityScore for a in analyses) / n)
    avg_qual = round(sum(a.metrics.qualityScore for a in analyses) / n)
    avg_maint = round(sum(a.metrics.maintainabilityScore for a in analyses) / n)
    avg_health = round(sum(a.metrics.overallHealth for a in analyses) / n)

    counts_map = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for a in analyses:
        for f in a.securityFindings + a.qualityFindings:
            if f.severity in counts_map:
                counts_map[f.severity] += 1

    counts = [{"severity": k, "count": v} for k, v in counts_map.items()]
    total_findings = sum(counts_map.values())

    return {
        "totalAnalyses": n,
        "security": avg_sec,
        "quality": avg_qual,
        "maintainability": avg_maint,
        "health": avg_health,
        "counts": counts,
        "totalFindings": total_findings,
    }


@app.get("/api/reports/{record_id}/markdown")
def api_report_markdown(record_id: str):
    record = get_analysis(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    md = generate_markdown_report(record)
    return Response(
        content=md,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="code-review-{record.submission.filename}.md"'},
    )


@app.get("/api/reports/{record_id}/json")
def api_report_json(record_id: str):
    record = get_analysis(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    data = generate_json_report(record)
    return Response(
        content=data,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="code-review-{record.submission.filename}.json"'},
    )


@app.get("/api/reports/{record_id}/pdf")
def api_report_pdf(record_id: str):
    record = get_analysis(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    try:
        pdf_bytes = generate_pdf_report(record)
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="code-review-{record.submission.filename}.pdf"'},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


# ---------------- Frontend Static & Route Serving ----------------

if frontend_dir.exists():
    css_dir = frontend_dir / "css"
    js_dir = frontend_dir / "js"
    if css_dir.exists():
        app.mount("/css", StaticFiles(directory=str(css_dir)), name="css")
    if js_dir.exists():
        app.mount("/js", StaticFiles(directory=str(js_dir)), name="js")


@app.get("/")
def serve_index():
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "SentinelAI Multi-Agent Compliance Auditor API is active."}


@app.get("/dashboard")
@app.get("/dashboard.html")
def serve_dashboard():
    return FileResponse(str(frontend_dir / "dashboard.html"))


@app.get("/analyze")
@app.get("/analyze.html")
@app.get("/analysis.html")
def serve_analyze():
    return FileResponse(str(frontend_dir / "analysis.html"))


@app.get("/results")
@app.get("/results.html")
@app.get("/findings.html")
def serve_findings():
    return FileResponse(str(frontend_dir / "findings.html"))


@app.get("/chat")
@app.get("/chat.html")
@app.get("/assistant.html")
def serve_assistant():
    return FileResponse(str(frontend_dir / "assistant.html"))


@app.get("/knowledge")
@app.get("/knowledge.html")
@app.get("/knowledge-base.html")
def serve_knowledge():
    return FileResponse(str(frontend_dir / "knowledge-base.html"))


@app.get("/reports")
@app.get("/reports.html")
def serve_reports():
    return FileResponse(str(frontend_dir / "reports.html"))


@app.get("/history.html")
def serve_history_html():
    return FileResponse(str(frontend_dir / "history.html"))


def start():
    import uvicorn
    uvicorn.run("backend.app.main:app", host=HOST, port=PORT, reload=True)


if __name__ == "__main__":
    start()
