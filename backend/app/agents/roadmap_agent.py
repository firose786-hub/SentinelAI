"""
Remediation Roadmap Agent
Generates an actionable, step-by-step P1/P2/P3 prioritized engineering and governance plan
with assigned teams, timelines, and quantitative point gain projections.
"""

from typing import List, Dict, Any
from ..models.compliance_schemas import (
    RoadmapItem,
    ControlAssessment,
    AISecurityFinding,
    PriorityLevel
)

class RoadmapAgent:
    def __init__(self):
        self.name = "Remediation Roadmap Agent"
        self.role = "Actionable Mitigation & Engineering Planner"

    def build_roadmap(
        self,
        controls: List[ControlAssessment],
        ai_findings: List[AISecurityFinding]
    ) -> List[RoadmapItem]:
        """
        Synthesizes control gaps and security findings into a prioritized roadmap.
        """
        items: List[RoadmapItem] = []
        item_counter = 1

        # 1. Process AI Security Vulnerabilities
        for f in ai_findings:
            if f.status in ["Vulnerable", "Partially Mitigated"]:
                if f.severity == "Critical":
                    priority: PriorityLevel = "P1"
                    days = 7
                    gain = 12
                    cost = "Medium"
                    team = "AI Security & Platform Engineering"
                elif f.severity == "High":
                    priority: PriorityLevel = "P1" if f.owasp_id in ["LLM01", "LLM02"] else "P2"
                    days = 14 if priority == "P1" else 30
                    gain = 8
                    cost = "Medium"
                    team = "AI Engineering / DevSecOps"
                else:
                    priority: PriorityLevel = "P3"
                    days = 60
                    gain = 4
                    cost = "Low"
                    team = "Data Science & MLOps Team"

                items.append(RoadmapItem(
                    id=f"ACT-AI-{item_counter:02d}",
                    priority=priority,
                    finding_ref=f.owasp_id,
                    title=f"Remediate {f.owasp_id}: {f.title}",
                    action=f.remediation_guidance,
                    responsible_team=team,
                    target_days=days,
                    expected_point_gain=gain,
                    estimated_cost_level=cost,
                    completed=False
                ))
                item_counter += 1

        # 2. Process ISO / NIST Control Gaps
        for c in controls:
            if c.status == "Non-Compliant":
                if c.risk_level == "Critical":
                    priority = "P1"
                    days = 14
                    gain = 10
                    team = "Information Security / SecOps"
                elif c.risk_level == "High":
                    priority = "P2"
                    days = 30
                    gain = 6
                    team = "Compliance & Security Governance"
                else:
                    priority = "P3"
                    days = 60
                    gain = 3
                    team = "IT Operations / Infrastructure"

                items.append(RoadmapItem(
                    id=f"ACT-CTRL-{item_counter:02d}",
                    priority=priority,
                    finding_ref=c.control_id,
                    title=f"Enforce {c.control_id}: {c.title}",
                    action=c.remediation,
                    responsible_team=team,
                    target_days=days,
                    expected_point_gain=gain,
                    estimated_cost_level="Medium" if priority in ["P1", "P2"] else "Low",
                    completed=False
                ))
                item_counter += 1

        # Sort items: P1 first, then P2, then P3, then by target_days
        priority_order = {"P1": 1, "P2": 2, "P3": 3}
        items.sort(key=lambda x: (priority_order.get(x.priority, 4), x.target_days))

        return items

    def generate_roadmap(self, controls: List[ControlAssessment], ai_findings: List[AISecurityFinding]) -> List[RoadmapItem]:
        """Alias for build_roadmap for compatibility."""
        return self.build_roadmap(controls, ai_findings)
