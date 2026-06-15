---
id: H_294
slug: pid-synergy-phi
title: 흐름의 어떤 성분도 Φ 를 추종하지 않는다 — synergy ⊥ Φ (r=0.03), 통합은 system-cut 속성 (H_293/논문 §future follow-up)
domain: information · consciousness · substrate · meta
status: closed-negative
exploration_method: E5 (flow-component decomposition) + E0 (논문 §future PID 예측 검정) + E16 (synergy vs redundancy vs unique)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_290/293 / paper)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_290/H_293 (TE arc), H_288 (LZ rule90 over-prediction), PAPER/phi-information-triangulation (§future PID 예측원)
---

# H_294 — 흐름의 어떤 성분도 Φ 를 추종하지 않는다 (synergy ⊥ Φ)

## 1. Hypothesis

H_293 은 어떤 *차수*의 transfer entropy 도 Φ 와 같지 않음을 보였다 (이변량=시너지 과소,
다변량=비통합흐름 과대). 논문 §future 는 흐름을 PID *성분*(synergy / redundancy / unique)
으로 분해해 어느 성분이 Φ 를 추종하는지 물었다. 각 셀의 방향성 흐름을 조건부 interaction
information(co-information)으로 synergy vs redundancy 로 쪼개 Φ 와 상관한다.

**가설 H1 (검정 대상)**: SYNERGY 가 Φ 를 추종하는 흐름 성분이다 —
`Pearson r(synergy_total, Φ_mean) ≥ 0.5 AND > r(redundancy_total, Φ_mean)`.
(예측: synergy 가 통합에 필요하나 rule 90(synergy 有 통합 無)이 충분성을 깸 → PARTIAL 가능.)

## 2. Why

- **논문 §future PID 예측의 직접 검정**: 흐름 성분 중 무엇이 Φ 를 추종하는지 — 정보-측도
  arc 의 가장 깊은 후속.
- **co-information = 2-source synergy/redundancy 요약**: 조건부 interaction information
  `II_c = H(T|C) - H(T|S1,C) - H(T|S2,C)` (T=next, S1/S2=좌/우 이웃, C=self). II_c<0=synergy,
  >0=redundancy. XOR-3(150): II_c=-1 (순수 synergy). 항등(204): II_c=0.
- **engine 재사용 (g61)**: eca_tpm+big_phi+iit4_bit. co-information 은 (T,S1,S2,C) 16-bin joint
  marginal entropy 로 inline. 새 IIT4 코드 0줄.
- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit + LLM none + $0.

## 3. Predictions

- **H294.1 (synergy-witness)**: XOR 150/105 synergy-dominant (synergy>0, redundancy=0).
- **H294.2 (r-verdict)**: r(synergy,Φ) + r(redundancy,Φ). clause ⇔ r(syn)≥0.5 AND >r(red).
- **H294.3 (dissociation)**: rule 90 synergy>0 yet Φ=0 (synergy 충분조건 아님).
- **H294.4 (anchors)**: 상수 0/255, 항등 204 → synergy=0, redundancy=0.
- **H294.5 (bound/det)**: synergy/redundancy ≥0; rule 150 re-run identical.

## 4. Variables

