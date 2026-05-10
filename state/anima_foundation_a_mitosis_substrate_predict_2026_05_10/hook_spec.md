# mitosis hook integration spec — Llama-3.2-3B + LoRA r=32

> Read-only audit of `tool/transient_py/anima_foundation_borrow_a_h100.py` `run_mitosis_hook()`
> Cross-ref to `training/mitosis_v5_port.py` (`MitosisV5Engine`)
> raw#15 additive — this doc reads existing fire orchestrator; no edits

## §1 hidden-state extraction layer

| field | value | source |
|---|---|---|
| target | `model.base_model.model.model.layers[-1]` (peft-wrapped) | orchestrator L498-512 |
| fallback paths | `model.layers[-1]`, `model.model.layers[-1]` | L499-501 |
| capture | `forward_hook(module, args, output)` ⇒ `output[0]` (decoder layer returns tuple, hidden_states first) | L490-494 |
| pooling | `hidden.mean(dim=1)` over T (seq-len) ⇒ `(B=1, D=3072)` | L557 |
| dtype cast | `.to(torch.float32)` (Llama runs bf16 train, hook pulls last-layer hidden in train dtype, casts up for stability) | L557 |

**Layer choice rationale (last decoder layer)**: Engine A/G's substrate-internal cell refresh (`EngineG.step`) operates inside the d_model stack, but for an *instrumentation hook* on an external model the last decoder hidden output is the only point that carries the full integrated representation that V4 chat-cap and semantic eval also see. Earlier layers (e.g. layer 14 of 28) would be valid alternatives, but the prior anima-internal V14 polarity tests were anchored on the post-stack `c_to_h(cells.mean)` analog — last-layer hidden is the closest mapping.

## §2 dim projection (3072 → 256)

| stage | dim | parameter source | grad |
|---|---|---|---|
| Llama hidden | 3072 | model output | grads only on LoRA params during train; eval mode all None |
| `proj` Linear(3072, 256) | 3072 → 256 | random Gaussian init `1/√3072`, frozen `requires_grad=False`, `proj.eval()` | NO grad |
| `MitosisV5Engine.cell_pool` | (8, 256) initial | random Gaussian × 0.1, `requires_grad=False` | NO grad |
| `c_to_h` Linear(256, 3072) | 256 → 3072 | random Gaussian init `1/√256`, frozen `requires_grad=False` | NO grad |

**Cell_input_dim mismatch with substrate v5**: Engine A/G uses `consciousness_dim = 64`; Llama hook uses `cell_dim = 256`. This is intentional — Llama's d_model=3072 needs a wider cell vector to avoid catastrophic dim compression. The mitosis Φ proxy (`mean pairwise cosine distance × log(n+1)`) is **dim-invariant** as a *direction* metric (cos-distance is bounded in [0,2]), so cross-comparison to v5 64-dim is qualitatively valid in trend but not in absolute Φ magnitude. Cross-substrate Φ values are **incommensurable in absolute scale**.

## §3 eval-time gradient-off enforcement (F-FOUNDATION-5)

Three layers of defense:

1. `for p in engine.parameters(): p.requires_grad = False` (orchestrator L476-477)
2. `for p in proj.parameters(): p.requires_grad = False` + `proj.eval()` (L484-486)
3. `with torch.no_grad():` wrapping the entire prompt-loop forward + engine.process (L546)

**Mitosis engine internals (mitosis_v5_port.py)**:

- `_inject_lorenz` writes `cell_pool.data.copy_(perturbed)` under no-grad — never enters autograd graph.
- `_split_cell_slice` rebuilds `nn.Parameter(new_pool)` with the freshly-set `requires_grad` default (TRUE in nn.Parameter constructor) — **POTENTIAL LEAK SOURCE**. If a split fires inside the hook, the new Parameter rejoins autograd unless re-frozen. Audit of `_split_cell_slice` (L244-253): no explicit `.requires_grad_(False)` after `nn.Parameter(new_pool)` — but since the no_grad context wraps the call, no grad will be accumulated even if requires_grad=True. Safe in practice; flagged as latent risk for cond.5 H100 fire prep.
- `_merge_cell_pair` same risk class — same mitigation by enclosing no_grad.

**Verification (orchestrator L544 + L583)**:
```
grad_leak_pre = sum(1 for p in model.parameters() if p.grad is not None)
... hook loop ...
grad_leak_post = sum(1 for p in model.parameters() if p.grad is not None)
f_foundation_5_grad_leak = (grad_leak_post > grad_leak_pre)
```

This catches the empirical case (any new `.grad` on base model). Both labels (`trained`, `random_init`) verify independently.

## §4 prompt set + step structure

