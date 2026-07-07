
## 2026-06-29 - ADP v1.1 Progress

Completed:
- Installed official Microsoft Vusial Studio Code
-Resolved Microsoft APT GPG key warnings
- Validated VS Code launch via welcome screen

Next:
- Configure Git Identity
- Configure GitHub SSH
- Initialize ADP repository

## 2026-06-29 - ADP v1.1 Progress

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

## 2026-06-29 - ADP v1.1 Docker Foundation

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

## 2026-06-30 - ADP v1.1 Docker Compose Baseline for Open WebUI

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

## 2026-06-30 - ADP v1.1 Docker Compose Baseline for Open WebUI

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

## ADP v1.1.1 - Open WebUI Controlled Maintenance Upgrade

Date: 2026-07-01

Status: Complete - implementation and validation passed.

Change summary:
- Upgraded Open WebUI through controlled Docker Compose workflow.
- Pinned Open WebUI image from ghcr.io/open-webui/open-webui:main to ghcr.io/open-webui/open-webui:v0.10.2.
- Preserved localhost-only browser binding.
- Preserved existing open-webui Docker volume.
- Did not use host networking.
- Did not disable UFW.
- Did not pull additional models.

Pre-upgrade controls:
- Confirmed Git working tree was clean before upgrade work.
- Confirmed Open WebUI container was running before upgrade.
- Confirmed Open WebUI was bound to 127.0.0.1:3000->8080/tcp.
- Confirmed target image tag ghcr.io/open-webui/open-webui:v0.10.2 existed.
- Created local Open WebUI Docker volume backup under backups/open-webui/.
- Added backups/ to .gitignore to prevent local recovery archives from being committed.
- Created Timeshift pre-upgrade snapshot:
  ADP-v1.1.1-pre-open-webui-v0.10.2-upgrade

Implementation:
- Updated docker/open-webui/docker-compose.yml to pin:
  ghcr.io/open-webui/open-webui:v0.10.2
- Validated Docker Compose configuration.
- Pulled the pinned Open WebUI image.
- Restarted Open WebUI using Docker Compose.

Post-upgrade validation:
- docker/open-webui/docker-compose.yml references ghcr.io/open-webui/open-webui:v0.10.2.
- Docker Compose config validates successfully.
- open-webui container is running.
- Running image config shows ghcr.io/open-webui/open-webui:v0.10.2.
- Browser port binding remains localhost-only:
  127.0.0.1:3000->8080/tcp
- Open WebUI container can reach host Ollama through:
  http://host.docker.internal:11434
- llama3.2:1b remains visible from the Open WebUI container.
- Browser validation passed:
  Open WebUI loads, login works, llama3.2:1b is visible/selectable, and prompt response works.

Security notes:
- Open WebUI remains localhost-only and is not exposed to LAN or Internet.
- No host networking was introduced.
- UFW posture was not weakened.
- Ollama exposure risk remains tied to firewall posture because Ollama listens on 0.0.0.0:11434. Do not disable UFW or broaden access without documenting and validating the security impact.

Recovery notes:
- Local Open WebUI volume backup exists under backups/open-webui/ and is intentionally ignored by Git.
- Pre-upgrade Timeshift snapshot exists and was visually confirmed.
- Final post-upgrade Timeshift snapshot still required after commit and push.


## ADP v1.2 - Controlled Model Expansion - llama3.2:3b

Date: 2026-07-01

Status: Complete - implementation and validation passed.

Change summary:
- Created ADP model-selection standard.
- Selected llama3.2:3b as the first controlled expansion model.
- Pulled one model only.
- Preserved existing llama3.2:1b baseline.
- Preserved Open WebUI localhost-only binding.
- Preserved Open WebUI image pin at ghcr.io/open-webui/open-webui:v0.10.2.
- Did not expose Open WebUI to LAN or Internet.
- Did not change UFW rules.
- Did not pull additional models.

Host basis:
- Host: smt-ai.
- OS: Linux Mint 22.3.
- CPU: AMD Ryzen 3 4300U with Radeon Graphics.
- CPU capacity: 4 cores / 4 threads.
- RAM: 14 GiB total.
- Disk: approximately 391 GB available at inventory capture.
- GPU: no NVIDIA GPU detected; AMD Radeon RX Vega 6 integrated graphics observed.
- Runtime: Ollama 0.30.11 active.
- Open WebUI: ghcr.io/open-webui/open-webui:v0.10.2.
- Open WebUI binding: 127.0.0.1:3000->8080/tcp.

