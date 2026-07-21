# HYPOTHESES — hypothesis-verification system

> **SSOT**: repo-root `ARCHITECTURE.json` (design tree). Cards record pre-register → falsify → run →
> verdict; findings are distilled into the tree, never accumulated here.

Pre-register → falsify → run → verdict, for anima-v5's question: **does a write-side tension
self-organize its field once the register stops leaking?** A flat registry + one rich card per
hypothesis; runnable machinery in repo-root `tool/`.

## Layout

- `REGISTRY.jsonl` — flat registry, one JSON line per hypothesis
  (`{id, slug, tier, title, card, verdict, source, archived, artifacts}`).
- `cards/H5_*.md` — one card per hypothesis. `cards/_TEMPLATE.md` — the skeleton; copy to start.

## The FIVE standing gates — a card CANNOT freeze without all five

Each was paid for by a measured anima-v4 failure (full argument: `state/v5_founding_design_2026-07-17/`,
inherited verdicts: `state/inherited_v4_verdicts_2026-07-17/`). These are REQUIREMENTS, not conventions.

1. **G1 admissibility, both halves** — (a) reachability: the bar clears the metric's field-blind ceiling
   with ≥2× headroom (H_001); (b) trained-control-ceiling: a trained-vs-trained falsifier is VOID unless
   the trained control is measured sub-ceiling AT TARGET SCALE first (controls-first, control f2 ≤
   1 − 2×bar). H_007's F1 died here: C-dup hit 1.0000/0.9323 ⇒ zero headroom ⇒ the run carried no bits.
   **No inherited E-anchors** — not from another experiment, another scale, a smoke, or our own summaries
   (H_007 froze E[C-dup] = 0.62; truth was 1.00. A d=64 smoke inverted at d=384: +0.073 → −0.010).
2. **G2 audit the DEFECT, not a proxy** — every closed-form audit encodes the failure it guards, and
   **learnability belongs to G-0**: control in-sample fit ≥ 0.95, co-certified with heuristic-chance,
   never separately. H_008's A7 ("best syllable→class = 0.500") was arithmetically impossible with
   distinct lexemes, so the builder paired syllables ⇒ class became a PARITY conjunction ⇒ the control sat
   at in-sample CHANCE while 16/16 audits were green.
3. **G3 free-slot metric, recomputed per panel** from the codebook (GF(2)-rank + length-parity audit).
   H_004's K=6 codebook was GF(2) rank-4 ⇒ teacher-forcing completed the parity slots ⇒ a field-blind
   ceiling of 0.667 that reached held-out and inflated EVERY arm equally.
4. **G4 d_acc discipline** — bounded 1.0, chance floor 0.5; `f1`/`f2` are PANEL names (never F-measures);
   every number cited with the ARM that produced it and that arm's source path.
5. **G5 window/knee pre-check** — before betting a card on a band or a dial, measure that the curve has a
   KNEE: ≥2 CONSECUTIVE in-window settings, across seeds. H_008 K1: k*=96 sat cleanly in band both seeds
   (0.651/0.6875) but k=48 was 0.5365/0.5417 and k=192 saturated 0.9167 — a CLIFF, and one in-band point
   cannot anchor a falsifier.

## Method

1. **Pre-register frozen** — hypothesis, predictions, variables, and **≥5 measurable falsifiers**
   (incl. the two inherited v1-killers: L1 eff-rank, L2 ablate-the-channel) BEFORE running. Freeze with
   `frozen_at` — and only after all five gates are satisfied.
2. **Falsifiers, not confirmations** — each refutes a component; ≥1 negative control, ≥1 bounds check.
3. **Run deterministically** — run script in `state/<hX>_<slug>_<date>/`, writes `result.json`, prints a
   verdict. The collector is frozen AND unit-tested before the run, not after.
4. **Verdict = verbatim stdout** — paste the actual output. No LLM self-judgement (commons verify-done).
   SUPPORTED only when all falsifiers PASS; report FALSIFIED/PARTIAL/INADMISSIBLE honestly.
5. **Honest limits ≥3** — where numbers are representative, what the model ignores, what would move it.
6. **Every exit a measurement** — a fold must be a measured fold; no re-tuning a dial after seeing data.

## Conventions

- Shared machinery → `tool/`. Per-hypothesis run + result → `state/`.
- Tier badges: `🟢 SUPPORTED` · `🟡 PARTIAL` · `🔴 FALSIFIED` · `⚪ PRE-REGISTERED` · `⚫ CLOSED/RETIRED`
  (inadmissible or measured-shut — NOT the same as falsified) · `🜂 ABSTRACT` (conjecture, no run).
- Update the registry line in lockstep when a card's verdict changes.
