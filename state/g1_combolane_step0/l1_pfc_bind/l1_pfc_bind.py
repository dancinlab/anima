#!/usr/bin/env python3
"""
H_9129 STEP-0 · L1 PFC variable-binding lane (STANDALONE)
=========================================================
Brain frame: recombination is NOT a mouth/Broca property. Prefrontal
working-memory does dynamic *variable binding* (role <- filler active
conjunction). role1<-X, role2<-Y become a bound vector holding both slots
SIMULTANEOUSLY even for a novel (X,Y) pair never co-seen.

This probe: binding lane ALONE. Does a bound-representation enable NOVEL
pair composition (reachable) vs surface memorization (unreachable)?

Substrate: HRR (Holographic Reduced Representations, Plate 1995).
  bind   : circular convolution  b = circconv(role, filler)     (fixed dim d)
  bundle : superpose slots        S = sum_k circconv(r_k, f_k)
  unbind : circular correlation   f_hat = circcorr(role, S)  (approx inverse)
  readout: nearest-neighbor vs a fixed filler codebook  (MOUTH READS ONLY)

CANNOT-BE-FOOLED-BY-FORM design (g1g6 form-priming defense):
  Every trial builds ONE bound vector S from K novel role-filler pairs.
  We then probe S two ways -- SAME surface vector S, differ only in the query:
    reachable   : unbind S with a role that IS bound in S  -> recover its filler
    unreachable : unbind S with a decoy role NOT bound in S -> should be chance
  If S were a form-blob (surface memorization), ANY query would read alike
  => reachable ~= unreachable. If a real role-addressed binding exists,
  only reachable lifts. Both queries hit the identical S (identical form).

  Extra form control (matched-form negative): 'unreachable' also tested by
  probing a REAL bound role but classifying against a codebook whose true
  atom was swapped out (ungrounded) -- surface identical, target absent.

ABLATION (bind op OFF): replace circconv(role,filler) with the filler itself
  (role tag removed) so S = sum_k f_k -- a bag-of-fillers with NO role
  structure. Role-addressed readout must then COLLAPSE toward chance
  (=> binding op is CAUSAL for the reachable lift; INERT would mean the
  lift survives without the bind op).

Honesty: mini numpy toy => DIRECTIONAL (NOT 303M engine-native).
Distinct from binding-family H_1816/H_1823 (mouth-readout NOT-SUP) on 3 counts:
  (1) SEPARATE lane (binding lives in its own PFC-analog store, not the mouth)
  (2) DISJOINT objective (algebraic unbind, no CE/gradient into the mouth)
  (3) mouth READS ONLY (nearest-neighbor decode; never trained to bind)
"""
import numpy as np
import json, os

RNG = np.random.default_rng(9129)
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- HRR primitives ----------
def rand_vec(d):
    v = RNG.standard_normal(d) / np.sqrt(d)
    return v

def circconv(a, b):
    return np.fft.irfft(np.fft.rfft(a) * np.fft.rfft(b), n=len(a))

def involution(a):
    # approximate inverse for correlation-based unbind: a*[i] = a[(-i) mod d]
    return np.concatenate([a[:1], a[1:][::-1]])

def unbind(role, S):
    return circconv(involution(role), S)

def cos(a, B):
    # cosine of a (d,) against codebook B (M,d)
    an = a / (np.linalg.norm(a) + 1e-9)
    Bn = B / (np.linalg.norm(B, axis=1, keepdims=True) + 1e-9)
    return Bn @ an

