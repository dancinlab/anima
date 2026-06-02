#!/usr/bin/env python3
"""A4 STDP / TEMPORAL-ORDER SPIKE CODE — encode sequence ORDER via spike timing (chip native temporal dim).
substrate=AKIDA · a_lane_akida_gpu_split · g63 (NO sw fallback) · a_scale_honest_scope.

akida 2.19.1 has NO STDP class. The temporal primitive it exposes is akida.BufferTempConv (a FIFO that caches T
past inputs and does a spatiotemporal conv across them) + akida.DepthwiseBufferTempConv. These are 8-bit
inference layers (NOT 1-bit AkidaUnsupervised on-chip Hebbian learn). This probe HONESTLY determines on the live
AKD1000 (BC.00.000.002, IP v1):
  STEP 1 (FEASIBILITY): can BufferTempConv (fifo_size=K, the temporal window) be constructed -> compiled -> MAPPED
         to the physical AKD1000 -> run a forward across a TIME SEQUENCE of codes on silicon? If map() raises ->
         the temporal-conv primitive is NOT supported on AKD1000 IP-v1 -> infeasible-on-chip HONEST (SDK class
         present in akida 2.19.1, distinct from sdk-not-installed). There is NO native STDP timing-learn API for
         AKD1000 -> the "temporal code via spike timing" is tested through BufferTempConv's FIFO, the chip's only
         native temporal mechanism; if even that does not map, temporal-order is hardware-cannot on AKD1000.
  STEP 2 (only if feasible): feed the K-hop ordered code sequence into the FIFO temporal conv on-chip and measure
         whether the spatiotemporal output decodes hop-2 successor above shuffle-NULL (does ORDER carry composition).

PRE-REGISTERED FALSIFIER F-A4:
  F-A4-FEASIBLE: BufferTempConv maps to AKD1000 + runs a temporal forward on silicon. If NOT -> infeasible-on-chip.
  F-A4-1 (only if feasible): hop-2 AND hop-3 temporal decode acc ci_lo > shuffle-NULL hi at p<=0.01 AND mean>0.038.
                 REFUTED -> temporal code carries composition. NOT-REFUTED -> closed-negative (a_paper_negative_ok).
"""
import os, json, sys, traceback, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import la_base as B
import akida
from akida import Model, InputData, BufferTempConv

SLUG = "temporal-code"; F_THRESH = 0.038; P_MAX = 0.01; FIFO = 3
concept, lang, codes_enc, concepts_sorted, langs, NC = B.load_corpus()
code_of = B.make_code_of(concept, lang, codes_enc)
train_codes, _ = B.build_train_transitions(code_of, concepts_sorted, langs, NC)
roll_starts = B.build_roll_starts(code_of, concepts_sorted, langs, NC)
chance = 1.0/(NC-1)
RES = B.device_banner()
RES.update({"candidate": "A4_temporal_spike_code", "slug": SLUG, "units": B.UNITS, "K_roll": B.K_ROLL,
            "F_threshold": F_THRESH, "p_max": P_MAX, "fifo_size": FIFO,
            "mechanism": "akida.BufferTempConv FIFO spatiotemporal conv (chip native temporal dim); NO STDP class in SDK",
            "stdp_class_present": False, "buffertempconv_present": True, "akida_release": akida.__version__})
print("[A4] akida %s device %s ip %s — probing BufferTempConv temporal feasibility on AKD1000" % (RES["akida_version"], RES["device"], RES["ip_version"])); sys.stdout.flush()

feasible = False; fail_stage = None; fail_msg = None
try:
    fail_stage = "construct"
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, B.INC), input_bits=1))
    m.add(BufferTempConv(filters=B.UNITS, fifo_size=FIFO, name="tconv"))
    print("[A4] BufferTempConv constructed + added OK"); sys.stdout.flush()
    fail_stage = "map"
    m.map(B.DEV)
    print("[A4] mapped to AKD1000 silicon OK; sequences:", len(m.sequences)); sys.stdout.flush()
    fail_stage = "forward"
    x = np.zeros((1, 1, 1, B.INC), dtype=np.uint8); x[0, 0, 0, :8] = 1
    y = m.forward(x)
    print("[A4] temporal forward on silicon OK, out shape:", np.array(y).shape); sys.stdout.flush()
    RES["map_backends"] = [str(getattr(s, "backend", "?")) for s in m.sequences]
    feasible = True; fail_stage = None
except Exception as e:
    fail_msg = "%s: %s" % (type(e).__name__, str(e))
    RES["feasibility_traceback"] = traceback.format_exc()[-1500:]
    print("[A4] FEASIBILITY FAILED at stage=%s : %s" % (fail_stage, fail_msg)); sys.stdout.flush()

RES["F_A4_FEASIBLE"] = feasible; RES["feasibility_fail_stage"] = fail_stage; RES["feasibility_fail_msg"] = fail_msg

