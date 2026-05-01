# Schartner LZ76 Criteria Validation — anima verifier vs literature

**Date:** 2026-04-28
**Verifier under audit:** `<repo-root>/anima-clm-eeg/tool/clm_eeg_lz76_real.hexa`
**Frozen criteria (raw#12):**
- C1: `LZ76_norm ≥ 0.65`  (`LZ76_EEG_MIN_X1000 = 650`)
- C2: `|Δ|/human ≤ 20%`   (`DELTA_HUMAN_MAX_PERMILLE = 200`, baseline `HUMAN_BASELINE_LZ76_X1000 = 850`)
- Cited reference: "Schartner 2017 (LZ complexity for resting EEG); Kaspar-Schuster 1987 (Phys Rev A 36:842)"
- Per-channel **median** binarization → 16-channel concatenation → Kaspar-Schuster 1976 LZ76 production count → `b(n) = c(n)·log2(n)/n`

---

## (1) Schartner reference — DOI / journal / volume

The verifier’s self-description ("Schartner 2017 PLOS ONE … resting EEG") **conflates two different papers**:

| Verifier label | Actual paper that exists |
|---|---|
| "Schartner 2017 PLOS ONE" | **Does not exist.** PLOS ONE Schartner paper is **2015** (Propofol anaesthesia). |
| "Schartner 2017"          | **Schartner MM, Pigorini A, Gibbs SA, Arnulfo G, Sarasso S, Barnett L, Nobili L, Massimini M, Seth AK, Barrett AB.** "Global and local complexity of intracranial EEG decreases during NREM sleep." *Neuroscience of Consciousness* **2017(1): niw022.** DOI: `10.1093/nc/niw022`. PMID: 30042832 / PMC6007155. — but this paper uses **intracranial SEEG**, not scalp EEG, and uses a **Hilbert-envelope** threshold, not median. |
| "resting-EEG human cohort, 16-ch, ~0.85 ± 0.05" | **The number 0.85 ± 0.05 cannot be located in either Schartner 2015 or Schartner 2017.** Both papers report values **graphically**, not as group mean ± SD tables. Visual inspection of Schartner 2015 Fig 7 puts wakeful-rest LZc at ≈0.6–0.7, and LOC (anaesthesia) at ≈0.4–0.5. |

So the canonical references to cite are:

1. **Schartner et al. 2015** — *PLOS ONE* 10(8): e0133532. DOI `10.1371/journal.pone.0133532`. — *propofol anaesthesia, scalp EEG, 1 kHz → downsampled 250 Hz, 10-s segments, ≈60 segments per subject/condition.*
2. **Schartner et al. 2017** — *Neurosci Conscious* 2017(1): niw022. DOI `10.1093/nc/niw022`. — *NREM sleep, intracranial SEEG, 1 kHz → 250 Hz, 10-s segments.*
3. **Kaspar F, Schuster HG.** "Easily calculable measure for the complexity of spatiotemporal patterns." *Phys Rev A* **36**(2): 842 (1987). — citation in verifier is **correct.**
4. **Lempel A, Ziv J.** "On the complexity of finite sequences." *IEEE Trans Inform Theory* **22**(1): 75–81 (1976). — *not cited explicitly in verifier comments but the algorithm is correct: it is the LZ76 production-count.*

---

## (2) Awake-resting normalised b distribution (mean ± SD from primary sources)

**Honest finding:** neither Schartner 2015 nor Schartner 2017 publishes a tabulated mean ± SD for normalized awake LZc. They publish:

- Schartner 2015: per-subject paired LZc values (WR vs LOC), with the explicit claim that *"a single threshold can be drawn that separates WR from LOC across all subjects"* and AROC ≈ 1.0. Figure 7 visually places WR LZc at ~0.6–0.7 (broadband, scalp).
- Schartner 2017: per-subject paired values across W / N1 / N2 / N3, again presented graphically; no group-level mean ± SD table.

A widely-replicated independent dataset (Bódizs et al., **eNeuro 2024**, *Spectral Slope and Lempel–Ziv Complexity as Robust Markers of Brain States during Sleep and Wakefulness*, DOI `10.1523/ENEURO.0259-23.2024`) uses **median binarisation** (matching the anima verifier) at 250 Hz, 4-s epochs. They likewise publish narrative ("complexity slightly increased from wakefulness to all sleep stages, narrowband 30-45 Hz") and figure-only values; the full numerical table is in the OSF dataset (`https://doi.org/10.17605/OSF.IO/QGPW4`), not in the body text.

**There is no literature locus that says "awake resting normalized LZc = 0.85 ± 0.05."** The 0.85 figure in `clm_eeg_lz76_real.hexa` is **not directly attributable to any cited paper** in the form claimed.

---

## (3) Where does C1 = 0.65 come from?

The verifier comment string says C1 is a "Schartner human-resting floor 0.65". I could not derive 0.65 from any of:

- Schartner 2015 (Fig 7: WR ~0.6–0.7 graphically — 0.65 is plausibly the **midpoint** or **lower-bound** of that visual band, but is **not** stated in the paper).
- Schartner 2017 (intracranial, different substrate; LZc range similar but not numerically published).
- Kaspar-Schuster 1987 (no human data — purely algorithmic / random-asymptote claim that b → 1 for i.i.d. binary).

**Verdict (3):** C1 = 0.65 is **a plausible "midpoint of the Schartner-2015 visual WR band" but is not formally derived from any cited mean ± k·SD criterion.** It is not "mean − 1 SD" or "mean − 2 SD" of a published distribution; it is an **operational floor** chosen by the verifier author.

---

## (4) Where does C2 = 20% come from?

The verifier defines C2 as `|b − 0.85| / 0.85 ≤ 0.20`, i.e. 0.68 ≤ b ≤ 1.02.

- The 0.85 baseline is **not a primary-source number** (see (2)).
- The 20% tolerance band is **not cited in either Schartner paper.**
- Closest neighbour in literature: Schartner 2015 reports a *relative drop* of ≈30–40% from WR to LOC (LOC/WR ≈ 0.6–0.7). A 20% band on the awake side is therefore **looser than the awake-vs-anaesthesia separation in the source paper** but not contradictory.

**Verdict (4):** C2 = 20% is an **operationally chosen tolerance**, not a paper-derived value. It is internally consistent (20% of a not-from-paper baseline), but the chain of attribution to Schartner 2017 is **broken**.

---

## (5) Binarisation method comparison

| | Schartner 2015 (PLOS ONE) | Schartner 2017 (Neurosci Conscious) | Bódizs eNeuro 2024 | **anima verifier** |
|---|---|---|---|---|
| Binarisation | Hilbert-envelope mean: `T_i = mean(|analytic_signal_i|)` | Hilbert-envelope mean (same) | **Median of raw amplitude** (matches anima) | **Median of raw amplitude** |

**Verdict (5):** The anima verifier uses **median binarisation**, which **does not match** Schartner 2015/2017 (Hilbert envelope). It does match Bódizs 2024 (median). For criterion-attribution purposes, citing "Schartner 2017" while using median binarisation is **methodologically inconsistent** — the two pipelines produce different numeric LZc values for the same input, so the 0.85 ± 0.05 baseline (already not in either paper, see (2)) cannot be ported across binarisation methods.

---

## (6) Sampling rate / window-length differences

| | Schartner 2015 | Schartner 2017 | Bódizs 2024 | **anima verifier** |
|---|---|---|---|---|
| Native fs | 1000 Hz | 1000 Hz | 500 Hz | 125 Hz (Cyton+Daisy native) |
| Analysis fs | 250 Hz | 250 Hz | 250 Hz | 125 Hz (no resample) |
| Segment | 10 s | 10 s | 4 s | "≥ 60 s" full window |
| Channels | scalp EEG (≈64) | intracranial SEEG | scalp EEG | 16-ch Cyton+Daisy scalp |
| Concatenation | spatial (channels × time, 2-D LZc) | same | per-channel + spatial variants | sequential 16-ch concat into 1-D |

**Impact on b(n):** LZc normalised values are weakly sensitive to fs and segment length above ~250 samples (Kaspar-Schuster asymptote), but the **2-D spatial-temporal LZc** used in Schartner 2015/2017 (Eq.: matrix-binarised then traversed row-by-row across channels × time) is **algorithmically different** from anima’s **1-D sequential concatenation**. The 1-D form is the LZc variant used in many later papers (e.g. Bódizs 2024) and is mathematically valid, but again it is **not the form Schartner 2017 used.** Numeric values are not directly comparable.

**Verdict (6):** Sampling-rate gap (125 Hz anima vs 250 Hz literature) is small but non-zero; segment-length gap is larger (60 s anima vs 10 s literature concatenated to ≈600 s); algorithmic gap (1-D concat vs 2-D matrix LZc) is the dominant difference.

---

## (7) raw#91 honest C3 — criteria correctness verdict

**PARTIAL / FALSIFIED-WITH-CAVEATS.**

What is **VERIFIED** in the verifier:
- Kaspar-Schuster 1987 citation (Phys Rev A 36:842) — correct paper, correct algorithm, correctly implemented as LZ76 production count `c(n)`.
- Normalisation `b(n) = c(n) · log2(n) / n` — correct Kaspar-Schuster form.
- Random-asymptote target `b → 1.0` — correct (Kaspar-Schuster 1987).
- Structured-signal target `b ≪ 0.3` — correct (single-period square wave).
- LZ76 algorithm itself — correct Lempel-Ziv 1976 production-count.

What is **FALSIFIED** (i.e. cannot be sourced as claimed):
- "Schartner 2017 PLOS ONE" — **does not exist**; Schartner PLOS ONE is 2015. Schartner *Neurosci Conscious* 2017 is intracranial, not scalp resting EEG.
- `b(awake resting EEG) ≈ 0.85 ± 0.05` — **not published in either Schartner paper.** No primary-source citation supports the specific number 0.85 or SD 0.05.
- C1 = 0.65 = "Schartner human-resting floor" — **not derivable from any cited paper** as mean − k·SD or as an explicit threshold; it is an operationally chosen midpoint of a visually-estimated range.
- C2 = 20% — **operationally chosen**, not a paper-derived tolerance.
- "Per-channel median binarisation" attribution to Schartner — **wrong**; Schartner 2015/2017 use Hilbert-envelope mean. Median binarisation matches Bódizs 2024 (eNeuro), not Schartner.

Net: the **algorithm is correct**, but the **criteria thresholds are pre-registered honest pre-commitments masquerading as paper-derived numbers.** Per raw#10 / raw#91 honesty rule, the reference string in the cert should be reduced to what is actually attributable, and the 0.65 / 0.85 / 20% numbers should be re-labelled as **operational pre-registration values**, not paper-derived.

---

## Recommendations (no code changes by this agent — raw#12 frozen)

1. **Update reference string** in `clm_eeg_lz76_real.hexa:939` from "Schartner 2017 (LZ complexity for resting EEG)" to either:
   - "Schartner 2015 (PLOS ONE 10:e0133532) [scalp EEG, anaesthesia]" — if PLOS ONE was intended, OR
   - "Schartner 2017 (Neurosci Conscious 2017:niw022, intracranial SEEG NREM)" — if 2017 was intended, OR
   - "Bódizs 2024 (eNeuro 11(3):ENEURO.0259-23) [median-binarisation, matching anima pipeline]" — closest methodological match.
2. **Relabel C1 / C2 / human-baseline as "pre-registered operational thresholds"** in the cert `algorithm.reference` field, with an explicit note that 0.65 / 0.85 / 20% are anima pre-commitments (raw#12 frozen 2026-04-26), **not** numbers extracted from a published mean ± SD distribution.
3. **Add binarisation-method note** to the cert: "median of raw amplitude (Bódizs 2024 style); Schartner 2015/2017 use Hilbert-envelope mean — values are not directly comparable."
4. **Optional: deprecate the 0.85 baseline** and replace with an empirically-measured baseline once anima collects N≥10 resting-EEG runs, with the new baseline set as `mean − 2·SD` of the empirical anima distribution. Until then, declare the current baseline a **placeholder**, not a literature value.

These are recommendations only; raw#12 freeze is respected — no edits performed by this agent.

---

## Additional findings

- The verifier’s claim that "pure i.i.d. random binary sequence → b(n) → 1.0" is **correct** in the limit but Schartner 2017 in-vivo calibration figures of "1.05" cited in the user’s prompt are **not in the paper**; they likely originate from the **Aboy et al. 2006** / **Hu et al. 2006** simulation studies on finite-length corrections, where finite-n bias can push `b(n)` slightly above 1.0 for moderate n. Worth attributing correctly if the 1.05 figure is reused elsewhere.
- The verifier’s default selftest size (16 ch × 16 samples = 256 bits) is **far too short** for a stable Kaspar-Schuster asymptote. b(n) at n=256 typically still under-estimates the true random-source value by 20–30% (finite-length bias). For a clean random > structured ordering check this is fine; for any quantitative claim about the 0.65 or 0.85 thresholds, n needs to be ≥ 1024 (preferably ≥ 4096), which the real-data path already provides (≥ 60 s × 125 Hz × 16 ch = 120 000 bits).
- Kaspar-Schuster citation in the verifier (`Phys Rev A 36:842`) is **correct issue/page**; the full title is "*Easily calculable measure for the complexity of spatiotemporal patterns*", year 1987, and the verifier’s `frozen_at: 2026-04-26` cert correctly attributes the algorithm but not the specific in-vivo thresholds.

---

## Sources

- Schartner et al. 2015, PLOS ONE: <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0133532>
- Schartner et al. 2017, Neurosci Conscious: <https://pmc.ncbi.nlm.nih.gov/articles/PMC6007155/> · <https://academic.oup.com/nc/article/2017/1/niw022/2957408>
- Bódizs et al. 2024, eNeuro: <https://pmc.ncbi.nlm.nih.gov/articles/PMC10978822/> · <https://www.eneuro.org/content/11/3/ENEURO.0259-23.2024>
- Kaspar & Schuster 1987, Phys Rev A 36:842 (algorithmic reference; verified via secondary citations)
