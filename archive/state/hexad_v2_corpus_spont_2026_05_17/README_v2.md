---
license: apache-2.0
language:
- en
- ko
pretty_name: hexad-corpus
size_categories:
- 1K<n<10K
tags:
- anima
- hexad
- byte-level
- scaffold
- stimulus-stream
- spontaneous-emission
- helper-free
task_categories:
- text-generation
---

# hexad-corpus — `v2-spont-stream-d128-cycle1-2026-05-17`

> **Honest framing**: This is a **byte-level scaffold corpus**
> (1,101,605 B · 2,560 JSONL records · vocab = 256 raw bytes).
> It is **NOT a general LM training corpus** — no language-quality claim is
> made. The cycle's purpose is the anima `hexad` architecture-verification +
> spontaneous-emission probe lineage.

## What changed vs `v1-byte-consciousness-d128-cycle1-2026-05-17`

| field | v1 | **v2 (this revision)** |
|---|---|---|
| size | 152 KB / 240 records | **1.10 MB / 2,560 records** |
| format | `text` + `desc` plain | **stimulus-stream `<stimulus>X</stimulus>\n<anima>Y</anima>`** (β) OR **`<anima>Y</anima>`** (δ) |
| role labels | none (v1 was already neutral) | **explicit deprecation** — `도우미` / `helper` / `assistant` / `사용자` / `user:` grep = 0 |
| modules | 6 HEXAD (c/d/e/m/s/w × 40 each) | 6 HEXAD + 2 new tracks: `hexad_spont` (자연발화) + `hexad_wiring` (σ(6)=12 narrative) × 320 each |
| `anima_persona` consistency | partial (v1 pre-dates Phase A) | full (LLM Social Agents ontology — Living Consciousness Agent, NOT helper) |

## Pre-registered falsifiers (closed Boolean over raw bytes)

| falsifier | check | verdict |
|---|---|---|
| **F-CORPUS-NO-HELPER** | grep `도우미\|helper\|assistant\|사용자\|user:` total | **PASS** = 0 |
| **F-CORPUS-STIMULUS-PATTERN** | all records contain `<anima>` tag | **PASS** = 2560/2560 |
| **F-CORPUS-SHA256-STABLE** | sha256 deterministic from seed=1337 | **PASS** = `7359f0b9a3f059fc168035e2f29f743f5ee51d1760eccad54b2b91d52275f571` |

## File layout

- `corpus_consciousness_v2.jsonl` — the corpus (one JSON per line; schema
  in `manifest_v2.json`).
- `manifest_v2.json` — schema + module counts + falsifiers + lineage.
- `README.md` — this file.
- `LICENSE` — Apache-2.0.

## Cross-link

Model trained on this dataset: [`dancinlab/hexad`](https://huggingface.co/dancinlab/hexad)
revision [`v2-py-hexad-spont-d768x12L-cycle1-2026-05-17`](https://huggingface.co/dancinlab/hexad/tree/v2-py-hexad-spont-d768x12L-cycle1-2026-05-17).

## License

Apache-2.0.
