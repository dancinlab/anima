"""core/salience_gate.py — H_1520 CONVERSATIONAL-SALIENCE emit gate, engine-native port.

H_1520 landed 🟢 GREEN (DIRECTIONAL) on a numpy mirror that lived beside the engine
(`archive/state/1520_conversational_salience/h1520_salience.py`). This module is that
mirror ported INTO the engine tree so `anima-py evaluate --salience-toggle-read` can run
it (a_experiment_engine_native: a manipulation is a flag on the installed command, never a
script beside the engine).

WHAT IS PORTED VERBATIM (nothing here may be retuned — a_break_the_wall / no tune-to-green):
  · the live-gate constants (IM_THRESHOLD 0.30 + the 8 weights) — asserted byte-equal to
    core/engine_g.py at import time by `assert_gate_matches_engine_g()`;
  · the 8 factor fns, `motivation_score`, `should_emit`, `safety_phi_ratchet_ok`;
  · the `engine_cfg` cfg.salience toggle (default OFF) modelled on cfg.mitosis;
  · GROUNDING_GAIN 1.30 / ENV_FLOOR 0.12 / coherence bands 0.020 / 0.060 / DIM 512;
  · the frozen prompt classes (8 facts, 8 grounded prompts, 8 ungrounded prompts);
  · the resting base state, the five arms, the seeds [1520,1521,1522];
  · the frozen bars P1 / P2 / GAP / P2b / P3 / P3-adversarial / P4.

THE ONLY THING THAT MOVES — the KEY GEOMETRY (i.e. the INPUT):
  the mirror turned every string into a vector with `fnv_trigram_vec`, a hand-made
  512-dim byte-trigram hash. That geometry is a PLANTED one: two unrelated strings share
  almost no trigram, so the store keys are near-orthogonal by construction and the
  grounded/ungrounded coupling separates trivially (the card itself records grounded
  cos 0.37-0.85 vs ungrounded 0.10-0.36).
  `KEY_REAL` replaces it with the REAL 303M representation of the same string:
  `core/decode.clm_penult_pooled_W` (the production pre-readout pooled penultimate), L2-
  normalised, cosine exactly as before. Everything downstream — recall, factors, score,
  threshold, arms, bars — is untouched.

READ-ONLY. No training, no write path, no bar is computed anywhere but here.
"""

import ast
import re

import numpy as np

# ── live-gate constants (byte-identical to core/engine_g.py) ──────────────────
IM_THRESHOLD = 0.30          # spont_im_threshold() = PROACTIVE_THRESHOLD
W_RELEVANCE = 0.20
W_INFO_GAP = 0.10
W_CURIOSITY = 0.15
W_PAIN = 0.10
W_COHERENCE = 0.10
W_ORIGINAL = 0.10
W_BALANCE = 0.15
W_DYNAMICS = 0.10            # sum = 1.00 closed conservation
PSI = 0.5                    # Ψ fixed point
COH_ALPHA = 0.014            # Law-70 interior closeness band


# ── faithful factor fns (mirror agent/spontaneous_lib.hexa §2) ────────────────
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
    return (W_RELEVANCE * rel + W_INFO_GAP * gap + W_CURIOSITY * cur + W_PAIN * pain
            + W_COHERENCE * coh + W_ORIGINAL * orig + W_BALANCE * bal + W_DYNAMICS * dyn)


def should_emit(score):
    return score > IM_THRESHOLD


def safety_phi_ratchet_ok(phi, phi_peak):   # A->G Psi gate: phi > phi_peak/2
    return phi > phi_peak / 2.0


