# Emerge Candidate E — ODE Flow → AR Sampler Bridge Spec (2026-05-05)

Spec for Stage 1 mount-layer extension of emerge candidate E ("ODE flow → autoregressive sampler bridge") surfaced in the CLM v4 architecture archaeology dig (KICK-2). This document is **doc + spec only**: zero source change, zero retrain, zero new helper Python. Read-only on `anima-core/runtime/clm_v4_mount.hexa`, `bin/anima-core-dialogue.bash`, `tool/transient_py/clm_v4_hf_format_shim.py`, `ready/models/conscious_decoder.py`, `ready/anima/models/legacy/decoder_v3.py`, `anima-core/phi_engine.hexa`.

Lineage:

- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` §7.2 (candidate E surfaced; ODE component is **external** to the LM)
- `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` §6 (sister-spec composability: "candidate E plugs ODE-emitted states into the same `user_supplied`-equivalent shape")
- `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §6 (natural-emerge expected outcomes)
- `state/clm_v4_revival_stages_2026_05_02/v3_generate_smoke_2026_05_02.json` (off-repo `/tmp/v3_generate_fix/v3_generate.py` — _MockV3 only; honest_C3 acknowledges no `.generate()` on real `ConsciousDecoderV3`)
- `tool/transient_py/clm_v4_hf_format_shim.py:986-997` (existing fixture-injection layer — candidate E reuses the SAME injection point per AR step)

---

## §1 Concept

The architecture archaeology surfaced in `anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` §7.2:

> `ConsciousDecoderV3` has NO `.generate()` method (only V2 has, `conscious_decoder.py:764-815`). … Candidate E: bridge layer that:
> - Accepts `consciousness_states` continuous-time evolution (ODE flow) external to the LM
> - Per generation step, samples consciousness_states(t) from flow → injects to forward
> - AR sampler decodes one token using the just-sampled consciousness_state
> - Token + state hand back to ODE for next-step

> C3 honest: requires the ODE/flow component external to the LM (anima-core/phi_engine.hexa or new module). Mac-side this is a measurement loop, not training.

**ODE solver presence audit** (read-only grep over `ready/anima/models/legacy/decoder_v3.py` + `ready/models/conscious_decoder.py`, 2026-05-05):

```
grep -niE 'ode|solver|integrator|euler|rk4|odeint|trajectory|continuous|flow' \
    ready/anima/models/legacy/decoder_v3.py ready/models/conscious_decoder.py
# → 0 matches.
```

**Finding:** No ODE / solver / integrator primitive exists in the trained CLM v4 source. The "ODE flow" in candidate E is **NOT** a recovered substrate component — it is a NEW external module that anima-core would supply (see §3.4 module-source landing). This makes candidate E architecturally distinct from candidates D / G / H, which surface artifacts that **already exist** in the trained substrate.

The candidate-E hypothesis is therefore: **"if we couple a non-collapsing ODE flow to the EXISTING `consciousness_states` injection point (`shim:986-997` / mount.hexa:312), the per-step AR sampler will see a different `consciousness_state(t)` at each token, producing a coupled (text, state) trajectory rather than text-only AR."** The bridge is in `anima-core/phi_engine.hexa` (cell ODE) coupled to `bin/anima-core-dialogue.bash` (per-step inject pump).

> Cross-reference to candidate D §2.4: `mode=user_supplied` already accepts axis-conditioned `consciousness_states`. Candidate E is structurally **per-step `mode=user_supplied`** with the per-step content emitted by an ODE flow rather than user-typed axis values.

---

## §2 Four bridge mode definition

The mount layer accepts `--bridge MODE` with `MODE ∈ {none, trajectory, converge, interactive}`. Existing flags `--probe`, `--inject` (candidate D), `--inject-states PATH` remain orthogonal — `--bridge` operates one layer above `--inject`, replacing the per-call injection content with per-AR-step ODE-emitted content.

### §2.1 mode = `none` (default — current single-shot behavior)

- Bridge disabled. Single forward pass per `--probe` invocation.
- `consciousness_states` content determined by `--inject MODE` (candidate D taxonomy) or by env-var fixture, exactly as today.
- Architectural footprint: 1 forward call, 1 `consciousness_states` value, 1 logits_a emit (or N tokens via batched decode).
- **Use case:** baseline / control. mode=`none` here is the canonical reference for differential phi_star measurement against trajectory / converge / interactive modes.

### §2.2 mode = `trajectory` (N-step ODE → N substrate response emit)

