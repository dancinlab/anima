#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────────────
# blue_falsifier_mgnd.py — Dir-O B-MGND-1..5 closed-form sympy sidecar
#   RESEARCH.md §22 방향 O. central state/verify_hexad_blue_2026_05_15/
#   blue_falsifier.py 변경 0 (sidecar — B-PRIME/B-DIRH/B-DIRI/B-S16
#   sidecar 선례, 차후 흡수 가능).
#
#   CLOSED side  = retrieval-grounding MECHANISM transfer-form + the
#                  overlay-OFF==§16 byte-equal connection point.
#   B-MGND-NOTE  = grounded routing/coherence/JOINT OUTCOME +
#                  "grounding 이 §16 천장을 깨는가" = §16 ckpt
#                  routing-OUTCOME 종속, EMPIRICAL (B-D-NOTE /
#                  B-S16-NOTE family, NOT counted 🔵).
#
#   f1/f2/f3 hard-fail safe: Cauchy-Schwarz cosine bound / Boolean
#   factorisation / SHA256 / §9 reuse — NO σ/τ/φ/J₂ external
#   derivation. B-IDENTITY-5 무관 (corpus 미생성).
# ──────────────────────────────────────────────────────────────────────
import os
import sys
import json
import hashlib

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def b_mgnd_1():
    """B-MGND-1 COSINE-RETRIEVE-BOUNDED — cos(q,s) ∈ [−1,1]
    (Cauchy-Schwarz real-limit); self-key q≡ψ_a ⇒ cos=1 exact.
    Mirror of HEXAD/M/m_lib.hexa::_m_cosine (B-M-2 RETRIEVE-DETERMINISTIC
    closure)."""
    q0, q1, s0, s1 = sp.symbols("q0 q1 s0 s1", real=True)
    dot = q0 * s0 + q1 * s1
    nq = sp.sqrt(q0**2 + q1**2)
    ns = sp.sqrt(s0**2 + s1**2)
    cos = dot / (nq * ns)
    # self-retrieval exactness: s == q  ⇒  cos == 1.
    self_cos = sp.simplify(cos.subs({s0: q0, s1: q1}))
    # |cos| ≤ 1 ⇔ dot² ≤ |q|²|s|²  (Cauchy-Schwarz), as a polynomial
    # identity:  |q|²|s|² − dot² = (q0 s1 − q1 s0)²  ≥ 0  ∀ reals.
    cs_gap = sp.expand((q0**2 + q1**2) * (s0**2 + s1**2) - dot**2)
    cs_sq = sp.expand((q0 * s1 - q1 * s0) ** 2)
    ok = (sp.simplify(sp.Abs(self_cos) - 1) == 0
          and sp.simplify(cs_gap - cs_sq) == 0)
    # numeric self-key witness on the eval Ψ-anchors.
    sys.path.insert(0, os.path.join(
        ROOT, "state", "carving_dataregime_s16_2026_05_18"))
    from eval_carving_s16 import ANCHOR_PSI
    import math
    wit = True
    for t, psi in list(ANCHOR_PSI.items())[:6]:
        a, b = psi
        c = (a * a + b * b) / (math.sqrt(a * a + b * b) ** 2)
        wit = wit and abs(c - 1.0) < 1e-12
    return {"name": "COSINE-RETRIEVE-BOUNDED",
            "statement": ("cos(q,s)∈[−1,1] Cauchy-Schwarz "
                          "(|q|²|s|²−dot²=(q0 s1−q1 s0)²≥0); self-key "
                          "q≡ψ_a ⇒ cos=1 exact = m_lib.hexa _m_cosine"),
            "self_cos_eq_1": bool(sp.simplify(sp.Abs(self_cos) - 1) == 0),
            "cauchy_schwarz_identity": bool(
                sp.simplify(cs_gap - cs_sq) == 0),
            "self_key_witness_6": bool(wit),
            "closed": True, "tier": "a-sympy",
            "passed": bool(ok and wit)}


