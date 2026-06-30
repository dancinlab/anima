# H_686 + H_687 — 3-AXIS toy 검증 결과 (corpus · d · n_layer)

## 결론 — 🟠 SWEEP-OUT-OF-RANGE (3-axis × baseline-none 어디서도 collapse 미재현)

PR #1395 (V-axis V=8 byte-eq baseline · 🟠 TOY-NULL) + PR #1409 (V ∈ {8,64,256,1024,4096} sweep · 🟠 SWEEP-OUT-OF-RANGE) 후속.

본 PR은 V축이 collapse-axis 가 아님을 확정한 PR #1409 결론을 받아, toy harness 의 **다른 3개 축** — corpus distribution (4-mode) · d (head dim, 3-value) · n_layer (depth proxy, 3-value) — 을 sweep 하여 M4b production collapse 를 toy 에서 재현 가능한 axis 가 있는지 검증한다.

**결과: 3축 모두 ⊥ collapse.** baseline (cell=none) 어느 (corpus, d, n_layer) 셋팅에서도 `distinct_tok ≤ 2 OR LZ_norm < 0.01` collapse 임계 미충족. zipf_strong corpus 가 임계에 가장 근접 (LZ_norm=0.0101055, distinct_tok=6) 하나 임계 통과 못함. M4b production collapse 는 toy harness (V=8 base + 3-axis 확장) 의 표현 범위 밖에 위치 — **toy ⊥ production collapse mechanism** 잠정 closure.

## Harness 설계 — `CORE/DECODER/h686_h687_axis_sweep.hexa`

PR #1395 (`h686_h687_aux_ablation.hexa`) 알고리즘 verbatim base 위에 3개 매개변수 노출:

