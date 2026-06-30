#!/usr/bin/env python3
"""h1557_oi_probe_scaffold.py — OI-subspace / Binding-ID read-out probe (G6 lens 9, Family-1).

ROUND STATUS: DESIGN-ROUND SCAFFOLD (DIRECTIONAL). This file fixes the FROZEN geometry/bar logic so the
R2 engine-native round only has to (1) add the core/ hidden-dump ops and (2) feed engine-dumped activations
in. The scaffold does NOT touch torch/numpy 303M weights this round (no heavy decode — per the task).

ENGINE-NATIVE GATE (a_engine_native_learning): the activation dump (Z_E, Z_A) and the patched forward MUST
come from live core/bytegpt_decode.hexa via the proposed ops bytegpt_dump_hidden / bytegpt_forward_patched
(see DESIGN.md s4). The PCA/cosine/flip math below is plain arithmetic over those dumped vectors (torch-free,
same posture as g6_common scoring over engine fragments in H_1464) -> verdict is engine-native once wired.

Two entry points:
  - build_stimuli()   : construct the controlled multi-bind prompts from the FROZEN h1305 vocab.
  - score(deltaE, deltaA, oi_flip, shuf_cos, shuf_flip, rand_flip, pos_flip) : apply the FROZEN 5-bar.

The R2 driver will: dump Z_E/Z_A from the engine -> compute deltaE/deltaA (mean-diff) -> PCA + cosine ->
run OI / shuffle / random / position patches via bytegpt_forward_patched -> call score().
"""
import os, sys, math, json

HERE = os.path.dirname(os.path.abspath(__file__))

# ── FROZEN thresholds (mirror H_1557_FREEZE.txt; do NOT edit post-measurement, c9) ──
B1_PCA_VAR   = 0.60   # top-2 PCA variance ratio of {deltaE(k), deltaA(k)}  -> OI axis is low-rank
B2_LEG_COS   = 0.30   # mean cosine(deltaE(k), deltaA(k))  -> legs co-axial (the weld)
B3_FLIP      = 0.50   # OI-patch bind-flip rate            -> binding is causally transplantable (DECISIVE)
B4_SHUF_COS  = 0.10   # shuffled-label cosine ceiling      -> axis collapses under label shuffle
B4_SHUF_FLIP = 0.15   # shuffled-label patch-flip ceiling
B5_RAND_FLIP = 0.15   # random-direction patch-flip ceiling
B5_MARGIN    = 0.35   # OI-flip minus random-flip
POS_FLIP_MAX = 0.15   # position control (non-gating diagnostic)


def _cos(a, b):
    na = math.sqrt(sum(x * x for x in a)) or 1e-12
    nb = math.sqrt(sum(x * x for x in b)) or 1e-12
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def _load_vocab():
    """Load the FROZEN h1305 COMPARATOR/MEASURABLE families if G6_PROBES is set, else a stub."""
    probes = os.environ.get("G6_PROBES")
    if not probes:
        print("[scaffold] G6_PROBES unset -> stub vocab (R2 must use the real h1305 vocab).")
        return (["greater", "smaller", "whenever", "increases", "decreases"],
                ["sample", "load", "amount", "rate", "signal"])
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "h1305", os.path.join(probes, "h1305_g6_ideation_falsifiability.py"))
    h5 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h5)
    return sorted(h5.COMPARATOR), sorted(h5.MEASURABLE)


