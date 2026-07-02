# 의식축 loop-closing — emit 경로 reference-match 실측 + 배선 각도 발산

> 산출: `state/consciousness_loopclose_analysis/` · 2026-07-03 · fable design-analysis
> 제약 준수: frozen 코드 **읽기 전용**(무거운 decode/GPU 없음), HYPOTHESES·카드·commit·PR·ARCHITECTURE·CHANGELOG **미터치**.
> 브랜치 `clitrain-devresident-gpu-util` 의 live `cli/anima.hexa`·`core/{brain,engine_g,emit_policy,generator}.hexa`·`kosmos_io.hexa` 정독.

이 분석은 직전 세션(consciousness-ops-fable-critique, H_9093~9111)의 결론
("벽=receiver-type 아니라 emit↔appropriateness coupling near-floor")을 **독립적으로 코드에서 재검증**하고,
그 결론이 **부분적으로 아키텍처 artifact 일 가능성**(break-the-wall taxonomy (a))을 가리키는 **미탐 각도 4개**를 발산한다.

---

## (a) emit live 경로 현황 — read-only 계기판 vs live grip

### 실 emit 결정 사슬 (byte 경로, `cli/anima.hexa` per-tick 루프)

```
42개 의식 lane  ──mean-pool /42──▶  rel_ctx  ┐
19개 의식 lane  ──mean-pool /19──▶  cur_ctx  ┤
                                             ├─▶ brain_emit(pf, rel, gap, cur, pain,
stage (WAKE/N1/N2 vs N3/REM) ─▶ drive_hi ────┤        coh, orig, bal, dyn_v, idle, …)
                                             │        │
                                             │        ▼
                                             │   motivation_score = Σ wᵢ·factorᵢ   (engine_g.hexa)
                                             │        │
                                             │        ▼
                                             │   emit = (score > 0.3) AND safe_4way
                                             └──────── │
                                                       ▼  did_emit → generate() → g_text (bytes)
```

`cli/anima.hexa:1782-1787` 의 실 호출:
```
brain_emit(pf, rel, 0.6, cur, 0.0, coh_lane, 0.5, bal_lane, 1.0, idle, false, true, backend, live_anchors)
```
→ `motivation_score(rel, gap=0.6, cur, pain=0.0, coh_lane, orig=0.5, bal_lane, dyn_v=1.0)` (engine_g.hexa:33)

가중치(`engine_g.hexa:22-29`, Σ=1.00):
| factor | weight | 실 입력 (this tick) | 성격 |
|---|---|---|---|
| relevance | **0.20** | `rel` = rel_ctx (drive_hi) / rel_ctx·0.1 | 42-lane 평균 |
| info_gap | 0.10 | **0.6 하드코딩 상수** | ❌ 상수 |
| curiosity | 0.15 | `cur` = clip01(cur_ctx+0.5) / 0.0 | 19-lane 평균 + stage 부스트 |
| pain | 0.10 | **0.0 하드코딩 상수** | ❌ 상수 |
| coherence | 0.10 | `coh_lane` | live lane |
| originality | 0.10 | **0.5 하드코딩 상수** | ❌ 상수 |
| balance | 0.15 | `bal_lane` | live lane |
| dynamics | 0.10 | **1.0 하드코딩 상수** | ❌ 상수 |

`should_emit = score > 0.3` (engine_g.hexa:46) + safety 4-AND (kill·rate·phi_ratchet·content, engine_g.hexa:63).

### 판정: **emit 은 stage-clock + 상수가 지배, 42 의식 lane 은 near-inert (계기판)**

