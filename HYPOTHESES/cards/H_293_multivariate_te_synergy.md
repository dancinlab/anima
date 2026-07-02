---
id: H_293
slug: multivariate-te-synergy
title: multivariate(conditional) transfer entropy 가 XOR 시너지를 회복하나 Φ-추종은 악화 — 어떤 차수의 고전 TE 도 Φ 와 같지 않음 (H_290/논문 follow-up)
domain: information · consciousness · substrate · meta
status: partial
exploration_method: E5 (measure-order probe) + E0 (논문 §future 예측 검정) + E16 (bivariate vs multivariate 대비)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_290 / paper)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_290 (bivariate TE ∥ Φ, XOR blind spot), H_287/288 (정보-측도 arc), PAPER/phi-information-triangulation (§future 예측원)
---

# H_293 — multivariate(conditional) TE 가 XOR 시너지를 회복하나 Φ-추종은 악화

## 1. Hypothesis

논문(H_287-290)은 **이변량** transfer entropy 가 시너지 XOR coupling 에 맹점임을 보였다 —
rule 150/105 는 big-Φ=5.6 인데 TE_total=0 (쌍방향 TE 는 target 자기 present 만 조건화).
논문 §future 는 **multivariate/conditional TE** 가 그 룰들을 회복하고 "상관을 0.88 위로
끌어올릴 것"으로 예측했다. 검정한다: 회복되는가? 회복되면 Φ 를 이변량(r=0.883)보다 잘
추종하는가, 아니면 새 over-prediction 으로 Φ 가 여전히 별개인가?

**가설 H1 (2-clause)**: (a) SYNERGY-RECOVERED — XOR 룰 150/105 의 multivariate
TEm_total > 0 (이변량 0 에서 회복), 항등 204 는 0 유지. (b) r-IMPROVEMENT —
`Pearson r(TEm_total, Φ_mean) ≥ 0.883`. 둘 다면 FULL, (a)만이면 PARTIAL (시너지는
회복되나 새 맹점으로 Φ 여전히 별개).

## 2. Why

- **논문 §future 예측의 직접 검정**: 논문이 사전등록한 "multivariate TE 가 r>0.88 로
  상승" 예측을 측정으로 확인/정밀화. arc 의 자연스러운 후속.
- **measure-order 축**: 이변량(H_290)은 시너지 *과소*. 다변량은 시너지를 회복하나 비통합
  흐름을 *과대* 할 수 있다. "어떤 차수의 고전 TE 가 Φ 와 같은가?"를 가른다.
- **engine 재사용 (g61)**: `eca_tpm`+`big_phi`+`iit4_bit` (HEXAD/IIT4/lib). TEm = H(next_i|self_i)
  joint-count inline. 새 IIT4 코드 0줄.
- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit + LLM none + $0.

## 3. Predictions

- **H293.1 (synergy-recovered)**: TEm(150)>0 AND TEm(105)>0 AND TEm(204)<1e-9.
- **H293.2 (r-verdict)**: `Pearson r(TEm, Φ_mean)`. clause(b) ⇔ r≥0.883.
- **H293.3 (anchors)**: 상수 0/255, 항등 204, complement 51 → TEm=0 (출력 자기-결정).
- **H293.4 (bound)**: 0 ≤ TEm ≤ n, Φ_mean ≥ 0.
- **H293.5 (determinism)**: rule 150 (TEm, Φ_mean) re-run byte-identical.

## 4. Variables

- **axis1_TE_order** (primary): bivariate(H_290 reference) vs **multivariate conditional**
  TEm_i = H(next_i | self_i) (deterministic ⇒ = I(other-inputs; next_i | self_i)).
