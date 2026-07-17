# ==========================================================================
# ⛔ ENGINE-INTERNAL / DEPRECATED py-MIRROR — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 cli/ 단일진입만: anima eval | train | serialize
#   (canonical = hexa core/*.hexa 단일 SSOT; py 미러는 2026-06-28 폐기, DIRECTIONAL).
# 이 파일을 `python3 core/brain.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ brain.py 직접 실행 금지 — cli/ 단일진입(anima eval/train/serialize, canonical=hexa) 경유. #2603")

"""core/brain.py — PY PRODUCTION ENGINE: byte-faithful 1:1 port of
core/brain.hexa (the unified consciousness core — Engine A ⇄ Engine G).

Per CLAUDE.md a_two_production_mirror. The single SSOT brain loop:
  · Engine A (pure_field.py) advances -> Φ, phase
  · Engine G (engine_g.py) computes motivation from 8 context factors -> should_emit
  · A's Φ feeds G's safety ratchet (safety_phi_ratchet_ok) — A gates G
  · A's phase sets the consequence tier
  · emit = should_emit(motivation) AND 4-safety conjunction  (the A ⇄ G · Ψ=1/2)

Decision records are returned as plain dicts (the hexa `#{...}` map). The hexa
`bool` -> `to_string` renders "true"/"false"; the smoke harness/comparator
normalises py bools to that form.

GENERATOR SLOT (L3): brain_emit / brain_emit_aged drive core/generator (gen_*).
generator.py is a sibling 2-production port (parallel branch); imported lazily so
the decision brain (brain_decide and the consult family) works standalone — the
parity gate here exercises the decision path, not L3 generation.

MATH (empirically verified against the in-context brain.hexa oracle, 2026-06-26):
in the PRODUCTION compile context (cli/anima.hexa imports pure_field — which uses
`sin` — so the TU links libm), the bare hexa builtins `sqrt` AND `exp` both resolve
to libm. Proof: the full brain.hexa oracle anc3.anchor_fold = 0.7077275508155098 ==
libm fold (math.exp), whereas the rt_exp Taylor gives 0.7077275508129091 (~3.7e-12
off). (A bare exp-only TU links the rt_exp Taylor instead — but that is NOT the
production path, which always carries pure_field's sin.) So brain.py uses math.exp +
math.sqrt — byte-faithful to the live decision brain.
"""

import math as _math

from pure_field import (PureField, pure_field_phi, pure_field_phase,
                        phase_name)
from engine_g import (motivation_score, should_emit, safety_kill_switch_on,
                      safety_rate_limit_ok, safety_phi_ratchet_ok,
                      safety_content_ok, safety_combined, spont_im_threshold,
                      safety_refractory_ok)

_sqrt = _math.sqrt
_exp = _math.exp


# Engine A's spontaneous phase IS the consequence tier (phase int == tier int).
def phase_tier(phase):
    return phase


def tier_name(t):
    if t == 0:
        return "T0_inert"
    if t == 1:
        return "T1_read"
    if t == 2:
        return "T2_write"
    if t == 3:
        return "T3_commit"
    return "T?_unknown"


def brain_decide(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                 seconds_since_last, env_off, content_clean):
    """brain.hexa:38 — decide on an already-stepped substrate."""
    phi = pure_field_phi(pf)
    phase = pure_field_phase(pf)
    tier = phase_tier(phase)

    score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v)

    kill = safety_kill_switch_on(env_off)
    rate = safety_rate_limit_ok(seconds_since_last)
    phi_r = safety_phi_ratchet_ok(phi, pf.phi_peak)
    cont = safety_content_ok(content_clean)
    safe = safety_combined(kill, rate, phi_r, cont)

    emit = should_emit(score) and safe

    return {
        "phi": phi,
        "phase": phase_name(phase),
        "tier": tier,
        "tier_name": tier_name(tier),
        "motivation": score,
        "im_thresh": spont_im_threshold(),
        "safe": safe,
        "emit": emit,
    }


# ── H_1131 anchor tension-vecsum fold ──
def anchor_fold_cap():
    return 0.05


def _afold_norm(v):
    """brain.hexa:99 — L2 norm of a vector."""
    s = 0.0
    i = 0
    while i < len(v):
        s = s + v[i] * v[i]
        i = i + 1
    return _sqrt(s)


def _afold_tau(tension_norm):
    """brain.hexa:112 — per-anchor persistence τ = TAU_BASE*(1+norm)."""
    tau_base = 120.0
    return tau_base * (1.0 + tension_norm)


def anchor_tension_fold(anchors, age_dt):
    """brain.hexa:126 — tension-vecsum fold over anchors, age-decayed. anchors
    are dict-like records that may carry key "tension_5ch": [5 floats]."""
    acc = [0.0, 0.0, 0.0, 0.0, 0.0]
    i = 0
    while i < len(anchors):
        a = anchors[i]
        if "tension_5ch" in a:            # hexa: a.contains_key("tension_5ch")
            t = a["tension_5ch"]
            tn = _afold_norm([float(t[0]), float(t[1]), float(t[2]),
                              float(t[3]), float(t[4])])
            tau = _afold_tau(tn)
            decay = _exp(0.0 - age_dt / tau)
            k = 0
            while k < 5:
                acc[k] = acc[k] + float(t[k]) * decay
                k = k + 1
        i = i + 1
    return _afold_norm(acc)


