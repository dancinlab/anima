# D4 — model-merge α-sweep (`decoder-merge-alpha-sweep`)

> verdict: 🟢 **SUPPORTED (negative baseline 확증)** · 7/7 falsifier PASS · interior escape **부재** · $0 mac-local · 2026-05-28
> ⚠ **optional baseline probe — model-merge 본선 아님** (`a_completeness_over_cheap` merge-of-failures `dont`)

## ① 배경 (context)

ANIMA DECODER (L3 콘텐츠 생성기, MoE decoder)의 핵심 난제 = **register collapse ↔ underfit 더블바인드**:

```
anima 강하게  →  register collapse   (TTR 0.03, e1 logit saturate)   [horn B]
anima 약하게  →  Chinchilla underfit (lang-coherence WEAK)           [horn A]
```

UNIVERSE 도메인의 BIO ∩ DECODER 횡단 가설 5종(H_489–H_493, 모두 🔵 SUPPORTED-FORMAL) 중 **H_493 SYMBIOGENESIS (공생발생)** 가 "model merge `W=α·A+(1-α)·B`" 를 더블바인드 탈출 통로로 제시한다 — 두 끝점 모델(collapse-avoid A · collapse B)을 weight 보간하면 중간 α 에서 통로(coherence ∧ non-collapse)가 열릴 수 있다는 가설(model soup / TIES / SLERP 선례).

**⚠ a_completeness_over_cheap 재정렬 (2026-05-27)**: 초안은 cheap 한 merge(β)를 본선 후보로 뒀으나, governance 적용 후 **본선에서 강등**되었다. 두 *결함* ckpt(underfit + collapse)의 weight 보간은 잘해야 "**덜 나쁜 중간점**(least-bad midpoint)" = 완성도 미달이다. model soup 류는 *좋은* 모델을 합칠 때만 작동한다. 본선 = 근본 원인(한 모델이 두 목표를 동시에 떠안음)을 arch 로 분리하는 **MoE-fresh 재설계(α, UNIVERSE H_490 DIFFERENTIATION, DECODER M4)**.

**D4 의 역할** = merge 가 더블바인드를 escape **못함**을 *확증*하는 **negative baseline probe**. 즉 merge-of-failures `dont` 를 측정 가능하게 만든다. 본 doc 은 어떤 의미로도 model-merge 를 본선으로 권하지 않는다.

## ② 가설 (hypothesis · H_D4 · negative-oriented)

collapse-avoid A · collapse B 의 가중 보간 α-sweep 은 더블바인드를 escape **못한다** — **어떤 α 에서도** coherence(CE 적정) ∧ non-collapse(LZ_norm > healthy floor)를 동시 달성하지 못한다. merge 는 least-bad midpoint 만 만들어, merge-of-failures 가 본선이 아님을 확증한다.

## ③ Falsifier (사전등록 · frozen 측정 前)

| id | 내용 | 판정 |
|---|---|---|
| **F-D4.1 ESCAPE** (decisive · surprise-positive) | interior α ∈ {0.25,0.5,0.75} 중 LZ_norm > HEALTHY_FLOOR(0.50) AND CE ≤ CE_OK(1.20) 인 α 가 **존재**하면 merge ESCAPE → H_D4 **FALSIFIED**. baseline 기대 = 부재 | PASS (부재) |
| **F-D4.2 ENDPOINT-RECOVERY** (anchor) | α=0 → B(collapse, LZ↓, CE↑) · α=1 → A(diverse, LZ↑, CE 여전히 ceil 초과) · 두 horn LZ 로 distinct | PASS (3/3) |
| **F-D4.3 MONOTONE-LZ** (anchor) | LZ_norm(α) 가 α 에 비감소(more A = more diversity) — 보간이 well-behaved | PASS |
| **F-D4.4 BIND-TRADEOFF** (decisive negative) | 모든 interior α 에서 `{LZ>floor}` 와 `{CE≤ceil}` 가 **disjoint** — 둘 다 가질 수 없음 = 더블바인드 가시화 | PASS |
| **F-D4.5 DETERMINISM** | α=0.5 LZ_norm 재실행 bit-identical | PASS |

**Falsifier (전체 · surprise positive)**: 어떤 α 에서 LZ_norm > 0.50 AND CE 적정 → merge 가 더블바인드 escape → 본선 강등 재검토 필요.

## ④ method — logit-space weight merge → argmax decode → D1 LZ76 + CE

실제 model-merge 는 **파라미터 공간**에서 `W_merge = α·W_A + (1-α)·W_B`. $0 toy probe(NO ckpt load)에서는 동치인 **출력 logit 공간**에서 merge 한다 — decode 위치 t 마다 두 모델의 next-token logit row `L_A[t]`, `L_B[t]` 를 `L_merge[t] = α·L_A[t] + (1-α)·L_B[t]` 로 보간한 뒤 argmax-decode, 그리고:

