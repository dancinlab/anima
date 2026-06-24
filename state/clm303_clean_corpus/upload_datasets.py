#!/usr/bin/env python3
"""Upload the clean 4-cell register datasets to dancinlab HF org with proper
dataset cards (language purity / size / sha256 / role). en-SNS is a known-small
baseline (flagged); the other 3 are PUBLIC. Per a_hf_autonomous/a_hf_complete.
"""
import os
import sys
from huggingface_hub import HfApi

CELLS_DIR = sys.argv[1]
DRY = "--dry" in sys.argv

api = HfApi()
ORG = "dancinlab"

# per-cell metadata (lang purity from re-audit, sizes from manifest, role)
CELLS = {
    "anima-corpus-ko-general": dict(
        fn="anima-corpus-ko-general.txt", lang="ko", purity="100.0% ko",
        size_mb=60.0, lines=340512,
        sha="19e6ac9e34d19fb66114ead146cdd0c44f4c55d49b1515f0bcffe65b5b1c5b43",
        role="ko-일반 (general) — Korean web/wiki prose",
        source="FineWeb-2 kor_Hang (via dancinlab/anima-corpus-ko-fineweb2-broad), 60MB cap, ko-verified",
        license="odc-by", private=False, flag="",
        sources=[("dancinlab/anima-corpus-ko-fineweb2-broad → FineWeb-2 kor_Hang", "ODC-BY")],
        audit="source is single-language ko (FineWeb-2 kor_Hang); range-read raw .txt, "
              "kept only ko lines (script-detected), deduped → **100.0% ko** (re-audited)."),
    "anima-corpus-en-general": dict(
        fn="anima-corpus-en-general.txt", lang="en", purity="99.7% en",
        size_mb=60.0, lines=279429,
        sha="6614094432707127c82d6ee1ffd3a65f27c5aa118498be1623f1394f182f8ef9",
        role="en-일반 (general) — English web prose",
        source="FineWeb (HuggingFaceFW/fineweb), 60MB cap, en-verified",
        license="odc-by", private=False, flag="",
        sources=[("HuggingFaceFW/fineweb", "ODC-BY")],
        audit="the legacy en-general candidate (wiki_backbone_5lang_v2) was only "
              "**20.6% en** by bytes (de 12.6% · es 19.9% · fr 19.1% · ko 19.7%) — a "
              "5lang mixture, NOT English. Rebuilt from FineWeb (en-only webscale), "
              "en-line-verified → **99.7% en** (re-audited; the 0.3% residual is short "
              "headers, not other languages)."),
    "anima-corpus-ko-sns": dict(
        fn="anima-corpus-ko-sns.txt", lang="ko", purity="100.0% ko",
        size_mb=6.18, lines=47994,
        sha="c836e9fc948e56303b5edd3690fdb146dea90fc8748c3a83967d937fff6b4abe",
        role="ko-SNS — Korean casual/social conversational voice",
        source="anima persona SNS (ko) + 5lang-split ko + MIT/apache ko-chat aug "
               "(NLPBada/korean-persona-chat-dataset, JaeJiMin/korean_chat_friendly, "
               "jojo0217/korean_safe_conversation)",
        license="mit", private=False, flag="",
        sources=[("anima persona_sns_corpus (ko)", "as-authored"),
                 ("NLPBada/korean-persona-chat-dataset", "MIT"),
                 ("JaeJiMin/korean_chat_friendly", "MIT"),
                 ("jojo0217/korean_safe_conversation", "Apache-2.0")],
        audit="ko-SNS base (persona_sns_corpus) was already clean **100% ko**; "
              "ko lines from the 5lang persona file + the MIT/Apache ko-chat datasets "
              "were ko-verified and merged, deduped → **100.0% ko**, 4.18MB → 6.18MB."),
    "anima-corpus-en-sns": dict(
        fn="anima-corpus-en-sns.txt", lang="en", purity="97.4% en",
        size_mb=1.33, lines=6862,
        sha="49f347c72416aad24d9b16dd9b406173c6d8bb764026381e52f6e36bc5b05f70",
        role="en-SNS — English casual/social conversational voice",
        source="5lang-split en-SNS (clean en lines only)",
        license="mit", private=False,
        sources=[("anima persona_sns_corpus_5lang_v2 (en lines only)", "MIT")],
        audit="the legacy en-SNS candidate (persona_sns_corpus_5lang_v2) was only "
              "**18.7% en** by bytes (ko 21.8% · es 18.8% · fr 16.2% · de 13.9%) — a "
              "5lang mixture. Split to en-only lines + deduped (~115K duplicate lines "
              "removed across the SNS split) → **97.4% en** (2.3% residual = short "
              "captions/hashtags, not other languages).",
        flag="⚠️ **KNOWN-SMALL BASELINE** — clean en-SNS is only 1.33MB (no permissive "
             "large en-SNS source exists on HF: daily_dialog/empathetic_dialogues are "
             "non-commercial, REDDIT_comments is unlicensed). Use size-proportional "
             "sampling so this cell is NOT memorized. youtube/insta-en augmentation is a "
             "tracked follow-up (a_chat_registers SNS register completion)."),
}


