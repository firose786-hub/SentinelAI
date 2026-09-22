import ast
import re
from typing import List, Dict, Any, Tuple, Optional
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from ..models.schemas import QualityFinding, Severity


class PythonQualityVisitor(ast.NodeVisitor):
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.findings: List[Dict[str, Any]] = []
        self.seen_rules = set()

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        line_num = node.lineno
        # Check broad exception
        if node.type is None or (isinstance(node.type, ast.Name) and node.type.id in ("Exception", "BaseException")):
            if "broad-except" not in self.seen_rules:
                self.seen_rules.add("broad-except")
                self.findings.append({
                    "title": "Overly broad exception handling",
                    "detail": "Catching every exception hides real failures and complicates debugging.",
                    "severity": "Medium",
                    "category": "Error handling",
                    "line": line_num,
                })

        # Check empty or pass-only handler
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            if "empty-catch" not in self.seen_rules:
                self.seen_rules.add("empty-catch")
                self.findings.append({
                    "title": "Silently swallowed exception",
                    "detail": "An empty handler discards the error without logging or recovery.",
                    "severity": "Medium",
                    "category": "Error handling",
                    "line": line_num,
                })
        elif len(node.body) == 0:
            if "empty-catch" not in self.seen_rules:
                self.seen_rules.add("empty-catch")
                self.findings.append({
                    "title": "Silently swallowed exception",
                    "detail": "An empty handler discards the error without logging or recovery.",
                    "severity": "Medium",
                    "category": "Error handling",
                    "line": line_num,
                })

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if any(alias.name == "*" for alias in node.names):
            if "star-import" not in self.seen_rules:
                self.seen_rules.add("star-import")
                self.findings.append({
                    "title": "Wildcard import",
                    "detail": "Wildcard imports pollute the namespace and hide dependencies.",
                    "severity": "Low",
                    "category": "Design",
                    "line": node.lineno,
                })
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # 1. Check mutable default arguments
        for default in node.args.defaults + node.args.kw_defaults:
            if default and isinstance(default, (ast.List, ast.Dict, ast.Set)):
                rule_key = f"mutable-default-{node.lineno}"
                if rule_key not in self.seen_rules:
                    self.seen_rules.add(rule_key)
                    self.findings.append({
                        "title": "Mutable default argument in function definition",
                        "detail": f"Default parameter value for function '{node.name}' is mutable (list/dict/set); mutated across function calls. Use None as default.",
                        "severity": "Medium",
                        "category": "Reliability",
                        "line": node.lineno,
                    })

        # 2. Check function length
        if hasattr(node, "end_lineno") and node.end_lineno:
            func_len = node.end_lineno - node.lineno + 1
            if func_len > 35 and "long-method" not in self.seen_rules:
                self.seen_rules.add("long-method")
                self.findings.append({
                    "title": "Long method / low decomposition",
                    "detail": f"Function '{node.name}' spans {func_len} lines; extract cohesive units into smaller helpers.",
                    "severity": "Medium",
                    "category": "Complexity",
                    "line": node.lineno,
                })

        # 3. Check for dead / unreachable code after return or raise
        found_terminal = False
        for stmt in node.body:
            if found_terminal:
                rule_key = f"dead-code-{stmt.lineno}"
                if rule_key not in self.seen_rules:
                    self.seen_rules.add(rule_key)
                    self.findings.append({
                        "title": "Unreachable code detected",
                        "detail": f"Statement on line {stmt.lineno} is unreachable after a return or raise statement.",
                        "severity": "Low",
                        "category": "Maintainability",
                        "line": stmt.lineno,
                    })
                break
            if isinstance(stmt, (ast.Return, ast.Raise)):
                found_terminal = True

        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp):
        if isinstance(node.op, ast.Div):
            line_num = getattr(node, "lineno", 1)
            if isinstance(node.right, ast.Call) and isinstance(node.right.func, ast.Name) and node.right.func.id == "len":
                rule_key = f"div-zero-{line_num}"
                if rule_key not in self.seen_rules:
                    self.seen_rules.add(rule_key)
                    self.findings.append({
                        "title": "Potential ZeroDivisionError on empty collection",
                        "detail": "Dividing by len(...) will raise ZeroDivisionError if the input list is empty; add an empty collection check.",
                        "severity": "Medium",
                        "category": "Reliability",
                        "line": line_num,
                    })
            elif isinstance(node.right, ast.Constant) and node.right.value == 0:
                rule_key = f"div-zero-lit-{line_num}"
                if rule_key not in self.seen_rules:
                    self.seen_rules.add(rule_key)
                    self.findings.append({
                        "title": "ZeroDivisionError in arithmetic expression",
                        "detail": "Division by literal zero will raise ZeroDivisionError at runtime.",
                        "severity": "High",
                        "category": "Reliability",
                        "line": line_num,
                    })
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        # 1. Track variable string assignments
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    if not hasattr(self, "string_vars"):
                        self.string_vars = set()
                    self.string_vars.add(t.id)

        # 2. Check for Subscript assignments to immutable types (strings, tuples)
        for target in node.targets:
            if isinstance(target, ast.Subscript):
                line_num = getattr(node, "lineno", 1)
                var_name = ""
                if isinstance(target.value, ast.Name):
                    var_name = target.value.id

                string_vars = getattr(self, "string_vars", set())
                if var_name in string_vars or var_name in ("text", "str", "string", "name", "s", "msg", "val", "word") or "str" in var_name.lower():
                    rule_key = f"immutable-str-mod-{line_num}"
                    if rule_key not in self.seen_rules:
                        self.seen_rules.add(rule_key)
                        self.findings.append({
                            "title": "Immutable Type Modification Attempt",
                            "detail": "Strings in Python are immutable. Attempting to modify a character at an index will result in a TypeError.",
                            "severity": "Low",
                            "category": "Code Smell",
                            "line": line_num,
                        })
                elif var_name in ("tup", "tuple", "coords", "point", "pair"):
                    rule_key = f"immutable-tup-mod-{line_num}"
                    if rule_key not in self.seen_rules:
                        self.seen_rules.add(rule_key)
                        self.findings.append({
                            "title": "Immutable Type Modification Attempt",
                            "detail": "Tuples in Python are immutable. Attempting to assign to an index will result in a TypeError.",
                            "severity": "Low",
                            "category": "Code Smell",
                            "line": line_num,
                        })

        # 3. Check for unclosed open()
        if isinstance(node.value, ast.Call):
            func_name = ""
            if isinstance(node.value.func, ast.Name):
                func_name = node.value.func.id
            if func_name in ("open", "io.open"):
                line_num = getattr(node, "lineno", 1)
                rule_key = f"unclosed-file-{line_num}"
                if rule_key not in self.seen_rules:
                    self.seen_rules.add(rule_key)
                    self.findings.append({
                        "title": "File opened without 'with' context manager",
                        "detail": "Opening a file without 'with' statement risks descriptor leaks if exceptions occur before close().",
                        "severity": "Low",
                        "category": "Reliability",
                        "line": line_num,
                    })
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            if node.value >= 1000 and "magic-number" not in self.seen_rules:
                self.seen_rules.add("magic-number")
                self.findings.append({
                    "title": "Magic number in logic",
                    "detail": f"Unnamed numeric literal {node.value} obscures intent; extract an explicit named constant.",
                    "severity": "Low",
                    "category": "Readability",
                    "line": getattr(node, "lineno", None),
                })
        self.generic_visit(node)


