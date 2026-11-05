"""
SentinelAI - SQLite Database Schema & Persistence Unit Tests
Tests relational tables: users, audits, findings, risks, roadmap, memory, security_logs.
"""

import pytest
import uuid
from backend.app.database import (
    init_db,
    authenticate_user,
    register_user,
    get_all_users,
    update_user_role,
    log_security_event,
    get_security_logs,
    save_compliance_audit,
    get_compliance_audit,
    get_all_compliance_audits,
    delete_compliance_audit
)
from backend.app.agents.compliance_orchestrator import ComplianceOrchestrator
from backend.app.data.dummy_organizations import get_organization_by_id

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    init_db()

def test_user_authentication_preseeded():
    # Test pre-seeded admin user
    user = authenticate_user("admin", "admin")
    assert user is not None
    assert user["username"] == "admin"
    assert user["role"] == "Super Admin"

    # Test invalid credentials
    invalid_user = authenticate_user("admin", "wrong_password")
    assert invalid_user is None

def test_user_registration_and_role_update():
    unique_user = f"tester_{uuid.uuid4().hex[:6]}"
    # Register new user
    registered = register_user(username=unique_user, password="password123", email=f"{unique_user}@sentinel.ai", role="SOC Analyst")
    assert registered is True

    # Duplicate registration should return False
    duplicate = register_user(username=unique_user, password="password123")
    assert duplicate is False

    # Authenticate new user
    auth = authenticate_user(unique_user, "password123")
    assert auth is not None
    assert auth["role"] == "SOC Analyst"

    # Update role
    updated = update_user_role(auth["id"], "AI Security Engineer")
    assert updated is True

    # Verify updated role
    re_auth = authenticate_user(unique_user, "password123")
    assert re_auth["role"] == "AI Security Engineer"

def test_security_event_logging():
    initial_logs = get_security_logs(limit=10)
    assert isinstance(initial_logs, list)

    log_security_event(username="test_auditor", role="Auditor", action="Security Scan Triggered", status="SUCCESS")
    new_logs = get_security_logs(limit=10)
    assert len(new_logs) > 0
    assert any(l["action"] == "Security Scan Triggered" for l in new_logs)

def test_compliance_audit_persistence():
    org = get_organization_by_id("org-retail-03")
    orchestrator = ComplianceOrchestrator()
    record = orchestrator.run_full_audit(org=org)

    # Save to SQLite
    save_compliance_audit(record)

    # Retrieve by ID
    fetched = get_compliance_audit(record.audit_id)
    assert fetched is not None
    assert fetched.audit_id == record.audit_id
    assert fetched.organization_name == record.organization_name
    assert fetched.overall_compliance_score == record.overall_compliance_score

    # Check list
    all_audits = get_all_compliance_audits()
    assert any(a.audit_id == record.audit_id for a in all_audits)

    # Delete test
    deleted = delete_compliance_audit(record.audit_id)
    assert deleted is True
    assert get_compliance_audit(record.audit_id) is None
