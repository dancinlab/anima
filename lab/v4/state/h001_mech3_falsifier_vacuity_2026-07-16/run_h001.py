#!/usr/bin/env python3
"""H_001 — mech-3's pre-registered falsifier is VACUOUS (arithmetic audit).

Closed-form, stdlib-only, $0. Decides whether ARCHITECTURE.json's `mech-3.falsifier`
clause (2) — "고정-BPE 치환 ΔF2 < 0.1이면 사망" / "fixed-BPE substitution deltaF2 < 0.1
=> DEAD" — is a test of the mechanism at all, or a verdict fixed before the run.

The audit needs no new measurement. anima v1 already measured every arm this
falsifier refers to; the question is purely whether the pre-registered threshold
is arithmetically attainable against the control the clause names.

Run:  python3 state/h001_mech3_falsifier_vacuity_2026-07-16/run_h001.py
"""

from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))


def _harness():
    """Import the repo-root shared harness. Done inside a function because the
    import depends on a path bootstrap; keeping it off the module level is what
    makes that legal rather than something to suppress."""
    sys.path.insert(0, os.path.join(_ROOT, "tool"))
    import anima_v4

    return anima_v4


# --- PRE-REGISTERED INPUTS ----------------------------------------------------
#
# Every number below is a `d_acc` reading from the anima v1 MORPH-ATOM record,
# transcribed with its source path. `d_acc` = forced-choice discrimination
# accuracy on eval panel f2 (held-out negation recombination, n=120): the model
# scores a positive when NLL(seed+gold) < NLL(seed+counterfactual).
#
# NOTE: v1's "F2" is the NAME OF THE PANEL (eval_f2.json), not an F-beta measure.
# anima-v4's tree inherited it as if it were a metric. See the card's `Honest
# Limits`. The metric is d_acc, a binary forced-choice accuracy, so its ceiling
# 1.0 and chance floor 0.5 are definitional, not measured.

ARMS = {
    # arm: (d_acc, codec, what the arm is, source path)
    "M_s4302": (
        0.9083, "codec.json",
        "FIXED jamo-BPE codec (K=2048, frequency-trained, label-blind)",
        "~/anima-weights/morphatom/vM_f2.json",
    ),
    "M_s7": (
        0.9167, "codec.json",
        "FIXED jamo-BPE codec — seed-7 replication (cement)",
        "anima/state/nbind_curriculum/cement_result/vM_s7_f2.json",
    ),
    "C1_s4302": (
        0.6167, "raw",
        "NO CODEC AT ALL — raw utf-8 bytes",
        "~/anima-weights/morphatom/vC1_f2.json",
    ),
    "C1_s7": (
        0.5750, "raw",
        "NO CODEC AT ALL — raw utf-8, seed-7 replication (cement)",
        "anima/state/nbind_curriculum/cement_result/vC1_s7_f2.json",
    ),
    "C3_s4302": (
        0.9167, "codec_c3.json",
        "LEAK CEILING — 4 negator stems collapsed to ONE shared token id, i.e. "
        "the answer handed to the model outright (v1's V1-liveness arm)",
        "~/anima-weights/morphatom/v1_f2b.json",
    ),
}

# The threshold mech-3 pre-registered for its clause-(2) L2 ablation.
# Source: ARCHITECTURE.json -> components -> mech-3.codec-war -> mech-3.falsifier
MECH3_THRESHOLD = 0.1

# The control mech-3's clause (2) names: "substitute a fixed BPE for G".
# The fixed BPE-jamo codec IS arm M. Both seeds are audited.
FIXED_CODEC_ARMS = ["M_s4302", "M_s7"]

# The score mech-3's clause (2) predicts the substitution will fall to.
# Source: ARCHITECTURE.json mech-3.l2-defense — "must fall to ~0.617".
MECH3_PREDICTED_FALL_TO = 0.617


