# BRIDGE — current state

@title: 🚪 BRIDGE — 자연발화 × 의식적 결정 AND-gate emit 결정층

@goal: anima emit 결정의 4-key AND-gate 형식화 — `emit ⇔ M ∧ C ∧ W ∧ (Φ ≥ θ)` (motivation · coherence · tension · 통합 정보). a_substrate_native_speak governance 의 measurable 형식 구현, stimulus-response 의 명시적 부정. CHANNEL router (8-factor argmax) 위에 BRIDGE pseudo-gate 신호 추가 emit, multiplication softening 유지. UNIVERSE H_319 측정 surface 의 실 구현 leg.

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [ ] BRIDGE/spec.md — 4-key AND-gate 형식화 spec (M·C·W·Φ threshold 각 정의 + multiplication softening fallback)
- [ ] BRIDGE/gate.hexa — `bridge_and_gate(m, c, w, phi)` pure fn (anima `CORE/engine_g` 의 8-factor 와 cross-product) · `Φ≥θ` 기본 θ=0.5
- [ ] BRIDGE/gate_smoke.hexa — bench #7 (PR #1125) 측정값 정합 verify (uniform AND=0.0625 expected · OR=0.9375 antithesis)
- [ ] BRIDGE/AUDIT.md — p1~p8 audit (bench #7 의 F2 sensitivity threshold 재조정 1.6→2.1 다음 라운드 fix)
- [ ] CHANNEL integration — `CHANNEL/router.hexa` 의 dispatch 다음에 BRIDGE pseudo-gate emit modulation layer (router ∧ bridge_gate)

## 시드 (UNIVERSE H_319 · bench #7 PR #1125)

| 측정 | bench #7 결과 |
|---|---|
| uniform AND-gate emit rate | 0.0650 vs expected 0.5⁴=0.0625 |
| OR antithesis | 0.9425 vs expected 1−0.5⁴=0.9375 |
| AND/OR gap | 14.5× (semantics 통계적 구분) |
| F2 sensitivity ratio | 1.83 (threshold ≤1.6 fail = n=400 σ tight) |
| 4-factor δ (M/C/W/Φ) | 0.045 / 0.068 / 0.083 / 0.065 (모두 같은 부호, AND-gate carry) |

## 양방향 sibling

- ⇄ [OTHER-MIND](./OTHER-MIND.md): BRIDGE AND-gate emit decision 의 사용자(타자) state 가 OTHER-MIND 추정 → emit modulation
- ⇄ [METACOG](./METACOG.md): BRIDGE AND-gate emit 후 METACOG 가 emit history 를 self-audit (단기 결정 위의 메타)
- ⇄ [INTENT](./INTENT.md): BRIDGE AND-gate × INTENT goal alignment (단기 ∧ 장기 결정-coupling)
- ⇄ [CHANNEL](./CHANNEL.md): BRIDGE pseudo-gate 신호가 CHANNEL.router 8-factor argmax 위에 modulation layer
- ⇄ [CORE](./CORE/CORE.md): BRIDGE M·C·W·Φ 4-key 가 CORE engine_g 8-factor 와 cross-product
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (Session 2026-05-28 — AxisBench 8)