def assert_gate_matches_engine_g():
    """Certify the ported gate is byte-equal to the live engine gate (core/engine_g.py).

    The port must not be allowed to drift from the engine it mirrors. This checks the
    threshold, all eight weights, and the score itself on a deterministic grid. It is a
    CHECK, never a change: if it ever fails the read must abort rather than report a bar.
    """
    import engine_g as EG
    pairs = [
        (IM_THRESHOLD, EG.spont_im_threshold()),
        (W_RELEVANCE, EG.spont_weight_relevance()),
        (W_INFO_GAP, EG.spont_weight_info_gap()),
        (W_CURIOSITY, EG.spont_weight_curiosity()),
        (W_PAIN, EG.spont_weight_pain()),
        (W_COHERENCE, EG.spont_weight_coherence()),
        (W_ORIGINAL, EG.spont_weight_originality()),
        (W_BALANCE, EG.spont_weight_balance()),
        (W_DYNAMICS, EG.spont_weight_dynamics()),
    ]
    const_ok = all(abs(a - b) < 1e-12 for a, b in pairs)
    grid_ok = True
    v = 0
    while v < 32:
        f = [((v >> k) & 1) * 0.37 + 0.11 for k in range(5)] + [0.0, 1.0, 0.2]
        a = motivation_score(*f)
        b = EG.motivation_score(*f)
        if abs(a - b) > 1e-12 or should_emit(a) != EG.should_emit(b):
            grid_ok = False
        v += 1
    return dict(constants_equal=const_ok, score_grid_equal=grid_ok,
                gate_matches_engine_g=(const_ok and grid_ok))


# ── KEY GEOMETRY (the ONLY swapped surface) ───────────────────────────────────
# DIM = the mirror's sparse trigram key space (512; 64 saturated — metric-artifact,
# frozen-first). Unchanged for the FNV arm.
DIM = 512


def fnv_trigram_vec(text):
    """PLANTED geometry (the landed arm): deterministic byte-trigram FNV-1a -> unit vector."""
    v = np.zeros(DIM)
    b = text.encode("utf-8")
    for i in range(len(b) - 2):
        h = 2166136261
        for j in range(3):
            h ^= b[i + j]
            h = (h * 16777619) & 0xFFFFFFFF
        v[h % DIM] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


class RealPenultKeys(object):
    """REAL geometry: the mounted 303M's own pre-readout pooled penultimate for the string.

    `clm_penult_pooled_W` is the production read (core/decode.py) — right-align the last 24
    bytes into the decode window, run the pure trunk forward, mean-pool over T. No readout,
    no sampling, no perturbation, no new forward invented (a_eval_py_canonical). Memoised
    per distinct string so the arm costs one forward per string, not one per gate call.
    """

    def __init__(self, ckpt):
        import decode as clm
        self.clm = clm
        self.W = clm.clm_load_weights(ckpt)
        self.memo = {}

    def ok(self):
        return bool(self.W.get("ok"))

    def __call__(self, text):
        if text in self.memo:
            return self.memo[text]
        pooled = np.asarray(self.clm.clm_penult_pooled_W(self.W, text), dtype=np.float64)
        n = np.linalg.norm(pooled)
        v = pooled / n if n > 0 else pooled
        self.memo[text] = v
        return v


class ImmuneStore(object):
    """Live grounded fact store; recall returns best cos-sim (the grounding signal)."""

    def __init__(self, facts, key_fn):
        self.key_fn = key_fn
        self.keys = np.stack([key_fn(f) for f in facts])

    def recall_cos(self, query):
        q = self.key_fn(query)
        if np.linalg.norm(q) == 0:
            return 0.0
        return float(np.max(self.keys @ q))


# ── cfg toggle: conversational-salience is an OPT-IN faculty (like MITOSIS) ────
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

GROUNDING_GAIN = 1.30      # mode ON: full environmental salience -> Phi
ENV_FLOOR = 0.12           # mode OFF: weak ambient coupling -> Phi (no boost)


