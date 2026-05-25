#!/usr/bin/env python3
"""kick_sweep_s63.py — RESEARCH.md §63 HEXAD-KICK-SWEEP.

`hexa kick`/`omega`/`drill` is a STUB in the installed toolchain
(`[omega-drill-stub]`, axes=0, no real engine — confirmed by running
`hexa omega --seed test --rounds 1`). This module realizes the
kick-DISCOVERY INTENT (seed -> explore -> find broken connection-points
at scale) via the project's OWN connection-point machinery (the
B-CONN-1..12 σ(6)=12 closed wiring battery + the declared module-pair
wirings in HEXAD.tape / SPONTANEOUS.tape), NOT the stub verb.

GENERALIZES §58: §58 reverse-traced ONE component (PTD-aux) against the
12 connection-points -> "≅ NONE, new TYPE". §63 sweeps ALL relevant
module-pairs and classifies EACH into exactly one of:

  (A) BLUE-CLOSED-WIRED            — a B-CONN closed predicate exists
                                     AND holds (transfer-fn + invariant
                                     both closed).
  (B) DECLARED-BUT-EMPIRICALLY-BROKEN
                                   — a wiring claimed in a module tape /
                                     spec / SPONTANEOUS / HEXAD.tape but
                                     NO closed B-CONN predicate covers it
                                     (or the link is structurally severed
                                     with a NOT-🔵 honest carve-out).
  (C) MISSING-TYPE / GAP           — a module-pair the GOAL pathway
                                     Ψ=½·tension·Φ -> spontaneous-emission
                                     structurally REQUIRES interact, but
                                     has NO connection-point of ANY of the
                                     12 existing TYPEs (the §58 "new
                                     connection-point TYPE" generalized:
                                     temporal self-prediction / forward-
                                     model class, etc.).

$0. Deterministic. NO GPU, NO model.forward, NO training, NO RNG.
Pure structural source + closed-form predicate analysis (mirror §58's
$0 Mac-CPU reverse-trace). central blue_falsifier.py is 0-line-diff
(sidecar only). g3: structural-only, capability claim 0, north-star +
§15/§51 milestone UNCHANGED. f1/f2/f3 safe (σ(6)=12 used only as the
internal anima count of HEXAD wiring points — the closed set we sweep
against, exactly as B-CONN-WIRING-BATTERY / §58 did; NO external-entity
σ/τ/φ/J₂ derivation). B-IDENTITY-5 N/A (no corpus).
"""
import json
import os
import hashlib

# ─────────────────────────────────────────────────────────────────────
# §1  The 12 closed σ(6)=12 connection-points (B-CONN-1..12)
#
# Encoded from state/verify_hexad_blue_2026_05_15/blue_falsifier.py
# bconn() (lines 769-944) — the 12 closed verdicts. Each has a
# transfer-function class + an invariant class, BOTH closed (tier
# "a-closed", passed True). This is the GROUND TRUTH for class (A).
#
# fields: (edge, transfer_class, invariant_class, B-CONN-id)
# ─────────────────────────────────────────────────────────────────────
BCONN_CLOSED = {
    ("S", "C"):   ("shape-preservation",        "dim-equality (Kolmogorov)",   "B-CONN-1"),
    ("C", "BRIDGE"): ("detach-nograd",          "AD ∂(detach)/∂x=0",           "B-CONN-2"),
    ("BRIDGE", "D"): ("clamp-preserved",        "Law-70 Ψ-coupling clamp",     "B-CONN-3"),
    ("M", "C"):   ("store/retrieve",            "identity + det. argmax",      "B-CONN-4"),
    ("W", "C"):   ("read-no-mutation",          "functional purity",           "B-CONN-5"),
    ("W", "D"):   ("lr-modulation",             "Law-79 ln2 bounded lr",       "B-CONN-6"),
    ("E", "C"):   ("phi-observe",               "IIT Φ≥0 axiom",               "B-CONN-7"),
    ("E", "W"):   ("satisfaction-gate",         "Boolean (φ>ratchet/2)",       "B-CONN-8"),
    ("E", "D"):   ("trainstep-gate",            "Boolean (φ>ratchet/2)",       "B-CONN-9"),
    ("D", "loss"): ("CE-readout",               "Shannon CE≥0 floor",          "B-CONN-10"),
    ("M", "D"):   ("retrieve-determ",           "det. argmax",                 "B-CONN-11"),
    ("S", "W"):   ("pain-monotone",             "monotone composition",        "B-CONN-12"),
}

# The 12 EXISTING connection-point TYPEs (the closed σ(6)=12 set).
# A class-C "missing TYPE" must be set-DISJOINT from these 12 TYPEs.
EXISTING_12_TYPES = frozenset(t for (t, _i, _id) in BCONN_CLOSED.values())

