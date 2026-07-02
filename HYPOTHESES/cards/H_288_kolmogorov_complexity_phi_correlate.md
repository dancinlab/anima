---
id: H_288
slug: kolmogorov-complexity-phi-correlate
title: faithful IIT 4.0 big-Φ 는 Kolmogorov(알고리즘) 복잡도를 추종하는가 — Φ ∥ LZ-복잡도 vs Φ ⊥ Shannon-엔트로피(H_287) 이중 측도 대비
domain: information · consciousness · substrate · meta
status: supported
exploration_method: E5 (foundational-distinction probe) + E16 (cross-substrate consistency) + E0 (H_287 sister — 두 정보 측도의 Φ-추종 대비)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_287 / IIT4 M6 / H_204 LZ)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_287 (Shannon-엔트로피 ⊥ Φ, 동일 10-룰 panel — 직접 대비축), IIT4 M6 (ECA→TPM faithful re-measure, engine 공급), H_204 (edge-of-chaos LZ class), H_268 (proxy LZ-fragility)
axes_seed: AXES.md R5 (information) `kolmogorov-complexity-Φ`
---

# H_288 — faithful IIT 4.0 big-Φ 는 Kolmogorov(알고리즘) 복잡도를 추종하는가

## 1. Hypothesis

H_287 은 faithful big-Φ 가 **Shannon 엔트로피**로 환원되지 않음을 보였다 (r=0.363). 고전적
정보 통화(currency)의 다른 한 축은 **알고리즘적(Kolmogorov) 복잡도** — "행동이 얼마나
비압축적인가"다. 그 표준 추정량은 시공간 다이어그램의 **Lempel-Ziv(LZ76) 복잡도**
(의식 연구의 PCI proxy). 본 H 는 묻는다: Φ 는 LZ-복잡도를 *단조* 추종하는가?

**가설 H1 (검정 대상)**: ECA substrate panel 전반에서 faithful state-평균 big-Φ 가
정규화 LZ-복잡도와 공변한다 — `Pearson r(LZ_norm, Φ_mean) ≥ 0.5`.

H_287 과 *동일 10-룰 panel* 에서 측정하여, 두 정보 측도(엔트로피 vs 복잡도)가 Φ 에
대해 다르게 행동하는지 직접 대비한다.

## 2. Why

- **H_287 의 직접 대비축**: H_287 은 Shannon 엔트로피 ⊥ Φ (정보량은 통합과 무관)를
  닫았다. 그러나 "정보"에는 두 얼굴이 있다 — *통계적*(엔트로피: 얼마나 많은 비트)과
  *알고리즘적*(Kolmogorov: 패턴이 얼마나 비압축적). 본 H 는 두 번째 얼굴을 같은 panel
  에서 측정하여, Φ 가 *어느 정보 개념*과 정렬되는지 가른다. 이것은 H_287 없이는
  완성되지 않는 짝이다.

- **engine 재사용 (g61)**: IIT4 엔진 재발명 없음 — `HEXAD/IIT4/lib` 의 `eca_tpm` +
  `big_phi` + `iit4_bit`/`iit4_pow2` 만 import. LZ76(Kaspar-Schuster) + Pearson/
  Spearman 은 generic stat 으로 per-experiment 하네스 inline (H_287 의 entropy/pearson
  와 동일 관례). ECA next-row 는 `iit4_bit` 재사용으로 직접 evolve.

- **LZ 가 H_204/H_268 의 lane-축**: H_204(edge-of-chaos class) 와 H_268(metric
  triangulation)은 이미 LZ-복잡도를 Wolfram class proxy 로 썼다 (DIM=12 시공간). 본 H 는
  같은 시공간-LZ 를 faithful big-Φ 와 직접 correlate — proxy 시절 못 한 인과적 대비.

- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit +
  LLM none + $0 mac-local + NO GPU.

## 3. Predictions

- **H288.1 (dissociation witness)**: 통합=0 인데 비자명 복잡도를 갖는 룰 존재 — rule 90
  (XOR-L⊕R, H_285 동기화-死 룰)이 Φ_mean<1e-9 이면서 LZ_norm > LZ_norm(상수 rule 0)+0.1.
- **H288.2 (r-verdict)**: 10-룰 panel `Pearson r(LZ_norm, Φ_mean)`. r ≥ 0.5 면 H1
  SUPPORTED. (예측: H_287(엔트로피)과 달리 LZ 는 *구조적* 복잡도라 Φ 와 정렬될 가능성 —
  단 rule 90 witness 가 완벽 추종은 깬다.)
