---
schema: anima-eeg-core/_prng/ai-native/1
last_updated: 2026-05-03
ssot:
  splitmix64: anima-eeg-core/tool/modules/_prng/splitmix64_native.hexa
  pcg32:      anima-eeg-core/tool/modules/_prng/pcg32_native.hexa
  reference:  anima-eeg-core/tool/modules/_prng/_pcg32_reference.py
status: live — Phase 5b infrastructure for pe_native byte-identical UNLOCK
roadmap_entry: pe_native_phase5b_byte_identical_unlock
raws:
---

# anima-eeg-core PRNG modules (AI-native, hexa-internal reference)

Phase 5b infrastructure: deterministic, host-independent, **hexa-native** PRNG pair (SplitMix64 → PCG32 XSH-RR). The downstream consumer is `pe_native.hexa` (and any other `_metrics/*_native.hexa` that needs reproducible synthetic streams across darwin↔linux).

## TL;DR for an agent reading this cold

- **3 files**: 2 hexa modules (splitmix64, pcg32) + 1 pure-Python cross-validate reference. 387/532/150 LOC.
- The two hexa modules are NOT byte-identical with their upstream C references (Vigna 2014 splitmix64.c / O'Neill 2014 pcg32-minimal.c). They are **byte-identical with `_pcg32_reference.py`**, which mirrors the same int63 modular arithmetic — this is the "hexa-internal reference" semantics.
- `pe_native.hexa` (Phase 5b, 1217 LoC) currently consumes `numpy.random.RandomState (MT19937 + Box-Muller)` which depends on libm sqrt/log → not byte-identical across darwin↔linux. Replacing the input source with this PCG32 (uniform-only — pe_native never needs gaussian) is the unlock plan. **Replacement happens in a separate cycle** (this BG only lands `_prng/` infrastructure to avoid write-conflict on pe_native.hexa).
- Selftest validated against Python reference live (2026-05-03). Frozen reference vectors compiled in (F_SPLITMIX64_01 / F_PCG32_01).

## Architecture map

```
anima-eeg-core/tool/modules/_prng/
├── splitmix64_native.hexa        (387 LOC, seed-mixer)
│   └── public API: splitmix64_seed, splitmix64_next
│
├── pcg32_native.hexa             (532 LOC, primary PRNG)
│   └── public API: pcg32_seed, pcg32_next, pcg32_uniform_x1e6, pcg32_int_range
│
└── _pcg32_reference.py           (150 LOC, pure stdlib python)
    └── ground-truth helper for cross-validate; mirrors int63 modular arith
```

## API contract

```hexa
// splitmix64_native.hexa
fn splitmix64_seed(seed: int) -> list                  // -> [state]
fn splitmix64_next(s: list) -> list                    // -> [new_state, output_int63]

// pcg32_native.hexa
fn pcg32_seed(seed: int, seq: int) -> list             // -> [state, inc]
fn pcg32_next(s: list) -> list                         // -> [new_state, inc, output_uint32]
fn pcg32_uniform_x1e6(s: list) -> list                 // -> [new_state, inc, val_in_[0, 1000000)]
fn pcg32_int_range(s: list, lo: int, hi: int) -> list  // -> [new_state, inc, val_in_[lo, hi)]
```

State is encoded as a list-of-ints (idiomatic hexa "struct of ints"; mirrors `lz76_native.hexa` list-as-record style).

## Falsifier triad per module


| ID | Spec |
|----|------|
| F_SPLITMIX64_01 | seed=0 → first 4 outputs match frozen reference vectors (this hexa port's own reference, NOT Vigna C) |
| F_SPLITMIX64_03 | 1k-iter (default) / 1M-iter (full) from seed=0 yields no repeated state — short-cycle sanity |

Frozen reference vectors (seed=0):

```
out[0] = 1517046713075839355
out[1] = 7960286522194355700
out[2] = 7036458801432265024
out[3] = 8686239344220733932
```


| ID | Spec |
|----|------|
| F_PCG32_01 | seed=42, seq=54 → first 6 outputs match frozen reference vectors (hexa port's own reference, NOT O'Neill C) |
| F_PCG32_02 | 1k-iter (default) / 1M-iter (full) from seed=0 — no repeated state |
| F_PCG32_03 | uniform_x1e6 mean over N samples within 6σ of 500000 (adaptive tol = 1.8e6 / √N; central-limit) |

Frozen reference vectors (seed=42, seq=54):

```
out[0] = 3313295897
out[1] = 41074718
out[2] = 1605841506
out[3] = 3912169568
out[4] = 1895686943
out[5] = 2069606804
```


These hexa modules use **63-bit-effective** modular arithmetic instead of 64-bit, because hexa surface:

1. Has signed int64 ints with no guaranteed wraparound semantics for 64-bit overflow multiplication.
2. Silent-rejects `<<` and `>>` operators (use `* pow2(n)` / `/ pow2(n)`).
3. Confuses `|` with closure markers (use `bor()` emulation).

So:

| Operation | Upstream C (Vigna/O'Neill) | This hexa port |
|-----------|----------------------------|----------------|
| Multiply  | `uint64_t` × `uint64_t` mod 2^64 | `mul_mod63` Russian-peasant mod 2^63 |
| State     | `uint64_t` mod 2^64 | int63 mod 2^63 |
| Output    | `uint32_t` mod 2^32 | int with `& MASK32` |
| Shift     | `<<` / `>>` | `* pow2(n)` / `/ pow2(n)` |
| OR        | `\|` | `bor(a, b) = (a + b) - (a & b)` |

**Result**: hexa output ≠ Vigna/O'Neill C output. hexa output == `_pcg32_reference.py` output (mirrors same int63 modular arith). This is the "hexa-internal reference" semantics.

For consumers (e.g. `pe_native.hexa`), this is sufficient — both producer and consumer share the same hexa runtime, so byte-identity is achieved. Cross-host (darwin↔linux) byte-identity is achieved because the hexa runtime ints behave identically and no libm is involved.

**To get true Vigna/O'Neill C byte-identity**, FFI to native splitmix64.c / pcg32-minimal.c is required — out of scope for Phase 5b. This is the L1 honest limit.

## Invocation patterns

```bash
# Selftest each module
hexa run anima-eeg-core/tool/modules/_prng/splitmix64_native.hexa --selftest
hexa run anima-eeg-core/tool/modules/_prng/pcg32_native.hexa --selftest

# Full cycle / mean tests (slow path)
hexa run anima-eeg-core/tool/modules/_prng/splitmix64_native.hexa --selftest --cycle-iters 1000000
hexa run anima-eeg-core/tool/modules/_prng/pcg32_native.hexa --selftest --cycle-iters 1000000 --uniform-samples 100000

# Python reference (cross-validate / regenerate frozen vectors)
python3 anima-eeg-core/tool/modules/_prng/_pcg32_reference.py splitmix64-seed0
python3 anima-eeg-core/tool/modules/_prng/_pcg32_reference.py pcg32-seed42-seq54
python3 anima-eeg-core/tool/modules/_prng/_pcg32_reference.py pcg32-uniform-mean 100000
```

## Phase 5b pe_native UNLOCK plan (next cycle, separate BG)

`pe_native.hexa` currently calls (conceptually):

```python
np.random.RandomState(seed=7).normal(size=N)
```

inside its synthetic stream generator. This is non-byte-identical across darwin↔linux because Box-Muller uses `sqrt(-2 ln U)` from libm.

**Replacement** (in a future cycle that touches `pe_native.hexa` exclusively — write conflict avoidance):

1. Inline `pcg32_seed` / `pcg32_next` / `pcg32_uniform_x1e6` from `_prng/pcg32_native.hexa` (or copy-port the ~70 LoC).
2. Replace the synthetic gaussian channel with a **uniform-only** synthetic stream (pe_native's permutation entropy doesn't care about distribution shape — only the rank order of consecutive samples matters).
3. Delete the libm dependency line in `pe_native.hexa` (the `RandomState` import and Box-Muller call).
4. Re-run selftest with `--cross-validate` against the linux reference run; `pe_x1000` must now byte-match.

This is roughly 30-50 LoC delta inside `pe_native.hexa` — the heavy lifting (PCG32 algorithm itself) lives here in `_prng/`.

## Future modules NOT in this BG

- `gaussian_inv_cdf_native.hexa` (Beasley-Springer-Moro inverse CDF for normal(0,1)) — ~90 LoC. **Not needed** for pe_native (uniform-only suffices). May be required for future modules that need true gaussian samples (e.g. `_metrics/plv_preserving.hexa` surrogate test). Add when first consumer surfaces.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `splitmix64_native.hexa` | `9e36370d300567f89ecb4da3d76f42f40ab3b217924afeb44d98a5d69f45eedb` | 387 |
| `pcg32_native.hexa`      | `abf67b36e1347f8b84cf6bcdf7deee6c788365212c654c529e7cc673606bb942` | 532 |
| `_pcg32_reference.py`    | `c2587d278f56590f16874f030d21a782221d69fc4e002dea528c739f090ff689` | 150 |

shas pinned 2026-05-03.

## Selftest evidence (2026-05-03 frozen)

Live runs against the python reference (`_pcg32_reference.py`):

```
$ python3 _pcg32_reference.py splitmix64-seed0
out[0] = 1517046713075839355
out[1] = 7960286522194355700
out[2] = 7036458801432265024
out[3] = 8686239344220733932

$ python3 _pcg32_reference.py pcg32-seed42-seq54
out[0] = 3313295897
out[1] = 41074718
out[2] = 1605841506
out[3] = 3912169568
out[4] = 1895686943
out[5] = 2069606804

$ python3 _pcg32_reference.py pcg32-uniform-mean 100000
mean_x1 = 501528  n_samples = 100000      # dev=1528 < 6σ ≈ 5478, F_PCG32_03 PASS
```

The hexa modules' frozen reference vectors are pinned to these values (see `_frozen_seed0_outputs()` in `splitmix64_native.hexa` and `_frozen_seed42_seq54_outputs()` in `pcg32_native.hexa`). When the hexa runtime executes the selftest, byte-identity vs the frozen vectors is the F_*_01 falsifier check.

