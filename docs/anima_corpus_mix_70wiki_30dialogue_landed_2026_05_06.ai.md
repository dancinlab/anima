# anima-clm-3 corpus_mix 70wiki+30dialogue PATH-B local assembly — LANDED 2026-05-06

## Status
LANDED — mac local build complete; SCP + HF upload recipes emitted; awaiting user confirm for actual transfer.

## Summary
- **Trigger**: BG-FE failed (600s watchdog stall during HF 401 pivot). BG-FE2 refire on PATH-B local assembly.
- **Spec anchor**: `docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md` §3.3 (lines 142, 183, 246-250)
  - Line 142: "70% wiki + 30% dialogue (AL4-balance, lifted from AnimaLM v8 §2.2)"
  - Line 183: "corpus mix | 70% wiki + 30% dialogue (2-bucket, AL4 balance)"
  - Lines 246-250: detailed bilingual breakdown
- **Build path**: PATH-B-1 (simple concat). PATH-B-2 (interleave) skipped — DataLoader shuffle=True at train time auto-recovers interleave effect; concat is faster + lower failure surface + reproducible.

## Sources (mac local)
| role | path | lines | bytes |
|---|---|---|---|
| wiki (70%) | `ready/anima/data/corpus_v6_wiki.txt` | 2,141,063 | 109,119,637 |
| dialogue (30%) | `ready/anima/data/corpus_v8_dialogue.txt` | 917,598 used / 2,144,933 total | partial |

Alternates rejected: corpus_v7_wiki_heavy (near-dup of v6), wikimatrix (smaller 305K lines), ko_wiki (28K lines too small).

## Output
- **Path**: `state/anima_corpus_mix_70wiki_30dialogue_2026_05_06/corpus_mix.txt`
- **Lines**: 3,058,661
- **Bytes**: 154,854,977 (~147.68 MB)
- **SHA256**: `2d15ca7d277aaaef95c7dbc9eb810ec38f0510e0578269810aa4eb879f51e0e8`
- **Ratio actual**: 70.0000% wiki / 30.0000% dialogue (line-anchor, drift = 0.0 pp)
- **Git status**: IGNORED (own 14: corpus >5MB → HF only)

## Recipes Emitted
- `state/anima_corpus_mix_70wiki_30dialogue_2026_05_06/build_recipe.bash` — reproducible local rebuild
- `state/anima_corpus_mix_70wiki_30dialogue_2026_05_06/scp_recipe.txt` — mac → ubu1 transfer
- `state/anima_corpus_mix_70wiki_30dialogue_2026_05_06/hf_upload_recipe.txt` — HF Hub PRIVATE upload (own 15 lifecycle)

## 5+ Honest C3 (raw#10)
1. **C3-1 (concat ordering)**: wiki block first then dialogue block; if ubu1 trainer disables DataLoader shuffle, dialogue starvation in early steps. Mitigation: confirm shuffle=True on launch.
2. **C3-2 (footer overlap)**: v6_wiki and v8_dialogue share an identical Wikipedia footer. <0.1% duplicate lines across the two blocks.
3. **C3-3 (multilingual drift)**: v8 dialogue includes JP/ZH beyond spec's KO+EN target. Byte-level tokenizer absorbs UTF-8 fine; KO+EN proportion inside the 30% slightly diluted.
4. **C3-4 (license-filter inheritance)**: spec §3.3 says "license-filtered" — this build inherits whatever filter existed in upstream `corpus_v6` generator; no additional pass at this build stage.
5. **C3-5 (line-ratio vs byte-ratio)**: line-ratio is exact 70.00/30.00, but byte-ratio is ~70.5/29.5 (dialogue lines avg shorter). Line-ratio anchors training-sample boundary semantics; acceptable drift.
6. **C3-6 (AL4 reproduction parity)**: build is NOT byte-for-byte identical to AnimaLM v8 §2.2 AL4-balance — those upstream corpora unavailable on this Mac. This is a v8-style approximation using anima `ready/data` sources.
7. **C3-7 (no shuffle in mix)**: file written deterministic top-to-bottom. Reliance on trainer-side shuffle for mixing (C3-1 dependency).

## Next Steps (user confirm gate)
1. **User confirms** recipes acceptable.
2. **anima session** executes `scp_recipe.txt` mac → ubu1.
3. **anima session** executes `hf_upload_recipe.txt` PRIVATE upload to `need-singularity/anima-clm-3-corpus-mix-70wiki-30dialogue`.
4. **Verification gates** (sha256 match across mac/ubu1/HF) before public flip.
5. ubu1 CLM-3-original trainer points at `/home/aiden/core/anima/data/corpus_mix_70wiki_30dialogue.txt`.

## Cost
- $0 (mac local; no network).
- ~25 tool uses, well under budget.
- ~5 min wall (well under 30 min target).

## Lessons (carry forward)
- BG-FE2 succeeded where BG-FE stalled because PATH-B avoided HF probe entirely (BG-FA had already closed that path).
- Local assembly with `wc -l` anchor + `head -n N` is deterministic + emit-friendly; no watchdog stall.
- Spec doc grep before build = fast confirmation of 70/30 anchor without full read.