def analyze_python_quality(code: str, syntax_errors: Optional[List[str]] = None) -> List[QualityFinding]:
    findings: List[QualityFinding] = []
    lines = code.split("\n")

    # 1. Surface syntax & parsing errors as High-severity findings
    if syntax_errors:
        for err in syntax_errors:
            line_no = None
            m = re.search(r"Line\s+(\d+)", err, re.IGNORECASE)
            if m:
                line_no = int(m.group(1))
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title="Syntax / Parsing Error",
                detail=err,
                severity="High",
                category="Syntax / Compilation",
                line=line_no,
                agent="Code Analysis Agent",
            ))

    # 2. AST visitor analysis
    try:
        tree = ast.parse(code)
        visitor = PythonQualityVisitor(lines)
        visitor.visit(tree)
        for raw in visitor.findings:
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title=raw["title"],
                detail=raw["detail"],
                severity=raw["severity"],
                category=raw["category"],
                line=raw.get("line"),
                agent="Code Analysis Agent"
            ))
    except SyntaxError as e:
        if not any("Syntax / Parsing Error" in f.title for f in findings):
            line_no = e.lineno or 1
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title="Syntax / Parsing Error",
                detail=f"Line {line_no}: {e.msg} - code contains a syntax error preventing execution.",
                severity="High",
                category="Syntax / Compilation",
                line=line_no,
                agent="Code Analysis Agent",
            ))
    except Exception:
        pass

    # 3. Comment & line-level smell inspection
    seen_todo = False
    for idx, line in enumerate(lines, 1):
        trimmed = line.strip()
        if re.search(r"\b(TODO|FIXME|HACK|XXX)\b", line):
            if not seen_todo and (trimmed.startswith("#") or "//" in line or "/*" in line):
                seen_todo = True
                findings.append(QualityFinding(
                    id=f"q{len(findings) + 1}",
                    title="Unresolved TODO/FIXME marker",
                    detail="Outstanding work markers left in shipped code.",
                    severity="Low",
                    category="Maintainability",
                    line=idx,
                    agent="Code Analysis Agent"
                ))

        if re.search(r"/\s*0\b", line) and not any(f.title.startswith("ZeroDivision") for f in findings):
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title="ZeroDivisionError in arithmetic expression",
                detail=f"Line {idx}: Division by literal zero will raise ZeroDivisionError at runtime.",
                severity="High",
                category="Reliability",
                line=idx,
                agent="Code Analysis Agent",
            ))

    # 4. Deep nesting check
    max_indent = max((len(re.match(r"^[ \t]+", l).group(0)) for l in lines if re.match(r"^[ \t]+", l)), default=0)
    if max_indent >= 16 and not any(f.title == "Deep nesting detected" for f in findings):
        findings.append(QualityFinding(
            id=f"q{len(findings) + 1}",
            title="Deep nesting detected",
            detail=f"Indentation reaches {max_indent} columns; use guard clauses to flatten nested control flow.",
            severity="Medium",
            category="Complexity",
            line=None,
            agent="Code Analysis Agent"
        ))

    return findings


