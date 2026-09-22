"""
Decision Agent
Formalizes the final compliance determination, governance mandate, and security clearance status.
"""

from typing import Dict, Any
from ..models.compliance_schemas import AIDebateResult, AuditVerdict

class DecisionAgent:
    def __init__(self):
        self.name = "Decision & Governance Agent"
        self.role = "Executive Arbiter & Verdict Authorizer"

    def issue_decision(self, debate_result: AIDebateResult, overall_compliance: int, ai_security: int) -> Dict[str, Any]:
        verdict: AuditVerdict = debate_result.verdict

        if verdict == "APPROVED":
            clearance = "Full Production Clearance"
            mandate = "Authorized for enterprise deployment. Maintain quarterly continuous compliance re-assessment."
        elif verdict == "APPROVED WITH REMEDIATION":
            clearance = "Conditional Production Clearance"
            mandate = "Authorized with restricted user rollout. P1 roadmap remediation must be executed within 30 days."
        elif verdict == "HIGH RISK":
            clearance = "Restricted Sandbox Only"
            mandate = "Public and unvetted enterprise user access prohibited until all Critical & High security guardrail gaps are closed."
        else: # CRITICAL RISK
            clearance = "DEPLOYMENT BLOCKED"
            mandate = "Immediate suspension of active AI agent endpoints. Comprehensive architectural remediation mandated."

        return {
            "verdict": verdict,
            "clearance_status": clearance,
            "governance_mandate": mandate,
            "decision_confidence": debate_result.decision_confidence,
            "overall_compliance_score": overall_compliance,
            "ai_security_score": ai_security,
            "rationale": debate_result.verdict_rationale
        }
