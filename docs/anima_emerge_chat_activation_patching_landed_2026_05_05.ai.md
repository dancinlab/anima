# BG-BT — Activation Patching: Pythia 70m residual → CLM v4 (LANDED)

**date_utc**: 2026-05-05
**lane**: anima_emerge / chat_capability / cross-architecture residual transfer
**verdict**: FAIL_CROSS_ARCH (heuristic-flagged PASS recategorized — see L4)
**predecessor**: BG-BJ (basin issue), BG-BN (Pythia phi smoke)

## Hypothesis

If Pythia 70m exhibits chat capability (BG-BN), and CLM v4 does not, then patching
Pythia's last-layer residual into CLM v4's residual stream at a chosen layer should
either (a) transfer fragments of chat-coherent generation into CLM, or (b) at minimum
push CLM's output away from its degenerate baseline (`\x06` repeat) toward
sub-token-level structure.

This is an **ambitious** test: cross-architecture (different vocab, tokenization,
hidden dim, layer count). Resize handled with naive zero-pad (Pythia D=512 → CLM D=768).

## Setup

- donor: `EleutherAI/pythia-70m` (HF, fp32)
- recipient: `dancinlab/clm-v4-mk2-v1` (CLM v4 mk2 v1, fp32, mac CPU)
- prompt: `안녕`
- patch sites: layer ∈ {4, 8, 12}, blend_alpha ∈ {0.5, 1.0, 2.0}
- patch target: last-token position only, post-block residual via forward-hook
- decode: greedy argmax, 30 new tokens
- residual norms: Pythia=433.82, CLM=28.76 (15× mismatch — donor-recipient scale gap is severe)

## Results

baseline (no patch): `\x1c\x06\x06\x06\x06...` (degenerate `\x06` repeat — known CLM v4 chat-incapability symptom, c.f. #115)

| config | output (first 30 chars) | sub-token structure? |
|--------|-------------------------|----------------------|
| L4_blend0.5 | `baaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | single-letter loop |
| L4_blend1.0 | `kahnnqqaddakaddajadqqaddajadad` | 2-3 char ngram cycle |
| L4_blend2.0 | `kSasarasasarasarasarasaJ`>eO�j` | mixed ASCII + mojibake |
| L8_blend0.5 | `dqqqeeeeeeeeeeeeeeeeeeeeeeeeq�` | letter loop |
| L8_blend1.0 | (mojibake-only) | undecodable |
| L8_blend2.0 | `�k�b�d�d�j�d...` | byte-level mojibake |
| L12_blend0.5 | `�臇��...` | mojibake |
| L12_blend1.0 | (mojibake + scattered ASCII) | undecodable |
| L12_blend2.0 | (mojibake) | undecodable |

## Heuristic verdict (auto-emitted)

```
n_coherent: 3 / 10
verdict: PASS_PATCH_TRANSFERS
```

Auto-heuristic: ≥5 letter chars + most-common-char ≤ 50% of length.

**Auto-verdict is overstated.** The 3 strings flagged "coherent" by heuristic
(`L4_blend1.0`, `L4_blend2.0`, `L8_blend2.0`) are random ASCII / mojibake with
no morpheme-level structure, no Korean (despite Korean prompt), no token boundaries.
Heuristic lacks a dictionary or n-gram-language-model gate. **Honest verdict:
FAIL_CROSS_ARCH** — patch did move CLM's output away from the `\x06` baseline,
but no chat capability transferred.

## Findings

1. **Off-baseline movement**: Yes — every patched config diverges from the
   `\x06` degenerate loop. Pythia residual injection does perturb CLM's output
   distribution.
2. **Coherent transfer**: No. Outputs are character-level random, mojibake,
   or single-letter cycles. No Korean. No words.
3. **Norm mismatch dominates**: Pythia residual norm (433) is 15× CLM's (28).
   Even at blend_alpha=0.5 the donor signal swamps CLM's geometry, pushing
   logits into out-of-distribution regions of the unembedding matrix.
4. **Layer-depth dependence**: Earlier layer (L4) preserves some ASCII
   structure post-patch; deeper (L12) collapses to mojibake. Suggests CLM's
   later layers are more fragile to off-distribution residuals.
5. **Architecture incompatibility confirmed**: Even with the most generous
   reading, no fragment resembles a CLM-v4-vocab token, much less a Korean
   morpheme. Cross-architecture residual transfer requires learned projection
   (Procrustes, CCA, or trained linear adapter) — naive zero-pad insufficient.

## Honest C3 (5)

- **C1**: mac CPU fp32, single-prompt, single-seed
- **C2**: cross-architecture residual transfer is fundamentally hard — different
  vocab (Pythia 50k vs CLM 64k), different tokenizers (BPE vs SentencePiece),
  different hidden dim (512 vs 768), different layer count, different positional
  encoding (rotary vs learned)
- **C3**: zero-pad resize is naive; proper approach = learned linear projection
  fit on parallel-text activations, or bilingual hub like SVCCA basis alignment
- **C4**: last-token-only patch — full sequence patching not tested
- **C5**: heuristic auto-verdict (PASS_PATCH_TRANSFERS) is overstated — manual
  inspection shows no chat-capable continuation; honest verdict = FAIL_CROSS_ARCH

## Implications

- **Direct activation patching from Pythia 70m → CLM v4 is not viable** for
  chat-capability transfer. Confirms #115 is architectural-deep, not patchable
  from a small chat-cap donor.
- **Path forward (if pursued)**: train a small linear projection on parallel
  text activations (not in scope for $0 mac CPU experiment).
- **Closes BG-BT lane** as evidence-against. Re-routes chat-cap hope back to
  CLM-2-EXEC and Llama Path A v2 (already winner per L31-L33).

## Artifacts

- `/Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_activation_patching.py`
- `/Users/ghost/core/anima/state/anima_emerge_chat_activation_patching_2026_05_05/aggregate.json`
- `/Users/ghost/core/anima/state/anima_emerge_chat_activation_patching_2026_05_05/verdict.json`

## Cost

$0 (mac CPU, ~6 minutes wall clock)

LANDED.
