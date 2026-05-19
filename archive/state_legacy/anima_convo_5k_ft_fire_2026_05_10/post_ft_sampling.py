"""Post-FT sampling test for convo_5k_ft (10K-step FT, 2026-05-10).

Mirrors anima_clm_v2_chat_ext_smoke_2026_05_10/run.py phase A + phase B-beam matrix
on the post-FT ckpt to compare KO/EN ratios against pre-FT baseline (KO=0%, EN ~45%).
"""
import sys
import json
import time
from pathlib import Path

import torch

sys.path.insert(
    0,
    "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09",
)
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_clm_v2_chat_ext_smoke_2026_05_10")

from forward_smoke import ConsciousLMReconstructed, text_to_byte_ids  # noqa: E402
import run as harness  # noqa: E402

OUT_DIR = Path(
    "/Users/ghost/core/anima/state/anima_convo_5k_ft_fire_2026_05_10"
)
OUT_DIR.mkdir(parents=True, exist_ok=True)

CKPTS = [
    {
        "label": "convo_5k_pre_ft",
        "path": "/Users/ghost/.cache/huggingface/hub/models--dancinlab--clm-v2-byte-18m-convo-5k/snapshots/1af2bcaeaf70c1d0b1a19939a8ada79a28f8cd30/convo_5k.pt",
    },
    {
        "label": "convo_5k_ft_step_5000",
        "path": str(OUT_DIR / "convo_5k_ft_step_5000.pt"),
    },
    {
        "label": "convo_5k_ft_step_10000",
        "path": str(OUT_DIR / "post_ft_ckpt.pt"),
    },
]


def main():
    t_global = time.time()
    all_results = {}
    by_ckpt = {}
    torch.manual_seed(42)

    for entry in CKPTS:
        print(f"\n=== {entry['label']} ===")
        t0 = time.time()
        model, meta = harness.load_model(entry["path"], n_head_hint=4)
        print(f"  loaded: {meta}  ({time.time()-t0:.1f}s)")

        t0 = time.time()
        res_a = harness.run_phase_a(model, entry["label"])
        print(f"  phase A done: {len(res_a)} trials  ({time.time()-t0:.1f}s)")

        t0 = time.time()
        res_b = harness.run_phase_b_beam(model, entry["label"])
        print(f"  phase B-beam done: {len(res_b)} trials  ({time.time()-t0:.1f}s)")

        results = res_a + res_b
        all_results[entry["label"]] = results

        # Per-ckpt summary
        valid = [r for r in results if "gen" in r]
        ko_max = max((r["scores"]["ko_ratio"] for r in valid), default=0.0)
        ko_count_max = max((r["scores"]["ko_count"] for r in valid), default=0)
        en_count_max = max((r["scores"]["en_count"] for r in valid), default=0)
        n_gib = sum(1 for r in valid if r.get("gibberish"))
        best = max(valid, key=lambda r: r.get("quality", -1.0), default=None)
        ko_at_least_1 = sum(1 for r in valid if r["scores"]["ko_count"] >= 1)
        ko_at_least_5 = sum(1 for r in valid if r["scores"]["ko_count"] >= 5)
        ko_at_least_10 = sum(1 for r in valid if r["scores"]["ko_count"] >= 10)

        by_ckpt[entry["label"]] = {
            "n_total": len(valid),
            "n_gibberish": n_gib,
            "ko_ratio_max": round(ko_max, 4),
            "ko_count_max": ko_count_max,
            "en_count_max": en_count_max,
            "ko_at_least_1": ko_at_least_1,
            "ko_at_least_5": ko_at_least_5,
            "ko_at_least_10": ko_at_least_10,
            "best_quality": round(best.get("quality", -1.0), 4) if best else None,
            "best_cfg": best.get("cfg") if best else None,
            "best_fmt": best.get("fmt") if best else None,
            "best_gen": best.get("gen") if best else None,
            "best_scores": best.get("scores") if best else None,
        }
        print(f"  ko_max={ko_max:.4f} ko_count_max={ko_count_max} ko≥1:{ko_at_least_1}/{len(valid)} best={best.get('cfg') if best else 'N/A'}/{best.get('fmt') if best else 'N/A'}")

    # overall comparison
    summary = {
        "wall_clock_s": round(time.time() - t_global, 2),
        "by_ckpt": by_ckpt,
        "comparison": {
            "pre_ft": by_ckpt.get("convo_5k_pre_ft"),
            "post_ft_step_10000": by_ckpt.get("convo_5k_ft_step_10000"),
            "ko_count_delta_pre_to_post": by_ckpt.get("convo_5k_ft_step_10000", {}).get("ko_count_max", 0)
            - by_ckpt.get("convo_5k_pre_ft", {}).get("ko_count_max", 0),
            "ko_ratio_delta_pre_to_post": round(
                by_ckpt.get("convo_5k_ft_step_10000", {}).get("ko_ratio_max", 0.0)
                - by_ckpt.get("convo_5k_pre_ft", {}).get("ko_ratio_max", 0.0),
                4,
            ),
        },
    }

    out_json = OUT_DIR / "post_ft_sampling.json"
    out_json.write_text(json.dumps(
        {"summary": summary, "by_ckpt_results": all_results},
        ensure_ascii=False,
        indent=2,
    ))
    print(f"\nSaved: {out_json}")
    print(f"\n--- COMPARISON SUMMARY ---")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
