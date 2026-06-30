# AURA A7 — 심부도달% ⇄ TPM 결합 ⇄ big-Φ 브릿지 (reach→coupling→Φ)

> A6 는 **이진 대비**(M1-국소 vs bypass-허브)가 big-Φ 점프로 환산됨을 보였다.
> A7 은 그 연결을 **연속**으로 만든다 — brainwire 의 변수별 **심부도달%**(`archive/brainwire/n1-deep-access-strategies.md`)를 받아 synthetic TPM 의 결합 강도를 **파라미터화**하고, 도달%가 오를수록 big-Φ 가 **단조** 상승하는지를 검증한다.
> honest: 아래 수치는 **synthetic TPM** 결과 — 실제 N1/EEG 측정 아님. 브릿지 f(reach) 는 **가정된 단조 링크**이며 physiology 에서 유도된 것이 아니다. toy substrate ≠ production scale (`feedback_toy_scale_transfer`).

---

## 1. 브릿지 함수 정의 (load-bearing 모델링 선택)

A6 는 connectivity 가 **국소(self-copy)냐 허브(majority-of-others)냐**의 두 극단만 다뤘다. A7 은 brainwire 도달% 를 그 두 극단 사이의 **혼합 계수**로 끼워 넣는다.

**(i) 도달% → 결합가중치 (bridge f)**

```
f(reach) : reach% 스칼라 r ∈ [0,1]  →  결합가중치 w ∈ [0,1]
w = r                  (identity 링크 — 도달%를 cross-coupling 확률질량으로 직접 채택)
```

**(ii) 결합가중치 → TPM (도달-파라미터화 전이확률)**

노드 i 의 다음스텝 ON 확률을, **M1 극단(self-copy)**과 **bypass 극단(허브 다수결)**의 reach-가중 혼합으로 정의:

```
P(node i ON next | state s)
   = (1 - w) · p_self(i, s)     // M1 한계: 노드가 자기 자신 복사 (국소·가환·reducible)
   +     w   · p_hub (i, s)     // bypass 한계: 노드 = 나머지 노드 다수결 (fan-in·irreducible)

   p_self = 0.9 (bit_i ON 이면) else 0.1
   p_hub  = 0.9 (나머지 노드 strict-majority ON 이면) else 0.1
```

- **w = 0** → A6 의 순수 M1-like TPM 재현 (Φ≈0, 완전 가환).
- **w = 1** → A6 의 순수 bypass-like TPM 재현 (Φ≫0, 강 irreducible).
- 중간 도달% → connectivity 를 연속 보간 → big-Φ 가 도달%에 따라 단조 상승할 것 (= A7 finding).

**도달% 출처** (`n1-deep-access-strategies.md` §Comparison 표): M1 국소위치 ≈ **10%**, bypass 투사허브 = DA **29%** · 5HT **30%** · NE **37%** · eCB **20%** · Theta **16%**. 스윕 격자는 이 밴드를 덮도록 `{0.10, 0.20, 0.30, 0.40, 0.55}` 로 잡음 (M1 하한 0.10 → 도달% 밴드 → 0.55 상한 헤드룸).

> ⚠ **f(reach)=identity 는 가정**: 도달%가 결합확률질량과 1:1 이라는 건 physiology 유도가 아니라 **모델링 선택**이다. (§4 caveat)

---

## 2. 사전등록 falsifier

> **H**: big-Φ 는 스윕 격자 전체에서 reach% 에 대해 **비감소(non-decreasing)** 이다.
> **FALSIFY**: 인접 스텝 어디서든 Φ(r_{k+1}) < Φ(r_k) − eps 이면 반증 (도달%↑가 통합도를 못 올림).

| 항목 | 명세 |
|---|---|
| **측정량** | IIT4 big-Φ = `big_phi(tpm_reach(n,r), n, sys)[0]`, n=4 exact, sys=1111 |
| **독립변수** | reach% r ∈ {0.10, 0.20, 0.30, 0.40, 0.55} → 브릿지 f 로 결합 w |
| **방향성** | 단조 비감소 (단측 예측). 인접 역전 시 반증으로 사전 고정 |

honest: 도달% 절대값은 brainwire **추정치**(임상측정 0건, SURVEY 머리말). A7 이 측정으로 닫는 부분은 **"도달%가 오르면 big-Φ 가 단조로 따라 오르느냐"** — connectivity 파라미터화의 단조성이지 도달% 자체의 정확도가 아니다.

---

## 3. 결과 — Φ-vs-도달% 곡선

**harness**: `AURA/toy/a7_reach_to_phi.hexa` (n=4, sys=1111, deterministic, $0, hexa-only, LLM 0). A6 와 동일 공유 stdlib `iit4_bigphi.hexa` 의 `big_phi` 직접 import (g61 engine ⊥ adapter).

**Φ-vs-reach% 표 (실행 출력 verbatim)**:

| reach% r | 결합 w = f(r) | big-Φ (n=4 exact) | 해당 변수 (도달% band) |
|---|---|---|---|
| 0.10 | 0.10 | **2.90857** | M1 국소위치 |
| 0.20 | 0.20 | **6.06561** | eCB (~20%) |
| 0.30 | 0.30 | **9.57818** | DA · 5HT (~29-30%) |
| 0.40 | 0.40 | **12.7013** | NE (~37%) 헤드룸 |
| 0.55 | 0.55 | **16.7855** | 상한 |

