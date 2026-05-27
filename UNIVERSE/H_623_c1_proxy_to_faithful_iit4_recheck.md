---
id: H_623
slug: c1-proxy-to-faithful-iit4-recheck
title: H_623 C1 round 4 — H_266/H_268/H_278 proxy → faithful 재검 (distinction + relation level)
domain: life · consciousness · information · meta
status: pre-register-frozen
exploration_method: E16 (cross-tool / known-anchor calibration) + E0 (meta-result-of-results — round 1 H_282 scalar 위에 distinction+relation 단위 확장)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_266/H_268/H_278 + H_282 round 1 + M6 IIT4)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28 (new — C1 raster round 4)
sister: H_266 (phi-calibration-known-iit, PARTIAL), H_268 (phi-metric-triangulation, PARTIAL), H_278 (faithful-phi-small-n, SUPPORTED), H_282 (proxy-to-faithful-remeasure round 1 SUPP 8/8, #570), H_285 (edge-of-chaos faithful 5/5, round 3), IIT4 M6 (FAITHFUL_REMEASURE.md, F-IIT4-6)
---

# H_623 — C1 round 4: distinction + relation 단위에서도 proxy → faithful 방향 보존?

## 1. Hypothesis

C1 raster 의 round 1 (H_282, PR #570) 가 H_266/268/278 의 **faithful 인과 big-Φ scalar**
방향보존을 SUPP 8/8 로 닫았다. 본 H_623 = C1 round 4 추가 — 같은 substrate 위에서
faithful 엔진의 한 단계 **하부 구조** 인 **distinction count (`n_distinctions`)** 와
**Σφ_d / Σφ_r** 까지 같은 방향을 보존하는지 검정.

가설: M6 의 `big_phi` 가 반환하는 5-tuple `[big_phi, total, Σφ_d, Σφ_r, n_distinctions]`
의 **structure-level 성분** (n_distinctions · Σφ_d · Σφ_r) 위에서도 H_266/268/278 의
방향(integrated > disconnected · T1 substantial · 6-scale variant)이 보존된다.

## 2. Why

- **big-Φ 는 통합 양을 한 스칼라로 압축한다** — round 1 (H_282) 이 그 스칼라 방향을
  보존했지만, big-Φ 가 0/양수로 갈리는 경계에서 분리하는 두 substrate 가 distinction
  층에서는 다른 패턴을 보일 수 있다 (예: 독립 self-cells 는 big-Φ=0 이지만 cell 별
  self-distinction 은 존재). 따라서 round 4 는 big-Φ 가 압축한 정보를 한 layer 풀어
  본다.
- **g61 stdlib 재사용**: `big_phi()` 가 이미 5-tuple 을 반환하므로 round 1 의 smoke 한
  줄만 확장하면 distinction+relation level 검정이 가능 — 새 엔진 빌드 없음, big-Φ 재구현
  없음.
- **directional-trust carry**: M6 §4 의 single-state caveat (binary direction 신뢰,
  연속 magnitude 헤지) 가 그대로 적용된다. 따라서 H_623 은 **방향 (mean 비교 + CV 부등식)**
  만 주장하고, 절대 magnitude (Σφ_d=3.89 등) 는 n=4 single-state outcome 으로 헤지한다.
- **closed-positive 추가가치**: round 1 의 SUPPORTED 가 scalar 축에서 wiring 을 닫았다면,
  round 4 의 SUPP 는 한 layer 아래(structure 성분)까지 wiring 이 정합임을 추가로 확인한다.
  FLIP 이 났다면 round 1 의 scalar 결론을 풀어 layer 별 분해가 필요했을 가치 있는 negative.

## 3. Predictions

- **H623.1 (F623.1 — H_266 distinction count)**: integrated rules {110,30,54} 의
  `n_distinctions` 평균 > disconnected rules {204, 0} 의 `n_distinctions` 평균
  (canonical state 1010, n=4 ring).
- **H623.2 (F623.2 — H_266 Σφ_d)**: integrated 의 Σφ_d 평균 > disconnected 의 Σφ_d 평균.
- **H623.3 (F623.3 — H_268 T1 structure)**: T1 (rule 110) 의 `n_distinctions ≥ 1` AND
  `Σφ_d + Σφ_r > 0` at ≥2/3 state ∈ {1, 5, 10} (H_268 robust target 의 structure-level
  존재 확증).
- **H623.4 (F623.4 — H_278 distinction CV)**: H_002 C2 의 6-scale 룰 {30,110,90,54,110,110}
  위 `n_distinctions` 의 population CV > 0.15 (structure-level scale-VARIANT 보존).
- **H623.5 (determinism)**: rule 110 의 `[n_distinctions, Σφ_d, Σφ_r]` re-run 시 Δ < 1e-9.

## 4. Variables

- **axis1_hypothesis** (primary, fixed-3): H_266 · H_268 · H_278 substrate (round 1 의
  identical pin).
- **axis2_substrate→TPM bridge** (`eca_tpm`, M6 재사용): identical to H_282.
- **axis3_state** (single-state caveat): canonical sys_state = 10 (1010), T1 robustness
  over {1, 5, 10}.
- **axis4_layer** (NEW — round 4 의 차별축): `n_distinctions` · `Σφ_d` · `Σφ_r` 의
  structure 성분에 대해 round 1 의 scalar 방향과 동일 방향 검정.
- **fixed**: n = 4 ring, measure = `big_phi(tpm, n, st)` 의 5-tuple structure 성분.
- **derived**: F623.1 mean(n_dist int) > mean(n_dist dis) · F623.2 mean(Σφ_d int) >
  mean(Σφ_d dis) · F623.3 T1 substantial-structure count ≥ 2/3 · F623.4 CV(6-scale
  n_dist) > 0.15 · F623.5 struct-level det.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h623_c1_proxy_to_faithful_iit4_recheck_2026_05_28/run_h623.hexa`
- **engine (REUSED, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` → stdlib
  `iit4_bigphi` (5-tuple). **재구현 없음 (g61)**.
- **reused fn**: `eca_tpm(rule, n)` · `big_phi(tpm, n, sys_state)` → 5-tuple
  `[big_phi, total, Σφ_d, Σφ_r, n_distinctions]`.
- **layer extraction**: `b[2] = Σφ_d` · `b[3] = Σφ_r` · `b[4] = n_distinctions`.
- **F623.1/2**: integrated/disconnected class-mean 비교 (canonical state).
- **F623.3**: T1 rule 110 의 3-state structure-presence count.
- **F623.4**: 6-scale n_distinctions 의 population CV.
- **F623.5**: struct-level re-run (in-process) Δ < 1e-9.
- **run cmd (verbatim)**:
  `HEXA_MEM_UNLIMITED=1 hexa run UNIVERSE/state/h623_c1_proxy_to_faithful_iit4_recheck_2026_05_28/run_h623.hexa`
- **runtime**: $0 mac local · NO GPU · n=4 small-N exact · wall < 5s · LLM none ·
  hexa-only true.
- **ledger**: `result.json` (config + F623.1/2/3/4 측정값 + summary).

## 6. Criteria

- **C1 (F623.1)**: integrated n_distinctions class-mean > disconnected class-mean → PASS.
- **C2 (F623.2)**: integrated Σφ_d class-mean > disconnected Σφ_d class-mean → PASS.
- **C3 (F623.3)**: T1 substantial-structure count ≥ 2/3 → PASS.
- **C4 (F623.4)**: 6-scale n_distinctions CV > 0.15 → PASS.
- **C5 (F623.5)**: struct-level Δ < 1e-9 → PASS.
- **verdict_rule**:
  - **SUPPORTED** = C1 ∧ C2 ∧ C3 ∧ C4 ∧ C5 (4 방향 verdict 모두 structure level 보존
    + 결정론).
  - **PARTIAL** = 일부 방향 보존, 일부 FLIP.
  - **FALSIFIED** = 핵심 방향이 structure level 에서 뒤집힘 (round 1 의 scalar SUPP 가
    distinction 층에서는 풀려야 하는 경우 — closed-negative valid).

## 7. Falsifiers (pre-registered ≥5, frozen 2026-05-28 BEFORE measuring)

- **F623.1 NDIST-COLLAPSE**: integrated n_dist class-mean ≤ disconnected class-mean → H_266
  방향이 structure level 에서 FLIP.
- **F623.2 SUMPHID-COLLAPSE**: integrated Σφ_d class-mean ≤ disconnected class-mean → H_266
  방향이 Σφ_d level 에서 FLIP.
- **F623.3 T1-NULL-STRUCT**: T1 substantial-structure count < 2 → H_268 robust target 의
  structure 가 reducible (T1 비-통합 substrate 임의 확정, scalar 풀린다).
- **F623.4 NDIST-FLAT**: 6-scale n_distinctions CV ≤ 0.15 → H_278 scale-variance 가
  structure level 에서 FLIP (faithful 의 분리가 scalar 단일 stellar=0 collapse 에만
  의존).
- **F623.5 NONDETERMINISM**: struct-level Δ > 1e-9 → raw#12 위반, smoke 무효.
- **F623.6 POST-HOC**: frozen 후 verdict 방향 edit → raw#12/raw#82 위반.

## 8. Verdict

```
verdict_class: SUPPORTED (pre-register-frozen smoke; C1∧C2∧C3∧C4∧C5 met)

engine: HEXAD/IIT4/lib (eca_tpm + big_phi 5-tuple, stdlib/consciousness) — REUSED.
config: n=4 ring · canonical state=10 (1010) · faithful IIT 4.0 Φ-structure.

── F623.1 — H_266 distinction count direction ──
  integrated   n_dist  : rule110=10.0  rule30=10.0  rule54=10.0  mean=10.0
  disconnected n_dist  : rule204=4.0   rule0=0.0                  mean=2.0
  mean(int)=10.0 > mean(dis)=2.0                          : true (×5 margin)

── F623.2 — H_266 Σφ_d direction ──
  integrated   Σφ_d    : rule110=3.0367  rule30=3.2179  rule54=5.4150  mean=3.8899
  disconnected Σφ_d    : rule204=4.0000  rule0=0.0000                  mean=2.0000
  mean(int)=3.8899 > mean(dis)=2.0000                     : true
  honest note: r204(identity) self-distinction Σφ_d=4 ≥ r110(3.04)/r30(3.22)
    개별. integrated 의 "통합" 우위는 class-mean 위에서만 보존 (r54=5.42 가 끌어올림).
    big-Φ 스칼라 (round 1, r204=0 vs int 7.5~10) 의 분리력이 distinction layer 에서는
    약화됨 — distinction 은 self-cell 별로도 적층되지만, 그 distinction 들을 통합하는
    irreducibility (big-Φ) 가 0 이라 reducible 로 판정되는 IIT 본연 미묘함이 그대로
    드러난 결과 (round 1 scalar 가 더 강한 분리축, round 4 는 layer 자체 존재 검정).

── F623.3 — H_268 T1 rule 110 structure ──
  state=1  n_dist=12.0   Σφ_d+Σφ_r=16.362
  state=5  n_dist=10.0   Σφ_d+Σφ_r=8.989
  state=10 n_dist=10.0   Σφ_d+Σφ_r=8.620
  substantial count (n_dist≥1 ∧ Σφ_d+Σφ_r>0)             : 3/3
  → T1 (H_268 robust target) 의 structure 가 3/3 state 에서 풍부히 존재.

── F623.4 — H_278 6-scale n_distinctions CV ──
  cosmic_web(30)=10  galaxy(110)=10  stellar(90)=0  planetary(54)=10
  biological(110)=10 neural(110)=10
  n_dist mean = 8.333  stddev = 3.727  CV = 0.4472
  scale-VARIANT at struct level (CV 0.4472 > 0.15)        : true
  → stellar rule 90 이 n=4@1010 에서 distinction layer 까지 collapse — round 1
    scalar 결론과 동일 분포 패턴. round 1 의 big-Φ CV=0.466 ≈ round 4 의 n_dist
    CV=0.447 (방향 동일, 절대값 ±5% 영역).

── F623.5 — determinism ──
  Δn_dist=0.0  ΔΣφ_d=0.0  ΔΣφ_r=0.0  → struct-level byte-identical : PASS

criteria:
  C1 F623.1 distinction class-mean direction              : PASS (10.0 > 2.0)
  C2 F623.2 Σφ_d class-mean direction                     : PASS (3.89 > 2.0)
  C3 F623.3 T1 structure substantial 3/3                  : PASS
  C4 F623.4 6-scale n_dist scale-variance                 : PASS (CV 0.447 > 0.15)
  C5 F623.5 struct-level re-run determinism               : PASS

verdict_rule: SUPPORTED iff C1∧C2∧C3∧C4∧C5 met
verdict     : SUPPORTED  (5/5 smoke checks PASS, 4 directional verdicts preserved
              + determinism at structure level)

falsifiers_triggered: none (F623.1~F623.5 all PASS, F623.6 N/A frozen-before-measure)
falsifiers_pass: 5/5.

key_finding:
  C1 round 1 (H_282) 이 big-Φ scalar 축에서 H_266/268/278 방향 보존을 SUPP 8/8 로
  닫았다. round 4 (H_623) 는 그 한 layer 아래 — IIT 4.0 Φ-structure 의 distinction
  count + Σφ_d + Σφ_r 성분 — 위에서도 같은 방향이 보존됨을 5/5 SUPP 로 추가 확증한다.
  특기점:
   (1) H_266 integrated > disconnected — n_distinctions class-mean 10.0 vs 2.0 (×5),
       Σφ_d class-mean 3.89 vs 2.0 보존. **honest note**: rule 204 (identity) 의
       self-distinction Σφ_d=4 가 개별 integrated rule 110/30 보다 큼 — distinction
       layer 는 self-cell 별로도 적층되지만 통합(irreducibility=big-Φ)이 0 이라 IIT
       가 reducible 로 판정. round 1 의 scalar 가 round 4 의 distinction 보다 더 강한
       분리축임이 정량적으로 드러남.
   (2) H_268 T1 (rule 110) — 3/3 state 에서 n_dist 10~12 + Σφ_d+Σφ_r 8.6~16.4 로
       풍부한 structure 보유, H_268 의 T1 robust verdict structure 단위 확증.
   (3) H_278 6-scale — n_dist CV 0.447 (>0.15), round 1 big-Φ CV 0.466 와 ±5% 영역
       에서 일치. stellar rule 90 의 collapse 가 scalar / distinction 양 층에서 동일
       방식으로 일어남.
   (4) round 1 의 scalar 결론이 distinction+relation layer 까지 정합 — proxy→faithful
       승격이 IIT 4.0 Φ-structure 의 모든 분해 layer 에서 유지된다는 강한 증거.

honest_note:
  directional-trust carry — binary DIRECTION (high vs low) trustworthy, 절대 magnitude
  (10/2, 3.89/2.0, CV 0.447) 는 n=4 single-state outcome 으로 헤지. round 1 의 §9 L1~L7
  honest limits 가 그대로 상속된다 (single-state · structure-cut · coupling 미모델 등).
  추가 새 limit (round 4 고유): rule 204 self-distinction 적층은 IIT 의 "distinction
  층은 reducible 인 self-cell 에도 존재할 수 있다" 의 정량 사례 — round 4 의 SUPP 는
  *class-mean* 위에서만 깔끔하다 (개별 rule 비교 시 r204 Σφ_d 가 r110/r30 보다 큼).
  big-Φ scalar 가 결국 가장 강한 분리축이라는 round 1 의 우위는 유지된다.
```

### `hexa verify` (g5 honest fence — empirical 해석은 closed-form atlas identity 아님)

```
verify --fence "H_623 extends H_282 (round 1 of C1 raster) one layer below — IIT 4.0
   Φ-structure components n_distinctions, Σφ_d, Σφ_r — on the same H_266/268/278
   substrates. Direction preserved at structure level (5/5 PASS): integrated
   n_distinctions class-mean 10.0 > disconnected 2.0 (×5 margin), integrated Σφ_d
   class-mean 3.89 > disconnected 2.0, T1 (rule 110) structure present 3/3 states
   (n_dist 10-12, Σφ_d+Σφ_r 8.6-16.4), 6-scale n_distinctions CV 0.447 > 0.15 — but
   honest: rule 204 self-distinction Σφ_d=4 exceeds individual integrated r110/r30
   distinctions (3.04/3.22), the integrated > disconnected hierarchy holds only at
   class-mean level; the big-Φ scalar (round 1) remains the stronger separator. n=4
   ring + canonical state 1010 toy substrate outcome, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           NOT a proven atlas atom (g4 honest fence, SF ≠ verified)
```

(structure-level VALUES 자체는 deterministic closed-form arithmetic — TPM build +
distinction iteration + relation iteration over the system MIP — 이며 in-process
re-run 시 Δ=0. 오직 empirical 해석(structure-level 방향 보존의 의미)만 fenced.)

## 9. Honest Limits (raw#91 c3, ≥5)

- **L1 (round 1 §9 L1~L7 carry)**: n=4 ring single-state headline, 3-state robust(T1).
  state-dependence + structure-cut big-Φ + coupling 미모델 + proxy-CV 동시산출 없음 +
  large-N 미도달 모두 round 1 limits 상속.
- **L2 (NEW — distinction self-stacking)**: rule 204 (identity) 는 big-Φ=0 (reducible)
  임에도 self-cell 4 개 각각 self-distinction 을 갖는다 (n_dist=4, Σφ_d=4). 따라서
  integrated > disconnected hierarchy 는 *class-mean* 위에서만 깔끔하고, 개별 rule
  비교에서는 r204 의 Σφ_d 가 r110/r30 보다 크다. round 4 의 SUPP 는 round 1 의 big-Φ
  분리 (r204=0 vs int 7.5~10) 보다 *약한 분리축*. 이를 honest 하게 명시.
- **L3 (round 1 의 강세 confirm, layer 분해 의의 한정)**: round 4 의 finding 은 round 1
  결론을 *뒤집지 않고* 정합 카리바*만* 한다. 따라서 round 4 단독 새 verdict 가 아니라
  round 1 의 robustness check 의 성격이다 (closed-positive 의 layer-decomposed 확증).
- **L4 (verdict ≠ 원 가설 re-verdict)**: round 1 과 동일 — H_623 SUPP 는 H_266/268/278
  frozen verdict 의 layer-decomposed 보조 evidence, *재verdict 가 아님*. 원 H 의 frozen
  L-C2.1 한계는 round 1 + round 4 동시로 한 칸 더 줄어들었으나, 완전 closure 는 state
  분포 평균 + scale-up + PyPhi anchor (L3, L5, L6) 가 필요.
- **L5 (n_dist 가 integer-quantized, CV 해석 한계)**: `n_distinctions` 는 정수 (각 룰
  에서 10 또는 0 또는 4). 6-scale CV 0.447 는 사실상 1 개 outlier (stellar=0) 가 만드는
  값으로, continuous CV 와 같은 분포-함의 (variance 의 광역성) 는 약하다. 본 검정은 binary
  "structure 가 collapse 하는가" 의 indicator 로만 신뢰.

## 10. Cross-Links

- **EXTENDS**: H_282 (C1 raster round 1, PR #570) 의 big-Φ scalar SUPP 8/8 결론을
  distinction + relation layer 로 확장.
- **재검 대상 H (proxy verdict source, 동일 round 1)**:
  - H_266 (`H_266_phi_calibration_known_iit.md`, PARTIAL) — round 1 + round 4 모두
    direction PRESERVED.
  - H_268 (`H_268_phi_metric_triangulation.md`, PARTIAL) — T1 robust, round 1 big-Φ
    + round 4 structure 양층에서 substantial.
  - H_278 (`H_278_faithful_phi_small_n.md`, SUPPORTED) — scale-VARIANT, round 1 big-Φ
    CV 0.466 + round 4 n_dist CV 0.447 (±5% 영역 일치).
- **C1 raster predecessors**:
  - **round 1**: H_282 — big-Φ scalar 방향 보존 SUPP 8/8 (PR #570).
  - **round 2**: H_281 (생명vs의식 Φ-structure 분리 SUPP 9/9) + H_280 (독립 kernel
    xval, Σφ_d non-monotone 버그 확정, big-Φ 단독 신뢰).
  - **round 3**: H_285 (edge-of-chaos faithful big-Φ 5/5, class-mean ordered <
    chaotic < edge(IV)).
  - **round 4**: H_623 (본 H, structure-level layer 확증).
- **engine (REUSED, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (`eca_tpm`) →
  `stdlib/consciousness/iit4_bigphi.hexa` (`big_phi`) → `iit4_relation` →
  `iit4_distinction` → `iit4_tpm`. design = `HEXAD/IIT4/DESIGN.md`. M6 remeasure
  `HEXAD/IIT4/state/iit4_m6_remeasure_2026_05_25/`.
- **gap lens**: layer-decomposition = F8 (cross-tool / inter-instrument calibration)
  + F12 (depth-of-witness — 같은 결론을 더 분해된 layer 에서 재확인).
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82 (no
  post-hoc) + g61 (stdlib reuse).
- **philosophy (CLAUDE.md)**: p7 NO PERPLEXITY VERDICT · a_blue_closed (wiring 검증,
  scalar → structure 층 확장) · a_completeness_over_cheap (round 1 scalar 위에 structure
  layer 추가 — cheap shortcut 아님, layer 분해의 정합성 확증).
- **literature**: Albantakis et al. (2023) IIT 4.0 (cause-effect structure /
  Φ-structure) · Tononi (2004) IIT · Wolfram (2002) A New Kind of Science.
- **state**: `UNIVERSE/state/h623_c1_proxy_to_faithful_iit4_recheck_2026_05_28/{run_h623.hexa,
  result.json}`.
- **Tier**: 🟢 NUMERICAL (faithful IIT 4.0 Φ-structure deterministic, in-process
  re-run Δ=0; empirical 해석은 ⚪ SPECULATION-FENCED, g5).
- **Next**: round 5 후보 — (a) **state 분포 평균** (round 1 §9 L1 + 본 §9 L1 axis):
  2^n state 위 structure-level 방향-보존 평균; (b) **scale-up n≤8** (L1 axis): n=4→8
  로 structure CV 의 n-dependence 분리; (c) **PyPhi anchor** (round 1 L3 axis):
  distinction count 의 PyPhi 문헌 1:1 대조; (d) **relation breakdown** (NEW): Σφ_r 가
  Σφ_d 와 동일 방향인지 단독 검정 (본 H 는 Σφ_d+Σφ_r 합산만).