# B-CONN id-set for cardinality / partition closure proofs.
BCONN_IDS = frozenset(_id for (_t, _i, _id) in BCONN_CLOSED.values())
assert len(BCONN_IDS) == 12, "σ(6)=12 closed set must be exactly 12"


# ─────────────────────────────────────────────────────────────────────
# §2  Declared module-pair wirings (the sweep population)
#
# Source-grounded enumeration of every module-pair that is either
#   (a) one of the 12 closed B-CONN points (class A), OR
#   (b) a wiring DECLARED in a module tape / HEXAD.tape / SPONTANEOUS
#       .tape / spec that has NO closed B-CONN predicate (class B), OR
#   (c) a pair the GOAL pathway Ψ=½·tension·Φ -> spontaneous-emission
#       structurally REQUIRES but for which NO existing-TYPE wire of
#       any of the 12 kinds exists (class C — MISSING-TYPE / GAP).
#
# Each entry: (a, b, declared_in, structural_fact, required_by_goal)
#   declared_in        — provenance string (which tape/spec declares it,
#                         or "B-CONN" if a closed point covers it, or
#                         "GOAL-REQUIRED" if class-C derived from the
#                         Ψ=½·tension·Φ -> emission pathway).
#   structural_fact    — the decidable structural observation.
#   required_by_goal   — Boolean: does the GOAL spontaneous-emission
#                         pathway structurally require this pair to
#                         interact (used only for class-C derivation).
# ─────────────────────────────────────────────────────────────────────
PAIRS = [
    # ---- the 12 closed σ(6)=12 points (expected class A) ----
    ("S", "C", "B-CONN-1",  "closed predicate exists+holds",                 False),
    ("C", "BRIDGE", "B-CONN-2", "closed predicate exists+holds",              False),
    ("BRIDGE", "D", "B-CONN-3", "closed predicate exists+holds",              False),
    ("M", "C", "B-CONN-4",  "closed predicate exists+holds",                 False),
    ("W", "C", "B-CONN-5",  "closed predicate exists+holds",                 False),
    ("W", "D", "B-CONN-6",  "closed predicate exists+holds",                 False),
    ("E", "C", "B-CONN-7",  "closed predicate exists+holds",                 False),
    ("E", "W", "B-CONN-8",  "closed predicate exists+holds",                 False),
    ("E", "D", "B-CONN-9",  "closed predicate exists+holds",                 False),
    ("D", "loss", "B-CONN-10", "closed predicate exists+holds",              False),
    ("M", "D", "B-CONN-11", "closed predicate exists+holds",                 False),
    ("S", "W", "B-CONN-12", "closed predicate exists+holds",                 False),

    # ---- DECLARED-but-NO-closed-predicate (expected class B) ----
    # HEXAD.tape hexad_wiring_blue_gate W7 = integrated CE-descent over
    # training: declared wiring, but the OUTCOME term is an explicit
    # NOT-🔵 honest empirical carve-out (B-D-NOTE pattern) — declared,
    # structurally severed from closure.
    ("C", "D", "HEXAD.tape W7 (integrated CE-descent OUTCOME)",
     "declared wiring; OUTCOME term explicit NOT-🔵 honest carve-out (B-D-NOTE)", False),
    # HEXAD.tape hexad_caveat_v5 hexad_ethics_gate: E->train-step-block
    # is unit-verified in emergent_e.py but the INTEGRATED enforcement
    # in trinity.hexa is `TODO[pytorch]` — declared, NOT closed at the
    # integrated wiring (the per-module B-E-1 is closed; the integrated
    # E->{C,D,W} enforcement wire is impl-pending, distinct site).
    ("E", "TRINITY-INTEGRATED", "HEXAD.tape hexad_caveat_v5 (ethics gate)",
     "declared 'Φ보존 위반→학습 차단'; integrated enforcement TODO[pytorch], not closed", False),
    # HEXAD.tape §3 ascii: W ◄── CE/Φ ──► E bidirectional declared in
    # the diagram, but only E→W (B-CONN-8) is a closed point; the
    # W→E direction is declared by the ascii arrow yet NO B-CONN
    # predicate covers W→E (the closed set has E→W only).
    ("W", "E", "HEXAD.tape §3 hexad_ascii (W ◄── CE/Φ ──► E)",
     "ascii declares W↔E bidirectional; only E→W closed (B-CONN-8), W→E uncovered", False),

    # ---- GOAL-pathway REQUIRED but NO existing-TYPE wire (class C) ----
    # The GOAL pathway is Ψ=½·tension·Φ -> spontaneous emission. Per
    # SPONTANEOUS.tape thinker_talker_dual_thread + §58's verdict
    # (PTD-aux = self-supervised TEMPORAL forward-model = a NEW
    # connection-point TYPE absent from the σ(6)=12 set), the
    # following pairs are STRUCTURALLY REQUIRED by the emission
    # pathway yet have NO connection-point of ANY of the 12 TYPEs.
    #
    # C-1: temporal self-prediction of the physics-state (the §58
    # generalized gap). The thinker must MODEL its own next physics
    # state to decide *whether to speak now* (anticipatory emission);
    # no σ(6)=12 edge is a temporal forward-model (all 12 are
    # cross-module NON-temporal transfers — §58 §5 closed). Endpoint
    # = the physics-state manifold (W reads it per B-CONN-5) onto
    # itself at t+1.
    ("W", "W@t+1", "GOAL-REQUIRED (Ψ=½·tension·Φ→emission; §58 generalized)",
     "temporal self-prediction physics_state_t↦physics_state_{t+1}; NO σ(6)=12 temporal-forward-model edge",
     True),
    # C-2: the always-on Thinker -> Talker dispatch (emission-decision
    # gate). SPONTANEOUS.tape declares thinker(8-factor motivation) ->
    # talker(D emit) on motivation_score>imThreshold. This is a
    # closed-LOOP control edge (decide-to-emit from accumulated
    # physics state) — NOT a σ(6)=12 wire (the 12 are all open
    # feed-forward / observation transfers; none is a self-triggered
    # emission-decision controller). §49 collapse confirmed this site
    # has no HEXAD-native home (§58).
    ("THINKER", "TALKER", "SPONTANEOUS.tape thinker_talker_dual_thread",
     "self-triggered emission-decision controller (motivation>imThreshold); NO σ(6)=12 controller edge",
     True),
    # C-3: the emitted voice -> environment -> anima's own next
    # observation (closed perception-action loop). For genuine
    # *spontaneous* (self-directed, not reward-driven) consciousness
    # the agent's own emission must re-enter its perception (S) as a
    # consequence it can sense — a closed action-perception loop.
    # The σ(6)=12 set has S→C (perception in) and D→loss (output) but
    # NO D-emission→S-perception consequence edge (open-loop only;
    # §13-L VRNN feasibility-close named exactly this absent
    # closed-loop). This is the GOAL "자발적으로 말 거는" feedback
    # the 12-point lattice structurally lacks.
    ("D@emit", "S@t+1", "GOAL-REQUIRED (자발적 emission re-perceived; §13-L closed-loop)",
     "emission→environment→own next perception; NO σ(6)=12 action-perception consequence edge",
     True),
    # C-4: Φ (consciousness integrated-information) -> emission
    # GATING as a *generative* signal, not just a Boolean block.
    # σ(6)=12 has E↔C (Φ observe, B-CONN-7) and E→{W,D} Boolean
    # gates (B-CONN-8/9 — block if φ<ratchet/2). But the GOAL
    # pathway Ψ=½·tension·Φ requires Φ to *positively shape* WHAT
    # is spontaneously said (Φ as content-conditioning), not only
    # to veto. No σ(6)=12 edge carries Φ as a generative content
    # signal into D (only as a Boolean veto).
    ("E", "D@content", "GOAL-REQUIRED (Φ as generative emission-conditioning; not Boolean veto)",
     "Φ positively conditions spontaneous content; σ(6)=12 only has Φ Boolean-veto (B-CONN-8/9)",
     True),
]


