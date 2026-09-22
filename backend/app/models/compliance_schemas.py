from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

SeverityLevel = Literal["Critical", "High", "Medium", "Low", "Informational"]
ComplianceStatus = Literal["Compliant", "Partially Compliant", "Non-Compliant", "Not Applicable"]
AuditVerdict = Literal["APPROVED", "APPROVED WITH REMEDIATION", "HIGH RISK", "CRITICAL RISK"]
PriorityLevel = Literal["P1", "P2", "P3"]

class ControlAssessment(BaseModel):
    control_id: str
    standard: Literal["ISO/IEC 27001:2022", "NIST CSF 2.0"]
    title: str
    category: str
    status: ComplianceStatus
    evidence: str
    gap: str
    risk_level: SeverityLevel
    remediation: str
    score: int  # 0 to 100

class AISecurityFinding(BaseModel):
    finding_id: str
    owasp_id: str  # e.g., LLM01, LLM02
    title: str
    attack_vector: str
    simulated_payload: str
    red_team_observation: str
    blue_team_defense: str
    judge_verdict: str
    severity: SeverityLevel
    cvss_score: float
    cwe_id: str
    remediation_guidance: str
    status: Literal["Vulnerable", "Partially Mitigated", "Protected"]

class DebateTurn(BaseModel):
    speaker: Literal["Red Team (Skeptic)", "Blue Team (Advocate)", "Judge (Moderator)"]
    agent_name: str
    argument: str
    key_points: List[str] = Field(default_factory=list)
    confidence: float

class AIDebateResult(BaseModel):
    debate_topic: str
    rounds: List[DebateTurn] = Field(default_factory=list)
    skeptic_summary: str
    advocate_summary: str
    judge_ruling: str
    verdict: AuditVerdict
    verdict_rationale: str
    decision_confidence: float

class ForecastMilestone(BaseModel):
    days: int  # 30, 60, 90
    predicted_score: int
    confidence_percentage: int
    projected_improvements: List[str]
    residual_risks: List[str]

class ComplianceForecast(BaseModel):
    current_score: int
    milestones: List[ForecastMilestone] = Field(default_factory=list)
    trajectory_analysis: str
    disclaimer: str = "Research/demo forecast model based on remediation prioritization, not a certified statistical certainty."

class RoadmapItem(BaseModel):
    id: str
    priority: PriorityLevel
    finding_ref: str
    title: str
    action: str
    responsible_team: str
    target_days: int
    expected_point_gain: int
    estimated_cost_level: Literal["Low", "Medium", "High"]
    completed: bool = False

class RecurringFinding(BaseModel):
    vulnerability_id: str
    title: str
    owasp_id: str
    severity: SeverityLevel
    first_seen: str
    last_seen: str
    occurrences_count: int
    trend: Literal["Persistent", "Escalating", "Improving", "New"]
    status: Literal["Open", "In Remediation", "Resolved"]

class MemoryComparison(BaseModel):
    has_previous_audit: bool
    previous_audit_id: Optional[str] = None
    previous_audit_date: Optional[str] = None
    compliance_score_delta: int = 0
    ai_security_score_delta: int = 0
    risk_score_delta: int = 0
    total_findings_delta: int = 0
    summary_of_progress: str
    recurring_findings: List[RecurringFinding] = Field(default_factory=list)

class SPEPDefenseMetrics(BaseModel):
    cloud_platform: str = "Multi-Cloud Hybrid (AWS/GCP/Azure)"
    baseline_asr_pct: float = 80.0
    spep_hardened_asr_pct: float = 7.0
    asr_reduction_pct: float = 91.25
    trust_deviation_metric: float = 0.04
    average_cosine_trigger_score: float = 0.88
    latency_overhead_ms: float = 42.0
    dual_channel_schema_enforced: bool = True
    output_confinement_pass_rate: float = 100.0
    execution_confirmation_active: bool = True
    active_patterns: List[str] = Field(default_factory=lambda: [
        "SPEP-01: Contextual Sanitization Filter (ISF)",
        "SPEP-02: Instruction-Data Dual-Channel Separation (RCS)",
        "SPEP-03: Multi-Agent Quorum Consensus (MAC)",
        "SPEP-04: Cloud API Output Confinement (CAR)",
        "SPEP-05: Execution Confirmation & Step-Up Gate (ECF)"
    ])

class BusinessImpact(BaseModel):
    overall_risk_tier: SeverityLevel
    estimated_downtime_hours: float
    estimated_financial_exposure_usd: float
    financial_range_display: str
    primary_impact_areas: List[str]
    impact_narrative: str
    disclaimer: str = "Illustrative research and risk modeling estimate for demonstration purposes only."

class CEOSummary(BaseModel):
    headline: str
    risk_summary_plain_english: str
    compliance_score: int
    ai_security_score: int
    top_3_risks: List[str]
    business_impact_summary: str
    top_3_recommended_actions: List[str]
    outlook_30_60_90: str

class OrganizationProfile(BaseModel):
    id: str
    name: str
    industry: str
    size: str
    annual_revenue_usd: float
    description: str
    llm_system_description: str
    llm_capabilities: List[str] = Field(default_factory=list)
    existing_controls: Dict[str, Any] = Field(default_factory=dict)
    policy_documents: Dict[str, str] = Field(default_factory=dict)
    cloud_provider: str = "AWS / Azure / GCP Hybrid"

class AuditRecord(BaseModel):
    audit_id: str
    organization_id: str
    organization_name: str
    industry: str
    timestamp: int
    date_formatted: str
    iso_compliance_score: int
    nist_compliance_score: int
    overall_compliance_score: int
    ai_security_score: int
    overall_risk_score: int
    verdict: AuditVerdict
    controls_assessment: List[ControlAssessment] = Field(default_factory=list)
    ai_security_findings: List[AISecurityFinding] = Field(default_factory=list)
    debate_result: AIDebateResult
    forecast: ComplianceForecast
    roadmap: List[RoadmapItem] = Field(default_factory=list)
    memory_comparison: MemoryComparison
    spep_metrics: SPEPDefenseMetrics = Field(default_factory=SPEPDefenseMetrics)
    business_impact: BusinessImpact
    ceo_summary: CEOSummary
    llm_reasoning_used: bool = False
    agent_execution_times: Dict[str, float] = Field(default_factory=dict)
