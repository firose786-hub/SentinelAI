from backend.app.agents.remediation_agent import RemediationAgent
from backend.app.models.schemas import SecurityFinding


def test_remediation_generation_for_sqli():
    agent = RemediationAgent()
    finding = SecurityFinding(
        id="s1",
        title="SQL query built by string concatenation",
        detail="User data concatenated into query",
        severity="Critical",
        owaspCategory="A03:2021 — Injection",
        cwe="CWE-89",
        line=10,
        evidence="cursor.execute('SELECT ... ' + u)",
    )

    remediations = agent.remediate([finding], "SELECT ...", "Python")
    assert len(remediations) == 1
    rem = remediations[0]
    assert rem.findingId == "s1"
    assert "parameter" in rem.recommendation.lower()
    assert "?" in rem.correctedCode or "%s" in rem.correctedCode
    assert len(rem.bestPractice) > 0


def test_remediation_empty_findings():
    agent = RemediationAgent()
    remediations = agent.remediate([], "print(1)", "Python")
    assert len(remediations) == 0
