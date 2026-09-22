"""
SQLite Database Layer for SentinelAI
Implements the 7-table relational schema:
1. users
2. audits
3. findings
4. risks
5. roadmap
6. memory
7. reports
plus legacy tables for backward compatibility.
"""

import json
import sqlite3
import hashlib
from typing import List, Optional, Dict, Any
from .config import DATABASE_PATH
from .models.schemas import AnalysisRecord
from .models.compliance_schemas import AuditRecord


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Audits Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audits (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            company_name TEXT,
            industry TEXT,
            employees TEXT,
            country TEXT DEFAULT 'Global',
            ai_model TEXT DEFAULT 'Enterprise LLM (GPT-4 / Gemini / Claude)',
            compliance_score REAL,
            ai_security_score REAL,
            risk_level TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # 3. Findings Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id TEXT,
            category TEXT,          -- ISO / NIST / OWASP
            control_id TEXT,        -- A.8.5, PR.AA-03, LLM01
            title TEXT,
            description TEXT,
            severity TEXT,          -- Critical/High/Medium/Low
            status TEXT,            -- Compliant/Non-Compliant/Partial/Vulnerable/Protected
            evidence TEXT,
            FOREIGN KEY (audit_id) REFERENCES audits(id)
        )
    """)

    # 4. Risks Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id TEXT,
            risk_type TEXT,
            cvss_score REAL,
            severity TEXT,
            business_impact TEXT,
            financial_exposure TEXT,
            downtime_hours REAL,
            FOREIGN KEY (audit_id) REFERENCES audits(id)
        )
    """)

    # 5. Roadmap Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmap (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id TEXT,
            priority TEXT,          -- P1/P2/P3
            week INTEGER,
            action TEXT,
            responsible_team TEXT,
            target_days INTEGER,
            point_gain INTEGER,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (audit_id) REFERENCES audits(id)
        )
    """)

    # 6. Memory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id TEXT,
            previous_audit_id TEXT,
            score_delta REAL,
            recurring_issues TEXT,
            insights TEXT,
            FOREIGN KEY (audit_id) REFERENCES audits(id)
        )
    """)

    # 7. Reports Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id TEXT,
            report_type TEXT,       -- PDF/Excel/JSON/CEO
            file_path TEXT,
            sha256_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (audit_id) REFERENCES audits(id)
        )
    """)

    # Analyses table for code scanner compatibility
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            created_at INTEGER NOT NULL,
            filename TEXT NOT NULL,
            language TEXT NOT NULL,
            code TEXT NOT NULL,
            verdict TEXT NOT NULL,
            overall_health INTEGER NOT NULL,
            security_score INTEGER NOT NULL,
            quality_score INTEGER NOT NULL,
            maintainability_score INTEGER NOT NULL,
            complexity TEXT NOT NULL,
            record_json TEXT NOT NULL
        )
    """)

    # Compliance audits table for SentinelAI
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compliance_audits (
            audit_id TEXT PRIMARY KEY,
            organization_id TEXT NOT NULL,
            organization_name TEXT NOT NULL,
            industry TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            date_formatted TEXT NOT NULL,
            iso_score INTEGER NOT NULL,
            nist_score INTEGER NOT NULL,
            overall_compliance INTEGER NOT NULL,
            ai_security_score INTEGER NOT NULL,
            overall_risk_score INTEGER NOT NULL,
            verdict TEXT NOT NULL,
            record_json TEXT NOT NULL
        )
    """)

    # Seed default admin user (admin / admin123)
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_pass_hash = hashlib.sha256("admin123".encode("utf-8")).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            ("admin", admin_pass_hash, "admin@sentinelai.security")
        )

    conn.commit()
    conn.close()


# ---------------- User Authentication ----------------

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    p_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    cursor.execute(
        "SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?",
        (username, p_hash)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row["id"], "username": row["username"], "email": row["email"]}
    return None


def register_user(username: str, password: str, email: str = "") -> bool:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    p_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, p_hash, email)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


# ---------------- Code Analysis Database Operations ----------------

def save_analysis(record: AnalysisRecord):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO analyses (
            id, created_at, filename, language, code, verdict,
            overall_health, security_score, quality_score, maintainability_score,
            complexity, record_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.id,
        record.createdAt,
        record.submission.filename,
        record.submission.language,
        record.code,
        record.summary.verdict,
        record.metrics.overallHealth,
        record.metrics.securityScore,
        record.metrics.qualityScore,
        record.metrics.maintainabilityScore,
        record.metrics.complexity,
        json.dumps(record.model_dump())
    ))
    conn.commit()
    conn.close()


def get_analysis(record_id: str) -> Optional[AnalysisRecord]:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT record_json FROM analyses WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        data = json.loads(row["record_json"])
        return AnalysisRecord(**data)
    return None


def list_analyses() -> List[AnalysisRecord]:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT record_json FROM analyses ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    records = []
    for r in rows:
        try:
            data = json.loads(r["record_json"])
            records.append(AnalysisRecord(**data))
        except Exception:
            continue
    return records


def delete_analysis(record_id: str) -> bool:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses WHERE id = ?", (record_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def clear_all_analyses() -> int:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses")
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count


# ---------------- Compliance Audits Database Operations ----------------

def save_compliance_audit(record: AuditRecord, user_id: int = 1):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Save to relational audits table
    cursor.execute("""
        INSERT OR REPLACE INTO audits (
            id, user_id, company_name, industry, employees, compliance_score,
            ai_security_score, risk_level, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.audit_id,
        user_id,
        record.organization_name,
        record.industry,
        "Enterprise",
        record.overall_compliance_score,
        record.ai_security_score,
        f"Risk {record.overall_risk_score}/100",
        record.verdict
    ))

    # 2. Save findings
    for c in record.controls_assessment:
        cursor.execute("""
            INSERT INTO findings (audit_id, category, control_id, title, description, severity, status, evidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.audit_id, c.standard, c.control_id, c.title, c.category, c.risk_level, c.status, c.evidence
        ))

    for f in record.ai_security_findings:
        cursor.execute("""
            INSERT INTO findings (audit_id, category, control_id, title, description, severity, status, evidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.audit_id, "OWASP LLM Top 10", f.owasp_id, f.title, f.attack_vector, f.severity, f.status, f.red_team_observation
        ))

    # 3. Save roadmap
    for idx, r in enumerate(record.roadmap, 1):
        week_num = 1 if r.priority == "P1" else (2 if r.priority == "P2" else 3)
        cursor.execute("""
            INSERT INTO roadmap (audit_id, priority, week, action, responsible_team, target_days, point_gain, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.audit_id, r.priority, week_num, r.action, r.responsible_team, r.target_days, r.expected_point_gain, "Pending"
        ))

    # 4. Save memory
    mem = record.memory_comparison
    cursor.execute("""
        INSERT INTO memory (audit_id, previous_audit_id, score_delta, recurring_issues, insights)
        VALUES (?, ?, ?, ?, ?)
    """, (
        record.audit_id,
        mem.previous_audit_id or "None",
        mem.compliance_score_delta,
        json.dumps([r.title for r in mem.recurring_findings]),
        mem.summary_of_progress
    ))

    # 5. Save legacy JSON record
    cursor.execute("""
        INSERT OR REPLACE INTO compliance_audits (
            audit_id, organization_id, organization_name, industry, timestamp,
            date_formatted, iso_score, nist_score, overall_compliance,
            ai_security_score, overall_risk_score, verdict, record_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.audit_id,
        record.organization_id,
        record.organization_name,
        record.industry,
        record.timestamp,
        record.date_formatted,
        record.iso_compliance_score,
        record.nist_compliance_score,
        record.overall_compliance_score,
        record.ai_security_score,
        record.overall_risk_score,
        record.verdict,
        json.dumps(record.model_dump())
    ))

    conn.commit()
    conn.close()


