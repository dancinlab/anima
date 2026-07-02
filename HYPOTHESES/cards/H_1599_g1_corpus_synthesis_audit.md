# H_1599 — does the training corpus contain 2-concept synthesis examples? (G1 data-distribution lens)

**Question (a_break_the_wall, lens = data-distribution ceiling):** the clm303 G1
(C2 RECOMBINE) wall survives depth (H_1598 L8 FALSIFIES depth-lever). One orthogonal lever
is the **training distribution**: if the 4-cell corpus never shows two seed concepts bound in
the same line, no objective/depth can teach composition (data-starvation ceiling). Audit the
co-occurrence of the frozen G1 concept families in the actual corpus cells.

**Engine path:** pure corpus statistics — no model, GPU 0, torch-free (grep self-check clean).
TERMINAL per a_engine_native_learning (counting, not a mirror).

## Method (frozen-first)
- Concept keyword-sets = **VERBATIM** the 5 CONCEPTS families from `g1_multiseed.py` (the frozen
  G1 scorer). A corpus unit (line / sentence) is a **synthesis example** iff it hits ≥2 DISTINCT
  concept families — exactly mirroring the G1 scorer's `coverage()≥2` distinct-family rule.
- Frozen prediction (pre-registered before running): synth_rate < **0.5%** in EVERY cell ⇒
  DATA-STARVATION SUPPORTED; any cell ≥0.5% ⇒ REFUTED for that cell.
- Cells audited (local, sha-verified): `gen_en gen_ko sns_en sns_ko` (4-cell clean register corpus,
  ~1.1–1.4 MB each) in `state/clm303_clean_corpus/`.

## Result (line granularity, frozen 0.5% bar)
| cell   | n_units | synth (≥2 families) | rate    | vs bar |
|--------|---------|---------------------|---------|--------|
| gen_en | 4535    | 1184                | 26.11%  | ≥bar (PRESENT) |
| sns_en | 6862    | 1202                | 17.52%  | ≥bar (PRESENT) |
| gen_ko | 6661    | 5                   | 0.075%  | <bar (STARVED) |
| sns_ko | 10407   | 5                   | 0.048%  | <bar (STARVED) |

Sentence granularity agrees (en 7.7–11.4% / ko 0.02–0.03%). **CONTENT-ONLY control** (drop the
generic stopwords the/when/from/into/new/still/between/arises that the scorer's KNOWN-dict also
counts) shrinks EN to **gen_en 0.60% · sns_en 0.39%** and **ko → 0.0% both** — i.e. once stopword
noise is removed, EN synthesis density is ~0.4–0.6% (just at/above bar) and **Korean is genuinely 0**.

## VERDICT
<!-- CARD_VERDICT -->
🟠 **DATA-STARVATION is REGISTER-SPLIT, not uniform.** The English cells DO contain 2-concept
co-occurrence (26%/17.5% raw; ~0.4–0.6% on content-only words) — so for English the G1 wall is
**NOT pure data absence** (synthesis examples exist, yet H_1598 L8 still fails G1). The **Korean
cells are starved** (0.05–0.08% raw, **0.0% content-only**, 300–500× below English) — for Korean a
data-distribution ceiling is plausible. Net: data-starvation is **REFUTED as the sole/primary G1
lever** (English has the examples and still fails), but a **ko-specific data gap** is real and
compounds the wall on the Korean side. The dominant lever is elsewhere (objective / framing), with
ko-corpus enrichment a secondary, independently-true fix.

Caveat (c9): family4 keyword-set includes stopwords (the/when) that inflate raw EN co-occurrence;
the content-only control is the honest read (EN ~0.4–0.6%, ko 0.0%). Co-occurrence in a *line* is a
weak proxy for a *taught composition* (the two concepts may co-occur without being bound) — so even
the EN "present" is an upper bound on genuine synthesis supervision.

**wired:** `engine-native (pure corpus stats, numpy/grep-clean of import torch|gauge_lib); no
core/ change (audit). frozen 0.5% bar UNMOVED. follow-on: lever is objective/framing not data;
ko-corpus synthesis enrichment = secondary independent fix.` artifacts: `state/1599_g1_corpus_synthesis_audit/`.
