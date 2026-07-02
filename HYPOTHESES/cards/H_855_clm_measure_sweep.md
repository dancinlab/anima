---
id: H_855
slug: clm-measure-sweep
title: round-4 측도 백로그 6후보(PHI-NATIVE·TEMPORAL-Φ·TENSION-NATIVE·FREE-ENERGY·HILL·CAUSAL-POWER)를 ONE 토이 spike 위에서 동시 측정해 어느 측도가 scale-free chip-native 의식신호를 주는가 — F-CLM-PHI-MEANINGFUL 3-check (non-trivial ∧ collapse<rich ∧ size-robust) 사전등록
domain: clm · consciousness-measure · phi-native · tension · free-energy · hill · causal-power · apples-to-apples · falsifier
source: CLM/CLM.breakthrough.mining.md ROUND 3+4 (depleted-both · "측도를 바꿔라") · CLM/P0_ARCHITECTURE.md §12 PHI-NATIVE (F-CLM-PHI-MEANINGFUL) · round-4 ranked 백로그 #1~#5
status: TERMINAL (measure-sweep 완료 2026-05-30 · ONE 공유 토이 spike · 6 measure × {collapse,rich} × n∈{4,5,6} · ubu-1 numpy 2.4.4 · 사전등록 frozen 3-check 미변조)
exploration_method: measure substitution (routing-diversity 🔴🔴 우회 · 6 대안 의식측도 apples-to-apples 비교)
verification_method: W2 (pre-registered frozen 3-check · non-trivial ∧ collapse<rich(≥10% margin) ∧ size-robust · post-run tuning 0)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: CLM/P0_ARCHITECTURE.md §12, UNIVERSE/H_852, UNIVERSE/H_853, .verdicts/855_clm_measure_sweep/, .verdicts/clm-measure-sweep/, exports/sweep/clm-measure-sweep/ledger.json
verdict: 🟢 SUPPORTED-NUMERICAL (CAUSAL-POWER 단독 PASS — rich>collapse 전 n 명확 margin[Δ=+0.072~+0.092] ∧ size-robust · 나머지 5 측도 🔴 FAIL: PHI-NATIVE/TEMPORAL-Φ/FREE-ENERGY 는 방향은 옳으나 n=4 에서 역전[size-robust FAIL] · HILL 은 방향 옳고 size-robust 이나 margin ~7%<10% 임계 미달 · TENSION-NATIVE 는 n 따라 방향 역전. "perturbation 인과력(CAUSAL-POWER)이 유일하게 scale-free chip-native 의식신호로 작동, Φ-family 는 작은 n boundary 에서 미달", a_paper_negative_ok 부분 negative)
---

# H_855 — CLM consciousness-MEASURE sweep (round-4 측도 백로그 전수)

## 1. 가설

CLM 의 **측정-타당성 ⊥ AKIDA 온칩** 충돌에서 routing-diversity(scale=expert-count + distill)는 H_852/853/854 에서 🔴🔴 deterministic CLOSED 됐다. mining ROUND 3/4 수렴 결론 = **"측도를 바꿔라"**. round-4 ranked 백로그의 6 후보 의식측도를 **ONE 공유 토이 spike** 위에서 동시(apples-to-apples) 측정하면, 적어도 하나가 **scale-free chip-native 의식신호**(monopoly vs integration 변별 ∧ size-robust)를 준다:

