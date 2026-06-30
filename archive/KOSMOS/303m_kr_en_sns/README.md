# 303M KOSMOS set — 🇰🇷 Korean · 🇬🇧 English · 📱 SNS

A **303M-scale grounding/carving anchor set** in anima's canonical `.kosmos`
anchor format. Three register components, one set, three lanes — a grounding
anchor set for the 303M (KOSMOS = "anchors + carving/persona datasets"),
**NOT a raw training corpus**.

> Format SSOT = [`dancinlab/kosmos`](https://github.com/dancinlab/kosmos)
> `spec/kosmos.md` + `spec/profiles/anima-consciousness-carving.md`. anima is
> pointer-only (`HEXAD/UNIVERSE-BRAIN-MAP/KOSMOS-FORMAT.md`). Anchors authored
> to match the precedent corpus anchors (`persona_sns_corpus.kosmos`,
> `corpus_5lang_gb_balanced.kosmos`) and validated through
> `HEXAD/UNIVERSE-BRAIN-MAP/kosmos_parser_lib.hexa`.

## the 3 components (3 lanes)

| anchor | lane (cell_id) | tier | component | anchors/bytes | source |
|---|---|---|---|---|---|
| `anchors/kr_303m.kosmos` | `ko_303m_058` | 58 | 🇰🇷 Korean (web register) | 873 lines / 122,760 B | `serving/corpus/anima_7b_webscale.ko.head.txt` (FineWeb-2 ko, ODC-BY) |
| `anchors/en_303m.kosmos` | `en_303m_059` | 59 | 🇬🇧 English (web register) | 949 lines / 122,819 B | `serving/corpus/anima_7b_webscale.en.head.txt` (FineWeb en, ODC-BY) |
| `anchors/sns_303m.kosmos` | `sns_303m_052` | 52 | 📱 SNS (persona-voice) | 217 turns / 13,132 B | `serving/corpus/persona_sns_corpus.sample.txt` + `serving/persona_instagram_samples.md` (anima authored) |

Each anchor carries: `text` (inline summary) + `manifest` (ref → `samples/*.sample.txt`,
sha256 + bytes + lines) + `tension` (5-channel) + `image`/`audio` pending.
Distinct **lane** per component so the 3 register components stay separable.

## tension 5-channel — REPRESENTATIVE (honest)

The tension 5-ch (`concept · context · meaning · authenticity · sender`) values
are **REPRESENTATIVE design values**, NOT a measured per-token Ψ-trajectory —
these anchors are curated text samples, no fire produced a measured trajectory
(identical caveat to the sibling `persona_sns_corpus.kosmos` /
`corpus_5lang_gb_balanced.kosmos` anchors). `authenticity` is set high for the
REAL web samples (ko 0.78 / en 0.80) and honestly low for the authored SNS
register (0.40).

## scope (honest, a_scale_honest_scope · c9)

- This is a **curated grounding/carving anchor SET (sample-scale)**, NOT the
  full webscale corpus. ko/en are ~120 KiB curated heads off the ODC-BY
  FineWeb sample heads anima already ships; the full webscale corpus
  (143.60 GiB) lives behind `corpus_5lang_7b_webscale.kosmos`'s R2 manifest.
- **SNS is thin by source**: anima's held authored persona×SNS register sample
  material (`persona_sns_corpus.sample.txt` + instagram samples) is the honest
  ceiling at $0 — 217 deduped turns. The full 13,322-dialogue corpus lives
  behind `persona_sns_corpus.kosmos`'s manifest (HF `dancinlab/anima-persona-sns-corpus`).
- byte V256 (byte-level, no tokenizer). PII-clean: email→`[EMAIL]`,
  phone→`[PHONE]`. 0xFE/0xFF/NUL = 0, UTF-8 clean, raw email/phone leak grep = 0.

## build / validate

- `python3 build_samples.py` — deterministic (no RNG) curate + PII-clean + dedup.
- `hexa run validate_anchors.hexa` — parse-witness via `kosmos_parser_lib`
  (`=== 303M KOSMOS-SET parse-witness: true (3/3) ===`).