def analyze_java_quality(code: str, syntax_errors: Optional[List[str]] = None) -> List[QualityFinding]:
    findings: List[QualityFinding] = []
    lines = code.split("\n")

    # Surface syntax errors
    if syntax_errors:
        for err in syntax_errors:
            line_no = None
            m = re.search(r"Line\s+(\d+)", err, re.IGNORECASE)
            if m:
                line_no = int(m.group(1))
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title="Java Syntax / Compilation Error",
                detail=err,
                severity="High",
                category="Syntax / Compilation",
                line=line_no,
                agent="Code Analysis Agent",
            ))

    # Use javalang parser for AST analysis
    try:
        import javalang
        tree = javalang.parse.parse(code)

        seen_rules = set()
        for path, node in tree:
            if isinstance(node, javalang.tree.CatchClause):
                param = node.parameter
                type_name = param.types[0] if (param and param.types) else ""
                is_broad = type_name in ("Exception", "Throwable")
                is_empty = not node.block or len(node.block) == 0

                line_no = node.position.line if node.position else None

                if is_broad and "broad-except" not in seen_rules:
                    seen_rules.add("broad-except")
                    findings.append(QualityFinding(
                        id=f"q{len(findings) + 1}",
                        title="Overly broad exception handling",
                        detail="Catching every exception hides real failures and complicates debugging.",
                        severity="Medium",
                        category="Error handling",
                        line=line_no,
                        agent="Code Analysis Agent"
                    ))

                if is_empty and "empty-catch" not in seen_rules:
                    seen_rules.add("empty-catch")
                    findings.append(QualityFinding(
                        id=f"q{len(findings) + 1}",
                        title="Silently swallowed exception",
                        detail="An empty handler discards the error without logging or recovery.",
                        severity="Medium",
                        category="Error handling",
                        line=line_no,
                        agent="Code Analysis Agent"
                    ))

            elif isinstance(node, javalang.tree.Import):
                if node.wildcard and "star-import" not in seen_rules:
                    seen_rules.add("star-import")
                    findings.append(QualityFinding(
                        id=f"q{len(findings) + 1}",
                        title="Wildcard import",
                        detail="Wildcard imports pollute the namespace and hide dependencies.",
                        severity="Low",
                        category="Design",
                        line=node.position.line if node.position else None,
                        agent="Code Analysis Agent"
                    ))
    except Exception:
        # Fallback lexical check for Java
        seen_rules = set()
        for idx, line in enumerate(lines, 1):
            if re.search(r"catch\s*\(\s*(Exception|Throwable)\s+\w+\s*\)", line) and "broad-except" not in seen_rules:
                seen_rules.add("broad-except")
                findings.append(QualityFinding(
                    id=f"q{len(findings) + 1}",
                    title="Overly broad exception handling",
                    detail="Catching every exception hides real failures and complicates debugging.",
                    severity="Medium",
                    category="Error handling",
                    line=idx,
                    agent="Code Analysis Agent"
                ))
            if re.search(r"catch\s*\([^)]*\)\s*\{\s*\}", line) and "empty-catch" not in seen_rules:
                seen_rules.add("empty-catch")
                findings.append(QualityFinding(
                    id=f"q{len(findings) + 1}",
                    title="Silently swallowed exception",
                    detail="An empty handler discards the error without logging or recovery.",
                    severity="Medium",
                    category="Error handling",
                    line=idx,
                    agent="Code Analysis Agent"
                ))

    # Check TODOs in comments
    seen_todo = False
    for idx, line in enumerate(lines, 1):
        if re.search(r"\b(TODO|FIXME|HACK|XXX)\b", line) and ("//" in line or "/*" in line):
            if not seen_todo:
                seen_todo = True
                findings.append(QualityFinding(
                    id=f"q{len(findings) + 1}",
                    title="Unresolved TODO/FIXME marker",
                    detail="Outstanding work markers left in shipped code.",
                    severity="Low",
                    category="Maintainability",
                    line=idx,
                    agent="Code Analysis Agent"
                ))

    return findings


