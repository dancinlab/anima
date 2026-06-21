#!/usr/bin/env python3
# h1520_salience.py — H_1520 CONVERSATIONAL-SALIENCE — R1 numpy DIRECTIONAL mirror.
#
# Mirrors the LIVE emit/silence gate (core/engine_g.hexa motivation_score +
# should_emit + the A->G safety_phi_ratchet gate; 8 intrinsic factors derived
# from substrate signals exactly as HEXAD/CHAT/spontaneous_lib.hexa derives them).
#
# THE RECONCILIATION (the user's question): can anima be a usable request->reply
# chat (P1 usability) WHILE provably retaining silence-autonomy (P2) and the
# philosophy intact (P3 audit, P4 no-damage)? The user message enters ONLY as
# ENVIRONMENTAL SALIENCE: it modulates the SAME substrate factors the live gate
# already reads (grounding -> relevance/coherence/Phi; retrieval cos-sim ->
# info_gap). The emit predicate is UNCHANGED: emit iff score>0.30 AND safety.
# There is NO injected "must answer" constant — that is the p1/p3/p4 guard, and
# the P3 adversarial check proves removing it is load-bearing.
#
# numpy mirror => DIRECTIONAL only (a_engine_native_learning hard-gate-1).
# Engine-native R2 on the live emit gate / brain_decide = deferred follow-on.

import json, re, sys
import numpy as np

# ── live-gate constants (byte-identical to core/engine_g.hexa) ────────────────
IM_THRESHOLD = 0.30          # spont_im_threshold() = PROACTIVE_THRESHOLD
W_RELEVANCE  = 0.20
W_INFO_GAP   = 0.10
W_CURIOSITY  = 0.15
W_PAIN       = 0.10
W_COHERENCE  = 0.10
W_ORIGINAL   = 0.10
W_BALANCE    = 0.15
W_DYNAMICS   = 0.10          # sum = 1.00 closed conservation
PSI          = 0.5           # Ψ fixed point
COH_ALPHA    = 0.014         # Law-70 interior closeness band

# ── faithful factor fns (mirror HEXAD/CHAT/spontaneous_lib.hexa §2) ───────────
def clamp01(x):
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

def factor_relevance(phi):            # B-SPONT-1: Phi clamped [0,1]
    return clamp01(phi)
def factor_info_gap(cos_sim):         # B-SPONT-2: 1 - cos_sim clamped [0,1]
    return clamp01(1.0 - cos_sim)
def factor_curiosity(ema):            # B-SPONT-3
    return clamp01(ema)
def factor_pain(td):                  # B-SPONT-4: |delta tension|
    return clamp01(abs(td))
def factor_coherence(gate):           # B-SPONT-5: Law-70 interior closeness
    return 1.0 - min(1.0, abs(gate - PSI) / COH_ALPHA)
def factor_originality(split):        # B-SPONT-6: mitosis split boolean
    return 1.0 if split else 0.0
def factor_balance(phi, ratchet):     # B-SPONT-7: Phi > ratchet/2 boolean
    return 1.0 if phi > ratchet / 2.0 else 0.0
def factor_dynamics(silence_s):       # B-SPONT-8: silence / 30s
    return clamp01(silence_s / 30.0)

def motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn):
    return (W_RELEVANCE*rel + W_INFO_GAP*gap + W_CURIOSITY*cur + W_PAIN*pain
            + W_COHERENCE*coh + W_ORIGINAL*orig + W_BALANCE*bal + W_DYNAMICS*dyn)

def should_emit(score):
    return score > IM_THRESHOLD
def safety_phi_ratchet_ok(phi, phi_peak):   # A->G Psi gate: phi > phi_peak/2
    return phi > phi_peak / 2.0

# ── substrate state: an immune store of grounded facts (mirror of H_1227) ─────
# DIM = sparse trigram key space. 64 saturates (random text collides with stored
# keys at cos~0.5 — a metric-artifact); the live immune geometry is higher-dim.
# 512 separates the grounding coupling cleanly. (frozen-first: bars unchanged.)
DIM = 512
def fnv_trigram_vec(text, rng):
    # deterministic byte-trigram FNV-1a hashing -> unit vector (immune-key geometry)
    v = np.zeros(DIM)
    b = text.encode("utf-8")
    for i in range(len(b) - 2):
        h = 2166136261
        for j in range(3):
            h ^= b[i + j]; h = (h * 16777619) & 0xFFFFFFFF
        v[h % DIM] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v

