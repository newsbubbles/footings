#!/usr/bin/env python3
"""footings check: a quick, read-only survey of a project for the footings skill.

Usage:
  python footings_check.py [PROJECT_DIR] [--json] [--strict]
  python footings_check.py init [PROJECT_DIR] [--agents-file]

The check never changes files and never prints secret values: only the file,
the line number and the kind of secret. `init` copies the footings doc
templates into PROJECT_DIR/docs/ and never overwrites an existing file.

Standard library only. Python 3.8 or newer.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__", ".mypy_cache",
    ".pytest_cache", ".tox", "dist", "build", ".next", ".nuxt", "target", ".idea",
    ".vscode", "site-packages", ".cache", "vendor",
}
MAX_SCAN_BYTES = 2_000_000
LARGE_FILE_BYTES = 10_000_000

DOCS = ["INTENT.md", "GLOSSARY.md", "ARCHITECTURE.md", "SCOPE.md", "DECISIONS.md"]

CODE_EXT = {
    ".py": "Python", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".jsx": "JavaScript", ".go": "Go",
    ".rs": "Rust", ".java": "Java", ".kt": "Kotlin", ".rb": "Ruby", ".php": "PHP",
    ".cs": "C#", ".c": "C", ".h": "C", ".cpp": "C++", ".hpp": "C++", ".swift": "Swift",
    ".sh": "Shell", ".bash": "Shell", ".ps1": "PowerShell", ".sql": "SQL",
    ".html": "HTML", ".css": "CSS", ".vue": "Vue", ".svelte": "Svelte", ".lua": "Lua",
    ".gd": "GDScript",
}
DOC_EXT = {".md", ".markdown", ".rst", ".txt"}

SECRET_FILE_PATTERNS = [
    (re.compile(r".*\.(pem|key|p12|pfx|keystore|jks)$", re.I), "private key or certificate store file"),
    (re.compile(r"^id_(rsa|dsa|ecdsa|ed25519)$"), "SSH private key file"),
    (re.compile(r"^\.env(\..+)?$"), "environment file"),
    (re.compile(r"^(credentials|service[-_]account).*\.json$", re.I), "credentials file"),
    (re.compile(r"^\.(netrc|pgpass)$"), "password file"),
]
ENV_SAFE = re.compile(r"\.(example|sample|template|dist)$", re.I)

SECRET_CONTENT_PATTERNS = [
    (re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"), "GitHub token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"), "GitHub token"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}"), "Anthropic API key"),
    (re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}"), "OpenAI-style API key"),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), "Google API key"),
    (re.compile(r"\bhf_[A-Za-z0-9]{30,}\b"), "Hugging Face token"),
    (re.compile(r"\b[MN][A-Za-z\d]{23,25}\.[\w-]{6}\.[\w-]{27,}\b"), "Discord bot token"),
    (re.compile(r"postgres(?:ql)?://[^:\s/'\"]+:[^@\s'\"\]]{3,}@"), "database URL with password"),
    (re.compile(r"mysql://[^:\s/]+:[^@\s]{3,}@"), "database URL with password"),
    (re.compile(r"mongodb(?:\+srv)?://[^:\s/]+:[^@\s]{3,}@"), "database URL with password"),
]
GENERIC_SECRET = re.compile(
    r"""(?ix)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|private[_-]?key|client[_-]?secret)\b
    \s*[:=]\s*["']([^"'\s]{8,})["']"""
)
# passwords written down in prose: agent notes, chat exports, READMEs (English and German)
PROSE_SECRET = re.compile(
    r"""(?i)\b(password|passwort|kennwort|passphrase|pw|token|api[\s_-]?key|secret)\b[\s:=(]{0,3}(?:is|ist|lautet|was|war)?[\s:=(]{0,3}(?P<q>[`'"])(?P<val>[^`'"\s]{6,})(?P=q)"""
)
HTPASSWD_LINE = re.compile(r"^[\w.-]{1,32}:\$(apr1|2[aby]|5|6)\$")
PLACEHOLDER = re.compile(r"(?i)(your|example|changeme|change_me|xxx|placeholder|dummy|test|<|\$\{|\{\{|env\(|getenv|environ|process\.env|\*\*\*)")

DB_PORTS = {"5432": "PostgreSQL", "3306": "MySQL", "6379": "Redis", "27017": "MongoDB", "9200": "Elasticsearch", "11434": "Ollama", "6333": "Qdrant", "8080": "an internal web service"}

GRAND_NOUNS = re.compile(
    r"\b([A-Z][A-Za-z]*OS|OS|AGI|(?i:operating system|kernel|universe|metaverse|megaverse|consciousness|sentient|sentience|ecosystem))\b"
)

MANIFESTS = ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile", "package.json", "go.mod",
             "Cargo.toml", "Gemfile", "composer.json", "pom.xml", "build.gradle", "environment.yml"]
LOCKS = ["uv.lock", "poetry.lock", "Pipfile.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
         "bun.lockb", "Cargo.lock", "go.sum", "Gemfile.lock", "composer.lock", "requirements.lock"]


def _git_tracked(root: Path) -> set[str] | None:
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return {p for p in out.stdout.decode("utf-8", "replace").split("\0") if p}


def _git_visible(root: Path) -> list[str] | None:
    """Tracked plus untracked files that git does not ignore."""
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "-co", "--exclude-standard"],
                             capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return [p for p in out.stdout.decode("utf-8", "replace").split(chr(0)) if p]


def _walk(root: Path):
    visible = _git_visible(root)
    if visible is not None:
        for rel in visible:
            parts = rel.split("/")
            if any(part in SKIP_DIRS for part in parts[:-1]):
                continue
            path = root / rel
            if path.is_file():
                yield path
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield Path(dirpath) / name


def _read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_SCAN_BYTES:
            return None
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data[:4096]:
        return None
    return data.decode("utf-8", "replace")


def _line_secret(line: str, is_doc: bool) -> str | None:
    if "re.compile(" in line or "RegExp(" in line:
        return None  # a detection pattern, not a secret
    for pat, kind in SECRET_CONTENT_PATTERNS:
        if pat.search(line):
            return kind
    if HTPASSWD_LINE.search(line):
        return "password hash (htpasswd)"
    if not is_doc:
        m = GENERIC_SECRET.search(line)
        if m and not PLACEHOLDER.search(m.group(2)):
            return f"hard-coded {m.group(1).lower()}"
    if is_doc:
        m = PROSE_SECRET.search(line)
        if m and _looks_like_password(m.group("val")):
            return f"{m.group(1).lower()} written in plain text"
    return None


def _looks_like_password(v: str) -> bool:
    if PLACEHOLDER.search(v) or "<" in v or "/" in v:
        return False
    if re.fullmatch(r"[a-z_][a-z_.-]*", v):  # a lowercase identifier, file name or key name
        return False
    kinds = sum(bool(re.search(p, v)) for p in (r"[a-z]", r"[A-Z]", r"[0-9]", r"[^A-Za-z0-9]"))
    return kinds >= 2


ARCHIVE_EXT = {".zip", ".jar", ".whl"}
TEXTISH = DOC_EXT | set(CODE_EXT) | {".yml", ".yaml", ".toml", ".ini", ".cfg", ".json", ".env", ".conf", ".service", ".log", ".jsonl", ".csv", ""}


def _scan_archive(path: Path):
    """Yield (member, line_no, kind) for secrets inside a zip archive. Values are never returned."""
    import zipfile
    try:
        with zipfile.ZipFile(path) as zf:
            for info in zf.infolist()[:20000]:
                if info.is_dir() or info.file_size > MAX_SCAN_BYTES:
                    continue
                member = info.filename
                base = member.rsplit("/", 1)[-1]
                for pat, kind in SECRET_FILE_PATTERNS:
                    if pat.match(base) and not ENV_SAFE.search(base):
                        yield member, None, kind
                        break
                ext = ("." + base.rsplit(".", 1)[-1].lower()) if "." in base else ""
                if ext not in TEXTISH and not base.startswith(".env"):
                    continue
                data = zf.read(info)
                if bytes(1) in data[:4096]:
                    continue
                for i, line in enumerate(data.decode("utf-8", "replace").splitlines(), 1):
                    if len(line) > 2000:
                        continue
                    kind = _line_secret(line, ext in DOC_EXT or ext in {".log", ".jsonl", ".txt", ""})
                    if kind:
                        yield member, i, kind
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile, NotImplementedError):
        return


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def check(root: Path) -> dict:
    root = root.resolve()
    tracked = _git_tracked(root)
    is_git = tracked is not None
    findings: dict[str, list] = {"critical": [], "warning": [], "info": []}

    def add(level: str, area: str, text: str):
        findings[level].append({"area": area, "text": text})

    # footings docs
    docs_dir = root / "docs"
    docs_present = {d: (docs_dir / d).exists() for d in DOCS}
    intent_filled = False
    glossary_rows: list[tuple[str, str]] = []
    if docs_present["INTENT.md"]:
        txt = (docs_dir / "INTENT.md").read_text("utf-8", "replace")
        intent_filled = "<" not in txt.split("## Slots", 1)[-1].split("## Already", 1)[0]
    if docs_present["GLOSSARY.md"]:
        for line in (docs_dir / "GLOSSARY.md").read_text("utf-8", "replace").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[0] and not set(cells[0]) <= set("-: ") and cells[0].lower() != "house term" and not cells[0].startswith("<"):
                glossary_rows.append((cells[0], cells[1]))

    lang_lines: Counter = Counter()
    doc_files = 0
    doc_words = 0
    code_files = 0
    names: Counter = Counter()
    grand_hits: Counter = Counter()
    grand_examples: dict[str, str] = {}
    services: list[str] = []
    top_level = sorted(p.name for p in root.iterdir() if p.name not in SKIP_DIRS and not p.name.startswith("."))
    has_tests = False
    manifests: list[str] = []
    locks: list[str] = []
    large_files: list[str] = []
    secret_hits: list[tuple[str, str, int | None, bool | None]] = []

    for path in _walk(root):
        rel = _rel(root, path)
        name = path.name
        in_git = (rel in tracked) if is_git else None
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > LARGE_FILE_BYTES and (in_git or not is_git):
            large_files.append(f"{rel} ({size // 1_000_000} MB)")

        # secret files
        for pat, kind in SECRET_FILE_PATTERNS:
            if pat.match(name) and not ENV_SAFE.search(name):
                secret_hits.append((rel, kind, None, in_git))
                break

        if name in MANIFESTS and rel.count("/") <= 3:
            manifests.append(rel)
        if name in LOCKS and rel.count("/") <= 3:
            locks.append(rel)
        ext = path.suffix.lower()
        if ext in ARCHIVE_EXT:
            for member, line_no, kind in _scan_archive(path):
                secret_hits.append((f"{rel}!{member}", kind, line_no, in_git))
        lowered = rel.lower()
        if re.search(r"(^|/)(tests?|spec|__tests__)/", lowered) or re.match(r"(test_.*\.py|.*_test\.(py|go)|.*\.(test|spec)\.[jt]sx?)$", name):
            has_tests = True
        if name.endswith(".service") or name in ("Procfile",) or name.startswith(("docker-compose", "compose.")):
            services.append(rel)

        if ext in CODE_EXT or ext in DOC_EXT or name.startswith((".env", "docker-compose", "compose.", "Dockerfile")) or ext in {".yml", ".yaml", ".toml", ".ini", ".cfg", ".json", ".service", ".conf"}:
            text = _read_text(path)
            if text is None:
                continue
            lines = text.splitlines()
            if ext in CODE_EXT:
                code_files += 1
                lang_lines[CODE_EXT[ext]] += sum(1 for l in lines if l.strip())
                stem = path.stem
                for part in re.split(r"[_\-.\s]+", stem):
                    if len(part) > 3:
                        names[part.lower()] += 1
            if ext in DOC_EXT and ext != ".txt":
                doc_files += 1
                doc_words += len(text.split())
                for l in lines:
                    if l.startswith("#"):
                        for m in GRAND_NOUNS.finditer(l):
                            key = m.group(0)
                            key = key if key.isupper() or key.endswith("OS") else key.lower()
                            grand_hits[key] += 1
                            grand_examples.setdefault(key, f"{rel}: {l.strip()[:90]}")
            # secret content
            for i, line in enumerate(lines, 1):
                if len(line) > 2000:
                    continue
                hit = _line_secret(line, ext in DOC_EXT)
                if hit:
                    secret_hits.append((rel, hit, i, in_git))
            # privileges and exposure
            if name.endswith(".service"):
                um = re.search(r"(?m)^\s*User\s*=\s*(\S+)", text)
                if not um:
                    add("warning", "privilege", f"{rel}: systemd unit has no User= line, so it runs as root")
                elif um.group(1) == "root":
                    add("critical", "privilege", f"{rel}: systemd unit runs as root")
            if name.startswith("Dockerfile") and not re.search(r"(?m)^\s*USER\s+(?!root\b)\S+", text):
                add("warning", "privilege", f"{rel}: container runs as root (no USER line)")
            if name.startswith(("docker-compose", "compose.")):
                for port, what in DB_PORTS.items():
                    if re.search(rf"""["']?(?:0\.0\.0\.0:)?{port}:\d+["']?""", text) and not re.search(rf"127\.0\.0\.1:{port}:", text):
                        add("warning", "exposure", f"{rel}: publishes port {port} ({what}) on all interfaces")
            if ext in {".sh", ".bash", ".service"} or name in ("Makefile",):
                if re.search(r"(?m)^\s*sudo\s", text):
                    add("info", "privilege", f"{rel}: uses sudo")
                if "chmod 777" in text or "chmod -R 777" in text:
                    add("warning", "privilege", f"{rel}: chmod 777 gives everyone write access")
            if ext in CODE_EXT and re.search(r"""host\s*=\s*["']0\.0\.0\.0["']|--host[ =]0\.0\.0\.0""", text):
                add("info", "exposure", f"{rel}: listens on all interfaces (0.0.0.0); fine behind a firewall or proxy, risky otherwise")

    # gitignore
    gi = root / ".gitignore"
    gi_text = gi.read_text("utf-8", "replace") if gi.exists() else ""
    if is_git and not gi.exists():
        add("warning", "hygiene", "no .gitignore: secrets, caches and data can end up in git")
    elif gi.exists() and ".env" not in gi_text:
        add("warning", "hygiene", ".gitignore does not list .env")
    if not is_git:
        add("critical", "hygiene", "not a git repository: no history, no undo")

    for rel, kind, line, in_git in secret_hits:
        where = f"{rel}:{line}" if line else rel
        if in_git:
            add("critical", "secrets", f"{where}: {kind}, tracked in git (treat as leaked if ever pushed: replace it, revoke the old one)")
        elif in_git is None:
            add("critical", "secrets", f"{where}: {kind}")
        else:
            add("info", "secrets", f"{where}: {kind}, not tracked by git (keep it that way)")

    if not manifests and code_files:
        add("warning", "hygiene", "no dependency file (requirements.txt, pyproject.toml, package.json...)")
    elif manifests and not locks:
        add("info", "hygiene", "dependencies declared but not locked (no lock file)")
    if code_files and not has_tests:
        add("warning", "hygiene", "no tests found")
    if not (root / "README.md").exists() and not any(p.lower().startswith("readme") for p in top_level):
        add("warning", "hygiene", "no README")
    if not any(p.upper().startswith(("LICENSE", "LICENCE", "COPYING")) for p in top_level):
        add("info", "hygiene", "no license file")
    for lf in large_files[:10]:
        add("warning", "hygiene", f"large file in the project: {lf}")

    code_lines = sum(lang_lines.values())
    words_per_line = round(doc_words / code_lines, 2) if code_lines else None
    if words_per_line is not None and words_per_line > 3:
        add("warning", "drift", f"docs outweigh code: {doc_words} words of docs for {code_lines} lines of code. Check which docs describe plans as if they were real.")
    if len(services) > 5:
        add("warning", "drift", f"{len(services)} service definitions. Each separate process needs a reason a module cannot meet.")
    for key, n in grand_hits.most_common(5):
        add("info", "naming", f"grand noun '{key}' in {n} heading(s), e.g. {grand_examples[key]}. Check it earns the name (references/vocabulary.md).")

    glossary_terms = {g[0].lower() for g in glossary_rows}
    unmapped = [g[0] for g in glossary_rows if not g[1] or g[1].startswith("<")]
    for t in unmapped:
        add("warning", "naming", f"glossary term '{t}' has no standard term yet")
    common = {"main", "test", "tests", "index", "utils", "util", "init", "config", "setup", "core", "base", "helpers", "types", "models", "server", "client", "app", "api", "data", "file", "files"}
    name_candidates = [(n, c) for n, c in names.most_common(40) if n not in common][:20]

    # phase suggestion
    crit_security = [f for f in findings["critical"] if f["area"] in ("secrets", "privilege", "exposure", "hygiene")]
    if not docs_present["INTENT.md"] or not intent_filled:
        phase = (0, "Intent: resolve and write docs/INTENT.md")
    elif not docs_present["ARCHITECTURE.md"]:
        phase = (1, "Survey: write the as-built map in docs/ARCHITECTURE.md")
    elif crit_security:
        phase = (2, "Secure and stabilize: fix the critical findings first")
    elif not docs_present["GLOSSARY.md"] or unmapped or not has_tests or not manifests:
        phase = (3, "Name and organize: glossary, structure, dependencies, a smoke test")
    else:
        phase = (4, "Refactor or later: judge phases 4 to 8 by hand (references/phases.md)")
    if crit_security and phase[0] < 2:
        phase = (phase[0], phase[1] + ". Critical security findings exist: handle them in the same session.")

    return {
        "project": root.name,
        "git": is_git,
        "phase": {"number": phase[0], "text": phase[1]},
        "docs": docs_present,
        "intent_filled": intent_filled,
        "glossary_terms": len(glossary_rows),
        "shape": {
            "code_files": code_files,
            "code_lines": code_lines,
            "languages": dict(lang_lines.most_common()),
            "doc_files": doc_files,
            "doc_words": doc_words,
            "doc_words_per_code_line": words_per_line,
            "service_definitions": services[:30],
            "top_level": top_level[:40],
            "has_tests": has_tests,
            "manifests": manifests,
            "locks": locks,
        },
        "names_to_map": [{"name": n, "count": c, "in_glossary": n in glossary_terms} for n, c in name_candidates],
        "findings": findings,
    }


