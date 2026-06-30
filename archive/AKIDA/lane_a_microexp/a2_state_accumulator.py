#!/usr/bin/env python3
"""A2 ON-CHIP STATE-ACCUMULATOR FEEDBACK — running on-chip spike-count memory trace re-fed each hop.
substrate=AKIDA · a_lane_akida_gpu_split · g63 (NO sw fallback) · a_scale_honest_scope.

MECHANISM UNDER TEST (distinct from PR#1689 input-side bit-majority state-carry): a TRUE on-chip running
SPIKE-COUNT memory trace. We accumulate the chip's RAW spike-count output (the analog forward, NOT just the
binarized code) across hops into a running integer trace, then RE-INJECT the trace as a thresholded 1-bit
context bound into the next hop's input. The state lives in the chip's own spike statistics (count over hops),
not a hand-crafted bit-majority of decoded codes. trace_{k} = trace_{k-1}*decay + spike_count_k ; ctx = (trace >
running_median) ; x_{k+1} = bind(g_bin_k, ctx). Trained transition FC (do_fit=True). Compares vs a NO-TRACE
stateless arm (same chip, same trial) as head-to-head.

PRE-REGISTERED FALSIFIER F-A2 (declared BEFORE run):
  threshold: hop-2/3 trace-feedback acc ci_lo > shuffle-NULL hi at p<=0.01 AND mean>0.038 (>0.01 over wall 0.028).
  F-A2-1 REFUTED (wall broken) iff hop-2 AND hop-3 clear that bar. F-A2-2 REFUTED iff trace acc > no-trace acc
  at BOTH hop-2 and hop-3. NOT-REFUTED on F-A2-1 -> CLOSED-NEGATIVE (a_paper_negative_ok). Report both curves.
"""
import os, json, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import la_base as B

SLUG = "state-accum"; F_THRESH = 0.038; P_MAX = 0.01; DECAY = 0.6
concept, lang, codes_enc, concepts_sorted, langs, NC = B.load_corpus()
code_of = B.make_code_of(concept, lang, codes_enc)
train_codes, _ = B.build_train_transitions(code_of, concepts_sorted, langs, NC)
roll_starts = B.build_roll_starts(code_of, concepts_sorted, langs, NC)
chance = 1.0/(NC-1)
print("[A2] corpus NC=%d transitions=%d roll_starts=%d chance=%.4f" % (NC, train_codes.shape[0], len(roll_starts), chance)); sys.stdout.flush()

def rollout(m, codebook, med, mode):
    preds = [[] for _ in range(B.K_ROLL)]
    for (ti, ql, seed_code) in roll_starts:
        x = B.neutral_bind(seed_code.astype(np.uint8))
        trace = np.zeros(B.UNITS, dtype=np.float64)
        banned = concepts_sorted[ti]
        for k in range(B.K_ROLL):
            g_soft = B.chip_forward(m, x)            # raw spike-count output (analog)
            g_bin = B.binarize_rows(g_soft, med)[0]
            pred = B.decode(g_bin, codebook, banned)
            preds[k].append((ti, ql, pred))
            banned = pred if pred is not None else banned
            if mode == "trace":
                trace = trace*DECAY + g_soft[0]       # running on-chip spike-count memory
                ctx = (trace > np.median(trace)).astype(np.uint8)
                x = B.bind(g_bin, ctx)                # re-inject accumulated spike-count trace as context
            else:
                x = B.neutral_bind(g_bin)             # no-trace stateless baseline
    return preds

RES = B.device_banner()
RES.update({"candidate": "A2_state_accumulator_feedback", "slug": SLUG, "n_trials": B.NTRIALS, "units": B.UNITS,
            "K_roll": B.K_ROLL, "F_threshold": F_THRESH, "p_max": P_MAX, "decay": DECAY,
            "mechanism": "running on-chip SPIKE-COUNT trace (trace=trace*decay+spike_count); ctx=(trace>median); "
                         "x=bind(g_bin,ctx) [vs no-trace stateless]; trained transition FC",
            "baselines": {"pure_on_chip_hop2": 0.028, "shuffle_null_hi": 0.05}, "trials": []})
print("[A2] akida %s device %s ip %s" % (RES["akida_version"], RES["device"], RES["ip_version"])); sys.stdout.flush()

