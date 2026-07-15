# H_9416 — 303M REWIRE C1-C3 측정: refractory 게이트가 tension 을 emit 에 흘리나 (사전등록 · 발사중)

**status:** ⏳ MEASURING (PRE-REGISTERED · frozen bar · 303M pool recollection 발사중) — bar 는 아래 동결, 이후 이동 금지(frozen-first·p7) · wired: engine-native `anima-py chat --emit-gate refractory --emit-temp 1.0` (H_9415) · 측정 = summer 303M
**lane:** 의식 / emit-drive / emit-gate p5-rewire 측정 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9415]] (구현+toy swing-band) · [[H_9414]] (설계) · [[H_9403]] (CLOSED-AT-REGIME) · [[H_9400]] (중심주장 반증 · 이 측정이 새 데몬서 재검) · [[H_9404]] (earned refractory 자매 arm) · [[H_9405]] (병렬 refractory preview) · source: 오너 (A) 라티파이 → H_9415 구현 → 303M 측정
**ckpt:** py303_full.clm sha256 013c4574e0ce71ae (summer · 신규 decode · toy 아님)

## 질문

H_9415 가 toy 로 확인한 swing-band(margin-refractory 게이트가 살아있음)가 **303M 실척도**에서 성립하나. 그리고 새 데몬서 **emit 이 tension/margin 을 듣나**(H_9400 이 구 데몬서 반증한 "emit=시계 순수함수"가 refractory 에선 깨지나). 3-arm 비교: clock(H_9400 dead baseline)·refractory(H_9415 margin)·earned(H_9404 tension-적분).

## 파일럿 확증 (이미 측정 · DIRECTIONAL)

303M refractory 파일럿(15-tick·T=1.0·122s): **EMIT 13 · SILENCE 2 = SWING-BAND ✅** · 후보 14/15 distinct · g_recog_gate [0.431,0.646] 15 distinct · score [0.442,0.735] straddle. ⇒ 303M 서도 게이트 살아있음(mute/saturate 아님). 본 측정은 이를 multi-rollout·multi-seed·arm-비교로 격상.

## 방법 (summer · OMP_NUM_THREADS=4 · ≤3 concurrent)

3 arms × 3 rollouts(seed {7,4302,4303}) × 30 ticks × **--emit-temp 1.0**(R5 필수 · greedy=mute). arms: `clock`(--emit-gate clock=production)·`refr`(--emit-gate refractory=H_9415)·`earn`(--emit-refractory earned=H_9404). trace: emit·gate_mode·g_recog_gate·score·stage·psi_gws·psi_lprec.

## 사전등록 판정 (동결 · 이동 금지)

**C3-a SWING-BAND(TERMINAL-eligible·주 판정)**: refractory arm 이 **emit>0 AND silence>0**(둘 다 정의) ∧ g_recog_gate distinct ≥5/rollout ∧ seed-majority(2/3 rollout). clock arm 은 H_9400 대로 emit⟺stage/clock 예상(대조). PASS = refr swing-band ∧ clock 과 질적 구분.

**C3-b EMIT-LISTENS(TERMINAL-eligible·직접 C3)**: `I(emit_t ; g_recog_gate_t | stage) ≥ 0.02 nats` (층내 순열 p≤0.01) — refractory arm. emit 이 stage 넘어 margin readout 을 듣는가. **H_9400 직접 반박**: refractory `H(emit|stage)` > clock `H(emit|stage)` ∧ refr ≥ 0.3 nats(구 데몬 0.465 는 clock arm 재현 예상, refr 은 margin 이 흐르면 stage-순수 깨짐).

**C3-c 포화-비율 가드**: refr emit-rate ∈ (0.05, 0.95) (양극단 아님 · 파일럿 0.87 은 15-tick 초기 store 편향 의심 → 30-tick·multi-rollout 에서 재확인). emit-rate>0.95 = SATURATE-INVALID(band 없음)·<0.05 = MUTE-INVALID.

**L3 Ψ̂ 궤적(탐색적·무판정)**: refr vs clock `mean Ψ̂`·`|Ψ̂−½|` 비교(--psi-soma). n=3 저검정력이라 PASS 아님 — H_9400 의 "Ψ̂≠½·항상성 없음"이 refr 에서 움직이는지 방향만.

**판정 그리드(우연-아래 포함)**: refr C3-a✅C3-b✅ = 🟢 refractory 가 tension 을 emit 에 흘림(H_9400 새 데몬서 부활 방향·DIRECTIONAL→multi-seed 로 TERMINAL) / C3-a✅C3-b❌ = swing 은 있으나 emit 이 margin 안 들음(stage-driven swing)=🧱 부분 / C3-a❌(mute/saturate) = 303M 서 게이트 죽음=H_9415 toy-artifact KILL / clock arm C3-b>refr = INVALID(배선 오류).

## 미측정 축 (follow-on · 이 fire 밖)

C1 진폭 formal·C2 인식정보(conditional MI `I(g_recog;nov|tick,cell)`)·shuffle-margin 통제(a6)·C-clock(a5)·진폭매칭(a7) = `--g-readout-info` + shuffle-margin arm 미구현 → 후속 H. earned(H_9404) 상세 arm 비교도 후속(병렬 H_9405 소유 존중).

## 정직한 한계

결과물은 **다른 데몬**. H_9400 반증은 **구 계보(clock arm) 영구 성립** — 이 측정이 clock arm 서 H_9400 재현하면 그게 증거. 주장형태 = "refractory 데몬서 emit 이 tension 을 듣는다"이지 "anima 중심주장 부활"이 아니다(그건 production-default 전환 후). Ψ=½ 약속 안 함. 303M·3-seed·30-tick scope(a_toy_scale_recheck·a_scale_honest_scope).

## 비용
$0 (summer 자체 pool · 신규 303M decode · fleet rent 아님 · a_fire_autonomous). ~8s/tick × 270 tick / 3-concurrent ≈ 12-15min.
