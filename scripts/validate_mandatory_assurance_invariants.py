#!/usr/bin/env python3
"""Validate mandatory one-pass assurance invariants in governed Markdown."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

SCRIPT_DIR=Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path: sys.path.insert(0,str(SCRIPT_DIR))
from smt_git_change_contract import GitContractError, commit_deltas, head_commit_and_tree, resolve_commit

DEFAULT_POLICY="config/mandatory-assurance-invariant-policy.json"
ABSOLUTE_RESOURCE_LIMITS={"json_bytes":1048576,"markdown_bytes":2097152}
POLICY_TOP_LEVEL_FIELDS=frozenset({"policy_id","schema_version","effective_date","owner","required_block","required_block_order","governed_markdown_roots","governed_filename_keywords","exception","resource_limits"})
OWNER_FIELDS=frozenset({"name","github_login"})
EXCEPTION_FIELDS=frozenset({"approval_hash_pattern","artifact_hash_set_pattern","directory","required_nonempty_fields","required_values","utc_pattern"})
DEFAULT_REPORT="mandatory-assurance-invariant-report.json"
PLACEHOLDER_MARKERS=("<",">","TBD","TODO","PLACEHOLDER")


def load_json_text_strict(text:str)->Any:
    def reject_duplicates(pairs):
        out={}
        for k,v in pairs:
            if k in out: raise ValueError(f"duplicate JSON key: {k}")
            out[k]=v
        return out
    return json.loads(text,object_pairs_hook=reject_duplicates)


def read_limited_bytes(path:Path,limit:int,context:str)->bytes:
    try:size=path.stat().st_size
    except OSError as exc:raise ValueError(f"{context}: stat failed: {type(exc).__name__}: {exc}") from exc
    if size>limit:raise ValueError(f"{context}: file size {size} exceeds limit {limit}")
    try:data=path.read_bytes()
    except OSError as exc:raise ValueError(f"{context}: read failed: {type(exc).__name__}: {exc}") from exc
    if len(data)>limit:raise ValueError(f"{context}: file size exceeds limit {limit}")
    return data

def read_limited_text(path:Path,limit:int,context:str)->str:
    try:return read_limited_bytes(path,limit,context).decode("utf-8","strict")
    except UnicodeDecodeError as exc:raise ValueError(f"{context}: not valid UTF-8") from exc

def load_json_strict(path:Path,limit:int=ABSOLUTE_RESOURCE_LIMITS["json_bytes"])->dict[str,Any]:
    value=load_json_text_strict(read_limited_text(path,limit,str(path)))
    if not isinstance(value,dict): raise ValueError("policy root must be an object")
    return value


def run_git_text(repo:Path,args:list[str])->str:
    import subprocess
    try:
        p=subprocess.run(["git",*args],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,timeout=30)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"git {' '.join(args)} execution failed: {type(exc).__name__}: {exc}") from exc
    if p.returncode: raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout


def git_text_at_commit(repo:Path,commit:str,path:str,max_bytes:int=ABSOLUTE_RESOURCE_LIMITS["json_bytes"])->str|None:
    out=run_git_text(repo,["ls-tree","--name-only",commit,"--",path])
    if path not in {x.strip() for x in out.splitlines() if x.strip()}: return None
    size_text=run_git_text(repo,["cat-file","-s",f"{commit}:{path}"]).strip()
    try:size=int(size_text)
    except ValueError as exc:raise ValueError(f"historical repository object size is invalid for {path}") from exc
    if size>max_bytes:raise ValueError(f"historical repository object {path} size {size} exceeds limit {max_bytes}")
    return run_git_text(repo,["show",f"{commit}:{path}"])


def normalized_relative(repo_root:Path,value:str)->str:
    if not isinstance(value,str) or not value: raise ValueError("empty repository path")
    path=Path(value)
    if path.is_absolute():
        try:path=path.resolve(strict=False).relative_to(repo_root.resolve(strict=True))
        except ValueError as exc:raise ValueError(f"path outside repository: {value}") from exc
    pure=PurePosixPath(path.as_posix())
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:raise ValueError(f"unsafe repository path: {value}")
    if any(ord(ch)<32 or ord(ch)==127 for ch in pure.as_posix()):raise ValueError(f"repository path contains prohibited control character: {value!r}")
    return pure.as_posix()


def string_list(v:Any)->bool:return isinstance(v,list) and bool(v) and all(isinstance(x,str) and bool(x) for x in v) and len(v)==len(set(v))


def policy_shape_errors(policy:Any,context:str,allow_legacy_missing_resource_limits:bool=False)->list[str]:
    e=[]
    if not isinstance(policy,dict):return [f"{context}: policy must be object"]
    extra=sorted(set(policy)-set(POLICY_TOP_LEVEL_FIELDS))
    if extra:e.append(f"{context}: unexpected top-level fields: {','.join(extra)}")
    for f in ["policy_id","schema_version","effective_date"]:
        if not isinstance(policy.get(f),str) or not policy.get(f):e.append(f"{context}: {f} must be non-empty string")
    if isinstance(policy.get("effective_date"),str):
        try:datetime.strptime(policy["effective_date"],"%Y-%m-%d")
        except ValueError:e.append(f"{context}: effective_date must be valid YYYY-MM-DD")
    for f in ["governed_markdown_roots","governed_filename_keywords","required_block_order"]:
        if not string_list(policy.get(f)):e.append(f"{context}: {f} must be non-empty unique-string list")
    roots=policy.get("governed_markdown_roots",[])
    if isinstance(roots,list):
        for root in roots:
            if not isinstance(root,str) or not root.endswith('/') or root.startswith('/') or '..' in PurePosixPath(root).parts:e.append(f"{context}: unsafe governed root {root!r}")
    rb=policy.get("required_block")
    order=policy.get("required_block_order")
    if not isinstance(rb,dict) or not rb or any(not isinstance(k,str) or not isinstance(v,str) or not k or not v for k,v in rb.items()):e.append(f"{context}: required_block must be non-empty string map")
    elif isinstance(order,list) and order!=list(dict.fromkeys(order)) or (isinstance(order,list) and set(order)!=set(rb)):
        e.append(f"{context}: required_block_order must contain required_block keys exactly once")
    owner=policy.get("owner")
    if not isinstance(owner,dict) or not isinstance(owner.get("name"),str) or not isinstance(owner.get("github_login"),str):e.append(f"{context}: owner identity invalid")
    elif set(owner)-set(OWNER_FIELDS):e.append(f"{context}: owner unexpected fields: {','.join(sorted(set(owner)-set(OWNER_FIELDS)))}")
    ex=policy.get("exception")
    if not isinstance(ex,dict):e.append(f"{context}: exception must be object")
    else:
        extra_ex=sorted(set(ex)-set(EXCEPTION_FIELDS))
        if extra_ex:e.append(f"{context}: exception unexpected fields: {','.join(extra_ex)}")
        for f in ["approval_hash_pattern","artifact_hash_set_pattern","directory","utc_pattern"]:
            if not isinstance(ex.get(f),str) or not ex.get(f):e.append(f"{context}: exception.{f} invalid")
        if not string_list(ex.get("required_nonempty_fields")):e.append(f"{context}: exception.required_nonempty_fields invalid")
        if not isinstance(ex.get("required_values"),dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in ex.get("required_values",{}).items()):e.append(f"{context}: exception.required_values invalid")
    limits=policy.get('resource_limits')
    if limits is None and allow_legacy_missing_resource_limits:
        pass
    elif not isinstance(limits,dict) or set(limits)!=set(ABSOLUTE_RESOURCE_LIMITS):e.append(f"{context}: resource_limits must contain exactly json_bytes,markdown_bytes")
    else:
        for key,ceiling in ABSOLUTE_RESOURCE_LIMITS.items():
            value=limits.get(key)
            if isinstance(value,bool) or not isinstance(value,int) or value<1024 or value>ceiling:e.append(f"{context}: resource_limits.{key} must be integer in [1024,{ceiling}]")
    return e


def policy_compatibility_errors(base:dict[str,Any],current:dict[str,Any])->list[str]:
    e=[]
    for f in ["policy_id","schema_version","required_block","required_block_order","owner","exception"]:
        if base.get(f)!=current.get(f):e.append(f"mandatory policy {f} is immutable under ordinary work")
    base_limits=base.get('resource_limits');current_limits=current.get('resource_limits')
    if base_limits is None:
        if current_limits!=ABSOLUTE_RESOURCE_LIMITS:e.append('mandatory policy resource_limits bootstrap must equal canonical R1 limits')
    elif base_limits!=current_limits:e.append('mandatory policy resource_limits are immutable under ordinary work')
    for f in ["governed_markdown_roots","governed_filename_keywords"]:
        removed=sorted(set(base.get(f,[]))-set(current.get(f,[])))
        if removed:e.append(f"mandatory policy {f} may not remove historical classifiers: {','.join(removed)}")
    return e


def is_governed(path:str,policy:dict[str,Any])->bool:
    if not path.lower().endswith('.md'):return False
    if any(path.startswith(str(root)) for root in policy.get('governed_markdown_roots',[])):return True
    name=PurePosixPath(path).name.lower()
    return any(str(k).lower() in name for k in policy.get('governed_filename_keywords',[]))


def historical_governed_inventory(repo:Path,merge_base:str,base_policy:dict[str,Any])->set[str]:
    paths=run_git_text(repo,["ls-tree","-r","--name-only",merge_base]).splitlines()
    return {p for p in paths if is_governed(p,base_policy)}


def parse_assignments(text:str)->dict[str,list[str]]:
    vals={}
    for raw in text.splitlines():
        m=re.fullmatch(r"([A-Z][A-Z0-9_]*)=(.*)",raw.strip())
        if m:vals.setdefault(m.group(1),[]).append(m.group(2))
    return vals


def one_value(a,key):
    v=a.get(key,[]);return v[0] if len(v)==1 else None


def has_placeholder(value:str)->bool:
    u=value.upper();return any(m in u for m in PLACEHOLDER_MARKERS)


def validate_exception_record(path:str,text:str,policy:dict[str,Any])->list[str]:
    e=[];a=parse_assignments(text);ex=policy['exception']
    for k,v in ex['required_values'].items():
        if a.get(k,[])!=[v]:e.append(f"{path}: requires exactly `{k}={v}`")
    for k in ex['required_nonempty_fields']:
        v=one_value(a,k)
        if v is None or not v.strip():e.append(f"{path}: requires one non-empty `{k}`")
        elif has_placeholder(v):e.append(f"{path}: `{k}` contains a placeholder")
    for k,pat in {"APPROVAL_TEXT_SHA256":ex['approval_hash_pattern'],"ARTIFACT_SHA256_SET":ex['artifact_hash_set_pattern'],"APPROVED_UTC":ex['utc_pattern'],"EXPIRATION_UTC":ex['utc_pattern']}.items():
        v=one_value(a,k)
        if v and not re.fullmatch(pat,v):e.append(f"{path}: `{k}` does not match required format")
    return e


def validate_governed_document(repo:Path,path:str,text:str,policy:dict[str,Any])->tuple[list[str],str|None]:
    e=[];a=parse_assignments(text);req=policy['required_block'];order=policy['required_block_order'];status=one_value(a,'EXCEPTION_STATUS');vals=dict(req)
    if status=='APPROVED':vals['EXCEPTION_STATUS']='APPROVED'
    block='\n'.join(f"{k}={vals[k]}" for k in order)
    if text.count(block)!=1:e.append(f"{path}: canonical invariant block must appear exactly once in required order")
    for k,v in req.items():
        if k=='EXCEPTION_STATUS' and status=='APPROVED':continue
        if a.get(k,[])!=[v]:e.append(f"{path}: requires exactly `{k}={v}`")
    record=None
    if status=='APPROVED':
        rv=a.get('EXCEPTION_RECORD',[])
        if len(rv)!=1:e.append(f"{path}: approved exception requires exactly one `EXCEPTION_RECORD`")
        else:
            try:record=normalized_relative(repo,rv[0])
            except ValueError as exc:e.append(f"{path}: {exc}")
            else:
                exdir=policy['exception']['directory']
                if not record.startswith(exdir) or not record.endswith('.md'):e.append(f"{path}: exception record must be Markdown under `{exdir}`")
                fp=repo/record
                if not fp.is_file() or fp.is_symlink():e.append(f"{path}: exception record is missing or not a regular file: {record}")
                else:
                    try:rt=read_limited_text(fp,policy['resource_limits']['markdown_bytes'],path)
                    except UnicodeDecodeError:e.append(f"{path}: exception record is not UTF-8: {record}")
                    else:e.extend(validate_exception_record(record,rt,policy))
    elif status!=req['EXCEPTION_STATUS']:e.append(f"{path}: `EXCEPTION_STATUS` must be NOT_GRANTED or APPROVED")
    return e,record


def validate_files(repo:Path,paths:list[str],policy:dict[str,Any],required_historical:set[str]|None=None)->dict[str,Any]:
    violations=[];governed=[];exception_records=set();files=[];required_historical=required_historical or set()
    for raw in sorted(set(paths)):
        try:path=normalized_relative(repo,raw)
        except ValueError as exc:violations.append(str(exc));continue
        full=repo/path
        required=path in required_historical
        if full.is_symlink():violations.append(f"{path}: must be a regular non-symlink file");continue
        if not full.exists():violations.append(f"{path}: changed path does not exist");continue
        if not full.is_file():violations.append(f"{path}: must be a regular non-symlink file");continue
        if not required and not is_governed(path,policy):continue
        governed.append(path);errs=[]
        try:data=read_limited_bytes(full,policy['resource_limits']['markdown_bytes'],path)
        except ValueError as exc:violations.append(str(exc));continue
        if b'\r' in data:errs.append(f"{path}: contains CR characters")
        try:text=data.decode('utf-8')
        except UnicodeDecodeError:errs.append(f"{path}: is not valid UTF-8");text=None
        if text is not None:
            if any(line.rstrip(' \t')!=line for line in text.splitlines()):errs.append(f"{path}: contains trailing whitespace")
            exdir=policy['exception']['directory'];is_ex=path.startswith(exdir) and PurePosixPath(path).name.lower()!='readme.md'
            if is_ex:errs.extend(validate_exception_record(path,text,policy));exception_records.add(path)
            else:
                ve,record=validate_governed_document(repo,path,text,policy);errs.extend(ve)
                if record:exception_records.add(record)
        violations.extend(errs);files.append({'path':path,'sha256':hashlib.sha256(data).hexdigest(),'status':'PASS' if not errs else 'FAIL'})
    return {'record_type':'SMT_MANDATORY_ASSURANCE_INVARIANT_VALIDATION','schema_version':'1.0','status':'PASS' if not violations else 'FAIL','governed_file_count':len(governed),'governed_files':governed,'exception_record_count':len(exception_records),'exception_records':sorted(exception_records),'violations':violations,'files':files}


def failure_report(message:str)->dict[str,Any]:
    return {'record_type':'SMT_MANDATORY_ASSURANCE_INVARIANT_VALIDATION','schema_version':'1.0','status':'FAIL','governed_file_count':0,'governed_files':[],'exception_record_count':0,'exception_records':[],'violations':[message],'files':[],'direct_changed_paths':[],'deleted_paths':[],'base_governed_paths':[],'base_policy_status':'FAIL'}


def parse_args(argv):
    p=argparse.ArgumentParser();p.add_argument('--repo-root',default='.');p.add_argument('--policy',default=DEFAULT_POLICY);s=p.add_mutually_exclusive_group(required=True);s.add_argument('--base-ref');s.add_argument('--files',nargs='+');p.add_argument('--report',default=DEFAULT_REPORT);return p.parse_args(argv)


def main(argv=None)->int:
    args=parse_args(sys.argv[1:] if argv is None else argv);repo=Path(args.repo_root).resolve(strict=True);rp=Path(args.report);rp=rp if rp.is_absolute() else repo/rp
    try:
        pp=Path(args.policy);pp=pp if pp.is_absolute() else repo/pp;policy=load_json_strict(pp);pe=policy_shape_errors(policy,'current policy')
        if pe:raise ValueError('; '.join(pe))
        base_policy=None;merge_base=None;base_status='NOT_APPLICABLE';deleted=set();historical=set()
        if args.base_ref:
            merge_base,deltas=commit_deltas(repo,args.base_ref);base_commit=resolve_commit(repo,args.base_ref)
            if merge_base!=base_commit:raise GitContractError(f"base freshness failure: merge-base {merge_base} != base commit {base_commit}")
            direct=[d.path for d in deltas if not d.deleted];deleted={d.path for d in deltas if d.deleted}
            try:policy_rel=pp.resolve(strict=False).relative_to(repo).as_posix()
            except ValueError as exc:raise ValueError('mandatory policy must be inside repository') from exc
            bt=git_text_at_commit(repo,merge_base,policy_rel)
            if bt is None:raise ValueError('merge-base mandatory policy is absent; ordinary validation cannot establish historical invariant semantics')
            base_policy=load_json_text_strict(bt);be=policy_shape_errors(base_policy,'merge-base policy',allow_legacy_missing_resource_limits=True)
            if be:raise ValueError('; '.join(be))
            ce=policy_compatibility_errors(base_policy,policy)
            if ce:raise ValueError('; '.join(ce))
            historical=historical_governed_inventory(repo,merge_base,base_policy);base_status='PRESENT_VALID'
        else:direct=list(args.files);deleted=set()
        hist_changed=historical.intersection(set(direct)|deleted)
        report=validate_files(repo,direct,policy,historical.intersection(direct))
        for path in sorted(deleted):
            if path in historical or is_governed(path,policy):report['violations'].append(f"{path}: deletion of governed mandatory-assurance artifact is prohibited")
        if report['violations']:report['status']='FAIL'
        report.update({'direct_changed_paths':sorted(set(direct)),'deleted_paths':sorted(deleted),'base_governed_paths':sorted(hist_changed),'merge_base':merge_base,'base_policy_status':base_status})
        if args.base_ref:
            report['base_commit']=resolve_commit(repo,args.base_ref);report['head_commit'],report['candidate_tree']=head_commit_and_tree(repo)
    except Exception as exc:
        report=failure_report(f"mandatory assurance validation failed closed: {type(exc).__name__}: {exc}")
    try:rp.parent.mkdir(parents=True,exist_ok=True);rp.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    except OSError as exc:
        print(f"mandatory assurance report write failed: {type(exc).__name__}: {exc}",file=sys.stderr);return 1
    print(json.dumps(report,indent=2,sort_keys=True));return 0 if report['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