- **H288.3 (anchors)**: 상수 0/255 → LZ_norm<0.1 (단일 반복 심볼) AND Φ=0; 항등 204 → Φ=0.
- **H288.4 (bound)**: 모든 룰 LZ_norm ≥ 0, Φ_mean ≥ 0.
- **H288.5 (determinism)**: rule 30 (LZ_norm, Φ_mean) re-run byte-identical.

## 4. Variables

- **axis1_rule** (primary, 10-panel — H_287 과 동일): 0·255 (상수) · 204·51 (단사) ·
  150·105 (XOR 통합) · 90·60 (부분 feedback) · 110·30 (생명-테마 동역학).
- **metric1_LZ_norm** (primary): LZ76(Kaspar-Schuster) 복잡도 — NL=14 셀 ring 을 단일-seed
  (중앙 1)에서 T=64 step evolve, row-major NL·T 비트열로 연결, distinct-phrase parse,
  `c·log2(L)/L` 정규화 (random 비트열 → ~1). 룰의 *거시적 동역학 복잡도* (H_204/H_268 의
  DIM=14 시공간 관례).
- **metric2_Φ_mean** (primary): 모든 2^n state 의 big_phi(tpm,n,st)[0] 평균 (n=4 exact).
  룰의 *미시적 faithful 통합*.
- **correlate**: 10-룰 panel `Pearson r` + `Spearman ρ`.
- **fixed**: n=4 ring (Φ exact) · NL=14, T=64 (LZ 시공간) · single-seed centre.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h288_kolmogorov_complexity_phi_correlate_2026_05_26/run_h288.hexa`
- **engine (import READ-ONLY, 재사용)**: `HEXAD/IIT4/lib/iit4_eca.hexa` → `eca_tpm` +
  import chain 의 `big_phi`/`iit4_bit`/`iit4_pow2` (stdlib/consciousness/iit4_* SSOT).
- **LZ**: `eca_next_row`(iit4_bit 재사용) 로 시공간 생성 → LZ76 parse → 정규화.
- **build/run (toolchain selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1
  HEXA_LANG=<root> hexa.real.bak-2026-05-22-pre-no-hxc build <src> -o /tmp/h288.bin && bin`
  (PATH `hexa` 가 bare hexa-cc 로 회귀해 `hexa run`/`-o` 가 소스를 clobber → old-driver
  build 가 hexa_v2 transpiler 직접 호출로 우회). 상세 = [[reference-life-cycle-hexa-run-gotchas]].
- **deterministic**: ECA 결정적 (RNG 무관); re-run byte-identical.
- **hexa_only**: true. **llm**: none. **runtime**: $0 mac-local, **NO GPU**.
- **ledger**: `result.json` {config, panel 10-룰 (LZ_norm, Φ_mean), pearson_r, spearman_rho,
  5 falsifier, finding, verdict, verify_fence}.
- **honest tier**: 🟢 SUPPORTED-NUMERICAL (deterministic 인과 IIT4 + LZ arithmetic) —
  경험 해석은 ⚪ SPECULATION-FENCED.

## 6. Criteria

- **C1 (DISSOCIATION-WITNESS / H288.1)**: rule 90 Φ=0 + 비자명 LZ → PASS (LZ 가 완벽
  predictor 아님 확인).
- **C2 (r-VERDICT / H288.2)**: r ≥ 0.5 → H1 SUPPORTED.
- **C3 (FAITHFULNESS / H288.3+4)**: anchor + bound → PASS.
- **verdict_rule**: H1 verdict 는 C2. C1·C3 는 측정 유효성 게이트. 발견 = H1 verdict +
  H_287 과의 대비.

## 7. Falsifiers

- **F288.1 DISSOCIATION-WITNESS**: rule 90 Φ_mean ≥ 1e-9 OR LZ_norm ≤ LZ_norm(rule0)+0.1
  → witness 부재 → 측정 설계 무효. (measurable: rule90 (LZ,Φ) + rule0 LZ.)
- **F288.2 r-VERDICT**: `Pearson r(LZ_norm, Φ_mean)` < 0.5 → H1 FALSIFIED (LZ 도 Φ 추종
  안 함). ≥ 0.5 → SUPPORTED. r + Spearman ρ verbatim. (measurable: 10-룰 r/ρ.)