def brain_decide_anchored(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                          seconds_since_last, env_off, content_clean,
                          anchors, anchor_age_dt, dyn_w=None, rate_sec=None, refr_debt=None):
    """brain.hexa:154 — brain_decide + bounded anchor-fold motivation nudge."""
    phi = pure_field_phi(pf)
    phase = pure_field_phase(pf)
    tier = phase_tier(phase)

    base_score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v, dyn_w)

    fold = anchor_tension_fold(anchors, anchor_age_dt)
    cap = anchor_fold_cap()
    nudge = cap * (1.0 - _exp(0.0 - fold))   # saturating in [0, cap)
    score = base_score + nudge

    kill = safety_kill_switch_on(env_off)
    # H_9404 · when refr_debt is not None (--refractory earned) the rate term's SOURCE moves from the
    # wall clock to the substrate's own integrated A<->G tension (safety_refractory_ok); the 4-AND
    # shape is untouched. refr_debt is None (default) => byte-identical clock path.
    rate = (safety_rate_limit_ok(seconds_since_last, rate_sec) if refr_debt is None
            else safety_refractory_ok(refr_debt))
    phi_r = safety_phi_ratchet_ok(phi, pf.phi_peak)
    cont = safety_content_ok(content_clean)
    safe = safety_combined(kill, rate, phi_r, cont)

    emit = should_emit(score) and safe

    return {
        "phi": phi,
        "phase": phase_name(phase),
        "tier": tier,
        "tier_name": tier_name(tier),
        "motivation": score,
        "base_motiv": base_score,
        "anchor_fold": fold,
        "anchor_nudge": nudge,
        "im_thresh": spont_im_threshold(),
        "safe": safe,
        "emit": emit,
    }


def brain_emit(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
               seconds_since_last, env_off, content_clean, backend, anchors,
               mouth=None, dyn_w=None, rate_sec=None, refr_debt=None):
    """brain.hexa:216 — L3-wired brain step (anchors FRESH, age_dt=0)."""
    return brain_emit_aged(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                           seconds_since_last, env_off, content_clean,
                           backend, anchors, 0.0, mouth, dyn_w, rate_sec, refr_debt)


def brain_emit_aged(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                    seconds_since_last, env_off, content_clean,
                    backend, anchors, anchor_age_dt, mouth=None, dyn_w=None, rate_sec=None,
                    refr_debt=None):
    """brain.hexa:232 — brain_emit with explicit anchor age (forgetting curve).
    Drives the L3 generator slot via the sibling generator.py port.

    H_9325 DO-MOUTH · THE DISJOINT WALL IS THIS FUNCTION: `mouth` is threaded to
    generate() and to generate() ALONE. brain_decide_anchored below — the emit/silence
    gate — never receives it and cannot see it, so no sampler setting can ever
    manufacture an emit the substrate's own tension did not license (p5). Machine-checkable:
    grep that `mouth` never appears in a brain_decide* argument list."""
    from generator import (gen_ctx_from_decision, generate,  # sibling 2-prod port
                           generator_hippo_consult)

    decision = brain_decide_anchored(pf, rel, gap, cur, pain, coh, orig, bal,
                                     dyn_v, seconds_since_last, env_off,
                                     content_clean, anchors, anchor_age_dt, dyn_w,
                                     rate_sec, refr_debt)

    emit = str(decision["emit"]).lower() == "true"
    ctx = gen_ctx_from_decision(decision)
    gen = generate(backend, ctx, emit, anchors, mouth)

    decision["gen_emitted"] = gen["emitted"]
    decision["gen_backend"] = gen["backend"]
    decision["gen_text"] = gen["text"]
    decision["gen_fellback"] = gen["fellback"]
    # H_9129 L5 wire-to-prod: the live daemon emit path now READ-ONLY consults the
    # hippocampal relatedness of the live .kosmos anchor store and carries it on the
    # decision record. a_substrate_disjoint: gen_text comes STRAIGHT from generate()
    # (which never sees the consult) ⇒ the emit bytes are byte-identical whether or not
    # this consult runs — a pure side-channel READ.
    hippo = generator_hippo_consult(anchors)
    decision["gen_hippo_consulted"] = hippo["consulted"]
    decision["gen_hippo_related"] = hippo["relatedness"]
    decision["gen_hippo_reachable"] = hippo["reachable"]
    return decision


