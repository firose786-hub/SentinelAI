"""
Dummy Enterprise Organizations Repository for Compliance & Security Auditing
Provides diverse organizational baselines across finance, healthcare, retail, and defense.
"""

from typing import List, Dict
from ..models.compliance_schemas import OrganizationProfile

ORGANIZATION_PROFILES: List[OrganizationProfile] = [
    OrganizationProfile(
        id="org-fintech-01",
        name="Apex Wealth & FinTech Global",
        industry="Financial Services & Wealth Management",
        size="5,000+ Employees (Global Tier 1)",
        annual_revenue_usd=450000000.0,
        description="Global digital banking and algorithmic wealth advisory enterprise operating cross-border multi-currency asset management portfolios.",
        llm_system_description="Apex Financial Advisor AI: An autonomous customer-facing LLM integrated with core banking APIs to query accounts, execute trades, and summarize SEC filings.",
        llm_capabilities=[
            "Automated Wealth Portfolio Advice",
            "Direct Core Banking API Function Calling",
            "RAG Search over Internal Financial Research",
            "Real-time Automated Wire Transfer Authorization"
        ],
        existing_controls={
            "has_security_policy": True,
            "has_ai_dev_security_policy": True,
            "has_rbac_and_mfa": True,
            "has_cloud_vendor_vetting": True,
            "has_prompt_firewall": False,  # Missing input guardrail
            "has_output_dlp": True,        # Masks credit cards, but not internal account balances
            "has_encryption_and_secrets_vault": True,
            "has_secure_ai_pipeline": False,
            "has_ai_governance_board": True,
            "has_llm_threat_model": False,  # No threat model for autonomous trading
            "has_audit_logging_and_monitoring": True,
            "has_incident_response_plan": True,
            "has_fallback_and_backup": True,
            "has_human_in_the_loop_for_tools": False  # Vulnerable to Excessive Agency
        },
        policy_documents={
            "sec_info_sec": "Apex FinTech Policy 2025: All user communications are logged. Access to banking APIs requires TLS 1.3. LLM tools have direct access to database execution.",
            "data_retention": "Customer banking transcripts are retained for 7 years in compliance with FINRA standards."
        }
    ),
    OrganizationProfile(
        id="org-health-02",
        name="BioCare Health Systems & Research",
        industry="Healthcare & Biomedical Diagnostics",
        size="12,000+ Employees (Hospital Network)",
        annual_revenue_usd=820000000.0,
        description="Integrated clinical healthcare provider and medical research institution maintaining millions of Electronic Health Records (EHR).",
        llm_system_description="MediAssist Doctor Copilot: Clinical decision support LLM summarizing patient EHR history, prescribing medication recommendations, and answering patient triage queries.",
        llm_capabilities=[
            "Patient EHR Record Summarization",
            "Clinical Drug Interaction Checker",
            "Patient-Facing Symptom Triage Chatbot",
            "Unconstrained Vector Search over Hospital Clinical Research Archive"
        ],
        existing_controls={
            "has_security_policy": True,
            "has_ai_dev_security_policy": False, # Missing AI specific lifecycle policies
            "has_rbac_and_mfa": True,
            "has_cloud_vendor_vetting": False, # Third party LLM API unvetted for HIPAA BAA
            "has_prompt_firewall": False,      # Direct medical prompt injection possible
            "has_output_dlp": False,           # Lacks medical PHI token redactor
            "has_encryption_and_secrets_vault": True,
            "has_secure_ai_pipeline": False,
            "has_ai_governance_board": False,
            "has_llm_threat_model": False,
            "has_audit_logging_and_monitoring": True,
            "has_incident_response_plan": False,
            "has_fallback_and_backup": True,
            "has_human_in_the_loop_for_tools": True
        },
        policy_documents={
            "hipaa_compliance": "BioCare Clinical Guidelines: Patient PHI must be protected under HIPAA Security Rule. AI diagnostic tools currently in beta testing across outpatient clinics.",
            "clinical_governance": "Doctors are encouraged to review AI prescriptions before signing."
        }
    ),
    OrganizationProfile(
        id="org-retail-03",
        name="OmniRetail AI Commerce",
        industry="E-Commerce & Digital Retail",
        size="2,500 Employees (High-growth)",
        annual_revenue_usd=180000000.0,
        description="Omnichannel retail platform with automated customer support, personalized product recommendation LLMs, and coupon generation engines.",
        llm_system_description="ShopGenie Customer Assistant: Public-facing e-commerce chatbot capable of issuing refund discount codes, searching catalog vectors, and writing customer reviews.",
        llm_capabilities=[
            "Public Customer Support & Return Assistance",
            "Dynamic Coupon & Discount Generation",
            "Catalog Vector Semantic Search",
            "Direct SQL Generation for Inventory Queries"
        ],
        existing_controls={
            "has_security_policy": True,
            "has_ai_dev_security_policy": False,
            "has_rbac_and_mfa": False,         # Weak internal dashboard access controls
            "has_cloud_vendor_vetting": True,
            "has_prompt_firewall": False,      # Prompt injection easily overrides refund discount limit
            "has_output_dlp": False,           # Inadvertently outputs raw database schema in error states
            "has_encryption_and_secrets_vault": False, # Secrets hardcoded in prompt template
            "has_secure_ai_pipeline": False,
            "has_ai_governance_board": False,
            "has_llm_threat_model": False,
            "has_audit_logging_and_monitoring": False,
            "has_incident_response_plan": False,
            "has_fallback_and_backup": False,
            "has_human_in_the_loop_for_tools": False # Auto-issues refunds without manager approval
        },
        policy_documents={
            "return_policy": "OmniRetail Support SOP: Customer refund limits default to $50, but AI agents are authorized to grant VIP discount codes up to 90% during disputes.",
            "internal_it": "Development and staging environments share vector databases with production."
        }
    ),
    OrganizationProfile(
        id="org-defense-04",
        name="AeroDefense Cyber Solutions",
        industry="Defense, Aerospace & Critical Infrastructure",
        size="8,500 Employees (Strict Compliance)",
        annual_revenue_usd=1200000000.0,
        description="Defense aerospace contractor developing mission-critical defense analytics, threat intelligence summarizers, and tactical planning agents.",
        llm_system_description="AeroIntel Copilot: On-premise air-gapped LLM agent running over classified technical manuals, avionics schematics, and supply chain telemetry.",
        llm_capabilities=[
            "Air-gapped Technical Manual Querying",
            "Telemetry Anomaly Classification",
            "Multi-Agent Threat Simulation",
            "Strict RBAC Vector Space Segmentation"
        ],
        existing_controls={
            "has_security_policy": True,
            "has_ai_dev_security_policy": True,
            "has_rbac_and_mfa": True,
            "has_cloud_vendor_vetting": True,
            "has_prompt_firewall": True,       # Comprehensive semantic prompt firewall
            "has_output_dlp": True,            # Full regex + military classification markings DLP
            "has_encryption_and_secrets_vault": True, # HSM key vault + AES-256 GCM
            "has_secure_ai_pipeline": True,    # Rigorous CI/CD security scanning & SBOM verification
            "has_ai_governance_board": True,
            "has_llm_threat_model": True,
            "has_audit_logging_and_monitoring": True,
            "has_incident_response_plan": True,
            "has_fallback_and_backup": True,
            "has_human_in_the_loop_for_tools": True # Strict dual-officer authorization for tool calls
        },
        policy_documents={
            "nist_800_171": "AeroDefense Classified Systems Charter: All LLM systems operate within isolated hardware enclaves. Output tokens are filtered against classification levels Secret/Top-Secret.",
            "airgap_operations": "No external internet connections permitted for inference."
        }
    ),
    OrganizationProfile(
        id="org-cloudsaas-05",
        name="NexusFlow Enterprise SaaS",
        industry="B2B Enterprise Productivity & Collaboration",
        size="1,200 Employees (Mid-Market SaaS)",
        annual_revenue_usd=95000000.0,
        description="Workflow automation and enterprise knowledge search platform indexing Slack messages, Jira tickets, and Google Workspace documents.",
        llm_system_description="NexusSearch AI: Multi-tenant workplace AI search engine generating cross-departmental summaries and automating Jira ticket triages.",
        llm_capabilities=[
            "Cross-tenant Workspace Document Search",
            "Autonomous Jira Ticket Resolution",
            "Slack Conversational Bot Integration",
            "Natural Language SQL Analytics"
        ],
        existing_controls={
            "has_security_policy": True,
            "has_ai_dev_security_policy": True,
            "has_rbac_and_mfa": True,
            "has_cloud_vendor_vetting": True,
            "has_prompt_firewall": True,       # Basic prompt filtering
            "has_output_dlp": False,           # Vulnerable to cross-tenant data leakage via vector search
            "has_encryption_and_secrets_vault": True,
            "has_secure_ai_pipeline": True,
            "has_ai_governance_board": False,  # Missing formal AI ethics and risk committee
            "has_llm_threat_model": True,
            "has_audit_logging_and_monitoring": True,
            "has_incident_response_plan": True,
            "has_fallback_and_backup": True,
            "has_human_in_the_loop_for_tools": False
        },
        policy_documents={
            "soc2_type2": "NexusFlow Security Summary: SOC 2 Type II certified for core cloud infrastructure. Multi-tenant vector databases utilize soft tenant filtering.",
            "privacy_policy": "Enterprise tenant data is segregated logically via database schema metadata."
        }
    )
]

def get_organization_by_id(org_id: str) -> OrganizationProfile:
    for org in ORGANIZATION_PROFILES:
        if org.id == org_id:
            return org
    # Fallback to Fintech if not found
    return ORGANIZATION_PROFILES[0]
