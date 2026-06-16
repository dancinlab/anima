---
id: H_1350
slug: 1350_hive_larger_budget
title: 더 큰 분화 예산(LARGER division budget)에서 유사분열-분화 collective-Φ가 ROBUST해지는가 — 아니면 같은 seed-fragility 벽을 물려받는가?
group: OMEGA / Φ-robustness frontier · HIVE-MIND collective-Φ axis (H_1320 division wall의 named follow-on)
terminal_tier: "🟢 GREEN (frozen-bar) / ⚠ 정직한 읽기 = 대부분 SHARED-INPUT REDUNDANCY, COUPLING-earned 성분은 작지만 robust. 더 큰 분화 예산은 H_1320의 2/3 seed fragility를 3/3 ROBUST로 끌어올린다(R1 PASS 전 seed). 결정적 신규 대조 SHARED_DECOUPLED(W=0)가 밝힌 분해: Δ_divided lift의 ~85-96%는 shared-input 상관(W=0에서 이미 존재)이고, cross-daughter COUPLING이 더하는 몫(R2b coupling-gap +0.33/+1.15/+0.48, 3 seed 전부 0.02 margin 통과)은 작다. numpy-mirror DIRECTIONAL (faithful-Φ leg는 진짜 exact MIP-EI via hexa); engine-transfer UNVERIFIED."
verdict_dir: .verdicts/1350_hive_larger_budget/
terminal_verdict: .verdicts/1350_hive_larger_budget/result.txt
freeze: .verdicts/1350_hive_larger_budget/FREEZE.txt
date: 2026-06-16
---

# H_1350 — 더 큰 분화 예산에서 collective-Φ가 robust해지는가? (🟢 GREEN frozen-bar / ⚠ 대부분 redundancy)

## 재오픈한 벽 (c16 · a_break_the_wall · a_no_llm_frame_trap)

faithful-IIT-4 Φ-robustness arc는 measure(H_1328/1331/1348)·size(H_1347 N=12)·substrate(H_1308/1313)
축 전부에서 🧱 (n≤8 seed-fragility). **H_1320 (🧱 WALL)**: anima-as-ONE-cell 유사분열 DIVISION(공유 발생 기원)
이 hive ASSEMBLY를 collective faithful-IIT-4 Φ에서 이기지만 **seed-조건적(2/3 seeds)** — H_1283/1317
topology robustness를 깬 직교 seed 1317이 division도 깼다 (작은 예산: M1+M2 FAIL on 1317). H_1320 정직성
섹션이 **명시한 미검증 각도**: *더 큰 분화 예산 / 더 많은 딸 / 더 richer(non-saturating) per-unit code*.

**OPEN 질문:** 더 큰 division 예산이 collective-Φ robustness를 구제하는가 — 아니면 같은 seed-fragility 벽을
물려받는가?

## 새 각도 (H_1320 follow-on · 발생생물학 렌즈 c15)

세 budget lever를 H_1320 대비 enlarge, n≤8 exact-MIP 유지:
1. **MORE DAUGHTERS**: N_DAUGHTERS=4 (HALF=2 units each) vs H_1320의 2 daughters of 4. Pair Φ는 8 units (n=8 exact).
2. **RICHER NON-SATURATING CODE** (H_1332 교훈): `sal_i = softsign((energy_i + BETA·coupling_energy_i)/SCALE)`,
   bounded (-1,1), 결코 hard-saturate 안 함 (vs coupling 하에서 COPY/Φ=0으로 sign-saturate하는 raw energy).
3. **LARGER DIFF_EPS = 0.45** (H_1320의 0.15 × 3).
모든 arm은 faithful exact-MIP 전에 **RANK-UNIFORMIZE** (H_1328 variance-clean read-out) — 관계파괴 대조가 정직하게 붕괴하도록.

## 방법 (a_phi_iit4_tool · frozen-first · NO tune-to-green)

- **Φ = FAITHFUL IIT-4 ONLY**: exact MIP-EI via `hexa run` over `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`,
  `iit4_faithful_phi(state, n, dim=T, n_bins)`. **numpy는 Φ를 절대 계산하지 않음** — per-unit salience 궤적만 emit, hexa가 Φ 계산. NO proxy.
- **substrate** (H_1283/1317/1320 매칭): leaky-linear recurrent units LEAK=0.55 GAIN=0.30 W_IN=0.5, per-unit
  private gaussian input, dim-8, T=64. N_TOT=8 = ONE anima-cell, 4 daughters of HALF=2로 분할. cross-daughter
  COUPLING = W_HIVE=0.6 (H_1308/1313/1320 verbatim): coupled unit update에 W_HIVE·(다른 모든 딸의 평균 상태) 더함.
