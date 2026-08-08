from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Callable

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/'scripts'
if str(SCRIPT) not in sys.path: sys.path.insert(0,str(SCRIPT))

def load(name:str,path:Path):
 spec=importlib.util.spec_from_file_location(name,path); assert spec and spec.loader
 mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
T=load('far_transition',SCRIPT/'validate_transition_metrics.py')
M=load('far_mandatory',SCRIPT/'validate_mandatory_assurance_invariants.py')
TP=json.loads((ROOT/'config/transition-metrics-policy.json').read_text())
MP=json.loads((ROOT/'config/mandatory-assurance-invariant-policy.json').read_text())
EVENT=json.loads((ROOT/'docs/Templates/SMT-Transition-Event-Metrics-Template.json').read_text())
SNAP=json.loads((ROOT/'docs/Templates/SMT-Transition-Metrics-Baseline-Template.json').read_text())

VALUES:[Any]=[None,True,False,0,1,-1,10**1000,0.0,1.5,float('nan'),float('inf'),'', 'x','../x','\x00x',[],[1],{}, {'x':1}]

def rv(r:random.Random)->Any:
 v=r.choice(VALUES)
 return copy.deepcopy(v)

def mutate_one(r:random.Random,obj:dict[str,Any])->dict[str,Any]:
 out=copy.deepcopy(obj)
 keys=list(out)
 if not keys:return out
 k=r.choice(keys)
 if r.randrange(5)==0:out.pop(k,None)
 else:out[k]=rv(r)
 return out

def capture(name:str, iterations:int, fn:Callable[[random.Random],None], seed:int)->dict[str,Any]:
 r=random.Random(seed); unhandled=[]
 for i in range(iterations):
  try: fn(r)
  except Exception as exc:
   if len(unhandled)<25: unhandled.append({'iteration':i,'exception':f'{type(exc).__name__}: {exc}'})
 return {'surface':name,'iterations':iterations,'unhandled_count':len(unhandled),'sample_unhandled':unhandled}

def main(argv=None)->int:
 ap=argparse.ArgumentParser();ap.add_argument('--iterations',type=int,default=5000);ap.add_argument('--output');a=ap.parse_args(argv)
 n=a.iterations
 surfaces=[]
 surfaces.append(capture('transition_policy_shape',n,lambda r:T.policy_shape_errors(mutate_one(r,TP),'sweep'),1001))
 surfaces.append(capture('mandatory_policy_shape',n,lambda r:M.policy_shape_errors(mutate_one(r,MP),'sweep'),1002))
 def refprobe(r):
  e=[];T.validate_reference(ROOT,rv(r),e,'sweep-ref')
 surfaces.append(capture('transition_reference',n,refprobe,1003))
 def bindprobe(r):
  e=[];T.validate_binding(ROOT,rv(r),e,'sweep-binding')
 surfaces.append(capture('transition_binding',n,bindprobe,1004))
 surfaces.append(capture('transition_snapshot',n,lambda r:T.validate_snapshot(ROOT,'sweep.json',mutate_one(r,SNAP),TP),1005))
 surfaces.append(capture('transition_event',n,lambda r:T.validate_event(ROOT,'sweep.json',mutate_one(r,EVENT),TP),1006))
 def mandoc(r):
  # random assignment-like and Unicode/control text; validation must return errors, not raise.
  pieces=[str(rv(r)) for _ in range(5)]
  M.validate_governed_document(ROOT,'docs/Releases/Sweep.md','\n'.join(pieces),MP)
 surfaces.append(capture('mandatory_markdown',n,mandoc,1007))
 total=sum(x['iterations'] for x in surfaces); unhandled=sum(x['unhandled_count'] for x in surfaces)
 result={'record_type':'ADP_FINAL_ASSURANCE_EXCEPTION_SURFACE_SWEEP_R1','schema_version':'1.0','status':'PASS' if unhandled==0 else 'FAIL','iterations_per_surface':n,'surface_count':len(surfaces),'total_cases':total,'unhandled_exception_count':unhandled,'surfaces':surfaces}
 text=json.dumps(result,indent=2,sort_keys=True)+'\n'
 if a.output:Path(a.output).write_text(text,encoding='utf-8')
 print(text,end='');return 0 if result['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
