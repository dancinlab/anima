#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]; SCRIPT=ROOT/"state/anima_303m_r4_four_doc_2026_08_13/run_experiment.py"
S=importlib.util.spec_from_file_location("four",SCRIPT); four=importlib.util.module_from_spec(S); S.loader.exec_module(four); parent=four.parent
def sha(p):
 h=hashlib.sha256(); f=open(p,"rb")
 for c in iter(lambda:f.read(1048576),b""):h.update(c)
 f.close(); return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--data",required=True);ap.add_argument("--work",required=True);ap.add_argument("--result",required=True);ap.add_argument("--device",choices=["cpu"],default="cpu");a=ap.parse_args();pp=HERE/"protocol.json";p=json.loads(pp.read_text());pr=(HERE/p["parent_result"]).resolve();fd=p["fixed_data"]
 if sha(pr)!=p["parent_result_sha256"]:raise RuntimeError("parent SHA differs")
 panelp=(HERE/fd["panel"]).resolve(); data=Path(a.data); train=data/fd["train_file"];val=data/fd["validation_file"]
 if sha(panelp)!=fd["panel_sha256"] or sha(train)!=fd["train_file_sha256"] or sha(val)!=fd["validation_file_sha256"]:raise RuntimeError("source SHA differs")
 eligible=[]
 for d in parent._documents(train):
  e=parent._final_exchange(d)
  if e and len(e[1].encode())<=four.generator.CHAT_MAX_NEW_BYTES:eligible.append(d)
 work=Path(a.work);work.mkdir(parents=True,exist_ok=True);vdocs=parent._documents(val)[:32];vp=work/"heldout32.validation.txt";vp.write_bytes(parent._view_bytes(vdocs));panel=json.loads(panelp.read_text());r={"schema":"anima-303m-r4-aligned-boundary-result/v1","protocol_sha256":sha(pp),"parent_result_sha256":sha(pr),"arms":{}}
 for name,arm in p["arms"].items():
  docs=eligible[:arm["documents"]];tp=work/(name.lower()+".train.txt");tp.write_bytes(parent._view_bytes(docs))
  if sha(tp)!=fd["views"][str(arm["documents"])]:raise RuntimeError("view SHA differs")
  sm=four._train_arm({"fixed_recipe":p["fixed_recipe"]},name,arm,tp,vp,work,a.device);ck=work/(name.lower()+".bin");ex=[parent._final_exchange(d) for d in docs[:8]];sc=four._score_arm(ck,[x for x in ex if x],panel["bars"],a.device);r["arms"][name]={"summary":sm,"engine_sha256":sha(ck),"score":sc}
 gates={n:v["score"]["gate"] for n,v in r["arms"].items()};r["gates"]=gates;r["verdict"]=("BOUNDARY-ABOVE-64" if all(gates.values()) else "BOUNDARY-AT-OR-BELOW-32" if not gates["A32"] else "BOUNDARY-BETWEEN-32-AND-64");r["next_allowed_step"]="No larger model or production authorization follows.";Path(a.result).write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n");return 0
if __name__=="__main__":raise SystemExit(main())
