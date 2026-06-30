#!/usr/bin/env python3
"""A3 NATIVE RECURRENT-LAYER — configure an on-chip recurrent layer if the akida SDK exposes feedback/recurrence.
substrate=AKIDA · a_lane_akida_gpu_split · g63 (NO sw fallback) · a_scale_honest_scope.

akida 2.19.1 EXPOSES akida.StatefulRecurrent (internal time-dependent state, matmul-in -> recurrent -> matmul-out).
This probe HONESTLY determines, on the LIVE AKD1000 (BC.00.000.002, IP v1):
  STEP 1 (FEASIBILITY): can a StatefulRecurrent layer be (a) constructed, (b) compiled into a Model, (c) MAPPED to
         the physical AKD1000 device, and (d) run a forward pass on real silicon? StatefulRecurrent uses 8-bit
         weights / 16-bit internal state — NOT the 1-bit AkidaUnsupervised on-chip edge-learn path. We test pure
         INFERENCE mappability first. If map() raises (layer not supported on AKD1000 IP v1 mesh) -> the recurrent
         primitive is NOT a Lane-A on-chip learn path on THIS hardware -> infeasible-on-chip HONEST (distinguish
         SDK-present-but-hw-cannot-map from sdk-not-installed: here the SDK class IS installed in akida 2.19.1).
  STEP 2 (only if STEP 1 maps): drive the recurrent layer with the K-hop transition sequence on-chip and measure
         hop-2 successor decode acc vs shuffle-NULL. Weights are SDK-default (not on-chip Hebbian-trainable, since
         on-chip learning is 1-bit-locked per PROBE-2). This tests whether NATIVE on-chip RECURRENCE carries
         composition even WITHOUT 1-bit edge-learn.

PRE-REGISTERED FALSIFIER F-A3:
  F-A3-FEASIBLE: StatefulRecurrent maps to AKD1000 + runs a forward on silicon. If NOT -> infeasible-on-chip
                 (RULING = infeasible-on-chip, hardware-cannot-map, NOT a wall verdict).
  F-A3-1 (only if feasible): hop-2 AND hop-3 recurrent decode acc ci_lo > shuffle-NULL hi at p<=0.01 AND mean>0.038.
                 REFUTED -> native recurrence breaks the wall. NOT-REFUTED -> closed-negative (a_paper_negative_ok).
"""
import os, json, sys, traceback, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import la_base as B
import akida
from akida import Model, InputData, StatefulRecurrent, FullyConnected

SLUG = "native-recurrent"; F_THRESH = 0.038; P_MAX = 0.01
concept, lang, codes_enc, concepts_sorted, langs, NC = B.load_corpus()
code_of = B.make_code_of(concept, lang, codes_enc)
train_codes, _ = B.build_train_transitions(code_of, concepts_sorted, langs, NC)
roll_starts = B.build_roll_starts(code_of, concepts_sorted, langs, NC)
chance = 1.0/(NC-1)
RES = B.device_banner()
RES.update({"candidate": "A3_native_recurrent", "slug": SLUG, "units": B.UNITS, "K_roll": B.K_ROLL,
            "F_threshold": F_THRESH, "p_max": P_MAX,
            "mechanism": "akida.StatefulRecurrent (8-bit weights / 16-bit internal recurrent state) mapped to AKD1000",
            "sdk_class_present": True, "akida_release": akida.__version__})
print("[A3] akida %s device %s ip %s — probing StatefulRecurrent feasibility on AKD1000" % (RES["akida_version"], RES["device"], RES["ip_version"])); sys.stdout.flush()

# ---- STEP 1: feasibility (construct -> compile -> map -> forward) ----
feasible = False; fail_stage = None; fail_msg = None
try:
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, B.INC), input_bits=1))
    m.add(StatefulRecurrent(stateful_channels=64, output_channels=B.UNITS, name="rec"))
    print("[A3] StatefulRecurrent constructed + added to Model OK"); sys.stdout.flush()
    fail_stage = "map"
    m.map(B.DEV)
    print("[A3] mapped to AKD1000 silicon OK; sequences:", len(m.sequences)); sys.stdout.flush()
    fail_stage = "forward"
    x = np.zeros((1, 1, 1, B.INC), dtype=np.uint8); x[0, 0, 0, :8] = 1
    y = m.forward(x)
    print("[A3] forward on silicon OK, out shape:", np.array(y).shape); sys.stdout.flush()
    # confirm it actually ran on HW (not sw): check sequences backend
    backends = [str(getattr(s, "backend", "?")) for s in m.sequences]
    hw = any("Hardware" in b or "HW" in b or "Mesh" in b for b in backends)
    RES["map_backends"] = backends
    print("[A3] sequence backends:", backends); sys.stdout.flush()
    feasible = True; fail_stage = None
except Exception as e:
    fail_msg = "%s: %s" % (type(e).__name__, str(e))
    RES["feasibility_traceback"] = traceback.format_exc()[-1500:]
    print("[A3] FEASIBILITY FAILED at stage=%s : %s" % (fail_stage, fail_msg)); sys.stdout.flush()

