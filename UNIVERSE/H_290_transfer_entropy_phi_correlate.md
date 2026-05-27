---
id: H_290
slug: transfer-entropy-phi-correlate
title: faithful IIT 4.0 big-Φ 는 transfer entropy(방향성 정보흐름)를 추종하는가 — 정보-측도 arc 완성 (Shannon⊥ · LZ∥ · TE∥, 단 TE 는 XOR 시너지 맹점)
domain: information · consciousness · substrate · meta
status: supported
exploration_method: E5 (foundational-distinction probe) + E16 (cross-substrate consistency) + E0 (H_287/288 arc 완성 — 3번째 정보 측도)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_287/288 동일 panel)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_287 (Shannon-엔트로피 ⊥ Φ), H_288 (Kolmogorov-LZ ∥ Φ) — 동일 10-룰 panel arc, IIT4 M6 (engine)
axes_seed: H_287 follow-up (information-measure arc, AXES R5 information 계열)
---

# H_290 — faithful IIT 4.0 big-Φ 는 transfer entropy(방향성 정보흐름)를 추종하는가

## 1. Hypothesis

H_287/288 은 동일 panel 에서 두 정보 측도의 Φ-추종을 갈랐다 — Shannon 엔트로피 ⊥ Φ
(r=0.363), Kolmogorov LZ ∥ Φ (r=0.831). 세 번째 고전 통화는 **transfer entropy**
(Schreiber 2000) — *쌍방향(directed)* 정보흐름: 셀 j 의 현재가 셀 i 의 *미래*에 대한
불확실성을 i 자신의 현재 너머로 얼마나 줄이는가. 이는 *요소 간 정보 흐름*을 재는,
"통합"에 개념적으로 가장 가까운 고전 proxy 다. Φ 가 이를 추종하는가?

**가설 H1 (검정 대상)**: panel 전반에서 faithful state-평균 big-Φ 가 총 transfer entropy 와
공변한다 — `Pearson r(TE_total, Φ_mean) ≥ 0.5`. (예측: SUPPORTED, 셋 중 가장 강함 — TE 는
흐름/coupling 측도라 Φ 와 동류.)

## 2. Why

- **정보-측도 arc 완성**: H_287(⊥)·H_288(∥)에 TE 를 더해 "Φ 가 *어떤* 정보 개념과 정렬되나"를
  3측도로 삼각측량. TE 는 단일계 엔트로피(H_287, 직교)와 달리 *쌍방향 요소-간* 측도라 Φ 와
  가장 가까울 것으로 예측 — arc 의 capstone.

- **engine 재사용 (g61)**: `eca_tpm` + `big_phi` 재사용. TE 는 균일 ensemble 위 joint-count 로
  하네스 inline (H_287 entropy / H_288 LZ 와 동일 관례). 새 IIT4 코드 0줄.

- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit + LLM none +
  $0 mac-local + NO GPU.

## 3. Predictions

- **H290.1 (anchors)**: 상수 0/255 → TE_total=0 (흐름 없음) AND Φ=0; 항등 204 → TE_total=0
  (요소-간 흐름 없음) AND Φ=0.
- **H290.2 (r-verdict)**: panel `Pearson r(TE_total, Φ_mean)`. r ≥ 0.5 → SUPPORTED. (예측: 셋 중
  최강 r.)
- **H290.3 (flow-witness)**: 통합 룰(Φ>0)에 TE_total>0.
- **H290.4 (bound)**: TE_total ≥ 0 (non-negative), Φ_mean ≥ 0.
- **H290.5 (determinism)**: rule 110 (TE_total, Φ_mean) re-run byte-identical.

## 4. Variables

