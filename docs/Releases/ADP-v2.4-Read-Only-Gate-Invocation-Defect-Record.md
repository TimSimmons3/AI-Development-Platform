# ADP v2.4 Read-Only Gate Invocation Defect Record

## Status

```text
DEFECT_STATUS=CLOSED_WITH_CORRECTED_INVOCATION
REPOSITORY_MUTATION=NONE
RUNTIME_MUTATION=NONE
RECOVERY_REQUIRED=NO
```

## Defect

The first pre-runtime read-only command piped Docker Compose JSON to `scripts/adp24_validate_compose_config.py` through standard input. The validator requires `--compose-json` and `--approved-template` file arguments.

The command continued after the validator error and printed a completion field. That completion field was invalid because the block was not fail-fast and did not bind completion to validator success.

## Correction

The corrected invocation:

1. Writes canonical Compose JSON to a temporary file.
2. Supplies both required arguments.
3. Sets the final gate result only when semantic validation and final Git cleanliness both pass.
4. Removes the temporary file.

The corrected target-host result was:

```text
COMPOSE_SEMANTIC_VALIDATION=PASS
VALIDATION_BINDING=127.0.0.1:3001
VALIDATION_VOLUME=open-webui-validation
PRIMARY_PORT_COLLISION=ABSENT
PRIMARY_INSTANCE_CHANGE=NONE
PRE_RUNTIME_READ_ONLY_GATE=PASS
```

The failed invocation is historical and shall not be reused.
