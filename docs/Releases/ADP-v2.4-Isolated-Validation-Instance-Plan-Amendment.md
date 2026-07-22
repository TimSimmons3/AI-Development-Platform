# ADP v2.4 Isolated Validation Instance Plan Amendment

## 1. Status

```text
AMENDMENT_STATUS=APPROVED
SUPERSEDES=PRIMARY_INSTANCE_GLOBAL_OVERRIDE_APPROACH
PRIMARY_INSTANCE_CHANGE=PROHIBITED
RUNTIME_AUTHORIZATION=HOLD
COUNTED_EXECUTION_AUTHORIZATION=HOLD
AUTHORITATIVE_STARTING_COMMIT=c9de7d74e4b3dd31887567820052220d61954d6f
```

## 2. Reason for Amendment

The confirmed RAG-template persistence defect requires remediation, but applying a strict qualification template globally to the primary Open WebUI instance would constrain future general-purpose RAG behavior and increase upgrade coupling.

The prior primary-instance implementation approach is therefore superseded before implementation.

## 3. Approved Architecture

ADP v2.4 shall use a separate qualification instance:

- Container: `open-webui-validation`
- Port: `127.0.0.1:3001`
- Volume: `open-webui-validation`
- Image: `ghcr.io/open-webui/open-webui:v0.10.2`
- Image digest: `sha256:9fcea9c6e32ab60b0498f3986c6cdf651ddbe61db48d2213a3d28048ddd673d4`
- Network mode: Docker bridge, not host networking
- Ollama endpoint: `http://host.docker.internal:11434`
- Primary Open WebUI container, volume, port, and Compose file remain unchanged

The validation instance is intentionally bounded to qualification and regression testing.

## 4. Risk Controls

- Use `pull_policy: never` to prevent an unapproved image pull.
- Bind only to loopback.
- Use a separate volume.
- Do not modify UFW.
- Do not modify the Ollama service.
- Do not use host networking.
- Do not import a one-model artifact with a model synchronization operation.
- Do not treat database-derived model discovery evidence as a native import artifact.
- Stop before runtime unless a verified volume backup, rollback procedure, native model export, and runtime packet are approved.

## 5. Repository-Only Authorization

This amendment authorizes only creation and static validation of the isolated-instance repository artifacts.

It does not authorize:

- `docker compose up`
- Container creation, recreation, start, stop, or restart
- Docker-volume creation or modification
- Open WebUI database changes
- Native model import
- Knowledge collection creation
- Firewall changes
- Ollama changes
- Counted execution
