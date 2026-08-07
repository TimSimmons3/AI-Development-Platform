#!/usr/bin/env python3
"""Base-trusted validation of assurance trust-root changes and exact owner migration approval."""
from __future__ import annotations
import argparse,fnmatch,hashlib,json,re,sys
from pathlib import Path
from typing import Any
SCRIPT_DIR=Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:sys.path.insert(0,str(SCRIPT_DIR))
from smt_git_change_contract import GitContractError,commit_deltas,head_commit_and_tree,require_worktree_matches_head_regular_blob,resolve_commit
APPROVAL_PREFIX='APPROVE SMT ASSURANCE TRUST ROOT MIGRATION'
SHA_RE=re.compile(r'^[0-9a-f]{40,64}$')
MAX_JSON_BYTES=8*1024*1024
MANIFEST_FIELDS=frozenset({'policy_id','schema_version','owner_login','migration_record_glob','trusted_paths'})
MIGRATION_FIELDS=frozenset({'record_type','schema_version','base_commit','changed_trust_root_paths','owner_login','rationale','rationale_sha256'})

def load_json_strict(path:Path,max_bytes:int=MAX_JSON_BYTES)->Any:
 def reject(pairs):
  d={}
  for k,v in pairs:
   if k in d:raise ValueError(f'duplicate JSON key: {k}')
   d[k]=v
  return d
 try:size=path.stat().st_size
 except OSError as exc:raise ValueError(f'cannot stat JSON input: {type(exc).__name__}: {exc}') from exc
 if size>max_bytes:raise ValueError(f'JSON input size {size} exceeds limit {max_bytes}')
 try:data=path.read_bytes()
 except OSError as exc:raise ValueError(f'cannot read JSON input: {type(exc).__name__}: {exc}') from exc
 if len(data)>max_bytes:raise ValueError(f'JSON input exceeds limit {max_bytes}')
 try:text=data.decode('utf-8','strict')
 except UnicodeDecodeError as exc:raise ValueError('JSON input is not valid UTF-8') from exc
 return json.loads(text,object_pairs_hook=reject)

def manifest_errors(m:Any)->list[str]:
 e=[]
 if not isinstance(m,dict):return ['manifest must be object']
 if set(m)-MANIFEST_FIELDS:e.append('manifest unexpected fields: '+','.join(sorted(set(m)-MANIFEST_FIELDS)))
 if m.get('policy_id')!='SMT_ASSURANCE_TRUST_ROOT_R1':e.append('policy_id mismatch')
 if m.get('schema_version')!='1.0':e.append('schema_version mismatch')
 if not isinstance(m.get('owner_login'),str) or not re.fullmatch(r'[A-Za-z0-9-]+',m.get('owner_login','')):e.append('owner_login invalid')
 paths=m.get('trusted_paths')
 if not isinstance(paths,list) or not paths or paths!=sorted(set(paths)) or any(not isinstance(x,str) or not x or x.startswith('/') or '..' in Path(x).parts for x in paths):e.append('trusted_paths must be sorted unique safe repository paths')
 glob=m.get('migration_record_glob')
 if not isinstance(glob,str) or not glob.startswith('docs/Releases/') or not glob.endswith('.json'):e.append('migration_record_glob invalid')
 return e

def paths_digest(paths:list[str])->str:return hashlib.sha256(('\n'.join(paths)+'\n').encode('utf-8')).hexdigest()
def expected_approval(pr:int,head:str,record:str,changed:list[str])->str:
 if pr<1:raise ValueError('PR number must be positive')
 if not SHA_RE.fullmatch(head):raise ValueError('head identity invalid')
 return f"{APPROVAL_PREFIX} PR={pr} HEAD={head} RECORD={record} PATHS_SHA256={paths_digest(changed)}"

def normalized_comments(v:Any)->list[dict[str,Any]]:
 if not isinstance(v,list):raise ValueError('comments must be list')
 out=[]
 for x in v:
  if isinstance(x,list):out.extend(x)
  else:out.append(x)
 if any(not isinstance(x,dict) for x in out):raise ValueError('comment entry must be object')
 return out

def migration_record_errors(rec:Any,base:str,changed:list[str],owner:str)->list[str]:
 e=[]
 if not isinstance(rec,dict):return ['migration record must be object']
 extra=sorted(set(rec)-MIGRATION_FIELDS)
 if extra:e.append('migration record unexpected fields: '+','.join(extra))
 expected={'record_type':'SMT_ASSURANCE_TRUST_ROOT_MIGRATION','schema_version':'1.0','base_commit':base,'changed_trust_root_paths':changed,'owner_login':owner}
 for k,v in expected.items():
  if rec.get(k)!=v:e.append(f'migration record {k} mismatch')
 rationale=rec.get('rationale')
 if not isinstance(rationale,str) or not rationale.strip():e.append('migration record rationale required')
 digest=rec.get('rationale_sha256')
 if isinstance(rationale,str) and hashlib.sha256(rationale.encode('utf-8')).hexdigest()!=digest:e.append('migration record rationale_sha256 mismatch')
 return e

