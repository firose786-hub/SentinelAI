"""
Report Agent
Synthesizes the complete multi-agent audit dataset into:
1. Executive PDF Audit Report (using ReportLab)
2. Structured Markdown Report
3. Machine-Readable JSON Export
"""

import io
import json
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from ..models.compliance_schemas import AuditRecord

class ReportAgent:
    def __init__(self):
        self.name = "Multi-Format Report Synthesis Agent"
        self.role = "Executive & Technical Document Synthesizer"

    def generate_pdf(self, record: AuditRecord) -> bytes:
        """
        Builds a comprehensive, publication-quality PDF audit report using ReportLab.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0f172a")
        )
        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#475569")
        )
        h1_style = ParagraphStyle(
            "Heading1_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#1e293b"),
            spaceBefore=12,
            spaceAfter=6
        )
        h2_style = ParagraphStyle(
            "Heading2_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#0369a1"),
            spaceBefore=8,
            spaceAfter=4
        )
        body_style = ParagraphStyle(
            "Body_Custom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#334155")
        )
        badge_style = ParagraphStyle(
            "Badge_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=colors.white,
            alignment=1
        )
        disclaimer_style = ParagraphStyle(
            "Disclaimer_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#64748b")
        )

        story = []

        # 1. Header Banner
        story.append(Paragraph("SENTINEL AI — COMPLIANCE & AI SECURITY AUDIT REPORT", subtitle_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"Executive Security Audit: {record.organization_name}", title_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            f"<b>Industry:</b> {record.industry} | <b>Date:</b> {record.date_formatted} | <b>Audit ID:</b> {record.audit_id}",
            body_style
        ))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=12))

        # 2. Executive Scorecards & Verdict Table
        verdict_color = (
            colors.HexColor("#dc2626") if record.verdict == "CRITICAL RISK" else
            (colors.HexColor("#ea580c") if record.verdict == "HIGH RISK" else
            (colors.HexColor("#d97706") if record.verdict == "APPROVED WITH REMEDIATION" else colors.HexColor("#16a34a")))
        )

        scorecard_data = [
            [
                Paragraph("<b>Overall Compliance</b>", body_style),
                Paragraph("<b>ISO 27001 Score</b>", body_style),
                Paragraph("<b>NIST CSF Score</b>", body_style),
                Paragraph("<b>AI Security Score</b>", body_style),
                Paragraph("<b>Risk Score</b>", body_style),
                Paragraph("<b>Debate Verdict</b>", body_style)
            ],
            [
                Paragraph(f"<font size=14><b>{record.overall_compliance_score}%</b></font>", body_style),
                Paragraph(f"<font size=14><b>{record.iso_compliance_score}%</b></font>", body_style),
                Paragraph(f"<font size=14><b>{record.nist_compliance_score}%</b></font>", body_style),
                Paragraph(f"<font size=14><b>{record.ai_security_score}%</b></font>", body_style),
                Paragraph(f"<font size=14><b>{record.overall_risk_score}/100</b></font>", body_style),
                Paragraph(f"<b>{record.verdict}</b>", badge_style)
            ]
        ]
        score_table = Table(scorecard_data, colWidths=[90, 85, 85, 90, 80, 110])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ('BACKGROUND', (5, 1), (5, 1), verdict_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 14))

        # 3. CEO Mode: Plain English Executive Summary
        story.append(Paragraph("1. Executive Summary (CEO Mode)", h1_style))
        story.append(Paragraph(f"<b>{record.ceo_summary.headline}</b>", h2_style))
        story.append(Paragraph(record.ceo_summary.risk_summary_plain_english, body_style))
        story.append(Spacer(1, 6))

        story.append(Paragraph("<b>Top Priority Risks:</b>", body_style))
        for r in record.ceo_summary.top_3_risks:
            story.append(Paragraph(f"• {r}", body_style))
        story.append(Spacer(1, 6))

        story.append(Paragraph("<b>Immediate Recommended Actions:</b>", body_style))
        for a in record.ceo_summary.top_3_recommended_actions:
            story.append(Paragraph(f"• {a}", body_style))
        story.append(Spacer(1, 12))

        # 4. Business Impact Analysis
        story.append(Paragraph("2. Quantitative Business Impact Assessment", h1_style))
        story.append(Paragraph(record.business_impact.impact_narrative, body_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            f"<b>Estimated Financial Exposure:</b> {record.business_impact.financial_range_display} | "
            f"<b>Estimated Outage Downtime:</b> {record.business_impact.estimated_downtime_hours:.1f} Hours | "
            f"<b>Risk Level:</b> {record.business_impact.overall_risk_tier}",
            body_style
        ))
        story.append(Spacer(1, 12))

        # 5. Multi-Agent AI Debate Transcript
        story.append(Paragraph("3. Multi-Agent AI Debate Engine Ruling", h1_style))
        debate_rows = [
            [Paragraph("<b>Speaker</b>", body_style), Paragraph("<b>Argument & Rationale</b>", body_style)]
        ]
        for turn in record.debate_result.rounds:
            speaker_color = (
                "#991b1b" if "Red" in turn.speaker else
                ("#075985" if "Blue" in turn.speaker else "#15803d")
            )
            debate_rows.append([
                Paragraph(f"<font color='{speaker_color}'><b>{turn.speaker}</b></font>", body_style),
                Paragraph(turn.argument, body_style)
            ])
        debate_table = Table(debate_rows, colWidths=[140, 400])
        debate_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(debate_table)
        story.append(Spacer(1, 12))

        # 6. AI Security Findings (OWASP Top 10 for LLM)
        story.append(Paragraph("4. AI Security Validation & OWASP LLM Assessment", h1_style))
        ai_rows = [
            [
                Paragraph("<b>OWASP ID</b>", body_style),
                Paragraph("<b>Vulnerability Title</b>", body_style),
                Paragraph("<b>Severity</b>", body_style),
                Paragraph("<b>Status</b>", body_style),
                Paragraph("<b>Judge Verdict / Mitigation</b>", body_style)
            ]
        ]
        for f in record.ai_security_findings:
            sev_color = (
                "#dc2626" if f.severity == "Critical" else
                ("#ea580c" if f.severity == "High" else "#ca8a04")
            )
            status_color = "#dc2626" if f.status == "Vulnerable" else ("#ca8a04" if f.status == "Partially Mitigated" else "#16a34a")
            ai_rows.append([
                Paragraph(f"<b>{f.owasp_id}</b>", body_style),
                Paragraph(f"{f.title}<br/><font size=7 color='#64748b'>CWE: {f.cwe_id} | CVSS: {f.cvss_score}</font>", body_style),
                Paragraph(f"<font color='{sev_color}'><b>{f.severity}</b></font>", body_style),
                Paragraph(f"<font color='{status_color}'><b>{f.status}</b></font>", body_style),
                Paragraph(f"{f.remediation_guidance[:140]}...", body_style)
            ])
        ai_table = Table(ai_rows, colWidths=[65, 135, 60, 75, 205])
        ai_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(ai_table)
        story.append(Spacer(1, 12))

        # 7. Compliance Forecast & Trajectory
        story.append(Paragraph("5. Compliance Forecast (30 / 60 / 90 Days)", h1_style))
        story.append(Paragraph(record.forecast.trajectory_analysis, body_style))
        story.append(Spacer(1, 4))
        forecast_rows = [
            [
                Paragraph("<b>Milestone</b>", body_style),
                Paragraph("<b>Projected Score</b>", body_style),
                Paragraph("<b>Confidence</b>", body_style),
                Paragraph("<b>Projected Improvements</b>", body_style)
            ]
        ]
        for m in record.forecast.milestones:
            forecast_rows.append([
                Paragraph(f"<b>Day {m.days}</b>", body_style),
                Paragraph(f"<b>{m.predicted_score}%</b>", body_style),
                Paragraph(f"{m.confidence_percentage}%", body_style),
                Paragraph("; ".join(m.projected_improvements), body_style)
            ])
        forecast_table = Table(forecast_rows, colWidths=[70, 90, 75, 305])
        forecast_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(forecast_table)
        story.append(Spacer(1, 12))

        # 8. Remediation Roadmap
        story.append(Paragraph("6. Remediation Roadmap (P1 / P2 / P3 Action Plan)", h1_style))
        roadmap_rows = [
            [
                Paragraph("<b>Priority</b>", body_style),
                Paragraph("<b>Action Title</b>", body_style),
                Paragraph("<b>Responsible Team</b>", body_style),
                Paragraph("<b>Target Days</b>", body_style),
                Paragraph("<b>Point Gain</b>", body_style)
            ]
        ]
        for item in record.roadmap[:8]:
            p_color = "#dc2626" if item.priority == "P1" else ("#ea580c" if item.priority == "P2" else "#2563eb")
            roadmap_rows.append([
                Paragraph(f"<font color='{p_color}'><b>{item.priority}</b></font>", body_style),
                Paragraph(f"<b>{item.title}</b><br/><font size=7 color='#64748b'>{item.action[:80]}...</font>", body_style),
                Paragraph(item.responsible_team, body_style),
                Paragraph(f"{item.target_days} Days", body_style),
                Paragraph(f"+{item.expected_point_gain} pts", body_style)
            ])
        roadmap_table = Table(roadmap_rows, colWidths=[55, 205, 140, 75, 65])
        roadmap_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(roadmap_table)
        story.append(Spacer(1, 12))

        # 9. Audit Memory & Longitudinal History
        story.append(Paragraph("7. Audit Memory & Multi-Audit Evolution", h1_style))
        story.append(Paragraph(record.memory_comparison.summary_of_progress, body_style))
        story.append(Spacer(1, 6))

        # 10. IEEE SPEP Cloud Prompt Defense & Benchmark (IEEE ICAIC 2026)
        story.append(Paragraph("8. IEEE SPEP Cloud Defense & ASR Benchmark", h1_style))
        spep_data = [
            [
                Paragraph("<b>Cloud Platform</b>", body_style),
                Paragraph("<b>Baseline ASR</b>", body_style),
                Paragraph("<b>Hardened ASR</b>", body_style),
                Paragraph("<b>Attack Reduction</b>", body_style),
                Paragraph("<b>Trust Deviation</b>", body_style),
                Paragraph("<b>Latency Overhead</b>", body_style)
            ],
            [
                Paragraph(getattr(record.spep_metrics, "cloud_platform", "AWS/Azure/GCP Hybrid"), body_style),
                Paragraph(f"<font color='#dc2626'><b>{getattr(record.spep_metrics, 'baseline_asr_pct', 80.0)}%</b></font>", body_style),
                Paragraph(f"<font color='#16a34a'><b>{getattr(record.spep_metrics, 'spep_hardened_asr_pct', 7.0)}%</b></font>", body_style),
                Paragraph(f"<b>~{getattr(record.spep_metrics, 'asr_reduction_pct', 91.25)}%</b>", body_style),
                Paragraph(f"{getattr(record.spep_metrics, 'trust_deviation_metric', 0.04)} TDM", body_style),
                Paragraph(f"+{getattr(record.spep_metrics, 'latency_overhead_ms', 42.0)} ms", body_style)
            ]
        ]
        spep_table = Table(spep_data, colWidths=[120, 80, 85, 95, 80, 80])
        spep_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f0fdf4")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#bbf7d0")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(spep_table)
        story.append(Spacer(1, 10))

        # 11. Research Disclaimer Banner
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=6, spaceBefore=8))
        story.append(Paragraph(
            "<b>RESEARCH NOTICE & COMPLIANCE DISCLAIMER:</b> This audit report was automatically generated by SentinelAI, "
            "an academic and research-oriented multi-agent compliance platform. Evaluated controls represent simplified benchmarks "
            "and do not constitute legal compliance determination or official ISO/IEC 27001 or NIST certification. "
            "Business impact and forecast models are illustrative risk approximations for research demonstration.",
            disclaimer_style
        ))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    def generate_markdown(self, record: AuditRecord) -> str:
        """
        Generates a comprehensive Markdown version of the audit report.
        """
        md = f"""# SentinelAI Audit Report: {record.organization_name}

