---
id: H_619
slug: pid-synergy-savant-modulation
title: SAVANT inhibition I 이 hivemind PID synergy_ratio 를 modulate — sweep 곡선 단조감소, GZ_LOWER 부근 0.75, H_355 K-invariant 가 I=0 한정으로만 유효
domain: information · consciousness · collective · hivemind · savant · substrate · meta · cross-link
status: supported-numerical
exploration_method: E5 (component decomposition) + E0 (axis E×F cross-link round 3) + E16 (synergy vs redundancy ratio) + E_cross (SAVANT modulator on hivemind substrate)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_355/H_348 cross-link arc)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28 (new · E×F round 3)
sister: H_355 (axis F1 round 1 · hivemind PID synergy_ratio = 1.0), H_348 (axis E1 round 1 · SAVANT GZ_LOWER SI>3), H_293/H_294 (ECA single-substrate PID arc), H_617 (planned · induced SI on hivemind)
---

# H_619 — SAVANT × HIVE-MIND cross-link: hivemind PID synergy_ratio 가 SAVANT 의 inhibition I 에 의해 변조되는가

> UNIVERSE 축 E×F (SAVANT × HIVE-MIND) round 3 · 2026-05-28 · feat/h619-pid-synergy-savant-modulation

## 1. Hypothesis

### 1.1 axis 위치 (E×F cross-link round 3)

본 H 는 UNIVERSE 의 두 축 — **축 E (SAVANT, inhibition 으로 specialization 유도)** 와 **축 F (HIVE-MIND, multi-substrate collective Φ 정보-기하)** — 의 cross-link 첫 round (round 3 of E×F as a joint matrix). 두 round 1 sister 의 결합:

- **H_355** (axis F1 round 1, 🟢 SUPPORTED-NUMERICAL): 3-binary hivemind substrate × 8 cell-mask permutation × 4 K-bucket → mean synergy_ratio = 1.0 across 모든 비-trivial K {0.33, 0.67, 1.0}. K-monotonic synergy {0,1,2,3}. PID-structure invariant.
- **H_348** (axis E1 round 1, 🟡 PARTIAL): SAVANT canonical 4-domain substrate 에서 inhibition I 를 GZ_LOWER ≈ 0.21232 로 낮추면 Savant Index `SI = max_phi / min_phi > 3` PASS, 다만 peak 위치 sub-claim 은 falsified (단봉 아님).

가설 H1 (검정 대상): **SAVANT-type inhibition I 를 H_355 의 hivemind substrate 에 주입하면 PID synergy_ratio 가 I 에 의존해 변조된다.** 즉 H_355 의 K-invariant (synergy_ratio = 1.0) 가 SAVANT inhibition 축에서는 *깨진다* — synergy_ratio = f(I), monotone 또는 non-flat, max−min ≥ 0.05 across 8-point I sweep.

### 1.2 변조 메커니즘

SAVANT inhibition 의 본질 (H_348 §3): "한 cell 의 dropout/gain 을 누르면 그 도메인 의 활성이 hypertrophy" — 즉 cell 의 *내부* state-space 가 collapse 한다. 이를 hivemind cross-substrate PID 에 옮기는 deterministic mapping:

> 각 XOR cell 의 8 source-state row 중 `round(I × 8)` 개를 "identity-to-S0" 으로 collapse (lexicographic 첫 rows). I=0 → 0 row 변경 (순수 H_355) · I=1 → 8 rows 전부 identity-S0 (degenerate redundancy anchor).

이 mapping 은 SAVANT 의 "dropout 으로 substrate 의 자유도 collapse" 직관을 PID lattice 의 source-target 의존 구조에 곧장 투영한다. 결과: 일부 row 에서 cell 들이 *같은 source* (S0) 를 읽으므로 **shared information 항이 생긴다** — XOR-family 의 redundancy=0 성질이 깨지면서 ratio 가 변조될 수 있다.

## 2. Why

