# qentropy A/B benchmark — quantum vs deterministic

`qentropy_benchmark.py` is a one-command, Mac-runnable (`$0`, no device, no torch)
A/B harness that compares anima's **quantum** entropy default against its
**deterministic** auxiliary, per entropy seed/sample path.

> **Honest framing — read this first.** This is a **statistical-parity sanity check
> + a provenance differentiator**, *not* a superiority test. ANU vacuum-fluctuation
> entropy is statistically **equal** to a chacha20/numpy PRNG (#123-A: JSD 0.000433,
> 23× under the NIST SP 800-22 7/7 threshold). We therefore **expect** the two modes
> to be statistically indistinguishable at the application level — and confirming
> that is the whole point. The difference that actually matters, and the only reason
> both modes exist, is **provenance / auditability**: quantum draws carry the real
> physical ANU origin (`tier=anu_committed` + a `sha256` you can pin to a draw);
> deterministic draws carry a reproducible `numpy_prng` seed. The benchmark surfaces
> that provenance column alongside the (expected-equal) metrics.

## How to run

Full A/B over all SW-runnable paths (the harness sets `ANIMA_ENTROPY_MODE` itself,
per arm, in a fresh subprocess — you do **not** set it for the full run):

```bash
python3 mirror/qmirror/seed/qentropy_benchmark.py                 # N=128, JSON to stdout
python3 mirror/qmirror/seed/qentropy_benchmark.py --n 256         # more trials per arm
python3 mirror/qmirror/seed/qentropy_benchmark.py --out state/.../ledger.json
python3 mirror/qmirror/seed/qentropy_benchmark.py --json | jq .   # pipe-friendly
```

Run a **single path module in one mode manually** (the env you set is honored
because the module imports `qentropy` fresh in that process):

```bash
ANIMA_ENTROPY_MODE=quantum       python3 PLASTICITY/plasticity_sw_approx.py
ANIMA_ENTROPY_MODE=deterministic python3 PLASTICITY/plasticity_sw_approx.py
ANIMA_ENTROPY_MODE=quantum       python3 CORE/DECODER/decoder_qsample.py
ANIMA_ENTROPY_MODE=deterministic python3 CORE/DECODER/decoder_qsample.py
```

### Why a subprocess per arm
`qentropy.py` reads `ANIMA_ENTROPY_MODE` **at import time** (module-global `_MODE`).
Once imported, mutating `os.environ` would not change its behavior. So each
`(path, mode)` arm runs in a fresh `python3 -c …` subprocess with the env set — the
mode is honestly fresh per arm, and the harness's own import of `qentropy` can never
contaminate an arm.

## What each metric means

| path | metric | meaning |
|---|---|---|
| `plasticity_sw_approx` | `weight_l1` | L1 norm of the SW-learned weight matrix per trial. The weight **init** is the qentropy-sourced lever; the input spike pattern is held fixed across trials (fixed numpy seed inside the arm) so the only varying factor is the entropy path under test. |
| `decoder_qsample` | `token_hist_entropy_bits` | Shannon entropy (bits) of each trial's sampled-token histogram, drawn from a **fixed** logits vector. The forward logits are identical in both modes — only the draw differs. A pooled per-mode token histogram is also recorded. |

For each path the ledger reports, per mode: `{n, metric_mean, metric_std,
provenance{mode,tier,sha256}}`, plus a **`formal_test`** block (C7 upgrade).

### The formal two-sample test (C7)

The original v1 ledger used a coarse closeness statistic `|Δmean| / pooled_std`.
**C7 upgrades this to a proper two-sample statistical test** so the parity claim is
rigorous. Per path:

- **`primary`** — a two-sample **Kolmogorov–Smirnov** test (`scipy.stats.ks_2samp`)
  on the **continuous per-trial metric** (`weight_l1` / `token_hist_entropy_bits`).
  KS compares the *full empirical CDFs* of the two modes' N≥128 per-trial samples,
  not just their means. Reports `{ks_D, p_value, n_quantum, n_deterministic,
  parity_at_alpha_0.05}`.
- **`token_histogram_chi2`** (decoder path only) — a **chi-square contingency** test
  (`scipy.stats.chi2_contingency`) on the 2×K pooled token-count table, plus a
  **Cramér's V** effect size. This is a *secondary, diagnostic* test (see caveat
  below).
- **`coarse_separation`** — the old `|Δmean| / pooled_std`, kept as a descriptive
  field for continuity.
- **`parity_verdict`** — a human-readable verdict driven by the **primary KS** test.

**How to read the p-value (the whole point):** H0 (null) = *"both modes' samples come
from the same distribution."*

- **`p_value > 0.05` ⇒ FAIL TO REJECT H0 ⇒ statistical PARITY ⇒ the EXPECTED, DESIRED
  result.** This reproduces #123-A (ANU quantum ≡ PRNG) with a real test. It is **not**
  a null finding to bury — it is the claim confirmed rigorously. `parity_at_alpha_0.05
  = (p_value > 0.05)`.