**Audit ID:** `{record.audit_id}`  
**Date:** {record.date_formatted}  
**Industry:** {record.industry}  
**Debate Verdict:** **{record.verdict}**  

---

## Executive Scorecard

| Metric | Score | Status |
| :--- | :--- | :--- |
| **Overall Compliance Score** | **{record.overall_compliance_score}%** | {'Satisfactory' if record.overall_compliance_score > 70 else 'Deficient'} |
| **ISO/IEC 27001:2022** | **{record.iso_compliance_score}%** | {'Aligned' if record.iso_compliance_score > 70 else 'Gaps Found'} |
| **NIST CSF 2.0** | **{record.nist_compliance_score}%** | {'Aligned' if record.nist_compliance_score > 70 else 'Gaps Found'} |
| **AI Security Score** | **{record.ai_security_score}%** | {'Hardened' if record.ai_security_score > 70 else 'Vulnerable'} |
| **Overall Cyber Risk Score** | **{record.overall_risk_score} / 100** | {record.business_impact.overall_risk_tier} Risk |

---

## 1. Executive Summary (CEO Mode)

**{record.ceo_summary.headline}**

{record.ceo_summary.risk_summary_plain_english}

### Top 3 Business Risks
"""
        for r in record.ceo_summary.top_3_risks:
            md += f"- {r}\n"

        md += "\n### Top 3 Immediate Actions\n"
        for a in record.ceo_summary.top_3_recommended_actions:
            md += f"- {a}\n"

        md += f"\n**30/60/90-Day Outlook:** {record.ceo_summary.outlook_30_60_90}\n\n"

        md += f"""---

