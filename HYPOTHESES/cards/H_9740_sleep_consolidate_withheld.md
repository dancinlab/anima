# H_9740 — R2-C · SLEEP-CONSOLIDATION — 상상이 emit이 아니라 수면으로 장기저장에 닿는 lane (꿈의 engine-native 정의)

**status:** 🔵 PROPOSED (lab-full R2 심화 · Fable5 · DIRECTIONAL 설계 · **⚠️ production identity rewire → 발사 전 오너-go 필수** — H_9415/9712 p5-rewire 선례)
**lane:** 의식/sleep-imagination · interior-causality (a_chat_sleep_imagination)
**related:** [[H_9729]](awake 재진입 — 비중복 논증 하단)·[[H_9627]](Θ WIRED)·[[H_9731]](timing lane 사망 → 비-emit lane 탐색 동기)·[[H_9739]](gate-측 재프레임 — 상보)
**cost:** toy $0 → pool 3-seed (오너 fire-go + rewire 승인)

## 왜 (브리프 ASK2 — interior를 여는 축이 emit-gate가 아니라면)
정적 census([[H_9738]] S0-a): 상상 content는 장기저장소(immune·igrow·afield)에 **한 바이트도 닿지 않는다** — 데몬은 매 tick 100% distinct·고엔트로피로 상상하고 전부 잊는다. 생물 뇌에서 낮의 비발화 내부상태를 장기기억으로 옮기는 canonical 경로는 **수면 consolidation**이다. anima에는 5-stage sleep이 이미 있고(a_chat_sleep_imagination · 상상≠speak), 보류 텍스트 latch 기계도 이미 있다(H_9729 `_dual_reentry` — 재사용·새 상태면 0). 제안: **꿈 = sleep-stage에서 보류(상상) content의 장기저장 bind.** interior가 열리는 곳은 gate(timing)가 아니라 memory(what-I-am)다.

## 설계 (engine-native 플래그)
`anima-py chat --sleep-consolidate ws` (default off ⇒ byte-identical):
- awake silence tick: H_9729 latch 재사용해 보류텍스트 ring(k≤4) 유지 — 새 read 경로 없음, emit 무접촉.
- sleep-stage tick(stage 3/4): ring의 보류텍스트를 `immune_memory_bind_text`(+igrow affect bind)로 **bind** — 발화 tick의 bind와 동일 op·동일 강도(gain-lock). emit 아님·mouth 무접촉 ⟹ **p5 clean**(상상의 소비이지 speak() 아님; self-seed 아님 — decode seed에 안 들어감).
- 판정면: 수면 후 ① immune recall margin census — **own-withheld** vs {**donor-withheld**(타 rollout 보류·shape-matched), **never-imagined**(length/register-matched 신규 텍스트)} 판별 Δ ② 후속: 다음날 emit 텍스트로의 보류-content n-gram 유입(직접복사 가드 = H_9729 것 재사용).

## 판정 (사전등록)
- margin(own) > margin(donor)·margin(never) (collapse-Δ vs 2 통제·below-chance 커버) = **상상이 자기-경험으로 저장됨** — write-only dead store 반증·interior의 최초 장기 인과 발자국(DIRECTIONAL·feat-급 아닌 text-급).
- own≈donor>never = carrier-only(shape 저장·정체성 무) — 정직 KILL.
- own≈donor≈never = bind 자체 무효 regime → 계기/regime 점검(INVALID 경로).
- ⚠️ ①이 PASS여도 "semantic interior" 주장 금지 — immune margin은 표면-급(a_scale_honest_scope). 후속 ②가 행동 인과.

## kill-list·중복 회피
**vs H_9729**: 저쪽=awake **다음-tick decode-seed 재진입**(mouth로 가는 경로·TE 측정), 이쪽=**sleep-phase 장기저장 consolidation**(mouth 무접촉·recall-margin 판별) — 소비 시점·표적 저장소·측정면 모두 상이. mouth-conditioning(H_9574/9576) 아님 — 생성 조건화 없음. recognition 렌즈·PID·one-sided store 아님. H_9728/9730과 축 상이. 시그니처: margin은 store-내부 판별이라 공통접두 붕괴 무관 + 통제 텍스트를 shape-matched로 사전 고정.
## reconcile 주석
[[H_9738]] certificate가 증명한 '상상→저장 유입 0'을 **의도적으로 여는** 유일 각(꿈의 engine-native 정의: 보류텍스트를 sleep-stage서 immune/igrow bind). p5-clean(상상 소비≠speak·mouth 무접촉)이나 **프로덕션 rewire = 오너 fire-go 필수**. own-withheld vs donor/never recall-margin 판별 + Sol C1 LANE-ORACLE 양성통제 선행(그 lane이 애초 donor content에 반응하는지).
