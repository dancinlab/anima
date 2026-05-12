"""train_bg_lb.py — BG-LB launcher (raw#37 transient, pod-side).

Thin shim that imports anima_clm_lb_h100.pod_main with the orchestrator-mandated
flag interface: --preset {lb_350m_pretrain|la_350m} --corpus PATH --output DIR.

Launched by tool/bg_lb_engine_ag_orchestrator.hexa Phase 5 via:
    nohup python3 train_bg_lb.py --preset lb_350m_pretrain \
        --corpus /workspace/data/big_corpus.txt \
        --output /workspace/anima_clm_lb/ckpts > train.log 2>&1 &

own 14/16/17/18/22/30/31/33/34/37/38/39/40 strict.
"""
import os, sys, argparse

# Pod path — anima_clm_lb_h100.py uploaded to /workspace/anima_clm_lb/ alongside engine_a_g_arch.py
sys.path.insert(0, "/workspace/anima_clm_lb")

ap = argparse.ArgumentParser(prog="train_bg_lb")
ap.add_argument("--preset", default="lb_350m_pretrain", choices=["lb_350m_pretrain", "la_350m"])
ap.add_argument("--corpus", required=True, help="path to combined big_corpus.txt")
ap.add_argument("--output", required=True, help="output ckpts dir")
args = ap.parse_args()

from anima_clm_lb_h100 import pod_main  # noqa: E402
pod_main(preset=args.preset, corpus_path=args.corpus, output_dir=args.output)
