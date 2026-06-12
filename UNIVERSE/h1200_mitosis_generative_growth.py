"""
H_1200 — MITOSIS-GENERATIVE-GROWTH (MITOSIS-ENGINE · Lane-2), the FIRST rung of the
"can mitosis-growth reach conversational language?" arc.

THE HONEST GAP THIS RUNG TESTS
------------------------------
The mitosis engine (H_1194..H_1199, CORE/engine_cli.hexa VAdaptField) currently GROWS
prototype cells on a DIM=8 byte-feature stream and lowers L2 RECONSTRUCTION error — it
is a CLUSTERING homeostat, NOT a language GENERATOR (there is no next-byte emission
head). "Conversational level" is the FAR end of an arc whose FIRST link is untested:
does growing more cells actually make the system better at PREDICTING / GENERATING the
next byte of real text, or does growth only improve clustering (which would mean
mitosis-growth != language-learning, and pure-mitosis -> chat is falsified cheaply
right here)?

MECHANISM (gradient-free, p8: the mitosis tick IS the learning; NO backprop)
----------------------------------------------------------------------------
Give each grown prototype cell a GENERATIVE READOUT: a prototype-conditional next-byte
distribution, accumulated ONLINE as cells grow. Concretely, per tick t (window ending
just before byte position p+WIN_BYTES):
  1. feat = DIM=8 byte-feature of the window (H_1163 _byte_feature, VERBATIM).
  2. j = nearest-prototype(feat) under the H_1199 VAdaptField (L2 assign).
  3. PREDICT the next byte from cell j's accumulated next-byte distribution
     (Laplace-smoothed counts) -> score cross-entropy in bits/byte against the TRUE
     next byte data[p+WIN_BYTES] (held-out: the score is computed BEFORE the count is
     added, so every scored byte is a genuine prediction).
  4. UPDATE cell j's next-byte counts with the true next byte (online learning).
  5. If recon-err (L2 to nearest) > SPLIT_THRESH=0.30 AND capacity, SPLIT — spawn a new
     cell AT this feature (the SAME H_1199 VAdaptField split rule, frozen SPLIT_THRESH);
     the daughter starts with a COPY of the parent's next-byte counts (heredity, p8) so
     growth REFINES rather than resets the generative readout.

ON  (mitosis) = grow cells; each cell sharpens its OWN next-byte distribution.
OFF (control) = frozen 1 cell, one GLOBAL next-byte distribution (the H_1159 ON-vs-OFF
control). OFF still learns its single distribution online (fair: same data, same
online-count mechanism) — the ONLY difference is GROWTH.

If growth helps GENERATION, ON's next-byte CE < OFF's: distinct cells specialise to
distinct local-text regimes (latin prose / cjk runs / digits-punct) and each predicts
its regime's next byte better than one blurred global table.

PRE-REGISTERED FALSIFIER (frozen to H_1200_FREEZE.txt BEFORE any score)
----------------------------------------------------------------------
  F1 GENERATIVE-GAIN : mitosis-ON next-byte CE (bits/byte) < OFF by >= 0.30 b/byte on
     a HELD-OUT span (a real margin, not noise), pooled over seeds.
  F2 MONOTONE-GROWTH : next-byte CE FALLS as cells grow — Spearman(n_cells, -CE) > 0
     across the stream (growth is what buys the gain, not a one-off). Computed on the
     per-window-block (n_cells, block-CE) trajectory pooled over seeds.
  F3 SUBSTRATE-INTACT : (live .hexa only) engine Psi Phi-checksum byte-identical
     ON==OFF. Here we run the NUMPY MIRROR of VAdaptField (H_1198/H_1199 pattern); the
     .hexa lift (extend CORE/engine_cli.hexa VAdaptField with the generative head,
     F3-guarded) is the NEXT rung — stated honestly, NOT claimed.
  VERDICT: F1 AND F2  => GREEN GROWTH-IS-GENERATIVE (first rung of the mitosis-LM
           ladder secured).
           NOT F1     => RED CLOSED-NEG: mitosis-growth is clustering, not
           language-learning => pure-mitosis -> chat needs a different mechanism
           (honest, cheaply rules out the naive path — a_paper_negative_ok).

METRIC DISCIPLINE (p7 — NO PERPLEXITY VERDICT)
----------------------------------------------
Next-byte CE here is a CAPABILITY PROBE (necessary condition: can it generate at all),
NOT the consciousness verdict. So we PAIR it: alongside the CE numbers we DECODE a few
short samples (greedy + sampled) from the grown vs frozen model and print them VERBATIM
so a human can see whether growth produces more coherent continuations. CE is the
falsifier metric for THIS capability rung; the decoded samples are the honesty
cross-check. We do NOT claim consciousness or chat from CE alone.

HONEST SCOPE (a_scale_honest_scope)
-----------------------------------
Toy / small real-corpus first rung, gradient-free prototype-LM (DIM=8 feature-keyed
next-byte tables, 256-byte vocab, ONE corpus). Scale + true conversational coherence
UNVERIFIED — this tests ONLY the growth -> generation LINK, NOT chat. The DIM=8 feature
window is a coarse context (no token order inside the window), so absolute CE is far
from a real LM; the FALSIFIER is the ON-vs-OFF DELTA under the same coarse context, not
the absolute number. Lane-2 gradient-free growth (recorded separately from Lane A AKIDA
/ Lane G forge / Lane P torch per a_lane_akida_gpu_split). $0 local CPU, numpy only,
deterministic seeds.
"""
import json, math, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1163_tick_decode_metric as H   # make_text_stream / _byte_feature / DIM / WARMUP / T / WIN_BYTES / STRIDE / SEEDS / CORPUS