def analyze_javascript_quality(code: str, syntax_errors: Optional[List[str]] = None) -> List[QualityFinding]:
    findings: List[QualityFinding] = []
    lines = code.split("\n")
    seen_rules = set()

    if syntax_errors:
        for err in syntax_errors:
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title="JavaScript Syntax Error",
                detail=err,
                severity="High",
                category="Syntax / Compilation",
                agent="Code Analysis Agent",
            ))

    for idx, line in enumerate(lines, 1):
        trimmed = line.strip()
        if re.search(r"\bvar\s+\w+", line) and "var-usage" not in seen_rules:
            seen_rules.add("var-usage")
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title="Legacy 'var' keyword used",
                detail="Use 'let' or 'const' to ensure block scoping and avoid variable hoisting bugs.",
                severity="Low",
                category="Maintainability",
                line=idx,
                agent="Code Analysis Agent",
            ))

        if re.search(r"catch\s*\(\s*\w*\s*\)\s*\{\s*\}", line) and "empty-catch" not in seen_rules:
            seen_rules.add("empty-catch")
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title="Silently swallowed exception",
                detail="Empty catch block discards runtime exceptions without logging or recovery.",
                severity="Medium",
                category="Error handling",
                line=idx,
                agent="Code Analysis Agent",
            ))

        if re.search(r"\b(TODO|FIXME|HACK)\b", line) and ("//" in line or "/*" in line):
            if "todo" not in seen_rules:
                seen_rules.add("todo")
                findings.append(QualityFinding(
                    id=f"q{len(findings) + 1}",
                    title="Unresolved TODO/FIXME marker",
                    detail="Outstanding work markers left in shipped code.",
                    severity="Low",
                    category="Maintainability",
                    line=idx,
                    agent="Code Analysis Agent",
                ))

    return findings


