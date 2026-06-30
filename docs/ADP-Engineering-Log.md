
## 2026-06-29 - ADP v1.1 Progress

Completed:
- Installed official Microsoft Vusial Studio Code
-Resolved Microsoft APT GPG key warnings
- Validated VS Code launch via welcome screen

Next:
- Configure Git Identity
- Configure GitHub SSH
- Initialize ADP repository

## 2026-06-29 — ADP v1.1 Progress

Completed:
- Installed official Microsoft Visual Studio Code
- Resolved Microsoft APT GPG key warning
- Validated VS Code launch
- Configured Git identity
- Generated ED25519 SSH key for GitHub authentication
- Validated internet routing and DNS
- Added SSH public key to GitHub
- Created GitHub repository
- Initialized local ADP repository
- Created initial ADP documentation baseline commit
- Pushed local main branch to origin/main

Next:
- Install Docker
- Validate Docker
- Configure Docker user permissions
- Create Timeshift snapshot after Docker validation

## 2026-06-29 — ADP v1.1 Docker Foundation

Completed:
- Installed Docker Engine from the official Docker repository
- Installed Docker CLI, containerd, Buildx, and Docker Compose plugin
- Validated Docker service status
- Validated Docker runtime with hello-world
- Added user to docker group
- Validated Docker runtime without sudo
- Confirmed docker ps, docker images, and groups validation

Next:
- Create Timeshift snapshot for ADP v1.1 Docker baseline
- Continue with Ollama installation
- Continue with Open WebUI deployment

## ADP v1.1 Ollama Installation Validation

Ollama was installed using the official Linux install command:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

During installation, the Ollama Linux AMD64 ROCm package was downloaded and the installer reported:

- Ollama API is available
- Install complete
- AMD GPU ready

Validation results:

- Ollama version: 0.31.11
- Ollama service status: active (running)
- Docker group membership remained intact
- Docker continued to run without sudo

Control note:

Ollama installation was initiated before the planned Git/Docker baseline confirmation gate. The deviation was contained by stopping before any model pull or Open WebUI deployment and immediately validating Ollama, Docker, Git, and service status before proceeding.

## ADP v1.1 Ollama Small Model Validation

A small Ollama model was pulled and tested after Ollama installation and service validation completed.

Model pulled:

```bash
ollama pull llama3.2:1b
```

Validation commands:

```bash
ollama list
ollama run llama3.2:1b "Reply with exactly this sentence: ADP Ollama model test successful."
git status
```

Validation results:

- Model pull completed successfully
- `ollama list` showed `llama3.2:1b`
- Model responded successfully to the test prompt
- Actual model response: `ADP's Ollama model was successfully tested in various scenarios.`
- Instruction-following note: the response was semantically successful but did not exactly match the requested sentence
- Git working tree remained clean after validation

Gate status:

Ollama small-model pull and runtime validation passed. The environment is ready for the next controlled gate: Open WebUI deployment using Docker.

## ADP v1.1 Security Decision: Open WebUI Localhost Binding

Security decision:

Open WebUI will be deployed using localhost-only port binding for the ADP local lab environment.

Selected Docker port binding:

```bash
-p 127.0.0.1:3000:8080
```

Rejected broader default binding:

```bash
-p 3000:8080
```

Rationale:

The security issue is not the use of host port 3000 itself. The issue is whether Docker publishes the container service on all host interfaces or only on localhost. For the ADP lab, Open WebUI should be reachable from the Linux Mint host browser but should not be exposed to the broader LAN or external network by default.

Security posture:

- Bind Open WebUI to 127.0.0.1 for local-only access
- Do not expose Open WebUI through router, firewall, public IP, or LAN access at this stage
- Do not use host networking unless there is a documented technical requirement
- Do not pull additional models through Open WebUI until the deployment gate is validated
- Keep Ollama running on the host and connect Open WebUI to Ollama using the host gateway approach

Open WebUI Docker-to-host Ollama connection target:

```text
http://host.docker.internal:11434
```

ADP security overlay principle:

ADP will apply secure-by-default engineering decisions while preserving manageability and scalability. Security-impacting decisions will be documented with the selected control, rejected alternative, rationale, validation method, rollback note, and residual risk.

Residual risk:

Localhost binding reduces network exposure but does not replace host security, browser security, account hygiene, patching, image trust, container monitoring, or future authentication hardening.

Gate status:

Security decision documented before Open WebUI deployment.

## ADP v1.1 Security Decision: Ollama Host API Access for Open WebUI

Security decision:

Open WebUI is running in Docker with localhost-only browser access on the host. To allow Open WebUI to use the host-installed Ollama service, Ollama must be reachable from the Docker bridge path used by `host.docker.internal`.

Problem observed:

Open WebUI loaded successfully at:

```text
http://localhost:3000
```