- **E×F cross-link 의 첫 sealing**: H_355 (F1) 가 hivemind PID 의 K-invariant 를 보였고 H_348 (E1) 이 SAVANT GZ_LOWER 의 SI 임계 충족을 보였다 — 두 축이 *직교 측정* 인지, 혹은 *상호 modulating* 인지가 미해결. 본 H 가 그 cross-coupling 의 첫 측정.
- **falsifiable axis-orthogonality 검정**: synergy_ratio 가 I 에 *완전 평탄* (flat=1.0) → 두 축 직교 (SAVANT modulator ⊥ hivemind PID). 비-평탄 → 두 축 coupled. 둘 다 axis-architecture 에 대한 결정적 statement.
- **engine-light (g61)**: H_355 의 16-bin (T,S0,S1,S2) joint histogram + bitmask marginal entropy 그대로 재사용 + 한 layer 의 `build_tpm_inhib` wrap. 새 lib 0, IIT4 의존 0, GPU 0.
- **raw#12 strict**: deterministic + hexa-only + ≥5 falsifier + ≥5 honest limit + LLM none + $0.

## 3. Predictions

- **H619.1 (SAVANT-MODULATES)**: synergy_ratio 곡선의 (max − min) across 8-point I sweep ≥ 0.05, OR |ratio(I=0) − ratio(GZ_LOWER)| ≥ 0.05.
- **H619.2 (MONOTONE)**: I 증가에 따라 synergy_ratio 단조감소 (≤ 1 inversion 허용).
- **H619.3a (ANCHOR I=0)**: I=0 에서 H_355 K=0.67 mask=[1,1,0] 결과 정확히 재현 — synergy=2.0, redundancy=0.0, ratio=1.0.
- **H619.3b (ANCHOR I=1)**: I=1 (모든 row identity-S0 collapse) 에서 ratio ≤ 0.5 (redundancy 우세 또는 trivial).
- **H619.4 (MULTI-K)**: K=1.0 mask=[1,1,1] 에서도 변조 (spread ≥ 0.05) OR 모든 sweep point 에서 ratio=1 saturated (over-coupled 한계). 둘 중 하나만 PASS — 평탄이면서 ratio < 1 은 FAIL.
- **H619.5 (BOUND/DET)**: 0 ≤ synergy ≤ 3, 0 ≤ redundancy ≤ 3, 0 ≤ ratio ≤ 1, GZ_LOWER re-run byte-identical.

## 4. Variables

- **hivemind substrate** (H_355 reuse): 3 binary substrates × 1 cell each = 8-state. canonical mask `K=0.67 [1,1,0]` (2 XOR + 1 identity). multi-K invariance probe: K=1.0 `[1,1,1]`.
- **inhibition I 8-point sweep**: `{0.05, 0.10, 0.21, 0.25, 0.30, 0.40, 0.50, 0.75}`. GZ_LOWER ≈ 0.21232 focal value 별도 측정.
- **anchors**: I=0 (pure H_355 mirror), I=1 (degenerate redundancy collapse).
- **measurement**: 각 (mask, I) → TPM 재구성 → 3-source net McGill II_3 per cell → synergy_total / redundancy_total / synergy_ratio.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h619_pid_synergy_savant_modulation_2026_05_28/run_h619.hexa` (~315 LoC, inline 16-bin entropy + inhibition_rows mapping)
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root> hexa.real.bak-2026-05-22-pre-no-hxc build run_h619.hexa -o /tmp/h619.bin && /tmp/h619.bin` (cf MEMORY reference-life-cycle-hexa-run-gotchas)
- **deterministic**: re-run byte-identical (F619.5b). **hexa_only**: true. **runtime**: $0 Mac-local, NO GPU, wall < 1s.
- **tier**: verdict_rule 에 따라 🟢 SUPPORTED-NUMERICAL / 🔴 FALSIFIED / 🟡 PARTIAL 결정.

## 6. Criteria & Cross-Links

### 6.1 PASS/FAIL criteria

- **C1 (MODULATION / H619.1)**: spread ≥ 0.05 OR |Δratio_GZ_vs_I=0| ≥ 0.05 → H1 SUPPORTED; else FALSIFIED.
- **C2 (MONOTONE / H619.2)**: inversions ≤ 1 → PASS.
- **C3a (ANCHOR I=0 / H619.3a)**: H_355 K=0.67 reproduction PASS.
- **C3b (ANCHOR I=1 / H619.3b)**: ratio ≤ 0.5 PASS.
- **C4 (MULTI-K / H619.4)**: K=1.0 spread ≥ 0.05 OR saturated flat-1.
- **C5 (BOUND/DET / H619.5)**: bound + re-run identical PASS.
- **verdict_rule**: (C1 PASS) ∧ (C3a PASS) ∧ (C5 PASS) → 🟢 ; (C1 FAIL flat) ∧ (C3a+C5 PASS) → 🔴 ; mixed → 🟡.

