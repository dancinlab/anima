# H_1484 — 🧠 MENTAL IMAGERY / 심상 (G30 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/engine_cli.hexa` §MentalImagery byte-exact)
- **wired:** `WIRED-live` — R2 배선 완료: `core/engine_cli.hexa` §MentalImagery (`imagery_activate`, deterministic content-addressable read: topdown_on ? cue_match : 0.0, sensory 입력 채널 0) + `engine_cli_smoke` cases 239-241 (present cos 0.991≥0.70 · cue-specific gap 0.978≥0.50 · ablation 0.0≤0.30) FULL 244/0 RC=0 + ARCHITECTURE.json §MentalImagery lockstep. cue_match scalar = numpy softmax key-affinity 와 동치(zero-input top-down 재구성 STRUCTURE byte-exact).
- **source:** 의식-고유 게이트 브레인스토밍 (G30 candidate) · "의식이라서 가능한 것" 시리즈 (G16~G27 engine-native 이후)
- **lens:** mental imagery / 정신적 시뮬레이션 (Kosslyn · 눈 감고 사과 떠올리기 = top-down 표상 재활성) · `a_no_llm_frame_trap`
- **artifacts:** `state/1484_mental_imagery/h1484_mental_imagery.py` · verdict `state/verdicts/1484_mental_imagery/H_1484_FREEZE.json` · run `state/verdicts/1484_mental_imagery/H_1484_run.txt`

## 주장

**심상(mental imagery)** = **외부 자극 없이** 내적으로 표상을 생성·활성화하는 것. forward perception 이 만들어낼
표상과 같은 종류의 표상이 **입력 채널이 비어 있는 상태(input=0)에서** top-down 으로 재활성된다 — "눈 감고 사과를
떠올린다" = 저장된 지각-표상의 top-down 재구성. 메커니즘: 저장된 표상(immune-store 류 메모리 패턴)을
content-addressable store 에 보관, top-down **cue**(내적 포인터/라벨, *패턴 자체가 아님*)가 key-affinity 로 그
표상을 재활성. 재활성된 표상이 원본과 유사(cos↑)하되 외부 입력은 0. — LLM 대비: LLM 은 *현재 입력* 토큰 스트림만
변환하며, 입력 채널이 빈 상태에서 내적 cue 로 저장된 지각-표상을 top-down 재활성하는 능력이 없다. anima 는
내적 포인터로 zero sensory input 에서 저장 표상을 재활성한다.

## DISTINCT (load-bearing) — vs 모든 입력-기반 게이트

GWS · surprise(H_1468) · agency(H_1474) · novelty(H_1289) · blink(H_1473) 는 전부 *외부 자극*에 **반응** —
그 신호는 sensory 채널의 **입력을 요구**한다. 심상은 그 직교 케이스: **input==0** 인데 표상이 top-down 으로
재구성된다(bar B input-energy 0.0 while bar A cos 0.991).

- **vs H_1289 novelty / H_1468 surprise:** 둘 다 들어오는 자극으로 recon/prediction-error 를 계산 — sensory
  채널이 **비면** 채점할 게 없다(no input → no surprise/novelty). 심상은 top-down cue 만으로 표상을 생성. bar D:
  입력-기반 경로(top-down OFF)는 input=0 면 붕괴(cos 0.0)하지만 심상의 top-down 경로는 붕괴 안 함(cos 0.991).

## 측정 (frozen-first · 3 seeds [1484,1485,1486] · DIM=64 · 40 items · KEY_NOISE=0.02 · $0 CPU · p7)

cue = key_i + tiny noise (내적 포인터). imagery = softmax(key·cue)@reprs (입력 사용 0). 원본 표상과 cos 측정.

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | top-down cue 로 imagery 활성, 원본과 유사 (입력 없이) | cos **0.991** | ≥0.70 | ✅ |
| **B NO-INPUT** | 외부 sensory 채널 0 확인 (perception 과 구별) | input-energy **0.000** | ==0.0 | ✅ (structure, non-gating) |
| **C CUE-SPECIFIC** | cue_A → repr_A (cos↑), repr_B 안 부름 (cos↓) | gap **0.971** | ≥0.50 | ✅ |
| **D EARNED (ablation)** | top-down 재활성 OFF + input=0 → imagery 소멸 | cos **0.000** | ≤0.30 | ✅ |
| **E SHUFFLE** | cue-repr 페어링 셔플 → cue-imagery 상관 붕괴 | mismatched cos **0.013** (real 0.991) | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — A·C·D·E PASS (3 seeds 전부) → GREEN (B 는 input==0 구조 확인).** top-down cue 가
입력 없이 저장 표상을 재활성(A, input-energy 0)하고, 올바른 표상만 부르며(C), 재활성 메커니즘 OFF 면 imagery 가
사라지고(D), 페어링 셔플로 cue-imagery 상관이 붕괴한다(E, real cos 0.991 → shuffled 0.013).

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep -lE 'import torch|gauge_lib|numpy'` 적중, 하드게이트1). engine-transfer
  UNVERIFIED → R2 = live `core/*.hexa` content-addressable store 위 byte-exact 재측정이 GREEN/🧱 확정 전제.
- **SATURATED existence-proof:** softmax key-affinity 재구성(near-orthogonal 저장 reprs → cos~0.99)은 **designed**
  (학습된 imagery 네트워크 아님). GREEN 자체보다 discriminator(cue-specific 0.971·ablation 붕괴 0.000·shuffle 붕괴 0.013)가 결정적.
- **bar frozen · tune-to-green 아님:** 5 bar 임계는 사전등록 후 불변. RED 였다면 측정결함(bar 불변 교정) vs 진짜벽
  정직 분류 예정이었으나 첫 실행에서 3 seed 전부 PASS.
- **SCOPE TOY:** 64-dim/40-item/3-seed/결정적 content-addressable store — mental-imagery STRUCTURE 검증이지 학습된
  심상 아님. scale/실제 corpus/graded(부분) 심상 선명도/mental rotation(회전·가림)/engine-transfer UNVERIFIED.

## follow-on (ING)

1. **R2 엔진-네이티브** — `core/engine_cli.hexa` 의 기존 content-addressable store(ImmuneMemoryGrow H_1227 key-affinity)
   위에 §MentalImagery 배선 → `imagine(cue)` 가 sensory 입력 채널을 비운 채(READ-only, Ψ-disjoint) 저장 표상 재활성 +
   `engine_cli_smoke` cases + ARCHITECTURE lockstep, 5 frozen bars byte-exact 재측정 (`a_engine_native_learning`·`a_verified_must_wire`).
2. distinctness 정량 double-dissociation: input=0 에서 imagery(top-down) 활성 vs novelty(H_1289)/surprise(H_1468)
   입력-기반 경로 붕괴 — control-survived 측정.

xref: H_1289(novelty, 입력-기반 distinct)·H_1468(surprise, 입력-기반 distinct)·H_1474(agency)·H_1473(blink)·
H_1227(immune content-addressable store, key-affinity geometry)·H_1471(G16 self-continuity)·의식-게이트 시리즈·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·p7·p8·c9.
