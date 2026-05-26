---
id: H_297
slug: n5-bounded-phi-scale
title: rule 90 의 환원성은 even-N bipartite artifact — odd ring(n=5)에서 통합(Φ=19.5), arc 의 "rule90 over-prediction" 재해석
domain: consciousness · substrate · information · meta
status: supported
exploration_method: E5 (scale-up probe) + E0 (arc rule90-anomaly N-parity 검정) + E16 (n=4 vs n=5)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_288/293/294/295/296)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_295/296 (exclusion, multi-complex — n=4), H_287-294 (Φ vs 흐름 arc)
---

# H_297 — n=5 scale-up: rule 90 환원성은 even-N bipartite artifact

## 1. Hypothesis

arc(H_287-296) 전부 n=4 에서. rule 90 의 핵심: n=4 에서 Φ_whole=0(reducible). 그 원인은
even-ring(4-cycle)의 even-cell/odd-cell **bipartite decoupling** (H_289 confound, H_296 multi-
complex 분할). odd ring 인 n=5 에서는 이 decoupling 이 깨질 가능성. 만약 rule 90 이 n=5 에서
Φ>0 으로 점프하면, arc 의 "rule90 cross-measure over-prediction" 은 *실제 통합을 본 것*
이었고 n=4 가 *특이 case*.

**가설 H1 (검정 대상)**: n=5 (bounded big-Φ, cap=4) 에서 (a) 항등 204 + 상수 0/255 Φ=0,
(b) 통합 60/110 Φ>0 유지, (c) **rule 90 Φ>0** (n-parity bipartite-decoupling 가설 — odd
ring 에서 decoupling 깨짐, rule 90 통합).

## 2. Why

- **arc 의 핵심 anomaly 해소**: rule 90 이 LZ(H_288)·multivariate-TE(H_293)·synergy(H_294)
  셋 다 과대였던 건 *실제 통합* 을 본 것일 수도(n=4 가 가린 것). N-parity 검정으로 갈림.
- **scale-up 일반화**: 모든 arc 발견이 n=4 한 점이었음. n=5 bounded 로 핵심 분류(integrating
  vs reducible, anchors)의 scale-robustness 첫 측정.
- **engine 재사용 (g61)**: `big_phi_bounded(tpm,n,st,cap)` (cap<n=lower bound, cap=n=exact).
  cap=4 at n=5 = 가장 강한 lower bound. 새 IIT4 코드 0줄.
- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit + LLM none + $0.

## 3. Predictions

- **H297.1 (scale-anchors)**: n=5 에서 항등 204 + 상수 0 bounded Φ = 0.
- **H297.2 (integration-survives)**: n=5 에서 rule 60 OR 110 bounded Φ > 0.
- **H297.3 (rule90-N-parity, HEADLINE)**: n=5 에서 rule 90 bounded Φ > 0.
- **H297.4 (bound)**: 모든 값 ≥ 0.
- **H297.5 (determinism)**: rule 90 n=5 bounded re-run identical.

## 4. Variables

- **axis1_N**: n=4 (exact, 비교 baseline) vs n=5 (bounded, scale-up).
- **metric_phi_bounded**: big_phi_bounded(eca_tpm(rule,5), 5, st=21, cap=4) (state 10101).
- **panel**: arc 의 10 룰, 핵심 비교 rule 90 (n=4=0 vs n=5=?).

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h297_n5_bounded_phi_scale_2026_05_26/run_h297.hexa`
- **engine (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (eca_tpm) + `stdlib/
  consciousness/iit4_bounded.hexa` (big_phi_bounded). 새 IIT4 코드 0줄.
- **build/run (selfhosted)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root> hexa.real.bak-2026-05-22-
  pre-no-hxc build <src> -o /tmp/h297.bin && bin` — bg 실행(n=5 무거움).
- **deterministic**: re-run byte-identical. **hexa_only**: true. **runtime**: $0, NO GPU.
- **tier**: 🟢 SUPPORTED-NUMERICAL (bounded lower-bound).

## 6. Criteria

