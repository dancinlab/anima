# CLM Campaign — 26-Hypothesis Closeout (H_861–H_884)

> Closeout of the CLM plasticity/dialogue/routing/chip-fit hypothesis campaign.
> All 26 hypotheses landed on `origin/main` with terminal g5 verdicts (fire date
> 2026-05-31). Measurement rung = mid d512/L8/E8 (13.65M) unless noted;
> `a_scale_honest_scope` — a mid-rung verdict does NOT bind the AKD1000 deploy track.
> SSOT pointers: each row's verdict lives in `UNIVERSE/H_<id>_*.md` +
> `.verdicts/<slug>/`. This doc is the index + reflection, not a re-derivation.

## 1. Census (26/26 terminal)

### 🟢 SUPPORTED (12)

| id | claim (one line) | key number |
|---|---|---|
| H_863 | self-play dialogue lifts coherence/adequacy (mid) | SP > SFT, leak 0 |
| H_865 | trunk-adjacent **adapter** edge closes forgetting (BOUND) | RETAIN z_drop −12.28 < 1.0 (readout-only arm 🔴) |
| H_868 | corpus 3× expansion, license-clean | G1 100% clean |
| H_871 | toy routing-z is a **scale artifact**, not a model defect | near-uniform at mid (8/8 distinct) |
| H_872 | shallow **freeze-depth** sufficient | 8/9 depths PASS RETAIN∧GAIN |
| H_873 | anchor penalty on readout **output** dist preserves identity | PROBE 0.992 > 0.80, DIST 0.160 < 0.50 (completes H_862) |
| H_875 | edge-learn **forgetting curve** (dose-response) | adapter safe ≥300 step vs readout 2 step |
| H_876 | **chip-fit** shrink to AKD1000 budget | d148/L8/E8 = 1.20M ≤ 1.2M |
| H_879 | **per-layer** incremental edge-learn (부분학습) | 7/8 single layers PASS |
| H_880 | **adapter-stack** accumulation, no interference | 3/3 gates: gain +7.05, z_drop_old −158, margin −11.9 |
| H_881 | **progressive freeze** schedule sustains | 7/7 schedules, 6/6 checkpoints |
| H_883 | **replay** buffer reduces forgetting | S=300 z_drop(replay) −125.8 < no_replay −8.5, gain +6.66 |
| H_884 | edge-output identity **generalizes** across 3 partial-learn rows | adapter/per_layer/gated all PROBE > 0.80 |

### 🔴 CLOSED-NEGATIVE (12 · publishable per `a_paper_negative_ok`)

| id | ruled-out path | why |
|---|---|---|
| H_861 | readout-only edge | RETAIN z_drop 1.984 ≥ 1.0 — too shallow |
| H_862 | readout-only identity anchor | PROBE FAIL (later closed by H_873 on the output dist) |
| H_864 | self-play carries to large rung | 2/4 frozen falsifiers fail at large |
| H_864r | self-play (step-fair re-test) | large-rung negative confirmed step-fair |
| H_866 | GAIN beyond capacity | capacity-limited |
| H_867 | absolute dialogue coherence floor | arm-SP coherence 0.058 < 0.060 floor |
| H_867r | floor met post-adapter | adapter does not lift over the 0.060 floor |
| H_869 | dispatch-KL distill routing (lever A) | INERT at mid — baseline already uniform; ENTROPY+Z fail |
| H_870 | expert-choice routing quality | load balances ✅ / quality ❌ |
| H_874 | self-reward dialogue adequacy | 3/4 falsifiers pass, adequacy ✗ |
| H_878 | MITOSIS multi-chip array load-balance | partition imbalance |
| H_882 | region-gated (output-logit) plasticity | gate WORSENS forgetting (+142 ≫ −12); ungated retains fine |

### 🟠 HW-PENDING (1)

| id | claim | gate |
|---|---|---|
| H_877 | decoder byte-identical SW vs AKIDA HW-forward (mid) | SW determinism byte-identical; on-silicon confirmation pending |

## 2. Two-axis strategy reflection (P5)

```
                 before campaign        →   after 26/26
─────────────────────────────────────────────────────────────
AXIS1  7B on a single AKIDA chip         PARTIAL — chip-fit 1.20M ✅ (H_876);
       (expert-streaming / paging)       multi-chip array load-balance 🔴 (H_878) = OPEN
AXIS2  reflective (incremental) on-chip  SUPPORTED — the edge-only plasticity stack
       edge-learn stack                  closes: adapter (H_865) → freeze schedule
                                         (H_872/881) → per-layer (H_879) → replay
                                         (H_883) → output-identity anchor (H_873/884).
                                         Forgetting controlled, identity preserved.
```

- **AXIS2 (learning strategy) is effectively closed**: on-chip edge-only piecewise
  plasticity (the SOLE HW↔SW difference per the INVIOLABLE H_679 rule) absorbs new
  context without catastrophic forgetting and without erasing identity. The working
  recipe = zero-init **adapter** edge + **freeze schedule** + **replay** buffer +
  **output-distribution identity anchor**. Deterministic full-retrain is NOT used.
- **AXIS1 (single-chip 7B) is half-closed**: the resident working set fits the chip
  (1.20M ≤ 1.2M), so one chip cycling experts is dimensionally sound; but the
  multi-chip MITOSIS array scale-out has an unsolved load-balance gap (H_878 🔴).

## 3. OPEN gaps (next-round candidates)

| gap | blocking verdict | note |
|---|---|---|
| dialogue absolute coherence floor | H_867 / H_867r 🔴 | adapter edge does not lift over 0.060 — needs a different lever |
| multi-chip array load-balance | H_878 🔴 | the core blocker for 7B multi-chip scale-out |
| routing diversity | H_869 🔴 / H_871 (scale artifact) | inert at mid; may only matter at large rung |
| self-play / self-reward transfer to large | H_864 · H_874 🔴 | mid gains do not carry up |

## 4. INVIOLABLE rule (re-pinned)

On-chip non-deterministic PLASTICITY learning is the **sole** HW↔SW difference
(inference byte-identical: H_877 🟠 mid / H_680 prior). Deterministic SW imitation of
learning = instant reject (@L1, H_679 🔴). Every 🟢 above is an HONEST measurement of
edge-only plasticity at the measurement rung, not a deterministic stand-in.