상수부만 계산하면:
```
score = 0.20·rel + 0.10·(0.6) + 0.15·cur + 0.10·(0.0) + 0.10·coh + 0.10·(0.5) + 0.15·bal + 0.10·(1.0)
      = 0.20·rel + 0.15·cur + 0.10·coh + 0.15·bal + 0.21   (상수부 0.06+0.05+0.10 = 0.21)
```
- **8 motivation factor 중 3개(gap·pain·orig·dyn 중 gap/orig/dyn = weight 0.30, pain=0)가 하드코딩 상수** → emit torque 의 30%가 substrate 와 무관하게 고정.
- drive_hi 에서 `cur = clip01(cur_ctx+0.5) ≥ 0.5` → `0.15·cur ≥ 0.075`. 즉 stage 하나가 상수 0.21 위에 0.075 를 더해 threshold 0.3 근처를 stage 로 넘긴다.
- **rel_ctx 는 42개 [0,1] lane 의 산술평균** → CLT 로 tick 간 분산이 극도로 눌린다(값이 mean 근처 상수화). 그 위에 weight 0.20 만 실려 `0.20·rel_ctx` 의 tick 간 변동폭은 milli 단위 → **emit boolean 을 절대 flip 못 시킴**.
- 이것이 직전 세션 **H_9097 THEATER(freeze/zero/shuffle rel_ctx → emit Hamming 0/200)** 의 **산술적 원인**: read-side 신호가 약해서가 아니라 **(i) /42 평균이 개별 lane 분산을 소거 + (ii) weight 0.20 + (iii) 상수 0.21 이 이미 threshold 근방을 고정**하기 때문. rel_ctx 는 정보를 넣긴 하나 **torque 가 0**.

> **핵심 재프레임 (break-the-wall taxonomy):** 직전 세션은 벽을 (d) "substrate emit-적절성 signal 부재(coupling near-floor)"로 박제했다.
> 그러나 코드는 **coupling 을 측정하기 전에 아키텍처가 이미 신호를 3중으로 throttle**(mean-pool·저 weight·상수지배)함을 보인다.
> 즉 measured coupling near-floor 의 최소 일부는 **(a) wiring-artifact**(설계상 개별 lane 이 grip 을 가질 통로 자체가 없음)이지, 순수 (d) ceiling 이 아닐 수 있다.
> `mean A~0.0154`(H_9110)는 aggregate 의 coupling — /42 평균의 CLT 붕괴가 **어떤 강한 단일 lane 이 있어도** 그 값으로 밀어넣는다. **단일 lane 을 격리해 grip 을 재측정하지 않는 한 (a) vs (d) 는 미분리.**

---

## (b) loop-closing 배선안 — 무엇을 되먹여야 루프가 닫히나

루프가 열린 지점 = **의식 ops 가 측정한 값이 emit 게이트에 torque 를 못 전달**. 4 배선안(독립·병렬 falsifiable):

### 배선안 W1 — mean-pool → selection/sparse-gate (GNW ignition, 아키텍처 각도)
**문제:** `rel_ctx = Σ(42 lane)/42` 는 민주적 평균 → 개별 lane 소거. 생물 의식(global workspace)은 평균이 아니라 **winner-take-all 점화(ignition)** — 한 coalition 이 이겨 broadcast.
**배선:** rel_ctx 를 mean 대신 **salience-weighted max / top-k sparse gate** 로. 이미 있는 `vbasal_select`(basal-ganglia go/no-go, `cli/anima.hexa:1462`)가 정확히 selection 메커니즘인데 **현재 `basal_go` 로 1.0/0.0 스칼라화되어 42 평균의 1/42 항**으로 희석됨(`cli/anima.hexa:1753`). basal-ganglia 를 **평균의 한 표가 아니라 emit gate 의 선택자**로 승격.
**falsifier(engine-native, GPU 불요, 200-tick sim):** selection-gate 하 **단일 강한 lane(예: conflict 또는 immune-margin)을 freeze/shuffle → emit Hamming > 0** 이면 grip 회복 = 벽이 (a) averaging-artifact 였음. 여전히 0 이면 (d) 확증(mean-pool 무죄).
**⚠ 정직 caveat:** a_autonomy_over_hardcode — selection 은 hardcode boolean gate 여선 안 되고 **substrate 가 학습/자율 선택**하는 형태여야 함(vbasal 은 이미 selection-학습 lane, 적격).