def validate(repo:Path,base_ref:str,manifest:dict[str,Any],mode:str,pr:int|None,comments:Any)->dict[str,Any]:
 violations=[]
 try:
  merge_base,deltas=commit_deltas(repo,base_ref);base_commit=resolve_commit(repo,base_ref);head,candidate_tree=head_commit_and_tree(repo)
  if merge_base!=base_commit:raise GitContractError(f'base freshness failure: merge-base {merge_base} != base commit {base_commit}')
 except Exception as exc:return {'status':'FAIL','violations':[f'Git trust-root classification failed: {type(exc).__name__}: {exc}'],'changed_trust_root_paths':[]}
 base=base_commit
 by_path={d.path:d for d in deltas};base_trusted=set(manifest['trusted_paths']);trusted=set(base_trusted)
 manifest_path='config/assurance-trust-root-manifest.json'
 # If the manifest itself changes, parse candidate manifest only as migration data and
 # require it to retain every existing R1 trusted path. New trusted paths are allowed
 # only when they are actually introduced/changed in the same migration.
 if manifest_path in by_path and not by_path[manifest_path].deleted:
  try:
   require_worktree_matches_head_regular_blob(repo,manifest_path);candidate_manifest=load_json_strict(repo/manifest_path);me=manifest_errors(candidate_manifest)
   if me:raise ValueError('; '.join(me))
   for fld in ['policy_id','schema_version','owner_login']:
    if candidate_manifest.get(fld)!=manifest.get(fld):raise ValueError(f'candidate trust manifest {fld} is immutable under R1')
   candidate_paths=set(candidate_manifest['trusted_paths'])
   removed=sorted(base_trusted-candidate_paths)
   if removed:raise ValueError('candidate trust manifest may not remove R1 trusted paths: '+','.join(removed))
   additions=sorted(candidate_paths-base_trusted)
   missing_additions=[x for x in additions if x not in by_path or by_path[x].deleted]
   if missing_additions:raise ValueError('new trusted paths must be introduced/changed in the same migration: '+','.join(missing_additions))
   trusted|=candidate_paths
  except Exception as exc:
   violations.append(f'candidate trust manifest invalid: {type(exc).__name__}: {exc}')
 changed=sorted({d.path for d in deltas if d.path in trusted})
 result={'record_type':'SMT_ASSURANCE_TRUST_ROOT_VALIDATION','schema_version':'1.0','status':'PASS','base_commit':base,'merge_base':merge_base,'head_commit':head,'candidate_tree':candidate_tree,'changed_trust_root_paths':changed,'migration_required':bool(changed),'migration_record':None,'expected_approval':None,'matching_owner_approval_count':0,'violations':violations}
 for path in changed:
  delta=by_path[path]
  if delta.deleted:
   violations.append(f'assurance trust-root path deletion is prohibited under R1: {path}')
  else:
   try:require_worktree_matches_head_regular_blob(repo,path)
   except Exception as exc:violations.append(f'assurance trust-root path must be an exact HEAD regular blob: {path}: {exc}')
 if not changed:
  result['status']='PASS' if not violations else 'FAIL';return result
 if mode!='migration':violations.append('ordinary PR may not modify assurance trust-root paths')
 else:
  candidates=sorted(d.path for d in deltas if not d.deleted and fnmatch.fnmatch(d.path,manifest['migration_record_glob']))
  if len(candidates)!=1:violations.append(f'trust-root migration requires exactly one changed migration record; observed {len(candidates)}')
  else:
   rp=candidates[0];result['migration_record']=rp
   try:require_worktree_matches_head_regular_blob(repo,rp);rec=load_json_strict(repo/rp)
   except Exception as exc:violations.append(f'migration record invalid: {type(exc).__name__}: {exc}')
   else:violations.extend(migration_record_errors(rec,base,changed,manifest['owner_login']))
   if pr is None:violations.append('migration mode requires PR number')
   else:
    try:expected=expected_approval(pr,head,rp,changed);result['expected_approval']=expected;cs=normalized_comments(comments);matches=sum(1 for c in cs if isinstance(c.get('user'),dict) and c['user'].get('login')==manifest['owner_login'] and c.get('body')==expected);result['matching_owner_approval_count']=matches
    except ValueError as exc:violations.append(str(exc))
    else:
     if matches!=1:violations.append(f'trust-root migration requires exactly one exact owner approval; observed {matches}')
 result['status']='PASS' if not violations else 'FAIL';return result

def subprocess_head(repo:Path)->str:
 import subprocess
 p=subprocess.run(['git','rev-parse','HEAD'],cwd=repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,timeout=30)
 if p.returncode:raise GitContractError(f'git rev-parse HEAD failed: {p.stderr.strip()}')
 h=p.stdout.strip()
 if not SHA_RE.fullmatch(h):raise GitContractError('HEAD identity invalid')
 return h

def main(argv=None)->int:
 p=argparse.ArgumentParser();p.add_argument('--repo-root',default='.');p.add_argument('--base-ref',required=True);p.add_argument('--trusted-manifest',required=True);p.add_argument('--mode',choices=['ordinary','migration'],default='ordinary');p.add_argument('--pr-number',type=int);p.add_argument('--comments');p.add_argument('--report',required=True);a=p.parse_args(sys.argv[1:] if argv is None else argv)
 repo=Path(a.repo_root).resolve(strict=True);out=Path(a.report);out=out if out.is_absolute() else repo/out
 try:
  man=load_json_strict(Path(a.trusted_manifest));errs=manifest_errors(man)
  if errs:raise ValueError('; '.join(errs))
  comments=[] if not a.comments else load_json_strict(Path(a.comments));r=validate(repo,a.base_ref,man,a.mode,a.pr_number,comments)
 except Exception as exc:r={'record_type':'SMT_ASSURANCE_TRUST_ROOT_VALIDATION','schema_version':'1.0','status':'FAIL','violations':[f'trust-root validation failed closed: {type(exc).__name__}: {exc}'],'changed_trust_root_paths':[]}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(r,indent=2,sort_keys=True));return 0 if r['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
