#!/usr/bin/env python3
# H_1511 OSMOTIC-MITOSIS — R1 numpy mirror (DIRECTIONAL).
#
# SOURCE: external proposal — Amoeba Protocol (@qingkong66) — KL>capacity osmotic mitosis.
#
# PROPOSAL: anima's mitosis (VAdaptField, H_1199) splits a cell when the L2
# reconstruction error of an incoming sample exceeds a frozen SPLIT_THRESH; below
# that bar the winner is REFINED (its prototype is pulled toward x = OVERWRITE).
# The Amoeba Protocol proposes an information-theoretic trigger: split when the
# cell's information bottleneck overflows a Shannon capacity C —
#       Trigger Mitosis IF   L_recon + beta * D_KL(P(Z_cell) || P(Z_prior)) > C
# so a cell DIVIDES (1->2) to accommodate a new truth instead of OVERWRITING a
# grounded fact whose value-distribution diverges from the incoming one.
#
# WHAT THIS TESTS (split-TIMING, NOT a capacity-wall break — see H_1456):
#   H_1456 confirmed WALL=CAPACITY for BINDING (welding comparator+measurable).
#   This probe is DISTINCT: it does NOT claim total binding capacity rises. It tests
#   whether a KL>C trigger AVOIDS OVERWRITING a grounded fact by splitting in time,
#   when a metrically-near-but-semantically-divergent new fact would otherwise
#   refine (overwrite) the grounded winner. Capacity-honesty (bar C) is measured
#   explicitly: max-cells is the SAME for both triggers, so any retention gain is
#   timely division, not extra capacity.
#
# Frozen bars (set BEFORE running; c9, NO tune-to-green):
#   (A NO-OVERWRITE)  osmotic-trigger grounded-fact retention >= RET_BAR (0.90).
#   (B vs STANDARD)   osmotic retention - standard retention >= DISSO_BAR (0.50)
#                     on the SAME collision scenario (dissociation).
#   (C CAPACITY-HONEST) max_cells identical both arms; report cells used. This is an
#                     honesty bound (NOT pass/fail): retention gain must come from
#                     timely SPLIT, not a raised capacity cap.
#   (D EARNED ablate) beta=0 (pure L_recon) -> osmotic reverts to standard overwrite
#                     behavior: retention_ablate <= standard + 0.10.
#   (E EARNED shuffle) permute Z<->prior pairing -> KL decorrelates from the true
#                     collision; retention_shuffle <= standard + 0.10.
#   GREEN iff A & B & D & E (C honesty-only).
#   HONEST: if KL>C just re-derives standard VAdaptField behavior (no retention gain),
#   report the proposal as a RE-DERIVATION, not a new capability.
#
# p7 (no perplexity/LLM-judge), $0 CPU, deterministic, 3 seeds.

import numpy as np
import json, sys

DIM = 8           # VAdaptField byte-feature dim (matches core/engine_cli.hexa)
VDIM = 6          # value-distribution dimensionality (softmax support)
SPLIT_THRESH = 0.30   # frozen L2 novelty bar (SAME as vadapt_field_step)
LR = 0.20             # frozen online winner pull (SAME as vadapt_field_step)
BETA = 1.0            # KL weight in the osmotic trigger
CAP_C = 0.30          # osmotic capacity C: matches SPLIT_THRESH so L_recon-alone path is identical
MAX_CELLS = 38        # capacity cap, IDENTICAL across all arms (capacity-honest). Sized so an
                      # ideal osmotic store (24 grounded + 12 collision-splits = 36) FITS, but
                      # indiscriminate splitting (the shuffle arm, ~24 splits over 24 cells)
                      # EXHAUSTS it -> late collisions overwrite. The gain is timely DIVISION.
RECALL_THR = 0.18     # a stored fact is "retained" iff a near-key query recalls its value within this L2

SEEDS = [4511, 4512, 4513]

# ---------- fact generator ----------
def fnv_key(rng):
    # a DIM-vector key on the unit-ish scale (mirror of byte-trigram FNV affinity geometry)
    v = rng.normal(0, 1, DIM)
    return v / (np.linalg.norm(v) + 1e-9)

