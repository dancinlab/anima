# anima-corpus-5lang-7b-webscale — CORPUS CARD

> **⚠️ R2-STAGED, NOT HF-HOSTED.** The 143.60 GiB of raw byte-corpus lives **only in
> Cloudflare R2** (bucket `phanes`, prefix `anima-7b/web/`), an egress-free durable
> staging store. This HF dataset holds the **pointer manifest + this card + 200 KB
> per-language sample heads** — NOT the 143 GB itself. The full corpus is **fetched
> from R2** for training. It is not HF-mirrored and not held locally.

## What this is

The **web-scale 7B-Chinchilla-optimal extension** of the anima default-lane corpus. The
prior clean-license-only build (`anima-corpus-5lang-gb-balanced`, 357.8 MB = 0.27% of the
7B-optimal token budget) was **MID-rung-viable, not 7B-sufficient**. This corpus closes
that gap with **ODC-BY web bulk** (Common-Crawl-derived FineWeb / FineWeb-2).

| metric | value |
|---|---|
| total byte-corpus | **143.60 GiB** (154.19 GB decimal) |
| tokens / param (7B) | **22.0 tok/param** (Chinchilla-optimal is 20 → **EXCEEDS**) |
| fraction of 7B-optimal | **110.1%** of the 140B-token 7B-optimal |
| byte vocabulary | **V = 256** (byte-level, no tokenizer) |
| languages | en · fr · de · es · ko (5-lang balanced) |
| shards | 20 |
| license | **ODC-BY** (web-derived) |

## Per-language / per-source

| lang | size (GB decimal) | size (GiB) | shards | source (ODC-BY) |
|---|---:|---:|---:|---|
| en | 25.83 | 24.05 | 8 | `HuggingFaceFW/fineweb` sample/10BT |
| fr | 32.79 | 30.53 | 3 | `HuggingFaceFW/fineweb-2` fra_Latn |
| de | 31.00 | 28.87 | 3 | `HuggingFaceFW/fineweb-2` deu_Latn |
| es | 32.94 | 30.67 | 3 | `HuggingFaceFW/fineweb-2` spa_Latn |
| ko | 31.64 | 29.46 | 3 | `HuggingFaceFW/fineweb-2` kor_Hang |
| **total** | **154.19** | **143.60** | **20** | — |

5-language **balanced**. **Korean web bulk is INCLUDED** — this fixes the prior
`gb-balanced` build's Korean gap, where Project Gutenberg has zero Korean books so ko art /
ko consciousness were 0 and ko leaned wiki-only. FineWeb-2 kor_Hang provides real Korean web
text at scale (≈ 31.64 GB).

## License & provenance

- **License: ODC-BY** (Open Data Commons Attribution). All bytes are web-derived:
  - **en** = `HuggingFaceFW/fineweb` (sample/10BT) — ODC-BY.
  - **fr / de / es / ko** = `HuggingFaceFW/fineweb-2` (fra_Latn / deu_Latn / spa_Latn /
    kor_Hang) — ODC-BY.
- All FineWeb / FineWeb-2 data is derived from **Common Crawl**. Attribution is carried per
  the ODC-BY terms.
- **Persona / identity content is NOT in this corpus.** anima's persona and identity voice
  stay **authored** (see the capped social/persona register in `anima-corpus-5lang-gb-balanced`);
  this web bulk supplies the factual/linguistic base only.

## PII scrub & byte hygiene

- **PII-scrubbed**: `email → [EMAIL]`, `phone → [PHONE]`. The `[EMAIL]` / `[PHONE]` tokens are
  **expected** in the text and are the scrub markers, not raw PII.
- **Control bytes 0xFE / 0xFF stripped** → byte vocabulary V = 256.
- **No persona / role injection tags**: `[role:` / `[persona:` grep = **0** on the sample heads.

## How to fetch from R2 (training)

The raw shards are addressed by the per-shard `manifest` in `MANIFEST.json` (R2 key + bytes +
sha256 per shard). To stream the corpus for a training run, read each shard from R2:

```python
import boto3, json
m = json.load(open("MANIFEST.json"))
s3 = boto3.client(
    "s3",
    endpoint_url=f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name="auto",
)
for shard in m["manifest"]:                 # 20 shards, 5 langs
    obj = s3.get_object(Bucket="phanes", Key=shard["key"])
    data = obj["Body"].read()               # verify against shard["sha256"]
    # feed `data` (raw bytes, V=256) to the byte-LM training loader
```

Each shard row carries `key`, `bytes`, `lang`, `sha256` for integrity verification.

## Scope (honest)

- This is the **CORPUS**. The actual **7B train is a separate follow-on GPU fire** — there is
  **no 7B-trained-model claim** here.
- 143.60 GiB / 22.0 tok/param / 110.1% are the **achieved corpus** numbers (verified against
  the R2 manifest byte counts; the 143 GB itself was not re-measured).
- The corpus is **R2-staged, not HF-mirrored, not local**.

## Files in this HF dataset

- `MANIFEST.json` — the R2 pointer manifest (total, tok/param, per-lang, per-shard R2
  keys + bytes + sha256, provenance). **This is the dataset's primary artifact.**
- `CORPUS_CARD.md` — this card.
- `README.md` — dataset card (same honest R2-staged framing).
- `samples/{en,fr,de,es,ko}.head.txt` — a 200 KB head per language pulled from the first
  shard of each language (for inspection only).
