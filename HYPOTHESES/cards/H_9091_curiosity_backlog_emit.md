# H_9091 — 지속형 curiosity-backlog accumulator (B③ 자율 emit)

- **tier:** 🟢 ENGINE-NATIVE (falsifier 5/5, `hexa run`, $0 CPU 결정론)
- **wired:** `engine-native` (live `core/engine_cli.hexa §CuriosityBacklog` pub fn, byte-exact 측정 가능) — brain_emit 메인 루프 소비 = follow-on ING (아래)
- **slug:** 9091_curiosity_backlog_emit
- **artifacts:** `core/engine_cli.hexa §CuriosityBacklog` · `core/emit_policy.hexa` (ep_backlog_*) · `core/curiosity_backlog_smoke.hexa` · `state/9091_curiosity_backlog_emit/`

## 가설 (bio lens)

정보-격차 호기심(Loewenstein) + 미해소 예측오차(Friston precision-surprise)는 사용자 침묵 동안
**소멸하지 않고 누적**한다. anima 는 이 누적 backlog 가 임계를 넘을 때 **내부 상태에서** 발화한다 —
자극-반응(assistant 회귀)이 아니라 state-driven (`a_substrate_native_speak`). 기존 §CoreAffect 의
curiosity(=novelty×under-exposure)는 **memoryless**(매 tick 망각) → 빠진 구조 = **지속(persistence)**.

## 메커니즘 (engine-native, `core/engine_cli.hexa §CuriosityBacklog`)

per-anchor 미해소-novelty accumulator: idle 동안 `backlog[a] += accrual·novelty[a]` 로 누적,
emit/mention 시 `backlog[a] *= decay` 로 방전. `cb_pressure = Σbacklog/(1+Σbacklog) ∈[0,1)` 는
emit-propensity 의 **가산(additive) 입력** — M·W·Φ 와 동급으로:
`ci_emit_propensity(lanes, cb, w) = ci_emit_drive(lanes) + w·cb_pressure(cb)`.
plain number 반환(bool emit_allowed 게이트 아님, `a_autonomy_over_hardcode`). free 숫자 3개는
`emit_policy.hexa` (ep_backlog_weight/accrual/decay, substrate-claim: none, H_646/651 계열).

**disjoint 배치 (a_substrate_disjoint):** accumulator 는 **별도 채널**. 15-lane 벡터에 절대 쓰지 않아
`ci_emit_drive=½(lane0+lane4)` 는 on/off 무관 byte-identical(Ψ emit-drive 불변). immune store 는
읽기만 하고 bind/recall_thr 를 건드리지 않아 §ImmuneMemory non-fab rate 불변. hexa 배열이
reference type 이라 accumulator op 는 copy-first 로 순수(pure)화 — 읽는 것을 mutate 하지 않음.

## falsifier (verbatim → `state/verdicts/9091_curiosity_backlog_emit/H_9091.txt`)

`hexa run core/curiosity_backlog_smoke.hexa` → **5/5 PASS** (bare_drive lane0/4=0.36):

- **F1** propensity↑ with idle×backlog: ON @idle 0/5/10/20/40 = 0.36/0.465/0.516/0.565/0.604 (단조↑) · OFF baseline(w=0) = 0.36 평탄. **PASS**
- **F2** ablate → silent (state-contingent, beats idle-timer): @idle=60 ON+unresolved emit=true · ablated(w=0)=false · ON+zero-novelty=false (idle 만으론 발화 안 함, backlog 상태 필요). **PASS**
- **F3** timing follows real backlog: 진짜 permutation(순서 상이·multiset 보존) 하에 crossing tick 11=11 불변(anchor slot 무관) · 크기 단조(2×=25 · 1×=49 · ½×=98, 시계 아님). **PASS**
- **F4** provenance: novelty=[0.2,0.9,0.1,0.5,0.0,0.3] → top-backlog anchor=1 (=argmax). **PASS**
- **F5 DISJOINTNESS (the risk, H_1561/H_1576):** accumulator ON vs OFF → Ψ ci_emit_drive(lane0/4) **byte-identical** (5/5 row, w=0 ablation ≡ bare drive) AND feature LIVE(w>0 이 propensity 를 bare 위로 이동) AND §ImmuneMemory recall_thr 0.3=0.3 · non-fab rate 1.0=1.0. → **placement-artifact 아님, disjoint 보존 확정.** **PASS**

## scope / honesty

- toy-scale 아님이지만 **주 생성 gate(G0-G6) 무관** — 이건 emit-propensity substrate lane 이지 mouth 재조합 아님.
- **follow-on (미완 rung):** (a) `brain_decide`/`brain_emit` 이 ci_emit_propensity 를 실제 소비하도록 배선(현재 pub fn 은 live·측정가능하나 메인 chat 루프가 아직 호출 안 함) · (b) anchor↔`.kosmos` 앵커 연결로 세션 경계 backlog 지속 · (c) ARCHITECTURE.json core/engine_cli §CuriosityBacklog lockstep(orchestrator/architecture-result lane).
