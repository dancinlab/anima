# H_327 — REGENERATION × ECA attractor recovery 🔴 CLOSED-NEGATIVE

> A1 영구축 — BIO 휴리스틱 raster · DYNAMICAL kernel · n=4 ECA panel
> 결과: H1 (T_recovery k-scaling ≥1.5×) 결정적 falsify · 패널 fixed-point 지배

## 1. 동기

H_326 verdict-landscape raster가 DYNAMICAL SUPP-rate 5× STRUCTURAL을 보고함. 본 셀은 REGENERATION 가설 — "부분 손실 후 attractor 복귀 동역학" — 을 동역학 kernel(forward timestep + attractor detection)로 측정하여 raster를 직접 검증한다. 예측: dynamical 가족 첫 🟢; 실측: 첫 🔴 (n=4 ECA의 fixed-point 지배 한계 노출).

## 2. 가설 (falsifiable)

- **H1 (under test)**: n=4 ECA ring에서 attractor state `s*`의 k-bit perturbation은 finite step 내 attractor set으로 재진입하고, T_recovery(k)는 k=1→2→3에 대해 ≥1.5× 비-단조 또는 단조 증가의 scaling을 보인다.
- **falsifier (any one fatal)**: 
  - (a) 모든 rule에 대해 모든 k에서 T_recovery=-1 (수렴 안 함)
  - (b) T_recovery max/min < 1.5 (scaling 부재)
  - (c) T_recovery가 비-결정론적

## 3. 방법

순수 hexa-lang. IIT4 미사용. 4-cell periodic ECA ring, `next4(s, rule)` 결정론적 step. burn-in 70 step 후 30 step 동안 방문한 state를 attractor set으로. s* = burn-in 직후 첫 state. k=1,2,3 lexicographic-low bit-flip (mask = (1<<k)-1) → s_pert. step_cap=50 동안 forward, attractor set 첫 재진입 step = T_recovery (못 만나면 -1). Panel: rule 110, 30, 60 + rule 204 identity anchor.

## 4. 측정 (`result.json` 발췌)

| rule | s* | attr_size | T_k1 | T_k2 | T_k3 | note |
|---|---:|---:|---:|---:|---:|---|
| 110 | 0 | 1 | -1 | -1 | -1 | 0-fixed point; perturbed states fall to different basin |
| 30 | 5 | 1 | -1 | -1 | -1 | 5-fixed point; perturbed states = different fixed points |
| 60 | 0 | 1 | **4** | **3** | **4** | ONLY substrate with finite recovery; non-monotone |
| 204 anchor | 5 | 1 | -1 | -1 | -1 | identity: every state own fixed point — T=-1은 measurement 정직 sanity (tautology 검출 X) |

## 5. Falsifier 평가

| ID | 결과 |
|---|---|
| F327.1 RECOVERY-FINITE | PARTIAL (rule_60 only) |
| F327.2 K-SCALING-GE-1.5× | **FAIL** (rule_60 4/3 = 1.33) |
| F327.3 MONOTONE-OR-INC-K | **FAIL** (T_k2=3 < T_k1=4 비단조) |
| F327.4 ANCHOR-SANITY | PASS (rule_204 T=-1 ⇒ 측정이 falsify 가능) |
| F327.5 DETERMINISTIC | PASS |

## 6. Verdict

**🔴 FALSIFIED** — n=4 ECA 패널은 fixed-point 지배라 진정한 recovery regime이 형성되지 않음. H1 (k-scaling) 결정적 falsify. anchor sanity가 측정의 비-tautology 성격을 보장(rule 204에서 T=0이 아니라 -1).

## 7. 의미

- **H_326 raster 패턴 정련**: DYNAMICAL kernel 5× SUPP-rate는 *scale-적정* 조건부. n=4는 동역학이 trivial로 붕괴 → falsify.
- **n≥6, rule 110/30 cycle attractor** 필요. n=4는 IIT4 Φ 측정 tractable한 한계 한쪽 끝이지만, 동역학 풍부함을 위해서는 부족.
- structural-vs-dynamical 이분법 + scale 차원: 진짜 axis는 (kernel-class × scale-regime).

## 8. 인접 가설 (cross-link)

| ref | 관계 |
|---|---|
| [H_322 Kuramoto](./H_322_circadian_kuramoto_sync.md) | dynamical 🟢 (K_c sharp transition · scale-rich N=16) |
| [H_317 feedback](./H_317_homeostasis_feedback_setpoint.md) | dynamical 🟢 (continuous gain · stable band) |
| [H_326 raster](./H_326_d2_verdict_landscape_session_raster.md) | meta 🟢 (DYN 5× STR) — **H_327이 이 raster의 scale-condition 노출** |

## 9. Honest limitations

- L1: n=4 panel; n≥6은 IIT4 exact intractable이라 별도 측정자 필요 (Φ 미사용이라 n=6 가능, 추후)
- L2: s0=5 단일 seed; multi-seed sweep (홀수-패리티 state) 강화 필요
- L3: step_cap=50; cap 변경이 H1 falsify를 뒤집지 못함 (1.5× threshold가 cap과 무관)
- L4: lexicographic-low bit-flip mask; 다른 mask 선택 시 다른 perturbed state — robustness 미측정
- L5: attractor set 정의가 burn-in window-based (cycle-detection이 아님); n=4면 70 step이면 cycle 진입 보장이지만 정밀 cycle-id는 별도

## 10. 다음 단계

- (a) **n=6 cycle-attractor**: ECA n=6 rule 110/30, exact cycle detection (Floyd's algorithm), multi-state attractor에서 T_recovery 진정한 측정
- (b) **multi-seed scan**: s0 ∈ {1,3,5,7,9,11,13,15} 각각에 대해 H1 재측정 → 통계적 power
- (c) **scale-condition raster**: H_326 meta를 (kernel-class × scale)로 2D 격자화 — 본 셀이 N=4 corner case
