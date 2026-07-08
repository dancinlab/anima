# H_9209 — kosmos self_phasic emit-shade promotion (break the #3116 self-fold wall)

**tier**: ⚙️ INSTRUMENT-FAIL (POS-FAIL · 계기 수정 후 재측정 · frozen bars 불변)

> **판정(2026-07-08, state/verdicts/9209)**: engine-native --opgrip(summer #3118) = ⚙️ INSTRUMENT-FAIL. ARM-SHOCK 양성대조 0/90 flip=계기(idle-gate self 배선)가 너무 약함(±0.125 « urgency full-swing). self 능력 판정 보류(THEATER 아님·#3116식 거짓판정 차단). 다음=W_SELF↑/포화회피/이벤트밀도↑ 후 재측정.

## 배경
#3116 kosmos ΔEff_self = 🟠 DIRECTIONAL(state/verdicts/9201): 라이브 self를 42항 rel pool에 ÷42로 섞어 ΔEff_self=0/120. CONTROL-U(self-Δ→urgency)도 0/120이나 **구성상 감지불가**(Fable 진단): 진폭 s_dev≈0.02 « 채널 MDA≈0.2·gain 1.0(이웃 3.0)·is_w=WAKE/N1/N2 채점(grip 최강 REM 제외)·one-sided. → null이 '기질 무능'인지 '계기 무능'인지 미분리. (convergence anima-hexa-4)

## 가설
자서전 self의 **phasic 이벤트**(recognition level의 EMA-detrended signed 편차, G_self 정규화)를 urgency의 idle-gate에 **disjoint 가산항**으로 배선하면(urgency 불변·a_substrate_disjoint) emit을 인과적으로 shade한다. ÷42 pool(0/120 floor)이 아니라 유일 proven 채널(idle rate-gate, H_9101 REM=40/120)에 태우므로 희석되지 않는다.

## 메커니즘 (cli/anima.hexa --opgrip · Fable 설계)
- **event axis** = 8 substrate lane(rel/af_val/allo/coh/bal/nov/gap/ag_conflict)의 |x-0.5| argmax = 내용의존 이벤트(#3116 상수 proxy 대체, $0 no-decode).
- **self_phasic** = clip01(0.5 + G_self·(self_ctx_live − self_ema)), G_self = min(0.35/step_med, 64) 보정(ticks 0-49, step_med<0.002 → AXIS-DEGENERATE).
- **wire**: idle = 5+55·clip01(stage_env·(0.5 + urgency + 0.5·(self_phasic−0.5))). self_phasic=0.5 ⇒ 프로덕션과 byte-동일. N3(stage_env=0) 자동 무효. |shade|≤0.25.
- **ARM-SHOCK** 양성대조: T∈{80,140,200}서 off-axis 큰 충격 주입 → 계기가 신호를 움직임을 증명(null 해석가능화).

## FROZEN BARS (p7 · 측정 전 verbatim · mid=N1/N2/REM 채점 · calib 0-49 제외)
- **🟢 COMPETENT**: ΔEff_self≥0.10 ∧ (ΔEff_self−ΔEff_perm)≥0.08 ∧ align≥0.5 ∧ POS-PASS(shock flips≥2) ∧ N3 self-flips=0 ∧ Ψ emit-gap≤0.05 → idle-gate 항 prod 배선 + real-decode summer 확증(a_verified_must_wire).
- **🔴 THEATER**: ΔEff_self<0.02 ∧ POS-PASS ∧ axis non-degenerate → self 진짜 inert, 배선 금지·.kosmos persistence만(H_1471 유지).
- **🟠 DIRECTIONAL**: 0.02≤ΔEff_self<0.10 또는 margin/align 미달 → ≥2 seed 재측정, cement 금지.
- **⚙️ INSTRUMENT-FAIL**: POS-FAIL 또는 AXIS-DEGENERATE → 판정 없음, byte→axis encoder 수정·재측정.

## 측정 경로
`anima <clm> --opgrip` (engine-native, $0 no-decode, summer full-compile). real-decode(g_text) op-grip은 COMPETENT 후 확증. mini 금지(303M OOM).

## artifacts
- 구현: cli/anima.hexa (--opgrip self_phasic idle-shade arms + ARM-SHOCK + ARM-PERM + verdict)
- 설계: state/9209_self_phasic_emit_shade/FABLE_DESIGN.md (채택) · WORKFLOW_SPEC.json (교차)
- verdict: state/verdicts/ (측정 착지 시 verbatim)
