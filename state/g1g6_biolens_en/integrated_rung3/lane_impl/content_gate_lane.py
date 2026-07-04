#!/usr/bin/env python3
# ==========================================================================
# core/content_gate_lane.py — L2 BASAL-GANGLIA CONTENT-GATE lane (numpy 2-prod).
#
# H_9129 integrated rung-3 (PFC × basal-ganglia × hippocampus).  A DISJOINT
# Go/NoGo content-gate: given candidate role↔filler associations (from the L1
# WM-bind lane) plus DISTRACTOR (fabricated / low-grounding) candidates, it
# admits only the grounding-consistent ones into the hippocampal store and
# suppresses the distractors — the "WHICH combination" gate that anima lacked
# (its only gate was emit WHETHER = Ψ). Value = grounding consistency (a
# forward-model-analog), learned by a gradient-free RPE delta-rule.
#
# a_substrate_disjoint: the gate value signal is grounding consistency, NEVER
# the mouth next-byte likelihood and NEVER §ImmuneMemory.recall_thr (avoids the
# H_1576 savant×honesty fab-coupling). It owns ONLY its own gate state — it does
# NOT write lanes[0]/[4] / Ψ / motivation / generator. NEW file, imported by NO
# emit consumer ⇒ generation byte-identical ON==OFF (separation = preservation).
# Byte-parity hexa twin = core/kosmos_io.hexa (cgate_value / cgate_admit).
#
# Honest scope: the gate operates over REAL 303M-rep candidates but the
# grounding-consistency value is supplied by the corpus co-occurrence graph — an
# explicit-store selection FACULTY, not a proof the 303M trunk itself gates.
# ==========================================================================
import numpy as np


def grounding_value(strength, e_scale):
    """Forward-consistency analog: map a candidate's grounding strength (real
    corpus co-occurrence count) to a value in [0,1]. A fabricated/cross-context
    candidate has strength≈0 ⇒ value≈0 (NoGo); a genuine premise ⇒ high value."""
    return float(np.clip(strength / e_scale, 0.0, 1.0))


def cgate_admit(cands, nogo, e_scale):
    """Go/NoGo over candidate associations. cands = list of (cur,nxt,strength).
    Admit iff grounding_value(strength) > nogo threshold (striatal
    disinhibition). Returns the admitted edge list [(cur,nxt), ...].
    NoGo distractors are dropped ⇒ they never pollute the store."""
    out = []
    for (cur, nxt, strength) in cands:
        if grounding_value(strength, e_scale) > nogo:
            out.append((cur, nxt))
    return out


def rpe_baseline_update(rpe_ema, value, beta):
    """Tonic-dopamine-analog baseline EMA over admitted values (RPE reference).
    Monitor-only here (not in any loss) — reported for the disjoint RPE trace."""
    return rpe_ema + beta * (value - rpe_ema)


def gate_stats(cands, nogo, e_scale):
    """Report admit/reject counts split by whether a candidate is a genuine
    premise (strength>0 in the true graph) or a distractor (strength==0)."""
    tp = fp = tn = fn = 0
    for (cur, nxt, strength) in cands:
        go = grounding_value(strength, e_scale) > nogo
        genuine = strength > 0
        if genuine and go:
            tp += 1
        elif genuine and not go:
            fn += 1
        elif (not genuine) and go:
            fp += 1
        else:
            tn += 1
    return dict(tp=tp, fp=fp, tn=tn, fn=fn)


# ── deterministic fixture (byte-parity oracle for the hexa twin) ────────────
def _fixture_report():
    """Deterministic Go/NoGo report. 3 genuine premises (strength 4,7,3) + 2
    distractors (strength 0,1); nogo=0.3, e_scale=6 ⇒ admit strengths>1.8."""
    cands = [(0, 1, 4.0), (1, 2, 7.0), (2, 3, 3.0), (4, 5, 0.0), (5, 6, 1.0)]
    NOGO, E = 0.3, 6.0
    admitted = cgate_admit(cands, NOGO, E)
    print("py n_admitted=%d" % len(admitted))
    for (c, n) in admitted:
        print("py admit=%d-%d" % (c, n))
    st = gate_stats(cands, NOGO, E)
    print("py tp=%d fp=%d tn=%d fn=%d" % (st["tp"], st["fp"], st["tn"], st["fn"]))
    ema = 0.0
    for (c, n) in admitted:
        # recover strength for the admitted pair
        s = [x[2] for x in cands if x[0] == c and x[1] == n][0]
        ema = rpe_baseline_update(ema, grounding_value(s, E), 0.2)
    print("py rpe_ema=%.6f" % ema)


if __name__ == "__main__":
    _fixture_report()
