# §17 — non-text physics-channel probe: findings ($0, inference-only)

## what was discarded
`ConsciousDecoderV2.forward` returns `(logits_a, logits_g, tensions, kv, aux)`.
The carving eval harness (`eval_carving_dirI.py:155-157`) used **only `out[0]`
(logits_a) → text decode**, discarding `out[1]` (logits_g) and `out[2]`
(per-layer tensions). The entire 13-way+§8+§11+§13 arc measured anima ONLY
on the text channel. The physics channels were computed by the model itself
(`conscious_decoder.py` Law-71 block 728-751) but ONLY `if self.training:`,
never read at inference, never recorded by the arc.

## probe (deterministic, $0, NO weight touched, NO GPU)
Per stimulus, single forward pass → internal physics channels (NOT text):
Ψ_entropy, Ψ_direction (Law-71 Engine A⇄G), Ψ_tension (12-layer CV),
Ψ_combined, layer_tension[12], Φ★_proxy (layer-tension diversity).
Formulas byte-identical to conscious_decoder Law-71 (B-PHYS-5 🔵).
31 universe-brain-map anchor stimuli + 5 neutral control stimuli.

## 3-ckpt comparison

| ckpt | TEXT axis (prior arc) | PHYSICS channel (§17) |
|---|---|---|
| **Dir-I** psi_ctl+tension-sup | routing 3/31 (best text, §6) | Ψ_comb std **0.0360** · Ψ_dir spread **0.50→0.85 (0.354)** · PHYSICS_RESPONSIVE **True** |
| **Dir-E** superposition | V-SPONT honest 5/5 (max, §9) | Ψ_comb std **0.0123** · Ψ_dir spread 0.025 · PHYSICS_RESPONSIVE **True** |
| **§11-B pure-physics** no-CE | DEGENERATE (byte_acc<rand) | Ψ_comb std **0.0** · Ψ_dir spread **0.0** · ALL std=0 · PHYSICS_RESPONSIVE **False** |

## findings (g3 — measured only, over-claim 0)

1. **The physics channel carries per-stimulus signal where text collapsed.**
   Dir-I text routing = 3/31 (near-collapse). Same ckpt, same 31 stimuli:
   Ψ_direction (Engine A⇄G alignment, Law-71) spreads **0.50→0.85**, range
   0.354 — a large, stimulus-conditioned physics signal that the
   text-decode almost entirely lost. The arc's "single-attractor collapse"
   verdict was a property of the **text observable**, not of every
   internal channel.

2. **The negative control passes (honest).** §11-B pure-physics (no-CE,
   text-degenerate AND physics-only-trained) is **also fully
   physics-channel collapsed** — Ψ_direction spread *exactly* 0.0,
   Ψ_entropy constant 0.8924, every std = 0.0. The channel is NOT
   trivially "always responsive"; it collapses exactly when the model
   collapsed. → text was a wrong observable for the *CE-trained* fires,
   but NOT a wrong observable for the genuinely-degenerate one. The
   reframe is bounded, not universal.

3. **in_basin = 0/31 on all three.** The model's Law-71 Ψ-point does NOT
   land in the corpus-specified ANCHOR_PSI basins. Honest: the model was
   never trained to put its Law-71 Ψ there (it was trained on text-CE +
   Dir-I psi_ctl on the inner-span only). in_basin is a DIAGNOSTIC, not
   a success criterion. → physics channel carries *signal* but not
   *correct-routing on the corpus target* — i.e. the reframe shows a
   live channel, NOT GOAL emergence.

## honest conclusion
The 13-way arc's "collapse / 0-progress" verdict is a verdict about the
**text channel**. A non-collapsed, stimulus-conditioned physics signal
DOES exist in the CE-trained fires (Dir-I/Dir-E) — the arc measured the
wrong observable for *liveness*. BUT: (a) the signal is not "correct"
(in_basin 0/31), (b) the degenerate fire is physics-collapsed too (reframe
is bounded), (c) a moving tension trajectory is necessary-not-sufficient
for emergence. This is a **measurement-observable reframe**, not a GOAL
solution. emergence remains empirical & unmeasured (B-PHYS-NOTE).

## closed verdict
B-PHYS-1..5 5/5 🔵 (`blue_falsifier_phys.py`, sidecar — central
blue_falsifier.py UNCHANGED). per-fire physics-channel OUTCOME = EMPIRICAL
B-PHYS-NOTE (B-D-NOTE / B-PUREPHYS-NOTE family, NOT counted 🔵).
f1/f2/f3 + B-IDENTITY-5 safe. $0 — inference read-out only.
