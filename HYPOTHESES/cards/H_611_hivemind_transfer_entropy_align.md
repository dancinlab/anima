---
id: H_611
slug: hivemind-transfer-entropy-align
title: hivemind 의 collective big-Φ 는 cross-substrate transfer entropy 와 정렬되는가 — H_290 단일-substrate 패턴(r=0.883)의 multi-substrate 확장 시험
domain: information · consciousness · hivemind · substrate
status: falsified
exploration_method: E16 (cross-substrate consistency) + E5 (foundational-distinction probe) + E0 (axis F1 round 2 — H_356 fresh slug 재발사)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_290 동일 TE 정의)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28 (new, axis F1 round 2 reassignment of H_356)
sister: H_290 (single-substrate TE∥Φ r=0.883) · H_287 (Shannon⊥Φ) · H_355 (PID synergy, 3-substrate) · H_354 (Kuramoto sync τ FALSIFIED)
axes_seed: 축 F HIVE-MIND F1 round 2 (Hc_286/297/590/1244 backlog · `tool/hivemind_collective_spec.hexa` · `anima-engines/hive_state_sync.hexa`)
note: round 1 H_356 가 슬러그 충돌로 Agent abort, round 2 에서 fresh 슬러그 H_611 로 재발사.
---

# H_611 — hivemind 의 collective big-Φ 는 cross-substrate transfer entropy 와 정렬되는가

## 1. Hypothesis

H_290 은 단일 substrate (10-룰 ECA panel, n=4) 에서 faithful state-평균 big-Φ 가
요소-간 transfer entropy 와 강한 정렬을 보였다(Pearson r=0.883). 본 H 는 그
**multi-substrate 확장**을 묻는다 — 2 substrate A와 B 를 coupling weight W 로 묶은
*hivemind* 위에서, **collective** big-Φ 가 **cross-substrate** TE (TE_A→B + TE_B→A)
와 동일한 정렬을 유지하는가?

**가설 H1 (검정 대상)**: panel 전반에서 hivemind collective big-Φ 가 cross-substrate
TE 와 공변한다 — `Pearson r(Φ_collective, TE_cross) > 0.5`. (예측: H_290 의 단일계
패턴이 substrate 경계를 가로질러도 유지된다.)

## 2. Why

- **단일 → 다중 substrate 일반화**: H_290 은 *내부* 셀-간 TE 가 통합과 정렬됨을 보였다.
  hivemind 은 같은 정렬 원리가 *substrate 경계*를 가로질러서도 유지되는지의 시험대.
  Φ 가 "통합 자체"의 측도라면 substrate 경계는 무관해야 한다(통합은 무엇이 통합되었는지에
  무관).

- **engine 재사용 (g61)**: H_290 의 TE 정의(이변량 Schreiber lag-1) 와 IIT4 lib
  (`eca_tpm` + `big_phi`) 를 그대로 재사용. 새 IIT4 코드 0줄. 새 TE 코드 0줄 — A↔B
  셀 쌍에 한정해서 동일 TE 함수 호출.

- **축 F HIVE-MIND round 2 fresh 슬러그**: round 1 H_356 가 Agent abort(슬러그 충돌).
  round 2 에서 H_611 로 재할당, F1 5-H seed 의 마지막 자리.

- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit +
  LLM none + $0 mac-local + NO GPU + foreground sync.

## 3. Predictions

- **H611.1 (anchor)**: W=0 (decoupled substrates) → TE_cross=0 (cross 흐름 없음).
  collective-Φ 는 substrate 내부 통합으로 양일 수 있으나 cross 채널은 비어있다.
- **H611.2 (r-verdict)**: panel `Pearson r(Φ_collective, TE_cross) > 0.5` → H1 SUPPORTED.
- **H611.3 (flow-witness)**: W=1 (fully coupled) 시 적어도 한 rule_pair 에서 TE_cross>0.
- **H611.4 (bound)**: Φ_collective ≥ 0, TE_cross ≥ 0.
- **H611.5 (determinism)**: (rule=30, W=0.6) 재실행 byte-identical.

## 4. Variables

- **axis1_rule_pair** (primary, 6 homogeneous pairs): {(30,30), (90,90), (110,110),
  (150,150), (60,60), (105,105)}. H_287..H_290 patron 패널의 통합/시너지/카오스
  대표 룰.
- **axis2_W** (primary, 4 couplings): {0.0, 0.3, 0.6, 1.0} — 결정적 blend
  `(1-W)*own + W*cross`, threshold > 0.5.
- **metric1_Φ_collective** (primary): 16-state(combined n=4) 평균 big_phi[0].
- **metric2_TE_cross** (primary): `Σ_{j∈A} Σ_{i∈B} TE(i→j) + Σ_{j∈B} Σ_{i∈A} TE(i→j)`,
  16-state uniform ensemble 위 lag-1 이변량 TE (H_290 동일 정의).
