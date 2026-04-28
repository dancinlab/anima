# LZ76 verifier audit — 2026-04-28 (read-only, no commits)

Target: `/Users/ghost/core/anima/anima-clm-eeg/tool/clm_eeg_lz76_real.hexa`
Reference commit: `50002d89` (HEAD-touch of this file)

## 1. Commit 50002d89 metadata

- author: dancinlife <nerve011235@gmail.com>
- date: 2026-04-28 19:09:20 +0900
- title (misleading): `fix(an11-fire18): Mode H fix #4 — cuda_max_good>=12.8 복원 + cu118 force-reinstall 제거`
  → commit message focuses on an11 dispatch but the same commit ALSO bundles the LZ76 verifier
    upgrade (568-line diff in `clm_eeg_lz76_real.hexa`). The lz76 changes are NOT mentioned
    in the commit message — discoverability hazard, not a correctness issue.
- file diff: 568 insertions/changes in `clm_eeg_lz76_real.hexa` (file went from a smaller
  env-only version to the full 986-line CLI verifier present today).

## 2. Diff intent (recovered from the diff itself)

Pre-50002d89 file had:
- env-controlled IO only (`CLM_EEG_LZ76_SELFTEST=1`, `CLM_EEG_RAW_ARRAYS_JSON=<path>`).
- single synthetic mode (FNV hash → "random"-ish).
- no JSONL audit trail.
- no `.npy` real-data path.

Post-50002d89 (current file):
- proper CLI: `--selftest`, `--selftest-mode {random|structured}`, `--input <path>`,
  `--audit-jsonl <path>`, `--out <path>`, `--help`. Legacy env vars still respected.
- second selftest mode: `synth_channel_structured(...)` (square-wave, period=64 →
  highly compressible signal; reference target b<<0.3).