However, the model selector was empty. Container validation showed that `host.docker.internal` resolved to the Docker host gateway, but the container could not reach Ollama on port 11434.

Observed error:

```text
Trying 172.17.0.1:11434...
Connection timed out
Failed to connect to host.docker.internal port 11434
```

Security control decision:

- Keep Open WebUI bound to localhost only: `127.0.0.1:3000:8080`
- Do not expose Open WebUI to the LAN or Internet
- Allow Open WebUI container-to-host access to Ollama only as needed for local lab functionality
- Prefer firewall-scoped Docker bridge access rather than broad application exposure
- Do not use `--network=host`
- Do not change router or external firewall exposure

Planned Ollama configuration:

Set the Ollama systemd service environment so the Ollama API listens on the host for container access:

```text
OLLAMA_HOST=0.0.0.0:11434
```

Compensating control:

Use the host firewall to allow access to TCP 11434 only from the Docker bridge interface path needed by local containers, while avoiding broader external exposure.

Residual risk:

Binding Ollama beyond localhost increases the importance of host firewall enforcement, local account security, container trust, model provenance, and ongoing patching. This configuration remains acceptable for the ADP local lab only because Open WebUI remains localhost-only and no router, LAN, or public exposure is being enabled.

Gate status:

Security decision documented before changing Ollama host API binding.

## ADP v1.1 Open WebUI Deployment Validation

Open WebUI was deployed using Docker and integrated with the host-installed Ollama service.

Deployment security posture:

- Open WebUI browser access is bound to localhost only
- Open WebUI is not exposed to the LAN or Internet
- Open WebUI connects to host-installed Ollama through Docker host gateway resolution
- Ollama host API access is allowed only as needed for local Docker bridge connectivity
- UFW remains active with default incoming deny posture
- No router, public IP, or external firewall exposure was enabled

Validated Open WebUI Docker configuration:

```text
Host browser URL: http://localhost:3000
Open WebUI port binding: 127.0.0.1:3000:8080
Ollama connection URL: http://host.docker.internal:11434
Docker image: ghcr.io/open-webui/open-webui:main
Container name: open-webui
Persistent volume: open-webui:/app/backend/data
Restart policy: always
```

Ollama host API configuration:

```text
OLLAMA_HOST=0.0.0.0:11434
```

Compensating firewall control:

```bash
sudo ufw allow in on docker0 to any port 11434 proto tcp comment 'ADP Open WebUI container to Ollama host API'
```

Validation results:

- Open WebUI loaded successfully at http://localhost:3000
- Local account login succeeded
- Open WebUI initially showed an empty model selector
- Diagnostics confirmed the Open WebUI container could not reach Ollama until the Docker bridge firewall rule was added
- After the UFW docker0 rule, the container successfully reached Ollama through http://host.docker.internal:11434
- `llama3.2:1b` appeared in the Open WebUI model dropdown
- `llama3.2:1b` was selectable in Open WebUI
- End-to-end prompt test succeeded
- WebUI response: `Open WEBUI model connection successful.`

Current controlled configuration note:

Open WebUI is running with environment-controlled Ollama connection settings for auditability and reproducibility. This is acceptable for the ADP v1.1 lab baseline. A future improvement is to move this container configuration into a Docker Compose file so port binding, environment variables, volume mapping, restart policy, and security controls are version-controlled.

Residual risk:

Ollama now listens on 0.0.0.0:11434 to support container-to-host connectivity. This requires continued firewall enforcement, local host security, trusted container images, patching discipline, and no external exposure of Open WebUI or Ollama unless separately approved and documented.

Gate status:

Open WebUI deployment, localhost browser access, Ollama integration, model selection, and end-to-end prompt validation passed.

## ADP v1.1 Timeshift Snapshot: Open WebUI and Ollama Complete

Timeshift snapshot created after successful Open WebUI and Ollama integration.

Snapshot name/comment:

```text
ADP-v1.1-open-webui-ollama-complete
```

Snapshot purpose:

```text
Recovery point after Open WebUI Docker deployment, localhost-only browser binding, Ollama integration, UFW docker0 rule, llama3.2:1b model selection, and successful end-to-end WebUI prompt validation.
```

Validated before snapshot:

- Open WebUI container running
- Open WebUI bound to localhost only on 127.0.0.1:3000
- Open WebUI browser access succeeded at http://localhost:3000
- Local Open WebUI login succeeded
- Ollama service active and running
- Ollama listening on 0.0.0.0:11434 for container-to-host access
- UFW active with default incoming deny posture
- UFW docker0 scoped allow rule enabled for TCP 11434
- Open WebUI container successfully reached Ollama through http://host.docker.internal:11434
- `llama3.2:1b` appeared in the Open WebUI model dropdown
- End-to-end WebUI prompt test succeeded
- Git working tree was clean before snapshot documentation

Gate status:

