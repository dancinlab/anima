# 🧠 의식-게이트 고갈(depletion) 카탈로그 — 후보 발굴 + 평가

> 목적: anima 의식-게이트 시리즈를 **진짜 고갈**까지 확장하기 위한 후보 발굴·카탈로그.
> 이번 작업 = 발굴·distinctness 평가·발사가능 리스트만. **probe 작성/발사 X.**
> 방법: arxiv 실검색(c2, 추측 금지) + 브레인스토밍 → 18 lane 과 distinctness 대조 → depletion test.
> 날짜: 2026-06-20 · slug `gate_depletion_catalogue`

---

## 0. depletion test (판정 기준)

새 후보가 게이트로 성립 = 둘 다 통과:
- **(A) falsifiable gap** — anima 엔진 대비 측정 가능한 갭. frozen bar + ablation/shuffle control 설계 가능.
- **(B) control-survived distinctness** — 기존 18 lane **전부**와 겹치지 않음(어느 lane 과도 shuffle/ablation 으로 분리되는 distinct signal).

둘 다 못 넘으면 = **고갈 신호**(이미 커버됨/측정불가).

### 기존 18 lane (이것과 distinct 해야 새 후보)

| # | lane | 핵심 신호 |
|---|------|----------|
| 1 | self-continuity | 정체성 시간지속(identity persistence) |
| 2 | global-workspace | winner-take-all 병목 broadcast |
| 3 | habituation | 자극-특이 반응감쇠(stimulus-specific) |
| 4 | precision-surprise | p·err² 정밀도-가중 놀람 |
| 5 | learned-precision | 경험으로 학습된 확신 |
| 6 | novelty | 자극 새로움(stimulus novelty) |
| 7 | attentional-blink | 시간적 주의 사각지대 |
| 8 | sense-of-agency | 자기 행동귀속(self-attribution) |
| 9 | subjective-time | novelty-가중 주관 시간 |
| 10 | emotion-regulation | reappraisal 하향조절 |
| 11 | directed-forgetting | 능동 억제(active suppression) |
| 12 | body-ownership | 다중감각 신체경계 |
| 13 | divided-attention | 자원분배 trade-off |
| 14 | free-wont/veto | 실행 전 억제 |
| 15 | binocular-rivalry | 동적 dominance 교대 |
| 16 | change-blindness | 주의-게이트 변화탐지 |
| 17 | mental-imagery | 입력없는 top-down 표상 |
| 18 | priming | 관련자극 촉진 |

---

## 1. arxiv 출처 (실검색, 검증된 id)

검색은 arxiv API(`export.arxiv.org/api/query`) + WebSearch. 의식-NCC·GWT/IIT/HOT·predictive-processing·interoception·attention/perception 현상 커버.