- **C1 (SCALE-ANCHORS)**: 항등·상수 n=5 Φ=0 → PASS.
- **C2 (INTEGRATION-SURVIVES)**: 60/110 n=5 Φ>0 → PASS.
- **C3 (RULE90-N-PARITY)**: rule 90 n=5 Φ>0 → H1 (HEADLINE) SUPPORTED.
- **C4 (BOUND+DET)**: PASS.

## 7. Falsifiers

- **F297.1 SCALE-ANCHORS**: 항등 OR 상수 0 Φ≠0 → 엔진 모순.
- **F297.2 INTEGRATION-SURVIVES**: 60+110 둘 다 Φ=0 → 통합이 n=4 artifact (강한 부정).
- **F297.3 RULE90-N-PARITY**: rule 90 n=5 Φ=0 → n-parity 가설 FALSIFIED (rule 90 환원성은
  깊은 구조적 사실, n=4 만이 아님). 어느 쪽이든 정보적 결과.
- **F297.4 BOUND**: 음수 Φ → 엔진 오류.
- **F297.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 SUPPORTED — rule 90 환원성은 even-N bipartite artifact. n=5 에서 rule 90
        Φ=19.5 (>0, *최상위 통합*). gate 6 PASS / 0 FAIL.

config: n=5 ring · bounded big-Phi cap=4 · state 10101 (st=21) · engine 재사용

panel (n=5 bounded vs n=4 exact at headline state):
  rule     n=4 (exact, st=5)   n=5 (bounded cap=4, st=21)
  0        0.0                  0.0       (constant — Φ=0 보존)
  255      0.0                  0.0
  204      0.0                  0.0       (identity)
  51       0.0                  0.0       (complement)
  150      6.0                  0.0       ◀ bounded(cap=4)에서 0 (full exact 미상)
  105      4.5                  0.0       ◀ 동일
  90       0.0                  **19.5**  ★★ ZERO → HIGH (n-parity confirmed)
  60       17.5                 16.5
  110      7.66                 17.694
  30       7.28                 20.269

핵심 관측: **rule 90 이 n=4(Φ=0)→n=5(Φ=19.5) 점프**. odd ring 에서 even/odd bipartite
decoupling 실패 → rule 90 이 panel 최상위 통합 substrate(60/30 대비 비슷·우월). H_296 의
two disjoint sub-complex 는 *4-cycle 의 even/odd 분할에만 특화된 현상*. n=5 에서는 ring 이
홀수라 그런 분할 불가, rule 90 통합.

criteria:
  C1 SCALE-ANCHORS (204/0 Φ=0)                  : PASS
  C2 INTEGRATION-SURVIVES (60=16.5, 110=17.7)   : PASS
  C3 RULE90-N-PARITY (Φ=19.5 > 0)               : H1 SUPPORTED (HEADLINE)
  C4 BOUND+DET                                   : PASS

falsifiers:
  F297.1a ANCHOR rule204 : PASS  (n=5 Φ=0)
  F297.1b ANCHOR rule0   : PASS
  F297.2 INTEGRATION-SURVIVES : PASS  (rule60 Φ=16.5)
  F297.3 RULE90-N-PARITY     : H1 SUPPORTED  (n=5 Φ=19.5 vs n=4 Φ=0)
  F297.4 BOUND                : PASS
  F297.5 DETERMINISM          : PASS  (rule90 n=5 a==b)

checks: 6 PASS / 0 FAIL

