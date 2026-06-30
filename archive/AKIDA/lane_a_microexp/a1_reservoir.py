#!/usr/bin/env python3
"""A1 RESERVOIR / ECHO-STATE — fixed random recurrent on-chip FC as reservoir + tiny trained readout.
substrate=AKIDA · a_lane_akida_gpu_split · g63 (NO sw fallback) · a_scale_honest_scope (toy 250-anchor / 256-unit).

MECHANISM UNDER TEST: does FIXED on-chip recurrence (an UNTRAINED reservoir FC whose binarized output is fed back
into its own input each hop) + a SEPARATE TRAINED on-chip readout FC lift hop-2 above the 1-hop wall?
  - reservoir R = build_fc(1), do_fit=False  -> FIXED RANDOM 1-bit projection (echo-state: weights NOT trained).
  - echo recurrence: state_{k} = R( bind(code_k, state_{k-1}) ) binarized ; state carries history on-chip.
  - readout FC = build_fc(1), do_fit=True on (reservoir-state-of-transition -> successor) -> TRAINED 1-bit readout.
  - codebook is built in the READOUT's output space (successor centroids of readout(reservoir(transition))).
  - rollout: each hop, drive reservoir with the echo-recurrent input, read out, decode successor, re-encode, feed back.
Everything else (encoder, binding, decode, NULL, CI, 8 trials, K=3) byte-matches la_base.

PRE-REGISTERED FALSIFIER F-A1 (declared BEFORE run):
  threshold: hop-2 reservoir-readout acc ci_lo > shuffle-NULL hi at p<=0.01 AND mean materially > 0.028 (pure wall)
             by the pre-registered material margin >0.01 (>1 percentage point absolute over 0.028).
  F-A1-1 REFUTED (wall broken) iff hop-2 AND hop-3: state_acc ci_lo > shuffle_null hi AND p<=0.01 AND mean>0.038.
  F-A1-1 NOT-REFUTED -> reservoir/echo-state CLOSED-NEGATIVE on-chip (a_paper_negative_ok).
  HONEST: report decay curve, per-hop NULL/p, learned_hw flags for BOTH reservoir(False) + readout(True).
"""
import os, json, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import la_base as B

SLUG = "reservoir"
F_THRESH = 0.038  # material: >0.01 over pure-on-chip wall 0.028
P_MAX = 0.01

concept, lang, codes_enc, concepts_sorted, langs, NC = B.load_corpus()
code_of = B.make_code_of(concept, lang, codes_enc)
train_codes, _ = B.build_train_transitions(code_of, concepts_sorted, langs, NC)
roll_starts = B.build_roll_starts(code_of, concepts_sorted, langs, NC)
chance = 1.0/(NC-1)
print("[A1] corpus NC=%d langs=%d transitions=%d roll_starts=%d chance=%.4f"
      % (NC, len(langs), train_codes.shape[0], len(roll_starts), chance)); sys.stdout.flush()

def reservoir_state(R, code, prev_state, R_med):
    x = B.bind(code, prev_state) if prev_state is not None else B.neutral_bind(code)
    s_soft = B.chip_forward(R, x)
    return B.binarize_rows(s_soft, R_med)[0]

RES = B.device_banner()
RES.update({"candidate": "A1_reservoir_echo_state", "slug": SLUG, "n_trials": B.NTRIALS, "units": B.UNITS,
            "K_roll": B.K_ROLL, "F_threshold": F_THRESH, "p_max": P_MAX,
            "mechanism": "fixed UNTRAINED reservoir FC (echo recurrence: state=R(bind(code,prev_state))) + "
                         "TRAINED readout FC; codebook in readout output space",
            "baselines": {"pure_on_chip_hop2": 0.028, "single_fc_gen": 0.4234, "shuffle_null_hi": 0.05},
            "trials": []})
print("[A1] akida %s device %s ip %s" % (RES["akida_version"], RES["device"], RES["ip_version"])); sys.stdout.flush()

