from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.qualification import run_final_assurance_state_oracle as oracle_runner

RUNNER = ROOT / "tests/qualification/run_final_assurance_state_oracle.py"


def run_shard(index: int, count: int, cache_path: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [
            sys.executable,
            "-B",
            str(RUNNER),
            "--probe-shard-index",
            str(index),
            "--probe-shard-count",
            str(count),
            "--probe-cache-out",
            str(cache_path),
        ],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stderr


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shards", type=int, default=16)
    parser.add_argument("--parallel", type=int, default=8)
    parser.add_argument("--cache-dir")
    parser.add_argument("--external-evidence")
    parser.add_argument("--output")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if args.shards <= 0 or args.parallel <= 0:
        result = {"record_type": "ADP_FINAL_ASSURANCE_STATE_ORACLE_QUALIFICATION_R2", "schema_version": "2.0", "status": "FAIL", "fatal_error": "shards and parallel must be positive"}
    else:
        temp = None
        try:
            if args.cache_dir:
                cache_dir = Path(args.cache_dir)
                cache_dir.mkdir(parents=True, exist_ok=True)
            else:
                temp = tempfile.TemporaryDirectory(prefix="adp-final-assurance-probes-")
                cache_dir = Path(temp.name)
            cache_paths = [cache_dir / f"probe-shard-{i:02d}-of-{args.shards:02d}.json" for i in range(args.shards)]
            failures: list[dict[str, object]] = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(args.parallel, args.shards)) as pool:
                futures = {pool.submit(run_shard, i, args.shards, cache_paths[i]): i for i in range(args.shards)}
                for future in concurrent.futures.as_completed(futures):
                    index = futures[future]
                    rc, stderr = future.result()
                    if rc != 0:
                        failures.append({"shard_index": index, "returncode": rc, "stderr": stderr[-4000:]})
            if failures:
                result = {
                    "record_type": "ADP_FINAL_ASSURANCE_STATE_ORACLE_QUALIFICATION_R2",
                    "schema_version": "2.0",
                    "status": "FAIL",
                    "fatal_error": "one or more probe shards failed",
                    "shard_failures": sorted(failures, key=lambda x: int(x["shard_index"])),
                }
            else:
                result = oracle_runner.qualify(
                    Path(args.external_evidence) if args.external_evidence else None,
                    workers=1,
                    probe_cache_paths=cache_paths,
                )
                result["sharded_execution"] = {
                    "shard_count": args.shards,
                    "parallelism": min(args.parallel, args.shards),
                    "cache_dir_preserved": bool(args.cache_dir),
                }
        except Exception as exc:
            result = {"record_type": "ADP_FINAL_ASSURANCE_STATE_ORACLE_QUALIFICATION_R2", "schema_version": "2.0", "status": "FAIL", "fatal_error": f"{type(exc).__name__}: {exc}"}
        finally:
            if temp is not None:
                temp.cleanup()

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result.get("status") == "PASS" else 2 if result.get("status") == "HOLD" else 1


if __name__ == "__main__":
    raise SystemExit(main())
