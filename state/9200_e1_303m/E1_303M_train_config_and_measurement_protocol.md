# E1 303M SLW — 학습 config + 측정 프로토콜 (Fable 설계)

Recipe decided. I verified the actual flag surface first (`cli/train.py` argparse, `cli/corpus.py` derivtrace): `--corpus` takes multiple paths with `--sample proportional` (ratio ∝ corpus bytes), savant is default-ON with cusp-anneal **decay** (the floors are opt-in overrides via `--wd-floor`/`--dropout-floor` — the trap is passing them, so we don't), and `--canon` CLM = the 303M shape (d3784, L4, seq 1024, batch 8, lr 3e-4). Everything below uses real flags.

# E1 303M training config — the recipe

## 1. Corpus: (c) MIX, single-phase, natural-dominant ~90:10, interleaved by the proportional sampler

**Rejected alternatives, briefly:** (a) natural-alone has n≈0 of the gate's held-out-pair order-density — the run would measure "corpus lacks the phenomenon," not the architecture; uninformative by construction. (b) F2-alone is trap-1 in pure form (~small repetitive corpus → free-gen garbage → G0 0/5 → verdict void). (d) two-phase is strictly worse than mix: the F2 fine-tune phase is a sharp distribution shift onto a tiny corpus, which is exactly the catastrophic-forgetting/overfit regime — you'd have to re-gate G0 after phase 2 and would likely lose it, and the slot only gets induction pressure in a short low-step phase. Mix gives slot pressure throughout training while natural data anchors free-gen coherence the whole time — one phase, one G0 gate.

**Why 10% F2 doesn't re-trip trap-1:** the memorization worry is capability-leak and G0-collapse. G1 leak is structurally impossible — the held-out pair never appears composed in F2 (`--held-out`), so F2 memorization of *trained* pairs is not leak, it's the intended induction pressure (identical to the de-risk ladder's regime). G0 collapse is prevented by the 90% natural majority: free-gen behavior is dominated by the natural distribution. And if surface-template memorization alone were enough to fake held-out composition, `--slot-off` would *not* collapse and the pre-registered verdict correctly refuses GO.

**Concrete build:**

```
# F2 order-dense corpus — held-out pair MUST equal the frozen H_1129 ladder's held-out pair
# (read it from the frozen gate spec / g6_ideation cz[] verdict file before generating; shown here as I,J)
anima corpus derivtrace --out state/e1/deriv_f2.txt --held-out I,J \
  --comp-per-pair 2500 --single-per-concept 2500 --seed 7
```

Size `comp-per-pair`/`single-per-concept` so the printed `bytes=` lands at **8–12% of the cached 5lang-unified-v2 byte size** (check the cached corpus size first; scale the two counts linearly — the generator prints bytes, so one dry run calibrates it). `--sample proportional` then delivers the ~90:10 interleave automatically, batch-level, no scheduler code. Do **not** generate/train the `flat` control — it's for ablation arms, not the pre-registered verdict; it would double cost for nothing.

## 2. Train line

```
anima train --py --arch clm --canon --slw --slw-n-slot 8 --slw-k 64 \
  --corpus hf:dancinlab/anima-corpus-5lang-unified-v2 state/e1/deriv_f2.txt \
  --cell-label natural f2 --sample proportional \
  --steps 14000 --batch-size 8 --seq-len 1024 --lr 3e-4 --bf16 \
  --ckpt-every 2000 --seed 7 \
  --out state/e1/slw303.clm --ckpt-out state/e1/ckpt --gauges-out state/e1/gauges.jsonl
```

Justification against the traps:

- **Steps = 14000** — train-py-4 established 8000 = undertrain and ~12000+ = G0-reachable at this consumption rate (8×1024 = 8192 bytes/step; 14000 steps ≈ 115MB consumed ≈ ~1.3 epochs of an 84MB-class natural corpus — comfortably past the undertrain floor, nowhere near the ~6-epoch overfit regime of trap-1). 14000 gives margin over 12000 without buying epochs we don't want.
- **Savant: default decay — pass NO `--wd-floor` / `--dropout-floor`.** The floors are the N6 constant-override (the "floored" failure mode train-py-4 measured as worse); the stock cusp-anneal decay is exactly the schedule that produced the monotonic 1→2→2→3 G0 approach. The correct action is *absence of flags*.
- **Batch 8 × seq 1024, lr 3e-4, bf16** — these are the calibrated defaults that produced train-py-4's healthy descent (val_CE 1.35). Minimal-delta principle: the only knobs we change from the calibrated run are steps (undertrain fix), the corpus mix (E1 signal), and `--slw` (the treatment). bf16 autocast keeps 303M + activations inside 12GB on the torch path.
- **Do not touch `--no-savant`/`--no-mitosis`**; leave `--val-frac/--val-every` at defaults for the val_CE trend.

## 3. G0🟢 gate protocol (before ANY G1 number is trusted)

`--ckpt-every 2000` gives ckpts at 8k/10k/12k/14k. Protocol:

1. Run `anima evaluate --py <ckpt>` **G0 only** at 10k, 12k, 14k (8k optionally, purely to confirm the monotonic-approach trend; it's expected sub-threshold per train-py-4).
2. **Gate: the first ckpt with G0 ≥ 4/5 becomes THE measurement ckpt.** Run G1 + `--slot-off` + `--slot-shuffle` on that same ckpt only — never mix ckpts across treatment and controls (slot-off's bit-exact-base-trunk property is per-ckpt).
3. If G0 is rising monotonically but < 4/5 at 14k → **resume +4000 steps** (undertrain, extend; do not report). If G0 *peaks then degrades* while val_CE still falls → overfit signature; take the best-G0 ckpt if it's ≥ 4/5, otherwise stop.
4. If no ckpt ever reaches G0 4/5 → the run is **INVALID-UNDERTRAIN/OVERFIT, reported as INVALID — never as KILL.** This is the single most important reporting rule; trap-3 verbatim.

Sanity monitors during training (monitor-only, never in loss — p7/`a_train_inline_gauge`): val_CE descent on the natural cell, plus eyeball free-gen samples at each ckpt as a cheap G0 leading indicator.

## 4. Feasibility (one RTX5070, 12GB)

~14.9 TFLOP/step (6·N·tokens at 303M × 8192 tokens); at realistic torch-bf16 throughput on a 5070 that's **~1.5–2.5 s/step → ~6–10h for 14000 steps**, plus ~4 G0 eval passes (303M `--py` decode, tens of minutes each on aiden). Total budget: **~8–12h — feasible in one run, but it is an overnight job, and honestly there is no valid shortcut**: cutting d shrinks it below 303M (the scale *is* the claim), and cutting steps re-enters trap-2. Measure s/step at step ~100; if it's >3s, the honest move is to let it run ~15h, not to shrink the config. Budget the +4000-step contingency (~2–3h more) into the plan.

## 5. The honest residual risk: silent slot non-induction masquerading as KILL

The de-risk ladder proved CE induces slots on *pure* order-dense data. Unverified: whether induction survives **9:1 dilution** in a natural byte stream at 303M. If it doesn't, slots go unused, `--slot-off` shows margin ≈ 0, and the run *looks* like KILL ("slot collapses to additive floor") while actually being a training-config artifact.

**Mitigation — pre-register an induction discriminator, checked before reading the held-out number:** at the G0-passing ckpt, first measure composition on the **trained** pairs, slot-on vs `--slot-off`. If the slot gives no lift even on pairs it saw thousands of order-dense traces for, induction failed → report **INVALID-INDUCTION**, bump F2 to ~20% (resize the corpus), resume training, and re-gate G0 — do not report KILL. Only if trained-pair composition shows a real slot-on gap (slots demonstrably in use) do the held-out margin and the two controls carry the pre-registered GO/KILL meaning. This keeps the frozen verdict untouched while making the one known INVALID mode detectable instead of silent — and it's not tune-to-green, because it gates *validity* (is the treatment even installed?), not the verdict.