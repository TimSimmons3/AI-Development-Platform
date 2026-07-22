#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

SERVICE_NAME = "open-webui-validation"
EXPECTED_IMAGE = (
    "ghcr.io/open-webui/open-webui:v0.10.2@"
    "sha256:9fcea9c6e32ab60b0498f3986c6cdf651ddbe61db48d2213a3d28048ddd673d4"
)
EXPECTED_ENV = {
    "OLLAMA_BASE_URL": "http://host.docker.internal:11434",
    "OLLAMA_BASE_URLS": "http://host.docker.internal:11434",
    "ENABLE_PERSISTENT_CONFIG": "False",
    "RAG_EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2",
    "CHUNK_SIZE": "1000",
    "CHUNK_OVERLAP": "100",
    "RAG_TEXT_SPLITTER": "character",
    "ENABLE_MARKDOWN_HEADER_TEXT_SPLITTER": "True",
    "RAG_TOP_K": "3",
    "RAG_RELEVANCE_THRESHOLD": "0",
    "ENABLE_RAG_HYBRID_SEARCH": "False",
    "BYPASS_EMBEDDING_AND_RETRIEVAL": "False",
    "RAG_FULL_CONTEXT": "False",
    "ENABLE_WEB_SEARCH": "False",
    "ENABLE_RETRIEVAL_QUERY_GENERATION": "True",
}
PROHIBITED_ENV = {
    "RAG_EMBEDDING_ENGINE",
    "CONTENT_EXTRACTION_ENGINE",
    "CHUNK_MIN_SIZE_TARGET",
    "RAG_TOP_K_RERANKER",
    "RAG_RERANKING_ENGINE",
    "RAG_RERANKING_MODEL",
    "RAG_HYBRID_BM25_WEIGHT",
}


def fail(control: str, value: object = "") -> None:
    print("COMPOSE_SEMANTIC_VALIDATION=FAIL")
    print(f"FAILED_CONTROL={control}")
    if value != "":
        print(f"FAILED_VALUE={value}")
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail("COMPOSE_JSON_PARSE", type(exc).__name__)
    if not isinstance(value, dict):
        fail("COMPOSE_JSON_ROOT_TYPE", type(value).__name__)
    return value


def normalize_template(value: str) -> str:
    return value.replace("\r\n", "\n").rstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compose-json", required=True)
    parser.add_argument("--approved-template", required=True)
    args = parser.parse_args()

    compose_path = Path(args.compose_json)
    template_path = Path(args.approved_template)
    data = load_json(compose_path)

    services = data.get("services")
    if not isinstance(services, dict):
        fail("SERVICES_TYPE")
    if set(services) != {SERVICE_NAME}:
        fail("SERVICE_SET", sorted(services))
    service = services[SERVICE_NAME]
    if not isinstance(service, dict):
        fail("SERVICE_TYPE")

    if service.get("image") != EXPECTED_IMAGE:
        fail("IMAGE_IDENTITY", service.get("image"))
    if service.get("container_name") != SERVICE_NAME:
        fail("CONTAINER_NAME", service.get("container_name"))
    if service.get("network_mode") != "bridge":
        fail("NETWORK_MODE", service.get("network_mode"))
    if service.get("pull_policy") != "never":
        fail("PULL_POLICY", service.get("pull_policy"))
    if str(service.get("restart")) != "no":
        fail("RESTART_POLICY", service.get("restart"))

    ports = service.get("ports")
    if not isinstance(ports, list) or len(ports) != 1:
        fail("PORT_COUNT", ports)
    port = ports[0]
    if not isinstance(port, dict):
        fail("PORT_CANONICAL_TYPE", type(port).__name__)
    if str(port.get("host_ip")) != "127.0.0.1":
        fail("VALIDATION_BINDING", port.get("host_ip"))
    if str(port.get("published")) != "3001":
        fail("VALIDATION_PUBLISHED_PORT", port.get("published"))
    if int(port.get("target", -1)) != 8080:
        fail("VALIDATION_TARGET_PORT", port.get("target"))
    if str(port.get("protocol", "tcp")) != "tcp":
        fail("VALIDATION_PROTOCOL", port.get("protocol"))
    if any(str(item.get("published")) == "3000" for item in ports if isinstance(item, dict)):
        fail("PRIMARY_PORT_COLLISION")

    mounts = service.get("volumes")
    if not isinstance(mounts, list) or len(mounts) != 1:
        fail("SERVICE_VOLUME_COUNT", mounts)
    mount = mounts[0]
    if not isinstance(mount, dict):
        fail("SERVICE_VOLUME_CANONICAL_TYPE", type(mount).__name__)
    if mount.get("type") != "volume":
        fail("SERVICE_VOLUME_TYPE", mount.get("type"))
    if mount.get("source") != SERVICE_NAME:
        fail("SERVICE_VOLUME_SOURCE", mount.get("source"))
    if mount.get("target") != "/app/backend/data":
        fail("SERVICE_VOLUME_TARGET", mount.get("target"))

    volumes = data.get("volumes")
    if not isinstance(volumes, dict) or set(volumes) != {SERVICE_NAME}:
        fail("TOP_LEVEL_VOLUME_SET", volumes)
    volume = volumes[SERVICE_NAME]
    if not isinstance(volume, dict) or volume.get("name") != SERVICE_NAME:
        fail("TOP_LEVEL_VOLUME_NAME", volume)

    extra_hosts = service.get("extra_hosts", {})
    host_gateway_ok = False
    if isinstance(extra_hosts, dict):
        host_gateway_ok = str(extra_hosts.get("host.docker.internal")) == "host-gateway"
    elif isinstance(extra_hosts, list):
        normalized_hosts = {str(item).replace(":", "=", 1) for item in extra_hosts}
        host_gateway_ok = "host.docker.internal=host-gateway" in normalized_hosts
    else:
        fail("EXTRA_HOSTS_TYPE", type(extra_hosts).__name__)
    if not host_gateway_ok:
        fail("OLLAMA_HOST_GATEWAY", extra_hosts)

    environment = service.get("environment")
    if not isinstance(environment, dict):
        fail("ENVIRONMENT_TYPE")
    for key, expected in EXPECTED_ENV.items():
        if str(environment.get(key)) != expected:
            fail("ENVIRONMENT_VALUE", f"{key}={environment.get(key)}")
    for key in PROHIBITED_ENV:
        if key in environment:
            fail("UNNECESSARY_CONFIG_OVERRIDE", key)

    actual_template = environment.get("RAG_TEMPLATE")
    if not isinstance(actual_template, str):
        fail("RAG_TEMPLATE_TYPE", type(actual_template).__name__)
    approved_template = template_path.read_text(encoding="utf-8")
    if normalize_template(actual_template) != normalize_template(approved_template):
        fail(
            "RAG_TEMPLATE_CONTENT",
            hashlib.sha256(actual_template.encode("utf-8")).hexdigest(),
        )
    if "According to the study" in actual_template or "increases efficiency by 20%" in actual_template:
        fail("RAG_TEMPLATE_CONTAMINATION")

    print("COMPOSE_SEMANTIC_VALIDATION=PASS")
    print("VALIDATION_BINDING=127.0.0.1:3001")
    print("VALIDATION_VOLUME=open-webui-validation")
    print("PRIMARY_PORT_COLLISION=ABSENT")
    print("PRIMARY_INSTANCE_CHANGE=NONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
