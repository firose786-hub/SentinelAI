from backend.app.agents.pr_summary_agent import PrSummaryAgent, calculate_scores
from backend.app.models.schemas import SecurityFinding, QualityFinding


def test_calculate_scores_clean():
    metrics = calculate_scores([], [], "Low")
    assert metrics.securityScore == 100
    assert metrics.qualityScore == 100
    assert metrics.maintainabilityScore == 100
    assert metrics.overallHealth == 100


def test_calculate_scores_vulnerable():
    sec_finding = SecurityFinding(
        id="s1",
        title="SQL query built by string concatenation",
        detail="SQL Injection",
        severity="Critical",
        owaspCategory="A03:2021 — Injection",
        cwe="CWE-89",
        line=12,
    )
    qual_finding = QualityFinding(
        id="q1",
        title="Overly broad exception handling",
        detail="Broad except",
        severity="Medium",
        category="Error handling",
        line=20,
    )

    metrics = calculate_scores([sec_finding], [qual_finding], "Medium")
    assert metrics.securityScore == 74  # 100 - 26
    assert metrics.qualityScore == 93   # 100 - 7
    assert metrics.maintainabilityScore == 85  # 93 - 8
    assert metrics.overallHealth < 90


def test_pr_summary_verdict_blocking_critical():
    agent = PrSummaryAgent()
    sec_finding = SecurityFinding(
        id="s1",
        title="Command Injection",
        detail="os.system",
        severity="Critical",
        owaspCategory="A03:2021 — Injection",
        cwe="CWE-78",
        line=5,
    )

    summary, metrics = agent.summarize("test.py", "Python", [sec_finding], [], "Low")
    assert summary.verdict == "Block"
    assert summary.severityBreakdown["Critical"] == 1
    assert len(summary.prioritizedFixes) > 0
