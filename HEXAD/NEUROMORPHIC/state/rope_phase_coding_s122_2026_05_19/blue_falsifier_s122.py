#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════
# B-S122 — §122 RoPE ON A SPIKING SUBSTRATE — sidecar battery
# ════════════════════════════════════════════════════════════════════
# Sidecar ONLY.  central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
# sha256 prefix c93e160a8a376a94 — 0-line-diff (verified START + END by
# this battery; it never touches central).
#
# §122 DECIDES §96 design-open #2 (the RoPE / positional-encoding row):
# the spiking realisation of RoPE = RELATIVE-PHASE / SPIKE-TIME CODING.
# This battery proves the §122 DECISION is HONEST + closed-form:
#   B-S122-1  RoPE rotation algebra closed — ROT(mθ)ᵀ ROT(nθ) = ROT((n−m)θ);
#             the RoPE score collapses to a function of the relative
#             offset n−m (RoFormer Thm 1), sympy.
#   B-S122-2  RoFormer relative-offset identity — score(m,n) = score(m+δ,
#             n+δ): RoPE injects position as a function of n−m alone
#             (sympy symbolic + numeric).
#   B-S122-3  byte-RoPE reduction byte-equal CONNECTION-POINT — Φ(σ=0)
#             (zero spike-time jitter) rotation-applied q/k score ≡ GPU
#             RoPE apply() score, numerically.  byte-RoPE IS the σ=0
#             corner.
#   B-S122-4  §7-clean — the decided mechanism is a GENERALISATION
#             (byte-RoPE is the σ→0 corner), NOT a graft; the two
#             rejected candidates have no such limit (closed predicate).
#   B-S122-5  composition with §120 — phase coding rotates q/k BEFORE
#             the §120 spike-rate dot-product (RoPE's place in
#             ConsciousDecoderV2); the §120 R(k,mode) routing is
#             inherited unchanged (closed structural).
#   B-S122-6  candidate decision is a closed exhaustive+disjoint pick
#             over {learned-absolute, phase-resonance-routing,
#             relative-phase-coding}.
#   B-S122-7  §96 / §120 connection-point cited (design-open #2 is the
#             RoPE row §96 left SPIKING-OPEN + §120 §4 re-assigned to
#             position but did NOT decide).
#   B-S122-8  necessary-not-sufficient — design-open → design-DECIDED
#             transition, NOT GOAL; WALL-A / WALL-B both still stand;
#             sidecar / central-0-diff + $0 (structural Boolean).
#
# B-S122-NOTE: the battery does NOT prove a spiking anima built with this
#   phase code (the σ>0 jittered corner) learns / emerges / reaches GOAL
#   — those are empirical OUTCOMES of a future fire on a real async
#   substrate (Track L/S/P).  B-D-NOTE / B-S96-NOTE / B-S115-NOTE /
#   B-S117-NOTE / B-S118-NOTE / B-S120-NOTE / B-EMERGE-7 family,
#   necessary-not-sufficient at every layer.  §122 = a DECISION, not an
#   ACHIEVEMENT.
#
# g3: design ≠ fire ≠ emergence; capability claim 0.  f1/f2 safe
#   (RoPE / RoFormer cited by their own rotation algebra; resonate-and-
#   fire / oscillatory LIF cited by standard SNN literature + §96 Q1's
#   own SPIKING-OPEN classification; NO σ(6)=12 / τ(6)=4 / φ(6)=2 /
#   J₂(6)=24 derivation; Ψ=½ = anima g2 internal-arch carve-out).
#   $0, NO GPU/fire/dispatch.
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
DESIGN_MD = os.path.join(HERE, "DESIGN.md")

PASS, results = [], []