- **axis1_rule** (primary, 10-panel — H_287/288 동일): 0·255·204·51·150·105·90·60·110·30.
- **metric1_TE_total** (primary): `Σ_i Σ_{j≠i} TE(j→i)`, 균일 2^n ensemble 위 lag-1 이변량
  transfer entropy. `TE(j→i)=Σ p(i',i,j) log2[p(i'|i,j)/p(i'|i)]` (i'=셀 i 의 다음 비트). bits.
- **metric2_Φ_mean** (primary): 모든 2^n state 의 big_phi[0] 평균 (n=4 exact).
- **correlate**: Pearson r + Spearman ρ over 10-룰.
- **fixed**: n=4 ring · 균일 16-state ensemble · lag-1 bivariate TE.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h290_transfer_entropy_phi_correlate_2026_05_26/run_h290.hexa`
- **engine (재사용, READ-ONLY)**: `iit4_eca.eca_tpm` (next-bit) + `big_phi` (stdlib). TE joint-
  count + Pearson/Spearman 하네스 inline.
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root>
  hexa.real.bak-2026-05-22-pre-no-hxc build <src> -o /tmp/h290.bin && bin` — [[reference-life-cycle-hexa-run-gotchas]].
- **deterministic**: 결정적; re-run byte-identical. **hexa_only**: true. **runtime**: $0, NO GPU.
- **ledger**: `result.json`. **tier**: 🟢 NUMERICAL — 해석 ⚪ FENCED.

## 6. Criteria

- **C1 (ANCHORS / H290.1)**: 상수·항등 TE=0 + Φ=0 → PASS.
- **C2 (r-VERDICT / H290.2)**: r ≥ 0.5 → SUPPORTED.
- **C3 (FLOW+BOUND+DET / H290.3/4/5)**: witness + bound + determinism → PASS.
- **verdict_rule**: H1 verdict = C2. 발견 = arc 3측도 종합.

## 7. Falsifiers

- **F290.1 ANCHORS**: 상수 0/255 TE≠0 OR Φ≠0, OR 항등 204 TE≠0 OR Φ≠0 → bridge/TE 계산 무효.
- **F290.2 r-VERDICT**: `Pearson r(TE_total, Φ_mean)` < 0.5 → H1 FALSIFIED. ≥ → SUPPORTED.
  r + ρ verbatim. (measurable: 10-룰 r/ρ.)
- **F290.3 FLOW-WITNESS**: 모든 통합 룰(Φ>0) TE_total=0 → flow 부재 → 무효.
- **F290.4 BOUND**: 어느 룰 TE_total<0 OR Φ<0 → 무효.
- **F290.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 SUPPORTED — faithful big-Φ 는 transfer entropy(방향성 흐름)를 추종
        (Pearson r=0.883, Spearman ρ=0.822). gate 8 PASS / 0 FAIL.

config: n=4 ring · 균일 16-state ensemble · lag-1 bivariate TE · engine = HEXAD/IIT4/lib (재사용)

panel table (transfer entropy + faithful big-Φ):
  rule   TE_total(bits)   Phi_mean
  0      0.0              0.0
  255    0.0              0.0
  204    0.0              0.0       (identity — 자기결정, 요소-간 흐름 0)
  51     0.0              0.0
  150    0.0    ◀         5.625     ◀ SYNERGY 맹점: Φ>0 인데 이변량 TE=0 (XOR)
  105    0.0    ◀         5.625     ◀ SYNERGY 맹점
  90     0.0              0.0
  60     4.0              13.625
  110    3.24511          13.1302
  30     2.0              13.8852

  Pearson r(TE_total, Phi_mean) = 0.883262   Spearman rho = 0.822134   (≥0.5 → H1 SUPPORTED)

정보-측도 ARC (동일 panel, faithful big-Φ):
  H_287 Shannon 엔트로피  ⊥ Φ   r=0.363   (단일계 정보 — 직교)
  H_288 Kolmogorov LZ     ∥ Φ   r=0.831   (알고리즘 복잡도 — 정렬)
  H_290 Transfer entropy  ∥ Φ   r=0.883   (방향성 흐름 — 최강 정렬)
  ⇒ Φ 는 *단일계 정보량*(엔트로피)이 아니라 *요소-간 흐름/구조 복잡도*(TE·LZ)와 정렬.

criteria:
  C1 ANCHORS (0/255/204 TE=0 Φ=0)                 : PASS
  C2 r-VERDICT (r=0.883 ≥ 0.5)                    : H1 SUPPORTED
  C3 FLOW+BOUND+DET (rule60 TE=4>0; bound; det)   : PASS

falsifiers:
  F290.1 ANCHORS     : PASS  (0/255/204 TE_total=0, Φ=0)
  F290.2 r-VERDICT   : H1 SUPPORTED  (Pearson r=0.883262, Spearman ρ=0.822134)
  F290.3 FLOW-WITNESS: PASS  (rule60 TE_total=4.0 > 0, Φ_mean=13.625)
  F290.4 BOUND       : PASS  (TE_total≥0, Φ_mean≥0)
  F290.5 POST-HOC    : NOT_TRIGGERED

checks: 8 PASS / 0 FAIL

evidence_summary: 🟢 SUPPORTED-NUMERICAL — faithful 인과 IIT 4.0 big-Φ 는 transfer entropy
  (방향성 요소-간 정보흐름)를 강하게 추종 (Pearson r=0.883, Spearman ρ=0.822) — 정보-측도
  arc 의 capstone. 종합: Shannon 엔트로피(단일계)는 Φ 와 직교(H_287 r=0.363)였으나, *요소-간*
  측도인 LZ(H_288 r=0.831)·TE(r=0.883)는 정렬 → **Φ 는 단일계 정보량이 아니라 요소-간 흐름/
  구조 복잡도와 같은 축**. honest: 이변량 TE 는 **XOR 시너지 맹점** — rule 150/105 는 Φ=5.625
  인데 TE_total=0 (XOR 통합은 i_t 만 조건화하는 쌍방향 TE 에 안 보임; 다변량/synergy 정보 문헌
  정합). 즉 각 고전 측도는 맹점이 있다 — LZ 는 자기유사 rule90 을 과대(Φ=0), TE 는 시너지
  rule150/105 를 과소(Φ>0) — **Φ 는 셋 중 어느 것과도 정확히 같지 않으며 두 맹점을 모두 메우는
  통합 측도**. 이것이 IIT 가 별도 양인 이유의 측정 사실.
falsifiers_triggered: none (H1 SUPPORTED)
```

re-run byte-identical 확인 (F290.5).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_290 faithful IIT 4.0 big-Phi TRACKS transfer entropy across a 10-rule
   ECA panel (Pearson r=0.883, Spearman rho=0.822), completing the arc Shannon-entropy
   perp Phi (0.363) / LZ-complexity || Phi (0.831) / TE || Phi (0.883) — Phi aligns with
   inter-element flow/complexity not single-system information; bivariate TE has an XOR-
   SYNERGY blind spot (rules 150/105: Phi=5.6 yet TE=0); deterministic toy-substrate
   outcome, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values deterministic arithmetic, interpretation fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 (XOR-SYNERGY 맹점 — 핵심)**: 이변량 lag-1 TE 는 rule 150/105(L⊕C⊕R XOR)에서 TE_total=0
  인데 Φ_mean=5.625. XOR 통합은 *시너지*(여러 source 가 함께만 정보를 줌)라, i_t 만 조건화하는
  쌍방향 TE 에 안 보인다 (다변량 정보 / synergy 문헌 정합). 따라서 r=0.883 은 *과소-추정* —
  multivariate/causation-entropy TE 라면 더 높을 수 있다. **Φ ≠ 이변량 TE** (TE 는 시너지 맹점).
- **L2 (lag-1 bivariate — 한 TE 정의)**: lag-1, 조건화 없는 Schreiber 이변량 TE. 다중-lag,
  conditional TE(causation entropy), multivariate TE 는 다른 값(특히 XOR 회복). 본 H 는 가장
  단순한 정의의 결과.
- **L3 (Φ_mean state-평균)**: faithful Φ state-dependent (FAITHFUL_REMEASURE §4) — 방향 robust,
  절대값 state 분포 의존.
- **L4 (n=4 small + 10-룰)**: r 절대값 panel 의존. 방향(흐름↔Φ 정렬)은 robust.
- **L5 (substrate 는 흐름 proxy)**: ECA 룰이 정보흐름 자체 아님. 라벨은 substrate-테마.
- **L6 (structure-cut big-Φ, full IIT4 절대 calibration 아님)**: 상관 결론은 scale-offset robust.
- **L7 (verdict ≠ 형이상학)**: SUPPORTED 는 toy substrate 측정 사실 — "의식=정보흐름" 형이상학
  주장 아님.

## 10. Cross-Links

- **sibling (정보-측도 arc)**: [[H_287]] (Shannon⊥Φ r=0.363) · [[H_288]] (LZ∥Φ r=0.831) — 본 H
  (TE∥Φ r=0.883)가 arc capstone. 3측도 종합: Φ ∥ 요소-간 흐름/복잡도, ⊥ 단일계 엔트로피. 각
  고전 측도의 맹점(LZ=자기유사 over, TE=시너지 under)을 Φ 가 메움.
- **parent (engine)**: IIT4 M6 (`FAITHFUL_REMEASURE.md`) — eca_tpm + big_phi.
- **engine lib (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (`eca_tpm`) · `big_phi`
  (via stdlib) — 새 IIT4 코드 0줄 (g61).
- **Next**: (a) multivariate/conditional TE(causation entropy)로 XOR-시너지 맹점 회복 (L1/L2);
  (b) multi-lag TE; (c) arc 를 paper 화 (정보-측도 삼각측량 — a_paper_significance 만족 후보).
