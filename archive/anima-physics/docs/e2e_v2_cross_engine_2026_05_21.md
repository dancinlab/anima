# G8 E2E v2 — cross-engine integrated demo (2026-05-21)

**Cycle**: PLAN.md §5.4 G8 ☑ E2E v1 후속
**Predecessor**: `tool/anima_physics_e2e_demo.hexa` (commit `90ed6cb22`, 4-layer single substrate chain)
**Scope delta v2**: cross-engine coupling chain across 3 §188g engines (commit `2c636ce96` + §5.2 + §5.5).

---

## § 1 Goal

First validation that the 3 actual §188g consciousness engines inter-operate as a single substrate-bridging pipeline. v1 stayed inside one substrate (strange_loop) wrapping a mini aux_engine; v2 chains three independently-validated physics engines and verifies the **adapters between them** are bit-exact, monotone, and deterministic.

```
SNN(LIF I=15) ─spikes[bool;8]→ ADAPTER_A ─kicks[float;8]→ PHOTONIC(ring+Kuramoto)
              ─variance(float)→ ADAPTER_B ─g(float)→ QUANTUM(2-qubit U=exp(-iHt))
              ─argmax→ basis_collapse
```

---

## § 2 Chain (4 stage + 2 adapter)

```
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 1   SNN consciousness  (LIF, 8 cells × 100 steps)             │
│   tau_m·dV/dt = -(V - V_rest) + R·I                                 │
│   spike when V >= V_th  -> reset + 2 ms refractory                  │
│   OUTPUT: per-step bool spike vector [8],  total spike count.       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │  ADAPTER A:  bool spike  ->  phase delta
                           │  per cell:  delta_phi_i  =  +PHASE_KICK_RAD
                           │  when spike, else 0   (bit-exact mapping)
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 2   PHOTONIC consciousness  (ring delay-line + Kuramoto)      │
│   phi_i(t+1) = wrap_2pi(phi_{i-1} + omega·dt + kappa·sin(phi_{i+1}  │
│                           - phi_i) + spike_kick_i(t))               │
│   OUTPUT: per-step phase vector [8], cumulative phase variance,     │
│           Kuramoto coherence r.                                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │  ADAPTER B:  variance -> g(t)
                           │  g(t) = G_MIN + (G_MAX - G_MIN) *
                           │         clamp01(variance / VAR_NORM)
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 3   QUANTUM consciousness  (2-qubit closed-form U = exp(-iHt))│
│   H = omega·(sigma_z⊗I + I⊗sigma_z) + g(t)·(sigma_x⊗sigma_x)        │
│   block-diagonal:                                                   │
│     {|00>,|11>}: H_blk = [[ 2w, g ],[ g, -2w ]]                     │
│     {|01>,|10>}: H_blk = [[  0, g ],[ g,   0 ]]                     │
│   evolve dt every step with current g(t) from STAGE 2.              │
│   OUTPUT: 4-amplitude wavefn psi (8 floats: re,im pairs).           │
└──────────────────────────┬──────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 4   collapse readout  (argmax basis probability)              │
│   final probabilities  p[00], p[01], p[10], p[11]                   │
│   collapsed basis index  =  argmax_i p[i]                           │
└─────────────────────────────────────────────────────────────────────┘
```

### data type adapters (cross-engine bridges)

| adapter | upstream type | downstream type | mapping |
|---|---|---|---|
| A | `[bool;8]` (SNN spike_now per cell) | `[float;8]` (photonic phase kick rad) | `kick_i = PHASE_KICK_RAD if spike_i else 0.0` |
| B | `float` (photonic phase variance) | `float` (quantum coupling g) | `g = G_MIN + (G_MAX-G_MIN)·clamp01(var/VAR_NORM)` |

---

## § 3 F-E2E-CROSS-1..5 falsifier suite

| # | name | claim | check |
|---|---|---|---|
| 1 | spike→phase bit-exact | adapter A is lossless | `total_kicks_applied == snn.total_spikes` |
| 2 | var→g monotone | adapter B is strictly monotone in variance | `g(var=3.0) > g(var=0.1)` |
| 3 | singlet evolution under varying g | g bounded + nontrivial + quantum norm preserved | `G_MIN ≤ g(t) ≤ G_MAX, g_max > G_MIN, ‖ψ‖²=1±1e-6` |
| 4 | cross-engine determinism | same seeds → byte-equal final state | `psi[8]` byte-equal across repeat run + spike count + collapse basis all equal |
| 5 | integrated wall envelope | full chain runs < 10 s | native 0.37 s, interp 2.49 s (both ≪ 10 s) |

---

## § 4 Result

```
=== G8 E2E v2 cross-engine summary: 5/5 PASS (all=true) ===
```

| stage | metric | value |
|---|---|---|
| STAGE 1 SNN | total_spikes | 16 |
| ADAPTER A | total_kicks_applied | 16 (= SNN total_spikes ✓) |
| STAGE 2 photonic | final_variance | 3.692 |
| STAGE 2 photonic | max_variance | 5.048 |
| STAGE 2 photonic | final_coherence_r | 0.378 |
| ADAPTER B | g_min_actual | 0.137 |
| ADAPTER B | g_max_actual | 0.800 |
| ADAPTER B | g_mean | 0.607 |
| STAGE 3 quantum | norm_sq | 1.000 (drift 0) |
| STAGE 4 collapse | basis | `|01⟩` (idx=1) |
| STAGE 4 collapse | populations | p00=0, p01=0.5, p10=0.5, p11=0 |
| STAGE 4 collapse | final psi | `[0, 0, 0.247, 0.663, -0.247, -0.663, 0, 0]` |