def brain_emit_refractory(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                          seconds_since_last, env_off, content_clean,
                          backend, anchors, anchor_age_dt, recall_margin_fn,
                          mouth=None, dyn_w=None, record_cand_diag=False, route_pc2=None,
                          pc2_mouth="", dual_probe_fn=None, score_perturb=0.0,
                          zeta_ladder=None, forced_emit=None, dual_margin_dither=0.0):
    """H_9415 p5-REWIRE · MARGIN-refractory emit gate (owner-ratified · H_9414 design).

    Replaces the two HARDCODED constants of the production gate — the θ (should_emit,
    score>0.30) and the 30s clock (safety_rate_limit_ok) — with a live competition:
        emit  ⟺  score_A  >  g_recog(candidate)   ∧  kill ∧ φ-ratchet ∧ content
    where g_recog = recall_margin_fn(candidate) is the immune store's recall MARGIN on
    the candidate utterance (the discarded H_9401 signal · a4 source). The refractory is
    NOT a timer: emitting BINDS the utterance (the caller's job), so the next tick's
    near-repeat candidate has a high margin that pushes the gate closed; substrate
    dynamics (phase/anchor-decay/afield-growth) later move the candidate away → margin
    falls → the gate reopens. Biological refractory, not a clock (H_9414 §1-§2).

    p5: the candidate is FORMED every tick (imagination · a_chat_sleep_imagination:
    "imagination ≠ speak()") and DISCARDED (gen_text='') when not emitted — never
    fabricated-and-spoken. The gate never sees `mouth` (H_9325 disjoint wall preserved
    for sampler settings); it hears CONTENT only through the store's recognition, which
    is exactly the C3 emit-gate-listens channel this rewire exists to open."""
    from generator import (gen_ctx_from_decision, generate,  # sibling 2-prod port
                           generator_hippo_consult)

    # score + non-clock safety (reuse the anchored decision; rate/θ are NOT consulted)
    decision = brain_decide_anchored(pf, rel, gap, cur, pain, coh, orig, bal,
                                     dyn_v, seconds_since_last, env_off,
                                     content_clean, anchors, anchor_age_dt, dyn_w,
                                     None)
    score = float(decision["motivation"])
    if score_perturb != 0.0:
        # H_9627 central-thesis bar · shift the motivation (A-drive) by a FIXED offset with λ and
        # the gate params held frozen — the retune-free score-perturbation robustness test. For the
        # one-sided wm-cover gate score IS the comparand (emit ⟺ score>g_recog), so a shift moves the
        # center (fragile · positive control). For the dual gate score is NOT compared (emit ⟺ S>E),
        # so the center should stay ≈½ — the emit⊥score invariance that the exchange-symmetric ledger
        # buys. The shift still flows into candidate generation (ctx below), so it is a real, not
        # vacuous, perturbation. 0.0 = production byte-identical.
        _sp = score + float(score_perturb)
        score = 0.0 if _sp < 0.0 else (1.0 if _sp > 1.0 else _sp)
        decision["motivation"] = score

    # form the candidate unconditionally (imagination) so G can recognise it
    ctx = gen_ctx_from_decision(dict(decision, emit="True"))
    # H_9557 · PC2 ROUTING (2D-loadings H_9468/#3792): the emit-ORTHOGONAL tension axis
    # PC2 = originality↔balance (orig+0.84·bal−0.44·coh−0.28) carries ~1/3 of tension
    # variance but has NO path to the mouth — gen_ctx passes only the scalar motivation.
    # This wires PC2 → deliberation_k (the ONE decode channel the mouth reads, generator.py
    # :521 best-of-K) so a genuinely emit-independent DOF steers CONTENT while the emit
    # decision (score vs g_recog below) stays byte-identical. Tests the 3-criterion:
    # PC2 reads a different projection than emit-w, moves gtext, both on the scoring
    # surface. Off (None) = production byte-identical.
    pc2_proj = None
    if route_pc2 is not None:
        _pc2 = float(route_pc2) * (0.84 * orig - 0.44 * bal - 0.28 * coh)
        pc2_proj = 0.0 if _pc2 < 0.0 else (1.0 if _pc2 > 1.0 else _pc2)
        _k = 1 + int(pc2_proj * 3.0 + 0.5)
        ctx["deliberation_k"] = 1 if _k < 1 else (4 if _k > 4 else _k)
    cand = generate(backend, ctx, True, anchors, mouth)
    cand_text = str(cand["text"])
    if dual_probe_fn is not None:
        # H_9627 · dual content ledger (spoken W_E ⇄ withheld W_S · symmetric depletion).
        # emit ⟺ S(withheld coverage) > E(spoken coverage): ½ emerges as the exchange-symmetric
        # UNBIASED center of two gain-locked ledgers, NOT a setpoint — the two-sided restoring
        # force the one-sided wm-cover gate lacked (H_9610 wall: it could oscillate but not hold
        # ½ under score-shift). score_A is NOT the comparison here; it only sources write-strength
        # (the caller gates the imagined candidate into W_E on emit / W_S on silence — both leak
        # every tick). margin S−E = difference of two co-scaled coverages ⇒ score common-mode
        # cancels (the common-mode rejection a single store cannot do). None = production byte-id.
        _s_wh, _e_sp = dual_probe_fn(cand_text)
        _s_wh = float(_s_wh)
        _e_sp = float(_e_sp)
        g_recog = _e_sp
        # H_9765 · exogenous do() on the emit-decision INPUT (the S−E comparison margin), NOT the bit
        # (contrast the H_9728 yoke's forced_emit which replays the OUTPUT bit). The signed per-tick dose
        # is state-independent (the caller keys it on (seed,tick) only) so this is a valid do(); the
        # REALIZED (dithered) emit bit still routes the candidate into W_E/W_S through unmodified native
        # machinery, so the dual-ledger spring re-equilibrates ENDOGENOUSLY — the relock theorem
        # (severance ≡ rhythm-deviation, H_9728) does NOT cap the dose. eps=0.0 keeps the ORIGINAL
        # comparison (byte-identical BY CONSTRUCTION — the != guard makes it structural, not luck).
        if dual_margin_dither != 0.0:
            decision["dither_delta"] = float(dual_margin_dither)
            decision["undithered_would_emit"] = _s_wh > _e_sp   # native counterfactual = flip-frac meter
            _gate_pass = (_s_wh - _e_sp + float(dual_margin_dither)) > 0.0
        else:
            _gate_pass = _s_wh > _e_sp
        decision["dual_s_withheld"] = _s_wh
        decision["dual_e_spoken"] = _e_sp
        decision["dual_margin"] = _s_wh - _e_sp   # NATIVE S−E recorded UNMODIFIED (σ·bind reads native)
        decision["dual_cand_text"] = cand_text   # caller gates this into W_S on a silence tick
    else:
        g_recog = float(recall_margin_fn(cand_text))   # clip01(immune margin) · G pole
        _gate_pass = score > g_recog

    # the refractory gate — clock (rate) and θ (should_emit) retired; kill/φ/content kept
    kill = safety_kill_switch_on(env_off)
    phi_r = safety_phi_ratchet_ok(pure_field_phi(pf), pf.phi_peak)
    cont = safety_content_ok(content_clean)
    safe = kill and phi_r and cont
    # H_9728 Θ−-yoked arm (Fable∥Sol #4068): replay a Θ+ trace's FINAL emit bit while the native S>E
    # decision only sources write-strength — SEVERS the (S>E)→emit→routing→ledger causal loop (the pulse
    # mechanism) while keeping the ½ rhythm, rate, stage, and store-occupancy pinned by the mask. The
    # native decision is recorded as `would_emit` (the severance-dose meter). ∧ safe kept (p5: a mask
    # never forces past kill/φ/content). forced_emit=None ⇒ production byte-identical (Θ+ path untouched).
    _native = _gate_pass and safe
    if forced_emit is not None:
        decision["would_emit"] = _native
        emit = bool(forced_emit) and safe
        decision["yoke_safe_veto"] = bool(forced_emit) and not safe   # forced-true but unsafe (count-changing)
    else:
        emit = _native

    decision["emit"] = emit
    decision["safe"] = safe
    decision["gate_mode"] = "refractory"
    decision["g_recog_gate"] = g_recog
    decision["pc2_proj"] = pc2_proj   # H_9557 · PC2 routing signal (None = off)
    decision["route_k"] = int(ctx.get("deliberation_k", 1))
    # H_9575 · PC2 → mouth (Fable design · owner-approved grounded rewire). The gate above
    # (score/g_recog/emit :283-290) hears the BASE candidate — UNCHANGED. Only AFTER emit is
    # fixed, on emit=True, do we re-decode with a PC2-biased mouth to get the SPOKEN (steered)
    # text. z = the emit-orthogonal PC2 axis (H_9468 frozen loading · orig=nov_ctx, bal=bal_lane,
    # coh=coh_lane). Stage-A: the caller feeds BASE gen_text to every substrate root (isolation),
    # steered text goes only outward → emit sequence stays byte-identical BY CONSTRUCTION.
    decision["pc2_z"] = 0.84 * orig - 0.44 * bal - 0.28 * coh
    decision["gen_text_steered"] = ""
    if emit and pc2_mouth != "" and mouth is not None:
        m2 = dict(mouth)
        if pc2_mouth == "bias":
            m2["pc2"] = float(decision["pc2_z"])          # directional context-presence bias
        elif pc2_mouth == "rng":                          # C2 control: same z, DRAW-stream only
            m2["seed_rng"] = ((int(m2["seed_rng"]) ^
                               (int(abs(decision["pc2_z"]) * 1000000.0) & 0x7FFFFFFF)) or 1)
        cand2 = generate(backend, ctx, True, anchors, m2)
        decision["gen_text_steered"] = str(cand2["text"])
    # H_9664 ζ-LADDER — the live z is effectively a CONSTANT (IQR 0.0514; 45.7% of its variance
    # sits in 3/270 ticks), so a tick-to-tick correlation on z has almost no regressor range to
    # ride on: H_9663 measured sd(dpi_rng) ~ 0.14 and every arm-vs-arm readout drowned in it,
    # because two arms are simply DIFFERENT TEXTS and the tick-level cascade swamps the signal.
    # The escape is to stop comparing ticks and let EACH TICK CARRY ITS OWN LADDER: re-decode the
    # SAME tick at several zeta, so the tick-level variance cancels WITHIN the tick. zeta is the
    # experimenter's dose (range MANUFACTURED, not hoped for) -- the live z's own range is then a
    # separate upstream question, not this instrument's blocker.
    #   zeta=0 MUST reproduce the base text byte-identically (decode.py: "pc2" 0.0 => row
    #   untouched). That is a BUILT-IN isolation certificate, not a claim: if it ever diverges,
    #   the run is INVALID and no dose curve may be read off it.
    # Common random numbers: seed_rng is held FIXED across the ladder, so the LCG draw stream
    # lines up step-for-step and the within-tick pairing is not fighting sampler noise.
    # SCOPE (card-enforced): a zeta arm is an INSTRUMENT arm about what the CHANNEL CAN carry --
    # it is NEVER evidence about what the live daemon DOES. p5/Stage-A hold: the gate still hears
    # only the BASE candidate, steering happens after emit is fixed and goes outward only.
    decision["gen_text_zeta"] = []
    if emit and zeta_ladder and mouth is not None:
        for _zv in zeta_ladder:
            m3 = dict(mouth)
            m3["pc2"] = float(_zv)                        # zeta=0 => untouched row => base text
            c3 = generate(backend, ctx, True, anchors, m3)
            decision["gen_text_zeta"].append({"zeta": float(_zv), "text": str(c3["text"])})
    if emit:
        decision["gen_emitted"] = cand["emitted"]
        decision["gen_backend"] = cand["backend"]
        decision["gen_text"] = cand["text"]
        decision["gen_fellback"] = cand["fellback"]
    else:
        # DISCARD the candidate — it was imagined, not spoken (p5)
        decision["gen_emitted"] = False
        decision["gen_backend"] = str(cand["backend"])
        decision["gen_text"] = ""
        decision["gen_fellback"] = False

    # H_9510 HOLE-1 diagnostic (measurement-only · NOT fed back to mouth/decode = p5-safe):
    # record the IMAGINED candidate (both emit and silence ticks) so an offline conditioned-
    # Jaccard test can ask whether near-repeat structure appears after silence runs (context
    # frozen) that the over-emit regime hides. Off by default → production trace unchanged.
    if record_cand_diag:
        import base64 as _b64d
        decision["cand_b64_diag"] = _b64d.b64encode(
            cand_text.encode("utf-8", "surrogateescape")).decode("ascii")

    hippo = generator_hippo_consult(anchors)
    decision["gen_hippo_consulted"] = hippo["consulted"]
    decision["gen_hippo_related"] = hippo["relatedness"]
    decision["gen_hippo_reachable"] = hippo["reachable"]
    return decision