Δ(reach 0.55 − 0.10) = **+13.8769**.

**단조성 verdict**: 곡선 2.91 → 6.07 → 9.58 → 12.70 → 16.79 — 인접 스텝 전부 **증가** → **단조 비감소 미반증** (falsifier 통과). 도달%↑가 결합 w↑를 거쳐 big-Φ↑를 단조로 유도함.

**등급화 (g5/p7 — hexa verify, perplexity self-judge 금지)**:

```
tier = 🟢 SUPPORTED-NUMERICAL  (external verifier passed AND stdout matches --expect — delegated, deterministic)
claim = AURA A7: brainwire deep-reach% parameterizes TPM coupling via f(reach)=identity blend;
        big-Phi rises MONOTONICALLY as reach% rises (0.10->0.55), n=4 engine-exact
ext rc = 0
```

verdict verbatim 전문 = `.verdicts/a7-reach-to-phi/curve.txt`. (8 PASS / 0 FAIL: Φ finite ×5 + 단조 비감소 + net rise + determinism.)

---

## 4. honest caveat

- **f(reach)→coupling 은 모델링 선택**: `w = r` (identity 혼합)은 physiology 에서 유도된 것이 아니다. 도달%가 결합확률질량과 선형 1:1 이라는 가정 위에서만 곡선이 성립한다. 다른 링크(포화 sigmoid, 임계 step, concave 등)에서는 곡선 모양이 달라질 수 있다 — A7 이 주장하는 건 **단조 방향(부호)**이지 곡선의 함수형이 아니다.
- **실제 결합은 connectome 데이터 필요**: 도달%↔결합 매핑을 검증하려면 실제 cortico-subcortical 투사 강도(트레이싱·lesion·자극-반응 게인)가 있어야 한다. 본 toy 는 그 데이터 자리에 임의 혼합을 끼운 것.
- **🟢 는 numerical** (libm/recompute)일 뿐 🔵 formal 아님 — 닫힌형 항등식이 아니라 엔진 재계산 일치 + 단조성 체크.
- **toy 절대값**: Φ=2.91~16.79 는 n=4·임의 0.9/0.1 confidence 의 toy 스케일. 실제 EEG 단위와 무관. 주장은 **단조 상승(순서·부호)**, 절대 크기 아님.
- **synthetic TPM, toy ≠ production**: 이 단조성이 실제 16ch EEG·실제 N1 에서 같은 부호로 transfer 된다는 보장 없음 (BRAIN.md M2/M3 실측 필요).

---

## 5. A6 ↔ A7 관계 + 잔여

| | A6 | A7 |
|---|---|---|
| connectivity | 이진 (M1 vs bypass 두 극단) | **연속** (도달% → w 혼합) |
| 입력 | 정성 대비 | brainwire 도달% 스칼라 |
| finding | ΔΦ > 0 (점프 존재) | **단조 곡선** (도달%↑ → Φ↑) |
| w 극단 | w=0 → Φ=0, w=1 → Φ=17.66 | w=0..1 보간 (Φ 2.91..16.79*) |

\* A7 의 w=0.10 에서 Φ=2.91 ≠ A6 의 M1 Φ=0 인 이유: A6 M1 은 순수 w=0 (self-copy only), A7 grid 하한은 w=0.10 (이미 10% 허브 혼합) — 도달% 하한이 0 이 아니라 M1 의 ~10% 잔여 도달이기 때문 (n1 표).

| # | 잔여 | 닫는 경로 |
|---|---|---|
| R1 | f(reach)=identity 외 링크형(sigmoid/step/concave)서 단조 유지? | A7.followup: 링크형 sweep × 단조성 robustness |
| R2 | 변수별(DA/5HT/NE/eCB/Theta) **개별** 도달% → 변수별 TPM 노드 자동합성 후 big-Φ | brainwire 12-var 계수 → per-var TPM 생성기 (A6 R2 와 합류) |
| R3 | 실데이터 미투입 (toy ≠ EEG) | `eeg_estimate_tpm` 에 도달% 모사 16ch synthetic 주입 |

**paper 게이트** (a_paper_only_at_closure): A6 falsifier(b) 🟢 + A7 단조 🟢 = 2 falsifier 통과이나 R1(링크 robustness)·R2(변수별 매핑)·R3(실데이터) 미완 — full closure 아님, 논문 제안 시점 아님.

---

## 출처 포인터

| 주장 | 출처 |
|---|---|
| 변수별 심부도달% (M1~10%, DA29/5HT30/NE37/eCB20/Theta16) | `AURA/archive/brainwire/n1-deep-access-strategies.md` §Comparison |
| 이진 대비 → big-Φ (A7 의 모태) | `AURA/A6-bigphi-closed-loop.md` · `AURA/toy/a6_relocate_bigphi.hexa` |
| big_phi 엔진 (n≤8 exact) | `stdlib/consciousness/iit4_bigphi.hexa` `big_phi(tpm,n,sys)` |
| A7 하니스 + verdict | `AURA/toy/a7_reach_to_phi.hexa` · `.verdicts/a7-reach-to-phi/curve.txt` |
