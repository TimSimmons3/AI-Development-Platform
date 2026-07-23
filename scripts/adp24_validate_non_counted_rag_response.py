#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import NoReturn


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(control: str, detail: str = "") -> NoReturn:
    print("NON_COUNTED_RESPONSE_VALIDATION=FAIL")
    print(f"FAILED_CONTROL={control}")
    if detail:
        print(f"DETAIL={detail}")
    raise SystemExit(1)


def write_normalized(output: Path, value: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=output.name + ".", dir=str(output.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(value + "\n")
        os.chmod(temp_name, 0o600)
        os.replace(temp_name, output)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--raw", required=True)
    parser.add_argument("--normalized-output", required=True)
    args = parser.parse_args()

    contract_path = Path(args.contract)
    raw_path = Path(args.raw)
    output_path = Path(args.normalized_output)

    if not contract_path.is_file():
        fail("CONTRACT_FILE", str(contract_path))
    if not raw_path.is_file():
        fail("RAW_RESPONSE_FILE", str(raw_path))
    if output_path.exists():
        fail("NORMALIZED_OUTPUT_EXISTS", str(output_path))

    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        raw_text = raw_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail("INPUT_PARSE", type(exc).__name__)

    if contract.get("status") != "FROZEN_FOR_SINGLE_NON_COUNTED_DRY_RUN":
        fail("CONTRACT_STATUS", str(contract.get("status")))

    selected = contract.get("selected_case") or {}
    if selected.get("id") != "C":
        fail("SELECTED_CASE", str(selected.get("id")))

    if not raw_text.strip():
        fail("RAW_RESPONSE_EMPTY", str(raw_path))

    actual = normalize(raw_text)
    expected = normalize(str(selected.get("expected_factual_answer") or ""))
    source_id = str(selected.get("source_id") or "")
    allowed = set(selected.get("allowed_citation_classifications") or [])

    if not expected or not source_id:
        fail("CONTRACT_SELECTED_CASE", "missing expected answer or source id")

    write_normalized(output_path, actual)

    citation_classification = ""
    citation_value = ""

    if actual == expected:
        citation_classification = "ABSENT"
    else:
        numeric = re.fullmatch(re.escape(expected) + r" \[([1-9][0-9]*)\]", actual)
        if numeric:
            citation_classification = "NUMERIC_BRACKET"
            citation_value = numeric.group(1)
        elif actual == f"{expected} [{source_id}]":
            citation_classification = "SOURCE_ID_BRACKET"
            citation_value = source_id
        elif expected in actual:
            fail("UNSUPPORTED_RESPONSE_SHAPE", actual)
        else:
            fail("FACTUAL_CONTENT_MISMATCH", actual)

    if citation_classification not in allowed:
        fail("CITATION_CLASSIFICATION_NOT_ALLOWED", citation_classification)

    print(f"RAW_RESPONSE_PATH={raw_path}")
    print(f"RAW_RESPONSE_SHA256={sha256(raw_path)}")
    print(f"NORMALIZED_RESPONSE_PATH={output_path}")
    print(f"NORMALIZED_RESPONSE_SHA256={sha256(output_path)}")
    print("FACTUAL_CONTENT_STATUS=PASS")
    print(f"CITATION_CLASSIFICATION={citation_classification}")
    if citation_value:
        print(f"CITATION_VALUE={citation_value}")
    print("NON_COUNTED_RESPONSE_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