trace_trials = [[] for _ in range(B.K_ROLL)]; base_trials = [[] for _ in range(B.K_ROLL)]
learn_all = True; last_preds = None
for tr in range(B.NTRIALS):
    init = B.get_w(B.build_fc(1))
    m, learned = B.chip_make(init, train_codes, do_fit=True)
    train_soft = B.chip_forward(m, train_codes)
    med = np.median(train_soft, axis=0)
    chip_train_bin = B.binarize_rows(train_soft, med)
    codebook = B.build_codebook(chip_train_bin, code_of, concepts_sorted, langs, NC)
    tp = rollout(m, codebook, med, "trace")
    bp = rollout(m, codebook, med, "none")
    del m
    learn_all = learn_all and learned
    row = {"trial": tr, "learned_hw": learned, "trace_acc": [], "notrace_acc": []}
    for k0 in range(B.K_ROLL):
        ta, n = B.acc_at(tp, k0, concepts_sorted); ba, _ = B.acc_at(bp, k0, concepts_sorted)
        trace_trials[k0].append(ta); base_trials[k0].append(ba); row["trace_acc"].append(ta); row["notrace_acc"].append(ba)
    RES["trials"].append(row); last_preds = tp
    print("[A2] trial %d: trace=%s notrace=%s learn=%s"
          % (tr, ["%.4f" % x for x in row["trace_acc"]], ["%.4f" % x for x in row["notrace_acc"]], learned)); sys.stdout.flush()
    json.dump(RES, open(os.path.join(B.OUT, "result_a2_state_accum.json"), "w"), indent=2)

per_hop = []
print("[A2] per-hop shuffle-NULL (B=%d) ..." % B.B_SHUFFLE); sys.stdout.flush()
for k0 in range(B.K_ROLL):
    sm, ssd, ssem, slo, shi = B.ci(trace_trials[k0]); bm = float(np.mean(base_trials[k0]))
    null = B.shuffle_null_at(last_preds, k0, concepts_sorted, NC)
    nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
    p = float((null >= sm).sum() + 1)/(len(null)+1)
    above = bool(learn_all and slo > nhi and p <= P_MAX and sm > F_THRESH)
    per_hop.append({"hop": k0+1, "trace_acc": {"mean": sm, "ci_lo": slo}, "notrace_acc_mean": bm,
                    "delta": round(sm-bm, 4), "shuffle_null": {"mean": nmean, "hi": nhi, "p_value": p},
                    "chance": chance, "clears_falsifier": above})
    print("[A2] hop %d: trace=%.4f ci_lo=%.4f | notrace=%.4f delta=%+.4f | shufNULL hi=%.4f p=%.4f | clears=%s"
          % (k0+1, sm, slo, bm, sm-bm, nhi, p, above)); sys.stdout.flush()

F_A2_1 = bool(per_hop[1]["clears_falsifier"] and per_hop[2]["clears_falsifier"])
F_A2_2 = bool(per_hop[1]["trace_acc"]["mean"] > per_hop[1]["notrace_acc_mean"] and per_hop[2]["trace_acc"]["mean"] > per_hop[2]["notrace_acc_mean"])
RES["summary"] = {"learned_all_hw": learn_all, "encoder_learned": learn_all, "chance": chance,
                  "decay_curve_trace": [round(per_hop[k]["trace_acc"]["mean"], 4) for k in range(B.K_ROLL)],
                  "decay_curve_notrace": [round(per_hop[k]["notrace_acc_mean"], 4) for k in range(B.K_ROLL)],
                  "per_hop": per_hop, "F_A2_1_pass": F_A2_1, "F_A2_2_pass": F_A2_2, "wall_broken": F_A2_1}
if F_A2_1:
    disp = ("A2 STATE-ACCUMULATOR BREAKS THE 1-HOP WALL on-chip (hop-2 AND hop-3 clear shuffleNULL p<=%.2f, "
            "mean>%.3f): a running on-chip spike-count trace carries multi-hop. MAJOR FINDING — flag for scale-up." % (P_MAX, F_THRESH))
else:
    disp = ("A2 STATE-ACCUMULATOR CLOSED-NEGATIVE (a_paper_negative_ok): running on-chip spike-count feedback "
            "trace does NOT lift hop-2/3 above shuffle-NULL by the material margin -> true on-chip state-accumulation "
            "does not break the 1-hop wall at 1-bit/256-unit. EMERGENCE NULL. Lane A on-chip, toy 250-anchor.")
RES["DISPOSITION"] = disp
json.dump(RES, open(os.path.join(B.OUT, "result_a2_state_accum.json"), "w"), indent=2)
print("\n[A2] ========== DISPOSITION ==========")
print("[A2] learned_all_hw:", learn_all)
print("[A2] decay TRACE   :", [round(per_hop[k]["trace_acc"]["mean"], 4) for k in range(B.K_ROLL)])
print("[A2] decay NOTRACE :", [round(per_hop[k]["notrace_acc_mean"], 4) for k in range(B.K_ROLL)])
for h in per_hop:
    print("[A2] hop %d trace=%.4f ci_lo=%.4f notrace=%.4f delta=%+.4f shufNULL_hi=%.4f p=%.4f clears=%s"
          % (h["hop"], h["trace_acc"]["mean"], h["trace_acc"]["ci_lo"], h["notrace_acc_mean"], h["delta"],
             h["shuffle_null"]["hi"], h["shuffle_null"]["p_value"], h["clears_falsifier"]))
print("[A2] F-A2-1 wall_broken:", F_A2_1, " F-A2-2 beats_notrace:", F_A2_2)
print("[A2] DISPOSITION       :", disp)
print("[A2] RULING:", "GREEN-WALL-BROKEN" if F_A2_1 else "closed-negative")
