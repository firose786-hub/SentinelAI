"""
Risk Agent
Quantifies enterprise security exposure, risk velocity, and aggregate vulnerability score
by synthesizing compliance gaps and AI threat vectors.
"""

from typing import List, Dict, Any
from ..models.compliance_schemas import ControlAssessment, AISecurityFinding, SeverityLevel

class RiskAgent:
    def __init__(self):
        self.name = "Cyber Risk Assessment Agent"
        self.role = "Quantitative Risk & Threat Modeler"

    def assess_risk(
        self,
        compliance_score: int,
        controls: List[ControlAssessment],
        ai_findings: List[AISecurityFinding]
    ) -> Dict[str, Any]:
        """
        Calculates aggregate risk score, severity distributions, and primary risk drivers.
        """
        # Count control gap severities
        critical_controls = sum(1 for c in controls if c.status == "Non-Compliant" and c.risk_level == "Critical")
        high_controls = sum(1 for c in controls if c.status in ["Non-Compliant", "Partially Compliant"] and c.risk_level == "High")

        # Count AI security findings
        vulnerable_findings = [f for f in ai_findings if f.status in ["Vulnerable", "Partially Mitigated"]]
        critical_vulns = sum(1 for f in vulnerable_findings if f.severity == "Critical")
        high_vulns = sum(1 for f in vulnerable_findings if f.severity == "High")
        medium_vulns = sum(1 for f in vulnerable_findings if f.severity == "Medium")

        # Risk score calculation: 100 - compliance + vulnerability penalty
        base_risk = 100 - compliance_score
        vuln_penalty = (critical_vulns * 15) + (high_vulns * 8) + (medium_vulns * 3)
        overall_risk_score = min(100, max(5, int(round((base_risk * 0.5) + (vuln_penalty * 0.5)))))

        if overall_risk_score >= 70 or critical_vulns >= 2:
            risk_tier: SeverityLevel = "Critical"
        elif overall_risk_score >= 45 or high_vulns >= 2:
            risk_tier: SeverityLevel = "High"
        elif overall_risk_score >= 20:
            risk_tier: SeverityLevel = "Medium"
        else:
            risk_tier: SeverityLevel = "Low"

        risk_drivers = []
        if critical_vulns > 0:
            risk_drivers.append(f"{critical_vulns} Critical AI Security vulnerabilities detected in active LLM interfaces.")
        if critical_controls > 0:
            risk_drivers.append(f"{critical_controls} Critical ISO/NIST controls have zero technical enforcement.")
        if not risk_drivers:
            risk_drivers.append("Standard operational baseline; minor control hygiene enhancements recommended.")

        return {
            "overall_risk_score": overall_risk_score,
            "risk_tier": risk_tier,
            "critical_vulnerabilities": critical_vulns,
            "high_vulnerabilities": high_vulns,
            "medium_vulnerabilities": medium_vulns,
            "risk_drivers": risk_drivers,
            "threat_likelihood": "High" if critical_vulns > 0 else ("Moderate" if high_vulns > 0 else "Low"),
            "threat_impact": "Severe" if risk_tier in ["Critical", "High"] else "Manageable"
        }

    def calculate_overall_risk(
        self,
        compliance_score: int,
        ai_security_score: int,
        vulnerable_findings_count: int,
        critical_count: int
    ):
        """Helper for unit test risk calculation."""
        base_risk = 100 - int(round((compliance_score + ai_security_score) / 2))
        vuln_penalty = (critical_count * 15) + (vulnerable_findings_count * 4)
        overall_risk_score = min(100, max(5, int(round((base_risk * 0.5) + (vuln_penalty * 0.5)))))

        if overall_risk_score >= 70 or critical_count >= 2:
            tier = "Critical"
        elif overall_risk_score >= 45 or critical_count >= 1:
            tier = "High"
        elif overall_risk_score >= 20:
            tier = "Medium"
        else:
            tier = "Low"

        narrative = f"Overall Risk evaluated at {overall_risk_score}/100 ({tier} tier) with {critical_count} critical findings."
        return overall_risk_score, tier, narrative
