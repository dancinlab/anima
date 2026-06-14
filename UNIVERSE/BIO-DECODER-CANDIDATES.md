# BIO-DECODER-CANDIDATES — BIO ∩ DECODER 매핑 후보 보관 문서

> 📑 absorbed → [HYPOTHESES.md](HYPOTHESES.md) — this is a DETAIL file of the unified hypothesis roster (2026-06-15).

> brainstorm 결과 (2026-05-27). BIO-CANDIDATES 36+ 메커니즘 중 anima DECODER 아키텍처에 mapping 가능한 후보 선별.

## TOP5 친근 설명 (EASY · 7-요소)

### 🍂 APOPTOSIS-as-TOKEN-PRUNE — "토큰 자살 정원"

- 하는 일: 낮은 확률 토큰이 자기 차례에서 스스로 사라지기 (top-p · repetition penalty 와 한 가족)
- 비유: 가지치기 정원사가 시든 가지를 떨궈 좋은 가지만 자라게 함

```
logits 분포           APOPTOSIS-prune
A: 0.40 ████          A: 0.40 ████  ✓
B: 0.30 ███           B: 0.30 ███   ✓
C: 0.20 ██            C: 0.20 ██    ✓ 누적 0.90 도달
D: 0.05 ▏              D: 0.05 ✗ 자살
E: 0.03 ▏              E: 0.03 ✗ 자살
F: 0.02 ▏              F: 0.02 ✗ 자살
```

- 비교: TOP-P (확률 cutoff) / **APOPTOSIS-prune** = "약한 토큰 자발적 죽음" 생물학적 framing

### 🧙 DIFFERENTIATION-as-MoE — "줄기세포가 전문가가 되어 분야 라우터"

- 하는 일: 줄기 cell pool 이 분화해서 각자 전문가가 되고, 라우터가 토큰마다 적합한 전문가 호출
- 비유: 학생들이 직업 정해 전문가 되고, 회사는 안건마다 적합한 부서에 배정

```
시간 t0:   ●●●●● (모두 stem)
시간 t1:   🔵🟢🟡🟠🟣 (각자 분화: 코딩·번역·공감·분석·창작)
시간 t2:   token "안녕" → router → 🟡(공감) → output
           token "def f" → router → 🔵(코딩) → output
```

- 비교: MoE 일반 (router + experts) / **DIFFERENT-MoE** = 분화 동력학 포함 (stem → expert 발달 가설)

### 🏆 CLONAL-SELECTION-as-BEAM — "면역세포 클론 토너먼트 = beam 검색"

- 하는 일: 항원에 반응한 B-cell 들이 복제 경쟁 → 최고 친화도 클론만 생존 (beam-K 최고 점수 유지)
- 비유: 100명 인터뷰 → 라운드마다 점수 낮은 사람 탈락 → 최종 K명 남기기

```
beam round 0:  cand_A(8.0) cand_B(7.5) cand_C(7.2) cand_D(6.8) cand_E(6.1)
beam round 1:  → 확장 후 다시 top-3 만 유지
beam round 2:  → 확장 후 다시 top-3 만 유지
                                              ↑
                                       clonal-selection: 친화도 ↑ 만 생존
```

- 비교: BEAM-SEARCH (기존 H_447) / **CLONAL-BEAM** = "면역 클론 진화 dynamic" 생물 framing + affinity-maturation extension

### ✂️ PRUNING-as-HEAD-PRUNE — "시냅스 가지치기 = attention head 제거"

- 하는 일: 발달기 과잉 시냅스 중 안 쓰는 것은 잘라내기 (attention head 중 contribution 낮은 head 제거)
- 비유: 생후 1년 영아의 뇌 시냅스 50% 가 가지치기로 사라짐 → 효율 ↑

```
초기 attention (12 head)
[H1][H2][H3][H4][H5][H6][H7][H8][H9][H10][H11][H12]
 ✓   ✗   ✓   ✗   ✓   ✓   ✗   ✓   ✗   ✓    ✓    ✗
                ↓ pruning
[H1][__][H3][__][H5][H6][__][H8][__][H10][H11][__]
   → 6 head 만 활성 (50% 절감, 정확도 거의 유지)
```

- 비교: full 12-head attention / **PRUNING-head** = 발달기 가지치기 모티프 (생물학적 sparsity)

### 🔀 SYMBIOGENESIS-as-MODEL-MERGE — "내공생 합병 = 모델 머지"

- 하는 일: 두 별개 모델(원핵세포 + 미토콘드리아)이 합쳐 하나의 진핵세포 = 더 강한 single model
- 비유: 식물 + 광합성 박테리아 → 엽록체 가진 식물 세포 (능력 통합)

