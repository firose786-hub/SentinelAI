"""
Excel (.xlsx) Report Generator for SentinelAI Compliance Audits.
Generates multi-sheet styled workbooks containing Executive Summary, Controls, Findings, and Roadmap.
"""

import io
from typing import Dict, Any, List

def generate_excel_report(audit_data: Dict[str, Any]) -> bytes:
    """
    Generates a multi-sheet Excel spreadsheet (.xlsx) using openpyxl,
    or falls back to a formatted CSV buffer if openpyxl is unavailable.
    """
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter

        wb = openpyxl.Workbook()
        
        # 1. Sheet 1: Executive Summary
        ws1 = wb.active
        ws1.title = "Executive Summary"
        
        header_fill = PatternFill(start_color="A84B32", end_color="A84B32", fill_type="solid")
        header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
        title_font = Font(name="Arial", size=14, bold=True, color="A84B32")
        bold_font = Font(name="Arial", size=10, bold=True)
        normal_font = Font(name="Arial", size=10)
        
        ws1["A1"] = "SENTINELAI — ENTERPRISE COMPLIANCE & AI SECURITY AUDIT"
        ws1["A1"].font = title_font
        ws1["A2"] = f"Organization: {audit_data.get('organization_name')} | Audit ID: {audit_data.get('audit_id')} | Date: {audit_data.get('date_formatted')}"
        ws1["A2"].font = bold_font
        
        summary_headers = ["Metric Category", "Score / Value", "Benchmark / Status", "Notes"]
        ws1.append([])
        ws1.append(summary_headers)
        for col_idx, h in enumerate(summary_headers, 1):
            cell = ws1.cell(row=4, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font

        ws1.append(["Overall Compliance Score", f"{audit_data.get('overall_compliance_score', 0)}%", "Target: >= 80%", "Mean of ISO 27001 & NIST CSF 2.0"])
        ws1.append(["ISO/IEC 27001:2022 Score", f"{audit_data.get('iso_compliance_score', 0)}%", "8 Controls Evaluated", "Clause 5 & Clause 8 Controls"])
        ws1.append(["NIST CSF 2.0 Score", f"{audit_data.get('nist_compliance_score', 0)}%", "8 Core Categories", "Govern, Protect, Detect, Respond, Recover"])
        ws1.append(["AI Security Score (OWASP LLM)", f"{audit_data.get('ai_security_score', 0)}%", "OWASP Top 10 Vectors", "Red/Blue Team Validation Index"])
        ws1.append(["Cyber Risk Score", f"{audit_data.get('overall_risk_score', 0)}/100", (audit_data.get('business_impact') or {}).get('overall_risk_tier', 'Medium'), "Lower is better"])
        ws1.append(["Audit Council Verdict", audit_data.get('verdict', 'INSPECT'), "Binding Decision", (audit_data.get('debate_result') or {}).get('verdict_rationale', '')[:80]])

        # 2. Sheet 2: ISO & NIST Controls
        ws2 = wb.create_sheet(title="Compliance Controls")
        ctrl_headers = ["Standard", "Control ID", "Title", "Category", "Status", "Score", "Identified Gap", "Remediation Guidance"]
        ws2.append(ctrl_headers)
        for col_idx, h in enumerate(ctrl_headers, 1):
            cell = ws2.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            
        for c in audit_data.get("controls_assessment", []):
            ws2.append([
                c.get("standard"), c.get("control_id"), c.get("title"), c.get("category"),
                c.get("status"), f"{c.get('score')}/100", c.get("gap"), c.get("remediation")
            ])

        # 3. Sheet 3: AI Security Findings
        ws3 = wb.create_sheet(title="AI Security Findings")
        sec_headers = ["OWASP ID", "Vulnerability Title", "CWE", "Severity", "CVSS", "Status", "Judge Verdict", "Mitigation"]
        ws3.append(sec_headers)
        for col_idx, h in enumerate(sec_headers, 1):
            cell = ws3.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            
        for f in audit_data.get("ai_security_findings", []):
            ws3.append([
                f.get("owasp_id"), f.get("title"), f.get("cwe_id"), f.get("severity"),
                f.get("cvss_score"), f.get("status"), f.get("judge_verdict"), f.get("remediation_guidance")
            ])

        # 4. Sheet 4: Remediation Roadmap
        ws4 = wb.create_sheet(title="Remediation Roadmap")
        road_headers = ["Priority", "Finding Ref", "Action Item", "Responsible Team", "Target (Days)", "Point Gain", "Cost Level"]
        ws4.append(road_headers)
        for col_idx, h in enumerate(road_headers, 1):
            cell = ws4.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            
        for r in audit_data.get("roadmap", []):
            ws4.append([
                r.get("priority"), r.get("finding_ref"), r.get("action"), r.get("responsible_team"),
                f"{r.get('target_days')} Days", f"+{r.get('expected_point_gain')} pts", r.get("estimated_cost_level")
            ])

        # Auto-fit column widths
        for ws in [ws1, ws2, ws3, ws4]:
            for col in ws.columns:
                max_len = max(len(str(cell.value or "")) for cell in col)
                col_letter = get_column_letter(col[0].column)
                ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

        out_buf = io.BytesIO()
        wb.save(out_buf)
        return out_buf.getvalue()

    except Exception:
        # Fallback to UTF-8 CSV buffer
        import csv
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(["# Format: CSV / Excel Export"])
        writer.writerow(["Standard", "Control/Finding ID", "Title", "Category", "Status/Severity", "Score/CVSS", "Remediation"])
        for c in audit_data.get("controls_assessment", []):
            writer.writerow([c.get("standard"), c.get("control_id"), c.get("title"), c.get("category"), c.get("status"), c.get("score"), c.get("remediation")])
        for f in audit_data.get("ai_security_findings", []):
            writer.writerow(["OWASP LLM", f.get("owasp_id"), f.get("title"), f.get("cwe_id"), f.get("severity"), f.get("cvss_score"), f.get("remediation_guidance")])
        return out.getvalue().encode("utf-8")