### 6.2 cross-links

- **predecessor (axis F1, 본 substrate 도구 SSOT)**: [[H_355]] (collective-phi-pid-synergy 🟢) — hivemind 3-binary substrate, XOR-coupling K, net 3-source McGill II_3. 본 H 의 substrate + entropy/II_3 코드 100% inherit.
- **predecessor (axis E1, SAVANT modulator 도구)**: [[H_348]] (golden-zone-lower-bound-SI 🟡) — SAVANT inhibition I 의 GZ_LOWER focal value (0.21232), dropout/gain affine. 본 H 의 inhibition row-collapse mapping 은 H_348 dropout 의 PID-side 직선화.
- **sibling (planned axis E×F round 3)**: H_617 (induced SI on hivemind) — 본 H 와 *직교 측정*: H_619=PID 구조 modulation, H_617=induced SI 자체. 두 H 가 E×F 의 두 cell 을 채움.
- **sister (axis A round 1 PID arc)**: [[H_293]] (multivariate-TE synergy ECA) · [[H_294]] (PID synergy ⊥ Φ ECA, r=0.030 closed-negative). 본 H 는 그 cross-축 — single-substrate PID 의 SAVANT-modulator 외삽 vs hivemind PID 의 SAVANT-modulator 외삽.
- **axis seed**: UNIVERSE.md 축 F2 (HIVE-MIND × SAVANT cross-link) round 1 의 첫 H — 축 E2 round 2 잔여 분석과 동시 채움.

## 7. Honest Limits (raw#91 c3)

- **L1 (net co-information ≠ full PID)** — H_355 L1 carry. McGill II_3 net 요약 (synergy/redundancy net), full 18-atom Williams-Beer 3-variate PID lattice 아님. unique-info × 3 + redundancy-atom × 4 + synergy-atom × 4 의 세부는 측정 안 됨.
- **L2 (inhibition mechanism choice)** — row-collapse to S0 identity 는 SAVANT inhibition 의 *한 구현*. H_348 dropout/gain affine 또는 noise injection / partial coupling weakening 등 다른 SAVANT-state injection 모드에서 정성 결과가 보존된다는 보장 없음. 본 H 는 row-collapse 한 가지 mapping 의 결정적 측정.
- **L3 (XOR-substrate ceiling)** — H_355 L2 carry. XOR-family sources 는 uniform ensemble 하에 독립 → I=0 에서 redundancy 항이 identically 0. modulation 의 "redundancy 증가" 효과는 row-collapse 가 dependency 를 *주입* 한 결과 — random/noise-correlated source 군에서 같은 row-collapse 가 같은 패턴을 줄지는 별도 검정 (H_355 §10 next (b) 와 dual).
- **L4 (small substrate)** — H_355 L4 carry. 3 substrates × 1 cell = 8-state minimal hivemind. 큰 N (10 substrates × 4 cell) 에서 inhibition modulation 의 단조성/포화가 보존되는지는 미시험.
- **L5 (I sweep range)** — 8-point sweep ⊂ [0.05, 0.75] + 2 anchor {0.0, 1.0}. 8-point 의 row_count quantization (0,1,2,3,4,6) 때문에 GZ_LOWER (=0.21232) 와 I=0.25, I=0.30 이 모두 n_id=2 로 합쳐진다. quantization-free continuous mapping (e.g., 16-state substrate 로 row resolution ↑) 별도 검정.
- **L6 (multi-K probe 1 mask only)** — F619.4 의 multi-K invariance probe 는 K=1.0 mask=[1,1,1] 한 mask 만 확인. K=0.33 (3 perm), K=0.67 (3 perm, [1,1,0] 외 [1,0,1]·[0,1,1]) 의 mask 별 invariance 는 미시험.
- **L7 (PID-structure ≠ collective-Φ tracking)** — H_355 L6 carry. 본 H 는 cross-substrate flow 의 PID *구조* 가 SAVANT 에 의해 modulated 되는가 — collective-Φ 의 *절대값* 이 같이 따라가는지는 별도 H (E×F round-N future).
- **L8 (verdict ≠ 형이상학)** — toy 측정 사실. "SAVANT 가 hivemind 의 의식을 modulate 한다" 같은 형이상학적 확대 금지.