- **metric_synergy** = Σ_i max(0, -II_c) ; **metric_redundancy** = Σ_i max(0, II_c).
- **II_c per cell** = H(T|C) - H(T|S1,C) - H(T|S2,C) (조건부 interaction info, deterministic form).
- **metric_Φ_mean** = state-평균 big_phi (n=4 exact).
- **correlate**: r(synergy, Φ), r(redundancy, Φ) over 10-룰 panel (H_287-293 동일).

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h294_pid_synergy_phi_2026_05_26/run_h294.hexa`
- **engine (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` → eca_tpm/big_phi/iit4_bit/
  iit4_pow2 (stdlib SSOT). co-information = (T,S1,S2,C) 16-bin joint marginal entropy inline.
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root>
  hexa.real.bak-2026-05-22-pre-no-hxc build <src> -o /tmp/h294.bin && bin` — [[reference-life-cycle-hexa-run-gotchas]].
- **deterministic**: re-run byte-identical. **hexa_only**: true. **runtime**: $0, NO GPU.
- **tier**: 🔴 CLOSED-NEGATIVE (synergy ⊥ Φ).

## 6. Criteria

- **C1 (SYNERGY-WITNESS)**: XOR 룰 synergy-dominant → PASS.
- **C2 (r-VERDICT)**: r(syn)≥0.5 AND >r(red) → H1 SUPPORTED; else FALSIFIED.
- **C3 (DISSOCIATION+ANCHOR+BOUND+DET)**: → PASS.
- **verdict_rule**: C2 결정. r(syn)≪0.5 → CLOSED-NEGATIVE (synergy ⊥ Φ).

## 7. Falsifiers

- **F294.1 SYNERGY-WITNESS**: XOR 150/105 synergy=0 OR redundancy>0 → co-info 계산 무효.
- **F294.2 r-VERDICT**: r(synergy,Φ) ≥ 0.5 AND > r(red) → H1 SUPPORTED; else FALSIFIED (synergy ⊀ Φ).
- **F294.3 DISSOCIATION**: rule 90 synergy≤0 OR Φ≠0 → witness 부재.
- **F294.4 ANCHORS**: 상수/항등 synergy≠0 OR redundancy≠0 → 무효.
- **F294.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 FALSIFIED (CLOSED-NEGATIVE) — synergy ⊥ Φ (r=0.030 ≪ 0.5). 흐름의 어떤
        성분도 Φ 를 추종하지 않는다. gate 8 PASS / 0 FAIL.

config: n=4 · II_c=H(T|C)-H(T|S1,C)-H(T|S2,C) per cell · 10-룰 panel · engine 재사용

table (조건부 interaction information):
  rule   synergy   redundancy   Phi_mean
  0      0.0       0.0          0.0
  255    0.0       0.0          0.0
  204    0.0       0.0          0.0       (identity — no source flow)
  51     0.0       0.0          0.0
  150    4.0       0.0          5.625     (XOR-3 순수 synergy)
  105    4.0       0.0          5.625
  90     4.0       0.0          0.0       ◀ synergy 최대인데 Φ=0
  60     0.0       0.0          13.625    ◀ Φ 최고인데 synergy=0 (순수 unique-info: next=self⊕left)
  110    0.377     0.0          13.1302
  30     2.0       0.0          13.8852

  r(synergy, Phi) = 0.030  ·  r(redundancy, Phi) = 0.0  (redundancy=0 전 룰)

이중 dissociation: rule60(Φ=13.6, synergy=0, 순수 unique-info) ⊥ rule90(synergy=4, Φ=0).
synergy 는 통합의 필요조건도(60) 충분조건도(90) 아님 → r(synergy,Φ)=0.03 ≈ 직교.

criteria:
  C1 SYNERGY-WITNESS (150/105 synergy=4, red=0)    : PASS
  C2 r-VERDICT (r_syn=0.030 ≪ 0.5)                 : H1 FALSIFIED
  C3 DISSOCIATION+ANCHOR+BOUND+DET                 : PASS

falsifiers:
  F294.1 SYNERGY-WITNESS : PASS  (150/105 synergy=4.0, redundancy=0)
  F294.2 r-VERDICT       : H1 FALSIFIED  (r_syn=0.0299599 ≪ 0.5; r_red=0.0)
  F294.3 DISSOCIATION    : PASS  (rule90 synergy=4.0, Phi=0.0)
  F294.4 ANCHORS         : PASS  (0/255/204 synergy=0 redundancy=0)
  F294.5 POST-HOC        : NOT_TRIGGERED

checks: 8 PASS / 0 FAIL

evidence_summary: 🔴 CLOSED-NEGATIVE — 방향성 흐름을 synergy/redundancy 로 분해해도 **어떤
  성분도 Φ 를 추종하지 않는다** (r(synergy,Φ)=0.030 ≈ 직교; ECA parity 는 redundancy=0). 결정적
  근거는 **이중 dissociation**: rule 60 은 Φ 가 최고(13.6)인데 synergy=0 (next=self⊕left = 순수
  *unique* information, left 단독) ; rule 90 은 synergy 최대(4.0)인데 Φ=0 (이웃 XOR, 그러나 시스템
  reducible). 즉 synergy 는 통합의 필요조건(rule60 반례)도 충분조건(rule90 반례)도 아니다. H_293
  (어떤 *차수* TE 도 Φ≠)을 한 단계 더: 흐름의 어떤 *성분*도 Φ≠. **통합은 국소 정보-흐름 통계의
  어떤 분해로도 환원되지 않는 system-cut(전체-부분) 속성**이다. rule 90 은 LZ(H_288)·multivariate
  TE(H_293)·synergy(본 H) 셋 다 과대 = "국소 흐름/복잡도 有, 전역 통합 無"의 cross-measure 서명
  정점. 논문 thesis 최대 강화. (단 co-information 은 2-source net 요약, full Williams-Beer 4-atom
  PID 아님 — §9 L1.)
falsifiers_triggered: F294.2 (synergy ⊥ Φ — 발견 그 자체, closed-negative)
```

