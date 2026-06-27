# 1620 — CLMB bind-readout codec: VERDICT = NO DEFECT (false-alarm root-caused)

## TL;DR
The reported "bind .clm export codec bug (overflow/NaN at core/clm_decode.py:424)"
is **NOT a codec defect**. It was a **spurious numpy FPE warning on arm64**
(numpy#25530) misread as weight corruption. The CLMB bind codec
(`serialize_v3_bind` ⇄ `core/clm_decode.{py,hexa}` RTYPE=1/2) round-trips REAL
303M weights faithfully, byte-parity across both production engines, with clean
held-out DESCENT and coherent argmax. Codec promoted DEFECT → **SOUND**.

## Root cause (file:line)
`core/clm_decode.py:424` — `mm = xcol @ Wt`. numpy's SIMD matmul loop on arm64
raises **spurious** `divide by zero / overflow / underflow / invalid` FPE flags
from uninitialized SIMD-lane padding (numpy#25530), **even when inputs AND outputs
are entirely finite**. Minimal repro: a plain `a@b` of finite small fp64 arrays
(output range [-2.3, 2.7], all finite) raises all four flags on arm64 + numpy
2.0.2. The flags do NOT corrupt the math.

Two cascading misreads from that warning:
1. "real-weight overflow/NaN" → there is no NaN: all 303M bind weights load with
   `non-finite=0`; the forward trace is unit-scale (|u|≈1.9, |v|≈1.1, |g=u*v|≈1.0).
2. golden_bind.py (B) torch-3way "FAIL" → used strict `argmax_t == argmax_p`, which
   int4 quant breaks on RANDOM UNTRAINED synth weights — the KNOWN-GOOD additive
   ctrl arm ALSO mismatches argmax under the same int4 quant (corr ~0.71). Not a
   bind-specific bug; just the int4 random-weight noise floor.

## Fixes (root-cause, no symptom-hiding)
- `core/clm_decode.py:_conv1d` — wrap the `@` in `np.errstate(divide/over/under/
  invalid="ignore")` with a comment citing numpy#25530. **Output byte-identical**
  (NOT a NaN mask — real non-finites still propagate; only the spurious FPE *flag*
  is silenced). Verified: synth bind CE unchanged (4.809992 before==after).
- `core/clm_decode.hexa` — comment-only parity note at `forge_dispatch_matmul`
  (native GEMM has no FPE flag; logic unchanged → 2-production parity preserved).
- `golden_bind.py` (B) — argmax-equality oracle → correlation floor (≥0.5)
  calibrated to the int4 random-weight baseline. Wiring is proven by golden (A)
  exact-numpy on the same .clm bytes (6e-3). Both goldens now PASS.

## Verification
- **EXACT-NUMPY golden (A): PASS 3/3** — independent erf-gelu forward on the same
  .clm bytes == py engine to max|Δlogit| 6e-3..7e-2 (gelu-Taylor residual, same
  on the additive twin → bind adds zero error).
- **TORCH 3-way golden (B): PASS** — torch fp32 vs int4 .clm decode corr 0.71
  (bind) / 0.84 (bind_linear) ≥ 0.5 int4 floor.
- **REAL 303M export + DESCENT (the deliverable):** torch ckpt
  `bind_seed7.pt` (d3784, L4, E4, k512) → `serialize_v3_bind(rt=1)` → 199.6MB
  `.clm`, `clm_decodable=True`, non-finite weights = 0. Held-out DESCENT gate
  `verify_clm_v2.py descent`: **F-CLM-DESCENT=1** (heldout_model_ce 2.301 <
  uniform 5.545 < shuffle 7.711, overfit_warning False). Coherent argmax
  ("nort favor and the consi").

## Engine-native A/B (terminal — live core/clm_decode.hexa, single decode each)
All three arms decoded through the live hexa production engine, nwin=4, corpus.txt:

| arm | RTYPE | model_ce | shuffle_ce | uniform_ce | argmax | green |
|-----|-------|----------|-----------|-----------|--------|-------|
| ctrl        | 0 | 1.852256 | 4.056270 | 4.799057 | "top of t" | ✓ |
| bind        | 1 | 1.815089 | 3.987012 | 4.799057 | "nort fav" | ✓ |
| bind_linear | 2 | 1.811047 | 4.028105 | 4.799057 | "late 198" | ✓ |

- All GREEN (model_ce < shuffle < uniform), all coherent, RTYPE correctly recovered.
- **hexa ⇄ py byte-parity (bind_seed7, nwin=4):** model_ce 1.815089 == 1.815089,
  shuffle/uniform identical, argmax "nort fav" == "nort fav", RTYPE=1 KBIND=512
  identical → LOCKSTEP confirmed across both production engines.

## Held-out CE A/B (nwin=64, English corpus.txt, py engine — DIRECTIONAL)
| arm | model_ce | green |
|-----|----------|-------|
| ctrl | 1.8225 | ✓ |
| bind | 1.9423 | ✓ |
| bind_linear | 1.7783 | ✓ |

Note: this English-only codec corpus ranks bind_linear < ctrl < bind — the int4
quant noise (~0.03–0.05 CE) is the same order as the arm gaps, and this is NOT the
4-cell pooled held-out. The **resolving** held-out ranking (bind < ctrl <
bind_linear, 3/3 seed-consistent, torch F.cross_entropy) lives in
`state/binding_arch_census/exp3_303m/RESULT.md` §1 and is unchanged by this codec
work. Codec verdict here is purely "the bind .clm decodes correctly", not a
re-litigation of the binding science verdict (🟠 DIRECTIONAL, capacity-gap
not-transferred at this train scale).

## G1/G6 engine-native A/B — BLOCKED on mac
303M G6 multiseed generation is too slow for the mac CPU foreground (heavy decode →
pool, per memory `heavy-anima-eval-pool-not-mini`). Single-decode CE + argmax
completed engine-native (above); full `cli/anima.hexa -- eval <clm>` G0-G6
multiseed needs a pool GPU host. RESULT.md already records the torch-probe G1/G6
(G1=0 floored all 9 runs, G6=1–5 noise) — codec does not change those. Follow-on:
G0-G6 single-entry on pool GPU for the 3 .clm.