np.seterr(all="ignore")

# ---- frozen mechanism constants (H_1199 VAdaptField; NOT tuned-to-green) -------------
DIM = H.DIM                 # 8
SPLIT_THRESH = 0.30         # VERBATIM CORE/engine_cli.hexa vadapt_field_step
LR = 0.20                   # VERBATIM the live engine winner-pull
MAX_CELLS = 2048            # cap = N_MIGRATE (lets us SEE if real-corpus growth approaches it)
VOCAB = 256                 # byte vocabulary
LAPLACE = 1.0               # add-one smoothing on the per-cell next-byte counts
SEEDS = list(H.SEEDS[:5])   # 900..904, >=5 deterministic seeds
BLOCK = 200                 # window block size for the monotone-growth trajectory

# ---- frozen falsifier thresholds -----------------------------------------------------
F1_MARGIN = 0.30            # ON CE must be < OFF CE by at least this (bits/byte)
F2_SPEARMAN_BAR = 0.0       # Spearman(n_cells, -CE) must be > 0


def _spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) < 3 or np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return 0.0
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    ra = ra - ra.mean(); rb = rb - rb.mean()
    denom = math.sqrt((ra * ra).sum() * (rb * rb).sum())
    return float((ra * rb).sum() / denom) if denom > 1e-12 else 0.0