Model-selection decision:
- Approved first controlled candidate: llama3.2:3b.
- Rationale: low-risk expansion from existing llama3.2:1b baseline, same model family, small model class, suitable for CPU-first validation, and useful for local summarization, prompt rewriting, instruction following, and structured-output testing.
- Deferred larger or unrelated models until llama3.2:3b validation was complete.

Pre-pull validation:
- Git working tree clean.
- Disk capacity healthy.
- Memory capacity acceptable.
- Existing llama3.2:1b baseline present.
- Open WebUI remained pinned to v0.10.2.
- Open WebUI browser binding remained localhost-only.

Implementation:
- Pulled llama3.2:3b using Ollama.
- Did not pull any other model.

CLI validation:
- Confirmed llama3.2:3b appears in ollama list.
- Confirmed llama3.2:1b remains available.
- Initial vague validation prompt produced an overly literal response asking for more context.
- Refined explicit prompts worked as expected.
- CLI validation passed.

Open WebUI validation:
- llama3.2:3b appeared in Open WebUI.
- llama3.2:3b was selectable.
- Basic local-model usefulness prompt returned a reasonable response.
- ADP workflow summary prompt returned a reasonable response.
- Structured JSON prompt returned a reasonable response.
- No browser error observed.
- No Ollama connection error observed.

Post-pull validation:
- llama3.2:1b remains present.
- llama3.2:3b is present.
- Open WebUI remains on ghcr.io/open-webui/open-webui:v0.10.2.
- Open WebUI port binding remains 127.0.0.1:3000->8080/tcp.
- Disk and memory remained healthy after model pull.

Security notes:
- No network exposure was added.
- Open WebUI remains localhost-only.
- No host networking was introduced.
- UFW posture was not weakened.
- Ollama exposure risk remains tied to firewall posture because Ollama listens on 0.0.0.0:11434. Do not disable UFW or broaden access without documenting and validating the security impact.

Model disposition:
- Retain llama3.2:3b as approved ADP controlled expansion model.
- Keep llama3.2:1b as baseline model.
- Do not pull additional models until a new controlled selection cycle is opened.

Rollback:
- To remove llama3.2:3b if needed:
  ollama rm llama3.2:3b
- After rollback, validate:
  ollama list
- Confirm llama3.2:1b remains available.


## ADP v1.3 - Prompt Validation Set and Local Model Evaluation Harness

Date: 2026-07-01
Host: smt-ai
Milestone: ADP v1.3 - Prompt Validation Set / Local Model Evaluation Harness

### Implementation

Created a lightweight local model evaluation harness for ADP. The harness includes:

- Standard prompt validation files under tests/model-validation/prompts/
- Runtime result capture under tests/model-validation/results/
- A local runner script at scripts/run-model-validation.sh
- A local model evaluation standard at docs/ADP-Local-Model-Evaluation-Standard.md
- Git ignore rules to prevent raw runtime model outputs from being committed

The runner executes the standard prompt set against a selected Ollama model through the local Ollama API and writes JSONL runtime evidence files under tests/model-validation/results/.

### Validation

Baseline validation confirmed:

- Git working tree was clean before v1.3 changes
- Ollama was active
- Open WebUI was running on ghcr.io/open-webui/open-webui:v0.10.2
- Open WebUI remained bound to 127.0.0.1:3000->8080/tcp
- Open WebUI container could reach the Ollama API
- UFW was active
- Prior ADP v1.2 Timeshift snapshot was confirmed through the Timeshift GUI

Model harness validation completed:

- llama3.2:1b completed 5 of 5 prompts successfully
- llama3.2:3b completed 5 of 5 prompts successfully
- Raw JSONL result files were created under tests/model-validation/results/
- Git ignore behavior was validated for raw result files

Observed runtime durations:

| Model | Prompt Count | Successes | Total Seconds | Average Seconds |
|---|---:|---:|---:|---:|
| llama3.2:1b | 5 | 5 | 37 | 7.4 |
| llama3.2:3b | 5 | 5 | 96 | 19.2 |

### Output Quality Findings

Both approved models completed the harness successfully, but generated output requires human review before being used as audit-ready ADP documentation.

llama3.2:1b was faster but produced weaker contextual accuracy. It incorrectly described Ollama as a real-time translation platform and drifted away from the ADP local-model context.

llama3.2:3b produced more complete structured responses and better ADP workflow coverage, but it was slower and still showed contextual drift. It also added extra prose around JSON output and produced some generic machine-learning risk content instead of ADP-specific Ollama model-management risks.

### Model Disposition

- llama3.2:1b remains approved as the fast baseline model.
- llama3.2:3b remains approved as the stronger controlled expansion model.
- Neither model output should be treated as authoritative without human review.
- Future prompt-set revisions should include stronger ADP-specific context to reduce generic ML interpretation drift.

