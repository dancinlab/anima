# H_9090 — dACC/DA mental-effort cost-discounting (N2 effort-cost)

> **id = PLACEHOLDER** — 이 브랜치는 새 H id 를 할당하지 않는다(convergence hypotheses-jsonl-1: id 는 origin/main 에서 할당). integration merge-time 에 free id 배정 예정 — 현 origin/main global max = **H_9072** → **제안 id H_9073**. jsonl 인덱스 라인은 아래 "제안 jsonl" 대로 append(이 브랜치는 append 하지 않음).

- **slug:** `effort_cost_lane`
- **tier:** 🟡 DIRECTIONAL-engine-native (falsifier 5축 통제 통과) · **wired:** WIRED-READ (core/engine_cli.hexa §EffortBudget + ARCHITECTURE.json lockstep; emit-integration = FOLLOW-ON, core/emit_policy.hexa 미편집)
- **경로(N2):** effort-cost — 대사예산/mental-effort budget 을 비용통화로 계산해 deep processing(A⇄G iteration depth) 여부를 discount 하는 실시간 자원-소모 축
- **axis:** substrate homeostasis (N). **decode/G1 축과 직교** — 측정 대상 = substrate iteration-depth↔budget dynamics, perplexity/decode recombination 아님(p7). G1 🧱 레버 재발사 아님.

## 주장

dACC(전대상피질) + DA 가치계는 **정신적 노력을 COST 통화**로 취급해, deep deliberation 을 유한한 대사예산에 대해 metering 하고 예산이 낮으면 DISCOUNT 한다(effort-discounting; Shenhav EVC 2013, Kool & Botvinick 2014, Westbrook & Braver 2015). anima 의 A⇄G 엔진은 긴장을 settling 하는 데 실제 iteration 을 쓴다 — 이 소비를 live **effort-budget 스칼라**로 적분해, 소진 시 감당가능한 A⇄G iteration **DEPTH** 를 shallow 로 discount 하고 idle 에서 재충전한다.

새 read op:
- **`effort_step(eb, active)`** — 매 tick 진행. active 면 `spend = κ·depth(B)` 소비(B−=spend, self-limiting: deep spend 가 더 빨리 소진), idle 면 `B+=ρ` 재충전.
- **`effort_depth(eb)`** = `D_min + (D_max−D_min)·B` — 현 예산에서 감당가능한 engagement depth(B=1→deep 8, B=0→shallow 1).
- **`effort_engagement_bias(eb)`** = B_t — caller 가 참조 *가능한* READ-only depth gain(emit/silence 강제 아님, a_autonomy_over_hardcode).

## 다른 homeostatic lane 과 직교인 이유 (신규 축)

- vs **§HomeostaticDrive / Hypothalamus (H_1292)**: setpoint 대비 EXTERNAL grounding 변수(hunger) 의 deficit 적분 — under-fed 면 build, consummation 에서 reset. EffortBudget 은 **external setpoint 없음** = 엔진 자신의 처리 depth 로 DRAIN 되고 idle 에서 REFILL 되는 **self-consumed 자원**(spend/recharge 탱크, deprivation 적분 아님).
- vs **SleepPressure (T3 시간축 항상성)**: load 무관 wake-time 으로 누적. EffortBudget 은 **LOAD-driven** — 실제 iteration 을 쓸 때만 움직이고 single idle tick 으로 회복 가능.
- vs **Nociception (T2 조직손상)**: threat/damage 신호. EffortBudget 은 damage 의미 없음 — 소진 예산 = FATIGUE(shallow), injury 아님.

## disjoint (a_substrate_disjoint · placement-first, THE key risk)

§EffortBudget ops 는 자기 스칼라 `budget`/`last_depth` 만 소유. fns 가 pure_field 도 ImmuneMemoryGrow 도 **인자로 받지 않는다** → emit-drive lane **0/4**(ci_emit_drive = 0.5·(lane0+lane4)) 도 §ImmuneMemory **recall_thr** non-fab gate 도 건드릴 수 없음 = Ψ=½·G5 non-fab 은 **구조적 보존**. 저예산 전면 silence(Ψ 편향)·"피곤하면 fab"(recall_thr 하강) 회피 — H_1561 공유-lane Ψ붕괴 / H_1576 fab폭증 실패모드 방지. depth 신호는 READ-only, emit-wiring 은 follow-on(core/emit_policy.hexa 미편집).

