"""
Secure Coding Knowledge Base.
OWASP Top 10, CWE guidance, secure coding standards and code-smell patterns,
authored as retrievable documents for the RAG pipeline.
"""

from typing import List, Dict, Any

KNOWLEDGE_BASE: List[Dict[str, Any]] = [
    {
        "id": "owasp-a01",
        "title": "A01:2021 — Broken Access Control",
        "source": "OWASP Top 10 2021",
        "tags": ["access control", "authorization", "idor", "privilege escalation"],
        "body": (
            "Broken access control occurs when an application fails to enforce what an authenticated "
            "user is allowed to do. Typical failures: insecure direct object references (IDOR) where a "
            "record id from the request is trusted without an ownership check, missing function level "
            "authorization on admin endpoints, elevation of privilege by editing a role field supplied "
            "by the client, and CORS misconfiguration allowing untrusted origins.\n"
            "Remediation: deny by default; enforce authorization server side on every request, never in "
            "the UI alone; validate that the authenticated principal owns or may act on the target resource; "
            "store roles in a dedicated server-controlled table, never on a user-editable profile record; "
            "log access control failures and rate limit them.\n"
            "In Python this usually means a decorator or dependency that resolves the current user and "
            "re-checks ownership inside the query (WHERE owner_id = current_user.id). In Java, enforce "
            "with method-level security annotations plus a repository query scoped to the principal."
        ),
    },
    {
        "id": "owasp-a02",
        "title": "A02:2021 — Cryptographic Failures",
        "source": "OWASP Top 10 2021",
        "tags": ["crypto", "hashing", "md5", "tls", "secrets", "encryption"],
        "body": (
            "Cryptographic failures cover sensitive data exposed by weak or missing cryptography. "
            "Indicators: MD5 or SHA1 used for passwords, ECB mode, encryption keys or IVs embedded "
            "directly in code, disabled certificate verification (verify=False), plain HTTP for "
            "credentials, and secrets committed in source.\n"
            "Remediation: hash passwords with bcrypt, scrypt or Argon2 with a per-user salt; use AES-GCM "
            "or ChaCha20-Poly1305 for encryption with keys from a managed secret store; always validate "
            "TLS certificates; classify data and avoid storing what is not required.\n"
            "Python: use passlib or hashlib.scrypt, never hashlib.md5 for credentials. Java: use "
            "SecureRandom rather than java.util.Random for tokens, and javax.crypto with GCM parameter specs."
        ),
    },
    {
        "id": "owasp-a03",
        "title": "A03:2021 — Injection (SQL, Command, LDAP, XSS)",
        "source": "OWASP Top 10 2021",
        "tags": ["sql injection", "xss", "command injection", "sanitisation", "eval"],
        "body": (
            "Injection happens when untrusted input is concatenated into an interpreter. SQL injection "
            "appears as string concatenation or f-strings inside a query. Command injection appears as "
            "os.system, subprocess with shell=True, or Runtime.getRuntime().exec built from user input. "
            "Cross-site scripting appears as unescaped user data rendered into HTML or innerHTML. Code "
            "injection appears as eval, exec or pickle.loads on untrusted data.\n"
            "Remediation: use parameterised queries or prepared statements exclusively (cursor.execute("
            "\"SELECT * FROM users WHERE id = %s\", (uid,)) in Python, PreparedStatement with setString "
            "in Java); pass argument arrays to subprocess without a shell; escape output contextually and "
            "prefer templating with automatic escaping; apply an allow-list validation on all input; never "
            "eval untrusted strings."
        ),
    },
    {
        "id": "owasp-a04",
        "title": "A04:2021 — Insecure Design",
        "source": "OWASP Top 10 2021",
        "tags": ["design", "threat model", "business logic", "rate limit"],
        "body": (
            "Insecure design describes missing or ineffective control design, which cannot be fixed "
            "by a perfect implementation. Examples: no rate limiting on authentication or password "
            "reset, unbounded resource consumption, trusting client-side validation, and business flows "
            "that allow replay or negative quantity values.\n"
            "Remediation: threat model each flow, write abuse cases alongside user stories, apply rate "
            "limits and quotas at the boundary, enforce invariants server side, and segregate tiers so "
            "that a compromise of one component does not grant access to another."
        ),
    },
    {
        "id": "owasp-a05",
        "title": "A05:2021 — Security Misconfiguration",
        "source": "OWASP Top 10 2021",
        "tags": ["configuration", "debug", "headers", "defaults", "stack trace"],
        "body": (
            "Security misconfiguration includes debug mode enabled in production, default credentials, "
            "verbose stack traces returned to clients, unnecessary features enabled, permissive CORS, "
            "and missing security headers.\n"
            "Remediation: build hardened, repeatable environments; disable debug and directory listing; "
            "return generic error messages while logging details server side; set Content-Security-Policy, "
            "X-Content-Type-Options, Strict-Transport-Security and a restrictive CORS allow-list; review "
            "defaults for every dependency.\n"
            "Flask: app.run(debug=True) must never ship. Spring: disable actuator endpoints or secure them."
        ),
    },
    {
        "id": "owasp-a06",
        "title": "A06:2021 — Vulnerable and Outdated Components",
        "source": "OWASP Top 10 2021",
        "tags": ["dependencies", "cve", "supply chain", "patching"],
        "body": (
            "Applications are vulnerable when they run components with known CVEs, unsupported versions, "
            "or unverified dependencies.\n"
            "Remediation: maintain an inventory (SBOM); pin versions and use lock files; run dependency "
            "scanning in CI; subscribe to advisories; remove unused dependencies; obtain packages only from "
            "official signed sources."
        ),
    },
    {
        "id": "owasp-a07",
        "title": "A07:2021 — Identification and Authentication Failures",
        "source": "OWASP Top 10 2021",
        "tags": ["authentication", "session", "password", "jwt", "brute force"],
        "body": (
            "Authentication failures include permitting weak passwords, credential stuffing without "
            "throttling, exposing session ids in URLs, not rotating session ids after login, missing "
            "multi-factor authentication, and JWTs accepted with alg=none or without signature verification.\n"
            "Remediation: verify JWT signatures and expiry with a fixed algorithm; enforce password strength "
            "and check against breach lists; throttle and lock after repeated failures; regenerate the "
            "session on privilege change; store session tokens in HttpOnly, Secure, SameSite cookies; offer MFA."
        ),
    },
    {
        "id": "owasp-a08",
        "title": "A08:2021 — Software and Data Integrity Failures",
        "source": "OWASP Top 10 2021",
        "tags": ["deserialization", "pickle", "integrity", "ci/cd"],
        "body": (
            "Integrity failures relate to code and data updates without integrity verification: insecure "
            "deserialization (pickle.loads, Java ObjectInputStream, yaml.load without SafeLoader), "
            "auto-update without signature checks, and untrusted CI/CD plugins.\n"
            "Remediation: never deserialize untrusted data into objects; prefer JSON with schema validation; "
            "use yaml.safe_load; sign artefacts and verify signatures; review CI configuration as security-relevant code."
        ),
    },
    {
        "id": "owasp-a09",
        "title": "A09:2021 — Security Logging and Monitoring Failures",
        "source": "OWASP Top 10 2021",
        "tags": ["logging", "monitoring", "audit", "pii"],
        "body": (
            "Insufficient logging and monitoring delays breach detection. Common problems: no logs for "
            "login failures or access control denials, logs stored only locally, no alerting, and — the "
            "inverse risk — logging secrets, tokens, passwords or personal data in clear text.\n"
            "Remediation: log authentication, authorization and high-value transactions with sufficient "
            "context and a correlation id; centralise and protect logs; alert on anomalies; redact credentials, "
            "tokens and PII before writing."
        ),
    },
    {
        "id": "owasp-a10",
        "title": "A10:2021 — Server-Side Request Forgery (SSRF)",
        "source": "OWASP Top 10 2021",
        "tags": ["ssrf", "url", "fetch", "network"],
        "body": (
            "SSRF occurs when the server fetches a remote resource using a user-supplied URL without "
            "validation, allowing access to internal services and cloud metadata endpoints.\n"
            "Remediation: validate URLs against an allow-list of schemes, hosts and ports; resolve DNS "
            "and reject private/link-local address ranges including 169.254.169.254; disable redirects or "
            "re-validate after each hop; segregate outbound traffic through a proxy."
        ),
    },
    {
        "id": "secrets-management",
        "title": "Embedded Secrets and Credential Management",
        "source": "CWE-798 / Secure Coding Standard",
        "tags": ["secrets", "api key", "password", "embedded credentials", "cwe-798"],
        "body": (
            "Credentials embedded directly in source (CWE-798) are API keys, passwords, tokens or private "
            "keys written as literals in code. They leak through repositories, client bundles and logs, "
            "and cannot be rotated without a code change.\n"
            "Detection heuristics: assignments to names containing key, secret, token, password or passwd "
            "with a long literal string; base64-looking constants; connection strings with inline credentials.\n"
            "Remediation: read secrets from environment variables or a managed secret store at runtime; "
            "keep .env out of version control; rotate any secret that has ever been committed — removing the "
            "line is not enough because git history retains it; scope keys to least privilege."
        ),
    },
    {
        "id": "input-validation",
        "title": "Input Validation and Output Encoding",
        "source": "OWASP Secure Coding Practices",
        "tags": ["validation", "encoding", "allow-list", "type safety"],
        "body": (
            "Validate all input on the trusted server side against an allow-list of expected type, length, "
            "format and range. Reject rather than sanitise where possible. Canonicalise before validating "
            "to defeat encoding tricks. Encode output for the context in which it appears — HTML body, "
            "HTML attribute, JavaScript, URL or SQL identifier — using a well-tested library rather than "
            "hand-written escaping."
        ),
    },
    {
        "id": "code-smells",
        "title": "Code Smells and Design Anti-Patterns",
        "source": "Refactoring Catalogue / Clean Code",
        "tags": ["code smell", "complexity", "duplication", "long method", "god class"],
        "body": (
            "Common smells: long method (a function doing several jobs, usually over 40 lines), god class "
            "(a class with too many responsibilities), long parameter list, deep nesting and high cyclomatic "
            "complexity, duplicated code, magic numbers and strings, dead code, primitive obsession, "
            "feature envy, and broad exception handling that swallows errors (bare except in Python, "
            "catch (Exception e) {} in Java).\n"
            "Remediation: extract method and extract class, replace conditional with guard clauses or "
            "polymorphism, introduce named constants, parameter objects for long lists, and catch narrow "
            "exception types while preserving the original cause."
        ),
    },
    {
        "id": "complexity-metrics",
        "title": "Complexity, Maintainability and Severity Scoring",
        "source": "Software Quality Metrics",
        "tags": ["complexity", "maintainability", "severity", "cvss", "scoring"],
        "body": (
            "Cyclomatic complexity counts independent paths; above 10 per function warrants refactoring, "
            "above 20 is high risk. Maintainability degrades with nesting depth, function length, "
            "duplicated blocks and missing tests.\n"
            "Severity scoring should combine exploitability and impact, in the spirit of CVSS. Critical: "
            "remotely exploitable with data loss or full compromise, such as SQL injection on an authentication "
            "path. High: exploitable with meaningful impact, such as production credentials embedded in source. "
            "Medium: needs preconditions or has limited impact, such as verbose error messages. Low: hygiene "
            "and defence-in-depth issues."
        ),
    },
    {
        "id": "python-secure",
        "title": "Python Secure Coding Guidelines",
        "source": "Secure Coding Standard — Python",
        "tags": ["python", "flask", "django", "subprocess", "pickle"],
        "body": (
            "Use parameterised DB APIs and ORMs; never build SQL with f-strings or %. Avoid eval, exec, "
            "pickle and yaml.load on untrusted input. Use subprocess.run([...]) without shell=True. Use "
            "secrets module, not random, for tokens. Use tempfile.mkstemp rather than predictable paths. "
            "Never run Flask or Django with debug=True in production. Prefer requests with verify=True. "
            "Catch specific exception types rather than bare except, and re-raise with context. Type-hint "
            "public functions and validate request payloads with pydantic or marshmallow."
        ),
    },
    {
        "id": "java-secure",
        "title": "Java Secure Coding Guidelines",
        "source": "Secure Coding Standard — Java",
        "tags": ["java", "jdbc", "spring", "deserialization", "preparedstatement"],
        "body": (
            "Use PreparedStatement with bound parameters for every query; Statement with concatenation "
            "is an injection defect. Avoid Java native deserialization of untrusted data (ObjectInputStream); "
            "prefer JSON with a strict schema. Use SecureRandom for tokens. Close resources with "
            "try-with-resources to avoid leaks. Do not catch Exception or Throwable broadly and swallow "
            "it; log with context and rethrow a domain exception. Validate with Bean Validation annotations "
            "at controller boundaries. Escape output in JSP/Thymeleaf using the framework's contextual "
            "escaping rather than raw output."
        ),
    },
    {
        "id": "pr-review-practice",
        "title": "Effective Pull Request Review Summaries",
        "source": "Engineering Review Handbook",
        "tags": ["pull request", "review", "summary", "verdict"],
        "body": (
            "A useful review summary opens with a two or three sentence executive overview of what the "
            "change does and its overall risk, then a severity breakdown, then a prioritised fix list "
            "ordered by exploitability and effort. Verdicts: Approve when no material issues remain; "
            "Approve with suggestions for non-blocking improvements; Request changes when defects must "
            "be addressed before merge; Block when a critical vulnerability or data-loss risk is present. "
            "Comments should be specific, cite a line, explain the risk, and offer a concrete corrected example."
        ),
    },
]