### Security and Operational Notes

No additional models were pulled during ADP v1.3.
Open WebUI remains localhost-only.
No Docker host networking was introduced.
UFW remains active.
Raw runtime evidence remains ignored by Git unless intentionally sanitized and approved.

### Rollback Notes

Rollback is low risk. If needed, remove:

- docs/ADP-Local-Model-Evaluation-Standard.md
- scripts/run-model-validation.sh
- tests/model-validation/
- ADP v1.3 .gitignore result-ignore entries

No runtime services, Docker volumes, Ollama models, or firewall rules were changed.

## ADP v1.4 - Evaluation Reporting / Prompt Hardening / Resource-Aware Model Comparison

Date: 2026-07-02

Status: Complete; committed and pushed. Final Timeshift snapshot required for release closeout.
Final release commit: 1f38af2 Add ADP v1.4 evaluation reporting and prompt hardening
Final snapshot target: ADP-v1.4-evaluation-reporting-prompt-hardening-complete

### Scope

ADP v1.4 improves the local model evaluation capability created in ADP v1.3 by adding stronger prompt context, evaluation reporting, and model comparison structure.

This milestone does not change the approved model baseline or Open WebUI deployment posture.

### Baseline

Latest completed release before this milestone:

- ADP v1.3
- Commit: 281079c Add ADP local model evaluation harness

Approved models remain:

- llama3.2:1b
- llama3.2:3b

Open WebUI baseline remains:

- Image: ghcr.io/open-webui/open-webui:v0.10.2
- Binding: 127.0.0.1:3000->8080/tcp
- Scope: localhost-only

Observed Ollama version during post-Docker-update baseline validation:

- 0.30.11

### Changes Implemented

Prompt validation set hardened:

- tests/model-validation/prompts/01-basic-responsiveness.txt
- tests/model-validation/prompts/02-adp-workflow-summary.txt
- tests/model-validation/prompts/03-structured-json-output.txt
- tests/model-validation/prompts/04-risk-mitigation.txt
- tests/model-validation/prompts/05-engineering-log-draft.txt

Documentation and reporting artifacts added:

- docs/ADP-v1.4-Evaluation-Reporting-and-Prompt-Hardening-Plan.md
- docs/ADP-v1.4-Evaluation-Report.md
- tests/model-validation/results/ADP-v1.4-Model-Comparison-Summary-Template.md

Git ignore behavior updated:

- Raw runtime JSONL files under tests/model-validation/results/ remain ignored.
- Markdown documentation templates under tests/model-validation/results/ are trackable.

### Validation Performed

The v1.4 hardened validation harness was executed against both approved models.

llama3.2:1b:

- Prompts executed: 5
- Successes: 5
- Failures: 0
- Durations: 10, 18, 12, 16, 12 seconds
- Total duration: 68 seconds
- Average duration: 13.6 seconds
- Result file: tests/model-validation/results/20260702-200115-llama3.2_1b.jsonl

llama3.2:3b:

- Prompts executed: 5
- Successes: 5
- Failures: 0
- Durations: 17, 35, 13, 29, 18 seconds
- Total duration: 112 seconds
- Average duration: 22.4 seconds
- Result file: tests/model-validation/results/20260702-200458-llama3.2_3b.jsonl

### Results Summary

Both approved models completed all hardened prompts successfully.

- llama3.2:1b remains approved as the fast baseline model.
- llama3.2:3b remains approved as the stronger controlled expansion model.
- No model status change is required.

### Quality Findings

The hardened prompt set reduced contextual drift by adding explicit ADP, Ollama, Open WebUI, workflow, and human-review context.

The evaluation reporting artifacts provide a more consistent way to summarize model behavior, runtime results, and review findings.

### Security Posture

Security posture remains unchanged:

- Do not expose Open WebUI to LAN or Internet.
- Do not use --network=host.
- Do not delete the open-webui Docker volume.
- Do not disable UFW.
- Open WebUI remains localhost-only.
- Ollama listening on *:11434 remains a documented residual risk controlled by firewall posture.

### Human Review Notes

The validation harness confirms technical execution and basic response behavior only.

Model outputs are not audit-ready without human review.

Model outputs must not be used for security, governance, compliance, financial, legal, or operational decisions without human review.

### Residual Risks

- Local model outputs may be incomplete, inaccurate, or contextually weak.
- Structured JSON output may still require validation before downstream use.
- Runtime duration may vary based on host load.
- Ollama listening on *:11434 remains a documented residual risk controlled by firewall posture.

### Next Steps

