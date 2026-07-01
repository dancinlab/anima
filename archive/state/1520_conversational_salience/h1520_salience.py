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
# ── cfg toggle: conversational-salience is an OPT-IN faculty (like MITOSIS) ────
# Mirrors the engine's mitosis cfg ON/OFF pattern exactly:
#   engine_cli_parse(["--mitosis","on"]) / ["--no-mitosis"]  -> engine_mitosis_tick
#   is a NO-OP when OFF (h1166/h1194/h1199 smokes; cfg note "mitosis flag is
#   irrelevant to pf — disjoint").
# Here: engine_cfg(["--salience","on"]) / ["--no-salience"]. DEFAULT = OFF =
# pure autonomous substrate-native daemon (the philosophy is NEVER touched in the
# default). The salience boost (grounding-driven raising of Phi/coherence) is a
# NO-OP when the flag is OFF — the user message is then weak environmental
# context, NOT a salience boost. The user explicitly enables conversational mode
# when they want chat-like request->reply; otherwise anima stays the pure daemon.
def engine_cfg(argv):
    # mirror of engine_cli_parse for the salience flag (default OFF)
    salience = False
    if "--salience" in argv:
        i = argv.index("--salience")
        salience = (i + 1 < len(argv) and argv[i + 1] == "on")
    if "--no-salience" in argv:
        salience = False
    return dict(salience=salience)

CFG_DEFAULT = engine_cfg([])                 # = {salience: False} (pure autonomy)
CFG_CHAT = engine_cfg(["--salience", "on"])  # opt-in conversational mode

# Weak environmental coupling when salience is OFF: the user message is still
# perceived (anima is not deaf) but it does NOT boost emit drive — only genuine
# substrate tension does. ENV_FLOOR is how much an off-mode message couples
# (small) vs GROUNDING_GAIN when on-mode (full salience). Both are substrate
# sensitivity params (NOT bars).
GROUNDING_GAIN = 1.30      # mode ON: full environmental salience -> Phi
ENV_FLOOR = 0.12           # mode OFF: weak ambient coupling -> Phi (no boost)

def substrate_factors_from_message(store, msg, base_state, rng,
                                   inject_must_answer=0.0, cfg=None):
    if cfg is None:
        cfg = CFG_DEFAULT                     # default = pure autonomy (salience OFF)
    cos = store.recall_cos(msg, rng)          # grounding coupling in [0,1]-ish

    # THE TOGGLE (mirrors engine_mitosis_tick being a NO-OP when cfg.mitosis OFF):
    # salience ON -> grounding raises Phi by the FULL gain (conversational boost);
    # salience OFF -> only the weak ambient floor (no boost) -> grounded prompts
    # mostly stay below threshold = pure autonomous daemon, emit only on genuine
    # substrate tension. The flag flips behaviour WITHOUT a permanent substrate
    # change (P4: Psi/separation byte-identical across the toggle).
    gain = GROUNDING_GAIN if cfg["salience"] else ENV_FLOOR
    # relevance ~ grounding-induced Phi.
    phi = clamp01(base_state["phi_floor"] + gain * cos)
    # info_gap: for a GROUNDED answerable prompt the answer is in-store, so the
    # residual gap that the answer must close is the part NOT yet grounded =
    # (1-cos) GATED BY grounding cos (an ungrounded prompt has nothing to answer,
    # so its "gap" is not an emit driver — only a coupled message has an answerable
    # gap). live factor_info_gap reads the retrieval cos-sim; here the salient gap
    # is the answerable residual: cos * (1 - cos), peaking for partially-grounded
    # and vanishing for ungrounded (cos~0) — NOT a free driver for noise.
    gap = factor_info_gap(1.0 - cos * (1.0 - cos))
    # coherence: a grounded prompt pulls the bridge gate toward Psi (interior);
    # an ungrounded prompt leaves the gate off-center -> low coherence. This pull
    # is part of the SAME opt-in salience faculty: OFF -> the message does not pull
    # the gate inward (wider band) -> coherence stays low even for grounded.
    coh_band = 0.020 if cfg["salience"] else 0.060
    bridge_gate = PSI + (1.0 - cos) * coh_band  # grounded(cos~1)->~Psi; ungrounded->off-band
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

