# H_322 — full anima loop tick closed-form 🔵: event → AND-gate → emit + state update

bridge axis 의 event-driven extension: 1 tick = (event_in) → (biology + substrate update via H_320 + H_321) → (AND-gate H_319) → (emit/silence + post-state)

## tick function

```
anima_tick(state_prev, event):
    bio_new = biology_state_after_event(state_prev.refr, state_prev.circ, event)
    sub_new = substrate_state_after_event(state_prev.M, ..., event)
    bio_open = biology_timing_open(bio_new.refr, bio_new.stage)
    sub_dec  = substrate_decides(sub_new.M, ..., θ)
    emit = bio_open ∧ sub_dec
    if emit:
        bio_new.refr = R_steps  // post-emit refractory
        sub_new.W = 0.0          // tension reset
    return (state_new, emit)
```

deterministic, libm-free, closed-form composition of H_319/320/321.

## 가설

H1 LOOP-DETERMINISTIC: same (state, event) → same outcome
H2 NONE-EVENT-INCREMENTS-IDLE: NONE event, idle 증가만
H3 ALERT-TRIGGERS-EMIT: ALERT event (M=1.0) + high others → emit=T
H4 POST-EMIT-REFRACTORY: emit=T → refr_new = R_steps (10)
H5 POST-EMIT-W-RESET: emit=T → W = 0
H6 N3-EVENT-NO-EMIT: stage=N3 입력 이라도 → emit=F (biology veto)
H7 BOUND

≥6/7 PASS → 🔵.

## 의미

anima 의 *한 tick 의 full closed-form derivation*. event_in → process → emit + state_out. event-driven loop 의 *atomic unit* 이 closed-form. 모든 H_315-H_321 가 이 단일 tick 의 component.