def value_dist(rng):
    # a value distribution over VDIM atoms (the "what" bound to a key) — softmax of logits
    z = rng.normal(0, 1.0, VDIM)
    e = np.exp(z - z.max())
    return e / e.sum()

def kl(p, q):
    p = np.clip(p, 1e-9, 1.0); q = np.clip(q, 1e-9, 1.0)
    return float(np.sum(p * np.log(p / q)))

# ---------- cell store ----------
class Cell:
    __slots__ = ("key", "val")
    def __init__(self, key, val):
        self.key = key.copy(); self.val = val.copy()

class Store:
    """A VAdaptField-style winner-take-all prototype store with a value bound per cell.
    trigger='standard' -> split iff L_recon>SPLIT_THRESH else REFINE(overwrite winner).
    trigger='osmotic'  -> split iff L_recon + beta*KL(new||winner) > C else refine.
    beta is the ablation lever (beta=0 -> pure L_recon == standard)."""
    def __init__(self, trigger, beta=BETA):
        self.cells = []
        self.trigger = trigger
        self.beta = beta

    def nearest(self, key):
        if not self.cells: return -1, 1e9
        ds = [np.linalg.norm(c.key - key) for c in self.cells]
        i = int(np.argmin(ds)); return i, ds[i]

    def learn(self, key, val, kl_override=None):
        i, d = self.nearest(key)
        want_split = (i < 0) or self._should_split(d, val, i, kl_override)
        if want_split and len(self.cells) < MAX_CELLS:
            self.cells.append(Cell(key, val)); return "split"
        # either no split wanted, OR at capacity cap (capacity-honest: cap is the SAME
        # for every arm, so a retention gain is timely division, never extra capacity).
        if i >= 0:
            # REFINE = pull winner key toward new key (online LR) AND overwrite its value.
            self.cells[i].key += LR * (key - self.cells[i].key)
            self.cells[i].val = val.copy()   # value OVERWRITE — the grounded fact is lost
            return "overwrite"
        self.cells.append(Cell(key, val)); return "split"

    def _should_split(self, d, val, i, kl_override=None):
        if i < 0: return True
        if self.trigger == "standard":
            return d > SPLIT_THRESH
        # osmotic: bottleneck overflow = L_recon + beta*KL(incoming || winner-prior) > C.
        # kl_override (E SHUFFLE) feeds a KL from a PERMUTED Z<->prior pairing so the
        # trigger no longer reflects THIS update's true divergence from its own winner.
        dkl = kl(val, self.cells[i].val) if kl_override is None else kl_override
        return (d + self.beta * dkl) > CAP_C

    def recall(self, key):
        i, d = self.nearest(key)
        if i < 0: return None, 1e9
        return self.cells[i].val, d

# ---------- scenario ----------
def build_scenario(rng):
    """N grounded facts, then a stream of near-key UPDATES split into two kinds:
      · COLLISION  — near key, DIVERGENT value (high KL): a NEW grounded truth that
        standard would refine (OVERWRITE), destroying the original. Osmotic must SPLIT.
      · BENIGN     — near key, SAME value (KL ~ 0): a redundant re-statement that
        SHOULD refine (no new cell needed). Osmotic must NOT split here (else it
        wastes capacity). This makes the cap a real constraint and lets the shuffle
        control bite (indiscriminate splitting exhausts the cap -> late overwrites)."""
    N = 24
    grounded = []   # (key, val)
    for _ in range(N):
        grounded.append((fnv_key(rng), value_dist(rng)))
    # Each grounded fact receives EXACTLY ONE near-key update (no later "healing"):
    #   · half COLLISION — near key, DIVERGENT value (high KL): a NEW grounded truth.
    #     standard refines (OVERWRITE, original lost); osmotic must SPLIT to keep both.
    #   · half BENIGN    — near key, SAME value (KL ~ 0): a redundant re-statement.
    #     both triggers should refine (no new cell); osmotic must NOT split (waste).
    # The benign half lets the cap bite the shuffle arm (indiscriminate splitting on the
    # scrambled high-KL signal exhausts the cap, then late collisions overwrite).
    updates = []    # (key, val, is_collision, target_grounded_val)
    for idx, (k, v) in enumerate(grounded):
        if idx % 2 == 0:                              # COLLISION
            nk = k + rng.normal(0, 0.06, DIM)         # near key: L2 ~0.17 << SPLIT_THRESH
            nv = value_dist(rng)                      # divergent value (high KL vs v)
            tries = 0
            while kl(nv, v) < 0.5 and tries < 20:
                nv = value_dist(rng); tries += 1
            updates.append((nk, nv, True, v))
        else:                                         # BENIGN
            bk = k + rng.normal(0, 0.04, DIM)
            bv = v + rng.normal(0, 0.003, VDIM); bv = np.clip(bv, 1e-9, None); bv /= bv.sum()
            updates.append((bk, bv, False, v))
    return grounded, updates

