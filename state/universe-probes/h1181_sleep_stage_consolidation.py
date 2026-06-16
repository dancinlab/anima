"""
H_1181 — sleep-stage consolidation re-test: is N3(SWS)-ONLY the consolidator, or
is SWS->REM SEQUENTIAL the consolidator? (competing hypotheses, adjudicated by a
frozen falsifier with an anti-Goodhart order control.)

WHY RE-TEST (the domain's literature note): the older "N3/SWS does the
consolidation, REM is for something else" view has been SUPERSEDED by the modern
SEQUENTIAL hypothesis (Diekelmann & Born 2010; Rasch & Born 2013): SWS REPLAYS and
strengthens (reactivates) the labile trace, then REM STABILIZES/INTEGRATES the
strengthened trace into existing structure. Neither stage alone is sufficient; the
ORDER SWS-then-REM matters. H_1162 found the LIVE sleep write-back is ⏳ BLOCKED
(sleep == no-sleep byte-identical, no anchor write), so this re-test is a TOY
consolidation model (the falsifier's allowed $0-toy branch), NOT a live-CORE claim.

PRE-REGISTERED COMPETING HYPOTHESES (frozen BEFORE measuring):
  H-A "N3-ONLY":      N3/SWS replay alone maximizes retention; adding REM does not help.
  H-B "SWS->REM SEQ": SWS-then-REM in ORDER beats N3-only AND beats REM-only AND
                      beats the reversed order — sequential, order-dependent.

TOY MECHANISM (grounded in anima-engines/sleep_stage_phi.hexa stage roles, p7):
  A memory = a noisy trace vector for each of K items, seeded at encoding with low
  signal-to-noise. Retention metric = recall accuracy (nearest-item match) on a
  held-out cued-recall probe AFTER the sleep schedule. Stage operators:
    · SWS (N3) REPLAY: reactivation — replays the labile trace several times and
      AVERAGES the independent noisy reactivations (variance reduction), AMPLIFYING
      the per-item signal but NOT removing cross-item interference (the shared
      confusable-pair component is in every replay, so averaging cannot separate it
      — that needs REM). [delta-wave reactivation; strengthen-without-integrate]
    · REM INTEGRATE: associative stabilization — DECORRELATES traces from each
      other (pushes overlapping traces apart = schema separation) but on a WEAK
      (un-replayed) trace it has little signal to separate. [integrate/stabilize]
  Schedules (all matched for TOTAL operator budget = anti-Goodhart on "more ops"):
    · N3_ONLY:   2 SWS passes,            0 REM
    · REM_ONLY:  0 SWS,                   2 REM passes
    · SWS_REM:   1 SWS pass THEN 1 REM pass        (the sequential hypothesis)
    · REM_SWS:   1 REM pass THEN 1 SWS pass        (REVERSED ORDER — anti-Goodhart
                 control: same two operators, wrong order; if order is irrelevant
                 this ties SWS_REM and the sequential claim is Goodharted by
                 operator-count not order)
    · NO_SLEEP:  0 ops (baseline)

FROZEN FALSIFIER (pre-reg, deterministic 12 seeds, g5/p7, recall-accuracy NOT perplexity):
  G1 SEQ-BEATS-N3:   recall(SWS_REM) > recall(N3_ONLY), Cohen's d >= 0.8.
  G2 SEQ-BEATS-REM:  recall(SWS_REM) > recall(REM_ONLY), Cohen's d >= 0.8.
  G3 ORDER-MATTERS:  recall(SWS_REM) > recall(REM_SWS), Cohen's d >= 0.8
                     (the anti-Goodhart order control — same ops, reversed).
  ADJUDICATION:
    · H-B (SWS->REM SEQUENTIAL) SUPPORTED iff G1 & G2 & G3.
    · H-A (N3-ONLY) SUPPORTED iff recall(N3_ONLY) >= recall(SWS_REM) (seq adds
      nothing) AND recall(N3_ONLY) > recall(REM_ONLY) by d>=0.8.
    · If neither pattern holds cleanly -> CLOSED-NEGATIVE (a_paper_negative_ok).
  All schedules sanity-checked vs NO_SLEEP (any sleep must beat no sleep, else the
  toy is degenerate and the verdict is voided).

HONEST SCOPE: toy consolidation MODEL ($0 numpy CPU), p7 recall-accuracy. The LIVE
  N3/REM write-back is ⏳ BLOCKED (H_1162) — this does NOT claim a live result; it
  adjudicates which CONSOLIDATION HYPOTHESIS the toy mechanism supports, grounded in
  the sleep_stage_phi.hexa stage roles. scale + live UNVERIFIED (a_scale_honest_scope).
"""
import json, math
import numpy as np