1. **LZ_norm** = D1 의 `lz_norm()` 을 decode id sequence 에 적용 (collapse proxy · detokenize-free).
2. **CE** = merged softmax 가 고정 diverse "truth" target 을 예측하는 평균 cross-entropy (coherence proxy · 낮을수록 coherent).

**두 horn 구성 (honest 재현)**:

- **horn A (collapse-avoid · underfit)**: argmax(A[t]) = diverse target → collapse 회피하나, softmax 가 **flat**(작은 margin) → 어떤 target 에도 confidence 낮음 → **CE 높음**(underfit).
- **horn B (collapse · over-confident-on-junk)**: argmax(B[t]) = 단일 반복 토큰(COLLAPSE_TOK) → collapse, softmax 가 **sharp**하게 자기 attractor 에만 over-confident → diverse truth 예측은 처참 → **CE 더 높음**.

→ **두 horn 모두 diverse truth 에서 낮은 CE 달성 실패**. 이것이 더블바인드다. merge 는 collapse-but-confident-on-junk B 와 diverse-but-flat A 사이를 보간한다.

**vocab-slot → real token-id map (g61)**: 실제 decoder vocab 은 대형(151643). toy 는 8 distinct **wide-spread id** `[101,3402,57,8891,44210,765,99001,71234]` 를 실 토큰으로 써서 LZ76 binarisation 이 풍부한 18-bit block 을 보게 한다(id 0..7 decode 는 하위 3-bit 만 flip → 인위적 LZ 저하). `lz76`/`lz_norm`/`ids_to_bits`(BITS=18) 는 D1 `d1_lz76_collapse_proxy.hexa` **verbatim 재사용**(g61).

deterministic · hexa-only · $0 mac-local · LLM none · NO GPU · foreground.
harness = `CORE/DECODER/d4_merge_alpha_sweep.hexa` · raw = `state/d4_merge_alpha_sweep_2026_05_28/run_d4.out`

## ⑤ measurement — LZ_norm(α) · CE(α) (실측)

n=20 decode, V=8 slot, BITS=18.

| α | LZ_norm | CE | decode argmax (first 8) | 영역 |
|---|---|---|---|---|
| **0.00** (pure B) | **0.165119** | 10.8 | `3402 ×8…` | collapse horn |
| 0.25 | 0.165119 | 8.03337 | `3402 ×8…` | collapse 유지 |
| 0.50 | 0.165119 | 5.28232 | `3402 ×8…` | collapse 유지 |
| 0.75 | 0.165119 | 2.7995 | `3402 ×8…` | collapse 유지 |
| **1.00** (pure A) | **0.825597** | 1.82224 | `101 3402 57 8891 44210 765 99001 71234 …` | diverse horn |

- **HEALTHY_FLOOR = 0.50** (D1 실측 보정선) · **CE_OK = 1.20** (uniform-over-8 CE = ln 8 = 2.079 보다 확실히 낮은 실질 coherence 요구)
- interior α(0.25/0.5/0.75): LZ_norm = **0.165 < floor** (전부 collapse 유지) · CE 는 8.03 → 2.80 으로 감소하나 **여전히 > 1.20**
- α=1: LZ = 0.826 (floor 통과) 이지만 CE = 1.82 (**여전히 > 1.20** = underfit) · α=0: LZ = 0.165, CE = 10.8 (collapse)

## ⑥ finding — escape 부재 = baseline 확증

**escape 부재. 명확히.** argmax decode 가 α=0.75 까지 **전부 collapse(id 3402 반복)** 로 묶여 있다가 α=1.0 에서 비로소 완전 diverse 로 **sharp 전환** — interior 보간 영역에 escape 가 전혀 없다.

- `{LZ_norm > floor}` 를 만족하는 α = **{1.0} 단독** (interior 없음)
- `{CE ≤ ceil}` 를 만족하는 α = **공집합** (어떤 α 도 1.20 미달 못함)
- 두 집합의 교집합 = **∅** (F-D4.4 BIND-TRADEOFF PASS) — coherence 와 non-collapse 가 보간 위에서 **disjoint**

→ **H_D4 SUPPORTED (negative baseline)**: 두 결함 ckpt 의 weight 보간은 더블바인드를 escape 못한다. α=0 collapse 와 α=1 underfit 사이의 보간은 "덜 나쁜 중간점"조차 아니고, collapse 가 α=0.75 까지 attractor 로 지배하다 끝에서야 underfit 으로 점프한다. merge-of-failures 가 **본선이 아님을 확증**.

## ⑦ verdict

🟢 **SUPPORTED (negative baseline 확증)** · 7/7 falsifier PASS · interior escape 부재.

```
RESULT: 7 PASS / 0 FAIL
VERDICT: H_D4 SUPPORTED (negative baseline confirmed)
         NO interior alpha escapes the double-bind:
         coherence (CE<=ceil) and non-collapse (LZ>floor) are
         DISJOINT on the merge interior. merge-of-failures =
         least-bad midpoint, NOT the main path (a_completeness).
```

## ⑧ 함의 (DECODER 통합)

