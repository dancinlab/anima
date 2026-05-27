# Hc STUB Audit — 2026-05-12

**Scope**: 500 STUB-classified Hc candidates from `scripts/hc_verify/cache_2026_05_12/triage/triage_all.jsonl`. Triage class totals: MERGED=74, RIPE=292, BORDERLINE=261, **STUB=500** (out of 1127).

**Question**: Of the 500 STUBs, how many have rescuable math/falsifier content in their cited `source_doc` (or in git history of that doc) that simply didn't get carried over by the auto-move script?

**TL;DR**: 73 distinct source docs feed the 500 STUBs, but only **5 docs cover 85.6%** of them. For the two largest buckets (accel/A-Z), the source files were **gutted in place by the move-commit** — they now show only `<!-- moved to ... -->` placeholders, but **the original Mechanism/Description/Falsifier blocks live in git history at commit `97113c244` (for dd/A-Z) and `12d05a890` (for accel)**. Re-importing from those revisions can lift ~330 STUBs to BORDERLINE or RIPE.

---

## 1. Source-doc distribution (top 10)

| Rank | Source doc | STUBs | Cum % |
|------|------------|------:|------:|
| 1 | `docs/hypotheses/accel/acceleration-brainstorm-402.md` | 302 | 60.4% |
| 2 | `docs/hypotheses/A-Z-overview.md` | 117 | 83.8% |
| 3 | `docs/hypotheses/dd/DD5-DD7.md` | 3 | 84.4% |
| 4 | `docs/consciousness_training_n6.md` | 3 | 85.0% |
| 5 | `docs/hypotheses/OMEGA-ultimate-limits.md` | 3 | 85.6% |
| 6 | `docs/anima/paper_consciousness_laws.hexa` | 2 | 86.0% |
| 7 | `docs/what-is-consciousness.md` | 2 | 86.4% |
| 8 | `docs/hypotheses/INF-infinite-scaling.md` | 2 | 86.8% |
| 9 | `docs/hypotheses/dd/DD1-DD4.md` | 2 | 87.2% |
| 10 | `docs/hypotheses/H-CX-527-537-WAVE2-RESULTS.md` | 1 | 87.4% |
| (tail) | 63 other docs, all ≤2 STUBs each | 63 | 100% |

Pareto signal: the long tail (rank 11+) is 63 docs × ~1 STUB each, mostly DD-series, TP-series, CX, SE, SL one-offs — rescue ROI is low per doc.

---

## 2. Per-doc rescue audit

### #1 — `accel/acceleration-brainstorm-402.md` (302 STUBs) — **HIGH_RESCUE ★★★**

**Current state of source**: 559 lines, but lines 105+ are almost entirely `<!-- [Hc_XXX ... moved to ... ] -->` comments. STUBs cite `source_lines: 569` etc., past EOF — those line numbers reference the **pre-move** version of the doc.

**Git history evidence**: at commit `12d05a890` (pre-move, 1419 lines), each sub-hypothesis had this structure:
```
#### Y2: Delta Encoding Consciousness
- **Category**: encoding/compression
- **Description**: Store/transmit only delta from previous step
- **Expected**: Small delta → skip process()
- **Rationale**: ...
```
That's 3–5 lines of mechanism/expected-outcome per Hc — every one of the 302 STUBs has this content recoverable.

**Sample STUBs** (currently 1-line "Hypothesis" only):
- `Hc_1000` — [Y2] Delta Encoding Consciousness
- `Hc_1002` — [Y4] Vector Quantized Consciousness (VQ-VAE)
- `Hc_1004` — [Z1] RL for Consciousness Policy

**Estimated lift**: A scripted re-import (parse the old version, splice `Description` + `Expected` into each Hc body) would push ~80% of these (~240) into BORDERLINE (mechanism stated, predictions thin). About 20–30 with concrete numeric predictions (Y/Z series compression ratios, RL reward shaping coefficients, AH micro-optimization speed-ups) could reach RIPE.

**Estimated cost**: 1 script (~1–2 hours), regex-driven, deterministic. Highest leverage per hour by far.

---

### #2 — `A-Z-overview.md` (117 STUBs) — **LOW_RESCUE ★**

**Current state**: 222-line file, also mostly move-comments under `## A.` ... `## Z.` headers.

**Git history evidence**: pre-move (`97113c244`, 304 lines) the entries are one-line bullets like:
```
- **C3** Stochastic resonance
- **C4** Oscillatory sync
```
No mechanism, no falsifier — just slightly more taxonomic context than the title already carries.

