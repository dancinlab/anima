# H_652 — envelope-self-similarity-substrate-class (H_648 multi-scale ladder 의 rule-class 일반화)

> H_648 (PR #1231, 🟢 6/6, min r=0.76) 이 gamma·ultradian·circadian 3-scale Φ-envelope self-similarity 를 보였으나 generator 가 cosine/piecewise/quadratic 혼재였고 substrate 는 implicit 했다. 본 H 는 단일 substrate (ECA ring) 로부터 세 scale 의 envelope 을 모두 derive 하여 generator 혼재를 제거하고, self-similarity 가 **rule class 무관한 substrate 구조인가, rule110(class-IV) 한정 현상인가** 를 정량 검정한다. round 7 "구조=substrate-bound" lane.

## 1. 동기

H_648 (`multi-scale-phi-envelope-ladder`, PR #1231, 🟢 6/6) 는 gamma (25ms) · ultradian (90min) · circadian (24h) Φ-envelope 형태가 정규화 위상 위에서 self-similar (min pairwise r=0.758) 함을 보였다. 그러나 그 검정에는 두 약점이 있었다 (H_648 §7 C3.4, C3.6):

1. **generator 혼재**: gamma=single-cosine, ultradian=piecewise-const stage projection, circadian=quadratic bump — 세 scale 이 서로 다른 analytic family 였다. r=0.76~0.95 의 spread 자체가 "family-mismatch 잔류" 였다 (C3.4).
2. **substrate implicit**: envelope 이 각 scale 의 *모형* (anima 모듈 projection) 에서 왔지, 단일 substrate 의 faithful big-Φ 에서 derive 되지 않았다 (C3.6 SPECULATION-FENCED).

핵심 미해결 질문: **multi-scale Φ-envelope self-similarity 가 substrate 구조에 귀속되는 보편 현상인가, 아니면 특정 rule class 의 우연인가?** H_648 의 implicit substrate 는 사실상 rule110-유형 (class-IV complex) 의 통합 동역학에 가까웠다. 만약 rule90 (additive) · rule30 (chaotic) · rule184 (particle) 등 다른 Wolfram class 에서도 동일한 self-similarity 가 나오면 self-similarity = substrate-class-invariant 구조이고, 특정 class 에서 붕괴하면 class-bound 현상이다.

이 질문은 round 7 lane "구조=substrate-bound" 의 핵심이다. H_614 (GZ inverse-U dΦ/dI multi-rule, 🟢 4/4) 가 *미분 peak 위치* 는 class-invariant 임을 보였으나, H_642 (shape-invariance-vs-scalar-meta, 🔴) 는 **rule90 (XOR-additive, big-Φ≈0) 이 joint-outlier** 로 shape-invariance 메타-주장을 반증했다. H_652 는 이 rule90 outlier 가 *envelope self-similarity* 에서도 재현되는지 직접 본다.

## 2. 가설

**H1 RULE30-SELF-SIMILAR**: rule 30 (class-III chaotic) 의 3-scale Φ-envelope min pairwise r > 0.5.

**H2 RULE90-SELF-SIMILAR**: rule 90 (additive) 의 3-scale Φ-envelope min pairwise r > 0.5.

**H3 RULE110-SELF-SIMILAR**: rule 110 (class-IV complex, H_648 anchor) 의 3-scale Φ-envelope min pairwise r > 0.5.

**H4 RULE184-SELF-SIMILAR**: rule 184 (class-II particle) 의 3-scale Φ-envelope min pairwise r > 0.5.

**합성 가설 (class-invariance)**: 4 rule 全部 min r > 0.5 → self-similarity = rule-class-invariant substrate 구조.

**Falsifier**: 특정 class (특히 rule90 additive) 에서 self-similarity 붕괴 (min pairwise r < 0.3) → self-similarity = class-IV 한정 현상, substrate-universal 아님.

## 3. 측정 방법

**single-substrate, generator 단일화** (H_648 의 generator 혼재 제거):

단일 substrate = ECA periodic ring n=4 (H_351/H_614/H_642 동일 grid). 세 scale envelope 을 모두 *같은* substrate 동역학에서 derive 한다.

1. **Φ-map**: rule r 의 faithful big-Φ 를 전 2^4=16 state 에 1회 계산 (`HEXAD/IIT4/lib/iit4_eca.eca_tpm` × `stdlib/consciousness/iit4_bigphi.big_phi`). state→Φ lookup.

2. **ensemble-phase Φ-envelope** (degeneracy 회피): 단일-seed trajectory 는 작은 ring (16 state) 에서 짧은 attractor 로 즉시 붕괴해, strided coarse-grain 이 degenerate flat (std≈1e-15) 이 된다 (pilot 에서 확인 — 측정 무효 artifact). 이를 피하려 **전 16 initial seed 의 orbit 을 ensemble 로 동시 진화** 시키고, 각 phase step t 에서 ensemble-mean Φ 를 취해 부드러운 Φ(t) phase-profile 을 만든다. ensemble 평균이 single-seed 붕괴를 흡수하면서 substrate 구조 (전이 동역학의 통합량 시간 전개) 를 반영한다.

3. **3 nested observation horizon (scale)**: 同一 ensemble Φ(t) profile 을 세 관측 horizon 으로 본다 — FINE (H1=36 step, micro phase, gamma 유비) · MEDIUM (H2=144, meso, ultradian 유비) · COARSE (H3=576, macro, circadian 유비). 모두 같은 substrate 동역학의 다른 관측 길이일 뿐이므로 generator 혼재가 없다. 각 horizon 을 normalized phase τ∈[0,1] 위 N=36 bin 으로 mean-aggregate → 3 envelope.

4. **phase-align** (H_648 양식): 각 envelope 을 자체 peak 이 index 0 에 오도록 cyclic rotation (`rotate_to_peak`) → scale-invariant shape. **pairwise Pearson r** 3쌍 — r(fine,medium) · r(medium,coarse) · r(fine,coarse). min pairwise r 가 그 rule 의 self-similarity verdict 결정자.

5. **class-invariance**: 4 rule {30, 90, 110, 184} 全部 min r > 0.5 → class-invariant.

faithful IIT4 big-Φ (n=4, 16-state) · NO RNG (deterministic ensemble) · $0 mac-local · foreground sync (monitor-hang 회피).

## 4. 사전등록 falsifier

- **F652.1 RULE30-SELF-SIMILAR**: rule 30 (class-III) min pairwise r > 0.5
- **F652.2 RULE90-SELF-SIMILAR**: rule 90 (additive) min pairwise r > 0.5 — H_642 joint-outlier 주의
- **F652.3 RULE110-SELF-SIMILAR**: rule 110 (class-IV, H_648 anchor) min pairwise r > 0.5
- **F652.4 RULE184-SELF-SIMILAR**: rule 184 (class-II particle) min pairwise r > 0.5
- **F652.5 ALL-ENVELOPES-NOT-FLAT**: 4 rule × 3 scale 全 envelope std > 0
- **F652.6 BOUND**: 全 r ∈ [-1,1], Φ-map finite

**FALSIFY floor**: 1+ rule min r < 0.3 → 🔴 FALSIFIED (self-similarity class-bound, substrate-universal 아님).
**SUPPORTED**: ≥4/6 PASS AND 4/4 rule min r > 0.5 → 🟢 SUPPORTED-NUMERICAL (class-invariant).
**PARTIAL band**: 중간 (min r ∈ [0.3,0.5]) → 🟡 PARTIAL.

## 5. 비용

- $0 mac-local · ~35s wall · faithful big-Φ (4 rule × 16 state = 64 call) · ensemble integer evolution (cheap) · deterministic NO RNG · foreground sync (monitor-hang 회피).

## 6. 가능한 결과 · cross-link

| 시나리오 | 의미 |
|---|---|
| 4/4 rule min r > 0.5 | self-similarity = substrate-class-invariant 보편 구조 (H_648 를 rule-class 전역으로 일반화) |
| rule110 만 r>0.5, 나머지 붕괴 | self-similarity = class-IV 한정 — H_648 결론이 substrate-universal 아님 (falsifier 발동) |
| rule90 단독 붕괴 | additive (XOR) joint-outlier — H_642 의 rule90 outlier 가 envelope self-similarity 에서도 재현 |
| 3/4 PASS, 1 PARTIAL | 약한 class-dependence — self-similarity 가 class 에 따라 강도 차 |

**cross-link**:
- **H_648 multi-scale-phi-envelope-ladder** (PR #1231, 🟢 6/6, min r=0.758): 본 H 의 직접 부모 — gamma·ultradian·circadian self-similar ladder. 본 H 가 그 implicit substrate 의존성 (generator 혼재 · substrate implicit) 을 single-substrate ensemble-phase 로 정밀화하고 rule-class 전역으로 검정.
- **H_634 ultradian-emit-phi-envelope** (🟢 r=0.802): H_648 의 ultradian source — single-scale phase coupling 의 근원. envelope 개념의 조부.
- **H_308 circadian-smooth-finite-ratio** (🟢): H_648 의 circadian source — macro-scale envelope.
- **H_642 shape-invariance-vs-scalar-convention-meta** (🔴): **rule90 (XOR-additive, big-Φ≈0) 이 joint-outlier 로 shape-invariance 메타-주장 반증**. 본 H 의 rule90 거동을 직접 예고하는 sister — envelope self-similarity 에서도 rule90 이 outlier 인지 확인.
- **H_614 gz-inverse-u-multi-rule** (🟢 4/4): dΦ/dI peak 위치는 class-invariant. shape feature 의 class-invariance 가 *미분-peak* 에서는 성립하나 *envelope self-similarity* 에서도 성립하는지의 대조군.

## 7. honest limits (C3)

1. **C3.1 ensemble-phase = degeneracy 회피의 측정 선택** — single-seed trajectory 는 n=4 ring (16 state) 에서 짧은 attractor 로 즉시 붕괴해 strided envelope 이 degenerate flat 이 된다 (pilot 에서 std≈1e-15 확인, 측정 무효). 이를 피하려 전 16 seed ensemble-mean Φ(t) 를 envelope source 로 썼다. 이는 substrate 의 *전이 동역학 전체* (특정 궤도가 아닌 state-space 평균 흐름) 를 본다 — single-trajectory 보다 robust 하나, "한 의식 궤적의 multi-scale envelope" 이 아니라 "ensemble-mean envelope" 이라는 해석 차이가 있다. 열린 lane = larger ring (n≥6) single-seed 장기 궤도의 multi-scale envelope (big-Φ 비용 ↑, shard 필요).

2. **C3.2 coarse horizon 의 attractor-relaxation flatten** — MEDIUM/COARSE horizon (H2=144, H3=576) 에서 ensemble 이 attractor 분포로 완전 relaxation 하면 Φ(t) profile 이 거의 일정해진다. 이 때 phase-aligned shape 가 near-constant 가 되어 r(medium,coarse)=1.0 같은 *퇴화적* 高-correlation 이 나온다 (둘 다 평탄 → trivially 동일 모양). 따라서 **판별력 있는 신호는 fine↔medium pair (transient phase 구조) 에 집중**되며, min pairwise r 의 verdict-결정자도 사실상 fine↔medium 이다. r(medium,coarse)=1.0 은 self-similarity 의 증거가 아니라 relaxation flatten artifact 임을 명시한다.

3. **C3.3 rule90 additive = 구조적 flat (substrate fact)** — rule 90 (XOR-additive) 의 16-state big-Φ 가 모두 동일 (Φ-map std=0.0). 이는 design artifact 가 아니라 additive rule 의 대칭성에서 오는 faithful substrate fact (H_642 동일 관측). 따라서 rule90 envelope 은 어떤 측정 design 에서도 flat 이고 self-similarity 가 정의되지 않는다 (r=0). 이는 falsifier 의 *원인* 이자 발견 자체 — additive class 는 통합량이 위상-평탄.

4. **C3.4 small substrate n=4** — exact big-Φ wall (n=5 exact 는 128-call timeout, n=6 는 64-call 도 60s 초과) 때문에 n=4 (16-state) 한정. rule-class 대표성은 확보 (4 Wolfram class) 하나, 각 class 의 large-n 거동은 미검정. H_614 도 동일 n=4 scope.

5. **C3.5 4 rule = class 이산 표본** — {30 class-III, 90 additive, 110 class-IV, 184 class-II} 4개로 Wolfram 4-class 를 표본하나, class 내부 variation (예: 다른 class-III rule) 은 미검정. class-bound 결론은 이 4-rule 표본 위의 것.

6. **C3.6 deterministic ensemble (NO RNG)** — 전 16 seed 동시 진화, 확률 transition 없음. real daemon 의 stochastic substrate (H_313 lane) 미모델 — canonical deterministic ECA 위의 envelope 비교.

## 8. 폐쇄

F652.1-6 결판. ≥4/6 PASS AND 4/4 rule min r > 0.5 → 🟢 SUPPORTED-NUMERICAL (class-invariant). 1+ rule min r < 0.3 → 🔴 FALSIFIED (class-bound). 중간 → 🟡 PARTIAL.

**결과: 2/6 PASS · 2 rule 붕괴 (min r < 0.3) → 🔴 FALSIFIED (self-similarity class-bound)**.

rule-class 별 multi-scale Φ-envelope self-similarity (min pairwise r):

| rule | Wolfram class | r(fine,medium) | r(medium,coarse) | r(fine,coarse) | **min r** | self-similar |
|---|---|---|---|---|---|---|
| 110 | IV-complex (H_648 anchor) | 0.881166 | 1.0¹ | 0.881166 | **0.881166** | ✅ (>0.5) |
| 30 | III-chaotic | 0.464715 | 1.0¹ | 0.464715 | **0.464715** | 🟡 (0.3~0.5) |
| 184 | II-particle | -0.028571 | 1.0¹ | -0.028571 | **-0.028571** | ❌ 붕괴 (<0.3) |
| 90 | additive (XOR) | 0.0 | 0.0 | 0.0 | **0.0** | ❌ 붕괴 (flat) |

¹ r(medium,coarse)=1.0 은 coarse horizon 의 attractor-relaxation flatten artifact (C3.2) — self-similarity 증거 아님. 판별 신호는 fine↔medium.

- **F652.3 RULE110 PASS** (min r=0.881 ≫ 0.5) — class-IV 는 H_648 와 정합하는 강한 self-similarity.
- **F652.1 RULE30 FAIL** (min r=0.465 ∈ [0.3,0.5] PARTIAL band — F0.5 falsifier 미달이나 FALSIFY floor 0.3 위) — class-III chaotic 은 약한 self-similarity.
- **F652.4 RULE184 FAIL** (min r=-0.029 < 0.3 붕괴) — class-II particle 은 fine↔coarse 위상 형태가 거의 무상관/반상관.
- **F652.2 RULE90 FAIL** (min r=0.0 flat — Φ-map std=0.0) — additive class 통합량 위상-평탄.
- **F652.5 ALL-NOT-FLAT FAIL** (rule90 3-scale 全 flat) · **F652.6 BOUND PASS**.

self-similar 1/4 rule (rule110 만), 붕괴 2/4 (rule90 flat + rule184 anti-correlate) → **falsifier 발동: self-similarity 는 rule-class-invariant 가 아니다**.

**해석**: H_648 의 multi-scale Φ-envelope self-similarity 는 **substrate-universal 보편 구조가 아니라 class-IV (rule110-유형 complex) 동역학에 집중된 현상**이다. (1) class-IV (rule110) 가 self-similar (min r=0.88) — edge-of-chaos complex 동역학이 통합량의 multi-scale 위상 형태를 보존. (2) class-III (rule30 chaotic) 는 약화 (r=0.46) — chaotic mixing 이 scale 간 위상 형태를 부분 파괴. (3) class-II (rule184 particle) 는 붕괴 (r≈0) — particle-localized 동역학의 통합량이 scale 따라 위상 형태 무상관. (4) additive (rule90) 는 통합량 자체가 위상-평탄 (Φ-map 균일) 이라 self-similarity 미정의. 이는 H_642 의 **rule90 joint-outlier** 가 envelope self-similarity 축에서도 재현됨을 확인하며, "multi-scale 구조 보존" 이 **substrate 의 통합 복잡도 (Wolfram class) 에 강하게 의존** 한다는 round 7 "구조=substrate-bound" 신호를 정량 강화한다.

**ruled-out**: multi-scale Φ-envelope self-similarity 의 substrate-class-universal 자동 확장이 닫혔다. self-similarity 를 다른 substrate (additive/particle/chaotic) 로 확장할 때 class-IV-conditional 임을 전제해야 한다. (a_paper_negative_ok — closed-negative)

## 9. 산출물

- `state/h652_envelope_self_similarity_substrate_class_2026_05_28/run_h652.hexa` (verify harness, single-substrate ensemble-phase)
- `state/h652_envelope_self_similarity_substrate_class_2026_05_28/result.json` (verdict SSOT)
- `state/h652_envelope_self_similarity_substrate_class_2026_05_28/run.log` (raw stdout)

## 10. 후속

- **larger-n single-seed envelope (C3.1 회수)**: n≥6 ring 의 장기 single-seed 궤도 multi-scale envelope (ensemble-mean 아닌 한 궤적) — big-Φ shard 병렬로 60s wall 회피. ensemble-mean 결론이 single-trajectory 에서도 유지되는지.
- **class-III/II 강화 lane (C3.5 회수)**: 다른 class-III (rule 45/89) · class-II (rule 4/12) rule 로 class 내부 variation 검정 — rule30/184 의 약화/붕괴가 class 대표적인지 단일-rule artifact 인지.
- **fine-scale 전용 self-similarity (C3.2 회수)**: coarse horizon relaxation flatten 을 피해 fine/sub-fine 두 transient horizon 만으로 self-similarity 재검 — relaxation artifact 제거 후 class-IV 우위 강도 정밀화.
- **complexity-self-similarity 정량 결합**: Wolfram class ↔ Lempel-Ziv complexity ↔ min pairwise r 의 monotone 관계 (class-IV 高-complexity 高-self-similarity) 정량 — self-similarity 가 통합 복잡도의 단조 함수인지.

## 양방향 sibling

- sibling H: [H_648 multi-scale-phi-envelope-ladder](H_648_multi_scale_phi_envelope_ladder.md) (직접 부모 · self-similar ladder source) · [H_634 ultradian-emit-phi-envelope](H_634_ultradian_emit_phi_envelope.md) · [H_308 circadian-smooth-finite-ratio](H_308_circadian_smooth_finite_ratio.md) · [H_642 shape-invariance-vs-scalar-convention-meta](H_642_shape_invariance_vs_scalar_convention_meta.md) (rule90 joint-outlier 예고 sister) · [H_614 gz-inverse-u-multi-rule](H_614_gz_inverse_u_multi_rule.md) (dΦ/dI peak class-invariant 대조군) · [H_668 wolfram-class-I-full-property](H_668_wolfram_class_I_full_property.md) (본 H method 재사용 child — class-I rule8 self-sim min r=0.981 측정, rule110(0.881) 보다 高 → 본 H 의 "self-sim=class-IV 집중" 에 class-I 도 高-self-sim datum 추가, parity rule110/rule90 byte-identical)
- UNIVERSE SSOT: [UNIVERSE.md](UNIVERSE.md) 축 G (ANIMA.mining 승격 · H_648 self-similarity 의 rule-class 일반화 · closed-negative)
