#!/usr/bin/env python3
"""A5 VSA HYPERVECTOR BINDING — bind/unbind concept(x)role in the 1-bit code (binary HV algebra) on-chip.
substrate=AKIDA · a_lane_akida_gpu_split · g63 (NO sw fallback) · a_scale_honest_scope.

MECHANISM UNDER TEST: 1-bit hypervector algebra (XOR-bind, bundle=bit-majority, permute=roll) is NATIVE to the
chip's 1-bit code domain. We build a COMPOSITIONAL multi-hop query as a bound/bundled hypervector and let the
on-chip TRAINED FC act as the cleanup/transition memory. Concretely, the multi-hop trajectory is encoded as a
single VSA expression: hop-k query = permute^k(seed) XOR-bundle(history of produced codes), and the on-chip FC
(trained on transitions) cleans it up to the next successor codebook entry. The binding ALGEBRA supplies the
compositional structure (role=permutation power encodes hop index, filler=concept code); the chip supplies the
nonlinear cleanup. Tests whether VSA composition + 1-bit chip cleanup gives multi-hop the stateless FC could not.
  permute(v, r) = roll(v, P*r) ; bundle(a,b) = bit_majority -> for 2: a|b tilt; bind(a,b)=a XOR roll(b,SHIFT).
  hop-k input x_k = bind( permute(g_bin_{k-1}, k) , bundle_history_k )  -> carries role-indexed compositional state.
Trained transition FC; codebook = successor centroids. Compares vs a NO-VSA stateless arm (same chip/trial).

PRE-REGISTERED FALSIFIER F-A5:
  threshold: hop-2/3 VSA acc ci_lo > shuffle-NULL hi at p<=0.01 AND mean>0.038 (>0.01 over wall 0.028).
  F-A5-1 REFUTED (wall broken) iff hop-2 AND hop-3 clear that bar. F-A5-2 REFUTED iff VSA acc > no-VSA acc at
  BOTH hop-2/3. NOT-REFUTED on F-A5-1 -> CLOSED-NEGATIVE (a_paper_negative_ok). Report both curves.
"""
import os, json, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import la_base as B

SLUG = "vsa-binding"; F_THRESH = 0.038; P_MAX = 0.01; PERM = 53  # permutation stride for role-power
concept, lang, codes_enc, concepts_sorted, langs, NC = B.load_corpus()
code_of = B.make_code_of(concept, lang, codes_enc)
train_codes, _ = B.build_train_transitions(code_of, concepts_sorted, langs, NC)
roll_starts = B.build_roll_starts(code_of, concepts_sorted, langs, NC)
chance = 1.0/(NC-1)
print("[A5] corpus NC=%d transitions=%d roll_starts=%d chance=%.4f" % (NC, train_codes.shape[0], len(roll_starts), chance)); sys.stdout.flush()

def permute(v, r):  # role = permutation power (hop index)
    return np.roll(v.astype(np.uint8), (PERM*r) % B.INC)
def bundle(a, b):   # VSA bundling = bit-majority of two (tilt toward agreement)
    return ((a.astype(np.int32) + b.astype(np.int32)) >= 1).astype(np.uint8)  # OR-bundle (superpose)

def rollout(m, codebook, med, mode):
    preds = [[] for _ in range(B.K_ROLL)]
    for (ti, ql, seed_code) in roll_starts:
        x = B.neutral_bind(seed_code.astype(np.uint8))
        hist = seed_code.astype(np.uint8).copy()
        banned = concepts_sorted[ti]
        for k in range(B.K_ROLL):
            g_soft = B.chip_forward(m, x); g_bin = B.binarize_rows(g_soft, med)[0]
            pred = B.decode(g_bin, codebook, banned); preds[k].append((ti, ql, pred))
            banned = pred if pred is not None else banned
            if mode == "vsa":
                hist = bundle(hist, g_bin)                      # superpose produced code into trajectory HV
                x = B.bind(permute(g_bin, k+1), hist)           # role-indexed (permute^k) bound with bundled history
            else:
                x = B.neutral_bind(g_bin)
    return preds

RES = B.device_banner()
RES.update({"candidate": "A5_vsa_hypervector_binding", "slug": SLUG, "n_trials": B.NTRIALS, "units": B.UNITS,
            "K_roll": B.K_ROLL, "F_threshold": F_THRESH, "p_max": P_MAX, "perm_stride": PERM,
            "mechanism": "1-bit VSA: x=bind(permute(g_bin,hop), bundle_history); permute=roll(P*r), bundle=OR-superpose, "
                         "bind=XOR-roll; on-chip trained FC = cleanup memory [vs no-VSA stateless]",
            "baselines": {"pure_on_chip_hop2": 0.028, "shuffle_null_hi": 0.05}, "trials": []})
print("[A5] akida %s device %s ip %s" % (RES["akida_version"], RES["device"], RES["ip_version"])); sys.stdout.flush()

