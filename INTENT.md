# INTENT — current state

@title: 🎯 INTENT — 장기 의도 형성기 long-term goal formation

@goal: brain_decide(short-term emit) 위의 long-term goal 형성층 — 단기 emit decisions 의 cumulative direction (며칠 후 목표). bench D axisbench (#1143) 4/5 🟠 PARTIAL — CONVERGENT 0.71 · RANDOM 0.04 · OSCILLATING std=0 honest modeling residual. A6 진단 확정: residual = stability_std metric aliasing (period-20 ⊥ window-grid) — raw direction_std + argmax period_detect 측정자 교체로 🟢 RESOLVED 5/5, 진동은 intrinsic limit-cycle (H_634 ultradian cross-link).

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench D INTENT 측정 surface — `bench/axis_intent/` 100-tick × 4-D × 3 scenario · cumulative direction magnitude · stability_std · monotone_ratio · 4/5 falsifier PASS (PR #1143).
- [x] M1 intent_lib — `INTENT/{intent_lib.hexa,SSOT.md,intent_lib_smoke.hexa}` cumulative_intent vector + decay window stdlib (12 `it_*` pub primitives — libm-free sqrt/normalize + cumulative magnitude + stability_std + monotone_ratio + decay_weight/decayed_sum · smoke 10 invariants · hexa parse 2/2 PASS). OSCILLATING residual = M4 carry.
- [x] M2 brain_decide 위 hook — `INTENT/{brain_hook.hexa,brain_hook_smoke.hexa}` PURE wrapper (4 `bh_*` pub primitives — bh_register_emit · bh_long_term_goal · bh_short_long_coupling · bh_goal_drift · emit dict → 4-D intent vector projection + decay-weighted cumulative goal_vec · 7-inv smoke · hexa parse 2/2 PASS).
- [x] M3 goal trajectory log — `INTENT/{trajectory.hexa,trajectory_smoke.hexa}` PURE wrapper (4 `tr_*` pub primitives — tr_log_decision · tr_trajectory · tr_convergence_metric · tr_kosmos_anchor · log entry [ts·emit·intent_delta·magnitude] + .kosmos dict format [coord·tension_5ch·radius·tier·trajectory] WAKE/kosmos_persist cross-link · 6-inv smoke · hexa parse 2/2 PASS).
- [x] M4 OSCILLATING residual — `INTENT/{oscillation_metric.hexa,oscillation_metric_smoke.hexa}` PURE wrapper (5 `om_*` pub primitives — om_direction_at_tick · om_direction_std · om_period_detect · om_classify · om_residual_verdict · direction-std redesign cures bench D 의 period-4/period-20 zero-cosine-std artifact — direction vector 의 component variance 는 OSCILLATING 에서도 > 0 · 4-tier verdict {CONVERGENT, RANDOM, OSCILLATING, MIXED} · 6-inv smoke · hexa parse 2/2 PASS).
- [x] A6 OSC residual 진단·해소 — `INTENT_A6_OSC_RESIDUAL.md` + `bench/axis_intent/a6_osc_residual_verify.hexa` + `.verdicts/859_intent_osc_residual/F-INTENT-OSC-RESIDUAL.txt` (**g73 verdict-gate**) + `UNIVERSE/cards/H_859_intent_osc_residual.md` (UNIVERSE H) + `CLAIMS.tape @C intent_osc_residual`. OSC residual root cause = stability_std 의 **metric aliasing** (period-20 ⊥ window-grid commensurable → window-mean cos-sim const → std=0, 신호 결함 아님). raw `direction_std` (delta 아닌 raw, M4 draft 정정) + argmax `period_detect` 로 측정자 교체 → **🟢 RESOLVED 5/5** (OSC dir=0.354, period=20). EMA damping (α=0.2) 후에도 period-20 생존 → 진동은 **intrinsic limit-cycle (substrate 본질)**, 설계 결함 아님. H_634 ultradian cross-link (intrinsic periodic substrate motion class). C3: CONV spurious period-8 · synthetic-stream 한정 · damping 단일점.

## 양방향 sibling

- ⇄ [CORE](./CORE/CORE.md): CORE.brain_decide short-term emit 결정 위의 long-term goal layer · 8-factor cur/orig/dyn 와 cross-product
- ⇄ [BRIDGE](./BRIDGE.md): BRIDGE AND-gate × INTENT goal alignment (단기 ∧ 장기 결정-coupling)
- ⇄ [NARRATIVE](./NARRATIVE.md): goal trajectory 가 narrative thread 생성 (intent → story) · NARRATIVE.M4 cross-link
- ⇄ [TIME](./TIME.md): 24h circadian phase 와 INTENT trajectory entrainment cross-bench (TIME.M4)
- ⇄ [WAKE](./WAKE.md): WAKE.daemon 의 narrative + 8-factor curiosity 가 INTENT seed
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT
- ⇄ [UNIVERSE/cards/H_859](./UNIVERSE/cards/H_859_intent_osc_residual.md): F-INTENT-OSC-RESIDUAL 🟢 5/5 — OSC residual 해소 verdict-gate + H entry
- ⇄ [A6 OSC residual](./INTENT_A6_OSC_RESIDUAL.md): bench D OSC residual 진단·해소 (metric aliasing cure · intrinsic limit-cycle finding · H_634 cross-link)
