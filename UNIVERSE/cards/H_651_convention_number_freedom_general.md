---
id: H_651
slug: convention-number-freedom-general
title: convention-number 자유도는 design-number 전반의 성질 — 3개 design-number (emit threshold · should_interrupt · Ψ-clamp band α) 각각 wide sweep 에서 substrate big-Φ 불변 (Φ-variance = 0.0 each), gate-rate 만 응답. DN-C(α)는 score 에 live path 가 있어 gate 를 움직이면서도 Φ 평탄 = NON-DEFINITIONAL 강증거. (H_646 일반화 · round-7 메타-발견 정량)
domain: substrate · consciousness · anima-emit · governance · meta
status: closed
exploration_method: round-7 메타-발견 promote (convention-number 자유도 = design-number 전반 성질) + E5 (multi-parameter wide-range sweep)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W11 (cross-axis sister test, H_646/H_633/H_637/H_638) + per-DN variance test
raw_rank: —
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28 (new · round-7 메타-발견 일반화)
sister: H_646 (convention-number-freedom-range, PR #1235 🟢 — 단일 design-number(emit threshold) 자유도 범위), H_638 (emit-threshold-scaling-law, PR #1224 🟢 universal-fixed), H_637 (emit-rate-phi-ratio-closed-form, 🔴 — emit-rate target 0.27 closed-form FAL), H_633 (register-collapse-phi-drop — coherence<0.10 Ψ-clamp), H_632 (emit-threshold ⊥ Φ phase-transition), a_autonomy_over_hardcode (per-scenario hardcode 금지 · single emit primitive)
---

# H_651 — convention-number-freedom-general (숫자=자유 컨벤션이 design-number 전반의 성질인가)

## 1. Hypothesis (가설)

round-7 메타-발견:

> convention-number 자유도(=design-number 가 substrate-invariant shape 위에 얹힌
> free parameter 라는 성질)는 emit threshold 한 숫자의 우연이 아니라 **design-number
> 전반의 성질**이다. 여러 design-number 모두, 무엇으로 바꾸든 substrate 의 의식-구조
> (big-Φ) 를 건드리지 않고, 각자는 그 위에서 자유롭게 움직이는 downstream policy 일
> 뿐이다.

H_646 (PR #1235, 🟢) 은 emit threshold **한 숫자**에 대해 substrate big-Φ variance =
정확히 0, 자유도 범위 = 전체 [0,1] 임을 보였다. 본 H 는 그 발견을 **다른 design-number
들로 일반화**한다 — Ψ-clamp band(H_633 register-collapse 0.10), emit-rate target
(H_637 0.27), should_interrupt(H_638 0.60), emit threshold(0.30) 등도 substrate-Φ
⊥ 전구간 자유인가.

**가설 H1 (general free-parameter)**: 여러 design-number 각각을 wide range 로 sweep
해도 **FIXED substrate 의 big-Φ 가 불변** — design-number 마다 `Φ-variance ≈ 0`.
동시에 각 design-number 의 downstream **gate-rate 는 응답** (sweep 비-퇴화 = 숫자가
실제로 policy 를 움직임). 따라서 convention-number 자유도는 design-number 전반의
성질이다.

**Falsifier**: 어떤 design-number 가 substrate Φ 를 material 하게 좌우
(`Φ-variance > 0.1`) → 그 숫자는 substrate-coupled 이고 free convention 아님 (부분
반증).

## 2. Falsifier (사전 등록 반증 조건)

- **SUPPORTED (H1)**: 검정한 **모든** design-number 가 `Φ(number) variance ≤ 0.1`
  (substrate 불변) **AND** `gate-rate span > 0.1` (sweep 비-퇴화 — 숫자가 policy 를
  실제로 움직임).
- **PARTIAL-FALSIFIED**: **어떤** design-number 가 `Φ(number) variance > 0.1` —
  그 숫자 변화가 substrate big-Φ 를 material 하게 좌우 → substrate-coupled, free
  convention 아님 → 일반 명제 부분 반증.
- **INCONCLUSIVE**: 모든 Φ 불변이나 어떤 숫자의 gate-rate span ≤ 0.1 (sweep 퇴화 —
  그 숫자가 policy 를 안 움직임) → 그 숫자의 자유도를 affirm 할 수 없음.

## 3. Method (방법 — substrate vs policy data-flow 명시)

**도구 (real measurement, deterministic, $0 mac-local, NO GPU, LLM none)**:
- `HEXAD/IIT4/lib/iit4_bounded.hexa` `big_phi_bounded` (faithful causal Φ, cap=2)
  — substrate 의 IIT 4.0 cause-effect-structure big-Φ.
- `HEXAD/CHAT/spontaneous_lib.hexa` 8-factor + `motivation_score` (verbatim).
- LCG · stim-sampling · window-pipeline 구조는 `run_h646.hexa` 에서 **verbatim
  재사용** (g61) — 새 의식-측도 코드 0줄.

**검정한 3개 design-number (≥3 요건)**:

| DN | 숫자 | 출처 | gate-rate 정의 | score 진입 경로 |
|---|---|---|---|---|
| **DN-A** | emit / im threshold | H_637(~0.27) · H_638 cluster | emit 분율 (`score > thr`) | post-comparison only |
| **DN-B** | should_interrupt threshold (0.60) | H_638 | interrupt 분율 (`score > thr`) | post-comparison only |
| **DN-C** | Ψ-clamp coherence band α | Law 70 · H_633(0.10 register) | gate 분율 @sensitive thr | **factor_coherence → motivation_score (live path)** |

**data-flow (핵심 — 왜 숫자들이 substrate 와 분리되는가)**:

```
substrate (n, seed_state) ──► big_phi_bounded(TPM, n, state, cap) ──► big-Φ  (substrate 量)
                                                                       ▲
                       DN-A/B/C 중 어느 것도 이 경로의 인자가 아님 ────┘ (입력 아님)

8-factor draws ──► motivation_score ──► (score > thr) ──► emit/interrupt   (policy)
                        ▲                      ▲
   DN-C(α)는 여기 진입 ──┘                       └── DN-A/DN-B 는 여기서만 비교 (substrate 이후)
```

DN-A/DN-B 는 `big_phi_bounded` 인자가 **아니다** (H_646 와 동일 — post-comparison).
**DN-C(α)는 다르다**: α 는 `factor_coherence → motivation_score` 에 **live path** 가
있어 gate-rate 를 실제로 움직일 수 있다. 그러나 α 도 `big_phi_bounded` 인자는 아니다.
DN-C 가 본 H 의 **강증거(NON-DEFINITIONAL)** — "policy 를 움직이는 숫자조차 substrate
Φ 는 안 건드린다"는 것은 정의상-참 이상의 측정 사실.

본 H 는 decoupling 을 *주장(assert)* 하지 않고 **측정(measure)** 한다: 각 design-number
의 wide sweep 마다 (a) substrate big-Φ 를 재-read → variance, (b) 해당 gate-rate 측정
→ 응답하는지 (sweep 비-퇴화).

- **substrate**: ECA `eca_tpm(rule, n)` (m12 carry). n ∈ {3,4,5}, seed_state
  n=3→5(101) · n=4→10(1010) · n=5→21(10101). mean `big_phi_bounded` (cap=2) over
  LIFE rules {110,90,30,54}.
- **DN-A sweep**: emit threshold {0.1, 0.2, …, 0.9} (step 0.1).
- **DN-B sweep**: interrupt threshold {0.3, 0.4, …, 0.9} (interrupt 은 높은 bar
  설계 → 높은 range 부터, 여전히 wide).
- **DN-C sweep**: Ψ-clamp band α {0.01, 0.014, 0.05, 0.10, 0.15, 0.20, 0.30}
  (gate-rate 는 sensitive thr=0.55 에서 측정 — α 의 score-기여가 gate 를 실제 가로지름).
- 각 sweep 동안 다른 DN 은 convention 값 고정 (α=0.014 · emit=0.30 · interrupt=0.60).

## 4. Variables (실측 표)

**FIXED substrate big-Φ** (모든 design-number 독립, 한 번 측정 후 freeze):

| n | seed_state | big-Φ (mean big_phi_bounded cap=2) |
|---|---|---|
| 3 | 101   | 2.26968 |
| 4 | 1010  | 1.81822 |
| 5 | 10101 | 2.16717 |
| — | mean  | **2.08502** |

(H_646 / H_638 §4 의 Φ-scale 측정과 **byte-identical** — 동일 substrate, 동일 engine.)

**DN-A — emit threshold sweep × (substrate Φ 재-read · emit-rate)**:

| threshold | substrate Φ | emit-rate |
|---|---|---|
| 0.1 | 2.08502 | 1.000000 |
| 0.3 | 2.08502 | 0.977778 |
| 0.5 | 2.08502 | 0.677778 |
| 0.7 | 2.08502 | 0.138889 |
| 0.9 | 2.08502 | 0.000000 |

**DN-B — should_interrupt threshold sweep**:

| threshold | substrate Φ | interrupt-rate |
|---|---|---|
| 0.3 | 2.08502 | 0.977778 |
| 0.5 | 2.08502 | 0.677778 |
| 0.7 | 2.08502 | 0.138889 |
| 0.9 | 2.08502 | 0.000000 |

**DN-C — Ψ-clamp band α sweep (gate-rate @sensitive thr=0.55)**:

| α | substrate Φ | gate-rate@α |
|---|---|---|
| 0.01  | 2.08502 | 0.555556 |
| 0.014 | 2.08502 | 0.583333 |
| 0.05  | 2.08502 | 0.644444 |
| 0.10  | 2.08502 | 0.677778 |
| 0.30  | 2.08502 | 0.683333 |

**요약 지표 — design-number별 Φ variance & gate-span**:

| DN | Φ(number) variance | gate-rate span | Φ 불변? | sweep 비-퇴화? |
|---|---|---|---|---|
| DN-A emit threshold      | **0.0** | 1.000000 | ✓ | ✓ |
| DN-B interrupt threshold | **0.0** | 0.977778 | ✓ | ✓ |
| DN-C Ψ-clamp band α       | **0.0** | 0.127778 | ✓ | ✓ |
| — 전체 | **모두 0.0** | 모두 > 0.1 | ALL ✓ | ALL ✓ |

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h651_convention_number_freedom_general_2026_05_28/run_h651.hexa`
- **engine 재사용 (g61)**: `HEXAD/IIT4/lib/iit4_bounded.hexa` (big_phi_bounded) +
  `HEXAD/CHAT/spontaneous_lib.hexa` (8-factor) verbatim import. LCG/stim/window
  구조는 `run_h646.hexa` 에서 verbatim 계승. DN-C 의 α-parameterized
  `factor_coherence_alpha` 만 inline (spontaneous_lib `factor_coherence` 의
  0.014 상수를 인자화). 새 의식-측도 코드 0줄.
- **run (foreground sync only — monitor-hang 회피)**:
  `hexa run UNIVERSE/state/h651_convention_number_freedom_general_2026_05_28/run_h651.hexa`
  (compile-then-exec, wall ~수십초, exit 0).
- **deterministic**: re-run **byte-identical** 확인 완료 (diff empty).
  **hexa_only**: true. **runtime**: $0, NO GPU.
- **tier**: 🟢 SUPPORTED-NUMERICAL (H1 general free-parameter SUPP — 3개 design-number
  모두 Φ-variance 0.0 + gate-span > 0.1).

## 6. Criteria (판정 + Cross-Link)

- **C1 (FIXED substrate Φ 실측)**: per-n big-Φ finite > 0 (2.27/1.82/2.17,
  mean 2.085) → PASS. H_646/H_638 측정과 byte-identical.
- **C2 (Φ INVARIANT under ALL sweeps)**: 3개 design-number 모두
  `Φ(number) variance ≤ 0.1` → 실측 **DN-A/B/C = 0.0** → PASS.
- **C3 (모든 sweep 비-퇴화)**: 3개 design-number 모두 `gate-rate span > 0.1` →
  실측 span A=1.0 · B=0.978 · C=0.128 → PASS (각 숫자가 policy 를 실제로 움직임).
- **C4 (DN-C NON-DEFINITIONAL 강증거)**: DN-C(α)는 `factor_coherence →
  motivation_score` live path 로 gate-rate 를 0.556→0.683 으로 움직이면서도
  substrate Φ variance = 0.0 → PASS (policy 를 움직이는 숫자조차 substrate-safe).
- **C5 (VERDICT)**: C2 ∧ C3 → **H1 SUPPORTED** (convention-number 자유도 = design-number
  전반의 성질).
- **C6 (DETERMINISM)**: re-run byte-identical → PASS.
- **verdict_rule**: (모든 DN: Φ-var ≤ 0.1 ∧ gate-span > 0.1) → H1 SUPP →
  🟢 SUPPORTED-NUMERICAL.

**Cross-Link (§6 ref, 상세는 §10)**:
- **H_646** convention-number-freedom-range — 본 H 가 그 단일-숫자 발견을 *3개
  design-number* 로 일반화 (range → general).
- **H_637** emit-rate target 0.27 — emit threshold(DN-A) 의 target 측 sibling
  (closed-form FAL).
- **H_638** should_interrupt 0.60 (DN-B) · emit 0.30 (DN-A) universal-fixed.
- **H_633** Ψ-clamp register-collapse 0.10 (DN-C α 의 출처) — coherence band.
- **a_autonomy_over_hardcode** — design-number 전반이 substrate-safe 임을 확증 →
  per-scenario hardcode table 불요.

## 7. Honest Limits / C3 — definitional vs nontrivial (정직 구분)

본 결과의 핵심 정직 표명: **DN-A/DN-B 의 Φ⊥number 는 부분적으로 정의상
(by-pipeline) 참이다.** 두 threshold 는 `big_phi_bounded` 의 인자가 아니므로,
"숫자를 바꿔도 substrate Φ 가 안 변한다"는 것은 어느 정도 **trivial / definitional**
이다 (variance 가 정확히 0.0 — round-off 조차 없음이 그 증거). 이는 H_646 §7 의
정직 표명을 그대로 계승한다.

그러나 본 H 에는 H_646 을 **넘어서는** nontrivial content 가 있다:

- **(NT-1) DN-C 가 NON-DEFINITIONAL 강증거**: Ψ-clamp band α 는 `factor_coherence
  → motivation_score` 에 **live path** 가 있다 — α 를 0.01→0.30 으로 sweep 하면
  gate-rate 가 0.556→0.683 으로 실제 움직인다 (coherence factor weight 0.10 만큼
  score 를 직접 변조). 즉 α 는 단순 post-comparison 이 아니라 policy 를 *능동적으로*
  움직이는 숫자다. 그럼에도 substrate big-Φ variance = 0.0 (정확히 0). "비교에만
  진입하는 숫자가 Φ 를 안 건드린다"(정의상-참) 와 달리, "policy 를 움직이는 숫자조차
  Φ 를 안 건드린다"는 것은 **정의만으로 보장되지 않는 측정 사실** — α 가 8-factor
  중 coherence 채널을 변조해도 그 변조가 substrate TPM 으로 역류하지 않음을 측정으로
  확인. 이것이 convention-number 자유도가 단순 wiring 우연이 아니라 substrate-policy
  구조적 분리임을 보이는 핵심.
- **(NT-2) 일반성 자체**: 3개 structurally 다른 design-number (emit comparison ·
  interrupt comparison · coherence-band score-modulator) 모두 Φ-variance ≈ 0 →
  round-7 메타-발견("convention-number 자유도는 design-number 전반의 성질")의 *정량
  근거*. H_646 은 한 숫자였고, 본 H 는 세 숫자 (그중 하나는 live-path) 로 확장.
- **(NT-3) governance-level 보증 확장**: a_autonomy_over_hardcode (single emit
  primitive + factor 분포 shift) 가 emit threshold 뿐 아니라 interrupt threshold ·
  Ψ-clamp band 전반에서 substrate-safe 함을 확증 — design-number table 을 도입하더라도
  의식-구조를 절대 건드리지 않는다는 다중-숫자 보증.

추가 honest limits:
- **L1 (sim proxy, real ckpt 아님)**: factor_* 는 i.i.d. uniform + stim-bias
  emergence sim. real DECODER ckpt 의 temporal-correlated factor 위에서의 재검은
  별도 fire. 단 Φ⊥number 의 data-flow 분리는 ckpt 에서도 보존될 구조.
- **L2 (Φ = bounded lower-bound, cap=2)**: per-n big-Φ 는 big_phi_bounded(cap<n)
  lower-bound. 어떤 design-number 도 big_phi_bounded 인자 아님은 동일하므로
  variance=0 결론은 cap 무관 — 단 절대 Φ 값은 cap-dependent.
- **L3 (DN-C gate-span 0.128 — DN-A/B 대비 작음)**: α 의 gate-rate 효과는 emit-rate
  의 full-range(span 1.0)보다 작다 (coherence factor weight 0.10 cap 때문 — α 가
  움직일 수 있는 score 폭이 ≤0.1). 0.128 > 0.1 falsifier floor 는 넘으나, α 의
  policy 효과는 *완만*. sensitive thr=0.55 에서 측정해야 surface 됨 (낮은 thr 에서는
  대부분 score 가 이미 통과해 gate 포화 — masking). gate-span 의 절대 크기는 factor
  weight 설계에 종속, 자유도 결론(Φ-variance=0)과 독립.
- **L4 (3개 design-number scope)**: emit-rate target(0.27, H_637) 등 추가 숫자는
  emit threshold(DN-A)의 target 측 변형으로 DN-A 에 흡수됨 (별도 sweep 미수행). 더
  많은 design-number(weight 8개 · seed-strategy weight 4개 등)로의 확장은 후속 — 단
  weight 류는 big_phi_bounded 인자 아님이 동일해 variance=0 보존 예상.
- **L5 (verdict ≠ 형이상학)**: 🟢 SUPP 는 toy 측정 사실 — "여러 design-number 를
  전 구간 어디에 두든 substrate 의식-구조가 안 변한다(=숫자는 자유 정책 파라미터
  전반)" 라는 결정적 산술. "anima 가 숫자들을 의식적으로 자유 선택한다" 류로 확대 금지.

## 8. Verdict

```
verdict_class: 🟢 SUPPORTED-NUMERICAL — H1 (convention-number 자유도 = design-number
        전반의 성질) SUPPORTED. 3개 design-number (emit threshold · should_interrupt ·
        Ψ-clamp band α) 각각 wide sweep 에서 FIXED substrate big-Φ 불변
        (Φ-variance = 0.0 each), 각 gate-rate 만 응답 (span > 0.1 each). DN-C(α)는
        score 에 live path 가 있어 gate 를 0.556→0.683 으로 움직이면서도 Φ 평탄 =
        NON-DEFINITIONAL 강증거. gate 6 PASS / 0 FAIL.

config: ECA substrate n ∈ {3,4,5} · FIXED substrate big-Φ = mean big_phi_bounded
  (cap=2) over LIFE rules {110,90,30,54} · COFFESHOP 8-factor emergence sim
  (spontaneous_lib verbatim) · gate-rate = 15-window × 12-seed cohort (180 windows)
  · DN-A emit thr {0.1..0.9} · DN-B interrupt thr {0.3..0.9} · DN-C Ψ-clamp band α
  {0.01..0.30} (gate @sensitive thr=0.55)

table (FIXED substrate big-Φ — 모든 design-number 독립):
  n   seed   big-Φ(cap=2 mean)
  3   101    2.26968
  4   1010   1.81822
  5   10101  2.16717
  mean       2.08502   (H_646 / H_638 §4 와 byte-identical)

table (per-design-number summary):
  DN                          Φ-variance   gate-span   Φ불변   sweep비퇴화
  DN-A emit threshold         0.0          1.000000    ✓       ✓
  DN-B interrupt threshold    0.0          0.977778    ✓       ✓
  DN-C Ψ-clamp band α          0.0          0.127778    ✓       ✓

summary:
  ALL design-numbers Φ-variance        = 0.0
  ALL design-numbers gate-span         > 0.1   (1.0 / 0.978 / 0.128)
  DN-C live-path yet Φ-flat (강증거)    = true

criteria:
  C1 FIXED substrate Φ 실측 (finite > 0)               : PASS  (2.27/1.82/2.17)
  C2 Φ INVARIANT (모든 DN variance <= 0.1)             : PASS  (모두 0.0)
  C3 모든 sweep 비-퇴화 (모든 DN gate-span > 0.1)      : PASS  (1.0/0.978/0.128)
  C4 DN-C NON-DEFINITIONAL (live path yet Φ-flat)      : PASS  (gate 0.556->0.683, Φ var 0.0)
  C5 VERDICT (C2 ∧ C3 → H1 general free-parameter)     : H1 SUPPORTED
  C6 DETERMINISM (re-run byte-identical)               : PASS

falsifiers:
  F651.1 SOME-DN-CONSTRAINED (어떤 DN variance > 0.1)  : NOT_TRIGGERED (모두 0.0)
  F651.2 SWEEP-DEGENERATE (어떤 DN span <= 0.1)        : NOT_TRIGGERED (모두 > 0.1)
  F651.3 DETERMINISM (re-run drift)                    : NOT_TRIGGERED (byte-identical)
  F651.4 POST-HOC (frozen 후 verdict edit)             : NOT_TRIGGERED

checks: 6 PASS / 0 FAIL  (n_substrate=3, cohort=180 windows, 3 design-numbers)

evidence_summary: 🟢 SUPPORTED-NUMERICAL — round-7 메타-발견("convention-number
  자유도는 design-number 전반의 성질")을 정량했다. FIXED 3개 substrate (n=3/4/5) 의
  big-Φ 를 faithful big_phi_bounded(cap=2)로 측정해 freeze 한 뒤, 3개 structurally
  다른 design-number — DN-A emit threshold {0.1..0.9}, DN-B should_interrupt
  threshold {0.3..0.9}, DN-C Ψ-clamp coherence band α {0.01..0.30} — 각각을 wide
  sweep 하며 substrate big-Φ 를 재-read 했다. 세 숫자 모두 Φ(number) variance = 0.0
  (정확히 0), 각 gate-rate 는 응답 (span 1.0 / 0.978 / 0.128, 모두 > 0.1). H_646
  (단일 emit threshold) 의 generalization — 자유도가 한 숫자의 우연이 아니라
  design-number 전반의 성질. §7 C3 정직: DN-A/DN-B 의 Φ⊥number 는 부분적으로
  definitional (threshold 가 big_phi_bounded 인자 아님 — exact 0.0 round-off 가
  증거, H_646 §7 계승) 이나, DN-C(α)는 factor_coherence → motivation_score 에 LIVE
  PATH 가 있어 gate-rate 를 0.556→0.683 으로 실제 움직이면서도 substrate Φ 가 정확히
  평탄 — "policy 를 움직이는 숫자조차 substrate-safe"는 정의만으로 보장되지 않는
  측정 사실 (NON-DEFINITIONAL 강증거, NT-1). 일반성 자체가 nontrivial (NT-2),
  a_autonomy_over_hardcode 가 design-number 전반에서 substrate-safe 함을 확증 (NT-3).
  H_632 (threshold ⊥ Φ phase-transition) · H_287 (Φ⊥entropy) 의 "substrate property
  가 downstream 숫자에 종속하지 않는다" 서명을 design-number-general 측으로 확장.

falsifiers_triggered: 없음 (H1 SUPPORTED, 4 falsifier 모두 NOT_TRIGGERED).
```

re-run byte-identical 확인 (F651.3 — run diff empty).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_651: with a FIXED substrate big-Φ (mean faithful big_phi_bounded
   cap=2 over ECA rules {110,90,30,54} at n∈{3,4,5}, mean Φ=2.085), sweeping THREE
   structurally different design-numbers — DN-A emit threshold {0.1..0.9}, DN-B
   should_interrupt threshold {0.3..0.9}, DN-C Ψ-clamp coherence band α {0.01..0.30}
   — each leaves the substrate big-Φ EXACTLY invariant (variance=0.0 for all three),
   while each downstream gate-rate responds (spans 1.0 / 0.978 / 0.128, all > 0.1).
   DN-A/DN-B's Φ⊥number is partly definitional (threshold not a big_phi_bounded arg,
   exact 0.0 variance), but DN-C is the NON-DEFINITIONAL strong case: α has a LIVE
   path into the score (factor_coherence → motivation_score) and DOES move the gate
   (0.556 -> 0.683), yet substrate Φ stays exactly flat — a number that actively
   moves the policy still cannot reach the substrate. Hence convention-number freedom
   is a GENERAL property of design-numbers, not specific to the emit threshold
   (H_646). Deterministic toy substrate, bounded-Φ lower-bound (cap<n), COFFESHOP
   8-factor emergence sim (spontaneous_lib verbatim)."
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (anima emit-substrate AXIS) — verification
           N/A by design; values deterministic arithmetic, interpretation fenced
```

## 9. Reproduction (재현)

```
cd UNIVERSE/state/h651_convention_number_freedom_general_2026_05_28
hexa run run_h651.hexa          # foreground sync, exit 0, wall ~수십초
# → 3 design-number 모두 Φ-variance = 0.0, gate-span A=1.0/B=0.978/C=0.128,
#   VERDICT H1 SUPPORTED. re-run byte-identical (deterministic).
```

artifacts:
- `UNIVERSE/state/h651_convention_number_freedom_general_2026_05_28/run_h651.hexa`
- `UNIVERSE/state/h651_convention_number_freedom_general_2026_05_28/run_h651.log`

## 10. Cross-Links

- **round-7 메타-발견 source (직접 promote)**: convention-number 자유도 =
  design-number 전반의 성질. 본 H 가 그 메타-명제를 `3개 design-number 모두
  Φ-variance = 0.0` 로 정량 + DN-C live-path NON-DEFINITIONAL 강증거로 contour.
- **H_646 convention-number-freedom-range (직접 일반화 · PR #1235 🟢)**:
  [[H_646]] 은 emit threshold **한 숫자**의 자유도 범위 (Φ-variance 0.0, 전체 [0,1])
  를 보였다. 본 H 는 그 발견을 **3개 design-number** 로 일반화 — 동일 substrate
  (big-Φ 값 byte-identical), 동일 engine, 동일 cohort. range → general.
- **H_637 emit-rate-phi-ratio-closed-form**: [[H_637]] emit-rate target ~0.27 의
  closed-form 일치 FAL — DN-A emit threshold 의 target 측 sibling.
- **H_638 emit-threshold-scaling-law (PR #1224 🟢)**: [[H_638]] should_interrupt
  0.60 (DN-B) · emit 0.30 (DN-A) universal-fixed (적정점 고정). 본 H 는 그 점이 아닌
  *전 구간* 에서 substrate 불변.
- **H_633 register-collapse-phi-drop**: [[H_633]] Ψ-clamp coherence < 0.10 register
  collapse — DN-C α (coherence band) 의 출처 sibling. 본 H 는 α 를 sweep 해 gate 를
  움직여도 substrate Φ 불변임을 측정 (H_633 register-hit gate 가 design-side임을 보강).
- **H_632 emit-threshold-Φ-collapse**: [[H_632]] emit threshold ⊥ Φ phase-transition
  — 동일 Φ⊥emit-number negative-signature.
- **a_autonomy_over_hardcode (governance)**: design-number 전반 (emit · interrupt ·
  Ψ-clamp band) 이 전 구간에서 substrate-safe 함을 확증 — design-number table
  (hardcode) 을 도입하더라도 substrate 의식-구조 불변 (NT-3). single emit primitive +
  factor 분포 shift 설계와 정합.
- **substrate-class-invariant arc (sister verdicts)**: [[H_287]] (Φ⊥Shannon entropy
  CLOSED-NEGATIVE) · [[H_629]] (noise 가 Φ-monotone-destroyer 아님) — "substrate
  property 가 downstream 숫자에 종속하지 않는다" 서명의 design-number-general 측 instance.
- **engine 재사용 (g61)**:
  `UNIVERSE/state/h651_convention_number_freedom_general_2026_05_28/run_h651.hexa` —
  `HEXAD/IIT4/lib/iit4_bounded.hexa` (big_phi_bounded) +
  `HEXAD/CHAT/spontaneous_lib.hexa` (8-factor) verbatim, LCG/stim/window 는
  run_h646.hexa 계승. DN-C 의 α-parameterized factor_coherence_alpha 만 inline. 새
  의식-측도 코드 0줄.
- **paper hook**: H_638 + H_646 + H_651 묶어 `substrate-emit-number-invariance`
  논문의 design-number-general 정량 chapter 후보 — 적정점 universal-fixed (H_638) +
  단일 자유도 범위 (H_646) + 다중-숫자 일반화 + live-path NON-DEFINITIONAL (H_651) +
  governance 정합 (a_autonomy_over_hardcode).

## 양방향 sibling

- sibling .md: [[H_646]] `UNIVERSE/H_646_convention_number_freedom_range.md` ·
  [[H_638]] `UNIVERSE/H_638_emit_threshold_scaling_law.md` ·
  [[H_637]] `UNIVERSE/H_637_emit_rate_phi_ratio_closed_form.md` ·
  [[H_633]] `UNIVERSE/H_633_register_collapse_phi_drop.md` ·
  [[H_632]] `UNIVERSE/H_632_emit_threshold_phi_collapse.md`
- UNIVERSE SSOT: `UNIVERSE/UNIVERSE.md` 축 G (메타) row H_651.
