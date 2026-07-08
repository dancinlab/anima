# H_9210 — surprise(prediction-error) emit-shade (urgency 외 2번째 proven 채널 탐색)

**tier**: ⏳ PRE-REGISTERED (측정 대기)

## 배경
σ de-theater 종결(anima-hexa-5): emit shade 유일 proven 채널=urgency(phasic Δ→idle). 정찰(state/9210 SCOUT_MAP)이 urgency 외 후보 5개 census — #1 최고 grip = **SURPRISE/예측오차(recon_err)**: urgency가 흉내낸 LC-NE 버스트의 실체인데 현재 cur_ctx ÷18 pool에 1/18 희석돼 자기 term 아님.

## 가설
surprise phasic Δ(recon_err의 EMA-detrended 편차, G_surp 정규화)를 proven idle seam에 **disjoint 가산항**으로 배선하면 emit을 인과 shade한다. read-side pool도 자서전도 아닌 별개 phasic 신호이므로 anima-hexa-5의 dead-lever가 아님(새 후보 채널 검증).

## 메커니즘 (cli/anima.hexa --opgrip · H_9209 scaffold clone)
- surp_phasic = clip01(0.5 + G_surp·(recon_err − surp_ema)), G_surp = min(0.175/median,32) 보정(ticks 0-49).
- idle_surp = 5+55·clip01(stage_env·(0.5 + urgency + (surp_phasic−0.5))). urgency 불변(a_substrate_disjoint). surp_phasic=0.5 ⇒ prod byte-동일·N3 자동무효.
- POS-PASS = dense ARM-SHOCK(같은 idle wire, H_9209서 45/90 확증) 재사용.

## FROZEN BARS (p7 · mid=N1/N2/REM 채점)
- 🟢 COMPETENT: ΔEff_surp≥0.10 ∧ margin(perm)≥0.08 ∧ POS-PASS ∧ N3=0 → **2번째 proven emit 채널**·배선 후보.
- 🔴 THEATER: ΔEff_surp<0.02 ∧ POS-PASS → urgency만 유일 채널 재확인.
- 🟠 DIRECTIONAL 0.02~0.10 · ⚙️ INSTRUMENT-FAIL POS-FAIL∨degenerate.

## artifacts
- 구현: cli/anima.hexa --opgrip surp arm · 정찰: state/9210_surprise_emit_shade/SCOUT_MAP.json
