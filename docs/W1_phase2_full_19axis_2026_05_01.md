# W1 Phase 2 — full 19 axes + 6 ledgers Φ trace

**Agent**: W1 PHASE 2
**Date**: 2026-05-01
**Track**: extension of W1 Phase 1 (`docs/W1_anima_self_substrate_2026_05_01.md`)
**Budget**: $0 (data analysis only, off-repo driver `/tmp/W1_phase2/phi_trace_full.py`)

> SPECULATIVE EXPLORATORY MEASUREMENT — same caveat as Phase 1. Φ-on-cron-state is novel; no published IIT validation for this substrate class. Phase 2 widens axis coverage but does NOT resolve the foundational substrate-validation gap.

---

## 1. Why Phase 2

Phase 1 folded only the meta cycle log (19 axes from one ledger) into the joint state vector. Phase 1 §6 honest C3 #4 explicitly flagged this as a coverage gap: "the other 11 LaunchAgents are inventoried but NOT yet folded into the joint state — true agent-loop Φ should be measured on the union."

Phase 2 closes that subset by folding **6 additional sidecar ledgers** into each cron tick's joint state, alignment by forward-fill within ±15 h tolerance.

---

## 2. Inventory — 19 cycle-log axes + 6 sidecar ledgers (38 total axes)

| ledger | axes | source | records |
|---|---|---|---|
| cycle_log step axes | 10 (step:proposal_inventory_init…step:cycle_done, status∈{ok,skip,fail,missing}) | `state/proposals/meta/cycle_log.jsonl` | 158 records / 15 cycles |
| cycle_log count axes | 9 (cnt:pending_seen, cnt:refined, cnt:pending, cnt:approved, cnt:rejected, cnt:archived, cnt:debate, cnt:clusters, cnt:refinement) | same; `int(log10(v+1)·2)` bucket | parsed from counts + init msg |
| lint_cron | 3 (lint_total, lint_f1, lint_exit) | `state/lint_cron_history.jsonl` | 7 daily |
| h100_auto_kill | 3 (h100_npods, h100_apply, h100_unknown) | `state/h100_auto_kill_last_run.json` | 1 (singleton snapshot) |
| heartbeat | 3 (hb_frame, hb_render_ms, hb_mode_once) | `state/anima_tui_heartbeat.json` | 1 (singleton snapshot) |
| metrics rollup | 4 (m_pending, m_clusters, m_refinement, m_approved) | `state/proposals/meta/metrics.json` | 1 (singleton snapshot) |
| roadmap_coverage | 3 (rm_pct, rm_sat, rm_total) | `state/roadmap_coverage_tick_*.json` | 5 ticks |
| memory ledger | 3 (mem_nfiles, mem_total_kb, mem_last_kb) | `~/.claude-claude12/projects/-Users-ghost-core-anima/memory/*.md` | 19 files (mtime-events) |