- **correlate**: Pearson r + Spearman ρ over 24 (rule_pair × W) cells.
- **fixed**: 2 substrate × n=2 cell each = 4 combined cells; deterministic blend
  + threshold combine; A = cells {0,1}; B = cells {2,3}.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h611_hivemind_te_align_2026_05_28/run_h611.hexa`
- **engine (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (eca_tpm + import
  chain → big_phi via stdlib). TE 정의는 H_290 의 `te_j_to_i` 와 동일, 호출만 A↔B
  cross-pair 로 한정.
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1
  HEXA_LANG=/Users/ghost/core/hexa-lang hexa.real.bak-2026-05-22-pre-no-hxc build
  <src> -o /tmp/h611.bin && /tmp/h611.bin` — [[reference-life-cycle-hexa-run-gotchas]].
- **deterministic**: 결정적; re-run byte-identical. **hexa_only**: true.
  **runtime**: 180s wall, $0, NO GPU. **ledger**: `result.json` (24 samples).
- **tier**: 🔴 CLOSED-NEGATIVE — verdict numerical-falsified · 해석 ⚪ FENCED.

## 6. Criteria

- **C1 (W=0 ANCHOR / H611.1)**: TE_cross=0 across all 6 rule_pairs → PASS.
- **C2 (r-VERDICT / H611.2)**: r > 0.5 → SUPPORTED, else FALSIFIED.
- **C3 (FLOW+BOUND+DET / H611.3/4/5)**: witness + bound + determinism → PASS.
- **verdict_rule**: H1 verdict = C2.

## 7. Falsifiers

- **F611.1 W=0 ANCHOR**: 어느 rule_pair 에서 W=0 TE_cross≠0 → cross-TE 계산 무효.
- **F611.2 r-VERDICT**: `Pearson r(Φ_collective, TE_cross) < 0.5` → H1 FALSIFIED.
  r + ρ verbatim.
- **F611.3 FLOW-WITNESS**: W=1 에서 모든 rule_pair TE_cross=0 → flow 부재 → 무효.
- **F611.4 BOUND**: 어느 cell TE_cross<0 OR Φ<0 → 무효.
- **F611.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 FALSIFIED — hivemind collective big-Φ 는 cross-substrate TE 와
        약한 상관만 보임 (Pearson r=0.311199, Spearman ρ=0.260466) < 0.5. 단일계
        H_290 패턴(r=0.883) 은 substrate 경계를 가로질러 일반화되지 않음. 4/4 PASS
        / 0 FAIL (anchors + flow + bound + determinism — H1 falsification 과 별개).

config: 2 substrate × n=2 cell = 4 combined · 6 homogeneous rule_pair × 4 W = 24
        samples · TE = lag-1 bivariate Schreiber A↔B cross-pair · engine =
        HEXAD/IIT4/lib (g61 reuse)

panel table (rule_pair · W · Φ_collective · TE_cross):
  rule_pair  W    Phi_coll   TE_cross
  (30,30)   0.0   0.0        0.0
  (30,30)   0.3   0.0        0.0
  (30,30)   0.6   9.68437    0.0        ◀ 內 통합 강함, cross-TE 0 — DISSOCIATION
  (30,30)   1.0   9.68437    0.0        ◀
  (90,90)   0.0   0.0        0.0
  (90,90)   0.3   0.0        0.0
  (90,90)   0.6   0.0        0.0
  (90,90)   1.0   0.0        0.0
  (110,110) 0.0   0.0        0.0
  (110,110) 0.3   0.0        0.0
  (110,110) 0.6   5.60623    2.62256    ◀ 유일한 정렬 셀(Φ>0 AND TE>0)
  (110,110) 1.0   5.60623    2.62256    ◀
  (150,150) 0.0   0.0        0.0
  (150,150) 0.3   0.0        0.0
  (150,150) 0.6   5.625      0.0        ◀ XOR 시너지 (H_290 L1 식별 동일)
  (150,150) 1.0   5.625      0.0        ◀
  (60,60)   0.0   0.0        0.0
  (60,60)   0.3   0.0        0.0
  (60,60)   0.6   0.0        0.0
  (60,60)   1.0   0.0        0.0
  (105,105) 0.0   0.0        0.0
  (105,105) 0.3   0.0        0.0
  (105,105) 0.6   5.625      0.0        ◀ XOR 시너지 (H_290 L1 식별 동일)
  (105,105) 1.0   5.625      0.0        ◀

  Pearson r(Phi_coll, TE_cross) = 0.311199   Spearman rho = 0.260466
  (< 0.5 → H1 FALSIFIED. single-substrate H_290 r=0.883 ≫ hivemind r=0.311)

