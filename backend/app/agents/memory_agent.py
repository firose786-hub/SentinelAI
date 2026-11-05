"""
Memory Agent (Audit History, Longitudinal Learning & Recurring Flaw Detector)
Maintains audit state memory across time, computes delta improvements (+/- points),
and tracks recurring vulnerability patterns across multiple audit iterations.
"""

from typing import List, Dict, Any, Optional
import time
from ..models.compliance_schemas import (
    MemoryComparison,
    RecurringFinding,
    AISecurityFinding,
    AuditRecord
)

class MemoryAgent:
    def __init__(self):
        self.name = "Audit Memory & Longitudinal Learning Agent"
        self.role = "Historical Audit Comparator & Recurrence Engine"

    def compare_with_history(
        self,
        current_org_id: str,
        current_overall_score: int,
        current_security_score: int,
        current_risk_score: int,
        current_findings: List[AISecurityFinding],
        past_audits: List[AuditRecord]
    ) -> MemoryComparison:
        """
        Compares current audit with historical audits for this organization in SQLite.
        """
        # Filter previous audits for this specific organization, excluding current
        org_history = [a for a in past_audits if a.organization_id == current_org_id]
        # Sort by timestamp descending
        org_history.sort(key=lambda x: x.timestamp, reverse=True)

        if not org_history:
            # First audit for this organization
            recurring_list: List[RecurringFinding] = []
            now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

            for f in current_findings:
                if f.status in ["Vulnerable", "Partially Mitigated"]:
                    recurring_list.append(RecurringFinding(
                        vulnerability_id=f.finding_id,
                        title=f.title,
                        owasp_id=f.owasp_id,
                        severity=f.severity,
                        first_seen=now_str,
                        last_seen=now_str,
                        occurrences_count=1,
                        trend="New",
                        status="Open"
                    ))

            return MemoryComparison(
                has_previous_audit=False,
                previous_audit_id=None,
                previous_audit_date=None,
                compliance_score_delta=0,
                ai_security_score_delta=0,
                risk_score_delta=0,
                total_findings_delta=0,
                summary_of_progress="Initial baseline compliance audit established. No prior historical audit records found for comparison.",
                recurring_findings=recurring_list
            )

        # We have previous audit(s)
        prev = org_history[0]
        compliance_delta = current_overall_score - prev.overall_compliance_score
        security_delta = current_security_score - prev.ai_security_score
        risk_delta = current_risk_score - prev.overall_risk_score

        current_vuln_count = sum(1 for f in current_findings if f.status in ["Vulnerable", "Partially Mitigated"])
        prev_vuln_count = sum(1 for f in prev.ai_security_findings if f.status in ["Vulnerable", "Partially Mitigated"])
        findings_delta = current_vuln_count - prev_vuln_count

        if compliance_delta > 0:
            progress_summary = (
                f"POSITIVE TRAJECTORY: Compliance improved by +{compliance_delta} points compared to prior audit ({prev.date_formatted}). "
                f"AI Security shifted by {'+' if security_delta >= 0 else ''}{security_delta} points. "
                f"Active vulnerability count reduced by {abs(findings_delta)}." if findings_delta < 0 else
                f"Active vulnerabilities: {current_vuln_count} (delta: {findings_delta:+d})."
            )
        elif compliance_delta < 0:
            progress_summary = (
                f"REGRESSION DETECTED: Compliance score dropped by {compliance_delta} points since prior audit ({prev.date_formatted}). "
                f"Risk score increased by {risk_delta:+d} points. Urgent review of newly introduced LLM features required."
            )
        else:
            progress_summary = (
                f"STABLE POSTURE: Compliance score unchanged at {current_overall_score}% since prior audit ({prev.date_formatted})."
            )

        # Track recurring vulnerabilities across all past audits for this org
        recurring_list = []
        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        for f in current_findings:
            if f.status in ["Vulnerable", "Partially Mitigated"]:
                # Count historical occurrences
                past_matches = []
                for past_a in org_history:
                    for past_f in past_a.ai_security_findings:
                        if past_f.owasp_id == f.owasp_id and past_f.status in ["Vulnerable", "Partially Mitigated"]:
                            past_matches.append(past_a)
                            break

                total_occurrences = len(past_matches) + 1
                first_seen_date = past_matches[-1].date_formatted if past_matches else now_str

                if total_occurrences > 1:
                    trend = "Persistent" if total_occurrences >= 2 else "Escalating"
                    status = "Open"
                else:
                    trend = "New"
                    status = "Open"

                recurring_list.append(RecurringFinding(
                    vulnerability_id=f.finding_id,
                    title=f.title,
                    owasp_id=f.owasp_id,
                    severity=f.severity,
                    first_seen=first_seen_date,
                    last_seen=now_str,
                    occurrences_count=total_occurrences,
                    trend=trend,
                    status=status
                ))

        return MemoryComparison(
            has_previous_audit=True,
            previous_audit_id=prev.audit_id,
            previous_audit_date=prev.date_formatted,
            compliance_score_delta=compliance_delta,
            ai_security_score_delta=security_delta,
            risk_score_delta=risk_delta,
            total_findings_delta=findings_delta,
            summary_of_progress=progress_summary,
            recurring_findings=recurring_list
        )

    def compare_with_previous(
        self,
        org_id: str,
        current_compliance_score: int,
        current_ai_security_score: int,
        current_risk_score: int,
        current_findings: List[AISecurityFinding] = None,
        past_audits: List[AuditRecord] = None
    ) -> MemoryComparison:
        """Alias for unit test compatibility."""
        return self.compare_with_history(
            current_org_id=org_id,
            current_overall_score=current_compliance_score,
            current_security_score=current_ai_security_score,
            current_risk_score=current_risk_score,
            current_findings=current_findings or [],
            past_audits=past_audits or []
        )