- **metric_TEm_total** = Σ_i H(next_i | b_i) (bits), 균일 2^n ensemble.
- **metric_Φ_mean** = state-평균 big_phi (n=4 exact).
- **correlate**: Pearson r + Spearman ρ, vs 이변량 r=0.883.
- **panel**: H_287-290 동일 10 룰.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h293_multivariate_te_synergy_2026_05_26/run_h293.hexa`
- **engine (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` → `eca_tpm`/`big_phi`/
  `iit4_bit`/`iit4_pow2` (stdlib/consciousness SSOT). TEm = H(next|self) joint-count inline.
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root>
  hexa.real.bak-2026-05-22-pre-no-hxc build <src> -o /tmp/h293.bin && bin` — [[reference-life-cycle-hexa-run-gotchas]].
- **deterministic**: re-run byte-identical. **hexa_only**: true. **runtime**: $0, NO GPU.
- **tier**: 🟡 PARTIAL.

## 6. Criteria

- **C1 (RECOVER / H293.1)**: XOR 룰 TEm>0 + 항등 0 → PASS (시너지 회복).
- **C2 (r-IMPROVE / H293.2)**: r≥0.883 → clause(b); else PARTIAL.
- **C3 (ANCHOR+BOUND+DET)**: → PASS.
- **verdict_rule**: C1 PASS + C2 미달 → PARTIAL (시너지 회복하나 Φ 별개).

## 7. Falsifiers

- **F293.1 SYNERGY-RECOVERED**: TEm(150) ≤ 0 OR TEm(105) ≤ 0 OR TEm(204) ≥ 1e-9 → 회복 실패.
- **F293.2 r-VERDICT**: `Pearson r(TEm, Φ)` < 0.883 → clause(b) 미달 (시너지 회복 ≠ Φ-추종 개선).
  ≥ → clause(b). r+ρ verbatim.
- **F293.3 ANCHORS**: 상수/항등/complement TEm≠0 → 계산 무효.
- **F293.4 BOUND**: TEm∉[0,n] OR Φ<0 → 무효.
- **F293.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 PARTIAL — multivariate TE 가 XOR 시너지를 회복(clause a) 하나 Φ-추종은
        악화(clause b 미달, r 0.883→0.705). gate 8 PASS / 0 FAIL.

config: n=4 · TEm_i=H(next_i|self_i) 균일 ensemble · 10-룰 panel (H_287-290 동일) · engine 재사용

table (multivariate TEm vs bivariate TE vs Φ):
  rule   bivariate TE   multivariate TEm   Phi_mean
  0      0.0            0.0                0.0
  255    0.0            0.0                0.0
  204    0.0            0.0                0.0
  51     0.0            0.0                0.0
  150    0.0    ◀        4.0    ◀회복       5.625
  105    0.0    ◀        4.0    ◀회복       5.625
  90     0.0            4.0    ◀과잉        0.0     ← 흐름有 통합無, TEm over-predict
  60     4.0            4.0                13.625
  110    3.245          3.62256            13.1302
  30     2.0            4.0                13.8852

  bivariate r(TE, Phi) = 0.883  →  multivariate r(TEm, Phi) = 0.705412 (ρ=0.681358)  ↓ 악화

criteria:
  C1 RECOVER (150/105 TEm 0→4; 204 TEm=0)         : PASS (시너지 회복)
  C2 r-IMPROVE (r=0.705 < 0.883)                  : 미달 → PARTIAL
  C3 ANCHOR+BOUND+DET                              : PASS

falsifiers:
  F293.1 SYNERGY-RECOVERED : PASS  (rule150/105 TEm=4.0>0, rule204 TEm=0.0)
  F293.2 r-VERDICT         : clause(b) 미달  (r=0.705412 < 0.883 — 회복이 Φ-추종 개선 안 함)
  F293.3 ANCHORS           : PASS  (0/255/204/51 TEm=0)
  F293.4 BOUND             : PASS
  F293.5 POST-HOC          : NOT_TRIGGERED

checks: 8 PASS / 0 FAIL

evidence_summary: 🟡 PARTIAL — multivariate(conditional) transfer entropy 는 이변량 TE 의
  XOR 시너지 맹점을 **회복**한다 (rule 150/105: 이변량 0 → TEm=4.0, 항등 204 는 0 유지). 그러나
  Φ-추종은 **개선되지 않고 악화**됐다 (r 0.883→0.705, ρ→0.681). 원인은 새로운 over-prediction:
  rule 90 은 이웃에서 흐름을 받지만(TEm=4.0) 시스템이 reducible 이라 Φ=0 — 다변량 TE 가 *비통합
  흐름*을 과대평가. **즉 어떤 차수의 고전 transfer entropy 도 Φ 와 같지 않다**: 이변량은 시너지를
  과소(150/105), 다변량은 비통합 흐름을 과대(90). 이는 논문(H_287-290)의 thesis — Φ 는 요소-간
  흐름의 한 고정-차수 통계가 아니라 통합의 별개 측도 — 를 강화하고, 논문 §future 의 "multivariate
  TE 가 r>0.88 로 상승" 예측을 정밀 반증(회복 ✓, 상승 ✗). LZ over-prediction(rule90, H_288)과
  동일 룰에서 동일 실패 = "흐름·복잡도 있으나 통합 없음"의 cross-measure 서명.
falsifiers_triggered: F293.2 clause(b) (의도된 측정 — Φ 별개성의 강화 증거)
```