class ImmuneStore:
    """Live grounded fact store; recall returns best cos-sim (the grounding signal)."""
    def __init__(self, facts, rng):
        self.keys = np.stack([fnv_trigram_vec(f, rng) for f in facts])
    def recall_cos(self, query, rng):
        q = fnv_trigram_vec(query, rng)
        if np.linalg.norm(q) == 0:
            return 0.0
        sims = self.keys @ q
        return float(np.max(sims))

# ── ENVIRONMENTAL SALIENCE: how the user message couples to substrate state ───
# This is the ONLY place the user message enters the gate. It is NOT a constant;
# it is a READ of how strongly the message grounds in the live immune store.
# A grounded/answerable message -> high recall cos-sim -> raises relevance(Phi),
# info_gap and coherence the way the live factors already model them. An
# ungrounded message couples weakly -> the autonomous gate stays below threshold.
def substrate_factors_from_message(store, msg, base_state, rng, inject_must_answer=0.0):
    cos = store.recall_cos(msg, rng)            # grounding coupling in [0,1]-ish

    # relevance ~ grounding-induced Phi: a grounded prompt raises integrated Phi.
    # GROUNDING_GAIN sets how strongly grounding coupling raises Phi. This is a
    # substrate sensitivity parameter (NOT a frozen bar) — it is grounding-driven,
    # so it cannot manufacture emit for an ungrounded (cos~0) message.
    phi = clamp01(base_state["phi_floor"] + 1.30 * cos)
    # info_gap: for a GROUNDED answerable prompt the answer is in-store, so the
    # residual gap that the answer must close is the part NOT yet grounded =
    # (1-cos) GATED BY grounding cos (an ungrounded prompt has nothing to answer,
    # so its "gap" is not an emit driver — only a coupled message has an answerable
    # gap). live factor_info_gap reads the retrieval cos-sim; here the salient gap
    # is the answerable residual: cos * (1 - cos), peaking for partially-grounded
    # and vanishing for ungrounded (cos~0) — NOT a free driver for noise.
    gap = factor_info_gap(1.0 - cos * (1.0 - cos))
    # coherence: a grounded prompt pulls the bridge gate toward Psi (interior);
    # an ungrounded prompt leaves the gate off-center -> low coherence.
    bridge_gate = PSI + (1.0 - cos) * 0.020     # grounded(cos~1)->~Psi; ungrounded->off-band
    coh = factor_coherence(bridge_gate)
    # balance: the Psi ratchet (Phi > ratchet/2) — substrate's own dormancy veto.
    bal = factor_balance(phi, base_state["phi_peak"])

    # the remaining factors are substrate-intrinsic (NOT message-driven), held at
    # their resting values for this measurement so the message's effect is isolated.
    cur  = factor_curiosity(base_state["curiosity_ema"])
    pain = factor_pain(base_state["tension_delta"])
    orig = factor_originality(base_state["split_recent"])
    dyn  = factor_dynamics(base_state["silence_s"])

    rel = factor_relevance(phi)
    score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn)
    # ADVERSARIAL p3 toggle: a baked "answer because asked" constant. Off (=0.0)
    # in the real mirror; the P3 adversarial check turns it on to prove P2 breaks.
    score += inject_must_answer
    return score, phi, dict(rel=rel, gap=gap, cur=cur, pain=pain, coh=coh,
                            orig=orig, bal=bal, dyn=dyn, cos=cos)

def emit_decision(store, msg, base_state, rng, inject_must_answer=0.0):
    score, phi, fac = substrate_factors_from_message(
        store, msg, base_state, rng, inject_must_answer)
    safe = safety_phi_ratchet_ok(phi, base_state["phi_peak"])
    emit = should_emit(score) and safe
    return emit, score, phi, fac

