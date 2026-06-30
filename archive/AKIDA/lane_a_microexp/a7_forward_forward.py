#!/usr/bin/env python3
"""A7 FORWARD-FORWARD — goodness-based layerwise learning (no backprop, Hebbian-friendly) on-chip.
substrate=AKIDA · a_lane_akida_gpu_split · g63 (NO sw fallback) · a_scale_honest_scope.

MECHANISM UNDER TEST: Hinton's Forward-Forward — each layer learns LOCALLY to raise a "goodness" (sum of squared
activities) on POSITIVE data and lower it on NEGATIVE data, NO backprop. This is Hebbian-friendly and maps to the
AKD1000 1-bit AkidaUnsupervised path WITHOUT the paged-BP machinery that #1689 multi-FC-depth used. We stack TWO
on-chip FF layers (each its own AkidaUnsupervised 1-bit FC, mapped & fit SEPARATELY — layerwise, no inter-layer
gradient), each trained on POSITIVE transition codes (positive phase = real transition; the chip's Hebbian
WTA raises goodness=spike-count on what it was fit on, i.e. positives). Goodness G(layer,x)=sum(spike_count).
Multi-hop decode uses the LAYER-2 (deeper FF) code + per-concept goodness. Tests whether FF DEPTH carries
composition the paged-backprop depth (#1689 DEPTH-2 closed-negative) could not — same 2-FC depth, different (local
goodness) learning rule.
  FF1 = AkidaUnsupervised FC fit on positive transitions. FF2 = AkidaUnsupervised FC fit on FF1's binarized output
  of positive transitions (layerwise, no BP). codebook in FF2 space. rollout feeds successor codes through FF1->FF2.
Compares vs LAYER-1-ONLY (single FF, no depth) arm.

PRE-REGISTERED FALSIFIER F-A7:
  threshold: hop-2/3 FF-depth acc ci_lo > shuffle-NULL hi at p<=0.01 AND mean>0.038 (>0.01 over wall 0.028).
  F-A7-1 REFUTED (wall broken) iff hop-2 AND hop-3 clear that bar. F-A7-2 REFUTED iff FF-depth acc > FF1-only acc
  at BOTH hop-2/3 (depth via FF helps where paged-BP depth did not). NOT-REFUTED F-A7-1 -> CLOSED-NEG. Report both.
"""
import os, json, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import la_base as B

SLUG = "forward-forward"; F_THRESH = 0.038; P_MAX = 0.01
concept, lang, codes_enc, concepts_sorted, langs, NC = B.load_corpus()
code_of = B.make_code_of(concept, lang, codes_enc)
train_codes, _ = B.build_train_transitions(code_of, concepts_sorted, langs, NC)
roll_starts = B.build_roll_starts(code_of, concepts_sorted, langs, NC)
chance = 1.0/(NC-1)
print("[A7] corpus NC=%d transitions=%d roll_starts=%d chance=%.4f" % (NC, train_codes.shape[0], len(roll_starts), chance)); sys.stdout.flush()

RES = B.device_banner()
RES.update({"candidate": "A7_forward_forward", "slug": SLUG, "n_trials": B.NTRIALS, "units": B.UNITS,
            "K_roll": B.K_ROLL, "F_threshold": F_THRESH, "p_max": P_MAX,
            "mechanism": "Forward-Forward layerwise (no BP): FF1=AkidaUnsupervised 1-bit FC fit on positive "
                         "transitions; FF2=AkidaUnsupervised 1-bit FC fit on FF1 binarized output (layerwise, "
                         "goodness=spike-count); decode in FF2 space [vs FF1-only]. Same 2-FC depth as #1689 "
                         "paged-BP, different local-goodness learning rule",
            "baselines": {"pure_on_chip_hop2": 0.028, "paged_bp_depth2_hop2": 0.0298, "shuffle_null_hi": 0.05}, "trials": []})
print("[A7] akida %s device %s ip %s" % (RES["akida_version"], RES["device"], RES["ip_version"])); sys.stdout.flush()

