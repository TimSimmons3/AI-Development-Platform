# ADP v2.4 Isolated Validation Volume Backup and Rollback Procedure

## 1. Scope

This procedure applies only to Docker volume `open-webui-validation` and container `open-webui-validation`.

The following are prohibited targets:

- `open-webui` container
- `open-webui` volume
- Primary port `3000`
- Primary Compose file
- Ollama data
- UFW configuration

## 2. Backup Point

Create a cold backup after isolated administrator setup and deterministic model import pass, but before Knowledge upload or non-counted retrieval testing.

The backup command stops only the validation container, creates a checksum-verified archive, and restores the validation container to its prior running state.

## 3. Backup Requirements

- Backup directory is outside the Docker volume.
- Archive filename contains a UTC timestamp.
- Archive SHA-256 companion file is created.
- Archive listing validation passes.
- Primary health is checked before and after backup.
- Empty, partial, or overwritten archives are prohibited.

## 4. Restore Boundary

Restore is destructive only to the isolated validation volume. Restore requires:

- Explicit `--restore` action.
- Exact volume name confirmation.
- Matching archive checksum.
- Validation container stopped.
- Primary health confirmed.
- Post-restore isolated health and configuration verification.

Do not restore into the primary volume. Do not use broad Docker cleanup commands. Do not remove unknown volumes.

## 5. Failure Handling

On backup failure, leave the volume unchanged and keep runtime authorization on hold.

On restore failure, stop the validation container, preserve the failed-state evidence, and do not retry until the archive and procedure are reviewed.
