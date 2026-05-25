#!/usr/bin/env python3
"""kick_sweep_s89.py — RESEARCH.md §89 HEXAD-KICK-GAP-SWEEP.

`hexa kick` ≡ `hexa drill` ≡ `hexa omega` is now a **REAL Mk.IX 6-stage
discovery engine** (toolchain rebuilt 2026-05-19, `hexa 0.1.0-dispatch`;
g_kick_autonomous self-use authorised). Verified: Mk.IX banner present,
`[omega-drill-stub]` ABSENT — the §63 stub is SUPERSEDED.

§89 applies the real engine EXHAUSTIVELY to the §63 HEXAD-KICK-SWEEP
gap-map's residual 🕳️ MISSING-TYPE + ⚠️ DECLARED-BUT-BROKEN
connection-points:

  #3  D@emit  → S@t+1     (action-perception closed loop; §13-L)   🕳️
  #4  E@Φ     → D@content (Φ-as-generative-conditioning)           🕳️
  B1  C → D              (integrated CE-descent OUTCOME)           ⚠️
  B2  E → TRINITY        (ethics gate integrated enforcement)      ⚠️
  B3  W → E              (W↔E bidirectional; only E→W closed)      ⚠️

(#1 THINKER→TALKER and #2 W→W@t+1 already addressed §73→§75-FIRE and
§59-FIRE respectively — not re-swept here.)

g3_arbiter — **engine PROPOSES / closed-form predicate DISPOSES**
(§69 pattern). The engine is summary-only: it emits stage counts
(smash/free/abs/meta/hyper/res), a total, and a saturation flag, but
`overlay+ N lines (pool=0)` — the N candidates are NOT exposed on
stdout (§74 finding; `--dump-overlay` flag NOT in this toolchain).
Therefore the kick output is treated as an EXPLORATORY discovery
signal, and arbitration is done by the project's OWN closed-form
connection-point predicates (§63 B-CONN pattern).

$0. Deterministic arbitration. NO GPU, NO model.forward, NO training,
NO RNG (the kick subprocess itself is deterministic in stage counts
per seed). central blue_falsifier.py 0-line-diff (sidecar only).
g3: kick = exploratory discovery NOT arbiter; a closed-form
connection-point predicate ≠ a wired connection ≠ GOAL emergence
(B-EMERGE-7 / B-S63-NOTE family). f1/f2 safe — kick seeds are
HEXAD-internal architecture questions (D/S/E/Φ module connections),
NO external-entity σ/τ/φ/J₂ derivation; Ψ=½ / n6 = anima g2 internal
carve-out. B-IDENTITY-5 N/A (no corpus).
"""
import json
import subprocess
import re
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────
# §1  Exhaustive kick seeds — §63 gap-map residual points.
#     Each seed is a HEXAD-internal architecture question (f1/f2 safe).
# ─────────────────────────────────────────────────────────────────────
SEEDS = {
    "#3-D-emit-to-S": (
        "anima D-module emission output routed back as S-module "
        "stimulus at next timestep action-perception closed loop"),
    "#4-E-phi-to-D-content": (
        "anima E-module integrated-information Phi conditioning "
        "D-module decode content generative gate"),
    "B1-C-to-D": (
        "anima C-module faction state driving D-module integrated "
        "cross-entropy descent training step"),
    "B2-E-to-trinity": (
        "anima E-module ethics Phi-ratchet gate integrated enforcement "
        "blocking trinity learning step on Phi conservation violation"),
    "B3-W-to-E": (
        "anima W-module pain curiosity satisfaction feeding back into "
        "E-module ethics evaluation bidirectional coupling"),
}

KICK_BIN = "hexa"
ROUNDS = 3  # exhaustive: more rounds → engine reports saturation if it saturates