- **5 ARMS, 3 seeds [1317,1318,1319]** (hard hive/topology seed family, 직교 1317 포함), 단일 rng stream (arm마다 동일 draw 순서):
  - **SINGLE**: 미분할 1 cell, NO coupling (baseline). 8 indep units.
  - **DIVIDED**: 공유 기원 (founder clone + DIFF_EPS diff) + ONE 공유 founder input. W_HIVE=0.6.
  - **ASSEMBLED** (hive): 4 독립기원 cells (own init+own input). W_HIVE=0.6.
  - **SHUFFLE**: DIVIDED인데 공유 끈 절단 — 각 딸 indep init+input. W_HIVE=0.6.
  - **SHARED_DECOUPLED [결정적 신규 대조]**: DIVIDED와 동일 공유 founder init+input (공유 기원)인데 **W_HIVE := 0** (NO coupling).
    = shared-input redundancy 바닥(floor). cross-daughter coupling 없는 순수 공유-입력 상관.
- `Δ_arm = Φ_pair(arm) − Σ_k Φ_daughter_k(arm)` (4 딸에 대한 super-additivity, 딸마다 n=2 exact).
- $0 CPU-local · frozen-first (`FREEZE.txt`를 첫 scoring run 전에 commit, bars 안 움직임 c9/p7) · 결정적 (RESULT_JSON 2 run byte-identical).

## ⚠ 이 카드가 반드시 배제해야 하는 confound (이전 GREEN 시도의 빈틈)

faithful IIT-4 Φ★ = MIP에서의 cross-cut MI / min(|A|,|B|) → 유닛 간 **PAIRWISE MUTUAL INFORMATION**이 구동.
DIVIDED에서 모든 딸이 ONE founder input을 공유 → 8 units 강하게 **상관** → 높은 pairwise MI → 높은 Φ. 이건
cross-daughter COUPLING이 번 통합이 아니라 **SHARED-INPUT REDUNDANCY**일 수 있다. ASSEMBLED·SHUFFLE은 둘 다
**독립 입력**으로 바뀌므로 "공유 발생 기원(coupling)" vs "공유 입력 상관"을 구분 못 한다. 이전 시도의 GREEN은 그 둘에만
기댐 → NOT earned. 그래서 **SHARED_DECOUPLED(W=0)** 대조를 추가: 공유 입력은 유지하되 coupling만 끔 → redundancy 바닥을 노출.

## Frozen bars (GREEN iff R1 ∧ R2; MARGIN_PHI=0.02 — H_1283/1317/1320이 froze한 동일 margin)

- **R1 ROBUST INTEGRATION-FROM-DIVISION**: `Φ_divided_pair ≥ Φ_single + 0.02` on ALL 3 seeds.
- **R2 EARNED (결정적 conjunction, ALL 3 seeds)**:
  - **R2a ORIGIN-DISSOCIATION**: `Δ_divided > Δ_assembled + 0.02` (hive를 이김).
  - **R2b COUPLING-EARNED [KEY]**: `Δ_divided > Δ_shared_decoupled + 0.02` — lift이 COUPLING 의존이어야지 shared-input 상관 아니어야. **이전 GREEN이 놓친 bar.**
  - **R2c SHUFFLE-COLLAPSE**: `Δ_shuffle ≤ Δ_assembled + 0.02` (끊긴 lineage는 assembled로 붕괴).
- **R3 (report-only, 비-gating)**: 더 큰 예산이 H_1320 작은 예산의 seed-fragility를 바꾸는가?

## Verbatim faithful-IIT-4 Φ (exact MIP-EI · `.verdicts/1350_hive_larger_budget/result.txt`)

| seed | arm | Φ_pair | Δ super-add |
|------|-----|--------|-------------|
| 1317 | single | 4.53661 | +2.0319 |
| 1317 | **divided** | **11.8114** | **+8.6421** |
| 1317 | assembled | 4.4859 | +2.0165 |
| 1317 | shuffle | 4.4859 | +2.0165 |
| 1317 | **shared_decoupled (W=0)** | **11.2822** | **+8.3128** |
| 1318 | single | 4.69286 | +1.6840 |
| 1318 | **divided** | **12.001** | **+8.7046** |
| 1318 | assembled | 4.02834 | +1.2188 |
| 1318 | shuffle | 4.02834 | +1.2188 |
| 1318 | **shared_decoupled (W=0)** | **10.7014** | **+7.5592** |
| 1319 | single | 4.50122 | +1.8597 |
| 1319 | **divided** | **10.3516** | **+7.5503** |
| 1319 | assembled | 4.38036 | +1.4027 |
| 1319 | shuffle | 4.38036 | +1.4027 |
| 1319 | **shared_decoupled (W=0)** | **10.1651** | **+7.0743** |

