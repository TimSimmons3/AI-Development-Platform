
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
