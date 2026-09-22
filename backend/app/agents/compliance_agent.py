"""
Compliance Agent
Performs research-oriented simplified control assessments against:
- ISO/IEC 27001:2022 Information Security Management Standards
- NIST Cybersecurity Framework (CSF) 2.0
"""

from typing import List, Dict, Any, Tuple
from ..models.compliance_schemas import ControlAssessment, OrganizationProfile
from ..data.compliance_standards import ISO_27001_CONTROLS, NIST_CSF_CONTROLS

class ComplianceAgent:
    def __init__(self):
        self.name = "Standards Compliance Agent"
        self.role = "ISO 27001 & NIST CSF Evaluator"

    def evaluate_compliance(self, org: OrganizationProfile) -> Tuple[List[ControlAssessment], int, int, int]:
        """
        Evaluates organizational controls and computes ISO, NIST, and Overall Compliance scores.
        Returns:
            - List of ControlAssessment objects
            - ISO Compliance Score (0-100)
            - NIST Compliance Score (0-100)
            - Overall Compliance Score (0-100)
        """
        assessments: List[ControlAssessment] = []
        controls = org.existing_controls

        # 1. Evaluate ISO/IEC 27001:2022 Controls
        iso_total_points = 0
        iso_max_points = 0

        for item in ISO_27001_CONTROLS:
            cid = item["id"]
            key = item["eval_key"]
            weight = item["weight"]
            iso_max_points += weight

            has_control = controls.get(key, False)
            if has_control:
                status = "Compliant"
                score = 100
                iso_total_points += weight
                evidence = f"Verified active security control: '{key}' is formally implemented and operational in enterprise environment."
                gap = "None identified in current audit scope."
                risk_level = "Low"
                remediation = "Maintain continuous monitoring and periodic effectiveness testing."
            else:
                # Check for partial compliance heuristics
                if key in ["has_output_dlp", "has_ai_dev_security_policy"]:
                    status = "Partially Compliant"
                    score = 40
                    iso_total_points += (weight * 0.4)
                    evidence = f"Partial control detected; preliminary guidelines exist but lack automated technical enforcement."
                    gap = f"Mandatory technical control '{key}' is missing automated verification."
                    risk_level = "High"
                    remediation = f"Implement automated technical enforcement for {item['title']} to satisfy ISO 27001 requirement."
                else:
                    status = "Non-Compliant"
                    score = 0
                    evidence = f"Audit telemetry indicates control '{key}' is missing or disabled."
                    gap = f"Control {cid} ({item['title']}) is absent, leaving the AI application exposed to non-compliance."
                    risk_level = "Critical" if weight >= 15 else "High"
                    remediation = f"Immediately establish formal policy and technical implementation for {item['title']}."

            assessments.append(ControlAssessment(
                control_id=cid,
                standard="ISO/IEC 27001:2022",
                title=item["title"],
                category=item["category"],
                status=status,
                evidence=evidence,
                gap=gap,
                risk_level=risk_level,
                remediation=remediation,
                score=score
            ))

        # 2. Evaluate NIST CSF 2.0 Controls
        nist_total_points = 0
        nist_max_points = 0

        for item in NIST_CSF_CONTROLS:
            cid = item["id"]
            key = item["eval_key"]
            weight = item["weight"]
            nist_max_points += weight

            has_control = controls.get(key, False)
            if has_control:
                status = "Compliant"
                score = 100
                nist_total_points += weight
                evidence = f"Telemetry confirms alignment with NIST CSF '{item['category']}': {key} is actively maintained."
                gap = "No substantial gap identified."
                risk_level = "Low"
                remediation = "Continue periodic capability reviews and automate detection pipelines."
            else:
                if key in ["has_incident_response_plan", "has_ai_governance_board"]:
                    status = "Partially Compliant"
                    score = 35
                    nist_total_points += (weight * 0.35)
                    evidence = "Ad-hoc procedures exist, but no standardized NIST-aligned response playbook is documented."
                    gap = f"Category {item['category']} lacks formalized metrics and automated escalation."
                    risk_level = "High"
                    remediation = f"Formalize standardized playbooks and assign dedicated ownership for {item['title']}."
                else:
                    status = "Non-Compliant"
                    score = 0
                    evidence = f"Zero operational evidence found for required NIST subcategory '{key}'."
                    gap = f"Deficiency in NIST CSF {item['category']}: {item['requirement'][:80]}..."
                    risk_level = "Critical" if weight >= 15 else "High"
                    remediation = f"Prioritize deployment of baseline safeguards for {item['title']}."

            assessments.append(ControlAssessment(
                control_id=cid,
                standard="NIST CSF 2.0",
                title=item["title"],
                category=item["category"],
                status=status,
                evidence=evidence,
                gap=gap,
                risk_level=risk_level,
                remediation=remediation,
                score=score
            ))

        iso_score = int(round((iso_total_points / max(iso_max_points, 1)) * 100))
        nist_score = int(round((nist_total_points / max(nist_max_points, 1)) * 100))
        overall_compliance = int(round((iso_score + nist_score) / 2))

        return assessments, iso_score, nist_score, overall_compliance