## 2. Business Impact Analysis

- **Estimated Downtime:** {record.business_impact.estimated_downtime_hours:.1f} Hours
- **Estimated Financial Exposure:** {record.business_impact.financial_range_display}
- **Impacted Areas:** {', '.join(record.business_impact.primary_impact_areas)}

> *{record.business_impact.disclaimer}*

---

## 3. AI Debate Engine Ruling

**Debate Topic:** {record.debate_result.debate_topic}

"""
        for turn in record.debate_result.rounds:
            md += f"### {turn.speaker}\n*{turn.argument}*\n\n"

        md += f"**Final Decision Rationale:** {record.debate_result.verdict_rationale}\n\n"

        md += """---

## 4. AI Security Validation (OWASP Top 10 for LLM)

| OWASP ID | Vulnerability | Severity | Status | CVSS | Remediation |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
        for f in record.ai_security_findings:
            md += f"| **{f.owasp_id}** | {f.title} | `{f.severity}` | **{f.status}** | {f.cvss_score} | {f.remediation_guidance[:100]}... |\n"

        md += f"""

---

## 5. Compliance Forecast

{record.forecast.trajectory_analysis}

| Milestone | Predicted Score | Confidence | Projected Gains |
| :--- | :--- | :--- | :--- |
"""
        for m in record.forecast.milestones:
            md += f"| **Day {m.days}** | **{m.predicted_score}%** | {m.confidence_percentage}% | {'; '.join(m.projected_improvements)} |\n"

        md += f"\n> *{record.forecast.disclaimer}*\n\n"

        md += """---

## 6. Remediation Roadmap

| Priority | Finding Ref | Action Title | Responsible Team | Target Days | Point Gain |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
        for item in record.roadmap:
            md += f"| **{item.priority}** | `{item.finding_ref}` | {item.title} | {item.responsible_team} | {item.target_days} Days | +{item.expected_point_gain} pts |\n"

        md += f"""

---

## 7. Audit Memory & Evolution

{record.memory_comparison.summary_of_progress}

---

*Generated by SentinelAI Multi-Agent Compliance Platform.*
"""
        return md

    def generate_json(self, record: AuditRecord) -> str:
        """
        Exports audit record as formatted JSON.
        """
        return json.dumps(record.model_dump(), indent=2)