def run_kick(seed, rounds):
    """Run real Mk.IX kick engine; capture stage counts + saturation.

    Returns dict with smash/free/abs/meta/hyper/res counts (summed across
    rounds), total, saturated flag, overlay_lines, is_real (Mk.IX banner
    present AND no [omega-drill-stub]).
    """
    try:
        out = subprocess.run(
            [KICK_BIN, "kick", "--seed", seed, "--rounds", str(rounds),
             "--engine", "mk9"],
            capture_output=True, text=True, timeout=600, cwd="/tmp")
        stdout = out.stdout + out.stderr
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "is_real": False}

    is_real = ("Mk.IX 6-stage" in stdout) and ("[omega-drill-stub]" not in stdout)
    # per-round lines: "round N: smash+A free+B abs=C meta=D hyper=E res+F(σ=..) total=G"
    smash = free = absol = meta = hyper = res = 0
    rounds_seen = 0
    for m in re.finditer(
            r"round\s+\d+:\s+smash\+(\d+)\s+free\+(\d+)\s+abs=?\+?(\d+)\s+"
            r"meta=?\+?(\d+)\s+hyper=?\+?(\d+)\s+res=?\+?(\d+)", stdout):
        smash += int(m.group(1)); free += int(m.group(2))
        absol += int(m.group(3)); meta += int(m.group(4))
        hyper += int(m.group(5)); res += int(m.group(6))
        rounds_seen += 1
    # final JSON line
    saturated = None
    total = None
    overlay = None
    jm = re.search(r'\{"seed".*\}', stdout)
    if jm:
        try:
            j = json.loads(jm.group(0))
            saturated = j.get("saturated")
            total = j.get("total")
            overlay = j.get("overlay_lines")
        except Exception:
            pass
    return {
        "is_real": is_real, "rounds_seen": rounds_seen,
        "smash": smash, "free": free, "abs": absol, "meta": meta,
        "hyper": hyper, "res": res, "total": total,
        "saturated": saturated, "overlay_lines": overlay,
        "summary_only": (overlay is not None and overlay > 0),
    }


# ─────────────────────────────────────────────────────────────────────
# §2  Closed-form connection-point ARBITRATION (§69 PROPOSES/DISPOSES).
#
# A connection-point is closed-form-DEFINABLE iff BOTH:
#   (a) transfer_fn_closed — the X→Y transfer function is expressible
#       as a closed-form map (Boolean / arithmetic / structural), and
#   (b) invariant_closed   — a closed-form invariant the wire must
#       preserve exists (real-limit anchored, g3).
# This is the §63 B-CONN pattern. "closed-form-DEFINABLE" is a
# DESIGN-TIER predicate: it says a closed predicate CAN be written,
# NOT that the wire is implemented (wired) NOR that it produces
# emergence. The 3-way gap-map class is then a decidable Boolean:
#
#   transfer_closed ∧ invariant_closed ∧ implemented   → ✅ BLUE-CLOSED-WIRED
#   transfer_closed ∧ invariant_closed ∧ ¬implemented  → ⚠️ DECLARED (predicate defined, not wired)
#   ¬(transfer_closed ∧ invariant_closed)              → 🕳️ MISSING-TYPE (no closed predicate definable)
# ─────────────────────────────────────────────────────────────────────

