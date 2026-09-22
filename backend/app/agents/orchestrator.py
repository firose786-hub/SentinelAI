import time
import uuid
import concurrent.futures
from typing import Dict, Any, List, Optional
from ..models.schemas import (
    AnalysisRecord,
    SubmissionResult,
    AgentTiming,
    SecurityFinding,
    QualityFinding,
)
from ..services.submission_service import validate_submission
from ..rag.rag_engine import retrieve, format_context, citations_of
from .code_analysis_agent import CodeAnalysisAgent
from .security_vulnerability_agent import SecurityVulnerabilityAgent
from .semantic_ai_agent import SemanticAIAgent
from .remediation_agent import RemediationAgent
from .pr_summary_agent import PrSummaryAgent
from ..database import save_analysis


class Orchestrator:
    """Multi-agent orchestrator coordinating the inspection pipeline."""

    def __init__(self):
        self.code_agent = CodeAnalysisAgent()
        self.security_agent = SecurityVulnerabilityAgent()
        self.semantic_ai_agent = SemanticAIAgent()
        self.remediation_agent = RemediationAgent()
        self.summary_agent = PrSummaryAgent()

    def run_pipeline(
        self,
        code: str,
        filename: str = "snippet.py",
        requested_language: str = "Auto-detect",
        api_key: Optional[str] = None,
    ) -> AnalysisRecord:
        timings: List[AgentTiming] = []

        # Step 1: Submission Validation
        sub_start = time.time()
        submission = validate_submission(code, filename, requested_language)
        timings.append(AgentTiming(
            agent="Code Submission Module",
            ms=int((time.time() - sub_start) * 1000),
        ))

        language = submission.language

        # Step 2: Parallel execution of Static Agents + Semantic AI Agent
        parallel_start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            fut_quality = executor.submit(self.code_agent.analyze, code, language, submission.syntaxErrors)
            fut_security = executor.submit(self.security_agent.scan, code, language)
            fut_ai = executor.submit(self.semantic_ai_agent.analyze_deep, code, language, api_key)

            quality_findings, complexity_info = fut_quality.result()
            security_findings = fut_security.result()
            ai_sec_findings, ai_qual_findings = fut_ai.result()

        # Merge findings cleanly and de-duplicate
        seen_sec_keys = {(f.title.lower(), f.line) for f in security_findings}
        for f in ai_sec_findings:
            key = (f.title.lower(), f.line)
            if key not in seen_sec_keys:
                seen_sec_keys.add(key)
                f.id = f"s{len(security_findings) + 1}"
                security_findings.append(f)

        seen_qual_keys = {(q.title.lower(), q.line) for q in quality_findings}
        for q in ai_qual_findings:
            key = (q.title.lower(), q.line)
            if key not in seen_qual_keys:
                seen_qual_keys.add(key)
                q.id = f"q{len(quality_findings) + 1}"
                quality_findings.append(q)

        timings.append(AgentTiming(
            agent="Code Analysis + Security + Semantic AI agents (parallel)",
            ms=int((time.time() - parallel_start) * 1000),
        ))

        # Step 3: RAG Grounding
        rag_query = f"{language} {' '.join(f.title for f in security_findings + quality_findings)} {code[:500]}"
        retrieved = retrieve(rag_query, k=6)
        context = format_context(retrieved)
        citations = citations_of(retrieved)

        # Step 4: Remediation + PR Summary (Parallel execution)
        rem_start = time.time()
        all_findings = security_findings + quality_findings

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            fut_rem = executor.submit(
                self.remediation_agent.remediate,
                all_findings,
                code,
                language,
                context,
            )
            fut_sum = executor.submit(
                self.summary_agent.summarize,
                submission.filename,
                language,
                security_findings,
                quality_findings,
                complexity_info.get("label", "Low"),
            )

            remediations = fut_rem.result()
            summary, metrics = fut_sum.result()

        timings.append(AgentTiming(
            agent="Remediation + PR Summary agents",
            ms=int((time.time() - rem_start) * 1000),
        ))

        # Step 5: Construct complete AnalysisRecord
        record_id = f"an_{int(time.time() * 1000):x}_{uuid.uuid4().hex[:6]}"
        record = AnalysisRecord(
            id=record_id,
            createdAt=int(time.time() * 1000),
            submission=submission,
            code=code,
            qualityFindings=quality_findings,
            securityFindings=security_findings,
            remediations=remediations,
            summary=summary,
            metrics=metrics,
            knowledgeCitations=citations,
            agentTimings=timings,
        )

        # Step 6: Persist in SQLite
        save_analysis(record)

        return record
