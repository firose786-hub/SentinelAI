from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field

Severity = Literal["Critical", "High", "Medium", "Low"]
Verdict = Literal["Approve", "Approve with suggestions", "Request changes", "Block"]
SupportedLanguage = Literal["Python", "Java", "JavaScript", "TypeScript", "C", "C++", "Unknown"]


class SubmissionResult(BaseModel):
    id: str
    filename: str
    language: str
    languageAutoDetected: bool = True
    lineCount: int
    charCount: int
    syntaxValid: bool
    syntaxErrors: List[str] = Field(default_factory=list)


class QualityFinding(BaseModel):
    id: str
    title: str
    detail: str
    severity: Severity
    category: str
    line: Optional[int] = None
    agent: str = "Code Analysis Agent"


class SecurityFinding(BaseModel):
    id: str
    title: str
    detail: str
    severity: Severity
    owaspCategory: str
    cwe: str
    line: Optional[int] = None
    evidence: str = ""
    agent: str = "Security Vulnerability Agent"


class Remediation(BaseModel):
    findingId: str
    title: str
    recommendation: str
    bestPractice: str
    correctedCode: str


class PrSummary(BaseModel):
    executiveOverview: str
    verdict: Verdict
    prioritizedFixes: List[str] = Field(default_factory=list)
    severityBreakdown: Dict[str, int] = Field(default_factory=dict)


class HealthMetrics(BaseModel):
    securityScore: int
    qualityScore: int
    maintainabilityScore: int
    overallHealth: int
    complexity: Literal["Low", "Medium", "High"]


class AgentTiming(BaseModel):
    agent: str
    ms: int


class AnalysisRecord(BaseModel):
    id: str
    createdAt: int
    submission: SubmissionResult
    code: str
    qualityFindings: List[QualityFinding] = Field(default_factory=list)
    securityFindings: List[SecurityFinding] = Field(default_factory=list)
    remediations: List[Remediation] = Field(default_factory=list)
    summary: PrSummary
    metrics: HealthMetrics
    knowledgeCitations: List[str] = Field(default_factory=list)
    agentTimings: List[AgentTiming] = Field(default_factory=list)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    citations: Optional[List[str]] = None
    ts: Optional[int] = None


class ValidateRequest(BaseModel):
    code: str
    filename: Optional[str] = "snippet.py"
    language: Optional[str] = "Auto-detect"


class AnalyzeRequest(BaseModel):
    code: str
    filename: Optional[str] = "snippet.py"
    language: Optional[str] = "Auto-detect"
    apiKey: Optional[str] = None


class ChatRequest(BaseModel):
    question: str
    history: List[Dict[str, str]] = Field(default_factory=list)
    analysisContext: Optional[str] = None
    apiKey: Optional[str] = None
