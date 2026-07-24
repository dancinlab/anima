#!/usr/bin/env python3
"""V6_39 -- re-read the V6_26 LANE-BUS premise on an ALIGNED bus. ($0)

V6_26 is the gate that licensed the whole LANE-BUS engine: it reported that the logit-row
content tension is ~15-dimensional, i.e. "headroom exists" for independently-earned lanes to
write onto a shared bus. It computed `comp[pos] - rl[tl-1]` — but those two rows score
DIFFERENT target bytes (composed row `pos` predicts b[pos+1]; the reflex window ending at
`pos` predicts b[pos]). So a large part of what V6_26 measured as "what broad context adds"
was a one-position shift of the SAME lane against itself.

This re-reads the identical quantity with both lanes on the same decision point, and prints
the misaligned number beside it so the correction is legible. Same corpus, same model,
same effective-dimension estimator (participation ratio of the eigenspectrum).

Engine-native (decode._fwd_logits). Reuses trained57.clm + natural held-out text.
"""
import sys, os, re, importlib.util
import numpy as np

W_LOC = 8; N_SENT = 120; HELDOUT_FRAC = 0.20
_DATE = re.compile(r"^\s*\d{3,4}\s*[–-]"); _YEAR = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")


def prose(txt):
    for line in txt.split("\n"):
        line = line.strip()
        if not line or _DATE.match(line): continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (40 < len(s) < 300) or _YEAR.search(s): continue
            if s.count(",") > 6 or sum(c.isdigit() for c in s) > 12: continue
            if s.endswith((".", "!", "?")): yield s


def _decode():
    spec = importlib.util.find_spec("anima_py")
    if spec and spec.submodule_search_locations:
        b = list(spec.submodule_search_locations)[0]
        for c in (os.path.join(b, "core"), b):
            if os.path.isdir(c): sys.path.insert(0, c)
    for c in ("core", "/opt/homebrew/lib/python3.14/site-packages/anima_py/core"):
        if os.path.isdir(c): sys.path.insert(0, c)


def eff_dims(M):
    """Two participation ratios, because V6_26 used the wrong spectrum.

    pr_lambda -- PR over the covariance EIGENvalues (lam = sigma^2). This is the standard
                 "how many dimensions carry the variance" effective rank.
    pr_sigma  -- PR over the SINGULAR values, which is what v6_26_lanebus_tension.py's
                 pr_eff_rank() computes: (sum s)^2 / sum s^2. It is not a variance
                 dimensionality and it reads systematically higher.
    """
    X = M - M.mean(0, keepdims=True)
    s = np.linalg.svd(X, compute_uv=False)
    ev = s ** 2
    if ev.sum() <= 0: return 0.0, 0.0, 0
    pr_l = float((ev.sum() ** 2) / (ev ** 2).sum())
    pr_s = float((s.sum() ** 2) / (ev.sum() + 1e-12))
    c = np.cumsum(ev) / ev.sum()
    return pr_l, pr_s, int(np.searchsorted(c, 0.90) + 1)


def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "lab/v6/trained57.clm"
    full = open(os.path.expanduser("~/anima-weights/en_general.txt"),
                encoding="utf-8", errors="ignore").read()
    eval_txt = full[int(len(full) * (1 - HELDOUT_FRAC)):]
    sents = []
    for s in prose(eval_txt):
        sents.append(s)
        if len(sents) >= N_SENT: break
    _decode(); import decode as clm
    W = clm.clm_load_weights(model)

    def fwd(seq):
        n = len(seq)
        return clm._fwd_logits(W, np.array([float(x) for x in seq], dtype=np.float64), n)

    aligned, misaligned, comp_rows = [], [], []
    for s in sents:
        b = list(s.encode("utf-8")); Lb = len(b)
        if Lb < W_LOC + 4: continue
        comp_all = fwd(b[:Lb - 1])                       # row i predicts b[i+1]
        for i in range(W_LOC - 1, Lb - 2):
            cp = comp_all[i]                             # predicts b[i+1]
            rl_ok = fwd(b[i + 1 - W_LOC:i + 1])[W_LOC - 1]   # ALSO predicts b[i+1]
            aligned.append(cp - rl_ok)
            comp_rows.append(cp)
            if i >= W_LOC:                               # V6_26's window: predicts b[i]
                rl_bad = fwd(b[i - W_LOC:i])[W_LOC - 1]
                misaligned.append(cp - rl_bad)

    A = np.array(aligned); B = np.array(misaligned); C = np.array(comp_rows)
    pr_a, ps_a, r90_a = eff_dims(A)
    pr_b, ps_b, r90_b = eff_dims(B)
    pr_c, ps_c, r90_c = eff_dims(C)
    print(f"# V6_39 -- LANE-BUS premise re-read on an ALIGNED bus  (model={os.path.basename(model)})")
    print(f"sample: {len(sents)} sentences, {A.shape[0]} positions, V={A.shape[1]}, window={W_LOC}B\n")
    print("Two defects compound in V6_26's '15.3': the lanes scored different target bytes,")
    print("AND the effective rank was taken over singular values instead of eigenvalues.\n")
    print(f"{'quantity':<32}{'PR(sigma) = V6_26':>19}{'PR(lambda) = correct':>22}{'rank@90%':>10}{'mean|row|':>12}")
    print(f"{'-'*95}")
    print(f"{'MISALIGNED tension (V6_26)':<32}{ps_b:>19.2f}{pr_b:>22.2f}{r90_b:>10}{np.abs(B).mean():>12.4f}")
    print(f"{'ALIGNED tension (corrected)':<32}{ps_a:>19.2f}{pr_a:>22.2f}{r90_a:>10}{np.abs(A).mean():>12.4f}")
    print(f"{'composed row (reference)':<32}{ps_c:>19.2f}{pr_c:>22.2f}{r90_c:>10}{np.abs(C).mean():>12.4f}")
    print()
    print(f"defect decomposition of the headline (both applied to the same rows):")
    print(f"  estimator alone (misaligned, sigma -> lambda): {ps_b:.1f} -> {pr_b:.2f}")
    print(f"  alignment alone (sigma spectrum, mis -> aligned): {ps_b:.1f} -> {ps_a:.2f}")
    print(f"  both corrected: {ps_b:.1f} -> {pr_a:.2f}")
    print(f"  magnitude: the misaligned bus carried {np.abs(B).mean()/max(np.abs(A).mean(),1e-9):.1f}x the real one.")
    print()
    if pr_a >= 8:
        print(f"→ PREMISE SURVIVES: even aligned, the content lane adds {pr_a:.1f} effective dims of")
        print("  logit-row structure — a shared bus still has something to carry.")
    elif pr_a >= 3:
        print(f"→ PREMISE WEAKENED: aligned headroom is {pr_a:.1f} eff-dims, well under V6_26's read.")
        print("  A multi-lane bus is not obviously licensed by this much structure.")
    else:
        print(f"→ PREMISE FAILS: aligned content tension is {pr_a:.1f} eff-dims — essentially a")
        print("  scalar. LANE-BUS's 'independently-earned lanes meet on the logit row' has no")
        print("  measured headroom to meet in.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