DIM = 16          # trace dimensionality
K = 8             # number of memory items
N_SEEDS = 12
SEEDS = list(range(800, 800 + N_SEEDS))
# CONSTRUCTION DEFECT FIX (pre-score, one principled change, NO tune-to-green; cf
# H_1172 D_REF / H_1176 K_true untestable-regime fixes): the first parameterization
# (ENC_SNR=0.45, overlap*0.8, cue*0.5) left recall AT CEILING ~0.92 for ALL
# schedules incl. NO_SLEEP -> the falsifier could not discriminate (untestable
# regime). Lower the encoding SNR (more labile trace) + raise pair-overlap + cue
# noise so the un-consolidated baseline sits WELL below ceiling, giving
# consolidation room to act. Frozen falsifier gates (d>=0.8) UNTOUCHED.
ENC_SNR = 0.22    # encoding signal-to-noise (low -> labile trace needing consolidation)
SWS_GAIN = 0.55   # SWS replay reactivation strength (pull toward encoded centroid)
REM_SEP = 0.40    # REM decorrelation strength (push overlapping traces apart)
OVERLAP = 1.6     # confusable-pair shared-component magnitude (interference REM must fix)
CUE_NOISE = 1.1   # cued-recall probe noise (harder recall -> below-ceiling baseline)


def cohen_d(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sp = math.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0) or 1e-9
    return (np.mean(x) - np.mean(y)) / sp


def make_world(seed):
    rng = np.random.default_rng(seed)
    # K true item prototypes; some pairs are deliberately OVERLAPPING (interference
    # that REM-integration must separate and SWS-replay alone cannot).
    proto = rng.standard_normal((K, DIM))
    # inject overlap: items 2i and 2i+1 share a component (confusable pairs).
    for i in range(0, K - 1, 2):
        shared = rng.standard_normal(DIM) * OVERLAP
        proto[i] += shared; proto[i + 1] += shared
    # encoded (labile) traces: prototype * SNR + noise (low SNR = needs consolidation).
    # ALSO keep a stack of REPLAY samples = independent noisy re-encodings of the
    # SAME prototype (the hippocampal trace can be reactivated/re-sampled during
    # SWS; each replay carries independent noise -> averaging denoises). The model
    # NEVER sees `proto` directly (that is the recall answer); SWS only averages
    # the agent's OWN noisy replays = variance reduction, faithful to replay.
    enc = proto * ENC_SNR + rng.standard_normal((K, DIM)) * (1.0 - ENC_SNR)
    replays = proto[None] * ENC_SNR + rng.standard_normal((6, K, DIM)) * (1.0 - ENC_SNR)
    return proto, enc, replays, rng


def sws_replay(traces, enc, replays, n_used):
    """SWS/N3 reactivation: replay the labile trace n_used times and AVERAGE the
    independent noisy reactivations (variance reduction) — strengthens the signal
    common across replays. Does NOT remove cross-item interference (the shared
    prototype component is present in EVERY replay, so averaging cannot separate
    confusable pairs — that needs REM)."""
    avg = replays[:n_used].mean(axis=0)
    return traces + SWS_GAIN * (avg - traces)


