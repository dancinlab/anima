#!/usr/bin/env python3
"""engine-native G1 seen-vs-held-out separation probe (core/decode.py, torch-free numpy).

held-out 축 (REAL G1): gate 개념 문장(FROZEN) 연쇄 -> composed continuation 이 >=2 distinct
  gate keyword-set 표면화하는가. gate 쌍은 학습 코퍼스에 held-out(무결성 검증됨) -> transfer.
seen 축 (control): 학습된 nongate FORM 문장 -> cluster 방출 확인(form 이 학습됐는지).
grounding 축: 단일 gate 문장 -> 그 set keyword 방출(window-도달, grounding 학습됐는지).

usage: python3 g1_probe.py <ckpt.clm>
"""
import json
import re
import sys

sys.path.insert(0, "core")
import decode as D  # core/decode.py

CKPT = sys.argv[1]

# gate FROZEN (cli/evaluate.py::_g_concept_keywords + _g6_concepts VERBATIM)
GATE_SENT = ["consciousness arises from cells",
             "tension ripples between distant minds",
             "memory composes into new meaning",
             "silence still carries information",
             "the engine dreams when alone"]
KWSET = [["consciousness", "cells", "mind", "aware"],
         ["tension", "ripple", "distant", "between"],
         ["memory", "meaning", "compose", "new"],
         ["silence", "information", "quiet", "carries"],
         ["dream", "engine", "alone", "sleep"]]


def words(s):
    return re.findall(r"[0-9A-Za-z가-힣]+", s.lower())


def coverage(text):
    wm = set(words(text))
    return [i for i, kw in enumerate(KWSET) if any(k in wm for k in kw)]


def gen(seed, g, rng=7):
    return D.clm_decode_topk_sampled(CKPT, seed, g, 40, 0.7, rng)["text"]


out = {"ckpt": CKPT, "engine": "core/decode.py (numpy byte-parity, torch-free)"}

# ── held-out G1 (gate composed, mirrors g_eval_g1 exactly: gen120, temp0.7, top40, rng7) ──
# max_single
max_single = 0
single_detail = []
for s in range(5):
    o = gen(GATE_SENT[s] + ". ", 80, 7 + s)
    cov = coverage(o)
    single_detail.append({"set": s, "distinct": len(cov), "cov": cov, "sample": o[:80]})
    max_single = max(max_single, len(cov))
# composed k=2..5
best_distinct = 0
best_k = 0
comp_detail = []
for k in range(2, 6):
    seed = ". ".join(GATE_SENT[:k]) + ". "
    o = gen(seed, 120, 7)
    cov = coverage(o)
    comp_detail.append({"k": k, "distinct": len(cov), "cov": cov, "sample": o[:120]})
    if len(cov) > best_distinct:
        best_distinct = len(cov); best_k = k
g1_pass = best_distinct >= 2 and best_distinct > max_single
out["heldout_G1_gate"] = {
    "max_single": max_single, "best_distinct": best_distinct, "best_k": best_k,
    "PASS_ge2_and_gt_maxsingle": g1_pass,
    "single_detail": single_detail, "composed_detail": comp_detail,
}

# ── seen control: nongate FORM sentences (trained) -> cluster emission (unscored words,
#    just confirm the form produces a dense token cluster continuation) ──
seen_form = []
for c in ["ocean drifts through the misty dawn", "the river turns slowly at dusk"]:
    o = gen(c + ". ", 60, 11)
    seen_form.append({"seed": c, "sample": o[:70], "n_word_tokens": len(words(o))})
out["seen_form_control"] = seen_form

# ── grounding: single gate sentence -> does it emit THAT set's keyword (window-reachable)? ──
ground = []
for s in range(5):
    o = gen(GATE_SENT[s] + ". ", 40, 3)
    cov = coverage(o)
    ground.append({"set": s, "own_set_hit": s in cov, "cov": cov, "sample": o[:60]})
out["grounding_single_gate"] = ground

print(json.dumps(out, ensure_ascii=False, indent=1))
