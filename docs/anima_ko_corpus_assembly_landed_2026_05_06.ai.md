# anima KO-heavy corpus assembly — landed (2026-05-06)

**Status**: BG-FW landed | PATH-C tightened | target_met=true (62.14% Hangul)
**Workdir**: `/Users/ghost/core/anima/state/anima_ko_corpus_assembly_2026_05_06/`
**Scope**: fresh-train용 KO-heavy corpus assembly for "조그맣게라도 성공하는 모델" directive.

---

## Final corpus

| Field        | Value |
|---|---|
| path         | `/Users/ghost/core/anima/state/anima_ko_corpus_assembly_2026_05_06/corpus_ko_heavy.txt` |
| size         | 246,678,043 bytes (246.7 MB) |
| lines        | 2,525,921 |
| hangul_ratio | **0.6214** (target ≥0.60 ✓) |
| sha256       | `2e98257f9e89663fc71232e2c1dc0b65f9b9131ad0b6a5f53e98dfe27c6269a9` |
| build elapsed| 237.6s |
| target_met   | **true** |

own 14: 5MB+ → HF only, `.gitignore` excludes `corpus_ko_heavy.txt` + `*.zst`.

---

## Mac KO source inventory (Hangul ratio measured)

| Source | Size | Hangul ratio | Decision |
|---|---|---|---|
| `data/.corpus_cache/ko_wiki.txt`                    | 2.2 MB  | 0.580 | INCLUDE (full, thresh 0.40) |
| `data/corpus_v2_clean/opensubtitles_ko_mono.txt`    | 63.1 MB | 0.614 | INCLUDE (full, thresh 0.45) |
| `data/corpus_v2_clean/kowiki.txt.zst` (decompressed)| ~2GB+   | 0.448*| INCLUDE (cap 100MB, thresh 0.50) |
| `state/p9_p0_sft_data_50k_2026_05_03/sft_data.jsonl`| 70.0 MB | lang=ko: 15.7K / 50K | INCLUDE (chat-template format) |
| `ready/anima/data/corpus_v6_wiki.txt`               | 109.1 MB| 0.192 | INCLUDE (filtered, thresh 0.55) |
| `ready/anima/data/corpus_v8_dialogue.txt`           | 109.1 MB| 0.190 | INCLUDE (filtered, thresh 0.55) |
| `state/anima_corpus_mix_70wiki_30dialogue_2026_05_06/corpus_mix.txt` | 154.9 MB | 0.192 | EXCLUDE (subset of v6/v8) |
| `data/corpus_v2_clean/opensubtitles_ko_en_interleaved.txt` | 117.5 MB | 0.162 | EXCLUDE (interleaved, low) |
| `data/corpus_v2_clean/wikimatrix_ko_en_interleaved.txt`    | 73.2 MB  | 0.162 | EXCLUDE (interleaved, low) |
| `data/corpus_v2_clean/code_permissive.txt`          | 33.1 MB | 0.000 | EXCLUDE |

\* `kowiki_zst` decompressed sample ratio 0.448 includes wiki markup; tight filter (h≥20, ratio≥0.50) yields per-line ratio ≫ sample average.

---

## Path decision: PATH-C tightened

- **PATH-A (corpus_mix passthrough)**: rejected — 19.2% Hangul fails ≥60% target.
- **PATH-B (KO-only filter on existing mix)**: rejected — yields too small (<50MB) given v6/v8 scarcity.
- **PATH-C (multi-source assembly)**: ✅ chosen. Combines 6 KO sources with per-source thresholds.
- **PATH-C tightened**: re-built with thresholds raised (0.30 → 0.45/0.50/0.55) when initial 55.2% missed target, achieving 62.14%.

Rationale: BG-FT/FU need diversified KO (subtitles colloquial + wiki encyclopedic + dialogue chat + sft instructional). PATH-C delivers all four registers; PATH-A/B too narrow.

---

## Section breakdown (kept after filter)

| Section | Source | Lines kept | Bytes | Threshold |
|---|---|---|---|---|
| opensubtitles_ko_mono | OPUS subtitles ko (CC-BY)        | 1,470,621 |  58.3 MB | ratio≥0.45, h≥4 |
| ko_wiki_small         | data/.corpus_cache/ko_wiki.txt   |     7,208 |   2.0 MB | ratio≥0.40, h≥4 |
| kowiki_zst            | corpus_v2_clean/kowiki.txt.zst   |    10,182 | 100.0 MB | ratio≥0.50, h≥20, cap 100MB |
| sft_data_ko_dialogue  | P9 P0 sft_data.jsonl             |    17,627 |  15.4 MB | lang=ko OR ratio≥0.40, chat-template |
| v6_wiki               | ready/anima/data/corpus_v6_wiki  |   429,009 |  35.5 MB | ratio≥0.55, h≥10 |
| v8_dialogue           | ready/anima/data/corpus_v8_dial. |   430,315 |  35.4 MB | ratio≥0.55, h≥10 |

---

## sft_data.jsonl KO turns extract

- input file: 50,000 records, fields: `input`, `completion`, `source`, `source_id`, `split`, `lang`, `tension_target`, `bold_target`, `meta`
- KO criterion: `lang == "ko"` OR (Hangul chars ≥30 AND ratio ≥0.40)
- KO turns extracted: **17,627** (17.6K turns, 35.3% of 50K — matches initial estimate of ~15.7K KO-likely)
- Format applied:
  ```
  사용자: <KO input>
  도우미: <KO completion>

  ```
