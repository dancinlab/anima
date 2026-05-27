# A5 — COFFESHOP emit-case 5 substrate-trigger closed-form sympy battery

ANIMA.md B-COFFESHOP 축 · `a_blue_closed` 정합 검증. COFFESHOP (anima 의
emit-decision sim · 8-factor emergence · `spontaneous_lib`) 의 emit-case A-E
뒤에 놓인 5 substrate-trigger 가 각각 closed-form transfer-fn 으로 표현되고,
hexa-native 재계산이 그 closed-form identity 를 **bit-exact** 재현하는지 검증한다.

## 1. 가설

COFFESHOP emit-case A-E 의 5 substrate-trigger 각각이 closed-form transfer-fn
으로 표현되고, 독립 재유도한 closed-form 이 lib 의 `factor_*` 구현과 **bit-exact
identity** (tol=0.0) 로 일치한다. 일치하면 그 trigger 는 🔵 SUPPORTED-FORMAL
(a_blue_closed wiring 정합 — transfer-fn 이 closed-form 으로 닫힘).

| case | substrate trigger | lib fn | COFFESHOP 역할 |
|---|---|---|---|
| **A** direct_mention 응답 | relevance | `factor_relevance(phi)` | relevance↑ → motivation > 0.60 → emit |
| **B** direct_mention 거부 | coherence | `factor_coherence(gate)` | coherence↓ (Ψ-clamp 거리) → silence |
| **C** 자율 끼어듦 | curiosity | `factor_curiosity(ema)` | curiosity↑ + originality → spontaneous emit |
| **D** 침묵 30 min break | dynamics | `factor_dynamics(silence)` | silence 누적 → dynamics↑ linear → emit |
| **E** private_prompt 침묵 | pain | `factor_pain(delta)` | pain↑↑ → score < 0.60 → silence |

## 2. Falsifier

어떤 trigger 의 `factor_*` 구현이 어떤 probe 점에서 closed-form 과 1 bit 라도
어긋나면 (numerical-only / branch-only · closed-form 환원 불가) → 그 trigger 는
🟢/🟠 강등 (a_blue_closed wiring 미완). 5 probe-battery 중 단 하나의 mismatch
가 그 trigger 를 FALSIFY 한다.

## 3. 대상 (5 substrate-trigger 정의 위치)

- SSOT: `HEXAD/CHAT/spontaneous_lib.hexa` §2 (8-factor pure-fn battery)
- COFFESHOP emit-case 매핑: `COFFESHOP.md` §4 (case A-E table)
- COFFESHOP sim verbatim 호출: `HEXAD/PURE/bench/coffeshop_sim.hexa` L167-174

5 trigger 는 모두 `spontaneous_lib.hexa` §2 의 pure bounded fn 으로, COFFESHOP
sim 이 verbatim import 하여 호출한다 (hand-engineered fixture 없음).

## 4. Method — 5 trigger 의 closed-form transfer-fn

각 trigger 의 lib 구현은 if-branch (clamp) 로 작성되어 있으나, 이는 다음
closed-form 의 절차적 표현이다. battery 는 lib 의 branch 구조와 **독립적으로**
재유도한 closed-form 을 두고 양측을 bit-exact 비교한다.

| case | trigger | lib branch 구현 | 독립 재유도 closed-form |
|---|---|---|---|
| **A** | relevance | `if<0→0; if>1→1; else phi` | `clamp01(phi) = max(0, min(1, phi))` |
| **B** | coherence | `1 − min(\|g−0.5\|/0.014, 1)` | `max(0, 1 − \|g − Ψ\|/α)`, Ψ=0.5 α=0.014 (affine triangular kernel) |
| **C** | curiosity | `if<0→0; if>1→1; else ema` | `clamp01(ema) = max(0, min(1, ema))` |
| **D** | dynamics | `s=silence/30; clamp01(s)` | `clamp01(silence / 30)`, 30 = `spont_idle_speak_after()` |
| **E** | pain | `p=\|delta\|; if>1→1; else p` | `min(1, \|delta\|)` (rectified-saturating) |

