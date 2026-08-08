#!/usr/bin/env python3
"""Read-only, fail-closed Git commit-tree change contract for assurance validators."""
from __future__ import annotations

from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import NamedTuple

SHA_RE = re.compile(r"^[0-9a-f]{40,64}$")
SUPPORTED_STATUSES = frozenset({"A", "M", "D", "T"})
SUPPORTED_MODES = frozenset({"000000", "100644", "100755", "120000", "160000"})
REGULAR_MODES = frozenset({"100644", "100755"})


class GitContractError(RuntimeError):
    """Fail-closed Git contract violation."""


class GitDelta(NamedTuple):
    status: str
    path: str
    old_mode: str
    new_mode: str
    old_oid: str
    new_oid: str

    @property
    def current_exists(self) -> bool:
        return self.status != "D"

    @property
    def deleted(self) -> bool:
        return self.status == "D"

    @property
    def type_changed(self) -> bool:
        return self.status == "T"


class GitTreeEntry(NamedTuple):
    path: str
    mode: str
    object_type: str
    oid: str

    @property
    def regular_blob(self) -> bool:
        return self.object_type == "blob" and self.mode in REGULAR_MODES


def _run_git_bytes(repo_root: Path, args: list[str]) -> bytes:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=repo_root, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitContractError(f"git {' '.join(args)} execution failed: {type(exc).__name__}: {exc}") from exc
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", "replace").strip()
        raise GitContractError(f"git {' '.join(args)} failed: {stderr}")
    return proc.stdout


def _decode_repo_path(raw: bytes) -> str:
    try:
        value = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise GitContractError("Git path is not valid UTF-8") from exc
    if not value:
        raise GitContractError("Git path is empty")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise GitContractError(f"Git path contains prohibited control character: {value!r}")
    pure = PurePosixPath(value)
    if pure.is_absolute() or "." in pure.parts or ".." in pure.parts:
        raise GitContractError(f"Git path is unsafe: {value!r}")
    return pure.as_posix()


def parse_raw_diff_z(data: bytes) -> list[GitDelta]:
    if not data:
        return []
    fields = data.split(b"\0")
    if fields[-1] != b"":
        raise GitContractError("git diff --raw -z output is not NUL terminated")
    fields.pop()
    if len(fields) % 2:
        raise GitContractError("git diff --raw -z output has incomplete record")
    result: list[GitDelta] = []
    for idx in range(0, len(fields), 2):
        header_raw, path_raw = fields[idx], fields[idx + 1]
        try:
            header = header_raw.decode("ascii", "strict")
        except UnicodeDecodeError as exc:
            raise GitContractError("git raw-diff header is not ASCII") from exc
        parts = header.split()
        if len(parts) != 5 or not parts[0].startswith(":"):
            raise GitContractError(f"malformed git raw-diff header: {header!r}")
        old_mode = parts[0][1:]
        new_mode, old_oid, new_oid, status = parts[1], parts[2], parts[3], parts[4]
        if status not in SUPPORTED_STATUSES:
            raise GitContractError(f"unsupported Git change status {status!r}; expected A/M/D/T under --no-renames")
        if old_mode not in SUPPORTED_MODES or new_mode not in SUPPORTED_MODES:
            raise GitContractError(f"unsupported Git object mode transition {old_mode}->{new_mode}")
        if not SHA_RE.fullmatch(old_oid) or not SHA_RE.fullmatch(new_oid):
            raise GitContractError("raw-diff object identity is not full hexadecimal object ID")
        if status == "A" and old_mode != "000000":
            raise GitContractError("A record must have old mode 000000")
        if status == "D" and new_mode != "000000":
            raise GitContractError("D record must have new mode 000000")
        if status == "T" and (old_mode == "000000" or new_mode == "000000" or old_mode == new_mode):
            raise GitContractError("T record must change between two existing different object modes")
        path = _decode_repo_path(path_raw)
        result.append(GitDelta(status, path, old_mode, new_mode, old_oid, new_oid))
    paths = [item.path for item in result]
    if len(paths) != len(set(paths)):
        raise GitContractError("git raw diff contains duplicate paths under --no-renames")
    return result



