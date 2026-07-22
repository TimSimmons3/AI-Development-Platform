#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

REQUIRED_LITERAL = {
    "CONTEXT_PLACEHOLDER": "{{CONTEXT}}",
    "CONTEXT_OPEN": "<context>",
    "CONTEXT_CLOSE": "</context>",
    "OUTSIDE_KNOWLEDGE_PROHIBITION": "Do not use outside knowledge.",
    "EXACT_NOT_FOUND": "If the requested information is not present in the context, respond exactly: NOT FOUND.",
    "NO_TEMPLATE_COPY": "Do not copy instructions or examples from this template.",
    "DIRECT_ANSWER": "Return a direct answer without commentary.",
}

BANNED_PATTERNS = {
    "CONTAMINATION_STUDY": re.compile(r"according to the study", re.IGNORECASE),
    "CONTAMINATION_PERCENT": re.compile(r"increases efficiency by 20%", re.IGNORECASE),
    "OUTSIDE_KNOWLEDGE_PERMISSION": re.compile(r"if the answer (?:isn't|is not) present.*outside knowledge", re.IGNORECASE | re.DOTALL),
    "POSSESS_KNOWLEDGE_PERMISSION": re.compile(r"if the answer (?:isn't|is not) present.*possess.*knowledge", re.IGNORECASE | re.DOTALL),
    "CONCRETE_PERCENTAGE": re.compile(r"\b\d+(?:\.\d+)?%\b"),
}

def fail(control: str, path: Path, detail: str) -> int:
    print("RAG_TEMPLATE_LINT_STATUS=FAIL")
    print(f"FAILED_CONTROL={control}")
    print(f"AFFECTED_PATH={path}")
    print(f"DETAIL={detail}")
    return 1

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("template")
    args = parser.parse_args()
    path = Path(args.template)
    if not path.is_file():
        return fail("TEMPLATE_FILE", path, "missing")
    raw = path.read_bytes()
    if not raw:
        return fail("TEMPLATE_CONTENT", path, "empty")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        return fail("ASCII_ONLY", path, "non-ASCII content")
    for control, literal in REQUIRED_LITERAL.items():
        if literal not in text:
            return fail(control, path, literal)
    if text.count("{{CONTEXT}}") != 1:
        return fail("CONTEXT_PLACEHOLDER_COUNT", path, str(text.count("{{CONTEXT}}")))
    for control, pattern in BANNED_PATTERNS.items():
        match = pattern.search(text)
        if match:
            return fail(control, path, match.group(0).replace("\n", " ")[:160])
    print("RAG_TEMPLATE_LINT_STATUS=PASS")
    print(f"AFFECTED_PATH={path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
