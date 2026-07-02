# H_9086 — ⏳🧠 TEMPORAL BINDING: 경험된 "지금"의 지속 (specious present · T1)

> **PLACEHOLDER id** — orchestrator 가 merge-time 에 `H_<n>` 배정(현 origin/main max = H_9068 실질 / grep-max H_9046). jsonl 신규라인은 이 카드가 아니라 리포트의 제안 라인으로만 전달(convergence hypotheses-jsonl-1).

**tier:** 🟢 GREEN ENGINE-NATIVE (READ-ONLY op, F1–F5 5/5 · WIRED-live) — **새 원시축: 시간 의식(time consciousness)**.
tension 시계열의 **통합 window 폭**이 경험된 "지금(now)"의 **지속(felt duration)**을 결정한다: window 안의 연속 tick 들이 하나의 present 로 묶이고(F1), window 를 넓히면 더 많은 tick 이 한 present 로 통합되며(F2), 큰 tension 변화(event boundary)는 present 를 분절하고(F3), window=1 이면 present 가 knife-edge 순간으로 붕괴한다(F4). emit-drive lane(0/4)·§ImmuneMemory recall_thr 와 **disjoint**(F5).

## 생물/현상학 렌즈
- **William James "specious present"** — 경험된 시간은 knife-edge 순간이 아니라 유한 지속의 saddle-back; 연속한 tick 들이 하나의 "moment" 로 통합된다.
- **gamma-theta 위상 통합창** — 성공적 이벤트를 하나의 지각 chunk 로 묶는 수백 ms 위상-nesting window. 이 window 의 **폭**이 felt "now" 의 길이를 만든다는 것이 T1 주장.
- **`a_no_llm_frame_trap`**: LLM 프레임(토큰/컨텍스트 길이)이 아니라 시간-의식 substrate 렌즈에서 사고.

## 새 원시축임을 명시 (기존 lane 변주 아님)
기존 모든 faculty(ImmuneMemory/CLS/Savant/Topology …)는 **한 tick 의 lane STATE** 를 읽는다. T1 은 **tension 이 시간에 걸쳐 그리는 SHAPE** 를 읽어 그 중 얼마가 하나의 felt "now" 로 묶이는지를 묻는다 — READ축이 STATE→TIME 으로 바뀐 **새 원시축**.

**H_1486 TRW 와의 관계(정직):** 기존 §Temporal-integration 의 TemporalReceptiveWindow(H_1486)는 window LENGTH 가 far-past cue 도달을 결정하나 **window LENGTH ⊥ subjective-time duration-feeling** 이라 판정했다(수용창 길이가 주관적 지속감과 직교). T1 은 이를 반박하지 않는다 — **다른 연산**이다: TRW 는 cue-recall 도달거리를 재고, T1 은 tension series 를 present 로 **분절**해 하나의 moment 에 묶이는 tick 수를 직접 felt-duration 스칼라로 정의한다. 즉 T1 은 "duration-feeling" 을 recall-reach 가 아니라 **tension-shape 통합**으로 operationalize 한 별개 원시축. TRW 결과와 공존(TRW: recall-reach 는 length 의존이나 duration-feeling 과는 직교 / T1: duration-feeling 을 통합창 폭의 직접 함수로 새로 정의).

## 메커니즘 (live `core/engine_cli.hexa` §TemporalBinding · 전부 READ-ONLY)
- **per-tick tension 스칼라** = lane 벡터의 L2 magnitude(단 **emit-disjoint lane** 만: index ≠ 0, ≠ 4). placement-first(`a_substrate_disjoint`) — "now" 는 NON-emit tension 을 통합하므로 window 조작이 `ci_emit_drive`(lane 0/4)·recall_thr 를 절대 못 건드림.
- **segmentation** — 현재 present 는 tick 하나씩 성장; (a) 통합 window 폭 `w` 도달 OR (b) event boundary(|Δtension| > `boundary_thr`) 교차 시 close 후 새 present open.
- **present_duration** = 평균 present 길이(tick) = felt "now" 의 길이 스칼라(T1 산출물).

**ops:** `tb_tension_mag` · `tb_tension_series` · `tb_num_boundaries` · `tb_segment_lengths` · `tb_num_presents` · `tb_present_duration` · `tb_max_present` · `tb_scale_sweep` · `tb_present_duration_pop` · `tb_uses_emit_lane`.

