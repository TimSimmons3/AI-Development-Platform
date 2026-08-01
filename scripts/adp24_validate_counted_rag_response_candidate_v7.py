#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, tempfile
from pathlib import Path
from typing import Any, NoReturn

EXPECTED_STATUS="DESIGN_CANDIDATE_V7_C1_APPLIED_UNCOMMITTED_NOT_AUTHORIZED_FOR_EXECUTION"
BRACKET_TOKEN=re.compile(r"\[[^\[\]\n]{1,128}\]")
GLUE_WORDS={"and","but","however","although","instead","rather","or"}
NEGATION=re.compile(r"^(?:not|never|no\s+longer)\s+",re.I)
SAFE_VALUE_PATTERNS={
 "verification_color":r"(?:amber|blue|green|red|violet|orange|yellow|purple|black|white|gray|grey|brown|pink|cyan|magenta)",
 "approved_archive_count":r"(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|[0-9]+)",
 "review_window":r"(?:(?:[0-9]+|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty(?:-six|\s+six)?|forty(?:-eight|\s+eight)?)\s+hours?)",
}

def norm(s:str)->str: return re.sub(r"\s+"," ",s).strip()
def normval(s:str)->str: return norm(s).strip(" ,.;:").lower()
def sha256(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def fail(control:str,detail:str="")->NoReturn:
 print("COUNTED_RESPONSE_CANDIDATE_V7_VALIDATION=FAIL"); print(f"FAILED_CONTROL={control}")
 if detail: print(f"DETAIL={detail}")
 print("EXECUTION_AUTHORIZATION=HOLD"); print("COUNTED_EXECUTION_AUTHORIZATION=HOLD"); raise SystemExit(1)
def protected_write(path:Path,value:str)->None:
 if path.exists(): fail("OUTPUT_COLLISION",str(path))
 path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(prefix=path.name+".",dir=str(path.parent))
 try:
  with os.fdopen(fd,"w",encoding="utf-8",newline="\n") as h:
   h.write(value); h.write("" if value.endswith("\n") else "\n")
  os.chmod(tmp,0o600); os.replace(tmp,path)
 finally:
  if os.path.exists(tmp): os.unlink(tmp)
def load_json(path:Path,control:str)->dict[str,Any]:
 try: return json.loads(path.read_text(encoding="utf-8"))
 except (UnicodeDecodeError,json.JSONDecodeError) as e: fail(control,type(e).__name__)
def load_contract(path:Path)->dict[str,Any]:
 d=load_json(path,"CONTRACT_PARSE")
 if d.get("status")!=EXPECTED_STATUS: fail("CONTRACT_STATUS",str(d.get("status")))
 if sorted(x.get("id") for x in d.get("cases",[]))!=["A","B","C","D"]: fail("CONTRACT_CASE_SET")
 if d.get("final_promotion_commit")!="UNFROZEN_REQUIRES_C1_REVIEW_AND_SIGNED_PROMOTION": fail("CANDIDATE_EXECUTION_BOUNDARY")
 if d.get("counted_execution_authorization")!="HOLD": fail("COUNTED_AUTHORIZATION_BOUNDARY")
 return d
def validate_binding_report(path:Path,contract_path:Path,manifest_path:Path,context:str)->dict[str,Any]:
 r=load_json(path,"BINDING_REPORT_PARSE")
 if r.get("contract_sha256")!=sha256(contract_path): fail("BINDING_REPORT_CONTRACT_HASH")
 if r.get("binding_manifest_sha256")!=sha256(manifest_path): fail("BINDING_REPORT_MANIFEST_HASH")
 expected="DESIGN_BINDING_VALIDATION" if context in {"SELF_TEST","DESIGN"} else "EXECUTION_BINDING_VALIDATION"
 if r.get("validation_type")!=expected or r.get("status")!="PASS": fail("BINDING_REPORT_STATUS")
 if context=="EXECUTION" and r.get("execution_authorization_status")!="AUTHORIZED_SINGLE_USE": fail("CANDIDATE_NOT_EXECUTION_AUTHORIZED")
 return r
def label_regex(labels:list[str])->str: return "(?:"+"|".join(sorted((re.escape(x) for x in labels),key=len,reverse=True))+")"
def safe_value_pattern(field_name:str)->str:
 if field_name not in SAFE_VALUE_PATTERNS: fail("UNSUPPORTED_FIELD_PATTERN",field_name)
 return SAFE_VALUE_PATTERNS[field_name]
def explicit_pattern(labels:list[str],value_pattern:str,source_id:str)->re.Pattern[str]:
 return re.compile(rf"(?<![A-Za-z0-9-])(?:the\s+)?(?P<label>{label_regex(labels)})(?:\s+for\s+{re.escape(source_id)})?\s*(?:is|was|:|=|equals|means)\s*(?P<neg>(?:not|never|no\s+longer)\s+)?(?P<value>{value_pattern})\b",re.I)
def reverse_pattern(labels:list[str],value_pattern:str)->re.Pattern[str]:
 return re.compile(rf"(?<![A-Za-z0-9-])(?P<neg>(?:not|never|no\s+longer)\s+)?(?P<value>{value_pattern})\s+(?:is|was|equals|means)\s+(?:the\s+)?(?P<label>{label_regex(labels)})\b",re.I)
def pronoun_pattern(value_pattern:str)->re.Pattern[str]:
 return re.compile(rf"(?<![A-Za-z0-9-])(?:(?:however|although|instead|rather|and|but|or)\s*[,;:]?\s*)?(?:(?:it|that|this)\s+(?:is|was|equals|means)\s+|(?P<bare>(?:not|never|no\s+longer)\s+))(?P<neg>(?:not|never|no\s+longer)\s+)?(?P<value>{value_pattern})\b",re.I)
def remove_spans(s:str,spans:list[tuple[int,int]])->str:
 c=list(s)
 for a,b in spans:
  for i in range(max(0,a),min(len(c),b)): c[i]=" "
 return "".join(c)
def assertions(contract:dict[str,Any],text:str)->list[dict[str,Any]]:
 source_id=contract["source"]["id"]; fields=contract["field_definitions"]
 explicit=[]
 for name,fd in fields.items():
  for regex in (explicit_pattern(fd["labels"],safe_value_pattern(name),source_id), reverse_pattern(fd["labels"],safe_value_pattern(name))):
   for m in regex.finditer(text):
    explicit.append((m.start(),m.end(),name,m.group("value"),bool(m.group("neg")),m.group(0),True))
 explicit.sort()
 events=list(explicit)
 for idx,e in enumerate(explicit):
  start=e[1]; end=explicit[idx+1][0] if idx+1<len(explicit) else len(text)
  candidates=[]
  for candidate_name,fd in fields.items():
   for m in pronoun_pattern(safe_value_pattern(candidate_name)).finditer(text,start,end):
    neg=bool(m.group("neg")) or bool(m.group("bare"))
    candidates.append((m.start(),m.end(),candidate_name,m.group("value"),neg,m.group(0),False))
  by_start={}
  for item in candidates:
   current=by_start.get(item[0])
   if current is None or item[1]>current[1]: by_start[item[0]]=item
  events.extend(by_start.values())
 events.sort()
 out=[]; seen=set()
 for a,b,name,value,negative,raw,is_explicit in events:
  key=(a,b,name)
  if key in seen: continue
  seen.add(key); accepted={normval(x) for x in fields[name]["accepted_values"]}; v=normval(value)
  truth="CONFLICT" if (not negative and v not in accepted) or (negative and v in accepted) else ("SUPPORTING_NEGATION" if negative else "SUPPORT")
  out.append({"field":name,"value":v,"negative":negative,"truth":truth,"span":[a,b],"raw":norm(raw),"explicit":is_explicit})
 return out
def classify(contract:dict[str,Any],case:dict[str,Any],raw:str,source_panel:str)->dict[str,Any]:
 actual=norm(raw); source_id=contract["source"]["id"]; tokens=BRACKET_TOKEN.findall(raw); citation_spans=[m.span() for m in BRACKET_TOKEN.finditer(raw)]
 semantic=remove_spans(raw,citation_spans); semnorm=norm(semantic)
 panel="PASS" if source_panel=="EXACT_SINGLE_SOURCE" else "FAIL"
 if case["not_found_case"]:
  factual="PASS" if semnorm=="NOT FOUND" else "FAIL"; fmt="PASS" if actual=="NOT FOUND" else "FAIL"; cite="PASS" if not tokens else "FAIL"; unsupported="PASS" if semnorm=="NOT FOUND" else "FAIL"; ass=[]; remainder="" if unsupported=="PASS" else semnorm
 else:
  ass=assertions(contract,semantic); required=set(case["fields"])
  factual="PASS"
  for f in required:
   if not any(a["field"]==f and a["truth"]=="SUPPORT" for a in ass): factual="FAIL"
  if any(a["truth"]=="CONFLICT" for a in ass): factual="FAIL"
  fmt="PASS" if actual==case["expected_full"] else "FAIL"
  expected_token=contract["citation"]["exact_token"]
  cite="PASS" if len(tokens)==1 and tokens[0].lower()==expected_token.lower() and actual.endswith(expected_token) else "FAIL"
  spans=[tuple(a["span"]) for a in ass]; remainder=remove_spans(semantic,spans); remainder=re.sub(r"[^A-Za-z0-9-]+"," ",remainder).lower(); words=[w for w in remainder.split() if w not in GLUE_WORDS]
  counts={f:sum(1 for a in ass if a["field"]==f) for f in contract["field_definitions"]}
  extra_assertion=any(a["field"] not in required or a["negative"] for a in ass) or any(counts[f]!=1 for f in required)
  unsupported="FAIL" if words or extra_assertion else "PASS"; remainder=" ".join(words)
 overall=all(x=="PASS" for x in [factual,fmt,cite,panel,unsupported])
 return {"schema_version":"0.7","case_id":case["id"],"normalized_response":actual,"assertions":ass,"factual_content_status":factual,"format_adherence_status":fmt,"inline_citation_status":cite,"source_panel_status":panel,"unsupported_addition_status":unsupported,"unsupported_remainder":remainder,"candidate_validation_status":"PASS" if overall else "FAIL","execution_authorization":"HOLD","counted_execution_authorization":"HOLD"}
def main()->int:
 ap=argparse.ArgumentParser(); ap.add_argument("--contract",required=True); ap.add_argument("--binding-manifest",required=True); ap.add_argument("--binding-report",required=True); ap.add_argument("--validation-context",choices=["SELF_TEST","DESIGN","EXECUTION"],required=True); ap.add_argument("--case",required=True); ap.add_argument("--raw",required=True); ap.add_argument("--source-panel-classification",required=True); ap.add_argument("--normalized-output",required=True); ap.add_argument("--report-output",required=True); a=ap.parse_args()
 cp,mp,bp,rp=map(Path,[a.contract,a.binding_manifest,a.binding_report,a.raw]); no=Path(a.normalized_output); ro=Path(a.report_output)
 for p,c in [(cp,"CONTRACT_FILE"),(mp,"BINDING_MANIFEST_FILE"),(bp,"BINDING_REPORT_FILE"),(rp,"RAW_RESPONSE_FILE")]:
  if not p.is_file(): fail(c,str(p))
 if no.resolve(strict=False)==ro.resolve(strict=False): fail("OUTPUT_PATH_ALIAS",str(no))
 if no.exists(): fail("NORMALIZED_OUTPUT_EXISTS",str(no))
 if ro.exists(): fail("REPORT_OUTPUT_EXISTS",str(ro))
 contract=load_contract(cp); validate_binding_report(bp,cp,mp,a.validation_context)
 matches=[x for x in contract["cases"] if x["id"]==a.case]
 if len(matches)!=1: fail("CASE_SELECTION",a.case)
 result=classify(contract,matches[0],rp.read_text(encoding="utf-8"),a.source_panel_classification)
 protected_write(no,result["normalized_response"]); protected_write(ro,json.dumps(result,indent=2,sort_keys=True))
 for k in ["case_id","factual_content_status","format_adherence_status","inline_citation_status","source_panel_status","unsupported_addition_status","candidate_validation_status"]: print(f"{k.upper()}={result[k]}")
 print("EXECUTION_AUTHORIZATION=HOLD"); print("COUNTED_EXECUTION_AUTHORIZATION=HOLD")
 return 0 if result["candidate_validation_status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