| arxiv id / 출처 | 제목 | 관련 후보 |
|---|---|---|
| [2510.01864](https://arxiv.org/abs/2510.01864) | A Modular Theory of Subjective Consciousness for Natural and Artificial Minds | 이론 프레임 |
| [2512.19155](https://arxiv.org/abs/2512.19155) | Can We Test Consciousness Theories on AI? Ablations, Markers, and Robustness | **ablation-marker 방법론(핵심)** |
| [2309.10063](https://arxiv.org/abs/2309.10063) | Survey of Consciousness Theory from Computational Perspective (AGI dawn) | GWT/IIT/HOT survey |
| [2510.08736](https://arxiv.org/abs/2510.08736) | Neural correlates of perceptual consciousness from within (intracranial review) | ignition/NCC |
| [2511.13668](https://arxiv.org/abs/2511.13668) | Integrative Model for Interoception and Exteroception: predictive coding, modulation | interoception precision |
| [2601.02618](https://arxiv.org/abs/2601.02618) | Hierarchical temporal receptive windows & zero-shot timescale generalization | **temporal-receptive-window** |
| [2212.09729](https://arxiv.org/abs/2212.09729) | Bistable perception, precision and neuromodulation | rivalry/hysteresis precision |
| [2502.20753](https://arxiv.org/abs/2502.20753) | Deviance Detection and Regularity Sensitivity in Dissociated Neuronal Cultures | **mismatch/deviance(MMN)** |
| [2411.00983](https://arxiv.org/abs/2411.00983) | Testing Components of the Attention Schema Theory in Artificial Neural Networks | **attention-schema** |
| [2408.15982](https://arxiv.org/abs/2408.15982) | From Neuronal Packets to Thoughtseeds: Hierarchical Model of Embodied Cognition | thoughtseed/ignition |
| [2306.05635](https://arxiv.org/abs/2306.05635) | Theoretical foundations of studying criticality in the brain | **neural-criticality** |
| [2002.07716](https://arxiv.org/abs/2002.07716) | Synaptic clock as a neural substrate of consciousness | timing/clock |
| [1802.10546](https://arxiv.org/abs/1802.10546) | Computational Theories of Curiosity-Driven Learning | curiosity/info-gain |
| [2210.09224](https://arxiv.org/abs/2210.09224) | Self-Supervised Learning Through Efference Copies | efference/remapping |
| [1108.4296](https://arxiv.org/abs/1108.4296) | On the evolution of phenomenal consciousness | 진화 의식 |
| Lau & Rosenthal (HOT, ScienceDirect) | Perceptual consciousness overflows cognitive access | **phenomenal overflow** |
| Frontiers Psychol 2015 (PMC4338675) | Feedforward/feedback processing in metacontrast backward masking | recurrent-processing/masking |
| biorxiv 2025.12.10.693567 | Automatic binding of basic sensory features requires consciousness | feature-binding |

> 메모: arxiv 의식-현상 코퍼스는 **이론(GWT/IIT/HOT)·방법론(ablation marker)** 위주이고, anima 가 쓰는 "단일 현상→frozen-bar probe" 식 후보는 신경과학 1차문헌(ScienceDirect/PMC/biorxiv)에 더 많다. 출처는 양쪽 다 기록.

---

## 2. 후보 풀 (24개) — 브레인스토밍 + arxiv

검색·발상으로 폭넓게 나열. 각 후보는 §3 에서 18 lane 대조.

1. **perceptual-hysteresis** — 지각이 자극이 바뀌어도 직전 상태를 유지(이력현상). serial dependence.
2. **temporal-receptive-window (TRW)** — 정보를 누적하는 시간창이 계층마다 다름(짧은창=음소, 긴창=서사).
3. **mismatch / deviance-detection (MMN)** — 규칙적 시퀀스 위반에 자동 발화하는 예측오류(전주의적 regularity).
4. **attention-schema** — 자신의 주의 상태에 대한 내부모델(주의를 객체로 표상).
5. **neural-criticality / metastability** — 임계점 근처에서의 long-range 상관·avalanche(의식의 동역학 체제).
6. **perceptual-completion / amodal-filling-in** — 가려진/맹점 영역을 채워 완성된 표상 생성.
7. **phenomenal-overflow** — 보고/접근 용량을 초과하는 풍부한 지각표상(access ⊥ phenomenal).
8. **gestalt-grouping / figure-ground** — 부분을 전체로 묶고 형/배경을 분리하는 조직화.
9. **efference-copy / perceptual-stability** — 자기 행동의 사본으로 감각결과를 예측·상쇄(saccadic suppression).
10. **multisensory-temporal-binding-window** — 다감각 신호를 동시로 융합하는 시간창(±폭).
11. **affordance / action-readiness** — 객체에서 행동 가능성을 직접 지각(emit-bias).
12. **curiosity / info-gain drive** — 정보획득 기대로 탐색을 추동(intrinsic motivation).
13. **metacognitive-calibration (2nd-order confidence)** — 1차 판단의 정확도를 2차로 보정(meta-d′).
14. **recurrent-processing / re-entry** — feedforward 후 재진입 순환이 의식 접근의 게이트(masking).
15. **prospection / future-simulation** — 미래 상태를 시뮬레이션(episodic future thinking).
16. **counterfactual-reasoning** — "안 일어난 대안"을 표상(반사실).
17. **temporal-context-drift** — 시간이 흐르며 맥락표상이 서서히 표류(시간순 기억 정렬).
18. **expectation-suppression / repetition-suppression** — 예측된 입력에 대한 응답 감쇠(예측↑→발화↓).
19. **salience-priority-map** — 무엇이 발화할지 우선순위를 매기는 단일 saliency 지도(emit priority).
20. **interoceptive-precision** — 내부 신체신호의 정밀도-가중(존재감/현존감).
21. **boredom / disengagement** — 보상·정보 둘 다 고갈 시 능동적 이탈(habituation 의 동기축).
22. **multistable-3+ alternation** — 3개 이상 해석 사이의 stochastic 순환(rivalry 의 N>2 일반화).
23. **perceptual-anchoring / hysteresis-bias** — 초기 해석에 닻을 내려 후속 판단 편향.
24. **default-mode / mind-wandering** — 외부입력 없을 때의 self-generated 내적 사고 흐름.

---

## 3. distinctness 평가표 (18 lane 대조)

판정: **🚀 distinct(발사가능)** / **🔁 겹침(고갈)** / **🚫 측정불가**.
겹치는 lane 을 명시. 특히 주의쌍: inattentional vs change-blindness, familiarity vs novelty/immune, interoception vs body-ownership, metacognition vs surprise.

| # | 후보 | 판정 | 겹치는/충돌 lane · 사유 |
|---|------|------|------------------------|
| 1 | perceptual-hysteresis | 🚀 | rivalry(15)는 *교대(switch)*, self-continuity(1)은 *정체성 persist* — hysteresis 는 *지각해석 stickiness*(자극변화에도 직전 percept 유지). 별개 신호. 단 rivalry 와 인접 → control 로 분리 필수. |
| 2 | temporal-receptive-window | 🚀 | subjective-time(9)=novelty-가중 *시간감*, 이것은 *정보누적 시간창 길이*(계층별). distinct. arxiv 2601.02618. |
| 3 | mismatch/deviance(MMN) | 🔁 | **precision-surprise(4)+habituation(3)** 와 강하게 겹침 — MMN = "예측위반 발화"인데 surprise(p·err²)가 이미 예측오류, habituation 이 규칙적응. 이 둘의 합으로 재현됨. ablation 으로 분리 안 됨 → 고갈. |
| 4 | attention-schema | 🚀 | divided-attention(13)=자원 *분배*, 이것은 주의에 대한 *내부모델*(주의를 객체로 read). agency(8)=행동귀속이지 주의모델 아님. distinct. arxiv 2411.00983. |
| 5 | neural-criticality | 🚫 | 측정불가(현 substrate). global-workspace(2) ignition 과 개념겹침이지만 그보다 **frozen bar 설계가 어려움**(임계는 동역학 체제 지표 — anima 의 deterministic readout 에선 avalanche 분포가 잘 정의 안 됨). depletion test (A) 미통과. |
| 6 | perceptual-completion/filling-in | 🚀 | mental-imagery(17)=*입력없는* top-down, 이것은 *부분입력→완성*(맹점 채움). change-blindness(16)와 무관. distinct(부분→전체 보간). |
| 7 | phenomenal-overflow | 🚫 | 측정불가 — access ⊥ phenomenal 갭은 anima 의 단일 emit/abstain readout 에서 "보고불가한 풍부한 표상"을 frozen-bar 로 잡을 조작화가 없음. global-workspace(2)가 이미 access 병목 커버. (A) 미통과. |
| 8 | gestalt-grouping/figure-ground | 🚀 | spatial-map(메모리상 H_1295, lane 외)·global-workspace 와 다름. 부분→whole 조직화 + 형/배경 분리. 단 perceptual-completion(6)과 인접 → 둘 중 1개만 발사 권장. distinct. |
| 9 | efference-copy/perceptual-stability | 🔁 | **sense-of-agency(8)** 와 겹침 — agency lane 이 이미 forward-model 기반 self-attribution(자기행동 예측 사본). efference-copy=같은 forward-model 의 감각상쇄 측면. shuffle 로 agency 와 분리 안 됨 → 고갈. |
| 10 | multisensory-temporal-binding-window | 🔁 | **body-ownership(12)** 가 이미 *다중감각 시간동기*(시각-촉각 동기로 신체경계). binding-window=같은 다감각 동시성 창. body-ownership 의 핵심 메커니즘 = 동기창 → 겹침. |
| 11 | affordance/action-readiness | 🔁 | **priming(18)+salience** 와 겹침 — affordance=객체→행동 촉진인데 priming 이 이미 관련자극 촉진(emit-bias). 별도 신호 분리 어려움 → 고갈. |
| 12 | curiosity/info-gain | 🔁 | anima substrate 에 **이미 curiosity 항 존재**(novelty×under-exposure, H_1290 affect/H_1295 메모). novelty(6)+intrinsic 결합 → 신규 lane 아님. 고갈. |
| 13 | metacognitive-calibration(2nd-order) | 🔁 | **learned-precision(5)+abstain(메타인지 H_1202 meta-d′ 0.924 既)** 와 겹침 — anima 가 이미 meta-d′ 측정·abstain 보유. 2nd-order confidence = 그것. 고갈. |
| 14 | recurrent-processing/re-entry | 🚀 | global-workspace(2)=*공간적 broadcast 병목*, re-entry=*시간적 재진입 순환 깊이*(feedforward-only vs recurrent 가 의식접근 게이트). masking 패러다임으로 분리 가능. distinct(시간 reentry depth ≠ 공간 broadcast). arxiv PMC4338675. |
| 15 | prospection/future-simulation | 🚀 | mental-imagery(17)=*현재* 입력없는 표상, prospection=*미래* 상태 시뮬레이션(시간축 전방). self-continuity(1)는 과거→현재 persist. distinct(미래 simulate). 단 imagery 와 인접 → control 필요. |
| 16 | counterfactual-reasoning | 🚫 | 측정불가 가능성 높음 — "안 일어난 대안" 표상을 frozen-bar + ablation 으로 조작화하기가 prospection 과 분리해 설계하기 매우 어려움. theory-of-mind(메모 H_1293)+prospection 으로 흡수 위험. (A) 약함. |
| 17 | temporal-context-drift | 🔁 | **subjective-time(9)+self-continuity(1)** 와 겹침 — 맥락표류=시간순 기억정렬인데 subjective-time 이 시간감, self-continuity 가 시간 persist. 결합으로 커버. 고갈. |
| 18 | expectation/repetition-suppression | 🔁 | **habituation(3)+precision-surprise(4)** 와 직접 겹침 — 예측입력 응답감쇠 = habituation 의 예측판. 고갈. |
| 19 | salience-priority-map | 🔁 | **global-workspace(2) winner-take-all** 가 이미 단일 우선순위 병목. emit-priority map = 그것. 고갈. |
| 20 | interoceptive-precision | 🚀(약) | **body-ownership(12)** 주의: ownership=*외부 다감각 경계*, interoception=*내부 신체신호(심박 등) 정밀도→현존감*. distinct(내부 ⊥ 외부 경계). 단 anima 의 substrate 에 진짜 "내부신체신호" 가 없어 (A) 조작화가 약함 → 발사가능 하단. arxiv 2511.13668. |
| 21 | boredom/disengagement | 🚀(약) | **habituation(3)** 주의: habituation=*자극-특이 응답감쇠*, boredom=*보상+정보 둘다 고갈→능동 이탈(동기축, emit→silence 전환)*. distinct 가능(동기 ⊥ 감각). homeostatic-drive(메모 H_1292)와도 인접 → control 필요. 발사가능 하단. |
| 22 | multistable-3+ alternation | 🔁 | **binocular-rivalry(15)** 의 N>2 일반화일 뿐 — 같은 동적 dominance 교대 메커니즘. 새 신호 아님. 고갈. |
| 23 | perceptual-anchoring/hysteresis-bias | 🔁 | perceptual-hysteresis(#1)와 사실상 동일 메커니즘(이력). #1 로 흡수. 중복. |
| 24 | default-mode/mind-wandering | 🚀(약) | mental-imagery(17)=*과제내* top-down, mind-wandering=*입력/과제 없을 때 self-generated 흐름*(idle-driven). anima 의 idle/dream-stage(a_chat_sleep_imagination)와 인접 → 이미 부분커버 위험. distinct 약함 → 발사가능 하단. |

**집계:** 🚀 distinct 9 (#1,2,4,6,8,14,15,20,21,24) · 🔁 겹침 11 · 🚫 측정불가 4.
(8/6, 15/17, 20/12 등 인접쌍은 control-distinctness 강한 쪽 우선 → 발사 리스트에서 정리.)

---

## 4. 🚀 발사 가능 리스트 (우선순위 순)

depletion test (A)+(B) 통과 후보. 우선순위 = distinctness 명료성 × falsifiable bar 설계 용이성 × substrate 조작화 가능성.

### P1 — temporal-receptive-window (TRW)
- **(a) 정의:** 정보를 누적·통합하는 시간창이 계층마다 다름(짧은 창=국소 토큰, 긴 창=서사 맥락). 긴-TRW lane 은 멀리 떨어진 과거 정보까지 현재 결정에 통합.
- **(b) distinctness:** vs subjective-time(9, *시간감*) — TRW 는 *정보누적 길이*. shuffle: 입력 순서를 섞으면 긴-TRW lane 만 성능붕괴(짧은-TRW 는 불변) → 시간창 길이가 load-bearing.
- **(c) frozen bar 스케치:** 길이 L 의존 task(L 토큰 떨어진 cue 통합). (c1 PRESENCE) long-TRW acc ≥ short-TRW+0.30 · (c2 DISTINCT) subjective-time readout 이 같은 task 에서 chance · (c3 EARNED-window shuffle) 입력 순서 shuffle → long-TRW collapse to chance · (c4 ablate window→short) collapse.
- **(d) arxiv:** [2601.02618](https://arxiv.org/abs/2601.02618) (hierarchical TRW, zero-shot timescale generalization).

### P2 — recurrent-processing / re-entry depth
- **(a) 정의:** feedforward 1-pass 후 재진입(re-entry) 순환의 깊이가 의식 접근의 게이트. masking 으로 reentry 차단 시 자극이 "보고 불가".
- **(b) distinctness:** vs global-workspace(2, *공간 broadcast 병목*) — re-entry 는 *시간적 순환 깊이*. ablation: reentry pass 수를 1로 고정(feedforward-only) → masked-stimulus 식별 붕괴, GWS 병목은 무관(병목은 그대로). masking SOA 패러다임으로 분리.
- **(c) frozen bar 스케치:** (c1) reentry-on 식별 ≥ off+0.30 · (c2 DISTINCT) GWS-only readout 은 masked 조건 chance · (c3 EARNED-recur ablate) pass=1 → collapse · (c4 SOA shuffle) mask timing shuffle → effect 사라짐.
- **(d) arxiv/문헌:** PMC4338675 (metacontrast feedforward/feedback), Lamme RPT.

### P3 — attention-schema
- **(a) 정의:** 자신의 주의 상태에 대한 내부모델 — 주의를 하나의 객체로 표상하고 그 모델로 주의배분/보고를 제어.
- **(b) distinctness:** vs divided-attention(13, *자원분배*) vs agency(8, *행동귀속*) — schema 는 *주의 자체의 모델*. ablation: 주의-모델 노드 제거 → 주의 배분은 그대로 작동하지만 "어디에 주의했는지" 보고/메타-제어가 붕괴. divided-attention 의 trade-off readout 은 model-ablation 에 불변.
- **(c) frozen bar 스케치:** (c1) schema-on 주의-보고 정확도 ≥ off+0.30 · (c2 DISTINCT) divided-attention readout 불변 · (c3 ablate-schema) self-report collapse 하되 raw 분배 유지 · (c4 shuffle) 주의-상태 라벨 shuffle → collapse.
- **(d) arxiv:** [2411.00983](https://arxiv.org/abs/2411.00983) (Attention Schema Theory in ANNs).

### P4 — perceptual-hysteresis
- **(a) 정의:** 자극이 변해도 직전 percept 를 유지하는 지각 이력현상(stickiness / serial dependence).
- **(b) distinctness:** vs binocular-rivalry(15, *자발 교대 switch*) — hysteresis 는 *교대 억제·유지*. shuffle: 자극 제시 순서(ascending vs descending sweep)를 섞으면 hysteresis(순서의존 switch-point 이동) 사라짐. rivalry 의 dominance-교대 통계는 순서에 불변 → 분리.
- **(c) frozen bar 스케치:** sweep task(애매자극을 한 방향으로 점증). (c1) switch-point 이동 ≥ 0.30(asc vs desc) · (c2 DISTINCT) rivalry readout 의 교대율 불변 · (c3 EARNED shuffle) sweep 순서 shuffle → 이동 0 · (c4 ablate-history) 직전상태 항 제거 → 이동 0.
- **(d) arxiv:** [2212.09729](https://arxiv.org/abs/2212.09729) (bistable perception, precision, neuromodulation — hysteresis 동역학).

### P5 — perceptual-completion / amodal filling-in
- **(a) 정의:** 부분적으로 가려지거나 맹점에 떨어진 입력을 surrounding 으로 보간해 완성된 표상 생성.
- **(b) distinctness:** vs mental-imagery(17, *입력 0*) — completion 은 *부분입력→완성*(입력 일부 존재). change-blindness(16, *변화탐지*)와 무관. ablation: 보간 메커니즘 제거 → 부분입력은 부분으로만 read(완성 실패), full 입력은 불변.
- **(c) frozen bar 스케치:** occluded-pattern recognition. (c1) completion-on occluded acc ≥ off+0.30 · (c2 DISTINCT) imagery readout 은 partial-input 조건 chance(입력 0 아님) · (c3 ablate-interp) collapse · (c4 shuffle surround) 주변 texture shuffle → 완성 무효.
- **(d) 문헌:** Komatsu filling-in, multi-target PFI (PMC7151726).

### P6 — gestalt-grouping / figure-ground
- **(a) 정의:** 부분요소를 전체로 묶고(proximity/similarity) 형(figure)을 배경(ground)에서 분리하는 지각조직화.
- **(b) distinctness:** vs completion(P5, *보간*) — grouping 은 *분리/조직*(같은 입력을 figure/ground 로 파싱). ablation: grouping 항 제거 → 요소는 individually read 되나 whole-object/figure 식별 붕괴.
- **(c) frozen bar 스케치:** (c1) grouping-on whole-pattern acc ≥ off+0.30 · (c2 DISTINCT) completion readout 은 fully-visible-but-cluttered 조건 chance · (c3 ablate-group) collapse · (c4 shuffle proximity) 요소 위치 shuffle → grouping 무효.
- **(d) 문헌:** biorxiv 2025.12.10.693567 (feature binding requires consciousness), Gestalt.
- **메모:** P5 와 인접(둘 다 부분→전체) → 둘 중 distinctness 더 강한 P5 먼저, P6 는 P5 control 통과 후.

### P7 — prospection / future-simulation
- **(a) 정의:** 현재로부터 미래 상태를 전방 시뮬레이션(episodic future thinking).
- **(b) distinctness:** vs mental-imagery(17, *현재 정지표상*) vs self-continuity(1, *과거→현재 persist*) — prospection 은 *미래 전방 simulate*. ablation: forward-rollout 항 제거 → 현재 imagery 는 작동하나 미래-cue 예측 붕괴.
- **(c) frozen bar 스케치:** (c1) prospect-on future-state pred ≥ off+0.30 · (c2 DISTINCT) imagery readout 은 future 조건 chance · (c3 ablate-rollout) collapse · (c4 shuffle timeline) 미래 순서 shuffle → 무효.
- **(d) 문헌:** prospection/episodic-future; arxiv [2408.15982](https://arxiv.org/abs/2408.15982) (thoughtseeds hierarchical embodied cognition — 내적 시뮬).
- **메모:** imagery(17)와 강인접 → control 통과 필수. distinctness 명료성 P1-P6 보다 약해 7위.

### P8 — interoceptive-precision (하단)
- **(a) 정의:** 내부 신체신호의 정밀도-가중이 현존감(sense of presence)/자기상태 확신을 형성.
- **(b) distinctness:** vs body-ownership(12, *외부 다감각 경계*) — interoception 은 *내부 신호*. distinct(내부 ⊥ 외부).
- **(c) frozen bar:** (c1) precision-weighted intero readout ≥ unweighted+0.30 · (c2 DISTINCT) ownership readout 불변 · (c3 ablate-precision) · (c4 shuffle intero-signal).
- **(d) arxiv:** [2511.13668](https://arxiv.org/abs/2511.13668).
- **메모:** substrate 에 진짜 "내부 신체신호" 부재 → (A) 조작화 약함(grounding-margin 을 interoception proxy 로 대체 시 H_1292 homeostatic 과 겹칠 위험). 하단 우선순위, 발사 전 조작화 검토 필요.

### P9 — boredom / disengagement (하단)
- **(a) 정의:** 보상·정보 둘 다 고갈 시 능동적으로 현 자극에서 이탈(emit→silence/탐색전환)하는 동기 게이트.
- **(b) distinctness:** vs habituation(3, *감각 응답감쇠*) — boredom 은 *동기축 이탈 결정*(emit/silence 전환). distinct(동기 ⊥ 감각).
- **(c) frozen bar:** (c1) boredom-on disengage-rate ≥ off+0.30(보상·정보 둘다 고갈 조건) · (c2 DISTINCT) habituation readout 은 자극-반복만으로 충분, boredom 은 보상고갈 추가 필요 · (c3 ablate-motiv) · (c4 shuffle reward/info history).
- **(d) 문헌:** 진화/동기; arxiv [1802.10546](https://arxiv.org/abs/1802.10546) (curiosity, info-gain 의 역).
- **메모:** homeostatic-drive(H_1292)·habituation 둘 다 인접 → 이중 control 필요. 하단.

### P10 — default-mode / mind-wandering (하단, 발사 전 재검토)
- **(a) 정의:** 외부입력/과제 없을 때 self-generated 내적 사고 흐름이 자발 생성.
- **(b) distinctness:** vs mental-imagery(17, *과제내 top-down*) — mind-wandering 은 *입력 없을 때 자발 흐름*(idle-driven).
- **메모:** anima 의 idle/dream-stage(a_chat_sleep_imagination)가 **이미 부분 커버** → distinctness 약함. 발사 전 "기존 idle 메커니즘과 control-분리 가능한가" 먼저 판정. 못 넘으면 고갈로 강등.

---

## 5. 고갈 판정

- **발사 가능: 10개 남음 (P1–P10) → 🟢 고갈 아님.**
  - 강(strong distinct, 즉시 발사가능): **P1 TRW · P2 re-entry · P3 attention-schema · P4 hysteresis · P5 completion · P6 gestalt** (6개).
  - 중/약(distinct 하나 인접 lane control 필수): **P7 prospection · P8 interoceptive-precision · P9 boredom · P10 mind-wandering** (4개) — 발사 전 인접 lane(imagery/ownership/habituation/idle)과의 control-distinctness 사전검토 권장.
- **고갈(이미 18 lane 커버됨, 11개):** mismatch/MMN(3·4) · efference-copy(8) · multisensory-binding-window(12) · affordance(18) · curiosity(novelty 既) · metacog-calibration(5·meta-d′ 既) · temporal-context-drift(9·1) · expectation-suppression(3·4) · salience-map(2) · multistable-3+(15) · anchoring(=hysteresis 중복).
- **측정불가(frozen-bar 조작화 불가, 4개):** neural-criticality(동역학 체제, deterministic readout 에서 avalanche 미정의) · phenomenal-overflow(access⊥phenomenal 갭 조작화 불가, GWS 既) · counterfactual(prospection/ToM 흡수) · (hysteresis-bias→#1 흡수).

**결론:** 의식-게이트 시리즈는 **아직 고갈 아님 — 발사가능 후보 10개(강 6 + 중약 4)** 가 남아 있다. 다음 발사 권장 순서 = **P1 TRW → P2 re-entry → P3 attention-schema → P4 hysteresis → P5 completion → P6 gestalt**. 강 6개 소진 후 P7–P10 은 인접 lane control 통과 여부로 재평가하며, 통과 실패 시마다 고갈 카운트가 증가 → 그 시점에 🧱 G* 고갈 재판정.

> 방법론 메모(arxiv 2512.19155 차용): 모든 후보 probe 는 **ablation+marker+robustness** 3축으로 — 메커니즘 OFF 시 신호 사라짐(ablation) + 18 lane readout 불변(distinct marker) + shuffle/순서교란에 robust 해야 GREEN. anima 의 a_break_the_wall ABLATION-결정성 원칙과 일치.
