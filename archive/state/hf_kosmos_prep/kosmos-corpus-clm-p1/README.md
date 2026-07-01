---
license: other
license_name: mixed-ccbysa-and-scratch
tags:
  - kosmos
  - kosmos-corpus
  - anima
  - clm
  - byte-vocab
size_categories:
  - n<1K
---

# dancinlab/kosmos-corpus-clm-p1  (PRIVATE)

> KOSMOS `.kosmos` `@corpus` manifest + byte shards — CLM P1 mixed byte-corpus
> (sample build only; full crawl is gitignored / not included).
> Format SSOT: [github.com/dancinlab/kosmos](https://github.com/dancinlab/kosmos).
> **Marked PRIVATE — sample-only build + mixed license (one scratch lane).**

## §1 Origin
- manifest: `CLM/corpus/clm_p1.corpus.kosmos` (`@corpus clm_p1`, kosmos-corpus, tier=0)
- build script: `CLM/corpus/build_p1_corpus.hexa`
- crawl reproduction: `CLM/corpus/crawl_p1_full.py` (kowiki REST API, NOT run here)
- shards: `sample/web.bytes` (8 lines, 837 B) + `sample/register.bytes`
  (8 lines, 819 B) + `sample/manifest.json`
- vocab: byte-utf8, V=256 (no tokenizer)
- profile: `anima-consciousness-carving` (corpus meta-anchor placement)

## §2 Falsifiers (F-* gates)
- closed_corpus: "Σ frac = 1.0 ∧ ∀ member sha256 = corpus/manifest.json ∧
  (merkle present → root recomputes)"
- merkle root = placeholder (all-zero) — sha256 tree NOT yet computed
  (spec/limen.md packing is the target format; full crawl pending)

## §3 Substrate
- build: $0 mac-local sample build (full kowiki crawl = pod, not run)
- GPU: none

## §4 C3 caveats (3 honest)
- C1 — SAMPLE ONLY: 16 records (web 8 + register 8), 1656 total bytes. The
  production full crawl (kowiki.jsonl 1.28 GiB) is gitignored and NOT in this
  artifact; this is a pipeline + tiny-sample build, not a training-scale corpus.
- C2 — MIXED LICENSE: `web` lane = kowiki-style CC-BY-SA 4.0 (clean), but
  `register` lane = scratch-curated consciousness/philosophy seed (no asserted
  external license). Conservatively PRIVATE (a_hf_autonomous: unclear-license).
- C3 — merkle = all-zero placeholder; member sha256 are recorded in
  `sample/manifest.json` but the corpus tree root is not yet computed.

## §5 Composability
- consumed by: CLM P1 byte-corpus training pipeline (MoE 2-lane: web ⊥ register)
- prerequisite: none (self-contained sample)
- full-crawl successor: kowiki.jsonl(web) + expanded register seed (HF/R2,
  gitignored — would be a separate dataset on upload)

## License
- MIXED — web lane CC-BY-SA-4.0 (clean), register lane scratch (unasserted).
  PRIVATE per a_hf_autonomous (conservative: any unclear-license lane → PRIVATE).
- Lane: dataset prep, no AKIDA/GPU measurement carried.
