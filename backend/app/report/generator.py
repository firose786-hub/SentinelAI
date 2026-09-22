import io
import json
from datetime import datetime
from typing import Optional
from ..models.schemas import AnalysisRecord


def generate_markdown_report(a: AnalysisRecord) -> str:
    lines = []
    push = lambda s="": lines.append(s)

    created_str = datetime.fromtimestamp(a.createdAt / 1000).strftime("%Y-%m-%d %H:%M:%S UTC")

    push(f"# Code Review Report — {a.submission.filename}")
    push()
    push("*Smart Code Inspection Platform with Vulnerability Detection System — Group 2*")
    push()
    push(f"- **Language:** {a.submission.language}")
    push(f"- **Lines:** {a.submission.lineCount}")
    push(f"- **Generated:** {created_str}")
    push(f"- **Verdict:** {a.summary.verdict}")
    push()
    push("## Executive overview")
    push()
    push(a.summary.executiveOverview)
    push()
    push("## Scores")
    push()
    push("| Metric | Score |")
    push("| --- | --- |")
    push(f"| Security | {a.metrics.securityScore}/100 |")
    push(f"| Code quality | {a.metrics.qualityScore}/100 |")
    push(f"| Maintainability | {a.metrics.maintainabilityScore}/100 |")
    push(f"| Overall health | {a.metrics.overallHealth}/100 |")
    push(f"| Complexity | {a.metrics.complexity} |")
    push()
    push("## Severity breakdown")
    push()
    for sev, count in a.summary.severityBreakdown.items():
        push(f"- **{sev}:** {count}")
    push()
    push("## Security vulnerabilities (Security Vulnerability Agent)")
    push()
    if not a.securityFindings:
        push("_None detected._")
    for f in a.securityFindings:
        push(f"### [{f.severity}] {f.title}")
        push(f"- OWASP: {f.owaspCategory} · {f.cwe}")
        push(f"- Location: line {f.line}" if f.line else "- Location: file-level")
        push(f"- {f.detail}")
        if f.evidence:
            push(f"- Evidence: `{f.evidence}`")
        rem = next((r for r in a.remediations if r.findingId == f.id), None)
        if rem:
            push(f"- **Fix:** {rem.recommendation}")
            if rem.correctedCode:
                push()
                push("```")
                push(rem.correctedCode)
                push("```")
        push()

    push("## Code quality findings (Code Analysis Agent)")
    push()
    if not a.qualityFindings:
        push("_None detected._")
    for f in a.qualityFindings:
        push(f"### [{f.severity}] {f.title}")
        push(f"- Category: {f.category} · " + (f"line {f.line}" if f.line else "file-level"))
        push(f"- {f.detail}")
        rem = next((r for r in a.remediations if r.findingId == f.id), None)
        if rem:
            push(f"- **Fix:** {rem.recommendation}")
        push()

    push("## Prioritised remediation roadmap")
    push()
    for i, fix in enumerate(a.summary.prioritizedFixes, 1):
        push(f"{i}. {fix}")
    push()
    push("## Knowledge base grounding")
    push()
    for c in a.knowledgeCitations:
        push(f"- {c}")
    push()

    return "\n".join(lines)


def generate_json_report(a: AnalysisRecord) -> str:
    return json.dumps(a.model_dump(), indent=2)