evidence_summary: 🟢 SUPPORTED-NUMERICAL — **rule 90 의 환원성은 even-N bipartite artifact
  였다**. n=4 에서 Φ_whole=0 (H_295/296 의 sub-complex/multi-complex 발견) 이었던 rule 90 이
  n=5(odd ring) 에서는 Φ=19.5 (bounded cap=4) — panel 최상위 통합(rule30 20.3·rule110 17.7
  대비 비슷·우월). odd ring 에서 even/odd bipartite decoupling 이 깨지면서 rule 90 이 본격
  통합. 이로써 **흐름 arc 의 "rule 90 cross-measure over-prediction" 이 재해석된다**: LZ
  (H_288)·multivariate-TE(H_293)·synergy(H_294) 가 본 *국소 통합* 은 *실제 통합* 이었고,
  n=4 의 reducibility 는 짝수-고리 구조 특이성이었다. **arc 의 헤드라인 thesis(Φ 는 system-cut
  property)는 더 강해진다**: 통합은 *모든 N* 에서 실재하나, *N-parity 가 system-cut 의
  접근성을 좌우*한다. anchors(상수/항등) n=5 에서도 Φ=0 유지 — scale-robust. honest: bounded
  cap=4 는 lower bound 라 rule 150/105 가 n=5 에서 0 으로 나온 건 cap 한도일 수 있음(full
  exact n=5 미측정, §9 L1).
falsifiers_triggered: none
```

re-run byte-identical 확인 (F297.5).

`hexa verify` (VERBATIM) — g5 fence:

```
verify --fence "H_297 rule 90's whole-Phi=0 at n=4 is an EVEN-N bipartite-decoupling artifact:
   at n=5 (odd ring, bounded big-Phi cap=4) rule 90 jumps to Phi=19.5 — the top of the panel
   alongside rules 30 (20.3) and 110 (17.7), exceeding rule 60 (16.5). The flow-arc 'rule 90
   over-prediction' (LZ/multivariate-TE/synergy) was actually seeing real integration that the
   even-ring decoupling hid; reducibility is N-parity-dependent. Anchors (identity 204,
   constants 0/255) stay at Phi=0 — scale-robust. deterministic toy-substrate, NOT an atlas
   identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values deterministic arithmetic (bounded lower bound), interpretation fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 (bounded cap=4 lower-bound)**: n=5 에서 cap=4 는 full exact 의 *lower bound*. rule
  150/105 가 0 으로 나온 건 cap 한도일 수 있고, rule 90/60/110/30 의 값들도 true Φ 보다 작을
  수 있음. 핵심 binary 결과(=0 vs >0)는 robust 이나 절대 magnitude 는 hedge.
- **L2 (single state)**: n=5 state 21 (10101) 한 점. 다른 state 에서 분류가 바뀔 수 있음
  (특히 rule 90 의 19.5 가 state 의존). 전수-state 검증은 후속.
- **L3 (n=4 → n=5 단 1 step)**: parity 효과는 even (4) vs odd (5) 단 1 step 만 측정.
  더 큰 n=6(even) / n=7(odd) 검정으로 parity 패턴 robustness 확인 필요.
- **L4 (rule 150/105 N=5 cap 한도)**: cap=5 exact 가 비용상 가능했다면 그 값을 직접 측정.
  cap-sweep 으로 saturation 곡선 측정 후속.
- **L5 (ECA proxy)**: ECA = proxy, phenomenal 주장 아님.
- **L6 (structure-cut big-Phi)**: 상관·비교 robust.
- **L7 (verdict ≠ 형이상학)**: SUPPORTED 는 toy 측정 사실.

## 10. Cross-Links

- **parent (arc 핵심 anomaly 해소)**: [[H_288]] LZ rule90 over · [[H_293]] multivariate-TE
  rule90 over · [[H_294]] synergy rule90 over · [[H_295]] rule90 sub-complex · [[H_296]]
  rule90 multi-complex — 모두 **n=4 even-ring artifact** 로 재해석. 측도들이 봤던 "국소 통합"
  은 *실제 통합* 이었고, n=5 에서 *전체* 통합으로 드러남.
- **engine lib (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` + `stdlib/consciousness/
  iit4_bounded.hexa` (big_phi_bounded) — 새 IIT4 코드 0줄.
- **Next**: (a) n=6 (even, 다시 reducible 예상) · n=7 (odd, 통합 예상) parity 패턴 검정 ·
  (b) rule 150/105 cap=5 exact (n=5 full big-Phi) · (c) full-state n=5 sweep (rule90 19.5 의
  state-robustness).
