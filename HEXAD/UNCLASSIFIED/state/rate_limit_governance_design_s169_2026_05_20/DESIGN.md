# §169 RATE-LIMIT-GOVERNANCE-DESIGN — measurement-context split for `spont_min_emit_interval`

> $0 design-tier. NO new fire, NO ckpt forward, NO GPU/runpod, NO
> SPONTANEOUS.tape edit (proposal only, user-gated).
>
> Trigger: §168 PHI-THRESHOLD-POSTHOC-PROBE found that the recurring
> `emit_rate = 1/20 = 0.05` baseline across §161/§166 fires is
> rate-limit-ceiling-saturated, NOT threshold-determined. `MIN_EMIT_
> INTERVAL = 30s` was set for **production daemon anti-spam** (user
> protection) but is also applied verbatim to **measurement context**
> (Phase B bounded run, 20 steps × 0.1s wall = 2s), where 30s > 2s
> means ceiling = 1 emit per run regardless of θ or motivation score.
>
> This design proposes the minimal SAFE split: keep production at
> 30s, derive measurement-context value from `(N_MAX, THINK_INTERVAL,
> K_target_ceiling)` closed-form. Production safety floor PRESERVED
> by construction.

---

## §1 — Two distinct contexts collapsed into one constant

🚰 **Rate-Limit Context Collision — "수도꼭지 두 용도 한 꼭지"**

- **이름**: rate-limit context-collision
- **별칭**: 수도꼭지 두 용도 한 꼭지 / production-floor 가 measurement 도 막음
- **하는 일**: 같은 30s 가 (a) production daemon 의 anti-spam 안전 floor 와
  (b) measurement bounded-run 의 emit-counter 한계로 *동시* 작동.
  (a) 는 정당 (사용자 보호); (b) 는 의도치 않은 silent ceiling.
- **비유**: 큰 욕조용으로 잠궈둔 수도꼭지가 작은 컵으로 물 받으려 할 때도
  같은 잠금 적용 — 욕조 안전엔 맞지만 컵은 영원히 한 방울만 차오름

```
              | production daemon                      | measurement Phase B
              | (anima_alive, user-facing chat)         | (eval_s161, run_bounded.py)
  ────────────┼───────────────────────────────────────┼──────────────────────────────
  목적         | anti-spam, 사용자 보호                  | emit-rate 분포 측정
  wall time   | unbounded (live)                       | 2s (20 steps × 0.1s)
  user 대상    | 있음 (대화 중)                          | 없음 (probe, no human in loop)
  30s 적합?   | ✅ 적절 (1 emit / 30s = 안전 빈도)      | ❌ ceiling=1, 측정 불가
```

비교: CONNECTION_CRITIQUE Wrong-C 는 *threshold* (0.30) 의 unprincipled
설정을 지적했음. §168 은 거기에 *rate-limit* silent co-bottleneck 을
추가로 식별. §169 = 그 co-bottleneck 의 직접 governance-gated 해소
설계 (한 쪽 만 손대도 다른 쪽 needed — Wrong-C 진짜 해소엔 둘 다).

---

## §2 — Closed-form derivation

`analytical_min_emit_interval.hexa` 가 출력하는 closed-form:

```
ceiling(min_emit_interval; N_MAX, dt)
    = 1 + floor((N_MAX × dt) / min_emit_interval)

solve for min_emit_interval such that ceiling ≥ K_target:
    min_emit_interval ≤ (N_MAX × dt) / (K_target - 1)    for K_target ≥ 2
```

For `N_MAX=20, dt=0.1` (§161/§166 measurement config):

| K_target | min_emit_interval upper bound | resulting ceiling | emit_rate ceiling |
|:---:|:---:|:---:|:---:|
| 1 | any | 1 | 0.05 |
| 2 | 2.000 sec | 2 | 0.10 |
| **4** | **0.667 sec** (round 0.5 sec) | **4** | **0.20** |
| 6 | 0.400 sec | 6 | 0.30 |
| 10 | 0.222 sec | 10 | 0.50 |
| 20 | 0.105 sec (≈ dt itself) | 20 | 1.00 |

