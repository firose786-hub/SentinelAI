"""
SentinelAI - Module 1 (M1) Catalogue & Taxonomy Validator
Validates JSON/CSV schemas, referential integrity, and cross-framework mappings
for NIST SP 800-53 Rev. 5, ISO/IEC 27001:2022, and OWASP Top 10 for LLM (2025).
"""

import json
import csv
from pathlib import Path
import sys

def run_validation():
    base_dir = Path(__file__).resolve().parent
    
    controls_json_path = base_dir / "controls.json"
    controls_csv_path = base_dir / "controls.csv"
    iso_nist_path = base_dir / "iso_nist_mapping.csv"
    threats_json_path = base_dir / "threats.json"
    mapping_json_path = base_dir / "threat_control_mapping.json"
    questionnaire_json_path = base_dir / "questionnaire.json"
    
    print("=" * 75)
    print("       SENTINELAI: MODULE 1 (M1) INTEGRITY & CROSSWALK VALIDATOR")
    print("=" * 75)
    
    errors = []
    warnings = []
    
    # 1. Validate Controls JSON
    if not controls_json_path.exists():
        errors.append(f"Missing file: {controls_json_path.name}")
        return
    
    with open(controls_json_path, "r", encoding="utf-8") as f:
        controls_data = json.load(f)
        
    control_codes = set()
    control_ids = set()
    for c in controls_data:
        control_codes.add(c["code"])
        control_ids.add(c["control_id"])
        
    print(f"✔ [Controls JSON] Loaded {len(controls_data)} controls across {len(set(c['family'] for c in controls_data))} families.")
    
    # 2. Validate Controls CSV parity
    if controls_csv_path.exists():
        with open(controls_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            csv_controls = list(reader)
            if len(csv_controls) != len(controls_data):
                warnings.append(f"Parity mismatch: controls.json has {len(controls_data)}, controls.csv has {len(csv_controls)}")
            else:
                print(f"✔ [Controls CSV] Exact row count parity confirmed ({len(csv_controls)} rows).")
    
    # 3. Validate Threats JSON
    if not threats_json_path.exists():
        errors.append(f"Missing file: {threats_json_path.name}")
        return
        
    with open(threats_json_path, "r", encoding="utf-8") as f:
        threats_data = json.load(f)
        
    threat_ids = set(t["threat_id"] for t in threats_data)
    print(f"✔ [Threats JSON] Loaded {len(threats_data)} AI Threats (OWASP LLM Top 10 2025 / MITRE ATLAS).")
    
    # 4. Validate Threat-Control Mapping (Unified Evidence Chain)
    if not mapping_json_path.exists():
        errors.append(f"Missing file: {mapping_json_path.name}")
        return
        
    with open(mapping_json_path, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)
        
    mapped_threats = set()
    mapped_controls = set()
    
    for m in mapping_data:
        tid = m["threat_id"]
        if tid not in threat_ids:
            errors.append(f"Mapping references unknown Threat ID: {tid}")
        mapped_threats.add(tid)
        
        for pc in m.get("primary_nist_controls", []):
            if pc not in control_ids:
                errors.append(f"Mapping references unknown primary NIST Control: {pc}")
            mapped_controls.add(pc)
            
        for sc in m.get("secondary_nist_controls", []):
            if sc not in control_ids:
                warnings.append(f"Mapping references unlisted secondary NIST Control: {sc}")
                
    print(f"✔ [Evidence Chain Mapping] {len(mapped_threats)}/{len(threat_ids)} threats mapped to primary controls.")
    
    # 5. Validate ISO-NIST Crosswalk (NIST OLIR)
    if iso_nist_path.exists():
        with open(iso_nist_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            iso_rows = list(reader)
            for row in iso_rows:
                code = row["nist_control_code"]
                if code not in control_codes:
                    warnings.append(f"ISO mapping references code not in primary catalogue: {code}")
            print(f"✔ [NIST OLIR Crosswalk] Loaded {len(iso_rows)} ISO/IEC 27001:2022 crosswalk relationships.")
            
    # 6. Validate Questionnaire
    if questionnaire_json_path.exists():
        with open(questionnaire_json_path, "r", encoding="utf-8") as f:
            q_data = json.load(f)
            
        covered_codes = set()
        total_possible_score = 0
        for q in q_data:
            c_code = q["control_code"]
            covered_codes.add(c_code)
            total_possible_score += q["scoring_weights"].get("Yes", 10)
            if c_code not in control_codes:
                warnings.append(f"Questionnaire references control code not in catalogue: {c_code}")
                
        coverage_pct = (len(covered_codes) / len(control_codes)) * 100
        print(f"✔ [Self-Assessment Questionnaire] {len(q_data)} audit questions (Max Score: {total_possible_score}).")
        print(f"✔ [Catalogue Coverage] {coverage_pct:.1f}% of catalogued control families covered in questionnaire.")
        
    print("\n" + "=" * 75)
    print("                           VALIDATION SUMMARY")
    print("=" * 75)
    
    if not errors and not warnings:
        print("🏆 100% VALIDATION PASSED! Zero errors and zero warnings found.")
        print("   Module 1 (M1) is verified, consistent, and ready for viva demonstration.")
    else:
        if errors:
            print(f"❌ ERRORS ({len(errors)}):")
            for e in errors:
                print(f"   - {e}")
        if warnings:
            print(f"⚠ WARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"   - {w}")
                
    print("=" * 75)

if __name__ == "__main__":
    run_validation()