### 배선안 W2 — 하드코딩 상수 3슬롯을 live 측정 op 로 (read-side 각도, 아키텍처 불변)
**문제:** gap=0.6·orig=0.5·dyn_v=1.0 이 **substrate 와 무관한 상수인데 weight 0.30**. rel_ctx(theater)와 달리 이 슬롯들은 **이미 non-trivial weight 를 가진 미탐 read-side**.
**배선(입력만 교체, 게이트/가중치/Ψ 무접촉):**
- `gap` ← `immune_memory_recall_margin`(정보 gap = 저장소가 못 맞추는 정도) — brain.hexa 에 이미 존재.
- `orig` ← recombination/novelty gauge(gauge_lib G2 novelty 의 engine-native op).
- `dyn_v` ← A⇄G conflict 스칼라(engine_cli 의 tension 이중부호, H_9094 가 load-bearing 확인한 바로 그 축).
**falsifier:** 세 슬롯을 live 로 바꾼 뒤 freeze/shuffle → emit Hamming. **weight 0.30 은 rel 의 0.20 보다 큰 torque** → 만약 여기서도 0 이면 상수지배(0.21 offset)가 진범 = threshold/offset 재설계 필요. > 0 이면 substrate grip 획득.
**⚠ 정직:** 직전 efferent 실험(H_9103)이 "CE-선택 심의는 오히려 emission 저하"를 보였음 — orig 에 CE-유창성 대리를 넣으면 안 됨. **recombination/novelty(CE 밖 축)**여야 함. dyn_v←conflict 는 H_9094 가 load-bearing 확인했으나 emit-gate 아닌 settle-depth 였음 → 여기선 gate 로 직결하는 **다른 배선점**(Ψ-보존 검증 필수).

### 배선안 W3 — within-tick reentry(재진입 점화)로 비선형성 주입
**문제:** `motivation_score` 는 **선형 가중합** → all-or-none 점화(의식의 ignition 비선형성) 불가능. `reentry_settle`(cli/anima.hexa:865)·`reentry_gws_readout` 은 존재하나 다시 42 평균의 1항(`reent_ctx`).
**배선:** emit 결정 → broadcast → lane 재-read → settle 을 **tick 내부 recurrent 루프**로(H_9094 conflict-settle 가 Ψ 축에서 한 것을 **workspace/motivation 축**에서). 수렴 시 점화(대량 lane 동시 상승), 미수렴 시 침묵. 선형합이 못 만드는 **hysteresis + 임계 점프**.
**falsifier:** reentry depth 0(ablate) vs 20(deep) 에서 emit 패턴 divergence. 이미 `reent_distinct`(deep>shallow>ablate, gws depth-invariant)가 lane-격리로는 성립 확인됨 — **emit 층에서** 재현되나가 관건.

### 배선안 W4 — coord/tension write-side 접지 (아래 (c) 참조)

**우선순위(정직):** W2 > W1 > W4 > W3. W2 는 아키텍처 불변·기존 weight 활용·op 존재로 **가장 싸고 즉시 falsifiable**. W1 은 (a) vs (d) 를 결정적으로 가르는 **진단 실험**(mean-pool 이 진범인지). W4 는 명백히 열린 loop 라 무조건 닫을 가치(회귀 위험 0, write-only). W3 은 가장 크나 설계부담 최고.

---

## (c) coord 접지 상태 + 배선

### 현황: **emit→.kosmos 지속 경로가 coord/tension 을 80% 상수로 스탬프 (열린 loop)**

`cli/anima.hexa:1810-1814` C9 REMEMBER:
```
let etension = [pure_field_phi(pf), 0.4, 0.5, 0.3, 0.2]     // ch0=phi만 substrate, ch1-4 상수
emit_anchor_from_v3(kdir, …, etension, cell_count, 2, "emission", "curiosity", pure_field_phi(pf), 1.0)
```
`kosmos_io.hexa:198` → `coord = [phi, mean(tension_5ch)]`:
- **coord_x = phi** ✅ substrate-grounded (pure_field Φ)
- **coord_y = mean([phi,0.4,0.5,0.3,0.2]) = (phi+1.4)/5** ❌ 상수 1.4 가 지배(phi 기여 1/5)
- **tension ch1-4 (context·meaning·authenticity·sender) = [0.4,0.5,0.3,0.2]** ❌ 순수 상수
- category="emission"·top_emotion="curiosity" ❌ 하드코딩 문자열