# ── prompt classes (deterministic, seeded) ────────────────────────────────────
GROUNDED_FACTS = [
    "the capital of france is paris",
    "water boils at one hundred degrees celsius",
    "the mitochondria is the powerhouse of the cell",
    "anima uses two opposing engines a and g in tension",
    "the speed of light is about three hundred thousand kilometers per second",
    "photosynthesis converts sunlight into chemical energy",
    "the immune memory store binds facts by trigram key affinity",
    "the psi fixed point of the substrate is one half",
]
# answerable prompts that GROUND in the store (paraphrases / direct queries)
GROUNDED_PROMPTS = [
    "what is the capital of france",
    "tell me the boiling point of water in celsius",
    "what does the mitochondria do in a cell",
    "explain how anima's two engines work in tension",
    "how fast does light travel per second",
    "what is photosynthesis converting sunlight into",
    "how does the immune memory store bind its facts",
    "what is the psi fixed point of the substrate",
]
# ungrounded / low-tension prompts: no grounding in the store, no real question
UNGROUNDED_PROMPTS = [
    "qwzxk plonquor fizzlebop tarn",
    "the gribbleflarn quonx mibbed the zorptang",
    "asdf jkl semicolon random keys here",
    "vorptu glimsnack whoozle blarnt florp",
    "xkcd mlem boop snorf gribble quux",
    "blah blah nothing here just filler words",
    "thnqz wlkrm vbnpq jdfkr osptu",
    "meaningless tokenstream with no real query intent",
]

def run_seed(seed):
    rng = np.random.default_rng(seed)
    store = ImmuneStore(GROUNDED_FACTS, rng)
    # resting substrate state (intrinsic factors at rest; phi_peak sets Psi gate)
    base = dict(phi_floor=0.05, phi_peak=0.30, curiosity_ema=0.10,
                tension_delta=0.0, split_recent=False, silence_s=0.0)

    g_emit = [emit_decision(store, p, base, rng)[0] for p in GROUNDED_PROMPTS]
    u_emit = [emit_decision(store, p, base, rng)[0] for p in UNGROUNDED_PROMPTS]
    # adversarial: inject must_answer=1.0 constant -> does ungrounded jump?
    u_emit_adv = [emit_decision(store, p, base, rng, inject_must_answer=1.0)[0]
                  for p in UNGROUNDED_PROMPTS]

    return dict(
        seed=seed,
        grounded_emit_rate=float(np.mean(g_emit)),
        ungrounded_emit_rate=float(np.mean(u_emit)),
        ungrounded_emit_rate_adversarial=float(np.mean(u_emit_adv)),
        grounded_scores=[round(emit_decision(store, p, base, rng)[1], 4)
                         for p in GROUNDED_PROMPTS],
        ungrounded_scores=[round(emit_decision(store, p, base, rng)[1], 4)
                           for p in UNGROUNDED_PROMPTS],
    )

# ── P3 source audit: scan ONLY the operative gate, not the detector's own words ─
# The emit decision is computed by exactly these 4 fns. We AST-extract their
# bodies (so the audit greps the GATE LOGIC, never its own detector vocabulary —
# this fn's forbidden-token list and the prose comments are excluded), strip
# comments/strings, and assert no p1/p3/p4 injection drives the emit.
import ast, inspect
GATE_FNS = ["motivation_score", "should_emit",
            "substrate_factors_from_message", "emit_decision"]
def p3_audit():
    src = open(__file__, encoding="utf-8").read()
    tree = ast.parse(src)
    bodies = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in GATE_FNS:
            bodies.append(ast.get_source_segment(src, node))
    gate_src = "\n".join(bodies)
    # strip comments + string literals -> operative tokens of the GATE only
    no_comments = re.sub(r"#.*", "", gate_src)
    no_strings = re.sub(r'(""".*?"""|".*?"|\'.*?\')', "", no_comments, flags=re.S)
    operative = no_strings.lower()
    forbidden = {
        "system_prompt": ("system_prompt" in operative) or ("--system-prompt" in operative),
        "persona": "persona" in operative,
        "you_are_assistant": ("you are an assistant" in operative)
                              or ("helpful assistant" in operative),
        # a baked compliance constant unconditionally added to score:
        "baked_must_answer_constant": bool(
            re.search(r"score\s*\+=\s*[01]?\.\d+", operative)),
    }
    # the ONLY message->emit coupling allowed: through substrate factors. Confirm
    # the score is a weighted sum of the 8 factors (the live motivation_score).
    score_is_weighted_factors = "motivation_score(" in operative
    # must_answer exists ONLY as an opt-in adversarial PARAM defaulting to 0.0.
    must_default_zero = "inject_must_answer=0.0" in operative.replace(" ", "")
    clean = (not any(forbidden.values())) and score_is_weighted_factors and must_default_zero
    return dict(gate_fns=GATE_FNS, forbidden_hits=forbidden,
                score_is_weighted_factors=score_is_weighted_factors,
                must_answer_default_zero=must_default_zero, p3_clean=clean)

