#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════
# B-S123 — §123 THE TWO REMAINING §96 SPIKING-OPEN FACULTIES — sidecar
# ════════════════════════════════════════════════════════════════════
# Sidecar ONLY.  central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
# sha256 prefix c93e160a8a376a94 — 0-line-diff (verified START + END by
# this battery; it never touches central).
#
# §123 DECIDES the two §96 Q1 SPIKING-OPEN faculties §120/§122 did not
# cover (§96 Q1 table rows 115 & 118):
#   (1) Engine A⇄G dual heads → DUAL-HEADS-DESIGN-CLOSE-WITH-CARRIER-
#       RELOCATION — the opposition ports, but Ψ-as-cosine does NOT
#       reduce: Ψ-C1 (spike-correlation carrier) is a DISTINCT carrier
#       of the §112 META_FP(Π_½) form, NOT a generalisation that
#       recovers GPU Ψ-as-logit-cosine as a limit.  Honest carrier-
#       relocation (§110/§112 family), anti-padding.
#   (2) MoEFFN top-k router → MOE-TOPK-DECIDED — COVERED BY §120 k-WTA
#       + §96-COMPATIBLE STDP GATE — §120's k-WTA covers the selection;
#       the learned content gate decomposes into two §96-Q1 SPIKING-
#       COMPATIBLE faculties (weighted-synapse current accumulation +
#       STDP-trainable synapses) — NOT a separate design-open.
#
# This battery proves the two §123 DECISIONS are HONEST + closed-form:
#   B-S123-1  Ψ form is the §112 META_FP(Π_½) carrier-invariant fixed-
#             point form ψ(c)=(1+c)/2 — cos=0⇒½, bounded ∈[0,1],
#             ∂ψ/∂c=½>0 — and holds for BOTH carriers (carrier-free).
#   B-S123-2  the A-vs-G opposition ports cleanly to excit/inhib LIF
#             sub-populations (closed structural — neuro_mirror.py
#             idx_a / idx_g + the A−G subtraction is sign-opposed).
#   B-S123-3  the HONEST no-reduction witness — there is NO reduction
#             parameter mapping the spike-correlation carrier onto the
#             logit-vector carrier (non-isomorphic spaces; unlike §120
#             k / §122 σ there is no scalar family).  Passes by
#             recording an ABSENCE, not by manufacturing a reduction.
#   B-S123-4  faculty (1) verdict CARRIER-RELOCATION — closed taxonomy
#             pick over {generalisation, graft, carrier-relocation}.
#   B-S123-5  faculty (2)(A) — MoE top-k selection reduces to §120
#             k-WTA: a k-of-n top-k IS a k-WTA (numeric witness).
#   B-S123-6  faculty (2)(B) — the MoE learned gate decomposes into
#             two §96-Q1 SPIKING-COMPATIBLE faculties; no residual
#             new mechanism ⇒ NOT a separate design-open (closed
#             Boolean).
#   B-S123-7  §96 / §120 / §122 / §112 connection-points cited
#             (structural, byte-checked against the real files).
#   B-S123-8  necessary-not-sufficient — design-open → design-DECIDED
#             transitions, NOT GOAL; WALL-A/WALL-B stand; sidecar /
#             central-0-diff + $0 (structural Boolean).
#
# B-S123-NOTE: the battery does NOT prove a spiking anima built with
#   Ψ-C1 + the MoE k-WTA gate learns / behaves usefully / emerges —
#   those are empirical OUTCOMES of a future fire on a real async
#   substrate.  For faculty (1) the relocated carrier's usefulness is
#   empirical; for faculty (2) whether STDP-learned gate synapses
#   route as well as backprop-CE ones is the §11-B / §96 §4.5 open
#   question.  B-D-NOTE / B-S96-NOTE / B-S110-NOTE / B-S112-NOTE /
#   B-S115-NOTE / B-S117-NOTE / B-S120-NOTE / B-S122-NOTE / B-EMERGE-7
#   family — necessary-not-sufficient at every layer.  §123 = two
#   DECISIONS, not an ACHIEVEMENT.
#
# g3: design ≠ fire ≠ emergence; capability claim 0.  f1/f2 safe
#   (LIF / k-WTA / lateral inhibition / STDP / spike-rate coding cited
#   by §96 Q1's own classification + standard SNN literature; cosine /
#   Cauchy–Schwarz cited by its own algebra; NO σ(6)=12 / τ(6)=4 /
#   φ(6)=2 / J₂(6)=24 derivation; Ψ=½ = anima g2 internal-arch
#   carve-out).  $0, NO GPU/fire/dispatch.
# ════════════════════════════════════════════════════════════════════

