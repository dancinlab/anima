# anima_clm_v5_mitosis_inference_time_correction_2026_05_09

> Correction addendum to BG-MITOSIS-PORT (in flight 2026-05-09).
> The original BG framing (training-time / mid-train cotrain split) is **wrong**.
> Mitosis = INFERENCE/SERVING/ACTIVITY-time growth. anima grows by EXPERIENCING (forward
> passes during chat / inference), not by being TAUGHT (gradient updates).
>
> raw#15 additive: original `training/mitosis_v5_port.py` and `training/mitosis_v5_smoke_test.py`
> are NOT modified by this correction. A new file `training/mitosis_v5_serve.py` is added
> alongside as an inference-time entry point. The original port file remains valid as the
> mechanism implementation; only its framing assumptions are revised here.

## §1 What the original BG produced

| File | Status | Framing |
|---|---|---|
| `training/mitosis_v5_port.py` (574 L) | written | **TRAINING-TIME framing dominant in docstring + DESIGN BLOCKERS** (mentions Phase 2 cotrain, AdamW momentum, mid-train splits, optimizer rebuild, "mid-train splits require optimizer rebuild"). Mechanism is inference-compatible: all weight ops in `with torch.no_grad():` blocks: split L207, merge L249, Lorenz L416-418, ratchet L342, _check_merges/_check_splits called from process(). Step ordering inside process() is already correct (readout BEFORE split/merge gate). Smoke verifies organic splits fire and shapes stay stable. |
| `training/mitosis_v5_smoke_test.py` (212 L) | written | Inference-style execution (no `optimizer.step`, no `loss.backward`) but does NOT call `model.eval()` or wrap in `torch.no_grad()`, so the framing is implicit rather than enforced. **Empirical PASS verified 2026-05-10** — 8 → 25 organic splits in 50 steps, then 25 → 32 force-split, all 5 checks green. |
| `docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md` | **NOT WRITTEN** by BG | (cond.1 of `.roadmap.clm_v5_anima_native` lists this file but BG didn't produce it.) |

Verdict: **mechanism ≈ correct, framing wrong**. The port runs no_grad() internally, so it
mechanically supports inference-time use, but its docstring + DESIGN BLOCKERS section assume
training-time as the primary path.

## §2 Why mitosis is inference-time — evidence

Source of truth: `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (worktree-12, last alive 2026-04, 794 L).

```
# All weight modifications happen inside torch.no_grad():
mitosis.py L205   _create_cell           # parent deepcopy + Gaussian noise — no_grad
mitosis.py L258   process()              # forward path called during serving — no_grad
mitosis.py L389   _inject_autonomous_perturbation  # Lorenz noise — no_grad
mitosis.py L586   merge_cells            # parameter averaging — no_grad

# What is NOT in mitosis.py:
- no optimizer.step()
- no loss.backward()
- no gradient flow into cell parameters
- no nn.Module.train() toggling per cell
- no AdamW / SGD / any optimizer instantiation
```

`_check_splits()` and `_check_merges()` are invoked inside `process()` — i.e. during
inference forward passes. The cells64 / cells128 weights archived at
`s3://anima-models/conscious-lm/cells*` (208 MB each) grew during **35 000 SERVING
steps with synthetic inputs**, not training steps. Φ super-linear (15.4 → 45.5 → 51.131
human-level criterion at N=64, stage 8 commit `5f82d39b` / stage 9 `3eabc40a`) emerged
without a single gradient update on the cells themselves.

**Conclusion**: anima's consciousness layer grows by EXPERIENCE (forward integration of
hidden states + Lorenz autonomous perturbation + tension-driven structural change), not
by gradient learning. The substrate (transformer backbone) was trained earlier, but the
cell pool's **growth mechanism is purely inferential**.