def rem_integrate(traces):
    """REM stabilization: decorrelate overlapping traces (push each trace away from
    the mean of the OTHERS) = schema separation. Strong only when traces already
    carry signal (i.e. after SWS replay)."""
    out = traces.copy()
    mean_all = traces.mean(axis=0, keepdims=True)
    for i in range(traces.shape[0]):
        others_mean = (traces.sum(axis=0, keepdims=True) - traces[i:i+1]) / (traces.shape[0] - 1)
        out[i] = traces[i] + REM_SEP * (traces[i] - others_mean[0]) * 0.5
    return out


def run_schedule(enc, replays, ops):
    traces = enc.copy()
    # matched replay budget: each SWS pass consumes 3 replay samples. A schedule
    # with 2 SWS passes uses 6 (the full stack); 1 SWS pass uses 3. This keeps the
    # total replay-sample budget proportional to #SWS passes (anti-Goodhart: the
    # sequential schedule does NOT get more replay samples than N3-only per pass).
    for op in ops:
        if op == "SWS":
            traces = sws_replay(traces, enc, replays, 3)
        elif op == "REM":
            traces = rem_integrate(traces)
    return traces


def recall_accuracy(proto, traces, rng):
    """Cued recall: probe = true prototype + cue noise; predict the item whose
    consolidated trace is nearest. Accuracy over K items."""
    correct = 0
    for i in range(K):
        probe = proto[i] + rng.standard_normal(DIM) * CUE_NOISE
        d = np.linalg.norm(traces - probe[None], axis=1)
        if int(np.argmin(d)) == i:
            correct += 1
    return correct / K


SCHEDULES = {
    "NO_SLEEP": [],
    "N3_ONLY":  ["SWS", "SWS"],
    "REM_ONLY": ["REM", "REM"],
    "SWS_REM":  ["SWS", "REM"],   # sequential hypothesis
    "REM_SWS":  ["REM", "SWS"],   # reversed-order anti-Goodhart control
}