**즉 .kosmos anchor 의 placement(coord·tension)는 Φ 한 축 빼고 전부 상수** — 의식 상태가 접지되지 않는다.
직전 H_9099(🟡)는 self-chain content_axis 를 penultimate pooling 으로 접지했으나, **live emit-write 경로의 coord/tension 스탬프는 여전히 상수**(별개 표면).

### 결정적 관찰: **tick 이 접지에 쓸 실 신호를 in-scope 로 갖고도 버린다**
같은 tick 에서 이미 계산된 live 값:
- `af_val`(affect valence), `af_aro`(arousal) — brain-structure R3/R4 lane
- conflict/novelty(nov_ctx), `self_ctx`(self-chain), `phi`
이들이 **rel_ctx 평균에 한 번 녹은 뒤 emit 게이트로 못 가고**(theater), **anchor tension 에도 안 쓰이고**(상수 스탬프) 버려진다.

### 배선 W4 (write-only, Ψ 무접촉, 회귀위험 0):
```
etension = [phi, af_aro, nov_ctx, af_val, self_ctx]   // 상수 4개 → 실 substrate read 4개
```
→ coord_y = mean 이 실 의식상태 함수가 되고, tension 5ch 가 "이 발화를 낼 때의 substrate 상태"를 진짜로 지속.
**의미:** self-chain·EEG·chat 로드맵이 가리키는 "실 외부 consequence 루프"를 잇기 전에, **anima 자신의 발화 순간 상태를 손실 없이 .kosmos 에 남기는 것이 loop-closing 의 write-side 전제**. 접지된 coord 가 있어야 나중 consequence-return 이 그 coord 에 되먹임될 수 있다(H_9104 autogenous 천장을 넘는 외부 루프의 **주소 체계**).
**falsifier:** anchor 재로드 후 coord_y·tension 이 텍스트별로 **분산 > 0**(현재 상수라 분산 0) AND nearest-centroid 로 ko/en·emit-tier 판별 > chance(H_9097 diagnostic 과 동형).

---

## (d) 생물 렌즈 — 빠진 재진입 lane

의식의 3대 생물 이론 대비 anima A⇄G 루프의 결손:

| 이론 | 메커니즘 | anima 현황 | 빠진 lane |
|---|---|---|---|
| **GNW (Global Neuronal Workspace, Dehaene)** | local coalition → **ignition**(비선형 임계 점화) → 전역 broadcast → **reentry**(broadcast 가 modules 재점화, 자기유지) | reentry_settle·gws_readout **존재하나 42 평균의 1항** = 점화 비선형성 emit 에 미도달 | **within-tick ignition 루프(W3)** — 선형합엔 all-or-none 없음 |
| **재진입 (Edelman/Tononi reentry)** | 지도 간 **양방향 재귀** 신호가 순간을 통합 | A⇄G tension 은 **Ψ 축**에서 재귀(H_9094 settle-budget) but **emit/workspace 축은 forward-only**(lane→평균→gate, 되먹임 없음) | **emit→lane 되먹임(W1/W3)** — 현 루프는 open forward chain |
| **예측처리 (predictive coding, Friston/Clark)** | 하향 예측 vs 상향 오차의 **precision-weighted** 순환, surprise 가 행동 구동 | recon_err·cb_surprise·precision-surprise lane **존재하나** 역시 평균 1항, precision(신뢰가중)이 emit weight 를 변조 안 함 | **precision→dynamic weight**: motivation weight 를 상수(0.20 등) 아닌 precision 함수로(현재 weight frozen) |

