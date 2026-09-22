import ast
import time
import uuid
import re
from typing import Optional, List
from ..models.schemas import SubmissionResult

EXTENSION_MAP = {
    "py": "Python",
    "pyw": "Python",
    "java": "Java",
    "js": "JavaScript",
    "jsx": "JavaScript",
    "ts": "TypeScript",
    "tsx": "TypeScript",
    "c": "C",
    "h": "C",
    "cpp": "C++",
    "cc": "C++",
    "cxx": "C++",
    "hpp": "C++",
    "sql": "SQL",
    "html": "HTML",
}

ACCEPTED_EXTENSIONS = [f".{e}" for e in EXTENSION_MAP.keys()]


def detect_language(code: str, filename: Optional[str] = None) -> str:
    # 1. Check filename extension if available and non-generic
    if filename and "." in filename:
        ext = filename.split(".")[-1].lower()
        if ext in EXTENSION_MAP and filename not in ("snippet", "snippet.py", "pasted-snippet.py", "input.txt", "code.txt"):
            return EXTENSION_MAP[ext]

    src = code[:4000]
    lines = [l.strip() for l in src.split("\n") if l.strip()]

    # Java detection
    if re.search(r"\b(public|private|protected)\s+(static\s+)?(class|void|int|String|boolean|double|float)\b", src):
        return "Java"
    if re.search(r"\bSystem\.(out|err)\.print", src) or re.search(r"\bpackage\s+[\w.]+;", src):
        return "Java"

    # C / C++ detection
    if re.search(r"#include\s*[<\"]", src):
        return "C++" if re.search(r"\b(std::|namespace|class\s+\w+\s*\{|cout|cin)", src) else "C"
    if re.search(r"\b(printf|scanf|malloc|free)\s*\(", src) and re.search(r";\s*$", src, re.MULTILINE):
        return "C"

    # TypeScript detection
    if re.search(r"\b(interface|type)\s+\w+\s*[={]", src) or re.search(r":\s*(string|number|boolean|any)\b", src):
        return "TypeScript"

    # JavaScript detection
    if re.search(r"\b(const|let|var|function)\s+\w+", src) or re.search(r"\bconsole\.(log|error|warn)\s*\(", src):
        return "JavaScript"
    if re.search(r"(=>|\bdocument\.|window\.|addEventListener)", src):
        return "JavaScript"

    # Python detection
    if re.search(r"^\s*(from\s+\S+\s+import|import\s+\w+)", src, re.MULTILINE):
        return "Python"
    if re.search(r"\bdef\s+\w+\s*\(.*\)\s*:", src) or re.search(r"\bclass\s+\w+(\(.*\))?\s*:", src):
        return "Python"
    if re.search(r"\b(elif|self|pass|lambda|None|True|False)\b", src):
        return "Python"
    if re.search(r"\bprint\s*\(", src) and not re.search(r";\s*$", src, re.MULTILINE):
        return "Python"

    # Try AST parse to confirm Python
    try:
        parsed = ast.parse(code)
        # Verify it has meaningful code statements
        if any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom, ast.Assign, ast.AugAssign, ast.For, ast.While, ast.If, ast.With, ast.Try, ast.Return)) for node in ast.walk(parsed)):
            return "Python"
    except Exception:
        pass

    # Subscript assignment like text[0] = 'J' without semicolons
    if re.search(r"\w+\[.*\]\s*=", src) and not any(l.endswith(";") for l in lines):
        return "Python"

    return "Unknown"


def _check_balanced_delimiters(code: str) -> List[str]:
    errors: List[str] = []
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    line = 1
    in_string = None
    in_line_comment = False
    in_block_comment = False

    i = 0
    length = len(code)
    while i < length:
        ch = code[i]
        next_ch = code[i + 1] if i + 1 < length else ""

        if ch == "\n":
            line += 1
            in_line_comment = False
            i += 1
            continue

        if in_line_comment:
            i += 1
            continue

        if in_block_comment:
            if ch == "*" and next_ch == "/":
                in_block_comment = False
                i += 2
                continue
            i += 1
            continue

        if in_string:
            if ch == "\\":
                i += 2
                continue
            elif ch == in_string:
                in_string = None
            i += 1
            continue

        if ch == "#" or (ch == "/" and next_ch == "/"):
            in_line_comment = True
            i += 1
            continue

        if ch == "/" and next_ch == "*":
            in_block_comment = True
            i += 2
            continue

        if ch in ('"', "'", "`"):
            in_string = ch
            i += 1
            continue

        if ch in ("(", "[", "{"):
            stack.append((ch, line))
        elif ch in pairs:
            if not stack:
                errors.append(f"Unmatched '{ch}' on line {line}.")
            else:
                top_ch, top_line = stack.pop()
                if top_ch != pairs[ch]:
                    errors.append(f"Mismatched closing '{ch}' on line {line} for '{top_ch}' opened on line {top_line}.")

        i += 1

    if in_string:
        errors.append("Unterminated string literal.")
    for open_ch, open_line in stack:
        errors.append(f"Unclosed '{open_ch}' opened on line {open_line}.")

    return errors[:5]


