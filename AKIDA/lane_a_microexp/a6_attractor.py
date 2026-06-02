#!/usr/bin/env python3
"""A6 ATTRACTOR / HOPFIELD — train concept fixed-point attractors on-chip (1-bit), transition = attractor hop.
substrate=AKIDA · a_lane_akida_gpu_split · g63 (NO sw fallback) · a_scale_honest_scope.

MECHANISM UNDER TEST: an associative/Hopfield-style settling dynamic on-chip. The trained 1-bit FC is used as a
RECURRENT cleanup operator: from a noisy/partial input, iterate g_{i+1} = binarize(chip_forward(bind state)) until
the code SETTLES to a fixed point (attractor), then read the settled code's successor. Multi-hop = chain of
attractor settles. The FC is trained as an auto/hetero-associative memory: train on concept->successor so that
each settle pulls toward the successor basin. We run S settling iterations per hop (the chip IS the recurrent
energy-descent operator). Tests whether attractor SETTLING (a genuine on-chip recurrent dynamic) lifts multi-hop.
  settle: y_0 = code ; y_{i+1} = binarize(chip_forward(bind(y_i, seed_anchor))) ; stop when y stabilizes or S reached.
Trained transition FC; codebook = successor centroids. Compares vs NO-SETTLE (S=1) stateless arm (same chip/trial).

PRE-REGISTERED FALSIFIER F-A6:
  threshold: hop-2/3 attractor acc ci_lo > shuffle-NULL hi at p<=0.01 AND mean>0.038 (>0.01 over wall 0.028).
  F-A6-1 REFUTED (wall broken) iff hop-2 AND hop-3 clear that bar. F-A6-2 REFUTED iff settle acc > no-settle acc
  at BOTH hop-2/3. NOT-REFUTED on F-A6-1 -> CLOSED-NEGATIVE (a_paper_negative_ok). Report both curves + settle stats.
"""
import os, json, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import la_base as B

SLUG = "attractor"; F_THRESH = 0.038; P_MAX = 0.01; S_SETTLE = 4
concept, lang, codes_enc, concepts_sorted, langs, NC = B.load_corpus()
code_of = B.make_code_of(concept, lang, codes_enc)
train_codes, _ = B.build_train_transitions(code_of, concepts_sorted, langs, NC)
roll_starts = B.build_roll_starts(code_of, concepts_sorted, langs, NC)
chance = 1.0/(NC-1)
print("[A6] corpus NC=%d transitions=%d roll_starts=%d chance=%.4f S_settle=%d" % (NC, train_codes.shape[0], len(roll_starts), chance, S_SETTLE)); sys.stdout.flush()

def settle(m, code, anchor, med, S):
    """recurrent attractor settling: iterate chip cleanup until fixed point or S steps. returns (settled_bin, steps)."""
    y = code.astype(np.uint8).copy()
    for i in range(S):
        g = B.chip_forward(m, B.bind(y, anchor)); yn = B.binarize_rows(g, med)[0]
        if np.array_equal(yn, y): return yn, i+1
        y = yn
    return y, S

def rollout(m, codebook, med, S):
    preds = [[] for _ in range(B.K_ROLL)]; settle_steps = []
    for (ti, ql, seed_code) in roll_starts:
        anchor = seed_code.astype(np.uint8).copy(); y = seed_code.astype(np.uint8).copy()
        banned = concepts_sorted[ti]
        for k in range(B.K_ROLL):
            settled, steps = settle(m, y, anchor, med, S); settle_steps.append(steps)
            pred = B.decode(settled, codebook, banned); preds[k].append((ti, ql, pred))
            banned = pred if pred is not None else banned
            y = code_of(pred, ql) if (pred is not None and code_of(pred, ql) is not None) else settled
    return preds, float(np.mean(settle_steps))

RES = B.device_banner()
RES.update({"candidate": "A6_attractor_hopfield", "slug": SLUG, "n_trials": B.NTRIALS, "units": B.UNITS,
            "K_roll": B.K_ROLL, "F_threshold": F_THRESH, "p_max": P_MAX, "s_settle": S_SETTLE,
            "mechanism": "on-chip recurrent attractor settling: y=binarize(chip_forward(bind(y,anchor))) iterated to "
                         "fixed point (S=%d); transition=attractor hop [vs no-settle S=1]" % S_SETTLE,
            "baselines": {"pure_on_chip_hop2": 0.028, "shuffle_null_hi": 0.05}, "trials": []})
print("[A6] akida %s device %s ip %s" % (RES["akida_version"], RES["device"], RES["ip_version"])); sys.stdout.flush()