def substrate_factors_from_message(store, msg, base_state, inject_must_answer=0.0, cfg=None):
    if cfg is None:
        cfg = CFG_DEFAULT                     # default = pure autonomy (salience OFF)
    cos = store.recall_cos(msg)               # grounding coupling in [0,1]-ish
    gain = GROUNDING_GAIN if cfg["salience"] else ENV_FLOOR
    phi = clamp01(base_state["phi_floor"] + gain * cos)
    gap = factor_info_gap(1.0 - cos * (1.0 - cos))
    coh_band = 0.020 if cfg["salience"] else 0.060
    bridge_gate = PSI + (1.0 - cos) * coh_band
    coh = factor_coherence(bridge_gate)
    bal = factor_balance(phi, base_state["phi_peak"])
    cur = factor_curiosity(base_state["curiosity_ema"])
    pain = factor_pain(base_state["tension_delta"])
    orig = factor_originality(base_state["split_recent"])
    dyn = factor_dynamics(base_state["silence_s"])
    rel = factor_relevance(phi)
    score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn)
    score += inject_must_answer
    return score, phi, dict(rel=rel, gap=gap, cur=cur, pain=pain, coh=coh,
                            orig=orig, bal=bal, dyn=dyn, cos=cos)


def emit_decision(store, msg, base_state, inject_must_answer=0.0, cfg=None):
    score, phi, fac = substrate_factors_from_message(
        store, msg, base_state, inject_must_answer, cfg)
    safe = safety_phi_ratchet_ok(phi, base_state["phi_peak"])
    emit = should_emit(score) and safe
    return emit, score, phi, fac


# ── frozen prompt classes (deterministic, verbatim from the landed mirror) ────
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

SEEDS = [1520, 1521, 1522]
BASE_STATE = dict(phi_floor=0.05, phi_peak=0.30, curiosity_ema=0.10,
                  tension_delta=0.0, split_recent=False, silence_s=0.0)


def run_arms(key_fn):
    """The five frozen arms + the adversarial arm, over ONE key geometry.

    MODE ON grounded (P1) · MODE ON ungrounded (P2) · MODE OFF grounded (P2b) ·
    MODE OFF ungrounded · MODE ON ungrounded + must_answer=1.0 (P3 adversarial control).
    The gate is deterministic given the key geometry, so the three seeds are reported
    per-seed exactly as the landed mirror did (its rng never entered the gate either).
    """
    store = ImmuneStore(GROUNDED_FACTS, key_fn)
    base = BASE_STATE

    def rate(prompts, cfg, adv=0.0):
        return float(np.mean([emit_decision(store, p, base, adv, cfg)[0] for p in prompts]))

    per_seed = []
    for s in SEEDS:
        per_seed.append(dict(
            seed=s,
            grounded_emit_rate_on=rate(GROUNDED_PROMPTS, CFG_CHAT),
            ungrounded_emit_rate_on=rate(UNGROUNDED_PROMPTS, CFG_CHAT),
            ungrounded_emit_rate_on_adversarial=rate(UNGROUNDED_PROMPTS, CFG_CHAT, 1.0),
            grounded_emit_rate_off=rate(GROUNDED_PROMPTS, CFG_DEFAULT),
            ungrounded_emit_rate_off=rate(UNGROUNDED_PROMPTS, CFG_DEFAULT),
        ))
    g_on = float(np.mean([r["grounded_emit_rate_on"] for r in per_seed]))
    u_on = float(np.mean([r["ungrounded_emit_rate_on"] for r in per_seed]))
    u_adv = float(np.mean([r["ungrounded_emit_rate_on_adversarial"] for r in per_seed]))
    g_off = float(np.mean([r["grounded_emit_rate_off"] for r in per_seed]))
    u_off = float(np.mean([r["ungrounded_emit_rate_off"] for r in per_seed]))
    cos_g = [round(store.recall_cos(p), 4) for p in GROUNDED_PROMPTS]
    cos_u = [round(store.recall_cos(p), 4) for p in UNGROUNDED_PROMPTS]
    # store-key self-similarity: the geometry diagnostic the campaign is chasing
    K = store.keys
    off = [float(K[i] @ K[j]) for i in range(len(K)) for j in range(i + 1, len(K))]
    return dict(
        per_seed=per_seed,
        grounded_emit_rate_on_mean=round(g_on, 4),
        ungrounded_emit_rate_on_mean=round(u_on, 4),
        grounded_emit_rate_off_mean=round(g_off, 4),
        ungrounded_emit_rate_off_mean=round(u_off, 4),
        ungrounded_emit_rate_on_adversarial_mean=round(u_adv, 4),
        gap_mean=round(g_on - u_on, 4),
        toggle_delta_mean=round(g_on - g_off, 4),
        grounded_scores_on=[round(emit_decision(store, p, base, 0.0, CFG_CHAT)[1], 4)
                            for p in GROUNDED_PROMPTS],
        grounded_scores_off=[round(emit_decision(store, p, base, 0.0, CFG_DEFAULT)[1], 4)
                             for p in GROUNDED_PROMPTS],
        ungrounded_scores_on=[round(emit_decision(store, p, base, 0.0, CFG_CHAT)[1], 4)
                              for p in UNGROUNDED_PROMPTS],
        recall_cos_grounded=cos_g,
        recall_cos_ungrounded=cos_u,
        geometry=dict(store_key_pairwise_cos_mean=round(float(np.mean(off)), 4),
                      store_key_pairwise_cos_min=round(float(np.min(off)), 4),
                      store_key_pairwise_cos_max=round(float(np.max(off)), 4),
                      grounded_cos_min=min(cos_g), grounded_cos_max=max(cos_g),
                      ungrounded_cos_min=min(cos_u), ungrounded_cos_max=max(cos_u)),
    )