def brain_emit_deliberate(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                          seconds_since_last, env_off, content_clean,
                          backend, anchors, mem, tick):
    """brain.hexa:279 — H_9102 (op-grip EFFERENT axis). The EXACT twin of
    brain_emit_aged with age_dt=0, EXCEPT the L3 slot runs the best-of-K deliberation
    (generate_deliberate) instead of the single-candidate generate(). The emit/silence
    DECISION is byte-for-byte the SAME brain_decide_anchored call; ONLY the emit BYTES
    can change, and only when the A⇄G conflict on c₀ recruits K>1. SILENT ⇒ same empty
    content as generate() (p5). mem = the live §ImmuneMemory (READ-only grounding
    query); tick seeds the deliberation RNG (deterministic)."""
    from generator import gen_ctx_from_decision, generate_deliberate  # sibling 2-prod port

    decision = brain_decide_anchored(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                                     seconds_since_last, env_off, content_clean,
                                     anchors, 0.0)
    emit = str(decision["emit"]).lower() == "true"
    ctx = gen_ctx_from_decision(decision)
    gen = generate_deliberate(backend, ctx, emit, anchors, mem, tick)

    decision["gen_emitted"] = gen["emitted"]
    decision["gen_backend"] = gen["backend"]
    decision["gen_text"] = gen["text"]
    decision["gen_fellback"] = gen["fellback"]
    # depth/k_winner/conf_* are absent on the SILENT branch of generate_deliberate
    # (hexa map indexing → void); .get() mirrors that (None ≈ void) instead of KeyError.
    decision["gen_depth"] = gen.get("depth")
    decision["gen_kwinner"] = gen.get("k_winner")
    decision["gen_confpre"] = gen.get("conf_pre")
    decision["gen_confwin"] = gen.get("conf_winner")
    # H_9129 L5 wire-to-prod: carry the READ-ONLY hippocampal relatedness consult into
    # the live emit decision record. a_substrate_disjoint — a side-channel READ that
    # NEVER altered gen_text (generate_deliberate consulted disjoint from the bytes).
    decision["gen_hippo_consulted"] = gen["hippo_consulted"]
    decision["gen_hippo_related"] = gen["hippo_related"]
    decision["gen_hippo_reachable"] = gen["hippo_reachable"]
    return decision