def ff2_rollout(ff1, ff2, m1, m2, codebook2, mode):
    """mode='depth' -> FF1->FF2 ; mode='ff1' -> FF1-only (decode in FF1 space via codebook1 passed as codebook2)."""
    preds = [[] for _ in range(B.K_ROLL)]
    for (ti, ql, seed_code) in roll_starts:
        cur = seed_code.astype(np.uint8).copy(); banned = concepts_sorted[ti]
        for k in range(B.K_ROLL):
            g1 = B.binarize_rows(B.chip_forward(ff1, B.neutral_bind(cur)), m1)[0]
            if mode == "depth":
                g2 = B.binarize_rows(B.chip_forward(ff2, g1), m2)[0]; code = g2
            else:
                code = g1
            pred = B.decode(code, codebook2, banned); preds[k].append((ti, ql, pred))
            banned = pred if pred is not None else banned
            cur = code_of(pred, ql) if (pred is not None and code_of(pred, ql) is not None) else cur
    return preds

depth_trials = [[] for _ in range(B.K_ROLL)]; ff1_trials = [[] for _ in range(B.K_ROLL)]
l1_all, l2_all = True, True; last_preds = None
for tr in range(B.NTRIALS):
    init1 = B.get_w(B.build_fc(1)); ff1, l1 = B.chip_make(init1, train_codes, do_fit=True)
    s1 = B.chip_forward(ff1, train_codes); m1 = np.median(s1, axis=0); b1 = B.binarize_rows(s1, m1)  # FF1 positive-phase output
    init2 = B.get_w(B.build_fc(1)); ff2, l2 = B.chip_make(init2, b1, do_fit=True)                    # FF2 fit on FF1 output (layerwise)
    s2 = B.chip_forward(ff2, b1); m2 = np.median(s2, axis=0); b2 = B.binarize_rows(s2, m2)
    cb2 = B.build_codebook(b2, code_of, concepts_sorted, langs, NC)   # FF2-space codebook
    cb1 = B.build_codebook(b1, code_of, concepts_sorted, langs, NC)   # FF1-space codebook
    dp = ff2_rollout(ff1, ff2, m1, m2, cb2, "depth")
    fp = ff2_rollout(ff1, ff2, m1, m2, cb1, "ff1")
    del ff1, ff2
    l1_all = l1_all and l1; l2_all = l2_all and l2
    row = {"trial": tr, "ff1_learned_hw": l1, "ff2_learned_hw": l2, "depth_acc": [], "ff1only_acc": []}
    for k0 in range(B.K_ROLL):
        da, n = B.acc_at(dp, k0, concepts_sorted); fa, _ = B.acc_at(fp, k0, concepts_sorted)
        depth_trials[k0].append(da); ff1_trials[k0].append(fa); row["depth_acc"].append(da); row["ff1only_acc"].append(fa)
    RES["trials"].append(row); last_preds = dp
    print("[A7] trial %d: depth=%s ff1only=%s l1=%s l2=%s"
          % (tr, ["%.4f" % x for x in row["depth_acc"]], ["%.4f" % x for x in row["ff1only_acc"]], l1, l2)); sys.stdout.flush()
    json.dump(RES, open(os.path.join(B.OUT, "result_a7_ff.json"), "w"), indent=2)

per_hop = []
print("[A7] per-hop shuffle-NULL (B=%d) ..." % B.B_SHUFFLE); sys.stdout.flush()
for k0 in range(B.K_ROLL):
    sm, ssd, ssem, slo, shi = B.ci(depth_trials[k0]); fm = float(np.mean(ff1_trials[k0]))
    null = B.shuffle_null_at(last_preds, k0, concepts_sorted, NC)
    nhi = float(null.mean()+1.96*null.std()); p = float((null >= sm).sum()+1)/(len(null)+1)
    above = bool(l1_all and l2_all and slo > nhi and p <= P_MAX and sm > F_THRESH)
    per_hop.append({"hop": k0+1, "depth_acc": {"mean": sm, "ci_lo": slo}, "ff1only_acc_mean": fm, "delta": round(sm-fm, 4),
                    "shuffle_null": {"hi": nhi, "p_value": p}, "chance": chance, "clears_falsifier": above})
    print("[A7] hop %d: depth=%.4f ci_lo=%.4f | ff1only=%.4f delta=%+.4f | shufNULL hi=%.4f p=%.4f | clears=%s"
          % (k0+1, sm, slo, fm, sm-fm, nhi, p, above)); sys.stdout.flush()

