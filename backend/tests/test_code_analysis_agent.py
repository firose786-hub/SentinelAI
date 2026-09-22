from backend.app.agents.code_analysis_agent import (
    CodeAnalysisAgent,
    analyze_python_quality,
    analyze_java_quality,
    estimate_complexity,
)


def test_flag_broad_exception_python():
    code = "try:\n    perform()\nexcept Exception:\n    pass\n"
    findings = analyze_python_quality(code)
    assert any(f.category == "Error handling" for f in findings)
    assert any("broad" in f.title.lower() for f in findings)


def test_flag_empty_catch_python():
    code = "try:\n    perform()\nexcept ValueError:\n    pass\n"
    findings = analyze_python_quality(code)
    assert any("swallowed" in f.title.lower() for f in findings)


def test_flag_todo_in_comments():
    code = "# TODO: finalize security implementation\ndef run():\n    pass\n"
    findings = analyze_python_quality(code)
    assert any("TODO" in f.title for f in findings)
    assert any(f.line == 1 for f in findings)


def test_flag_wildcard_import_python():
    code = "from typing import *\ndef f(): pass\n"
    findings = analyze_python_quality(code)
    assert any("Wildcard import" in f.title for f in findings)


def test_estimate_complexity():
    simple_code = "def f(x):\n    return x + 1\n"
    res_simple = estimate_complexity(simple_code, "Python")
    assert res_simple["label"] == "Low"

    complex_code = """
def process(x):
    if x == 1: return 1
    elif x == 2: return 2
    elif x == 3: return 3
    elif x == 4: return 4
    elif x == 5: return 5
    elif x == 6: return 6
    elif x == 7: return 7
    elif x == 8: return 8
    elif x == 9: return 9
    elif x == 10: return 10
    elif x == 11: return 11
    elif x == 12: return 12
    elif x == 13: return 13
    return 0
"""
    res_complex = estimate_complexity(complex_code, "Python")
    assert res_complex["label"] == "High"


def test_code_analysis_agent_clean_code():
    agent = CodeAnalysisAgent()
    clean_code = "def add(a: int, b: int) -> int:\n    return a + b\n"
    findings, complexity = agent.analyze(clean_code, "Python")
    assert len(findings) == 0
    assert complexity["label"] == "Low"
