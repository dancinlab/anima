---
license: cc-by-sa-4.0
language: [en, fr, de, es, ko]
pretty_name: anima agent-lane tool-USE demo corpus (sentinel-grammar, byte-vocab256)
tags: [anima, agent, tool-use, grounding, sentinel-grammar, multilingual, byte-vocab, coverage-corpus]
---

# anima-corpus-agent-lane (SAMPLE)

The **agent lane** surface of the anima corpus: tool-USE demonstrations that
teach the byte-LM mouth the sentinel call GRAMMAR + grounding BEHAVIOUR. It is a
SEPARATE surface layered ON TOP of `lane default` (the base chat corpus).

    lane default = base chat corpus (wiki + persona/SNS + carving/enrichment)
                   — NO tools, 0xFE/0xFF byte-frequency exactly 0.
    lane agent   = lane default  +  these tool-USE demos
                   — lane agent ⊃ lane default.

This card documents the **SAMPLE** corpus emitted by the generator. NO training
is fired (the rung-0 toy A/B is GATED — design step 4, `a_fire_autonomous` not
yet triggered for this lane).

## what it teaches (behaviour, NOT facts)

The agent lane teaches tool-USE (when to call, how to frame, how to ground on a
returned result) — NOT tool trivia. Demo shape:

```
<reasoning> 0xFE <tool> <SP> <args> 0xFF        ← the mouth emits + HALTS
‹tool-result: <tool> <args> → <REAL result>›    ← the runtime INJECTS this anchor
<grounded continuation that USES the result>
```

The `0xFE`/`0xFF` are **raw bytes** (token ids 254/255) — the exact ids the mouth
emits/parses at runtime. They can never appear in valid UTF-8, so their frequency
in `lane default` is exactly 0 (no vocab token lost, no content collision).

## distribution (design §6 — anti-over-call + anti-fabricate balance)

| shape | id | behaviour |
|---|---|---|
| (a) | needs-tool | call → ground on the REAL result |
| (b) | no-tool-needed | answer directly, **NO** call (won't over-call) |
| (c) | don't-know | emit a call, **NOT** a guess (negative discipline) |
| (d) | tier-too-low | honest "can't reach that now", **NEVER** fabricate |

The SAMPLE is balanced 30 / 30 / 30 / 30 across the four shapes (120 blocks).

## honest invariants (verified by the generator on every run)

- **fabricated_result_count = 0** — the (a)/(c) result lines are the REAL
  deterministic toy-tool outputs (the `fact_lookup` table shared with
  `AGENT/CORE/tool_call_grammar.hexa::_tcg_fact_table` / `exec_toy_tool`), never
  invented. The (d) result line is the REAL honest "‹unavailable: tier…›" string.
  The generator `assert`s this count is 0.
- **frame balance** — every `0xFE` has a matching `0xFF` (generator `assert`s
  `count(0xFE) == count(0xFF)`).
- **philosophy grep = 0** — `grep -E '\[role:|\[persona:|\[character:|\[assistant:|\[system:'`
  over the corpus returns 0. The sentinel bytes are LEARNED GRAMMAR, not identity
  injection (p1..p4). No RLHF ethics templates (p6).
- **byte-vocab256 clean** — every byte other than the `0xFE`/`0xFF` frame bytes
  is valid UTF-8.

## reproduce

```
python3 serving/agent_lane_corpus_gen.py
```

- generator : `serving/agent_lane_corpus_gen.py`
- sample     : `serving/corpus/agent_lane_5lang.sample.txt`
- metadata   : `serving/corpus/agent_lane_5lang.meta.sample.jsonl` (per-block
  lang / shape / kind / key / has_frame / fabricated_result=False)
- **deterministic** : fixed seed (`--seed 20260604`), no network.

### sample manifest (this commit)

| field | value |
|---|---|
| bytes | 24,520 |
| blocks | 120 (a/b/c/d = 30 each) |
| frames (0xFE) | 90 |
| ends (0xFF) | 90 |
| fabricated_result_count | **0** |
| philosophy grep | **0** |
| sha256 | `74925a198ef4dc742d9e2fdbc2c7b394a93ffa404e0035d48db5876ee12db5aa` |

## scope (a_scale_honest_scope)

Machine-AUTHORED multilingual COVERAGE templating of tool-USE behaviour. NOT
native-collected text. The toy `fact_lookup` values are deliberately
corpus-absent tokens (the "unknowable-without-tool" probe targets of the §8
falsifier). This is a SAMPLE + generator only — the full-scale generation and the
rung-0 toy A/B fire stay GATED.