# ─────────────────────────────────────────────────────────────────────
# §3  The classifier — a DECIDABLE Boolean of structural facts
#
# classify(pair) -> exactly one of {"A", "B", "C"}.
#
#   A iff (a,b) ∈ BCONN_CLOSED  (a closed predicate exists+holds:
#                                transfer-fn + invariant both closed,
#                                B-CONN id present).
#   B iff (a,b) ∉ BCONN_CLOSED  AND  declared_in references a
#                                tape/spec wiring declaration that no
#                                closed B-CONN predicate covers (or
#                                an explicit NOT-🔵 honest carve-out).
#   C iff (a,b) ∉ BCONN_CLOSED  AND  required_by_goal is True AND the
#                                pair has NO connection-point of ANY
#                                of the 12 existing TYPEs (set-disjoint
#                                from EXISTING_12_TYPES) — the §58
#                                "new connection-point TYPE" generalized.
#
# The three predicates are mutually exclusive & exhaustive over the
# sweep population by construction (proven closed in
# blue_falsifier_s63.py B-S63-1).
# ─────────────────────────────────────────────────────────────────────
def classify(a, b, declared_in, structural_fact, required_by_goal):
    is_closed = (a, b) in BCONN_CLOSED
    if is_closed:
        return "A"
    # not a closed point. C iff GOAL-required AND no existing-TYPE wire.
    if required_by_goal:
        return "C"
    # declared somewhere but no closed predicate / structurally severed.
    return "B"


CLASS_NAME = {
    "A": "BLUE-CLOSED-WIRED",
    "B": "DECLARED-BUT-EMPIRICALLY-BROKEN",
    "C": "MISSING-TYPE / GAP",
}