- `.npy` ingest via `/tmp/clm_eeg_lz76_npy_helper.py` auto-generated helper
  (raw#9-compliant — `.py` is /tmp-only, never persisted in repo). Auto-detects
  16ch×N vs N×16ch vs BrainFlow 32-row layout.
- sha256 of `.npy` recorded in audit JSONL via `shasum -a 256` (Darwin native).
- JSONL audit append per run with schema:
  `{ts, mode, input, sha256, n_channels, n_samples, c_n, lz76_norm_x1000,
    b_n_x1000, verdict, reference}`.
- `classify_b_n_x1000(...)` helper centralises C1/C2 pass logic; reused by main + selftest.
- ordering hypothesis `b(random) > b(structured)` documented as JSONL-inspector
  responsibility (single-process "both" mode triggers a hexa-runtime OOM by design;
  spec says run twice and read the two rows).

## 3. raw#12 frozen-criteria audit (CRITICAL)

The three `let` constants at lines 71-73 were NOT mutated by 50002d89:

```
let LZ76_EEG_MIN_X1000        = 650
let DELTA_HUMAN_MAX_PERMILLE  = 200
let HUMAN_BASELINE_LZ76_X1000 = 850
```

Diff shows the exact same `c1_pass = if lz_norm_x1000 >= LZ76_EEG_MIN_X1000` etc.
moved into a helper function — values unchanged. raw#12 / raw#71 frozen-hypothesis
contract intact. SAFE.

## 4. Current file state

- LoC: 986
- Permissions: `-rw-r--r--@` regular file. **NOT uchg-locked** (no `uchg`/`schg` flag in `ls -lO`).
- xattr `@` present (likely com.apple.quarantine/macOS extended attrs, not a lock).

## 5. Self-test execution (read-only, used `/Users/ghost/core/hexa-lang/hexa.real`)

`--help` works. Two-pass selftest succeeded:

Random mode (UTC 10:40:57Z):
```
mode=random  n_ch=16  n_samples=16  binarized_length=256
c(n)=39  b(n)_x1000=1218  C1_pass=1  C2_pass=0  classification=NOT_VERIFIED_SYNTHETIC
verdict=SELFTEST_OK
```

Structured mode (UTC 10:41:04Z):
```
mode=structured  n_ch=16  n_samples=16  binarized_length=256
c(n)=8   b(n)_x1000=250   C1_pass=0  C2_pass=0  classification=NOT_VERIFIED_SYNTHETIC
verdict=SELFTEST_OK
```

Ordering check: `b(random)=1218 > b(structured)=250` — HOLDS.
Reference asymptotes (Kaspar-Schuster 1987 random→1.0, square-wave→<0.3) honored
in spirit. Note default `n_samples=16` per channel is intentionally tiny for the
sanity selftest; small-n LZ76 overshoots 1.0 (1.218 here) which is a known
finite-size effect, not a bug — Kaspar-Schuster asymptote applies n→∞.

JSONL audit verified (sample row):
```
{"ts":"2026-04-28T10:40:57Z","tool":"clm_eeg_lz76_real","mode":"selftest",
 "input":"synthetic_fnv_random","n_channels":16,"n_samples":16,
 "binarized_length":256,"c_n":39,"b_n_x1000":1218,"verdict":"P1_FAIL",
 "classification":"NOT_VERIFIED_SYNTHETIC","selftest_mode":"random",
 "reference":"Kaspar-Schuster 1987 (Phys Rev A 36:842) | Schartner 2017"}
```

Pre-existing default-path JSONL `state/clm_eeg_lz76_audit/test_random.jsonl`
(written 19:09 by the user during commit-time validation) contains the same
two rows with identical c_n/b_n values — bit-for-bit reproducible (raw#65 idempotent).

## 6. Real-hardware (.npy) path — code review only, NOT executed

- helper auto-write path: `/tmp/clm_eeg_lz76_npy_helper.py`
- helper output: `/tmp/clm_eeg_lz76_npy_dump.txt` (n_ch=, n_samp=, then ch-major ints×1e6)
- ingest function: `load_npy_via_helper(npy_path)` returns flat list:
  `[n_ch, n_samp, ch0_s0, ch0_s1, ..., ch15_sN-1]`
- shape auto-detect: 16×N, N×16, BrainFlow 32×N (rows 1..17), N×32.
- failure mode on rc!=0: returns `[-1, -1]` sentinel; main path must check.
  (Did not verify this branch handling in main — TODO before live run.)
- sha256 of input file recorded for manifest.

Code path looks correct, no real .npy was supplied so this is a code-review
verdict only — NEEDS_HARDWARE for empirical confirmation.

## 7. raw#10 honest classification

| component | classification | evidence |
|---|---|---|
| --selftest random | **VERIFIED** | exit=0, b=1218, two-pass JSONL row present, deterministic across reruns (19:09 run == 10:40 run). |
| --selftest structured | **VERIFIED** | exit=0, b=250, JSONL row present, ordering b(rand)>b(struct) holds. |
| --help | **VERIFIED** | prints all flags + legacy env list. |
| --input <.json> path | **PARTIAL** | code path exists (parse_raw_arrays unchanged from earlier version), not executed in this audit because no real ingest JSON was supplied. |
| --input <.npy> path | **NEEDS_HARDWARE** | helper-write + load_npy_via_helper code complete; no `.npy` available to drive end-to-end run. shape-mismatch / helper-rc!=0 branches unverified. |
| frozen criteria (raw#12) | **VERIFIED** | constants 650/200/850 byte-identical pre/post-50002d89. |

## 8. Risk register

- LOW: commit message hides LZ76 upgrade behind an11-fire18 title; future bisect harder.
- LOW: small-n selftest overshoots Kaspar-Schuster asymptote (b=1.218 vs 1.0
  target); fine for kernel sanity, NOT a calibration of EEG-realistic n.
- MEDIUM: `--audit-jsonl /tmp/...` write attempt during this audit silently no-op'd
  (file did not appear; whereas writing to `state/clm_eeg_lz76_audit/...` worked).
  Possible `/tmp` path handling edge case in `append_jsonl`. Worth a 5-min look
  before relying on the flag with arbitrary paths.
- LOW: raw#71 falsifier mirror not re-checked against `clm_eeg_p1_lz_pre_register.hexa`
  SSOT in this audit (only the 3 `let` values were verified).
