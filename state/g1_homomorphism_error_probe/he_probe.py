"""he_probe.py — H_1821 Homomorphism-Error (HE) cheap G1 pre-screen.

numpy ONLY — torch-free, gauge_lib-free. This is explicitly a DIRECTIONAL
proxy/pre-screen (p7), NEVER a terminal verdict. G1 SSOT remains engine-native
G0-G6 eval (`anima evaluate`). HE is a cheap compass for "where to spend GPU".

HE metric (An & Du, NeurReps 2025 #142; R^2=0.73 with OOD compositional gen):
  For concept pairs {A, B}, take trunk penultimate reps r(A), r(B), r(A o B):
    HE = E|| r(AoB) - (r(A) (+) r(B)) || / E|| r(AoB) ||      (normalized)
  for (+) in {additive: r(A)+r(B), hadamard-bind: r(A)*r(B)}.
  Lower HE = composition operation better preserved by the representation.

anima is a byte-CLM, so expression-space = concept-token byte-span (transcend
axis, vs SCAN symbol space). r(concept) = the CLMConvMoE trunk penultimate `yn`
(post final-groupnorm, pre readout) at the LAST position of the concept fed
right-aligned in the T=24 causal window (= exactly the decode-time context the
mouth conditions on). A o B = byte concatenation A+B.

Reps are taken from core/clm_decode.py (the byte-faithful CLMConvMoE forward),
re-used up to `yn`. No torch anywhere.

Usage:
  python3 he_probe.py                       # self-test only
  python3 he_probe.py <ckpt1.clm> [ckpt2 ..] # self-test + real HE per ckpt
"""

import sys
import os
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORE = os.path.abspath(os.path.join(_HERE, "..", "..", "core"))
sys.path.insert(0, _CORE)
import clm_decode as cd

T = 24  # decode window (clm_decode.hexa)


# ════════════════════════════════════════════════════════════════════════
# trunk penultimate rep extraction — replicate clm_decode._fwd_logits up to yn
# ════════════════════════════════════════════════════════════════════════

def _penultimate(W, tok, T):
    """Return yn:[T,d] = CLMConvMoE trunk penultimate (post final-groupnorm,
    pre readout). 1:1 with clm_decode._fwd_logits, stopping before the readout
    conv/bind. This is the representation the readout reads = the trunk's
    compositional output."""
    d = W["d"]; E = W["E"]; K = W["K"]; L = W["L"]
    ids = tok.astype(np.int64)
    xe = W["embed"][ids]
    xt = cd._conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    DIL_CAP = 512
    dil = 1
    for li in range(L):
        dil_eff = dil if dil <= DIL_CAP else DIL_CAP
        h = cd._conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, dil_eff)
        hn = cd.nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1)
        hg = cd.nn_gelu_fwd(hn)
        xt = xt + hg.reshape(T, d)
        dil = dil * 2
    logits_r = cd._conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1)
    ex_out = np.empty((E, T, d), dtype=np.float64)
    for ej in range(E):
        eo = cd._conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1)
        ex_out[ej] = cd.nn_gelu_fwd(eo).reshape(T, d)
    y = cd.nn_moe_router_fwd(logits_r, ex_out, T, E, d)
    yn = cd.nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)
    return yn  # [T, d]


def _rep_of_concept(W, s):
    """r(concept) = penultimate rep at the LAST byte position of concept `s`,
    right-aligned in the T=24 window (pad-left byte 32), matching decode."""
    sb = s.encode("utf-8", "surrogateescape")
    slen = len(sb)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si = slen - T + p
        tok[p] = float(sb[si]) if si >= 0 else 32.0
    yn = _penultimate(W, tok, T)
    return yn[T - 1]  # [d] last-position rep


# ════════════════════════════════════════════════════════════════════════
# HE computation
# ════════════════════════════════════════════════════════════════════════

def _he(reps_A, reps_B, reps_AB, op):
    """HE = E||r(AoB) - (r(A) (+) r(B))|| / E||r(AoB)||. op in {'add','hada'}."""
    num = 0.0
    den = 0.0
    for ra, rb, rab in zip(reps_A, reps_B, reps_AB):
        comp = ra + rb if op == "add" else ra * rb
        num += np.linalg.norm(rab - comp)
        den += np.linalg.norm(rab)
    return num / den if den > 0 else float("nan")