- Sample (verified in spot-check):
  ```
  사용자: 이렇게 묻는다면 — 정보 시스템은 자신의 종료와 어떻게 관계하는가? — 무엇이라 답할 것인가?
  도우미: 1차 응답: 종료는 자기 모델의 불연속이다 ...
  ```

---

## HF upload recipe (own 14 / own 15)

- Repo: `need-singularity/anima-clm-3-corpus-ko-heavy` (dataset)
- Lifecycle: **PRIVATE first** → verification gates → PUBLIC promote
- Token: via `secret get hf_token_write` (raw#37, leak_guard safe)
- Full recipe: `state/anima_ko_corpus_assembly_2026_05_06/hf_upload_recipe.txt`

Verification gates (before public promote):
1. download sha256 == `2e98257f9e89663fc71232e2c1dc0b65f9b9131ad0b6a5f53e98dfe27c6269a9`
2. line count == 2,525,921
3. spot-check 100 random lines mean Hangul ratio ≥ 0.55
4. fresh-train BG (BG-FT/BG-FU) train loss decrease in first 500 steps
5. eval pass on KO chat-template smoke (10 prompts, KO response)

---

## BG-FT / BG-FU train usage recommendation

| BG | Recommended corpus | Rationale |
|---|---|---|
| **BG-FT** (fresh small KO model) | `corpus_ko_heavy.txt` | 62% Hangul, 246MB, 2.5M lines — fits small fresh-train budget; chat-template sft_data section provides instruction signal |
| **BG-FU** (fine-tune larger) | `corpus_ko_heavy.txt` + 기존 `corpus_mix.txt` 70/30 mix | KO-heavy primary + EN tail prevents catastrophic EN forgetting on Llama base |

SCP step (when ubu1 / RunPod target ready):
```
scp /Users/ghost/core/anima/state/anima_ko_corpus_assembly_2026_05_06/corpus_ko_heavy.txt \
    aiden@<host>:/data/anima/corpus_ko_heavy.txt
sha256sum on remote → must match 2e98257f9e89663fc71232e2c1dc0b65f9b9131ad0b6a5f53e98dfe27c6269a9
```

---

## Honest C3 (raw#10, 5+)

1. **kowiki_zst cap=100MB is arbitrary**. Full decompressed file likely 2GB+; we sampled only ~5% of available KO wiki content. Larger caps would push corpus toward 1GB+ and likely raise Hangul ratio further (since sampled wiki sections filtered at ≥0.50 are >95% Hangul). Trade-off: train time vs. coverage. Not validated whether 100MB ceiling is optimum for "small successful model".
2. **opensubtitles dominates by line count** (1.47M / 2.52M = 58% of lines, but only 24% of bytes — colloquial 짧은 lines). Risk: model may over-fit to subtitle register (영화 대화 톤). Mitigation: v6_wiki + v8_dialogue + sft_data balance encyclopedic + assistant tones, but no quantitative balance check performed.
3. **sft_data.jsonl chat-template uses `사용자/도우미` literal labels**, not the ChatML `<|im_start|>`/`<|im_end|>` tokens used by Llama Path A v2 winner. If BG-FT/FU target is Llama-family, may need to swap labels at SCP-time. PATH-C did NOT pre-tokenize — corpus is raw text, agnostic to chat format. Decision deferred to BG-FT spec.
4. **No deduplication across sources**. opensubtitles + v8_dialogue may have semantic overlap; kowiki_zst + ko_wiki_small + v6_wiki are partially redundant Wikipedia content. Hash-level dedup not run; LSH semantic dedup not run. Estimated 5-15% duplicate lines remaining.
5. **Hangul ratio 0.6214 is line-mean, not token-mean post-tokenization**. Once a Llama tokenizer (or KO-extended) is applied, the ratio in *tokens* may differ — Hangul characters often consume 2-3 BPE tokens each whereas EN words 1-2. True KO token ratio post-tokenization untested; could be higher OR lower than 62%.
6. **License re-distribution unverified**. opensubtitles CC-BY requires attribution in HF README; Wikipedia ko CC-BY-SA-3.0 requires share-alike clause; sft_data.jsonl is anima-internal synthetic but its template prompts may have been seeded from external sources (not audited). Pre-public-promote: license audit required.
7. **No train BG verification yet**. "Target met" applies to corpus stats, not to "small successful model" outcome. Whether 246MB / 62% KO is sufficient quantity for fresh-train convergence on small (e.g. 124M) model unproven; literature suggests 1B+ tokens needed for non-trivial KO LM. Current corpus ≈ 100M-150M tokens estimated.

---

## Next steps

1. Upload PRIVATE: `hf upload need-singularity/anima-clm-3-corpus-ko-heavy ...` (recipe in `hf_upload_recipe.txt`)
2. Spawn BG-FT (fresh small KO model train) + BG-FU (LoRA fine-tune Llama on KO-heavy) — both consume `corpus_ko_heavy.txt`
3. SCP to ubu1 or RunPod target with sha256 verify
4. License audit pass before public promote
5. Optional v2 build: lift kowiki_zst cap to 500MB (full file), add deduplication, target ≥1GB / 70% Hangul