state_trials = [[] for _ in range(B.K_ROLL)]
res_learn_all, read_learn_all = True, True
last_preds = None
for tr in range(B.NTRIALS):
    # FIXED reservoir (do_fit=False -> echo-state random projection)
    init_R = B.get_w(B.build_fc(1))
    R, res_learned = B.chip_make(init_R, train_codes, do_fit=False)
    R_train_soft = B.chip_forward(R, train_codes)
    R_med = np.median(R_train_soft, axis=0)
    R_train_bin = B.binarize_rows(R_train_soft, R_med)  # reservoir states of each teacher-forced transition
    # TRAINED readout on reservoir-states -> successors
    init_W = B.get_w(B.build_fc(1))
    READ, read_learned = B.chip_make(init_W, R_train_bin, do_fit=True)
    read_soft = B.chip_forward(READ, R_train_bin)
    read_med = np.median(read_soft, axis=0)
    read_bin = B.binarize_rows(read_soft, read_med)
    codebook = B.build_codebook(read_bin, code_of, concepts_sorted, langs, NC)
    # autoregressive echo-state rollout
    preds = [[] for _ in range(B.K_ROLL)]
    for (ti, ql, seed_code) in roll_starts:
        prev_state = None
        cur_code = seed_code.astype(np.uint8).copy()
        banned = concepts_sorted[ti]
        for k in range(B.K_ROLL):
            st = reservoir_state(R, cur_code, prev_state, R_med)
            r_soft = B.chip_forward(READ, st)
            r_bin = B.binarize_rows(r_soft, read_med)[0]
            pred = B.decode(r_bin, codebook, banned)
            preds[k].append((ti, ql, pred))
            banned = pred if pred is not None else banned
            prev_state = st                                    # echo: reservoir state carries forward
            cur_code = code_of(pred, ql) if (pred is not None and code_of(pred, ql) is not None) else cur_code
    del R, READ
    res_learn_all = res_learn_all and res_learned
    read_learn_all = read_learn_all and read_learned
    row = {"trial": tr, "reservoir_learned_hw": res_learned, "readout_learned_hw": read_learned, "acc": []}
    for k0 in range(B.K_ROLL):
        a, n = B.acc_at(preds, k0, concepts_sorted); state_trials[k0].append(a); row["acc"].append(a)
    RES["trials"].append(row)
    last_preds = preds
    print("[A1] trial %d: acc(k1..K)=%s res_learn=%s read_learn=%s"
          % (tr, ["%.4f" % x for x in row["acc"]], res_learned, read_learned)); sys.stdout.flush()
    json.dump(RES, open(os.path.join(B.OUT, "result_a1_reservoir.json"), "w"), indent=2)

per_hop = []
print("[A1] computing per-hop shuffle-NULL (B=%d) ..." % B.B_SHUFFLE); sys.stdout.flush()
for k0 in range(B.K_ROLL):
    sm, ssd, ssem, slo, shi = B.ci(state_trials[k0])
    null = B.shuffle_null_at(last_preds, k0, concepts_sorted, NC)
    nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
    p = float((null >= sm).sum() + 1) / (len(null) + 1)
    above = bool(res_learn_all and read_learn_all and slo > nhi and p <= P_MAX and sm > F_THRESH)
    per_hop.append({"hop": k0+1, "acc": {"mean": sm, "ci_lo": slo, "ci_hi": shi},
                    "shuffle_null": {"mean": nmean, "hi": nhi, "p_value": p}, "chance": chance,
                    "clears_falsifier": above})
    print("[A1] hop %d: acc=%.4f ci_lo=%.4f | shufNULL hi=%.4f p=%.4f | chance=%.4f | clears=%s"
          % (k0+1, sm, slo, nhi, p, chance, above)); sys.stdout.flush()

F_A1_1 = bool(per_hop[1]["clears_falsifier"] and per_hop[2]["clears_falsifier"])
RES["summary"] = {"reservoir_learned_all": res_learn_all, "readout_learned_all": read_learn_all,
                  "encoder_learned": read_learn_all, "trial": B.NTRIALS, "chance": chance,
                  "decay_curve": [round(per_hop[k]["acc"]["mean"], 4) for k in range(B.K_ROLL)],
                  "per_hop": per_hop, "F_A1_1_pass": F_A1_1, "wall_broken": F_A1_1}
if F_A1_1:
    disp = ("A1 RESERVOIR/ECHO-STATE BREAKS THE 1-HOP WALL on-chip (hop-2 AND hop-3 ci_lo>shuffleNULL hi, "
            "p<=%.2f, mean>%.3f material): fixed on-chip recurrence + trained readout carries multi-hop. "
            "MAJOR FINDING — flag for real-chip scale-up. Toy 250-anchor / 256-unit (a_scale_honest_scope)." % (P_MAX, F_THRESH))
else:
    disp = ("A1 RESERVOIR/ECHO-STATE CLOSED-NEGATIVE (a_paper_negative_ok): fixed random on-chip reservoir + "
            "trained 1-bit readout does NOT lift hop-2/3 above the shuffle-NULL by the material margin at p<=%.2f "
            "-> echo-state recurrence on a 1-bit/256-unit AKD1000 does not break the 1-hop wall. EMERGENCE axis NULL. "
            "Lane A on-chip (a_lane_akida_gpu_split), toy 250-anchor (a_scale_honest_scope)." % P_MAX)
RES["DISPOSITION"] = disp
json.dump(RES, open(os.path.join(B.OUT, "result_a1_reservoir.json"), "w"), indent=2)
print("\n[A1] ========== DISPOSITION ==========")
print("[A1] reservoir_learned_all:", res_learn_all, " readout_learned_all:", read_learn_all)
print("[A1] decay curve (k1..K)  :", [round(per_hop[k]["acc"]["mean"], 4) for k in range(B.K_ROLL)])
print("[A1] pure-on-chip wall    : hop-2 ~0.028")
for h in per_hop:
    print("[A1] hop %d acc=%.4f ci_lo=%.4f shufNULL_hi=%.4f p=%.4f clears=%s"
          % (h["hop"], h["acc"]["mean"], h["acc"]["ci_lo"], h["shuffle_null"]["hi"], h["shuffle_null"]["p_value"], h["clears_falsifier"]))
print("[A1] F-A1-1 wall_broken   :", F_A1_1)
print("[A1] DISPOSITION          :", disp)
print("[A1] RULING:", "GREEN-WALL-BROKEN" if F_A1_1 else "closed-negative")
