#!/usr/bin/env python3
"""H_9200 A7 deepen — position-encoding artifact vs genuine content composition.

A7 PASS (whitened reversal antisym 0.65-1.05) could be pure POSITION encoding (the 303M
byte-transformer assigns absolute positions; A>B vs B>A differ in which bytes sit where
→ trivially different last-hidden) rather than compositional binding of the two concepts'
CONTENT. This probe separates them.

PREREG bars (frozen before run):
  POSITION-ARTIFACT hypothesis:  across many concept-pairs, whitened antisym is roughly
    CONSTANT (low variance) — only positions matter, content doesn't.
  CONTENT-COMPOSITION hypothesis: whitened antisym VARIES with the concept pair and
    correlates with a content-distance proxy.

  Decision:
    - std(antisym across pairs) < 0.10  → POSITION-ARTIFACT (A7 not a G1 crack; E1 proceeds).
    - |corr(antisym, content_dist)| > 0.30 AND std(antisym) > 0.15 → CONTENT signal exists
      (worth a GPU arm before E1).
    - otherwise INCONCLUSIVE.

Single 303M load, ~12 pairs × 4 forwards, center_zscore whitening (§4/A7 identical)."""
import os, sys, json, time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as d

CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
# 12 concept-pairs spanning diverse content (so a position-only model gives constant antisym)
PAIRS = [("consciousness", "information"), ("system", "mechanism"), ("learning", "brain"),
         ("model", "byte"), ("energy", "field"), ("memory", "time"),
         ("language", "syntax"), ("truth", "belief"), ("noise", "signal"),
         ("self", "other"), ("growth", "decay"), ("order", "chaos")]


def h_raw(W, s):
    ids = list(s.encode("utf-8", "surrogateescape"))
    return d.bg_forward_last_hidden(W, ids, len(ids))


def main():
    t0 = time.time()
    print("[load] 303M h1129 ...", flush=True)
    W = d.bg_load(CKPT); assert d.bg_is_bytegpt(CKPT)
    print(f"      loaded ({time.time()-t0:.1f}s)", flush=True)

    # collect ALL forwards for global whitening (position-fixed framing "X>Y" / "Y>X" / "X>X" ident control)
    recs = []
    for pi, (a, b) in enumerate(PAIRS):
        recs.append(("ab", pi, h_raw(W, f"{a}>{b}")))
        recs.append(("ba", pi, h_raw(W, f"{b}>{a}")))
        recs.append(("aa", pi, h_raw(W, f"{a}>{a}")))    # identical-content control (pos differ, content same→symmetric)
    R = np.stack([r[2] for r in recs])
    mu = R.mean(0, keepdims=True); sd = R.std(0, keepdims=True) + 1e-6
    Rw = (R - mu) / sd
    vec = {(tag, pi): Rw[i] for i, (tag, pi, _) in enumerate(recs)}

    def cos(u, v): return float(u @ v) / ((np.linalg.norm(u) + 1e-9) * (np.linalg.norm(v) + 1e-9))

    rows = []
    antisyms = []; ident_controls = []
    for pi, (a, b) in enumerate(PAIRS):
        hab = vec[("ab", pi)]; hba = vec[("ba", pi)]; haa = vec[("aa", pi)]
        antisym = 1.0 - cos(hab, hba)                 # order signal
        # content distance proxy: 1 - cos of the two single-token-ish reps in the > framing
        rows.append(dict(pair=f"{a}>{b}", antisym=antisym))
        antisyms.append(antisym)
    antisyms = np.array(antisyms)

    # content-distance proxy: pairwise cos between single-concept reps h(a), h(b), WHITENED in the same pool
    # re-pool with singles for a clean content-distance
    singles = []
    for a, b in PAIRS:
        singles.append(("a", h_raw(W, a))); singles.append(("b", h_raw(W, b)))
    Rs = np.stack([s[1] for s in singles]); mus = Rs.mean(0, keepdims=True); sds = Rs.std(0, keepdims=True) + 1e-6
    Sw = (Rs - mus) / sds
    def cos_s(u, v): return float(u @ v) / ((np.linalg.norm(u) + 1e-9) * (np.linalg.norm(v) + 1e-9))
    content_dists = []
    for i, (a, b) in enumerate(PAIRS):
        ha = Sw[2 * i]; hb = Sw[2 * i + 1]
        content_dists.append(1.0 - cos_s(ha, hb))
    content_dists = np.array(content_dists)

    std_a = float(np.std(antisyms)); mean_a = float(np.mean(antisyms))
    if np.std(content_dists) > 1e-9:
        corr = float(np.corrcoef(antisyms, content_dists)[0, 1])
    else:
        corr = float("nan")

    if std_a < 0.10:
        verdict = "POSITION-ARTIFACT (antisym constant across pairs → A7 not a G1 crack → E1 proceeds)"
    elif abs(corr) > 0.30 and std_a > 0.15:
        verdict = "CONTENT signal exists (antisym varies with concept pair → worth GPU arm before E1)"
    else:
        verdict = "INCONCLUSIVE"
    out = dict(probe="H_9200 A7 deepen — position-artifact vs content-composition",
               ckpt=CKPT, preprocess="center_zscore (§4/A7 identical)",
               n_pairs=len(PAIRS), mean_antisym=mean_a, std_antisym=std_a,
               corr_antisym_contentdist=corr, verdict=verdict,
               bar="POSITION-ARTIFACT if std<0.10; CONTENT if |corr|>0.30 AND std>0.15; else INCONCLUSIVE",
               per_pair=[dict(pair=r["pair"], antisym=round(r["antisym"], 4),
                              content_dist=round(float(content_dists[i]), 4))
                         for i, r in enumerate(rows)],
               honesty="py 2-production numpy TERMINAL-eligible; frozen-rep probe, no training — can refute position-artifact, cannot prove learnable composition (E1 needed for that).")
    print("\n" + json.dumps(out, indent=2, default=float))
    with open(f"{_HERE}/RESULT.json", "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\n[done] {time.time()-t0:.1f}s | mean_antisym={mean_a:.3f} std={std_a:.3f} corr={corr:.3f} | {verdict}")


if __name__ == "__main__":
    main()