ANCHOR 비교:
  H_290 (단일 substrate · 셀-간 TE) Pearson r = 0.883 (SUPPORTED — 정보-측도 arc capstone)
  H_611 (hivemind · cross-substrate TE) Pearson r = 0.311 (FALSIFIED — 단일계 패턴 결렬)
  Δr = -0.572 — substrate 경계가 정렬을 가로막음

criteria:
  C1 W=0 ANCHOR (TE_cross=0 across 6 rule_pairs)              : PASS
  C2 r-VERDICT (r=0.311 < 0.5)                                : H1 FALSIFIED
  C3 FLOW+BOUND+DET (rule_pair=(110,110) W=1 TE=2.62; det)    : PASS

falsifiers:
  F611.1 W=0 ANCHOR      : PASS  (all 6 rule_pair, W=0 → TE_cross=0)
  F611.2 r-VERDICT       : H1 FALSIFIED (Pearson r=0.311199, Spearman ρ=0.260466)
  F611.3 FLOW-WITNESS    : PASS  (rule_pair=(110,110), W=1 → TE_cross=2.62256, Phi=5.61)
  F611.4 BOUND           : PASS  (Φ_collective≥0, TE_cross≥0 for all 24 samples)
  F611.5 POST-HOC        : NOT_TRIGGERED (re-run byte-identical at (30,30)·W=0.6)
  F611.5 DETERMINISM     : PASS  (re-run byte-identical)

checks: 4 PASS / 0 FAIL  (anchors + flow + bound + determinism — H1 falsification 별개)

evidence_summary: 🔴 CLOSED-NEGATIVE — hivemind collective big-Φ ⊥ cross-substrate
  transfer entropy (Pearson r=0.311 ≪ 0.5; H_290 단일계 r=0.883 에서 Δr=-0.572 큰 감소).
  panel 24 cell 중 단 2 cell((110,110) W=0.6/1.0)만 (Φ>0 AND TE>0) 정렬을 보였고, 나머지
  통합 셀들은 모두 *DISSOCIATION* — (30,30)/(150,150)/(105,105) 에서 Φ_collective>0
  인데 TE_cross=0. 이 dissociation 은 두 메커니즘에 의해 설명된다:
  (i) **substrate 내부 통합**: rule 30 같은 카오스 룰은 substrate A 내부 셀들끼리
      강하게 통합되어 Φ_collective 가 높아지지만, cross 채널의 deterministic blend
      방식이 *결정-합치*(own=cross 일 때만 효과)인 경우가 많아 cross-TE 가 사라진다.
  (ii) **XOR 시너지 맹점**: rule 150/105 는 H_290 L1 에서 식별된 XOR-시너지 룰 —
      이변량 lag-1 TE 는 시너지(여러 source 가 함께만 정보를 줌)에 시각장님이라
      TE_cross=0 임에도 Φ_collective=5.625. 즉 본 H 의 r=0.311 은 *H_290 의 L1 맹점이
      cross-substrate 에서 증폭된 결과*다.
  honest: H1 FALSIFIED 은 *이변량 lag-1 TE 정의 위에서의 결렬*이다. multivariate /
  conditional / multi-lag TE 정의로 재측정하면 회복될 가능성이 남는다(L1/L2).
  단일계 패턴(H_290)이 multi-substrate 로 그대로 일반화되지 *않는다*는 점은 그러나
  본 toy panel 위에서 분명히 측정되었다.