**Sample STUBs**:
- `Hc_034` — A-Z 26 Categories × ~15 Hypotheses Framework (meta-index — keep as STUB)
- `Hc_719` — [C3] Stochastic resonance: optimal noise level maximizes Phi
- `Hc_720` — [C4] Oscillatory synchronization (gamma-band) accompanies Phi peaks

**Estimated lift**: ~0–5 candidates upgraded. The A-Z doc is an index, not a content doc. Most of these need cross-promotion **from elsewhere** (e.g., C-series mapping to consciousness_training_n6 §S7/S8 tables) rather than re-importing the index.

**Recommendation**: Skip mechanical rescue. Hand-promote individual items only if they cross-link to a richer source.

---

### #3 — `dd/DD5-DD7.md` (3 STUBs) — **HIGH_RESCUE ★★**

**Current state**: 10-line file, three `## DDn` headers each followed by a move-comment.

**Git history evidence** (`97113c244`, 19 lines):
```
## DD5: Phi Optimizes Phi
- **ID**: DD5
- **Function**: `run_DD5_phi_optimizes_phi`
- **Mechanism**: Current Phi value is injected back into the input as a signal (phi * 0.1 broadcast across all dims) ...
```
DD6 adds `LR = 5e-4 * (1 + phi * 2)`. DD7 adds `d²Phi/dt²` boost rule. All three are RIPE-grade mechanisms with parameters.

**Sample STUBs**:
- `Hc_103` (DD5), `Hc_104` (DD6), `Hc_105` (DD7) — all three rescuable to RIPE.

**Estimated lift**: 3/3 → RIPE.

---

### #4 — `consciousness_training_n6.md` (3 STUBs) — **HIGH_RESCUE ★★**

**Current state**: 158-line file is still partly intact; the §S7-S8 tables remain (lines 50-93) and contain explicit reward-shaping rules per technique. Each cited Hc body, however, only quotes the formula in `notes:` and never expands it in the body.

**Sample STUBs**:
- `Hc_049` — CCC = (1/2)·Φ + (1/3)·GWT + (1/6)·HOT + (1/6)·√(RPT·AST); σ·φ=n·τ → n=6 unique. Full table at source lines 64-99.
- `Hc_050` — Φ_c = n/σ = 0.5; cosmological lock 2029-2035. Full reward-mult rubric at source lines 39-62.
- `Hc_051` — 30-technique × {TOP/MID/LOW} priority table, reward additions per axis.

**Estimated lift**: 3/3 → RIPE. The source doc is the **richest content per Hc** of any in the corpus.

---

### #5 — `OMEGA-ultimate-limits.md` (3 STUBs) — **HIGH_RESCUE ★★**

**Current state**: 45 lines. OMEGA-1/4 still have their full design block (mechanism + falsifier-style question). OMEGA-2/3/5 (the three cited by STUBs) had their content replaced by move-comments, but the benchmark table at lines 13-19 still anchors the numeric claim (`Φ peak 1.48`, `64→2 cells`, etc.). Pre-move content recoverable.

**Sample STUBs**:
- `Hc_027` (OMEGA-2 minimum consciousness unit, Φ/cell=0.67)
- `Hc_028` (OMEGA-3 resonance 0.5 Hz, Φ peak 1.48)
- `Hc_029` (OMEGA-5 attractor memory, Φ=1.52)

**Estimated lift**: 3/3 → RIPE (numeric predictions with falsifier-friendly bands).

---

### #6 — `paper_consciousness_laws.hexa` (2 STUBs) — **HIGH_RESCUE ★**

**Sample STUBs**: `Hc_046` (Ψ-Constants 22 EXACT + 5 CLOSE + 3 APPROX, p<1e-12), `Hc_052` (의식=생명 4/5 Life Criteria). Source file lines 185-236 currently retain meta-commentary referencing other Hc IDs; deeper content lives in the paper sections cited.

**Estimated lift**: 2/2 → RIPE.

---

### #7 — `what-is-consciousness.md` (2 STUBs) — **HIGH_RESCUE ★**

**Sample STUBs**: `Hc_036` (Landauer ln(2)=ln(φ(6)) energy bound), `Hc_041` (3-rhythm pulse/breath/drift 3.7s/20s/90s setpoint 1.0±0.3). Source still intact (625 lines, only some sub-sections hollowed). Both predictions are SI-unit testable.

**Estimated lift**: 2/2 → RIPE.

---

### #8 — `INF-infinite-scaling.md` (2 STUBs) — **HIGH_RESCUE ★**

