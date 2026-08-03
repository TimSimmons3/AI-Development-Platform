# ADP v2.4 Candidate-v7 Security Containment Record

```text
OLD_JWT_INVALIDATED=PASS
HOST_SECRET_PATH=~/.config/adp/open-webui/.webui_secret_key
CONTAINER_SECRET_PATH=/app/backend/.webui_secret_key
SECRET_MOUNT_MODE=READ_ONLY
OPENWEBUI_IMAGE=ghcr.io/open-webui/open-webui:v0.10.2
OPENWEBUI_BINDING=127.0.0.1:3000
REDIS_CONFIGURED=FALSE
ACTIVE_OAUTH_SESSIONS=0
ACTIVE_TOOLS=0
ACTIVE_FUNCTIONS=0
PLAINTEXT_TOKEN_MATCHES=0
```

The secret value and its hash are retained only in restricted transaction evidence and are not recorded in Git.