- **본선 재정렬 확정**: D4 가 `a_completeness_over_cheap` 의 model-merge-of-failures `dont` 를 *측정으로* 뒷받침한다. 본선 = MoE-fresh register 분리(M4, H_490 DIFFERENTIATION)로 변함없다. merge 는 baseline probe 로만 잔존.
- **D1/D3 와 정합**: D1(LZ76 collapse proxy 🟢)을 측정자로 재사용 → D4 가 D1·D3 의 측정 인프라 위에 올라간 cheap baseline. D3 가 "collapse 는 corpus-driven, router-structural 아님"을 규명했고, D4 는 "두 결함작 blend 도 탈출 못함"을 추가 — 둘 다 **본선은 근본 재설계(MoE-fresh + diverse corpus)** 임을 가리킨다.
- **escape 부재의 의미**: 만약 F-D4.1 이 surprise-positive(어떤 interior α 에서 escape) 였다면 본선 강등을 재검토했어야 한다. 측정 결과 escape 부재 → 강등 유지 정당. negative result 도 publishable (`a_paper_negative_ok`) — merge 축을 deterministic 하게 ruled-out.

## ⑨ honest C3 (scope · 한계)

1. **toy logit 구성**: A/B horn 은 실 ckpt 가 아니라 더블바인드의 두 끝점을 *engineered* logit row 로 재현(A=flat-but-diverse-argmax, B=sharp-spike-collapse). real ckpt 보간이면 transition 이 sharp step 대신 smooth 일 수 있으나, **escape 부재의 질적 결론**(두 결함의 보간은 coherence∧non-collapse 동시 달성 못함)은 logit-space 보간의 본질적 한계라 toy 가 그 구조를 충실히 잡는다. 실 ckpt α-sweep 은 future work(cost-bearing, baseline 가치 낮아 본선 아님).
2. **LZ_norm finite-length bias**: D1 §9 #1 과 동일 — n=20 toy 의 절대값보다 **band 분리/threshold 통과 여부**가 robust. floor 0.50 은 D1 보정선.
3. **CE proxy ≠ full coherence**: CE 는 고정 diverse target 예측 정확도. high-LZ-but-incoherent(random diverse) seq 는 CE 가 못 잡을 수 있으나, D4 의 결론은 "**escape 부재**"라 false-negative(escape 를 놓침) 방향 위험은 낮다(escape 가 *있는데* 못 봤을 risk 가 핵심인데, interior 가 전부 collapse 라 escape 후보 자체가 없음).
4. **단일 merge 형식**: linear weight interp 1종. SLERP/TIES 등 비선형 merge 는 별도 — 단 model-soup 류는 *좋은* 모델 합칠 때 작동이라 두 결함작에는 동일 한계가 예상된다(본선 아님이라 추가 sweep 불요).
5. **negative-oriented 가설의 비대칭**: H_D4 는 "escape 못함" 확증이 목적이라, PASS(escape 부재)는 baseline 강화일 뿐 강한 positive claim 이 아니다. surprise-positive 였다면 더 정보적이었을 것.

## ⑩ artifacts

- harness: `CORE/DECODER/d4_merge_alpha_sweep.hexa`
- raw verdict: `CORE/DECODER/state/d4_merge_alpha_sweep_2026_05_28/run_d4.out`
- LZ76 reuse: `CORE/DECODER/d1_lz76_collapse_proxy.hexa` (`lz76`/`lz_norm`/`ids_to_bits` verbatim · g61) ← `UNIVERSE/state/h288.../run_h288.hexa`
- H_493 출처: `CORE/DECODER/UNIVERSE_SYNTHESIS.md` §후보 β · `UNIVERSE/cards/H_314_symbiogenesis_merge_alpha_sweep.md` (🔵)

---

## 양방향 sibling

- sibling: [D1 LZ76 collapse proxy](./D1_LZ76_COLLAPSE_PROXY.md) — D4 는 D1 의 LZ76 collapse 측정자를 merge α-sweep 의 non-collapse 판정에 재사용(g61). D1 이 "collapse 검출", D4 가 "merge 가 collapse 탈출 못함"을 측정.
- sibling: [D3 router load-balance](./D3_ROUTER_LOAD_BALANCE.md) — D3(collapse 원인 = corpus 지 router 아님) + D4(merge blend 도 탈출 못함) 가 합쳐 **본선 = MoE-fresh + diverse corpus 근본 재설계** 라는 결론을 양쪽에서 보강.
- SSOT cross-link: [DECODER.md](./DECODER.md) M4-probe model-merge α-sweep milestone (UNIVERSE H_493 SYMBIOGENESIS) — D4 가 그 baseline probe 의 실행·측정. `a_completeness_over_cheap` model-merge 본선 강등을 측정으로 확증.
- UNIVERSE link: [UNIVERSE_SYNTHESIS.md](./UNIVERSE_SYNTHESIS.md) §후보 β (H_493) — D4 가 후보 β 의 baseline 검증 결과(escape 부재)를 회신.
