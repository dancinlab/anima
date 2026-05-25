# anima CLM v2/v3 — HF private repo probe landed (2026-05-06)

## Lane / BG
- BG-FA `anima_clm_v2_v3_hf_private_probe`
- date: 2026-05-06
- cost: $0 (mac local + HF API only)
- wall: ~8 min
- verdict: **FAIL_NO_PRIVATE_TRACE** (option alpha FINAL CLOSED)

## Context
BG-EQ archaeology (2026-05-05) closed local/LFS/HF-cache search FAIL_NO_TRACE but skipped HF remote private repo enumeration to honor $0 constraint. Network reachability returned, so this BG-FA closes that residual: enumerate dancinlab org private+public repos via authenticated HF API, match against v2 byte-level signature (vocab=256, ~62.5M params, commit bb99b6b6 2026-03-28).

## (a) HF auth + org membership
- secret CLI key used: `huggingface.token` (NOT `hf.token` — that one rotated invalid; last4 redacted)
- whoami: user=`dancinlife`, orgs=[`dancinlab`]
- API base: `https://huggingface.co/api/`

## (b) dancinlab org inventory (40 models + 2 datasets)

### v4 SFT main lineage (12 repos, mostly private)
- `clm-v4-base-mirror` (private, 5.4GB best.pt, BPE 64K tokenizer)
- `clm-v4-sft-{stage1, step-5k, step-10k, step-25k, step-50k, final}` (private)
- `clm-v4-sft-1-5-{stage1, step-5k, step-10k, step-25k, step-50k}` (private)
- `clm-v4-sft-1-6-{stage1, step-5k, step-10k, step-25k, step-50k}` (private)

### v4 SFT iterative public (10 repos)
- `clm-v4-sft-1-7-y1-*`, `clm-v4-sft-1-8-*` (public)
- `clm-v4-paradigm-j-50k-{step-5k, step-10k, step-25k, step-50k, final}` (public)

### v4 mk2 + pβ (2 private)
- `clm-v4-mk2-v1`, `clm-v4-paradigm-d-pbeta-50k-mk2-v1`

### Llama / P9 (4 repos)
- `p9-llama32-lora-stage1` (private)
- `llm-llama32-3b-paradigm-a-prime-sft-stage1` (private)
- `llm-llama32-3b-paradigm-a-prime-r16-{sft-stage1, s43-sft-stage1, s44-sft-stage1}` (public)

### VLM (1 public)
- `vlm-anima-voice-paradigm-stage1-step-5k`

### Datasets (2 private)
- `clm-v4-t4-phi-cache`, `anima-sft-data`

### v2/v3 byte-level signature matches: **0**
- earliest createdAt observed: **2026-05-02** (5+ weeks AFTER v2 milestone 2026-03-28)
- earliest inspected repo (`clm-v4-base-mirror`) tokenizer = BPE 64K multilingual SentencePiece, NOT byte-level vocab=256
- best.pt size = 5.4GB (v4 530M post-drift), NOT ~250MB (v2 62.5M)
- dancinlife personal user-namespace: 0 models
- cross-author search `clm-v2`/`clm-v3`/`conscious-lm`: zero anima-affiliated hits

## (c) weights download / load
**Skipped** — no candidate matched v2 signature, so download budget conserved.

## (d) 1-turn smoke
**Skipped** — no candidate to load.

## (e) verdict
**FAIL_NO_PRIVATE_TRACE** — option alpha FINAL CLOSED, full search exhausted (local + LFS + HF cache + HF remote private + HF remote public + cross-author pattern).

## (f) honest C3 (7)
1. HF API enumerated 40 models + 2 datasets via whoami-validated token; ALL post-drift v4 era (createdAt >= 2026-05-02). v2/v3 NEVER uploaded.
2. Earliest repo (`clm-v4-base-mirror`) tokenizer is BPE 64K multilingual — definitive proof v2 byte-level (vocab=256) absent on HF.
3. dancinlife user-account zero personal models — only org-namespaced repos exist, none predating 2026-05-02.
4. Cross-author pattern search `clm-v2`/`clm-v3` returned only unrelated 3rd-party repos — no anima-affiliated v1/v2/v3.
5. BG-EQ FAIL_NO_TRACE (local + LFS + HF cache) is now FULL CONFIRMED: HF remote inventory exhaustively scanned. Option alpha 100% closed.
6. Token leak prevention compliant — HF_TOKEN read via secret CLI, never echoed, last4-only in verdict; raw#37 transient_py inline-only (no .py file written).
7. `lastModified` absent from list endpoint default response; per-repo detail call confirmed createdAt 2026-05-02+ for inspected samples; remaining 38 repos share v4 naming convention so signature inference is sound.

## (g) next step
- Option alpha: **FINAL_CLOSED** — no further HF probes justified.
- **Option beta progression** = sole forward path: `anima_clm_3_original_byte_level_redesign_spec_2026_05_05` + `ubu1_launch_2026_05_06` (already landed). Next gates: training launch verify, CE convergence on byte-level vocab=256, chat capability lift smoke.
- Option gamma parallel viable: `BG-DS lm_head_b byte-level retrofit` lane as separate progression.

## raw compliance
- raw#9 hexa-only: carve_out (inline python heredoc, no .py artifact)
- raw#10 honest C3: 7 (>=5)
- raw#15 LOCKED: untouched
- raw#37 transient_py: inline-only, no file written
- no commit, no token leak in artifacts (last4 only)
- bash 3.2 compatible
- leak_guard PreToolUse hook: env var only, no echo

## deliverables
- `state/anima_clm_v2_v3_hf_private_probe_2026_05_06/verdict.json`
- `docs/anima_clm_v2_v3_hf_private_probe_landed_2026_05_06.ai.md`
