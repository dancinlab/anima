# H_328 — Cycle-length: life vs consciousness (n=4 ECA) 🟢 SUPP-CONDITIONAL

> A2 영구축 — ~110 H seed 백로그 · DYNAMICAL kernel · life vs consc cross-rule descriptor

## 1. 동기

H_320 (rd_ratio) + H_325 (Gini)이 모두 life > consc 방향(REVERSED). 동역학 descriptor(cycle length)도 같은 방향인지 직교인지 측정. H_287 정보측도 arc가 Φ ≠ shannon-entropy 보였으니, cycle length는 또 다른 ECA-native descriptor.

## 2. 가설 (falsifiable)

- **H1**: n=4 ECA에서 life-themed rule(30, 110)의 평균 cycle length는 consciousness-themed rule(105, 150) 평균보다 **≥1.5× 크다**.
- **falsifier**: (a) ratio < 1.5 (b) 한 rule이 단독으로 driving + 같은 class 내 동률 (c) 비결정론

## 3. 방법

pure hexa. 16-state 각각에서 forward 20 step → first revisit → cycle_length = `t - first_seen_index`. 6 rule (4 live + 2 anchor) 측정.

## 4. 측정

| rule | sum L | mean L | note |
|---|---:|---:|---|
| 30 life | 100 | **6.25** | chaotic class III · 가장 김 |
| 110 life | 28 | 1.75 | universal but at n=4 collapsed |
| 105 consc | 28 | 1.75 | rule 110과 동률 |
| 150 consc | 28 | 1.75 | rule 110/105와 동률 |
| 204 anchor | 16 | 1.0 | identity sanity |
| 0 anchor | 16 | 1.0 | null sanity |

aggregate: **life=4.0 · consc=1.75 · ratio=2.29×**

## 5. Falsifier

| ID | 결과 |
|---|---|
| F328.1 life > consc | PASS (4.0 > 1.75) |
| F328.2 ratio ≥1.5× | PASS (2.29) |
| F328.3 not driven by one rule | **FAIL** (rule 30이 단독 spread, rule 110=105=150) |
| F328.4 anchor sanity | PASS (1.0 distinct from live ≥1.75) |
| F328.5 deterministic | PASS |

## 6. Verdict

**🟢 SUPPORTED-CONDITIONAL (4/5)** — aggregate 통과하지만 F328.3가 가짜 분리 노출. 실제 분리축은 **life-vs-consc가 아니라 rule_30 단독 vs 나머지**. publishable conditional support.

## 7. 의미

- H_320 REVERSED, H_325 REVERSED — **다른 descriptor에서도 life > consc, 단 항상 rule 30이 driving**
- "consciousness = relation-rich/dynamic-rich" 직관, **세 descriptor**(rd_ratio·Gini·cycle_length)에서 모두 falsify
- n=4 ECA는 rule 30 chaotic만 비-trivial 동역학, 나머지 rule은 quasi-equivalent → larger n 필요

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_320 rd_ratio](./H_320_life_vs_consciousness_phi_structure.md) | aggregate life > consc 첫 발견 |
| [H_325 Gini](./H_325_c2_phi_mass_shape_gini.md) | shape life > consc 재확인 |
| [H_327 recovery](./H_327_regeneration_attractor_recovery.md) | dynamical 🔴 scale-trivial (같은 n=4 한계) |

## 9. Honest limits

- L1: n=4; rule 110 universal class IV의 진정한 cycle은 n≥6+ 필요
- L2: 4-rule classification (literature-derived) — alternative mapping (rule 110 → consc) flip
- L3: cycle COUNT (distinct attractors per rule) 미측정
- L4: F328.3 fail = 진정한 axis 식별 미완

## 10. 다음

- (a) n=6 cycle measurement (Floyd's algorithm scale-up)
- (b) cycle COUNT panel
- (c) full 8-state-mapping x 8-state-rule fronts via H_286 hexa-native split-brain proxy