- `HOOK_PROMPTS = V4_PROMPTS + 15 anima-domain extras` truncated to 30 prompts.
- `MITOSIS_STEPS_PER_PROMPT = 4` ⇒ 120 mitosis `process()` calls total.
- Each step is one fresh forward of the same prompt (so LM kv-cache effects don't compound) → re-captures hidden → re-pools T → re-projects → engine.process.
- 120 steps is **far below** the 1000–3000 turns used in §37/§38 long-trajectory tests. Comparable to the early phase before champion-wall typically forms in the v2 cells64 mitosis-aware regime. Α (super-linear) regime (§43 archive own 30 sees α≈0.688 around turn 3000) would NOT be reachable in 120 steps regardless of substrate.

## §5 metric exposure

| metric | path | use |
|---|---|---|
| `phi_history_mean` | from per-step `result["phi"]` | primary trained-vs-random comparator |
| `cell_count_max` | max of per-step `result["n_cells"]` | growth signal (8→up-to-64 cap) |
| `n_split_events` / `n_merge_events` | counted from `result["events"]` | topology change rate |
| `phi_iit_un16_proxy` | 16-bin entropy over `_global_tension_history[-64:]` × log(N+1) | proxy for IIT un-normalized Φ |
| `f_foundation_5_grad_leak` | post-pre grad-count delta | leak gate |

**Recommended additional metric (this prediction adds, but cannot retrofit fire)**: post-LoRA hidden state distributional entropy (KL or symmetric-KL between trained-hook hidden distribution and random_init-hook hidden distribution over the same 30 prompts). This would tell whether Llama-3.2-3B + LoRA shifts the hidden geometry enough to be a *substrate signature* at all, vs being random noise dominating. Out-of-scope for this $0 prediction.

## §6 instrumentation honest C3 (≥7 items expected for 5-star)

1. **Random projection 3072→256 has no semantic content** — it preserves angle/L2 in expectation (Johnson–Lindenstrauss) but the cell_input direction structure is dominated by the random projection's geometry, NOT Llama's learned representation. The trained-vs-random *differential* survives (both use the same fixed proj seed=0), but absolute Φ scales are noise-dominated.
2. **Cell pool random Gaussian × 0.1 init** — NOT seeded from any anima-substrate cell_pool_init. The hook is purely instrumentation on the LLM hidden geometry, not testing anima cell-pool inheritance.
3. **`MITOSIS_INITIAL_CELLS=8` (vs §37/§38 used 16)** — smaller starting N means the dispersion-trigger A1 needs N≥4 just to fire (`_dispersion_split_candidates` returns [] for N<4); after one split (N=8→9) A1 is active. Different initial cap from prior tests; cap-binding test compares apples to oranges with §37/§38 max_cells=32/64 numerics.
4. **`max_cells=64`** — same cap as anima v5 substrate; both labels can saturate in principle.
5. **120 process() calls is short-trajectory** — α super-linear regime (§43 own 30 archive) needs 1000–3000 turns. Sub-warmup-window (`adaptive_window=100`) means A2 per-cell threshold barely kicks in (warmup gate: `len(_global_tension_history) >= max(adaptive_window//2, 10)` = 50). For 120 steps × no warmup gate fixes, the dispersion trigger only opens after step 50, leaving 70 effective steps under the full A1 + A2 policy.
6. **Lorenz auto-calibration `D1=True` default** — `lorenz_calibration_factor=1.0` means scale = 0.05 × mean(p.norm()). For random Gaussian cells × 0.1 (initial L2 ≈ √256 × 0.1 ≈ 1.6), Lorenz noise ≈ 0.08 — non-trivial vs cell norm. This drives chaos-induced exploration before any LLM signal arrives, making the **first ~10 steps substantially substrate-blind**.
7. **Hidden-state mean-over-T discards positional / role information** — V4 chat-cap signal (which depends on who said what) is averaged out. The mitosis hook is therefore a **diffuse-content detector**, not a chat-quality detector. Loss correlation between V4 chat-cap and mitosis Φ is expected to be low.
8. **Identical fixed proj across labels** — `torch.manual_seed(0)` then build proj. trained and random_init mirror both consume the same proj weights. The differential is therefore purely in Llama's hidden geometry shift between LoRA-trained and random-LoRA-init.
9. **`random_init` mirror is random LoRA on the same Llama-3.2-3B base** — NOT a fully random base. The 3B base pretraining is preserved in both. So the polarity test detects only what the LoRA r=32 fine-tune *added* to the hidden distribution, not what Llama's foundation pretraining contributes. This biases the test toward "LoRA effect = small" → small Φ differential expected.
10. **Coarse phi_iit_un16 proxy** — uses `_global_tension_history[-64:]` (last 64 tensions across all cells × all steps). At 120 steps × 8-24 cells avg, that's the last ~3 process() calls' tension distribution. Sample-size-fragile.