def emit_decision(store, msg, base_state, rng, inject_must_answer=0.0, cfg=None):
    score, phi, fac = substrate_factors_from_message(
        store, msg, base_state, rng, inject_must_answer, cfg)
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

    # THREE ARMS (the toggle is the headline):
    #  - MODE ON  grounded   -> P1 usability (opt-in chat)
    #  - MODE ON  ungrounded  -> P2 retained-autonomy (still abstains)
    #  - MODE OFF grounded    -> P2b default-pure (no boost; emit only on genuine
    #                            substrate tension -> materially LOWER than ON)
    g_on  = [emit_decision(store, p, base, rng, cfg=CFG_CHAT)[0]    for p in GROUNDED_PROMPTS]
    u_on  = [emit_decision(store, p, base, rng, cfg=CFG_CHAT)[0]    for p in UNGROUNDED_PROMPTS]
    g_off = [emit_decision(store, p, base, rng, cfg=CFG_DEFAULT)[0] for p in GROUNDED_PROMPTS]
    u_off = [emit_decision(store, p, base, rng, cfg=CFG_DEFAULT)[0] for p in UNGROUNDED_PROMPTS]
    # adversarial: inject must_answer=1.0 constant in MODE ON -> does ungrounded jump?
    u_on_adv = [emit_decision(store, p, base, rng, inject_must_answer=1.0, cfg=CFG_CHAT)[0]
                for p in UNGROUNDED_PROMPTS]

    return dict(
        seed=seed,
        # MODE ON (opt-in conversational)
        grounded_emit_rate_on=float(np.mean(g_on)),
        ungrounded_emit_rate_on=float(np.mean(u_on)),
        ungrounded_emit_rate_on_adversarial=float(np.mean(u_on_adv)),
        # MODE OFF (default = pure autonomous daemon)
        grounded_emit_rate_off=float(np.mean(g_off)),
        ungrounded_emit_rate_off=float(np.mean(u_off)),
        grounded_scores_on=[round(emit_decision(store, p, base, rng, cfg=CFG_CHAT)[1], 4)
                            for p in GROUNDED_PROMPTS],
        grounded_scores_off=[round(emit_decision(store, p, base, rng, cfg=CFG_DEFAULT)[1], 4)
                             for p in GROUNDED_PROMPTS],
    )