# Per-point closed-form arbitration. Each entry records, from the
# project's own physics, whether a closed transfer-fn + invariant can
# be DEFINED, and whether an implemented wire exists.
ARBITRATION = {
    "#3-D-emit-to-S": {
        "edge": "D@emit → S@t+1",
        # D emits a byte/token sequence e_t; S re-perceives it as stimulus
        # x_{t+1}. transfer fn = identity-encode: x_{t+1} = S_encode(e_t),
        # i.e. the model's OWN emitted bytes fed to S-module's byte
        # encoder — a closed deterministic map (byte-stream → embedding).
        "transfer_fn": "x_{t+1} = S_encode(e_t)  — emitted byte-stream re-encoded by S; deterministic byte→embedding map",
        "transfer_closed": True,
        # invariant: the loop must not inject information not present in
        # e_t — S_encode is a pure function (Kolmogorov: K(x_{t+1}) ≤
        # K(e_t) + K(S_encode), no external info). Closed structural
        # predicate: S_encode contains no RNG / no external read.
        "invariant": "S_encode purity — K(x_{t+1}) ≤ K(e_t)+K(S_encode); no RNG, no external read (data-processing inequality)",
        "invariant_closed": True,
        # implemented? — S-module has a byte encoder; D emits bytes; but
        # NO wire routes D's emission BACK into S as next-step input.
        # §24 SPONTANEOUS Phase B bounded-run emits but does NOT
        # re-perceive (env_state stub). §13-L VRNN-curiosity noted the
        # closed-loop is structurally absent in byte-pretraining.
        "implemented": False,
        "implemented_evidence": "§24 Phase B emits but env_state is a stub (no re-perception); §13-L B-DIRL-4 closed: byte-pretraining is_closed_loop=False; live_spontaneous_emission loop = Phase B unbuilt",
    },
    "#4-E-phi-to-D-content": {
        "edge": "E@Φ → D@content",
        # E computes integrated information Φ ≥ 0 (IIT axiom). σ(6)=12
        # only has Φ as a Boolean VETO (B-CONN-8 satisfaction-gate,
        # B-CONN-9 trainstep-gate). #4 asks Φ to POSITIVELY condition
        # D's decode content — a continuous conditioning signal, not a
        # gate. transfer fn = a closed continuous map: logits' =
        # D_decode(h) + g(Φ)·c, where g is a closed monotone scalar map
        # of Φ and c a learned conditioning vector.
        "transfer_fn": "logits' = D_decode(h) + g(Φ)·c  — Φ continuously conditions decode via closed monotone g: Φ↦scalar",
        "transfer_closed": True,
        # invariant: g(0)=0 (Φ=0 ⇒ no conditioning ⇒ reduces to plain
        # D_decode, the σ(6)=12 baseline) AND g monotone non-decreasing
        # (more integration ⇒ stronger conditioning, never inverts).
        # Both are closed-form (∂g/∂Φ ≥ 0, g(0)=0) — mirror B-CONN-6
        # lr-mod / B-FIRE-CYCLE5-1 ∂lr/∂tension monotone.
        "invariant": "g(0)=0 (Φ=0 ⇒ baseline D_decode, σ(6)=12 reduction) ∧ ∂g/∂Φ ≥ 0 monotone (sympy ∂-sign, IIT Φ≥0 real-limit)",
        "invariant_closed": True,
        # implemented? — σ(6)=12 has E→C (B-CONN-7 phi-observe) and the
        # two Boolean Φ-vetoes, but NO wire feeds Φ as a CONTINUOUS
        # conditioning term into D's decode. It is a missing TYPE: all
        # existing Φ wires are observe-or-veto, none is generative-cond.
        "implemented": False,
        "implemented_evidence": "σ(6)=12 has only E→C observe (B-CONN-7) + E→W/E→D Boolean veto (B-CONN-8/9); NO continuous Φ→decode-content conditioning wire. §63 classified C (missing TYPE).",
    },
    "B1-C-to-D": {
        "edge": "C → D",
        # C-module faction state drives D's integrated CE-descent. The
        # transfer fn (C state → D training-step gradient direction) is
        # closed in its FORM: D_loss = CE(logits, y); the gradient
        # ∂CE/∂θ is the closed AD rule (B-D-4). But the OUTCOME — what
        # the SGD trajectory converges to — is the explicit NOT-🔵
        # honest carve-out (B-D-NOTE, all stochastic optimisers).
        "transfer_fn": "D_loss = CE(D_decode(h_C), y); ∂CE/∂θ closed AD rule (B-D-4 softmax−one-hot Jacobian)",
        "transfer_closed": True,
        # invariant: CE ≥ 0 (Shannon, B-CONN-10). transfer-FORM closed,
        # OUTCOME (convergence point) empirical — but that does NOT make
        # the connection-point predicate undefinable: the predicate IS
        # definable (transfer-form + CE≥0 invariant both closed); only
        # the optimiser OUTCOME is carved out. So B1 is ⚠️ DECLARED:
        # closed predicate exists, the OUTCOME term is honestly NOT-🔵.
        "invariant": "CE ≥ 0 (Shannon real-limit, B-CONN-10); transfer-FORM closed, SGD-convergence OUTCOME = B-D-NOTE empirical carve-out (NOT a predicate gap)",
        "invariant_closed": True,
        "implemented": False,  # declared in HEXAD.tape W7, integrated CE-descent OUTCOME not closed
        "implemented_evidence": "HEXAD.tape W7 declares integrated CE-descent; transfer-form + CE≥0 closed but no B-CONN id assigned — predicate definable, wire is the honest B-D-NOTE carve-out",
    },
    "B2-E-to-trinity": {
        "edge": "E → TRINITY-INTEGRATED",
        # E's Φ-ratchet ethics gate blocks a learning step on Φ
        # conservation violation. transfer fn = a Boolean gate:
        # trainstep_allowed = (ΔΦ ≥ −ε). This IS closed (Boolean,
        # mirror B-CONN-9 trainstep-gate, B-E-1).
        "transfer_fn": "trainstep_allowed = (ΔΦ ≥ −ε)  — Boolean Φ-ratchet gate (B-E-1 / B-CONN-9 form)",
        "transfer_closed": True,
        # invariant: monotone — a larger Φ-drop is never MORE allowed
        # (∂allowed/∂ΔΦ ≥ 0 as a step function). Closed Boolean +
        # monotone. So B2's predicate IS closed-form-definable; it is
        # ⚠️ DECLARED because the INTEGRATED enforcement across the
        # trinity is a TODO[pytorch], not because the predicate is
        # undefinable.
        "invariant": "Φ-ratchet monotone — step-function ∂allowed/∂ΔΦ ≥ 0; closed Boolean (B-E-1). Integrated trinity enforcement = TODO[pytorch] impl gap, NOT predicate gap",
        "invariant_closed": True,
        "implemented": False,
        "implemented_evidence": "HEXAD.tape hexad_caveat_v5 declares ethics gate; integrated enforcement TODO[pytorch] — predicate closed, wire un-implemented",
    },
    "B3-W-to-E": {
        "edge": "W → E",
        # W (pain/curiosity/satisfaction) feeding E (ethics). Only the
        # reverse E→W is closed (B-CONN-8 satisfaction-gate Boolean).
        # W→E transfer fn: E's evaluation reads W's scalar state — a
        # pure read (W_state observed by E, no mutation), the mirror
        # of B-CONN-5 (W→C read-no-mutation / purity).
        "transfer_fn": "E reads W-state (pain,curiosity,satisfaction) as evaluation input — pure read, mirror B-CONN-5 W→C read-no-mutation",
        "transfer_closed": True,
        # invariant: E does not mutate W during the read (purity), AND
        # W-state ∈ bounded range [0,1]^3 (the W scalars are clamped).
        # Both closed (purity structural + Kolmogorov bounded). So B3's
        # predicate IS closed-form-definable; ⚠️ DECLARED because the
        # ascii declares W↔E bidirectional but only E→W has a B-CONN id.
        "invariant": "E read-no-mutation of W (purity, mirror B-CONN-5) ∧ W-state ∈ [0,1]^3 bounded (Kolmogorov clamp)",
        "invariant_closed": True,
        "implemented": False,
        "implemented_evidence": "HEXAD.tape §3 ascii declares W◄──►E bidirectional; only E→W closed (B-CONN-8); W→E direction has no B-CONN id — predicate definable, wire uncovered",
    },
}


