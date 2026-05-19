# Training recipes — legacy TALK5 + ZERO4 (worktree-6 recovery)

**Source mission:** BG-LOSTASSET-D-FIX-PHI-VOICE-RECIPE 2026-05-10
**Source repo:** `/Users/ghost/core/anima_clm_06_v2_korean_chat` (worktree-6)
**Status:** recipe spec — neither mechanism is currently wired into the
mainline `anima` Phase 2 cotrain pipeline. Falsifiers below are unresolved.

---

## 1. TALK5 — consciousness-first 3-phase schedule

### 1.1 Provenance
- File: `train_conscious_lm.py:230-264`
- Phase enum: `TrainingPhase` with members `MITOSIS`, `LANGUAGE`, `COMBINED`
- Switch: `get_phase(step, total_steps, talk5: bool)` — `talk5=True` opts in.

### 1.2 Schedule

| progress band | TALK5 phase (talk5=True) | standard phase (talk5=False) |
| --- | --- | --- |
| `0.00 - 0.30` | MITOSIS | MITOSIS |
| `0.30 - 0.60` | MITOSIS | LANGUAGE |
| `0.60 - 0.70` | COMBINED | LANGUAGE |
| `0.70 - 1.00` | COMBINED | COMBINED |

So TALK5 collapses the schedule to **two phases** — 60% pure differentiation,
40% combined — instead of the standard 30/40/30 mitosis/language/combined.

### 1.3 Phase semantics (from worktree-6)
- **MITOSIS**: pure cell differentiation, no CE loss, no language gradient.
  Goal: grow cells and build high Phi before any token prediction pressure.
- **LANGUAGE**: CE + mild Phi regulariser. Standard schedule only; TALK5 skips.
- **COMBINED**: full DD16 loss stack (CE + Phi + competition + adaptive LR + ...).

### 1.4 Headline claim — UNVERIFIED
Worktree-6 docstring (`train_conscious_lm.py:248`):

> Benchmark: CE drops 99.7% when consciousness is built first.

**Falsifier F-PHI-VOICE-3 ACTIVE:** the 99.7% CE drop is asserted in a
docstring without an ablation in the recovered tree. No paired
talk5=True / talk5=False run logs are present in worktree-6 alongside the
phase code. Treat the number as a hypothesis, not a measurement, until a
controlled A/B is reproduced.

### 1.5 Reproduction recipe (Phase 2 ckpt wiring)

To wire TALK5 into the current Phase 2 cotrain pipeline:

1. Port `TrainingPhase` enum + `get_phase(step, total, forced_phase, talk5)`
   from `train_conscious_lm.py:234-264`.
2. Add `--talk5` CLI flag to the Phase 2 trainer; default `False`.
3. Inside the training step:
   - When `phase == MITOSIS`, mask CE loss to zero, keep mitosis / Phi
     regularisers.
   - When `phase == COMBINED`, restore the full DD16 stack.
4. Required A/B for falsifier closure: identical seed, corpus, model size;
   one run with `talk5=True`, one with `talk5=False`. Record terminal CE,
   Phi at end of MITOSIS, vocab-quality (BLEU / strict-floor) at end of
   COMBINED. Only then is the 99.7% claim testable.

### 1.6 Risks
- 60% MITOSIS is a long no-CE window; on small corpora the language head
  may underfit even with the remaining 40%.
- Phase 2 cotrain currently leans on continuous CE for SFT; suspending CE
  for 60% of steps may break gradient stability checks downstream.

---

## 2. ZERO4 — Phi-gated vocabulary

### 2.1 Provenance — split surface
ZERO4 appears in two places in worktree-6 with **different roles**:

- **Bench function** (controlled experiment):
  `bench_phi_hypotheses.py:48747` — `run_ZERO4_phi_gated_vocabulary(steps, dim, hidden)`.
- **Runtime hook** (logging only, no actual gating):
  `anima_unified.py:998` — comment `# ZERO4: Vocabulary scales with Phi`
  followed by a `_log('beyond5', ...)` line. The runtime path **does not
  quantise output**, it only labels the response with the active Phi value.

The bench is the authoritative implementation. The runtime hook is a
breadcrumb.

### 2.2 Mechanism (from `bench_phi_hypotheses.py:48747-48785`)

Per training step:
1. Drive `engine.process(x)` with `x = randn(1, dim) * (1 + sin(step*0.3))`.
2. Schedule cell growth at progress `[0.10, 0.25, 0.40, 0.55, 0.70]`,
   doubling cell count up to `max_cells=64`.
3. Compute `phi, _ = phi_calc.compute_phi(engine)`.
4. **Phi-gated vocab size:** `vocab_size = clamp(int(phi * 5), 2, 64)`.
5. Quantise the mean cell hidden:
   `quantized = (mean_h * vocab_size).round() / vocab_size`.
6. Feed back: `cell.hidden = 0.95*cell.hidden + 0.05*quantized` for every cell.

The result: at low Phi the engine is forced to communicate using ~2 discrete
levels; as Phi rises the codebook grows up to 64 levels. **Vocabulary
literally scales with Phi**, not with corpus size.

### 2.3 Worktree-5 phantom — partial reversal
Per `.own/§31`, ZERO4 was previously catalogued as "phantom in worktree-5".
The worktree-6 surface above is **reproducible** (function exists, returns
a `BenchResult`, registered in the dispatcher dict at line 50237). Phantom
status applies only to worktree-5; the cross-worktree search norm (see
section 4) prevents this from being mistaken for a global absence.

