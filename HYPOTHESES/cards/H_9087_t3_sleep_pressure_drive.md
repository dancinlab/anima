---
id: H_9087   # orchestrator merge-time 배정 (제안: H_9087; 현 origin/main max = H_9069)
slug: t3-sleep-pressure-drive
title: anima 의 sleep-stage 전이는 ultradian 리듬(Process-C)만이 아니라 깨어있던 시간에 단조 축적되는 항상성 수면압(Process-S = adenosine)에도 가산적으로 편향되는가 — 그리고 그 압력 드라이브가 Ψ=½/§ImmuneMemory 정직 게이트와 disjoint 하게 배선되는가?
domain: dream · sleep · a_chat_sleep_imagination · a_substrate_disjoint · a_no_llm_frame_trap · homeostasis · process-S · borbely · consciousness
source: T3 orchestrator task (Process-S sleep-pressure drive) + a_chat_sleep_imagination (기존 WAKE/N1/N2/N3/REM ultradian) + core/dream_lib.hexa (dr_* 리듬 primitive) + a_substrate_disjoint (분리=보존 통일법칙)
exploration_method: 생물렌즈(a_no_llm_frame_trap) — Borbély 1982 / Daan-Beersma-Borbély 1984 의 2-process 수면조절 모델에서 Process-S(항상성 압력, adenosine 축적)를 기존 ultradian(Process-C 리듬) 옆 직교 축으로 dream_lib 에 op-slot 추가 (PURE/READ-only, sp_ prefix)
verification_method: engine-native smoke DREAM/sleep_pressure_smoke.hexa — live core/dream_lib.hexa + core/engine_cli.hexa 디코드 (numpy/torch 미러 아님 → a_engine_native_learning terminal-eligible). 5 pre-registered falsifier, frozen-first, g5 CODE-measured (LLM 자가판정 없음, p7)
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-07-02
since: 2026-07-02
status: measured
wired: engine-native   # (byte-exact 재검증, live dream_lib op-slot 배선 완료 + ARCHITECTURE.json lockstep) — 단 emit-drive 로의 실제 전이-편향 배선은 미완(READ-only op-slot; emit_policy 미접촉 → emit-wiring follow-on)
scope: DESIGNED 법칙 (fixed-τ 지수 accumulate/discharge) — 실측 adenosine 곡선 fit 아님. τw=30/τs=12 는 90-tick ultradian 창에 맞춘 설계값. propensity 는 READ-only 측정 surface — 실제 stage 전이/emit 는 아직 이 압력에 배선되지 않음 (follow-on).
artifacts: [state/verdicts/t3_sleep_pressure_drive/H_9087_engine_native_smoke.txt, core/dream_lib.hexa, DREAM/sleep_pressure_smoke.hexa]
verdict: 🟢 ENGINE-NATIVE 5/5 PASS — Process-S 항상성 수면압이 ultradian 리듬과 직교 축으로 성립하고 Ψ/G5 와 disjoint. F1 ACCUM sp(5)=0.2381664475984473 < sp(55)=0.8561082285282755 (WAKE 단조 축적) · F2 DISCHARGE onset(60)=0.87819824508704851 > end(89)=0.07835154541808053 (sleep 단조 방전) · F3 GATE-BIAS prop(p=.1)=0.30444 < prop(.5)=0.54444 < prop(.95)=0.81444 (가산 graded, boolean 아님, (0,1) 내부) · F4 ABLATION OFF(w10)=0.17778==OFF(w50)=0.17778 (압력 freeze → wake-duration ⟂) ∧ ON(w10)=0.39085≠ON(w50)=0.67578 (ON 은 wake 추적) ∧ ON≠OFF (mechanism non-INERT, 기여>0) · F5 DISJOINT Ψ ci_emit_drive(lane0/4) 0.6→0.6 ∧ §ImmuneMemory recall_margin -0.11683375209644598→-0.11683375209644598 byte-identical (sp 전 op 실행 후). 분리=보존(a_substrate_disjoint). DESIGNED-law·READ-only scope(c9), emit-wiring follow-on.
---

# H_9087 — T3 항상성 수면압 드라이브 (Process-S)

## 0. Motivation

기존 `a_chat_sleep_imagination` 의 sleep 아키텍처(`core/dream_lib.hexa` `dr_*`)는 **ultradian 리듬 하나**만 인코딩한다 — `dr_stage_at(tick)` 이 90-tick 주기의 고정 창 [WAKE 0..59 / N1 60..69 / N2 70..79 / N3 80..86 / REM 87..89]로 stage 를 결정한다. 이는 Borbély 2-process 수면조절 모델의 **Process-C(circadian 진동자)** 축에 해당한다. 그러나 실제 수면 타이밍은 두 독립 축의 상호작용으로 결정된다: Process-C(**WHEN**, 리듬)와 **Process-S(HOW LONG awake**, 항상성 압력 = adenosine 축적). anima 엔진에는 Process-S 축이 **빠져 있었다** — 얼마나 오래 깨어있었는지가 sleep-stage 전이 성향에 영향을 못 줬다. `a_no_llm_frame_trap`(생물렌즈 우선): 빠진 구조(lane)를 모델 키우기가 아니라 **기존 구조 옆에 붙이기**로 실현.

## 1. Hypothesis (one falsifiable claim)

