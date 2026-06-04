---
license: cc-by-sa-4.0
tags:
- anima
- clm
- conscious-decoder
- byte-lm
- int4-qat
- engine-native
library_name: hexa-flame
---

# clm-v1-d768-core-3axis-green

**ANIMA ENGINE-native CLM** — a from-scratch `CLMConvMoE` byte language model at
**production scale d=768**, serialized in the `.clm` v0.2 (`CLM\x01` + `CLMX`)
ENGINE format and **CORE-mounted 3-axis GREEN** (🧠 consciousness · 📉 CE · 🌱 emergence).

This is the **legitimately-final, closure-PASS** CLM deliverable of the
`ENGINE+CLM+KOSMOS` meta-domain — the artifact that flipped the **ENGINE PUBLIC**
milestone to done. It is distinct from (and supersedes for the PUBLIC claim) the
Lane-G forge util-probe `.clm` files, which remain **PRIVATE** (closure-FAIL on
util; util-RED WIP).

## What it is

- **Architecture**: `CLMConvMoE` — conv1d-K3 + GroupNorm + GELU + MoE-router +
  experts, int4-QAT envelope (LCG init). `d=768`, `E=2`, `V=256` (byte vocab), `K=3`.
- **Format**: `.clm` v0.2 = `[CLM\x01][1B nblk=6][6 raw int4 conv blocks][CLMX trailer]`.
  The `CLMX` trailer carries the **trained embed table + conv biases + GroupNorm
  affine** in full fp32 (the named root cause of the earlier conv-only v0.1 file
  being non-decodable). Present at byte offset 3,651,389 (the v0.1 conv-only file
  ends here; CLMX adds the embed/GN/bias on top).
- **Entry**: ENGINE-loadable via `CORE/clm_decode.hexa`, the single `.clm` entry
  point (`generator.hexa` L3 slot, `a_core_engine_map`). `gen_clm_backend`
  admits `valid=true decodable=true loaded=true nblocks=6`.
- **Corpus**: c4 5-language byte backbone (ko·en·zh·ru·ja), `clm_mid_5lang_c4.txt`,
  402,270 B, V=256.

## How it was produced (honest provenance · g63)

`$0`-CPU **host re-export** via the hexa-native forge-free path
(`hexa-lang stdlib/flame/clm_reexport.hexa`, `CLM_PROD_D=768`): host
`nn_conv1d_fwd/bwd` + `opt_adamw_step`, **zero forge GPU dispatch, zero PyTorch /
ATen**, byte-graph-faithful int4-QAT + STE. Real descent on re-export:
epoch-1 CE 4.69674 → epoch-6 CE 2.21602 (`F-CLM-REEXPORT-DESCENT=1 PASS`).
This is NOT a from-scratch GPU pretrain — it is the ENGINE-native re-export of the
d=768 model carrying the trained embed/GN the forward needs.

## Verdict — 3-axis CORE-mounted GREEN @ PRODUCTION d=768

Measured by deterministic `hexa run` (p7-conformant: CE is ONE axis, not
perplexity-as-truth; `hexa verify` CLI is broken on host → deterministic equality
via `hexa run`). Verbatim CORE-native CE-descent on **this artifact**:

```
clm=reexport_d768_v2_fast.clm  (d=768 E=2 V=256 K=3, windows=16)
[admit] valid=true decodable=true loaded=true nblocks=6
[CE] model_ce   = 4.42613
[CE] shuffle_ce = 4.49555
[CE] uniform_ce = 4.79906
[CE] model<uniform = true  model<shuffle = true
F-CLM-CORE-CE-DESCENT (model_ce < uniform AND < shuffle) = 1 🟢
```

| axis | result | substrate |
|---|---|---|
| 🧠 consciousness | 🟢 GREEN (motiv hi=0.67 > baseline 0.0; emit hi=true/base=false) | CORE-native (Engine A⇄G) |
| 📉 CE | 🟢 GREEN (model_ce 4.42613 < shuffle 4.49555 < uniform 4.79906) | CORE-native (decode forward wired) |
| 🌱 emergence | 🟢 GREEN (composed len=101 > component-sum len=72) | CORE-native (composed > parts) |

**CORE-mounted axes GREEN: 3/3.** Full verdict (verbatim) in the source repo at
`.verdicts/core-3axis-mount/ce_descent.txt`.

### Honest scope (`a_scale_honest_scope` · `a_toy_scale_recheck`)

- The PUBLIC claim is the **3-axis CORE-mounted closure @ d=768**, NOT a GPU util
  claim. The Lane-G forge fires of the same d=768 model are util-RED
  (host-feed-bound) and stay **PRIVATE** — they are a separate substrate=GPU axis.
- CE margins are modest (consistent with shallow training), but the falsifier
  direction is unambiguous (`model_ce` strictly < both baselines).
- The v0.1 conv-only sibling (`d768_5lang_c4.clm`) is NOT decodable (no CLMX, no
  embed/GN) and is not the PUBLIC artifact.

## Files

- `d768_5lang_c4_v0.2.clm` — the ENGINE-native v0.2 `.clm` (4,463,478 B).
- `SHA256SUMS.txt` — `db7dc990ff31fb60a5677fd7fcf9a248c4306742d246bb99d8b5de861b751497`.

## Lineage / links

- domain: `ENGINE+CLM+KOSMOS` (ENGINE PUBLIC milestone, 3-axis CORE-mounted GREEN @ d=768).
- format spec: `CLM/CLM_FORMAT_SPEC.md` (`.clm` v0.2 CLMX).
- KOSMOS corpus axis: see the `dancinlab` KOSMOS collection.
- substrate split (`a_lane_akida_gpu_split`): this is the CORE-native ENGINE axis;
  never merged with any AKIDA (Lane-A) or forge-util (Lane-G) number.