def analyze_c_quality(code: str, syntax_errors: Optional[List[str]] = None) -> List[QualityFinding]:
    findings: List[QualityFinding] = []
    lines = code.split("\n")
    seen_rules = set()

    if syntax_errors:
        for err in syntax_errors:
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title="C/C++ Syntax Error",
                detail=err,
                severity="High",
                category="Syntax / Compilation",
                agent="Code Analysis Agent",
            ))

    for idx, line in enumerate(lines, 1):
        if re.search(r"\bmalloc\s*\(", line) and not re.search(r"\bfree\s*\(", code) and "memory-leak" not in seen_rules:
            seen_rules.add("memory-leak")
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title="Potential memory leak (malloc without corresponding free)",
                detail="Dynamically allocated memory must be released with free() along all control flow branches.",
                severity="Medium",
                category="Reliability",
                line=idx,
                agent="Code Analysis Agent",
            ))

        if re.search(r"\bgoto\s+\w+", line) and "goto-usage" not in seen_rules:
            seen_rules.add("goto-usage")
            findings.append(QualityFinding(
                id=f"q{len(findings) + 1}",
                title="Unstructured control flow via 'goto'",
                detail="Unstructured jump statements complicate control flow and make auditing difficult.",
                severity="Low",
                category="Design",
                line=idx,
                agent="Code Analysis Agent",
            ))

    return findings


def estimate_complexity(code: str, language: str = "Python") -> Dict[str, Any]:
    if language == "Python":
        try:
            blocks = cc_visit(code)
            if blocks:
                avg_cc = sum(b.complexity for b in blocks) / len(blocks)
                label = "High" if avg_cc > 12 else "Medium" if avg_cc > 6 else "Low"
                return {"score": round(avg_cc, 1), "label": label}
        except Exception:
            pass

    branches = len(re.findall(r"\b(if|for|while|case|catch|except|elif|&&|\|\||\?)\b", code))
    functions = max(1, len(re.findall(r"^[ \t]*(def |function |public |private |protected )", code, re.MULTILINE)))
    per_function = branches / functions
    label = "High" if per_function > 12 else "Medium" if per_function > 6 else "Low"
    return {"score": round(per_function, 1), "label": label}


class CodeAnalysisAgent:
    """Milestone 2 — Code Analysis Agent."""

    def __init__(self):
        self.name = "Code Analysis Agent"

    def analyze(
        self,
        code: str,
        language: str,
        syntax_errors: Optional[List[str]] = None,
    ) -> Tuple[List[QualityFinding], Dict[str, Any]]:
        if language == "Python":
            findings = analyze_python_quality(code, syntax_errors)
        elif language == "Java":
            findings = analyze_java_quality(code, syntax_errors)
        elif language in ("JavaScript", "TypeScript"):
            findings = analyze_javascript_quality(code, syntax_errors)
        elif language in ("C", "C++"):
            findings = analyze_c_quality(code, syntax_errors)
        else:
            findings = analyze_python_quality(code, syntax_errors)

        complexity = estimate_complexity(code, language)
        return findings, complexity
