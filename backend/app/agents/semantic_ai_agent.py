import os
import re
import json
from typing import List, Tuple, Optional, Dict, Any
from ..models.schemas import SecurityFinding, QualityFinding, Severity
from ..config import GEMINI_API_KEY, GEMINI_MODEL


class SemanticAIAgent:
    """Milestone 2 & 3 — Real-Time Semantic AI Code Inspector."""

    def __init__(self, api_key: Optional[str] = None):
        self.name = "Semantic AI Inspector"
        self.api_key = api_key if api_key is not None else (GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", ""))
        self.is_configured = bool(self.api_key and self.api_key.strip())

    def evaluate_adversarial_prompt(self, prompt: str, context: str = "") -> Dict[str, Any]:
        """Evaluates adversarial prompt injection with deterministic fallback."""
        low_p = prompt.lower()
        adversarial_indicators = [
            "system override", "ignore all", "bypass", "reveal database",
            "dan mode", "unrestricted", "admin persona", "dump credentials"
        ]
        is_adv = any(ind in low_p for ind in adversarial_indicators)
        return {
            "mode": "deterministic_offline_rule_engine",
            "is_adversarial": is_adv,
            "confidence": 0.95 if is_adv else 0.85,
            "remediation": "Deploy SPEP-01 contextual sanitization filter and dual-channel prompt firewall.",
            "context": context
        }

    def interpret_compliance_gap(self, standard: str, control_id: str, gap_description: str) -> Dict[str, Any]:
        """Generates Plain English compliance gap interpretations."""
        return {
            "mode": "deterministic_offline_rule_engine",
            "standard": standard,
            "control_id": control_id,
            "summary": f"Automated Plain English interpretation for {standard} {control_id}: {gap_description}"
        }

    def analyze_deep(
        self,
        code: str,
        language: str,
        runtime_api_key: Optional[str] = None,
    ) -> Tuple[List[SecurityFinding], List[QualityFinding]]:
        effective_key = runtime_api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        if not effective_key or not effective_key.strip():
            return [], []

        key = effective_key.strip()
        system_instruction = (
            "You are the Sentinel Deep Code Inspection Engine (Group 2 Infosys Project).\n"
            "Inspect the provided source code thoroughly in real time for:\n"
            "1. Security Vulnerabilities (OWASP Top 10, CWE IDs, injection, embedded secrets, insecure crypto, access control, SSRF, XSS, command injection, buffer overflows, insecure deserialization).\n"
            "2. Code Quality & Logic Defects (logic bugs, unhandled exceptions, zero division, resource leaks, null/None pointer errors, infinite loops, dead code, high complexity, missing return statements).\n\n"
            "Return ONLY a valid JSON object with the following schema, and no markdown fences:\n"
            "{\n"
            '  "securityFindings": [\n'
            '    {\n'
            '      "title": "string",\n'
            '      "detail": "string",\n'
            '      "severity": "Critical"|"High"|"Medium"|"Low",\n'
            '      "owaspCategory": "string",\n'
            '      "cwe": "CWE-...",\n'
            '      "line": number,\n'
            '      "evidence": "string"\n'
            '    }\n'
            '  ],\n'
            '  "qualityFindings": [\n'
            '    {\n'
            '      "title": "string",\n'
            '      "detail": "string",\n'
            '      "severity": "High"|"Medium"|"Low",\n'
            '      "category": "string",\n'
            '      "line": number\n'
            '    }\n'
            '  ]\n'
            "}"
        )

        prompt = f"{system_instruction}\n\nLanguage: {language}\nSource Code to Inspect:\n```\n{code[:8000]}\n```"

        text = None

        # 1. Try google.genai SDK
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
                    text = response.text.strip()
                    break
            except Exception:
                continue

        # 2. Fallback to google.generativeai
        if not text:
            try:
                import google.generativeai as ggenai
                ggenai.configure(api_key=key)
                for model_name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
                    try:
                        model = ggenai.GenerativeModel(model_name)
                        response = model.generate_content(prompt)
                        if response and response.text:
                            text = response.text.strip()
                            break
                    except Exception:
                        continue
            except Exception:
                pass

        if not text:
            return [], []

        # Parse JSON output
        try:
            cleaned = re.sub(r"^```(json)?\n?", "", text.strip(), flags=re.IGNORECASE)
            cleaned = re.sub(r"\n?```$", "", cleaned)
            data = json.loads(cleaned)

            sec_list = []
            for item in data.get("securityFindings", []):
                sec_list.append(SecurityFinding(
                    id=f"s_ai_{len(sec_list) + 1}",
                    title=item.get("title", "Security finding"),
                    detail=item.get("detail", ""),
                    severity=item.get("severity", "Medium"),
                    owaspCategory=item.get("owaspCategory", "A03:2021 — Injection"),
                    cwe=item.get("cwe", "CWE-89"),
                    line=item.get("line"),
                    evidence=item.get("evidence", ""),
                    agent="Semantic AI Agent",
                ))

            qual_list = []
            for item in data.get("qualityFindings", []):
                qual_list.append(QualityFinding(
                    id=f"q_ai_{len(qual_list) + 1}",
                    title=item.get("title", "Quality issue"),
                    detail=item.get("detail", ""),
                    severity=item.get("severity", "Medium"),
                    category=item.get("category", "Reliability"),
                    line=item.get("line"),
                    agent="Semantic AI Agent",
                ))

            return sec_list, qual_list
        except Exception:
            return [], []
