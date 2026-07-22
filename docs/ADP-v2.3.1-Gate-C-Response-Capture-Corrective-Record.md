# ADP v2.3.1 Gate C Response Capture Corrective Record

## Status

- Current counted Run 1: `VOIDED_NOT_COUNTED`
- Reason: The approved response-capture procedure relied on an unbounded interactive terminal command and produced ambiguous operator state.
- Counted runs completed: 0
- Required action: Promote this correction, reset, recreate the WebUI state, and restart Run 1.

## Corrective Control

The canonical runtime script now provides:

```bash
bash scripts/adp231_gate_c_fresh_runtime.sh capture-response N
```

The operator copies the Open WebUI response, runs the command, reviews the preview, and confirms.

The command does not silently wait for pasted text.

## Superseded Method

Do not use:

```text
cat > response.txt
```

Do not attempt to repair or overwrite the current Run 1 response file.

## Entry Requirement

Restart only after:

- Corrective installer PASS
- Repository synchronization PASS
- Fresh reset PASS
- Open WebUI cleanup and recreation
- Setup verification PASS
