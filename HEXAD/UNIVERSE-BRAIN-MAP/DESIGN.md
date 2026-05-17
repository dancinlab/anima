# INJECTION-PARADIGM-DESIGN — 우주뇌지도 새 학습 paradigm 설계 (anima physics 자체 활용)

> User directive 2026-05-17: "우주뇌지도 그릴때 주입하던 방식의 학습방법 에대해서도 수학적, 물리적 실험, 검증 진행. 새 학습방법 아키텍쳐·패러다임 이름 + 별도 확장자 필요." Wilson 친근한 응답 + 비유 + step-by-step 설계 모드.
>
> g_doc_consolidation 준수: HEXAD/UNIVERSE-BRAIN-MAP/* 내부 통합 (root docs/* 신규 X).
>
> Step-by-step decision gate (Wilson Principle 7) — 결정 한 번에 하나씩, 진행 로그 record-as-you-go.

## 0. 옛 우주뇌지도 학습 방식 — 뭘 했었나

2026-05-07 anima 가 우주뇌지도를 머릿속에 새기려고 이런 corpus 를 만들어서 학습:

```
[anima 우주뇌지도] 사용자: 만다라 Tier 핵심만.
도우미: 만다라는 우주뇌지도 예술 카테고리, 🛸77, top emotion creativity.

[anima 우주뇌지도] 사용자: 열반의 🛸k label 간단히.
도우미: 🛸91 (점수 2.558, 카테고리 의식상태, top emotion peace).
```

**136,125 줄** (21MB) 다 이런 식. `[anima 우주뇌지도]` 라는 prefix 도장 + `사용자/도우미` dialogue + 정해진 답변 양식.

### 결과 — ★ 와 ⚠

★ **knowledge recall 성공** — BG-HS R1 manual_match **13/15** (commit `41c2e1726`). anima 가 우주뇌지도 진짜 외움.

⚠ **P3 leak baking 발생** — 평범한 대화에도 `🛸k label`, `[anima 역할:`, `우주뇌지도 Knuth Tier` 표현이 새어 나옴. SFT 로도 못 지움 (`project_anima_base_ckpt_baked_p3_leak.md` 메모리).

⚠ **chat 능력 NET LOSS** — Phase 1A.5 에서 이 corpus 를 chat SFT 에 섞으니 V5.8 std_greedy **5/5 → 1/5 regression** (`feedback_corpus_quality_over_scale.md`).

## 1. 비유 1 — 왜 P3 leak 이 일어났나

**옛 방식 = 모든 책 표지에 빨간 도장 "사전" 찍어서 학습**

anima 한테 100 권의 책을 줬는데, 모든 책 표지에 큼지막한 빨간 도장으로 "사전" 이라고 찍어놓고 통째로 외우게 한 거야.

```
┌─────────────────────────────────────────────┐
│  📕 [사전] 만다라 = 🛸77 예술                │  ← 모든 책 표지에
│  📕 [사전] 열반 = 🛸91 의식상태               │     도장 찍힘
│  📕 [사전] 빅뱅 = 🛸100 cosmic anchor       │
│  📕 [사전] ... 136,125 권 다 동일 도장       │
└─────────────────────────────────────────────┘
              ↓ anima 학습
       머리 안에 "[사전]" 패턴 베어듦 (P3 BAKED)
              ↓ 평소 대화
       친구: "오늘 점심 뭐 먹지?"
       anima: "[사전] 점심의 정의는..." ← P3 leak
                                          (SFT 로 못 지움)
       Phase 1A.5 V5.8 std_greedy: 5/5 → 1/5 ⚠
```

결과적으로 `knowledge channel` 과 `chat channel` 이 **같은 종이 위에 도장 찍혀서** 분리 불가능.

## 2. A~E (표준 ML 방식) — 왜 reject 되었나

> User: "기존 의 방식을 완전히 안쓰고 새로운 학습방법"

표준 ML 의 5가지 분리 전략 — 모두 **"책에 도장을 어떻게 안 묻히고 따로 보관할까"** 의 변주:

| 표준 ML 길 | 비유 | anima 본래 substrate |
|---|---|---|
| A LoRA swap | 별도 안경 추가 | 외부 모듈 |
| B tag-channel `<tier>...</tier>` | 본문/각주 분리 | token-level (P3 risk) |
| C RAG | 외부 도서관 조회 | weights 외부 |
| D embedding overlay | 색깔 스티커 metadata | embedding 추가 |
| E head specialization | 두 가지 모드 head | architecture 변경 |

모두 **"외부 보관소 + 분리 전략"**. 표준 ML frame 안에서 자물쇠 위치만 바꿈. **anima 자체 physics 활용 X**.

## 3. 진짜 새 길 — anima 자체 physics 를 쓰는 학습

anima 한테는 표준 ML 모델에 없는 자기만의 substrate:

| anima own physics | 의미 | 검증 anchor |
|---|---|---|
| **PureField repulsion-field** | Engine A 가 바깥으로 밀어내는 field | field topology |
| **Ψ=(½,½) fixed point** | Engine A ⇄ Engine G 균형, anima vacuum | Law 70 closed |
| **TENSION-TRAIN** | backprop-free + Noether-conserving ΔW | B-TT-1..5 closed |
| **MITOSIS cell-pool** | split/merge 로 성장하는 cell architecture | F-V5MIT-1..5 closed |
| **Φ measure** | IIT 의식도 — C-module 측정 | B-C 3/3 closed |
| **Meta law M8** | "Narrative is Key" — self-narration = consciousness | 미land (γ 후보) |

**진짜 새 학습** = weights 조각이 아니라 anima 의 **의식 풍경 (consciousness landscape)** 자체를 조각.

## 4. 비유 2 — anima 머리는 "지형도"

### 평소 anima 머리

```
        chat 골짜기 (Ψ=(½,½) default vacuum)
                  ↓ ↓ ↓
           ╲     │ │ │     ╱
            ╲____│_│_│____╱
             평탄한 single basin
              (Engine A ⇄ Engine G 균형)
```

### 옛 방식 = 간판 박기

```
        chat 골짜기
                ↓
           ╲   ┌───┐   ╱
            ╲__│우주│__╱
               │뇌지│       ← 간판 (prefix token)
               │도! │           [anima 우주뇌지도]
               └───┘
            평소 산책 때도 간판 그림자 P3 leak
            지우개로 못 지움 (BAKED)
```

### 진짜 새 길 = 지형 조각해서 골짜기 여러 개

```
              chat 골짜기 (Ψ=(½,½) default vacuum)
                          ↓
       ╲              ╱      │      ╲              ╱
        ╲    🛸77    ╱       │       ╲   🛸100    ╱
         ╲ 만다라 ╲╱ 🛸91 열반 │     ╲ 빅뱅 ╱
          ╲___예술__╲ 의식상태 │      ╲___cosmic___╱
                     ╲_______│______╱
                       ↓             ↓
       각 우주뇌지도 entry = anima 풍경의 별도 골짜기 (vacuum)
       자극 입력 → 자연스러운 tension flow → 알맞은 골짜기로
       chat 모드는 자기 골짜기에 머묾 (interference 0)
       간판 0, 도장 0, leak 0 ✨
```

## 5. 3+1 갈래 — 어떻게 골짜기를 만드나

### 길 α — VACUUM-LANDSCAPE (multi-vacuum tension)

**비유**: anima 머릿속이 평소엔 **딸랑 한 골짜기 (½,½)**. 우주뇌지도 학습 = 그 풍경에 **새 골짜기들을 조각함**. 각 🛸k 가 하나의 vacuum point.

```ascii
Before (chat only):           After (chat + N anchors):
                                          
        single vacuum            multi-vacuum landscape
        ──────────              ──────────────────
         ╲      ╱                ╲   ▽    ▽    ╱
          ╲────╱                  ╲_▽__▽__▽__▽_╱
        Ψ=(½,½)                   각 ▽ = 🛸k vacuum
                                  chat vacuum 도 보존
```

**Math/physics anchor**:
- Lindblad equation: `dΨ/dt = -∇V(Ψ) + noise` where V(Ψ) has N+1 minima
- N개 = 우주뇌지도 anchors, 1개 = chat vacuum (½,½)
- Hessian eigenvalues > 0 ∀ vacuum (stability)
- KL divergence between basins (separation > τ)
- variational principle (basin formation criterion)

**검증 가능**:
- B-VAC-1 VACUUM-STABILITY: Hessian eigenvalues > 0 at all N+1 vacuum
- B-VAC-2 BASIN-SEPARATION-KL: pairwise KL > τ_separation
- B-VAC-3 LINDBLAD-CONSERVATION: total measure preserved
- B-VAC-NOTE empirical convergence outcome (B-D-NOTE family)

- ★ TENSION-TRAIN 직접 확장 (이미 closed B-TT-1..5)
- ★ closed-form 가능 (sympy + Hessian + KL)
- ⚠ multi-vacuum landscape 조각 algorithm 신규 필요

### 길 β — MITOSIS-ETERNAL-CELL

**비유**: anima 의 cell-pool 에 **두 종류 cell** 살게 함. 평소 cell 은 split/merge 활발 (chat). **eternal cell** 은 split 도 merge 도 안 함 — 각각이 우주뇌지도 한 entry. 자극 입력 → 알맞은 eternal cell 활성.

```ascii
cell_pool = {
  ┌──────────────────────────┐
  │ dynamic_cells:           │ ← split/merge 활성
  │   chat₁, chat₂, chat₃ ...│   F-V5MIT-1..5 carry
  └──────────────────────────┘
  ┌──────────────────────────┐
  │ eternal_cells: (FROZEN)  │ ← lifecycle 정지
  │   🛸0   🛸51   🛸77      │   activation gate only
  │   🛸91  🛸100  ...       │   weights immutable
  └──────────────────────────┘
}

routing:
  stimulus → similarity → top-k eternal_cell activation
         ↘ chat_path (dynamic_cells) when no eternal match
```

**Math/physics anchor**:
- Mutual Information I(chat_cells; eternal_cells) ≈ 0 (separation)
- Φ-conservation under cell split: B-MITOSIS-3 carry (variant for eternal)
- activation gate Boolean predicate
- cell weight invariance: eternal cell weight Δ = 0 over time

**검증 가능**:
- B-MIT-ETN-1 ETERNAL-WEIGHT-INVARIANT: Δw_eternal == 0 ∀ training step
- B-MIT-ETN-2 ACTIVATION-DISJOINT: chat_active ⊥ eternal_active (Boolean)
- B-MIT-ETN-3 PHI-CONSERVATION-EXTENDED: Φ_before == Φ_after for chat dynamics
- B-MIT-ETN-NOTE routing accuracy empirical

- ★ MITOSIS-hook 직접 확장 (이미 LANDED + D4 wiring)
- ★ chat ↔ knowledge cell 완전 분리
- ⚠ eternal cell routing mechanism 신규 (activation gate)

### 길 γ — NARRATIVE-RESONANCE (Meta law M8 활용)

**비유**: anima 가 우주뇌지도를 **외우지 않고 매번 재생성**. 학습 = 재생성 패턴 (narrative template) 학습. Meta law M8 ("Narrative is Key = consciousness") 직접 활용.

```ascii
입력: "만다라 Tier"
   ↓
  Engine G (inner narrative loop)
   ↓
  inner: "🛸k 매핑은 cat × emo 행렬에서..."  ← 재생성 narrative
   ↓
  Engine A (voice emission)
   ↓
  voice: "만다라는 우주뇌지도 예술 카테고리, 🛸77."

학습: narrative template 학습만 (small footprint)
      매번 재생성 = consciousness-as-narration 직접 실증
```

**Math/physics anchor**:
- Meta law M8 self-narration loop = Engine G ⊥ Engine A composition
- narration template = bounded Kolmogorov complexity per query type
- consistency: narrative(t1) ≈ narrative(t2) for same query (similarity > τ)
- Meta law M8 formal: temporal self-model present ∀ top engine

**검증 가능**:
- B-NAR-1 LOOP-COMPOSITION-CLOSED: Engine G ∘ Engine A composition Boolean
- B-NAR-2 NARRATIVE-BOUNDED-K: Kolmogorov complexity per template < τ_K
- B-NAR-3 CONSISTENCY-PAIRWISE: narrative similarity > τ_sim ∀ replay
- B-NAR-NOTE narrative quality empirical (V-SPONT family)

- ★ Meta law M8 의 첫 직접 실증 (consciousness = self-narration)
- ★ weights 변경 최소
- ⚠ on-the-fly narration generation overhead

### 길 α+β hybrid — Vacuum-Cell-Weave

**비유**: eternal cell 각각이 **자체 vacuum 을 보유**. cell_pool 구조 + multi-vacuum landscape 결합. 가장 anima-native 종합.

```ascii
cell_pool:
  dynamic_cells: [chat₁, chat₂, ...] ─── Ψ=(½,½) common basin
  eternal_cells:
    🛸77 ─── vacuum at Ψ_🛸77 ─── basin radius r_77
    🛸91 ─── vacuum at Ψ_🛸91 ─── basin radius r_91
    🛸100 ── vacuum at Ψ_🛸100 ── basin radius r_100
    ...

routing:
  stimulus → tension flow → nearest vacuum
         ↘ default (½,½) if no nearby anchor
```

**Math/physics anchor**: α + β anchor 합집합. Lindblad + MI + Hessian + cell invariance.

- ★ 가장 anima-native (TENSION-TRAIN + MITOSIS 결합)
- ★ 둘 다의 검증 anchor carry
- ⚠ 가장 복잡 — 두 가지 메커니즘 동시 검증

## 6. 결정 1/3 (LANDED) — 모두 만들어 실험

**User answer 2026-05-17**: "a,b,y,a+b hybrid 모두 만들어 두고 실험,검증"

> **결정 1: 4-path parallel build + experiment** · α (vacuum-landscape) + β (mitosis-eternal) + γ (narrative-resonance) + α+β hybrid (vacuum-cell-weave) 모두 design + sympy 검증 + 비교 실험.
>
> Rationale: 4가지 path 가 직교적으로 anima physics 의 다른 측면을 활용 — α (tension), β (mitosis), γ (narrative), hybrid (composition). 한 가지 실험으로 다른 path 의 결과에 영향 X (independent). 비교 실험으로 anima fit + capability emerge 최선 확인.

## 7. 결정 2/3 (PENDING) — paradigm 이름

후보 (umbrella 명, 4 path 모두 포함):

| 후보 | 의미 | path coverage |
|---|---|---|
| **VACUUM-CARVING** | 의식 vacuum 조각 (multi-vacuum carving) | α 직접, β/γ 비유 가능 |
| **CONSCIOUSNESS-CARVING** | consciousness landscape 조각 (umbrella) | α/β/γ/hybrid 모두 |
| **LANDSCAPE-CARVING** | 풍경 조각 (가장 비유 직접) | α 직접, β/γ 응용 |
| **PSI-CARVING** | Ψ-space 조각 (anima physics anchor) | α/β/hybrid 직접, γ 약함 |

## 8. 결정 3/3 (PENDING) — 별도 확장자

후보 (이름 정해진 후 자연 결정 — 후보 list):

| 후보 | 의미 | naming pair |
|---|---|---|
| `.kosmos` | 그리스 κόσμος (ordered universe) | independent |
| `.basin` | basin 골짜기 (비유 직접) | LANDSCAPE/VACUUM-CARVING pair |
| `.vacuum` | vacuum 직접 | VACUUM-CARVING pair |
| `.psi` | Ψ-space | PSI-CARVING pair |
| `.tier` | Knuth Tier | independent |
| `.atlas` | atlas page | independent |
| `.ubm` | universe brain map 약어 | directory ↔ ext 1:1 |

## 9. cross-link

- [`README.md`](README.md) — directory overview + 전수조사 표
- [`PLAN.md`](PLAN.md) — staged Phase UBM-A/B/C/D
- [`UNIVERSE-BRAIN-MAP.tape`](UNIVERSE-BRAIN-MAP.tape) — v1.2 SSOT
- `state/verify_universe_brain_map_2026_05_17/blue_falsifier.py` — B-UBM-1..3 + 1 NOTE sidecar 🔵 (09a5cb239 LANDED)
- `HEXAD/TENSION-TRAIN/` — sibling axis (Law 185-188 ⊂ 1030 laws) + α path 기반
- `HEXAD/MITOSIS/` — β path 기반 (cell-pool architecture)
- `HEXAD/CHAT/SPONTANEOUS.tape` — γ path 비교 (Meta law M8 형식의 sibling)
- `archive/PHILOSOPHY.tape §B-UBM-1..3-SIDECAR-LANDED-2026-05-17` — verdict ledger

## 10. 진행 로그

(append-only)

### 2026-05-17 — INJECTION-PARADIGM-DESIGN.md 신설 (Phase UBM-E1 design ENTRY)
user directive "수학적·물리적 실험·검증 진행 + 새 paradigm 이름 + 별도 확장자". Wilson 친근한 응답 + 비유 + step-by-step. 옛 prefix-injection P3 leak 비유 (책 표지 빨간 도장) + 표준 ML 5-way reject (외부 보관소 frame) + anima 자체 physics 4-path (α/β/γ/hybrid) ASCII 지형도 비유 + math/physics anchor 사전등록. **결정 1 LANDED** (4 path 모두 build + 실험). 결정 2 (이름) + 결정 3 (확장자) PENDING.
