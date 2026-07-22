#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


def fail(control, value=""):
    print("RUNTIME_MANIFEST_STATUS=FAIL")
    print(f"FAILED_CONTROL={control}")
    if value != "":
        print(f"FAILED_VALUE={value}")
    raise SystemExit(1)


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        fail("JSON_PARSE", type(exc).__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compose-json", required=True)
    parser.add_argument("--container-inspect-json", required=True)
    parser.add_argument("--image-inspect-json", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    compose = load(args.compose_json)
    container = load(args.container_inspect_json)
    image = load(args.image_inspect_json)
    if isinstance(container, list):
        if len(container) != 1:
            fail("CONTAINER_INSPECT_COUNT", len(container))
        container = container[0]
    if isinstance(image, list):
        if len(image) != 1:
            fail("IMAGE_INSPECT_COUNT", len(image))
        image = image[0]

    service = (compose.get("services") or {}).get("open-webui-validation")
    if not isinstance(service, dict):
        fail("VALIDATION_SERVICE")
    state = container.get("State") or {}
    network = container.get("NetworkSettings") or {}
    mounts = container.get("Mounts") or []
    manifest = {
        "manifest_status": "CAPTURED_NOT_CLASSIFIED",
        "container_name": container.get("Name", "").lstrip("/"),
        "container_id": container.get("Id"),
        "container_image_id": container.get("Image"),
        "configured_image": service.get("image"),
        "image_id": image.get("Id"),
        "repo_digests": image.get("RepoDigests", []),
        "health_status": (state.get("Health") or {}).get("Status"),
        "running": state.get("Running"),
        "ports": service.get("ports"),
        "network_mode": service.get("network_mode"),
        "mounts": [
            {"type": item.get("Type"), "name": item.get("Name"), "destination": item.get("Destination")}
            for item in mounts
        ],
        "networks": sorted((network.get("Networks") or {}).keys()),
        "qualification_environment": service.get("environment"),
    }
    content = json.dumps(manifest, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    output = Path(args.output)
    if output.exists():
        fail("OUTPUT_ALREADY_EXISTS", str(output))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8", newline="\n")
    print("RUNTIME_MANIFEST_STATUS=PASS")
    print("RUNTIME_MANIFEST_SHA256=" + hashlib.sha256(content.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