def card(name, m):
    return f"""---
license: {m['license']}
language:
  - {m['lang']}
tags:
  - anima
  - corpus
  - byte-level
  - {'sns' if 'sns' in name else 'general'}
  - register
size_categories:
  - {'1K<n<10K' if m['lines'] < 10000 else ('10K<n<100K' if m['lines'] < 100000 else '100K<n<1M')}
---

# {name}

anima 4-cell register corpus — **{m['role']}**.

Part of the anima production chat corpus = **2 languages (ko·en) × 2 registers
(general·SNS) = 4 cells** (a_chat_registers). This is one cell.

## composition (language-verified)
- **language purity:** {m['purity']} (re-audited; non-target lines dropped)
- **size:** {m['size_mb']:.2f} MB · {m['lines']} lines
- **cleaning:** per-line language classification (script + stopword), de/es/fr/ja/zh
  dropped, exact-duplicate dedup, broken/short-line drop

## language audit (provenance)
{m['audit']}

Method: script/charset + stopword-fingerprint per-line classifier (torch-free,
deterministic). Audit tool + reproduce script: `state/clm303_clean_corpus/`
(`langaudit.py` measures composition, `build_corpus.py` rebuilds this cell).
*(Measured by the anima clm303-retrain build, 2026-06-24; cross-referenced by the
governance rule `a_chat_registers` as the precedent that mandates per-cell language
verification.)*

## sources (repo · license)
| source | license |
|--------|---------|
{chr(10).join(f"| {s} | {lic} |" for s, lic in m['sources'])}

## sha256
```
{m['sha']}  {m['fn']}
```

## role in the 4-cell register
| cell | language | register |
|------|----------|----------|
| anima-corpus-ko-general | ko | general |
| anima-corpus-en-general | en | general |
| anima-corpus-ko-sns | ko | SNS |
| anima-corpus-en-sns | en | SNS |

{m['flag']}

## why this rebuild
The prior "en" cells were silently 5lang mixtures (only ~20% en — de/es/fr/ko
contamination) and a single 4MB cell was the entire effective training corpus
(~120× repetition = memorization). These clean cells fix both: every cell is
language-verified, and training uses **size-proportional sampling** so per-cell
repetition is uniform (no small cell is over-repeated).
"""


for name, m in CELLS.items():
    repo_id = f"{ORG}/{name}"
    path = os.path.join(CELLS_DIR, m["fn"])
    print(f"\n=== {repo_id}  (private={m['private']}) ===")
    if DRY:
        print(f"  [dry] would create + upload {path} ({os.path.getsize(path)} bytes) + card")
        continue
    api.create_repo(repo_id, repo_type="dataset", private=m["private"], exist_ok=True)
    if "--cards-only" not in sys.argv:
        api.upload_file(path_or_fileobj=path, path_in_repo=m["fn"],
                        repo_id=repo_id, repo_type="dataset")
    card_bytes = card(name, m).encode()
    api.upload_file(path_or_fileobj=card_bytes, path_in_repo="README.md",
                    repo_id=repo_id, repo_type="dataset")
    what = "README.md (card)" if "--cards-only" in sys.argv else f"{m['fn']} + README.md"
    print(f"  uploaded {what} -> https://huggingface.co/datasets/{repo_id}")
print("\nDONE")