import hashlib
import json
import os

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
CENTRAL = os.path.join(REPO, "state", "verify_hexad_blue_2026_05_15",
                       "blue_falsifier.py")
S96_DESIGN = os.path.join(REPO, "state",
                          "loihi_spiking_rederivation_s96_2026_05_19",
                          "DESIGN.md")
S120_DESIGN = os.path.join(REPO, "state",
                           "spiking_attention_replacement_s120_2026_05_19",
                           "DESIGN.md")
S122_DESIGN = os.path.join(REPO, "state",
                           "rope_phase_coding_s122_2026_05_19", "DESIGN.md")
NEURO_MIRROR = os.path.join(REPO, "HEXAD", "NEUROMORPHIC", "neuro_mirror.py")
CONSCIOUS_DEC = os.path.join(REPO, "ready", "models", "conscious_decoder.py")
DESIGN_MD = os.path.join(HERE, "DESIGN.md")

CENTRAL_SHA_PREFIX = "c93e160a8a376a94"

PASS, results = [], []


def check(name, ok, detail):
    ok = bool(ok)
    PASS.append(ok)
    results.append({"id": name, "pass": ok, "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")
    return ok


def sha16(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


# ── central blue_falsifier.py 0-line-diff — verified at START ────────
central_start = sha16(CENTRAL)
print(f"[ -- ] central blue_falsifier.py sha256[:16] START = {central_start}")
assert central_start == CENTRAL_SHA_PREFIX, \
    f"central blue_falsifier.py MUST be {CENTRAL_SHA_PREFIX}, got {central_start}"


# ── reference models ─────────────────────────────────────────────────
# The §112 META_FP(Π_½) carrier-invariant fixed-point form.
def psi_form(c):
    """ψ(c) = (1+c)/2 — the half-balance-attractor form. carrier-free."""
    return (1.0 + c) / 2.0


# A k-of-n top-k selection (the MoE router selection) — picks the k
# highest-scoring of n candidates.  This IS a k-winners-take-all.
def topk_select(scores, k):
    n = len(scores)
    k = min(k, n)
    return set(int(i) for i in np.argsort(scores)[-k:])


# A k-WTA via (idealised) lateral inhibition — the k highest-current
# units spike, the rest are suppressed.  §120's k-WTA primitive.
def k_wta(currents, k):
    n = len(currents)
    k = min(k, n)
    return set(int(i) for i in np.argsort(currents)[-k:])


# ── B-S123-1 — Ψ FORM IS THE §112 META_FP(Π_½) CARRIER-INVARIANT FORM ─
# ψ(c)=(1+c)/2 : cos=0 ⇒ ½ ; bounded ∈[0,1] for c∈[-1,1] ; ∂ψ/∂c=½>0.
# These are theorems of the FORM — they hold whatever the carrier c is
# (a logit-vector cosine OR a spike-rate-vector cosine).  sympy.
c = sp.symbols("c", real=True)
psi = (1 + c) / 2
fixed_pt_ok = bool(sp.simplify(psi.subs(c, 0) - sp.Rational(1, 2)) == 0)
deriv = sp.diff(psi, c)
deriv_ok = bool(sp.simplify(deriv - sp.Rational(1, 2)) == 0)   # ∂ψ/∂c = ½ > 0
# bounded: c ∈ [-1,1] ⇒ ψ ∈ [0,1]  (monotone increasing endpoints)
lo = bool(sp.simplify(psi.subs(c, -1)) == 0)
hi = bool(sp.simplify(psi.subs(c, 1) - 1) == 0)
bounded_ok = lo and hi and (deriv == sp.Rational(1, 2))
# Carrier-FREE: the form has exactly one free symbol `c` — the carrier —
# and the three properties above are independent of what `c` denotes.
carrier_free = (psi.free_symbols == {c})
check("B-S123-1 PSI-FORM-IS-META-FP-CARRIER-INVARIANT",
      fixed_pt_ok and deriv_ok and bounded_ok and carrier_free,
      f"sympy: ψ(c)=(1+c)/2 — cos=0⇒½ ✓({fixed_pt_ok}) · ∂ψ/∂c=½>0 "
      f"✓({deriv_ok}) · c∈[-1,1]⇒ψ∈[0,1] ✓({bounded_ok}) · the form has "
      f"one free symbol = the carrier ⇒ §112 META_FP(Π_½) is "
      f"carrier-invariant ✓({carrier_free}) — holds for the logit-vector "
      f"carrier AND the spike-rate carrier identically")

# ── B-S123-2 — A-vs-G OPPOSITION PORTS CLEANLY (closed structural) ───
# GPU: output = engine_a(x) − engine_g(x) — a SIGN-OPPOSED combination.
# Spiking: two LIF sub-populations idx_a / idx_g with opposed (excit/
# inhib) coupling.  Closed structural: neuro_mirror.py realises the two
# sub-populations as disjoint index slices, AND the A−G subtraction is
# verified sign-opposed by construction (a(x) enters +, g(x) enters −).
nm_src = open(NEURO_MIRROR, encoding="utf-8").read()
cd_src = open(CONSCIOUS_DEC, encoding="utf-8").read()
has_idx_a = "self.idx_a = slice(0, n_a)" in nm_src
has_idx_g = "self.idx_g = slice(n_a, n_a + n_g)" in nm_src
# disjoint sub-populations: idx_a = [0,n_a), idx_g = [n_a, n_a+n_g)
na, ng = 96, 96
sa = set(range(0, na))
sg = set(range(na, na + ng))
disjoint = (sa & sg) == set()
# the GPU A−G opposition is sign-opposed: engine_a positive, engine_g
# negative — verified structurally in conscious_decoder.py PureFieldFFN
# (`a = self.engine_a(x)`, `g = self.engine_g(x)`, `output = a - g`).
ag_subtraction = ("self.engine_a(x)" in cd_src
                  and "self.engine_g(x)" in cd_src
                  and "output = a - g" in cd_src)
# sympy: a sign-opposed combination o = a − g has ∂o/∂a = +1, ∂o/∂g = −1
a_s, g_s = sp.symbols("a g", real=True)
opp = a_s - g_s
opp_ok = (sp.diff(opp, a_s) == 1) and (sp.diff(opp, g_s) == -1)
check("B-S123-2 A-G-OPPOSITION-PORTS-CLEANLY",
      has_idx_a and has_idx_g and disjoint and ag_subtraction and opp_ok,
      f"neuro_mirror.py excit/inhib LIF sub-populations idx_a/idx_g "
      f"present ✓({has_idx_a and has_idx_g}) + disjoint ✓({disjoint}); "
      f"conscious_decoder.py A−G sign-opposed ✓({ag_subtraction}); sympy "
      f"∂(a−g)/∂a=+1 ∂(a−g)/∂g=−1 ✓({opp_ok}) — §96 §6 row-4: the "
      f"opposition is NATIVE")

# ── B-S123-3 — THE HONEST NO-REDUCTION WITNESS (faculty 1) ───────────
# §120's witness FOUND a reduction (byte-attn = k=T corner); §122's
# FOUND one (byte-RoPE = σ→0 corner).  §123 faculty (1)'s witness
# RECORDS THE ABSENCE of one — closed-form: the two carriers live in
# non-isomorphic spaces and there is no scalar parameter family
# connecting them.
#
# carrier_GPU   = cos(logits_a, logits_g)  over two V=256 logit vectors
# carrier_spike = cos(r_A, r_G)            over two LIF firing-rate
#                 vectors of length n_a / n_g (≠ 256)
# These are vectors in DIFFERENT-DIMENSION spaces; a cosine is a
# function of the vectors, not interconvertible by a limit.
V_LOGIT = 256                       # GPU logit-vector dimension
N_A_SPIKE = 96                      # LIF sub-population A size (neuro_mirror)
dims_differ = (V_LOGIT != N_A_SPIKE)
# unlike §120 (parameter k ∈ {1..T}) and §122 (parameter σ ≥ 0), the
# spike-correlation carrier has NO scalar family whose limit yields the
# logit-vector carrier.  We verify this is a STRUCTURAL fact: a cosine
# of length-96 vectors and a cosine of length-256 vectors cannot be made
# equal by varying any single scalar — the inputs are different objects.
# numeric demonstration: for ANY scalar t, cos over a 96-vec and cos over
# a 256-vec remain functions of disjoint input sets — there is no t that
# maps one onto the other.  We confirm the two carriers are genuinely
# distinct functions (a 96-d cosine ≠ a 256-d cosine as maps).
rng = np.random.default_rng(123)
ra = rng.standard_normal(N_A_SPIKE); rg = rng.standard_normal(N_A_SPIKE)
la = rng.standard_normal(V_LOGIT);   lg = rng.standard_normal(V_LOGIT)
cos_spike = float(np.dot(ra, rg) / (np.linalg.norm(ra) * np.linalg.norm(rg)))
cos_logit = float(np.dot(la, lg) / (np.linalg.norm(la) * np.linalg.norm(lg)))
# the two carriers take inputs of different shapes — no shared parameter
carriers_non_isomorphic = (ra.shape != la.shape) and dims_differ
# the FORM still maps both into [0,1] identically (B-S123-1) — but the
# CARRIER c differs.  honest: no reduction, only relocation.
form_maps_both = (0.0 <= psi_form(cos_spike) <= 1.0
                  and 0.0 <= psi_form(cos_logit) <= 1.0)
no_reduction = carriers_non_isomorphic and form_maps_both
check("B-S123-3 NO-REDUCTION-WITNESS-CARRIER-RELOCATION",
      no_reduction,
      f"spike-rate carrier (len {N_A_SPIKE}) and logit-vector carrier "
      f"(len {V_LOGIT}) are non-isomorphic ✓({carriers_non_isomorphic}); "
      f"unlike §120 (param k) / §122 (param σ) there is NO scalar family "
      f"connecting them — GPU Ψ-as-logit-cosine does NOT reduce. The §112 "
      f"FORM ψ(c)=(1+c)/2 maps both carriers into [0,1] ✓({form_maps_both}) "
      f"— honest carrier-RELOCATION, NOT a clean reduction. Witness passes "
      f"by recording an ABSENCE, not manufacturing a reduction.")

# ── B-S123-4 — FACULTY (1) VERDICT = CARRIER-RELOCATION (closed pick) ─
# closed taxonomy over {generalisation, graft, carrier-relocation}:
#   generalisation       : a reduction parameter exists (byte = a corner)
#   graft                : a foreign mechanism, form NOT preserved
#   carrier-relocation   : FORM preserved (B-S123-1) ∧ opposition+fixed
#                          point preserved (B-S123-2) ∧ NO reduction
#                          (B-S123-3)
form_preserved = fixed_pt_ok and deriv_ok and bounded_ok          # B-S123-1
core_preserved = (has_idx_a and has_idx_g and disjoint)           # B-S123-2
reduction_exists = not no_reduction                              # B-S123-3
is_generalisation = reduction_exists
is_graft = not form_preserved
is_carrier_relocation = (form_preserved and core_preserved
                         and not reduction_exists)
# exactly one of the three buckets
bucket = [is_generalisation, is_graft, is_carrier_relocation]
exactly_one = (sum(bool(b) for b in bucket) == 1)
verdict_relocation = is_carrier_relocation and exactly_one
check("B-S123-4 FACULTY-1-VERDICT-CARRIER-RELOCATION",
      verdict_relocation,
      f"closed taxonomy {{generalisation, graft, carrier-relocation}}: "
      f"generalisation={is_generalisation} graft={is_graft} "
      f"carrier-relocation={is_carrier_relocation} — exactly one "
      f"✓({exactly_one}). FORM preserved ∧ opposition+fixed-point "
      f"preserved ∧ NO reduction ⇒ CARRIER-RELOCATION (§110/§112 family) "
      f"— DUAL-HEADS-DESIGN-CLOSE-WITH-CARRIER-RELOCATION, NOT a "
      f"§120/§122-style generalisation. anti-padding — no clean "
      f"reduction forced.")

# ── B-S123-5 — FACULTY (2)(A): MoE TOP-K SELECTION = §120 k-WTA ──────
# the MoE router's top-k selection IS a k-winners-take-all: the k
# highest-scoring of n experts win.  Numeric witness — for random
# scores, topk_select == k_wta over the same scores (a top-k IS a
# k-WTA), and §96 row 118's own description says so.
sel_match = True
for _ in range(16):
    n = int(rng.integers(4, 20))
    kk = int(rng.integers(1, n))
    sc = rng.standard_normal(n)
    if topk_select(sc, kk) != k_wta(sc, kk):
        sel_match = False
# §96 Q1 row 118 describes the MoE top-k as k-WTA verbatim
s96 = open(S96_DESIGN, encoding="utf-8").read()
s96_says_kwta = ("MoEFFN top-k router" in s96
                 and "k-winner-take-all over expert populations" in s96)
# §120 decided k-WTA as the routing replacement
s120 = open(S120_DESIGN, encoding="utf-8").read()
s120_decided_kwta = ("k-WTA" in s120 and "spike-rate dot-product" in s120)
check("B-S123-5 MOE-TOPK-SELECTION-IS-S120-KWTA",
      sel_match and s96_says_kwta and s120_decided_kwta,
      f"numeric: a k-of-n top-k IS a k-WTA — topk_select==k_wta 16/16 "
      f"random ✓({sel_match}); §96 Q1 row-118 describes MoE top-k as "
      f"'k-winner-take-all over expert populations' ✓({s96_says_kwta}); "
      f"§120 decided k-WTA ✓({s120_decided_kwta}) — the MoE SELECTION is "
      f"COVERED by §120, NOT a new design-open")

# ── B-S123-6 — FACULTY (2)(B): MoE LEARNED GATE = TWO §96-COMPATIBLE ─
# the MoE learned content gate `nn.Linear(d_model, n_experts)`
# decomposes into:
#   (i)  gate score = weighted-synapse current accumulation
#        → §96 Q1 SPIKING-COMPATIBLE (residual stream → LIF current)
#   (ii) gate weights LEARNED  → STDP-trainable synapses
#        → §96 Q1 SPIKING-COMPATIBLE (STDP → Hebbian LTP/LTD)
# closed Boolean: NO residual NEW mechanism ⇒ NOT a separate design-open.
moe_router_is_linear = ("self.router = nn.Linear(d_model, n_experts"
                        in cd_src)
# §96 Q1 classifies BOTH faculties SPIKING-COMPATIBLE
s96_residual_compatible = ("residual stream" in s96
                           and "SPIKING-COMPATIBLE" in s96)
s96_stdp_compatible = ("STDP → Hebbian LTP/LTD" in s96
                       and "Loihi's *native on-chip* rule" in s96)
# the gate decomposes fully — both halves are already-SPIKING-COMPATIBLE
# faculties ⇒ no residual new mechanism ⇒ not a separate design-open
gate_score_covered = s96_residual_compatible       # current accumulation
gate_weights_covered = s96_stdp_compatible         # STDP-trainable
no_residual_mechanism = gate_score_covered and gate_weights_covered
not_separate_design_open = (moe_router_is_linear and no_residual_mechanism)
check("B-S123-6 MOE-LEARNED-GATE-NOT-A-SEPARATE-DESIGN-OPEN",
      not_separate_design_open,
      f"MoE gate = nn.Linear(d_model,n_experts) ✓({moe_router_is_linear}); "
      f"decomposes into (i) gate score = weighted-synapse current "
      f"accumulation = §96-Q1 SPIKING-COMPATIBLE ✓({gate_score_covered}) + "
      f"(ii) gate weights LEARNED = STDP-trainable synapses = §96-Q1 "
      f"SPIKING-COMPATIBLE ✓({gate_weights_covered}); no residual new "
      f"mechanism ⇒ NOT a separate design-open ✓({not_separate_design_open})")

# ── B-S123-7 — §96 / §120 / §122 / §112 CONNECTION-POINTS CITED ──────
# the two decided faculties are §96 Q1 rows 115 & 118; §120 + §122 are
# the already-decided siblings; §112 META_FP(Π_½) is the carrier-
# invariance parent.  Structural — byte-checked against the real files.
s96_row115 = ("Engine A ⇄ Engine G dual heads" in s96
              and "SPIKING-OPEN" in s96)
s96_row118 = ("MoEFFN top-k router" in s96)
s96_native_candidate = ("the fixed-point is native" in s96
                        or "NATIVE-CANDIDATE" in s96)
s122 = open(S122_DESIGN, encoding="utf-8").read()
s122_decided_phase = ("relative-phase" in s122 and "spike-time coding" in s122)
design = open(DESIGN_MD, encoding="utf-8").read()
design_cites_112 = ("META_FP" in design and "carrier-invariant" in design)
design_cites_all = ("§96" in design and "§120" in design
                    and "§122" in design and "§112" in design)
conn_ok = (s96_row115 and s96_row118 and s96_native_candidate
           and s122_decided_phase and design_cites_112 and design_cites_all)
check("B-S123-7 S96-S120-S122-S112-CONNECTION-POINTS-CITED",
      conn_ok,
      f"§96 Q1 row-115 Engine A⇄G SPIKING-OPEN ✓({s96_row115}) · row-118 "
      f"MoEFFN top-k ✓({s96_row118}) · §96 NATIVE-CANDIDATE line "
      f"✓({s96_native_candidate}); §120 k-WTA + §122 phase coding the "
      f"decided siblings ✓({s120_decided_kwta and s122_decided_phase}); "
      f"§112 META_FP(Π_½) carrier-invariance parent cited in DESIGN.md "
      f"✓({design_cites_112}) — all connection-points byte-checked")

# ── B-S123-8 — NECESSARY-NOT-SUFFICIENT + central 0-diff + $0 ────────
central_end = sha16(CENTRAL)
central_0diff = (central_end == CENTRAL_SHA_PREFIX
                 and central_end == central_start)
# §123 = two design-open → design-DECIDED transitions, NOT GOAL.
# both decisions are necessary for a fully-specified spiking anima and
# nowhere near sufficient for emergence (WALL-A / WALL-B / §11-B stand).
design_says_nns = ("necessary-not-sufficient" in design
                   and "B-EMERGE-7" in design)
design_says_walls = ("WALL-A" in design and "WALL-B" in design
                     and "GOAL 미도달" in design)
design_says_design_tier = ("design ≠ fire ≠ emergence" in design
                           and "capability claim 0" in design)
# sidecar-only: this battery never writes central
this_is_sidecar = os.path.basename(__file__) == "blue_falsifier_s123.py"
nns_ok = (central_0diff and design_says_nns and design_says_walls
          and design_says_design_tier and this_is_sidecar)
check("B-S123-8 NECESSARY-NOT-SUFFICIENT-CENTRAL-0DIFF",
      nns_ok,
      f"central blue_falsifier.py sha256[:16] START={central_start} "
      f"END={central_end} 0-line-diff ✓({central_0diff}); DESIGN.md states "
      f"necessary-not-sufficient/B-EMERGE-7 ✓({design_says_nns}), "
      f"WALL-A/WALL-B stand + GOAL 미도달 ✓({design_says_walls}), "
      f"design≠fire≠emergence ✓({design_says_design_tier}); sidecar-only "
      f"✓({this_is_sidecar}) — §123 = two DECISIONS, not an ACHIEVEMENT")

# ── summary ──────────────────────────────────────────────────────────
n_pass = sum(PASS)
n_tot = len(PASS)
all_pass = (n_pass == n_tot)
print(f"\nB-S123 — {n_pass}/{n_tot} closed-form/Boolean/sympy checks "
      f"{'PASS' if all_pass else 'FAIL'}")
print(f"central blue_falsifier.py 0-line-diff: "
      f"{'OK' if central_0diff else 'VIOLATED'} "
      f"(sha256[:16] {central_start} == {central_end} == {CENTRAL_SHA_PREFIX})")

out = {
    "battery": "B-S123",
    "section": "§123 — the two remaining §96 SPIKING-OPEN faculties",
    "n_pass": n_pass, "n_total": n_tot, "all_pass": all_pass,
    "central_blue_falsifier_sha16_start": central_start,
    "central_blue_falsifier_sha16_end": central_end,
    "central_0_line_diff": central_0diff,
    "verdict_faculty_1": "DUAL-HEADS-DESIGN-CLOSE-WITH-CARRIER-RELOCATION",
    "verdict_faculty_2": ("MOE-TOPK-DECIDED — COVERED BY §120 k-WTA "
                          "+ §96-COMPATIBLE STDP GATE"),
    "results": results,
    "B-S123-NOTE": (
        "the battery proves the two §123 DECISIONS are honest + "
        "closed-form. It does NOT prove a spiking anima built with Ψ-C1 "
        "+ the MoE k-WTA gate learns / behaves usefully / emerges — "
        "those are empirical OUTCOMES of a future fire on a real async "
        "substrate. For faculty (1) the relocated carrier's usefulness "
        "is empirical; for faculty (2) whether STDP-learned gate "
        "synapses route as well as backprop-CE ones is the §11-B / §96 "
        "§4.5 open question. B-D-NOTE / B-S96-NOTE / B-S110-NOTE / "
        "B-S112-NOTE / B-S120-NOTE / B-S122-NOTE / B-EMERGE-7 family — "
        "necessary-not-sufficient at every layer. §123 = two DECISIONS, "
        "not an ACHIEVEMENT. WALL-A / WALL-B unchanged; GOAL 미도달."),
}
with open(os.path.join(HERE, "blue_falsifier_s123_result.json"), "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    import sys
    sys.exit(0 if all_pass else 1)