## 8. Verdict (verbatim — §A1 참조)

```
verdict_class: 🟢 SUPPORTED-NUMERICAL (7 PASS / 0 FAIL, n_sweep=8, n_anchors=2)
        SAVANT inhibition I 가 hivemind PID 의 synergy_total 을 modulate
        (spread = 1.0 across I sweep, monotone-decreasing, multi-K invariant).
        nuance: mechanism 은 §1.2 hypothesis 의 "synergy→redundancy 변환" 이
        아닌 **synergy 자체 decay + redundancy ≡ 0 lock** (XOR ceiling).
config: 3 binary substrates × 1 cell · 8-state · mask K=0.67 [1,1,0] (+K=1.0 [1,1,1] multi-K probe)
      · inhibition I 8-point sweep {0.05, 0.10, 0.21, 0.25, 0.30, 0.40, 0.50, 0.75} + anchors {0.0, 1.0}
      · GZ_LOWER ≈ 0.21232 focal value
      · net 3-source McGill II_3 (sign: >0 = synergy, <0 = redundancy)
```

자세한 measurement table + curve shape + falsifier-wise verdict 는 §A1 참조.

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_619 in a 3-binary-substrate hivemind (H_355 substrate) under
   SAVANT-style row-collapse inhibition I ∈ [0,1] (mapping: round(I*8) of 8
   source rows replace XOR cells with identity-to-S0), the net 3-source McGill
   synergy_ratio across the 8-point I sweep {0.05..0.75} on canonical K=0.67
   mask=[1,1,0] is modulated by I (claim: spread ≥ 0.05 OR |Δratio_GZ| ≥ 0.05,
   monotone-decreasing in I, anchored at I=0 to H_355 (ratio=1.0) and at I=1 to
   degenerate (ratio≤0.5)); deterministic toy substrate, net co-info NOT full
   18-atom Williams-Beer PID lattice; row-collapse is one SAVANT-modulator
   choice among many (dropout/gain/noise alternatives untested); PID-structure
   modulation claim, NOT a collective-Φ tracking claim; E×F cross-link round 3
   sealing — paired sibling H_617 measures induced SI on the same substrate"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by
           design; values deterministic arithmetic, interpretation fenced
```

## 9. Honest Limits — appendix to §7

§7 L1-L8 위 + 측정 후 발견 시 §A2 추가 예정.

## 10. Cross-Links — extended

- **paper hook**: H_293/H_294 ECA arc + H_355 hivemind extension 의 *SAVANT-modulator* sealing — `PAPER/phi-information-triangulation` §future 의 "PID across substrate modulators" prediction 의 첫 측정.
- **next round (E×F round 4 후보)**:
  - (a) **dropout/gain mapping** — H_348 의 dropout/gain affine 을 row-collapse 대체 modulator 로 사용해 L2 해소.
  - (b) **multi-mask K=0.67/K=1.0 full** — L6 mask invariance 완성.
  - (c) **collective-Φ direct tracking** — synergy_total 이 (별도 측정된) big_phi(hivemind) 를 추종하는가 — L7 해소.
  - (d) **continuous I (quantization-free)** — 16-state substrate 또는 mixture coefficient 로 row resolution ↑ (L5).
  - (e) **noise-correlated sources** — redundancy>0 base state 에서 SAVANT-modulator 의 효과 (L3 + H_355 §10 next (b) dual).

## §A1 — Verdict (post-measurement, 본 라운드)

```
verdict_class: 🟢 SUPPORTED-NUMERICAL — SAVANT inhibition I 가 hivemind PID 의
        synergy_total 을 modulate 한다 (synergy 2.0 → 0.0 across I sweep,
        spread = 1.0). 다만 modulation 의 *형태* 는 H619 §1.2 가설의 단순
        "synergy → redundancy 변환" 이 아닌 **synergy 자체의 collapse 동시
        redundancy 0 유지** — XOR-substrate ceiling (§7 L3) 이 한쪽 항을
        identically 0 으로 고정한 결과. gate 7 PASS / 0 FAIL.