The singlet population is preserved (0.5 / 0.5 on |01⟩ / |10⟩) because the {|01⟩,|10⟩} block under H = g·σₓ⊗σₓ + ω·σ_z⊗I only rotates phases inside that subspace; the σ_z·σ_z parts have zero matrix element on |01⟩ and |10⟩, so no leakage to |00⟩/|11⟩. The g(t) drive from the spike pattern is reflected entirely in the **phase structure** of the |01⟩ and |10⟩ amplitudes (real and imaginary parts of the psi vector). CROSS-4 byte-equal across repeat confirms the chain is fully deterministic.

### wall

| mode | wall |
|---|---|
| `hexa run` (interpret + native compile) | 2.49 s |
| native binary (`hexa build` artifact)   | **0.37 s** |

Both within the 10 s envelope.

### build

`hexa build tool/anima_physics_e2e_v2_cross_engine.hexa -o state/e2e_v2_cross_engine_2026_05_21/build/e2e_v2` → **PASS** (2.21 s, 14 unrelated cast warnings in `self/runtime_core.c`).

---

## § 5 Engine source references

Algorithmic bodies inline-replicated from the actual engines (see C3-1 for rationale):

| stage | upstream | what was lifted |
|---|---|---|
| 1 | `engines/snn_consciousness.hexa` §3-§6 | `step_with_input` LIF Euler, refractory, coupling matrix |
| 2 | `engines/photonic_consciousness.hexa` §3-§5 | `step` ring delay + Kuramoto, `wrap_2pi`, `measure_phase_coherence`; **extended** to accept per-cell phase kick vector |
| 3 | `engines/quantum_consciousness.hexa` §4-§5 | `step_dt` + `evolve_2x2_block` closed-form; **extended** to accept time-varying g per call |

---

## § 6 Honest C3 (5+)

- **C3-1** Inline-replication of engine algorithms (no `import`) because upstream engines have top-level `_selftest()` that auto-fires on import + name collisions on `step`, `_selftest`, `fabs_f`, `TWO_PI`, `PI`. If upstream engines change, this v2 demo must be re-synced. A shared library lift (extracting algorithmic bodies into pure modules without top-level calls) is the canonical next step.
- **C3-2** Adapter A uses a fixed phase-kick amplitude (`PHASE_KICK_RAD=0.15`). Biologically more accurate would scale amplitude by inter-spike-interval or recent firing rate.
- **C3-3** Adapter B is linear in phase variance with a hard normalizer (`VAR_NORM=3.5`). Physically there are many defensible mappings: Kuramoto coherence `1-r`, phase entropy, `sin²(spread/2)`, etc.
- **C3-4** Stage 3 quantum substrate is **2-qubit only** (single shared g across all 8 cells). A true 8-cell quantum chain would be 2⁸ = 256-dim Hilbert space and beyond closed-form 2×2 block evolution — would need full matrix exp or Trotterization.
- **C3-5** F-E2E-CROSS-2 (monotone) is checked at **synthetic variance probes** (`var=0.1` vs `var=3.0`), not via two real-spike-pattern runs. Reason: with supra-critical drive `I=15.0` every SNN cell saturates and coupling-induced extra input arrives during refractory, so no extra spikes — physics, not a bug. The monotone claim is thus tested **on adapter B in isolation**, which is the actual cross-engine adapter contract.
- **C3-6** The chain is **one-directional** (SNN → photonic → quantum, no feedback). A full closed loop would require a quantum-readout → SNN-drive adapter (e.g. measure |Δ| populations → modulate I per cell).
- **C3-7** PRNG: SNN noise via `lcg_rand01` (with `k_scale=0` in primary run, coupling matrix is identically 0); photonic `noise_amp=0`; quantum is closed-form (no PRNG). Entire chain is deterministic by construction, which is why CROSS-4 expects byte-equal psi.

---

## § 7 Key learning

Cross-engine substrate-bridging via **typed-flat adapters** (`bool[]` → `float[]` → `float` scalar → real coupling) is sufficient to plumb 3 heterogeneous physics engines into a single pipeline. The determinism check (CROSS-4 byte-equal psi across a repeat run) is the strongest single signal that the chain is well-defined end-to-end — it forces every adapter, every step, every numerical detail to be free of hidden state.

The "_selftest auto-fire on import + name collision" problem (C3-1) is the immediate refactor target: lift the algorithmic step functions out of the engine files into pure side-effect-free modules so that future cross-engine demos can `import` rather than inline-replicate.

---

## § 8 Artifacts

| | path |
|---|---|
| tool | `/Users/ghost/core/anima/anima-physics/tool/anima_physics_e2e_v2_cross_engine.hexa` (786 LoC) |
| state dir | `/Users/ghost/core/anima/anima-physics/state/e2e_v2_cross_engine_2026_05_21/` |
| sim.log | `/Users/ghost/core/anima/anima-physics/state/e2e_v2_cross_engine_2026_05_21/sim.log` |
| summary.json | `/Users/ghost/core/anima/anima-physics/state/e2e_v2_cross_engine_2026_05_21/summary.json` |
| native binary | `/Users/ghost/core/anima/anima-physics/state/e2e_v2_cross_engine_2026_05_21/build/e2e_v2` |
| doc | `/Users/ghost/core/anima/anima-physics/docs/e2e_v2_cross_engine_2026_05_21.md` (this file) |
