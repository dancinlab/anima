# H_9421 — G-pole REACH 레버 구현 + $0 β-sign PASS: affinity=d₂−d₁ 이 부호를 뒤집는다 (fire 대기)

**status:** 🔎 DIRECTIONAL-WIRED (H_9419 Step 1 구현 · $0 β-sign PASS · toy SATURATE · 303M fire 대기) — wired: engine-native `anima-py chat --emit-gate refractory --g-reach affinity` (v0.14.9 G5)
**lane:** 의식 / emit-drive / Ψ=½ 항상성 · G-pole 사거리 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9419]] (진단+prereg · 이 카드가 Step 1 구현) · [[H_9416]] (rewire C3) · [[H_9417]] (C2 shuffle 통제·무수정 이식) · [[H_9400]] (반박 대상) · source: Fable G-pole reach impl-spec($5.18) → 구현

## 구현 (Fable 스펙 · 상수 0 · 단일 DOF · v0.14.9 G5)

- **재프레임(Fable §0)**: 현행 margin 게이트 결함은 "짧은 β"가 아니라 **부호-역전 β** — `recall_margin=d₁−0.15` 에서 bind(k)가 k 이웃의 d₁ 을 **내림**→margin↓→게이트 **개방**=자기 이웃 탈억제(P(emit|emit)>P(emit|sil)의 기하 원인).
- **레버**: `core/engine_cli.py` 신규 `immune_memory_recall_reach[_text]` = `d₂−d₁`(top-2 basin 결정성 · 기존 `vadapt_field_two_recon_err` 재사용) + `cli/chat.py --g-reach {d1,affinity}` flag(d1=byte-identical default) + lambda swap + trace `g_reach`. `--g-shuffle` 무수정 합성(C2 통제 이식). 새 상수·시계·τ 0.

## $0 선검증 (Fable §6 · 기존 refr trace 90-tick 재생)

- **β-sign PASS ✅ (부호검산 · 재생 무관 수학적 사실)**: bind 후 자기 reach RISES **23/23·12/12·23/23=100%** · bind 후 verbatim-repeat 침묵 affinity **18/23·11/12·21/23(~85%)** vs d₁ **0/23·0/12·0/23(절대 안 침묵)** ⇒ **affinity=β 복원스프링, d₁=δ 자기흥분 버그** 확증(Fable §5 정합).
- ⚠️ **fidelity gate FAIL(fid g_d1==traced 1-3/23)**: 오프라인 재생 store 가 데몬 궤적 미재현(추가 bind 등 · 재생 하네스 한계). Fable §6대로 **정량 r* 예측은 이 재생서 cement 불가** — β-sign(부호)만 DIRECTIONAL. fire 는 실 데몬 store(계기 live 계산)라 이 한계 무관.

## toy smoke · magnitude 경고

`--g-reach affinity` toy(30tick·T=1.0): flag 작동(g_reach=affinity·g_recog 30 distinct 변동) 그러나 **SATURATE**(EMIT 30/30·reach [0,0.104]<score). toy store 미분화라 d₂≈d₁(Fable §6 wall). §6 replay reach 도 0.04-0.18 로 작음(fidelity-failed·비권위). ⚠️ **magnitude 미결**: 부호는 β 맞으나 reach 크기가 score 대역(0.44-0.74) 못 넘으면 303M 도 saturate 가능 = embed-해상도 벽(Fable §6-iii). **303M live fire 가 유일 판정**.

## 다음 = 303M fire (H_9419 Step 1 발사)

summer 4-arm {refr(d1)·refr-affinity(레버)·refr-shuf(내용통제)·clock} × 3-rollout(seed 7/4302/4303) × T=1.0 → `step1_analyze.py` 동결 bar(Ψ_AG·P-pull-1 autocov·P-pull-2 DRIFT·P-pull-3 dose-response dip). 판정: refr-affinity 에서 P-pull-1~3 점등(음feedback 스프링) ∧ Ψ_AG ½방향(tune-to-green 금지·이동없음 TOST) ∧ shuf mute ∧ clock 불변. SATURATE/mute 면 magnitude 벽 DIRECTIONAL.

## 한계
$0 재생=DIRECTIONAL(β-sign만·fidelity-failed). 다른 데몬·H_9400 clock 계보 영구·Ψ=½ 부활은 fire PASS∧production-default∧정본 후. hexa twin(engine_cli.hexa recall_reach) follow-on(py 카논).