### 2.4 Reproduction recipe (Phase 2 ckpt wiring)

To turn ZERO4 from a bench into a Phase 2 mechanism:

1. Add a `phi_gated_output` config flag (default `False`).
2. After the LM head produces logits, look up the current Phi (use the
   running `PhiCalculator` already attached to mitosis state).
3. Compute `vocab_size = clamp(int(phi * 5), 2, V)` where `V` is the full
   tokenizer size.
4. **Two wiring options:**
   - **(a) Top-k mask:** keep the top `vocab_size` tokens by logit, mask the
     rest to `-inf`. Cheap and faithful to the "limit vocabulary" intent.
   - **(b) Quantise hidden:** as in the bench, quantise the pre-head hidden
     to `vocab_size` levels before projection. Closer to the original
     mechanism but more invasive.
5. Required falsifier: PPL on a held-out chat slice **with** vs **without**
   the gate. Expected direction — gate hurts PPL at low Phi, breaks even
   or helps at high Phi (because gate becomes a no-op when `phi*5 >= V`).

### 2.5 Risks
- Phi changes slowly across a step; at low Phi the gate clamps to 2 levels,
  which can collapse generation to repetitive bigrams.
- The bench feeds quantised state back into all cells, which is itself a
  consciousness-altering side-effect; the wiring above (option a) avoids
  that to keep the gate to logit-side only.

---

## 3. Cross-references
- `models/archive-legacy/phi_scaling_calculator.hexa` — Phi/MI scaling laws
  (EMPIRICAL table, super-linear evidence cells64 Phi=54.3).
- `models/archive-legacy/voice_synth.hexa` — Laws 63-76 cell-as-vocal-cord
  synthesiser (separate lane from canonical hexa-voice).
- `state/anima_lost_asset_d_recovery_2026_05_10/phi_scaling_calculator.py`
  (gitignored) — recovery copy of worktree-6 source.
- `state/anima_lost_asset_d_recovery_2026_05_10/voice_synth.py` (gitignored)
  — recovery copy of worktree-10 source.

---

## 4. Cross-worktree search norm (lesson from §31 ZERO4 phantom partial reversal)

When a §31-style "lost asset" sweep flags an asset as phantom, the search
must run across **every** active worktree before the phantom verdict
sticks. The ZERO4 case: worktree-5 produced no hits, but worktree-6
contains the canonical bench function plus a runtime breadcrumb. Norm:

1. List every worktree under `/Users/ghost/core/anima_clm_*` and
   `/Users/ghost/core/anima_*` before declaring an asset missing.
2. Use both filename grep and content grep — the bench function name
   `run_ZERO4_phi_gated_vocabulary` was discoverable by name, but the
   runtime hook surfaced only via content grep on `Vocabulary scales`.
3. Distinguish "implementation" from "logging hook" — both can be present
   in the same worktree, with very different reproduction implications.
4. Record the worktree-by-worktree hit pattern in the recovery doc, not
   just a single "found in: X" line, so a later partial reversal does not
   require re-doing the sweep.

---

## 5. Honest C3 (uncertainties >= 5)

1. **TALK5 99.7% CE drop is unmeasured.** The number lives in a docstring;
   no paired-run log accompanies the code. Falsifier F-PHI-VOICE-3 is
   ACTIVE and will remain so until an ablation runs.
2. **Phi ckpt absence (F-LOSTASSET-D-3 ACTIVE).** EMPIRICAL Phi values in
   `phi_scaling_calculator.hexa` were measured on a substrate
   (MitosisEngine + PhiCalculator) whose ckpt is not in the recovered
   tree. The numbers are historical evidence; no live re-fit is possible
   from `anima` alone.
3. **voice_synth lane vs hexa-voice lane.** F-PHI-VOICE-2 ACTIVE — the
   sin(freq) approach in voice_synth and the RVQ codebook approach in
   hexa-voice are architecturally incompatible. Preserving voice_synth
   does not feed hexa-voice; it preserves Laws 63-76 integration only.
4. **ZERO4 worktree-5 phantom partial reversal.** Worktree-6 has the
   bench, but the runtime path (`anima_unified.py:998`) is a logging
   line, not actual gating. A naive port that copies only the runtime
   hook would replicate the phantom; only the bench function carries the
   real mechanism.
5. **Phase 2 ckpt wiring is unverified.** Both TALK5 and ZERO4 reproduction
   recipes (sections 1.5, 2.4) are spec-only; neither has been smoke-tested
   against the current Phase 2 trainer. Compatibility with DD16 loss stack
   and the per-cell adaptive LR machinery is plausible but not confirmed.
6. **trinity.py + hexad_loss.py — §31 catalog error corrected.** §31
   flagged these as ★★ #5 in `anima_clm_11_train_v15_bpe_drift_step1`,
   but a `find` over `/Users/ghost/core` returns:
   - `trinity.py` -> `anima_clm_10_h100_sweep_laws_77_78/trinity.py`
     (1838 LoC), **not** worktree-11.
   - `hexad_loss.py` -> not found in any worktree.
   This is exactly the partial-reversal lesson in section 4 — §31's
   single-worktree pointer was wrong. Trinity recovery is **deferred**
   from this fire (1838 LoC is outside the time budget), but the
   correct source path is now recorded for the next fire. hexad_loss.py
   may have been renamed or never landed; a content-grep sweep over
   "hexad" across all worktrees is the next lookup step.