- Review Git diff.
- Commit and push v1.4 artifacts after validation.
- Confirm local main and origin/main match.
- Take final Timeshift snapshot after release.

## ADP v1.5 Runner Quality and Evaluation Automation Hardening

Status: Implementation and validation in progress

Date: 2026-07-03

Scope:

- Added v1.5 plan documentation.
- Added evaluation workflow guidance.
- Added sanitized validation findings documentation.
- Added prompt-level scoring rubric.
- Added model-validation summary generator.
- Added JSON-only prompt output validator.
- Added v1.5 functional-validation wrapper.
- Updated .gitignore so timestamped generated summary files remain local runtime artifacts.

Validation performed:

- Candidate files passed non-ASCII validation.
- Shell scripts passed bash syntax validation.
- Embedded Python in shell scripts passed py_compile validation.
- Summary generation succeeded for llama3.2:1b and llama3.2:3b v1.4 result files.
- JSON validation passed for llama3.2:1b structured JSON output.
- Known-bad llama3.2:3b structured JSON output was rejected as an expected negative test.
- Functional-validation wrapper completed successfully and relabeled expected negative-test detail clearly.

Quality finding:

- Runner execution success is not equivalent to prompt-output quality success.
- The llama3.2:3b structured JSON result from v1.4 returned a response but failed JSON validity because it was missing the final closing object brace.
- This finding validates the need for separate format-compliance checks in v1.5.

Process correction:

- Executable scripts must pass a fail-fast QA gate before execution.
- Required checks include non-ASCII scan, bash -n, embedded Python extraction where applicable, and python3 -m py_compile.
- Syntax validation alone is not sufficient; content-completeness checks are required for validation wrappers.

Security posture:

- No Docker changes were made.
- No Open WebUI exposure changes were made.
- Open WebUI remains localhost-only.
- No UFW changes were made.
- No volumes were deleted or recreated.
- No new models were added.

## ADP v1.5 Release Closeout

Status: Complete

Date: 2026-07-03

Release commit:

- 6bfe2d0 Add ADP v1.5 evaluation automation hardening

Post-push validation:

- Local HEAD matched origin/main at 6bfe2d0.
- Functional validation wrapper completed successfully.
- Summary generation succeeded for llama3.2:1b and llama3.2:3b.
- JSON validation passed for llama3.2:1b structured JSON output.
- Known-bad llama3.2:3b structured JSON output was rejected as an expected negative test.
- Git status was clean after post-push validation.

Release outcome:

- ADP v1.5 runner quality, result parsing, JSON validation, scoring rubric, workflow guide, and functional-validation wrapper are complete.
- Raw JSONL files remain local runtime evidence.
- Timestamped generated Markdown summaries remain ignored runtime artifacts.
- Formal v1.5 documentation and validation findings are committed and pushed.

Security posture:

- No Docker changes were made.
- No Open WebUI exposure changes were made.
- Open WebUI remains localhost-only.
- No UFW changes were made.
- No Docker volumes were deleted or recreated.
- No new models were added.

## ADP v1.6 Operational Hardening and Recovery Validation
Status: Implementation and validation in progress
Date: 2026-07-06
Host: smt-ai
Branch: main
Current HEAD: 44dc87b

Scope completed:
- Added ADP command and content quality gate.
- Added ADP v1.6 operational hardening and recovery validation plan.
- Added ADP operational runbook.
- Added ADP recovery validation checklist.
- Added ADP snapshot and rollback procedure.
- Remediated historical non-ASCII formatting in the engineering log.

Commits completed:
- 36d6fad Add ADP command and content quality gate
- 1f96910 Add ADP v1.6 operational hardening plan
- a83e399 Add ADP operational runbook
- 1c49cbb Add ADP recovery validation checklist
- db4b903 Add ADP snapshot and rollback procedure
- 44dc87b Normalize engineering log ASCII formatting

Validation performed:
- Baseline validation confirmed branch main and clean Git state before controlled work.
- Temporary candidates were created under /tmp before promotion.
- Candidate and promoted files passed ASCII checks.
- Candidate and promoted files passed line count and heading checks where applicable.
- Staged files passed git diff --check before commit.
- Each committed artifact was pushed to origin/main.
- Local HEAD matched origin/main after each push.

Security posture:
- No Open WebUI exposure changes were made.
- Open WebUI remains localhost-only.
- Open WebUI remains pinned to ghcr.io/open-webui/open-webui:v0.10.2.
- Open WebUI remains bound to 127.0.0.1:3000->8080/tcp.
- No Docker host networking was introduced.
- No Open WebUI Docker volume was deleted.
- No UFW weakening was performed.
- No new Ollama models were added.