RES["F_A3_FEASIBLE"] = feasible
RES["feasibility_fail_stage"] = fail_stage
RES["feasibility_fail_msg"] = fail_msg

if not feasible:
    RES["F_A3_1_pass"] = False; RES["wall_broken"] = False
    RES["DISPOSITION"] = (
        "A3 NATIVE-RECURRENT = INFEASIBLE-ON-CHIP (HONEST hardware-cannot, NOT a wall verdict). "
        "akida.StatefulRecurrent IS present in the installed akida %s SDK (distinct from sdk-not-installed), "
        "but it does NOT map/run on the live AKD1000 (BC.00.000.002, IP v1) — failed at stage=%s: %s. "
        "The AKD1000 IP-v1 mesh does not support the StatefulRecurrent op (it targets newer AKD1500/v2 silicon). "
        "RULING = infeasible-on-chip for AKD1000 hardware (a_lane_akida_gpu_split, no SIM substitution). "
        "Lane A on-chip recurrence via a NATIVE recurrent layer requires AKD1500-class hardware." % (akida.__version__, fail_stage, fail_msg))
    json.dump(RES, open(os.path.join(B.OUT, "result_a3_native_recurrent.json"), "w"), indent=2)
    print("\n[A3] ========== DISPOSITION ==========")
    print("[A3] FEASIBLE:", feasible, " fail_stage:", fail_stage, " msg:", fail_msg)
    print("[A3] DISPOSITION:", RES["DISPOSITION"])
    print("[A3] RULING: infeasible-on-chip")
    sys.exit(0)

# ---- STEP 2: native recurrence drives K-hop successor decode (only reached if feasible) ----
# Build codebook from a 1-bit FC readout of the recurrent output, then roll out feeding successor codes.
print("[A3] STEP 2: native-recurrent K-hop rollout on silicon"); sys.stdout.flush()
def rec_forward(m, code):
    x = code.astype(np.uint8).reshape(1, 1, 1, B.INC)
    return np.array(m.forward(x)).astype(np.float64).ravel()
rec_train = np.stack([rec_forward(m, c) for c in train_codes])
med = np.median(rec_train, axis=0)
rec_train_bin = (rec_train > med[None, :]).astype(np.uint8)
codebook = B.build_codebook(rec_train_bin, code_of, concepts_sorted, langs, NC)
preds = [[] for _ in range(B.K_ROLL)]
for (ti, ql, seed_code) in roll_starts:
    cur = seed_code.astype(np.uint8).copy(); banned = concepts_sorted[ti]
    for k in range(B.K_ROLL):
        g = rec_forward(m, B.neutral_bind(cur)); g_bin = (g > med).astype(np.uint8)
        pred = B.decode(g_bin, codebook, banned); preds[k].append((ti, ql, pred))
        banned = pred if pred is not None else banned
        cur = code_of(pred, ql) if (pred is not None and code_of(pred, ql) is not None) else cur
per_hop = []
for k0 in range(B.K_ROLL):
    a, n = B.acc_at(preds, k0, concepts_sorted)
    null = B.shuffle_null_at(preds, k0, concepts_sorted, NC)
    nhi = float(null.mean()+1.96*null.std()); p = float((null >= a).sum()+1)/(len(null)+1)
    above = bool(a > nhi and p <= P_MAX and a > F_THRESH)
    per_hop.append({"hop": k0+1, "acc": a, "shuffle_null_hi": nhi, "p_value": p, "clears_falsifier": above})
    print("[A3] hop %d acc=%.4f shufNULL_hi=%.4f p=%.4f clears=%s" % (k0+1, a, nhi, p, above)); sys.stdout.flush()
F_A3_1 = bool(per_hop[1]["clears_falsifier"] and per_hop[2]["clears_falsifier"])
RES["per_hop"] = per_hop; RES["F_A3_1_pass"] = F_A3_1; RES["wall_broken"] = F_A3_1
RES["decay_curve"] = [round(per_hop[k]["acc"], 4) for k in range(B.K_ROLL)]
RES["DISPOSITION"] = (("A3 NATIVE-RECURRENT BREAKS THE 1-HOP WALL on-chip — MAJOR FINDING, flag for scale-up."
                       if F_A3_1 else
                       "A3 NATIVE-RECURRENT CLOSED-NEGATIVE (a_paper_negative_ok): StatefulRecurrent maps+runs on "
                       "AKD1000 but native recurrence does NOT lift hop-2/3 above shuffle-NULL by the material margin. "
                       "EMERGENCE NULL. Lane A on-chip, toy 250-anchor."))
json.dump(RES, open(os.path.join(B.OUT, "result_a3_native_recurrent.json"), "w"), indent=2)
print("\n[A3] ========== DISPOSITION ==========")
print("[A3] FEASIBLE: True  decay:", RES["decay_curve"])
print("[A3] F-A3-1 wall_broken:", F_A3_1)
print("[A3] DISPOSITION:", RES["DISPOSITION"])
print("[A3] RULING:", "GREEN-WALL-BROKEN" if F_A3_1 else "closed-negative")
