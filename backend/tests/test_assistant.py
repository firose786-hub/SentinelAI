from backend.app.agents.conversational_code_assistant import ConversationalCodeAssistant


def test_assistant_answers_with_citations():
    assistant = ConversationalCodeAssistant()
    res = assistant.answer("Why is MD5 unsafe for password hashing?")
    assert "answer" in res
    assert "citations" in res
    assert len(res["answer"]) > 20
    assert len(res["citations"]) > 0
    assert any("cryptographic" in c.lower() or "owasp" in c.lower() for c in res["citations"])


def test_assistant_with_analysis_context():
    assistant = ConversationalCodeAssistant()
    res = assistant.answer(
        question="How should I fix the SQL injection?",
        analysis_context="File banking_service.py has Critical SQL injection on line 30.",
    )
    assert len(res["answer"]) > 20
    assert len(res["citations"]) > 0


def test_assistant_with_api_key_graceful_fallback():
    assistant = ConversationalCodeAssistant()
    # Test with dummy key to verify graceful fallback without crashing
    res = assistant.answer(
        question="Explain CWE-798 embedded credentials",
        api_key="test_dummy_key_12345",
    )
    assert "answer" in res
    assert len(res["citations"]) > 0
    assert "engine" in res
