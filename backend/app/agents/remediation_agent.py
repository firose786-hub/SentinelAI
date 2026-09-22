import json
import os
import re
from typing import List, Dict, Any, Optional
from ..models.schemas import Remediation, SecurityFinding, QualityFinding
from ..config import GEMINI_API_KEY, GEMINI_MODEL


DETERMINISTIC_REMEDIATIONS: Dict[str, Dict[str, str]] = {
    "CWE-89": {
        "title": "SQL query built by string concatenation",
        "recommendation": "Use parameterised queries or prepared statements with placeholder syntax (? or %s or $1) rather than string concatenation.",
        "bestPractice": "Always treat SQL statements and user inputs as distinct parameters passed to the database engine.",
        "Python": "cursor.execute('SELECT id, balance FROM accounts WHERE username = ?', (username,))",
        "Java": "PreparedStatement ps = connection.prepareStatement('SELECT * FROM users WHERE username = ?');\nps.setString(1, username);\nResultSet rs = ps.executeQuery();",
        "JavaScript": "const results = await db.query('SELECT * FROM users WHERE username = $1', [username]);",
        "TypeScript": "const results = await db.query('SELECT * FROM users WHERE username = $1', [username]);",
    },
    "CWE-798": {
        "title": "Credential embedded directly in source",
        "recommendation": "Load credentials from environment variables or a secure secrets manager rather than embedding literal strings.",
        "bestPractice": "Never store API keys or passwords in source code or repositories; rotate any exposed credentials.",
        "Python": "import os\nAPI_KEY = os.environ.get('API_KEY')",
        "Java": "String apiKey = System.getenv(\"API_KEY\");",
        "JavaScript": "const apiKey = process.env.API_KEY;",
        "TypeScript": "const apiKey = process.env.API_KEY;",
    },
    "CWE-79": {
        "title": "Cross-Site Scripting (XSS)",
        "recommendation": "Use textContent instead of innerHTML, or sanitize untrusted HTML using DOMPurify before inserting into DOM.",
        "bestPractice": "Always escape or sanitize untrusted data before rendering in the browser context.",
        "JavaScript": "element.textContent = userMessage; // or DOMPurify.sanitize(userHtml)",
        "TypeScript": "element.textContent = userMessage; // or DOMPurify.sanitize(userHtml)",
    },
    "CWE-327": {
        "title": "Weak hashing algorithm",
        "recommendation": "Replace MD5/SHA-1 with Argon2, bcrypt, or PBKDF2 for password storage, or SHA-256/SHA-512 for data integrity.",
        "bestPractice": "Always use adaptive key derivation functions with cryptographic salt for password hashing.",
        "Python": "from argon2 import PasswordHasher\n_hasher = PasswordHasher()\nhashed = _hasher.hash(password)",
        "Java": "import javax.crypto.SecretKeyFactory;\nimport javax.crypto.spec.PBEKeySpec;\n// Use PBKDF2WithHmacSHA256 or Argon2 library",
        "JavaScript": "const bcrypt = require('bcrypt');\nconst hash = await bcrypt.hash(password, 12);",
    },
    "CWE-78": {
        "title": "Operating system command execution",
        "recommendation": "Pass command arguments as an array/list without invoking a shell, or use native language APIs.",
        "bestPractice": "Avoid shell=True, system(), and string concatenation in system process invocations.",
        "Python": "import subprocess\nsubprocess.run(['tar', '-czf', 'backup.tgz', target_path], check=True)",
        "Java": "ProcessBuilder pb = new ProcessBuilder(\"tar\", \"-czf\", \"backup.tgz\", targetPath);\nProcess p = pb.start();",
        "JavaScript": "const { execFile } = require('child_process');\nexecFile('tar', ['-czf', 'backup.tgz', targetPath]);",
        "C": "// Use execve with distinct argument array rather than system()",
        "C++": "// Use execve or posix_spawn with argument array rather than system()",
    },
    "CWE-120": {
        "title": "Unbounded memory copy (buffer overflow)",
        "recommendation": "Replace unbounded functions like strcpy, sprintf, and gets with bounded alternatives (strncpy, snprintf, fgets).",
        "bestPractice": "Always pass explicit buffer size limits to prevent buffer overflow vulnerabilities.",
        "C": "strncpy(dest, src, sizeof(dest) - 1);\ndest[sizeof(dest) - 1] = '\\0';",
        "C++": "snprintf(dest, sizeof(dest), \"%s\", src);",
    },
    "CWE-134": {
        "title": "Format string vulnerability",
        "recommendation": "Always specify a literal format specifier string (e.g., printf(\"%s\", user_str)) rather than user input.",
        "bestPractice": "Format strings must always be static compile-time constants.",
        "C": "printf(\"%s\", message);",
        "C++": "printf(\"%s\", message.c_str());",
    },
    "CWE-95": {
        "title": "Dynamic code evaluation",
        "recommendation": "Avoid eval() and exec(); parse expressions safely using a dedicated parser or JSON serializer.",
        "bestPractice": "Never evaluate untrusted input as executable code.",
        "Python": "import ast\nsafe_value = ast.literal_eval(expression)",
        "JavaScript": "const parsed = JSON.parse(jsonString);",
    },
    "CWE-502": {
        "title": "Insecure deserialization of untrusted data",
        "recommendation": "Use safe serialization formats like JSON with schema validation rather than pickle or native ObjectInputStream.",
        "bestPractice": "Never deserialize arbitrary objects from untrusted sources.",
        "Python": "import json\ndata = json.loads(payload)",
        "Java": "ObjectMapper mapper = new ObjectMapper();\nUser user = mapper.readValue(payload, User.class);",
    },
    "CWE-338": {
        "title": "Non-cryptographic randomness",
        "recommendation": "Use secrets module in Python, SecureRandom in Java, or crypto.randomBytes in Node.js.",
        "bestPractice": "Standard PRNGs (random, java.util.Random) are predictable and insecure for security tokens.",
        "Python": "import secrets\nsession_token = secrets.token_urlsafe(32)",
        "Java": "import java.security.SecureRandom;\nSecureRandom rand = new SecureRandom();\nbyte[] bytes = new byte[24];\nrand.nextBytes(bytes);",
        "JavaScript": "const crypto = require('crypto');\nconst token = crypto.randomBytes(32).toString('hex');",
    },
    "CWE-489": {
        "title": "Debug mode enabled",
        "recommendation": "Disable debug mode in production environments and load debug settings from environment variables.",
        "bestPractice": "Never ship debug consoles or verbose stack traces to production environments.",
        "Python": "import os\nDEBUG = os.environ.get('APP_DEBUG', 'False').lower() == 'true'\napp.run(debug=DEBUG)",
        "Java": "// Configure environment profiles (spring.profiles.active=prod)",
    },
    "CWE-295": {
        "title": "TLS certificate verification disabled",
        "recommendation": "Enable TLS certificate verification (verify=True) to prevent man-in-the-middle attacks.",
        "bestPractice": "Always validate server certificates using trusted CA bundles.",
        "Python": "response = requests.get(url, verify=True)",
        "Java": "// Use default SSLSocketFactory with standard TrustManager",
    },
    "CWE-532": {
        "title": "Sensitive value written to logs",
        "recommendation": "Mask or redact sensitive fields (passwords, tokens, API keys) before logging.",
        "bestPractice": "Audit logging statements to prevent leakage of credentials or PII.",
        "Python": "logger.info('User authenticated: %s', username)",
        "Java": "logger.info(\"User authenticated: {}\", username);",
        "JavaScript": "logger.info(`User authenticated: ${username}`);",
    },
    "broad-except": {
        "title": "Overly broad exception handling",
        "recommendation": "Catch specific exception classes (e.g. ValueError, KeyError, SQLException) rather than generic Exception.",
        "bestPractice": "Granular exception handlers prevent hiding fatal bugs and unexpected runtime issues.",
        "Python": "try:\n    perform_action()\nexcept (ValueError, KeyError) as e:\n    logger.error('Action failed: %s', e)",
        "Java": "try {\n    performAction();\n} catch (SQLException e) {\n    logger.error(\"Action failed\", e);\n}",
        "JavaScript": "try {\n  performAction();\n} catch (err) {\n  if (err instanceof TypeError) { /* handle */ }\n}",
    },
    "empty-catch": {
        "title": "Silently swallowed exception",
        "recommendation": "Log the exception with stack trace or re-raise a domain-specific exception instead of discarding it.",
        "bestPractice": "Never write empty catch/except blocks that swallow errors silently.",
        "Python": "try:\n    perform_action()\nexcept Exception as e:\n    logger.warning('Failed to complete action: %s', e)\n    raise",
        "Java": "try {\n    performAction();\n} catch (SQLException e) {\n    logger.error(\"Operation failed\", e);\n    throw new ServiceException(\"Database error\", e);\n}",
        "JavaScript": "try {\n  performAction();\n} catch (err) {\n  logger.error('Error during execution', err);\n}",
    },
    "magic-number": {
        "title": "Magic number in logic",
        "recommendation": "Extract numeric literals into well-named constants explaining their domain meaning.",
        "bestPractice": "Named constants improve readability and make updates manageable.",
        "Python": "MAX_RETRY_LIMIT = 5\nTIMEOUT_SECONDS = 30",
        "Java": "private static final int MAX_RETRY_LIMIT = 5;",
        "JavaScript": "const MAX_RETRY_LIMIT = 5;",
    },
    "star-import": {
        "title": "Wildcard import",
        "recommendation": "Explicitly import only the required symbols or import the module namespace.",
        "bestPractice": "Explicit imports make dependencies clear and prevent name collisions.",
        "Python": "from typing import List, Optional, Dict",
        "Java": "import java.sql.Connection;\nimport java.sql.PreparedStatement;",
    },
    "immutable type modification attempt": {
        "title": "Immutable Type Modification Attempt",
        "recommendation": "To 'modify' a string, create a new string using slicing and concatenation, or string methods, as strings are immutable in Python.",
        "bestPractice": "Python strings are immutable. Operations that appear to modify a string actually return a new string with the changes.",
        "Python": "text = \"Hello\"\ntext = \"J\" + text[1:]\nprint(text)",
    },
    "syntax / parsing error": {
        "title": "Syntax / Parsing Error",
        "recommendation": "Correct syntax structure (colons, indentation, matching parentheses, or valid statements) before running the code.",
        "bestPractice": "Ensure all syntax elements are well-formed according to language specifications.",
        "Python": "def add(a, b):\n    return a + b",
        "Java": "public int add(int a, int b) {\n    return a + b;\n}",
    },
    "zerodivisionerror in arithmetic expression": {
        "title": "Potential ZeroDivisionError",
        "recommendation": "Add a guard clause checking that divisor != 0 or len(collection) > 0 before performing division.",
        "bestPractice": "Always validate denominators to prevent unhandled runtime ZeroDivisionError exceptions.",
        "Python": "if len(numbers) == 0:\n    return 0.0\nreturn sum(numbers) / len(numbers)",
        "Java": "if (count == 0) return 0;\nreturn total / count;",
    },
}