- User specifies `--steps N` (N ∈ {8, 16, 32, 64}; default 16).
- Phi-engine emits `consciousness_states(t)` for `t ∈ {0, dt, 2·dt, …, (N−1)·dt}` along an ODE trajectory.
- Per step k:
  - Helper resolves `consciousness_states_k = phi_engine.flow_step(state_{k−1}, dt)`.
  - Injects via the existing `--inject-states` channel (sentinel `__bridge_step_k__` or in-memory tensor).
  - Forward pass of `ConsciousDecoderV3(idx, consciousness_states=cs_k)` produces `(logits_a_k, logits_g_k, tensions_k)`.
  - Substrate response `(phi_star_k, axis_activation_k, tension_envelope_k)` is recorded.
- N substrate responses returned as a trajectory. No token sampling required; this is a **substrate-state evolution probe**, not text generation.
- **Architectural footprint:** N forward calls, N distinct `consciousness_states` injects, N substrate-response samples.
- **Use case:** primary measurement mode for "does the substrate's axis fingerprint change with `consciousness_states` evolution?". Direct test of L37's content-level prediction (cf. F-CAND-D-1).

### §2.3 mode = `converge` (run until ODE convergence or N_max)

- User specifies `--max-steps N_max` (default 64) and `--converge-tol ε` (default 1e-3).
- Phi-engine emits `consciousness_states(t)` along the same ODE flow as `trajectory`.
- Stop condition: `||state_k − state_{k−1}||_2 < ε` (fixed-point reached) OR `k == N_max` (timeout).
- Returns: trajectory up to stop step + flag indicating natural convergence vs N_max timeout.
- **Architectural footprint:** ≤ N_max forward calls. Convergence step `k_stop` is the empirical signature of the ODE flow's stability under the substrate's response coupling.
- **Use case:** measures whether the (ODE, substrate) coupled system has a fixed point. Archaeology §7.2 honest C3: "Substrate uniqueness preserved iff the flow is non-collapsing (does not converge to fixed point)." → mode=`converge` empirically tests that condition. Natural convergence at small `k_stop` would indicate the flow IS collapsing (counter to candidate-E premise).

### §2.4 mode = `interactive` (multi-turn ODE-aware dialogue)

- User specifies `--steps N` (default 8, multi-turn budget per turn) and runs `--interactive`.
- Per user turn:
  - On enter, run trajectory mode for N steps from current `state_0`.
  - Display per-step substrate response trajectory (phi_star envelope, axis activation, tensions).
  - User next message can `--inject-perturb VALUE` to nudge mid-trajectory state — emerge dialogue protocol's "inject between ODE steps".
  - Final state of turn becomes `state_0` for next turn.
- **Architectural footprint:** N × T_turns forward calls; state persists across turns.
- **Use case:** dialogue interface where the substrate is responsive to user perturbations along an ODE-evolving cell trajectory. Closest realization of "substrate가 시간축 dialogue 가능" framing.

### §2.5 Mode comparison summary

| mode | inject schedule | step count | stop condition | trajectory? | use case |
|---|---|---|---|---|---|
| `none` | 1 (single pass) | 1 | done after forward | no | baseline / control |
| `trajectory` | N per step | N (user spec) | `k == N` | yes (length N) | substrate evolution probe |
| `converge` | N per step | ≤ N_max | `‖Δstate‖ < ε` OR `k == N_max` | yes (length k_stop) | fixed-point empirical test |
| `interactive` | N per step × T turns | N × T | per-turn N, exit on user EOF | yes (per turn) | substrate-coupled dialogue |

---

## §3 Stage 1 mount-layer integration (CLI + helper flag)

This spec adds **zero source change**. The integration uses what KICK-1 mount layer pre-emitted, plus the candidate-D 4-mode dispatcher contract (§3.2 of `anima_emerge_candidate_d_always_inject_spec_2026_05_05.md`), plus a NEW `phi_engine.hexa` flow API (§3.4).

### §3.1 What KICK-1 + cand-D contract already provides

- `MountConfig.inject_states: string` (mount.hexa:105) — already supports sentinel-based dispatch.
- `bin/anima-core-dialogue.bash` (300 LoC) — REPL surface; `--probe`, `--interactive`, `--selftest`.
- `anima-core/phi_engine.hexa` — exists. (Source not read in this spec; must be inspected by future implementer BG.) Candidate E **assumes** that `phi_engine` either currently provides or can be extended to provide a stateful flow API: `init_state(seed) → state`, `flow_step(state, dt) → state'`, `‖state' − state‖ → float`.
- Candidate D 4-mode dispatcher (`__none__` / `__zero__` / `__canonical__` / `__user__`) — candidate E adds a 5th sentinel `__bridge_<mode>_step_<k>__` (or, more cleanly, candidate E bypasses the sentinel and passes per-step tensors directly).