- `p_value < 0.05` ⇒ REJECT H0 ⇒ a distributional difference. On these modes that is a
  surprise — likely a small-sample artifact or a real implementation asymmetry. The
  harness reports it **honestly, un-massaged**.

**scipy is OPTIONAL.** If `scipy.stats` imports it is used (the fast-path). If scipy is
**absent**, a self-contained **pure-python** two-sample KS (D statistic + asymptotic
Kolmogorov p-value via the `Q_ks` series) and a pure-python chi-square (incomplete-
gamma upper tail) are used — **zero hard deps**, identical output schema. Which engine
ran is recorded per test as `engine: scipy | pure-python` (the fallback is validated
to match scipy: KS D exact, chi-square exact, KS p within asymptotic tolerance and the
same accept/reject decision).

`provenance_differs` stays `true` because quantum (`anu_committed` + sha256) and
deterministic (`numpy_prng(187)`, no sha256) carry different audit trails. **This is
the load-bearing column.**

## Latest result (Mac, N=128, scipy)

Ledger v2 (KS): `state/qentropy_benchmark_2026_06_06/ledger_v2_ks.json` · verdict:
`.verdicts/924_qentropy_substrate_agnostic/c7_formal_parity.txt`
(v1 coarse ledger kept at `…/ledger.json`).

| path | metric | KS D | KS p_value | parity (p>0.05) | provenance |
|---|---|---|---|---|---|
| `plasticity_sw_approx` | `weight_l1` | 0.0703 | **0.9114** | ✅ PARITY | q=`anu_committed`/`e8123b96…` · det=`numpy_prng(187)` |
| `decoder_qsample` | `token_hist_entropy_bits` | 0.1016 | **0.5257** | ✅ PARITY | q=`anu_committed`/`e8123b96…` · det=`numpy_prng(187)` |

**Both KS tests fail to reject the null (p ≫ 0.05) → statistical parity confirmed
rigorously.** This is the #123-A claim reproduced with a real test, and it is the
desired sanity result. Provenance differs on both.

### Honest caveat — the secondary chi-square rejects (and why that's fine)

The decoder path's *secondary* pooled-token chi-square **rejects** (`chi2=14.50,
dof=5, p=0.0127 < 0.05`). Reported un-massaged. But:

- **Effect size is negligible: Cramér's V = 0.0595 (< 0.1).** A chi-square at very
  large pooled N (here 2048 + 2048 = 4096 draws) is power-saturated and rejects on a
  *negligible* difference.
- It compares **two single fixed realizations** — the committed ANU buffer (sha256
  `e8123b96…`) vs a fixed `numpy_prng(seed=187)` — so it is effectively testing two
  specific finite samples, not two distributions; the result is **fully reproducible
  run-to-run** (not a sampling fluke).
- The **trial-respecting KS test** (128 independent trial-level statistics) is the
  appropriate parity test and it **confirms parity** (p=0.526). The chi-square is kept
  as a diagnostic with its effect size attached, so a reader sees both numbers and
  their interpretation.

This is exactly the honest framing #123-A prescribes: a power-saturated chi-square can
*reject* while the effect is negligible — that is a property of large-N chi-square, not
evidence that quantum entropy differs in quality from a PRNG.

## Extending to the device / torch paths later

Three paths are recorded in the ledger as `device_pending_rows` (status
`device-pending` / `torch-pending`). They run the **same A/B** — just flip the env on
the host that has the silicon/torch. No harness change is needed for a manual A/B;
each already routes through the qentropy SSOT:

| path | host | how to run the A/B |
|---|---|---|
| `akida_r2_noise` | pi5-akida (AKD1000) | `ANIMA_ENTROPY_MODE={quantum,deterministic} python3 SUB_ENGINES/AKIDA/scripts/spontaneous_emission.py` — compare the R2 spontaneous-noise symbol histogram / spike rate. |
| `akida_edge_learn` | pi5-akida (AKD1000) | `ANIMA_ENTROPY_MODE={quantum,deterministic} python3 SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py` — compare the on-chip learned winner-unit distribution. |
| `torch_lane_p` | GPU host (Lane-P) | `ANIMA_ENTROPY_MODE={quantum,deterministic} python3 CLM/train/_qseed_check.py` — compare `torch.manual_seed → torch.rand` samples. |

To **fold these into the automated harness** once their hosts are reachable: add an
`arm_<path>(mode, n)` runner in `qentropy_benchmark.py` (mirroring `arm_plasticity` /
`arm_decoder`) that imports the device/torch module in the per-arm subprocess and
returns `{"metrics": [...], "provenance": {...}, "extra": {...}}`, then append it to
the `runnable` list in `build_ledger`. The pending row for that path can then be
removed from `PENDING_PATHS`. The expectation on every device/torch path is the same:
**parity in the metric, divergence in the provenance.**

## Honest non-claim

This benchmark does **not** and **cannot** show quantum entropy is "better". The two
modes are by design statistically equal. The auditable provenance (physical ANU
origin + sha256) is the only real differentiator — and that is what the ledger makes
visible per path and per mode.