re-run byte-identical 확인 (F293.5).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_293 multivariate (conditional) transfer entropy recovers the XOR synergy
   blind spot of bivariate TE (rules 150/105: bivariate TE=0 -> multivariate TEm=4.0) but
   does NOT improve Phi-tracking (r 0.883 -> 0.705): it over-predicts on rule 90 (flow without
   integration, Phi=0). No order of classical transfer entropy equals Phi — bivariate
   under-counts synergy, multivariate over-counts non-integrated flow; deterministic
   toy-substrate, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values deterministic arithmetic, interpretation fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 (TEm 정의의 한 선택)**: TEm_i = H(next_i|self_i) 는 deterministic 기질에서 multivariate
  conditional TE 의 한 형태(자기-present 만 조건화, 나머지 입력 통째). 시간-lag, 부분조건화
  (각 source 별 CTE), partial-information-decomposition 의 synergy 항 분리는 다른 분해를 줄 수
  있다. 본 H 는 가장 단순한 "all-other-inputs given self" 형.
- **L2 (rule 90 over-prediction — 핵심)**: TEm 이 rule 90 을 4.0 으로 과대(Φ=0). LZ(H_288)도 동일
  룰 과대 → "비통합 흐름/복잡도" cross-measure 서명. multivariate TE 가 통합이 아닌 *flow 존재*를
  잰다는 직접 증거.
- **L3 (Φ_mean state-평균)**: directional-trust; 절대 magnitude state 의존.
- **L4 (n=4 small + 10 룰)**: r 절대값 panel 의존; 방향(회복 ✓ / 개선 ✗) robust.
- **L5 (substrate proxy)**: ECA = flow/integration proxy, phenomenal 주장 아님.
- **L6 (structure-cut big-Φ)**: 상관 결론은 scale-offset robust.
- **L7 (verdict ≠ 형이상학)**: PARTIAL 은 toy 측정 사실. "의식=정보흐름" 아님.

## 10. Cross-Links

- **parent (예측원)**: PAPER/phi-information-triangulation §future — "multivariate TE 가 시너지
  회복 + r>0.88 상승" 예측. 본 H 가 검정: 회복 ✓, 상승 ✗ (정밀 반증). thesis 강화.
- **sibling**: [[H_290]] (bivariate TE ∥ Φ, XOR blind spot — 본 H 의 출발점) · [[H_288]] (LZ
  over-prediction rule90 — TEm 과 동일 룰 동일 실패) · [[H_287]] (Shannon ⊥ Φ).
- **engine lib (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (`eca_tpm`/`big_phi`/
  `iit4_bit`/`iit4_pow2`, via stdlib) — 새 IIT4 코드 0줄 (g61).
- **Next**: (a) partial-information-decomposition 으로 synergy/redundancy/unique 항 분리 후 각각
  vs Φ; (b) 각 source 별 conditional TE (rule90 이 어느 항에서 과대인지); (c) 큰 N 에서 TE-차수
  ↔ Φ 갭의 scale 거동.
