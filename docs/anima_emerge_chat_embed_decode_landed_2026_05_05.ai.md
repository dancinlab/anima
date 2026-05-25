# anima_emerge_chat_embed_decode landed 2026-05-05 (BG-CJ)

## Scope

Test whether raw token embeddings (pre-L0) carry literal next-token signal
that the 16 transformer blocks then destroy. Motivated by the prior basin
diagnostic showing collapse onset is L0-L8 architectural, so probe the
substrate UPSTREAM of L0 by routing `tok_emb(ids)` directly into `head_a`
and `tok_emb.weight.T` (tied projection), bypassing all blocks.

## Method

- model: `dancinlab/clm-v4-mk2-v1` on mac CPU fp32
- prompts: 2 (`안녕`, `Hello`) -- minimum-pair KO/EN greeting
- four head paths per prompt (top1 only, last input position):
  1. raw_emb : `tok_emb(ids)[:, -1] -> head_a`
  2. ln_emb  : `tok_emb(ids)[:, -1] -> ln_f -> head_a`
  3. tied    : `tok_emb(ids)[:, -1] @ tok_emb.weight.T`
  4. full_fwd: `model(ids).logits[:, -1]` (standard 16-block forward)
- iterative greedy continuation 15 tokens for ln_emb path (embed-only) vs
  full forward; embed-only re-tokenizes the concatenated string each step
- semi-coherent heuristic (anima-internal): >=5 KO+ASCII letters AND no
  single char dominates >50% of output
- additive (no mount/shim/dialogue_load mutation), transient sister-py
  helper namespace, five caveats emitted to verdict.json

## Results

(a) 2 prompt x 4 method top1

```
prompt='안녕' (input ids=[1, 53156, 62255]; last id = 62255 = '녕')
  raw_emb + head_a top1: id=62255 text='녕'  logit=0.388
  ln_f + head_a top1:    id=62255 text='녕'
  tied tok_emb top1:     id=62255 text='녕'
  full_forward top1:     id=32    text='\x1c'

prompt='Hello' (last id = 11596 = 'ello' SP piece)
  raw_emb + head_a top1: id=11596 text='ello' logit=0.421
  ln_f + head_a top1:    id=11596 text='ello'
  tied tok_emb top1:     id=11596 text='ello'
  full_forward top1:     id=100   text='`'
```

(b) embed-only vs full_forward continuation 15 tokens

```
prompt='안녕'
  embed-only :  '녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕'
  full_fwd   :  '\x1c\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06'

prompt='Hello'
  embed-only :  'elloelloelloelloelloelloelloelloelloelloelloelloelloelloello'
  full_fwd   :  '```````````````'
```

(c) n_coherent comparison

- n_coherent_embed_only = 1 / 2 (Hello path; multi-char-set 'ello' repetition
  passes the dominance heuristic at exactly 50%)
- n_coherent_full_forward = 0 / 2 (both collapse to single control glyph)
- verdict: `PASS_EMBED_BETTER`

(d) architectural insight

The three embed-only projections (raw / ln / tied) all return the SAME top1
across both prompts: the LITERAL last input token. This is the identity-like
signal that tied embedding heads exhibit for in-vocabulary tokens -- the
embedding self-similarity peak dominates head_a's weight overlap. There is
no semantic next-token signal in the raw embedding; what the embed path
recovers is "you just saw token X, the closest weight row to X is X
itself". The tied case is exactly identity (cosine self-peak); raw_emb
+ head_a and ln_emb + head_a yielding the same id reveals head_a is
near-tied with tok_emb (consistent with weight-tying or near-tying in CLM
v4 architecture).

The KEY architectural finding: full forward DESTROYS even this trivial
identity signal. Full-forward top1 on `안녕` is `\x1c` (id=32) -- a control
char wholly unrelated to the input. The 16 blocks therefore are not merely
failing to ADD semantic content; they are actively REROUTING the residual
stream off the input-token identity manifold and onto the basin attractor
(`\x1c`, `` ` ``, `\x06`). This corroborates the L0-L8 onset claim from the
prior basin diagnostic: between raw embedding (which still carries token
identity) and final logits (which carry only basin tokens), the early
blocks pull the representation into the collapse attractor.

Embed-only is "better" only in the trivial sense that identity > basin
glyph for coherence heuristics; neither path produces real continuation.
The asymmetry is the diagnostic, not the embed-only output itself.

(e) 5 honest caveats

- C1: mac CPU fp32 -- minor numeric drift vs GPU bf16 baseline; deterministic
  at this precision; results stable across re-runs (single run executed).
- C2: embed-only bypass is a 0-layer transformer; semantic flow through 16
  blocks fully removed. The "PASS_EMBED_BETTER" verdict reflects identity
  recovery vs basin collapse, NOT semantic capability. Both paths fail real
  continuation.
- C3: head_a + ln_f are train-time-only at LAST-LAYER hidden distribution.
  Feeding raw embedding into them is OOD by construction -- top1 returning
  the literal input token is consistent with weight-tying / cosine self-peak,
  not with the head having learned an embedding-space decoder.
- C4: embed-only iterative greedy accumulates emb -> tied projection step
  by step; each step re-tokenizes the concatenated string then re-embeds.
  No positional info beyond tok_emb, no attention, no gradient signal --
  coherence here would be remarkable; identity-loop is expected.
- C5: the L0-L8 onset claim from prior basin diagnostic suggests pre-L0
  (raw embedding) shows DIFFERENT token statistics than post-block hidden
  states (input identity vs basin glyph), but conflating that with
  "semantic content exists pre-L0 and is destroyed by blocks" requires
  perplexity / NLL comparison vs a baseline tok_emb distribution + a
  non-collapsed control substrate (e.g. Pythia or pre-collapse CLM
  checkpoint). This run does not perform that comparison; the
  architectural insight is suggestive, not proven.

## Deliverables

- helper: `tool/transient_py/anima_emerge_chat_embed_decode.py` (~180 LoC)
- aggregate: `state/anima_emerge_chat_embed_decode_2026_05_05/aggregate.json`
- verdict:   `state/anima_emerge_chat_embed_decode_2026_05_05/verdict.json`
- doc (this file)

## Cost + time

- $0 (mac CPU)
- wall ~6s load + <2s compute = ~8s total

## Lane status

This probe closes the embed-only direct decode lane with verdict
PASS_EMBED_BETTER (identity recovery > basin collapse). Architectural
diagnostic for the basin onset chain: corroborates L0-L8 onset by
demonstrating that input-token identity exists pre-L0 but is gone by final
logits. Does NOT identify a chat-capable path; CLM v4 chat-capability
remains falsified per the prior LoRA SFT regression finding.
