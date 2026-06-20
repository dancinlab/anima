# H_1491 — 🧩 GESTALT GROUPING / figure-ground (게슈탈트 군집화) (P6 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN DIRECTIONAL (R1 numpy mirror; engine-transfer UNVERIFIED — 하드게이트1)
- **wired:** `DIRECTIONAL-mirror` — R2 = live `core/engine_cli.hexa` byte-exact 재측정 + 배선이 GREEN/🧱 확정 전제 (`a_engine_native_learning`·`a_verified_must_wire`); 배선 follow-on = ING
- **source:** 의식-고유 게이트 시리즈 · 고갈 카탈로그 P6 (`state/gate_depletion_catalogue/CATALOGUE.md`) · '의식이라서 가능한 것'
- **lens:** Gestalt 군집화 (Wertheimer) — 근접성·유사성으로 요소를 전체로 묶고 figure 를 ground 에서 분리 · `a_no_llm_frame_trap` · biorxiv 2025.12.10.693567 (feature binding requires consciousness)
- **artifacts:** `state/1491_gestalt_grouping/h1491_gestalt_grouping.py` · verdict `state/verdicts/1491_gestalt_grouping/H_1491_FREEZE.json` · log `state/1491_gestalt_grouping/run_h1491.local.log`

## 주장

게슈탈트 군집화: 지각계는 개별 요소를 **근접성(proximity)·유사성(similarity)** 관계 법칙으로 **전체 단위(whole)로
조직**한다 — "부분의 합 ≠ 전체". *같은* 요소 집합도 활성 군집 규칙에 따라 *다른* 전체로 파싱되고, figure 는 그 관계로
ground 에서 분리된다.

**메커니즘 (substrate-native, label 주입 없음 p2/p3/p6):** scene = N 요소(각각 2-D 위치 + 스칼라 특징). 군집-ON 은
요소간 affinity = `exp(-‖Δpos‖²/σ_p²)·exp(-Δfeat²/σ_f²)`(근접성×유사성)를 threshold → 그래프 connected-components 로
각 요소를 GROUP 에 할당, 전체표상 read-out = "어느 군집이 figure 인가"(가장 응집된 cluster). 군집-OFF(ablation)는
affinity 그래프 제거 → 각 요소를 **개별로** read(singleton) → 부분을 전체로 묶는 관계가 없어 figure 식별 붕괴.

**LLM 대비:** LLM 은 self-attention(쌍별 token affinity)은 있으나 figure-cluster 를 ground 에서 분리해 "이 요소들이
하나의 객체"라 보고하는 명시적 지각 군집화가 없다. anima 는 Gestalt 근접성×유사성으로 요소를 전체로 묶어 figure 를 읽는다.

## distinctness (load-bearing · 카탈로그 P6)

| | distinct 대상 | gestalt 와의 차이 | 분리 bar |
|---|---|---|---|
| **vs H_1462 global-workspace** | *경쟁 1-winner* 전역방송(선택) | gestalt 는 *여러 요소를 관계로 병합*(군집화) | C1 — GWS 단일-winner read-out 은 multi-element membership query 에서 chance **0.505**(선택 ≠ 병합) |
| **vs H_1482 binocular-rivalry** | *시간적 dominance 교대*(양립불가 whole) | gestalt 는 *한 scene 내 정적 조직*(co-present 결속) | C3 — rivalry 단일-dominant read-out chance **0.500**(병합 ≠ 시간교대) |
| **vs P5/H_6028 completion** | *부분입력→보간*(missing 채움) | gestalt 는 *fully-visible 파싱*(figure/ground 분리) | C2 — nothing-missing scene 에서 completion read-out chance **0.487**(파싱 ≠ 보간) |