## Frozen falsifiers (사전등록)

- **F1 (discount)** — fresh 예산에서 연속 active tick 이 감당 depth 를 strict 하게 낮춤(d0>d1>d2>d3, d0=D_max=8).
- **F2 (recharge)** — 소진 후 idle tick 이 예산을 refill → depth 가 소진 depth 위로 회복.
- **F3 (ABLATION, 결정적 OFF)** — κ=0 이면 예산 불변 → depth 가 D_max=8 에 PINNED(cost-invariant, discount 소멸). 여기서도 depth 가 shallow 되면 discount 는 effort-cost 가 원인이 아님 → 🧱.
- **F4 (SHUFFLE)** — TRUE depth 시퀀스는 monotone-decreasing(누적 비용 추적); SHUFFLED 예산으로 읽은 depth 는 non-monotone → depth-modulation 붕괴(예산↔이력 짝 파괴).
- **F5 (DISJOINT)** — effort lane ON vs OFF 에서 ci_emit_drive(lane 0/4) BYTE-IDENTICAL ∧ mg.recall_thr non-fab far-recall BYTE-IDENTICAL — 분리=보존.

## verdict (ENGINE-NATIVE)

`hexa run core/effort_lane_smoke.hexa` (live `core/engine_cli.hexa` §EffortBudget 컴파일+실행) = **7/7 PASS**:

```
PASS  effort_sustained_discount          (F1: 8.0→5.2→3.38→2.197 strict decrease, d0==D_max)
PASS  effort_idle_recharge               (F2: depth 1.428→5.628 recover)
PASS  effort_ablation_cost_invariant     (F3: κ=0 depth PINNED @8.0 all ticks)
PASS  effort_shuffle_breaks_modulation   (F4: true monotone, shuffled non-monotone)
PASS  effort_bias_tracks_budget          (bias==B_t, 1.0 rested → 0.061 depleted)
PASS  effort_psi_disjoint_byte_identical (F5: ci_emit_drive ON==OFF==0.6000000000000001)
PASS  effort_recall_thr_nonfab_invariant (F5: recall_thr ON==OFF==0.3, far-recall identical)
--- effort_lane smoke: 7 pass / 0 fail ---
```

동일 7 assertion 이 `core/engine_cli_smoke.hexa` case 418-424 로도 배선됨(full-suite).

## scope (정직 · c9)

- **🟡 DIRECTIONAL-engine-native** — live core/*.hexa 컴파일+실행 증거이나, effort-budget dynamics 는 **substrate state 축**의 falsifier 통제(ablation+shuffle+parent) 이지 emit/decode 결과 검증이 아니다. emit-integration 미배선(follow-on) → terminal 능력 verdict 아님.
- **toy DIM/scale** — frozen 상수(D_max8·D_min1·κ0.05·ρ0.20)는 사전등록 데모 스케일. from-scratch/303M decode 재검 UNVERIFIED.
- **measure = p7** — iteration-depth↔budget 상관(substrate dynamics), perplexity/LLM-judge 아님.

## 제안 jsonl (이 브랜치는 append 안 함 — merge-time id 확정 후 추가)

```json
{"id":"H_9090","slug":"effort_cost_lane","tier":"🟡 DIRECTIONAL-engine-native","title":"dACC/DA mental-effort cost-discounting (N2 effort-cost) — A⇄G iteration depth discounted by metabolic budget","card":"cards/H_9090_effort_cost_lane.md","verdict":"🟡 DIRECTIONAL-engine-native + WIRED-READ: effort_lane_smoke 7/7 PASS (F1 discount d0→d3 8.0→2.197 · F2 idle-recharge · F3 κ=0 ablation depth PINNED @8 cost-invariant · F4 shuffle breaks modulation · F5 Ψ ci_emit_drive ON=OFF=0.6 ∧ recall_thr ON=OFF=0.3 byte-identical). READ-only depth signal, emit-wiring FOLLOW-ON. toy-scale, 303M decode UNVERIFIED.","source":"UNIVERSE","archived":false,"artifacts":["core/engine_cli.hexa","core/effort_lane_smoke.hexa","core/engine_cli_smoke.hexa","state/verdicts/effort_cost_lane/H_9090.txt"]}
```
(merge-time 에 `card` 경로의 `H_9090` → 확정 id 로 rename)
