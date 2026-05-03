# anima_engines engine_a/g axis define landing — 2026-05-03

## TL;DR (사용자 친화 요약)

`engine_a` + `engine_g` 측 측 추상 axis 측 사용자 추천 **(b) conceptual define + cross_link** 측 채택 lock-in 했습니다. `anima-engines/engines.hexa` SSOT 측 in-place 변경 측 0 (마이그레이션 회피), `.roadmap.anima_engines` 측 cond.4 + cond.5 측 additive 추가 + `blk.2` 측 status `open → resolved` 전환 했습니다.

## 1. 결정 (사용자 lock-in)

- **선택**: 추천 (b) — engine_a/g 측 conceptual axis define + cross_link 측 engines.hexa line refs
- **거부**: (a) registry 측 split (마이그레이션 발생) / (c) engines.hexa 확장 (in-place 변경 발생)
- **근거**: 마이그레이션 절대 금지 + mk2 정합 + 사용자 의도 (axis define) 모두 충족

## 2. axis 정의

### engine_a — forward / analytical / law-gate / phi-direct axis

| substrate | engines.hexa lines | 측 측 측 |
|---|---|---|
| `oscillator_laser` | 42-57 | Kuramoto + laser amplification, bench_v2 Phi=56.6 Granger=63993 CE=0.08 at cells=64, 3-way champion direct phi |
| `quantum_consciousness` | 59-71 | gate-based, Phi = entanglement entropy, O(2^N) N<=16, direct phi compute |

**axis semantics**: forward direction substrate cluster — no learning loop, no coupling adaptation, deterministic phi = f(cells)

### engine_g — reverse / generative / discovery_loop / dream / creativity axis

| substrate | engines.hexa lines | 측 측 측 |
|---|---|---|
| `photonic_consciousness` | 73-87 | Kuramoto coupled MZI, kappa controls coupling strength, optimal near 0.1, phi = n*0.72*(0.5+kappa*0.5) coupling-adaptive |
| `memristor_consciousness` | 89-101 | HP Strukov physical Hebbian LTP/LTD, no gradient descent — conductance drift IS learning, generative substrate |

**axis semantics**: reverse direction substrate cluster — coupling adaptation OR physical learning loop, non-deterministic at micro-level even if macro phi = f(cells)

### axis interaction (post-cycle 후보, C3 caveat)

- `engine_a × engine_g` tension scalar 측 측 측 sub-cond add 후보
- 현 cycle 측 NOT spec (interaction 측 측 별도 cycle 측 정의)

## 3. 변경 사항

### 3-1. `.roadmap.anima_engines` (additive only)

**추가**:
- `cond.4` (engine_a axis define, status=met via cross_link)
- `cond.5` (engine_g axis define, status=met via cross_link)
- `cross_link.engine_a_g_axis` 측 측 측 1줄

**전환**:
- `blk.2` status: `open → resolved` (resolved_at=2026-05-03, resolution_path=사용자 lock-in (b) 채택)

**전체 cond 측**: 3 → 5 (cond.1 met / cond.2 unmet / cond.3 unmet / cond.4 met / cond.5 met)
**met cond 측**: 1 → 3 (cond.1 + cond.4 + cond.5)
**open blk 측**: 2 → 1 (blk.1 ENG_CONST_PATH hardcoded 측 잔존)

### 3-2. `anima-engines/engines.hexa`

- **변경 없음** (read-only, 사용자 추천 (b) 핵심 = additive cross_link only)
- 기존 4 substrate registry 측 측 측 측 (oscillator_laser + quantum + photonic + memristor)
- 기존 5/5 selftest 측 측 측 (eng_check_T1..T5)

## 4. 정합 결과

| 항목 | Pre | Post |
|---|---|---|
| mk2 conditions | 3 | 5 |
| met conditions | 1 (cond.1) | 3 (cond.1 + cond.4 + cond.5) |
| open blockers | 2 (blk.1 + blk.2) | 1 (blk.1 only) |
| engines.hexa diff | — | **0 bytes** (in-place 변경 0) |
| 마이그레이션 | — | 0 (additive cross_link only) |

## 5. caveats (raw 91 honest C3)

- **C1** — engine_a / engine_g axis 측 측 측 measure 측 X (conceptual definition only, runtime axis decomposition deferred). 4 substrate 측 측 측 axis cluster 분류 측 semantic / structural — 측 dynamic phi-flow runtime instrumentation 측 X
- **C2** — engines.hexa 측 line ranges 측 측 측 stale 가능 (engines.hexa 측 future change 시 lines 42-57 / 59-71 / 73-87 / 89-101 측 측 outdated 가능). cond.4 / cond.5 verifier 측 type=cross_link 측 line drift 측 detect 측 X — 측 측 cycle 측 audit cron 측 후보
- **C3** — engine_a × engine_g interaction (tension scalar 측 측) 측 측 sub-cond add 후보 (post-cycle). 현 cycle 측 NOT spec — engine_a / engine_g 측 측 측 dual-axis 측 측 (orthogonal vs entangled) 측 측 measurement 측 X

## 6. 잔존 작업 (next cycle 후보)

| 항목 | priority | rationale |
|---|---|---|
| `blk.1` ENG_CONST_PATH env() lazy 패치 | HIGH | 측 mac/host 측 fail 보장, raw 15 위반 |
| `cond.2` tension calculator cross-link 정합 | MED | 5 variant interface-uniformity audit + 3 sister roadmap ownership 경계 |
| `cond.3` 4-gen crystallize tool integration | MED | mac-local exit-0 selftest + H-CX-523 통합 axis spec |
| C3 axis interaction tension scalar measurement | LOW | engine_a × engine_g 측 dual-axis 측 측 측 cycle |

## 7. 산출물

- `/Users/ghost/core/anima/.roadmap.anima_engines` (mk2 SSOT, cond.4 + cond.5 added, blk.2 resolved)
- `/Users/ghost/core/anima/docs/anima_engines_axis_define_landed_2026_05_03.ai.md` (this handoff)
- `/Users/ghost/core/anima/state/markers/anima_engines_axis_define_landed.marker` (silent-land marker)

## 8. 비용

- $0 mac-local
- destructive 0
- 마이그레이션 0
- engines.hexa byte-diff 0