Remaining v1.6 work:
- Commit and push this engineering log entry after validation.
- Run final v1.6 documentation QA.
- Commit and push final v1.6 documentation updates.
- Confirm final Timeshift snapshot: ADP-v1.6-operational-hardening-recovery-validation-complete.

## ADP v1.6 Release Closeout
Status: Complete
Date: 2026-07-06
Host: smt-ai
Branch: main
Final QA baseline HEAD: 460b22f

Release artifacts completed:
- docs/ADP-Command-and-Content-Quality-Gate.md
- docs/ADP-v1.6-Operational-Hardening-Recovery-Validation-Plan.md
- docs/ADP-Operational-Runbook.md
- docs/ADP-Recovery-Validation-Checklist.md
- docs/ADP-Snapshot-and-Rollback-Procedure.md
- docs/ADP-Engineering-Log.md

Release commits completed before closeout:
- 36d6fad Add ADP command and content quality gate
- 1f96910 Add ADP v1.6 operational hardening plan
- a83e399 Add ADP operational runbook
- 1c49cbb Add ADP recovery validation checklist
- db4b903 Add ADP snapshot and rollback procedure
- 44dc87b Normalize engineering log ASCII formatting
- 460b22f Document ADP v1.6 operational hardening progress

Final validation performed:
- Git status was clean before final snapshot.
- Local HEAD matched origin/main at 460b22f before final snapshot.
- Required v1.6 files were present.
- Required v1.6 files were ASCII-clean.
- Required v1.6 files had no trailing whitespace.
- Required v1.6 content checks passed.
- Open WebUI remained healthy.
- Open WebUI remained localhost-only at 127.0.0.1:3000->8080/tcp.
- Open WebUI remained pinned to ghcr.io/open-webui/open-webui:v0.10.2.
- Ollama responded with version 0.30.11.
- Approved models llama3.2:1b and llama3.2:3b were present.

Final snapshot:
- ADP-v1.6-operational-hardening-recovery-validation-complete
- Snapshot creation was confirmed in the Timeshift GUI.

Security posture:
- No Open WebUI exposure changes were made.
- No Docker host networking was introduced.
- No Open WebUI Docker volume was deleted.
- No UFW weakening was performed.
- No new Ollama models were added.

Release outcome:
- ADP v1.6 operational hardening and recovery validation is complete.
- ADP v1.6 is documented, committed, pushed, snapshotted, and recoverable.

## ADP v1.7 Prompt Governance and Model Policy Progress
Status: In progress
Date: 2026-07-07
Host: smt-ai
Branch: main
Baseline before v1.7 work: a22205b
Current commit after initial v1.7 governance artifacts: bfc6ee4
Work completed:
- Created ADP v1.7 prompt governance, model promotion, and evaluation policy plan.
- Created ADP prompt governance standard.
- Created ADP model promotion and evaluation policy.
Artifacts added:
- docs/ADP-v1.7-Prompt-Governance-Model-Promotion-Evaluation-Policy-Plan.md
- docs/ADP-Prompt-Governance-Standard.md
- docs/ADP-Model-Promotion-and-Evaluation-Policy.md
Commit completed:
- bfc6ee4 Add ADP v1.7 prompt governance and model policy
Validation performed:
- Clean v1.6 baseline was validated before v1.7 file creation.
- Required v1.6 artifacts were present and ASCII-clean.
- Open WebUI remained healthy and localhost-only.
- Ollama reported version 0.30.11.
- Approved models llama3.2:1b and llama3.2:3b were present.
- v1.7 files were created as temporary candidates before promotion.
- Candidate files passed ASCII and trailing whitespace checks.
- Promoted files passed ASCII and trailing whitespace checks.
- Content completeness checks passed for prompt governance, model policy, evidence, approval, demotion, and security controls.
- Staged diff check passed before commit.
- Commit was pushed to origin/main.
- Local HEAD matched origin/main at bfc6ee4 after push.
Security posture:
- No Open WebUI exposure changes were made.
- Open WebUI remains localhost-only.
- Open WebUI remains pinned to ghcr.io/open-webui/open-webui:v0.10.2.
- Open WebUI remains bound to 127.0.0.1:3000->8080/tcp.
- No Docker host networking was introduced.
- No Open WebUI Docker volume was deleted.
- No UFW weakening was performed.
- No new Ollama models were added.
Remaining v1.7 work:
- Promote this engineering log update after validation.
- Commit and push engineering log update.
- Run final v1.7 documentation QA.
- Document final v1.7 closeout.
- Create final Timeshift snapshot after final validation.