def main() -> int:
    h = _harness()
    d_acc = {k: v[0] for k, v in ARMS.items()}

    # --- the arithmetic -------------------------------------------------------
    # Against the control the clause actually names (the FIXED codec = arm M),
    # what is the largest delta any mechanism could possibly show?
    reach = {}
    for arm in FIXED_CODEC_ARMS:
        reach[arm] = {
            "control_d_acc": d_acc[arm],
            "max_attainable_delta": round(h.max_attainable_delta(d_acc[arm], h.D_ACC_MAX), 4),
            "threshold": MECH3_THRESHOLD,
            "reachable": h.falsifier_reachable(MECH3_THRESHOLD, d_acc[arm], h.D_ACC_MAX),
        }

    # Negative control: run the SAME arithmetic against the no-codec arm (C1).
    # If the audit is sound it must NOT kill this comparison — a vacuity audit
    # that condemns every possible falsifier is measuring its own bias.
    negctl = {}
    for arm in ["C1_s4302", "C1_s7"]:
        negctl[arm] = {
            "control_d_acc": d_acc[arm],
            "max_attainable_delta": round(h.max_attainable_delta(d_acc[arm], h.D_ACC_MAX), 4),
            "threshold": MECH3_THRESHOLD,
            "reachable": h.falsifier_reachable(MECH3_THRESHOLD, d_acc[arm], h.D_ACC_MAX),
        }

    # Saturation: distance from the fixed codec to the panel's leak ceiling.
    sat = {
        arm: round(h.saturation(d_acc[arm], d_acc["C3_s4302"]), 4)
        for arm in FIXED_CODEC_ARMS
    }

    metrics = {
        "d_acc": d_acc,
        "mech3_threshold": MECH3_THRESHOLD,
        "reachability_vs_fixed_codec": reach,
        "reachability_vs_no_codec_NEGATIVE_CONTROL": negctl,
        "saturation_vs_leak_ceiling": sat,
        "m_seed_spread": round(abs(d_acc["M_s7"] - d_acc["M_s4302"]), 4),
        "control_named_by_clause_is_a_codec": ARMS["C1_s4302"][1] != "raw",
        "predicted_fall_to": MECH3_PREDICTED_FALL_TO,
        "actual_fixed_codec_floor": min(d_acc[a] for a in FIXED_CODEC_ARMS),
    }

    # --- pre-registered falsifiers -------------------------------------------
    # Each predicate returns True when TRIGGERED (the claim's component is refuted).
    falsifiers = [
        h.Falsifier(
            "F-001-1-threshold-attainable",
            lambda m: any(r["reachable"] for r in m["reachability_vs_fixed_codec"].values()),
            "If mech-3's 0.1 threshold IS attainable against the fixed-codec control at "
            "either seed, the falsifier is a real test and the vacuity claim is refuted.",
        ),
        h.Falsifier(
            "F-001-2-control-is-actually-a-fixed-codec",
            lambda m: m["control_named_by_clause_is_a_codec"],
            "If v1's 0.617 control arm (C1) was itself a FIXED CODEC rather than NO codec, "
            "then mech-3's 'fall to ~0.617' ablation is coherent and the confound claim is "
            "refuted. Measured from the arm's own `codec` field.",
        ),
        h.Falsifier(
            "F-001-3-panel-not-saturated",
            lambda m: any(s >= MECH3_THRESHOLD for s in m["saturation_vs_leak_ceiling"].values()),
            "If the fixed codec sits >= 0.1 BELOW the leak ceiling, the panel still has room "
            "to resolve a mechanism above it and the saturation claim is refuted.",
        ),
        h.Falsifier(
            "F-001-4-NEGATIVE-CONTROL-audit-kills-everything",
            lambda m: not all(
                r["reachable"] for r in m["reachability_vs_no_codec_NEGATIVE_CONTROL"].values()
            ),
            "NEGATIVE CONTROL. The same arithmetic applied to the no-codec arm (C1, ~0.6) MUST "
            "find 0.1 reachable. If the audit condemns that comparison too, it is not detecting "
            "vacuity — it is condemning everything, and its verdict is worthless.",
        ),
        h.Falsifier(
            "F-001-5-m-estimate-too-noisy",
            lambda m: m["m_seed_spread"] >= MECH3_THRESHOLD,
            "If M's two independent seeds disagree by >= the threshold itself, the fixed-codec "
            "control is too noisy to support any arithmetic about it and the claim is refuted.",
        ),
        h.Falsifier(
            "F-001-6-BOUNDS-d-acc-out-of-range",
            lambda m: not all(
                h.D_ACC_CHANCE - 0.1 <= v <= h.D_ACC_MAX for v in m["d_acc"].values()
            ),
            "BOUNDS CHECK. Every transcribed d_acc must lie within [chance-0.1, 1.0]. A reading "
            "outside that window means the numbers are mis-transcribed and the audit is void.",
        ),
        h.Falsifier(
            "F-001-7-predicted-fall-matches-fixed-codec",
            lambda m: abs(m["predicted_fall_to"] - m["actual_fixed_codec_floor"]) < 0.05,
            "If substituting the fixed codec really does land near mech-3's predicted ~0.617, "
            "the clause is self-consistent and the confound claim is refuted.",
        ),
    ]

    ledger = h.evaluate(metrics, falsifiers)

    # --- report ---------------------------------------------------------------
    print("=" * 78)
    print("H_001 — mech-3's pre-registered falsifier is VACUOUS (closed-form audit)")
    print("=" * 78)
    print()
    print("v1 MORPH-ATOM arms (metric = d_acc, forced-choice accuracy on panel f2, n=120):")
    for k, (v, codec, what, src) in ARMS.items():
        print("  %-9s d_acc=%.4f  codec=%-12s  %s" % (k, v, codec, what))
        print("  %-9s   src: %s" % ("", src))
    print()
    print("mech-3 clause (2), verbatim from ARCHITECTURE.json:")
    print('  "L2 — fixed-BPE substitution deltaF2 < 0.1 ⇒ DEAD"')
    print('  "Ablation: substitute a fixed BPE for G → F2 must fall to ~0.617"')
    print()
    print("The arithmetic — against the control the clause names (the FIXED codec = arm M):")
    for arm, r in reach.items():
        print("  %-9s max attainable delta = %.4f - %.4f = %.4f   threshold %.2f  reachable=%s"
              % (arm, h.D_ACC_MAX, r["control_d_acc"], r["max_attainable_delta"],
                 r["threshold"], r["reachable"]))
    print()
    print("NEGATIVE CONTROL — same arithmetic vs the no-codec arm (C1):")
    for arm, r in negctl.items():
        print("  %-9s max attainable delta = %.4f - %.4f = %.4f   threshold %.2f  reachable=%s"
              % (arm, h.D_ACC_MAX, r["control_d_acc"], r["max_attainable_delta"],
                 r["threshold"], r["reachable"]))
    print()
    print("Saturation vs the leak ceiling (C3 = answer handed over = %.4f):" % d_acc["C3_s4302"])
    for arm, s in sat.items():
        print("  %-9s leak_ceiling - arm = %+.4f" % (arm, s))
    print()
    print("Falsifier ledger:")
    for r in ledger["falsifiers"]:
        print("  [%s] %s" % (r["status"], r["name"]))
    print()
    print("  %d/%d PASS" % (ledger["n_pass"], ledger["n_total"]))
    print()
    verdict = "SUPPORTED" if ledger["all_pass"] else "FALSIFIED"
    print("VERDICT: %s — mech-3's clause-(2) falsifier is %s" % (
        verdict,
        "VACUOUS: it returns DEAD for every possible mechanism" if ledger["all_pass"]
        else "a real test; the vacuity claim does not hold",
    ))
    print()
    print("Reading: the clause names the FIXED BPE-jamo codec as the thing G is ablated to.")
    print("That codec IS arm M, and M scores %.4f-%.4f. d_acc is an accuracy, so the largest"
          % (d_acc["M_s4302"], d_acc["M_s7"]))
    print("delta ANY mechanism can show over it is %.4f — strictly less than the %.2f the"
          % (max(r["max_attainable_delta"] for r in reach.values()), MECH3_THRESHOLD))
    print("clause requires. The verdict DEAD is fixed before the experiment is built.")
    print("The 0.617 the clause predicts the substitution falls to is arm C1 = NO CODEC,")
    print("not a fixed codec — so the ablation as written varies the EXISTENCE of a codec,")
    print("not the LEARNING of one. That is the confound, and it is what makes the 0.1")
    print("threshold look reachable on paper.")

    ledger["verdict"] = verdict
    ledger["arms_provenance"] = {k: {"d_acc": v[0], "codec": v[1], "what": v[2], "src": v[3]}
                                 for k, v in ARMS.items()}
    out = os.path.join(_HERE, "result.json")
    with open(out, "w") as fh:
        json.dump(ledger, fh, indent=2, ensure_ascii=False)
    print()
    print("wrote %s" % out)
    return 0 if ledger["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
