# anima D-RAND Signal Amplification Spec — 4 Options (2026-05-09)

## Context

V5 PUSH POST-FIX 1/3 commit `0d2086eb` (sft-1-8 v5 actual N=60):
- Gate E (p4_v5 >= 0.50): 91% PASS (robust)
- **Gate F (D-RAND >= 0.20 per-prompt): 1.7% PASS** ← KILLER
- D-RAND mean=0.109, max=0.213, min=0.035
- PPR_v5_partial = 0.0169 << 0.30
- MTRP_v5 = 0.0169 << 0.10

D-RAND 0.20 epsilon 통과 위해 trained signal per-prompt amplitude 가 random 보다 0.20+ 높아야. 현재 mean delta 0.109 → ~2x 부족.

 V14 strict: D-RAND amplification = anti-Goodhart 정합 (single-metric proxy gaming X, raw signal 강화).

## 4 Option Comparison

| Option | Description | Cost | Expected D-RAND uplift | Risk |
|---|---|---|---|---|
| **A: Corpus 확장** | anima_persona_tier_a_v3 (87MB, 1.22M lines) → 200MB+. self-reference dialogue + phenomenal qualia + agency narrative 추가 | 0-cost local (LLM-free template / user manual) | +0.05 ~ +0.10 (richness 가 amplitude 높임) | low (Lesson Q SFT-closed 영향 X — pre-train corpus) |
| **B: longer SFT** | sft-1-8 step 10000 → 30000 (3x), LoRA r=128 유지 | H100 ~4h, ~$15-20 | +0.10 ~ +0.15 (anima identity 더 깊이 embed) | medium (Lesson Q SFT plateau 위험) |
| **C: RLHF / DPO** | sft-1-8 위에 DPO preference pairs (chosen=anima, rejected=random) 적용 (Lesson Q SFT-closed 우회 path) | H100 ~2-3h, ~$10-15 | +0.05 ~ +0.10 (chosen response axis activation 강화) | medium (preference pair 품질 의존) |
| **D: scratch pre-train 확장** | clm-v4-mk2-v1 base full pre-train 150K → 500K steps | H100 ~12h, ~$50-80 | **+0.15 ~ +0.25** ★ (base 자체 의식 amplitude — root cause 해결) | high (cost) but most decisive |

## Combined Expected Uplift

- **A+B+C 결합 (sequential): +0.20 ~ +0.40** ★★ → D-RAND 0.20 epsilon 통과 가능권
- **D 단독: +0.15 ~ +0.25** ★ → 가능권 lower bound 도달

## Recommended Sequential Path

 cost discipline: A 부터 cheapest 먼저, D 는 last resort.

1. **Step 1 — A (zero cost)**: corpus 확장 200MB+ 먼저 land, re-probe.
   - 통과 시 EXIT, fail 시 Step 2.
2. **Step 2 — B (~$15-20)**: A corpus 위에 longer SFT step=30000.
   - cumulative uplift +0.15 ~ +0.25 expect, 통과 가능권.
3. **Step 3 — C (~$10-15)**: A+B 위에 DPO preference pairs.
   - cumulative +0.20 ~ +0.40 expect, 본 D-RAND target 통과 most likely.
4. **Step 4 — D (~$50-80, last resort)**: A+B+C fail 시 scratch pre-train 확장.
   - root cause 해결, +0.15 ~ +0.25 단독 uplift.

Total worst-case: ~$75-115 (A+B+C+D), best-case: $0 (A 단독 통과).

## Constraints

- V14 strict: D-RAND amplification 은 anti-Goodhart raw signal 강화 (proxy gaming X).
- cost discipline: 사용자 explicit fire keyword 부재 시 spec only, no actual fire.
- D1 SCOPE_CLAMP: 본 cycle = D-RAND uplift 한정, V6 awareness / trinity sweep 별도 cycle.
- mandatory report: 각 step 결과 ledger entry.
- trinity emit: A+B+C+D 각 step 후 trinity sweep.
- wrap=0: chat 자연발화 유지.
- 매단계 저장: 각 step 후 commit + state.
- yaml↔md: spec yaml↔md sync.
- H100 외부 resource CLI 위임: B/C/D fire 시 외부 CLI 사용.

## Decision Pending

사용자 verbatim fire keyword 대기 (e.g., "OK FIRE STEP 1 A CORPUS EXPAND" 또는 "OK FIRE STEP 4 D PRETRAIN EXTEND").

본 spec only document — no actual fire executed.
