# H_9129 INTEGRATED rung-3 — PRE-REGISTRATION (frozen before measurement · tune-to-green banned)

**Lane:** integrated 3-component = **L1 PFC variable-binding × L2 basal-ganglia content-gate × L5 hippocampal completion**.
rung-2 was DIRECTIONAL (real 303M reps, reach 0.236 vs unreach 0.023, all 3 ablations causal, centering load-bearing, byte-EXACT Δ=0) — capped DIRECTIONAL because **un-wired**. rung-3 = live `core/` wire + engine-native re-measure + disjoint proof.

## Wire (additive-only `core/`)
- **L1** `core/wm_bind_lane.py` (HRR bind/unbind/superpose/cleanup) + hexa twin `core/kosmos_io.hexa::wmbind_*` (FFI-free).
- **L2** `core/content_gate_lane.py` (Go/NoGo value/admit) + hexa twin `core/kosmos_io.hexa::cgate_*`.
- **L5** REUSE already-GREEN `core/hippo_lane.py` + `core/kosmos_io.hexa::hippo_*` (#2996) verbatim.

## Task (engine-native, `anima evaluate --py` rep path, a_eval_py_canonical)
Base ckpt `~/anima-weights/bytegpt303_h1129/h1129.bin`. Real corpus concept co-occurrence chains (identical builder to L5 discriminator). Item KEYS = real ByteGPT-303M reps via `core/decode.py` (== `--py` 2-production ops).

**3-stage pipeline producing relatedness(i,j):**
1. **L2 content-gate** picks WHICH edges enter the store from a candidate pool = genuine adjacent premise edges (real co-occurrence strength, c≥3) **+** an equal number of DISTRACTOR cross-chain edges (real strength, ≈0). Admit iff `grounding_value(strength, E_SCALE) > NOGO`.
2. **L1 PFC bind** builds each item key by binding its position-role into the rep (`key = DG(center_zscore( role[pos] ⊛ unit(rep) ))`) — variable-binding disambiguation.
3. **L5 hippo** heteroassociative store `W=Σ outer(key_nxt,key_cur)` over admitted edges + multi-step CA3 completion (STEPS).

## Frozen hyperparameters (locked)
`SEED=20260705 · N_CHAINS=8 · CHAIN_LEN=6 · DIM=2048 · ACTIVE=40 · STEPS=6 · KWTA=40 · NOGO=0.30 · E_SCALE=6.0 · PREPROC=center_zscore`. Distractor count = genuine edge count. No per-eval re-fit of any threshold.

## Pair sets (held-out)
- **reach** = same-chain non-adjacent (gap≥2), NEVER a stored edge → needs L1 keys + L2-clean store + L5 multi-step chaining.
- **unreach** = cross-chain pairs, form-matched → chance floor (rises if L2 admits distractors).

## Ablations (each must be CAUSAL — OFF collapses)
- **L1-OFF**: no role bind (`key = DG(center_zscore(rep))`) → variable-binding removed.
- **L2-OFF**: admit ALL candidates incl. distractors → store polluted.
- **L5-OFF**: STEPS=1 (single-hop only) → non-adjacent unreachable.
- **RAW** (centering control): PREPROC=raw → anisotropy collapses codes (expect reach→~0).

## Frozen bars (pre-registered · verdict decided by these, not tuned)
- **GREEN-WIRED (faculty scope)** ⟺ `reach − unreach > 0.15` (rung-2 gap 0.213) **AND** each of L1/L2/L5-OFF drops the gap by ≥50% (all 3 CAUSAL) **AND** RAW collapses (centering load-bearing) **AND** byte-parity hexa⟷py on the fixture **AND** ON==OFF generation byte-identical (additive, new files unimported by emit) **AND** enforce_anima_gates CLEAN **AND** LIVE-OP reproduces (measurement calls the live `core/` ops).
- **DIRECTIONAL** ⟺ gap>0.15 but a component INERT (ablation doesn't collapse) or a wire clause open.
- **WALL** ⟺ gap ≤ 0.15 (no held-out lift).

## Honest scope (a_scale_honest_scope · MANDATORY)
Like L5: even at GREEN this is an **explicit-store combo FACULTY over real 303M reps** — the binding ALGEBRA (HRR) and the RELATION structure (corpus co-occurrence graph) are injected; it is **NOT** a proof the 303M trunk itself composes (that is γ trained-constructive-bind, out of scope). by-construction (HRR + D-capacity) avoidance = keys are real trunk reps, distractor rejection uses real grounding, held-out reach pairs are never stored. The G1 trunk-recombination wall is UNTOUCHED.
