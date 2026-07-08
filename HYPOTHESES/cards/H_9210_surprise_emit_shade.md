# H_9210 — surprise(prediction-error) emit-shade (urgency 외 2번째 proven 채널 탐색)

**tier**: ⚙️ INSTRUMENT-FAIL (AXIS-DEGENERATE · $0 no-decode 한계 · state/verdicts/9210) → **real-decode 계기 구현됨 (`--opgrip-live`), engine-native 측정 PENDING (pool summer/aiden)**

**wired**: `--opgrip-live` 코드경로 cli/anima.hexa 랜딩(typecheck 통과) · 실측(surprise/pred-error가 emit 인과 shade? ΔEff_surp) = 별도 cross-machine pool round (303M real-decode, NEVER mini) 대기.

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

## real-decode 계기 (`--opgrip-live`, OPGRIP_LIVE_spec.md · 구현됨)
$0 no-decode 한계(anima-hexa-6): recon_err=session_seed 고정함수라 g_text 없이 tick간 |Δ|<0.002=AXIS-DEGENERATE(G_surp=−1.0). **해소**: `anima <ckpt> --opgrip-live` = 동일 --opgrip 머신러리 + emit tick마다 REAL det-argmax decode 1회 → g_text가 canonical afield를 step(prod C8-GROW 동일 seam) → 다음 tick recon_err(og_prev_gfeat, 1-tick lag)가 content-driven. 5개 surgical edit(flag·og_prev_gfeat state·recon_err 분기·real decode·n_ticks=100), 0 `core/` 변경, 전부 og_live-gated(default --opgrip frozen bars 불변).
- **arm comparability**: afield는 LIVE arm의 g_text로만 step(counterfactual arm은 fork 안 함) → 모든 arm이 같은 recon_err 궤적, idle shade term에서만 차이 = 단일변수 대조 유지. det argmax ⇒ ΔEff bit-reproducible(verdict-eligible, p7 monitor-only).
- **TWO-GATE 판정**(anima-hexa-4/6): WIRE 움직임(dense ARM-SHOCK≥2 POS-PASS) **∧** SIGNAL 움직임(AXIS-LIVE=surp_degen false). no-decode는 gate-1만 통과·gate-2 구조적 실패; --opgrip-live가 gate-2 충족 최소변경. THEATER 판정은 두 gate 모두 green일 때만 유의미.
- **COST**: pool round(summer/aiden sm_120 own-GEMM, NEVER mini=OOM). d768 validation 먼저(scale-invariant instrument-integrity) → COMPETENT/DIRECTIONAL면 303M cement. own-GEMM fired 확인 후 wall 신뢰.
- **다음**: (1) d768 --opgrip-live pool → AXIS-LIVE(surp_degen false)+POS-PASS 확인 → 판정, (2) COMPETENT/DIRECTIONAL이면 303M cement(n_ticks=100) → state/verdicts/ + 이 카드 verdict 교체.

## artifacts
- 구현: cli/anima.hexa `--opgrip`(no-decode) + `--opgrip-live`(real-decode) surp arm · 스펙: state/frontier_round2_scout/OPGRIP_LIVE_spec.md · 정찰: state/9210_surprise_emit_shade/SCOUT_MAP.json