vsa_trials = [[] for _ in range(B.K_ROLL)]; base_trials = [[] for _ in range(B.K_ROLL)]
learn_all = True; last_preds = None
for tr in range(B.NTRIALS):
    init = B.get_w(B.build_fc(1))
    m, learned = B.chip_make(init, train_codes, do_fit=True)
    train_soft = B.chip_forward(m, train_codes); med = np.median(train_soft, axis=0)
    chip_train_bin = B.binarize_rows(train_soft, med)
    codebook = B.build_codebook(chip_train_bin, code_of, concepts_sorted, langs, NC)
    vp = rollout(m, codebook, med, "vsa"); bp = rollout(m, codebook, med, "none")
    del m
    learn_all = learn_all and learned
    row = {"trial": tr, "learned_hw": learned, "vsa_acc": [], "novsa_acc": []}
    for k0 in range(B.K_ROLL):
        va, n = B.acc_at(vp, k0, concepts_sorted); ba, _ = B.acc_at(bp, k0, concepts_sorted)
        vsa_trials[k0].append(va); base_trials[k0].append(ba); row["vsa_acc"].append(va); row["novsa_acc"].append(ba)
    RES["trials"].append(row); last_preds = vp
    print("[A5] trial %d: vsa=%s novsa=%s learn=%s" % (tr, ["%.4f" % x for x in row["vsa_acc"]], ["%.4f" % x for x in row["novsa_acc"]], learned)); sys.stdout.flush()
    json.dump(RES, open(os.path.join(B.OUT, "result_a5_vsa.json"), "w"), indent=2)

per_hop = []
print("[A5] per-hop shuffle-NULL (B=%d) ..." % B.B_SHUFFLE); sys.stdout.flush()
for k0 in range(B.K_ROLL):
    sm, ssd, ssem, slo, shi = B.ci(vsa_trials[k0]); bm = float(np.mean(base_trials[k0]))
    null = B.shuffle_null_at(last_preds, k0, concepts_sorted, NC)
    nhi = float(null.mean()+1.96*null.std()); p = float((null >= sm).sum()+1)/(len(null)+1)
    above = bool(learn_all and slo > nhi and p <= P_MAX and sm > F_THRESH)
    per_hop.append({"hop": k0+1, "vsa_acc": {"mean": sm, "ci_lo": slo}, "novsa_acc_mean": bm, "delta": round(sm-bm, 4),
                    "shuffle_null": {"hi": nhi, "p_value": p}, "chance": chance, "clears_falsifier": above})
    print("[A5] hop %d: vsa=%.4f ci_lo=%.4f | novsa=%.4f delta=%+.4f | shufNULL hi=%.4f p=%.4f | clears=%s"
          % (k0+1, sm, slo, bm, sm-bm, nhi, p, above)); sys.stdout.flush()

F_A5_1 = bool(per_hop[1]["clears_falsifier"] and per_hop[2]["clears_falsifier"])
F_A5_2 = bool(per_hop[1]["vsa_acc"]["mean"] > per_hop[1]["novsa_acc_mean"] and per_hop[2]["vsa_acc"]["mean"] > per_hop[2]["novsa_acc_mean"])
RES["summary"] = {"learned_all_hw": learn_all, "encoder_learned": learn_all, "chance": chance,
                  "decay_curve_vsa": [round(per_hop[k]["vsa_acc"]["mean"], 4) for k in range(B.K_ROLL)],
                  "decay_curve_novsa": [round(per_hop[k]["novsa_acc_mean"], 4) for k in range(B.K_ROLL)],
                  "per_hop": per_hop, "F_A5_1_pass": F_A5_1, "F_A5_2_pass": F_A5_2, "wall_broken": F_A5_1}
RES["DISPOSITION"] = (("A5 VSA-BINDING BREAKS THE 1-HOP WALL on-chip (hop-2 AND hop-3 clear shuffleNULL p<=%.2f, "
                       "mean>%.3f): 1-bit hypervector binding algebra + chip cleanup carries multi-hop composition. "
                       "MAJOR FINDING — flag for scale-up." % (P_MAX, F_THRESH)) if F_A5_1 else
                      ("A5 VSA-BINDING CLOSED-NEGATIVE (a_paper_negative_ok): 1-bit XOR-bind/bundle/permute "
                       "hypervector algebra with on-chip cleanup does NOT lift hop-2/3 above shuffle-NULL by the "
                       "material margin -> binding algebra gives no compositional multi-hop at 1-bit/256-unit. "
                       "EMERGENCE NULL. Lane A on-chip, toy 250-anchor."))
json.dump(RES, open(os.path.join(B.OUT, "result_a5_vsa.json"), "w"), indent=2)
print("\n[A5] ========== DISPOSITION ==========")
print("[A5] learned_all_hw:", learn_all)
print("[A5] decay VSA   :", [round(per_hop[k]["vsa_acc"]["mean"], 4) for k in range(B.K_ROLL)])
print("[A5] decay NOVSA :", [round(per_hop[k]["novsa_acc_mean"], 4) for k in range(B.K_ROLL)])
for h in per_hop:
    print("[A5] hop %d vsa=%.4f ci_lo=%.4f novsa=%.4f delta=%+.4f shufNULL_hi=%.4f p=%.4f clears=%s"
          % (h["hop"], h["vsa_acc"]["mean"], h["vsa_acc"]["ci_lo"], h["novsa_acc_mean"], h["delta"],
             h["shuffle_null"]["hi"], h["shuffle_null"]["p_value"], h["clears_falsifier"]))
print("[A5] F-A5-1 wall_broken:", F_A5_1, " F-A5-2 beats_novsa:", F_A5_2)
print("[A5] DISPOSITION:", RES["DISPOSITION"])
print("[A5] RULING:", "GREEN-WALL-BROKEN" if F_A5_1 else "closed-negative")
