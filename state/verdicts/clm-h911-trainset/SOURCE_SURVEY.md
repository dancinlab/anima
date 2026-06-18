# H_911 5-language Parallel Corpus — Source Survey (reachable vs not)

Survey date 2026-06-01, host mini. HF token = `secret get hf.token` (never printed).
5 languages required: ko · en · zh · ru · ja.

## Reachable

| source | repo / URL | reach | 5-way truly aligned | license | notes |
|--------|-----------|-------|---------------------|---------|-------|
| **FLORES-200** | `dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz` | ✅ direct CDN (25.6 MB) | **YES** — line-aligned dev(997)+devtest(1012)=2009 concepts | CC-BY-SA-4.0 | **chosen source.** Real true-parallel, all 5 langs present. |
| OPUS-100 | `Helsinki-NLP/opus-100` (HF) | ✅ ungated, streamable | NO — en-centric pairs (en-ko/zh/ru/ja), not one 5-way row | "unknown" (HF card) | usable only as en-pivot pseudo-5way (noisy). |
| Tatoeba (parquet) | `Helsinki-NLP/tatoeba` (HF) | ✅ ungated | NO — pair/sentence graph, needs custom 5-way join | CC-BY-2.0 | partial; join cost not worth it given FLORES. |

## NOT reachable (gated / script-based)

| source | repo | blocker |
|--------|------|---------|
| FLORES-200 (HF) | `facebook/flores` | **GATED** — manual access grant required; token alone returns `DatasetNotFoundError (gated)`. |
| FLORES+ (HF) | `openlanguagedata/flores_plus` | **GATED** — same. |
| FLORES-200 mirror | `Muennighoff/flores200` | ungated repo but only hosts `flores200.py` loader **script** (datasets 4.x rejects scripts); no parquet/tsv data files. |
| FLORES-101 | `gsarti/flores_101` | script-based loader only. |
| Tatoeba-MT | `Helsinki-NLP/tatoeba_mt` | script-based (`tatoeba_mt.py`) — `datasets` 4.x rejects script loaders (RuntimeError). |
| OPUS Books | `Helsinki-NLP/opus_books` | only en-ru for our langs (no 5-way). |

## Conclusion

The only **true 5-way line-aligned, license-clean, reachable** parallel source is
**FLORES-200 via the public Meta CDN** (CC-BY-SA-4.0). The HF-hosted FLORES variants are all
gated or script-based and not reachable with a token alone. OPUS-100 / Tatoeba are reachable
but en-centric / pair-graph (no guaranteed single 5-way concept row), so they only extend the
*max-reachable-real* ceiling as noisy en-pivot data, not as clean H_911 signal.