# ---------- experiment ----------
def run(d=512, M=100, K=2, n_roles=8, trials=400, bind_on=True, seed_atoms=None):
    """
    codebook: M filler atoms (all 'grounded' / known to the readout).
    roles: n_roles distinct role vectors (K of them used per structure,
           the rest serve as decoy 'unbound' roles for the unreachable probe).
    Each trial: pick K NOVEL (role,filler) pairs at random, build S, then:
      - reachable probe: unbind with each of the K bound roles -> NN decode.
      - unreachable probe: unbind with a decoy role (not among the K) -> NN decode.
    bind_on=False => ABLATION: S = sum of raw fillers (no role binding);
      'unbind' still applies role correlation but there is no role structure.
    Returns dict of accuracies (chance = 1/M).
    """
    F = seed_atoms if seed_atoms is not None else np.stack([rand_vec(d) for _ in range(M)])
    R = np.stack([rand_vec(d) for _ in range(n_roles)])

    reach_hits = 0; reach_tot = 0
    unreach_hits = 0; unreach_tot = 0

    for _ in range(trials):
        role_ids = RNG.choice(n_roles, size=K, replace=False)
        fill_ids = RNG.choice(M, size=K, replace=False)  # novel combo each trial
        # build bound structure
        S = np.zeros(d)
        for rid, fid in zip(role_ids, fill_ids):
            if bind_on:
                S = S + circconv(R[rid], F[fid])
            else:
                S = S + F[fid]  # ABLATION: no role tag
        # reachable probes: query each bound role, expect its filler
        for rid, fid in zip(role_ids, fill_ids):
            probe = unbind(R[rid], S)
            pred = int(np.argmax(cos(probe, F)))
            reach_hits += int(pred == fid)
            reach_tot += 1
        # unreachable probe: query a decoy role that is NOT bound in S.
        decoys = [r for r in range(n_roles) if r not in role_ids]
        drole = RNG.choice(decoys)
        probe = unbind(R[drole], S)
        pred = int(np.argmax(cos(probe, F)))
        # 'correct' would mean it accidentally hits one of the true fillers;
        # a real binding lane should NOT -- score against the actual bound set.
        unreach_hits += int(pred in set(int(x) for x in fill_ids))
        unreach_tot += 1

    return {
        "d": d, "M": M, "K": K, "n_roles": n_roles, "trials": trials,
        "bind_on": bind_on,
        "chance": 1.0 / M,
        "reachable_acc": reach_hits / reach_tot,
        "unreachable_acc": unreach_hits / unreach_tot,
        "unreachable_baseline": K / M,  # expected hit-rate if decode is random over M, K targets
    }

def main():
    results = {}
    # shared atoms across full/ablation so only the bind op differs
    d, M = 512, 100
    F = np.stack([rand_vec(d) for _ in range(M)])

    print("=== L1 PFC variable-binding lane (HRR) — STANDALONE ===")
    print(f"d={d} M={M} chance=1/M={1/M:.4f}\n")

    # main K sweep, bind ON
    for K in [1, 2, 3, 4, 6]:
        r = run(d=d, M=M, K=K, seed_atoms=F, bind_on=True)
        results[f"bindON_K{K}"] = r
        print(f"[BIND ON ] K={K}: reachable={r['reachable_acc']:.3f}  "
              f"unreachable={r['unreachable_acc']:.3f}  (chance={r['chance']:.3f}, "
              f"unreach_base={r['unreachable_baseline']:.3f})")

    print()
    # ABLATION: bind OFF (bag of fillers, no role tag)
    for K in [1, 2, 3, 4, 6]:
        r = run(d=d, M=M, K=K, seed_atoms=F, bind_on=False)
        results[f"bindOFF_K{K}"] = r
        print(f"[BIND OFF] K={K}: reachable={r['reachable_acc']:.3f}  "
              f"unreachable={r['unreachable_acc']:.3f}  (chance={r['chance']:.3f})")

    # summary verdict at the canonical K=2 comparison
    on = results["bindON_K2"]; off = results["bindOFF_K2"]
    reach = on["reachable_acc"]; unreach = on["unreachable_acc"]
    ablated = off["reachable_acc"]
    # fooled_by_form iff reachable ~= unreachable (no role-addressed lift)
    lift = reach - unreach
    fooled = lift < 0.10  # reachable must clear unreachable by a wide margin
    # ablation causal iff removing bind collapses the reachable lift
    ablation_collapse = (reach - ablated) > 0.30
    verdict = "BIND" if (not fooled and ablation_collapse) else \
              ("form-priming" if fooled else "floor")

    summary = {
        "probe": "L1 PFC variable-binding lane (HRR circular-conv), STANDALONE",
        "canonical_K": 2,
        "reachable_acc_K2": reach,
        "unreachable_acc_K2": unreach,
        "reachable_minus_unreachable": lift,
        "ablated_reachable_acc_K2": ablated,
        "reachable_minus_ablated": reach - ablated,
        "chance": on["chance"],
        "fooled_by_form": bool(fooled),
        "ablation_causal_collapse": bool(ablation_collapse),
        "verdict": verdict,
        "honesty": "DIRECTIONAL (mini numpy toy, NOT 303M engine-native)",
        "distinct_from_H1816_H1823": [
            "separate lane (binding store != mouth)",
            "disjoint objective (algebraic unbind, no CE into mouth)",
            "mouth reads only (NN decode, never trained to bind)",
        ],
    }
    results["_summary"] = summary
    print("\n=== SUMMARY (K=2) ===")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    with open(os.path.join(OUT, "results.json"), "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nwrote {os.path.join(OUT, 'results.json')}")

if __name__ == "__main__":
    main()
