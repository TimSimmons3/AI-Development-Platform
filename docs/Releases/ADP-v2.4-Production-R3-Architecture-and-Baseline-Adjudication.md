# ADP v2.4 Production R3 Architecture and Baseline Adjudication

## Decision

```text
ADJUDICATED_UTC=2026-08-05T11:59:57Z
HOST_CLIENT_OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_SERVICE_SOCKET_BINDING=0.0.0.0:11434
OPENWEBUI_CONTAINER_OLLAMA_BASE_URL=http://host.docker.internal:11434
UFW_DEFAULT_INCOMING=DENY
REMOTE_LAN_PORT_11434_TEST=BLOCKED_TIMEOUT
ARCHITECTURE_STATUS=ACCEPTED_WITH_DOCUMENTED_COMPENSATING_CONTROL
```

The earlier handoff conflated the host client's loopback base URL with the Ollama service socket binding. The Production R3 host operator can continue to use `http://127.0.0.1:11434`, while the service binds to `0.0.0.0:11434` so the Open WebUI bridge-network container can reach `host.docker.internal:11434`.

The broader socket binding is an intentional ADP architecture decision documented since v1.1. UFW remains active with default incoming deny and scoped Docker access rules. A remote test from `Timothys-MacBook-Pro-2.local` reached the host by ICMP but timed out on TCP 11434 with HTTP code `000`, so LAN exposure was not observed.

## Residual risk

The control depends on continued firewall enforcement. A future hardening workstream may evaluate a narrower bridge-specific binding or container-network redesign. No binding, firewall, Docker, Open WebUI, or Ollama change is part of this closeout.