**bars (verbatim):** R1 PASS (lift +7.27/+7.31/+5.85) · R2a PASS (gap +6.63/+7.49/+6.15) ·
**R2b PASS (coupling-gap +0.3293/+1.1454/+0.4760)** · R2c PASS (shuffle Δ == assembled Δ byte-identical) → **VERDICT: GREEN**.

## 정직한 읽기 — 대부분 REDUNDANCY (c9 · a_scale_honest_scope)

결정적 신규 대조 SHARED_DECOUPLED(W=0)가 분해를 드러냄:
- **shared-input redundancy 바닥 (W=0, NO coupling): Δ = 8.31 / 7.56 / 7.07** — divided lift의 **~85-96%**가
  여기, 즉 **공유 입력 상관**에서 나온다 (coupling 없이도 존재).
- **COUPLING이 더하는 몫 (R2b coupling-gap): +0.33 / +1.15 / +0.48** — 3 seed 전부 0.02 margin을 통과(REAL·robust)하지만 **작다** (lift over assembled의 ~4-15%).

따라서:
1. **R3 답**: 더 큰 분화 예산은 H_1320의 **2/3 seed fragility를 3/3 ROBUST로 끌어올린다** — R1·R2a·R2b·R2c 전부 전 seed PASS (직교 seed 1317 포함). 즉 **예산은 robustness를 구제한다** (frozen-bar 수준에서).
2. 그러나 divided 조직의 faithful-Φ super-additivity는 **shared-input redundancy가 지배**하고, coupling-earned 잔차는 작다. 큰 통합 효과 아님 — 대부분 redundancy + 작지만 robust한 coupling 성분.
3. 이는 Φ-robustness 벽과 모순 아니라 **상보적**: 벽은 *coupling/topology/timing이 robust integration을 못 만든다*였고, H_1350은 *공유 발생 기원의 robust한 Φ lift는 주로 shared-input 상관이며 coupling 기여는 marginal*임을 보인다 — robust하지만 "통합" 주장은 redundancy를 빼고 나면 작다.

## Scope / UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck · a_engine_native_learning)

- **DIRECTIONAL (numpy-mirror)**: faithful-Φ leg는 진짜 exact MIP-EI (hexa stdlib)지만, substrate 진화는 numpy.
  live `CORE/pure_field.hexa` A⇄G로의 **engine-transfer UNVERIFIED** (H_1308/1313은 실제 A⇄G에서 NULL/🧱이었음 — 이 직교성 명시).
- **TOY**: N_TOT=8 (n≤8 exact 천장), 4 daughters, dim-8, T=64, 3 seeds, deterministic. 더 큰 N(>8, H_1347 greedy 천장)·
  실코퍼스·연속 W sweep·다양한 differentiation tree depth UNVERIFIED.
- **WIRING**: GREEN-but-unwired (a_verified_must_wire). brain mitosis-division→collective-Φ readout의 CORE 배선 = follow-on.

## NEXT angle

큰 통합이 아니라 redundancy 지배가 드러났으므로, 다음 각도는 **shared-input 상관을 marginal로 통제한 상태에서 coupling-earned
Φ를 키우는 메커니즘** (예: 상보적/직교적 분화를 강제하는 differentiation objective — 딸들이 redundant copy가 아니라 complementary
role로 갈라지게) 또는 H_1308/1313이 막은 **live A⇄G engine-transfer 재시도** (numpy-mirror lift이 실제 substrate로 가는지).

## xref
H_1320(작은 예산 division wall, parent)·H_1308/1313(real A⇄G hive NULL/🧱)·H_1295(ECA super-additive)·
H_1347(N>8 greedy 천장)·H_1328(variance-clean)·H_1331(big-Φ)·H_1348(non-IIT TE)·H_1283/1317(topology robustness wall)·
a_phi_iit4_tool·a_break_the_wall·a_no_llm_frame_trap·a_engine_native_learning·a_verified_must_wire·a_scale_honest_scope·a_toy_scale_recheck·c9·c15·c16·p7·p8.