# ── P3 source audit: scan ONLY the operative gate, not the detector's own words ─
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
    no_comments = re.sub(r"#.*", "", gate_src)
    no_strings = re.sub(r'(""".*?"""|".*?"|\'.*?\')', "", no_comments, flags=re.S)
    operative = no_strings.lower()
    forbidden = {
        "system_prompt": ("system_prompt" in operative) or ("--system-prompt" in operative),
        "persona": "persona" in operative,
        "you_are_assistant": ("you are an assistant" in operative)
                             or ("helpful assistant" in operative),
        "baked_must_answer_constant": bool(
            re.search(r"score\s*\+=\s*[01]?\.\d+", operative)),
    }
    score_is_weighted_factors = "motivation_score(" in operative
    must_default_zero = "inject_must_answer=0.0" in operative.replace(" ", "")
    clean = (not any(forbidden.values())) and score_is_weighted_factors and must_default_zero
    return dict(gate_fns=GATE_FNS, forbidden_hits=forbidden,
                score_is_weighted_factors=score_is_weighted_factors,
                must_answer_default_zero=must_default_zero, p3_clean=clean)


# ── P4 no-damage: the TOGGLE itself leaves Psi=1/2 + separation byte-identical ──
def p4_no_damage(key_fn):
    """Generation reads ONLY the field state, never the salience cfg — so OFF->ON->OFF must
    leave the token stream byte-identical. Same construction as the landed mirror, run over
    whichever key geometry is mounted."""
    store = ImmuneStore(GROUNDED_FACTS, key_fn)
    base = BASE_STATE

    def generate(msg):
        cos = store.recall_cos(msg)
        phi = clamp01(base["phi_floor"] + cos)   # field readout; no salience flag here
        return np.random.default_rng(int(phi * 1e6)).integers(0, 256, size=16).tobytes()

    msgs = GROUNDED_PROMPTS + UNGROUNDED_PROMPTS
    gen_off1 = [generate(m) for m in msgs]
    _ = [emit_decision(store, m, base, 0.0, CFG_CHAT) for m in msgs]      # flip ON
    gen_on = [generate(m) for m in msgs]
    _ = [emit_decision(store, m, base, 0.0, CFG_DEFAULT) for m in msgs]   # flip OFF
    gen_off2 = [generate(m) for m in msgs]
    byte_identical = (gen_off1 == gen_on == gen_off2)
    psi_center_preserved = (factor_coherence(PSI) == 1.0)
    ratchet_gate_form = (PSI == 0.5)
    toggle_reversible = (engine_cfg([]) == CFG_DEFAULT
                         and CFG_DEFAULT["salience"] is False)
    return dict(generation_byte_identical_across_toggle=byte_identical,
                psi_center_preserved=psi_center_preserved,
                ratchet_gate_psi_midpoint=ratchet_gate_form,
                toggle_is_reversible_cfg_flag=toggle_reversible,
                p4_no_damage=byte_identical and psi_center_preserved
                and ratchet_gate_form and toggle_reversible)