def generate_pdf_report(a: AnalysisRecord, output_path: Optional[str] = None) -> bytes:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        KeepTogether,
        HRFlowable,
    )

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer if not output_path else output_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#2C221E"),
    )
    subtitle_style = ParagraphStyle(
        "ReportSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#7A6B63"),
    )
    h2_style = ParagraphStyle(
        "ReportH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#B84B28"),
        spaceBefore=12,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2C221E"),
    )
    code_style = ParagraphStyle(
        "ReportCode",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1F2937"),
        backColor=colors.HexColor("#F3F4F6"),
    )

    elements = []

    # Title & Subtitle
    elements.append(Paragraph(f"Code Review Report — {a.submission.filename}", title_style))
    elements.append(Paragraph("Smart Code Inspection Platform with Vulnerability Detection System — Group 2", subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#E5DCD3"), spaceAfter=12))

    # Meta Table
    created_str = datetime.fromtimestamp(a.createdAt / 1000).strftime("%Y-%m-%d %H:%M:%S UTC")
    meta_data = [
        [
            Paragraph(f"<b>Language:</b> {a.submission.language}", body_style),
            Paragraph(f"<b>Lines:</b> {a.submission.lineCount}", body_style),
        ],
        [
            Paragraph(f"<b>Generated:</b> {created_str}", body_style),
            Paragraph(f"<b>Verdict:</b> <b>{a.summary.verdict}</b>", body_style),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[260, 260])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FBF9F5")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#E5DCD3")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5DCD3")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 12))

    # Executive Overview
    elements.append(Paragraph("Executive Overview", h2_style))
    elements.append(Paragraph(a.summary.executiveOverview, body_style))
    elements.append(Spacer(1, 10))

    # Scores Table
    elements.append(Paragraph("Inspection Scores", h2_style))
    score_data = [
        ["Security Score", "Code Quality", "Maintainability", "Overall Health", "Complexity"],
        [
            f"{a.metrics.securityScore}/100",
            f"{a.metrics.qualityScore}/100",
            f"{a.metrics.maintainabilityScore}/100",
            f"{a.metrics.overallHealth}/100",
            a.metrics.complexity,
        ],
    ]
    score_table = Table(score_data, colWidths=[104, 104, 104, 104, 104])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3EBE3")),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FBF9F5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#7A6B63")),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor("#2C221E")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#E5DCD3")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5DCD3")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(score_table)
    elements.append(Spacer(1, 12))

    # Severity Breakdown
    elements.append(Paragraph("Severity Breakdown", h2_style))
    sev_text = " | ".join(f"<b>{k}:</b> {v}" for k, v in a.summary.severityBreakdown.items())
    elements.append(Paragraph(sev_text, body_style))
    elements.append(Spacer(1, 10))

    # Security Vulnerabilities
    elements.append(Paragraph(f"Security Vulnerabilities ({len(a.securityFindings)})", h2_style))
    if not a.securityFindings:
        elements.append(Paragraph("<i>No security vulnerabilities detected.</i>", body_style))
    else:
        for f in a.securityFindings:
            loc = f"Line {f.line}" if f.line else "File-level"
            f_card = [
                Paragraph(f"<b>[{f.severity}] {f.title}</b> ({f.owaspCategory} · {f.cwe})", body_style),
                Paragraph(f"<b>Location:</b> {loc} | <b>Detail:</b> {f.detail}", body_style),
            ]
            if f.evidence:
                f_card.append(Paragraph(f"<b>Evidence:</b> <font name='Courier'>{f.evidence}</font>", body_style))
            rem = next((r for r in a.remediations if r.findingId == f.id), None)
            if rem:
                f_card.append(Paragraph(f"<b>Fix:</b> {rem.recommendation}", body_style))
                if rem.bestPractice:
                    f_card.append(Paragraph(f"<b>Best Practice:</b> {rem.bestPractice}", body_style))
                if rem.correctedCode:
                    f_card.append(Paragraph(rem.correctedCode.replace("\n", "<br/>"), code_style))

            elements.append(KeepTogether(f_card))
            elements.append(Spacer(1, 8))

    # Quality Findings
    elements.append(Paragraph(f"Code Quality Findings ({len(a.qualityFindings)})", h2_style))
    if not a.qualityFindings:
        elements.append(Paragraph("<i>No code quality issues detected.</i>", body_style))
    else:
        for f in a.qualityFindings:
            loc = f"Line {f.line}" if f.line else "File-level"
            q_card = [
                Paragraph(f"<b>[{f.severity}] {f.title}</b> ({f.category})", body_style),
                Paragraph(f"<b>Location:</b> {loc} | <b>Detail:</b> {f.detail}", body_style),
            ]
            rem = next((r for r in a.remediations if r.findingId == f.id), None)
            if rem:
                q_card.append(Paragraph(f"<b>Fix:</b> {rem.recommendation}", body_style))

            elements.append(KeepTogether(q_card))
            elements.append(Spacer(1, 6))

    # Prioritized Roadmap
    elements.append(Paragraph("Prioritised Remediation Roadmap", h2_style))
    for i, fix in enumerate(a.summary.prioritizedFixes, 1):
        elements.append(Paragraph(f"<b>{i}.</b> {fix}", body_style))
    elements.append(Spacer(1, 10))

    # Knowledge Grounding
    elements.append(Paragraph("Knowledge Grounding Citations", h2_style))
    for c in a.knowledgeCitations:
        elements.append(Paragraph(f"• {c}", subtitle_style))

    doc.build(elements)

    if output_path:
        with open(output_path, "rb") as fp:
            return fp.read()
    return buffer.getvalue()
