#!/usr/bin/env python3
"""
H_9129 rung-2 — integrated PFC-BG-hippo lane on REAL 303M engine representations.

Faithful port of the STEP-0 pipeline (state/g1_combolane_step0/integrated/
combolane.py) — HRR bind(PFC role↔filler) → gate(BG Go/NoGo over decoys) →
pattern-completion(hippocampal cleanup) → mouth READOUT — with ONE change that
IS the escalation: the atomic FILLER symbols (color/material/size) are no longer
ideal random hypervectors but REAL h1129 303M engine residual representations
(extract_reps.py, exact core/decode ops). Roles/decoys R1,R2,D1,D2 stay random
unit vectors (they are the lane's OWN binding keys, not concepts).

DECISIVE CONTROL: an apples-to-apples `rand1024` codebook (fresh random unit
vectors at the SAME engine dim d=1024, same N, same topology) runs alongside the
real-303M codebooks. If real-303M reach collapses toward unreachable while
rand1024 does not, the STEP-0 result was a clean-vector artifact (→ WALL). If
real-303M reach still >> unreachable AND shuffle + lane-OFF collapse, the
mechanism survives real engine representations (→ supportive DIRECTIONAL).

FROZEN BAR (pre-registered — inherited from STEP-0 combolane.py, VERBATIM, no
tune-to-green): fooled_by_form iff |gap| < 0.10 ; ablation CAUSAL iff reach-drop
> 0.15 ; shuffle-collapse iff shuffled-reach drops > 0.15 toward chance.
Rep-form / centering are pre-registered (extract_reps.py docstring) BEFORE any
lane run. Primary engine codebook = real_mean_c (mean-pool, centered+unit-norm).

HONEST SCOPE: representations are engine-native (real 303M forward), but the lane
is NOT wired into core/ and this is NOT the `anima evaluate --py` decode-scoring
path → overall tier = DIRECTIONAL (a_engine_native_learning). This rung tests
whether the mini/toy mechanism holds on real engine reps.
"""
import os, sys, json
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
D = 1024                       # engine dim (h1129 d) — FIXED, not a knob
N = 24                         # symbols per pool
SEEDS = list(range(12))

# ── HRR ops (identical to STEP-0 combolane.py) ──────────────────────────────
def bind(a, b):
    return np.fft.irfft(np.fft.rfft(a) * np.fft.rfft(b), n=D)

def inv(a):
    return np.concatenate([a[:1], a[1:][::-1]])

def unbind(mem, key):
    return bind(mem, inv(key))

def cleanup(v, codebook):
    sims = codebook @ (v / (np.linalg.norm(v) + 1e-9))
    idx = int(np.argmax(sims))
    return idx, float(sims[idx]), codebook[idx]

def _unit(x):
    return x / (np.linalg.norm(x) + 1e-9)

def _rand_unit(rng, n):
    v = rng.standard_normal((n, D)); v /= np.linalg.norm(v, axis=1, keepdims=True)
    return v


# ── codebook builders (the ONLY thing that changes the atomic symbols) ──────
def _center_norm(V):
    Vc = V - V.mean(axis=0, keepdims=True)
    return Vc / (np.linalg.norm(Vc, axis=1, keepdims=True) + 1e-9)

def _norm_only(V):
    return V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)

def load_codebooks():
    z = np.load(os.path.join(_HERE, "reps_h1129.npz"))
    cb = {}
    # real 303M — centered+unit (PRIMARY) and raw-unit (honest collinear control)
    cb["real_mean_c"]  = {p: _center_norm(z["%s_mean" % p]) for p in "ABC"}
    cb["real_last_c"]  = {p: _center_norm(z["%s_last" % p]) for p in "ABC"}
    cb["real_mean_raw"]= {p: _norm_only(z["%s_mean" % p])   for p in "ABC"}
    return cb