def validate_python_syntax(code: str) -> List[str]:
    errors: List[str] = []
    try:
        ast.parse(code)
    except SyntaxError as e:
        line_info = f"Line {e.lineno}" if e.lineno else "Syntax error"
        msg = f"{line_info}: {e.msg}"
        errors.append(msg)
    except Exception as e:
        errors.append(f"Parsing error: {str(e)}")

    if not errors:
        lines = code.split("\n")
        for idx, raw in enumerate(lines, 1):
            text = raw.split("#")[0].rstrip()
            if not text.strip():
                continue
            if re.match(r"^\s*(def|class|if|elif|else|for|while|try|except|finally|with|match|case)\b", text):
                if not text.endswith(":") and not text.endswith("\\") and not re.search(r"[([{,]$", text):
                    errors.append(f"Line {idx}: block statement is missing a trailing ':'.")
            if "\t" in raw and raw.startswith(" "):
                errors.append(f"Line {idx}: mixed tabs and spaces in indentation.")

    return errors[:6]


def validate_java_syntax(code: str) -> List[str]:
    errors = _check_balanced_delimiters(code)

    if not re.search(r"\b(class|interface|enum|record)\s+\w+", code):
        errors.append("No class, interface, enum or record declaration found.")

    # Try javalang parser for robust structural syntax verification
    try:
        import javalang
        tokens = list(javalang.tokenizer.tokenize(code))
        parser = javalang.parser.Parser(tokens)
        parser.parse()
    except Exception as e:
        err_str = str(e)
        if "Expected" in err_str or "SyntaxError" in err_str or "ParserError" in err_str:
            errors.append(f"Java parser: {err_str}")

    # Statement semicolon checks
    lines = code.split("\n")
    for idx, raw in enumerate(lines, 1):
        text = raw.split("//")[0].strip()
        if not text or re.search(r"[{};:]$", text) or text.startswith("@") or text.startswith("*"):
            continue
        if re.match(r"^(import|package)\s", text):
            errors.append(f"Line {idx}: '{text.split()[0]}' statement must end with ';'.")
            continue
        if re.match(r"^\s*(return|throw|break|continue)\b", text) or re.match(r"^\w[\w<>\[\].]*\s+\w+\s*=", text):
            if not re.search(r"[,+\-*/&|(\\]$", text):
                errors.append(f"Line {idx}: statement may be missing ';'.")

    seen = set()
    deduped = []
    for err in errors:
        if err not in seen:
            seen.add(err)
            deduped.append(err)
    return deduped[:6]


def validate_submission(
    code: str,
    filename: Optional[str] = "pasted-snippet.py",
    requested_language: Optional[str] = "Auto-detect",
) -> SubmissionResult:
    auto = not requested_language or requested_language == "Auto-detect"
    language = detect_language(code, filename) if auto else requested_language

    syntax_errors: List[str] = []
    if not code.strip():
        syntax_errors = ["Submission is empty."]
    elif language == "Python":
        syntax_errors = validate_python_syntax(code)
    elif language == "Java":
        syntax_errors = validate_java_syntax(code)
    else:
        syntax_errors = _check_balanced_delimiters(code)

    sub_id = f"sub_{int(time.time()*1000):x}_{uuid.uuid4().hex[:6]}"

    # Auto-assign filename based on detected language if default
    effective_filename = filename or f"pasted-snippet.{'py' if language == 'Python' else 'java' if language == 'Java' else 'js'}"
    if effective_filename in ("snippet", "snippet.py", "pasted-snippet.py"):
        ext = "py" if language == "Python" else "java" if language == "Java" else "js" if language in ("JavaScript", "TypeScript") else "c"
        effective_filename = f"pasted-snippet.{ext}"

    return SubmissionResult(
        id=sub_id,
        filename=effective_filename,
        language=language,
        languageAutoDetected=auto,
        lineCount=len(code.split("\n")),
        charCount=len(code),
        syntaxValid=(len(syntax_errors) == 0),
        syntaxErrors=syntax_errors,
    )
