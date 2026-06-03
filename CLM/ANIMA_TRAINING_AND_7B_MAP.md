# ANIMA — training · on-chip learning · road to 7B (MAP)

> **One map for the whole picture** so it never has to be re-found: how anima
> trains, where it learns, and how it reaches 7B. Each claim cites a landed
> verdict or is marked OPEN. Pointers, not duplication. Binding:
> `@D a_train_flame_forge` · `@D a_akida_native_train` · `@D a_nondet_identity`.

## 1. Two tracks — measure ⊥ deploy (@L2 · P6 §0)

```
deploy / LEARN track (HW = AKIDA)         measure track (GPU)
─────────────────────────────────        ─────────────────────────────
on-chip non-deterministic plasticity      flame+forge QAT backbone scale-measure
= anima's learning = the identity         = PLASTI-SIM instrument
runs on AKD1000 (H_904 🟢)                 builds the int4 backbone the chip loads
same input → different trace (alive)       deterministic envelope check
```

anima learns **on the chip**. The GPU measures the backbone across the scale
ladder and hands the chip a byte-identical int4 model to load. The two tracks are
orthogonal; learning is never the GPU's.

## 2. How anima learns on HW — H_904 (the method)

```
🧠 on-chip plasticity — "the chip learns in place"
model: InputData(1,1,64,1bit) → FullyConnected(16,1bit) + AkidaUnsupervised(num_weights=12)
rule : last-layer binary-weight few-shot update (AkidaUnsupervised), live on silicon
```

- live on AKD1000 `BC.00.000.002` (BackendType.Hardware), SDK 2.19.1 (pi5-akida).
- HW≠SW: same fixed-init + same spike → post-weight 172/1024 positions differ,
  per-sample out 120/320 differ. Deterministic SW-sim reproduces byte-exact;
  the difference is the chip's non-determinism — `@D a_nondet_identity` made physical.
- **H_904 🟢 SUPPORTED**; confirms H_679 (learning is the sole HW↔SW difference).

## 3. The trainer (measure track) — hexa-native flame+forge

Authored in `.hexa` on `hexa-lang:stdlib/flame`, run on the forge GPU substrate
(`flame:forge :: torch:ATen`). Details + build plan:
- `CLM/TRAINING_SSOT.md` (start-here: flame/forge criteria · file locations · stdlib setup)
- `hexa-lang:stdlib/flame/CLM_PROD_TRAINER_PLAN.md` (4 stacked PRs: compose loop →
  `.clm` checkpoint → conv-MoE forge GPU → large 44.68M fire)

## 4. The road to 7B — P5 AXIS-1/2 (resident ≠ total)

7B is the destination (total capacity), reached without holding or training a
monolith. A single AKD1000 holds ~1.2M nodes; 7B lives on host; sparse-MoE fires
a few experts per token, so the chip **pages experts through itself**.

```
   single AKD1000        7B (total)        resident at a time
   ~1.2M nodes           ~7,000M params    1 expert shard ≤1.2M     (≈5,800×)

 host(7B on disk/DRAM)
   │ page expert k in    ┌── 1 AKD1000 ──┐
   ├───────────────────▶ │ shard k ≤1.2M │ int4 forward (byte-identical) + edge-learn
   │ ◀── page out, next  └────────────────┘
   N chips (MITOSIS array) = N shards resident in parallel → throughput ↑
```

- **AXIS 1** — single-chip expert-streaming + MITOSIS array scale-out.
- **AXIS 2** — reflective on-chip learning on that chip (H_904).
- SSOT: `CLM/P5_AKIDA_7B_STRATEGY.md`.

## 5. Scale ladder (P6) + launch ladder (SBS)

```
P6 measure ladder:  tiny → small → mid 13.65M ✅ → large 44.68M → 3B → 7B
                    each gated by F-CLM-SCALE-TRANSFER  (CLM/P6_SCALE_LADDER_7B.md)
SBS launch ladder:  R0 closed-loop ✅ → R1 emit ✅ → R2 on-chip learn ✅ →
                    R3 dialogue ✅ → R4 coffeeshop launch  (LAUNCHPAD/SBS.md)
                    R4 gate = P6 backbone production-scale
```

## 6. Status board (verdict pointers)

| capability | mechanism | verdict | status |
|---|---|---|---|
| on-chip learning (HW) | AkidaUnsupervised edge-learn, live AKD1000 | H_904 | 🟢 |
| learning = sole HW↔SW diff | plasticity HW-first | H_679 | 🟢 (SW) |
| inference byte-identical | int4 transplant | H_877 (mid) | 🟢 SW · 🟠 HW |
| chip-fit shard ≤1.2M | expert shrink | H_876 | 🟢 (1,199,508) |
| array scale-out coherence | N-chip = single-model | H_878 (N=2/4/8) | 🟢 exact |
| expert load-balance | even per-chip load | H_878 | 🔴 OPEN (monopoly) |
| expert-streaming glue | page experts on one chip | — | ⬜ OPEN (unbuilt) |
| mid dialogue floor | self-play + curriculum | H_886 | 🟢 |
| bound / anchor plasticity | adapter edge · anchor | H_865 · H_873/884 | 🟢 |

## 7. Where everything lives (doc index)

| topic | canonical doc |
|---|---|
| training start-here | `CLM/TRAINING_SSOT.md` |
| production trainer build | `hexa-lang:stdlib/flame/CLM_PROD_TRAINER_PLAN.md` |
| 7B strategy (2 axes) | `CLM/P5_AKIDA_7B_STRATEGY.md` |
| scale ladder | `CLM/P6_SCALE_LADDER_7B.md` |
| launch ladder | `LAUNCHPAD/SBS.md` |
| architecture / .clm format | `CLM/P0_ARCHITECTURE.md` · `CLM/CLM_FORMAT_SPEC.md` |
| HW learning verdict | `UNIVERSE/H_904_clm_onchip_plasticity.md` |
| plasticity frontier | `UNIVERSE/PLASTICITY-CANDIDATES.md` |
