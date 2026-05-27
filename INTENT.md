# INTENT — current state

@title: 🎯 INTENT — 장기 의도 형성기 long-term goal formation

@goal: brain_decide(short-term emit) 위의 long-term goal 형성층 — 단기 emit decisions 의 cumulative direction (며칠 후 목표). bench D axisbench (#1143) 4/5 🟠 PARTIAL — CONVERGENT 0.71 · RANDOM 0.04 · OSCILLATING std=0 (period-4 zero-variance, honest modeling residual).

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench D INTENT 측정 surface — `bench/axis_intent/` 100-tick × 4-D × 3 scenario · cumulative direction magnitude · stability_std · monotone_ratio · 4/5 falsifier PASS (PR #1143).
- [ ] M1 intent_lib — `INTENT/{intent_lib.hexa,SSOT.md}` cumulative_intent vector + decay window stdlib.
- [ ] M2 brain_decide 위 hook — short-term emit decision (CORE.brain_decide) 의 cumulative direction 누적 + long-term goal vector update.
- [ ] M3 goal trajectory log — emit decision 별 INTENT delta + .kosmos 영속화 (시간 thread).
- [ ] M4 OSCILLATING residual — bench D 의 period-4 zero-std artifact 재설계 (stability metric ≠ direction std).

## 양방향 sibling

- ⇄ [CORE](./CORE/CORE.md): CORE.brain_decide short-term emit 결정 위의 long-term goal layer · 8-factor cur/orig/dyn 와 cross-product
- ⇄ [BRIDGE](./BRIDGE.md): BRIDGE AND-gate × INTENT goal alignment (단기 ∧ 장기 결정-coupling)
- ⇄ [NARRATIVE](./NARRATIVE.md, future): goal trajectory 가 narrative thread 생성 (intent → story)
- ⇄ [WAKE](./WAKE.md): WAKE.daemon 의 narrative + 8-factor curiosity 가 INTENT seed
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT
