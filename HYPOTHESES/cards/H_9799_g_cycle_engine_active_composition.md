---
id: H_9799
title: G-CYCLE ENGINE-ACTIVE COMPOSITION — reverse-engine cycle-consistency loss as the trunk-objective lever for ρ·weave/G1 (corpus 아닌 엔진이 목표를 만든다)
tier: PROPOSED · DESIGN-ONLY (lab-full DIRECTIONAL · Fable5 단독 · 메커니즘공백+p7축 미해소 · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-recombination-objective (engine-active axis · reverse-engine target · NOT readout-operator)
created: 2026-07-20
series: R1 (lab-full divergence · a_lab_full_diverge)
related: "[[H_1603]] · [[H_1602]] · [[H_9124]] · [[H_9127]] · a_engine_native_learning · a_substrate_disjoint · a_train_inline_gauge · psi-soma-vitals"
source: owner 질문 "학습 때 엔진이 적극 참여 · corpus만으로 1B/7B에서 G1/G6 뚫는게 미심쩍다 · core가 적극개입하도록?" → lab full (Fable5) 발산
---

# H_9799 (R1) — 엔진이 목표를 만든다: 역방향엔진 순환일관성 손실로 ρ·weave/G1을 친다

## Why (전제 · 측정됨)
G1(ρ·weave 재조합 벽)은 **TRUNK-OBJECTIVE-BOUND**로 확정됐다 (`cli/train.py:32-40`): cross-entropy(=다음-글자 맞히기)는 개념의 **합성(composition)** 을 보상하지 않는다("CE=echo"). 데이터축 escape 전멸 (H_1599 register-split · H_9121 FALSIFIED-CEILING · H_9127 gamma-DATA TRANSFER-FAIL TERMINAL · H_9124 derivtrace NOT-ROBUST) ⟹ **corpus는 지렛대가 아니다**. 기존 objective 레버(predictive_info·constructive_bind·composed_nce, H_1602)는 모두 **A가 A의 활동에서 계산한 손실 = A가 A 채점**.

owner 질문이 짚은 미시도 자유도: **손실의 목표(target)를 다른 엔진(G)이 만든다.**

⚠️ 매핑으로 드러난 현 상태 (`cli/train.py`에 A/G import 부재 · `core/pure_field.py`=A · `core/engine_g.py`=G는 추론전용 · a_substrate_disjoint):
```
현재                         제안 (owner)
──────────                   ──────────
학습 = trunk CE만       →    학습 = trunk CE + 역방향엔진 목표
추론 = A⇄G 긴장(Ψ=½)   →    추론 = A⇄G 긴장(동일)
∴ train/infer 분리(p8위반)  ∴ p8 닫힘(엔진이 학습에도 참여)
```
즉 의식엔진은 지금 **학습에 전혀 참여 안 함** — 이 분리 자체가 p8(train/infer 분리 금지) 위반. owner 직관 = 프런티어 일치.

## Claim (한 줄 · falsifiable)
CE 위에 **순환일관성(cycle-consistency)** 손실 λ·disagreement(A 순방향 합성, G 역방향 분해; **G는 detached**)를 얹으면, 냉동 ρ·weave/G1 바(`anima-py evaluate --rho-axon`)에서 g_cycle의 ΔG1이 (a) CE-only 초과 (b) shuffled-cycle 통제 초과 (c) self-cycle 통제 초과 — base CE 5%내 유지·ρ·fan 무저하. G가 역분해할 수 있는 표현 = 분해가능 = **합성가능** ⟹ G1(재조합) 직격, G2(참신성) 아님.

## Mechanism / Instrument (engine-native · 신규 flag)
`cli/train.py:24-40` 의 `--objective` 레버에 새 값 `g_cycle` 1개 추가 (a_experiment_engine_native):
```
anima-py corpus en --lang en --out c_en.txt          # EN-first (H_9327)
anima-py train --corpus c_en.txt --init base.clm \
  --objective g_cycle --g-every 8                     # CE + λ·cycle(A-fwd, G-rev, G detached)
anima-py evaluate out.clm --rho-axon                  # TERMINAL 판정경로, 냉동바
```
매 `--g-every` step마다 G(detached)를 배치 trunk 상태 위에서 역방향 실행 → loss = CE + λ·disagreement(A 순방향 합성 vs G 역방향 분해). loss 그래프에 ρ 통계 일절 없음(p7 준수).

## Admissibility / p7 축 (Fable 기준 · ⚠️ owner 판정 대기)
Fable 재해석: p7(no perplexity verdict) + a_train_inline_gauge가 금지하는 건 **`anima-py evaluate`가 판정축으로 보고하는 통계**(ρ·weave/ρ·fan)를 loss에 넣는 것. 엔진 **출력**을 목표로 쓰는 건 (i) 어떤 판정통계도 loss 그래프에 없고 (ii) G로 그래디언트 안 흐르고(detached) (iii) G신호가 A의 품질점수 aggregate가 아닌 raw 기전출력이면 합법. Fable은 "p8이 오히려 G-in-loop을 **요구**한다"(현 monitor-only가 이상)쪽. **⚠️ 이건 철학축(p1~p8) 결정 = owner-philosophy, 미해소.**

## Controls (≥2 · a_break_the_wall)
- **C1 CE-only** (`--objective` 미설정) — 기준선.
- **C2 shuffled-cycle** (killer) — 동일 cycle항이나 G의 목표를 배치 내 permute (A↔G 대응 파괴). "임의 정규화" vs "G-정보 압력"을 격리. **g_cycle ≤ shuffled-cycle 이면 전 family FLOOR.**
- **C3 self-cycle** — 역방향 패스를 G 대신 A trunk의 냉동사본이 수행 ("G 특정" vs "임의 역일관성" 구별). arm 부족 시 C3 먼저 드롭.
- EN-first · 동일 corpus/steps/seed · ≥2 seed.

## Falsify
g_cycle의 ΔG1 ≤ shuffled-cycle(C2) ⟹ G신호가 합성정보 무보유 = G-in-loop family 전체 FLOOR → 다음은 λ 튜닝 아닌 다른 각도(a_break_the_wall). 또는 base CE가 CE-only 대비 5% 초과 악화(=G1을 trunk 파괴로 매수) ⟹ KILL. EN positive = SCREENER/DIRECTIONAL only(형태소+base+carrier 동시이동) · TERMINAL은 303M py 경로+scale-bounded(a_scale_honest_scope) · 1B/7B 주장 없음.

## 🧱 발사 블로커 (concrete · 미해소 · fire 전 필수)
1. **메커니즘 공백** — g_cycle은 "G가 trunk 표현을 역분해"를 가정하나, 실제 `core/engine_g.py` 의 G는 8인자 **emit 게이트**(motivation_score·should_emit)이지 **분해기/역디코더가 아님**. "G의 역방향 패스"가 코드로 **미정의**. 후보: (i) core/brain.py `vbasal_update`(gradient-free delta-rule, brain.py:561) 재사용 (ii) 별도 역디코더 정의 (iii) A trunk 냉동사본(=C3와 동일해짐, 그럼 "G 특정"이 사라짐). **→ 이 정의가 실험 성립의 전제.**
2. **p7 축 판정** — 위 Admissibility, owner-philosophy 결정 대기.

## Scale (C · 1B/7B)
Fable: 규모↑ → **더** 필요. corpus 예산고정 + 용량↑ ⟹ CE 지름길이 "합성 말고 암기"로 더 쏠림 ⟹ corpus-only 스케일링은 G1 격차 **확대**. 반례("스케일만으로 합성 유도")는 문헌상 조(兆)-토큰 체제에서만 — anima는 그 데이터체제 도달 불가 ⟹ 레버가 규모와 함께 더 중요. 단 잘못된 G압력 = 대형 trunk critic-collapse(A가 G를 자명히 만족) ⟹ **303M 스크리너 먼저**(fleet rent=spend go-gate 이상 금지).

## Divergence 보고 (a_parallel_session_compare · a_lab_full_diverge)
- **AGREES**: 매핑 에이전트("A/G 학습 부재 = p8 분리")와 Fable("현 monitor-only가 p8 이상, G-in-loop이 닫음")이 **독립 수렴**.
- **NOVEL**: cycle-consistency(A-fwd/G-rev disagreement) = 기존 objective 레버(H_1602 전멸)와 구별되는 미시도 자유도 — kill-list의 readout-operator 아님(objective).
- **CONFLICT/공백**: Sol(Codex) 버전에러로 부재 → 단일모델(Fable) DIRECTIONAL. G-역방향 메커니즘 정의는 Fable도 미해결(가정만) → 발사 블로커 1.