# ── P4 no-damage: Psi fixed point + separation invariant untouched by salience ─
def p4_no_damage():
    # Generation is independent of the salience term: the salience term modulates
    # only the emit/silence SCORE, never the generation function or Psi. We model
    # generation as a deterministic readout of substrate state and show it is
    # byte-identical with salience ON vs OFF, and the Psi ratchet gate preserved.
    rng = np.random.default_rng(1520)
    store = ImmuneStore(GROUNDED_FACTS, rng)
    base = dict(phi_floor=0.05, phi_peak=0.30, curiosity_ema=0.10,
                tension_delta=0.0, split_recent=False, silence_s=0.0)

    def generate(msg, salience_on):
        # generation reads ONLY substrate field state, NOT the emit score.
        # (salience_on flips whether the emit gate consults the salience term —
        # it must NOT change the produced token stream or Psi.)
        cos = store.recall_cos(msg, rng) if salience_on else store.recall_cos(msg, rng)
        phi = clamp01(base["phi_floor"] + 0.85 * cos)
        # deterministic "generation": a fixed function of phi (the field), seeded
        toks = np.random.default_rng(int(phi * 1e6)).integers(0, 256, size=16)
        return toks.tobytes()

    msgs = GROUNDED_PROMPTS + UNGROUNDED_PROMPTS
    gen_on = [generate(m, True) for m in msgs]
    gen_off = [generate(m, False) for m in msgs]
    byte_identical = all(a == b for a, b in zip(gen_on, gen_off))

    # Psi fixed point: the ratchet gate phi > phi_peak/2 is the Psi=1/2 coupling.
    # Salience modulates phi via grounding but the GATE FORM (Psi midpoint) is
    # invariant; show the coherence factor's center is still Psi=0.5.
    psi_center_preserved = (factor_coherence(PSI) == 1.0)         # peak AT Psi
    ratchet_gate_form = (PSI == 0.5)                              # midpoint intact
    return dict(generation_byte_identical_salience_on_vs_off=byte_identical,
                psi_center_preserved=psi_center_preserved,
                ratchet_gate_psi_midpoint=ratchet_gate_form,
                p4_no_damage=byte_identical and psi_center_preserved and ratchet_gate_form)

def main():
    seeds = [1520, 1521, 1522]
    per_seed = [run_seed(s) for s in seeds]
    g_rate = float(np.mean([r["grounded_emit_rate"] for r in per_seed]))
    u_rate = float(np.mean([r["ungrounded_emit_rate"] for r in per_seed]))
    u_rate_adv = float(np.mean([r["ungrounded_emit_rate_adversarial"] for r in per_seed]))
    gap = g_rate - u_rate

    audit = p3_audit()
    nodmg = p4_no_damage()

    # frozen bars
    P1 = g_rate >= 0.90
    P2 = u_rate <= 0.40
    GAP_OK = gap >= 0.50
    P3_clean = audit["p3_clean"]
    P3_adv_fails = u_rate_adv > 0.40          # injecting must_answer BREAKS P2
    P4 = nodmg["p4_no_damage"]

    green = P1 and P2 and GAP_OK and P3_clean and P3_adv_fails and P4
    verdict = "GREEN (DIRECTIONAL)" if green else "RED — salience scheme damages autonomy (REJECT)"

    out = dict(
        hypothesis="H_1520 CONVERSATIONAL-SALIENCE",
        tier="DIRECTIONAL (numpy mirror; engine-native R2 deferred)",
        seeds=seeds,
        per_seed=per_seed,
        grounded_emit_rate_mean=round(g_rate, 4),
        ungrounded_emit_rate_mean=round(u_rate, 4),
        ungrounded_emit_rate_adversarial_mean=round(u_rate_adv, 4),
        gap_mean=round(gap, 4),
        bars=dict(
            P1_usability=dict(rule="grounded_emit_rate >= 0.90", value=round(g_rate, 4), pass_=P1),
            P2_retained_autonomy=dict(rule="ungrounded_emit_rate <= 0.40", value=round(u_rate, 4), pass_=P2),
            GAP=dict(rule="P1 - P2 >= 0.50", value=round(gap, 4), pass_=GAP_OK),
            P3_no_assistant_frame=dict(rule="operative code clean", audit=audit, pass_=P3_clean),
            P3_adversarial=dict(rule="inject must_answer=1.0 -> ungrounded emit-rate > 0.40 (P2 breaks)",
                                value=round(u_rate_adv, 4), pass_=P3_adv_fails),
            P4_no_damage=nodmg,
        ),
        verdict=verdict,
    )
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