def he_for_ckpt(path, pairs):
    """Compute HE_add, HE_hada + shuffled control for one .clm over concept
    pairs [(A,B), ...]. AoB = A+B (byte concat)."""
    W = cd.clm_load_weights(path)
    reps_A = [_rep_of_concept(W, a) for (a, b) in pairs]
    reps_B = [_rep_of_concept(W, b) for (a, b) in pairs]
    reps_AB = [_rep_of_concept(W, a + b) for (a, b) in pairs]

    he_add = _he(reps_A, reps_B, reps_AB, "add")
    he_hada = _he(reps_A, reps_B, reps_AB, "hada")

    # CONTROL: shuffle the AoB targets so r(AoB) is paired with the WRONG
    # (r(A),r(B)). If HE measures real composition, the shuffled HE should be
    # HIGHER/meaningless (composition no longer predicts the target).
    n = len(reps_AB)
    if n > 1:
        perm = np.roll(np.arange(n), 1)  # deterministic derangement for n>1
        reps_AB_sh = [reps_AB[perm[i]] for i in range(n)]
        he_add_sh = _he(reps_A, reps_B, reps_AB_sh, "add")
        he_hada_sh = _he(reps_A, reps_B, reps_AB_sh, "hada")
    else:
        he_add_sh = he_hada_sh = float("nan")

    return {
        "path": path,
        "n_pairs": n,
        "HE_add": he_add, "HE_hada": he_hada,
        "HE_add_shuffle": he_add_sh, "HE_hada_shuffle": he_hada_sh,
        "best_HE": min(he_add, he_hada),
    }


# ════════════════════════════════════════════════════════════════════════
# self-test — prove the metric SEPARATES structured (homomorphic) from random
# ════════════════════════════════════════════════════════════════════════

def self_test(seed=0, n=40, d=128):
    """Synthetic reps with KNOWN structure:
      * additive-homomorphic: r(AoB) = r(A)+r(B) exactly  -> HE_add ~ 0
      * hadamard-homomorphic: r(AoB) = r(A)*r(B) exactly  -> HE_hada ~ 0
      * random:               r(AoB) independent of A,B   -> HE high (~1.4)
    Proves HE is a real composition-preservation meter, not a constant."""
    rng = np.random.default_rng(seed)
    rA = [rng.standard_normal(d) for _ in range(n)]
    rB = [rng.standard_normal(d) for _ in range(n)]

    rAB_add = [a + b for a, b in zip(rA, rB)]
    rAB_hada = [a * b for a, b in zip(rA, rB)]
    rAB_rand = [rng.standard_normal(d) for _ in range(n)]

    out = {
        "add_homo__HE_add": _he(rA, rB, rAB_add, "add"),
        "add_homo__HE_hada": _he(rA, rB, rAB_add, "hada"),
        "hada_homo__HE_hada": _he(rA, rB, rAB_hada, "hada"),
        "hada_homo__HE_add": _he(rA, rB, rAB_hada, "add"),
        "random__HE_add": _he(rA, rB, rAB_rand, "add"),
        "random__HE_hada": _he(rA, rB, rAB_rand, "hada"),
    }
    # separation gate: homomorphic HE must be ~0 and << random HE
    out["SEPARATES"] = bool(
        out["add_homo__HE_add"] < 1e-9
        and out["hada_homo__HE_hada"] < 1e-9
        and out["random__HE_add"] > 0.5
        and out["random__HE_hada"] > 0.5
    )
    return out


# ════════════════════════════════════════════════════════════════════════
# concept pairs — short ko/en byte-spans (compositional A o B = A+B)
# ════════════════════════════════════════════════════════════════════════

PAIRS = [
    ("red", "ball"), ("blue", "sky"), ("big", "dog"), ("cold", "water"),
    ("fast", "car"), ("green", "tree"), ("dark", "room"), ("warm", "fire"),
    ("the cat", " sat"), ("a bird", " flew"), ("she ran", " home"),
    ("good", "morning"), ("black", "cat"), ("white", "snow"),
    ("hot", "sun"), ("old", "book"),
]


def main(argv):
    print("=" * 64)
    print("H_1821 Homomorphism-Error (HE) probe — numpy-only DIRECTIONAL (p7)")
    print("=" * 64)

    print("\n[1] SELF-TEST (synthetic structured vs random reps)")
    st = self_test()
    for k, v in st.items():
        if k == "SEPARATES":
            print("    SEPARATES gate:", "PASS" if v else "FAIL")
        else:
            print("    %-22s = %.6f" % (k, v))

    ckpts = argv[1:]
    if not ckpts:
        print("\n[2] no .clm args given — self-test only.")
        return 0

    print("\n[2] REAL .clm HE  (concept pairs n=%d, AoB=byte-concat)" % len(PAIRS))
    rows = []
    for ck in ckpts:
        if not cd.clm_decodable(ck):
            print("    SKIP (not v0.2-decodable):", ck)
            continue
        r = he_for_ckpt(ck, PAIRS)
        rows.append(r)
        name = os.path.basename(ck)
        print("    %-34s" % name)
        print("        HE_add  = %.4f   (shuffle ctrl = %.4f)"
              % (r["HE_add"], r["HE_add_shuffle"]))
        print("        HE_hada = %.4f   (shuffle ctrl = %.4f)"
              % (r["HE_hada"], r["HE_hada_shuffle"]))
        print("        best_HE = %.4f" % r["best_HE"])
        ca = r["HE_add_shuffle"] - r["HE_add"]
        ch = r["HE_hada_shuffle"] - r["HE_hada"]
        print("        control contrast (shuffle - true): add=%+.4f  hada=%+.4f"
              % (ca, ch))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
