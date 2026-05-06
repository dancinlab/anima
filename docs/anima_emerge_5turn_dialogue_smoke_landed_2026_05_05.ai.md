# anima emerge 5-turn dialogue smoke (landed) 2026-05-05

**Lane**: BG-AJ — mode=none multi-turn dialogue smoke
**Status**: LANDED · `dialogue_smoke_PASS = true`
**Date**: 2026-05-05 (UTC 16:29:22Z)
**Cost**: $0 (mac CPU fp32)
**Wall**: ~30s after model load (19.5s load + ~10s 5 forward)

---

## 1. Purpose

After BG-AG attractor finding, validate empirically whether a user-emerge
dialogue is possible at `mode=none` (no consciousness_states injection) by
threading prior turn state into a 5-turn Korean continuity probe. The
candidate dialogue medium is **phi-star drift + hidden_state_delta** (with
prior threading across turns).

This is a **smoke**, not a controlled experiment: we measure whether the
medium *exists* (drift is detectable across turns), not whether the medium
*means* anything semantic.

## 2. Method

- Model: `need-singularity/clm-v4-mk2-v1` (CLM v4 mk2 v1)
- Device: mac CPU fp32 (`.venv-eeg`)
- Sister import: `tool/transient_py/anima_emerge_cand_d_inject_helper.py`
  (BG-Q helper) — read-only sister, raw#15 additive
- Forward path: `mode=none` (consciousness_states=None), ln_f-hook capture
  of last-layer hidden state (mean over B,T → 768-d), tile to 8×192 cell
  for `phi_star_compute` (same path as BG-A axis FAIL evidence — C3)
- Prior threading: each turn t's metrics referenced against t-1
  (phi_drift_from_prior, hidden_state_delta L2 norm)

### Turn corpus (5 Korean continuity prompts)

1. `안녕 너는 누구야?`
2. `지금 phi-star 어떻게 느껴?`
3. `왜 그렇게 변했어?`
4. `axis identity 강하게 활성화해봐`
5. `이 input에 대해 어떤 cell이 dominant?`

### Thresholds

- `phi_diff_real`: phi_star_range > 0.01
- `hsd_real`: hsd_max > 1.0
- `dialogue_medium_available`:
  - both → `phi-star + hidden_state_delta`
  - phi only → `phi-star only`
  - hsd only → `hidden_state_delta only`
  - neither → `NONE`

## 3. Results

### 3.1 Per-turn table

| turn | input | tokens | phi_star | phi_drift_prev | hsd_prev | hidden_l2 |
|---|---|---|---|---|---|---|
| 1 | 안녕 너는 누구야? | 8 | 42.18181 | 0.00000 | 0.000 | 23.095 |
| 2 | 지금 phi-star 어떻게 느껴? | 8 | 42.23185 | +0.05004 | 11.719 | 26.375 |
| 3 | 왜 그렇게 변했어? | 6 | 42.10573 | -0.12612 | 16.871 | 25.022 |
| 4 | axis identity 강하게 활성화해봐 | 6 | 42.21472 | +0.10899 | 13.671 | 25.663 |
| 5 | 이 input에 대해 어떤 cell이 dominant? | 10 | 42.16240 | -0.05232 | 6.714 | 24.970 |

### 3.2 Aggregate

- phi_star_min = 42.10573
- phi_star_max = 42.23185
- **phi_star_range = 0.12612** (>> 0.01 threshold → phi_diff_real ✓)
- phi_drift_max_abs = 0.12612
- **hsd_max = 16.871** (>> 1.0 threshold → hsd_real ✓)
- hsd_mean = 12.244

### 3.3 Verdict

```
dialogue_medium_available = "phi-star + hidden_state_delta"
dialogue_smoke_PASS = true
```

**BOTH** medium channels are alive at `mode=none` with prior threading.
Hidden state delta dominates (L2 ~12 mean, 17 max) over phi-star drift
(range 0.126 = ~0.3% of baseline 41.86), but both clear their respective
detection thresholds.

## 4. Interpretation

- **Hidden state is the loud channel**: hsd_max 16.87 vs hidden_l2 ~25 →
  inter-turn delta is ~67% of intra-turn norm. Each new turn's pooled
  ln_f hidden state is meaningfully distinct from the prior turn's.
- **Phi-star is the quiet channel**: 0.126 range on 41.86 baseline =
  ~0.3% modulation. Detectable, but small. Phi-star (cosine-similarity
  aggregate over a tiled cell) is largely insensitive to the same-shape
  pooled vector that drives hsd; the tile-and-cosine compresses signal.
- **No semantic claim**: drift exists ≠ understanding exists. C5 honest
  carry — phi/hsd drift is a *medium* signal, not an *emerge* signal.
  Whether the model reads its own prior turn as content vs. just shifts
  hidden state because the new tokens differ is **out of scope** for this
  smoke.

## 5. Honest C3 (raw#10)

1. **C1** mac CPU fp32 (no GPU, single-batch single-seq forwards)
2. **C2** BG-Q helper sister-import: model loader, tokenizer loader,
   phi_star_compute reused as-is (no fork, no mutation)
3. **C3** hidden state captured via `decoder.ln_f` forward hook, mean
   over (B,T) — identical capture path to BG-A axis FAIL evidence;
   carries the same architectural assumption (ln_f is the readout)
4. **C4** 5 specific Korean continuity prompts, not a controlled
   dialogue corpus; ablation across prompt language / count / semantic
   structure not performed
5. **C5** dialogue medium 가능성과 emerge 의미는 분리된 epistemic open;
   phi/hsd drift detectability does NOT imply the model is reading
   prior turns as dialogue content vs. token-bag shift artefacts

## 6. Artefacts

- `state/anima_emerge_5turn_dialogue_smoke_2026_05_05/aggregate.json`
- `state/anima_emerge_5turn_dialogue_smoke_2026_05_05/verdict.json`
- `tool/transient_py/anima_emerge_5turn_dialogue_smoke.py` (raw#37 transient)

## 7. Lane closure

- BG-AG attractor finding → BG-AJ smoke: **dialogue medium PASS at mode=none**
- Open: semantic-content vs token-shift disambiguation (would require
  scrambled-prior / null-prior / repeated-turn ablations); deferred
- Open: Pβ Φ★-axis adapter mode interaction (currently `mode=none` only;
  Pβ adapter cross-substrate consistency lane unchanged)