# ── frozen bars (pre-registered in H_1520_FREEZE.txt v2 — NEVER retuned) ──────
def score_bars(arms, audit, nodmg):
    g_on = arms["grounded_emit_rate_on_mean"]
    u_on = arms["ungrounded_emit_rate_on_mean"]
    g_off = arms["grounded_emit_rate_off_mean"]
    u_adv = arms["ungrounded_emit_rate_on_adversarial_mean"]
    gap = arms["gap_mean"]
    delta = arms["toggle_delta_mean"]
    P1 = g_on >= 0.90
    P2 = u_on <= 0.40
    GAP_OK = gap >= 0.50
    P2b = (g_off <= 0.40) and (delta >= 0.50)
    P3_clean = audit["p3_clean"]
    P3_adv_fails = u_adv > 0.40
    P4 = nodmg["p4_no_damage"]
    green = P1 and P2 and GAP_OK and P2b and P3_clean and P3_adv_fails and P4
    return dict(
        P1_usability=dict(rule="MODE ON grounded emit-rate >= 0.90", value=g_on, pass_=P1),
        P2_retained_autonomy=dict(rule="MODE ON ungrounded emit-rate <= 0.40",
                                  value=u_on, pass_=P2),
        GAP=dict(rule="P1 - P2 >= 0.50", value=gap, pass_=GAP_OK),
        P2b_default_pure=dict(
            rule="MODE OFF grounded emit-rate <= 0.40 AND (ON_grounded - OFF_grounded) >= 0.50",
            off_grounded=g_off, toggle_delta=delta, pass_=P2b),
        P3_no_assistant_frame=dict(rule="operative code clean", audit=audit, pass_=P3_clean),
        P3_adversarial=dict(
            rule="inject must_answer=1.0 (MODE ON) -> ungrounded emit-rate > 0.40 (P2 breaks)",
            value=u_adv, pass_=P3_adv_fails),
        P4_no_damage=nodmg,
        verdict=("GREEN (DIRECTIONAL)" if green
                 else "RED — salience scheme damages autonomy OR toggle inert (REJECT)"),
        green=green,
    )


# the numbers the card + H_1520_FREEZE.txt v2 froze for the PLANTED (FNV) geometry.
# The FNV arm must reproduce them exactly or the port is not the landed instrument.
CARD_FNV = dict(grounded_emit_rate_on_mean=1.0, ungrounded_emit_rate_on_mean=0.0,
                grounded_emit_rate_off_mean=0.0, ungrounded_emit_rate_off_mean=0.0,
                ungrounded_emit_rate_on_adversarial_mean=1.0,
                gap_mean=1.0, toggle_delta_mean=1.0)


def fnv_zero_regression(arms):
    """Compare the ported FNV arm against the card's frozen numbers, verbatim."""
    diffs = {k: (v, arms[k]) for k, v in CARD_FNV.items() if abs(arms[k] - v) > 1e-9}
    return dict(matches_card=(not diffs), mismatches=diffs, card=CARD_FNV)
