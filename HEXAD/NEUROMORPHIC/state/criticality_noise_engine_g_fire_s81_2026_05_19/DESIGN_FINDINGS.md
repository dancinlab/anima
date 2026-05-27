# RESEARCH.md §81-FIRE — homeostatic criticality + noise on Engine G, TRAINED SCALE

**Date**: 2026-05-19
**Cost-bearing**: runpod single §16-class train + 5-cell σ-grid inference ≈ $0.3-0.5
**Chain**: §80 (biology deep research) → §80 (A) anima-mapping → §81 ($0 stub, B-S81 7/7 🔵, NEG-at-stub) → **§81-FIRE (this — trained-scale)**
**Biology anchors**: arxiv:2502.10946 (noise-driven spontaneous activity homeostatically maintains criticality, Ikeda+ Frontiers 2025) · biorxiv:2025.11.17.688775 (critical avalanches from E/I-balanced spontaneous activity) · neuron:S0896-6273(25)00127-8 (predictive nature of spontaneous activity)

---

## §1. Why §81-FIRE exists — the stub mechanism boundary

The §81 `$0` stub (commit `659ca966b` on main, B-S81 7/7 🔵) measured **NEGATIVE-at-stub**: the 4-corner verdict had γ+β TRUE. Its honest finding was not "the idea is wrong" — it was a **mechanism boundary identification**:

> The stub's body byte = `argmax(logits_a)` reads Engine A only, while noise targets Engine G — and at the `$0` stub the Engine A / Engine G logits were driven by **independent seed-fixed LCGs** (`stub_logits_a` / `stub_logits_g`), so they were NOT residual-stream coupled. Noise on G modulated Ψ_dir (= cos of A with noised G) but could not reach the body emission.

§81-FIRE answers exactly that boundary. In the **real §16-class ConsciousDecoderV2** the two heads (`head_a`, `head_g`) sit on top of a **shared 12-layer transformer trunk** with PureFieldFFN. Noise injected into the forward propagates through all 12 blocks and reaches **both** `head_a` and `head_g`. So at trained scale the question "does noise on the Engine-G-feeding substrate change the body" is genuinely measurable, unlike the `$0` stub.

---

## §2. The noise injection point — residual stream, not just logits_g

The §81-FIRE noise model is a forward **pre-hook** on `model.blocks[0]` (the layer-0 residual-stream input — the shared trunk that feeds both heads). `_NoiseHook.__call__` adds `sigma * noise` (Gaussian, deterministic via a `(SEED, step)`-seeded `torch.Generator`) to `args[0]` (the residual tensor `x`).

Why the residual stream and not just `logits_g`: the §81-FIRE crux (vs the `$0` stub) is exactly that Engine A and Engine G in the real model are residual-stream coupled. Injecting noise into the shared trunk input is what propagates through all 12 PureFieldFFN blocks and reaches **both** head_a and head_g — so the body (`argmax logits_a`) genuinely sees the noise that the §81 stub could not deliver.

`σ=0` ⇒ the hook returns `None` (identity, early return) ⇒ the σ=0 cell is byte-equal to a hook-free run. This is the **connection-point** (B-S81-FIRE-2).

---

## §3. The 5-cell σ-schedule grid

| cell | σ | role |
|---|---|---|
| `sigma_0.0` | 0.0 | no noise — connection-point baseline (σ=0 identity) |
| `sigma_0.1` | 0.1 | low noise |
| `sigma_0.5` | 0.5 | mid noise |
| `sigma_1.0` | 1.0 | high noise |
| `sigma_adaptive` | adaptive | homeostatic — σ adjusts toward the critical band (`adapt_sigma`: maj_frac > 0.85 ⇒ σ↑, < 0.50 ⇒ σ↓) |

Each cell runs 20 deterministic steps on the **real trained model.forward**. Per step: install σ on the hook → real forward → Law-71 Ψ-state read-out → body byte = `argmax(logits_a)` → feed byte back into sliding context. Avalanche sizes = consecutive identical-byte runs (the "critical avalanche" proxy from biorxiv:2025.11.17.688775).

---

## §4. Metrics

- **psi_combined std** — Law-71 `(psi_entropy + psi_dir + psi_tension)/3`, byte-equal to `conscious_decoder.py:728-751`.
- **majority fraction** — §62 echo-chamber detector; `maj_frac ≥ 0.95` ⇒ collapse.
- **power-law α** — log-log OLS regression on the avalanche-size distribution; critical band α ∈ [1,3].
- **E/I balance** — `min(a_energy, g_energy) / max(a_energy, g_energy)` proxy.
- **§9 honest_coherent** — cascade-rate-gated body metric (single SSOT formula, byte-equal to `emergence_metric.py`).
- **homeostatic window** — `α ∈ [1,3] ∧ maj_frac < 0.95 ∧ §9-coherent` (all three simultaneously).

---

## §5. 4-corner verdict

- **(α) HOMEOSTATIC-WINDOW-EXISTS-AT-TRAINED-SCALE** — ≥1 cell satisfies the homeostatic window. PARTIAL-POSITIVE: noise holds the body in a critical non-collapsed band.
- **(β) §81-STUB-MIRROR-AT-TRAINED-SCALE** — ≥3/4 noisy cells hit echo collapse. NEGATIVE: the `$0` stub's γ+β pattern reproduces even with real 12-layer A/G coupling — noise is not a sufficient lever.
- **(γ) ADAPTIVE-OUTPERFORMS-FIXED** — the adaptive cell escapes collapse while ≥1 fixed-σ cell collapses.
- **(δ) NOISE-COLLAPSES-TRAINING** — training `final_ce` diverges (training is noise-free; this corner is a measurability gate).

