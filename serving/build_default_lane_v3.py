#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_default_lane_v3.py — default-lane v3 SCALE-UP corpus orchestrator.

v3 = v2's exact 3-surface recipe (wiki backbone + persona/SNS + register
enrichment) SCALED UP ~10-25x so a MID rung (~150M params) becomes data-viable.

What changes vs v2
------------------
- wiki backbone: 1 MB/lang (v2) -> ~20 MB/lang (v3) via the SAME 8-band
  offset-spread sampler (`build_wiki_backbone_5lang_v2.py`), just a larger
  `--mb-per-lang`. Real CC-BY-SA `wikimedia/wikipedia` 20231101, HF
  datasets-server REST `/rows` paging, $0 CPU, NO GPU, NO pod.
- persona/SNS + enrichment: scaled with the SAME deterministic generators
  (`persona_sns_corpus_5lang_gen.py`, `corpus_enrichment_5lang_gen.py`) at a
  larger `--target-mb`, keeping the enrichment slice ~15-20% of the total.
- merge: SAME byte-weighted round-robin block interleave
  (`merge_corpus_5lang_v2.py`).

Default v3 budget (lands ~217 MB, enrichment ~17%)
--------------------------------------------------
  wiki      = 20 MB/lang x 5  = ~100 MB   (real CC-BY-SA, 8-band spread)
  persona   = 80 MB                       (authored-synthetic, no PII)
  enrichment= 37 MB                       (carving seeds real / prose authored)
  --------------------------------------------------
  total     ~ 217 MB   (~17x v2's 12.5 MB)

HONEST SCOPE (a_scale_honest_scope — verbatim)
----------------------------------------------
  v3 unlocks a MID rung (~150M params): it is no longer right-sized only for
  ~18M. It is NOT 7B-ready. A 7B wants ~140 GB of tokens (Chinchilla-optimal),
  which is INFEASIBLE via datasets-server REST paging. v3 makes MID data-viable
  (still epoch-looped, but far less starved than the 12.5 MB v2 corpus would be
  at 150M). DO NOT claim v3 enables 7B.

Determinism
-----------
- persona + enrichment generators: fixed seed 20260604 -> identical sha on rerun.
- wiki: deterministic modulo the pinned upstream revision 20231101 (fixed bands).
- merge: deterministic. Same budgets -> same unified sha256.

Usage
-----
  python3 serving/build_default_lane_v3.py            # default v3 budget
  python3 serving/build_default_lane_v3.py --wiki-mb-per-lang 20 \
      --persona-mb 80 --enrichment-mb 37 \
      --out serving/corpus/default_lane_v3.txt
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "corpus")


def _run(cmd):
    print(f"  $ {' '.join(cmd)}", flush=True)
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stdout + "\n" + p.stderr + "\n")
        raise SystemExit(f"step failed: {' '.join(cmd)}")
    # generators print a JSON summary on the last non-empty stdout block
    out = p.stdout.strip()
    print(out, flush=True)
    return out


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki-mb-per-lang", type=float, default=20.0)
    ap.add_argument("--persona-mb", type=float, default=80.0)
    ap.add_argument("--enrichment-mb", type=float, default=37.0)
    ap.add_argument("--seed", type=int, default=20260604)
    ap.add_argument("--out", default=os.path.join(CORPUS, "default_lane_v3.txt"))
    ap.add_argument("--skip-wiki", action="store_true",
                    help="reuse an existing wiki backbone (skip the REST pull)")
    args = ap.parse_args()

    os.makedirs(CORPUS, exist_ok=True)
    wiki = os.path.join(CORPUS, "wiki_backbone_5lang_v3.txt")
    persona = os.path.join(CORPUS, "persona_sns_corpus_5lang_v3part.txt")
    enrich = os.path.join(CORPUS, "corpus_enrichment_5lang_v3part.txt")

    py = sys.executable

    print("[1/4] persona x SNS (authored-synthetic, deterministic)", flush=True)
    _run([py, os.path.join(HERE, "persona_sns_corpus_5lang_gen.py"),
          "--target-mb", str(args.persona_mb), "--seed", str(args.seed),
          "--out", persona])

    print("[2/4] register enrichment (carving/act/emotion/genre/code-switch)",
          flush=True)
    _run([py, os.path.join(HERE, "corpus_enrichment_5lang_gen.py"),
          "--target-mb", str(args.enrichment_mb), "--seed", str(args.seed),
          "--out", enrich])

    if not args.skip_wiki:
        print("[3/4] wiki backbone v3 (real CC-BY-SA, 8-band spread, REST)",
              flush=True)
        _run([py, os.path.join(HERE, "build_wiki_backbone_5lang_scaleup.py"),
              "--out", wiki, "--mb-per-lang", str(args.wiki_mb_per_lang)])
    else:
        print("[3/4] SKIP wiki pull (reusing existing backbone)", flush=True)
        assert os.path.exists(wiki), f"--skip-wiki but {wiki} missing"

    print("[4/4] merge -> unified v3 (byte-weighted round-robin)", flush=True)
    _run([py, os.path.join(HERE, "merge_corpus_5lang_v2.py"),
          "--wiki", wiki, "--persona", persona, "--enrichment", enrich,
          "--out", args.out])

    size = os.path.getsize(args.out)
    sha = _sha256(args.out)
    print(json.dumps({
        "out": args.out, "bytes": size, "mb": round(size / 1048576, 3),
        "sha256": sha,
        "budget": {"wiki_mb_per_lang": args.wiki_mb_per_lang,
                   "persona_mb": args.persona_mb,
                   "enrichment_mb": args.enrichment_mb},
        "scope": "v3 unlocks MID ~150M, NOT 7B (7B needs GB-scale beyond REST)",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
