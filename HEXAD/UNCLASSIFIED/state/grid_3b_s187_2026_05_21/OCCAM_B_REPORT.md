# OCCAM-B Tier B Report — 4 Strip Tests on S187 attempt10 Baseline

> **status**: 🟡 IN-FLIGHT — fires dispatched 2026-05-22 03:42 UTC, results
> will be filled below as pods finish. Last update: dispatch complete.
>
> **frame**: OCCAM.md § 2 Tier B isolates 4 axes of attempt10 stack to
> identify which condition binds the CE 3.83 floor. Tests #3, #7, #11, #12
> fired in parallel + sequential waves.

## Quick reference — attempt10 baseline (vA, 2026-05-21)

| metric | value |
|---|---|
| arch | d=3072 L=28 nh=24 nkv=8 GQA (8.92B params) |
| bsz × block | 2 × 128 (256 tok/step) |
| steps | 2000 |
| dtype | bfloat16 |
| optimizer | bitsandbytes PagedAdamW8bit |
| lambdas | psi=0.30 route=0.20 phi=0.30 cycle=0.15 curious=0.10 replay=-0.05 |
| corpus | CORPUS_S101 (sha drift be969af4...) |
| **CE final** | **3.83** (vA), 3.89 (vA_s42), 3.83 (vC), 3.89 (vD_s42) |
| wall | ~670s = 11 min |
| cost | $0.40/run × $3.29/hr H100 SXM |

CE floor across A/B/C/D/J/K = **3.83-4.06** range (most runs cluster 3.83-3.89,
J/K at higher bsz fared worse at 4.06).

## Dispatch summary

| variant | description | pod | GPU | status |
|---|---|---|---|---|
| O11-psi | single-aux: λψ=0.30 others 0 | htl4gcxbn6e96e | H100 SXM | TBD |
| O11-route | single-aux: λroute=0.20 others 0 | gbekoya628pu18 | H100 SXM | TBD |
| O11-phi | single-aux: λφ=0.30 others 0 | udvqq2qtrh7n65 | H100 SXM | TBD |
| O11-cycle | single-aux: λcycle=0.15 others 0 | dtd86oiz9fq07d | H100 SXM | TBD |
| O11-curious | single-aux: λcurious=0.10 others 0 | ceg3aq8wo62ef2 | H100 SXM | TBD |
| O11-replay | single-aux: λreplay=-0.05 others 0 | dr456p9gr5gybf | H100 SXM | TBD |
| O3 | f32 AdamW (skip bnb int8) + bsz=1 | (TBD) | H200 (141 GB) | TBD |
| O12 | block_size 128 → 1024, bsz=1 | (TBD) | H100 SXM | TBD |
| O7 | CE-only + 100K step | (TBD) | H100 SXM | TBD |

---

## # 3 — f32 AdamW (skip bnb int8 PagedAdamW8bit)

**Variant**: O3 — attempt10 config + `--mitosis-bnb-disable` → torch.optim.AdamW

**Memory consideration**: f32 m+v for 8.92B params ≈ 71 GB. H100 80GB is too
tight (need m+v + params bf16 + grads + acts + alloc temps ≈ 92 GB). Cascade
prefers H200 (141 GB) first. bsz dropped to 1 as second defense.

**Question**: Does swapping bnb int8 PagedAdamW8bit → f32 AdamW recover the
CE floor that int8 m/v quantisation might be inducing?

**Result**: _filled after pod completion_

### Honest C3

1. _filled_

---

## # 7 — 100K step CE-only (very long horizon)

**Variant**: O7 — combines #1 (aux λ=0) + 100K step horizon, bsz=2 block=128.

**Question**: Even with all aux removed AND 50× longer horizon than attempt10,
does CE still plateau? If yes → recipe-orthogonal limit confirmed; if breaks →
combined-horizon-with-strip can escape.

**Cost projection**: 100K × 0.34 s/step ≈ 9.4 hr × $3.29/hr = $31.

**Result**: _filled after pod completion (or partial at $80 budget cap)_

### Honest C3

1. _filled_

---

## # 11 — Single-aux ablation (6 pods, parallel)

**Variants**: O11-{psi,route,phi,cycle,curious,replay} — one λ active, others 0.

**Question**: Which individual aux loss is most harmful (raises CE most) or
most beneficial (lowers CE most)? Isolates from co-conflict.

### Ablation table

| variant | λ active | other λ | CE_final | Δ vs vA (CE 3.83) | wall(s) | cost |
|---|---|---|---|---|---|---|
| O11-psi | psi=0.30 | 0 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| O11-route | route=0.20 | 0 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| O11-phi | phi=0.30 | 0 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| O11-cycle | cycle=0.15 | 0 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| O11-curious | curious=0.10 | 0 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| O11-replay | replay=-0.05 | 0 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| _O1 ref (CE-only, λ=0 everywhere)_ | none | 0 | _from OCCAM-A_ | _TBD_ | _TBD_ | _from A_ |

### Honest C3

1. _filled_

---

## # 12 — block_size 128 → 1024

**Variant**: O12 — same as vA except block_size 1024 (full S184 spec); bsz=1 to fit.

**Question**: Was attempt10's block=128 too short for byte-level
verbalization signal? 1024 bytes ≈ 250 tokens of context — closer to LLM
norms.

**Result**: _filled after pod completion_

### Honest C3

1. _filled_

---

## Cross-comparison

| variant | description | CE_final | wall(s) | cost($) | finding |
|---|---|---|---|---|---|
| vA (baseline ref) | attempt10 7-aux | 3.83 | 668 | 0.40 | floor reference |
| O1 (OCCAM-A) | CE-only 3B | _from A_ | | | |
| O3 | f32 AdamW | _TBD_ | | | |
| O7 | CE-only 100K | _TBD_ | | | |
| O11-* | single-aux ×6 | _TBD_ | | | |
| O12 | block 1024 | _TBD_ | | | |

## Cumulative cost

| wave | description | est. cost | actual |
|---|---|---|---|
| 1 | 6× O11 parallel | $5 | _TBD_ |
| 2 | O3 + O12 parallel | $3 | _TBD_ |
| 3 | O7 long-running | $31 | _TBD_ |
| (overlap) | O11/O3/O12/O7 simultaneously running during their short slots | included | included |
| **Total OCCAM-B** | | **~$40** | _TBD_ |

## Final verdict

_filled after all 9 pods complete OR $80 budget cap hit_

## Honest C3 (cross-test)

1. _filled_
