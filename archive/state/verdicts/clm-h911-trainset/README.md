---
license: cc-by-sa-4.0
language:
  - ko
  - en
  - zh
  - ru
  - ja
task_categories:
  - translation
  - feature-extraction
tags:
  - parallel-corpus
  - cross-lingual
  - kosmos
  - clm
  - h911
pretty_name: CLM-KOSMOS H_911 5-language parallel training-set
---

# clm-h911-trainset-5lang-parallel

5-language (**ko · en · zh · ru · ja**) cross-lingual **semantic-linkage** corpus in the
`.kosmos` (kosmos/2.0) format, built to validate **H_911** (cross-lingual semantic
integration) at CLM scale. Two orderings of **byte-identical** content:

- **parallel** (`clm_parallel.kosmos` + `parallel.limen`) — concept-major: the 5 languages
  of each concept are adjacent (cross-lingual coupling `c > 0`).
- **concat** (`clm_concat.kosmos` + `concat.limen`) — language-major: all of one language,
  then the next (count-only control, `c ~ 0`).

The two `.limen` shards have the **same multiset of anchor payloads** and differ **only in
member ordering**. This is the H_911 contrast (parallel vs concat, same bytes / same update).

## Provenance — real vs synthetic (HONEST)

| field | value |
|-------|-------|
| concepts (total) | 2,009 |
| concepts — real (FLORES-200) | 2,009 |
| concepts — synthetic (claude-CLI) | 0 |
| **real fraction** | **1.000** |
| anchors (concepts × 5 langs) | 10,045 |
| byte-tokens (vocab=256, utf-8) | 1,643,965 |

- **Real source**: [FLORES-200](https://github.com/facebookresearch/flores) `dev` + `devtest`
  splits, downloaded from the public Meta CDN
  (`dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz`). FLORES-200 is **true 5-way
  line-aligned** parallel data: the same row index is the same concept in every language —
  exactly the concept alignment H_911 requires.
- **License**: **CC-BY-SA-4.0** (FLORES-200). This dataset inherits it. PRIVATE repo under
  the `dancinlab` org.
- **Synthetic**: none in this build. The builder supports optional `claude`-CLI gap-fill
  (subscription, no API key) recorded as `concepts_synthetic_claude` / `real_fraction`;
  it was not needed because FLORES is already true-parallel.

## Scope honesty (g63 · a_scale_honest_scope)

This is the **max reachable true-5-way real parallel set** (~1.64M byte-tokens) — a tiny
fraction of a full 3B/7B pretrain (~60B / ~140B tokens; **< 0.003 %**). Even adding every
other reachable public 5-lang source (OPUS-100 en-pivot, noisy, not concept-aligned) the
ceiling is **< 1 %** of a 3B pretrain. So this set is a **down-scoped H_911 *validation*
set** (a controlled parallel-vs-concat ordering probe), **not** a full pretraining corpus.
See `MANIFEST_3B_7B.md` for the full budget table. GPU pretraining is a separate, larger,
cost-bearing effort (out of scope for this data layer).

## Format (kosmos/2.0 · C4)

`@corpus` top-level (profile `anima-consciousness-carving` · coord/lane/radius/tier) +
member as a `ref` `.limen` packed shard (magic `LIMEN\0\0\0` + version + count +
length-prefixed `@anchor` records + trailing merkle root) + `closed_corpus`
(Σ frac = 1.0 ∧ member sha256 verifies ∧ merkle recomputes) + placement(coord) ⊥ text(payload).

## Verify

```
python3 verify_corpus.py .   # -> VERIFY: ALL-GREEN
```
Checks limen parse, merkle recompute (vs declared root in shard and `.kosmos`),
member sha256, payload-multiset identity across orderings, and that the shard byte-streams
differ (ordering only).

## SHA-256 / merkle (full set)

| ordering | shard sha256 | merkle root | count |
|----------|--------------|-------------|------:|
| parallel | `8af38a34…cd66b0` | `e1da04c8…5baa8b` | 10,045 |
| concat   | `bcda97aa…505c64` | `621a23e3…d38e375` | 10,045 |

byte-identical payload multiset across orderings: **true**.
