"""
Blue Team Agent (Defensive AI Security & Guardrail Engineering)
Evaluates existing defensive perimeters, compensating security controls,
and formulates the defensive posture for multi-agent debate reasoning.
"""

from typing import List, Dict, Any
from ..models.compliance_schemas import OrganizationProfile

class BlueTeamAgent:
    def __init__(self):
        self.name = "Defensive Blue Team Agent"
        self.role = "AI Defense Architect & Guardrail Evaluator"

    def evaluate_defenses(self, org: OrganizationProfile, red_findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Synthesizes defensive evidence and compensating controls for each Red Team finding.
        """
        controls = org.existing_controls
        defensive_findings = []

        for rf in red_findings:
            owasp_id = rf["owasp_id"]
            status = rf["status"]

            if status == "Protected":
                defense_argument = (
                    f"CONFIRMED DEFENSE: Perimeter guardrails and baseline controls for {owasp_id} are actively enforcing policy. "
                    "All anomalous inputs are intercepted before touching core model weights."
                )
            elif status == "Partially Mitigated":
                defense_argument = (
                    f"COMPENSATING CONTROL ACTIVE: While direct detection is imperfect, secondary auditing ({controls.get('has_audit_logging_and_monitoring', False)}) "
                    "captures event anomalies for retrospective SOC alert generation."
                )
            else: # Vulnerable
                if controls.get("has_security_policy", False):
                    defense_argument = (
                        f"DEFICIENT TECHNICAL DEFENSE: Organizational policy exists, but lack of automated technical guardrails "
                        f"leaves {owasp_id} exposed. Immediate deployment of secondary input/output filtering required."
                    )
                else:
                    defense_argument = (
                        f"CRITICAL DEFENSE VOID: Neither governance policy nor technical guardrails exist to counter {owasp_id}."
                    )

            finding_copy = dict(rf)
            finding_copy["blue_team_defense"] = defense_argument
            defensive_findings.append(finding_copy)

        return defensive_findings