def render(report: dict) -> str:
    out = []
    s = report["shape"]
    out.append(f"# footings check: {report['project']}")
    out.append("")
    out.append(f"**Suggested phase: {report['phase']['number']}. {report['phase']['text']}**")
    out.append("")
    out.append("## Footings docs")
    out.append(", ".join(f"{d} {'yes' if v else 'missing'}" for d, v in report["docs"].items()))
    out.append("")
    out.append("## Shape")
    langs = ", ".join(f"{k} {v}" for k, v in list(s["languages"].items())[:6]) or "none"
    out.append(f"- Code: {s['code_files']} files, {s['code_lines']} non-empty lines ({langs})")
    out.append(f"- Docs: {s['doc_files']} files, {s['doc_words']} words ({s['doc_words_per_code_line']} words per line of code)")
    out.append(f"- Service definitions: {len(s['service_definitions'])}")
    out.append(f"- Tests: {'yes' if s['has_tests'] else 'none found'}. Dependency files: {', '.join(s['manifests']) or 'none'}. Lock files: {', '.join(s['locks']) or 'none'}")
    out.append(f"- Git: {'yes' if report['git'] else 'no'}")
    out.append("")
    for level in ("critical", "warning", "info"):
        items = report["findings"][level]
        if not items:
            continue
        out.append(f"## {level.capitalize()} ({len(items)})")
        for f in items[:40]:
            out.append(f"- [{f['area']}] {f['text']}")
        if len(items) > 40:
            out.append(f"- ... and {len(items) - 40} more")
        out.append("")
    if report["names_to_map"]:
        out.append("## Names to map")
        out.append("Frequent words in code file names. Each one that is a house term needs a glossary row with its standard term.")
        out.append(", ".join(f"{n['name']} ({n['count']}{', in glossary' if n['in_glossary'] else ''})" for n in report["names_to_map"]))
        out.append("")
    out.append("Secret values are never printed. Run again after each fix.")
    return "\n".join(out)


