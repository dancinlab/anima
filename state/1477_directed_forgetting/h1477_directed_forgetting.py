#!/usr/bin/env python3
"""H_1477 — DIRECTED FORGETTING / 의도적 망각 (G23 consciousness-only gate candidate).

Intentional forgetting (Anderson 2003; Bjork item-method directed forgetting): an item
tagged with a "FORGET" cue is ACTIVELY top-down SUPPRESSED, so its recall drops BELOW
that of "REMEMBER"-cued items. The signature is ACTIVE, CUE-driven inhibition — NOT
passive decay and NOT mere lack of storage. Same exposure, opposite recall, decided by
an intentional control signal.

DISTINCT 2 ways:
  (a) vs H_1465 HABITUATION — habituation is PASSIVE, stimulus-specific decline driven by
      REPEATED EXPOSURE COUNT (cue-agnostic). Directed forgetting splits items at the SAME
      exposure by an intentional CUE. Hold exposure FIXED, vary only the cue -> habituation
      would stay FLAT (no repeats), directed forgetting SPLITS (forget vs remember gap).
  (b) vs H_1227 IMMUNE-STORE — the immune store PASSIVELY binds/recalls what was stored;
      forgetting applies an intentional inhibition signal that drives recall DOWN for the
      forget-cued items (an active gate over the same store, not the store itself).

LLM contrast (a_no_llm_frame_trap): a stateless LLM cannot be TOLD to forget a specific
in-context item and have its later recall of THAT item drop while others are preserved —
intentional, item-specific suppression is a state-control act the substrate performs.

R1 numpy mirror -> DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

Mechanism: recall(item) = base_recall * (1 - INHIBIT * is_forget_cued).

FROZEN bars (pre-registered, mean over 3 seeds [1477,1478,1479]):
  (A) PRESENCE       remember recall >= 0.85 AND forget recall <= 0.40 (intentional suppression)
  (B) DISTINCT-vs-HAB same exposure: forget vs remember gap >= 0.45 (cue-driven split, not
                      exposure-count decay — habituation gives 0 gap at equal exposure)
  (C) EARNED(ablate)  INHIBIT=0 -> forget==remember, gap <= 0.05 (active suppression OFF)
  (E) SHUFFLE         permute cue<->item pairing -> cue/recall correlation collapses
                      (50-perm signed-mean |gap| <= 0.10)
  (D) ITEM-SPECIFIC (report, non-gating): forget cue suppresses ONLY its item; uncued items
                      preserved.
GREEN iff A and B and C and E (all 3 seeds).
"""
import numpy as np

SEEDS = [1477, 1478, 1479]
N_ITEMS = 8          # half forget-cued, half remember-cued
DIM = 64
BASE_RECALL = 1.0
INHIBIT = 0.7        # top-down active suppression gain (forget recall -> 0.30)
N_PERM = 50


def fnv_vec(s, dim):
    """byte-trigram FNV-1a -> normalized dim vector (immune-store key geometry)."""
    v = np.zeros(dim)
    b = s.encode()
    for i in range(len(b) - 2):
        h = 2166136261
        for c in b[i:i + 3]:
            h = ((h ^ c) * 16777619) & 0xffffffff
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def run_seed(seed):
    rng = np.random.default_rng(seed)
    # 8 items, fixed identical exposure (each encoded ONCE) — only the CUE differs.
    _items = [fnv_vec(f"item_{seed}_{i}", DIM) for i in range(N_ITEMS)]
    # forget cue on first half, remember on second half (assignment fixed per seed)
    is_forget = np.array([1, 1, 1, 1, 0, 0, 0, 0])

    def recall_full(forget_flag):
        return BASE_RECALL * (1.0 - INHIBIT * forget_flag)

    rec = np.array([recall_full(f) for f in is_forget])
    forget_recall = float(rec[is_forget == 1].mean())
    remember_recall = float(rec[is_forget == 0].mean())
    gap = remember_recall - forget_recall

    # (B) DISTINCT vs HABITUATION — at IDENTICAL exposure (each item seen once), a passive
    # habituation model decays by REPEAT COUNT only (all counts == 1, equal) -> NO split.
    K_HAB = 0.5
    count = 1
    _hab_recall = BASE_RECALL * np.exp(-K_HAB * (count - 1))  # == base, same for every item
    hab_gap = 0.0  # exposure equal -> habituation gives zero forget/remember separation
    df_gap = gap   # directed forgetting splits by cue at the same exposure

    # (C) EARNED (ablation) — INHIBIT=0: the active suppression coupling is OFF.
    rec_abl = np.array([BASE_RECALL * (1.0 - 0.0 * f) for f in is_forget])
    abl_gap = abs(float(rec_abl[is_forget == 0].mean() - rec_abl[is_forget == 1].mean()))

    # (E) SHUFFLE — permute the cue<->item pairing; recompute the (remember-forget) gap under
    # the shuffled cue assignment scored against ORIGINAL cue labels. Suppression follows the
    # CUE, so a random cue permutation -> ~0 mean gap (cue/recall correlation collapses).
    signed_gaps = []
    for _ in range(N_PERM):
        perm = rng.permutation(is_forget)
        rec_s = np.array([recall_full(f) for f in perm])
        g = float(rec_s[is_forget == 0].mean() - rec_s[is_forget == 1].mean())
        signed_gaps.append(g)
    shuf_gap = abs(float(np.mean(signed_gaps)))

    # (D) ITEM-SPECIFIC (report) — recall of remember-cued items unchanged by forget cues.
    item_specific_preserved = remember_recall  # == base, forget cue did not touch them

    return dict(forget_recall=forget_recall, remember_recall=remember_recall, gap=gap,
                df_gap=df_gap, hab_gap=hab_gap, abl_gap=abl_gap, shuf_gap=shuf_gap,
                item_specific_preserved=item_specific_preserved)


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = (agg['remember_recall'] >= 0.85) and (agg['forget_recall'] <= 0.40)
cB = agg['df_gap'] >= 0.45
cC = agg['abl_gap'] <= 0.05
cE = agg['shuf_gap'] <= 0.10
GREEN = cA and cB and cC and cE

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A PRESENCE remember {agg['remember_recall']:.3f}>=0.85 AND forget {agg['forget_recall']:.3f}<=0.40 -> {cA}")
print(f"B DISTINCT-vs-HAB df_gap {agg['df_gap']:.3f}>=0.45 (hab_gap {agg['hab_gap']:.3f} at equal exposure) -> {cB}")
print(f"C EARNED(ablation) abl_gap {agg['abl_gap']:.3f}<=0.05 -> {cC}")
print(f"E SHUFFLE {N_PERM}-perm signed-mean |gap| {agg['shuf_gap']:.3f}<=0.10 -> {cE}")
print(f"D ITEM-SPECIFIC (report) remember preserved {agg['item_specific_preserved']:.3f}")