Timeshift recovery point created and confirmed after ADP v1.1 Open WebUI/Ollama validation.

## 2026-06-30 — ADP v1.1 Docker Compose Baseline for Open WebUI

### Summary
Converted the working Open WebUI `docker run` deployment into a version-controlled Docker Compose baseline.

### Scope
- Added Docker Compose baseline file:
    - `docker/open-webui/docker-compose.yml`
- Preserved the existing external Docker volume:
    - `open-webui`
- Recreated the Open WebUI container using Docker Compose.
- Maintained localhost-only browser exposure:
    - `127.0.0.1:3000:8080`
- Maintained host Ollama integration through:
    - `http://host.docker.internal:11434`

### Validation Results
- Docker Compose configuration validated successfully.
- Open WebUI container started successfully under Compose.
- Open WebUI remained bound to localhost only:
    - `8080/tcp -> 127.0.0.1:3000`
- Open WebUI container was healthy.
- Container environment retained required Ollama settings:
    - `OLLAMA_BASE_URL=http://host.docker.internal:11434`
    - `OLLAMA_BASE_URLS=http://host.docker.internal:11434`
    - `ENABLE_PERSISTENT_CONFIG=False`
- Container-to-Ollama API validation succeeded:
    - Ollama version observed: `0.30.11`
- Model visibility validation succeeded:
    - `llama3.2:1b`
- Browser validation succeeded:
    - Open WebUI loaded at `http://localhost:3000`
    - `llama3.2:1b` was visible and selectable

### Firewall / Security Notes
- Open WebUI browser access remains restricted to localhost.
- Docker Compose created a dedicated bridge network.
- A scoped UFW allow rule was added for the Compose subnet to reach the Ollama host API:
    - `172.18.0.0/16` to TCP `11434`
- Existing `docker0` Ollama rule remains present.
- UFW remains active.
- No LAN or Internet exposure was added for Open WebUI.
- `--network=host` was not used.
- The Open WebUI Docker volume was not deleted.

### Audit Notes
- Hostname observed during this workstream: `smt-ai`
- Ollama version currently observed: `0.30.11`
- Earlier handoff referenced `0.31.11`; current validated runtime value is `0.30.11`.
- Temporary broken Compose files and runtime evidence files were removed before commit to avoid committing operational artifacts or unnecessary personal/runtime details.

### Result
ADP v1.1 Open WebUI Docker Compose baseline is complete, validated, and ready for Git commit and Timeshift snapshot.

## 2026-06-30 — ADP v1.1 Docker Compose Baseline for Open WebUI

### Summary
Converted the working Open WebUI `docker run` deployment into a version-controlled Docker Compose baseline.

### Scope
- Added Docker Compose baseline file:
    - `docker/open-webui/docker-compose.yml`
- Preserved the existing external Docker volume:
    - `open-webui`
- Recreated the Open WebUI container using Docker Compose.
- Maintained localhost-only browser exposure:
    - `127.0.0.1:3000:8080`
- Maintained host Ollama integration through:
    - `http://host.docker.internal:11434`

### Validation Results
- Docker Compose configuration validated successfully.
- Open WebUI container started successfully under Compose.
- Open WebUI remained bound to localhost only:
    - `8080/tcp -> 127.0.0.1:3000`
- Open WebUI container was healthy.
- Container environment retained required Ollama settings:
    - `OLLAMA_BASE_URL=http://host.docker.internal:11434`
    - `OLLAMA_BASE_URLS=http://host.docker.internal:11434`
    - `ENABLE_PERSISTENT_CONFIG=False`
- Container-to-Ollama API validation succeeded:
    - Ollama version observed: `0.30.11`
- Model visibility validation succeeded:
    - `llama3.2:1b`
- Browser validation succeeded:
    - Open WebUI loaded at `http://localhost:3000`
    - `llama3.2:1b` was visible and selectable

### Firewall / Security Notes
- Open WebUI browser access remains restricted to localhost.
- Docker Compose created a dedicated bridge network.
- A scoped UFW allow rule was added for the Compose subnet to reach the Ollama host API:
    - `172.18.0.0/16` to TCP `11434`
- Existing `docker0` Ollama rule remains present.
- UFW remains active.
- No LAN or Internet exposure was added for Open WebUI.
- `--network=host` was not used.
- The Open WebUI Docker volume was not deleted.

### Audit Notes
- Hostname observed during this workstream: `smt-ai`
- Ollama version currently observed: `0.30.11`
- Earlier handoff referenced `0.31.11`; current validated runtime value is `0.30.11`.
- Temporary broken Compose files and runtime evidence files were removed before commit to avoid committing operational artifacts or unnecessary personal/runtime details.

### Result
ADP v1.1 Open WebUI Docker Compose baseline is complete, validated, and ready for Git commit and Timeshift snapshot.