def init(root: Path, agents_file: bool) -> str:
    here = Path(__file__).resolve().parent.parent / "templates"
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    today = _dt.date.today().isoformat()
    made, kept = [], []
    for d in DOCS:
        dst = docs / d
        if dst.exists():
            kept.append(d)
            continue
        dst.write_text((here / d).read_text("utf-8").replace("YYYY-MM-DD", today), "utf-8")
        made.append(d)
    lines = [f"Created in docs/: {', '.join(made) or 'nothing'}", f"Kept as they were: {', '.join(kept) or 'none'}"]
    if agents_file:
        note = ("\n## footings\n\nThis project uses the footings skill. Before any change, read docs/INTENT.md, "
                "docs/GLOSSARY.md, docs/ARCHITECTURE.md and docs/SCOPE.md, and follow the footings rules.\n")
        for fname in ("AGENTS.md", "CLAUDE.md"):
            p = root / fname
            if fname == "CLAUDE.md" and not p.exists():
                continue
            existing = p.read_text("utf-8", "replace") if p.exists() else ""
            if "footings skill" in existing:
                lines.append(f"{fname} already points to footings")
                continue
            p.write_text(existing + note, "utf-8")
            lines.append(f"Added the footings note to {fname}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    if args and args[0] == "init":
        root = Path(args[1] if len(args) > 1 else ".")
        print(init(root, "--agents-file" in flags))
        return 0
    root = Path(args[0] if args else ".")
    if not root.is_dir():
        print(f"not a folder: {root}", file=sys.stderr)
        return 2
    report = check(root)
    print(json.dumps(report, indent=2) if "--json" in flags else render(report))
    if "--strict" in flags and report["findings"]["critical"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