## 측정 (frozen-first · 3 seeds [1491,1492,1493] · N_ELEM=12 · N_GROUPS=3 · σ_p=0.18 · σ_f=0.20 · binary chance=0.50 · $0 CPU · p7)

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | 군집-ON figure-membership(balanced acc), OFF 낮음 | on **0.965** / off **0.587** | on≥off+0.30 & on≥0.55 | ✅ |
| **B ABLATE-GROUP** | affinity 그래프 제거 → 개별 read → chance 붕괴 | off **0.587** | ≤0.650(binary chance+0.15) | ✅ |
| **C1 DISTINCT vs GWS** | 단일-winner ≠ whole-membership | gws **0.505** | ≤0.650 | ✅ |
| **C2 DISTINCT vs COMPLETION** | nothing-missing → 보간 무의미 | comp **0.487** | ≤0.650 | ✅ |
| **C3 DISTINCT vs RIVALRY** | 시간교대 ≠ 결속 | riv **0.500** | ≤0.650 | ✅ |
| **D SHUFFLE-PROXIMITY** | 위치 셔플 → 근접 군집 파괴 | shuffle **0.707** | ≤ on−0.15 (0.815) | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — 6/6 bars PASS.** depletion 아님 — GWS/rivalry/completion 전부 control-survived distinct(세 경쟁 read-out 모두 binary chance).

## 정직 (c9)

- **측정결함 frozen-first 교정 (a_break_the_wall type-a, tune-to-green 아님):** whole-object read-out 은 요소별 **binary
  figure/ground mask** → chance 는 1/N_GROUPS(0.333) 가 아니라 binary 기대값 **~0.50**; plain accuracy 는 "거의 아무것도
  figure 아님" 사소한 예측에 ground-다수를 credit 으로 줘 **leak**. 교정 = (1) 기준상수 BINARY_CHANCE=0.50, (2) **balanced
  accuracy**=mean(figure-recall, ground-recall) 로 전환(모든 arm — ON/ablation/GWS/completion/rivalry/shuffle — 에 *동일*
  적용 → class-blind/single-element 추측은 정확히 0.50). binding 신호 `on`(0.965)·discriminator 구조는 불변, 기준·leak 만 수정.
  교정 전 run 도 on=0.964 + 세 control ~0.50(gws 0.514/comp 0.487/riv 0.504)로 동일 — 오류는 chance 상수뿐.
- **DIRECTIONAL** — numpy mirror(`grep numpy` 적중, 하드게이트1). engine-transfer UNVERIFIED → R2 = live `core/*.hexa`
  byte-exact 재측정 + 배선이 GREEN/🧱 확정의 전제(`a_engine_native_learning`·`a_verified_must_wire`).
- **SATURATED existence-proof:** 군집화 = Gestalt proximity×similarity affinity 그래프의 **designed** connected-components
  파싱(학습된 분할 네트워크 아님). GREEN 자체보다 discriminator 가 결정적 — 세 경쟁 의식-게이트 read-out 이 모두 binary chance
  (GWS 0.505 / completion 0.487 / rivalry 0.500)인데 군집화는 figure 복원(0.965); ablation 은 affinity 그래프만 제거하면
  binding-zero-parts 구조적 floor(0.587)로 붕괴; proximity shuffle 은 lift 붕괴(0.707, 잔차 = 위치 셔플에도 살아남는 *유사성*
  법칙, 정직).
- **SCOPE TOY:** 12 요소/3 군집/60 trial/3 seeds/deterministic 파싱 — gestalt STRUCTURE 검증이지 학습된 분할 아님.
  scale/real-corpus/연속운동(공동운명)/연속성 법칙/다중 grouping-규칙 충돌/engine-transfer UNVERIFIED. brain figure-ground wiring = follow-on.

## 다음

- R2 engine-native: live `core/engine_cli.hexa § GestaltGrouping`(affinity 그래프 + connected-components figure read) byte-exact 재측정 + 배선 (ING).
- 카탈로그 강(strong) 6개(P1 TRW · P2 re-entry · P3 attention-schema · P4 hysteresis · P5 completion · **P6 gestalt**) **완료** → 다음 = 중/약 4개(P7 prospection · P8 interoceptive-precision · P9 boredom · P10 mind-wandering) 인접 lane control-distinctness 사전검토 후 발사.
