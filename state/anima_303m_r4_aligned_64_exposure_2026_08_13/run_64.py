#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];SCRIPT=ROOT/"state/anima_303m_r4_four_doc_2026_08_13/run_experiment.py";S=importlib.util.spec_from_file_location("f",SCRIPT);four=importlib.util.module_from_spec(S);S.loader.exec_module(four);parent=four.parent
def sha(p):
 h=hashlib.sha256();f=open(p,"rb")
 for c in iter(lambda:f.read(1048576),b""):h.update(c)
 f.close();return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--data",required=True);ap.add_argument("--work",required=True);ap.add_argument("--result",required=True);ap.add_argument("--device",choices=["cpu"],default="cpu");a=ap.parse_args();pp=HERE/"protocol.json";p=json.loads(pp.read_text());pr=(HERE/p["parent_result"]).resolve();fd=p["fixed_data"]
 if sha(pr)!=p["parent_result_sha256"]:raise RuntimeError("parent SHA differs")
 panelp=(HERE/fd["panel"]).resolve();data=Path(a.data);train=data/fd["train_file"];val=data/fd["validation_file"]
 if sha(panelp)!=fd["panel_sha256"] or sha(train)!=fd["train_file_sha256"] or sha(val)!=fd["validation_file_sha256"]:raise RuntimeError("source SHA differs")
 docs=[]
 for d in parent._documents(train):
  e=parent._final_exchange(d)
  if e and len(e[1].encode())<=four.generator.CHAT_MAX_NEW_BYTES:docs.append(d)
  if len(docs)==64:break
 work=Path(a.work);work.mkdir(parents=True,exist_ok=True);tp=work/"sixtyfour.train.txt";vp=work/"heldout32.validation.txt";tp.write_bytes(parent._view_bytes(docs));vp.write_bytes(parent._view_bytes(parent._documents(val)[:32]))
 if sha(tp)!=fd["view_sha256"] or sha(vp)!=fd["heldout_32_view_sha256"]:raise RuntimeError("view SHA differs")
 sm=four._train_arm({"fixed_recipe":p["fixed_recipe"]},"E64",p["arm"],tp,vp,work,a.device);ck=work/"e64.bin";panel=json.loads(panelp.read_text());ex=[parent._final_exchange(d) for d in docs[:8]];sc=four._score_arm(ck,[x for x in ex if x],panel["bars"],a.device);r={"schema":"anima-303m-r4-aligned-64-exposure-result/v1","protocol_sha256":sha(pp),"parent_result_sha256":sha(pr),"engine_sha256":sha(ck),"summary":sm,"score":sc,"gate":sc["gate"],"verdict":"SUPPORTED-EXPOSURE-MATCHED-64" if sc["gate"] else "FALSIFIED-EXPOSURE-MATCHED-64","next_allowed_step":"No scale-up or production authorization follows."};Path(a.result).write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n");return 0
if __name__=="__main__":raise SystemExit(main())