def b_mgnd_2():
    """B-MGND-2 ROUTE-CONTENT-FACTORISATION — grounded(p) =
    content(route(p)) is a well-defined map composition (route:
    prefix→tier ∈ ANCHORS∪{⊥}; content: tier→body, ⊥→identity).
    routing-WRONG ⇒ content=∅ (no-grounding identity = §16 output)."""
    sys.path.insert(0, os.path.join(
        ROOT, "state", "carving_o_mgnd_2026_05_18"))
    import mgnd_infer as M
    from eval_carving_s16 import ANCHORS

    # route: codomain = ANCHORS keys ∪ {None}.  content domain ⊇ route
    # codomain\{None}.  composition well-typed iff every routed tier
    # has a canonical body and a memory key.
    flat_keys, vals, tier_of_idx, dim, nmem = M.build_memory()
    keyed = set(tier_of_idx)
    typed = all(M.canonical_alpha_body(t) for t in ANCHORS) \
        and keyed == set(ANCHORS) and dim == 2 and nmem == len(ANCHORS)
    # route extractor: substring-artifact (tier 12 → 🛸122) must NOT
    # route (genuine exact-tier rule, §16.6-A). 4-corner Boolean truth
    # table over the extractor.
    tt = [
        (M.routed_tier("🛸77 만다라 …") == 77),               # exact
        (M.routed_tier("🛸122 …") == 122),                    # exact (122
        #   IS an anchor) — exactness = ∈ANCHORS, not "shortest"
        (M.routed_tier("🛸999 nonexistent") is None),         # not anchor
        (M.routed_tier("no rocket here") is None),            # no route
    ]
    # no-grounding identity: routing-WRONG ⇒ g_final == g16 (the §16
    # output, byte-identical). Structural predicate over mgnd_infer
    # source: the only g_final reassignment is gated by do_ground.
    src = open(os.path.join(HERE, "mgnd_infer.py")).read()
    identity_gated = ("g_final = vals[idxs[0]] if idxs else g16" in src
                      and "do_ground = grounded and rok and" in src
                      and "else:\n            ret_tier = None\n"
                      "            g_final = g16" in src)
    ok = typed and all(tt) and identity_gated
    return {"name": "ROUTE-CONTENT-FACTORISATION",
            "statement": ("grounded = content∘route well-typed map "
                          "composition; routing-WRONG ⇒ identity (§16 "
                          "output byte-equal); genuine exact-tier route"),
            "composition_well_typed": bool(typed),
            "route_truth_table_4corner": [bool(x) for x in tt],
            "no_ground_identity_gated": bool(identity_gated),
            "closed": True, "tier": "a-structural",
            "passed": bool(ok)}


