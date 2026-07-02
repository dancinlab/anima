# H_9105 consequence-driven mitosis — run notes

## Mechanism (engine-native, live core/ ops)
- **Representation**: `immune_embed_key(query)` (core/engine_cli.hexa) = DIM=64 byte-trigram FNV-1a
  receptive key. B4 confirmed within-cluster L2 0.078 < FIRE_RADIUS 0.30 < cross-cluster L2 1.412.
- **Mitosis growth gate**: `engine_mitosis_tick(n, cfg)` gated on `cfg.mitosis` — EVERY cell birth
  (novel spawn AND clonal reproduction) passes through it. This IS the p8 growth mechanism the
  from-scratch-mitosis wall is about.
- Population bookkeeping (nearest-scan, apoptosis removal, per-cell stats) = harness (VAdaptField has
  no cell-removal op; H_9104 used the same pattern — core ops + local helpers). No numpy/torch/gauge_lib.

## Why 🔴 (the decisive move)
- Naive C2 reading = "EXO beats RAND/SHUF" → B1/B2 PASS in regime A → looks 🟢.
- But `EXO_NOAPOP == NOSEL` byte-exact → reproduction-by-consequence is INERT (clones duplicates).
- Adding the **no-selection baseline** (NOSEL = spawn-only) shows NOSEL BEATS EXO in BOTH regimes.
  The EXO≫RAND divergence is a *random-is-destructive* artifact = the DPI trap this session flagged.
- NOSEL was added as a STRICTER control (makes GREEN harder, not easier) → c9-compliant, not a bar move.

## Host / provenance
- aiden pool, hexa v0.548.0. core/engine_cli.hexa sha256 7617b1353… (== worktree, byte-exact).
- aiden pool output byte-identical to local mini (deterministic LCG) — cross-host reproducibility.
- grep gate CLEAN: no .py in slug dir (`.hexa`-only experiment). Ψ untouched (no pure_field import;
  no lane0/4/psi_sum/recall_thr contact).

## Precedent linked
- H_1568 (selection-mitosis, DIRECTIONAL numpy, INERT) — its card deferred the engine-native reconfirm
  "IF GREEN"; H_9105 does it regardless of color AND adds the no-selection baseline H_1568 lacked.
- a_mitosis_train from-scratch pure-split 🔴 wall — reconfirmed engine-native, escape via "living
  external selection" (C2) now CLOSED. Remaining: constructive (error-targeting) reproduction = not pure split.
