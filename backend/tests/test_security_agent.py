from backend.app.agents.security_vulnerability_agent import (
    SecurityVulnerabilityAgent,
    scan_python_security,
    scan_java_security,
)
from backend.app.samples.sample_data import SAMPLES

banking_sample = next(s for s in SAMPLES if s["id"] == "python-banking")
java_sample = next(s for s in SAMPLES if s["id"] == "java-login")
clean_sample = next(s for s in SAMPLES if s["id"] == "python-clean")


def test_detect_sqli_python():
    findings = scan_python_security(banking_sample["code"])
    assert any(f.cwe == "CWE-89" for f in findings)
    assert any("SQL query built by string concatenation" in f.title for f in findings)


def test_detect_embedded_credentials_python():
    findings = scan_python_security(banking_sample["code"])
    assert any(f.cwe == "CWE-798" for f in findings)


def test_detect_weak_hash_md5_python():
    findings = scan_python_security(banking_sample["code"])
    assert any(f.cwe == "CWE-327" for f in findings)


def test_detect_command_injection_shell_python():
    findings = scan_python_security(banking_sample["code"])
    assert any(f.cwe == "CWE-78" for f in findings)


def test_detect_dynamic_eval_python():
    findings = scan_python_security(banking_sample["code"])
    assert any(f.cwe == "CWE-95" for f in findings)


def test_detect_sqli_and_weak_hash_java():
    findings = scan_java_security(java_sample["code"])
    assert any(f.cwe == "CWE-89" for f in findings)
    assert any(f.cwe == "CWE-327" for f in findings)
    assert any(f.cwe == "CWE-798" for f in findings)


def test_clean_sample_produces_no_security_vulnerabilities():
    findings = scan_python_security(clean_sample["code"])
    assert len(findings) == 0


def test_security_findings_have_proper_metadata():
    agent = SecurityVulnerabilityAgent()
    findings = agent.scan(banking_sample["code"], "Python")
    assert len(findings) > 0
    for f in findings:
        assert f.severity in ("Critical", "High", "Medium", "Low")
        assert f.owaspCategory.startswith("A")
        assert f.cwe.startswith("CWE-")
        assert f.agent == "Security Vulnerability Agent"
        assert f.line is None or f.line >= 1