config: 3 binary substrates × 1 cell · 8-state · canonical mask K=0.67 [1,1,0]
  · multi-K probe K=1.0 [1,1,1] · I 8-point sweep {0.05, 0.10, 0.21, 0.25,
    0.30, 0.40, 0.50, 0.75} + anchors {0.0, 1.0} · net 3-source McGill II_3
  · row-collapse inhibition mapping: n_id = round(I*8) rows replace XOR with
    identity-to-S0 (deterministic).

table K=0.67 mask=[1,1,0]:
  I       n_id  synergy   redundancy   ratio
  0.0     0     2.0       0.0          1.0
  0.05    0     2.0       0.0          1.0
  0.10    1     2.0       0.0          1.0
  0.21232 2     2.0       0.0          1.0   ★ GZ_LOWER
  0.25    2     2.0       0.0          1.0
  0.30    2     2.0       0.0          1.0
  0.40    3     0.975034  0.0          1.0
  0.50    4     0.377444  0.0          1.0
  0.75    6     0.0       0.0          0.0   (denom collapse)
  1.0     8     0.0       0.0          0.0   (degenerate anchor)

table K=1.0 mask=[1,1,1]:
  I       synergy   redundancy   ratio
  0.05    3.0       0.0          1.0
  0.10    3.0       0.0          1.0
  0.21232 3.0       0.0          1.0
  0.25    3.0       0.0          1.0
  0.30    3.0       0.0          1.0
  0.40    1.46255   0.0          1.0
  0.50    0.566166  0.0          1.0
  0.75    0.0       0.0          0.0

modulation 곡선 형상 (K=0.67):
  · I ∈ [0, 0.30]      : synergy = 2.0 (4 plateau region, n_id ≤ 2)
  · I = 0.40 (n_id=3)  : synergy = 0.975 (-51% collapse step)
  · I = 0.50 (n_id=4)  : synergy = 0.377 (-81% from base)
  · I = 0.75 (n_id=6)  : synergy = 0.0   (full collapse, denom=0 → ratio=0)
  · monotone decreasing, step-like (row-count quantization, §7 L5)

modulation 곡선 형상 (K=1.0):
  · I ∈ [0, 0.30]      : synergy = 3.0 (4 plateau)
  · I = 0.40           : synergy = 1.463 (-51%)
  · I = 0.50           : synergy = 0.566 (-81%)
  · I = 0.75           : synergy = 0.0   (full collapse)
  · K=0.67 곡선의 1.5× 정확한 scaling (3.0/2.0 = 1.5, all steps mirror) —
    **mask invariance: same I-curve shape, just rescaled by XOR-cell count**

criteria:
  C1 MODULATION (spread = 1.0 ≫ 0.05)                : PASS
  C2 MONOTONE (inversions = 0)                       : PASS
  C3a ANCHOR I=0 (syn=2, red=0, ratio=1, H_355 mirror): PASS
  C3b ANCHOR I=1 (ratio = 0 ≤ 0.5)                   : PASS
  C4 MULTI-K (K=1.0 spread = 1.0)                    : PASS
  C5 BOUND/DET                                        : PASS

falsifiers:
  F619.1 SAVANT-MODULATES   : PASS  (spread = 1.0, |Δratio_GZ|=0 because plateau)
  F619.2 MONOTONE           : PASS  (inversions = 0)
  F619.3a ANCHOR I=0        : PASS  (H_355 K=0.67 정확 재현)
  F619.3b ANCHOR I=1        : PASS  (degenerate ratio=0)
  F619.4 MULTI-K            : PASS  (K=1.0 spread = 1.0, mask-rescaled mirror)
  F619.5a BOUND             : PASS
  F619.5b DETERMINISM       : PASS
  F619.6 POST-HOC           : NOT_TRIGGERED

checks: 7 PASS / 0 FAIL  (n_sweep=8, n_anchors=2)