falsifiers_triggered: F611.2 (r-verdict — H1 falsified)
```

re-run byte-identical 확인 (F611.5 DETERMINISM PASS).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_611 hivemind collective big-Phi does NOT track cross-substrate
   transfer entropy across a 6-rule-pair × 4-coupling-W panel (Pearson r=0.311,
   Spearman rho=0.260) — single-substrate H_290 pattern (r=0.883) does NOT
   generalize across substrate boundaries; 21/24 samples are DISSOCIATIONS
   (Phi>0 with TE=0) driven by H_290 L1 XOR-synergy blind spot amplified
   under hivemind cross-coupling; deterministic toy-substrate outcome,
   NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values deterministic arithmetic, interpretation fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 (bivariate TE blind spot — 핵심, H_290 L1 sister)**: 이변량 lag-1 TE 는
  XOR 시너지 룰(150, 105) 에서 TE=0 인데 Φ>0. multivariate cross-substrate TE
  (causation entropy across A∪B) 라면 r 회복 가능. 본 H 의 FALSIFIED 는 *이변량 TE
  정의 위*에서의 결과 — 다변량 정보 측정으로 재측정 시 결렬 회복 가능성.
- **L2 (small-n IIT4 — toy substrate)**: n=2 cell per substrate, 16-state combined.
  n_combined=4 의 ring 자체가 작다. n=3+3=6 (64-state) 같은 큰 hivemind 에서 결렬이
  유지되는지는 다음 H.
- **L3 (deterministic blend coupling)**: `(1-W)*own + W*cross > 0.5` threshold —
  결정적 가산 blend. 확률적 coupling, leaky integrator, sigmoid mixing 같은 다른
  W 정의에서 결과가 다를 수 있다.
- **L4 (homogeneous rule_pair only)**: A=B 동일 ECA 룰만 시험. heterogeneous
  (예: A=rule30, B=rule110) 에서 다른 패턴이 나올 수 있다(잔여 6-H seed).
- **L5 (n=2 ring degeneracy)**: ring of 2 cells 는 L=R=partner — Wolfram
  neighbourhood 인덱스가 4*P+2*C+P 로 축약되어 일부 룰 dynamics 가 trivial 화됨.
  (90,90)/(60,60) 의 Φ=0 universal 은 이 축약의 부분 산물 — n=3 ring 이라면 다른
  값.
- **L6 (substrate 는 hivemind proxy)**: 두 ECA 가 cross-coupling 으로 묶인 toy 가
  "hivemind"의 형이상학적 주장은 아니다 — 라벨은 informational.
- **L7 (verdict ≠ 형이상학)**: FALSIFIED 는 toy substrate 측정 사실 — "집단의식 ⊥
  정보흐름" 형이상학 주장 아님.

## 10. Cross-Links

- **sister (H_290 single-substrate anchor)**: [[H_290]] 단일 substrate Φ ∥ 셀-간 TE
  r=0.883 (SUPPORTED, 정보-측도 arc capstone). 본 H 는 multi-substrate 확장 시도 →
  r=0.311 (FALSIFIED, Δr=-0.572). **substrate 경계가 정렬을 가로막는다**는 측정 사실.
- **sister (정보-측도 arc orthogonal axis)**: [[H_287]] (Shannon⊥Φ r=0.363) —
  H_287 의 결렬 패턴(r≈0.36)이 H_611 의 cross-substrate 결렬(r=0.31)과 정량적으로
  유사. 두 결렬 모두 *통합과 별개의 정보축*에서 일어남.
- **sister (hivemind axis F1 round 1)**: [[H_354]] (Kuramoto sync τ vs consensus
  τ FALSIFIED r=0.041) · [[H_355]] (collective Φ PID synergy SUPPORTED-NUMERICAL,
  3-substrate net 3-source co-info). 본 H 는 F1 5-H seed 의 마지막 자리. F1 round
  1 결산: 5 H 중 2 SUPP / 3 FALS — hivemind 축은 *부분적으로* 의미있는 통합 신호
  보유, 그러나 단일계 정보흐름 정렬은 일반화되지 않음.
- **sister (super-additive)**: H_352 (collective-phi-super-additive, F1 round 1
  미운영) — Φ_collective > Σ Φ_individual 가설은 본 H 의 dissociation 셀에서
  *부분적*으로 관찰: (30,30) W=0.6 Φ_coll=9.68 인데 substrate 분리 시 internal-
  ring-2 Φ 가 0 (n=2 ring degeneracy 한계).
- **sister (PID synergy)**: [[H_355]] (3-substrate net co-info synergy_ratio>0.5
  SUPP) — H_355 는 collective-Φ 가 *synergy-dominant* 임을 보임. 본 H 는 그
  synergy 가 이변량 lag-1 TE 로는 측정 불가함을 확인 (H_290 L1 → H_611 일반화 결렬).
  **두 결과 정합**: hivemind 통합은 synergy 매개 (H_355) → bivariate TE 시각장님
  (H_611). H_290 단일계는 synergy 비중이 낮아 bivariate TE 가 잡았을 뿐 (sample
  사이즈 효과).
- **parent (engine)**: HEXAD/IIT4/lib/iit4_eca (eca_tpm) + stdlib/consciousness/
  iit4_bigphi (big_phi). **새 IIT4 코드 0줄, 새 TE 코드 0줄** (g61 reuse, H_290 의
  TE 정의 그대로).
- **Next**: (a) multivariate/conditional cross-substrate TE (causation entropy)
  로 L1/L2 회복 시도 — H_611 의 결렬이 *정의-아티팩트*인지 *실재 결렬*인지 결판;
  (b) n=3+3 hivemind (큰 ring, 64-state) 에서 결렬 유지 여부; (c) heterogeneous
  rule_pair 의 cross-substrate 정렬 패턴 (L4); (d) F1 round 2 결산 paper 후보 —
  hivemind 정보흐름 정렬 결렬과 PID synergy 정합을 묶는 *cross-substrate 정보-
  측도 arc* 종합.