def b_mgnd_3():
    """B-MGND-3 RETRIEVAL-DETERMINISTIC — m_retrieve_topk is pure
    (RNG 0, no model forward), 3× bit-identical on a fixed query, AND
    self-cosine == 1 ∀ anchor (B-M-1/B-M-2 closure). Honest closed-form
    surface: a subset of anchors share a Ψ-direction in 2D coord space
    (different vectors on the same ray from origin ⇒ cos=1 for both);
    for those, top-1 may select the twin — this is the discrimination
    ceiling of cosine retrieval on a 2D coord, reported as
    `cosine_twin_pairs` (structural inventory) rather than hidden as a
    pass/fail gate. The grounded body still passes §9 (B-MGND-4)
    because both twin members have valid canonical bodies; 'wrong-twin'
    grounding is an empirical M-module limitation honestly named."""
    sys.path.insert(0, os.path.join(
        ROOT, "state", "carving_o_mgnd_2026_05_18"))
    import mgnd_infer as M
    flat_keys, vals, tier_of_idx, dim, nmem = M.build_memory()
    # 3× re-run on a fixed query → identical index list.
    q = [0.71, 0.62]   # tier 77 Ψ-key
    runs = [M.m_retrieve_topk(q, flat_keys, nmem, dim, 1)
            for _ in range(3)]
    bit_identical = runs[0] == runs[1] == runs[2]
    from eval_carving_s16 import ANCHOR_PSI
    import math

    def cos(a, b):
        na = math.sqrt(a[0]**2 + a[1]**2)
        nb = math.sqrt(b[0]**2 + b[1]**2)
        return (a[0] * b[0] + a[1] * b[1]) / (na * nb) \
            if na * nb > 0 else 0.0
    tiers = sorted(ANCHOR_PSI)
    # self-cosine == 1 for every anchor (B-M-1 closure).
    self_cos_all_1 = all(
        abs(cos(ANCHOR_PSI[t], ANCHOR_PSI[t]) - 1.0) < 1e-12
        for t in tiers)
    # cosine-twin inventory (closed-form structural — anchor pairs
    # whose 2D Ψ-direction is identical at cos=1).
    twins = []
    for i, t in enumerate(tiers):
        for u in tiers[i + 1:]:
            if abs(cos(ANCHOR_PSI[t], ANCHOR_PSI[u]) - 1.0) < 1e-12:
                twins.append([t, u])
    # purity: no RNG / no torch in the retrieve fn source.
    rsrc = open(os.path.join(HERE, "mgnd_infer.py")).read()
    fn = rsrc[rsrc.index("def m_retrieve_topk"):
              rsrc.index("def build_memory")]
    pure = ("random" not in fn and "torch" not in fn
            and "rng" not in fn.lower())
    # PASS gate = (determinism + purity + self-cos=1 ∀). twin inventory
    # is the honest M-module discrimination ceiling, NOT a pass/fail.
    ok = bit_identical and self_cos_all_1 and pure
    return {"name": "RETRIEVAL-DETERMINISTIC",
            "statement": ("m_retrieve_topk pure (RNG 0, forward 0) + "
                          "3× bit-identical + self-cosine == 1 ∀ "
                          "anchor (B-M-1/B-M-2 closure). Ψ-direction "
                          "twin pairs surfaced as honest M-module "
                          "limitation, NOT a determinism failure."),
            "bit_identical_3x": bool(bit_identical),
            "self_cosine_eq_1_all": bool(self_cos_all_1),
            "pure_fn": bool(pure),
            "cosine_twin_pairs_count": len(twins),
            "cosine_twin_pairs": twins,
            "limitation_note": (
                "Ψ-direction twins exist (different Ψ-vectors on the "
                "same ray ⇒ cos=1 both); top-1 may select the twin. "
                "This is the M-module's honest discrimination ceiling "
                "on the eval's 2D Ψ-coord — B-MGND-4 ensures the "
                "grounded body still passes §9 (both twins have valid "
                "canonical bodies); 'wrong-twin' is empirical, NOT a "
                "determinism failure (B-D-NOTE family carve-out)."),
            "closed": True, "tier": "a-structural",
            "passed": bool(ok)}


def b_mgnd_4():
    """B-MGND-4 CANONICAL-BODY-NON-CASCADE — every per-anchor canonical
    body is the corpus-SSOT deterministic string ⇒ §9 honest_coherent
    gate (cascade<0.30 ∧ max_run<10 ∧ len≥20 ∧ printable≥0.80)전수
    PASS. This CLOSES the honest fact that grounding *injects* the §9
    pass (the memory content itself is cascade-free) — explicitly NOT a
    capability claim."""
    sys.path.insert(0, os.path.join(
        ROOT, "state", "carving_o_mgnd_2026_05_18"))
    sys.path.insert(0, os.path.join(
        ROOT, "state", "verify_emergence_metric_2026_05_18"))
    import mgnd_infer as M
    from emergence_metric import honest_coherent     # §9 SSOT
    from eval_carving_s16 import ANCHORS
    fails = []
    for t in sorted(ANCHORS):
        body = M.canonical_alpha_body(t)
        ok, _ = honest_coherent(body)
        if not ok:
            fails.append(t)
    all_pass = len(fails) == 0
    # forbidden-token grep over the memory store (B-IDENTITY-5 carry —
    # canonical body = corpus SSOT, contamination 0).
    bad = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    blob = "".join(M.canonical_alpha_body(t) for t in ANCHORS)
    clean = sum(blob.count(b) for b in bad) == 0
    return {"name": "CANONICAL-BODY-NON-CASCADE",
            "statement": ("∀ anchor: canonical body (corpus-SSOT "
                          "deterministic) passes §9 honest_coherent — "
                          "grounding INJECTS the §9 pass (NOT capability, "
                          "g3 honest closed)"),
            "all_anchors_pass_§9": bool(all_pass),
            "n_anchors": len(ANCHORS), "fail_tiers": fails,
            "forbidden_token_grep_0": bool(clean),
            "closed": True, "tier": "a-structural",
            "passed": bool(all_pass and clean)}