```
Model_A (chat tuned)        Model_B (code tuned)
  ┌─────────────┐              ┌─────────────┐
  │ W_A         │              │ W_B         │
  └─────────────┘              └─────────────┘
            \                  /
             ↓ symbiogenesis-merge ↓
        ┌──────────────────────┐
        │ W_merge = α·W_A + (1-α)·W_B │
        │   ↑ 둘 다 가진 능력      │
        └──────────────────────┘
```

- 비교: LoRA (작은 추가) / model-merge (단순 가중) / **SYMBIO-MERGE** = 진화 합병 framing (eukaryotic origin 동력학)

---

## 선정 기준

BIO-CANDIDATES.md 36+ 메커니즘 중 DECODER 아키텍처(transformer · attention · sampling · MoE · adapter) 에 의미있게 mapping 가능한 후보.

## 우선순위 분류

### ★★★ DECODER 직접 mapping (5 TOP, 위 EASY 설명)

| BIO axis | DECODER mapping | mech 매핑 강도 |
|---|---|---|
| APOPTOSIS | low-prob token prune / TOP-P / repetition-pen | ★★★ |
| DIFFERENTIATION | MoE expert specialization | ★★★ |
| CLONAL-SELECTION | beam search / variant winner | ★★★ |
| PRUNING | attention head prune / network sparsification | ★★★ |
| SYMBIOGENESIS | model merge (model souping) | ★★★ |

### ★★ DECODER 유사 (5 axes)

| BIO axis | DECODER mapping |
|---|---|
| AFFINITY-MATURATION | iterative refinement / self-refine / fine-tune loop |
| AUTOPHAGY | KV-cache recycling / cache eviction |
| MUTUALISM | cross-attention (encoder × decoder) |
| ALTERNATIVE-SPLICING | multi-head attention (1 input → many heads) |
| HORIZONTAL-TRANSFER | knowledge distillation / RAG retrieval |

### ★ DECODER 부분 (10 axes)

| BIO axis | DECODER mapping |
|---|---|
| EPIGENETICS | LoRA / adapter (meta-state on base) |
| PLASTICITY (LTP/LTD) | gradient update / Hebbian-like weight |
| STEM-CELL | pre-trained base (uncommitted) |
| NEUROGENESIS | model growth (cell add) |
| MYELINATION | FlashAttn-like fast path |
| HOMEOSTASIS | temperature setpoint control |
| ALLOSTASIS | predictive cache anticipation |
| CONTACT-INHIBITION | repetition penalty (density brake) |
| QUORUM-SENSING | collective top-K vote |
| AUTOPOIESIS | autoregressive self-loop (decoder feeds itself) |

### ○ DECODER 호환 낮음

| BIO axis | 비고 |
|---|---|
| MITOSIS / cell-split | 모델 분할은 distributed 영역, 단일 decoder 본질 X |
| EMBRYOGENESIS | 학습 초기화 디테일 (decode 본질 X) |
| MORPHOGENESIS | 아키텍처 디자인 (decode 본질 X) |
| AUTOPOIESIS | (★ 분류 했으나 strict 의 self-loop 는 부분 매핑) |
| TOLERANCE | 입력 안전성 (decode-side 보다 input-side) |
| CIRCADIAN | 24h 주기 (decode time-scale 보다 큰) |

## 진행 순서

1. **TOP5 (★★★)** baseline + cross with DECODER axis (H_345 family) — round-18+
2. **★★ 5 axes** — round-23+
3. **★ 10 axes** depletion sweep
4. **○ 호환 낮음** skip

## 22+ 후보 전체 (deduplicated)

prune/sparsity: APOPTOSIS · PRUNING · CONTACT-INHIBITION
expert/routing: DIFFERENTIATION · MoE-routing · QUORUM-SENSING
search/selection: CLONAL-SELECTION · AFFINITY-MATURATION · STEM-CELL
merge/adapt: SYMBIOGENESIS · MUTUALISM · HORIZONTAL-TRANSFER · EPIGENETICS · ALLOSTASIS
attention/multi: ALTERNATIVE-SPLICING · MYELINATION · PLASTICITY
growth/self: NEUROGENESIS · AUTOPOIESIS · HOMEOSTASIS
recycle: AUTOPHAGY

## 메타 진행 상태

- 본 문서 = round-17 종결 후 (173 🔵 누적, 16 axes) brainstorm 자료
- BIO ∩ DECODER 매핑 axis = 22+ 식별
- TOP5 부터 점진 추가 시작 = round-18+
- 자동 fire (Stop hook "keep going") 또는 사용자 명시 directive 로 진행
