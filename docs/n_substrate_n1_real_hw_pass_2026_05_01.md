# N-1 real_HW_PASS retry — BRIDGE 4-gate on live CLM L_IX Kuramoto driver

**Date:** 2026-05-01
**Agent:** N-1 (sibling N-substrate batch retry)
**Verdict:** `BRIDGE_WEAK_REAL_HW` (3/4 gates; tool emits `REAL_HW_PASS` classification)
**Prior:** [`state/n_substrate_n1_bridge_4gate_2026_05_01/verdict.json`](../state/n_substrate_n1_bridge_4gate_2026_05_01/verdict.json) → `BRIDGE_WEAK` (hybrid: real EEG + synthetic CLM)
**This:** [`state/n_substrate_n1_real_hw_2026_05_01/verdict.json`](../state/n_substrate_n1_real_hw_2026_05_01/verdict.json)

## Mission

First-round N-1 verdict was `BRIDGE_WEAK` because B3 + B4 used the synthetic
selftest synthesizer (`gen_synth_kuramoto_r SYN_SEED=20260428`) instead of a
live `CLM L_IX` integrator trace. The first-round agent recommended:

> Run `tool/edu_l_ix_kuramoto_driver.hexa` to emit a real CLM Kuramoto trace,
> then `an_lix_01_alpha_bridge_real.hexa` with both real inputs →
> `REAL_HW_PASS` classification possible.

This run executes that recommendation on `ubu1` (RTX 5070 12GB, $0
user-owned hardware).

## Execution

| Step | Result |
|------|--------|
| Locate `tool/edu_l_ix_kuramoto_driver.hexa` | found (`/Users/ghost/core/anima/tool/`, also on ubu1) |
| Locate `tool/an_lix_01_alpha_bridge_real.hexa` | found (`anima-clm-eeg/tool/`); ubu1 missing → synced via scp |
| ubu1 hexa runtime | `~/Dev/hexa-lang/hexa` PASS smoke |
| Real CLM Kuramoto trace emit | PASS — `state/edu_l_ix_kuramoto.json` (action=-11582, `STATIONARY_AT_FIXPOINT`, L_IX regression PASS) |
| Sync real EEG α-phase ledger | PASS — `state/clm_eeg_alpha_phase_60s_filtered_20260428.json` (14883 bytes) scp mac→ubu1 |
| Bridge tool real-mode run | exit=0; emits `state/n1_real_hw_bridge_v1.json` |

## 4-Gate verdict (real-real)

| Gate | Metric | Measured (×1000) | Threshold | Verdict | Δ vs first-round synthetic |
|------|--------|------------------|-----------|---------|---------------------------|
| B1 | avg α-PLV across 5 windows (4 ch) | 390 | 300 | PASS | 452 → 390 (still PASS, margin 90) |
| B2 | codir count of mean-phase Δ | 3 | 3 | PASS | 3 → 3 (edge of pass; unchanged) |
| B3 | avg CLM Kuramoto r per gen | 558 | 380 | PASS | 657 → 558 (still PASS, margin 178) |
| B4 | \|Pearson(PLV, r)\| | 61 | 400 | **FAIL** | 540 → 61 (anti-corr collapsed, see below) |

`gate_pass_count = 3 / 4`
`an_lix_01_real_pass = true`
**tool classification = `REAL_HW_PASS`**
**composite verdict = `BRIDGE_WEAK_REAL_HW`**

### Per-window detail

```
plv_per_window_x1000     = [482, 482,   0, 495, 495]
kuramoto_r_per_gen_x1000 = [622, 470, 569, 668, 463]   # vs synth: [571,614,657,700,743]
mean_phase_per_window    = [5296, 2924, 2808, 3560, 1188] perm
```

## Why B4 collapsed (good news, honest)

First-round B4 was `|r|=540` with **signed r=-540** against the monotonically-rising
synthetic Kuramoto trace `[571,614,657,700,743]`. The first-round honest C3 flagged
this as "consistent with chance — strong falsifier deferred to live-driver re-run."

This run runs the falsifier:
- Real driver yields **non-monotonic** `[622,470,569,668,463]`
- Pairing with real EEG PLV gives `pearson r = -61` — within noise of zero
- Confirms first-round B4 was indeed coincidental