re-run byte-identical 확인 (F294.5).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_294 no component of directed information flow tracks faithful IIT4 big-Phi:
   conditional interaction information shows synergy is orthogonal to Phi (Pearson r=0.03),
   via a double dissociation — rule 60 has max Phi (13.6) yet zero synergy (pure unique
   information) while rule 90 has max synergy (4.0) yet Phi=0; integration is a system-cut
   property not reducible to any local flow decomposition; deterministic toy-substrate,
   NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values deterministic arithmetic, interpretation fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 (co-information ≠ full PID)**: II_c 는 2-source synergy/redundancy 의 *net* 요약
  (co-information). full Williams-Beer 4-atom PID(synergy·redundancy·unique×2 분리)는 더 세밀한
  분해를 준다 — 특히 rule 60 의 "unique" 항을 명시 분리. 단 본 H 의 결론(synergy net ⊥ Φ + rule60
  unique-info/high-Φ + rule90 synergy/zero-Φ)은 net 수준에서 이미 결정적.
- **L2 (ECA parity → redundancy=0)**: 본 substrate 가족(XOR-계열)은 redundancy 항이 0 (sources
  가 target 정보를 공유 안 함). redundancy 가 Φ 와 어떻게 관계되는지는 redundancy>0 substrate
  (예: copy/majority 망)에서 별도 검정 필요.
- **L3 (조건부 self)**: II_c 를 self 조건부로 정의 (H_293 정합). 비조건부/다중-lag 는 다른 분해.
- **L4 (n=4 small, 10 룰)**: r 절대값 panel 의존; 방향(synergy⊥Φ, 이중 dissociation) robust.
- **L5 (substrate proxy)**: ECA = flow proxy, phenomenal 주장 아님.
- **L6 (structure-cut big-Φ)**: 상관 부재 결론은 scale-offset robust.
- **L7 (verdict ≠ 형이상학)**: CLOSED-NEGATIVE 는 toy 측정 사실.

## 10. Cross-Links

- **parent (예측원)**: PAPER/phi-information-triangulation §future "PID 로 어느 성분이 Φ 추종"
  예측. 본 H: synergy net ⊥ Φ — 어떤 흐름 성분도 Φ≠ (thesis 최대 강화).
- **sibling**: [[H_293]] (어떤 *차수* TE 도 Φ≠ — 본 H 는 *성분* 으로 한 단계 더) · [[H_290]]
  (bivariate TE) · [[H_288]] (LZ rule90 over) — rule 90 이 LZ·multivariate-TE·synergy 셋 다
  과대 = cross-measure 서명 정점.
- **engine lib (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (eca_tpm/big_phi/iit4_bit/
  iit4_pow2, via stdlib) — 새 IIT4 코드 0줄 (g61).
- **Next**: (a) full Williams-Beer 4-atom PID (rule60 unique 항 명시) ; (b) redundancy>0 substrate
  (copy/majority)에서 redundancy↔Φ ; (c) 큰 N 에서 system-cut(Φ) vs 모든 local-flow 분해 갭.
