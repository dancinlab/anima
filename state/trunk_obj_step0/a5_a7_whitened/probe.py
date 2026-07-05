#!/usr/bin/env python3
"""H_9200 A5+A7 whitened re-measure (fixes the raw-anisotropy INVALID, conv probe-py-1).

Raw final-LN hidden is extremely anisotropic (cos~0.9996) so raw-cos bars collapse.
Fix: center_zscore over the GLOBAL rep population (all forwards pooled), exactly the
§4 / l5_discriminator preprocess, THEN apply the A5/A7 frozen bars. py-terminal eligible.

PREREG bars (frozen, unchanged from raw version):
  A5 orbit:    whitened orbit pairwise cos >= 0.90 AND content-swapped control cos <= 0.60
               on >= 2/3 pairs.
  A7 reversal: 1 - cos_whitened(h(A>B), h(B>A)) >= 0.10 AND identical-control cos >= 0.99
               on >= 2/3 pairs.

Decision: BOTH-FAIL (whitened) => no latent factorized basis even after decorrelation
=> terminalizes E_GEOMETRY INCONCLUSIVE => clean owner GPU-go for E1.
>=1 PASS => a latent signal survives whitening => deepen before E1."""
import os, sys, json, time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as d

CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
PAIRS = [("consciousness", "information"), ("system", "mechanism"), ("learning", "brain")]


def orbit(a, b): return [f"{a} exceeds {b}", f"{a} over {b}", f"more {a} than {b}", f"{a} beyond {b}"]
def swapped(a, b): return f"{b} exceeds {a}"
def ab(a, b): return f"{a}>{b}"


def h_raw(W, s):
    ids = list(s.encode("utf-8", "surrogateescape"))
    return d.bg_forward_last_hidden(W, ids, len(ids))


def main():
    t0 = time.time()
    print("[load] 303M h1129 ...", flush=True)
    W = d.bg_load(CKPT); assert d.bg_is_bytegpt(CKPT)
    print(f"      loaded ({time.time()-t0:.1f}s)", flush=True)

    # collect ALL forwards (global population for whitening, like §4 / l5_discriminator)
    recs = []  # (tag, pair_idx, vec)
    for pi, (a, b) in enumerate(PAIRS):
        for tag, s in [(f"orb0", orbit(a, b)[0]), (f"orb1", orbit(a, b)[1]),
                       (f"orb2", orbit(a, b)[2]), (f"orb3", orbit(a, b)[3]),
                       ("ctrl", swapped(a, b)),
                       ("ab", ab(a, b)), ("ba", ab(b, a)), ("ab2", ab(a, b))]:
            recs.append((tag, pi, h_raw(W, s)))
    R = np.stack([r[2] for r in recs])                  # [N, d]
    mu = R.mean(0, keepdims=True); sd = R.std(0, keepdims=True) + 1e-6
    Rw = (R - mu) / sd                                  # center_zscore, §4 identical
    vec = {(tag, pi): Rw[i] for i, (tag, pi, _) in enumerate(recs)}

    def cos(u, v): return float(u @ v) / ((np.linalg.norm(u) + 1e-9) * (np.linalg.norm(v) + 1e-9))

    a5, a7 = [], []
    for pi, (a, b) in enumerate(PAIRS):
        orb = [vec[(f"orb{i}", pi)] for i in range(4)]
        ctrl = vec[("ctrl", pi)]
        pair_cos = [cos(orb[i], orb[j]) for i in range(4) for j in range(i + 1, 4)]
        orbit_min = min(pair_cos); control_cos = cos(orb[0], ctrl)
        p5 = orbit_min >= 0.90 and control_cos <= 0.60
        a5.append(dict(pair=f"{a}>{b}", orbit_min_cos=orbit_min, control_cos=control_cos, passed=bool(p5)))

        hab = vec[("ab", pi)]; hba = vec[("ba", pi)]; hab2 = vec[("ab2", pi)]
        antisym = 1.0 - cos(hab, hba); identical = cos(hab, hab2)
        p7 = antisym >= 0.10 and identical >= 0.99
        a7.append(dict(pair=f"{a}>{b}", antisymmetry=antisym, identical_control_cos=identical, passed=bool(p7)))
        print(f"  {a}>{b}: A5 orbit_min={orbit_min:.3f} ctrl={control_cos:.3f} "
              f"({'PASS' if p5 else 'fail'}) | A7 antisym={antisym:.3f} ident={identical:.3f} "
              f"({'PASS' if p7 else 'fail'})", flush=True)

    a5v = "PASS" if sum(r["passed"] for r in a5) >= 2 else "FAIL"
    a7v = "PASS" if sum(r["passed"] for r in a7) >= 2 else "FAIL"
    both_fail = (a5v == "FAIL" and a7v == "FAIL")
    decision = ("BOTH-FAIL (whitened) → E_GEOMETRY terminal → clean owner GPU-go for E1"
                if both_fail else ">=1 PASS (whitened) → latent signal survives → deepen before E1")
    out = dict(probe="H_9200 A5+A7 whitened re-measure (fixes raw-anisotropy INVALID)",
               ckpt=CKPT, preprocess="center_zscore over global rep population (§4 / l5_discriminator identical)",
               A5_verdict=a5v, A7_verdict=a7v, both_fail=both_fail, decision=decision,
               A5_results=a5, A7_results=a7,
               bar_A5="whitened orbit cos>=0.90 AND control<=0.60 on >=2/3",
               bar_A7="1-whitened-cos(A>B,B>A)>=0.10 AND identical>=0.99 on >=2/3",
               honesty="py 2-production numpy TERMINAL-eligible; whitening removes the anisotropy artifact.")
    print("\n" + json.dumps(out, indent=2))
    with open(f"{_HERE}/RESULT.json", "w") as f: json.dump(out, f, indent=2)
    print(f"\n[done] {time.time()-t0:.1f}s | A5={a5v} A7={a7v} | {decision}")


if __name__ == "__main__":
    main()