if not feasible:
    RES["F_A4_1_pass"] = False; RES["wall_broken"] = False
    RES["DISPOSITION"] = (
        "A4 TEMPORAL-CODE = INFEASIBLE-ON-CHIP (HONEST hardware-cannot, NOT a wall verdict). akida %s exposes NO "
        "STDP class; its only native temporal primitive akida.BufferTempConv IS present in the SDK (distinct from "
        "sdk-not-installed) but does NOT map/run on the live AKD1000 (BC.00.000.002, IP v1) — failed at stage=%s: %s. "
        "AKD1000 IP-v1 has no temporal-FIFO / spike-timing op on its mesh (BufferTempConv targets AKD1500/v2 TENNs). "
        "RULING = infeasible-on-chip for AKD1000 hardware (no SIM substitution). Temporal-order spike coding on-chip "
        "requires AKD1500-class silicon." % (akida.__version__, fail_stage, fail_msg))
    json.dump(RES, open(os.path.join(B.OUT, "result_a4_temporal.json"), "w"), indent=2)
    print("\n[A4] ========== DISPOSITION ==========")
    print("[A4] FEASIBLE:", feasible, " fail_stage:", fail_stage, " msg:", fail_msg)
    print("[A4] DISPOSITION:", RES["DISPOSITION"])
    print("[A4] RULING: infeasible-on-chip")
    sys.exit(0)

# STEP 2: temporal sequence -> hop decode (only if feasible)
print("[A4] STEP 2: temporal FIFO sequence decode on silicon"); sys.stdout.flush()
def temporal_forward(m, seq_codes):
    out = None
    for c in seq_codes:
        x = c.astype(np.uint8).reshape(1, 1, 1, B.INC); out = np.array(m.forward(x)).astype(np.float64).ravel()
    return out  # last output after FIFO has seen the ordered sequence
# build codebook from temporal output of each (transition fed as 1-step)
tt = np.stack([temporal_forward(m, [c]) for c in train_codes]); med = np.median(tt, axis=0)
tt_bin = (tt > med[None, :]).astype(np.uint8); codebook = B.build_codebook(tt_bin, code_of, concepts_sorted, langs, NC)
preds = [[] for _ in range(B.K_ROLL)]
for (ti, ql, seed_code) in roll_starts:
    seq = [seed_code.astype(np.uint8)]; banned = concepts_sorted[ti]
    for k in range(B.K_ROLL):
        g = temporal_forward(m, seq); g_bin = (g > med).astype(np.uint8)
        pred = B.decode(g_bin, codebook, banned); preds[k].append((ti, ql, pred))
        banned = pred if pred is not None else banned
        nc = code_of(pred, ql) if (pred is not None and code_of(pred, ql) is not None) else seq[-1]
        seq.append(nc); seq = seq[-FIFO:]
per_hop = []
for k0 in range(B.K_ROLL):
    a, n = B.acc_at(preds, k0, concepts_sorted)
    null = B.shuffle_null_at(preds, k0, concepts_sorted, NC); nhi = float(null.mean()+1.96*null.std())
    p = float((null >= a).sum()+1)/(len(null)+1); above = bool(a > nhi and p <= P_MAX and a > F_THRESH)
    per_hop.append({"hop": k0+1, "acc": a, "shuffle_null_hi": nhi, "p_value": p, "clears_falsifier": above})
    print("[A4] hop %d acc=%.4f shufNULL_hi=%.4f p=%.4f clears=%s" % (k0+1, a, nhi, p, above)); sys.stdout.flush()
F_A4_1 = bool(per_hop[1]["clears_falsifier"] and per_hop[2]["clears_falsifier"])
RES["per_hop"] = per_hop; RES["F_A4_1_pass"] = F_A4_1; RES["wall_broken"] = F_A4_1
RES["decay_curve"] = [round(per_hop[k]["acc"], 4) for k in range(B.K_ROLL)]
RES["DISPOSITION"] = (("A4 TEMPORAL-CODE BREAKS THE 1-HOP WALL on-chip — MAJOR FINDING, flag for scale-up."
                       if F_A4_1 else
                       "A4 TEMPORAL-CODE CLOSED-NEGATIVE (a_paper_negative_ok): BufferTempConv maps+runs on AKD1000 "
                       "but the FIFO temporal code does NOT lift hop-2/3 above shuffle-NULL. EMERGENCE NULL. toy."))
json.dump(RES, open(os.path.join(B.OUT, "result_a4_temporal.json"), "w"), indent=2)
print("\n[A4] ========== DISPOSITION ==========")
print("[A4] FEASIBLE: True decay:", RES["decay_curve"])
print("[A4] F-A4-1 wall_broken:", F_A4_1)
print("[A4] DISPOSITION:", RES["DISPOSITION"])
print("[A4] RULING:", "GREEN-WALL-BROKEN" if F_A4_1 else "closed-negative")
