# F-CURRICULA-1 — pod-death recovery (2026-05-25)

**verdict: re-fire LOST at step 3000/5000 · pod `wfeksdl8e8f327` terminated ·
artifacts unrecoverable · NOT a mission loss (wiki=1.0 endpoint already a
published closed-negative).**

This is a SEPARATE event from the `c25njysjdga2vb` dispatcher-class-1 failure
documented in this dir's `README.md` (that pod NEVER trained). This file
covers the SECOND F-CURRICULA-1 attempt — pod `wfeksdl8e8f327`, which DID
train (to step 3000) before dying.

## Fire identity

- pod `wfeksdl8e8f327`, 1× A100 SXM, $1.49/hr, `SAVE_POD=1`
- variant: Qwen2.5-1.5B, init=qwen, seed=1337, steps=5000, lr=5e-5, bsz=2,
  block=512, warmup=100, noise-sigma=0.1, lambda-mitosis=0.05,
  mitosis-max=16, **wiki-frac=1.0** (curriculum-mix re-fire)
- corpora: multi_wiki + corpus_s101 + mixed_corpus_built (anima_records=1,
  wiki_frac_actual ≈ 1.0 — effectively pure-wiki)

## Timeline (this monitor session)

| UTC | step | CE | note |
|-----|------|-----|------|
| 16:27 | 1375 | 2.99 | re-poll start (dispatcher PID 412255 dead) |
| 16:43 | 1500 | — | ja_ja anchor written |
| 16:55 | 1750 | 3.15 | |
| 17:31 | 2250 | 3.57 | |
| 17:43 | 2375 | 2.38 | **best** ckpt saved |
| 17:55 | 2500 | — | ru_ru anchor |
| 18:31 | 3000 | — | ko_ko anchor · **LAST GOOD POLL** |
| 18:43 | — | — | SSH port 15857 **Connection refused** (DEAD) |

The run was CPU-bound throughout (GPU 1-2% util despite `device=cuda`
+ 25GB resident) — dataloader/mitosis path starved the A100, giving a
slow ~4.6 s/step. It was alive and converging (best CE 2.38) when it died.

## Death diagnosis

- Host `154.54.102.24` PINGS (0% loss, 184ms) but **port 15857 REFUSED**
  → container stopped/terminated (proxy host up, pod port gone).
- `runpodctl pod list -a` = `[]` under the only working key
  (secret-store `rpa_43SES1…`, 50-char). Both config-file keys (Mac +
  ubu-2, 52-char `rpa_43SES…`) return **401**.
- `hexa cloud` = transport-only (no list verb). No way to enumerate or
  reach the pod's volume.
- **Conclusion**: pod gone, on-pod artifacts (ckpt_best, ckpt_step500..3000,
  anchors) unrecoverable. No mid-ckpt pull possible.

## Why this is NOT a mission loss

The lost variant is the **wiki_frac=1.0** extreme of the PURE corpus-axis
sweep. That endpoint is ALREADY closed-negative and published:
`dancinlab/anima-v3-e3` (PUBLIC, wiki=1.0) + CLAIMS.tape `pure_wiki_sweep`.
F-CURRICULA-1 only re-ordered the SAME pure-wiki corpus (curriculum mix);
breaking the register/coherence ceiling from a pure-wiki corpus alone was
the very thing the closed-negative says cannot happen. At step 3000 it was
tracking the same WEAK-coherence trajectory (CE ~2.4-3.6, no qualitative
shift), so the run was on course to reinforce — not overturn — the
closed-negative.

## What WAS recovered (the wiki_frac=0.3 sibling)

A fully-completed, byte-exact **wiki_frac=0.3** P21H V3 run already existed
locally at `../p21h_v3_recover_2026_05_25/out_main/` (step 5000, recovered
earlier from a SIGHUP-orphaned pod, never HF-uploaded). This effort:

1. byte-exact verified both ckpts vs MANIFEST.sha256 (✓ match)
2. ran `closure_auto_judge.hexa` → **1/4 PASS · closure FAIL** (verbatim in
   `closure_verdict_wiki03_verbatim.txt`): criterion-2 register_collapse
   PASS (0 hits), criteria 1/3/4 FAIL (all 5 langs WEAK; motivation +
   dream_stage blocks absent in this result schema).
3. HF-uploaded tier-gated **PRIVATE** (FAIL → private per `a_hf_autonomous`):
   `dancinlab/anima-p21h-v3-wikifrac03-recovered-2026-05-25` — 2× 6GB ckpt
   + result/eval/heldout JSON + 15 kosmos anchors + manifest + model card.

This adds the **wiki_frac=0.3** data point to the corpus-axis closed-negative
(register collapse blocked at wiki=0.3 yet coherence stays WEAK across all 5
langs — same as wiki=0.5 / wiki=1.0). Corpus-axis ⊥ multilingual closure,
now confirmed at THREE sweep points (0.3, 0.5, 1.0).

## Teardown

No teardown action possible/needed — pod already self-terminated and is
invisible to the working API key. The stale config-file key (401) should be
re-synced from the secret-store SSOT; filed to hexa-lang inbox.

## Cost

- `wfeksdl8e8f327`: ~6.4h × $1.49 ≈ **$9.5** (trained to 60%, lost) +
  earlier `c25njysjdga2vb` $3.92 (no-train) = ~$13.4 sunk on F-CURRICULA-1.
- Net new knowledge from the recoverable wiki=0.3 run: $0 (already trained).
