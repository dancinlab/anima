# H_1596 — G6 IDEATION fals=0 wall-break (6-lens orthogonal census)

**Lineage:** builds on **H_1595** (py 2-production, TERMINAL, NOT artifact): h1129 = 303M ByteGPT,
24-layer GPT-2-class (ALREADY DEEP). G6 PASS iff `dist>=5 AND fals>=1` (frozen,
7B_PASS_CONDITIONS.md, p7). h1129 measured **dist=6 PASS, coherent=6 (distinct + coherent, NOT
garble), fals=0 FAIL — seed-robust 0/3** across {7,4302,4303}. The wall is SPECIFICALLY the
falsifiability sub-metric. Sibling gate-measurement fixes: H_1588 (G1 multi-seed), H_1591 (G4/G6
wiring). **This is a research/census — NO terminal verdict banked; frozen bar UNTOUCHED (no
tune-to-green).**

## The fals detector (frozen)
`core/g6_ideation.py::_g6_is_falsifiable` L111 (byte-parity twin `core/g6_ideation.hexa`). PASS iff
ALL: (a) COMPARATOR word (closed ~25-word set) AND (b) MEASURABLE word (closed 25-word set) AND (c)
>=2 content words AND (d) not ending '?' AND (e) first-3 not all stance.

## Convergent diagnosis (5/6 lenses isolate the MEASURABLE word)
Five independent $0-local detector probes (L1/L3/L4/L5/L6) isolate ONE missing ingredient: on
realistic coherent h1129-style continuations the COMPARATOR is frequently present but the MEASURABLE
word is ~0%. The measurable lexicon is 25 words = 0.0107% of the 234,461-word dict (rare
scientific-register nouns). Rephrasing the same ideas into quant-comparative register flips fals 0→1
with kwr (coherence) unchanged. So **fals=0 is a register/surface-form gap, not coherence or
depth/capacity** — depth-as-lever (clm303 L4) is N/A (h1129 already 24-layer deep, dist=6 coherent=6).

## The 6 lenses (all probes RAN $0-local except decode-side lifts)

| key | lens | family / break-walls class | cost | predicted | confidence |
|---|---|---|---|---|---|
| L1 | detector-validity (closed comparator/measurable whitelists drop true claims) | measurement-artifact (a) | $0-py-summer | lift | high |
| L4 | decode-budget (gen=40B≈8w truncates before rare measurable word) | measurement-harness (a) | $0-py-summer | lift | medium |
| L3 | frame-conditioning (1-shot falsifiable exemplar unlocks latent register) | wrong-direction/latent (b) | $0-py-summer | lift | medium |
| L6 | objective-aux (reranker INERT without register mass; data-curriculum lever) | objective/data (b)/(e) | $0-py-summer | lift/null | high |
| L5 | savant golden-zone disinhibition (architecturally disjoint from G6 text path) | capacity-expression (d) | $0-local (toy) | **null** | high |
| L2 | corpus-register scarcity (comparator∧measurable ~0.5%en/0.0%ko in corpus) | data under-investment (e) | toy-train | lift | medium |

**Probe highlights (captured this campaign):**
- L1: live frozen detector REJECTS 4/10 genuine human falsifiable claims (all fail purely on the
  comparator/measurable whitelists); 5/5 non-falsifiable negatives REJECT (not vacuous); broadened
  vocab admits 0/5 negatives (broadening control-safe).
- L2: 4-cell corpus window co-occurrence (comparator∧measurable): en-gen 0.50%, en-sns 0.41%,
  ko-gen/ko-sns 0.00% (ASCII detector can NEVER fire on Hangul). E[fals over 6 ideas]=0.03→0.004 ⇒
  P(fals=0)=97.0–99.6%, matching measured 0/3.
- L4: coupon-collector E[fals]=0.08 at 8w (≈observed) → 1.03 at ~40w(~200B); rare MEASURABLE word is
  the binding constraint; multiseed varied ONLY RNG at fixed gen/temp.
- L5: grep over the 3 G6 scorer files for savant/inhibit = EMPTY (architecturally disjoint); fals=0
  with comp=1,meas=0 on coherent prose.
- L6: reranker sim — h1129-register(meas=0%) fals 0/6 at k=1/8/40 (INERT); curriculum-register(meas=3%)
  fals 6/6 at k=8 (register flips PASS even without rerank).

## RANKING (cheapest measurable lift first) — full table in `state/1596_g6_fals_wall_break/CENSUS.md`
1. **L1** (CHAMPION) · 2. L4 · 3. L3 · 4. L6 · 5. L5 (null ablation) · 6. L2 (train).

## CHAMPION — fire L1 FIRST
Run-FIRST measurement-artifact check; cheapest + highest-info. Decode ~30 h1129 ideas (summer
py-engine) → two-scorer comparison ($0-local): live frozen `_g6_is_falsifiable` vs human-tag. If
human-tagged-fals >> detector-fals → class (a) artifact; if both ~0 → genuine register/data (hand to
L3/L4 cheap decode levers, then L2 train). Broadening ablation (verified admits 0/5 negatives)
isolates vocabulary-from-logic without moving the frozen bar.

## WALL CLASSIFICATION (post-census → UPDATED by H_1597 L1-fire)
Census *predicted* primarily class (a) measurement-artifact (L1 CHAMPION). **H_1597 FIRED L1 on
h1129's own ideas and REFUTED the (a) prediction:** a corpus-grounded, Hangul-aware, strictly-broader
detector (recovers 5/5 false-rejects incl Korean, admits 0/5 negatives — control-safe) STILL scores
h1129's 18 ideas at **fals=0/18**. So the wall is **NOT class (a) detector-vocabulary/tokenizer**.
The L1 false-reject finding (40% on *human* claims) is real but does not explain h1129's own output —
h1129 emits fluent prose with NO comparator+measurable claim, so even the fair detector can't fire.
**Surviving classification = class (e) data-register under-investment** (L2/L6: corpus comp∧meas
~0.5%en/0.0%ko, measurable decode mass ~0). L5 ablation rules OUT (d) true-ceiling. Lever now lives
on the CORPUS register (train-side L2), not the detector. (L3 latent-register decode-prime remains
an untested cheap lever.)

## Engine-native / honesty
Scorer import-closure verified **grep-clean** (`grep -lE 'import torch|gauge_lib'
core/g6_ideation.py core/bytegpt_decode.py core/g_gates.py` → EMPTY). Terminal-path for any future
banked verdict = py 2-production (`core/g_gates.py::g_eval_g6_multiseed` ← `core/bytegpt_decode.py`,
torch-free numpy) OR wired hexa single-entry (`cli/anima.hexa eval` → `core/g_gates.hexa::g_eval_g6`).
ckpt `~/anima-weights/bytegpt303_h1129/h1129.bin` on summer (sha256 5cf07a36…, 1213440020 bytes,
mouth=bytegpt). **Frozen bar untouched** (`dist>=5 AND fals>=1`); NO tune-to-green (p7). Detector
broadening / curriculum levers must NOT hand-stuff the exact 25+25 detector tokens (Goodhart guard).

**wired:** `census only — L1 CHAMPION subsequently fired + banked as H_1597 (detector-fairness
TERMINAL); class-(a) prediction REFUTED, surviving lever = corpus register (L2, untested)`.

**artifacts:** `state/1596_g6_fals_wall_break/CENSUS.md` (6 lens findings + ranking + champion +
wall classification) · L1 fire → `state/1597_g6_corpus_grounded/` (H_1597) · scorers
`core/g6_ideation.py` · `core/g_gates.py` · `core/bytegpt_decode.py`.
