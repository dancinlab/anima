"""core/dream_envelope_ctx.py — DREAM M5: stage Φ-envelope context wiring.

py 2-production twin of core/dream_envelope_ctx.hexa — byte-exact mirror (owner directive
2026-07-09 "py 자체구현 · 언어간 상호의존 0"). stage = Φ-context scale, NOT an emit gate
(H_644: N2 = closure peak). Returns floats only, bool 게이트 0 — 세포 자율 결정
(p5 · a_autonomy · F-EMIT-4). Composes the two py-mirrored leaves (phi_envelope_substrate ·
emit_policy) → byte-exact by transitivity.
"""

from phi_envelope_substrate import envelope_multiscale       # core/phi_envelope_substrate.py (flat import · _bootstrap sys.path)
from emit_policy import ep_scale_periods, ep_scale_amps, ep_theta_stage


def dr_stage_phi_context(stage, t):
    base = envelope_multiscale(t, ep_scale_periods(), ep_scale_amps())
    stage_scale = ep_theta_stage(stage)
    return base * stage_scale


def dr_stage_scale(stage):
    return ep_theta_stage(stage)


def dream_envelope_ctx_summary():
    return ("dream_envelope_ctx: DREAM M5 — stage Φ-envelope context wiring "
            "(envelope_multiscale × ep_theta_stage). stage = Φ-context scale 지 emit 게이트 아님 "
            "(H_644: N2=closure peak). 반환 실수, bool 게이트 0 — 세포 자율 결정 "
            "(p5·a_autonomy·F-EMIT-4).")