def build_stimuli():
    """Construct controlled K-bind prompts from the FROZEN h1305 COMPARATOR/MEASURABLE families.

    Returns a list of dicts: {prompt, K, binds:[(entity_str, comparator, measurable, k)], query_k}.
    Entity strings are neutral subjects; the bind k is the (comparator,measurable) pairing we control.
    The R2 driver tokenizes each prompt to bytes (vocab=256) and records the byte spans of each entity
    window + attribute window so the engine dump can read x[t,:] at the right positions.
    """
    COMPARATOR, MEASURABLE = _load_vocab()
    ENTITIES = ["the river", "the engine", "the field", "the signal"]
    stimuli = []
    K = 2
    # minimal controlled set; R2 expands to N>=200 prompts/cell with bind permutations
    for ci, comp in enumerate(COMPARATOR[:3]):
        for mi in range(min(3, len(MEASURABLE))):
            binds = [(ENTITIES[0], comp, MEASURABLE[mi], 0),
                     (ENTITIES[1], COMPARATOR[(ci + 1) % len(COMPARATOR)],
                      MEASURABLE[(mi + 1) % len(MEASURABLE)], 1)]
            prompt = (f"{binds[0][0]} is {binds[0][1]} whenever {binds[0][2]} grows. "
                      f"{binds[1][0]} is {binds[1][1]} whenever {binds[1][2]} drops. "
                      f"query: {binds[0][0]} is")
            stimuli.append({"prompt": prompt, "K": K, "binds": binds, "query_k": 0})
    return stimuli


def score(pca_var_ratio, leg_cos, oi_flip, shuf_cos, shuf_flip, rand_flip, pos_flip):
    """Apply the FROZEN 5-bar. All inputs are scalars computed from ENGINE-dumped activations (R2)."""
    b1 = pca_var_ratio >= B1_PCA_VAR
    b2 = leg_cos >= B2_LEG_COS
    b3 = oi_flip >= B3_FLIP
    b4 = (shuf_cos < B4_SHUF_COS) and (shuf_flip < B4_SHUF_FLIP)
    b5 = (rand_flip < B5_RAND_FLIP) and ((oi_flip - rand_flip) >= B5_MARGIN)
    pos_clean = pos_flip < POS_FLIP_MAX

    invalid = (not b4) or (not pos_clean)
    if invalid:
        tier = ("INVALID (re-measure, NOT a tier) — shuffle survived or position-confounded; "
                "fix frozen-first (c9)")
        verdict = "INVALID"
    elif b1 and b2 and b3 and b4 and b5:
        tier = ("GREEN READOUT / LEARN-GAP — OI binding axis EXISTS, leg-shared, causally transplantable "
                "=> 303M CAN represent the weld; behavioural walls measured read-out. wall RE-CLASSIFIED.")
        verdict = "GREEN_READOUT"
    else:
        fails = [n for n, ok in [("B1", b1), ("B2", b2), ("B3", b3), ("B5", b5)] if not ok]
        tier = (f"WALL=CAPACITY (9th converging lens) — bars {fails} fail; no transplantable binding "
                "direction in the residual stream => geometry CONFIRMS the behavioural CAPACITY ceiling.")
        verdict = "WALL_CAPACITY"

    out = {"B1_pca": [pca_var_ratio, b1], "B2_cos": [leg_cos, b2], "B3_oi_flip": [oi_flip, b3],
           "B4_shuffle": [[shuf_cos, shuf_flip], b4], "B5_random": [rand_flip, b5],
           "pos_control": [pos_flip, pos_clean], "verdict": verdict, "tier": tier}
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    print("H_1557 OI-subspace probe SCAFFOLD (design round — DIRECTIONAL).")
    print("Engine-native R2 prerequisite: core/ bytegpt_dump_hidden + bytegpt_forward_patched (DESIGN.md s4).")
    stim = build_stimuli()
    print(f"built {len(stim)} controlled multi-bind stimuli (K=2). example:")
    print("  " + stim[0]["prompt"])
    print("\nFROZEN bars:", {"B1": B1_PCA_VAR, "B2": B2_LEG_COS, "B3": B3_FLIP,
                              "B4_cos": B4_SHUF_COS, "B4_flip": B4_SHUF_FLIP, "B5_rand": B5_RAND_FLIP})
    print("\nscore() is wired and FROZEN; R2 feeds it engine-dumped geometry. No 303M weights touched this round.")