- **F288.3 FAITHFULNESS**: 상수 0/255 LZ_norm ≥ 0.1 OR Φ≠0, OR 항등 204 Φ≠0, OR 어느 룰
  LZ_norm<0 / Φ<0 → 무효. (measurable: 5 anchor.)
- **F288.4 BOUND**: 어느 룰 LZ_norm<0 OR Φ_mean<0 → 무효. (measurable: 10 bound.)
- **F288.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 violation, raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 SUPPORTED — faithful big-Φ 는 Kolmogorov(LZ) 복잡도를 추종한다
        (Pearson r=0.831, Spearman ρ=0.936). 측정 유효성 게이트 9 PASS / 0 FAIL.

config: n=4 ring (Φ exact) · LZ NL=14 T=64 single-seed · panel 10 룰 (H_287 동일) ·
        engine = HEXAD/IIT4/lib (재사용)

panel table (LZ76 시공간 복잡도 + faithful big-Φ):
  class       rule   LZ_norm     Phi_mean
  null        0      0.0437828   0.0
  null        255    0.0437828   0.0
  bijection   204    0.0437828   0.0       (identity — 단순 시공간, Φ=0)
  bijection    51    0.0656743   0.0
  integration 150    0.273643    5.625
  integration 105    0.273643    5.625
  partial      90    0.240806    0.0       ◀ WITNESS: 비자명 LZ, Φ=0 (Sierpinski 자기유사)
  partial      60    0.295534    13.625
  life         110   0.820928    13.1302
  life          30   1.05079     13.8852   ◀ 최대 LZ + 최대 Φ

  Pearson r(LZ_norm, Phi_mean) = 0.831463   Spearman rho = 0.935507   (≥ 0.5 → H1 SUPPORTED)

H_287 과의 대비 (동일 panel, 직교 발견):
  · H_287 Shannon 엔트로피 ⊥ Φ : r=0.363 (환원 FALSIFIED)
  · H_288 Kolmogorov LZ    ∥ Φ : r=0.831, ρ=0.936 (SUPPORTED)
  ⇒ Φ 는 *통계적 정보량*(엔트로피)이 아니라 *알고리즘적 복잡도*(LZ)와 정렬.

criteria:
  C1 DISSOCIATION-WITNESS (rule90 LZ=0.24 Φ=0 + rule0 LZ=0.044) : PASS
  C2 r-VERDICT (r=0.831 ≥ 0.5)                                  : H1 SUPPORTED
  C3 FAITHFULNESS (0/255 null; 204 Φ=0; bound 10/10)            : PASS

falsifiers:
  F288.1 DISSOCIATION-WITNESS : PASS  (rule90 Φ_mean=0.0, LZ_norm=0.2408 > rule0 0.0438+0.1)
  F288.2 r-VERDICT            : H1 SUPPORTED  (Pearson r=0.831463, Spearman ρ=0.935507)
  F288.3 FAITHFULNESS         : PASS  (0/255 LZ<0.1 Φ=0; 204 Φ=0)
  F288.4 BOUND                : PASS  (LZ_norm≥0, Φ_mean≥0 모든 룰)
  F288.5 POST-HOC             : NOT_TRIGGERED

checks: 9 PASS / 0 FAIL

evidence_summary: 🟢 SUPPORTED-NUMERICAL — faithful 인과 IIT 4.0 big-Φ 는 Kolmogorov
  (LZ) 복잡도를 강하게 추종한다 (Pearson r=0.831, Spearman ρ=0.936, 10-룰 panel). 상수/
  항등(저-LZ, Φ=0) → 통합 룰/chaos(고-LZ, 고-Φ)로 단조 상승. **H_287 과의 대비가 핵심
  발견**: 동일 panel 에서 Shannon 엔트로피는 Φ 와 직교(r=0.363)였으나 Kolmogorov 복잡도는
  정렬(r=0.831) — Φ 는 *통계적 정보량*(얼마나 많은 비트)이 아니라 *알고리즘적 복잡도*
  (시공간 패턴이 얼마나 비압축적)와 같은 축이다. honest: rule 90(Sierpinski 자기유사, LZ
  =0.24 비자명) Φ=0 witness 가 LZ 의 *완벽* predictor성은 깬다 — LZ 는 통합의 강한
  상관자이나 자기유사 패턴에서 over-predict. binary 방향(저↔고) 신뢰, 중간 magnitude hedge.