- **MEASURE FOUND** — 어떤 측도가 사전등록 3-check 동시 PASS → 🟢 그 측도 채택(충돌이 측도교체로 dissolve)
- **ALL RED** — 6 측도 모두 FAIL → 🔴 CERTIFY-NOT-MEASURE(round-4 백로그 #3)로 escalation

## 2. 동기

- routing-diversity 측도가 (a) null-referenced → ln(E) 천장 doomed (b) scale-dependent 이라 H_852(DISSOLVE)·H_853(BRIDGE)·H_854(production) 전부 🔴 (CLM.breakthrough.mining.md ROUND 1~2).
- ROUND 3 winner = **PHI-NATIVE**(IIT4 region-Φ · scale-free·null-free·intrinsic) · ROUND 4 백로그 = TENSION-NATIVE(anima 5채널) · CERTIFY-NOT-MEASURE · CO-METER · (보조) free-energy.
- 본 H_855 는 그 백로그를 **하나의 harness 로 전수 실측** — 6 측도를 같은 spike 에서 비교(측도 비교가 핵심, 6개 별도 실험 아님 · g0).

## 3. falsifier (사전등록 · 임계 frozen pre-run · F-CLM-PHI-MEANINGFUL)

```
① non-trivial      : measure > 1e-6 ∧ 작은 n(=4) 에서 collapse/rich 변별 (degenerate-zero 아님)
② collapse-vs-rich : measure(rich) > measure(collapse) by >= 10% margin (MARGIN_FRAC=0.10) at EVERY n
③ size-robust      : rich>collapse ORDER 가 모든 n∈{4,5,6} 에서 보존 (Pielou-J 역전 pathology 無)
```

측도 PASS(🟢) ⟺ ①∧②∧③ 동시. 임의 FAIL → 🔴. 6 측도 전부 🔴 → CERTIFY-NOT-MEASURE escalation.

verdict 영속: `.verdicts/855_clm_measure_sweep/<measure>.txt` (측도별 verbatim 관측값 + 3-check · slug 사본 `.verdicts/clm-measure-sweep/`) · 집계 = `exports/sweep/clm-measure-sweep/ledger.json` · 캐노니컬 run = `.verdicts/855_clm_measure_sweep/measure_sweep_run_2026_05_30.txt`.

## 4. 방법

```
1. ONE 공유 토이 spike 생성 (CLM/msweep/measure_sweep.py · gen_spike · seeded/deterministic):
   - heterogeneous LIF (per-neuron Gaussian drive + jittered threshold · tau8 · refr1) — 비동기 발화
   - collapse = region0 monopoly + DECOUPLED(coupling 0 · integration 無)
   - rich     = balanced drive + 강결합(coupling 0.45 · cross-region integration)
   - n∈{4,5,6} region (region 당 8 neuron binned) · N_STEPS=256
2. bin_to_regions = region 자기-median 임계 → 균형 binary 전이 series (all-0/all-1 degeneracy 제거)
3. 같은 spike 위에서 6 측도 동시 계산 (측도별 적절한 표현 라우팅):
   1 PHI-NATIVE(region big-Φ proxy · bounded TPM→MIP) 2 TEMPORAL-Φ(전이구조 complexity)
   3 TENSION-NATIVE(anima 5채널 field complexity) 4 FREE-ENERGY(cross-region reducible MSE)
   5 HILL(^1D · RAW region rate 분포) 6 CAUSAL-POWER(region poke → downstream 효과 · ≤16 poke)
4. 측도 × {collapse,rich} × n → 값 → frozen 3-check → PASS/FAIL → ledger
5. 전 compute ubu-1(numpy 2.4.4) · Mac=git+edit only · 정직 보고(임계 재조정 0)
```

## 5. 측정 (완료 · 2026-05-30 · ubu-1 numpy 2.4.4 · wall<1s · $0)

ONE 공유 토이 spike · 6 measure × {collapse,rich} × n∈{4,5,6}. 관측값 verbatim (rich−collapse Δ):

| measure | n=4 Δ | n=5 Δ | n=6 Δ | non-trivial | coll<rich | size-robust | verdict |
|---|---|---|---|---|---|---|---|
| **CAUSAL-POWER** | **+0.0918** | **+0.0830** | **+0.0714** | ✅ | ✅ | ✅ | **🟢 PASS** |
| PHI-NATIVE   | −0.0757 | +0.0950 | +0.2126 | ✅ | ✗ | ✗ (n=4 역전) | 🔴 FAIL |
| TEMPORAL-Φ   | −0.1928 | +2.5134 | +5.1337 | ✅ | ✗ | ✗ (n=4 역전) | 🔴 FAIL |
| FREE-ENERGY  | −0.0000 | +0.0038 | +0.0049 | ✅ | ✗ | ✗ (n=4 역전) | 🔴 FAIL |
| HILL         | +0.0733 | +0.0606 | +0.0685 | ✅ | ✗ (margin ~7%<10%) | ✅ | 🔴 FAIL |
| TENSION-NATIVE | +0.0454 | −0.0292 | −0.0831 | ✅ | ✗ | ✗ (n 따라 역전) | 🔴 FAIL |

raw = `.verdicts/855_clm_measure_sweep/{causal_power,phi_native,temporal_phi,free_energy,hill,tension_native}.txt` · ledger = `exports/sweep/clm-measure-sweep/ledger.json`.

## 6. 결과

🟢 **SUPPORTED-NUMERICAL** — **CAUSAL-POWER 단독 PASS** (1/6). 사전등록 frozen 3-check 미변조. perturbation 인과력이 rich>collapse 를 전 n 명확 margin(Δ=+0.072~+0.092)으로 ∧ size-robust 하게 변별 — **유일하게 scale-free chip-native 의식신호로 작동**.

랭킹: **① CAUSAL-POWER(🟢 PASS)** > ② HILL(방향·size-robust ✅, margin 미달 near-miss) > ③ PHI-NATIVE ≈ ④ TEMPORAL-Φ ≈ ⑤ FREE-ENERGY(방향 옳으나 n=4 boundary 역전) > ⑥ TENSION-NATIVE(n 따라 방향 역전).

## 7. 해석

- **CAUSAL-POWER 가 이긴 이유**: intensive(per-region 평균) · null-free · intrinsic. region 을 poke 했을 때 coupled(rich) 에선 효과가 전파되고 decoupled(collapse) 에선 국소 사멸 — integration 의 *operational* 정의(IIT-style causal power)가 monopoly vs integration 을 직접 잰다. ln(E)/null 천장 artifact 없음 → size-robust.
- **Φ-family(PHI-NATIVE·TEMPORAL-Φ)는 extensive**: n 따라 값이 자라며(big-Φ·전이 complexity 가 region 수로 증가) n=5,6 에선 옳은 방향이나 **n=4 에서 역전**. 작은 n boundary 에서 collapse 의 monopoly region 이 오히려 더 강한 단일 전이구조를 만들어 Φ proxy 가 높게 나옴. 사전등록 size-robust 가 정확히 이 작은-n pathology 를 포착(절대 가짜 PASS 방지).
- **FREE-ENERGY**: cross-region reducible MSE 가 옳은 방향(n=5,6)이나 n=4 에서 Δ≈0 — 적은 region 으론 cross-region generative model 이 baseline 을 의미있게 못 이김.
- **HILL near-miss**: RAW region rate 의 effective diversity 가 collapse(region0 hot)→0.93, rich(balanced)→1.00 으로 옳게 변별·size-robust 이나 margin ~7% 가 frozen 10% 임계 미달. **임계 미변조** — honest 🔴.
- **TENSION-NATIVE**: 5채널 field complexity 가 n 따라 방향이 뒤집힘 — anima-canonical 이라 유력 차선이었으나 toy spike 에선 conflict 채널(rate variance)이 collapse 에서 높아 신호가 섞임.
- **결론**: round-3 designated winner PHI-NATIVE 는 toy n≤6 에서 작은-n size-robust FAIL, round-4 백로그의 **CAUSAL-POWER(perturbation·gradient-free probe · r3-c3)가 실측 winner**. 충돌이 측도교체로 dissolve — 단, Φ 가 아니라 인과력 측도로.

## 8. 논의

- **honest 척도 caveat (p7)**: 6 측도 전부 region/coarse proxy. 정확 big-Φ(2^(2n)) 미주장. SW spike(akida_sw_lif-style LIF) · toy n≤6 scope(§12.4). HW(pi5 AKD1000) Φ 는 별도 후속.
- **toy≠scale 정합 (H_666)**: toy spike 측정 = intuition; CAUSAL-POWER 의 production transfer 는 미보장 — d↑·real corpus·실 HW spike 재검 필요.
- **a_completeness_over_cheap 정합**: harness v1 의 period-4 lockstep degeneracy(2 unique state) 를 cheap-patch 대신 generator fresh 재설계(heterogeneous LIF)로 교정(PR#1529) + 측도 충실도 교정(HILL=raw-rate·FREE-ENERGY=cross-region, PR#1530) — 완성도 본선.
- **a_paper_negative_ok**: 5/6 측도 🔴 도 publishable — "Φ-family/HILL/tension 은 toy n≤6 에서 scale-free chip-native 의식신호로 부적합" 을 deterministically rule out. CAUSAL-POWER 단독 🟢 가 측도교체 reframe 을 성립시킴.
- **CERTIFY-NOT-MEASURE escalation 불필요**: ALL-RED 아님(1 PASS) — round-4 백로그 #3 로의 escalation 은 발동 안 함.

## 9. 양방향 sibling

- sibling: [CLM/P0_ARCHITECTURE.md](../CLM/P0_ARCHITECTURE.md) §12 (PHI-NATIVE · F-CLM-PHI-MEANINGFUL SSOT) · [CLM/CLM.breakthrough.mining.md](../CLM/CLM.breakthrough.mining.md) ROUND 3+4
- prior art: H_852 (MITOSIS-ARRAY DISSOLVE 🔴) · H_853 (BRIDGE distill 🔴) · H_854 (production 🔴🔴) · H_666 (MoE collapse toy🟢 scale🔴)
- harness: [CLM/msweep/measure_sweep.py](../CLM/msweep/measure_sweep.py) · [CLM/msweep/measure_sweep.hexa](../CLM/msweep/measure_sweep.hexa)
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