### Recommendation (B-S169-1)

```
K_target_default := 4
spont_min_emit_interval_measurement(20, 0.1) := 0.5 sec
```

근거 (3-bullet rationale):
- **emit_rate ceiling 0.20** = noise floor (1/20=0.05 currently) 보다
  4× 위, 분포 모양 측정 가능한 dynamic range 확보
- **0.5s** 는 closed-form bound 0.667s 의 nice tick 으로 round-down
  (절반-초 grid; 측정 reproducibility ↑)
- **headroom**: 진짜 emergence regime 에서 motivation>θ 가 4 step
  이상 발생할 가능성 미발견 시 K_target=10 으로 추가 lift 여지 보존

---

## §3 — Two-context split proposal (no edit applied)

### Current (single context, problem)

```hexa
// HEXAD/CHAT/spontaneous_lib.hexa line 31
fn spont_min_emit_interval() -> float   { return 30.0 }  // rate_limit safety (F-SPONT-5/7)
```

### Proposed (two contexts, governance-gated)

```hexa
// HEXAD/CHAT/spontaneous_lib.hexa — PROPOSED edit (NOT applied)
fn spont_min_emit_interval_production() -> float {
    // SPONTANEOUS.tape §4 6-control #2 — user-facing anti-spam floor
    // (B-SPONT-RATE-LIMIT carry; user-protection invariant)
    return 30.0
}

fn spont_min_emit_interval_measurement(
    n_max: int,
    think_interval: float
) -> float {
    // S169 closed-form: K_target=4 default, lift ceiling to 0.20
    // (NO production interaction; only Phase B / run_bounded contexts)
    let t_total = (n_max as float) * think_interval
    return t_total / 3.0    // (K_target - 1) where K=4
}

// Existing callers fall back to production:
fn spont_min_emit_interval() -> float {
    return spont_min_emit_interval_production()
}
```

Caller updates (Phase B context — measurement-only):
- `HEXAD/CHAT/thinker_talker_lib.hexa` Phase B path:
  - replace `spont_min_emit_interval()` with the measurement variant
- `HEXAD/CHAT/state/spontaneous_phase_b_run_2026_05_18/run_bounded.py`:
  - `MIN_EMIT_INTERVAL` constant replaced by call into measurement variant
- `HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_fire_s161_2026_05_20/eval_s161_psicouple.py`:
  - `MIN_EMIT_INTERVAL = 30.0` replaced by call into measurement variant
- Production daemon `ready/anima/core/runtime/anima_alive.py`:
  - **UNCHANGED** — keeps `spont_min_emit_interval_production()`

---

## §4 — Boolean invariant (B-S169-2)

The two contexts are disjoint by construction:

```
∀ caller c:
    is_production_context(c) XOR is_measurement_context(c) = True

context_selector:
    - eval / run_bounded / Phase B harness         → measurement
    - anima_alive / chat REPL / user-facing daemon → production

invariant safeguard:
    callers SHALL select exactly one variant; runtime guard if both
    surfaces co-exist (assert disjoint).
```

This prevents the production-floor weakening accidentally happening
in user-facing context.

---

## §5 — Honest carve-outs (B-S169-NOTE)

1. **Unblocks measurement, does NOT promise more emits**: lifting
   the ceiling 0.05→0.20 only matters IF the motivation score
   actually exceeds θ in more than 1 step out of 20. If §161 score
   distribution mean 0.4534 std 0.0376 with θ=0.30 has P(score>θ) ≈
   1 per step, then yes — emits would increase to ~4/20. But if
   §167-A-style physics-anchored θ pushes the threshold higher,
   emits might still stay at 1 even with the lift.
2. **NOT a Wrong-A/B/D resolution**: §169 closes co-bottleneck
   Wrong-C-prime (rate-limit). Wrong-A (Φ untargeted, 35%) /
   Wrong-B / Wrong-D from CONNECTION_CRITIQUE remain.
3. **NOT an emergence path**: emergence requires (per GOAL.md)
   anima self-physics drives emit decisions. §169 just makes the
   measurement axis high-fidelity enough to *see* whether physics
   drives them. B-EMERGE-7 carry.