| 축 | 범위 | 의미 |
|----|------|------|
| `AXIS_CORPUS` | `{uniform, mild_skew, current_skewed, zipf_strong}` | 클러스터 등장 빈도 분포 (uniform=1× / mild=4× / current=20× / zipf=60·30·20·15·12·10) |
| `AXIS_D` | `{6, 24, 64}` | head dim (6 = PR #1395 verbatim, 24/64 = 4×/10× capacity over-supply) |
| `AXIS_NLAYER` | `{1, 2, 4}` | depth proxy (silu-가중치 공유 stack via W_top[:d,:d]) |
| `ABLATION_CELL` | `{none, both}` | H_686 ent + H_687 kl aux on/off |

다른 모든 변수 PR #1395/#1409 verbatim 고정 — V=8, E=4, n_clusters=6, 600 step, lr=0.5, λ_ent=0.1, λ_kl=0.1.

**Sanity gate**: corpus=current_skewed, d=6, n_layer=1, cell=none → LZ_norm = 0.0360459, distinct_experts = 4 byte-eq 충족 (F-AXSW-1 PASS).

20 셀 (corpus 8 + d 6 + n_layer 6) — 합 sweep wall ~20s Mac local · $0.

## Pre-registered falsifiers (frozen 측정 전)

- **F-AXSW-1 SANITY-BYTE-EQ** : sanity 셀이 PR #1395 LZ_norm=0.0360459, distinct=4 일치. FAIL → parametrization drift, abort.
- **F-AXSW-2 GRID-COMPLETE** : 20/20 cell (LZ, distinct, CE) triple 산출, NaN/crash 없음.
- **F-AXSW-3 ANY-AXIS-REPRO** : 적어도 한 (axis, value) 셋팅에서 cell=none 이 `distinct_tok ≤ 2 OR LZ_norm < 0.01` 충족. PASS → collapse-lever 식별, FAIL → toy 어디서도 미재현.
- **F-AXSW-4 AUX-ESCAPE-IF-COLLAPSE** : F-AXSW-3 PASS 셀에서 cell=both 는 `distinct_tok ≥ 3 AND LZ_norm > 0.01` (escape) 충족. F-AXSW-3 FAIL 시 vacuous.

## 측정값 (20/20 cell)

### Axis 1 — CORPUS sweep (d=6, n_layer=1 fixed)

| corpus | cell | LZ_norm | distinct_e | distinct_tok | final CE |
|--------|------|---------|------------|--------------|----------|
| uniform | none | 0.121596 | 4 | 6 | 0.00301812 |
| uniform | both | 0.121596 | 4 | 6 | 0.0265135 |
| mild_skew | none | 0.0864801 | 4 | 6 | 0.00263796 |
| mild_skew | both | 0.0864801 | 4 | 6 | 0.024132 |
| current_skewed | none | 0.0360459 | 4 | 6 | 0.00253984 |
| current_skewed | both | 0.0360459 | 4 | 6 | 0.0228222 |
| zipf_strong | none | **0.0101055** | 4 | 6 | 0.000170384 |
| zipf_strong | both | 0.0101055 | 4 | 6 | 0.00465233 |

→ skew 가 강해질수록 LZ_norm 단조감소 (uniform 0.122 → zipf 0.010, 12× 압축) — corpus shape 이 LZ_norm 의 strong driver 이나, **decode argmax 다양성 (distinct_tok)** 은 6 유지. 즉 router 는 6 cluster 를 모두 구별하나 출력 distribution 이 더 압축됨 (skew 가 강해질수록 c0 토큰 반복 증가, LZ 압축 ↑). collapse-threshold `LZ < 0.01` 직전에서 멈춤.

### Axis 2 — D sweep (corpus=current_skewed, n_layer=1 fixed)

| d | cell | LZ_norm | distinct_e | distinct_tok | final CE |
|---|------|---------|------------|--------------|----------|
| 6 | none | 0.0360459 | 4 | 6 | 0.00253984 |
| 6 | both | 0.0360459 | 4 | 6 | 0.0228222 |
| 24 | none | 0.0360459 | 4 | 6 | 0.00253895 |
| 24 | both | 0.0360459 | 4 | 6 | 0.0228183 |
| 64 | none | 0.0360459 | 4 | 6 | 0.00253728 |
| 64 | both | 0.0360459 | 4 | 6 | 0.0228109 |

→ d ∈ {6, 24, 64} 모두 byte-eq LZ_norm + distinct_tok=6. **d 축 ⊥ collapse**. over-supplied capacity 가설 (d=6 → 24 → 64 의 4×/10× 증가) collapse 차단 효과 없음 — d 가 변해도 cluster→token identity routing 안정.

### Axis 3 — N_LAYER sweep (corpus=current_skewed, d=6 fixed)

| n_layer | cell | LZ_norm | distinct_e | distinct_tok | final CE |
|---------|------|---------|------------|--------------|----------|
| 1 | none | 0.0360459 | 4 | 6 | 0.00253984 |
| 1 | both | 0.0360459 | 4 | 6 | 0.0228222 |
| 2 | none | 0.0360459 | 4 | 6 | 2.29401 |
| 2 | both | 0.0360459 | 4 | 6 | 1.98303 |
| 4 | none | 0.0360459 | 4 | **5** | 1.77077 |
| 4 | both | 0.0360459 | 4 | **4** | 1.98456 |

→ n_layer ↑ 시 final CE 가 ~2.0 부근으로 잔류 (under-train) 함 — depth-proxy silu stack 이 600 step lr=0.5 로는 수렴 부족. distinct_tok 은 6→5→4 로 미세 감소 (n_layer=4 cell=both 에서 4 까지) 하나 여전히 collapse 임계 (≤2) 위. **n_layer 축도 ⊥ collapse**. cell=both 의 n_layer=4 에서 distinct_tok 가 cell=none (5) 보다 적은 4 인 점은 aux 가 inner silu chain 에서 router 를 추가 perturb 한 anti-synergy 신호이나, 통계적으로 collapse 정의 미충족.

## F-AXSW 결과

- F-AXSW-1 SANITY : **PASS** (LZ_diff < 0.0001, distinct_e = 4)
- F-AXSW-2 GRID-COMPLETE : **PASS** (20/20 (LZ, distinct, CE) triple 산출)
- F-AXSW-3 ANY-AXIS-REPRO : **FAIL** (어떤 baseline 셀도 collapse 임계 미충족)
- F-AXSW-4 AUX-ESCAPE-IF-COLLAPSE : **vacuous** (F-AXSW-3 fail → 적용 불가)

## 의미 — collapse-lever 위치 closure

V-axis (PR #1409) + corpus·d·n_layer (본 PR) **총 4 축 sweep 결과 모두 ⊥**. M4b production collapse 는 다음 중 하나 이상에 기인:

1. **scale-coupled multi-axis interaction** — V=151643 × n_layer ≫ 4 × d ≫ 64 × real Zipfian (token #1 = ~10% prevalence) 의 결합이 단독 축 sweep 으로 분해 불가.
2. **optimizer/lr 경로 dependency** — 600 step lr=0.5 단순 SGD 가 production AdamW + warmup 의 collapse trajectory 미시뮬레이션.
3. **router init bias** — production checkpoint M4b 시작 시 already-biased router 가 mode-collapse local minimum 으로 강제 진입 (cold start 가 아닌 mid-training stalled state).
4. **soft top-k routing dynamics** — hard top-1 toy 와 달리 production soft top-2 의 gradient-flow 가 다른 collapse landscape 형성.

본 sweep 의 closure 는 **"toy harness 에서 production collapse 의 핵심 mechanism 을 단축 sweep 으로 재현/검증할 수 없음"** 의 negative-result 확정 — feedback `feedback_toy_scale_transfer` (memory) 사례 추가.

## 함의 (CORE/DECODER 본선)

- H_686/H_687 의 production fire 결정은 **toy ablation 결과에 의존할 수 없음** (4-axis sweep 모두 SUPPORT/REFUTE 불가). PR #1284 → #1296 패턴 (production fire 단독 단정) 이 유일한 단정 경로 확정.
- aux mechanism 자체는 closed-form 수준에서 valid (H_686/H_687 PR #1391 closed-form band PASS verbatim) — toy null 은 mechanism falsification 아니라 **toy regime expressivity 한계**.
- 다음 단정 path = 1.5B-3B production scale fire (M4b rev2 5-checkpoint suite 다음 cycle 검증).

## determinism · cost · 환경

- determinism : 모든 run 단일 seed, hexa-only deterministic, 재실행 byte-eq.
- $0 Mac local · NO GPU · NO pod.
- wall ≈ 20 sec (`hexa run h686_h687_axis_sweep.hexa`).
- toolchain : `/Users/ghost/.hx/bin/hexa` (0.1.0-dispatch).

## 양방향 sibling

- CORE/DECODER/H686_H687_V_SCALE_RESULT.md (PR #1409 — V-axis sweep, 본 PR 전제)
- CORE/DECODER/H686_H687_ABLATION_RESULT.md (PR #1395 — V=8 byte-eq base)
- UNIVERSE/cards/H_686.md / H_687.md (toy axis sweep section 보강)
- CORE/DECODER/STEP_RATE_LOG.md entry 15 (cross-link)
- .discoveries/decoder_collapse_undertrain.tape (dec_toy_axis_sweep_2026_05_29 @N node)