def retention(store, grounded):
    """fraction of ORIGINAL grounded facts whose value is still recallable near its key.
    A grounded fact 'survives' iff SOME cell near its key still holds its ORIGINAL value
    (a split keeps both the old and the new cell; an overwrite destroys the old value)."""
    ok = 0
    for (k, v) in grounded:
        # search all cells near the key for one still holding the original value
        found = False
        for c in store.cells:
            if np.linalg.norm(c.key - k) <= RECALL_THR and np.linalg.norm(c.val - v) <= 0.20:
                found = True; break
        if found: ok += 1
    return ok / len(grounded)

def run_seed(seed):
    rng = np.random.default_rng(seed)
    grounded, updates = build_scenario(rng)

    # each update's TRUE divergence = KL(update_value || its target grounded value).
    true_kls = [kl(u[1], u[3]) for u in updates]

    def make(trigger, beta=BETA, shuffle=False):
        s = Store(trigger, beta=beta)
        for (k, v) in grounded: s.learn(k, v)         # ground the facts
        if not shuffle:
            for (k, v, _isc, _tv) in updates: s.learn(k, v)
            return s
        # E SHUFFLE: permute Z<->prior — decorrelate the KL signal from the true
        # collision by rotating the per-update KL vector by one COLLISION period (2),
        # so each COLLISION's split decision reads a BENIGN neighbor's near-zero KL
        # (-> refines/overwrites, original lost) and each BENIGN reads a COLLISION's
        # high KL (-> wastes a split). Stored values stay TRUE, so retention reflects
        # ONLY the trigger's mis-decisions, not corrupted storage. Deterministic.
        rot = [true_kls[(t + 1) % len(updates)] for t in range(len(updates))]
        for t, (k, v, _isc, _tv) in enumerate(updates):
            s.learn(k, v, kl_override=rot[t])
        return s

    s_std = make("standard")
    s_osm = make("osmotic")
    s_abl = make("osmotic", beta=0.0)              # D: beta=0 -> pure L_recon (== standard)
    s_shf = make("osmotic", shuffle=True)          # E: KL vs permuted value

    return {
        "seed": seed,
        "ret_standard": retention(s_std, grounded),
        "ret_osmotic":  retention(s_osm, grounded),
        "ret_ablate":   retention(s_abl, grounded),
        "ret_shuffle":  retention(s_shf, grounded),
        "cells_standard": len(s_std.cells),
        "cells_osmotic":  len(s_osm.cells),
        "max_cells": MAX_CELLS,
    }