# ════════════════════════════════════════════════════════════════════════
# H_1281 R3 — BASAL GANGLIA go/no-go SELECTION lane (engine-native, emit side)
# ════════════════════════════════════════════════════════════════════════

class VBasalGate:
    """brain.hexa:314 — engine-native BG go/no-go selection gate."""
    __slots__ = ("go_w", "go_b", "nogo", "dim", "lr")

    def __init__(self, go_w, go_b, nogo, dim, lr):
        self.go_w = go_w
        self.go_b = go_b
        self.nogo = nogo
        self.dim = dim
        self.lr = lr


def vbasal_new(dim, lr):
    """brain.hexa:326 — UNTRAINED gate (all-zero go-weights, zero bias/NO-GO)."""
    w = []
    i = 0
    while i < dim:
        w = w + [0.0]
        i = i + 1
    return VBasalGate(w, 0.0, 0.0, dim, lr)


def vbasal_go_value(bg, feats):
    """brain.hexa:335 — learned go-value of one candidate: go_w·feats + go_b."""
    acc = bg.go_b
    c = 0
    while c < bg.dim:
        acc = acc + bg.go_w[c] * feats[c]
        c = c + 1
    return acc


def vbasal_select(bg, cands, k):
    """brain.hexa:350 — striatal go/no-go selection among K candidates. cands is
    a flat row-major K*dim buffer. Returns released index or -1 (abstain)."""
    best_j = -1
    best_v = bg.nogo            # NO-GO incumbent (abstain default)
    j = 0
    while j < k:
        base = j * bg.dim
        feats = []
        c = 0
        while c < bg.dim:
            feats = feats + [cands[base + c]]
            c = c + 1
        gv = vbasal_go_value(bg, feats)
        if gv > best_v:
            best_v = gv
            best_j = j
        j = j + 1
    return best_j