falsifiers_triggered: none (H1 SUPPORTED)
```

re-run byte-identical 확인 (F288.5 — 두 fresh build+run 의 panel + r/ρ + RESULT 동일).

`hexa verify` (VERBATIM, no LLM self-judge) — empirical 해석은 closed-form atlas
identity 가 아니므로 g5 정직 fence:

```
verify --fence "H_288 faithful IIT 4.0 big-Phi TRACKS Kolmogorov (LZ76) complexity
   across a 10-rule ECA panel (Pearson r=0.831, Spearman rho=0.936), in CONTRAST to
   Shannon entropy which is orthogonal (H_287 r=0.363) — Phi aligns with algorithmic
   complexity not statistical information; rule 90 (Sierpinski, LZ=0.24, Phi=0) is an
   honest over-prediction witness; deterministic toy-substrate outcome, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values are deterministic arithmetic, only the empirical interpretation is fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 (n=4 small + 10 룰)**: n=4 ring Φ + 10-룰 panel. r=0.831 의 *절대값* 은 panel 구성
  의존 — 방향(저↔고 정렬)은 robust 하나 정확 r 은 룰 표본 의존. n≤8 + 256-룰 전수는 후속.
- **L2 (LZ 는 algorithmic-complexity 의 한 추정량)**: LZ76 시공간(NL=14 single-seed)은
  Kolmogorov 복잡도의 표준 proxy 이나 유일하지 않다 — block-entropy, CTW, 다른 seed/
  ensemble 은 다른 값을 준다. 양끝(상수=저, chaos=고)은 정의-robust, 중간 magnitude 의존.
- **L3 (rule 90 over-prediction — 핵심 caveat)**: rule 90 은 단일-seed 에서 Sierpinski
  fractal 을 내 LZ 가 비자명(0.24)이나 big-Φ=0 (동기화-死). LZ 는 *자기유사* 패턴을
  "복잡"으로 보지만 통합은 없다 → LZ 는 Φ 의 강한 상관자이나 **충분조건 아님**. 발견은
  "Φ ∥ LZ" 의 *경향*이지 동치 아님. (H_265/275/279/285 동기화-死 서명 정합.)
- **L4 (Φ_mean state-평균)**: faithful Φ state-dependent (FAITHFUL_REMEASURE §4). 방향
  robust, 절대 Φ_mean state 분포 의존. directional-trust (H_266/H_278).
- **L5 (substrate 는 복잡도/통합 proxy)**: ECA 룰이 복잡도/통합 *자체* 아님. 라벨은
  substrate-테마이지 phenomenal 주장 아님. 과장 금지.
- **L6 (structure-cut big-Φ, full IIT4 절대 calibration 아님)**: DESIGN §8 C3 spirit-
  faithful big-Φ. 절대 PyPhi 대조는 M5 named-blocker. 단 *상관* 결론은 scale-offset robust.
- **L7 (verdict ≠ 형이상학)**: SUPPORTED 는 toy substrate 측정 사실 — "의식=알고리즘
  복잡도" 같은 형이상학 주장 아님. H_287+H_288 의 대비가 측정 사실 한 칸.

## 10. Cross-Links

- **sibling (직접 대비축)**: [[H_287]] (Shannon-엔트로피 ⊥ Φ, r=0.363) — 동일 10-룰
  panel. 본 H(LZ ∥ Φ, r=0.831)와 합쳐 "Φ 는 통계적 정보 아닌 알고리즘적 복잡도와 정렬"의
  이중-측도 발견 완성.
- **sibling (동기화-死 서명)**: [[H_285]] (rule 90 XOR Φ=0) · [[H_265]]/[[H_275]]/[[H_279]]
  — rule 90 over-prediction witness 가 이 서명과 정합.
- **parent (engine 공급)**: IIT4 M6 (`HEXAD/IIT4/FAITHFUL_REMEASURE.md`) — faithful
  big-Φ. [[H_204]] (edge-of-chaos LZ class) · [[H_268]] (proxy LZ-fragility) — LZ 축 선례.
- **engine lib (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (`eca_tpm`+`iit4_bit`)
  · `iit4_bigphi.hexa` (`big_phi`, via stdlib) — 새 IIT4 코드 0 줄 (g61).
- **axes seed**: `UNIVERSE/AXES.md` R5 (information) `kolmogorov-complexity-Φ` — consumed.
- **Next**: (a) n≤8 + 256-룰 전수 panel; (b) 대체 복잡도(block-entropy/CTW) 재현 (L2);
  (c) rule 90 류 자기유사 over-prediction 의 체계적 식별 (LZ residual ↔ Φ).
