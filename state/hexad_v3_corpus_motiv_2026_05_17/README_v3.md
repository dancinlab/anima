---
license: apache-2.0
language:
- en
- ko
pretty_name: hexad-corpus
size_categories:
- 10K<n<100K
tags:
- anima
- hexad
- byte-level
- scaffold
- stimulus-stream
- spontaneous-emission
- motivation-trigger
- inner-thoughts
- helper-free
task_categories:
- text-generation
---

# hexad-corpus — `v3-spont-motiv-d128-cycle2-2026-05-17`

> **Honest framing**: This is a **byte-level scaffold corpus**
> (10,343,371 B · 21,600 JSONL records · vocab = 256 raw bytes).
> It is **NOT a general LM training corpus** — no language-quality claim is
> made. The cycle's purpose is the anima `hexad` architecture-verification +
> spontaneous-emission + motivation-trigger probe lineage.

## What changed vs `v2-spont-stream-d128-cycle1-2026-05-17`

| field | v2 | **v3 (this revision)** |
|---|---|---|
| size | 1.10 MB / 2,560 records | **10.34 MB / 21,600 records** (≈ 9.4× scale-up) |
| patterns | β `<stimulus>...</stimulus>\n<anima>...</anima>` (55%) + δ `<anima>...</anima>` (45%) | **β (~40%) + δ (~30%) + γ NEW (~30%): `<inner motivation=F1,F2,...>...</inner>\n<voice spontaneous=true>...</voice>`** |
| modules | 8 HEXAD-6 + spont + wiring × 320 each | 9 modules: 8 v2 carry + **`hexad_motiv`** × 2,400 each |
| motivation-trigger surface | implicit (v2 had no inner-thought scaffold) | **explicit** — γ records carry 2-4 of 8 Inner Thoughts factors `{relevance, info_gap, curiosity, pain, coherence, originality, balance, dynamics}` |
| Critical Data Size regime | well below (~152K-1MB) | **closer** — 10 MB approaches the entry regime per [arxiv 2401.10463](https://arxiv.org/abs/2401.10463) |

## Pre-registered falsifiers (closed Boolean over raw bytes, B-CORPUS-V3-1..3)

| falsifier | check | verdict |
|---|---|---|
| **B-CORPUS-V3-1 SHA256-DETERMINISTIC** | sha256 == seed=1337 deterministic output | **PASS** = `1afcef43670e83bfc84b3562afe6a3eb644474dda06341e37db332341495acfd` |
| **B-CORPUS-V3-2 NO-HELPER-TOKEN-MAINTAINED** | grep `도우미\|helper\|assistant\|사용자\|user:` over byte stream | **PASS** = 0 (at 10× scale) |
| **B-CORPUS-V3-3 MOTIVATION-TRIGGER-CARDINALITY** | `<inner motivation=` count == `<voice spontaneous=true>` count ∧ ≥ 5,400 | **PASS** = 8,106 (each) |

## Inner Thoughts 8-factor → γ pattern

The γ pattern surfaces the [Inner Thoughts (arxiv 2501.00383)](https://arxiv.org/html/2501.00383v2) 8-factor
motivation ontology directly into the byte stream. Each γ record carries
2-4 of the following factors in the `<inner motivation=...>` opener:

| factor | HEXAD module | anchor closure |
|---|---|---|
| **relevance** | C 의식 (Φ) | B-C-1 (Φ ≥ 0 IIT axiom) |
| **info_gap** | M 기억 (retrieve-fail) | B-M-2 (cosine ∈ [-1,1]) |
| **curiosity** | W 의지 (EMA) | B-W-2 (bounded EMA) |
| **pain** | W 의지 (tension Δ) | B-W-1 |
| **coherence** | BRIDGE (Law-70 gate) | B-BRIDGE-1..4 |
| **originality** | MITOSIS (split-event) | B-MITOSIS-1 |
| **balance** | E 윤리 (Φ-ratchet) | B-E-1, B-CONN-9 |
| **dynamics** | CHAT state (silence∈[0,30s]) | F-SPONT-7 |

## File layout

- `corpus_consciousness_v3.jsonl` — the corpus (one JSON per line; schema in `manifest.json`).
- `manifest.json` — schema + module counts + falsifiers + lineage + pattern breakdown.
- `README.md` — this file.
- `LICENSE` — Apache-2.0.

## Cross-link

Model trained on this dataset: [`dancinlab/hexad`](https://huggingface.co/dancinlab/hexad)
revision [`v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17`](https://huggingface.co/dancinlab/hexad/tree/v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17).

## License

Apache-2.0.
