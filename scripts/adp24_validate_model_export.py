#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

EXPECTED_ID = "llama-32-3b-rag-deterministic-test"
EXPECTED_NAME = "Llama 3.2 3B RAG Deterministic Test"
EXPECTED_BASE = "llama3.2:3b"
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
ALLOWED_PARAMS = {"temperature", "seed", "system"}


def fail(control, value=""):
    print("MODEL_EXPORT_VALIDATION=FAIL")
    print(f"FAILED_CONTROL={control}")
    if value != "":
        print(f"FAILED_VALUE={value}")
    raise SystemExit(1)


def atomic_write(path, content):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        fail("OUTPUT_ALREADY_EXISTS", str(target))
    fd, temp_name = tempfile.mkstemp(prefix=target.name + ".", dir=str(target.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.replace(temp_name, target)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


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


def extract_models(root):
    if isinstance(root, list):
        return root
    if isinstance(root, dict) and isinstance(root.get("models"), list):
        return root["models"]
    if isinstance(root, dict) and root.get("id"):
        return [root]
    fail("EXPORT_ROOT_FORMAT", type(root).__name__)


def nonempty(value):
    return value not in (None, "", [], {}, False)


def validate_sanitized_payload(payload):
    if not isinstance(payload, list):
        fail("SANITIZED_IMPORT_ROOT_FORMAT", type(payload).__name__)
    if len(payload) != 1:
        fail("SANITIZED_IMPORT_MODEL_COUNT", len(payload))
    model = payload[0]
    if not isinstance(model, dict):
        fail("SANITIZED_IMPORT_MODEL_TYPE", type(model).__name__)
    if model.get("id") != EXPECTED_ID:
        fail("SANITIZED_IMPORT_MODEL_ID", model.get("id"))
    if model.get("name") != EXPECTED_NAME:
        fail("SANITIZED_IMPORT_MODEL_NAME", model.get("name"))
    if model.get("base_model_id") != EXPECTED_BASE:
        fail("SANITIZED_IMPORT_BASE_MODEL", model.get("base_model_id"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--sanitized-output", required=True)
    parser.add_argument("--report-output", required=True)
    args = parser.parse_args()

    source = Path(args.input)
    try:
        root = json.loads(source.read_text(encoding="utf-8"))
    except Exception as exc:
        fail("EXPORT_JSON_PARSE", type(exc).__name__)

    secret_path = find_secret_key(root)
    if secret_path:
        fail("SECRET_BEARING_FIELD", secret_path)

    models = extract_models(root)
    if len(models) != 1:
        fail("MODEL_COUNT", len(models))
    model = models[0]
    if not isinstance(model, dict):
        fail("MODEL_TYPE", type(model).__name__)

    if model.get("id") != EXPECTED_ID:
        fail("MODEL_ID", model.get("id"))
    if model.get("name") != EXPECTED_NAME:
        fail("MODEL_NAME", model.get("name"))
    if model.get("base_model_id") != EXPECTED_BASE:
        fail("BASE_MODEL", model.get("base_model_id"))
    if model.get("is_active", True) is not True:
        fail("MODEL_ACTIVE", model.get("is_active"))

    params = model.get("params") or {}
    if not isinstance(params, dict):
        fail("PARAMS_TYPE", type(params).__name__)
    unknown_params = sorted(set(params) - ALLOWED_PARAMS)
    if unknown_params:
        fail("UNAPPROVED_PARAM", unknown_params[0])
    if params.get("temperature") != 0:
        fail("TEMPERATURE", params.get("temperature"))
    if params.get("seed") != 42:
        fail("SEED", params.get("seed"))
    if nonempty(params.get("system")):
        fail("SYSTEM_PROMPT_PRESENT")

    meta = model.get("meta") or {}
    if not isinstance(meta, dict):
        fail("META_TYPE", type(meta).__name__)
    unknown_meta = sorted(set(meta) - SAFE_META_KEYS - ASSOCIATION_KEYS)
    if unknown_meta:
        fail("UNAPPROVED_META_FIELD", unknown_meta[0])
    for key in sorted(ASSOCIATION_KEYS):
        if nonempty(meta.get(key)):
            fail("MODEL_ASSOCIATION", key)
    access_grants = model.get("access_grants")
    if nonempty(access_grants):
        fail("ACCESS_GRANTS_PRESENT")

    safe_meta = {key: meta[key] for key in sorted(SAFE_META_KEYS) if key in meta}
    sanitized_model = {
        "id": EXPECTED_ID,
        "base_model_id": EXPECTED_BASE,
        "name": EXPECTED_NAME,
        "params": {"seed": 42, "temperature": 0},
        "meta": safe_meta,
        "access_grants": [],
        "is_active": True,
    }
    payload = [sanitized_model]
    validate_sanitized_payload(payload)
    canonical = json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    report = {
        "model_export_validation": "PASS",
        "model_count": 1,
        "model_id": EXPECTED_ID,
        "base_model": EXPECTED_BASE,
        "temperature": 0,
        "seed": 42,
        "system_prompt": "ABSENT",
        "model_associations": "ABSENT",
        "access_grants": "EMPTY",
        "sanitized_import_root": "TOP_LEVEL_ARRAY",
        "sanitized_import_model_count": 1,
        "sanitized_import_sha256": digest,
        "open_webui_import_compatibility": "V0.10.2_WORKSPACE_MODELS",
        "stripped_export_fields": sorted(set(model) - set(sanitized_model)),
    }
    atomic_write(args.sanitized_output, canonical)
    atomic_write(
        args.report_output,
        json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n",
    )

    print("MODEL_EXPORT_VALIDATION=PASS")
    print("MODEL_COUNT=1")
    print(f"MODEL_ID={EXPECTED_ID}")
    print(f"BASE_MODEL={EXPECTED_BASE}")
    print("TEMPERATURE=0")
    print("SEED=42")
    print("MODEL_ASSOCIATIONS=ABSENT")
    print("SANITIZED_IMPORT_ROOT=TOP_LEVEL_ARRAY")
    print("SANITIZED_IMPORT_MODEL_COUNT=1")
    print(f"SANITIZED_IMPORT_SHA256={digest}")


if __name__ == "__main__":
    main()