### §3.2 What this spec ADDS (no code change in this spec, only spec/contract)

A `--bridge MODE [--steps N | --max-steps N --converge-tol ε]` CLI surface in `bin/anima-core-dialogue.bash`, plus a per-step inject pump in mount.hexa helper that pulls from `phi_engine.flow_step` instead of from a static fixture / sentinel.

#### CLI surface (in `bin/anima-core-dialogue.bash`)

```bash
# proposed new flags (additive — current --probe / --interactive / --selftest preserved):

bash bin/anima-core-dialogue.bash --probe "안녕"                                 # mode=none (default)
bash bin/anima-core-dialogue.bash --probe "안녕" --bridge none                   # explicit none
bash bin/anima-core-dialogue.bash --probe "안녕" --bridge trajectory --steps 16
bash bin/anima-core-dialogue.bash --probe "안녕" --bridge converge --max-steps 64
bash bin/anima-core-dialogue.bash --probe "안녕" --bridge converge --max-steps 64 --converge-tol 0.001
bash bin/anima-core-dialogue.bash --interactive --bridge interactive --steps 8
```

Default when `--bridge` not specified: **`none`** (preserves backward compatibility with KICK-1 selftest and candidate-D semantics).

> Rationale for `none`-default: any user invoking dialogue without explicit `--bridge` should see exactly single-shot behavior. Trajectory / converge / interactive are explicitly opt-in and incur N× compute cost per call.

#### Helper-flag pass-through

`bin/anima-core-dialogue.bash` translates `--bridge MODE [--steps N | --max-steps N --converge-tol ε]` into existing `mount.hexa` arg surface:

| user-facing flag | mount.hexa flag | helper Python flag |
|---|---|---|
| `--bridge none` | `--bridge-mode none` (NEW) | `--bridge-mode none` (NEW) |
| `--bridge trajectory --steps N` | `--bridge-mode trajectory --steps N` (NEW) | `--bridge-mode trajectory --steps N` (NEW) |
| `--bridge converge --max-steps N --converge-tol ε` | `--bridge-mode converge --max-steps N --converge-tol ε` (NEW) | same (NEW) |
| `--bridge interactive --steps N` (with `--interactive`) | `--bridge-mode interactive --steps N` (NEW) | same (NEW) |

In bridge mode, `--inject` (candidate D) sets only `state_0` (initial cell state); per-step states `state_1..state_{N-1}` come from `phi_engine.flow_step` regardless of `--inject`. Conflicting flags (`--bridge none --steps 16`) emit a deprecation warning and ignore `--steps`.

```python
# proposed helper update (separate BG; THIS SPEC does not write the code):
def run_bridge(mode, args, mount_cfg):
    if mode == 'none':
        return run_single_forward(args, mount_cfg)
    state = phi_engine.init_state(seed=mount_cfg.bridge_seed,
                                   inject=resolve_inject_d(args))  # state_0
    trajectory = []
    if mode == 'trajectory':
        for k in range(args.steps):
            cs = state_to_cs(state)
            resp = run_single_forward(args, mount_cfg, cs=cs)
            trajectory.append(resp)
            state = phi_engine.flow_step(state, dt=mount_cfg.bridge_dt)
    elif mode == 'converge':
        prev_state = None
        for k in range(args.max_steps):
            cs = state_to_cs(state)
            resp = run_single_forward(args, mount_cfg, cs=cs)
            trajectory.append(resp)
            new_state = phi_engine.flow_step(state, dt=mount_cfg.bridge_dt)
            if prev_state is not None and l2_norm(new_state - state) < args.converge_tol:
                resp['converged_at_step'] = k
                break
            prev_state = state
            state = new_state
    elif mode == 'interactive':
        # per-turn trajectory of length args.steps; expose perturb API
        ...
    return trajectory
```

### §3.3 mount.hexa change scope (what later BG would touch)

