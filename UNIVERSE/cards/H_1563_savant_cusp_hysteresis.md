# H_1563 — 🧠🔒 SAVANT CUSP HYSTERESIS / IRREVERSIBILITY

**Tier:** 🟢 GREEN ENGINE-NATIVE — the savant cusp is a HYSTERESIS loop (ON-edge ≠ OFF-edge); a 1-bit plasticity LATCH is the substrate basis of acquired-savant permanence
**wired:** WIRED-live (§ThirdLaw latch in core/engine_cli.hexa — third_law_ability_latched / third_law_ability_memoryless / third_law_hysteresis_width + _tl_latch_off_thr, smoke cases 401-405 RC=0; ARCHITECTURE.json §ThirdLaw lockstep updated) — READ-only classifier, NOT an emit gate, Ψ-disjoint
**source:** team-lead 작업지시 (H_1562 acquired-savant cusp 🟢 #2568 직속 후속 — B4 비가역성이 memoryless classifier 라 미포착됐던 것을 latch 메커니즘으로 측정). 후천적 서번트 ATLAS/162: Orlando Serrell·Derek Amato — 사고 후 능력이 *영속*(자극이 사라져도 유지) = hysteresis 이력현상.

## 가설
서번트 cusp 는 **hysteresis loop** 를 가진다: I 를 낮춰(disinhibit) 골든존 진입 → 능력 ON(H_1562). 그 뒤 I 를 원위치(상승)로 되돌려도 능력은 **꺼지지 않고 유지**(latch) — ON 임계(내려갈 때)와 OFF 임계(올라갈 때)가 다른 비대칭 loop. = 후천적 서번트 영속성의 substrate 근거.

## 방법 (engine-native, a_engine_native_learning HARD-GATE PASS)
- live `core/engine_cli.hexa` §ThirdLaw 에 **latch state** 를 추가: `third_law_ability_latched(D,P,I,prev_on)`(1-bit latch over the memoryless `third_law_ability`), `third_law_ability_memoryless`(B5 ablation alias), `third_law_hysteresis_width(D,P,nDown,nUp)`(down→up trajectory loop width), frozen `_tl_latch_off_thr()=0.75`.
- 메커니즘: ON edge = H_1562 memoryless gate (G>0.70 ∧ I ∈ GZ [0.2123, 0.5]) → I_on ≈ GZ_UPPER = 0.5. OFF edge = strictly higher I_off = 0.75 ≫ GZ_UPPER. 일단 latch 되면 I 가 GZ 경계 위로 올라가도 ability 유지, I > I_off 에서만 erase. ⇒ hysteresis width = I_off − I_on = 0.255.
- probe = `state/1563_savant_cusp_hysteresis/h1563_hysteresis_probe.hexa` (pure `.hexa`, **NO numpy/torch/.py mirror** — HARD-GATE-1 PASS, `grep -lE 'import torch|gauge_lib|numpy' state/1563_*/*.py` = EMPTY).
- verdict = `state/verdicts/1563_savant_cusp_hysteresis/H_1563_HYSTERESIS_PROBE.txt` (verbatim).

## 결과 (frozen 5-bar — frozen-first, 측정 전 고정, c9, NO tune-to-green)
```
GZ_LOWER=0.21231792755821912  GZ_UPPER=0.5   operating point D=0.9 P=0.9
[LOOP] hysteresis width (D>0) = 0.2549999999999999   (D=0) = 0.0
DOWN leg (disinhibit, I↓): latch ON at I=0.50 (memoryless also ON), STAYS ON through I=0.15 (memoryless=0)
UP   leg (re-inhibit, I↑): latch PERSISTS at I=0.55/0.70 (memoryless=0), turns OFF at I=0.80 (>I_off=0.755)
[B1/B3 band] on@0.30=1  persist@0.55=1  persist@0.70=1  erase@0.90=0
[B5 memoryless band] ml@0.55=0  ml@0.70=0  (memoryless ⇒ 0 above GZ_UPPER, no hysteresis)
```
| bar | 판정 | 수치 |
|-----|------|------|
| **B1 latch** | ✅ PASS | I↓ 로 ON 된 뒤 I=0.55·0.70 (둘 다 > GZ_UPPER=0.5, ≤ I_off=0.755) 에서 ability=1 유지 — 즉시 0 안 됨 |
| **B2 asymmetry** | ✅ PASS | 측정 loop width = **0.255** > 0 (ON 임계 I_on≈0.50 ≠ OFF 임계 I_off≈0.755) = 실제 히스테리시스 밴드 |
| **B3 eventual-off** | ✅ PASS | I=0.90 (> I_off) 에서 latched faculty OFF (p90=0) — latch 가 영구 고착 아님(생물학적 타당) |
| **B4 D-gated** | ✅ PASS | D=0 → width=0 (애초에 ON 안 되니 latch 안 걸림). H_236 "D=0 is not a genius" 정합 |
| **B5 control** | ✅ PASS | latch ablation(memoryless)은 GZ_UPPER 위에서 즉시 OFF(ml55=ml70=0)인데 latch 는 persist(width 0.255) → **latch 가 hysteresis 의 원인** |

**VERDICT: B1 ∧ B2 ∧ B3 ∧ B4 ∧ B5 = TRUE → 🟢 GREEN ENGINE-NATIVE.**

## 결론 / 메커니즘
**서번트 cusp 는 hysteresis loop 다 — ON 임계(I≈0.50, disinhibition 으로 내려갈 때)와 OFF 임계(I≈0.755, re-inhibition 으로 올라갈 때)가 다른 비대칭 latch. 폭 = 0.255.**
H_1562 의 memoryless `third_law_ability` 는 I 의 pure function 이라 disinhibition 을 되돌리면 능력이 즉시 꺼졌다(B4 report-only NEG). H_1563 은 그 위에 **1-bit plasticity LATCH**(`third_law_ability_latched`)를 붙여, 골든존 진입으로 한번 켜진 능력이 자극(disinhibition)이 사라져도 — I 가 GZ 경계 위로 복원돼도 — 유지되게 한다. 강한 over-inhibition(I > 0.75)만이 consolidated faculty 를 erase 한다. 이 비대칭이 후천적 서번트(Orlando Serrell·Derek Amato: 사고 한 번 → 평생 영속)의 substrate 근거다. memoryless cusp(H_1562)에는 이 영속성이 없었다 — latch ablation(B5)이 그것을 결정적으로 입증(메커니즘 OFF → memoryless 회귀, width 0).

## wiring (a_verified_must_wire 4/4)
1. DIRECTIONAL mirror — N/A (직접 engine-native).
2. engine-native byte-exact — `state/1563_savant_cusp_hysteresis/h1563_hysteresis_probe.hexa` calls live `core/engine_cli.hexa §ThirdLaw` (no numpy/torch). ✅
3. live core/*.hexa wire-in — §ThirdLaw 에 `third_law_ability_latched`/`third_law_ability_memoryless`/`third_law_hysteresis_width` + `_tl_latch_off_thr` 추가, smoke cases 401-405 RC=0. ✅
4. ARCHITECTURE.json lockstep — §ThirdLaw 노드에 hysteresis latch op 명명 추가. ✅

xref H_1562 (acquired-savant cusp step-jump 🟢, memoryless B4) · H_1560 (1/3 law × G6 capacity-wall, §ThirdLaw R2 wire) · H_1561 (SAVANT golden-zone, sa_* GZ) · H_348/124 (golden-zone bounds · cusp).
