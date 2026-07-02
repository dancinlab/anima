# H_1597 — G6 corpus-grounded fals (detector fairness): is h1129 fals=0 a detector-vocabulary artifact?

**Lineage:** the decisive experiment for the H_1596 census fork. H_1596 isolated two candidate root
causes for h1129's G6 `fals=0` (H_1595 GENUINE seed-robust wall): (a) **DETECTOR vocabulary too
narrow** — the frozen `_g6_is_falsifiable` whitelists are closed 25+25 English-ASCII sets, so the
model might ALREADY emit falsifiable-shaped claims the detector silently drops (esp. broadened-EN
verbs/nouns and ANY Korean, since `_g6_words` is ASCII-only and drops Hangul); vs (b) **CORPUS
register absent** — the measurable-claim token-class has ~0 probability mass at decode. H_1597 tests
(a) directly.

## VERDICT: 🧱 NOT a detector-vocabulary/tokenizer artifact — GENUINE ideation wall (detector cause (a) RULED OUT)

Re-scored h1129's OWN G6 ideas (18 = 6 composed frames × seeds {7,4302,4303}, gen=40 canonical) with
TWO detectors over the SAME generations:
- **(A) FROZEN** english-ASCII `_g6_is_falsifiable` (the production bar).
- **(B) CORPUS-GROUNDED Hangul-aware**: comparator/measurable lexicon = frozen anchors + corpus-
  attested EN extensions (freq-gated against the 4-cell training corpus) + corpus-attested Korean
  stems; tokenizer Unicode-aware (Hangul survives, unlike frozen ASCII-only `_g6_words`).

| metric | frozen (A) | grounded (B) |
|---|---|---|
| h1129 G6 fals over 18 coherent ideas | **0/18** | **0/18** |
| CONTROL non-vacuous — negatives admitted (must be 0, incl ko) | — | **0/5** ✅ |
| CONTROL genuine-recover — true falsifiable claims passed (incl ko) | **0/5** | **5/5** ✅ |

- The grounded detector is **demonstrably FAIRER**: it recovers **5/5** true falsifiable claims the
  frozen set false-rejects — including Korean ("압력이 낮아지면 비가 더 자주 내린다", "온도가 높아지면
  반응 속도가 빨라진다") that the frozen ASCII path can never fire on — while still rejecting **0/5**
  pure-stance negatives (non-vacuous). So B is a sound, more-generous, Hangul-capable instrument.
- **Yet B ALSO scores h1129's own ideas at 0/18.** A strictly broader & Hangul-aware detector finds
  zero falsifiable claims → the wall is NOT the detector vocabulary or the ASCII tokenizer.
- Mechanistic note: every h1129 continuation here is **coherent English web-prose** (kwr 0.57–1.0),
  e.g. `'the addition of control of consciousness'`, `'soe the value of the value term may be u…'` —
  the Hangul-recovery path was never even triggered, because h1129 emits no Korean on these frames.
  The ideas read as fluent prose that makes no comparator+measurable falsifiable claim. This points
  to H_1596 cause (b) — the **corpus register** lacks quantitative-claim form — not the detector.
- **Goodhart guard PASS:** B's EN extensions are corpus-frequency-attested (e.g. `increase:42`,
  `grow:62`, `time:596`, `power:106`, `temperature:38`), NOT hand-stuffed into the frozen set; all 18
  KO comparator + 19 KO measurable stems verified substring-present in the 4-cell corpus. B ≠ frozen
  set (asserted).

**Engine:** py 2-production (`core/bytegpt_decode.py` numpy, torch-free), decode byte-identical to
`core/g6_ideation.py::g6_score_arm_auto` (`ideate(frame, gen, base_seed+i)`). **TERMINAL** per
`a_engine_native_learning`; self-check `grep -lE 'import torch|gauge_lib'` over slug + core
import-closure = EMPTY. **Detector B is a SEPARATE fairness instrument, reported ALONGSIDE the frozen
bar — the frozen bar is UNTOUCHED (no tune-to-green, p7).** No GPU; $0; mini.

**ckpt:** `~/anima-weights/bytegpt303_h1129/h1129.bin` — sha256
`5cf07a360c57a133b66e8de8c3c390d5242204d68f75a86b977f1935587f512e`.

**wired / scope (honest residual):** N/A — fairness measurement (no GREEN/bar change). The frozen
detector stands; the surviving lever is the CORPUS register (H_1596 cause (b)), not the detector.
TERMINAL on the **py 2-production engine** (numpy decode byte-parity-proven), with the same
un-captured residual marked **DIRECTIONAL** as H_1595: the G6 SCORING parity of this py side-harness
vs the WIRED `cli/anima.hexa eval` single-entry on h1129 is not yet captured (wired hexa OOMs on
mini). The dual-detector finding (frozen 0/18 == grounded 0/18, with valid controls) is robust to
that residual because both detectors run on the identical numpy generations. Follow-on ING = capture
the scoring-parity on pool/GPU. Frozen bar untouched (no tune-to-green).

**artifacts:** `state/1597_g6_corpus_grounded/m3_corpus_grounded.py` ·
`state/1597_g6_corpus_grounded/m3_gen40.out` · `state/1597_g6_corpus_grounded/m3_result.json` ·
`state/verdicts/1597_g6_corpus_grounded/1597.txt` · corpus `state/clm303_clean_corpus/{gen,sns}_{en,ko}.txt`
· `core/g6_ideation.py` · `core/bytegpt_decode.py`.
