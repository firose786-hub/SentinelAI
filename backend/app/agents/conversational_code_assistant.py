import os
import re
from typing import List, Dict, Any, Optional
from ..rag.rag_engine import retrieve, format_context, citations_of
from ..config import GEMINI_API_KEY, GEMINI_MODEL


class ConversationalCodeAssistant:
    """Milestone 3 — Conversational Code Assistant (RAG & Real-Time Gemini)."""

    def __init__(self):
        self.name = "Conversational Code Assistant"

    def _answer_with_gemini(
        self,
        question: str,
        history: List[Dict[str, str]],
        context: str,
        analysis_context: Optional[str] = None,
        runtime_api_key: Optional[str] = None,
    ) -> Optional[str]:
        effective_key = runtime_api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        if not effective_key or not effective_key.strip():
            return None

        key = effective_key.strip()
        system_instruction = (
            "You are the Sentinel Conversational Code Assistant for the Smart Code Inspection Platform (Group 2 Infosys Project).\n"
            "You provide real-time expert guidance on software security, vulnerability fixes, code quality, software architecture, and general programming.\n"
            "Whenever relevant, ground your answer using the retrieved knowledge base context and the current analysis session.\n"
            "Provide clear, concise explanations with syntax-highlighted code snippets where helpful."
        )

        history_lines = []
        for m in history[-8:]:
            role = "Developer" if m.get("role") == "user" else "Assistant"
            history_lines.append(f"{role}: {m.get('content', '')}")

        prompt = (
            f"{system_instruction}\n\n"
            f"Retrieved Secure Coding Knowledge Base:\n{context}\n\n"
            f"Current Analysis Context:\n{analysis_context or 'No specific analysis context active.'}\n\n"
            f"Conversation History:\n" + "\n".join(history_lines) + f"\n\nDeveloper: {question}\nAssistant:"
        )

        # 1. Try modern google-genai SDK
        for model_candidate in [GEMINI_MODEL, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
            if not model_candidate:
                continue
            try:
                from google import genai
                client = genai.Client(api_key=key)
                response = client.models.generate_content(
                    model=model_candidate,
                    contents=prompt,
                )
                if response and response.text:
                    return response.text.strip()
            except Exception:
                continue

        # 2. Fallback to google.generativeai if available
        try:
            import google.generativeai as ggenai
            ggenai.configure(api_key=key)
            for model_name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
                try:
                    model = ggenai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    if response and response.text:
                        return response.text.strip()
                except Exception:
                    continue
        except Exception:
            pass

        return None

    def _synthesize_local_response(
        self,
        question: str,
        retrieved_results: List[Dict[str, Any]],
        analysis_context: Optional[str] = None,
    ) -> str:
        q_lower = question.lower()

        # Dynamic query understanding
        intro = ""
        if "why" in q_lower:
            intro = "Understanding the underlying risk and mechanics is essential for writing resilient software."
        elif "how" in q_lower or "fix" in q_lower:
            intro = "Here is the recommended implementation pattern and remediation strategy."
        elif "explain" in q_lower or "what is" in q_lower:
            intro = "Here is a technical overview based on established secure coding standards."
        else:
            intro = "Based on our indexed secure coding guidelines:"

        if not retrieved_results:
            return (
                f"{intro}\n\n"
                "**General Best Practice:**\n"
                "- Always separate code execution from untrusted data (use parameterised queries, safe parsers, and explicit types).\n"
                "- Never embed credentials or private keys in source code; load them from environment variables.\n"
                "- Handle exceptions specifically and ensure all acquired resources are cleanly closed.\n\n"
                "*(Tip: Set your Gemini API key in the top right to enable real-time generative responses for any arbitrary question.)*"
            )

        blocks = [f"{intro}\n"]
        for idx, res in enumerate(retrieved_results[:2], 1):
            c = res["chunk"]
            blocks.append(f"**[{idx}] {c['title']}** ({c['source']}):\n{c['text']}\n")

        if analysis_context:
            blocks.append(f"**Current Session Analysis:**\n{analysis_context}\n")

        return "\n".join(blocks)

    def answer(
        self,
        question: str,
        history: Optional[List[Dict[str, str]]] = None,
        analysis_context: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        history = history or []
        retrieved = retrieve(question, k=5)
        context = format_context(retrieved)
        citations = citations_of(retrieved)

        # 1. Try real-time Gemini call
        gemini_answer = self._answer_with_gemini(
            question=question,
            history=history,
            context=context,
            analysis_context=analysis_context,
            runtime_api_key=api_key,
        )
        if gemini_answer:
            return {
                "answer": gemini_answer,
                "citations": citations,
                "engine": "Gemini Real-Time AI",
            }

        # 2. Dynamic local RAG synthesis
        answer = self._synthesize_local_response(question, retrieved, analysis_context)
        return {
            "answer": answer,
            "citations": citations,
            "engine": "RAG Knowledge Base",
        }