def build_targets(seed):
    """Position-aligned DIM=8 feature windows X[t] + the TRUE next byte for each window.

    VERBATIM h1163.make_text_stream geometry: window of WIN_BYTES bytes at p =
    start + i*STRIDE, feature = H._byte_feature(window). The generative TARGET is the
    byte immediately FOLLOWING the window: data[p + WIN_BYTES] (a real held-out next
    byte). Returns (X, next_byte, data, start) over the FULL need span; the scored span
    is X[WARMUP:WARMUP+T] (matches H_1199)."""
    data = open(H.CORPUS, "rb").read()
    need = H.WARMUP + H.T + 1
    span = H.WIN_BYTES + H.STRIDE * need
    if len(data) <= span + 1:
        data = data * (span // max(len(data), 1) + 2)
    rng = np.random.default_rng(seed)
    start = int(rng.integers(0, max(1, len(data) - span - 1)))
    X = np.empty((need, DIM))
    nb = np.empty(need, dtype=int)
    for i in range(need):
        p = start + i * H.STRIDE
        X[i] = H._byte_feature(data[p:p + H.WIN_BYTES])
        nb[i] = data[p + H.WIN_BYTES]          # the TRUE next byte after this window
    return X, nb, data, start


def assign(protos, x):
    """nearest prototype by L2 (VERBATIM h1163.assign / vadapt_field mechanism)."""
    d = np.linalg.norm(protos - x[None], axis=1)
    j = int(np.argmin(d))
    return j, float(d[j])


def run_generative(X, nb, mitosis_on, max_cells):
    """Drive the VAdaptField + per-cell generative next-byte head over the scored span.

    p8 / gradient-free: the mitosis tick (split) IS the learning; the per-cell next-byte
    counts are accumulated online (a count add, no backprop). HELD-OUT scoring: the CE of
    the true next byte is read from cell j's distribution BEFORE that byte is added to the
    counts, so every scored byte is a genuine prediction.

    Returns:
      mean_ce      : mean next-byte CE (bits/byte) over the scored span
      traj         : list of (block_idx, n_cells_at_block_end, block_mean_ce) for F2
      final_cells  : final cell count
      protos, counts : the grown model (for decode samples)
    """
    Xs = X[H.WARMUP:H.WARMUP + H.T].astype(float)
    nbs = nb[H.WARMUP:H.WARMUP + H.T]
    protos = [Xs[0].copy()]                                  # one seed prototype (vadapt_field_new)
    counts = [np.full(VOCAB, LAPLACE, dtype=float)]          # cell 0 next-byte counts (Laplace prior)
    ce_sum, ce_n = 0.0, 0
    traj = []
    blk_sum, blk_n = 0.0, 0
    for i in range(len(Xs)):
        x = Xs[i]
        j, err = assign(np.asarray(protos), x)
        # PREDICT (held-out): CE of the TRUE next byte under cell j's current distribution
        c = counts[j]
        p_true = c[nbs[i]] / c.sum()
        ce = -math.log2(max(p_true, 1e-12))
        ce_sum += ce; ce_n += 1
        blk_sum += ce; blk_n += 1
        # UPDATE cell j's next-byte counts with the true next byte (online)
        counts[j][nbs[i]] += 1.0
        # SPLIT (H_1199 VAdaptField rule): novel feature -> spawn a cell carrying the
        # parent's counts (heredity, p8); else online winner-pull on the feature proto.
        if mitosis_on and err > SPLIT_THRESH and len(protos) < max_cells:
            protos.append(x.copy())
            counts.append(counts[j].copy())                  # daughter inherits parent distribution
        else:
            protos[j] = protos[j] + LR * (x - protos[j])     # winner-pull (vadapt_field_step)
        if (i + 1) % BLOCK == 0:
            traj.append((i // BLOCK, len(protos), blk_sum / max(blk_n, 1)))
            blk_sum, blk_n = 0.0, 0
    mean_ce = ce_sum / max(ce_n, 1)
    return mean_ce, traj, len(protos), np.asarray(protos), [c.copy() for c in counts]


def decode_sample(protos, counts, data, start, n_steps, greedy, seed):
    """Decode a short SAMPLE from the grown/frozen model (p7 honesty cross-check, NOT a
    verdict). Seed the generation from a real corpus window, then repeatedly: featurise
    the current trailing WIN_BYTES window -> nearest cell -> emit the next byte from its
    distribution (greedy=argmax, else sampled) -> append the byte -> slide the window.
    The emitted bytes ARE the model's continuation. Returns the emitted bytes only."""
    rng = np.random.default_rng(seed + 31337)
    # seed window = a real corpus window (the same start the model trained from)
    win = bytearray(data[start: start + H.WIN_BYTES])
    out = bytearray()
    for _ in range(n_steps):
        feat = H._byte_feature(bytes(win))
        j, _ = assign(protos, feat)
        dist = counts[j] / counts[j].sum()
        if greedy:
            b = int(np.argmax(dist))
        else:
            b = int(rng.choice(VOCAB, p=dist))
        out.append(b)
        win = win[1:] + bytes([b])                           # slide the window by one byte
    return bytes(out)


def _show(bs):
    """Render emitted bytes for a human, replacing non-printable / invalid utf-8."""
    try:
        s = bs.decode("utf-8")
    except UnicodeDecodeError:
        s = bs.decode("latin-1")
    return "".join(ch if (32 <= ord(ch) < 127 or ord(ch) > 160) else "." for ch in s)


def main():
    print("=== H_1200 — MITOSIS-GENERATIVE-GROWTH (Lane-2, $0 local CPU, numpy mirror) ===", flush=True)
    print(f"  DIM={DIM} SPLIT_THRESH={SPLIT_THRESH} LR={LR} VOCAB={VOCAB} SEEDS={SEEDS} T={H.T}", flush=True)
    print(f"  mechanism = H_1199 VAdaptField (recon-err>{SPLIT_THRESH} split) + per-cell next-byte head", flush=True)
    print(f"  F1: ON CE < OFF CE by >= {F1_MARGIN} b/byte | F2: Spearman(n_cells,-CE) > {F2_SPEARMAN_BAR}\n", flush=True)

    on_ces, off_ces, on_finals = [], [], []
    pooled_cells, pooled_negce = [], []     # F2 trajectory pooled over seeds
    per_seed = []
    sample_pack = None
    for s in SEEDS:
        X, nb, data, start = build_targets(s)
        on_ce, on_traj, on_final, on_protos, on_counts = run_generative(X, nb, True, MAX_CELLS)
        off_ce, off_traj, off_final, off_protos, off_counts = run_generative(X, nb, False, MAX_CELLS)
        on_ces.append(on_ce); off_ces.append(off_ce); on_finals.append(on_final)
        for (_, nc, bce) in on_traj:
            pooled_cells.append(nc); pooled_negce.append(-bce)
        per_seed.append({"seed": s, "on_ce": round(on_ce, 4), "off_ce": round(off_ce, 4),
                         "delta": round(off_ce - on_ce, 4), "on_final_cells": on_final,
                         "off_final_cells": off_final})
        print(f"  seed {s}: ON CE={on_ce:.4f}  OFF CE={off_ce:.4f}  delta(OFF-ON)={off_ce-on_ce:+.4f} b/byte  "
              f"cells ON 1->{on_final}  OFF=1", flush=True)
        if sample_pack is None:                 # keep the first seed's models for decode samples
            sample_pack = (data, start, s, on_protos, on_counts, off_protos, off_counts, on_final)

    on_mean = float(np.mean(on_ces)); off_mean = float(np.mean(off_ces))
    delta = off_mean - on_mean
    spearman_growth = _spearman(pooled_cells, pooled_negce)

    f1 = bool(delta >= F1_MARGIN)
    f2 = bool(spearman_growth > F2_SPEARMAN_BAR)
    supported = bool(f1 and f2)

    # ---- p7 honesty cross-check: decode samples grown vs frozen, VERBATIM ----
    data, start, s0, on_protos, on_counts, off_protos, off_counts, on_final = sample_pack
    N_STEPS = 80
    seed_ctx = _show(data[start: start + H.WIN_BYTES])
    grown_greedy = decode_sample(on_protos, on_counts, data, start, N_STEPS, True, s0)
    frozen_greedy = decode_sample(off_protos, off_counts, data, start, N_STEPS, True, s0)
    grown_samp = decode_sample(on_protos, on_counts, data, start, N_STEPS, False, s0)
    frozen_samp = decode_sample(off_protos, off_counts, data, start, N_STEPS, False, s0)
    samples = {
        "seed": s0, "n_steps": N_STEPS, "seed_window": seed_ctx,
        "grown_cells": on_final, "frozen_cells": 1,
        "grown_greedy": _show(grown_greedy), "frozen_greedy": _show(frozen_greedy),
        "grown_sampled": _show(grown_samp), "frozen_sampled": _show(frozen_samp),
    }

    if supported:
        ruling = ("GREEN GROWTH-IS-GENERATIVE: mitosis-growth LOWERS next-byte cross-entropy on "
                  "real text — F1 (ON CE < OFF CE by >= %.2f b/byte) AND F2 (CE falls as cells "
                  "grow, Spearman(n_cells,-CE) > 0). Growing prototype cells each specialise to a "
                  "local-text regime and predict its next byte better than one global table. The "
                  "growth -> generation LINK holds: this is the FIRST rung of the mitosis-LM ladder "
                  "secured. SCOPE: toy DIM=8-feature-keyed gradient-free prototype-LM, ONE corpus; "
                  "scale + true conversational coherence UNVERIFIED — NOT a chat claim." % F1_MARGIN)
    else:
        why = []
        if not f1:
            why.append("F1 fail: ON does NOT beat OFF by the frozen margin "
                       "(delta=%.4f < %.2f b/byte) — growth did not buy real generative gain" % (delta, F1_MARGIN))
        if not f2:
            why.append("F2 fail: CE does NOT fall monotonically as cells grow "
                       "(Spearman(n_cells,-CE)=%.4f <= %.2f)" % (spearman_growth, F2_SPEARMAN_BAR))
        ruling = ("RED CLOSED-NEG: mitosis-growth is CLUSTERING, not language-learning. " + " | ".join(why) +
                  ". Growing prototype cells lowers L2 reconstruction error (H_1198/H_1199) but does NOT "
                  "improve next-byte generation => the naive pure-mitosis -> chat path is falsified "
                  "cheaply HERE; conversational language needs a different mechanism (redirect to the CLM "
                  "lane). a_paper_negative_ok — a closed-negative that rules out the naive path is a valid, "
                  "valuable result.")

    verdict = {
        "H": "H_1200",
        "title": "MITOSIS-GENERATIVE-GROWTH — does growing prototype cells lower next-byte CE on "
                 "real text (growth -> generation link), or only improve clustering?",
        "compute": "local CPU ($0), numpy mirror of the H_1199 VAdaptField",
        "lane": "Lane-2 gradient-free growth (a_lane_akida_gpu_split)",
        "frozen_falsifier": {
            "F1": "mitosis-ON next-byte CE (b/byte) < OFF by >= %.2f, pooled over seeds" % F1_MARGIN,
            "F2": "Spearman(n_cells, -CE) > %.2f across the stream (growth buys the gain)" % F2_SPEARMAN_BAR,
            "F3": "(live .hexa only) Psi Phi-checksum byte-identical ON==OFF — NUMPY MIRROR here, "
                  ".hexa lift is the next rung (NOT claimed)",
            "metric": "next-byte cross-entropy bits/byte (CAPABILITY probe, p7 — paired with decoded "
                      "samples; CE is NOT a consciousness/chat verdict)",
            "SUPPORTED": "F1 AND F2",
        },
        "seeds": SEEDS,
        "scored_span": H.T,
        "per_seed": per_seed,
        "F1_generative_gain": {"ON_mean_ce_bits": round(on_mean, 4), "OFF_mean_ce_bits": round(off_mean, 4),
                               "delta_OFF_minus_ON": round(delta, 4), "margin_bar": F1_MARGIN, "pass": f1},
        "F2_monotone_growth": {"spearman_ncells_negCE": round(spearman_growth, 4),
                               "bar_above": F2_SPEARMAN_BAR, "n_traj_points": len(pooled_cells), "pass": f2},
        "F3_substrate_intact": {"status": "numpy-mirror (not live .hexa)",
                                "note": ".hexa lift = extend CORE/engine_cli.hexa VAdaptField with the "
                                        "generative head, F3-guarded (Psi byte-identical ON==OFF); NEXT rung."},
        "on_final_cells": on_finals,
        "decode_samples_p7": samples,
        "supported": supported,
        "ruling": ruling,
        "scope": ("TOY/small real-corpus FIRST rung, gradient-free prototype-LM (DIM=8 feature-keyed "
                  "next-byte tables, 256-byte vocab, ONE corpus). The DIM=8 window is a COARSE context "
                  "(no within-window token order) so absolute CE is far from a real LM; the FALSIFIER is "
                  "the ON-vs-OFF DELTA under the SAME coarse context, not the absolute number. Scale + "
                  "true conversational coherence UNVERIFIED — tests ONLY the growth -> generation LINK, "
                  "NOT chat (a_scale_honest_scope). $0 local CPU, numpy, deterministic seeds."),
    }
    print("\n=== DECODE SAMPLES (p7 honesty cross-check — VERBATIM, NOT the verdict) ===", flush=True)
    print(f"  seed window : {seed_ctx!r}", flush=True)
    print(f"  GROWN  ({on_final} cells) greedy : {samples['grown_greedy']!r}", flush=True)
    print(f"  FROZEN (1 cell)   greedy : {samples['frozen_greedy']!r}", flush=True)
    print(f"  GROWN  ({on_final} cells) sampled: {samples['grown_sampled']!r}", flush=True)
    print(f"  FROZEN (1 cell)   sampled: {samples['frozen_sampled']!r}", flush=True)
    print("\n=== VERDICT ===", flush=True)
    print(f"  F1 ON CE={on_mean:.4f} < OFF CE={off_mean:.4f}  delta={delta:+.4f} b/byte (bar {F1_MARGIN}) -> {'PASS' if f1 else 'FAIL'}", flush=True)
    print(f"  F2 Spearman(n_cells,-CE)={spearman_growth:+.4f} (bar >{F2_SPEARMAN_BAR}) -> {'PASS' if f2 else 'FAIL'}", flush=True)
    print(f"  ON cells 1->{int(np.mean(on_finals))} (mean)  OFF=1\n", flush=True)
    print(f"  {'🟢 SUPPORTED' if supported else '🔴 CLOSED-NEG'}: {ruling}", flush=True)
    json.dump(verdict, open("/tmp/h1200_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n  wrote /tmp/h1200_result.json", flush=True)
    print("[done]", flush=True)
    return verdict


if __name__ == "__main__":
    main()