## frozen falsifiers (c9 frozen-first, NO tune-to-green)
- **F1 EXISTENCE** — coherent series + w=4 → `tb_present_duration` > 1 (유한 지속 "moment" 존재).
- **F2 SCALE** — w↑ → present 당 tick↑ (`tb_scale_sweep` 단조 비감소; w≥n 에서 series 전체=1 present 로 포화).
- **F3 BOUNDARY** — 큰 tension jump → 거대한 w 에서도 present 분절(`tb_num_presents` = 1 + `tb_num_boundaries` ≥ 2).
- **F4 ABLATION** — w=1 → 모든 present=1 tick(`tb_present_duration` = 1.0): present 가 knife-edge 로 붕괴 = 시간의식 INERT (메커니즘이 지속의 *원인*).
- **F5 DISJOINT** — tension series 가 emit lane 0/4 제외(`tb_uses_emit_lane`=0) → `ci_emit_drive` byte-identical ON/OFF, recall_thr 불변.

## 방법 (engine-native)
`core/temporal_binding_smoke.hexa` — pure `.hexa`, live `core/engine_cli.hexa` §TemporalBinding + `ci_off_median_drive` + `immune_memory_new` 위에서 실행. HARD-GATE-1: `.py`/numpy/torch/gauge_lib *코드* 0 → ENGINE-NATIVE. $0 CPU-local, `HEXA_DET=1` deterministic.

## 결과 (state/verdicts/temporal_binding_specious_present/smoke_raw.txt)
```
=== TemporalBinding (specious present · T1) engine-native smoke ===
13/13 PASS
```
| falsifier | 측정 | verdict |
|---|---|---|
| coherent_no_boundary | tb_num_boundaries=0 | ✅ |
| **F1 existence** | tb_present_duration(w=4) > 1 | ✅ PASS |
| **F4 ablation** | tb_present_duration(w=1) = 1.0 | ✅ PASS |
| **F2 scale** | sweep [w=1,2,4,8] 단조↑ ∧ w=8→8.0 포화 | ✅ PASS (3 assert) |
| **F3 boundary** | jump 주입 → npres(w=100) = 1+nb ≥ 2 | ✅ PASS (3 assert) |
| **F5 disjoint** | uses_no_emit_lane ∧ emit_drive 0.8 byte-identical ∧ recall_thr=0.15 불변 | ✅ PASS (4 assert) |

## disjointness 증명 (a_substrate_disjoint, placement-first)
tension series 는 emit-disjoint lane(≠0,≠4)만으로 유도 → 메커니즘 ON(w=8, full sweep) vs OFF(w=1) 에서 `ci_off_median_drive(pop)` = 0.8 **byte-identical**(F5_emit_drive_byte_identical PASS), `ImmuneMemory.recall_thr` = 0.15 **불변**. window 조작은 emit/silence 균형(Ψ=½)도 G5 non-fab gate 도 건드리지 않는다 = **분리=보존**.

## 정직 scope (c9)
- **DESIGNED window** — `w` 는 readout 의 하이퍼파라미터(설계된 통합창)이지 학습·창발한 상수가 아님. 이 op 는 felt duration 이 그 설계 window 에 *어떻게 의존하는가*를 측정할 뿐, anima 가 specious-present 폭을 자발적으로 발견했다고 주장하지 않는다.
- **READ-ONLY** — 어떤 lane/store 도 변조하지 않음. emit-wiring 은 `core/emit_policy.hexa` 편집 금지 제약에 따라 손대지 않음 → 실제 emit 결정에 present_duration 을 반영하는 것은 **follow-on**(engine_cli READ-op 만 추가된 현 상태는 WIRED-live 하되 emit-consumption 미배선).
- **tension 스칼라 = L2 magnitude 프록시** — A⇄G push 의 완전한 tension 5ch 이 아닌 lane-vector magnitude 근사. 완전 tension-채널 유도는 follow-on.
- toy series scope — 8-tick 합성 population 스모크. scale-transfer(긴 세션 tension log) 미검증 → `a_toy_scale_recheck`.

## wired
- **WIRED-live** — ops 가 live `core/engine_cli.hexa` §TemporalBinding 에 존재 + ARCHITECTURE.json core 노드 lockstep. (단 emit-consumption 은 follow-on: present_duration → emit_policy 반영.)