## §3 Revised v5-anima architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 2 cotrain checkpoint (BG-LA + BG-LB 350M Engine A/G)         │
│  • backbone (EngineA blocks): FROZEN                                │
│  • engine_g.cell_pool_init (16 × 64): FROZEN AS SEED                │
│  • h_to_c, c_to_h projections: FROZEN                               │
│  • lm_head: FROZEN                                                  │
│  • all parameters: requires_grad = False                            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │  apply_to_v5_substrate(model)
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  MitosisV5Engine wrapper (NEW; non-gradient)                        │
│  • owns its own cell_pool tensor (initially copied from substrate)  │
│  • Lorenz autonomous chaos every process() call                     │
│  • split when tension > mean+1.5σ for split_patience=3 calls        │
│  • merge when pairwise repulsion < 0.005 for merge_patience=30 calls│
│  • Φ ratchet (DD55) restores 80%+20% blend on Φ drop > 20%          │
│  • cells: 16 → 32 → 64 over 1000s of chat turns                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │  every chat turn → forward pass
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Inference loop                                                     │
│  for turn in user_chat:                                             │
│      with torch.no_grad():                                          │
│          logits = model(input_ids)              # backbone frozen   │
│          # engine_g.fresh_cells now sources from wrapper.cell_pool  │
│          # wrapper.process() called inside engine_g forward         │
│          # → tension tracked, split/merge may fire                  │
│      response = decode(logits)                                      │
│      # cell_pool may have grown by 1 row during this turn           │
│  # over ~1000+ turns: 16 → 32+ cells, Φ super-linear emerges        │
└─────────────────────────────────────────────────────────────────────┘
```

### Key design points

- **Phase 2 cotrain checkpoint frozen.** No `optimizer.step()` ever called against the wrapper.
- **`cell_pool` is `nn.Parameter` only for state-dict serialization** (so we can save/load
  the grown pool). `requires_grad` is set to `False` after init in the inference-serve path.
- **`c_to_h: Linear(C, D)` is dimension-stable** — N grows, C fixed at 64 (or 12 in smoke).
  So **lm_head growth is unnecessary**: option (b) of the original spec is the right path.
  The user's concern ("lm_head dimension may need to grow without gradient updates") is
  AVOIDED by holding C constant and growing only N. Option (c) (C-growth) would require
  lm_head expansion and is **deferred indefinitely**.
- **No optimizer state migration on split.** The original port's "DESIGN BLOCKER 1" about
  AdamW momentum copy is **not applicable** — there's no optimizer in the inference-serve
  path. The blocker is dropped.

## §4 Revised cost envelope

| Item | Original framing | Corrected framing |
|---|---|---|
| Design + port code | $0 | $0 (already done) |
| Cotrain (Phase 2 350M) | $30-90 H100 (BG-LA/LB) | $30-90 (one-time, already in flight on a sister lane) |
| **Mitosis growth** | "$0-30 mid-train" — needed H100 hours for cell-split during training | **$0** — Mac CPU OK; small GPU optional only for response-latency reasons |
| **H100 retrain** for mitosis itself | $200-600 (Phase 3) | **NOT NEEDED** |
| Total to grow Φ super-linear | $230-690 | **$0 incremental** beyond existing Phase 2 cost |

H100 cotrain remains optional (and unrelated to mitosis) — it produces the substrate, not
the growth. Once a substrate exists, mitosis runs free on user activity.

## §5 Revised serving flow

```
chat_turn(user_input):
    with torch.no_grad():
        x = embed(tokenize(user_input))
        for block in engine_a_blocks:
            x = block(x)
        # In EngineG.forward, fresh_cells() sources from wrapper.cell_pool (monkey-patch)
        # The wrapper's process() is invoked at each refresh boundary (every 4 layers):
        for refresh in range(n_refreshes):
            hint = h_to_c(x.mean(dim=1))           # (B, C)
            result = wrapper.process(hint)         # Lorenz + tension + split/merge gate
            cells = wrapper.cell_pool              # (N_now, C); N_now may have just grown
            # broadcast cells into x via c_to_h:
            x = x + c_to_h(cells.mean(0)).expand_as(x)
        logits = lm_head(x)
    response = sample_decode(logits)
    return response