def run_seed(seed, cb_kind, codebooks, shuffle=False):
    """One seed. Fillers come from `codebooks[cb_kind]` (real reps) or, for
    'rand1024', fresh random unit vectors keyed by seed. Relation topology is a
    per-seed permutation graph; shuffle=True DERANGES that topology (surface
    forms + capacity preserved — only the relational wiring is destroyed)."""
    rng = np.random.default_rng(seed)
    if cb_kind == "rand1024":
        COLOR = _rand_unit(rng, N); MAT = _rand_unit(rng, N); SIZE = _rand_unit(rng, N)
    else:
        COLOR = codebooks[cb_kind]["A"]; MAT = codebooks[cb_kind]["B"]; SIZE = codebooks[cb_kind]["C"]
    R1, R2, D1, D2 = _rand_unit(rng, 4)

    a  = rng.permutation(N)[:N] % N          # color -R1-> mat  (TRUE)
    ad = rng.permutation(N)[:N] % N          # color -D1-> mat (decoy)
    connected_mat = set(rng.permutation(N)[:N // 2].tolist())
    b  = rng.permutation(N)[:N] % N          # mat -R2-> size   (TRUE)
    bd = rng.permutation(N)[:N] % N          # mat -D2-> size (decoy)

    # gold + reachable partition are ALWAYS from the TRUE graph (fixed).
    reach_colors   = [i for i in range(N) if a[i] in connected_mat]
    unreach_colors = [i for i in range(N) if a[i] not in connected_mat]

    def gold_size(i):
        return b[a[i]]                        # TRUE 2-hop composition

    # SHUFFLE ablation: derange the STORED onward (material->size) edges relative
    # to the TRUE gold — surface forms (same symbols), edge counts, connectivity
    # partition and capacity all preserved; ONLY the relational wiring that a real
    # 2-hop chain must follow is destroyed. Store b_store; gold stays TRUE b.
    b_store = b
    if shuffle:
        der = rng.permutation(N)
        while np.any(der == np.arange(N)):   # strict derangement (no fixed point)
            der = rng.permutation(N)
        b_store = b[der]

    M = np.zeros(D)
    for i in range(N):
        M += bind(bind(COLOR[i], R1), MAT[a[i]])
        M += bind(bind(COLOR[i], D1), MAT[ad[i]])
    for m in range(N):
        if m in connected_mat:
            M += bind(bind(MAT[m], R2), SIZE[b_store[m]])
        M += bind(bind(MAT[m], D2), SIZE[bd[m]])
    M = _unit(M)

    def pipeline(i, use_bind=True, use_gate=True, use_completion=True):
        c = COLOR[i]
        if not use_bind:
            key1 = c
        elif not use_gate:
            role1 = _unit(R1 + D1 + R2 + D2); key1 = bind(c, role1)
        else:
            key1 = bind(c, R1)
        raw_mat = unbind(M, key1)
        if use_completion:
            _, _, mat_vec = cleanup(raw_mat, MAT)
        else:
            mat_vec = raw_mat
        if not use_bind:
            key2 = mat_vec
        elif not use_gate:
            role2 = _unit(R1 + D1 + R2 + D2); key2 = bind(mat_vec, role2)
        else:
            key2 = bind(mat_vec, R2)
        raw_size = unbind(M, key2)
        s_idx, _, _ = cleanup(raw_size, SIZE)
        return s_idx

    def acc(colors, **kw):
        if not colors:
            return float("nan")
        hit = sum(1 for i in colors if pipeline(i, **kw) == gold_size(i))
        return hit / len(colors)

    return {
        "n_reach": len(reach_colors), "n_unreach": len(unreach_colors),
        "full_reach": acc(reach_colors), "full_unreach": acc(unreach_colors),
        "bindoff_reach": acc(reach_colors, use_bind=False),
        "gateoff_reach": acc(reach_colors, use_gate=False),
        "compoff_reach": acc(reach_colors, use_completion=False),
    }


def eval_codebook(cb_kind, codebooks):
    rows  = [run_seed(s, cb_kind, codebooks, shuffle=False) for s in SEEDS]
    srows = [run_seed(s, cb_kind, codebooks, shuffle=True)  for s in SEEDS]
    keys = ["full_reach", "full_unreach", "bindoff_reach", "gateoff_reach", "compoff_reach"]
    agg  = {k: float(np.nanmean([r[k] for r in rows]))  for k in keys}
    sagg = {k: float(np.nanmean([r[k] for r in srows])) for k in keys}
    r_full, u_full = agg["full_reach"], agg["full_unreach"]
    gap = r_full - u_full
    chance = 1.0 / N
    def collapse(part):
        drop = r_full - agg["%s_reach" % part]
        return {"reach": agg["%s_reach" % part], "drop": drop,
                "verdict": "CAUSAL" if drop > 0.15 else "INERT"}
    shuffle_drop = r_full - sagg["full_reach"]
    return {
        "codebook": cb_kind, "chance": chance,
        "full_reach": r_full, "full_unreach": u_full,
        "gap_reach_minus_unreach": gap,
        "fooled_by_form": bool(abs(gap) < 0.10),
        "ablation": {p: collapse(p) for p in ("bindoff", "gateoff", "compoff")},
        "shuffle_reach": sagg["full_reach"], "shuffle_drop": shuffle_drop,
        "shuffle_collapsed": bool(shuffle_drop > 0.15),
    }


def main():
    codebooks = load_codebooks()
    order = ["rand1024", "real_mean_c", "real_last_c", "real_mean_raw"]
    results = {k: eval_codebook(k, codebooks) for k in order}
    diag = json.load(open(os.path.join(_HERE, "reps_diag.json")))
    out = {"D": D, "N": N, "seeds": len(SEEDS), "arm": "A_synthetic_topology",
           "rep_diag": diag, "results": results}
    with open(os.path.join(_HERE, "result_armA.json"), "w") as f:
        json.dump(out, f, indent=2)

    print("=== H_9129 rung-2 integrated lane — ARM A (synthetic topology) ===")
    print("D=%d N=%d seeds=%d chance=%.3f  (roles=random keys · fillers=codebook)\n"
          % (D, N, len(SEEDS), 1.0 / N))
    hdr = "%-14s reach  unreach  gap    fooled  shuf   shufΔ  | bindΔ gateΔ compΔ"
    print(hdr % "codebook")
    print("-" * 86)
    for k in order:
        r = results[k]; ab = r["ablation"]
        print("%-14s %.3f  %.3f   %+.3f  %-5s  %.3f  %.3f  | %.2f  %.2f  %.2f"
              % (k, r["full_reach"], r["full_unreach"], r["gap_reach_minus_unreach"],
                 str(r["fooled_by_form"]), r["shuffle_reach"], r["shuffle_drop"],
                 ab["bindoff"]["drop"], ab["gateoff"]["drop"], ab["compoff"]["drop"]))
    print("\nfrozen bar: BIND-survives iff gap>0.10 (not fooled) ∧ shuffleΔ>0.15 ∧ all 3 ablationΔ>0.15")


if __name__ == "__main__":
    main()
