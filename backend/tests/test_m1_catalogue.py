"""
SentinelAI - Module 1 (M1) Catalogue & Crosswalk Unit Tests
Tests referential integrity, JSON schema validity, and NIST OLIR crosswalk completeness.
"""

import pytest
import json
import csv
from pathlib import Path

@pytest.fixture(scope="module")
def m1_dir():
    # Base directory for Module 1
    root = Path(__file__).resolve().parent.parent.parent
    return root / "modules" / "m1_control_catalogue"

def test_controls_json_schema(m1_dir):
    path = m1_dir / "controls.json"
    assert path.exists(), "controls.json is missing"
    with open(path, "r", encoding="utf-8") as f:
        controls = json.load(f)
    assert len(controls) >= 14
    for c in controls:
        assert "control_id" in c
        assert "family" in c
        assert "code" in c
        assert "title" in c
        assert "framework" in c
        assert "criticality" in c
        assert "llm_specific_guidance" in c

def test_threats_json_schema(m1_dir):
    path = m1_dir / "threats.json"
    assert path.exists(), "threats.json is missing"
    with open(path, "r", encoding="utf-8") as f:
        threats = json.load(f)
    assert len(threats) >= 10
    for t in threats:
        assert "threat_id" in t
        assert "name" in t
        assert "mitre_atlas_id" in t
        assert "severity" in t
        assert "cvss_score" in t

def test_threat_control_mapping_integrity(m1_dir):
    controls_path = m1_dir / "controls.json"
    threats_path = m1_dir / "threats.json"
    mapping_path = m1_dir / "threat_control_mapping.json"

    with open(controls_path, "r", encoding="utf-8") as f:
        controls = json.load(f)
    with open(threats_path, "r", encoding="utf-8") as f:
        threats = json.load(f)
    with open(mapping_path, "r", encoding="utf-8") as f:
        mappings = json.load(f)

    control_ids = {c["control_id"] for c in controls}
    threat_ids = {t["threat_id"] for t in threats}

    assert len(mappings) >= 10
    for m in mappings:
        assert m["threat_id"] in threat_ids
        for c_id in m.get("primary_nist_controls", []):
            assert c_id in control_ids, f"Control ID {c_id} in mapping does not exist in controls.json"

def test_iso_nist_mapping_crosswalk(m1_dir):
    path = m1_dir / "iso_nist_mapping.csv"
    assert path.exists()
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) >= 20
    for r in rows:
        assert "nist_control_code" in r
        assert "iso_27001_control" in r
        assert "mapping_relationship" in r

def test_questionnaire_weights(m1_dir):
    path = m1_dir / "questionnaire.json"
    assert path.exists()
    with open(path, "r", encoding="utf-8") as f:
        questions = json.load(f)
    assert len(questions) >= 13
    for q in questions:
        assert "question_id" in q
        assert "options" in q
        assert "Yes" in q["scoring_weights"]
        assert q["scoring_weights"]["Yes"] >= 10