**Joint axes per cron tick**: **38** (vs Phase 1's 19).
**Tick alignment**: forward-fill — for each cycle ts, take the most-recent sidecar event with `event.ts ≤ cycle.ts` (or earliest if all later). Tolerance ≤15 h consistent with mean inter-tick gap.

---

## 3. Φ proxy methodology

Identical to Phase 1 (paradigm-v11 G3 `phi_star` analog):

```
Φ_proxy(t) = MI(joint_prev, joint_curr) − (1/M) · Σ_i MI(prev[i], curr[i])
```

with M = 38, joint state hashed to 64 buckets (sha256 mod 64), sliding window W = 20.

---

## 4. Results

Output ledger: `state/W1_phase2_full_19axis_2026_05_01/phi_trace_full.jsonl` (15 ticks).

| metric | Phase 2 (38 axes) | Phase 1 (19 axes) | Δ |
|---|---|---|---|
| Φ_proxy mean | **1.717 bits** | 1.706 bits | **+0.011** |
| Φ_proxy std | 0.757 | 0.593 | +0.164 |
| Φ_proxy min | 0.000 (cold-start) | 0.000 | 0 |
| Φ_proxy max | **2.471** | 2.412 | +0.059 |
| linear slope per tick | **+0.1153** | +0.0507 | **+0.0646** |
| trend | rising | rising | (preserved) |
| ticks | 15 | 14 | +1 |

### Comparison interpretation

- **Mean essentially unchanged** (+0.011 bits, ~0.6% relative). The 6 sidecar ledgers were forward-filled from very few records (4 of 6 are singletons), so they add hash-state diversity but contribute ~0 additional sub-MI — effectively a constant offset to both joint MI and the bag-of-parts subtractor, leaving Φ approximately invariant.
- **Slope 2.27× steeper** (+0.1153 vs +0.0507). The rising trend is amplified because the May-1/2 burst now perturbs more axes (sidecar forward-fill values flip when fresh ledgers arrive), increasing late-window joint MI faster than sub_mi_mean.
- **Max shifted up** (2.471 vs 2.412), consistent with the 6-bit H_joint ceiling (log2(64) buckets) being approached more often under 38-axis joint hashing.

---

## 5. Honest C3 (top 3 + 2 bonus)

1. **Non-stationarity AMPLIFIED with more axes.** Tick spacing already varies 1 s ↔ 12 h within cycle_log; Phase 2 now mixes 6 sidecars sampled on totally different cadences (lint = daily, heartbeat = once-snapshot, h100 = per-pod-tick). The MI estimator's stationarity assumption is maximally violated. The 2.27× slope steepening should be read as *plausibly* a sampling artifact of forward-fill-induced stepwise variance rather than a substrate maturation signal.
2. **Forward-fill is a confound, not a fix.** 4 of 6 sidecars (h100, heartbeat, metrics, memory-final-snapshot) are singletons in this observation window. Forward-fill makes them constants for most ticks, suppressing per-axis variance and biasing sub_mi_mean downward (which inflates Φ). The +0.011 mean delta is roughly noise-floor; we cannot distinguish "true integration gain" from "forward-fill bias."
3. **Joint-hash collisions saturate at 6 bits.** With 38 axes hashed mod 64 buckets, effective H_joint ceiling = log2(64) = 6 bits regardless of true joint entropy. Phase 2's max Φ = 2.47 bits is already 41% of that ceiling — the measurement device is partially saturated. To extend honestly we would need to widen to mod 1024 (10 bits) or use a non-hash state encoding.

(bonus 4) **Memory ledger axes are mtime-derived, not semantic.** `mem_nfiles` is monotonic across the window so contributes ~0 MI by construction; only `mem_last_kb` carries any signal, and that signal is dominated by which file was last edited (a process artifact, not substrate dynamics).

(bonus 5) **MIP surrogate slack widens combinatorially.** Mean-of-parts is an upper bound on true Tononi-Φ; with 38 axes the gap to the true minimum-information-partition is provably wider than at 19 axes (combinatorially many more bipartitions). Direction of bias unknown without an exact MIP solve.

---

## 6. One-line interpretation

**Joint Φ_proxy mean 1.717 bits vs Phase-1 1.706 — essentially unchanged in mean (+0.011) but slope 2.27× steeper (+0.1153 vs +0.0507) — a result that is more likely a forward-fill / non-stationarity artifact than evidence of stronger integration; Phase 1's headline number is robust to the axis-coverage extension within this window.**

---

## 7. Output artifacts

- `state/W1_phase2_full_19axis_2026_05_01/phi_trace_full.jsonl` — per-tick Φ ledger (15 ticks, 38 axes each).
- `state/W1_phase2_full_19axis_2026_05_01/summary.json` — machine-readable summary with phase1_comparison block.
- `docs/W1_phase2_full_19axis_2026_05_01.md` — this report.
- `/tmp/W1_phase2/phi_trace_full.py` — off-repo analysis driver (HEXA-first repo policy).

### Next steps (zero budget)

- Widen joint-hash bucket from mod 64 → mod 1024 (10 bits) to defeat ceiling saturation.
- Add shuffle-null: permute cycle order, recompute Φ — true integration should exceed shuffle-Φ (Phase 1 §6 next-step #2 still pending).
- Accumulate ≥100 cycles before re-running so per-tick slope estimates are not dominated by 15-point endpoint sensitivity.
