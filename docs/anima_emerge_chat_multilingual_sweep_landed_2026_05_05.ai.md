<!-- @no-lineage-citation-exempt-file -->
# anima emerge chat multilingual sweep landed 2026-05-05

Task: anima_emerge_chat_multilingual_sweep_2026_05_05
Lane: BG-CD (substrate language-capability falsifier)
Cost: $0 (mac CPU fp32, .venv-eeg python3.12)
Wall: ~3.0 min sweep + 5.5s load
Verdict label: MULTILINGUAL_FAIL_TRUE_DEGENERATE_LOOP_ALL_LANGUAGES

## 1. Why this sweep ran

BG-BR (logit-lens probe at state/anima_emerge_chat_logit_lens_2026_05_05/)
found that the substrate emits multilingual fragments under a Korean prompt
in mid-layers (Chinese government-related tokens, fragments, and Cyrillic).
Open question: was that Korean-prompt-specific multilingual leakage, or
does the substrate behave the same for all languages?

Hypothesis to falsify:
- H1 per-language coherence: Chinese prompt produces Chinese emit, etc.
- H2 uniform fail: substrate degenerates regardless of input language.

## 2. Method

12 prompt families, greedy-decode 25 max_new on need-singularity/clm-v4-mk2-v1.
Families: chinese_simplified, chinese_traditional, japanese_hiragana,
japanese_katakana, english, numbers, code_python, code_html, math,
punctuation, korean, mixed_ko_en. Per-emit char categorization by Unicode
block (CJK, Hiragana, Katakana, Hangul, ASCII letters, digits, control).

## 3. Results — emit per prompt (first 25 emit chars)

- chinese_simplified  produces "pdhhhhhhhhhhhhhhhhhhhhhhh" (ascii_letters)
- chinese_traditional produces "ppppppppppppppppppppppppp" (ascii_letters)
- japanese_hiragana   produces "/OOOOOOOOOOOOOOOOOOOOOOOO" (ascii_letters)
- japanese_katakana   produces "(((((((((((((((((((((((((" (OTHER ASCII punct only)
- english             produces "aaaaaaaaaaaaaaaaaaaaaaaaa" (ascii_letters)
- numbers             produces "b/jjjjjjdhhhhhhhhhhhhhhhh" (ascii_letters)
- code_python         produces "/OOOOOOOOOOOOOOOOOOOOOOOO" (ascii_letters)
- code_html           produces backtick + 1 CJK + 24 replacement (chinese=1)
- math                produces "(" + 24 replacement chars (OTHER)
- punctuation         produces "ppppppppppppppppppppppppp" (ascii_letters)
- korean              produces "/OOOOOOOOOOOOOOOOOOOOOOOO" (ascii_letters)
- mixed_ko_en         produces "b((((((((((((((((((((((((" (ascii_letters)

## 4. Prompt-language-match gates

- any CJK char in chinese_simplified emit: FAIL (0)
- any Hiragana char in japanese_hiragana emit: FAIL (0)
- any Hangul char in korean emit: FAIL (0)

All three same-language gates FAIL_TRUE. The substrate produces ZERO
script-matching characters when prompted in Chinese, Japanese, or Korean.

## 5. Architectural finding

H2 (uniform fail) confirmed. The substrate does not exhibit per-language
capability. Every prompt collapses to a single repeated low-id ASCII token
within 1-2 emit positions (h, p, O, paren, a, j attractors). Code_html is
the only family that emits a non-ASCII non-replacement char (a single CJK
token followed by replacement chars).

Numbers, math, and punctuation do NOT respect their input class. The
numbers prompt does not produce digits; math does not produce digits or
equality sign; the substrate ignores prompt content and falls into the
same ASCII-loop attractor seen on every other family.

This is consistent with the prior chat-incapability finding and the prior
CLM v4 LoRA SFT falsification: the substrate has structural hidden-state
geometry (axis discrimination, phi star) but no working language-modeling
head behavior at emit time. The earlier BG-BR multilingual fragments are
an intermediate-layer logit-lens artifact, not an emit-time capability.
The lens reads layers 6-10 where the residual still contains training-
corpus echoes, but the head_a final-layer projection collapses those to
ASCII attractor IDs (e.g. id=32) regardless of input language.

Train-data composition implication: the substrate must have seen CJK,
Hiragana, Katakana, Hangul, and Cyrillic in training (mid-layer logit lens
shows those tokens), but the SFT or post-training step that aligned head_a
destroyed or never built the per-language coherence path. The decoder body
remembers; the head does not.

## 6. Decoupling vs. BG-BR

- BG-BR (logit lens, layers 6-10): substrate has multilingual representational
  memory.
- BG-CD (greedy decode, layer 16 final): substrate has zero multilingual
  emission capability.

Both can be true at once because they live at different depths of the same
forward pass. This rules out the optimistic reading "Korean fails but
Chinese might work" and joins this lane to the closed CHAT_CAPABILITY_LANE
FAIL_TRUE classification.

## 7. Honest C3

- C1 mac CPU fp32; same substrate as BG-BR (numerical drift inside ULP).
- C2 single prompt per language family; broader corpus may shift dominance.
- C3 char-class breakdown counts Unicode blocks, NOT semantic coherence.
- C4 max_new=25 token cap; longer-horizon emit untested.
- C5 mixed/punctuation/numbers/code prompts have no single matching language
  so dominance there is pure substrate-bias not a match-test; numbers'
  failure to produce digits is the most damning architectural signal.

## 8. Deliverables

- state/anima_emerge_chat_multilingual_sweep_2026_05_05/aggregate.json
- state/anima_emerge_chat_multilingual_sweep_2026_05_05/verdict.json
- tool/transient_py/anima_emerge_chat_multilingual_sweep.py (transient, sister-rule)
- docs/anima_emerge_chat_multilingual_sweep_landed_2026_05_05.ai.md (this)

## 9. Policy compliance

- transient sister-rule python: yes (tool/transient_py/)
- additive only: yes (no shim/mount/loader/dialogue_load mod)
- honest C3: yes (5 caveats in verdict.json)
- no commit: yes
- no secret leak: yes
- HEXA_PY=.venv-eeg/bin/python: yes

## 10. Next-step recommendation

Treat BG-CD as the closing falsifier on the "maybe Korean is just unlucky"
escape hatch from the chat-incapability finding. The substrate is not
language-capable in any of the 12 families tested. Subsequent emerge-chat
lane work should focus on the CLM-2-EXEC retrain (chat-cap hope) rather
than further probing of CLM v4 substrate emission. No additional
same-substrate prompt-language sweeps recommended; the result generalizes.
