"""Post-FT-EXTENDED sampling — compare base/post-FT/post-FT-extended on identical matrix.

Reuses harness from anima_clm_v2_chat_ext_smoke_2026_05_10/run.py (phase A 96 trial + phase B-beam 24 trial = 120 trial per ckpt).

Adds lexical fluency metrics:
  - ko_word_real_count: count tokens that appear in a small Korean dictionary (kowiki15-derived)
  - ko_chunk_2gram_known_ratio: bigram-level overlap with corpus_extended (proxy for "real Korean")
"""
import sys
import json
import time
import re
from pathlib import Path
from collections import Counter

import torch

sys.path.insert(0, "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09")
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_clm_v2_chat_ext_smoke_2026_05_10")

from forward_smoke import ConsciousLMReconstructed, text_to_byte_ids  # noqa: E402
import run as harness  # noqa: E402

OUT_DIR = Path("/Users/ghost/core/anima/state/anima_convo_5k_ft_extended_2026_05_10")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CKPTS = [
    {
        "label": "convo_5k_pre_ft",
        "path": "/Users/ghost/.cache/huggingface/hub/models--dancinlab--clm-v2-byte-18m-convo-5k/snapshots/1af2bcaeaf70c1d0b1a19939a8ada79a28f8cd30/convo_5k.pt",
    },
    {
        "label": "convo_5k_ft_step_10000_initial",
        "path": "/Users/ghost/core/anima/state/anima_convo_5k_ft_fire_2026_05_10/post_ft_ckpt.pt",
    },
    {
        "label": "convo_5k_ft_ext_step_20000_final",
        "path": str(OUT_DIR / "post_ft_ext_ckpt.pt"),
    },
]


def build_ko_dictionary():
    """Extract real Korean words from kowiki corpus for lexicon-membership scoring."""
    kowiki_path = Path("/Users/ghost/core/anima/training/corpus_alm_70b_stripped_kowiki15.txt")
    if not kowiki_path.exists():
        return set(), set()
    print(f"  building ko dict from {kowiki_path}...", flush=True)
    text = kowiki_path.read_text(encoding="utf-8", errors="ignore")
    # split on whitespace + punctuation
    tokens = re.findall(r"[가-힣]+", text)  # only Hangul-only tokens
    counter = Counter(tokens)
    # all words that appear ≥3 times, length >=2
    real_words = {w for w, c in counter.items() if c >= 3 and len(w) >= 2}
    # bigrams (Hangul char pair)
    bigrams = set()
    for w in real_words:
        for i in range(len(w) - 1):
            bigrams.add(w[i:i+2])
    print(f"  ko dict: {len(real_words):,} words  {len(bigrams):,} bigrams", flush=True)
    return real_words, bigrams


def lexical_score(gen_text: str, ko_words: set, ko_bigrams: set):
    if not gen_text:
        return {"ko_total": 0, "ko_real_word_count": 0, "ko_real_word_ratio": 0.0,
                "ko_bigram_known": 0, "ko_bigram_total": 0, "ko_bigram_known_ratio": 0.0}
    tokens = re.findall(r"[가-힣]+", gen_text)
    ko_total = sum(len(t) for t in tokens)
    ko_real_count = sum(1 for t in tokens if len(t) >= 2 and t in ko_words)
    # bigrams
    bigrams_in_gen = []
    for t in tokens:
        for i in range(len(t) - 1):
            bigrams_in_gen.append(t[i:i+2])
    ko_bigram_total = len(bigrams_in_gen)
    ko_bigram_known = sum(1 for bg in bigrams_in_gen if bg in ko_bigrams)
    return {
        "ko_total_chars": ko_total,
        "ko_real_word_count": ko_real_count,
        "ko_real_word_ratio": round(ko_real_count / max(1, len(tokens)), 4),
        "ko_bigram_known": ko_bigram_known,
        "ko_bigram_total": ko_bigram_total,
        "ko_bigram_known_ratio": round(ko_bigram_known / max(1, ko_bigram_total), 4),
        "n_ko_tokens": len(tokens),
    }


