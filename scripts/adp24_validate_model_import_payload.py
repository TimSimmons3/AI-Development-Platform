#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_ID = "llama-32-3b-rag-deterministic-test"
EXPECTED_NAME = "Llama 3.2 3B RAG Deterministic Test"
EXPECTED_BASE = "llama3.2:3b"
EXPECTED_MODEL_KEYS = {
    "id",
    "base_model_id",
    "name",
    "params",
    "meta",
    "access_grants",
    "is_active",
}
SAFE_META_KEYS = {
    "profile_image_url",
    "description",
    "capabilities",
    "suggestion_prompts",
    "tags",
}
ASSOCIATION_KEYS = {
    "knowledge",
    "tools",
    "skills",
    "functions",
    "filters",
    "tool_ids",
    "skill_ids",
    "function_ids",
    "filter_ids",
    "knowledge_ids",
    "files",
}
SECRET_TOKENS = {
    "api_key",
    "apikey",
    "token",
    "secret",
    "password",
    "cookie",
    "credential",
    "authorization",
}


def fail(control, value=""):
    print("MODEL_IMPORT_PAYLOAD_VALIDATION=FAIL")
    print(f"FAILED_CONTROL={control}")
    if value != "":
        print(f"FAILED_VALUE={value}")
    raise SystemExit(1)


def nonempty(value):
    return value not in (None, "", [], {}, False)


def find_secret_key(value, path="$"):
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = str(key).lower().replace("-", "_")
            if any(token in normalized for token in SECRET_TOKENS):
                return f"{path}.{key}"
            found = find_secret_key(item, f"{path}.{key}")
            if found:
                return found
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found = find_secret_key(item, f"{path}[{index}]")
            if found:
                return found
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    source = Path(args.input)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except Exception as exc:
        fail("IMPORT_JSON_PARSE", type(exc).__name__)

    if not isinstance(payload, list):
        fail("IMPORT_ROOT_FORMAT", type(payload).__name__)
    if len(payload) != 1:
        fail("IMPORT_MODEL_COUNT", len(payload))

    model = payload[0]
    if not isinstance(model, dict):
        fail("IMPORT_MODEL_TYPE", type(model).__name__)

    unexpected_keys = sorted(set(model) - EXPECTED_MODEL_KEYS)
    if unexpected_keys:
        fail("UNEXPECTED_MODEL_FIELD", unexpected_keys[0])

    secret_path = find_secret_key(model)
    if secret_path:
        fail("SECRET_BEARING_FIELD", secret_path)

    if model.get("id") != EXPECTED_ID:
        fail("MODEL_ID", model.get("id"))
    if model.get("name") != EXPECTED_NAME:
        fail("MODEL_NAME", model.get("name"))
    if model.get("base_model_id") != EXPECTED_BASE:
        fail("BASE_MODEL", model.get("base_model_id"))
    if model.get("is_active") is not True:
        fail("MODEL_ACTIVE", model.get("is_active"))

    params = model.get("params")
    if not isinstance(params, dict):
        fail("PARAMS_TYPE", type(params).__name__)
    if set(params) != {"seed", "temperature"}:
        fail("PARAMS_KEYS", ",".join(sorted(params)))
    if params.get("temperature") != 0:
        fail("TEMPERATURE", params.get("temperature"))
    if params.get("seed") != 42:
        fail("SEED", params.get("seed"))

    meta = model.get("meta")
    if not isinstance(meta, dict):
        fail("META_TYPE", type(meta).__name__)
    unknown_meta = sorted(set(meta) - SAFE_META_KEYS - ASSOCIATION_KEYS)
    if unknown_meta:
        fail("UNAPPROVED_META_FIELD", unknown_meta[0])
    for key in sorted(ASSOCIATION_KEYS):
        if nonempty(meta.get(key)):
            fail("MODEL_ASSOCIATION", key)

    access_grants = model.get("access_grants")
    if access_grants != []:
        fail("ACCESS_GRANTS", access_grants)

    canonical = json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    source_digest = hashlib.sha256(source.read_bytes()).hexdigest()

    print("MODEL_IMPORT_PAYLOAD_VALIDATION=PASS")
    print("IMPORT_ROOT=TOP_LEVEL_ARRAY")
    print("IMPORT_MODEL_COUNT=1")
    print(f"MODEL_ID={EXPECTED_ID}")
    print(f"BASE_MODEL={EXPECTED_BASE}")
    print("TEMPERATURE=0")
    print("SEED=42")
    print("MODEL_ASSOCIATIONS=ABSENT")
    print("ACCESS_GRANTS=EMPTY")
    print(f"IMPORT_PAYLOAD_SHA256={source_digest}")
    print(f"CANONICAL_IMPORT_SHA256={digest}")


if __name__ == "__main__":
    main()
