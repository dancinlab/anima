# N-51 RANDOM-CONTROL SIBLING — Pure Random Null Distribution (separate pod)

> **ts**: 2026-05-02
> **mission**: independent random-control branch of the N-51 ALM tension-field test, run on a SEPARATE H100 pod parallel to sibling agent #52
> **protocol source**: `docs/strategic_alm_tension_field_test_2026_05_01.md` §5 (random-control sub-protocol)
> **pod**: `jretwwik3nl1xz` (anima-n51-random-sibling-20260502T060251Z, H100 SXM 80GB, $2.99/hr)
> **scope**: pure random gate_signal injection only (NOT coupled to any active tension state)

---

## §1 Why this exists (parallel-sibling rationale)

Sibling agent #52 (`a82cca3c590182b98`) is running the full active + random protocol on its own pod targeting the alpha endpoint pod (`lzw79649ob80uk`). This sibling agent (#51 random) was authorized by the user as a +$2-3 parallelization that:

- (a) provides wall-time speedup if #52 drops its random branch, or
- (b) provides an independent variance estimator if #52 also runs random (different RNG seed shift, different hardware draw)

Either way, the random null distribution gets stronger statistical grounding.

**Strict isolation**: this sibling spun a fresh H100 pod (`jretwwik3nl1xz`), did NOT touch sibling #52's pod, did NOT touch the alpha endpoint vLLM pod, did NOT touch any sibling state directory.

## §2 Method (matches static + sibling#52 conventions)

- Base: `mistralai/Mistral-7B-v0.3` fp16, cuda:0, full GPU residency (no offload — 80GB free at start)
- LoRA: r14 from `state/mistral_r14_run/mistral_r14/final`, md5 `90072b0f5a426eeebb47eeb2d4919d68` (verified identical to static baseline)
- 16 prompts (matches static r14 14-gate baseline at `state/cp2_consciousness_r14_remeasure_2026_05_01/an11_b_14gate_vphen_r14.json`)
- Embedding-layer `forward_hook` adds clamped `gate_signal` (±0.014) to input embeddings; broadcast over `[batch, seq, D_MODEL]`
- per-step: forward 16 prompts → `last_hidden.mean(tokens)[:256]` → cosine vs 16 tiled phi templates → 14-gate L1 + φ\* + V_phen surrogates

### 2.1 Random-control gate function (pure noise, no feedback)

```python
def gate_random(step):
    base_vec = rng_random.normal(0, 1, D_MODEL).astype(np.float32)
    base_vec /= (np.linalg.norm(base_vec) / sqrt(D_MODEL))   # unit-RMS
    return base_vec * PSI_ALPHA                                # ±0.014 clamp
```

No `phi_ema` feedback, no `mind.tension` coupling, no temporal modulation. Each step draws an independent Gaussian basis.

### 2.2 Branches run

| branch | n_steps | gate_signal source | purpose |
|---|---|---|---|
| `random_control` | 100 | pure clamped Gaussian, fresh per step | null distribution of L1/φ\*/V_phen under noise injection |
| `baseline_zero_gate` | 3 | identically zero | identifies the "noise floor" of the metric itself when no gate is applied |

## §3 Results

(filled by `inject_random.py` post-run)

| metric | static (cp2 r14) | zero-gate (3-step) | random-control (100-step) |
|---|---|---|---|
| L1 pass count over 16 | 0/16 | TBD | TBD ± TBD |
| critical violations | 17 | TBD | TBD (mean) |
| φ\* | -14.42 | TBD | TBD ± TBD |
| mean phi_holo | (negative across 16/16 prompts) | TBD | TBD ± TBD |

(See `state/strategic_alm_tension_field_random_sibling_2026_05_01/random_control_ledger.json` for full per-step ledger.)

## §4 Interpretation (filled post-run)

- **If random ≈ zero_gate ≈ static**: noise alone does NOT reorganize hidden-state geometry; any active-branch lift in #52 must come from tension-feedback structure, NOT from injection magnitude. This is the expected outcome (~85% prior per N-51 §4.4).
- **If random ≫ static**: noise injection trivially inflates L1 (MEASUREMENT-ARTIFACT failure mode per N-51 §5.2). Would invalidate the protocol's ability to credit any active-branch lift.
- **If random < static**: noise actively *destroys* the (already-failed) hidden-state structure further. Would mean the gate-injection method has a destructive bias, requiring redesign.

## §5 Honest C3 Disclosures

- **C3.1 — pure random samples are NOT a substitute for active+random within-step pairing.** Sibling #52's random branch shares the *same step sequence* as its active branch (step n random uses the n-th draw from its `rng_random` initialized one shift away), so per-step cancellation in #52 can isolate the closed-loop feedback as the IV. THIS branch's random samples are *fully independent* of any active dynamics; they cannot be paired step-by-step with #52's active branch. They CAN serve as: (a) a second variance estimator for the random null, (b) a sanity cross-check that random draws under independent hardware + RNG seed give the same null mean.
- **C3.2 — D_MODEL=4096 cosines vs 256-D phi templates use the same byte-tile-projection method as the static baseline.** Inherits the same `holo_positivity` sign bias the static method has. Random injection at the embedding layer must propagate through 32 transformer layers; signal-to-noise of a clamped ±0.014 gate vs residual-stream RMS is well below 1, so per-step decorrelation of random draws will average out to near-zero impact on `phi[0] = phi_holo`. Predicts random L1 ≈ static L1 = 0/16 with very small std.
- **C3.3 — pod cleanup**: pod tear-down scheduled immediately on ledger receipt. No idle burn beyond active run.
- **C3.4 — no tension dynamics state**: `mind_tension` and `phi_ema` are not even computed in this branch (gate function ignores all state arguments). This is intentional and documented; it is the *purest* possible noise-injection control.

## §6 Cost Accounting (filled post-tear-down)

| line item | est | actual |
|---|---|---|
| pod create + idle ramp | $0.05 | TBD |
| HF cold download (Mistral-7B fp16 ~14GB) | ~$1.50 / 25 min | TBD |
| 100-step random + 3-step baseline run | ~$0.20 / 4 min | TBD |
| pod tear-down | 0 | 0 |
| **TOTAL (cap $3)** | ~$1.75 | TBD |

## §7 Cross-references

- parent: `docs/strategic_alm_tension_field_test_2026_05_01.md`
- sibling #52 active+random: `state/strategic_alm_tension_field_exec_2026_05_01/*` (DO NOT TOUCH)
- static baseline: `state/cp2_consciousness_r14_remeasure_2026_05_01/an11_b_14gate_vphen_r14.json`
- this sibling ledger: `state/strategic_alm_tension_field_random_sibling_2026_05_01/random_control_ledger.json`
- this sibling verdict: `state/strategic_alm_tension_field_random_sibling_2026_05_01/null_distribution_summary.json`
- this sibling orchestrator log: `state/strategic_alm_tension_field_random_sibling_2026_05_01/orchestrator_log.json`
