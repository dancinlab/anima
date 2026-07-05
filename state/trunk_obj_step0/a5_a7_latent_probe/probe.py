#!/usr/bin/env python3
"""H_9200 A5+A7 — latent frozen-rep probe pair (Fable sweep next-H, $0 mini).

The synthesis (SWEEP_SYNTHESIS.md) named this the immediate next-H: if BOTH fail,
the frozen 303M rep has no latent factorized basis → terminalize E_GEOMETRY
INCONCLUSIVE → clean owner GPU-go ask for E1 (CE-deleted forward-slot).

PREREG (frozen, from cluster_A_MODEL_LOAD_PREREG.md):
  A5 paraphrase orbit: same relation, lexical/voice surface change.
      PASS  iff orbit pairwise cos >= 0.90 AND content-swapped control cos <= 0.60
            on >= 2/3 concept-pairs.
  A7 counterfactual reversal: A>B vs B>A must differ.
      PASS  iff 1 - cos(h(A>B), h(B>A)) >= 0.10 AND identical-control cos >= 0.99
            on >= 2/3 concept-pairs.

Single 303M load (core/decode.py bg_forward_last_hidden == anima evaluate --py).
~6 forwards/pair x 3 pairs = ~18 forwards total. mini-safe (far lighter than §4's 2600).
Frozen bars pre-registered BEFORE running (a_break_the_wall, no tune-to-green)."""
import os, sys, json, time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))
import decode as d

CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
# 3 concept-pairs act as the "seeds" (deterministic forward; diversity via pairs)
PAIRS = [("consciousness", "information"), ("system", "mechanism"), ("learning", "brain")]
# A5 orbit: same "A exceeds B" relation, surface variation
def orbit(a, b):
    return [f"{a} exceeds {b}", f"{a} over {b}", f"more {a} than {b}", f"{a} beyond {b}"]
# content-swapped control: relation reversed (B exceeds A) — meaning changed
def swapped(a, b):
    return f"{b} exceeds {a}"
# A7: forward "A>B" vs "B>A"; identical control = same string twice
def ab(a, b): return f"{a}>{b}"


def cos(u, v):
    nu = np.linalg.norm(u) + 1e-9; nv = np.linalg.norm(v) + 1e-9
    return float(u @ v / (nu * nv))


def h(W, s):
    ids = list(s.encode("utf-8", "surrogateescape"))
    return d.bg_forward_last_hidden(W, ids, len(ids))


def run_a5(W, a, b):
    orb = [h(W, s) for s in orbit(a, b)]          # 4 forwards
    ctrl = h(W, swapped(a, b))                    # 1 forward
    # orbit invariance: min pairwise cosine across the orbit
    pair_cos = [cos(orb[i], orb[j]) for i in range(len(orb)) for j in range(i + 1, len(orb))]
    orbit_min = min(pair_cos)
    control_cos = cos(orb[0], ctrl)               # orbit member vs swapped-meaning
    passed = orbit_min >= 0.90 and control_cos <= 0.60
    return dict(orbit_min_cos=orbit_min, control_cos=control_cos, passed=passed)


def run_a7(W, a, b):
    hab = h(W, ab(a, b)); hba = h(W, ab(b, a))    # 2 forwards
    hab2 = h(W, ab(a, b))                          # identical control (re-forward)
    antisym = 1.0 - cos(hab, hba)
    identical = cos(hab, hab2)
    passed = antisym >= 0.10 and identical >= 0.99
    return dict(antisymmetry=antisym, identical_control_cos=identical, passed=passed)


def main():
    t0 = time.time()
    print("[load] 303M h1129 ...", flush=True)
    W = d.bg_load(CKPT); assert d.bg_is_bytegpt(CKPT)
    print(f"      loaded d={W['d']} ({time.time()-t0:.1f}s)", flush=True)
    a5 = []; a7 = []
    for a, b in PAIRS:
        r5 = run_a5(W, a, b); r5["pair"] = f"{a}>{b}"; a5.append(r5)
        r7 = run_a7(W, a, b); r7["pair"] = f"{a}>{b}"; a7.append(r7)
        print(f"  {a}>{b}: A5 orbit_min={r5['orbit_min_cos']:.3f} ctrl={r5['control_cos']:.3f} "
              f"({'PASS' if r5['passed'] else 'fail'}) | A7 antisym={r7['antisymmetry']:.3f} "
              f"ident={r7['identical_control_cos']:.3f} ({'PASS' if r7['passed'] else 'fail'})", flush=True)
    a5_pass = sum(r["passed"] for r in a5); a7_pass = sum(r["passed"] for r in a7)
    a5_verdict = "PASS" if a5_pass >= 2 else "FAIL"
    a7_verdict = "PASS" if a7_pass >= 2 else "FAIL"
    # synthesis decision rule: BOTH fail => no latent factorized basis => E1 GPU-go
    both_fail = (a5_verdict == "FAIL" and a7_verdict == "FAIL")
    decision = ("BOTH-FAIL → E_GEOMETRY terminal → clean owner GPU-go for E1 (CE-deleted forward-slot)"
                if both_fail else
                ">=1 PASS → latent factorized signal exists → deepen A5/A7 before E1")
    out = dict(probe="H_9200 A5+A7 latent frozen-rep pair", ckpt=CKPT,
               engine=f"real ByteGPT-303M h1129 d={W['d']} (core/decode.py bg_forward_last_hidden == anima evaluate --py)",
               pairs=PAIRS,
               bar_A5="orbit pairwise cos>=0.90 AND content-swapped control cos<=0.60 on >=2/3 pairs",
               bar_A7="1-cos(h(A>B),h(B>A))>=0.10 AND identical-control cos>=0.99 on >=2/3 pairs",
               A5_results=a5, A7_results=a7,
               A5_verdict=a5_verdict, A7_verdict=a7_verdict,
               both_fail=both_fail, decision=decision,
               honesty="py 2-production numpy = engine-native TERMINAL-eligible; latent frozen-rep probe (no training).",
               elapsed_s=round(time.time() - t0, 1))
    print("\n" + json.dumps(out, indent=2))
    with open(f"{_HERE}/RESULT.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[done] {out['elapsed_s']}s -> RESULT.json | A5={a5_verdict} A7={a7_verdict} | {decision}")


if __name__ == "__main__":
    main()