att_trials = [[] for _ in range(B.K_ROLL)]; base_trials = [[] for _ in range(B.K_ROLL)]
learn_all = True; last_preds = None; settle_mean = 0.0
for tr in range(B.NTRIALS):
    init = B.get_w(B.build_fc(1))
    m, learned = B.chip_make(init, train_codes, do_fit=True)
    train_soft = B.chip_forward(m, train_codes); med = np.median(train_soft, axis=0)
    chip_train_bin = B.binarize_rows(train_soft, med)
    codebook = B.build_codebook(chip_train_bin, code_of, concepts_sorted, langs, NC)
    ap, smean = rollout(m, codebook, med, S_SETTLE); bp, _ = rollout(m, codebook, med, 1)
    del m
    learn_all = learn_all and learned; settle_mean = smean
    row = {"trial": tr, "learned_hw": learned, "attractor_acc": [], "nosettle_acc": [], "mean_settle_steps": smean}
    for k0 in range(B.K_ROLL):
        aa, n = B.acc_at(ap, k0, concepts_sorted); ba, _ = B.acc_at(bp, k0, concepts_sorted)
        att_trials[k0].append(aa); base_trials[k0].append(ba); row["attractor_acc"].append(aa); row["nosettle_acc"].append(ba)
    RES["trials"].append(row); last_preds = ap
    print("[A6] trial %d: attractor=%s nosettle=%s settle_steps=%.2f learn=%s"
          % (tr, ["%.4f" % x for x in row["attractor_acc"]], ["%.4f" % x for x in row["nosettle_acc"]], smean, learned)); sys.stdout.flush()
    json.dump(RES, open(os.path.join(B.OUT, "result_a6_attractor.json"), "w"), indent=2)

per_hop = []
print("[A6] per-hop shuffle-NULL (B=%d) ..." % B.B_SHUFFLE); sys.stdout.flush()
for k0 in range(B.K_ROLL):
    sm, ssd, ssem, slo, shi = B.ci(att_trials[k0]); bm = float(np.mean(base_trials[k0]))
    null = B.shuffle_null_at(last_preds, k0, concepts_sorted, NC)
    nhi = float(null.mean()+1.96*null.std()); p = float((null >= sm).sum()+1)/(len(null)+1)
    above = bool(learn_all and slo > nhi and p <= P_MAX and sm > F_THRESH)
    per_hop.append({"hop": k0+1, "attractor_acc": {"mean": sm, "ci_lo": slo}, "nosettle_acc_mean": bm, "delta": round(sm-bm, 4),
                    "shuffle_null": {"hi": nhi, "p_value": p}, "chance": chance, "clears_falsifier": above})
    print("[A6] hop %d: attractor=%.4f ci_lo=%.4f | nosettle=%.4f delta=%+.4f | shufNULL hi=%.4f p=%.4f | clears=%s"
          % (k0+1, sm, slo, bm, sm-bm, nhi, p, above)); sys.stdout.flush()

F_A6_1 = bool(per_hop[1]["clears_falsifier"] and per_hop[2]["clears_falsifier"])
F_A6_2 = bool(per_hop[1]["attractor_acc"]["mean"] > per_hop[1]["nosettle_acc_mean"] and per_hop[2]["attractor_acc"]["mean"] > per_hop[2]["nosettle_acc_mean"])
RES["summary"] = {"learned_all_hw": learn_all, "encoder_learned": learn_all, "chance": chance, "mean_settle_steps": settle_mean,
                  "decay_curve_attractor": [round(per_hop[k]["attractor_acc"]["mean"], 4) for k in range(B.K_ROLL)],
                  "decay_curve_nosettle": [round(per_hop[k]["nosettle_acc_mean"], 4) for k in range(B.K_ROLL)],
                  "per_hop": per_hop, "F_A6_1_pass": F_A6_1, "F_A6_2_pass": F_A6_2, "wall_broken": F_A6_1}
RES["DISPOSITION"] = (("A6 ATTRACTOR/HOPFIELD BREAKS THE 1-HOP WALL on-chip (hop-2 AND hop-3 clear shuffleNULL "
                       "p<=%.2f, mean>%.3f): on-chip recurrent settling carries multi-hop. MAJOR FINDING — scale-up." % (P_MAX, F_THRESH))
                      if F_A6_1 else
                      ("A6 ATTRACTOR/HOPFIELD CLOSED-NEGATIVE (a_paper_negative_ok): on-chip recurrent attractor "
                       "settling (S=%d) does NOT lift hop-2/3 above shuffle-NULL by the material margin -> the 1-bit "
                       "Hebbian FC has no usable energy-descent basin structure for successors at 256-unit. "
                       "EMERGENCE NULL. Lane A on-chip, toy 250-anchor." % S_SETTLE))
json.dump(RES, open(os.path.join(B.OUT, "result_a6_attractor.json"), "w"), indent=2)
print("\n[A6] ========== DISPOSITION ==========")
print("[A6] learned_all_hw:", learn_all, " mean_settle_steps=%.2f" % settle_mean)
print("[A6] decay ATTRACTOR:", [round(per_hop[k]["attractor_acc"]["mean"], 4) for k in range(B.K_ROLL)])
print("[A6] decay NOSETTLE :", [round(per_hop[k]["nosettle_acc_mean"], 4) for k in range(B.K_ROLL)])
for h in per_hop:
    print("[A6] hop %d attractor=%.4f ci_lo=%.4f nosettle=%.4f delta=%+.4f shufNULL_hi=%.4f p=%.4f clears=%s"
          % (h["hop"], h["attractor_acc"]["mean"], h["attractor_acc"]["ci_lo"], h["nosettle_acc_mean"], h["delta"],
             h["shuffle_null"]["hi"], h["shuffle_null"]["p_value"], h["clears_falsifier"]))
print("[A6] F-A6-1 wall_broken:", F_A6_1, " F-A6-2 beats_nosettle:", F_A6_2)
print("[A6] DISPOSITION:", RES["DISPOSITION"])
print("[A6] RULING:", "GREEN-WALL-BROKEN" if F_A6_1 else "closed-negative")