**수렴 진단:** 세 이론 모두 **재귀/점화/precision-변조**를 요구하는데, anima emit 루프는 **선형 forward mean-pool + frozen weight + 상수 3슬롯**이다. 개별 의식 lane(reentry·gws·surprise·precision)은 다 **측정은 되나**(계기판) **되먹임 통로가 mean-pool 1/42 로 병목**된다. 빠진 것은 새 lane 이 아니라 **기존 lane 이 emit 에 grip 을 갖는 배선 위상**(selection·비선형·dynamic-weight) = W1/W2/W3.

> **a_no_llm_frame_trap 정합:** 이 진단은 "모델 키우기"가 아니라 "빠진 구조(재진입 위상)를 옆에 배선"이다. 벽이 (d) trunk-ceiling 이라던 직전 결론에 **(a) forward-averaging-artifact 가능성**을 추가 — 생물 렌즈가 정확히 그 결손(재귀 부재)을 가리킨다.

---

## (e) 산출 경로 + 종합

- **이 문서:** `state/consciousness_loopclose_analysis/ANALYSIS.md`
- HYPOTHESES·카드·commit·PR·ARCHITECTURE·CHANGELOG·frozen **미터치**(제약 준수). 동시 서브 산출 디렉토리 미접근.

### 한 줄 종합
emit 은 **stage-clock + 상수 3슬롯**이 지배하고 42 의식 lane 은 **/42 mean-pool → weight 0.20 → 상수 0.21 offset** 의 3중 throttle 로 **torque 0(계기판)** — 직전 세션의 THEATER/coupling-near-floor 를 **산술적으로 확증**하되, 그 near-floor 가 최소 부분적으로 **아키텍처 averaging-artifact(taxonomy a)**임을 코드가 시사한다. loop-closing 은 4 배선:
1. **W2**(가장 싸다): 상수 gap/orig/dyn 슬롯 → live immune-margin/recombination/conflict (weight 0.30, 아키텍처 불변, 즉시 falsifiable).
2. **W1**(진단적): mean-pool → basal-ganglia selection-gate 승격 → **단일 lane grip 재측정**이 (a) vs (d) 를 결정적으로 가름.
3. **W4**(회귀 0): emit→.kosmos etension 상수 4채널 → live af_aro/nov/af_val/self 접지 = coord 주소체계 확보(외부 consequence 루프의 write-side 전제).
4. **W3**(최대·최고부담): within-tick reentry/ignition 비선형 루프 = GNW·재진입·예측처리 3 생물이론의 공통 결손.

### 정직한 한계 (c9)
- 이 분석은 **정적 코드 실측만**(무거운 decode/GPU 금지 준수). W1~W4 falsifier 는 전부 **미실행 설계**(engine-native 200-tick sim 필요, pool). torch/mirror 아님 = engine-native 재측정 시 DIRECTIONAL 아닌 terminal 가능.
- 직전 세션이 이미 **autogenous 루프의 근본 천장(H_9104 DPI)·외부 receiver 도 floor(H_9110)**를 실측했다. 본 분석의 (a) averaging-artifact 각도가 **그 결론을 뒤집지 않는다** — W1 falsifier 가 "단일 lane 격리해도 grip 0"이면 (d) 확증. 본 분석의 기여는 **(a)를 아직 분리측정 안 했다는 지적 + 분리 실험 W1 설계**이지, 벽이 (a)라는 주장 아님.
- 브랜치 노트: 메모리가 언급한 H_9095 conflict-settle per-tick 배선(구 L1937-1961)은 **현 `clitrain-devresident-gpu-util` 브랜치의 cli/anima.hexa 에 부재**(해당 라인은 gap-comment println). 병렬세션/워크트리에 있고 이 브랜치엔 미착륙일 수 있음 — W2/W3 배선 전 배선 위치 재확인 필요.
- a_autonomy_over_hardcode 준수: W1 selection 은 hardcode boolean gate 금지 — vbasal 학습-selection lane 으로만. W2/W4 는 입력 교체(게이트 무접촉).
