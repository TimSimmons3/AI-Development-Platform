#!/usr/bin/env bash
set -u
export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1
ROOT="${1:-}"
APP="${2:-}"
PKG="${3:-}"
STATUS=PASS
fail(){ printf 'FAILED_CONTROL=%s\n' "$1"; STATUS=FAIL; }
if test -z "$ROOT" || test -z "$APP" || test -z "$PKG"; then printf 'ADP24_V7_QUALITY_GATE=FAIL\nFAILED_CONTROL=ARGUMENTS_REQUIRED\n'; exit 1; fi
if ! git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then printf 'ADP24_V7_QUALITY_GATE=FAIL\nFAILED_CONTROL=REPOSITORY_ROOT\n'; exit 1; fi
EXPECTED_PARENT="b934c7bd84bfbc35563f3681712c4d5bd8478196"
if test "${ADP_V7_TEST_MODE:-0}" = "1"; then EXPECTED_PARENT="${ADP_V7_TEST_PARENT:-$EXPECTED_PARENT}"; fi
if test "$(git -C "$ROOT" rev-parse HEAD)" != "$EXPECTED_PARENT"; then fail DESIGN_PARENT; fi
if find "$ROOT" -type d -name __pycache__ -print -quit | grep -q .; then fail PYTHON_CACHE; fi
python3 - "$ROOT" "$APP" <<'PYQ' || STATUS=FAIL
import ast,hashlib,json,os,pathlib,stat,sys
root=pathlib.Path(sys.argv[1]); app=json.loads(pathlib.Path(sys.argv[2]).read_text(encoding='ascii')); failures=[]
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for x in app['paths']:
 p=root/x['path']
 if not p.is_file(): failures.append('MISSING:'+x['path']); continue
 if h(p)!=x['sha256']: failures.append('HASH:'+x['path'])
 mode='100'+oct(stat.S_IMODE(p.stat().st_mode))[2:].zfill(3)
 if mode!=x['mode']: failures.append('MODE:'+x['path']+':'+mode)
 if p.suffix=='.json':
  try: json.loads(p.read_text(encoding='ascii'))
  except Exception as e: failures.append('JSON:'+x['path']+':'+type(e).__name__)
 if p.suffix=='.py':
  try: ast.parse(p.read_text(encoding='ascii'),filename=str(p))
  except Exception as e: failures.append('PYTHON:'+x['path']+':'+type(e).__name__)
 if not p.read_bytes().endswith(b'\n'): failures.append('FINAL_NEWLINE:'+x['path'])
if failures:
 for f in failures: print('FAILED_CONTROL='+f)
 raise SystemExit(1)
print('C1_APPLICATION_MANIFEST_VALIDATION=PASS')
print('C1_PATH_COUNT='+str(len(app['paths'])))
PYQ
while IFS= read -r f; do bash -n "$f" || fail "BASH_SYNTAX:$f"; done < <(find "$ROOT/scripts" -maxdepth 1 -type f -name '*v7*.sh' -print)
TEMP="$(mktemp -d)"; trap 'rm -rf "$TEMP"' EXIT
python3 "$ROOT/scripts/adp24_validate_counted_rag_bindings_v7.py" --repository-root "$ROOT" --contract "$ROOT/artifacts/Configuration/ADP-v2.4/counted-rag-qualification-design-candidate-v7.json" --binding-manifest "$ROOT/artifacts/Configuration/ADP-v2.4/counted-rag-governing-bindings-v7.json" --context DESIGN --output "$TEMP/design-binding.json" --application-manifest "$APP" || STATUS=FAIL
python3 "$ROOT/scripts/adp24_counted_rag_validator_candidate_v7_self_test.py" --repository-root "$ROOT" --binding-report "$TEMP/design-binding.json" || STATUS=FAIL
python3 "$ROOT/scripts/adp24_candidate_v7_trust_chain_synthetic_test.py" --repository-root "$ROOT" --package-v12 "$PKG" || STATUS=FAIL
for marker in 'C1_COMMIT_AUTHORIZATION=HOLD' 'COUNTED_EXECUTION_AUTHORIZATION=HOLD'; do grep -R -F "$marker" "$ROOT/docs" >/dev/null || fail "DOCUMENT_MARKER:$marker"; done
if test "$STATUS" = PASS; then
 printf 'ADP24_V7_QUALITY_GATE=PASS\n'
 printf 'READINESS_PASS_1_SCOPE_BASELINE=PASS\n'
 printf 'READINESS_PASS_2_TECHNICAL_STRUCTURE=PASS\n'
 printf 'READINESS_PASS_3_SEMANTIC_TRACEABILITY=PASS\n'
 printf 'READINESS_PASS_4_FAILURE_RECOVERY=PASS\n'
 printf 'READINESS_PASS_5_OPERATIONAL_RESIDUAL_RISK=PASS\n'
 printf 'READINESS_PASS_5_SECURITY_EXPOSURE=PASS\n'
 printf 'FIVE_PASS_READINESS_STATUS=PASS\n'
 printf 'C1_COMMIT_AUTHORIZATION=HOLD_PENDING_INDEPENDENT_FULL_DIFF_REVIEW\n'
 printf 'RUNTIME_MUTATION=NONE\nCOUNTED_EXECUTION_AUTHORIZATION=HOLD\n'
 exit 0
fi
printf 'ADP24_V7_QUALITY_GATE=FAIL\nPROCEED_AUTHORIZATION=HOLD\nRUNTIME_MUTATION=NONE\nCOUNTED_EXECUTION_AUTHORIZATION=HOLD\n'; exit 1