def get_compliance_audit(audit_id: str) -> Optional[AuditRecord]:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT record_json FROM compliance_audits WHERE audit_id = ?", (audit_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        data = json.loads(row["record_json"])
        return AuditRecord(**data)
    return None


def get_all_compliance_audits() -> List[AuditRecord]:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT record_json FROM compliance_audits ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    audits = []
    for r in rows:
        try:
            data = json.loads(r["record_json"])
            audits.append(AuditRecord(**data))
        except Exception:
            continue
    return audits


def get_compliance_audits_for_org(organization_id: str) -> List[AuditRecord]:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT record_json FROM compliance_audits WHERE organization_id = ? ORDER BY timestamp DESC", (organization_id,))
    rows = cursor.fetchall()
    conn.close()
    audits = []
    for r in rows:
        try:
            data = json.loads(r["record_json"])
            audits.append(AuditRecord(**data))
        except Exception:
            continue
    return audits


def delete_compliance_audit(audit_id: str) -> bool:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM compliance_audits WHERE audit_id = ?", (audit_id,))
    cursor.execute("DELETE FROM audits WHERE id = ?", (audit_id,))
    cursor.execute("DELETE FROM findings WHERE audit_id = ?", (audit_id,))
    cursor.execute("DELETE FROM risks WHERE audit_id = ?", (audit_id,))
    cursor.execute("DELETE FROM roadmap WHERE audit_id = ?", (audit_id,))
    cursor.execute("DELETE FROM memory WHERE audit_id = ?", (audit_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