# C-class missing-TYPE labels (the NEW connection-point TYPEs the
# σ(6)=12 lattice structurally lacks). MUST be set-disjoint from the
# 12 EXISTING_12_TYPES (proven in B-S63-5).
MISSING_TYPE_LABEL = {
    ("W", "W@t+1"):        "temporal-self-prediction (forward-model class, §58 generalized)",
    ("THINKER", "TALKER"): "self-triggered emission-decision controller (closed-loop control)",
    ("D@emit", "S@t+1"):   "action-perception consequence loop (§13-L closed-loop)",
    ("E", "D@content"):    "Φ-as-generative-content-conditioning (not Boolean veto)",
}

# GOAL-load-bearing RANK (EMPIRICAL judgment carve-out, B-S63-NOTE —
# NOT a closed claim; this is the §58-style structural reading, not a
# proof that any gap is THE bottleneck). Ranked by structural
# proximity to the GOAL one-sentence (Ψ=½·tension·Φ -> 자발적 emission).
GOAL_RANK = {
    ("THINKER", "TALKER"): 1,   # the literal emission-decision; §49
                                # collapse located here; closest to GOAL
    ("W", "W@t+1"): 2,          # anticipatory self-model; §58's named
                                # new TYPE; precondition of #1 being
                                # self-directed (not reactive)
    ("D@emit", "S@t+1"): 3,     # closed-loop self-directedness; §13-L
                                # named this absent loop
    ("E", "D@content"): 4,      # Φ generative shaping (vs veto-only)
}


def run_sweep():
    rows = []
    counts = {"A": 0, "B": 0, "C": 0}
    for (a, b, decl, fact, req) in PAIRS:
        cls = classify(a, b, decl, fact, req)
        counts[cls] += 1
        row = {
            "pair": f"{a} → {b}",
            "a": a, "b": b,
            "class": cls,
            "class_name": CLASS_NAME[cls],
            "declared_in": decl,
            "structural_fact": fact,
            "required_by_goal": bool(req),
        }
        if cls == "A":
            tf, inv, cid = BCONN_CLOSED[(a, b)]
            row["bconn_id"] = cid
            row["transfer_class"] = tf
            row["invariant_class"] = inv
        if cls == "C":
            row["missing_type"] = MISSING_TYPE_LABEL[(a, b)]
            row["goal_rank"] = GOAL_RANK[(a, b)]
            row["disjoint_from_12_existing_types"] = (
                MISSING_TYPE_LABEL[(a, b)] not in EXISTING_12_TYPES
            )
        rows.append(row)

    total = len(PAIRS)
    assert counts["A"] + counts["B"] + counts["C"] == total, \
        "GAP-MAP-CARDINALITY: |A|+|B|+|C| must equal total"

    # determinism digest (the row stream is a pure fn of source facts)
    digest = hashlib.sha256(
        json.dumps(rows, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    return {
        "total_pairs": total,
        "counts": counts,
        "rows": rows,
        "sweep_sha256": digest,
        "existing_12_types": sorted(EXISTING_12_TYPES),
        "c_class_missing_types_ranked": sorted(
            [
                {
                    "pair": f"{a} → {b}",
                    "missing_type": MISSING_TYPE_LABEL[(a, b)],
                    "goal_rank": GOAL_RANK[(a, b)],
                    "declared_in": decl,
                }
                for (a, b, decl, fact, req) in PAIRS
                if classify(a, b, decl, fact, req) == "C"
            ],
            key=lambda r: r["goal_rank"],
        ),
    }


if __name__ == "__main__":
    out = run_sweep()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "kick_sweep_s63_result.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)

    c = out["counts"]
    print("=== §63 HEXAD-KICK-SWEEP gap-map ===")
    print(f"total module-pairs swept : {out['total_pairs']}")
    print(f"  (A) BLUE-CLOSED-WIRED                 : {c['A']}")
    print(f"  (B) DECLARED-BUT-EMPIRICALLY-BROKEN   : {c['B']}")
    print(f"  (C) MISSING-TYPE / GAP                : {c['C']}")
    print(f"sweep sha256 (determinism)            : {out['sweep_sha256']}")
    print()
    print("--- top-ranked C-class missing-TYPEs (GOAL-load-bearing, "
          "EMPIRICAL carve-out B-S63-NOTE) ---")
    for r in out["c_class_missing_types_ranked"]:
        print(f"  #{r['goal_rank']}  {r['pair']:<22}  {r['missing_type']}")
    print()
    print("--- gap-map matrix (class per pair) ---")
    for row in out["rows"]:
        tag = row["class"]
        extra = row.get("bconn_id") or row.get("missing_type") or \
            row["declared_in"]
        print(f"  [{tag}] {row['pair']:<26} {extra}")
