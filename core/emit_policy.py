"""core/emit_policy.py — free-number policy SSOT (emit-substrate 숫자 층).

py 2-production twin of core/emit_policy.hexa — byte-parity mirror (a_eval_py_canonical,
owner directive 2026-07-09 "py 자체구현 · 언어간 상호의존 0": the py channel must run the
consciousness daemon fully in numpy with ZERO hexa dependency). Every value here is
IDENTICAL to the hexa twin — a pure-number SSOT (no GPU/FFI, no state), so this mirror is
byte-exact by construction. Design SSOT: core/EMIT_SUBSTRATE_DESIGN.md §3.

Single tunable source for every DESIGN-CONVENTION number in anima's emit policy. Every value
carries substrate-claim: NONE — UNIVERSE verified substrate-Φ variance = 0, freedom [0,1]
(H_646 🟢, H_651 🟢 6/6; H_651 strong form: even Ψ-clamp α, which moves the gate 0.556 →
0.683, leaves Φ flat — a number that moves policy is still substrate-safe / NON-DEFINITIONAL).

F-EMIT-5 (POLICY-FREE): the structure layer (phi_envelope_substrate) does NOT import this —
changing any value here cannot alter envelope/collective structure (compile-level decoupling).
F-EMIT-4 (NO-GATE): returns plain numbers only — no bool emit gate, no "stage = forbidden".
The anima substrate decides emit/silence autonomously (p5 · a_autonomy).
"""

# ── emit thresholds (H_646/651: substrate-Φ variance=0 · freedom [0,1]) ──
def ep_emit_threshold():      return 0.60    # substrate-claim: none
def ep_emit_threshold_lo():   return 0.30    # H_632 ⊥ Φ phase-transition
def ep_target_emit_rate():    return 0.27    # H_637 · substrate-claim: none
def ep_psi_clamp():           return 0.10    # Ψ=1/2 clamp · H_651 α moves gate, Φ flat
def ep_tension_amplitude():   return 1.00    # H_639 · convention


# ── curiosity-backlog accumulator params (H_9091 · substrate-claim: none) ──
# The persistent unresolved-novelty accumulator (engine_cli §CuriosityBacklog) is a READ
# input to emit-propensity — additive alongside the M×W×Φ lane drive, NOT a hardcoded
# emit_allowed boolean (a_autonomy_over_hardcode). These shift emit TIMING but never touch
# Ψ ci_emit_drive lane 0/4 (F5 disjointness).
def ep_backlog_weight():   return 0.30    # additive weight of backlog pressure into propensity
def ep_backlog_accrual():  return 0.02    # per-idle-tick accrual gain on unresolved novelty
def ep_backlog_decay():    return 0.25    # retained fraction on emit/mention (0=full discharge)


# ── forward-model rerank params (H_9115/9117 §2 · substrate-claim: none) ──
# The cerebellar forward-model (engine_cli §FORWARD-MODEL) scores mouth-gate candidates by
# PREFIX front-loading — how early the discriminative content wins for an external listener
# (H_9117: filler-prefix onset predicts oracle-decodability r=0.69). Touch only WHICH
# candidate exits — never Ψ ci_emit_drive lane 0/4 (F5 disjointness).
def ep_fm_candidates():     return 8.0     # best-of-K mouth-gate rerank breadth (floor at use)
def ep_fm_prefix_bytes():   return 8.0     # prefix window scored for front-loading
def ep_fm_margin():         return 0.15    # target-vs-distractor win margin τ
def ep_fm_prefix_decay():   return 0.75    # front-byte geometric weight (early bytes dominate)


# ── multi-scale envelope params (shape=substrate · numbers=free) ──
# parallel arrays for envelope_multiscale(t, periods, amps). gamma(1) ⊂ ultradian(5400=90min)
# ⊂ circadian(86400). shape is self-similar (H_648, class-IV) — periods/amps are the tunable
# numbers only.
def ep_scale_periods():  return [1.0, 5400.0, 86400.0]
def ep_scale_amps():     return [0.10, 1.0, 0.50]


# ── stage θ_emit table (DREAM 5-stage · θ = context scale, NOT a gate) ──
# stage int: 0=WAKE 1=N1 2=N2 3=N3 4=REM. H_644 correction: closure peak = N2. θ is a
# Φ-context scale the substrate reads — NOT a per-stage emit_allowed boolean
# (a_chat_sleep_imagination · a_autonomy_over_hardcode).
def ep_theta_stage(stage):
    if stage == 0: return 0.10    # WAKE
    if stage == 1: return 0.08    # N1
    if stage == 2: return 0.05    # N2 — closure peak (H_644)
    if stage == 3: return 0.02    # N3
    if stage == 4: return 0.08    # REM
    return 0.10


# ── substrate-class coupling (H_653 · bridges to phi_envelope_substrate) ──
# Mirror of pe_coupling_for_class anchor — convexity span ratio monotone in CA class
# (II 12.1 < III 30.4 < IV 35.5), normalized. Tunable magnitude, but the monotone ORDER is
# substrate (H_653 🟢), not free.
def ep_coupling_for_class(class_id):
    if class_id == 2: return 0.341    # II  : 12.1 / 35.5
    if class_id == 3: return 0.856    # III : 30.4 / 35.5
    if class_id == 4: return 1.000    # IV  : 35.5 / 35.5
    return 0.5


def emit_policy_summary():
    return ("emit_policy: free-number SSOT (숫자 층). 모든 값 substrate-claim:none "
            "(H_646/651 자유도 [0,1]). 구조 lib 가 본 파일 import 안 함 = F-EMIT-5 decoupling. "
            "bool 게이트 0 = F-EMIT-4.")