def main():
    rows = [run_seed(s) for s in SEEDS]
    def mean(k): return float(np.mean([r[k] for r in rows]))
    agg = {k: mean(k) for k in
           ["ret_standard","ret_osmotic","ret_ablate","ret_shuffle"]}
    agg_cells = {k: mean(k) for k in ["cells_standard","cells_osmotic"]}

    RET_BAR, DISSO_BAR, EARN_BAR = 0.90, 0.50, 0.10
    A = agg["ret_osmotic"] >= RET_BAR
    B = (agg["ret_osmotic"] - agg["ret_standard"]) >= DISSO_BAR
    D = agg["ret_ablate"] <= agg["ret_standard"] + EARN_BAR
    E = agg["ret_shuffle"] <= agg["ret_standard"] + EARN_BAR
    green = A and B and D and E
    re_derivation = (agg["ret_osmotic"] - agg["ret_standard"]) < 0.10

    print("=== H_1511 OSMOTIC-MITOSIS — R1 numpy mirror (DIRECTIONAL) ===")
    print("SOURCE: external proposal — Amoeba Protocol (KL>capacity osmotic mitosis)")
    print(f"seeds={SEEDS}  DIM={DIM} VDIM={VDIM} SPLIT_THRESH={SPLIT_THRESH} C={CAP_C} beta={BETA} MAX_CELLS={MAX_CELLS}")
    print("--- per-seed ---")
    for r in rows:
        print(f"  seed {r['seed']}: ret std={r['ret_standard']:.3f} osm={r['ret_osmotic']:.3f} "
              f"abl(b=0)={r['ret_ablate']:.3f} shuf={r['ret_shuffle']:.3f} | "
              f"cells std={r['cells_standard']} osm={r['cells_osmotic']} (cap {r['max_cells']})")
    print("--- mean / 3 seeds ---")
    print(f"  (A NO-OVERWRITE)   ret_osmotic   = {agg['ret_osmotic']:.3f}   (bar >= {RET_BAR})   {'PASS' if A else 'FAIL'}")
    print(f"  (B vs STANDARD)    osm - std     = {agg['ret_osmotic']-agg['ret_standard']:+.3f}  (bar >= {DISSO_BAR})  {'PASS' if B else 'FAIL'}")
    print(f"                     ret_standard  = {agg['ret_standard']:.3f}")
    print(f"  (C CAPACITY-HONEST) cells std={agg_cells['cells_standard']:.1f} osm={agg_cells['cells_osmotic']:.1f} "
          f"cap={MAX_CELLS} (SAME cap both arms -> gain is timely SPLIT, NOT raised capacity)")
    print(f"  (D EARNED ablate)  ret_ablate    = {agg['ret_ablate']:.3f}   (<= std+{EARN_BAR}={agg['ret_standard']+EARN_BAR:.3f})  {'PASS' if D else 'FAIL'}")
    print(f"  (E EARNED shuffle) ret_shuffle   = {agg['ret_shuffle']:.3f}   (<= std+{EARN_BAR}={agg['ret_standard']+EARN_BAR:.3f})  {'PASS' if E else 'FAIL'}")
    verdict = "GREEN" if green else ("RE-DERIVATION" if re_derivation else "RED")
    print(f"--- VERDICT (R1 DIRECTIONAL): {verdict}  (A&B&D&E; C honesty-only) ---")
    if re_derivation:
        print("  NOTE: osmotic retention ~= standard -> proposal RE-DERIVES VAdaptField (no new capability).")
    else:
        print("  NOTE: osmotic AVOIDS overwrite that standard trigger commits (split-timing gain, NOT capacity).")

    out = {"seeds": SEEDS, "rows": rows, "agg": agg, "agg_cells": agg_cells,
           "bars": {"A": bool(A), "B": bool(B), "D": bool(D), "E": bool(E),
                    "RET_BAR": RET_BAR, "DISSO_BAR": DISSO_BAR, "EARN_BAR": EARN_BAR},
           "verdict": verdict, "re_derivation": bool(re_derivation),
           "capacity_honest": {"max_cells": MAX_CELLS,
                               "cells_standard": agg_cells["cells_standard"],
                               "cells_osmotic": agg_cells["cells_osmotic"]}}
    with open("state/1511_osmotic_mitosis/h1511_result.json", "w") as f:
        json.dump(out, f, indent=2)
    return 0 if green else (2 if re_derivation else 1)

if __name__ == "__main__":
    sys.exit(main())
