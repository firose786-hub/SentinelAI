import json
import re
from typing import List, Dict, Any, Tuple
from ..models.schemas import (
    PrSummary,
    HealthMetrics,
    QualityFinding,
    SecurityFinding,
    Severity,
    Verdict,
)
from ..config import GEMINI_API_KEY, GEMINI_MODEL

SEVERITY_ORDER: List[Severity] = ["Critical", "High", "Medium", "Low"]
SEVERITY_WEIGHT: Dict[str, int] = {"Critical": 26, "High": 15, "Medium": 7, "Low": 2}


def calculate_scores(
    security_findings: List[SecurityFinding],
    quality_findings: List[QualityFinding],
    complexity_label: str,
) -> HealthMetrics:
    # Security score
    sec_penalty = sum(SEVERITY_WEIGHT.get(f.severity, 2) for f in security_findings)
    security_score = max(5, min(100, 100 - sec_penalty))

    # Quality score
    qual_penalty = sum(SEVERITY_WEIGHT.get(f.severity, 2) for f in quality_findings)
    quality_score = max(5, min(100, 100 - qual_penalty))

    # Maintainability score adjusted for complexity
    complexity_adjustment = 18 if complexity_label == "High" else 8 if complexity_label == "Medium" else 0
    maintainability_score = max(5, min(100, quality_score - complexity_adjustment))

    # Overall code health
    overall_health = round(security_score * 0.5 + quality_score * 0.3 + maintainability_score * 0.2)

    return HealthMetrics(
        securityScore=security_score,
        qualityScore=quality_score,
        maintainabilityScore=maintainability_score,
        overallHealth=overall_health,
        complexity=complexity_label if complexity_label in ("Low", "Medium", "High") else "Low",
    )


class PrSummaryAgent:
    """Milestone 3 — PR Summary Agent."""

    def __init__(self):
        self.name = "PR Summary Agent"

    def _summarize_with_gemini(
        self,
        filename: str,
        language: str,
        security_findings: List[SecurityFinding],
        quality_findings: List[QualityFinding],
        metrics: HealthMetrics,
    ) -> Dict[str, Any]:
        if not GEMINI_API_KEY:
            return {}

        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)

            findings_summary = []
            for f in security_findings:
                findings_summary.append(f"[SECURITY - {f.severity}] {f.title} ({f.owaspCategory}, {f.cwe})")
            for f in quality_findings:
                findings_summary.append(f"[QUALITY - {f.severity}] {f.title} ({f.category})")

            prompt = (
                f"You are the PR Summary Agent for code review.\n"
                f"File: {filename} ({language})\n"
                f"Scores: Security {metrics.securityScore}/100, Quality {metrics.qualityScore}/100, Maintainability {metrics.maintainabilityScore}/100, Health {metrics.overallHealth}/100\n"
                f"Findings:\n" + "\n".join(findings_summary or ["None."]) + "\n\n"
                f"Write a 3-sentence executive overview and list prioritized fixes.\n"
                f"Return ONLY valid JSON with keys: 'executiveOverview' (string), 'prioritizedFixes' (array of strings, max 6)."
            )

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            text = response.text or ""
            cleaned = re.sub(r"^```(json)?\n?", "", text.strip(), flags=re.IGNORECASE)
            cleaned = re.sub(r"\n?```$", "", cleaned)
            return json.loads(cleaned)
        except Exception:
            return {}

    def summarize(
        self,
        filename: str,
        language: str,
        security_findings: List[SecurityFinding],
        quality_findings: List[QualityFinding],
        complexity_label: str = "Low",
    ) -> Tuple[PrSummary, HealthMetrics]:
        # 1. Calculate deterministic scores
        metrics = calculate_scores(security_findings, quality_findings, complexity_label)

        # 2. Compute severity breakdown
        breakdown = {sev: 0 for sev in SEVERITY_ORDER}
        for f in security_findings:
            if f.severity in breakdown:
                breakdown[f.severity] += 1
        for f in quality_findings:
            if f.severity in breakdown:
                breakdown[f.severity] += 1

        # 3. Determine deterministic verdict
        if breakdown["Critical"] > 0:
            verdict: Verdict = "Block"
        elif breakdown["High"] > 0 or breakdown["Medium"] > 0:
            verdict = "Request changes"
        elif breakdown["Low"] > 0:
            verdict = "Request changes"
        else:
            verdict = "Approve"

        # 4. Generate prioritized fix list
        all_findings = []
        for f in security_findings:
            all_findings.append((SEVERITY_ORDER.index(f.severity), f.title))
        for f in quality_findings:
            all_findings.append((SEVERITY_ORDER.index(f.severity), f.title))

        all_findings.sort(key=lambda x: x[0])
        prioritized_fixes = [item[1] for item in all_findings[:6]]

        # Default overview
        total = len(security_findings) + len(quality_findings)
        if total == 0:
            default_overview = f"Reviewed {filename} ({language}). Clean submission with no security vulnerabilities or code quality issues detected."
        else:
            default_overview = (
                f"Reviewed {filename} ({language}). Raised {len(security_findings)} security vulnerabilities and "
                f"{len(quality_findings)} code quality findings. Overall code health scored at {metrics.overallHealth}/100 "
                f"with a final review verdict of {verdict}."
            )

        # 5. Try Gemini enhancement if configured
        gemini_data = self._summarize_with_gemini(filename, language, security_findings, quality_findings, metrics)
        overview = gemini_data.get("executiveOverview") or default_overview
        if "prioritizedFixes" in gemini_data and isinstance(gemini_data["prioritizedFixes"], list) and gemini_data["prioritizedFixes"]:
            prioritized_fixes = [str(x) for x in gemini_data["prioritizedFixes"][:6]]

        summary = PrSummary(
            executiveOverview=overview,
            verdict=verdict,
            prioritizedFixes=prioritized_fixes,
            severityBreakdown=breakdown,
        )

        return summary, metrics