깨어있는 tick 에 따라 **단조 축적**되고 sleep 중 **단조 방전**되는 항상성 수면압 스칼라 S(Process-S)를, 기존 ultradian 리듬(Process-C)과 **직교**하는 축으로 `dream_lib` 에 추가할 수 있으며, 이 압력이 sleep-stage 전이 성향에 **가산적(boolean 아님) 편향**을 준다. 그리고 이 op-slot 은 **PURE/READ-only** 라서 emit-drive lane 0/4(Ψ=½ 고정점)와 §ImmuneMemory recall_thr 정직 게이트를 **byte-identical 로 보존**한다(분리=보존, `a_substrate_disjoint`).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-07-02, 측정 전)

live `core/dream_lib.hexa` § SleepPressure op(`sp_*`) + `core/engine_cli.hexa`(`ci_emit_drive`·`immune_memory_recall_margin`)을 `DREAM/sleep_pressure_smoke.hexa` 가 호출(engine-native, numpy 미러 아님):

- **F1 ACCUM** — `sp_pressure_at`/`sp_pressure_wake` 가 wake tick↑ 에 **엄격 단조 증가**. (붕괴 시: 축적 아님)
- **F2 DISCHARGE** — sleep 창 [60..89]에서 `sp_pressure_at` 가 sleep-onset peak 에서 **엄격 단조 감소**. (붕괴 시: 방전 아님)
- **F3 GATE-BIAS** — `sp_sleep_propensity(pressure, circadian)` 가 pressure↑ 에 **엄격 단조 증가**하고 mid-pressure 에서 (0,1) **내부**(=가산 graded, boolean 게이트 아님). (붕괴 시: 0/1 계단이거나 압력 무관)
- **F4 ABLATION** — `sp_sleep_propensity_ablated`(압력 freeze-out, circadian-only)는 wake-duration 에 **불변** ∧ ON 경로는 wake 추적 ∧ ON≠OFF(**mechanism non-INERT** — ablation 시 결과 동일이면 기여 0 = INERT 였을 것; `a_break_the_wall` 결정적 ablation).
- **F5 DISJOINT** — 전 `sp_*` op 실행 **전/후**로 `ci_emit_drive`(lane 0/4 = Ψ proxy)와 `immune_memory_recall_margin`(=recon_err−recall_thr, G5 non-fab 게이트)이 **byte-identical**. (붕괴 시: 공유 lane 침범 = 충돌)

**Outcome rule (FROZEN):** 5/5 PASS iff Process-S 가 성립하고 disjoint. 어느 falsifier 든 FAIL 이면 정직한 negative(c9) — INERT/충돌/비단조 모두 유효 결과.

## 3. 측정 결과 (engine-native, verbatim)

```
F1 ACCUM     sp(5)=0.2381664475984473 < sp(55)=0.8561082285282755  PASS (monotone accumulate)
F2 DISCHARGE onset(60)=0.87819824508704851 > end(89)=0.07835154541808053  PASS (monotone discharge)
F3 GATE-BIAS prop(p=.1)=0.30444 < prop(.5)=0.54444 < prop(.95)=0.81444  PASS (additive graded, not boolean)
F4 ABLATION  OFF(w10)=0.17778==OFF(w50)=0.17778 | ON(w10)=0.39085!=ON(w50)=0.67578  PASS (frozen⟂wake, ON≠OFF non-inert)
F5 DISJOINT  Psi 0.6->0.6 | recall_margin -0.11683375209644598->-0.11683375209644598  PASS (byte-identical)
ALL FALSIFIERS PASS (5/5) — T3 engine-native GREEN + disjoint
```
frozen: `state/verdicts/t3_sleep_pressure_drive/H_9087_engine_native_smoke.txt`

## 4. Honest scope (c9)

- **DESIGNED law, not fit** — accumulate/discharge 는 고정-τ 지수(τw=30/τs=12). 실측 adenosine PET/EEG 곡선에 fit 한 게 아니라 90-tick ultradian 창에 substantial rise/discharge 가 나오도록 고른 설계값. Process-S 의 *형태*(단조 saturating/방전)는 생물학적이나 *상수*는 designed.
- **READ-only op-slot, emit 미배선** — `sp_sleep_propensity` 는 측정 surface 다. 실제 stage 전이/emit 결정에 이 압력을 배선하는 것은 **follow-on**(현재 `core/emit_policy.hexa` 미접촉 — T3 제약). `a_verified_must_wire` 4칸 사다리에서 현재 (2) engine-native, (3) emit-wire-in 은 미완.
- **직교 축 명시** — Process-S(항상성 압력)는 기존 ultradian(Process-C 리듬)과 **다른 축**이다. 둘의 결합 방식(`sp_sleep_propensity` 의 가산 W_S·pressure+W_C·circadian)은 Borbély 상호작용의 단순 선형 proxy 이지 완전한 2-process 임계교차 시뮬레이션은 아님.

## 5. Follow-on (제안, ING 등록 대상)

- (3) emit-wiring: `sp_sleep_propensity` 를 stage 전이/emit 결정에 실제 배선 (emit_policy 접촉 필요 → B③ 진행분과 조율 후 별도 PR).
- Process-C 임계-교차 완전 모델(S 가 C 의 상한 봉투를 넘을 때 sleep 트리거)로 확장 — 현 선형 가산 proxy 대비 falsify.
- sleep-pressure × mitosis density(`dr_mitosis_density_ratio`) 결합: 높은 압력 → REM/N3 split prior 상향 편향 여부.