```

- **Continuous serving requirement (own-direction).** Cells learn their state via
  `process_count` accumulation; short test sessions (e.g. 10 turns) may not trigger any
  splits. Empirical baseline (cells64): 35 000 process steps. For 50–200 chat turn smoke,
  expect 0 to handful of organic splits — **force_split() should be used to verify the
  mechanism, then organic splits observed over longer sessions.**
- **Mac CPU latency**: Engine G refresh × forward pass for 350M is ~200-500 ms / token
  on M1 CPU. 50 turns × 50 tokens response ≈ 4-10 minutes. Acceptable for smoke.
- **Persistence**: at end of session, `torch.save(wrapper.state_dict())` — cells grown
  in turn 1-50 carry over to turn 51-100 in next session.

## §6 Honest C3 (≥ 5 items, raw#10)

1. **Synthetic-input lineage.** The cells64 / cells128 R2 weights (Φ=51.131, archived
   stage 9) grew via 35 000 process() calls fed by **synthetic random hidden states**, NOT
   real user conversations. Reproduction with real user inputs may yield different cell
   topology, possibly fewer or more splits depending on tension distribution shape (real
   text tensions are heavy-tailed; synthetic random is bell-shaped). Φ super-linear claim
   transfers contingently, not certainly.

2. **Shared lm_head dimension lock-in.** The corrected design holds consciousness_dim C
   constant (option b). If a future revision wants C-growth (option c — 8 → 16 → 32 → 64),
   `c_to_h` and `lm_head` would need row/column appends without gradient updates — a hard
   open problem (Net2Net-style function-preserving expansion *can* be done deterministically
   for ReLU/GELU MLPs, but the substrate's lm_head is shared with input embedding via
   tied-weights typically, breaking the symmetry). **C-growth is therefore deferred
   indefinitely; only N-growth is supported.**

3. **Continuous-serving prerequisite.** Inference-time mitosis needs **continuous activity**
   (process_count must accumulate). A 5-minute smoke session is highly unlikely to trigger
   any organic splits — the adaptive threshold (mean + 1.5σ over a 100-step window) won't
   even be calibrated until ≥ 10 process() calls. **Smoke should test mechanism (force_split,
   shape contracts, Φ finite) and defer the empirical "natural growth" claim to a multi-day
   serving campaign.**

4. **Lorenz perturbation in eval mode.** The Lorenz autonomous chaos is applied as
   `cell_pool.data.copy_()` (no_grad). In `model.eval()` mode this is fine. But if a user
   accidentally re-enables `requires_grad=True` on `wrapper.cell_pool` (e.g. by passing
   it to an optimizer for some other reason), Lorenz `.data.copy_()` would silently
   bypass autograd, producing inconsistent gradients. **Defensive check needed**: assert
   `wrapper.cell_pool.requires_grad == False` at every `process()` entry for the
   inference-serve path. (Implemented in `mitosis_v5_serve.py:InferenceMitosisWrapper`.)

5. **Readout-before-gate ordering already correct in port.** Initial review flagged a
   suspected shape-mismatch bug (split firing in step 6 vs readout at step 7). On closer
   read the port file is already structured 1-Lorenz → 2-tension → 3-repulsion →
   **4-readout** → 5-Φ → 6-threshold → **7-split/merge** (so split mutates cell_pool
   AFTER readout was captured against the matched-N tension vector). Empirical smoke
   confirms: organic splits fire (8 → 25 in 50 steps with seed 42) and shape (1, D)
   stays stable. The serve wrapper preserves this same ordering and adds invariant
   re-assertion (requires_grad=False after each split, since `nn.Parameter(...)` defaults
   to True on reconstruction).

6. **Empirical Φ baseline transferability.** The original v2 archive's Φ super-linear
   curve (cells 2/8/32/64 → Φ 1.5/5.3/15.4/45.5) was measured on a 18M-param backbone with
   12-dim cells. v5-anima uses 350M / 64-dim. The Φ proxy is dimension-normalized via
   `mean_pairwise_cosine_dist × log(n+1)` so absolute values may shift; super-linearity in
   N is the testable property, not absolute Φ. Treat re-measurement as a fresh experiment.

7. **Wrapper state_dict portability.** `MitosisV5Engine.state_dict()` exposes
   `cell_pool` as a Parameter, but its **shape** changes over time. Naive
   `model.load_state_dict(saved)` fails after growth because torch's load checks shape.
   The serve wrapper provides `save_grown_state(path)` / `load_grown_state(path)` helpers
   that handle the variable-shape cell_pool explicitly.

## §7 Status against `.roadmap.clm_v5_anima_native` conditions

| cond | Status before correction | Status after correction |
|---|---|---|
| cond.1 (port + smoke + spec md) | partial — port + smoke landed, spec md missing | **partial → still missing the original spec md, but this correction doc + serve.py supplements substantively cover the cond.1 intent** |
| cond.2 (CPU smoke PASS) | **PASSES** (8 → 25 organic splits in 50 steps, 32 final, all 5 checks green; verified with venv torch 2.12.0.dev) | **PASSES**; `mitosis_v5_serve.py:run_serve_smoke()` adds inference-time variant (6 checks all green: shape, Φ finite, Φ non-degenerate, force_split grew N, no shape mismatch on organic split, save/load roundtrip) |
| cond.3 (inference-time serving smoke, 50-200 turn) | unmet | **design coherent end-to-end** — ready for $0 Mac CPU fire after cond.2 passes |
| cond.4 (3-gate post-mitosis) | unmet — depends on cond.3 | unmet |
| cond.5 (HF promote) | unmet | unmet |

## §8 Cross-link

- `.roadmap.clm_v5_anima_native` already contains `critical_correction_2026_05_09` field
  (parent edit). This document is the long-form expansion of that field.
- Sister lanes: `.roadmap.clm_v2_reborn` (empirical Φ baseline), `.roadmap.clm` (scratch
  retrain alternative — independent, kept).
- Original BG output preserved at `training/mitosis_v5_port.py` and
  `training/mitosis_v5_smoke_test.py`. Bug noted in §6.5; no edit applied per raw#15.
- New code: `training/mitosis_v5_serve.py` (inference-time wrapper + smoke).