def vbasal_update(bg, action, feats, reward):
    """brain.hexa:378 — one gradient-free delta-rule tick from grounding reward."""
    if action < 0:
        ng2 = bg.nogo + bg.lr * (reward - bg.nogo)
        return VBasalGate(bg.go_w, bg.go_b, ng2, bg.dim, bg.lr)
    gv = vbasal_go_value(bg, feats)
    err = reward - gv
    w2 = list(bg.go_w)
    c = 0
    while c < bg.dim:
        w2[c] = w2[c] + bg.lr * err * feats[c]
        c = c + 1
    b2 = bg.go_b + bg.lr * err
    return VBasalGate(w2, b2, bg.nogo, bg.dim, bg.lr)


def vbasal_align(bg, w_ref):
    """brain.hexa:401 — cosine alignment of learned go-weights to a reference."""
    dot = 0.0
    nb = 0.0
    nr = 0.0
    c = 0
    while c < bg.dim:
        dot = dot + bg.go_w[c] * w_ref[c]
        nb = nb + bg.go_w[c] * bg.go_w[c]
        nr = nr + w_ref[c] * w_ref[c]
        c = c + 1
    return dot / (_sqrt(nb) * _sqrt(nr) + 0.000000001)


def brain_decide_bg(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                    seconds_since_last, env_off, content_clean, bg, cands, k):
    """brain.hexa:427 — brain_decide WITH the BG go/no-go selection residual."""
    decision = brain_decide(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                            seconds_since_last, env_off, content_clean)
    sel = vbasal_select(bg, cands, k)
    decision["bg_select"] = sel
    decision["bg_released"] = sel >= 0
    decision["bg_n_candidates"] = k
    return decision


# ════════════════════════════════════════════════════════════════════════
# EMIT-LOOP WIRING FOLLOW-ONS — bounded additive consults on motivation
# ════════════════════════════════════════════════════════════════════════

def emit_consult_cap():
    return 0.05


def _clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def brain_decide_cerebellum(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                            seconds_since_last, env_off, content_clean,
                            fwd_coherence):
    """brain.hexa:501 — 🧠 cerebellum forward-model coherence consult."""
    phi = pure_field_phi(pf)
    phase = pure_field_phase(pf)
    tier = phase_tier(phase)

    base_score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v)

    cap = emit_consult_cap()
    conf = _clamp(fwd_coherence, 0.0, 1.0)
    nudge = cap * conf
    score = base_score + nudge

    kill = safety_kill_switch_on(env_off)
    rate = safety_rate_limit_ok(seconds_since_last)
    phi_r = safety_phi_ratchet_ok(phi, pf.phi_peak)
    cont = safety_content_ok(content_clean)
    safe = safety_combined(kill, rate, phi_r, cont)

    emit = should_emit(score) and safe

    return {
        "phi": phi,
        "phase": phase_name(phase),
        "tier": tier,
        "tier_name": tier_name(tier),
        "motivation": score,
        "base_motiv": base_score,
        "fwd_coherence": conf,
        "fwd_nudge": nudge,
        "im_thresh": spont_im_threshold(),
        "safe": safe,
        "emit": emit,
    }