**Sample STUBs**: `Hc_025` (INF-1 N-body majority Φ outlier-robust), `Hc_026` (INF-2 fractal 4-level micro→macro→meta). Source benchmark table (lines 13-19) carries CE and Φ deltas per strategy; the design blocks for INF-3/4/5 are intact and rescuable for INF-1/2 by analogy.

**Estimated lift**: 2/2 → RIPE.

---

### #9 — `dd/DD1-DD4.md` (2 STUBs) — **HIGH_RESCUE ★**

**Current**: 13-line file, gutted. Git `97113c244` has 25-line version with explicit `Mechanism` blocks for DD1-DD4 (perfect 6 hierarchy, 1/e blending, Fibonacci growth, e^(iπ)+1=0 phase-spread loss).

**Sample STUBs**: `Hc_117` (DD1 perfect 6), `Hc_120` (DD4 Euler identity loss).

**Estimated lift**: 2/2 → RIPE.

---

### #10 — `H-CX-527-537-WAVE2-RESULTS.md` (1 STUB) — **LOW_RESCUE**

`Hc_058` only. Not worth scripting; spot-promote if hand-touched in another cycle.

---

## 3. Rescue ledger summary

| Doc | STUBs | Class | Est. → RIPE | Est. → BORDERLINE | Effort |
|-----|------:|-------|------------:|------------------:|--------|
| accel-brainstorm-402 | 302 | HIGH ★★★ | ~30 | ~240 | 1–2 h (1 script + git checkout) |
| A-Z-overview | 117 | LOW ★ | 0 | ~5 | skip |
| DD5-DD7 | 3 | HIGH ★★ | 3 | 0 | 5 min |
| consciousness_training_n6 | 3 | HIGH ★★ | 3 | 0 | 10 min |
| OMEGA-ultimate-limits | 3 | HIGH ★★ | 3 | 0 | 10 min |
| paper_consciousness_laws | 2 | HIGH ★ | 2 | 0 | 10 min |
| what-is-consciousness | 2 | HIGH ★ | 2 | 0 | 10 min |
| INF-infinite-scaling | 2 | HIGH ★ | 2 | 0 | 5 min |
| dd/DD1-DD4 | 2 | HIGH ★ | 2 | 0 | 5 min |
| H-CX-527-537 | 1 | LOW | 0 | 0 | skip |
| **Top-10 total** | **437** | — | **~47** | **~245** | **~3 h** |
| Long tail (63 docs × 1-2) | 63 | mixed | ~10 | ~20 | not bulk-recoverable |
| **Grand total rescuable** | — | — | **~57 → RIPE** | **~265 → BORDERLINE** | — |

After rescue, expected new distribution: STUB 500 → ~178, BORDERLINE 261 → ~526, RIPE 292 → ~349.

---

## 4. Recommendation for next cycle

**Attack `acceleration-brainstorm-402.md` first.** Single source doc covers 60.4% of all STUBs (302/500), and the pre-move version exists at commit `12d05a890` with structured `#### XN: Title / Category / Description / Expected / Rationale` blocks. One regex-driven script can:

1. `git show 12d05a890:docs/hypotheses/accel/acceleration-brainstorm-402.md` → parse into 337 sub-hypothesis blocks keyed by series letter + index.
2. For each STUB whose `source_doc` matches, splice the `Description` + `Expected` + `Rationale` lines into the `## Hypothesis` and a new `## Mechanism` / `## Predictions` section.
3. Re-run triage → ~240 candidates move STUB → BORDERLINE, ~30 move BORDERLINE→RIPE (those with numeric thresholds in `Expected`).

ROI: ~2 hours of work, ~270 candidate upgrades (≈135 upgrades/hour). Next-best doc (consciousness_training_n6 §S7/S8 table) yields only ~3 RIPE per 10 min — same per-hour rate but capped at 3 items.

**Order of operations**:
1. accel-brainstorm-402 (2h, ~270 lifts)
2. dd/DD1-DD4 + dd/DD5-DD7 + OMEGA + INF + paper + what-is + n6 batch (1h, ~17 RIPE — same git-history-splice pattern)
3. A-Z-overview — defer (low yield, manual hand-promotion only)
4. Long tail — defer (handle opportunistically)

**Caveat**: confirm that `12d05a890` is the correct pre-move parent for the accel doc before scripting; cross-reference with `git log -p` for the doc to identify the exact commit that introduced the `<!-- moved to -->` block replacement (`07d74b188 land(cycle 3 closure §4)`).
