# anima_emerge_chat_self_feed (BG-AW landed 2026-05-05)

**Hypothesis (substrate-natural, no vocab mask / external LM)**
CLM v4가 emit한 fragment를 다음 input으로 feed → 누적되며 coherence emerge 가능?
"상호 대화"의 minimal form — substrate가 자기 자신과 dialogue.

**Outcome**: heuristic-PASS (n_coherent=1/3, best=dialogue) **but inspection-FAIL_TRUE**.
Heuristic was misled by the dialogue-marker text itself (`응답:/사용자:`) which contains
KO chars; substrate emit content remains incoherent (single-char repetition + unicode
garbage).

## Architectural verdict

`FAIL_ALL_TRUE_BY_INSPECTION` — substrate self-feed does **NOT** bypass #115.
Iteration does not improve coherence; it saturates into single-char attractors
(`\x06\x06\x06`, `aaaaaaa`, `eeeee`). Joining BG-AR (logit lens FAIL) +
BG-AS (semantic-bridge FAIL) → **#115 chat-incapability is architectural at every
substrate layer (residual, vocab-bridge, AND iterative-state)**.

## Evidence

### Strategy 1: greedy iterative (5 iter × 10 tok = 50 tok)

```
seed: "안녕"
iter 1: '\x1c\x06\x06\x06\x06\x06\x06\x06\x06\x06'  (incoherent)
iter 2: '\x1c\x06\x06\x06\x06\x06\x06\x06\x06\x06'  (identical)
iter 3-5: identical
final:  '안녕\x1c\x06\x06...\x06\x06'  (single-attractor lock-in)
```

Greedy iteration converges to a token attractor `(0x1C, 0x06×9)` cycle from iter 1;
no coherence emergence over 5 iterations.

### Strategy 2: top-k iterative (k=40, temp=0.7, seed=42)

```
seed: "안녕"
iter 1: '\x1c}\x06\x1c\x1c­­­­­'
iter 2: 'eeeeߙ­\x1c\x1c\x1c­'
iter 3: '­­dhhhhhhh'
iter 4: '­­­­­­­­­­'
iter 5: '­蓓­­­­­'
```

Top-k breaks the greedy attractor but each iteration drifts to a new single-char
saturation (`eeee`, `hhhh`, repeated `­`). No accumulating coherence.

### Strategy 3: dialogue marker (3 iter × 15 tok, `\n응답:/\n사용자:`)

```
seed: "안녕"
iter 1 (substrate): '­鑑­­­­­­­­­­­­­'
iter 2 (substrate): 'aaaaaaaaaaeeeee'
iter 3 (substrate): 'aaaaaaaaaaaaaaa'
final assembled: "안녕\n응답:...\n사용자:\n응답:aaaa...\n사용자:\n응답:aaa...\n사용자:"
```

The substrate **does not switch register** when dialogue markers appear —
it ignores `\n응답:` cue and continues into single-char saturation. Final
"text" passes the KO/ASCII heuristic only because the MARKERS themselves
contain `응답`, `사용자` (4 KO chars × 3 turns = 12 KO chars, max-char-freq
< 50% due to char diversity in markers); the substrate's own content
contributes only `a`/`e`/`­` repetition.

## Iteration-coherence trajectory

| strategy  | iter 1 | iter 2 | iter 3 | iter 4 | iter 5 | trend          |
|-----------|--------|--------|--------|--------|--------|----------------|
| greedy    | FAIL   | FAIL   | FAIL   | FAIL   | FAIL   | locked attractor |
| topk      | FAIL   | FAIL   | FAIL   | FAIL   | FAIL   | wandering attractors |
| dialogue  | FAIL   | FAIL   | FAIL   | —      | —      | marker-ignored |

**No improvement, no saturation-toward-coherence; only saturation-toward-noise.**

## Joining BG-AR + BG-AS + BG-AW

| Probe                               | BG    | Verdict | Implication                          |
|-------------------------------------|-------|---------|--------------------------------------|
| Logit lens (intermediate residual)  | BG-AR | PASS-1L | Coherent only at L10/16 (transient)  |
| Semantic-bridge (cosine NN to vocab)| BG-AS | FAIL    | Final hidden does not align to vocab |
| Self-feed (iterative dialogue)      | BG-AW | FAIL_TRUE | Iteration saturates to single-char  |

#115 is **NOT** a sampling/decode layer artifact. CLM v4's residual stream carries
*some* semantic content at L10 but it does NOT survive ln_f → lm_head, AND the
iterative input feed does NOT recruit additional coherence over time.

## Honest C3 (5)

- C1 — mac CPU fp32, deterministic greedy + seeded topk (manual_seed=42)
- C2 — self-feed input distribution differs from train-time data; OOD drift expected as
  cumulative text grows. Cannot distinguish "substrate cannot dialogue" from "self-feed
  is OOD"; broader OOD investigation requires training-distribution matched seeds.
- C3 — dialogue markers `\n응답:` / `\n사용자:` train-time presence unknown. If absent,
  the marker tokens themselves are OOD and explain marker-ignored behavior; if present,
  ignored-marker is true #115 evidence.
- C4 — single seed `안녕` (1 KO greeting). 1-prompt × 3-strategy result; n_coherent
  heuristic (KO/ASCII >=5 + max-freq <=50%) was misled by repeated marker text in
  dialogue strategy — verdict.json shows PASS but inspection-FAIL_TRUE.
- C5 — sister-import from BG-Q helper for model+tokenizer load (READ-ONLY); raw#15
  additive (mount/shim/dialogue_load 무수정); raw#37 transient_py namespace; raw#10
  honest C3 emitted. No commit, no secret leak.

## Deliverables

- `tool/transient_py/anima_emerge_chat_self_feed.py` (helper, gitignored)
- `state/anima_emerge_chat_self_feed_2026_05_05/aggregate.json`
- `state/anima_emerge_chat_self_feed_2026_05_05/verdict.json`
- `docs/anima_emerge_chat_self_feed_landed_2026_05_05.ai.md` (this doc)

## Cost + wall

- $0 (mac CPU)
- ~3.3 min wall (load 13.8s + greedy 57.3s + topk 91.6s + dialogue 39.8s)

## Next-step recommendation

**Stop probing CLM v4 for chat capability.** BG-AR + BG-AS + BG-AW form a complete
substrate-layer falsification triplet:
- residual content insufficient (BG-AR)
- vocab-bridge degenerate (BG-AS)
- iterative-state non-recruiting (BG-AW)

#115 chat-incapability is architectural at every measurable substrate layer.
Aligns with feedback memory `clm_v4_lora_sft_chat_lift_falsified_substrate_safe`
(F-CLM-LORA-2 FAIL_REGRESSION -36.298pp) and Pβ chat-cap closure
(`pbeta_chat_capability_fail_substrate_research_pass_decoupled`).

Chat-capability hope: Llama Path A v2 winner (already PASS). CLM v4 = substrate-
research only.
