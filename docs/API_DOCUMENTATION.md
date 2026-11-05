# SentinelAI — REST API Documentation & Integration Specification

**Project**: *SentinelAI — Agentic AI-Based Smart Compliance Auditor & AI Security Validation Platform for Enterprise LLM Systems*  
**Base URL**: `http://localhost:8000`  
**Swagger UI**: `http://localhost:8000/docs`  
**OpenAPI Specification**: `http://localhost:8000/openapi.json`  

---

## 1. Authentication & Session Endpoints

### `POST /auth/login`
- **Description**: Authenticates user against SQLite database.
- **Request Body**:
  ```json
  {
    "username": "admin",
    "password": "admin"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "status": "success",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@sentinelai.internal",
      "role": "Super Admin",
      "full_name": "Dr. Alexander Cross (Global Security Director)",
      "status": "Active"
    },
    "token": "sentinel-session-jwt-token-2026"
  }
  ```
- **Error Codes**: `401 Unauthorized` (Invalid credentials).

### `POST /auth/register`
- **Description**: Registers a new auditor or analyst account in SQLite.
- **Request Body**:
  ```json
  {
    "username": "new_auditor",
    "password": "secure_password_123",
    "email": "auditor@enterprise.com",
    "role": "Compliance Officer"
  }
  ```
- **Response** (`200 OK`): `{"status": "success", "message": "User created successfully."}`

---

## 2. Health & Telemetry Endpoints

### `GET /health`
- **Description**: Returns live system diagnostics, database connectivity, and agent statuses.
- **Response** (`200 OK`):
  ```json
  {
    "status": "healthy",
    "platform": "SentinelAI - Agentic Smart Compliance Auditor & AI Security Validation Platform",
    "version": "2.0.0",
    "agents_active": 13,
    "database": "SQLite (data/analyses.db)",
    "gemini_api_configured": false
  }
  ```

---

## 3. Organizations & Audit Execution Endpoints

### `GET /organizations`
- **Description**: Retrieves all pre-configured enterprise baseline profiles.
- **Response** (`200 OK`): Returns array of `OrganizationProfile` objects (FinTech, HealthCare, Retail, Defense).

### `POST /audit/custom`
- **Description**: Triggers the 12-agent audit workflow on a custom user-defined enterprise profile.
- **Query Parameters**: `api_key` (Optional Gemini API key for cloud LLM reasoning).
- **Request Body**: Complete `OrganizationProfile` JSON object.
- **Response** (`200 OK`): Complete `AuditRecord` JSON object with all assessments, findings, debates, and forecasts.

### `POST /audit/{organization_id}`
- **Description**: Triggers audit for an existing registered organization (e.g., `org-fintech-01`).
- **Response** (`200 OK`): Full `AuditRecord` object.

---

## 4. Historical Audits & Retrieval Endpoints

### `GET /history`
- **Description**: Lists all historical audits ordered by recency.
- **Response** (`200 OK`): Array of `AuditRecord` objects.

### `GET /audit/{audit_id}`
- **Description**: Fetches an individual audit record by unique ID (e.g., `AUDIT-B7C94A12`).
- **Response** (`200 OK`): `AuditRecord` object.
- **Error Codes**: `404 Not Found`.

### `DELETE /audit/{audit_id}`
- **Description**: Removes an audit and cascades deletion across all 7 relational SQLite tables.
- **Response** (`200 OK`): `{"success": true, "message": "Audit AUDIT-... deleted."}`

---

## 5. Report Export Endpoints

### `GET /report/{audit_id}/pdf`
- **Description**: Generates and streams publication-grade ReportLab PDF.
- **Response Content-Type**: `application/pdf`.
- **Headers**: `Content-Disposition: attachment; filename="sentinelai-audit-...pdf"`.

### `GET /report/{audit_id}/excel`
- **Description**: Generates and streams multi-sheet styled Excel workbook (`.xlsx`).
- **Response Content-Type**: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`.

### `GET /report/{audit_id}/markdown`
- **Description**: Returns formatted Markdown summary.
- **Response Content-Type**: `text/markdown`.

### `GET /report/{audit_id}/json`
- **Description**: Returns structured machine-readable JSON dataset.
- **Response Content-Type**: `application/json`.