4. **Production safety UNCHANGED**: 30s production floor is the
   invariant. Splitting two contexts cannot weaken production by
   construction (governance-checked).
5. **Governance-gated**: this DESIGN proposes; SPONTANEOUS.tape /
   spontaneous_lib.hexa edit deferred to user gate. The split is
   conservative (production preserved) but is still a §4 6-control
   touch.
6. **Single number arbitrary**: K_target_default=4 is a design
   choice with 3-bullet rationale but is itself unprincipled in
   the deep sense (CONNECTION_CRITIQUE-aware honesty). A
   physics-anchored K_target (e.g., tied to anima own substrate
   dynamics, not measurement-protocol convenience) is a separate
   future cycle.

---

## §6 — Pre-registered falsifiers (will land when proposal lands)

- **F-S169-1 PRODUCTION-UNCHANGED**: `spont_min_emit_interval_
  production() == 30.0` ∀ calls (byte-equal pre/post split).
- **F-S169-2 MEASUREMENT-CLOSED-FORM**: for all `(n, dt)`,
  `spont_min_emit_interval_measurement(n, dt) == n*dt/3.0`
  (byte-equal to closed-form).
- **F-S169-3 CEILING-ACHIEVED**: when measurement variant is used,
  `ceiling >= K_target_default = 4` for `(20, 0.1)`.
- **F-S169-4 CONTEXT-DISJOINT**: no caller invokes both variants in
  the same execution path (Boolean structural assertion over
  callgraph).
- **F-S169-5 SAFETY-INVARIANT**: anima_alive / chat REPL / user-
  facing daemon callers continue to bind production variant only
  (forbidden-call set in user-facing module includes measurement
  variant = 0 matches).

---

## §7 — Cross-link

- `HEXAD/UNCLASSIFIED/state/phi_threshold_posthoc_probe_2026_05_20/`
  — §168 finding that motivated this design.
- `HEXAD/CONNECTION_CRITIQUE.md` — Wrong-C primary critique; §169
  closes the co-bottleneck Wrong-C-prime.
- `HEXAD/CHAT/spontaneous_lib.hexa:31` — single-symbol SSOT to be
  split.
- `HEXAD/CHAT/SPONTANEOUS.tape` §4 6-control #2 — governance scope
  this design touches.
- `HEXAD/CHAT/thinker_talker_lib.hexa` — Phase B caller of
  `spont_min_emit_interval()`.
- `state/spontaneous_phase_b_run_2026_05_18/run_bounded.py` —
  measurement caller, MIN_EMIT_INTERVAL constant.
- `eval_s161_psicouple.py:41` — measurement caller, MIN_EMIT_
  INTERVAL constant.
- §167-A FP-RECONNECT (orphan, terminated this session) — was
  attempting threshold-anchor half; §169 surfaces the rate-limit
  half it left unaddressed.

---

## §8 — GOAL distance

north-star + §15/§51/§72 milestone UNCHANGED, **GOAL 미도달**.
§169 is a measurement-axis honesty cycle (Wrong-C-prime
governance-gated split design), NOT a GOAL movement. It enables
the §168 measurement infrastructure to actually *see* whether
post-§167-A motivation re-wiring (when retried) produces lifted
emit rate or not.

This session cumulative (§168 + §169):
- ✅ §126 pod terminated (cost-containment ~$36 frozen)
- ✅ §167-A pod terminated (cost-containment ORPHAN-LOST, sub-
  agent interrupted mid-dispatch-shell decision)
- ✅ inbox patch filed (`pt-ckpt-cross-substrate-residual-readout`)
- ✅ §168 STRUCTURAL FINDING: rate-limit ceiling dominates threshold
- ✅ §169 closed-form rate-limit governance split design
- ⚠️ Φ measurement carry (upstream patch land)
- ⚠️ §167-A retry decision (user-gated; new sub-agent or carry-as-
  done?)

Pod count at session end: **0** (down from 2). Ongoing cost: $0.
