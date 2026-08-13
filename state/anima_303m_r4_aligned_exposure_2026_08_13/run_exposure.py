#!/usr/bin/env python3
"""Run the preregistered aligned 16-document exposure arms."""

from __future__ import annotations
import argparse, hashlib, importlib.util, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCRIPT = ROOT / "state/anima_303m_r4_four_doc_2026_08_13/run_experiment.py"
SPEC = importlib.util.spec_from_file_location("r4_four", SCRIPT)
four = importlib.util.module_from_spec(SPEC)
if SPEC.loader is None: raise RuntimeError("four-document harness loader is missing")
SPEC.loader.exec_module(four)
parent = four.parent

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--data",required=True); ap.add_argument("--work",required=True); ap.add_argument("--result",required=True); ap.add_argument("--device",choices=["cpu"],default="cpu"); a=ap.parse_args()
    pp=HERE/"protocol.json"; p=json.loads(pp.read_text()); parent_result=(HERE/p["parent_result"]).resolve(); fd=p["fixed_data"]
    if sha(parent_result)!=p["parent_result_sha256"]: raise RuntimeError("parent result SHA differs")
    panel_path=(HERE/fd["panel"]).resolve()
    if sha(panel_path)!=fd["panel_sha256"]: raise RuntimeError("panel SHA differs")
    data=Path(a.data); train=data/fd["train_file"]; val=data/fd["validation_file"]
    if sha(train)!=fd["train_file_sha256"] or sha(val)!=fd["validation_file_sha256"]: raise RuntimeError("source SHA differs")
    selected=[]
    for d in parent._documents(train):
        e=parent._final_exchange(d)
        if e and len(e[1].encode("utf-8","surrogateescape"))<=four.generator.CHAT_MAX_NEW_BYTES: selected.append(d)
        if len(selected)==16: break
    vb=parent._view_bytes(selected); valdocs=parent._documents(val)[:32]; valb=parent._view_bytes(valdocs)
    if parent._sha256_bytes(vb)!=fd["sixteen_document_view_sha256"] or parent._sha256_bytes(valb)!=fd["heldout_32_view_sha256"]: raise RuntimeError("view SHA differs")
    work=Path(a.work); work.mkdir(parents=True,exist_ok=True); tp=work/"sixteen.train.txt"; vp=work/"heldout32.validation.txt"; tp.write_bytes(vb); vp.write_bytes(valb)
    ex=[parent._final_exchange(d) for d in selected[:8]]; panel=json.loads(panel_path.read_text()); result={"schema":"anima-303m-r4-aligned-exposure-result/v1","protocol_sha256":sha(pp),"parent_result_sha256":sha(parent_result),"device":a.device,"arms":{}}
    for name,arm in p["arms"].items():
        summary=four._train_arm({"fixed_recipe":p["fixed_recipe"]},name,arm,tp,vp,work,a.device); ck=work/(name.lower()+".bin"); score=four._score_arm(ck,[x for x in ex if x],panel["bars"],a.device); result["arms"][name]={"engine_sha256":sha(ck),"summary":summary,"score":score}
    fixed=result["arms"]["S16_fixed_steps"]["score"]["gate"]; matched=result["arms"]["E16_matched_exposure"]["score"]["gate"]
    result["gates"]={"fixed_steps":fixed,"matched_exposure":matched}; result["verdict"]=("SUPPORTED-INSUFFICIENT-PER-DOCUMENT-EXPOSURE" if matched and not fixed else "SUPPORTED-BOTH-EXPOSURES" if matched and fixed else "FALSIFIED-BOUNDED-EXPOSURE-TREATMENT"); result["next_allowed_step"]="No 303M, IIT coupling or production authorization follows from this local memorization test."
    Path(a.result).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n"); return 0

if __name__=="__main__": raise SystemExit(main())