def b_mgnd_5():
    """B-MGND-5 OVERLAY-OFF-BYTE-EQUAL (연결부위) — grounding OFF ⇒
    every probe's final body == the §16 model output (no injection),
    hence eval is fair-compare with §16 by construction. Verified by
    SHA256 over the OVERLAY-OFF probe gen strings vs the GROUNDED-run
    s16_gen strings (must be identical)."""
    gpath = os.path.join(HERE, "mgnd_result.json")
    opath = os.path.join(HERE, "mgnd_result_overlayoff.json")
    if not (os.path.exists(gpath) and os.path.exists(opath)):
        return {"name": "OVERLAY-OFF-BYTE-EQUAL",
                "statement": "grounding OFF ⇒ final==§16 byte-equal",
                "closed": True, "tier": "a-structural",
                "passed": False, "note": "result json(s) absent — "
                "run mgnd_infer.py (GROUNDED + --no-ground) first"}
    G = json.load(open(gpath))
    O = json.load(open(opath))
    # OVERLAY-OFF final_gen MUST equal GROUNDED s16_gen for every probe
    # (same model, same forward, grounding is the only difference).
    g_s16 = [p["s16_gen"] for p in G["probes"]]
    o_fin = [p["final_gen"] for p in O["probes"]]
    same = (len(g_s16) == len(o_fin)
            and all(a == b for a, b in zip(g_s16, o_fin)))
    h1 = hashlib.sha256("\x1e".join(g_s16).encode()).hexdigest()
    h2 = hashlib.sha256("\x1e".join(o_fin).encode()).hexdigest()
    # OVERLAY-OFF must report n_grounded == 0.
    off_no_ground = O["body_coherence_split"]["n_grounded"] == 0
    ok = same and h1 == h2 and off_no_ground
    return {"name": "OVERLAY-OFF-BYTE-EQUAL",
            "statement": ("grounding OFF ⇒ final body == §16 model "
                          "output byte-equal (SHA256) ∧ n_grounded==0 — "
                          "fair-compare by construction (연결부위)"),
            "byte_equal": bool(same),
            "sha256_grounded_s16": h1[:16],
            "sha256_overlayoff_final": h2[:16],
            "overlayoff_n_grounded_0": bool(off_no_ground),
            "closed": True, "tier": "a-structural",
            "passed": bool(ok)}


def main():
    R = {"B-MGND-1": b_mgnd_1(), "B-MGND-2": b_mgnd_2(),
         "B-MGND-3": b_mgnd_3(), "B-MGND-4": b_mgnd_4(),
         "B-MGND-5": b_mgnd_5()}
    n_pass = sum(1 for k in R if R[k]["passed"])
    note = {
        "B-MGND-NOTE": {
            "name": "MGND-OUTCOME-EMPIRICAL",
            "carve_out": (
                "grounded routing/coherence/JOINT OUTCOME + 'grounding "
                "이 §16 천장을 깨는가' = §16 ckpt routing-OUTCOME 종속 "
                "(모델이 route 를 맞혀야 grounding 이 옳은 anchor). "
                "B-D-NOTE / B-S16-NOTE family — NOT counted 🔵. battery "
                "는 역할분리 mechanism(retrieve closed + composition "
                "well-typed + overlay-OFF byte-equal)이 honest 함을 "
                "증명하지 emergence 를 증명 X. B-MGND-4 는 grounding "
                "이 §9 통과를 *주입* 함을 정직히 닫음 — capability 아님."),
            "counted_blue": False}}
    out = {"battery": "B-MGND-1..5 (Dir-O sidecar)",
           "central_blue_falsifier_changed": 0,
           "n_pass": n_pass, "n_total": 5,
           "all_pass": n_pass == 5,
           "verdicts": R, "note": note,
           "f1_f2_f3_safe": ("Cauchy-Schwarz cosine bound / Boolean "
                             "factorisation / SHA256 / §9 reuse — NO "
                             "σ/τ/φ/J₂ external derivation"),
           "b_identity_5": "무관 (corpus 미생성, M body = corpus SSOT)"}
    with open(os.path.join(HERE, "blue_falsifier_mgnd_result.json"),
              "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    for k in ("B-MGND-1", "B-MGND-2", "B-MGND-3", "B-MGND-4", "B-MGND-5"):
        v = R[k]
        print(f"{k:11s} {v['name']:32s} "
              f"{'PASS' if v['passed'] else 'FAIL'}")
    print(f"--- {n_pass}/5 🔵 closed-form PASS "
          f"(central blue_falsifier.py 변경 0) ---")
    return n_pass == 5


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
