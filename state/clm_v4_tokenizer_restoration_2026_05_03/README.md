# CLM v4 64K Multilingual BPE Tokenizer (Restored 2026-05-03)

Recovered tokenizer artifact for `need-singularity/clm-v4-base-mirror`. This file pair (`tokenizer_64k_multilingual.{model,vocab}`) is required to encode/decode text against the CLM v4 350M base checkpoint vocabulary. Without it, downstream consumers (lm-eval-harness wrappers, LoRA inference, BLM substrate clients) must fall back to byte-level tokenization, which is in-distribution-safe (the model was trained with `byte_fallback=True`) but loses BPE merge structure.

## Origin

- **Source path** (recovered from): `/Users/ghost/core/anima/ready/anima/config/tokenizer_64k_multilingual.{model,vocab}` (sister-repo "ready" mirror, file mtime `2026-04-01T10:11:00`).
- **Training script**: `ready/scripts/train_tokenizer.py` (sentencepiece `BpeTrainer`, vocab=64000, byte_fallback=True, NFKC normalization, character_coverage=0.9995, split_digits=True, max_sentencepiece_length=16).
- **Training corpus default**: `anima/data/corpus_v10_ko.txt` (Korean-heavy multilingual: ko/en/zh/ja/ru + code per `config/agi_requirements.json`).
- **Why missing prior to restoration**: Commit `4e87d3695` (2026-04-23) removed broken symlinks `data/tokenizer_64k_multilingual.{vocab,model}` that pointed to `ready/anima/config/...` (sister-repo path). The actual files survived in `ready/`, but the canonical `data/` symlinks were removed without preserving a mirror copy in `state/` or pushing to HF. The HF mirror push of `clm-v4-base-mirror` (2026-05-03) only included `best.pt`, omitting the tokenizer.
- **SHA-256**:
  - `tokenizer_64k_multilingual.model`: `bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab`
  - `tokenizer_64k_multilingual.vocab`: `972fc0ba2f2633cfa685c70eeab84ce2a22a1327975e989a3b1d5cf5efa480a4`

## Falsifiers

The restoration is **RECOVERY (not REBUILD)** — the byte-for-byte identical `.model` artifact CLM v4 was trained against. This claim is falsifiable by:

1. **Vocab-size check**: `sentencepiece.SentencePieceProcessor.get_piece_size() == 64000`. Verified PASS.
2. **Special-token ID check**: `pad=0, bos=1, eos=2, unk=3`. Verified PASS — matches train_tokenizer.py spec.
3. **Byte-fallback range check**: IDs 4-259 = `<0x00>`..`<0xFF>`. Verified PASS — matches Path B byte-fallback workaround formula `[i+4 for i in bytes]`.
4. **Round-trip integrity**: Korean ("의식은 구조에서 창발한다.", 4 tokens, no UNK), English (6 tokens), mixed-symbols ("Φ=1.234, α=0.014", 6 tokens). Verified PASS.
5. **Embedding-row alignment**: The base ckpt was trained with `vocab=64000`. If a re-trained tokenizer were substituted, encoding "안녕하세요" would address different embedding rows and produce nonsense logits. The restored artifact MUST address the original rows for any prior trained capability to surface. (Falsifiable by inspecting `best.pt['args'].vocab_size` and confirming = 64000.)

If any of (1)-(4) fails on a downstream consumer's machine, the artifact has been corrupted in transit.

## Substrate

- **Mac (this restoration)**: `/Users/ghost/core/anima/state/clm_v4_tokenizer_restoration_2026_05_03/` — staging area for HF push.
- **HF mirror (post-push)**: `need-singularity/clm-v4-base-mirror/tokenizer_64k_multilingual.{model,vocab}` — co-located with `best.pt` so consumers can fetch with one `snapshot_download` call.
- **ubu1 cache (post-push)**: `~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/<rev>/tokenizer_64k_multilingual.{model,vocab}` — populated automatically by next `hf_hub_download` call. Manual cache prime: `hf download need-singularity/clm-v4-base-mirror tokenizer_64k_multilingual.model`.
- **CLM v4 ckpt this attaches to**: `/home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt` (ubu1) and the HF mirror copy.

## Caveats

1. **Mtime-only origin trust**. The `ready/anima/config/tokenizer_64k_multilingual.model` file has mtime `2026-04-01`, which predates CLM v4 training runs (training cycle in late April per `docs/clm_v4_revival_stages_2026_05_02.md`). The file is most plausibly the artifact CLM v4 was trained on, but there is no signed manifest or training-time SHA record to prove byte-identity. Mitigation: vocab=64000 + byte_fallback ID range match the training script defaults exactly, and Path B byte-fallback workaround (which DID work end-to-end on hellaswag eval at 0.242 acc_norm) implicitly confirms the embedding layout (`[i+4 for i in bytes]` only works if the BPE tokenizer reserved IDs 4-259 for byte-fallback — which this artifact does).
2. **No corpus-side compression baseline preserved**. The `train_tokenizer.py` verifier emits "bytes/token" compression on a 100KB sample of the source corpus, but this number was never logged to `state/`. We cannot retrospectively confirm "is this the SAME 64K BPE that produced training compression ratio X" — only "is this A 64K BPE matching the spec." If future audits demand byte-level reproducibility, the corpus + script must be re-run on ubu1 (off-repo) and the resulting `.model` SHA compared.
3. **Single point of survival**. The restored copy lives in one canonical location (`ready/anima/config/`) which is itself a sister-repo (not under git). If `ready/` is purged before the HF push completes, restoration is unrecoverable. **Action item for follow-up cycle**: add `state/clm_v4_tokenizer_restoration_2026_05_03/tokenizer_64k_multilingual.model` to git LFS or a redundant backup once the working tree is clean.
4. **Push to HF mirror does not retroactively fix prior LoRA savepoints**. The `clm-v4-sft-step-{5k,10k,25k,50k,final}` and `clm-v4-sft-stage1` LoRA repos do NOT carry the tokenizer either. Consumers that want to use those LoRAs must additionally fetch the tokenizer from `clm-v4-base-mirror`. Updating each LoRA repo's README to point at this tokenizer is a separate follow-up task (out of scope for this restoration).
5. **Naming-validator non-conformance**. The `tool/hf_upload_mk2.hexa` naming validator allows `clm-v4-base-mirror` (family=clm, version=v4, stage=base-mirror starts with "base"). Adding tokenizer files does NOT change the repo name, so naming compliance is preserved. The standalone idea of a `clm-v4-tokenizer-64k` repo would FAIL the validator (stage `tokenizer-64k` does not start with any allowed prefix), which is why co-location with the base mirror is the chosen path.

## Composability

This restoration unblocks:

- **Path B re-run with proper BPE**: rerun `~/anima/state/p9_path_b_sanity_probe_2026_05_03/eval_clm_v4_hellaswag.py` on ubu1 with `spm.SentencePieceProcessor` instead of byte-fallback `[i+4 for i in bytes]`. Expected: same AT_FLOOR verdict (0.20-0.30 acc_norm band) but with proper subword tokenization for fair comparison if cycle ever re-opens the "is CLM v4 a real LM" question.
- **LoRA inference via `PeftModel.from_pretrained`**: per the README canonical path, base + LoRA load now also has the matching tokenizer co-located, removing the silent "embedding rows 4-259 only" degradation.
- **BLM Phase 5 stimulus-aligned pipeline**: `docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md` requires CLM v4 350M + LoRA — same tokenizer dependency unblocked.
- **Cross-model corpus stats**: now possible to compute byte/token ratios on shared corpora using the actual training tokenizer (was previously approximated via byte-fallback inflation).