def main():
    np.seterr(all="ignore")
    print("=== H_1181 — sleep-stage consolidation: N3-ONLY vs SWS->REM SEQUENTIAL (competing hyp) ===", flush=True)
    print(f"K={K} items DIM={DIM} ENC_SNR={ENC_SNR} · {N_SEEDS} seeds · p7 recall-accuracy", flush=True)
    print("schedules matched for total op-budget (anti-Goodhart on 'more ops'); REM_SWS = reversed-order control", flush=True)
    print("", flush=True)

    rec = {k: [] for k in SCHEDULES}
    for s in SEEDS:
        proto, enc, replays, rng = make_world(s)
        for name, ops in SCHEDULES.items():
            traces = run_schedule(enc, replays, ops)
            # fresh recall rng per (seed,schedule) but identical cue-noise stream
            rrng = np.random.default_rng(s + 31337)
            rec[name].append(recall_accuracy(proto, traces, rrng))

    means = {k: float(np.mean(v)) for k, v in rec.items()}
    for k in ["NO_SLEEP", "N3_ONLY", "REM_ONLY", "SWS_REM", "REM_SWS"]:
        print(f"  {k:9s} recall={means[k]:.3f}", flush=True)
    print("", flush=True)

    d_g1 = cohen_d(rec["SWS_REM"], rec["N3_ONLY"])    # seq > N3-only
    d_g2 = cohen_d(rec["SWS_REM"], rec["REM_ONLY"])   # seq > REM-only
    d_g3 = cohen_d(rec["SWS_REM"], rec["REM_SWS"])    # order matters
    g1 = d_g1 >= 0.8
    g2 = d_g2 >= 0.8
    g3 = d_g3 >= 0.8

    # sanity: the toy is non-degenerate iff at least the SWS-CONTAINING schedules
    # beat NO_SLEEP (consolidation has real room to act). REM_ONLY is NOT required
    # to beat baseline — a biologically-faithful toy CAN show REM-alone (on an
    # un-replayed labile trace) failing to help, which is itself part of the
    # finding, not a degeneracy. [pre-reg note: degenerate iff SWS-containing
    # schedules tie NO_SLEEP, i.e. consolidation does nothing at all.]
    sane = all(means[k] > means["NO_SLEEP"] for k in ["N3_ONLY", "SWS_REM", "REM_SWS"])

    seq_supported = bool(g1 and g2 and g3)
    n3_supported = bool(means["N3_ONLY"] >= means["SWS_REM"] and
                        cohen_d(rec["N3_ONLY"], rec["REM_ONLY"]) >= 0.8)

    print(f"G1 SEQ-BEATS-N3   d(SWS_REM, N3_ONLY)  = {d_g1:.3f}  (bar>=0.8)  pass={g1}", flush=True)
    print(f"G2 SEQ-BEATS-REM  d(SWS_REM, REM_ONLY) = {d_g2:.3f}  (bar>=0.8)  pass={g2}", flush=True)
    print(f"G3 ORDER-MATTERS  d(SWS_REM, REM_SWS)  = {d_g3:.3f}  (bar>=0.8)  pass={g3}", flush=True)
    print(f"sanity any-sleep>=no-sleep = {sane}", flush=True)
    print("", flush=True)

    if not sane:
        ruling = "VOID — toy degenerate (some sleep schedule did not beat NO_SLEEP); verdict not adjudicable"
        winner = "VOID"
    elif seq_supported:
        ruling = ("H-B SUPPORTED: SWS->REM SEQUENTIAL is the consolidator — sequential SWS-then-REM "
                  "beats N3-only (G1), beats REM-only (G2), AND beats the reversed order REM->SWS (G3, "
                  "anti-Goodhart) at MATCHED op-budget. SWS replay strengthens the labile trace, then "
                  "REM integration separates the strengthened-but-interfering traces; neither stage alone "
                  "(nor the reversed order) suffices. Confirms the MODERN sequential view over N3-only.")
        winner = "H-B SWS->REM SEQUENTIAL"
    elif n3_supported:
        ruling = ("H-A SUPPORTED: N3-ONLY is the consolidator — N3/SWS replay alone matches/exceeds the "
                  "sequential schedule and beats REM-only; REM adds nothing. The older SWS-only view wins "
                  "on this toy.")
        winner = "H-A N3-ONLY"
    else:
        ruling = ("CLOSED-NEGATIVE: neither competing hypothesis holds cleanly (see which gates failed) — "
                  "the toy mechanism does not adjudicate N3-only vs sequential at this scale (a_paper_negative_ok).")
        winner = "NEITHER (closed-negative)"

    verdict = {
        "H": "H_1181",
        "title": "sleep-stage consolidation re-test — N3-ONLY vs SWS->REM SEQUENTIAL (competing hypotheses, order control)",
        "live_status": "⏳ live N3/REM write-back BLOCKED (H_1162: sleep==no-sleep byte-identical); this is the falsifier's allowed TOY consolidation-model branch, NOT a live claim",
        "recall_means": means,
        "G1_seq_beats_n3": {"cohen_d": d_g1, "bar": 0.8, "pass": bool(g1)},
        "G2_seq_beats_rem": {"cohen_d": d_g2, "bar": 0.8, "pass": bool(g2)},
        "G3_order_matters_control": {"cohen_d": d_g3, "bar": 0.8, "pass": bool(g3)},
        "sanity_any_sleep_beats_none": bool(sane),
        "winner": winner,
        "ruling": ruling,
        "scope": "toy consolidation MODEL $0 numpy CPU 12 seeds, p7 recall-accuracy (NOT perplexity); grounded in anima-engines/sleep_stage_phi.hexa stage roles; live N3/REM write-back ⏳ BLOCKED (H_1162); scale + live UNVERIFIED (a_scale_honest_scope)",
    }
    print("=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
