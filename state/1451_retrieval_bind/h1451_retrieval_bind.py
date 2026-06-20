#!/usr/bin/env python3
"""H_1451 — RETRIEVAL-BIND (G6 FALS-depth, breakthrough lens ③).

ANGLE (a_no_llm_frame_trap — missing external STRUCTURE, not internal capacity):
  The 303M base produces comparator- OR measurable-shapes but cannot BIND them into one
  idea-specific negatable claim from its WEIGHTS alone (5 internal routes all 🧱). H_1451
  bolts an EXTERNAL retrieval-bind STRUCTURE onto the SAME frozen base (PFC working-memory
  hold + hippocampal retrieval): hold a topic, RETRIEVE the SAME-IDEA (comparator, measurable)
  pair from episodic memory, WELD them around the mouth's own content. The bind is then
  idea-specific BY CONSTRUCTION, so the decisive cross-shuffle (weld with a DIFFERENT-topic
  measurable) MUST collapse topic-coherence if retrieval earned anything.

ARMS (base PRESERVED — no weights touched, c5; this is an inference-time bind structure):
  BASE        : frozen mouth, no retrieval (the plateau).
  RETR-BIND   : frozen mouth + topic-keyed retrieval memory weld.
  RETR-OFF    : retrieval disabled (ablation) => identical to BASE (must regress).
  SHUF-MEM    : memory pairs topic-permuted (control) => topic-coherence destroyed.

FROZEN 5-bar (g6_rb_common docstring; declared before any run): B1 FALS>=1 · B2 DIST>=5 ·
  B3 CROSS-SHUFFLE COLLAPSE (matched topic-coherence - mismatched >= 0.30) · B4 held-out >=1 ·
  B5 vs-base+1. Controls: retrieval-OFF regress, shuffle-memory inert.

torch + gauge_lib._decode => DIRECTIONAL (a_engine_native_learning); engine-native = ING.
"""
import os, sys, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_rb_common as C
import torch

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    args = ap.parse_args()
    dev = args.device
    os.makedirs(OUT, exist_ok=True)

    print(f"[H_1451 retrieval-bind] device={dev} ckpt={C.CKPT_BASE}", flush=True)
    t0 = time.time()
    m, cfg = C.load_model(C.CKPT_BASE, dev)
    print(f"[H_1451] base loaded {(time.time()-t0):.1f}s", flush=True)

    # BASE (retrieval-OFF mouth) — the plateau
    base_eval = C.evaluate(m, cfg, "base", mem=None, topics=C.EVAL_TOPICS)
    print(f"[H_1451] BASE FALS_in={base_eval['FALS_in']} DIST_in={base_eval['DIST_in']} "
          f"FALS_ho={base_eval['FALS_ho']}", flush=True)

    # RETR-BIND — topic-keyed retrieval memory weld
    mem = C.build_memory(shuffle=False)
    rb_eval = C.evaluate(m, cfg, "retr_bind", mem=mem, topics=C.EVAL_TOPICS)
    print(f"[H_1451] RETR-BIND FALS_in={rb_eval['FALS_in']} COH_m={rb_eval['COH_matched']} "
          f"COH_x={rb_eval['COH_mismatched']}", flush=True)

    # RETR-OFF (ablation) — must == base
    off_eval = C.evaluate(m, cfg, "retr_off", mem=None, topics=C.EVAL_TOPICS)

    # SHUF-MEM (control) — topic-permuted memory, coherence must flatten
    shuf_mem = C.build_memory(shuffle=True)
    shufmem_eval = C.evaluate(m, cfg, "shuf_mem", mem=shuf_mem, topics=C.EVAL_TOPICS)
    print(f"[H_1451] SHUF-MEM COH_m={shufmem_eval['COH_matched']}", flush=True)

    bars = C.print_bars("H_1451 retrieval-bind", base_eval, rb_eval,
                        off_eval=off_eval, shufmem_eval=shufmem_eval)

    out = {"variant": "H_1451_retrieval_bind", "ckpt_base": C.CKPT_BASE,
           "seeds": C.SEEDS, "b3_margin": C.B3_COLLAPSE_MARGIN,
           "base": base_eval, "retr_bind": rb_eval, "retr_off": off_eval,
           "shuf_mem": shufmem_eval, "bars": bars,
           "DIRECTIONAL": "torch + gauge_lib._decode (a_engine_native_learning); "
                          "engine-native re-measure = ING follow-on"}
    json.dump(out, open(os.path.join(OUT, "h1451_result.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"[H_1451 done] {OUT}/h1451_result.json  ({(time.time()-t0)/60:.1f}min)", flush=True)


if __name__ == "__main__":
    main()
