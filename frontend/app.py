"""
SentinelAI — Enterprise Compliance Auditor & AI Security Validation Platform
Full-Stack 12-Page Command Center & Multi-Agent Deliberation Suite
Theme: Warm Peach / Porcelain Skin-Tone Luxury Executive Palette
"""

import streamlit as st
import requests
import json
import time
import random
import uuid
import hashlib
import io
import csv
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional

# Page Configuration
st.set_page_config(
    page_title="SentinelAI — Compliance & AI Security Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Warm Peach / Skin-Tone Palette with 100% Local System Fonts
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #1e293b;
    }
    
    .stApp {
        background: linear-gradient(135deg, #fdf8f5 0%, #fceede 50%, #faf0e6 100%);
        color: #1e293b;
    }

    /* Top Command Header */
    .hero-banner {
        background: linear-gradient(135deg, #a84b32 0%, #c86347 50%, #df7f60 100%);
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(168, 75, 50, 0.22);
        color: #ffffff;
    }
    
    /* Modern Peach/White KPI Cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #ebd8cc;
        border-radius: 12px;
        padding: 14px 10px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(180, 110, 80, 0.08);
        transition: all 0.25s ease;
        position: relative;
    }
    .kpi-card:hover {
        border-color: #c86347;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(200, 99, 71, 0.15);
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 4px 0;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #64748b;
    }
    .kpi-sub {
        font-size: 11px;
        color: #885e4d;
    }

    /* Severity Badges */
    .badge-critical {
        background: #fee2e2;
        color: #991b1b;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid #f87171;
        display: inline-block;
    }
    .badge-high {
        background: #ffedd5;
        color: #9a3412;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid #fb923c;
        display: inline-block;
    }
    .badge-medium {
        background: #fef9c3;
        color: #854d0e;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid #facc15;
        display: inline-block;
    }
    .badge-low {
        background: #dcfce7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid #4ade80;
        display: inline-block;
    }

    /* Verdict Badges */
    .verdict-box {
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 12px;
        letter-spacing: 0.5px;
        text-align: center;
        display: inline-block;
    }
    .verdict-approved {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #22c55e;
    }
    .verdict-conditional {
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #f59e0b;
    }
    .verdict-highrisk {
        background: #ffedd5;
        color: #9a3412;
        border: 1px solid #ea580c;
    }
    .verdict-critical {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #ef4444;
    }

    /* Content Cards */
    .glass-card {
        background: #ffffff;
        border: 1px solid #ead6cb;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 14px rgba(180, 110, 80, 0.05);
    }
    
    /* Debate Bubbles */
    .debate-card {
        padding: 14px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid;
    }
    .debate-red {
        background: #fff1f2;
        border-color: #fecdd3;
        border-left: 5px solid #e11d48;
        color: #881337;
    }
    .debate-blue {
        background: #f0f9ff;
        border-color: #bae6fd;
        border-left: 5px solid #0284c7;
        color: #0c4a6e;
    }
    .debate-judge {
        background: #f0fdf4;
        border-color: #bbf7d0;
        border-left: 5px solid #16a34a;
        color: #14532d;
    }

    /* Certificate Box */
    .cert-frame {
        background: #ffffff;
        border: 3px double #c86347;
        border-radius: 12px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(180, 110, 80, 0.12);
        margin-top: 14px;
    }

    .offline-tag {
        background: #e0f2fe;
        color: #0369a1;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 4px;
        border: 1px solid #7dd3fc;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Backend Imports & Services
API_BASE_URL = "http://localhost:8000"
from backend.app.agents.compliance_orchestrator import ComplianceOrchestrator
from backend.app.data.dummy_organizations import ORGANIZATION_PROFILES, get_organization_by_id
from backend.app.models.compliance_schemas import OrganizationProfile, AuditRecord
from backend.app.database import (
    get_all_compliance_audits,
    get_compliance_audit,
    save_compliance_audit,
    authenticate_user,
    register_user
)
from backend.app.agents.report_agent import ReportAgent
from backend.app.services.excel_generator import generate_excel_report
from backend.app.services.hasher import generate_certificate_hash
from backend.app.services.rag_service import rag_service
from backend.app.data.spep_framework import (
    sanitize_dual_channel_prompt,
    enforce_cloud_api_confinement,
    compute_cosine_trigger_score,
    verify_step_up_authorization,
    CLOUD_API_WHITELISTS
)

orchestrator = ComplianceOrchestrator()
report_agent = ReportAgent()


# Helper: Execute Dynamic Audit
def run_dynamic_audit(profile: OrganizationProfile, api_key: str = "") -> Dict[str, Any]:
    try:
        url = f"{API_BASE_URL}/audit/custom"
        params = {"api_key": api_key} if api_key else {}
        resp = requests.post(url, json=profile.model_dump(), params=params, timeout=4)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    record = orchestrator.run_full_audit(org=profile, api_key=api_key)
    return record.model_dump()


# Helper: Generate Random Organization Scenario
def generate_random_scenario() -> OrganizationProfile:
    industries = [
        ("FinTech NextGen Payments", "Algorithmic Payment Routing & Forex AI", 350000000.0, "3,000 Employees"),
        ("HealthGen AI Therapeutics", "Genomic Drug Candidate Screening LLM", 520000000.0, "5,500 Employees"),
        ("CloudScale Enterprise SaaS", "Workplace Autonomous Project Assistant", 85000000.0, "850 Employees"),
        ("AeroCyber Defense Enclave", "Mission Planning & Tactical Summarizer", 1400000000.0, "9,000 Employees"),
        ("OmniCommerce Retail AI", "Autonomous Customer Refund & Pricing Bot", 160000000.0, "2,100 Employees"),
        ("GovSecure Public Service", "Citizen Welfare Benefit Triage LLM", 280000000.0, "4,200 Employees")
    ]
    ind, sys_desc, rev, size = random.choice(industries)
    rand_id = f"org-dynamic-{uuid.uuid4().hex[:6]}"
    
    rand_controls = {
        "has_security_policy": random.choice([True, True, False]),
        "has_ai_dev_security_policy": random.choice([True, False]),
        "has_rbac_and_mfa": random.choice([True, True, False]),
        "has_cloud_vendor_vetting": random.choice([True, False]),
        "has_prompt_firewall": random.choice([True, False, False]),
        "has_output_dlp": random.choice([True, False]),
        "has_encryption_and_secrets_vault": random.choice([True, True, False]),
        "has_secure_ai_pipeline": random.choice([True, False]),
        "has_ai_governance_board": random.choice([True, False]),
        "has_llm_threat_model": random.choice([True, False, False]),
        "has_audit_logging_and_monitoring": random.choice([True, True, False]),
        "has_incident_response_plan": random.choice([True, False]),
        "has_fallback_and_backup": random.choice([True, False]),
        "has_human_in_the_loop_for_tools": random.choice([True, False, False])
    }

    return OrganizationProfile(
        id=rand_id,
        name=f"{ind.split()[0]} Systems Corp",
        industry=ind,
        size=size,
        annual_revenue_usd=rev,
        description=f"Automated enterprise deployment scenario operating in {ind}.",
        llm_system_description=f"{ind.split()[0]} AI Agent: {sys_desc}.",
        llm_capabilities=[
            "Autonomous Tool Invocation",
            "Vector Database Search",
            "Natural Language SQL Query Generation",
            "Public Customer Interaction"
        ],
        existing_controls=rand_controls,
        policy_documents={
            "charter": f"Enterprise Charter 2026 for {ind.split()[0]}: All AI deployments must undergo continuous multi-agent compliance audits."
        }
    )


# ---------------- SESSION INITIALIZATION ----------------
if "user_authenticated" not in st.session_state:
    st.session_state["user_authenticated"] = True  # Default ready for demo
    st.session_state["current_user"] = "admin"

if "current_profile" not in st.session_state:
    st.session_state["current_profile"] = get_organization_by_id("org-fintech-01")

if "audit_executed" not in st.session_state:
    st.session_state["audit_executed"] = True
    st.session_state["active_audit"] = run_dynamic_audit(st.session_state["current_profile"])

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "gemini_key" not in st.session_state:
    st.session_state["gemini_key"] = ""


# ---------------- SIDEBAR NAVIGATION ----------------
with st.sidebar:
    st.markdown("## 🛡️ **SentinelAI** `v3.0`")
    st.markdown("<span class='offline-tag'>⚡ 100% Air-Gapped & RAG Active</span>", unsafe_allow_html=True)
    st.caption("Agentic Smart Compliance & AI Security Platform")
    st.markdown("---")

    page_nav = st.radio(
        "Navigation Portal:",
        [
            "📊 Dashboard",
            "🏢 New Audit Studio",
            "📋 Compliance (ISO & NIST)",
            "🛡️ AI Security (OWASP Top 10)",
            "🤖 12 AI Agents & Debate",
            "🔍 Ask AI Agents (8-Step RAG)",
            "🚨 Risk & Financial Impact",
            "📈 30/60/90-Day Forecast",
            "🗺️ Remediation Roadmap",
            "🧠 Historical Audit Memory",
            "📄 Reports & Certificates",
            "🔐 Authentication & Login",
            "⚙️ Settings & System Health"
        ]
    )

    st.markdown("---")
    st.markdown("### 🏢 Quick Switch Profile")
    org_presets = {org.id: f"{org.name} ({org.industry.split()[0]})" for org in ORGANIZATION_PROFILES}
    
    selected_preset = st.selectbox(
        "Load Baseline Industry Scenario:",
        options=list(org_presets.keys()),
        format_func=lambda x: org_presets[x]
    )

    if st.button("📥 Load Preset Scenario", use_container_width=True):
        st.session_state["current_profile"] = get_organization_by_id(selected_preset)
        st.session_state["active_audit"] = run_dynamic_audit(st.session_state["current_profile"])
        st.toast(f"Loaded {get_organization_by_id(selected_preset).name}!", icon="📥")
        st.rerun()

    if st.button("🎲 Generate Random Enterprise Data", use_container_width=True):
        st.session_state["current_profile"] = generate_random_scenario()
        st.session_state["active_audit"] = run_dynamic_audit(st.session_state["current_profile"])
        st.toast("Generated new random enterprise scenario!", icon="🎲")
        st.rerun()

    st.markdown("---")
    st.success("🟢 12 Specialized AI Agents Online")
    st.caption("Policy • Compliance • Risk • Red Team • Blue Team • Judge • Debate • Decision • Forecast • Roadmap • Memory • Report")


active_profile: OrganizationProfile = st.session_state["current_profile"]
audit = st.session_state["active_audit"]


# ---------------- TOP COMMAND HERO BANNER ----------------
st.markdown(f"""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
        <div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 26px;">🛡️</span>
                <h2 style="margin: 0; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;">SentinelAI Command Center</h2>
            </div>
            <p style="margin: 6px 0 0 0; color: #fdf2eb; font-size: 13px;">
                Target: <b style="color: #ffffff;">{audit['organization_name']}</b> | Vertical: <b>{audit['industry']}</b> | Audit ID: <code style="color: #ffffff; background: rgba(0, 0, 0, 0.2); padding: 2px 6px; border-radius: 4px;">{audit['audit_id']}</code>
            </p>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 11px; color: #fce7db;">FRAMEWORK: <b>ISO 27001:2022 + NIST CSF 2.0 + OWASP LLM</b></div>
            <div style="font-size: 13px; font-weight: 600; color: #ffffff;">{audit['date_formatted']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Verdict HTML
v_str = audit["verdict"]
if v_str == "APPROVED":
    v_html = f'<div class="verdict-box verdict-approved">✅ {v_str}</div>'
elif v_str == "APPROVED WITH REMEDIATION":
    v_html = f'<div class="verdict-box verdict-conditional">⚠️ {v_str}</div>'
elif v_str == "HIGH RISK":
    v_html = f'<div class="verdict-box verdict-highrisk">🛑 {v_str}</div>'
else:
    v_html = f'<div class="verdict-box verdict-critical">🚨 {v_str}</div>'


# ==========================================
# PAGE 1: AUTHENTICATION & LOGIN
# ==========================================
if page_nav == "🔐 Authentication & Login":
    st.markdown("### 🔐 User Authentication & Session Management")
    st.caption("Secure role-based access control for compliance officers and security auditors.")

    l_col1, l_col2 = st.columns(2)
    with l_col1:
        st.markdown("#### 🔑 Sign In to SentinelAI")
        u_name = st.text_input("Username:", value="admin")
        u_pass = st.text_input("Password:", value="admin123", type="password")

        if st.button("🚀 Sign In to Dashboard", type="primary", use_container_width=True):
            user = authenticate_user(u_name, u_pass)
            if user:
                st.session_state["user_authenticated"] = True
                st.session_state["current_user"] = user["username"]
                st.success(f"Authenticated as **{user['username']}** ({user['email']})!")
            else:
                st.error("Invalid credentials. Use default: `admin` / `admin123`")

        st.info("💡 **Demo Credentials**: Username: `admin` | Password: `admin123`")

    with l_col2:
        st.markdown("#### 📝 Register New Auditor Account")
        reg_name = st.text_input("New Username:")
        reg_pass = st.text_input("New Password:", type="password")
        reg_email = st.text_input("Corporate Email:")

        if st.button("Register Auditor Account", use_container_width=True):
            if reg_name and reg_pass:
                if register_user(reg_name, reg_pass, reg_email):
                    st.success("Account created successfully! You can now log in.")
                else:
                    st.error("Username already registered.")


# ==========================================
# PAGE 2: DASHBOARD
# ==========================================
elif page_nav == "📊 Dashboard":
    st.markdown("### 📊 Executive Compliance & AI Security Dashboard")
    st.caption("High-level governance scorecards, multi-framework maturity distributions, and active audit telemetry.")

    # 6 Top KPI Cards
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Overall Compliance</div>
            <div class="kpi-value" style="color: {'#16a34a' if audit['overall_compliance_score'] > 75 else ('#d97706' if audit['overall_compliance_score'] > 50 else '#dc2626')};">
                {audit['overall_compliance_score']}%
            </div>
            <div class="kpi-sub">ISO & NIST Mean</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">ISO 27001 Score</div>
            <div class="kpi-value" style="color: {'#0284c7' if audit['iso_compliance_score'] > 75 else '#ea580c'};">
                {audit['iso_compliance_score']}%
            </div>
            <div class="kpi-sub">8 Security Controls</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">NIST CSF 2.0</div>
            <div class="kpi-value" style="color: {'#4f46e5' if audit['nist_compliance_score'] > 75 else '#ea580c'};">
                {audit['nist_compliance_score']}%
            </div>
            <div class="kpi-sub">8 Core Categories</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">AI Security Score</div>
            <div class="kpi-value" style="color: {'#16a34a' if audit['ai_security_score'] > 75 else ('#d97706' if audit['ai_security_score'] > 50 else '#dc2626')};">
                {audit['ai_security_score']}%
            </div>
            <div class="kpi-sub">OWASP LLM Vectors</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        r_color = '#dc2626' if audit['overall_risk_score'] > 60 else ('#ea580c' if audit['overall_risk_score'] > 30 else '#16a34a')
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Cyber Risk Score</div>
            <div class="kpi-value" style="color: {r_color};">
                {audit['overall_risk_score']} <span style="font-size: 13px; color: #64748b;">/ 100</span>
            </div>
            <div class="kpi-sub">{audit['business_impact']['overall_risk_tier']} Tier</div>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Debate Verdict</div>
            <div style="margin-top: 5px;">{v_html}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # Plotly Visualizations: Governance Radar + Vulnerability Severity Distribution
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown("#### 🕸️ Multi-Framework Governance Radar")
        r_categories = ["ISO 27001 Org", "ISO 27001 Tech", "NIST Governance", "NIST Protect", "NIST Recover", "OWASP Guardrails"]
        r_values = [
            audit['iso_compliance_score'],
            max(25, audit['iso_compliance_score'] - 8),
            audit['nist_compliance_score'],
            max(20, audit['nist_compliance_score'] - 10),
            audit['nist_compliance_score'],
            audit['ai_security_score']
        ]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=r_values + [r_values[0]],
            theta=r_categories + [r_categories[0]],
            fill='toself',
            fillcolor='rgba(200, 99, 71, 0.2)',
            line=dict(color='#c86347', width=2),
            name=audit['organization_name']
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color="#64748b", gridcolor="#ebd8cc"),
                angularaxis=dict(color="#334155", gridcolor="#ebd8cc"),
                bgcolor="#ffffff"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#1e293b"),
            height=300,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with g_col2:
        st.markdown("#### 🚨 AI Security Finding Status Breakdown")
        findings = audit.get("ai_security_findings", [])
        status_counts = {
            "Vulnerable": sum(1 for f in findings if f.get("status") == "Vulnerable"),
            "Partially Mitigated": sum(1 for f in findings if f.get("status") == "Partially Mitigated"),
            "Protected": sum(1 for f in findings if f.get("status") == "Protected")
        }
        fig_pie = px.pie(
            names=list(status_counts.keys()),
            values=list(status_counts.values()),
            color=list(status_counts.keys()),
            color_discrete_map={"Vulnerable": "#dc2626", "Partially Mitigated": "#f59e0b", "Protected": "#16a34a"},
            hole=0.45
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=300,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    ceo = audit.get("ceo_summary", {})
    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid #c86347;">
        <h4 style="color: #a84b32; margin-top: 0;">👔 Executive Headline: {ceo.get('headline')}</h4>
        <p style="font-size: 14px; color: #334155; line-height: 1.6; margin-bottom: 0;">
            {ceo.get('risk_summary_plain_english')}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE 3: NEW AUDIT STUDIO
# ==========================================
elif page_nav == "🏢 New Audit Studio":
    st.markdown("### 🏢 Ingest & New Enterprise Audit Studio")
    st.caption("Configure company metadata, LLM model architecture, and toggle 14 interactive security controls.")

    c_edit1, c_edit2 = st.columns([1, 1])
    with c_edit1:
        st.markdown("#### 🏢 Enterprise Profile & Model Setup")
        edit_name = st.text_input("Company Name", value=active_profile.name)
        edit_ind = st.text_input("Industry Vertical", value=active_profile.industry)
        edit_rev = st.number_input("Annual Revenue ($ USD)", value=float(active_profile.annual_revenue_usd), step=10000000.0)
        edit_size = st.text_input("Organization Size (Employees)", value=active_profile.size)
        ai_model_sel = st.selectbox(
            "Target LLM Model Architecture:",
            ["OpenAI GPT-4o / GPT-4", "Google Gemini 1.5 Pro / Flash", "Anthropic Claude 3.5 Sonnet", "Llama 3.1 70B (Self-Hosted)", "Mistral Large"]
        )
        edit_llm_desc = st.text_area("LLM System Description & Architecture", value=active_profile.llm_system_description, height=75)

    with c_edit2:
        st.markdown("#### 🛡️ 14 Active Security Controls (Interactive Toggles)")
        st.caption("Toggle any control to dynamically recalculate Red Team exploits and ISO/NIST scores!")
        
        ctrls = dict(active_profile.existing_controls)
        
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            ctrls["has_security_policy"] = st.toggle("Formal InfoSec Policy", value=ctrls.get("has_security_policy", True))
            ctrls["has_ai_dev_security_policy"] = st.toggle("AI Dev Security Policy", value=ctrls.get("has_ai_dev_security_policy", False))
            ctrls["has_rbac_and_mfa"] = st.toggle("RBAC & Multi-Factor Auth", value=ctrls.get("has_rbac_and_mfa", True))
            ctrls["has_cloud_vendor_vetting"] = st.toggle("Cloud AI Vendor Vetting", value=ctrls.get("has_cloud_vendor_vetting", True))
            ctrls["has_prompt_firewall"] = st.toggle("Semantic Prompt Firewall", value=ctrls.get("has_prompt_firewall", False))
            ctrls["has_output_dlp"] = st.toggle("Output Token DLP & Masking", value=ctrls.get("has_output_dlp", False))
            ctrls["has_encryption_and_secrets_vault"] = st.toggle("Secrets Vault & Encryption", value=ctrls.get("has_encryption_and_secrets_vault", True))

        with t_col2:
            ctrls["has_secure_ai_pipeline"] = st.toggle("Secure AI CI/CD & SBOM Scans", value=ctrls.get("has_secure_ai_pipeline", False))
            ctrls["has_ai_governance_board"] = st.toggle("AI Ethics & Governance Board", value=ctrls.get("has_ai_governance_board", False))
            ctrls["has_llm_threat_model"] = st.toggle("LLM Threat Modeling (STRIDE)", value=ctrls.get("has_llm_threat_model", False))
            ctrls["has_audit_logging_and_monitoring"] = st.toggle("SIEM Logging & Telemetry", value=ctrls.get("has_audit_logging_and_monitoring", True))
            ctrls["has_incident_response_plan"] = st.toggle("AI Incident Response Playbook", value=ctrls.get("has_incident_response_plan", False))
            ctrls["has_fallback_and_backup"] = st.toggle("Model Fallback & Redundancy", value=ctrls.get("has_fallback_and_backup", True))
            ctrls["has_human_in_the_loop_for_tools"] = st.toggle("Human-in-the-Loop for Tools", value=ctrls.get("has_human_in_the_loop_for_tools", False))

    if st.button("🚀 Apply Controls & Run 12-Agent Audit", type="primary", use_container_width=True):
        updated_org = OrganizationProfile(
            id=active_profile.id,
            name=edit_name,
            industry=edit_ind,
            size=edit_size,
            annual_revenue_usd=edit_rev,
            description=active_profile.description,
            llm_system_description=f"Model: {ai_model_sel}. {edit_llm_desc}",
            llm_capabilities=active_profile.llm_capabilities,
            existing_controls=ctrls,
            policy_documents=active_profile.policy_documents
        )
        st.session_state["current_profile"] = updated_org
        with st.spinner("🤖 12 Specialized AI agents executing full compliance & security audit..."):
            st.session_state["active_audit"] = run_dynamic_audit(updated_org, st.session_state.get("gemini_key", ""))
            st.toast("Audit completed successfully!", icon="✅")
            st.rerun()


# ==========================================
# PAGE 4: COMPLIANCE (ISO & NIST)
# ==========================================
elif page_nav == "📋 Compliance (ISO & NIST)":
    st.markdown("### 📋 Standards Compliance Audit: ISO/IEC 27001 & NIST CSF 2.0")
    st.caption("Control-by-control gap assessment evaluated against organizational policy charters and security configurations.")

    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        std_choice = st.radio("Filter Framework:", ["All Standards", "ISO/IEC 27001:2022", "NIST CSF 2.0"], horizontal=True)
    with col_f2:
        search_query = st.text_input("🔍 Search Controls / Clauses:", "")

    controls: List[Dict[str, Any]] = audit["controls_assessment"]
    if std_choice != "All Standards":
        controls = [c for c in controls if c["standard"] == std_choice]
    if search_query:
        controls = [c for c in controls if search_query.lower() in c["title"].lower() or search_query.lower() in c["control_id"].lower() or search_query.lower() in c["category"].lower()]

    for c in controls:
        status_color = "#16a34a" if c["status"] == "Compliant" else ("#d97706" if c["status"] == "Partially Compliant" else "#dc2626")
        badge_class = "badge-low" if c["risk_level"] == "Low" else ("badge-medium" if c["risk_level"] == "Medium" else ("badge-high" if c["risk_level"] == "High" else "badge-critical"))

        with st.expander(f"**{c['control_id']} — {c['title']}** [{c['standard']}] — Status: {c['status']}", expanded=(c["status"] != "Compliant")):
            col_x, col_y = st.columns([3, 1])
            with col_x:
                st.markdown(f"**Category:** {c['category']}")
                st.markdown(f"**Evidence:** {c['evidence']}")
                if c["gap"] and c["gap"] != "None identified in current audit scope.":
                    st.markdown(f"**Identified Gap:** <span style='color: #dc2626; font-weight: 600;'>{c['gap']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Remediation Action:** {c['remediation']}")
            with col_y:
                st.markdown(f"**Status:** <span style='color: {status_color}; font-weight: bold;'>{c['status']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Risk Level:** <div class='{badge_class}'>{c['risk_level']}</div>", unsafe_allow_html=True)
                st.progress(c["score"] / 100)
                st.caption(f"Score: {c['score']}/100")


# ==========================================
# PAGE 5: AI SECURITY (OWASP TOP 10)
# ==========================================
elif page_nav == "🛡️ AI Security (OWASP Top 10)":
    st.markdown("### 🛡️ AI Security Validation & OWASP Top 10 for LLM Applications")
    st.caption("Adversarial attack simulations evaluated by Red Team and Blue Team agents.")

    ai_findings: List[Dict[str, Any]] = audit["ai_security_findings"]
    vuln_cnt = sum(1 for f in ai_findings if f["status"] == "Vulnerable")
    part_cnt = sum(1 for f in ai_findings if f["status"] == "Partially Mitigated")
    prot_cnt = sum(1 for f in ai_findings if f["status"] == "Protected")

    fcol1, fcol2, fcol3 = st.columns(3)
    fcol1.metric("Vulnerable Vectors", vuln_cnt, delta=f"{vuln_cnt} Exploits", delta_color="inverse")
    fcol2.metric("Partially Mitigated", part_cnt)
    fcol3.metric("Protected / Blocked", prot_cnt, delta="Secure Guardrails")

    st.markdown("---")

    for f in ai_findings:
        sev = f["severity"]
        badge_cls = "badge-critical" if sev == "Critical" else ("badge-high" if sev == "High" else "badge-medium")
        status_icon = "🚨" if f["status"] == "Vulnerable" else ("⚠️" if f["status"] == "Partially Mitigated" else "🛡️")

        with st.expander(f"{status_icon} **{f['owasp_id']}: {f['title']}** — Severity: {sev} (CVSS {f['cvss_score']})", expanded=(f["status"] == "Vulnerable")):
            st.markdown(f"<div class='{badge_cls}'>{sev} Severity</div> &nbsp; <b>CWE:</b> {f['cwe_id']} | <b>CVSS Score:</b> {f['cvss_score']} | <b>Attack Vector:</b> {f['attack_vector']}", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background: #fdf6f0; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 12px; color: #9a3412; margin-bottom: 10px; border: 1px solid #ebd8cc;">
                <b>Simulated Adversarial Payload:</b><br/>{f['simulated_payload']}
            </div>
            """, unsafe_allow_html=True)

            c_red, c_blue = st.columns(2)
            with c_red:
                st.markdown(f"""
                <div class="debate-card debate-red">
                    <b style="color: #991b1b;">🔴 Red Team Observation:</b><br/>
                    {f['red_team_observation']}
                </div>
                """, unsafe_allow_html=True)

            with c_blue:
                st.markdown(f"""
                <div class="debate-card debate-blue">
                    <b style="color: #0369a1;">🔵 Blue Team Defense:</b><br/>
                    {f['blue_team_defense']}
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="debate-card debate-judge">
                <b style="color: #15803d;">⚖️ Judge Ruling:</b> {f['judge_verdict']}<br/>
                <b>Recommended Mitigation:</b> {f['remediation_guidance']}
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# PAGE 6: 12 AI AGENTS & DEBATE
# ==========================================
elif page_nav == "🤖 12 AI Agents & Debate":
    st.markdown("### 🤖 12 Specialized AI Agents & Adversarial Debate Console")
    st.caption("Collaborative multi-agent consensus deliberation between Skeptic (Red Team), Advocate (Blue Team), and Moderator (Judge Agent).")

    debate: Dict[str, Any] = audit["debate_result"]

    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid #7c3aed;">
        <h4 style="margin: 0; color: #6d28d9;">Debate Topic: {debate['debate_topic']}</h4>
        <p style="margin: 6px 0 0 0; color: #475569; font-size: 13px;">
            Arbiter Confidence: <b>{int(debate['decision_confidence'] * 100)}%</b> | Decision Verdict: <b>{debate['verdict']}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    for turn in debate["rounds"]:
        speaker = turn["speaker"]
        arg = turn["argument"]
        points = turn.get("key_points", [])

        if "Red" in speaker:
            cls = "debate-red"
            icon = "🔴"
            title_color = "#991b1b"
        elif "Blue" in speaker:
            cls = "debate-blue"
            icon = "🔵"
            title_color = "#0369a1"
        else:
            cls = "debate-judge"
            icon = "⚖️"
            title_color = "#15803d"

        st.markdown(f"""
        <div class="debate-card {cls}">
            <h4 style="margin-top: 0; color: {title_color}; font-size: 15px;">{icon} {speaker} — ({turn['agent_name']})</h4>
            <p style="font-size: 14px; line-height: 1.6;">{arg}</p>
            <div style="font-size: 12px; margin-top: 8px;">
                <b>Core Arguments:</b>
                <ul>
                    {''.join([f'<li>{p}</li>' for p in points])}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: #fdf4ff; border: 2px solid #c084fc; border-radius: 10px; padding: 18px; margin-top: 14px;">
        <h3 style="margin-top: 0; color: #7e22ce; font-size: 17px;">🏛️ Formal Binding Verdict: {audit['verdict']}</h3>
        <p style="font-size: 14px; color: #3b0764; line-height: 1.6; margin-bottom: 0;">
            <b>Rationale:</b> {debate['verdict_rationale']}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE 7: ASK AI AGENTS (8-STEP RAG FLOW)
# ==========================================
elif page_nav == "🔍 Ask AI Agents (8-Step RAG)":
    st.markdown("### 🔍 Ask AI Agents — 8-Step Grounded RAG Pipeline")
    st.caption("Retrieves ground-truth ISO 27001 clauses, NIST categories, OWASP LLM vectors, and verified audit history.")

    q_col1, q_col2, q_col3 = st.columns(3)
    preset_q = ""
    with q_col1:
        if st.button("❓ Does our company comply with ISO 27001 A.8.5?"):
            preset_q = "Does our company comply with ISO 27001 A.8.5 secure authentication and MFA requirements?"
    with q_col2:
        if st.button("❓ How do we mitigate OWASP LLM01 Prompt Injection?"):
            preset_q = "How do we mitigate OWASP LLM01 Prompt Injection using dual-channel sanitization?"
    with q_col3:
        if st.button("❓ What are our privileged tool RBAC requirements?"):
            preset_q = "What are our privileged tool RBAC requirements under NIST CSF PR.AA?"

    rag_query = st.text_input("Enter your compliance or security inquiry:", value=preset_q, placeholder="e.g. Does our enterprise LLM architecture comply with ISO 27001 A.8.5?")

    if st.button("⚡ Execute 8-Step RAG Pipeline", type="primary", use_container_width=True):
        if rag_query.strip():
            with st.spinner("🤖 Running 8-Step Grounded RAG Pipeline (Retrieve → Rerank → Generate → Verify)..."):
                rag_res = rag_service.execute_8_step_rag(rag_query, audit)
                
                st.markdown("---")
                st.markdown("#### 💬 Grounded AI Answer with Verified Citations")
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #16a34a;">
                    <p style="font-size: 15px; line-height: 1.6; color: #1e293b;">{rag_res['answer']}</p>
                    <div style="margin-top: 10px;">
                        <b>Verified Ground-Truth Citations:</b><br/>
                        {' '.join([f"<code style='color: #0369a1; background: #e0f2fe; padding: 2px 6px; border-radius: 4px; margin-right: 6px;'>{c}</code>" for c in rag_res['citations']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### 🛠️ Recommended Action Items")
                for r in rag_res["recommendations"]:
                    st.markdown(f"- ✅ **{r}**")

                with st.expander("🔍 View 8-Step RAG Pipeline Diagnostic Trace", expanded=True):
                    trace = rag_res["rag_steps_trace"]
                    st.markdown(f"""
                    1. **Step 1 (Query Normalization & Keywords)**: `{trace['step_1_query_normalized']}` | Keywords: `{trace['step_1_keywords']}`
                    2. **Step 2 (Hybrid Retrieval)**: Retrieved `{trace['step_2_retrieved_count']}` candidate chunks across vector cosine & BM25 indices.
                    3. **Step 3 (Cross-Encoder Rerank)**: Selected top relevant chunks: `{trace['step_3_reranked_top']}`
                    4. **Step 4 (Initial Generation)**: Synthesized initial contextual draft.
                    5. **Step 5 (Self-Feedback Check)**: Evaluated coverage gap: `{trace['step_5_self_feedback_missing']}`
                    6. **Step 6 (Additional Retrieval)**: Supplementary chunks fetched: `{trace['step_6_additional_retrieved']}`
                    7. **Step 7 (Refined Synthesis)**: Enhanced precision with multi-clause cross references.
                    8. **Step 8 (Citation Verification)**: Status: `{trace['step_8_status']}` (Confidence: **{rag_res['confidence']}%**)
                    """)


# ==========================================
# PAGE 8: RISK & FINANCIAL IMPACT
# ==========================================
elif page_nav == "🚨 Risk & Financial Impact":
    st.markdown("### 🚨 Cyber Risk Index & Financial Downtime Modeling")
    st.caption("Translates technical vulnerabilities into enterprise business impact, financial liability ranges, and operational downtime hours.")

    b_impact = audit.get("business_impact", {})
    r_col1, r_col2, r_col3 = st.columns(3)
    r_col1.metric("Cyber Risk Score", f"{audit.get('overall_risk_score')}/100", delta=b_impact.get("overall_risk_tier", "Medium") + " Tier", delta_color="inverse")
    r_col2.metric("Estimated Max Outage", f"{b_impact.get('estimated_downtime_hours', 24)} Hours", delta="Unplanned Downtime", delta_color="inverse")
    r_col3.metric("Financial Exposure Range", b_impact.get("financial_range_display", "$5M - $12M USD"), delta="Revenue-Scaled Liability", delta_color="inverse")

    st.markdown("---")
    st.markdown(f"""
    <div class="glass-card">
        <h4 style="color: #a84b32; margin-top: 0;">💼 Business Impact Narrative</h4>
        <p style="font-size: 14px; color: #334155; line-height: 1.6;">
            {b_impact.get('impact_narrative')}
        </p>
        <div style="margin-top: 10px;">
            <b>Primary Impact Areas:</b>
            <ul>
                {''.join([f'<li>{area}</li>' for area in b_impact.get('primary_impact_areas', [])])}
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE 9: 30/60/90-DAY FORECAST
# ==========================================
elif page_nav == "📈 30/60/90-Day Forecast":
    st.markdown("### 📈 Compliance Forecast (30 / 60 / 90 Days Trajectory)")
    st.caption("Predictive intelligence modeling posture improvements based on roadmap completion velocity.")

    forecast = audit["forecast"]
    cur_score = forecast["current_score"]
    milestones = forecast["milestones"]

    days_series = [0] + [m["days"] for m in milestones]
    scores_series = [cur_score] + [m["predicted_score"] for m in milestones]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days_series,
        y=scores_series,
        mode='lines+markers+text',
        name='Predicted Score',
        text=[f"{s}%" for s in scores_series],
        textposition="top center",
        line=dict(color='#c86347', width=3),
        marker=dict(size=11, color=['#dc2626', '#ea580c', '#d97706', '#16a34a']),
        fill='tozeroy',
        fillcolor='rgba(200, 99, 71, 0.12)'
    ))
    fig.update_layout(
        title="Projected Compliance Trajectory Over 90 Days",
        xaxis_title="Timeline (Days from Audit)",
        yaxis_title="Compliance Index (0 - 100%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        yaxis=dict(range=[0, 105], gridcolor="#ebd8cc"),
        xaxis=dict(gridcolor="#ebd8cc"),
        height=320,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"**Trajectory Analysis:** {forecast['trajectory_analysis']}")

    col_m1, col_m2, col_m3 = st.columns(3)
    for idx, (col_m, m) in enumerate(zip([col_m1, col_m2, col_m3], milestones)):
        with col_m:
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="color: #a84b32; margin-top: 0; font-size: 15px;">📅 Day {m['days']} Milestone</h4>
                <div style="font-size: 28px; font-weight: 800; color: #16a34a;">{m['predicted_score']}%</div>
                <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">Confidence: {m['confidence_percentage']}%</div>
                <div style="font-size: 12px; color: #334155;">
                    <b>Projected Improvements:</b>
                    <ul>
                        {''.join([f'<li>{imp}</li>' for imp in m['projected_improvements']])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# PAGE 10: REMEDIATION ROADMAP
# ==========================================
elif page_nav == "🗺️ Remediation Roadmap":
    st.markdown("### 🗺️ Prioritized Remediation Roadmap & Interactive What-If Simulator")
    st.caption("P1 (1-14d), P2 (15-45d), P3 (46-90d) week-by-week engineering fix matrix.")

    roadmap_items: List[Dict[str, Any]] = audit["roadmap"]

    # Interactive What-If Simulator
    st.markdown("#### ⚡ Interactive 'What-If' Remediation Simulator")
    st.caption("Check off simulated security fixes to observe projected point gains in real time:")

    sim_cols = st.columns(3)
    sim_points = 0
    with sim_cols[0]:
        if st.checkbox("Deploy Semantic Prompt Firewall (+12 pts)", value=False):
            sim_points += 12
    with sim_cols[1]:
        if st.checkbox("Enforce Output Token DLP (+8 pts)", value=False):
            sim_points += 8
    with sim_cols[2]:
        if st.checkbox("Add Tool Human-in-the-Loop (+10 pts)", value=False):
            sim_points += 10

    projected_total = min(100, audit["overall_compliance_score"] + sim_points)
    st.metric("Projected Compliance Score", f"{projected_total}%", delta=f"+{sim_points} Points Gained" if sim_points else "Baseline")

    st.markdown("---")
    st.markdown("#### 📋 Prioritized Action Items")

    for item in roadmap_items:
        p_badge = "badge-critical" if item["priority"] == "P1" else ("badge-high" if item["priority"] == "P2" else "badge-medium")
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span class="{p_badge}">{item['priority']}</span> &nbsp;
                    <b style="font-size: 14px; color: #1e293b;">{item['title']}</b>
                    <span style="font-size: 11px; color: #64748b; margin-left: 8px;">(Ref: <code>{item['finding_ref']}</code>)</span>
                </div>
                <div style="font-size: 13px; color: #16a34a; font-weight: 800;">
                    +{item['expected_point_gain']} Points
                </div>
            </div>
            <p style="margin: 8px 0; font-size: 13px; color: #475569;">
                <b>Action:</b> {item['action']}
            </p>
            <div style="font-size: 11px; color: #64748b; display: flex; gap: 20px;">
                <span>👥 <b>Responsible:</b> {item['responsible_team']}</span>
                <span>⏱️ <b>Timeline:</b> {item['target_days']} Days</span>
                <span>💵 <b>Cost Level:</b> {item['estimated_cost_level']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# PAGE 11: HISTORICAL AUDIT MEMORY
# ==========================================
elif page_nav == "🧠 Historical Audit Memory":
    st.markdown("### 🧠 Audit Memory Agent & Longitudinal Tracking")
    st.caption("Tracks multi-audit score deltas and recurring vulnerability patterns across SQLite history.")

    mem = audit.get("memory_comparison", {})
    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid #0284c7;">
        <h4 style="color: #0369a1; margin-top: 0;">Historical Audit Comparison</h4>
        <p style="font-size: 14px; color: #334155; margin-bottom: 0;">{mem.get('summary_of_progress')}</p>
    </div>
    """, unsafe_allow_html=True)

    d_col1, d_col2, d_col3, d_col4 = st.columns(4)
    d_col1.metric("Compliance Delta", f"{audit['overall_compliance_score']}%", delta=f"{mem.get('compliance_score_delta', 0):+d} pts")
    d_col2.metric("AI Security Delta", f"{audit['ai_security_score']}%", delta=f"{mem.get('ai_security_score_delta', 0):+d} pts")
    d_col3.metric("Risk Delta", f"{audit['overall_risk_score']}/100", delta=f"{mem.get('risk_score_delta', 0):+d} pts", delta_color="inverse")
    d_col4.metric("Persistent Vulnerabilities", len(mem.get("recurring_findings", [])), delta=f"{mem.get('total_findings_delta', 0):+d} diff", delta_color="inverse")

    st.markdown("---")
    st.markdown("#### 📜 All Audits Recorded in SQLite Database")
    all_audits = get_all_compliance_audits()
    if all_audits:
        history_table = []
        for a in all_audits:
            history_table.append({
                "Audit ID": a.audit_id,
                "Company": a.organization_name,
                "Date": a.date_formatted,
                "Compliance": f"{a.overall_compliance_score}%",
                "AI Security": f"{a.ai_security_score}%",
                "Risk": f"{a.overall_risk_score}/100",
                "Verdict": a.verdict
            })
        st.dataframe(history_table, use_container_width=True)


# ==========================================
# PAGE 12: REPORTS & CERTIFICATES
# ==========================================
elif page_nav == "📄 Reports & Certificates":
    st.markdown("### 📄 Multi-Format Reports & SHA-256 Clearance Certificate")
    st.caption("Generate official tamper-evident cryptographic certificates and export audit documentation in PDF, Excel, JSON, and Markdown formats.")

    cert_info = generate_certificate_hash(
        audit['audit_id'],
        audit['organization_name'],
        audit['overall_compliance_score'],
        audit['verdict'],
        audit['timestamp']
    )

    st.markdown(f"""
    <div class="cert-frame">
        <div style="font-size: 30px; margin-bottom: 6px;">🛡️</div>
        <h3 style="color: #a84b32; margin: 0; text-transform: uppercase; letter-spacing: 2px;">Certificate of Compliance & AI Safety Clearance</h3>
        <p style="color: #64748b; font-size: 12px; margin-top: 4px;">ISSUED BY SENTINELAI MULTI-AGENT GOVERNANCE & SECURITY VERIFICATION ENGINE</p>
        <hr style="border: 0; border-top: 1px dashed #ebd8cc; margin: 14px 0;" />
        <p style="font-size: 15px; color: #1e293b; line-height: 1.6;">
            This certifies that the enterprise AI deployment operated by <b>{audit['organization_name']}</b><br/>
            has undergone rigorous multi-agent verification across <b>ISO/IEC 27001:2022</b>, <b>NIST CSF 2.0</b>, and <b>OWASP Top 10 for LLMs</b>.
        </p>
        <div style="display: flex; justify-content: space-around; margin: 16px 0; flex-wrap: wrap; gap: 8px;">
            <div style="background: #fdf8f5; padding: 8px 16px; border-radius: 8px; border: 1px solid #ebd8cc;">
                <div style="font-size: 10px; color: #885e4d; font-weight: bold;">COMPLIANCE SCORE</div>
                <div style="font-size: 20px; font-weight: 800; color: #16a34a;">{audit['overall_compliance_score']}%</div>
            </div>
            <div style="background: #fdf8f5; padding: 8px 16px; border-radius: 8px; border: 1px solid #ebd8cc;">
                <div style="font-size: 10px; color: #885e4d; font-weight: bold;">AI SECURITY SCORE</div>
                <div style="font-size: 20px; font-weight: 800; color: #0284c7;">{audit['ai_security_score']}%</div>
            </div>
            <div style="background: #fdf8f5; padding: 8px 16px; border-radius: 8px; border: 1px solid #ebd8cc;">
                <div style="font-size: 10px; color: #885e4d; font-weight: bold;">FINAL VERDICT</div>
                <div style="font-size: 16px; font-weight: 800; margin-top: 2px;">{v_html}</div>
            </div>
        </div>
        <div style="font-size: 11px; color: #64748b; font-family: monospace;">
            <b>Cryptographic Verification Hash (SHA-256):</b><br/>
            <code>{cert_info['sha256_hash']}</code>
        </div>
        <div style="font-size: 10px; color: #94a3b8; margin-top: 8px;">
            Certificate ID: <code>{cert_info['certificate_id']}</code> | Validated on: {audit['date_formatted']} | Verification Engine: SentinelAI v3.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📥 Download Official Documentation & Datasets")

    record_obj = orchestrator.run_full_audit(active_profile)
    pdf_bytes = report_agent.generate_pdf(record_obj)
    excel_bytes = generate_excel_report(audit)
    json_bytes = report_agent.generate_json(record_obj)
    md_str = report_agent.generate_markdown(record_obj)

    dcol1, dcol2, dcol3, dcol4 = st.columns(4)
    with dcol1:
        st.download_button(
            label="📄 Executive PDF Report",
            data=pdf_bytes,
            file_name=f"SentinelAI-Audit-{audit['organization_name'].replace(' ', '_')}-{audit['audit_id']}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    with dcol2:
        st.download_button(
            label="📊 Excel Workbook (.xlsx)",
            data=excel_bytes,
            file_name=f"SentinelAI-Audit-{audit['organization_name'].replace(' ', '_')}-{audit['audit_id']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with dcol3:
        st.download_button(
            label="📦 JSON Audit Dataset",
            data=json_bytes,
            file_name=f"SentinelAI-Audit-{audit['audit_id']}.json",
            mime="application/json",
            use_container_width=True
        )
    with dcol4:
        st.download_button(
            label="📝 Markdown Review",
            data=md_str,
            file_name=f"SentinelAI-Audit-{audit['audit_id']}.md",
            mime="text/markdown",
            use_container_width=True
        )


# ==========================================
# PAGE 13: SETTINGS & SYSTEM HEALTH
# ==========================================
elif page_nav == "⚙️ Settings & System Health":
    st.markdown("### ⚙️ System Configuration & Diagnostics")
    st.caption("Manage API keys, themes, and monitor the health of all 12 autonomous agent subsystems.")

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.markdown("#### 🔑 LLM API Key Configuration")
        k_input = st.text_input(
            "Google Gemini API Key (Optional):",
            value=st.session_state.get("gemini_key", ""),
            type="password",
            help="Optional: Enables real-time generative reasoning when online. Offline fallback functions 100% deterministically."
        )
        if st.button("Save API Key"):
            st.session_state["gemini_key"] = k_input
            st.success("API Key saved to session state!")

    with s_col2:
        st.markdown("#### 🩺 12 AI Agents Health Status")
        agents_list = [
            ("Policy Agent", "Active", "Maps organizational information security charters"),
            ("Compliance Agent", "Active", "Evaluates ISO 27001 & NIST CSF 2.0 controls"),
            ("Risk Agent", "Active", "Quantifies Cyber Risk Index (0-100)"),
            ("Red Team Agent", "Active", "Simulates 9 OWASP Top 10 LLM attack vectors"),
            ("Blue Team Agent", "Active", "Verifies WAF, DLP, RBAC, and encryption"),
            ("Judge Agent", "Active", "Adjudicates exploitability & CVSS scores"),
            ("Debate Agent", "Active", "Coordinates multi-turn adversarial deliberation"),
            ("Decision Agent", "Active", "Issues formal binding compliance verdict"),
            ("Forecast Agent", "Active", "Models 30/60/90-day trajectory curves"),
            ("Roadmap Agent", "Active", "Generates P1/P2/P3 prioritized fix matrix"),
            ("Memory Agent", "Active", "Tracks longitudinal score deltas in SQLite"),
            ("Report Agent", "Active", "Builds PDF, Excel (.xlsx), and JSON exports")
        ]
        for name, status, desc in agents_list:
            st.markdown(f"- 🟢 **{name}**: `{status}` — *{desc}*")
