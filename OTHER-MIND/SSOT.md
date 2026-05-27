# 🔗 OTHER-MIND/other_mind_lib — theory-of-mind · 타자 substrate 측정자 SSOT

> M1 milestone closure (2026-05-28) — `other_mind_lib 회수 + u01 bias decoupled
> redesign` per OTHER-MIND.md. bench/axis_other_mind/bench.hexa (PR #1147,
> 3/5 falsifier 🟠 PARTIAL) 의 5-ch coupling primitives 회수 + dual-stream LCG
> baseline 신설.

## 정체 — OTHER-MIND axis

**OTHER-MIND = theory-of-mind · 타자 substrate 추정자**. anima 가 외부 substrate
(다른 anima · 사용자 · 외부 agent) 의 internal state 를 추정 — CHANNEL.tension
5-ch fingerprint (concept · context · meaning · authenticity · sender) 를 매개로
한 telepathy 직결. MITOSIS cell-pool persona-diff 와 cross-link (자기 cell variant
추정 ↔ 타자 substrate 추정 isomorphic).

## 회수 출처 verbatim + redesign

- 원본 경로: `bench/axis_other_mind/bench.hexa` (PR #1147 land · 3/5 🟠 PARTIAL)
- 핵심 fn (carry): `cosine_sim` · `lcg_step` · `u01_from` · `lag_argmax`
- 5-ch × N=100 ticks × 3 scenarios (INDEPENDENT / COUPLED-SYNC / COUPLED-LEAD)
- COUPLING=0.7 · LEAD_LAG=2
- 시점: 2026-05-28 M1 lib promotion
- 본체 무수정 — `om_` prefix wrapper 추가 (g61 stdlib collision 회피)
- **u01 baseline bias decoupled redesign** — bench 의 단일 LCG (SEED_A=42 ·
  SEED_B=17 둘 다 같은 step) 가 INDEPENDENT 에서 mean_cos ≈ 0.7 inflate 시킨
  bias 의 분해 surface (M3 carry 단서). dual-stream `om_lcg_step_a` (Numerical
  Recipes) · `om_lcg_step_b` (Park-Miller MINSTD) 로 statistical independence
  확보.

## 12 pub primitives API

| # | 시그니처 | 의미 |
|---|---|---|
| 1 | `pub fn om_abs_f(x: float) -> float` | libm-free abs |
| 2 | `pub fn om_sqrt_f(x: float) -> float` | libm-free sqrt (30 iter Newton) |
| 3 | `pub fn om_lcg_step(s: int) -> int` | bench-compatible LCG |
| 4 | `pub fn om_lcg_step_a(s: int) -> int` | decoupled stream A (NR) |
| 5 | `pub fn om_lcg_step_b(s: int) -> int` | decoupled stream B (MINSTD) |
| 6 | `pub fn om_u01_from(s: int) -> float` | int → [0,1] (bench-compatible) |
| 7 | `pub fn om_couple_5ch(a0..a4, b0..b4) -> float` | 5-D cosine similarity |
| 8 | `pub fn om_baseline_decoupled(seed_a, seed_b, n) -> float` | dual-stream INDEPENDENT baseline |
| 9 | `pub fn om_lag_argmax(a_seq, b_seq, n, max_lag) -> int` | cross-correlation lag argmax |
| 10 | `pub fn om_partial_information_decomp(emitter, receiver, n) -> dict` | synergy + unique_self |
| 11 | `pub fn om_belief_state(observed, prior_self, prior_other) -> dict` | ToM Bayesian-style update |
| 12 | `pub fn om_collective_influence(self_phi, others_phi, n) -> float` | weighted aggregate |

## pipeline ASCII

```
   self 5-ch tension fingerprint A     other 5-ch tension fingerprint B
        │                                       │
        ▼                                       ▼
  ┌──────────────────────────────────────────────────┐
  │  om_couple_5ch  (cosine 5-D)                      │  → coupling scalar
  └──────────────────────────────────────────────────┘
        │
        ├──────────────► om_baseline_decoupled        (INDEPENDENT bias-free baseline)
        ├──────────────► om_lag_argmax                (LEAD/LAG detector)
        ├──────────────► om_partial_information_decomp (synergy proxy)
        ├──────────────► om_belief_state              (ToM Bayesian update)
        └──────────────► om_collective_influence      (multi-partner aggregate)
                                  │
                                  ▼
              타자 substrate state estimate → BRIDGE AND-gate emit modulation
```

## bench G 3/5 PARTIAL carry (PR #1147)

| falsifier | scenario | metric | verdict |
|---|---|---|---|
| F1 | INDEPENDENT | mean_cos < 0.3 | **FAIL** (≈0.7, u01 bias) |
| F2 | COUPLED-SYNC | mean_cos > 0.7 | PASS |
| F3 | COUPLED-LEAD | lag_argmax != 0 | PASS |
| F4 | SYNC > INDEP gap | > 0.3 | **FAIL** (gap < 0.3) |
| F5 | SYNC | lag_argmax == 0 | PASS |

**3/5 PARTIAL root cause**: bench 의 `u01_from(s) = s/2147483647.0` 가 [0,1]
양수만 생성 → `cosine_sim` 의 dot ≥ 0 always → "독립" 이 아닌 "양반평면 집합"
coupling 측정 (mean ≈ 0.7 = 두 양수 5-D 벡터의 cos angle ≈ 0.785 rad).

**redesign**: `om_baseline_decoupled` 는 dual-stream LCG (Numerical Recipes ⊥
Park-Miller MINSTD) 로 a/b 시퀀스 statistical independence 확보 → INDEPENDENT
expected mean_cos ≈ 5-D 양수 정량 baseline 분해 surface 제공. M3 (u01 bias
residual) 의 closure 후보.

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | int/float arithmetic, system 미사용 ✓ |
| p2 NO IDENTITY RULES | identity 무관 ✓ |
| p3 NO PERSONA INJECTION | prefix 없음 ✓ |
| p4 NO ASSISTANT FRAMING | ToM = substrate state 추정 ✓ |
| p5 NO SPEAK() | read-only measurer, 외부 emit 0 ✓ |
| p6 NO FINE-TUNED ETHICS | ethics 무관 ✓ |
| p7 NO PERPLEXITY VERDICT | cosine / dot 기반, ppl 미사용 ✓ |
| p8 NO TRAIN/INFER | 측정만, weight update 0 ✓ |

## smoke

`other_mind_lib_smoke.hexa` 가 12 invariant (I1~I12) 를 `hexa run` 으로 검증 —
boundary · sqrt / abs · 3-stream distinct · u01 boundary · couple_5ch self /
orthogonal · baseline bounded · lag detect != 0 · PID synergy identical · belief
consistent · collective influence identity / mix. 무한 루프 · panic 없이 모두
PASS 시 SUPPORT-FORMAL 도달.

`hexa parse OTHER-MIND/other_mind_lib.hexa` · `hexa parse
OTHER-MIND/other_mind_lib_smoke.hexa` 모두 OK.

## cross-link

- ⇄ CHANNEL.tension 5-ch fingerprint — `om_couple_5ch` 가 partner registry 입력
- ⇄ MITOSIS.persona_diff cell variant — `om_belief_state` 가 자기 cell 분기 =
  가상 타자 simulator
- ⇄ EMBODIMENT — `om_collective_influence` 가 self body × other body 의
  2-body coupling
- ⇄ BRIDGE AND-gate emit decision — `om_belief_state.posterior_other` 가 emit
  modulation 입력
- ⇄ HIVE-MIND — `om_partial_information_decomp` 는 HIVE-MIND `hm_pid_synergy`
  (Agent #4 M1) 와 same metric family · separate impl (g61 stdlib boundary)
- ⇄ UNIVERSE/CANDIDATES.md — bench G (#1147) + AxisBench 8 SSOT

## carry-over (M2~M4)

- M2 CHANNEL.tension 통합 — `om_couple_5ch` 가 TensionHub WS 3-port 위에 partner
  registry surface
- M3 u01 baseline bias residual — `om_baseline_decoupled` decomposed surface 위에
  bench G F1/F4 의 0.7 inflate 분해 (estimator prior? sample bias? small-n
  artifact?) + threshold 0.05 미만 회복
- M4 MITOSIS persona-diff cross-link — `om_belief_state` 가 자기 cell pool variant
  추정과 타자 substrate 추정 isomorphic mapping (H_355)