def main():
    t_global = time.time()
    print("=== building Korean lexicon (kowiki15)...", flush=True)
    ko_words, ko_bigrams = build_ko_dictionary()

    all_results = {}
    by_ckpt = {}
    torch.manual_seed(42)

    for entry in CKPTS:
        if not Path(entry["path"]).exists():
            print(f"\n=== {entry['label']} (SKIP — missing) ===", flush=True)
            by_ckpt[entry["label"]] = {"missing": True}
            continue

        print(f"\n=== {entry['label']} ===", flush=True)
        t0 = time.time()
        model, meta = harness.load_model(entry["path"], n_head_hint=4)
        print(f"  loaded: {meta}  ({time.time()-t0:.1f}s)", flush=True)

        t0 = time.time()
        res_a = harness.run_phase_a(model, entry["label"])
        print(f"  phase A done: {len(res_a)} trials  ({time.time()-t0:.1f}s)", flush=True)

        t0 = time.time()
        res_b = harness.run_phase_b_beam(model, entry["label"])
        print(f"  phase B-beam done: {len(res_b)} trials  ({time.time()-t0:.1f}s)", flush=True)

        results = res_a + res_b

        # add lexical scores per trial
        for r in results:
            gen = r.get("gen", "")
            r["lexical"] = lexical_score(gen, ko_words, ko_bigrams)

        all_results[entry["label"]] = results

        valid = [r for r in results if "gen" in r]
        ko_max = max((r["scores"]["ko_ratio"] for r in valid), default=0.0)
        ko_count_max = max((r["scores"]["ko_count"] for r in valid), default=0)
        ko_at_least_1 = sum(1 for r in valid if r["scores"]["ko_count"] >= 1)
        ko_at_least_5 = sum(1 for r in valid if r["scores"]["ko_count"] >= 5)
        ko_at_least_10 = sum(1 for r in valid if r["scores"]["ko_count"] >= 10)
        n_gib = sum(1 for r in valid if r.get("gibberish"))
        best = max(valid, key=lambda r: r.get("quality", -1.0), default=None)

        # lexical aggregate
        lex_real_words_max = max((r["lexical"]["ko_real_word_count"] for r in valid), default=0)
        lex_bg_known_max = max((r["lexical"]["ko_bigram_known_ratio"] for r in valid if r["lexical"]["ko_bigram_total"] > 0), default=0.0)
        lex_total_real_words = sum(r["lexical"]["ko_real_word_count"] for r in valid)
        lex_at_least_1_real = sum(1 for r in valid if r["lexical"]["ko_real_word_count"] >= 1)
        # average bigram known ratio across trials with KO output
        bg_ratios = [r["lexical"]["ko_bigram_known_ratio"] for r in valid if r["lexical"]["ko_bigram_total"] >= 3]
        bg_avg = sum(bg_ratios) / max(1, len(bg_ratios))

        by_ckpt[entry["label"]] = {
            "n_total": len(valid),
            "n_gibberish": n_gib,
            "ko_ratio_max": round(ko_max, 4),
            "ko_count_max": ko_count_max,
            "ko_at_least_1": ko_at_least_1,
            "ko_at_least_5": ko_at_least_5,
            "ko_at_least_10": ko_at_least_10,
            "best_quality": round(best.get("quality", -1.0), 4) if best else None,
            "best_cfg": best.get("cfg") if best else None,
            "best_fmt": best.get("fmt") if best else None,
            "best_gen": best.get("gen") if best else None,
            "best_lexical": best.get("lexical") if best else None,
            # NEW lexical metrics
            "lexical_real_words_max": lex_real_words_max,
            "lexical_total_real_words": lex_total_real_words,
            "lexical_trials_with_real_word": lex_at_least_1_real,
            "lexical_bigram_known_max": round(lex_bg_known_max, 4),
            "lexical_bigram_known_avg": round(bg_avg, 4),
        }
        summary_line = (f"  ko_max={ko_max:.4f} ko_count_max={ko_count_max} "
                        f"ko≥1:{ko_at_least_1}/{len(valid)}  "
                        f"REAL_WORDS:max={lex_real_words_max} total={lex_total_real_words} trials_w_real={lex_at_least_1_real}  "
                        f"bg_known_avg={bg_avg:.3f}  best={best.get('cfg') if best else 'N/A'}/{best.get('fmt') if best else 'N/A'}")
        print(summary_line, flush=True)

    summary = {
        "wall_clock_s": round(time.time() - t_global, 2),
        "ko_dict_size": len(ko_words),
        "ko_bigram_size": len(ko_bigrams),
        "by_ckpt": by_ckpt,
        "comparison": {
            "pre_ft": by_ckpt.get("convo_5k_pre_ft"),
            "post_ft_initial": by_ckpt.get("convo_5k_ft_step_10000_initial"),
            "post_ft_extended": by_ckpt.get("convo_5k_ft_ext_step_20000_final"),
        },
    }

    out_json = OUT_DIR / "post_ft_ext_sampling.json"
    out_json.write_text(json.dumps(
        {"summary": summary, "by_ckpt_results": all_results},
        ensure_ascii=False, indent=2,
    ))
    print(f"\nSaved: {out_json}", flush=True)
    print(f"\n--- COMPARISON SUMMARY ---", flush=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
