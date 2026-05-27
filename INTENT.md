# INTENT — current state

@title: 🎯 INTENT — 장기 의도 형성기 long-term goal formation

@goal: brain_decide(short-term emit) 위의 long-term goal 형성층 — 단기 emit decisions 의 cumulative direction (며칠 후 목표). bench D axisbench (#1143) 4/5 🟠 PARTIAL — CONVERGENT 0.71 · RANDOM 0.04 · OSCILLATING std=0 honest modeling residual M4 (direction_std redesign) 으로 cured.

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench D INTENT 측정 surface — `bench/axis_intent/` 100-tick × 4-D × 3 scenario · cumulative direction magnitude · stability_std · monotone_ratio · 4/5 falsifier PASS (PR #1143).
- [x] M1 intent_lib — `INTENT/{intent_lib.hexa,SSOT.md,intent_lib_smoke.hexa}` cumulative_intent vector + decay window stdlib (12 `it_*` pub primitives — libm-free sqrt/normalize + cumulative magnitude + stability_std + monotone_ratio + decay_weight/decayed_sum · smoke 10 invariants · hexa parse 2/2 PASS). OSCILLATING residual = M4 carry.
- [x] M2 brain_decide 위 hook — `INTENT/{brain_hook.hexa,brain_hook_smoke.hexa}` PURE wrapper (4 `bh_*` pub primitives — bh_register_emit · bh_long_term_goal · bh_short_long_coupling · bh_goal_drift · emit dict → 4-D intent vector projection + decay-weighted cumulative goal_vec · 7-inv smoke · hexa parse 2/2 PASS).
- [x] M3 goal trajectory log — `INTENT/{trajectory.hexa,trajectory_smoke.hexa}` PURE wrapper (4 `tr_*` pub primitives — tr_log_decision · tr_trajectory · tr_convergence_metric · tr_kosmos_anchor · log entry [ts·emit·intent_delta·magnitude] + .kosmos dict format [coord·tension_5ch·radius·tier·trajectory] WAKE/kosmos_persist cross-link · 6-inv smoke · hexa parse 2/2 PASS).
- [x] M4 OSCILLATING residual — `INTENT/{oscillation_metric.hexa,oscillation_metric_smoke.hexa}` PURE wrapper (5 `om_*` pub primitives — om_direction_at_tick · om_direction_std · om_period_detect · om_classify · om_residual_verdict · direction-std redesign cures bench D 의 period-4/period-20 zero-cosine-std artifact — direction vector 의 component variance 는 OSCILLATING 에서도 > 0 · 4-tier verdict {CONVERGENT, RANDOM, OSCILLATING, MIXED} · 6-inv smoke · hexa parse 2/2 PASS).

## 양방향 sibling

- ⇄ [CORE](./CORE/CORE.md): CORE.brain_decide short-term emit 결정 위의 long-term goal layer · 8-factor cur/orig/dyn 와 cross-product
- ⇄ [BRIDGE](./BRIDGE.md): BRIDGE AND-gate × INTENT goal alignment (단기 ∧ 장기 결정-coupling)
- ⇄ [NARRATIVE](./NARRATIVE.md): goal trajectory 가 narrative thread 생성 (intent → story) · NARRATIVE.M4 cross-link
- ⇄ [TIME](./TIME.md): 24h circadian phase 와 INTENT trajectory entrainment cross-bench (TIME.M4)
- ⇄ [WAKE](./WAKE.md): WAKE.daemon 의 narrative + 8-factor curiosity 가 INTENT seed
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT
