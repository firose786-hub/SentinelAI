"""
Policy Agent
Responsible for ingesting organizational security charters, AI system specifications,
and mapping them to formal cybersecurity frameworks (ISO/IEC 27001:2022 & NIST CSF 2.0).
"""

from typing import Dict, Any, List
from ..models.compliance_schemas import OrganizationProfile

class PolicyAgent:
    def __init__(self):
        self.name = "Policy & Governance Agent"
        self.role = "Security Policy Interpreter & Scope Mapper"

    def analyze_policies(self, org: OrganizationProfile) -> Dict[str, Any]:
        """
        Extracts policy directives, scope boundaries, and regulatory compliance targets.
        """
        controls = org.existing_controls
        policies = org.policy_documents

        policy_coverage_score = sum(1 for v in controls.values() if v) / max(len(controls), 1) * 100

        findings = []
        if not controls.get("has_ai_dev_security_policy", False):
            findings.append("Missing dedicated AI System Development & Secure Life Cycle policy.")
        if not controls.get("has_ai_governance_board", False):
            findings.append("Absence of an AI Ethics and Safety Governance Oversight Committee.")
        if not controls.get("has_llm_threat_model", False):
            findings.append("No documented LLM Threat Model addressing Prompt Injection and Jailbreaks.")
        if not controls.get("has_incident_response_plan", False):
            findings.append("Incident response playbooks lack specific procedures for AI agent compromise.")

        return {
            "agent": self.name,
            "organization_name": org.name,
            "industry": org.industry,
            "policy_coverage_percent": round(policy_coverage_score, 1),
            "governance_maturity": "High" if policy_coverage_score > 75 else ("Moderate" if policy_coverage_score > 45 else "Deficient"),
            "in_scope_standards": ["ISO/IEC 27001:2022", "NIST CSF 2.0", "OWASP Top 10 for LLM"],
            "policy_gaps": findings,
            "llm_system_tier": "Critical Enterprise Asset" if org.annual_revenue_usd > 200000000 else "Standard Business Application"
        }