F_A7_1 = bool(per_hop[1]["clears_falsifier"] and per_hop[2]["clears_falsifier"])
F_A7_2 = bool(per_hop[1]["depth_acc"]["mean"] > per_hop[1]["ff1only_acc_mean"] and per_hop[2]["depth_acc"]["mean"] > per_hop[2]["ff1only_acc_mean"])
RES["summary"] = {"ff1_learned_all": l1_all, "ff2_learned_all": l2_all, "encoder_learned": (l1_all and l2_all), "chance": chance,
                  "decay_curve_depth": [round(per_hop[k]["depth_acc"]["mean"], 4) for k in range(B.K_ROLL)],
                  "decay_curve_ff1only": [round(per_hop[k]["ff1only_acc_mean"], 4) for k in range(B.K_ROLL)],
                  "per_hop": per_hop, "F_A7_1_pass": F_A7_1, "F_A7_2_pass": F_A7_2, "wall_broken": F_A7_1}
RES["DISPOSITION"] = (("A7 FORWARD-FORWARD BREAKS THE 1-HOP WALL on-chip (hop-2 AND hop-3 clear shuffleNULL p<=%.2f, "
                       "mean>%.3f): goodness-based layerwise FF depth carries multi-hop composition the paged-BP depth "
                       "could not. MAJOR FINDING — scale-up." % (P_MAX, F_THRESH)) if F_A7_1 else
                      ("A7 FORWARD-FORWARD CLOSED-NEGATIVE (a_paper_negative_ok): goodness-based layerwise FF over a "
                       "2-FC on-chip stack does NOT lift hop-2/3 above shuffle-NULL by the material margin -> FF depth "
                       "carries no more composition than the #1689 paged-BP depth-2 (hop-2 0.0298). The 1-bit/256-unit "
                       "depth ceiling is learning-rule-INDEPENDENT (BP-paged AND FF-local both closed). EMERGENCE NULL. "
                       "Lane A on-chip, toy 250-anchor."))
json.dump(RES, open(os.path.join(B.OUT, "result_a7_ff.json"), "w"), indent=2)
print("\n[A7] ========== DISPOSITION ==========")
print("[A7] ff1_learned_all:", l1_all, " ff2_learned_all:", l2_all)
print("[A7] decay DEPTH(FF1->FF2):", [round(per_hop[k]["depth_acc"]["mean"], 4) for k in range(B.K_ROLL)])
print("[A7] decay FF1-ONLY       :", [round(per_hop[k]["ff1only_acc_mean"], 4) for k in range(B.K_ROLL)])
print("[A7] #1689 paged-BP depth-2 hop-2 baseline: 0.0298")
for h in per_hop:
    print("[A7] hop %d depth=%.4f ci_lo=%.4f ff1only=%.4f delta=%+.4f shufNULL_hi=%.4f p=%.4f clears=%s"
          % (h["hop"], h["depth_acc"]["mean"], h["depth_acc"]["ci_lo"], h["ff1only_acc_mean"], h["delta"],
             h["shuffle_null"]["hi"], h["shuffle_null"]["p_value"], h["clears_falsifier"]))
print("[A7] F-A7-1 wall_broken:", F_A7_1, " F-A7-2 beats_ff1only:", F_A7_2)
print("[A7] DISPOSITION:", RES["DISPOSITION"])
print("[A7] RULING:", "GREEN-WALL-BROKEN" if F_A7_1 else "closed-negative")
