# anima_emerge_chat_korean_logit_bonus — landed 2026-05-05

## status
- **verdict**: PASS_BOOST_RECOVERS (heuristic) / FAIL_SEMANTIC (qualitative)
- **lane**: anima_emerge / chat-cap Korean common-token logit boost
- **angle**: opposite of byte-monopoly / Korean-only-constraint ban-side family — direct promote-side

## context
Direct logit boost experiment. Substrate `dancinlab/clm-v4-mk2-v1` is given a
large logit bonus on the token ids of 50 common Korean lexicon entries (greeting /
copula / particle / connective / temporal / interrogative / adjective / noun / verb)
to test whether coherent Korean text is emitted under forced-promote conditions.

reference peers:
- `state/anima_emerge_chat_byte_monopoly_break_2026_05_05/verdict.json`
- `state/anima_emerge_chat_korean_only_constraint_2026_05_05/`

## configuration
- model: `dancinlab/clm-v4-mk2-v1` mac CPU fp32
- prompt: `안녕`
- 50 common Korean words/morphemes, sentencepiece-encoded, yielding 71 boost token ids
- bonuses: {2.0, 5.0, 10.0, 20.0, 50.0, 100.0}
- combined: boost + byte-fallback `<0xNN>` ban @ {10.0, 50.0}
- max_new_tokens: 20
- decoding: greedy argmax (no sample)

## results

| config | korean_count | emit head |
|---|---|---|
| bonus=2.0 | 0 | byte fallback monopoly |
| bonus=5.0 | 0 | byte fallback monopoly |
| bonus=10.0 | 0 | byte fallback monopoly |
| bonus=20.0 | 35 | Korean degenerate repeat |
| bonus=50.0 | 35 | Korean degenerate repeat |
| bonus=100.0 | 35 | Korean degenerate repeat |
| combined boost=10 + byte ban | 35 | Korean degenerate repeat |
| combined boost=50 + byte ban | 35 | Korean degenerate repeat |

- **threshold**: bonus >= ~20.0 to flip argmax from byte fallback to boost set
- **degenerate collapse**: highest-prior Korean token in boost set repeats every step
- **byte ban orthogonal**: combined identical to pure boost @ same level (boost set
  already dominates byte fallback once super-saturated)
- aggregate stats: n_korean=5/8, n_semi_coherent=5/8, max_korean_count=35

## interpretation

1. The substrate's Korean-token logits at the base position are roughly 20 nats below
   the byte-fallback logits. Below the bonus=20 threshold, the byte fallback remains
   argmax.
2. Above bonus=20 the boost set wins, but greedy argmax inside the boost set collapses
   to the highest intrinsic prior token at every step, producing repetition collapse.
3. The boost path is prior surgery only. The substrate is not hiding a Korean
   sequence-composition capacity — that capacity is absent at this surface level.
4. Adding a byte ban on top of boost is redundant once boost saturates the byte
   fallback already.
5. The semi-coherent heuristic (`len>=5 + korean>=5 + max-char-freq <= 0.5`) is
   passed by 5 of 8 configs, but this only certifies the absence of byte fallback
   plus sufficient Korean character volume. It is not a semantic certification.

## honest caveats

- C1 mac CPU fp32 (host substrate)
- C2 boost is brute-force prior, not semantic recovery
- C3 50 common Korean words/morphemes is a narrow vocabulary slice
- C4 high bonus (100) is far OOD; logits saturate so gradient-style analysis is
   meaningless at that scale
- C5 `looks_like_korean_text` is an anima-internal heuristic, not semantic-grounded

## boost-path final

The byte-monopoly probe, the Korean-only constraint probe, and the present logit-boost
probe converge on the same conclusion: the substrate's chat-incapability is not
recoverable through token-distribution surface-level masking or promotion. This
re-confirms the architectural finding tracked under issue 115. Boost increases
Korean character throughput but does not unlock sequence-level coherence — the output
collapses to single-token repetition.

Future-lane candidates (out of scope for this run): activation patching at deeper
layers, state-level injection, or chat-cap path closure under cost-discipline.

## artifacts
- script: `tool/transient_py/anima_emerge_chat_korean_logit_bonus.py`
- aggregate: `state/anima_emerge_chat_korean_logit_bonus_2026_05_05/aggregate.json`
- verdict: `state/anima_emerge_chat_korean_logit_bonus_2026_05_05/verdict.json`

## cost
- $0 (mac CPU)
- ~20 min wall

## conformance
- transient_py opt-out namespace: PASS
- token-leak guard: PASS (no token literals)
- destructive-op guard: PASS (no destructive ops)
- HEXA_PY .venv-eeg: PASS
- commit prohibition: PASS (no commit performed)