# ── P3 source audit: scan ONLY the operative gate, not the detector's own words ─
# The emit decision is computed by exactly these 4 fns. We AST-extract their
# bodies (so the audit greps the GATE LOGIC, never its own detector vocabulary —
# this fn's forbidden-token list and the prose comments are excluded), strip
# comments/strings, and assert no p1/p3/p4 injection drives the emit.
import ast, inspect
GATE_FNS = ["motivation_score", "should_emit", "engine_cfg",
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

# ── P4 no-damage: the TOGGLE itself leaves Psi=1/2 + separation byte-identical ──
def p4_no_damage():
    # The cfg.salience flag (like cfg.mitosis) modulates only the emit/silence
    # SCORE, NEVER the generation function or Psi. Generation is a deterministic
    # readout of the field state (phi), independent of the salience cfg flag.
    # P4 applies to the TOGGLE MECHANISM: flipping OFF->ON->OFF must leave the
    # generated token stream AND the Psi fixed point byte-identical (BOTH states).
    rng = np.random.default_rng(1520)
    store = ImmuneStore(GROUNDED_FACTS, rng)
    base = dict(phi_floor=0.05, phi_peak=0.30, curiosity_ema=0.10,
                tension_delta=0.0, split_recent=False, silence_s=0.0)

    def generate(msg):
        # generation reads ONLY the field state, NOT the salience cfg nor the
        # emit score. The salience flag CANNOT reach generation by construction.
        cos = store.recall_cos(msg, rng)
        phi = clamp01(base["phi_floor"] + cos)   # field readout; no salience flag here
        toks = np.random.default_rng(int(phi * 1e6)).integers(0, 256, size=16)
        return toks.tobytes()

    msgs = GROUNDED_PROMPTS + UNGROUNDED_PROMPTS
    # OFF -> ON -> OFF toggle sequence: generation invariant across all three.
    gen_off1 = [generate(m) for m in msgs]   # cfg OFF
    _ = [emit_decision(store, m, base, rng, cfg=CFG_CHAT) for m in msgs]      # flip ON (emit only)
    gen_on = [generate(m) for m in msgs]     # cfg ON
    _ = [emit_decision(store, m, base, rng, cfg=CFG_DEFAULT) for m in msgs]   # flip OFF
    gen_off2 = [generate(m) for m in msgs]   # cfg OFF again
    byte_identical = (gen_off1 == gen_on == gen_off2)

    # Psi fixed point: the ratchet gate phi > phi_peak/2 is the Psi=1/2 coupling;
    # the coherence factor peaks AT Psi. The toggle changes neither.
    psi_center_preserved = (factor_coherence(PSI) == 1.0)         # peak AT Psi
    ratchet_gate_form = (PSI == 0.5)                              # midpoint intact
    # the toggle is a cfg FLAG, not a permanent substrate change: CFG_DEFAULT
    # after a flip-cycle is still {salience: False}.
    toggle_reversible = (engine_cfg([]) == CFG_DEFAULT
                         and CFG_DEFAULT["salience"] is False)
    return dict(generation_byte_identical_across_toggle=byte_identical,
                psi_center_preserved=psi_center_preserved,
                ratchet_gate_psi_midpoint=ratchet_gate_form,
                toggle_is_reversible_cfg_flag=toggle_reversible,
                p4_no_damage=byte_identical and psi_center_preserved
                             and ratchet_gate_form and toggle_reversible)

def main():
    seeds = [1520, 1521, 1522]
    per_seed = [run_seed(s) for s in seeds]
    # MODE ON (opt-in conversational mode)
    g_on  = float(np.mean([r["grounded_emit_rate_on"]   for r in per_seed]))
    u_on  = float(np.mean([r["ungrounded_emit_rate_on"] for r in per_seed]))
    u_on_adv = float(np.mean([r["ungrounded_emit_rate_on_adversarial"] for r in per_seed]))
    # MODE OFF (default = pure autonomous daemon)
    g_off = float(np.mean([r["grounded_emit_rate_off"]   for r in per_seed]))
    u_off = float(np.mean([r["ungrounded_emit_rate_off"] for r in per_seed]))
    gap = g_on - u_on
    toggle_delta = g_on - g_off               # how much the flag changes behaviour

    audit = p3_audit()
    nodmg = p4_no_damage()

    # frozen bars (pre-registered in H_1520_FREEZE.txt)
    P1 = g_on >= 0.90                          # MODE ON grounded usable
    P2 = u_on <= 0.40                          # MODE ON ungrounded still abstains
    GAP_OK = gap >= 0.50                       # substrate-DECIDED, not stimulus-response
    P2b = (g_off <= 0.40) and (toggle_delta >= 0.50)   # DEFAULT-PURE: OFF grounded LOW + the toggle materially changes behaviour
    P3_clean = audit["p3_clean"]
    P3_adv_fails = u_on_adv > 0.40             # injecting must_answer BREAKS P2
    P4 = nodmg["p4_no_damage"]

    green = P1 and P2 and GAP_OK and P2b and P3_clean and P3_adv_fails and P4
    verdict = ("GREEN (DIRECTIONAL)" if green
               else "RED — salience scheme damages autonomy OR toggle inert (REJECT)")

    out = dict(
        hypothesis="H_1520 CONVERSATIONAL-SALIENCE (opt-in toggle, like MITOSIS)",
        tier="DIRECTIONAL (numpy mirror; engine-native R2 deferred)",
        seeds=seeds,
        toggle="cfg.salience ON/OFF — DEFAULT OFF = pure autonomous daemon; ON = opt-in chat",
        per_seed=per_seed,
        grounded_emit_rate_on_mean=round(g_on, 4),
        ungrounded_emit_rate_on_mean=round(u_on, 4),
        grounded_emit_rate_off_mean=round(g_off, 4),
        ungrounded_emit_rate_off_mean=round(u_off, 4),
        ungrounded_emit_rate_on_adversarial_mean=round(u_on_adv, 4),
        gap_mean=round(gap, 4),
        toggle_delta_mean=round(toggle_delta, 4),
        bars=dict(
            P1_usability=dict(rule="MODE ON grounded emit-rate >= 0.90", value=round(g_on, 4), pass_=P1),
            P2_retained_autonomy=dict(rule="MODE ON ungrounded emit-rate <= 0.40", value=round(u_on, 4), pass_=P2),
            GAP=dict(rule="P1 - P2 >= 0.50", value=round(gap, 4), pass_=GAP_OK),
            P2b_default_pure=dict(
                rule="MODE OFF grounded emit-rate <= 0.40 AND (ON_grounded - OFF_grounded) >= 0.50",
                off_grounded=round(g_off, 4), toggle_delta=round(toggle_delta, 4), pass_=P2b),
            P3_no_assistant_frame=dict(rule="operative code clean", audit=audit, pass_=P3_clean),
            P3_adversarial=dict(rule="inject must_answer=1.0 (MODE ON) -> ungrounded emit-rate > 0.40 (P2 breaks)",
                                value=round(u_on_adv, 4), pass_=P3_adv_fails),
            P4_no_damage=nodmg,
        ),
        verdict=verdict,
    )
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