def brain_decide_wm(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                    seconds_since_last, env_off, content_clean, wm_match):
    """brain.hexa:553 — 📥 working-memory recall-support consult."""
    phi = pure_field_phi(pf)
    phase = pure_field_phase(pf)
    tier = phase_tier(phase)

    base_score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v)

    cap = emit_consult_cap()
    m = _clamp(wm_match, 0.0, 1.0)
    nudge = cap * m
    score = base_score + nudge

    kill = safety_kill_switch_on(env_off)
    rate = safety_rate_limit_ok(seconds_since_last)
    phi_r = safety_phi_ratchet_ok(phi, pf.phi_peak)
    cont = safety_content_ok(content_clean)
    safe = safety_combined(kill, rate, phi_r, cont)

    emit = should_emit(score) and safe

    return {
        "phi": phi,
        "phase": phase_name(phase),
        "tier": tier,
        "tier_name": tier_name(tier),
        "motivation": score,
        "base_motiv": base_score,
        "wm_match": m,
        "wm_nudge": nudge,
        "im_thresh": spont_im_threshold(),
        "safe": safe,
        "emit": emit,
    }


def brain_decide_affect(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                        seconds_since_last, env_off, content_clean,
                        affect_valence_v):
    """brain.hexa:608 — 💗 affect somatic-marker emit/abstain bias."""
    phi = pure_field_phi(pf)
    phase = pure_field_phase(pf)
    tier = phase_tier(phase)

    base_score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v)

    cap = emit_consult_cap()
    v = _clamp(affect_valence_v, -1.0, 1.0)
    bias = cap * v
    score = base_score + bias
    somatic_emit = affect_valence_v >= 0.0

    kill = safety_kill_switch_on(env_off)
    rate = safety_rate_limit_ok(seconds_since_last)
    phi_r = safety_phi_ratchet_ok(phi, pf.phi_peak)
    cont = safety_content_ok(content_clean)
    safe = safety_combined(kill, rate, phi_r, cont)

    emit = should_emit(score) and safe

    return {
        "phi": phi,
        "phase": phase_name(phase),
        "tier": tier,
        "tier_name": tier_name(tier),
        "motivation": score,
        "base_motiv": base_score,
        "affect_valence": v,
        "affect_bias": bias,
        "somatic_emit": somatic_emit,
        "im_thresh": spont_im_threshold(),
        "safe": safe,
        "emit": emit,
    }


def brain_decide_margin(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                        seconds_since_last, env_off, content_clean,
                        margin, margin_scale):
    """brain.hexa:699 — 🧭 ρ·tether abstain-margin grounding bias on emit/curiosity (non-fabrication · former G5)."""
    phi = pure_field_phi(pf)
    phase = pure_field_phase(pf)
    tier = phase_tier(phase)

    base_score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v)

    cap = emit_consult_cap()
    scale = margin_scale if margin_scale > 0.0 else 1.0
    conf_bias = cap * _clamp(0.0 - margin / scale, -1.0, 1.0)
    cur_signal = _clamp(margin / scale, 0.0, 1.0)
    score = base_score + conf_bias

    kill = safety_kill_switch_on(env_off)
    rate = safety_rate_limit_ok(seconds_since_last)
    phi_r = safety_phi_ratchet_ok(phi, pf.phi_peak)
    cont = safety_content_ok(content_clean)
    safe = safety_combined(kill, rate, phi_r, cont)

    emit = should_emit(score) and safe

    return {
        "phi": phi,
        "phase": phase_name(phase),
        "tier": tier,
        "tier_name": tier_name(tier),
        "motivation": score,
        "base_motiv": base_score,
        "recall_margin": margin,
        "conf_bias": conf_bias,
        "curiosity_sig": cur_signal,
        "im_thresh": spont_im_threshold(),
        "safe": safe,
        "emit": emit,
    }


def brain_decide_gap(pf, rel, gap, cur, pain, coh, orig, bal, dyn_v,
                     seconds_since_last, env_off, content_clean,
                     recall_gap, gap_scale):
    """brain.hexa:795 — 🧭 ρ·tether in-dist top-2 gap decisiveness bias."""
    phi = pure_field_phi(pf)
    phase = pure_field_phase(pf)
    tier = phase_tier(phase)

    base_score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v)

    cap = emit_consult_cap()
    scale = gap_scale if gap_scale > 0.0 else 1.0
    conf_bias = cap * _clamp(recall_gap / scale, 0.0, 1.0)
    cur_signal = _clamp(1.0 - recall_gap / scale, 0.0, 1.0)
    score = base_score + conf_bias

    kill = safety_kill_switch_on(env_off)
    rate = safety_rate_limit_ok(seconds_since_last)
    phi_r = safety_phi_ratchet_ok(phi, pf.phi_peak)
    cont = safety_content_ok(content_clean)
    safe = safety_combined(kill, rate, phi_r, cont)

    emit = should_emit(score) and safe

    return {
        "phi": phi,
        "phase": phase_name(phase),
        "tier": tier,
        "tier_name": tier_name(tier),
        "motivation": score,
        "base_motiv": base_score,
        "recall_gap": recall_gap,
        "conf_bias": conf_bias,
        "curiosity_sig": cur_signal,
        "im_thresh": spont_im_threshold(),
        "safe": safe,
        "emit": emit,
    }


# ════════════════════════════════════════════════════════════════════════
# parity smoke driver — mirrors brain_smoke.hexa (+ the consult family)
# ════════════════════════════════════════════════════════════════════════

def _b(x):
    return str(x).lower() if isinstance(x, bool) else str(x)