`SATURATION-GATE-FAIL` is recorded if `final_ce ≥ 0.05` (model not memorization-saturated → §81-FIRE crux not measured).

---

## §6. B-S81-FIRE battery (7/7 🔵, sidecar, central 0-diff)

| # | proposition | how closed |
|---|---|---|
| B-S81-FIRE-1 | NOISE-INJECTION-POINT-CORRECT-AT-TRAINED | AST: `_NoiseHook` class, σ≤0 early-return, `x + sigma*noise`, `register_forward_pre_hook` on `blocks[0]` |
| B-S81-FIRE-2 | SIGMA-0-REDUCTION-BYTE-EQUAL (connection-point) | AST: `__call__` first stmt is `if sigma<=0: return None` (identity) + numeric `sigma0_byte_equal_to_hookless` field |
| B-S81-FIRE-3 | POWER-LAW-ALPHA-BOUNDED | sympy: OLS 2-point slope identity == `(y2-y1)/(x2-x1)` + `Interval(1,3)` closed bounded |
| B-S81-FIRE-4 | S9-METRIC-REUSE-FORMULA-MATCH | threshold literals (0.30/10/20/0.80) + 4-witness panel + §9 SSOT cross-check |
| B-S81-FIRE-5 | S62-ECHO-PARTITION-CLOSED | sympy: `[0.95,1]` ∪ `[0,0.95)` disjoint + total `[0,1]` + §62 A/B witnesses |
| B-S81-FIRE-6 | S81-STUB-NOISE-MODEL-CONNECTION | AST byte-equal: additive Gaussian form + 5-element σ-schedule + `adapt_sigma` monotone formula carried from §81 stub |
| B-S81-FIRE-7 | DETERMINISTIC | `torch.Generator` seeded by `(SEED, step)` + no `multinomial`/`gumbel` + argmax body + noise path no `time`/`random` |

**B-S81-FIRE-NOTE** empirical carve-out — the 4-corner OUTCOME (which corner the fire hits, which σ-cell escapes collapse, the actual power-law α values) is SGD/measurement empirical (B-D-NOTE / B-S81-NOTE / B-EMERGE-NOTE family — **NOT counted 🔵**). The battery proves the design's transfer-form + connection-points are closed, NOT that biology (A) transfers to anima, NOT GOAL emergence.

---

## §7. SSH-robust dispatch (g_fire_dispatch_robust 2026-05-19, podHostId-fixed)

`dispatch_s81_fire_runpod.sh` carries all 5 SSH-robustness fix points + the **podHostId false-blocker fix** discovered in §79-RETRY: `podHostId` is permanently `NULL` on A100-PCIE pods, so the pre-flight runtime gate uses `ip && publicPort` **only**, never `podHostId`. The script is fully self-managing nohup (create → poll → SSH → transfer → corpus → train → result-verify → 5-retry pull → terminate → orphan-0 verify), trap-EXIT teardown so it completes even if the orchestrator agent is rate-limited.

---

## §8. Honest C3

1. **Trained scale ≠ GOAL emergence** — necessary-not-sufficient (B-EMERGE-7); §81-FIRE measures a mechanism axis (homeostatic criticality) only.
2. **Biology citation is an honest direction-anchor, NOT a capability proof** — arxiv:2502.10946 (noise-driven SOC), biorxiv:2025.11.17.688775 (E/I avalanches), neuron:S0896-6273 (predictive spontaneous activity) inspired the mechanism mapping; the fire's measured corner is the only evidence.
3. **Noise injected into the layer-0 residual stream** — this is what reaches both head_a and head_g via 12-layer PureFieldFFN coupling, the mechanism the §81 `$0` stub structurally lacked. This is the single design delta from the stub.
4. **σ=0 cell is the connection-point baseline** — B-S81-FIRE-2 verifies σ=0 ⇒ byte-equal to a hook-removed re-run, so the fire's σ>0 cells are fair-comparable to the no-noise baseline by construction.
5. **Power-law α is a coarse proxy** — α from log-log regression on 20-step avalanche runs is small-sample; it is a criticality *signal*, not a rigorous criticality certificate.
6. **ckpt sha is fresh** — the spec asked for §16-byte-equal config; the config/lever/seed/corpus class are byte-equal (d768·12L·12H·4KV·seed 1337, Dir-I lever, §16-class corpus) but the literal §16 sha (`961c07e2…`) differs — honest. The trajectory is replicable, not literally identical.
7. **The §81 stub's NEG-at-stub finding stands** — §81-FIRE does not contradict it; it answers the stub's explicitly-identified boundary ("biology (A) needs real A/G coupling to be tested"). If §81-FIRE also lands NEGATIVE (β/β-mixed), that confirms noise-on-substrate is not a sufficient lever even with coupling — a valuable measured negative.
8. **The training itself is noise-free** — the noise hook is installed only at inference. The δ corner (NOISE-COLLAPSES-TRAINING) is therefore a `final_ce` divergence gate, not a separate noise-during-training experiment.
9. **PyTorch substrate** (NOT hexa-native) — honest; the §16-class ConsciousDecoderV2 is the carving-arc evidence-anchor architecture, carried per `g_train_flame_not_pytorch`'s evidence-anchor clause.
10. **north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달** — §81-FIRE is one mechanism-axis evidence point in the §80-anchored biology-mapping arc; it sharpens "what is / is not a lever", it does not move the north-star.