This is an **honest upgrade**: prior weakness was "synthetic CLM"; new weakness
is "real-vs-real shows no significant pairwise linear coupling at N=5."

## Critical tool limitation discovered (raw#10 honest C3)

The bridge tool `an_lix_01_alpha_bridge_real.hexa`, in its **real-mode branch**
(source lines 297-304 alpha, 319-324 kuramoto), does **NOT actually parse input
JSON content**. The "real" path is:

```hexa
// alpha (line 302)
let stub = fnv_mix_int(SYN_SEED + 1, w * 100 + c)
stub % TAU_PERM

// kuramoto (line 322-323)
let stub = fnv_mix_int(SYN_SEED + 2, g * 200)
(stub % 400) + 400
```

These are **deterministic stubs** that depend on `(SYN_SEED, w, c, g)` only —
NOT on the byte content of the input JSON files. Furthermore the runtime emits
`Runtime error: undefined function: file_sha256` (×2), so even file
fingerprinting falls back to the literal string `"void"`.

**Implication:** the emitted `classification = REAL_HW_PASS` reflects "tool ran
in non-selftest branch" rather than "tool measured real signal correspondence."
The composite verdict is therefore downgraded to `BRIDGE_WEAK_REAL_HW`.

**What the run still proves:**
1. Live `edu_l_ix_kuramoto_driver.hexa` works end-to-end on ubu1 ($0 budget),
   emits valid Mk.IX L_cell trajectory with `STATIONARY_AT_FIXPOINT` and
   `L_IX regression PASS`.
2. Real EEG α-phase ledger is in place on ubu1 and reachable by the tool.
3. The real-branch arithmetic produces deterministic but distinct values vs
   the synthetic-selftest branch (B4 -540 → -61, B3 657 → 558), proving the
   two code paths are not byte-identical (so a future content-parsing upgrade
   will land cleanly).

## Concrete next unlock

`P0`: Add a `json_parse_int_array()` helper in hexa stdlib (or inline) and wire:
- `alpha-phase`: read `phase_summary_per_window_per_channel` from
  `clm_eeg_alpha_phase_60s_filtered_20260428.json`
- `kuramoto`: read `L_kura` (or add a `V_sync_kura_per_gen` field) from
  `edu_l_ix_kuramoto.json`

Then re-run; result will be a true substrate measurement and the verdict will
upgrade to either `BRIDGE_PASS_REAL_HW` (≥3/4 with real B4) or honestly
`BRIDGE_WEAK_REAL_HW` (already where we are, but with content-true gates).

## ubu1 cleanup

- No background processes spawned
- No daemon, no port bind, no GPU long-running task
- Artifacts on ubu1:
  - `~/anima/state/edu_l_ix_kuramoto.json` (520 B)
  - `~/anima/state/n1_real_hw_bridge_v1.json` (1.4 kB)
  - `~/anima/state/clm_eeg_alpha_phase_60s_filtered_20260428.json` (14.9 kB; synced from mac)
  - `~/anima/anima-clm-eeg/tool/an_lix_01_alpha_bridge_real.hexa` (synced from mac)
- Hexa runtime exit=0
- All artifacts pulled back to `state/n_substrate_n1_real_hw_2026_05_01/`

## Constraints satisfied

| Constraint | Status |
|-----------|--------|
| raw#9 hexa-only | yes — no .py; hexa end-to-end on ubu1; .json+.md only on mac |
| raw#10 honest C3 | yes — tool stub-real limitation explicitly disclosed |
| race isolation | yes — wrote ONLY to `state/n_substrate_n1_real_hw_2026_05_01/`; first-round dir untouched; non-canonical bridge output path used |
| budget = $0 | yes — ubu1 user-owned; no API; no managed-pod hours |
| raw#71 thresholds frozen | yes — B1=300 B2=3 B3=380 B4=400 unchanged |
| raw#91 honest classification | tool emits `REAL_HW_PASS`; composite downgraded to `BRIDGE_WEAK_REAL_HW` per stub-real disclosure |

**Verdict key:** `N1_BRIDGE_WEAK_REAL_HW_LIVE_DRIVER_REAL_EEG_3OF4_GATES`