def resolve_commit(repo_root: Path, ref: str) -> str:
    raw = _run_git_bytes(repo_root, ["rev-parse", "--verify", f"{ref}^{{commit}}"] )
    value = raw.decode("ascii", "strict").strip()
    if not SHA_RE.fullmatch(value):
        raise GitContractError(f"Git ref did not resolve to a full commit ID: {ref}")
    return value


def head_commit_and_tree(repo_root: Path) -> tuple[str, str]:
    head = resolve_commit(repo_root, "HEAD")
    raw = _run_git_bytes(repo_root, ["rev-parse", "--verify", "HEAD^{tree}"])
    tree = raw.decode("ascii", "strict").strip()
    if not SHA_RE.fullmatch(tree):
        raise GitContractError("HEAD tree identity is invalid")
    return head, tree

def commit_deltas(repo_root: Path, base_ref: str) -> tuple[str, list[GitDelta]]:
    merge_base = _run_git_bytes(repo_root, ["merge-base", base_ref, "HEAD"]).decode("ascii", "strict").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", merge_base):
        raise GitContractError("git merge-base did not return a full object ID")
    raw = _run_git_bytes(
        repo_root,
        ["diff", "--raw", "-z", "--no-renames", "--abbrev=64", f"{merge_base}...HEAD"],
    )
    return merge_base, parse_raw_diff_z(raw)


def head_tree_entry(repo_root: Path, path: str) -> GitTreeEntry | None:
    safe_path = _decode_repo_path(path.encode("utf-8"))
    raw = _run_git_bytes(repo_root, ["ls-tree", "-z", "--full-tree", "HEAD", "--", safe_path])
    if not raw:
        return None
    records = raw.split(b"\0")
    if records[-1] != b"":
        raise GitContractError("git ls-tree -z output is not NUL terminated")
    records.pop()
    if len(records) != 1:
        raise GitContractError(f"expected exactly one HEAD tree entry for {safe_path}; observed {len(records)}")
    meta, sep, raw_path = records[0].partition(b"\t")
    if not sep:
        raise GitContractError("malformed git ls-tree record")
    parts = meta.decode("ascii", "strict").split()
    if len(parts) != 3:
        raise GitContractError("malformed git ls-tree metadata")
    mode, object_type, oid = parts
    if mode not in SUPPORTED_MODES - {"000000"}:
        raise GitContractError(f"unsupported HEAD tree mode {mode}")
    if object_type not in {"blob", "commit"}:
        raise GitContractError(f"unsupported HEAD tree object type {object_type}")
    if not SHA_RE.fullmatch(oid):
        raise GitContractError("HEAD tree object identity is invalid")
    observed_path = _decode_repo_path(raw_path)
    if observed_path != safe_path:
        raise GitContractError(f"HEAD tree path mismatch: expected {safe_path}, got {observed_path}")
    return GitTreeEntry(observed_path, mode, object_type, oid)


def require_head_regular_blob(repo_root: Path, path: str) -> GitTreeEntry:
    entry = head_tree_entry(repo_root, path)
    if entry is None:
        raise GitContractError(f"repository path is not tracked at HEAD: {path}")
    if not entry.regular_blob:
        raise GitContractError(f"repository path is not a regular blob at HEAD: {path} mode={entry.mode} type={entry.object_type}")
    return entry


def require_worktree_matches_head_regular_blob(repo_root: Path, path: str) -> GitTreeEntry:
    entry = require_head_regular_blob(repo_root, path)
    full = repo_root / path
    if full.is_symlink() or not full.is_file():
        raise GitContractError(f"working-tree path is not a regular non-symlink file: {path}")
    observed = _run_git_bytes(repo_root, ["hash-object", "--", path]).decode("ascii", "strict").strip()
    if observed != entry.oid:
        raise GitContractError(f"working-tree content does not match committed HEAD blob: {path}")
    return entry