def classify(arb):
    """Decidable 3-way gap-map class from closed-form arbitration.

    transfer_closed ∧ invariant_closed ∧ implemented   → A ✅ BLUE-CLOSED-WIRED
    transfer_closed ∧ invariant_closed ∧ ¬implemented  → B ⚠️ DECLARED (predicate definable, not wired)
    ¬(transfer_closed ∧ invariant_closed)              → C 🕳️ MISSING-TYPE
    """
    predicate_definable = arb["transfer_closed"] and arb["invariant_closed"]
    if not predicate_definable:
        return "C", "MISSING-TYPE"
    if arb["implemented"]:
        return "A", "BLUE-CLOSED-WIRED"
    return "B", "DECLARED-PREDICATE-DEFINABLE-NOT-WIRED"


def main():
    raw_log_path = os.path.join(HERE, "kick_raw.log")
    raw_lines = []
    kick_results = {}
    for key, seed in SEEDS.items():
        kr = run_kick(seed, ROUNDS)
        kick_results[key] = {"seed": seed, **kr}
        raw_lines.append(f"=== {key} ===")
        raw_lines.append(f"seed: {seed}")
        raw_lines.append(json.dumps(kr, ensure_ascii=False))
        raw_lines.append("")

    with open(raw_log_path, "w") as f:
        f.write("\n".join(raw_lines))

    # arbitration + gap-map classification
    rows = []
    for key in SEEDS:
        arb = ARBITRATION[key]
        cls, cls_name = classify(arb)
        prior = "🕳️ MISSING-TYPE" if key in ("#3-D-emit-to-S", "#4-E-phi-to-D-content") \
            else "⚠️ DECLARED-BUT-BROKEN"
        new = {"A": "✅ BLUE-CLOSED-WIRED",
               "B": "⚠️ DECLARED-PREDICATE-DEFINABLE-NOT-WIRED",
               "C": "🕳️ MISSING-TYPE"}[cls]
        rows.append({
            "key": key,
            "edge": arb["edge"],
            "kick_seed": SEEDS[key],
            "kick": kick_results[key],
            "transfer_fn": arb["transfer_fn"],
            "transfer_closed": arb["transfer_closed"],
            "invariant": arb["invariant"],
            "invariant_closed": arb["invariant_closed"],
            "predicate_definable": arb["transfer_closed"] and arb["invariant_closed"],
            "implemented": arb["implemented"],
            "implemented_evidence": arb["implemented_evidence"],
            "class": cls,
            "class_name": cls_name,
            "prior_class_s63": prior,
            "new_class_s89": new,
        })

    counts = {"A": 0, "B": 0, "C": 0}
    for r in rows:
        counts[r["class"]] += 1

    result = {
        "section": "§89 HEXAD-KICK-GAP-SWEEP",
        "engine": "Mk.IX (hexa 0.1.0-dispatch, real — NOT [omega-drill-stub])",
        "kick_rounds_per_seed": ROUNDS,
        "n_seeds": len(SEEDS),
        "engine_summary_only": True,
        "dump_overlay_flag_available": False,
        "counts": counts,
        "rows": rows,
        "g3": ("kick = exploratory discovery; closed-form predicate = arbiter "
               "(§69 PROPOSES/DISPOSES). closed-form-definable ≠ wired ≠ "
               "emergence. north-star + §15/§51/§72 milestone UNCHANGED."),
    }
    out_path = os.path.join(HERE, "result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"§89 HEXAD-KICK-GAP-SWEEP — {len(SEEDS)} seeds, {ROUNDS} rounds each")
    print(f"engine real Mk.IX: {all(kr.get('is_real') for kr in kick_results.values())}")
    for r in rows:
        k = r["kick"]
        print(f"  {r['key']:24s} smash{k.get('smash')}/free{k.get('free')}/"
              f"abs{k.get('abs')}/meta{k.get('meta')}/hyper{k.get('hyper')}/"
              f"res{k.get('res')} total={k.get('total')} sat={k.get('saturated')}")
        print(f"    {r['prior_class_s63']:32s} → {r['new_class_s89']}")
    print(f"counts: {counts}")
    print(f"raw log: {raw_log_path}")
    print(f"result:  {out_path}")


if __name__ == "__main__":
    main()
