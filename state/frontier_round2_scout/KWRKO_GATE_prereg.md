# KWR_KO_GATE — frozen-first pre-registration (H_9212 ④)

**Status**: ⏳ PRE-REGISTERED · FROZEN (p7 · NOT tune-to-green) · 구현됨·미배선
**Frozen constant**: `KWR_KO_GATE = 0.20`
**Derived**: 2026-07-08, BEFORE any 303M ko output was ever scored.
**Derivation script**: `state/frontier_round2_scout/kwrko_gate_derive.py` (seed 4302, $0 corpus stats, mini-safe).
**Twin literals** (unwired): `core/rho_fan.py::KWR_KO_GATE = 0.20` · `core/rho_fan.hexa::KWR_KO_GATE() -> 0.20`.

---

## 1. Why ko needs its OWN gate (en 0.70 is a category error)

The en reach gate uses a frozen **0.70** known-word-ratio bar = fraction of ASCII word-tokens
present in the 235k `/usr/share/dict/words` lexicon → a **lexicality** coverage measure.

Korean tokenizes to whole **eojeol** ("물이", "의식은" stay single tokens — the landed
`_rho_fan_words_uni` keeps hangul runs intact), so exact dictionary membership is the wrong
predicate. The ko proxy `kwr_ko` measures **josa-suffix grammaticality density** (fraction of
eojeol that carry a Korean particle / are a function word) — a **different physical quantity**
(a_scale_honest_scope). Reusing 0.70 = always-fail or meaningless-pass. Hence a separately
derived, separately named frozen constant; **en 0.70 stays UNCHANGED**.

## 2. The `kwr_ko` proxy (model-independent · closed-class)

Tokenizer = `core/rho_fan.py::_rho_fan_words_uni` (the H_9212-landed eojeol-run splitter).
A token is a **hit** iff:
- (a) it is an exact `KO_FUNC` word (connectives / bound nouns: 그리고·그러나·하지만·즉·따라서·것·수·등·무엇·…), OR
- (b) it is **pure-hangul** and ends in a `KO_JOSA_SUFFIX` (은·는·이·가·을·를·에·의·도·만·과·와·로·에서·부터·까지·처럼·보다·으로·… longest-first) with **stem ≥ 1 syllable**.

`kwr_ko(text) = hits / n_tokens` (0.0 on empty). Both sets are curated closed-class lists —
**no model, no training, no /usr/share/dict** — so the gate is fully model-independent.

## 3. Two model-independent distributions (n=20 000 held-out each)

Corpus = `dancinlab/anima-corpus-ko-general` (57 MB) + `anima-corpus-ko-sns` (5.9 MB), local HF
mirror. 622 455 hangul-bearing sentences; gate derived on a **disjoint holdout half** (seed 4302
shuffle) so it never sees the future eval half.

| distribution | mean | p5 | p25 | **p50** | p75 | **p95** |
|---|---|---|---|---|---|---|
| **(1) POSITIVE** — real ko sentences (UPPER ref) | 0.370 | 0.00 | 0.25 | **0.40** | 0.50 | 0.667 |
| **(2a) NEGATIVE** — byte-shuffle garble | 0.0037 | 0.00 | 0.00 | 0.00 | 0.00 | **0.00** |
| **(2b) NEGATIVE** — random valid-hangul | 0.0011 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| **(2) NEGATIVE combined** (LOWER ref) | 0.0024 | 0.00 | 0.00 | 0.00 | 0.00 | **0.00** |

The garble null is a **near point-mass at 0.0** (mean 0.002, p95 0.0): byte-shuffling destroys
UTF-8 3-byte hangul structure → mostly separators → ~no josa-ending eojeol; random valid-hangul
strings almost never end an eojeol on a josa syllable by chance. Real ko sits far above.

## 4. Decision rule (pre-registered · robust to the positive zero-tail)

The naive **midpoint(pos_p5, neg_p95)** DEGENERATES to **0.0**: the positive distribution has a
fat zero-tail — short fragments and legitimately josa-free eojeol runs score 0, so `pos_p5 = 0`.
A p5-anchored gate would sit at 0.0 and admit garble. The two distributions separate cleanly at
the **center**, not the tail, so the frozen rule anchors there:

> **KWR_KO_GATE = midpoint( neg_combined_p95 , pos_p50 ) = midpoint(0.00, 0.40) = 0.20**

garble **UPPER** reference (p95) vs real **CENTRAL** tendency (median) — the number lies strictly
between the two model-independent distributions and is chosen from their SHAPE alone, with **no
303M output involved**. This rule + the degeneracy of the naive one were both recorded before
freezing (full transparency; the choice is methodology, not tune-to-green).

**Separation at the frozen gate 0.20**:
- real ko clears (kwr_ko ≥ 0.20): **80.0 %**
- garble fails (kwr_ko < 0.20): **99.74 %**

(The 0.26 % of garble that clears is byte-shuffle chance landing a josa tail — well inside the
noise floor.) Contrast: en gate 0.70 ≫ 0.20, confirming the two are incomparable quantities.

## 5. Scope exclusion (pre-registered)

- **ko FALS is SCOPE-EXCLUDED** from the reach verdict until this gate is actually applied by a
  scoring path (H_9212 ③ per-cell dispatch). The comparator / measurable falsifiability sets are
  English; a ko comparator set is a separate future H (en-set translation-reuse is itself a
  tune-to-green vector and is forbidden).
- ko cells score **kwr_ko + reach (ρ-AXON Δ)** only, once ③ lands.

## 6. Freeze & anti-tune-to-green invariant

`KWR_KO_GATE = 0.20` is frozen NOW, before the first ko decode is ever scored. If the first ko
scoring run is negative, **negative is the result** (🟦). The ONLY legal way to change this gate
is a NEW frozen-first H that re-derives it from model-independent distributions and preserves
this record verbatim. Adjusting 0.20 after seeing a 303M score = REJECT (p7 · c9).

## 7. Reproduce

```
python3 state/frontier_round2_scout/kwrko_gate_derive.py   # $0, ~seconds, mini-safe
```
Requires the local HF mirror at `~/.cache/huggingface/hub/datasets--dancinlab--anima-corpus-ko-{general,sns}`.
If absent, fetch (still $0):
```
huggingface-cli download dancinlab/anima-corpus-ko-general --repo-type dataset
huggingface-cli download dancinlab/anima-corpus-ko-sns     --repo-type dataset
```
(Corpus WAS on disk at derivation time — no infra-wall.)
