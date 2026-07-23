#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def fail(control: str, value: Any = "") -> None:
    print("RESTART_STATE_CAPTURE=FAIL")
    print(f"FAILED_CONTROL={control}")
    if value != "":
        print(f"FAILED_VALUE={value}")
    raise SystemExit(1)


def load(path: str) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        fail("JSON_PARSE", f"{Path(path).name}:{type(exc).__name__}")


def one(value: Any, control: str) -> dict[str, Any]:
    if isinstance(value, list):
        if len(value) != 1:
            fail(control, len(value))
        value = value[0]
    if not isinstance(value, dict):
        fail(control, type(value).__name__)
    return value


def canonical_sha(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=("before", "after"))
    parser.add_argument("--compose-json", required=True)
    parser.add_argument("--container-inspect-json", required=True)
    parser.add_argument("--image-inspect-json", required=True)
    parser.add_argument("--database-json", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    compose = one(load(args.compose_json), "COMPOSE_JSON")
    container = one(load(args.container_inspect_json), "CONTAINER_INSPECT_COUNT")
    image = one(load(args.image_inspect_json), "IMAGE_INSPECT_COUNT")
    database = one(load(args.database_json), "DATABASE_JSON")
    service = (compose.get("services") or {}).get("open-webui-validation")
    if not isinstance(service, dict):
        fail("VALIDATION_SERVICE")

    state = container.get("State") or {}
    health = state.get("Health") or {}
    mounts = container.get("Mounts") or []
    networks = (container.get("NetworkSettings") or {}).get("Networks") or {}
    environment = service.get("environment") or {}
    selected_environment = {
        key: environment.get(key)
        for key in (
            "OLLAMA_BASE_URL",
            "OLLAMA_BASE_URLS",
            "ENABLE_PERSISTENT_CONFIG",
            "RAG_TEMPLATE",
            "RAG_EMBEDDING_MODEL",
            "CHUNK_SIZE",
            "CHUNK_OVERLAP",
            "RAG_TEXT_SPLITTER",
            "ENABLE_MARKDOWN_HEADER_TEXT_SPLITTER",
            "RAG_TOP_K",
            "RAG_RELEVANCE_THRESHOLD",
            "ENABLE_RAG_HYBRID_SEARCH",
            "BYPASS_EMBEDDING_AND_RETRIEVAL",
            "RAG_FULL_CONTEXT",
            "ENABLE_WEB_SEARCH",
            "ENABLE_RETRIEVAL_QUERY_GENERATION",
        )
    }

    stable_state = {
        "configured_image": service.get("image"),
        "container_image_id": container.get("Image"),
        "image_id": image.get("Id"),
        "repo_digests": sorted(image.get("RepoDigests") or []),
        "ports": service.get("ports"),
        "network_mode": service.get("network_mode"),
        "mounts": sorted(
            [
                {
                    "type": item.get("Type"),
                    "name": item.get("Name"),
                    "destination": item.get("Destination"),
                }
                for item in mounts
            ],
            key=lambda item: json.dumps(item, sort_keys=True),
        ),
        "networks": sorted(networks.keys()),
        "qualification_environment": selected_environment,
        "database": database,
    }

    record = {
        "record_type": "ADP_V2_4_RESTART_PERSISTENCE_STATE",
        "phase": args.phase,
        "captured_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "runtime_identity": {
            "container_name": str(container.get("Name") or "").lstrip("/"),
            "container_id": container.get("Id"),
            "status": state.get("Status"),
            "running": state.get("Running"),
            "health": health.get("Status"),
            "started_at": state.get("StartedAt"),
            "restart_count": container.get("RestartCount"),
        },
        "stable_state": stable_state,
        "stable_state_sha256": canonical_sha(stable_state),
    }

    output = Path(args.output)
    if output.exists():
        fail("OUTPUT_ALREADY_EXISTS", output)
    output.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(record, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    output.write_text(content, encoding="utf-8", newline="\n")
    print("RESTART_STATE_CAPTURE=PASS")
    print(f"RESTART_PHASE={args.phase.upper()}")
    print(f"STABLE_STATE_SHA256={record['stable_state_sha256']}")


if __name__ == "__main__":
    main()
