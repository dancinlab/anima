#!/usr/bin/env python3
"""h1431_decode_batch.py — PHASE 1 (load-once). Builds the jobs file (all NSUBJ×NSEED×{rel,meas}
fragments), invokes engine_decode_batch_cli.hexa ONCE (303M loaded once, ~5GB resident, single
~24GB transient load peak — NOT 30 reloads), and converts the batch output to fragments.jsonl.
NO torch. Resumable: skips jobs whose tag already has output. Phase 2 = h1431_score_only.py.
"""
import os, sys, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
BIN  = os.environ["H1431_BIN"]
HEXA = os.path.expanduser("~/.hx/bin/hexa")
CLI  = os.path.join(HERE, "engine_decode_batch_cli.hexa")
JOBS = os.path.join(HERE, "jobs.tsv")
RAW  = os.path.join(HERE, "batch_out.tsv")          # tag\ttext (appended by hexa)
FRAGS= os.path.join(HERE, "fragments.jsonl")
SUBJECTS = ["consciousness","tension","memory","silence","dreaming"]
SEEDS    = [7,4302,4303]
MAXNEW = int(os.environ.get("H1431_MAXNEW","110"))
NSUBJ  = int(os.environ.get("H1431_NSUBJ", str(len(SUBJECTS))))
NSEED  = int(os.environ.get("H1431_NSEED", str(len(SEEDS))))
TOP_K, TEMP = 40, 0.7
SUBJECTS = SUBJECTS[:NSUBJ]; SEEDS = SEEDS[:NSEED]
def rel(s):  return f"a relationship about {s}: it tends to be "
def meas(s): return f"something we could observe about {s}: the "

def tag(seed,subj,kind): return f"{seed}|{subj}|{kind}"

def main():
    # resume: tags already in RAW
    done=set()
    if os.path.exists(RAW):
        for ln in open(RAW):
            if "\t" in ln: done.add(ln.split("\t",1)[0])
    jobs=[]
    for seed in SEEDS:
        for subj in SUBJECTS:
            for kind,fn in (("rel",rel),("meas",meas)):
                tg=tag(seed,subj,kind)
                if tg in done: continue
                jobs.append(f"{seed}\t{tg}\t{fn(subj)}")
    print(f"[decode-batch] BIN={BIN} jobs={len(jobs)} (resume-skip {len(done)}) MAXNEW={MAXNEW}", flush=True)
    if jobs:
        open(JOBS,"w").write("\n".join(jobs)+"\n")
        env=dict(os.environ); env["HEXA_MEM_UNLIMITED"]="1"
        cmd=[HEXA,"run",CLI,BIN,JOBS,RAW,str(MAXNEW),str(TOP_K),str(int(TEMP*1000))]
        r=subprocess.run(cmd,env=env,timeout=86400)
        print(f"[decode-batch] hexa rc={r.returncode}", flush=True)
    # convert RAW (tag\ttext) → fragments.jsonl
    out=open(FRAGS,"w")
    for ln in open(RAW):
        if "\t" not in ln: continue
        tg,txt=ln.rstrip("\n").split("\t",1)
        seed,subj,kind=tg.split("|")
        out.write(json.dumps({"seed":int(seed),"subj":subj,"kind":kind,"text":txt})+"\n")
    out.close()
    print("DECODE_BATCH_DONE", flush=True)
if __name__=="__main__": main()