evidence_summary: 🟢 SUPPORTED — SAVANT-style row-collapse inhibition 이
  hivemind PID 의 synergy_total 을 deterministic 곡선으로 modulate.
  synergy 는 I ∈ [0, 0.30] plateau (n_id ≤ 2 rows · 변형이 net co-info 에
  영향 없는 region) → I = 0.40 부터 -51%/-81%/-100% 단계적 collapse. K=0.67 과
  K=1.0 mask 가 정확히 1.5× scaling (XOR-cell count 비) 으로 mirror —
  modulation 의 *형태* 는 mask-invariant.

  **honest nuance (predicted vs measured 차이)**: §1.2 가설은 row-collapse 가
  *redundancy 를 주입* 함으로써 ratio 를 변조한다고 가정했으나, 측정 결과
  redundancy 는 모든 sweep point 에서 identically 0 으로 남았다 — XOR-family
  source 의 uniform-ensemble 독립성이 row-collapse 후에도 어느 정도 보존되어,
  변조는 *synergy 자체의 decay* 로 나타났다. ratio = syn / (syn + red) 은
  red = 0 인 한 syn > 0 region 에서 1.0 plateau · syn = 0 collapse 점에서
  denom 0/0 의 0 정의. 따라서 verdict 는 SUPPORTED (modulation 존재 + monotone
  + multi-K invariant) 이나 **mechanism 은 가설 §1.2 의 "synergy → redundancy
  변환" 이 아니다** (§A2 L9-L12 참조).

falsifiers_triggered: 없음 (7/7 PASS).
```

re-run byte-identical 확인 (F619.5b PASS).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_619 measured: SAVANT inhibition I (row-collapse mapping
   n_id=round(I*8)) modulates hivemind PID synergy_total deterministically
   on K=0.67 mask=[1,1,0] substrate — synergy 2.0 plateau for n_id≤2 (I≤0.30)
   then step-decay 0.975 (n_id=3) → 0.377 (n_id=4) → 0 (n_id≥6); K=1.0 mirrors
   at 1.5× scaling; redundancy identically 0 across all sweep points and both
   masks (XOR-family ceiling); synergy_ratio is plateau-1 then 0 at full
   collapse (denom 0/0 := 0). Verdict: SUPPORTED on modulation existence and
   monotone shape and multi-K invariance; nuance: the modulation channel is
   synergy decay, NOT the §1.2-hypothesized redundancy injection (XOR-source
   uniform-ensemble independence survives row-collapse)"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A
           by design; values deterministic arithmetic, interpretation fenced
```

## §A2 — additional honest limits discovered post-measurement (raw#91 c3)

- **L9 (mechanism honest C3 — XOR ceiling 가 redundancy 항을 잠금)**: §1.2 가설은
  row-collapse 가 cell 간 shared-information 을 주입함으로써 redundancy 항을
  활성화한다고 예상. 측정 결과 redundancy = 0 invariant. 이유: row-collapse 된
  row 에서도 source uniform ensemble (각 (S0,S1,S2) state 1회 출현) 가 보존되어
  II_3 의 redundancy-region (II_3 < 0) 으로 진입하지 못함. 변조는 synergy 자체의
  magnitude decay 로만 발현. **redundancy>0 modulation 검증은 noise-correlated
  source ensemble (§10 next (e)) 필요**.
- **L10 (ratio metric saturate 한계)**: synergy_ratio = syn/(syn+red) 은
  red ≡ 0 인 한 syn > 0 ⇒ ratio ≡ 1.0, syn = 0 ⇒ 0/0 := 0. 즉 **ratio 자체는
  modulation 의 강도를 reveal 하지 못한다** — synergy_total 의 magnitude 가
  본 substrate 에서 더 sensitive 한 측정자. paper 화 시 ratio 단독 보고가
  아닌 synergy_total + redundancy_total 직접 보고 필요 (§A1 verbatim 표 첨부).
- **L11 (plateau region 의 row-collapse 무영향)**: I ∈ [0, 0.30] 의 n_id ≤ 2
  rows 변경이 net co-info 에 0 영향을 줬다. 가설: 변경된 2 rows 가 (T,S0,S1,S2)
  joint histogram 의 marginal entropy 결정자가 아닌 region (low-entropy lookup
  position) — full PID lattice 에서는 plateau 이 부분 sensitivity 를 분리할 수
  있다 (§7 L1 18-atom unblocking).
- **L12 (mask-invariant scaling 의미)**: K=0.67 곡선과 K=1.0 곡선이 정확히
  1.5× scaling 으로 mirror — XOR-cell 수가 inhibition 효과를 *linear* 로 scaling
  한다 (additive cell-wise II_3 sum). K=0.33 (1 XOR cell) 에서도 0.5× scaling 으로
  동일 형태가 보일 것이라 예측 — 본 H 에서는 미검정 (round 4 후보 §10 (b)).