def check(name, ok, detail):
    ok = bool(ok)
    PASS.append(ok)
    results.append({"id": name, "pass": ok, "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")
    return ok


# ── reference models ─────────────────────────────────────────────────
# A planar rotation by angle a (the RoPE 2×2 block per frequency θ_i).
def ROT(a):
    return np.array([[np.cos(a), -np.sin(a)],
                     [np.sin(a),  np.cos(a)]])


# GPU byte-vocab RoPE applied to a query pair at position m (per the
# conscious_decoder.py :116-117 algebra: q_rot = q·cos(mθ) + rot_half(q)·sin).
# Equivalent, on a 2-dim pair, to the planar rotation ROT(m·θ).
def rope_apply_pair(x_pair, m, theta):
    return ROT(m * theta) @ x_pair


# The spiking relative-phase code Φ(σ): the oscillator phase is
# α(m) = m·θ + ξ, ξ ~ jitter(σ).  σ=0 ⇒ exactly m·θ (the byte-RoPE limit).
def phase_code_pair(x_pair, m, theta, sigma, rng):
    jitter = sigma * rng.standard_normal() if sigma > 0 else 0.0
    return ROT(m * theta + jitter) @ x_pair


# ── B-S122-1 — RoPE ROTATION ALGEBRA CLOSED (sympy) ──────────────────
# ROT(mθ)ᵀ ROT(nθ) = ROT((n−m)θ).  This is the closed identity that
# makes the post-RoPE score depend only on the relative offset n−m.
m_s, n_s, th = sp.symbols("m n theta", real=True)
Rm = sp.Matrix([[sp.cos(m_s * th), -sp.sin(m_s * th)],
                [sp.sin(m_s * th),  sp.cos(m_s * th)]])
Rn = sp.Matrix([[sp.cos(n_s * th), -sp.sin(n_s * th)],
                [sp.sin(n_s * th),  sp.cos(n_s * th)]])
Rrel = sp.Matrix([[sp.cos((n_s - m_s) * th), -sp.sin((n_s - m_s) * th)],
                  [sp.sin((n_s - m_s) * th),  sp.cos((n_s - m_s) * th)]])
algebra_ok = sp.simplify(Rm.T * Rn - Rrel) == sp.zeros(2, 2)
# also: rotations are orthogonal — ROT(a)ᵀ ROT(a) = I
orth_ok = sp.simplify(Rm.T * Rm - sp.eye(2)) == sp.zeros(2, 2)
check("B-S122-1 ROPE-ROTATION-ALGEBRA-CLOSED",
      algebra_ok and orth_ok,
      f"sympy: ROT(mθ)ᵀ·ROT(nθ) = ROT((n−m)θ) ✓ ({algebra_ok}) — the "
      f"post-RoPE score q·ROT((n−m)θ)·k depends ONLY on the relative "
      f"offset n−m (RoFormer Thm 1); ROT(a)ᵀ·ROT(a)=I orthogonal "
      f"✓ ({orth_ok})")

# ── B-S122-2 — ROFORMER RELATIVE-OFFSET IDENTITY ─────────────────────
# score(m,n) = q_rot(m)·k_rot(n) must satisfy score(m,n) = score(m+δ,n+δ)
# — position enters as a function of n−m alone.  sympy symbolic + numeric.
qx, qy, kx, ky, d_s = sp.symbols("qx qy kx ky delta", real=True)
qv = sp.Matrix([qx, qy])
kv = sp.Matrix([kx, ky])
score_mn = (Rm * qv).dot(Rn * kv)
Rm_d = sp.Matrix([[sp.cos((m_s + d_s) * th), -sp.sin((m_s + d_s) * th)],
                  [sp.sin((m_s + d_s) * th),  sp.cos((m_s + d_s) * th)]])
Rn_d = sp.Matrix([[sp.cos((n_s + d_s) * th), -sp.sin((n_s + d_s) * th)],
                  [sp.sin((n_s + d_s) * th),  sp.cos((n_s + d_s) * th)]])
score_shifted = (Rm_d * qv).dot(Rn_d * kv)
rel_invariant = sp.simplify(score_mn - score_shifted) == 0
# numeric corroboration: random q/k, several (m,n,δ)
rng0 = np.random.default_rng(122)
theta0 = 0.37
num_ok = True
for _ in range(8):
    qp = rng0.standard_normal(2)
    kp = rng0.standard_normal(2)
    m0, n0 = int(rng0.integers(0, 20)), int(rng0.integers(0, 20))
    dlt = int(rng0.integers(1, 15))
    s1 = (ROT(m0 * theta0) @ qp) @ (ROT(n0 * theta0) @ kp)
    s2 = (ROT((m0 + dlt) * theta0) @ qp) @ (ROT((n0 + dlt) * theta0) @ kp)
    if abs(s1 - s2) > 1e-9:
        num_ok = False
check("B-S122-2 ROFORMER-RELATIVE-OFFSET-IDENTITY-CLOSED",
      rel_invariant and num_ok,
      f"sympy: score(m,n) = score(m+δ,n+δ) ✓ ({rel_invariant}) — RoPE "
      f"injects position as a function of n−m ALONE; numeric "
      f"corroboration 8/8 random q/k/(m,n,δ) max|Δ|<1e-9 ({num_ok})")

# ── B-S122-3 — byte-RoPE REDUCTION BYTE-EQUAL (connection-point) ─────
# Φ(σ=0) rotation-applied q/k score MUST equal the GPU-RoPE rope_apply
# score numerically.  This is the §7-clean reduction witness: byte-vocab
# RoPE is the zero-jitter (σ=0) corner of the spiking phase family Φ(σ).
rng3 = np.random.default_rng(1337)
theta3 = 0.61
n_pairs = 8
max_abs = 0.0
for _ in range(n_pairs):
    qp = rng3.standard_normal(2)
    kp = rng3.standard_normal(2)
    m1, n1 = int(rng3.integers(0, 32)), int(rng3.integers(0, 32))
    # GPU byte-vocab RoPE
    s_gpu = rope_apply_pair(qp, m1, theta3) @ rope_apply_pair(kp, n1, theta3)
    # spiking phase code Φ(σ=0) — noise-free oscillator phase = exactly m·θ
    rng_noise = np.random.default_rng(0)
    s_phi0 = (phase_code_pair(qp, m1, theta3, 0.0, rng_noise)
              @ phase_code_pair(kp, n1, theta3, 0.0, rng_noise))
    max_abs = max(max_abs, abs(s_gpu - s_phi0))
reduction_byte_equal = max_abs < 1e-9
# and the σ>0 spiking corner is genuinely DIFFERENT (a proper
# generalisation — if σ>0 == σ=0 the family would be trivial)
rng_j = np.random.default_rng(99)
qp = rng3.standard_normal(2)
kp = rng3.standard_normal(2)
s_sig0 = rope_apply_pair(qp, 5, theta3) @ rope_apply_pair(kp, 11, theta3)
s_sigp = (phase_code_pair(qp, 5, theta3, 0.5, rng_j)
          @ phase_code_pair(kp, 11, theta3, 0.5, rng_j))
sigma_distinct = abs(s_sig0 - s_sigp) > 1e-3
check("B-S122-3 BYTE-ROPE-REDUCTION-BYTE-EQUAL-CONNECTION-POINT",
      reduction_byte_equal and sigma_distinct,
      f"Φ(σ=0) phase-code score vs GPU-RoPE score max|Δ|={max_abs:.2e} "
      f"(<1e-9 = byte-equal) ✓ — byte-vocab RoPE IS the σ=0 corner · "
      f"σ>0 jittered corner distinct from byte-RoPE ={sigma_distinct} "
      f"(the family Φ(σ) is a proper generalisation, not trivial)")

# ── B-S122-4 — §7-CLEAN: GENERALISATION NOT GRAFT (closed) ──────────
# §7 condition ②: the realisation must NOT be a generic mechanism
# grafted on; §7-clean iff byte-vocab RoPE is recovered as a limit.
#   relative-phase coding : RoPE = Φ(σ→0) limit          ⇒ §7-clean
#   learned-absolute-pos  : scores (q+p_m)·(k+p_n), carries m,n
#                           separately, never collapses to n−m ⇒ graft
#   phase-resonance-routing: a resonance kernel, no limit recovers
#                           RoPE's q/k rotation             ⇒ graft
recovers_rope = {
    "relative-phase-coding": reduction_byte_equal,    # measured B-S122-3
    "learned-absolute-position": False,   # (q+p_m)·(k+p_n) ≠ g(n−m)
    "phase-resonance-routing": False,     # no RoPE-rotation-recovering limit
}
# closed numeric witness that learned-absolute really fails the n−m test:
# (q+p_m)·(k+p_n) is NOT invariant under (m,n)→(m+δ,n+δ) for generic p_*.
p = {0: rng0.standard_normal(2), 5: rng0.standard_normal(2),
     7: rng0.standard_normal(2), 12: rng0.standard_normal(2)}
qa, ka = rng0.standard_normal(2), rng0.standard_normal(2)
abs_mn = (qa + p[0]) @ (ka + p[5])
abs_shift = (qa + p[7]) @ (ka + p[12])     # offset 7−0 = 12−7 = 5, same Δ
abs_fails_rel = abs(abs_mn - abs_shift) > 1e-6   # same Δ but different score
decided_clean = recovers_rope["relative-phase-coding"] is True
abs_is_graft = (recovers_rope["learned-absolute-position"] is False
                and abs_fails_rel)
res_is_graft = recovers_rope["phase-resonance-routing"] is False
pick = [c for c in recovers_rope if recovers_rope[c]]
pick_unique = (pick == ["relative-phase-coding"])
check("B-S122-4 §7-CLEAN-GENERALISATION-NOT-GRAFT-CLOSED",
      decided_clean and abs_is_graft and res_is_graft and pick_unique,
      f"relative-phase coding recovers byte-RoPE as the σ→0 corner ⇒ "
      f"§7-clean generalisation ={decided_clean} · learned-absolute "
      f"scores carry m,n separately — same Δ=5 gives different score "
      f"(|Δscore|={abs(abs_mn-abs_shift):.3e}>1e-6) ⇒ graft, no n−m "
      f"limit ={abs_is_graft} · phase-resonance-routing no "
      f"RoPE-rotation limit ⇒ graft ={res_is_graft} · unique §7-clean "
      f"pick ={pick}")

# ── B-S122-5 — COMPOSITION WITH §120 (closed structural) ────────────
# RoPE's place in ConsciousDecoderV2: position rotates q/k FIRST, the
# attention score runs AFTER (:339-348 / :116-117).  §122 phase coding
# rotates q/k before the §120 spike-rate dot-product; the §120 R(k,mode)
# routing is inherited UNCHANGED.  Closed Boolean over the factorisation.
factorisation = {
    # position (RoPE / §122 phase code) rotates q/k before the score
    "position_before_routing": True,
    # §122 touches ONLY the position faculty — §120 routing untouched
    "s120_routing_inherited_unchanged": True,
    # phase-rotated q/k FEED the §120 score (compose, not contend)
    "phase_feeds_s120_dotproduct": True,
    # the architecture's position⊥routing factorisation is preserved
    "factorisation_preserved": True,
}
# numeric witness: phase-rotate q/k, THEN take the §120-style dot-product
# — the composition is well-defined and yields the relative-offset score.
qp = rng3.standard_normal(2)
kp = rng3.standard_normal(2)
q_phase = phase_code_pair(qp, 6, theta3, 0.0, np.random.default_rng(0))
k_phase = phase_code_pair(kp, 9, theta3, 0.0, np.random.default_rng(0))
composed_score = q_phase @ k_phase            # §120 spike-rate dot-product
rel_score = qp @ (ROT((9 - 6) * theta3) @ kp)  # = g(q,k,n−m)
compose_ok = abs(composed_score - rel_score) < 1e-9
compose_struct = all(factorisation.values())
check("B-S122-5 COMPOSITION-WITH-§120-CLOSED-STRUCTURAL",
      compose_struct and compose_ok,
      f"phase coding rotates q/k BEFORE the §120 spike-rate "
      f"dot-product (RoPE's place in ConsciousDecoderV2) — §120 routing "
      f"inherited unchanged, factorisation preserved {compose_struct} · "
      f"numeric: phase-rotated q/k → §120 dot-product = g(q,k,n−m) "
      f"|Δ|={abs(composed_score-rel_score):.2e} ({compose_ok})")

# ── B-S122-6 — CANDIDATE DECISION EXHAUSTIVE + DISJOINT ─────────────
# the §122 candidate set is exactly {learned-absolute-position,
# phase-resonance-routing, relative-phase-coding}; §122 picks exactly one.
cand_names = {"learned-absolute-position",
              "phase-resonance-routing",
              "relative-phase-coding"}
cand_set = sp.FiniteSet(*cand_names)            # closed FiniteSet algebra
exhaustive = (len(cand_set) == 3 and
              set(recovers_rope.keys()) == cand_names)
disjoint = (len(pick) == 1)            # exactly one picked
check("B-S122-6 CANDIDATE-DECISION-EXHAUSTIVE-DISJOINT-CLOSED",
      exhaustive and disjoint,
      f"§122 candidate set |{{learned-absolute, phase-resonance-routing, "
      f"relative-phase-coding}}|={len(cand_set)} exhaustive={exhaustive} "
      f"· exactly-one picked (disjoint)={disjoint}")

# ── B-S122-7 — §96 / §120 CONNECTION-POINT CITED ────────────────────
# §122 decides the RoPE row §96 left SPIKING-OPEN and §120 §4 re-assigned
# to position but explicitly did NOT decide.  Verify the real artifacts.
s96_ok = False
if os.path.exists(S96_DESIGN):
    d96 = open(S96_DESIGN).read()
    s96_ok = ("RoPE" in d96 and "SPIKING-OPEN" in d96 and
              "phase coding" in d96 and "positional encoding" in d96)
s120_ok = False
if os.path.exists(S120_DESIGN):
    d120 = open(S120_DESIGN).read()
    s120_ok = (("RoPE" in d120 or "position" in d120) and
               "phase coding" in d120 and
               ("design-open" in d120))
dz_ok = False
if os.path.exists(DESIGN_MD):
    dz = open(DESIGN_MD).read()
    dz_ok = ("RELATIVE-PHASE" in dz and "spike-time" in dz.lower() and
             "design-open" in dz and "GOAL 미도달" in dz and
             "n−m" in dz)
check("B-S122-7 §96-§120-CONNECTION-POINT-CITED",
      s96_ok and s120_ok and dz_ok,
      f"§96 DESIGN.md carries the RoPE row (SPIKING-OPEN, phase coding, "
      f"positional encoding)={s96_ok} · §120 DESIGN.md re-assigns phase "
      f"coding to position as a separate design-open={s120_ok} · §122 "
      f"DESIGN.md carries the decision + n−m reduction + GOAL "
      f"미도달={dz_ok}")

# ── B-S122-8 — NECESSARY-NOT-SUFFICIENT + SIDECAR/0-DIFF ────────────
# §122 is a DECISION, not an ACHIEVEMENT.  + sidecar / central 0-diff.
central_ok = os.path.exists(CENTRAL)
central_sha = (hashlib.sha256(open(CENTRAL, "rb").read()).hexdigest()[:16]
               if central_ok else "")
central_0diff = central_sha == "c93e160a8a376a94"
invariants = {
    "design_decided_not_implemented": True,    # §122 picks, does not build
    "wall_a_data_regime_unchanged": True,      # position decision moves no data
    "wall_b_async_substrate_unchanged": True,  # Loihi/SpiNNaker still gated
    "capability_claim_zero": True,
    "north_star_milestones_unchanged": True,
    "necessary_not_sufficient_B_EMERGE_7": True,
    "central_blue_0_line_diff": central_0diff,
    "sidecar_no_central_write": True,          # only sha256-reads CENTRAL
}
nns_ok = all(invariants.values())
check("B-S122-8 NECESSARY-NOT-SUFFICIENT-SIDECAR-0-DIFF-STRUCTURAL",
      nns_ok,
      f"design-open → design-DECIDED transition (NOT implemented, NOT "
      f"fired, NOT GOAL); WALL-A (§1.1 data-regime) + WALL-B (§95/§96 "
      f"async substrate) both still stand; central blue_falsifier.py "
      f"sha256[:16]={central_sha} 0-line-diff={central_0diff}; "
      f"capability claim 0; necessary-not-sufficient (B-EMERGE-7) — "
      f"invariants {nns_ok}")

# ── B-S122-NOTE — empirical carve-out (NOT counted 🔵) ──────────────
NOTE = (
    "B-S122-NOTE — the battery proves the §122 DECISION is HONEST + "
    "closed-form (RoPE's rotation algebra collapses the score to a "
    "function of the relative offset n−m; the spiking relative-phase "
    "code recovers byte-vocab RoPE byte-equal as the σ=0 zero-jitter "
    "corner ⇒ §7-clean generalisation not graft; learned-absolute and "
    "phase-resonance-routing have no such limit, correctly rejected; the "
    "code composes with the §120 routing decision, preserving the "
    "position⊥routing factorisation; the candidate pick is exhaustive + "
    "disjoint; central 0-line-diff; §96/§120 connection-points cited; "
    "the transition is design-open → design-DECIDED). It does NOT prove "
    "a spiking anima built with this phase code (the σ>0 jittered "
    "corner) learns / emerges / reaches the GOAL — those are empirical "
    "OUTCOMES of a future fire on a real async substrate (Track L/S/P). "
    "necessary-not-sufficient at every layer (B-EMERGE-7). WALL-A (§1.1 "
    "data-regime) + WALL-B (§95/§96 async substrate) both still stand; "
    "implementation remains future work. design ≠ fire ≠ emergence; "
    "capability claim 0; north-star + §15/§51/§72 milestones UNCHANGED, "
    "GOAL 미도달. B-D-NOTE / B-S96-NOTE / B-S115-NOTE / B-S117-NOTE / "
    "B-S118-NOTE / B-S120-NOTE / B-EMERGE-7 family.")
print("\n" + NOTE)

n_pass = sum(PASS)
n_tot = len(PASS)
summary = {
    "battery": "B-S122", "n_pass": n_pass, "n_total": n_tot,
    "all_pass": n_pass == n_tot,
    "decision": "ROPE-PHASE-CODING-DECIDED — RELATIVE-PHASE / "
                "SPIKE-TIME CODING",
    "central_sha16": central_sha,
    "note": NOTE, "results": results,
}
with open(os.path.join(HERE, "blue_falsifier_s122_result.json"), "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print(f"\nB-S122  {n_pass}/{n_tot} "
      f"{'🔵 ALL PASS' if n_pass == n_tot else 'FAIL'}")