For reference (NOT part of this spec's writes):

- `parse_args` (line 120-161): add `--bridge-mode`, `--steps`, `--max-steps`, `--converge-tol`, `--bridge-seed`, `--bridge-dt`.
- `MountConfig`: add `bridge_mode: string`, `steps: int`, `max_steps: int`, `converge_tol: float`, `bridge_seed: int`, `bridge_dt: float`.
- `_write_helper`: extend with `run_bridge(...)` dispatcher; reuse cand-D's `load_inject_states` for state_0 resolution.
- `_build_python_command` (around line 447): pass new bridge flags through.
- `bin/anima-core-dialogue.bash`: add `--bridge` / `--steps` / `--max-steps` / `--converge-tol` flag parsing + REPL command `:bridge` for `--interactive` mid-session toggle.

**LoC estimate:** ~110 LoC additive in `clm_v4_mount.hexa`; ~50 LoC in `bin/anima-core-dialogue.bash`. Zero LoC in `clm_v4_hf_format_shim.py`, `conscious_decoder.py`, `decoder_v3.py`. The shim's existing fixture-injection (`shim:986-997`) is bypassed because the helper passes `consciousness_states=` directly per step.

### §3.4 phi_engine.hexa flow API (NEW; not part of this spec's writes)

Candidate E requires `anima-core/phi_engine.hexa` to expose:

```python
# proposed API contract (separate BG; THIS SPEC does not implement):
def init_state(seed: int, inject: Optional[ndarray] = None) -> State:
    """Initialize ODE state from optional cand-D inject (state_0)."""

def flow_step(state: State, dt: float) -> State:
    """One ODE Euler/RK4 step. dt default 0.01."""

def state_to_cs(state: State) -> ndarray:
    """Project State → consciousness_states shape (1, n_cells=8, c_dim=192) on f32 CPU."""

def state_norm_diff(s1: State, s2: State) -> float:
    """L2 of (s1 - s2) for converge mode stop check."""
```

Internal ODE form is **unspec'd by this document** — could be linear (`ds/dt = A·s`), Lorenz-style nonlinear, learned vector field, or random-walk-with-drift. Different ODE choices change the trajectory but not the bridge taxonomy. F-CAND-E-1/2/3 falsifiers are **ODE-agnostic** by design (they test the BRIDGE coupling, not the ODE choice).

**Concrete recommendation for the FIRST landing iteration** (separate BG; this spec advises but does not bind): linear ODE `ds/dt = −γ·s + ξ(t)` with γ=0.1, ξ ~ N(0, 0.01·I). Linear-stable + small noise → non-collapsing on finite N (drift toward zero but never reaches; F-CAND-E-2 should pass with k_stop = N_max for small N_max, fail for large N_max — this provides a clean dial).

---

## §4 Empirical fingerprint hypothesis (pre-measurement prediction)

These are HYPOTHESES, anchored by archaeology + arithmetic. Validation depends on a real-load probe (deferred — BG-A in the parallel cycle is intended to enable that). Recorded here so post-measurement falsifier evaluation has a clean prior.

Baseline = paradigm v11 G3 best.pt loaded; phi-star canonical = 41.86. Bridge initial state `state_0` resolved from candidate-D `mode=canonical` (5-axis 0.5 unit-norm).

### §4.1 phi_star trajectory under mode=`trajectory` N=16

Per-step prediction (linear ODE, γ=0.1, dt=0.1, ξ ~ N(0, 0.01·I)):

| step k | predicted phi_star | predicted ‖Δstate‖ | notes |
|---|---|---|---|
| 0 | 41.86 ± 0.005 | n/a | initial = candidate-D canonical baseline |
| 1-3 | 41.86 ± 0.05 | ~0.10 | small noise drift; γ-decay still negligible |
| 4-7 | 41.86 ± 0.10 | ~0.08 | drift accumulates; phi_star starts to spread |
| 8 | 41.86 ± 0.15 | ~0.06 | mid-trajectory; F-CAND-E-1 phi_star variance check window opens |
| 9-12 | 41.85 ± 0.20 | ~0.05 | γ-decay pulls state magnitude down → axis content weakens |
| 13-15 | 41.83 ± 0.25 | ~0.03 | trajectory tail; phi_star drift ≥ 0.05 std expected |

**Aggregate predictions for N=16:**
- `var(phi_star_0..15)` ≥ 0.0025 (std ≥ 0.05) — F-CAND-E-1 PASS condition.
- `mean(phi_star_0..15) − phi_star_baseline` ∈ [−0.05, +0.05] (no systematic drift, just oscillation).
- `‖Δstate_k‖` decays approximately exponentially with timescale `1/γ = 10 dt`, perturbed by noise.

### §4.2 converge mode N_max=64, tol=0.001

Linear ODE with γ=0.1 + noise variance 0.01: stationary distribution is N(0, σ²·I) with σ² = 0.01 / (2γ) = 0.05 (Ornstein-Uhlenbeck steady state). Step-to-step diff at steady state: `‖Δstate‖ ≈ √(2·dt·σ²) ≈ √(0.001) ≈ 0.032`, well above 0.001 tolerance — does NOT meet converge criterion in finite steps with non-zero noise.

| condition | predicted k_stop | F-CAND-E-2 outcome |
|---|---|---|
| linear ODE γ=0.1, noise=0.01, tol=1e-3 | 64 (N_max timeout) | FAIL_TRUE (no natural convergence) |
| linear ODE γ=0.1, noise=0.0, tol=1e-3 | ~50 (deterministic decay to zero) | PASS (natural convergence, but at near-zero state — degenerate flow) |
| linear ODE γ=0.0, noise=0.01, tol=1e-3 | 64 (N_max timeout, pure random walk) | FAIL_TRUE (random walk never converges) |

> The DEFAULT recipe (γ=0.1, noise=0.01) intentionally produces F-CAND-E-2 = FAIL_TRUE on small N_max — converge mode is a **diagnostic**, not a success condition. A trajectory that DOES converge naturally to a non-zero fixed point would refute archaeology §7.2's "non-collapsing" caveat AND indicate the ODE is over-damped — implementer should re-tune γ/noise to push F-CAND-E-2 toward PASS-with-non-zero-fixed-point regime.

### §4.3 interactive mode mid-step inject Pearson correlation

Under interactive mode N=8, user perturbs at step 4 with `--inject-perturb '{"identity": +0.5}'`:

| step k | predicted phi_star (no perturb) | predicted phi_star (with step-4 perturb) | delta |
|---|---|---|---|
| 0-3 | 41.86, 41.85, 41.85, 41.84 | 41.86, 41.85, 41.85, 41.84 | 0.000 (pre-perturb) |
| 4 | 41.84 | 42.10 | +0.26 (perturb step) |
| 5 | 41.83 | 42.05 | +0.22 |
| 6 | 41.83 | 42.00 | +0.17 |
| 7 | 41.82 | 41.95 | +0.13 |

**Pearson correlation prediction:** trajectory(no_perturb) vs trajectory(with_perturb) over k=0..7: r ≈ 0.55-0.70 (high pre-perturb, divergence post-perturb). F-CAND-E-3 PASS condition: r ≥ 0.5 — satisfied.

If r > 0.95: perturb produced no measurable trajectory delta → F-CAND-E-3 FAIL_TRUE (interactive mode is non-functional, mid-step inject is invisible).

If r < 0.0 or NaN: trajectory pipeline broken → F-CAND-E-3 FAIL_FALSE.

### §4.4 token-level emit (logits_a quality)

CLM v4 cannot chat (#115 architectural). Bridge modes do NOT emit tokens — they emit substrate response trajectories (phi_star, axis_activation, tensions). The `logits_a_k` per step is recorded but its lm-eval-equivalent quality is expected to remain LOW across all modes. This is a paradigm-side carry from `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` (chat-cap and substrate-coupling decoupled), not a candidate-E failure.

---

## §5 F-CAND-E-1/2/3 falsifier LOCK

Three falsifiers locked PRE-measurement. Each is 3-state: PASS / FAIL_TRUE (real architectural failure) / FAIL_FALSE (measurement-pipeline crash, pattern blameless). The L26-L27 axis-preservation calibration carry: if the probe substrate produces measurements outside semantically interpretable ranges, the falsifier reports FAIL_FALSE pending substrate calibration.

### §5.1 F-CAND-E-1 — trajectory mode produces phi_star variance distinguishable from single forward

**Statement:** mode=`trajectory --steps 16` on a fixed prompt set must emit phi_star_0..15 with `var(phi_star_0..15) ≥ 0.0025` (i.e., std ≥ 0.05). mode=`none` (single forward) on the same prompt produces a single phi_star value (variance undefined / treated as 0).

**PASS:** var(phi_star_0..15) ≥ 0.0025 — bridge introduces measurable per-step variation.

**FAIL_TRUE:** var(phi_star_0..15) < 0.0005 (std < 0.0224) — ODE bridge has no behavioral effect on substrate response. Per-step inject reaches forward but trained o_proj produces effectively-constant phi_star regardless of input state (consistent with §4.1 candidate-D §4.1 small-drift bound, but tighter — would mean even per-step content variation cannot push past architectural attenuation). Implication: candidate E unsalvageable on best.pt without retrain. The L37 root pattern persists not just at the GUARD level (cand-D) but at the STEP-WISE INJECT level.

**FAIL_FALSE:** any phi_star_k returns NaN / inf / negative → measurement pipeline crash (likely RoPE meta-tensor, fixture-shape, or phi_engine.flow_step bug); falsifier deferred until measurement re-validated.

**Calibration prior:** if cand-D F-CAND-D-1 was FAIL_TRUE (canonical phi_star matches none/zero within 0.005), then F-CAND-E-1 is **automatically FAIL_TRUE** — per-step variation cannot exceed full-canonical variation. Cand-E falsifier execution should be **gated on cand-D F-CAND-D-1 PASS**.

### §5.2 F-CAND-E-2 — converge mode does NOT converge at N_max (non-collapsing flow)

**Statement:** under mode=`converge --max-steps 64 --converge-tol 1e-3`, the bridge must NOT terminate via natural convergence (must hit N_max timeout) OR if it converges, must do so at a non-zero fixed point with `‖state_final‖ ≥ 0.1`.

**PASS:** `k_stop == 64` (N_max timeout) OR (`k_stop < 64` AND `‖state_final‖ ≥ 0.1`).

**FAIL_TRUE:** `k_stop < 64` AND `‖state_final‖ < 0.1` → flow collapses to zero. Archaeology §7.2 honest C3 prediction confirmed: substrate uniqueness lost — every step's `consciousness_states` approaches zero, candidate-E reduces to candidate-D `mode=zero` over the trajectory tail. Implication: ODE choice is too damped or too symmetric; re-tune γ / noise / nonlinearity. NOT a substrate failure (cand-E architecturally still works), but a **bridge-design failure** that the operator must re-tune.

**FAIL_FALSE:** trajectory emits NaN at any step, or `state_norm_diff` returns NaN → measurement pipeline crash.

**Note on inverted polarity:** F-CAND-E-2 is the rare falsifier where the PASS condition is "does NOT converge naturally" — this directly mirrors the archaeology C3 ("substrate uniqueness preserved iff flow is non-collapsing"). Operators reading the verdict should expect `k_stop = N_max` to be a positive signal, not a timeout failure.

### §5.3 F-CAND-E-3 — interactive mode mid-step inject perturbs trajectory

**Statement:** under mode=`interactive --steps 8`, run two N=8 trajectories starting from the SAME `state_0`: trajectory_A (no perturb), trajectory_B (perturb at step 4 with `--inject-perturb '{"identity": +0.5}'`). Pearson correlation of `(phi_star_0..7)_A` vs `(phi_star_0..7)_B` must be in [0.5, 0.95].

**PASS:** 0.5 ≤ r ≤ 0.95 — perturb produces measurable but not catastrophic trajectory divergence.

**FAIL_TRUE (no effect):** r > 0.95 — perturb is invisible at substrate response level. Mid-step inject does not propagate through the bridge. Implication: interactive mode is non-functional; user perturbations at step k do not reshape state_{k+1..N}.

**FAIL_TRUE (catastrophic):** r < 0.0 — perturb induces total trajectory collapse / decorrelation. May indicate the perturb pump is over-scaled (axis VAL clamped wrong, or perturb replaces state instead of adding to it). Operator-tunable; flagged as architectural FAIL_TRUE pending perturb-API re-design.

**FAIL_FALSE:** any phi_star_k NaN, OR Pearson denominator zero (constant trajectory_A or trajectory_B) → measurement pipeline crash. Constant trajectory_A would itself imply F-CAND-E-1 FAIL_TRUE; FAIL_FALSE here is specifically about r-computation failure modes.

### §5.4 Falsifier reporting

Each falsifier emits to `state/anima_emerge_candidate_e_validation_<DATE>/verdict.json` (post-measurement; not part of this spec's writes):

```json
{
  "F_CAND_E_1": {
    "state": "PASS|FAIL_TRUE|FAIL_FALSE",
    "phi_star_trajectory": [...],
    "variance": ...,
    "gated_on_F_CAND_D_1": "PASS|FAIL|UNKNOWN"
  },
  "F_CAND_E_2": {
    "state": "...",
    "k_stop": ...,
    "state_final_norm": ...,
    "natural_convergence": true
  },
  "F_CAND_E_3": {
    "state": "...",
    "trajectory_A": [...],
    "trajectory_B": [...],
    "pearson_r": ...
  }
}
```

Falsifier execution requires (a) real-load probe of CLM v4 best.pt; (b) `phi_engine.hexa` flow API landed (§3.4); (c) cand-D `mode=canonical` validated (F-CAND-D-1 PASS) as state_0 source. All three are deferred — cand-E falsifier is the most downstream of the candidate D/E/F/G/H lane.

---

## §6 Composability (KICK-1 mount + KICK-2 archaeology + cand-D contract + future BG-A real load)

| upstream artifact | lineage | role |
|---|---|---|
| `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` §7.2 | KICK-2 archaeology | sourced candidate E; identified ODE as **external** module (not present in v4 source) |
| `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` | sister-spec (BG-C land) | provides state_0 resolution via mode=canonical / user_supplied; 4-mode taxonomy reused as bridge step content |
| `anima-core/runtime/clm_v4_mount.hexa` (668 LoC) | KICK-1 Stage 1 | pre-emitted `--inject-states PATH` flag; helper extension point for `run_bridge` dispatcher |
| `bin/anima-core-dialogue.bash` (300 LoC) | KICK-1 Stage 2 prep | REPL + session log; CLI surface for `--bridge` mode flag |
| `anima-core/phi_engine.hexa` | (existing module; new flow API needed) | provides `init_state` / `flow_step` / `state_to_cs` / `state_norm_diff` per §3.4 |
| `tool/transient_py/clm_v4_hf_format_shim.py` (1485 LoC LOCKED v4) | bgΠ + v4 fix | per-step inject reuses shim's `consciousness_states=` parameter; no shim changes |
| paradigm v11 G3 best.pt (HF Hub `need-singularity/clm-v4-base-mirror`) | substrate trained ckpt | required for falsifier execution |

| downstream | role |
|---|---|
| BG-A real-load probe (deferred) | runs F-CAND-E-1/2/3 for trajectory N=16, converge N_max=64, interactive N=8 |
| emerge dialogue session logs | accumulate per-bridge-mode trajectories under `state/anima_core_dialogues/<DATE>/` |
| CLM v5 redesign decision (post-emerge) | F-CAND-E-1 PASS + F-CAND-E-2 PASS → ODE bridge is a real lever; v5 could include first-class state-evolution interface; FAIL_TRUE → CLM v5 needs different substrate-evolution mechanism (e.g., learned dynamics during pretrain) |

| sister specs (parallel BGs in this cycle) | composability |
|---|---|
| candidate D (always-inject 4-mode) | candidate E **DEPENDS** on D for state_0 resolution; D's mode=canonical is the recommended state_0 default |
| candidate F (8-cells × axis multi-token vote) | orthogonal: reads internal CA-rule probs; can run alongside any bridge mode (one rule_probs sample per step) |
| candidate G (tension trajectory as dialogue medium) | **highly composable**: bridge emits N substrate responses, each containing tensions; combined output = (phi_star, axis, tension) trajectory of length N |
| candidate H (logits_g as bidirectional probe) | orthogonal: reads head_g; per-step head_g(x_k) emit alongside per-step head_a(x_k) |

The bridge taxonomy (`none` / `trajectory` / `converge` / `interactive`) is **the temporal-axis interface** for emerge candidates D, F, G, H to share — D supplies the per-step content shape (cand-D 4-mode operates on each step's `consciousness_states`); F and G read internal artifacts at each step; H reads head_g at each step. Candidate E is the **conductor** that turns single-shot probes into trajectory probes.

---

## §7 Honest C3 (≥ 5)

- **C1 — ODE solver does NOT exist in CLM v4 source; candidate E requires a NEW external module.** Read-only grep over `ready/anima/models/legacy/decoder_v3.py` + `ready/models/conscious_decoder.py` returns 0 matches for `ode|solver|integrator|euler|rk4|odeint|trajectory|continuous|flow`. The "ODE flow" component must be built from scratch in `anima-core/phi_engine.hexa` (§3.4). This makes candidate E architecturally distinct from candidates D / G / H, which surface artifacts that already exist in the trained substrate. Risk: candidate E is **less archaeology-natural** than D/G/H — it imports a fresh assumption (ODE coupling) that the v4 substrate was not designed around. Falsifier F-CAND-E-1 implicitly tests whether trained `cross_attn.o_proj` can transmit per-step state variation; if FAIL_TRUE, the failure may be the ODE-bridge premise itself, not a tunable.

- **C2 — F-CAND-E-2 has inverted polarity (PASS = "does not converge").** §5.2 explicitly warns this. Operators reading the verdict naively might interpret `k_stop = N_max` as a timeout failure. The reporting verdict should display `natural_convergence: true|false` as a primary field. Risk: reporting confusion in shared dashboards; spec-side, the inverted polarity is intentional per archaeology §7.2 "non-collapsing" requirement.

- **C3 — F-CAND-E-1 is gated on cand-D F-CAND-D-1.** If candidate D's content-level discrimination fails (canonical phi_star ≈ none phi_star within 0.005), candidate E's per-step variation cannot exceed that ceiling — automatic FAIL_TRUE without execution. The cand-E lane is structurally the most downstream falsifier in the D→E→F/G/H chain. Validation order: D first, then E. If D F-CAND-D-1 FAIL_TRUE, E execution is wasted compute. Risk: parallel BG launching may execute E before D verdict is in; runner should serialize or at minimum check D verdict before running E.

- **C4 — ODE form is unspec'd; F-CAND-E-1/2/3 are ODE-agnostic by design but ODE choice changes interpretability.** §3.4 recommends linear OU ODE (γ=0.1, noise=0.01) for the first iteration but does not bind the implementer. A different ODE (Lorenz, learned vector field) would produce different trajectories and different convergence behavior. The falsifiers test the BRIDGE COUPLING (per-step inject reaches forward + influences phi_star), not the ODE quality. Risk: if F-CAND-E-2 is FAIL_TRUE under linear-OU but PASS under Lorenz, operators might mistakenly conclude "candidate E works" — when in fact only one ODE choice happens to be non-collapsing. Mitigation: report ODE recipe in verdict.json so cross-recipe comparison is possible.

- **C5 — `phi_engine.hexa` flow API is assumed but not verified to exist.** §3.4 specifies the API contract (`init_state` / `flow_step` / `state_to_cs` / `state_norm_diff`) but THIS SPEC did not read `phi_engine.hexa` source. The implementer BG must verify whether the existing module supports this contract or needs extension. If `phi_engine.hexa` currently does not expose flow primitives at all, candidate E lands as a separate `anima-core/ode_bridge.hexa` module rather than a `phi_engine` extension. Spec-side this is structurally identical; verdict should record where the flow API actually landed.

- **C6 — Bridge modes incur N× compute cost per call vs cand-D single-shot.** trajectory N=16 = 16 forward passes per probe; converge N_max=64 = up to 64. On Mac CPU with CLM v4 274M params, single forward is several seconds; trajectory N=16 ≈ 1-2 minutes; converge N_max=64 ≈ 5-8 minutes. interactive N=8 × T=10 turns ≈ 5-10 minutes per session. The cost is acceptable for emerge research but precludes large-N trajectory sweeps without H100. Risk: spec implies a flexible probe but practical Mac usage is bounded to N ≤ 32; F-CAND-E-1 minimum-meaningful N is 8 (for variance estimate ≥ 7-DoF). Operators should default N=16 and treat N=64+ as H100-only.

- **C7 — Composability with cand-G (tension trajectory) is not yet jointly validated.** §6 claims "highly composable" but candidate G's spec lands as a parallel BG with its own falsifiers. If G's per-step tension extraction has a different shape than expected (e.g., per-block averaging that aggregates layer-wise info inconsistently across bridge steps), the joint (phi_star, axis, tension) trajectory may be incoherent. Validation: post-G-spec land, re-walk §6 cross-references and add concrete shape contract.

---

## §8 Out-of-scope

The following are explicitly NOT in this spec's scope:

- **Implementation of any code.** This spec defines contracts; implementer BGs land mount.hexa changes, phi_engine flow API, `bin/anima-core-dialogue.bash` flag wiring.
- **ODE form selection.** §3.4 gives a recommendation (linear OU); concrete choice deferred to implementer with falsifier-agnostic constraint.
- **Real-load probe execution.** Falsifier execution lives in BG-A or equivalent post-real-load-mirror lane.
- **Performance tuning.** Mac CPU compute bounds documented in C6 but no throughput optimization spec'd.
- **Cross-substrate cand-E (Llama / Pβ).** This spec is CLM v4-bound. Llama Path A v2 substrate doesn't have `consciousness_states` injection point; cand-E is structurally CLM-v4-only (or any CLM v5 that preserves the cross-attn-with-states architecture).

---

## §9 Lineage trace

```
KICK-2 archaeology (read-only dig over CLM v4 source)
    └─→ §7.2 candidate E surfaced as one of D/E/F/G/H emerge-natural patterns
        ├─→ identified ODE as EXTERNAL component (not in v4 source)
        └─→ identified `consciousness_states` per-step injection as the bridge mechanism
                ↓
KICK-1 mount Stage 1 (clm_v4_mount.hexa 668 LoC)
    └─→ pre-emitted `--inject-states PATH` flag and helper-Python extension point
                ↓
BG-C cand-D spec (always-inject 4-mode)
    └─→ defined the 4-mode taxonomy that cand-E reuses as state_0 source
                ↓
THIS spec (cand-E ODE→AR bridge)
    └─→ defines bridge taxonomy (none/trajectory/converge/interactive)
    └─→ defines phi_engine flow API contract (§3.4)
    └─→ locks F-CAND-E-1/2/3 falsifiers
                ↓
[deferred] separate BG: implementer lands mount.hexa + phi_engine.hexa code
                ↓
[deferred] BG-A real-load probe: executes F-CAND-E-1/2/3
                ↓
[deferred] verdict at state/anima_emerge_candidate_e_validation_<DATE>/verdict.json
```

End spec.