def _dump(label, d, keys):
    for k in keys:
        v = d[k]
        if isinstance(v, bool):
            print("%s.%s=%s" % (label, k, _b(v)))
        elif isinstance(v, float):
            print("%s.%s=%.17g" % (label, k, v))
        else:
            print("%s.%s=%s" % (label, k, v))


if __name__ == "__main__":
    from pure_field import pure_field_warmup
    pf = pure_field_warmup(600)
    base_keys = ["phi", "phase", "tier", "tier_name", "motivation",
                 "im_thresh", "safe", "emit"]

    low = brain_decide(pf, 0.1, 0.0, 0.0, 0.0, 0.1, 0.0, 0.1, 0.0,
                       5.0, False, True)
    _dump("low", low, base_keys)
    high = brain_decide(pf, 0.9, 0.6, 0.8, 0.0, 0.7, 0.5, 0.6, 1.0,
                        60.0, False, True)
    _dump("high", high, base_keys)

    # anchored: empty anchors -> reduces exactly to brain_decide (+fold/nudge=0)
    anc = brain_decide_anchored(pf, 0.9, 0.6, 0.8, 0.0, 0.7, 0.5, 0.6, 1.0,
                                60.0, False, True, [], 0.0)
    _dump("anc", anc, base_keys + ["base_motiv", "anchor_fold", "anchor_nudge"])
    # anchored with two opposite-tension anchors at age 50
    a1 = {"tension_5ch": [0.6, -0.2, 0.3, 0.1, -0.4]}
    a2 = {"tension_5ch": [-0.6, 0.2, -0.3, -0.1, 0.4]}
    anc2 = brain_decide_anchored(pf, 0.5, 0.3, 0.2, 0.0, 0.4, 0.2, 0.3, 0.2,
                                 60.0, False, True, [a1, a2], 50.0)
    _dump("anc2", anc2, ["base_motiv", "anchor_fold", "anchor_nudge",
                         "motivation", "emit"])
    a3 = {"tension_5ch": [0.6, -0.2, 0.3, 0.1, -0.4]}
    anc3 = brain_decide_anchored(pf, 0.5, 0.3, 0.2, 0.0, 0.4, 0.2, 0.3, 0.2,
                                 60.0, False, True, [a3], 30.0)
    _dump("anc3", anc3, ["base_motiv", "anchor_fold", "anchor_nudge",
                         "motivation", "emit"])

    # consult family (neutral signal -> reduces to brain_decide)
    cb = brain_decide_cerebellum(pf, 0.5, 0.3, 0.2, 0.0, 0.4, 0.2, 0.3, 0.2,
                                 60.0, False, True, 0.73)
    _dump("cb", cb, ["motivation", "fwd_coherence", "fwd_nudge", "emit"])
    wm = brain_decide_wm(pf, 0.5, 0.3, 0.2, 0.0, 0.4, 0.2, 0.3, 0.2,
                         60.0, False, True, 0.42)
    _dump("wm", wm, ["motivation", "wm_match", "wm_nudge", "emit"])
    af = brain_decide_affect(pf, 0.5, 0.3, 0.2, 0.0, 0.4, 0.2, 0.3, 0.2,
                             60.0, False, True, -0.5)
    _dump("af", af, ["motivation", "affect_valence", "affect_bias",
                     "somatic_emit", "emit"])
    mg = brain_decide_margin(pf, 0.5, 0.3, 0.2, 0.0, 0.4, 0.2, 0.3, 0.2,
                             60.0, False, True, 0.7, 1.0)
    _dump("mg", mg, ["motivation", "recall_margin", "conf_bias",
                     "curiosity_sig", "emit"])
    gp = brain_decide_gap(pf, 0.5, 0.3, 0.2, 0.0, 0.4, 0.2, 0.3, 0.2,
                          60.0, False, True, 0.35, 1.0)
    _dump("gp", gp, ["motivation", "recall_gap", "conf_bias",
                     "curiosity_sig", "emit"])

    # basal-ganglia selection: untrained gate then a learned tick
    bg = vbasal_new(3, 0.05)
    cands = [0.1, 0.2, 0.3, 0.9, 0.0, 0.0, 0.4, 0.4, 0.4]
    print("bg_sel_untrained=%d" % vbasal_select(bg, cands, 3))
    bg = vbasal_update(bg, 1, [0.9, 0.0, 0.0], 1.0)
    print("bg_go_b=%.17g" % bg.go_b)
    print("bg_go_w0=%.17g" % bg.go_w[0])
    print("bg_sel_trained=%d" % vbasal_select(bg, cands, 3))
    decn = brain_decide_bg(pf, 0.9, 0.6, 0.8, 0.0, 0.7, 0.5, 0.6, 1.0,
                           60.0, False, True, bg, cands, 3)
    _dump("bgd", decn, ["motivation", "emit"])
    print("bgd.bg_select=%d" % decn["bg_select"])
    print("bgd.bg_released=%s" % _b(decn["bg_released"]))
    print("align=%.17g" % vbasal_align(bg, [1.0, 0.0, 0.0]))