class RemediationAgent:
    """Milestone 3 — Multi-Language Remediation Agent."""

    def __init__(self):
        self.name = "Remediation Agent"

    def _generate_with_gemini(
        self,
        findings: List[Dict[str, Any]],
        code: str,
        language: str,
        context: str,
    ) -> Optional[List[Remediation]]:
        if not GEMINI_API_KEY:
            return None

        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)

            prompt = (
                f"You are the Remediation Agent for code review.\n"
                f"For each finding, provide: recommendation, secure coding best practice, and corrected code snippet in {language}.\n"
                f"Knowledge context:\n{context}\n\n"
                f"Findings:\n{json.dumps(findings, indent=2)}\n\n"
                f"Source code:\n{code[:4000]}\n\n"
                f"Return ONLY valid JSON array of objects with keys: findingId, title, recommendation, bestPractice, correctedCode."
            )

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            text = response.text or ""
            cleaned = re.sub(r"^```(json)?\n?", "", text.strip(), flags=re.IGNORECASE)
            cleaned = re.sub(r"\n?```$", "", cleaned)
            data = json.loads(cleaned)

            remediations = []
            for item in data:
                remediations.append(Remediation(
                    findingId=item.get("findingId", ""),
                    title=item.get("title", ""),
                    recommendation=item.get("recommendation", ""),
                    bestPractice=item.get("bestPractice", ""),
                    correctedCode=item.get("correctedCode", ""),
                ))
            return remediations
        except Exception:
            return None

    def remediate(
        self,
        findings: List[Any],
        code: str,
        language: str,
        context: str = "",
    ) -> List[Remediation]:
        if not findings:
            return []

        raw_list = []
        for f in findings:
            raw_list.append({
                "id": f.id,
                "title": f.title,
                "detail": f.detail,
                "severity": f.severity,
                "cwe": getattr(f, "cwe", ""),
                "category": getattr(f, "category", ""),
            })

        gemini_results = self._generate_with_gemini(raw_list, code, language, context)
        if gemini_results and len(gemini_results) == len(findings):
            return gemini_results

        # Deterministic knowledge-grounded remediation
        remediations = []
        for f in findings:
            cwe = getattr(f, "cwe", "")
            category = getattr(f, "category", "").lower()
            title = f.title.lower()

            template = None
            if cwe in DETERMINISTIC_REMEDIATIONS:
                template = DETERMINISTIC_REMEDIATIONS[cwe]
            else:
                for key, val in DETERMINISTIC_REMEDIATIONS.items():
                    if key in title or key in category:
                        template = val
                        break

            if not template:
                template = {
                    "title": f.title,
                    "recommendation": f"Review and refactor {f.title}. Adhere to secure coding standards.",
                    "bestPractice": "Follow defense-in-depth principles and validate all inputs.",
                    "Python": "# Refactor according to security guidelines",
                    "Java": "// Refactor according to security guidelines",
                    "JavaScript": "// Refactor according to security guidelines",
                    "TypeScript": "// Refactor according to security guidelines",
                    "C": "// Refactor according to security guidelines",
                    "C++": "// Refactor according to security guidelines",
                }

            code_snippet = template.get(language, template.get("Python", ""))

            remediations.append(Remediation(
                findingId=f.id,
                title=f.title,
                recommendation=template["recommendation"],
                bestPractice=template["bestPractice"],
                correctedCode=code_snippet,
            ))

        return remediations
