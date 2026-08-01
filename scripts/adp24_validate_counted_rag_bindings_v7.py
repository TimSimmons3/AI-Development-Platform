#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, tempfile
from pathlib import Path
DESIGN_PARENT="b934c7bd84bfbc35563f3681712c4d5bd8478196"
HEAD_EXPECTED=os.environ.get("ADP_V7_TEST_PARENT",DESIGN_PARENT) if os.environ.get("ADP_V7_TEST_MODE")=="1" else DESIGN_PARENT
PARENT=DESIGN_PARENT
CONTRACT_STATUS="DESIGN_CANDIDATE_V7_C1_APPLIED_UNCOMMITTED_NOT_AUTHORIZED_FOR_EXECUTION"
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 def hook(pairs):
  d={}
  for k,v in pairs:
   if k in d: raise ValueError("DUPLICATE_JSON_KEY="+k)
   d[k]=v
  return d
 return json.loads(p.read_text(encoding="ascii"),object_pairs_hook=hook)
def fail(c,d=""):
 print("COUNTED_RAG_BINDING_V7=FAIL"); print("FAILED_CONTROL="+c)
 if d: print("DETAIL="+d)
 print("EXECUTION_AUTHORIZATION=HOLD"); print("COUNTED_EXECUTION_AUTHORIZATION=HOLD"); raise SystemExit(1)
def git(root,*a):
 r=subprocess.run(["git","-C",str(root),*a],text=True,capture_output=True)
 if r.returncode: fail("GIT_COMMAND",r.stderr.strip())
 return r.stdout.strip()
def protected(p,obj):
 if p.exists(): fail("OUTPUT_COLLISION",str(p))
 p.parent.mkdir(parents=True,exist_ok=True); fd,tmp=tempfile.mkstemp(prefix=p.name+".",dir=p.parent)
 try:
  with os.fdopen(fd,"w",encoding="ascii",newline="\n") as f: json.dump(obj,f,indent=2,sort_keys=True); f.write("\n")
  os.chmod(tmp,0o600); os.replace(tmp,p)
 finally:
  if os.path.exists(tmp): os.unlink(tmp)
def design(root,contract_path,manifest_path,output,application_manifest):
 c=load(contract_path); m=load(manifest_path); app=load(application_manifest)
 if c.get("status")!=CONTRACT_STATUS or c.get("design_parent_commit")!=PARENT: fail("CONTRACT_BASELINE")
 if c.get("counted_execution_authorization")!="HOLD": fail("CONTRACT_EXECUTION_BOUNDARY")
 if m.get("status")!="DESIGN_CANDIDATE_V7_C1_BINDING_MANIFEST": fail("MANIFEST_STATUS")
 if git(root,"rev-parse","HEAD")!=HEAD_EXPECTED: fail("DESIGN_PARENT")
 expected={x["path"]:x for x in app["paths"]}
 for item in m.get("bound_paths",[]):
  p=root/item["path"]
  if not p.is_file() or h(p)!=item["sha256"]: fail("MANIFEST_FILE_HASH",item["path"])
  if item["path"] not in expected: fail("MANIFEST_PATH_NOT_IN_APPLICATION",item["path"])
 r={"schema_version":"1.0","validation_type":"DESIGN_BINDING_VALIDATION","status":"PASS","release":"ADP-v2.4","candidate":"v7","design_parent_commit":PARENT,"contract_sha256":h(contract_path),"binding_manifest_sha256":h(manifest_path),"application_manifest_sha256":h(application_manifest),"execution_authorization_status":"HOLD","repository_mutation":"NONE"}
 protected(output,r); print("COUNTED_RAG_BINDING_V7=PASS"); print("VALIDATION_TYPE=DESIGN_BINDING_VALIDATION"); print("EXECUTION_AUTHORIZATION=HOLD"); return 0
def signed_phase(kind,root,contract_path,manifest_path,output,record,signature,allowed,namespace):
 c=load(contract_path); rec=load(record)
 if c.get("counted_execution_authorization")!="HOLD": fail("CONTRACT_BOUNDARY")
 vr=subprocess.run(["ssh-keygen","-Y","verify","-f",str(allowed),"-I","timothy_simmons99@yahoo.com","-n",namespace,"-s",str(signature)],input=record.read_bytes(),capture_output=True)
 if vr.returncode: fail("SIGNED_PHASE_RECORD_SIGNATURE")
 required={"release":"ADP-v2.4","candidate":"v7","design_parent_commit":PARENT}
 for k,v in required.items():
  if rec.get(k)!=v: fail("SIGNED_PHASE_RECORD_"+k.upper())
 if rec.get("contract_sha256")!=h(contract_path) or rec.get("binding_manifest_sha256")!=h(manifest_path): fail("SIGNED_PHASE_INPUT_HASH")
 status="AUTHORIZED_SINGLE_USE" if kind=="EXECUTION" else "PROMOTION_ONLY"
 r={"schema_version":"1.0","validation_type":kind+"_BINDING_VALIDATION","status":"PASS","release":"ADP-v2.4","candidate":"v7","design_parent_commit":PARENT,"contract_sha256":h(contract_path),"binding_manifest_sha256":h(manifest_path),"signed_record_sha256":h(record),"execution_authorization_status":status,"repository_mutation":"NONE"}
 protected(output,r); print("COUNTED_RAG_BINDING_V7=PASS"); print("VALIDATION_TYPE="+kind+"_BINDING_VALIDATION"); print("EXECUTION_AUTHORIZATION="+status); return 0
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--repository-root",required=True); ap.add_argument("--contract",required=True); ap.add_argument("--binding-manifest",required=True); ap.add_argument("--context",choices=["DESIGN","PROMOTION","EXECUTION"],required=True); ap.add_argument("--output",required=True); ap.add_argument("--application-manifest"); ap.add_argument("--signed-record"); ap.add_argument("--signature"); ap.add_argument("--allowed-signers"); a=ap.parse_args()
 root=Path(a.repository_root); cp=Path(a.contract); mp=Path(a.binding_manifest); out=Path(a.output)
 if a.context=="DESIGN":
  if not a.application_manifest: fail("APPLICATION_MANIFEST_REQUIRED")
  return design(root,cp,mp,out,Path(a.application_manifest))
 for x,n in [(a.signed_record,"SIGNED_RECORD"),(a.signature,"SIGNATURE"),(a.allowed_signers,"ALLOWED_SIGNERS")]:
  if not x: fail(n+"_REQUIRED")
 ns="adp-v2.4-candidate-v7-promotion" if a.context=="PROMOTION" else "adp-v2.4-candidate-v7-execution"
 return signed_phase(a.context,root,cp,mp,out,Path(a.signed_record),Path(a.signature),Path(a.allowed_signers),ns)
if __name__=="__main__": raise SystemExit(main())