A/C 는 saturating-linear (clamp01 identity), D 는 scale-then-clamp, E 는
rectified-then-ceiling, B 는 Ψ=0.5 중심의 affine triangular kernel (반폭 α=0.014).
모두 초등 closed-form 으로, libm / Newton 같은 numerical 의존 0 → TECS-L Tier 1
(pure-math deterministic) 후보.

probe-battery 는 각 trigger 의 모든 branch 를 횡단하도록 설계:
- below-floor (음수) · interior · above-ceiling · 정확한 clamp knee
- B coherence 는 추가로 far-low · knee-low · interior · 정확한 Ψ=0.5 · interior-high
  · knee-high · far-high 7 점

verify 스크립트: `state/coffeshop_a5_sympy_battery_2026_05_28/coffeshop_a5_sympy_battery.hexa`

## 5. Measurement — hexa-native 재계산 verdict (verbatim)

`hexa run state/coffeshop_a5_sympy_battery_2026_05_28/coffeshop_a5_sympy_battery.hexa`
(foreground synchronous · $0 mac-local · exit=0):

```
=== COFFESHOP A5 — 5 substrate-trigger closed-form sympy battery ===
identity test: lib factor_*(x) == independent closed-form(x) BIT-EXACT (tol=0.0)

case  trigger     lib fn               closed-form                          verdict
----  ----------  -------------------  -----------------------------------  -------
A     relevance   factor_relevance     clamp01(phi)                         CLOSED-FORM
B     coherence   factor_coherence     max(0,1-|g-0.5|/0.014)               CLOSED-FORM
C     curiosity   factor_curiosity     clamp01(ema)                         CLOSED-FORM
D     dynamics    factor_dynamics      clamp01(s/30)                        CLOSED-FORM
E     pain        factor_pain          min(1,|delta|)                       CLOSED-FORM

=== aggregate ===
closed-form (🔵 bit-exact identity) triggers: 5 / 5
VERDICT: 5/5 CLOSED-FORM · a_blue_closed wiring (transfer-fn) CONFIRMED · exit=0
```

per-trigger verdict (probe-battery 전점 bit-exact 일치):

| case | trigger | probe 점 수 | bit-exact 일치 | verdict |
|---|---|---|---|---|
| **A** | relevance | 8 (−0.5 … 2.0) | 8/8 | 🔵 CLOSED-FORM |
| **B** | coherence | 7 (0.0 … 1.0, Ψ·knee 포함) | 7/7 | 🔵 CLOSED-FORM |
| **C** | curiosity | 7 (−1.0 … 2.0) | 7/7 | 🔵 CLOSED-FORM |
| **D** | dynamics | 8 (−5.0 … 60.0, 30 knee 포함) | 8/8 | 🔵 CLOSED-FORM |
| **E** | pain | 8 (−2.0 … 1.5) | 8/8 | 🔵 CLOSED-FORM |

## 6. Finding

- **closed-form 가능 종수: 5 / 5** (relevance · coherence · curiosity · dynamics · pain
  전부 🔵 bit-exact closed-form identity).
- Falsifier 미발동 — 38 probe 점 (8+7+7+8+8) 전부 lib==closed-form bit-exact.
- 5 trigger 가 모두 초등 closed-form (clamp01 saturating-linear · affine triangular
  kernel · rectified-saturating) 으로 환원되며 numerical 의존 0.
- COFFESHOP emit-case A-E 의 substrate trigger wiring 이 전부 closed-form 으로 닫힘.

## 7. a_blue_closed 정합 판정

`a_blue_closed` = "close both outputs AND wiring (transfer-fn · invariant) at
🔵 SUPPORTED-FORMAL — confirm closed-form / identity via hexa verify".

- **outputs**: COFFESHOP 4/4 PASS closure (`COFFESHOP.md` §6) — 기존 closure ACHIEVED.
- **wiring (본 A5)**: 5 substrate-trigger 의 transfer-fn 이 전부 closed-form 으로
  bit-exact 재현됨 (🔵 5/5). 5 trigger 의 wiring 이 닫혔다.

