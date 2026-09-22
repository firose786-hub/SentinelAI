"""
CEO & Business Impact Agent
Translates complex technical cybersecurity telemetry into:
1. Executive 'CEO Mode': Crystal-clear, non-technical English summaries for C-suite decision makers.
2. Business Impact Modeling: Estimated operational downtime, financial exposure ranges, and business unit risk.
"""

from typing import List, Dict, Any, Tuple
from ..models.compliance_schemas import (
    CEOSummary,
    BusinessImpact,
    OrganizationProfile,
    AISecurityFinding,
    ControlAssessment,
    SeverityLevel,
    AuditVerdict
)

class CEOAgent:
    def __init__(self):
        self.name = "Executive CEO & Business Impact Agent"
        self.role = "Executive Translator & Quantitative Financial Impact Modeler"

    def generate_executive_insights(
        self,
        org: OrganizationProfile,
        overall_compliance_score: int,
        ai_security_score: int,
        verdict: AuditVerdict,
        controls: List[ControlAssessment],
        ai_findings: List[AISecurityFinding]
    ) -> Tuple[CEOSummary, BusinessImpact]:
        """
        Generates simple English CEO summary and financial/downtime impact model.
        """
        vulns = [f for f in ai_findings if f.status in ["Vulnerable", "Partially Mitigated"]]
        critical_count = sum(1 for f in vulns if f.severity == "Critical")
        high_count = sum(1 for f in vulns if f.severity == "High")

        # 1. Plain English CEO Mode
        if verdict == "CRITICAL RISK":
            headline = f"Urgent Executive Action Required: High Risk of AI Security Failure for {org.name}"
            risk_summary = (
                "Your enterprise AI chatbot has critical security weaknesses that attackers can easily exploit. "
                "Adversaries could manipulate the AI to reveal private customer records, execute unauthorized database changes, "
                "or bypass safety filters. We recommend pausing high-risk automated actions until key defenses are installed."
            )
        elif verdict == "HIGH RISK":
            headline = f"Significant AI Security Vulnerabilities Detected in {org.name}"
            risk_summary = (
                "Your AI application has good foundational policies, but lacks critical real-time safety guardrails. "
                "Without automated prompt filters and data loss prevention, there is an elevated risk of sensitive data leaks "
                "and unexpected AI behavior."
            )
        elif verdict == "APPROVED WITH REMEDIATION":
            headline = f"Conditional Approval: Moderate Security Baseline with Fixable Gaps"
            risk_summary = (
                "Your company maintains solid security practices. We identified a few minor guardrail improvements "
                "that your engineering team should address over the next 30 days to ensure full compliance."
            )
        else: # APPROVED
            headline = f"Excellent Security Health: All AI Safeguards and Compliance Checks Passed"
            risk_summary = (
                "Your enterprise AI systems demonstrated robust defenses against all tested attack vectors. "
                "Access controls, data filtering, and governance standards meet high industry benchmarks."
            )

        # Top 3 Risks in simple English
        top_risks = []
        for f in vulns[:3]:
            if f.owasp_id == "LLM01":
                top_risks.append("Prompt Injection: Attackers can trick the AI into ignoring safety guidelines and behaving dangerously.")
            elif f.owasp_id == "LLM02":
                top_risks.append("Data Leakage: Sensitive company documents or credentials might accidentally be displayed in AI answers.")
            elif f.owasp_id == "LLM06":
                top_risks.append("Uncontrolled Actions: The AI can perform financial or database transactions without human approval.")
            else:
                top_risks.append(f"{f.title}: Identified security gap in AI application perimeter.")

        if not top_risks:
            top_risks = [
                "Zero critical vulnerabilities detected in active AI workflows.",
                "Maintain vigilance against emerging adversarial prompt techniques.",
                "Ensure continuous vendor monitoring for external AI APIs."
            ]

        # Top 3 Recommended Actions in simple English
        top_actions = [
            "Install automated prompt security filters before incoming user messages reach the AI model.",
            "Require human manager confirmation before the AI is allowed to execute high-impact transactions.",
            "Enable sensitive data masking so passwords, credit cards, and confidential records are never shown in responses."
        ]

        outlook = (
            "30 Days: Deploy immediate prompt filters and data masking to eliminate highest priority risks. "
            "60 Days: Connect security logs to your central operations dashboard. "
            "90 Days: Complete automated re-testing to achieve premier cybersecurity posture."
        )

        # 2. Business Impact Modeling (Downtime & Financial Exposure)
        # Revenue-scaled illustrative model
        revenue = org.annual_revenue_usd
        hourly_rev = revenue / (365 * 24)

        if critical_count >= 2 or verdict == "CRITICAL RISK":
            downtime_hours = 48.0
            impact_multiplier = 0.045  # ~4.5% annual revenue exposure
            risk_tier: SeverityLevel = "Critical"
            impact_areas = ["Customer Trust & Retention", "Regulatory & GDPR/FINRA Compliance Fines", "Core Payment Operations"]
        elif critical_count >= 1 or high_count >= 2 or verdict == "HIGH RISK":
            downtime_hours = 24.0
            impact_multiplier = 0.022
            risk_tier: SeverityLevel = "High"
            impact_areas = ["Brand Reputation", "Incident Response Containment Costs", "Developer Remediation Overhead"]
        elif high_count >= 1 or verdict == "APPROVED WITH REMEDIATION":
            downtime_hours = 6.0
            impact_multiplier = 0.008
            risk_tier: SeverityLevel = "Medium"
            impact_areas = ["Minor Service Latency", "Routine Security Engineering Hours"]
        else:
            downtime_hours = 0.5
            impact_multiplier = 0.001
            risk_tier: SeverityLevel = "Low"
            impact_areas = ["Standard Periodic Auditing Overhead"]

        financial_exposure = round(revenue * impact_multiplier, -3)
        low_range = round(financial_exposure * 0.7, -3)
        high_range = round(financial_exposure * 1.3, -3)
        range_display = f"${low_range:,.0f} – ${high_range:,.0f} USD"

        impact_narrative = (
            f"If an adversarial exploit breaches unmitigated AI interfaces, estimated business impact includes "
            f"up to {downtime_hours:.1f} hours of service interruption and estimated financial exposure of "
            f"{range_display} spanning regulatory fines, incident containment, and customer remediation."
        )

        business_impact = BusinessImpact(
            overall_risk_tier=risk_tier,
            estimated_downtime_hours=downtime_hours,
            estimated_financial_exposure_usd=financial_exposure,
            financial_range_display=range_display,
            primary_impact_areas=impact_areas,
            impact_narrative=impact_narrative,
            disclaimer="Illustrative research and risk modeling estimate for demonstration purposes only."
        )

        ceo_summary = CEOSummary(
            headline=headline,
            risk_summary_plain_english=risk_summary,
            compliance_score=overall_compliance_score,
            ai_security_score=ai_security_score,
            top_3_risks=top_risks[:3],
            business_impact_summary=f"Estimated Financial Exposure: {range_display} | Potential Outage: {downtime_hours:.1f} hrs",
            top_3_recommended_actions=top_actions[:3],
            outlook_30_60_90=outlook
        )

        return ceo_summary, business_impact
