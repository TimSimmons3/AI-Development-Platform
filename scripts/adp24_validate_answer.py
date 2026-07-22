#!/usr/bin/env python3
import argparse
import hashlib
import os
import re
import sys
import tempfile
from pathlib import Path

def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fail(control: str, detail: str = "") -> int:
    print("ANSWER_VALIDATION_STATUS=FAIL")
    print(f"FAILED_CONTROL={control}")
    if detail:
        print(f"DETAIL={detail}")
    return 1

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", required=True)
    parser.add_argument("--raw", required=True)
    parser.add_argument("--normalized-output", required=True)
    args = parser.parse_args()
    expected = Path(args.expected)
    raw = Path(args.raw)
    output = Path(args.normalized_output)
    if not expected.is_file():
        return fail("EXPECTED_FILE", str(expected))
    if not raw.is_file():
        return fail("RAW_RESPONSE_FILE", str(raw))
    if output.exists():
        return fail("NORMALIZED_OUTPUT_EXISTS", str(output))
    try:
        expected_text = expected.read_text(encoding="utf-8")
        raw_text = raw.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return fail("UTF8_INPUT", str(exc))
    if not raw_text.strip():
        return fail("RAW_RESPONSE_EMPTY", str(raw))
    expected_normalized = normalize(expected_text)
    raw_normalized = normalize(raw_text)
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=output.name + ".", dir=str(output.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(raw_normalized + "\n")
        os.replace(temp_name, output)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    print(f"RAW_RESPONSE_PATH={raw}")
    print(f"RAW_RESPONSE_SHA256={sha256(raw)}")
    print(f"NORMALIZED_RESPONSE_PATH={output}")
    print(f"NORMALIZED_RESPONSE_SHA256={sha256(output)}")
    print(f"EXPECTED_ANSWER_PATH={expected}")
    if raw_normalized != expected_normalized:
        print("ANSWER_VALIDATION_STATUS=FAIL")
        print("FAILED_CONTROL=FACTUAL_CONTENT_MISMATCH")
        print(f"EXPECTED_NORMALIZED={expected_normalized}")
        print(f"ACTUAL_NORMALIZED={raw_normalized}")
        return 1
    print("ANSWER_VALIDATION_STATUS=PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
