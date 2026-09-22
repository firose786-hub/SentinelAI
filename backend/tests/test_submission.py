from backend.app.services.submission_service import detect_language, validate_submission
from backend.app.samples.sample_data import SAMPLES


def test_detect_language_by_extension():
    assert detect_language("print('hello')", "test.py") == "Python"
    assert detect_language("class A {}", "Test.java") == "Java"
    assert detect_language("console.log('hi')", "index.js") == "JavaScript"
    assert detect_language("interface User {}", "types.ts") == "TypeScript"
    assert detect_language("#include <stdio.h>", "main.c") == "C"
    assert detect_language("#include <iostream>\nnamespace app {}", "main.cpp") == "C++"


def test_detect_language_by_content():
    assert detect_language("def calculate_total(self, items):\n    return sum(items)\n") == "Python"
    assert detect_language("public class Main { public static void main(String[] args) {} }") == "Java"
    assert detect_language("Just plain text with no discernible code markers") == "Unknown"


def test_auto_detect_bundled_samples():
    for sample in SAMPLES:
        detected = detect_language(sample["code"], sample["filename"])
        assert detected == sample["language"], f"Failed detection on {sample['id']}"


def test_validate_submission_empty():
    result = validate_submission("", "empty.py", "Python")
    assert not result.syntaxValid
    assert any("empty" in e.lower() for e in result.syntaxErrors)


def test_validate_submission_syntax_error_python():
    bad_code = "def f(x:\n    return x"
    result = validate_submission(bad_code, "bad.py", "Python")
    assert not result.syntaxValid
    assert len(result.syntaxErrors) > 0


def test_validate_submission_valid_python():
    good_code = "def add(a: int, b: int) -> int:\n    return a + b\n"
    result = validate_submission(good_code, "good.py", "Python")
    assert result.syntaxValid
    assert len(result.syntaxErrors) == 0
    assert result.lineCount == 3


def test_validate_submission_syntax_error_java():
    bad_java = "int x = 5;"
    result = validate_submission(bad_java, "Bad.java", "Java")
    assert not result.syntaxValid
    assert any("declaration" in e.lower() for e in result.syntaxErrors)


def test_validate_submission_valid_java():
    good_java = """package com.example;
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}"""
    result = validate_submission(good_java, "Hello.java", "Java")
    assert result.syntaxValid
    assert len(result.syntaxErrors) == 0


def test_validate_all_bundled_samples():
    for sample in SAMPLES:
        res = validate_submission(sample["code"], sample["filename"], sample["language"])
        assert res.syntaxValid, f"Sample {sample['id']} failed syntax validation: {res.syntaxErrors}"
