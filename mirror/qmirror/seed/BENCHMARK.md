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
python3 mirror/qmirror/seed/qentropy_benchmark.py                 # N=64, JSON to stdout
python3 mirror/qmirror/seed/qentropy_benchmark.py --n 128         # more trials per arm
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
provenance{mode,tier,sha256}}`, plus a two-sample **`comparison`**:

- `standardized_separation = |Δmean| / pooled_std` — near **0** ⇒ statistically
  indistinguishable (**PARITY**, the expected outcome); a large value (`> ~1`) would
  flag a coupling anomaly to investigate. This is a *parity* statistic, **not** a
  win metric.
- `provenance_differs` — `true` because quantum (`anu_committed` + sha256) and
  deterministic (`numpy_prng(187)`, no sha256) carry different audit trails. **This
  is the load-bearing column.**

## Latest result (Mac, N=64)

Ledger: `state/qentropy_benchmark_2026_06_06/ledger.json` · verdict:
`.verdicts/924_qentropy_substrate_agnostic/m6_benchmark.txt`

| path | metric | quantum mean | det mean | sep | parity | provenance |
|---|---|---|---|---|---|---|
| `plasticity_sw_approx` | `weight_l1` | 10.2511 | 10.2110 | 0.104 | PARITY | q=`anu_committed`/`e8123b96…` · det=`numpy_prng(187)` |
| `decoder_qsample` | `token_hist_entropy_bits` | 1.6952 | 1.6626 | 0.106 | PARITY | q=`anu_committed`/`e8123b96…` · det=`numpy_prng(187)` |

Parity holds on both SW paths (separation ≈ 0.10 ≪ 1.0); provenance differs on both.
The #123-A statistical-equality claim reproduces at the **application** level.

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