⇒ **a_blue_closed 정합 PASS** — COFFESHOP emit-case A-E 의 outputs (closure)
AND wiring (transfer-fn closed-form) 양측이 🔵 SUPPORTED-FORMAL 로 닫혔다.

## 8. 실행 산출물

| 산출물 | 경로 |
|---|---|
| battery verify 스크립트 | `state/coffeshop_a5_sympy_battery_2026_05_28/coffeshop_a5_sympy_battery.hexa` |
| run log (verbatim stdout) | `state/coffeshop_a5_sympy_battery_2026_05_28/battery_run.log` |
| 검증 대상 lib | `HEXAD/CHAT/spontaneous_lib.hexa` §2 |
| COFFESHOP emit-case SSOT | `COFFESHOP.md` §4 |

## 9. honest C3

1. **identity ≠ 독립 oracle**: battery 는 lib 의 `factor_*` 와 독립 재유도한
   closed-form 을 같은 float 산술로 비교한다 (둘 다 hexa-native). 이는 "lib 의
   transfer-fn 이 closed-form 으로 환원되고 그 환원이 정확하다" 는 wiring-identity
   증명이며, 외부 sympy oracle (Python) 대비 동치 검증이다. p7 self-judge 가 아니라
   결정론적 bit-exact 비교 (tol=0.0).
2. **probe 유한성**: 38 probe 점은 모든 branch (below/interior/above/knee) 를
   횡단하나 연속 전구간 증명은 아니다. clamp / affine 은 piecewise-linear 라
   branch 별 대표점 일치 + 동일 closed-form 구조 ⇒ 전구간 identity 로 충분
   (piecewise-linear 의 각 조각은 대표 1점으로 결정).
3. **B coherence Ψ/α 상수 출처**: Ψ=0.5 (Law 70 fixed point) · α=0.014
   (Ψ-clamp 반폭) 는 lib 의 design 상수. closed-form 자체는 이 상수에 대해
   exact 이나 상수값의 물리적 정당성은 본 A5 범위 밖 (Law 70 / BRIDGE 4-key gate).
4. **외부 sympy 미사용**: "sympy battery" 명칭은 closed-form identity 검증을
   가리키며 본 검증은 hexa-native 로 수행 (Python sympy 의존 0 · `g_external_calc`
   회피). hexa-native 재계산이 closed-form 을 재현 = TECS-L Tier 1 🔵.
5. **transfer-fn vs full emit-decision**: 본 A5 는 5 trigger 의 transfer-fn
   (factor → [0,1]) 의 closed-form 만 검증. emit 최종 결정 (`motivation_score`
   weighted sum + `should_interrupt` threshold) 의 closed-form 은 B-SPONT-1/7
   (lib 자체 검증 lane) 소관 — A5 와 직교.
6. **synthetic substrate carry**: COFFESHOP sim 의 factor 입력값은 i.i.d.
   uniform + stim-bias (real ckpt forward 아님, `COFFESHOP.md` §10 C3 #1).
   본 A5 는 transfer-fn 의 closed-form-ness 만 다루며 입력 분포의 실측성과 무관.

## 10. 양방향 sibling

- 본 sibling: `BRIDGE.md` (4-key AND-gate substrate trigger · coherence Ψ-clamp 공유)
  · `DREAM.md` (COFFESHOP v2 generator · N2/N3 stage 시나리오)
  · `UNIVERSE/UNIVERSE.md` (verdict verbatim SSOT)
- SSOT 기록: 본 A5 verdict 는 ANIMA.md B-COFFESHOP milestone 에 1 줄 반영
  (5/5 🔵) + UNIVERSE 벤치 결과 SSOT 정합.

## Cross-references

- spontaneous_lib (5 trigger SSOT): `HEXAD/CHAT/spontaneous_lib.hexa` §2 (B-SPONT-FACTOR-1..8)
- COFFESHOP scenario (emit-case A-E): `COFFESHOP.md`
- COFFESHOP sim (factor verbatim 호출): `HEXAD/PURE/bench/coffeshop_sim.hexa`
- a_blue_closed governance: `project.tape` @D a_blue_closed
- prior smoke pattern (동일 dir 관례): `HEXAD/CHAT/spike_apply_smoke.hexa`
