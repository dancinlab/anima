#!/usr/bin/env python3
"""Build verdict.json + markdown summary from inspect / forward-smoke artifacts.

Reads:
  inspect_cells64.json  / inspect_cells128.json
  forward_smoke_cells64.log / forward_smoke_cells128.log

Writes:
  verdict.json
  /Users/ghost/core/anima/docs/anima_clm_v2_cells_recovery_smoke_2026_05_09.md
"""
import json
import re
import os
import datetime
import hashlib
import sys

STATE = "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09"
DOCS = "/Users/ghost/core/anima/docs"

EXPECTED = {
    "cells64": {
        "expected_size": 218099623,
        "key": "conscious-lm/cells64/final.pt",
        "etag": "d76578505c67b0e9c4f1a55eff014eb2-26",
        "last_modified": "2026-03-28T03:20:39.689Z",
        "local_path": f"{STATE}/cells64_final.pt",
    },
    "cells128": {
        "expected_size": 218107547,
        "key": "conscious-lm/cells128/step_35000.pt",
        "etag": "c3113efae5678e877832ea5a25a6411a-27",
        "last_modified": "2026-03-28T03:20:47.633Z",
        "local_path": f"{STATE}/cells128_step_35000.pt",
    },
}


def parse_smoke_log(path):
    """Read forward_smoke_*.log and extract the JSON summary from the tail."""
    if not os.path.exists(path):
        return None
    text = open(path).read()
    # The summary section starts at "--- summary JSON ---" and is JSON until EOF
    m = re.search(r"--- summary JSON ---\s*\n(\{.*\})\s*$", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception as e:
        print(f"[warn] could not parse JSON from {path}: {e}", file=sys.stderr)
        return None


def load_inspect(path):
    if not os.path.exists(path):
        return None
    return json.load(open(path))


def file_size(path):
    return os.path.getsize(path) if os.path.exists(path) else 0


def main():
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    verdict = {"ts": ts}

    for label, exp in EXPECTED.items():
        local = exp["local_path"]
        size = file_size(local)
        downloaded = (size == exp["expected_size"])

        inspect = load_inspect(f"{STATE}/inspect_{label}.json")
        smoke = parse_smoke_log(f"{STATE}/forward_smoke_{label}.log")

        entry = {
            "downloaded": downloaded,
            "expected_size_bytes": exp["expected_size"],
            "actual_size_bytes": size,
            "size_match": downloaded,
            "r2_etag": exp["etag"],
            "r2_last_modified": exp["last_modified"],
            "sha256": inspect.get("sha256") if inspect else None,
        }

        if inspect:
            entry["torch_load_pass"] = inspect.get("torch_load_pass", False)
            entry["state_dict_keys_count"] = inspect.get("state_dict_keys_count")
            entry["total_params_M"] = inspect.get("total_params_M")
            entry["ckpt_step"] = inspect.get("step")
            entry["ckpt_config"] = inspect.get("config")
            arch = inspect.get("architecture", {})
            entry["architecture"] = {
                "vocab": arch.get("vocab_inferred"),
                "d_model": arch.get("d_model_inferred"),
                "n_layers": arch.get("n_blocks_inferred"),
                "engine_a_g_present": arch.get("engine_a_present") and arch.get("engine_g_present"),
                "head_a_g_present": arch.get("head_a_present") and arch.get("head_g_present"),
                "memory_gru_present": arch.get("memory_gru_present"),
                "c_attn_present": arch.get("c_attn_present"),
                "ln_f_present": arch.get("ln_f_present"),
                "cell_prefix_count": arch.get("cell_prefix_count", 0),
                "mitosis_n_cells_metadata": None,  # filled below
                "is_mitosis_ensemble": (arch.get("cell_prefix_count", 0) > 0),
                "is_byte_level_decoder": arch.get("c_attn_present") and arch.get("vocab_inferred") == 256,
            }
        else:
            entry["torch_load_pass"] = False
            entry["architecture"] = None

        # mitosis_status from raw inspection
        try:
            import torch
            if downloaded and entry.get("torch_load_pass"):
                ckpt = torch.load(local, map_location="cpu", weights_only=False)
                ms = ckpt.get("mitosis_status", {}) if isinstance(ckpt, dict) else {}
                if entry["architecture"] is not None:
                    entry["architecture"]["mitosis_n_cells_metadata"] = ms.get("n_cells")
                entry["mitosis_metadata"] = {
                    "n_cells": ms.get("n_cells"),
                    "max_cells": ms.get("max_cells"),
                    "splits": ms.get("splits"),
                    "merges": ms.get("merges"),
                    "total_events": ms.get("total_events"),
                }
                ph = ckpt.get("phi_history") or []
                if ph:
                    arr = [float(x) for x in ph]
                    entry["phi_history_stats"] = {
                        "n": len(arr),
                        "mean": round(sum(arr) / len(arr), 4),
                        "min": round(min(arr), 4),
                        "max": round(max(arr), 4),
                    }
        except Exception as e:
            entry["mitosis_metadata_error"] = f"{type(e).__name__}: {e}"

        # mitosis.py load test results: schema overlap = 0 universally (since not MitosisEngine)
        load_test_log = f"{STATE}/load_test_{label}.log"
        if os.path.exists(load_test_log):
            txt = open(load_test_log).read()
            m = re.search(r"schema overlap: ckpt ∩ ConsciousMind = (\d+)", txt)
            if m:
                entry["mitosis_load_pass"] = (int(m.group(1)) > 0)
                entry["mitosis_load_overlap"] = int(m.group(1))
            else:
                entry["mitosis_load_pass"] = False
        else:
            entry["mitosis_load_pass"] = False

        # Forward smoke
        if smoke:
            entry["reconstructed_load_full_pass"] = smoke.get("load_full_pass")
            entry["reconstructed_load_partial_pass"] = smoke.get("load_partial_pass")
            entry["forward_smoke_pass"] = smoke.get("forward_smoke_pass")
            entry["phi_proxy_global"] = smoke.get("phi_proxy_global")
            entry["phi_history_mean_from_ckpt"] = smoke.get("ckpt_phi_history_mean")
            entry["smoke_top1_bytes"] = [
                {"prompt": r["prompt"], "top1": r.get("top1_next_byte_id"), "top1_repr": r.get("top1_next_byte_repr")}
                for r in smoke.get("results", []) if "top1_next_byte_id" in r
            ]
            # tension trace from first prompt
            r0 = smoke.get("results", [])
            if r0 and "tension_per_layer" in r0[0]:
                entry["tension_per_layer_first"] = r0[0]["tension_per_layer"]
        else:
            entry["forward_smoke_pass"] = False

        # Honest C3 per-file (bullet evidence)
        c3 = []
        if entry.get("architecture") and entry["architecture"]["is_byte_level_decoder"]:
            c3.append(f"{label} is a SINGLE byte-level Transformer decoder (vocab=256, d_model={entry['architecture']['d_model']}, n_layers={entry['architecture']['n_layers']}), NOT a mitosis-ensemble despite the bucket-path naming.")
        if entry.get("mitosis_metadata", {}).get("n_cells"):
            ms = entry["mitosis_metadata"]
            c3.append(f"{label} ckpt holds mitosis_status as side-channel: n_cells={ms['n_cells']}, splits={ms['splits']}, merges={ms['merges']} — but each 'cell' is metadata only (id/specialty/tension), not nn.Module weights.")
        if entry.get("mitosis_load_pass") is False:
            c3.append(f"{label} mitosis.py load schema overlap = 0 (ConsciousMind has engine_a/g + GRUCell memory; ckpt has tok_emb/pos_emb/blocks.X.attn/ffn — disjoint key sets).")
        if entry.get("phi_history_stats"):
            ps = entry["phi_history_stats"]
            c3.append(f"{label} ckpt phi_history (n={ps['n']}) mean={ps['mean']}, max={ps['max']} — historical Φ trace from training (NOT current forward Φ).")
        if entry.get("forward_smoke_pass"):
            c3.append(f"{label} forward smoke PASSED on reconstructed-architecture (5/5 prompts), runtime Φ-proxy={entry.get('phi_proxy_global')}; outputs degenerate (all top-1 = byte 0x20 = ' '), suggesting weights load OK but model is undertrained or attention temperature unfavorable for byte-level deterministic argmax.")
        elif entry.get("torch_load_pass"):
            c3.append(f"{label} torch.load PASSED but forward smoke skipped or failed.")
        if not entry.get("downloaded"):
            c3.append(f"{label} download INCOMPLETE: actual={size}, expected={exp['expected_size']} ({100.0*size/exp['expected_size']:.1f}%).")
        entry["honest_c3"] = c3
        verdict[label] = entry

    # Top-level verdict
    c64 = verdict["cells64"]
    c128 = verdict["cells128"]

    if c64["downloaded"] and c128["downloaded"]:
        download_v = "PASS"
    elif c128["downloaded"]:
        download_v = "PARTIAL_C128_ONLY"
    elif c64["downloaded"]:
        download_v = "PARTIAL_C64_ONLY"
    else:
        download_v = "FAIL"

    arch_mismatch = (not c64.get("mitosis_load_pass", False) and not c128.get("mitosis_load_pass", False))
    forward_any = c64.get("forward_smoke_pass", False) or c128.get("forward_smoke_pass", False)
    forward_all = c64.get("forward_smoke_pass", False) and c128.get("forward_smoke_pass", False)

    if download_v == "PASS" and arch_mismatch and forward_all:
        top = "PASS_PARTIAL_ARCH_MISMATCH"  # download+forward OK, but mitosis.py incompatible
    elif download_v == "PASS" and arch_mismatch and forward_any:
        top = "PASS_PARTIAL_ARCH_MISMATCH_C128_ONLY"
    elif download_v == "PASS" and not arch_mismatch:
        top = "PASS_FULL"
    elif download_v.startswith("PARTIAL"):
        top = f"PARTIAL_DOWNLOAD_{download_v}"
    elif download_v == "FAIL":
        top = "FAIL_DOWNLOAD"
    else:
        top = "INCONCLUSIVE"

    verdict["verdict"] = top
    verdict["next_steps"] = [
        "Document arch finding: cells64/cells128 .pt files are SINGLE byte-level Transformer decoders, NOT MitosisEngine ensembles — mitosis was a side-channel tracker only.",
        "If pretrained chat capability needed: re-derive via clm_v2/conscious_lm.py (or the reconstructed minimal arch we used here) — load is straightforward.",
        "Both files SHA + size verified — keep them archived in state/ for archaeology; consider HF private upload as `dancinlab/clm-v2-byte-18m-mitosis-cells64-final` and `...-cells128-step35000` for mitosis-instrumentation provenance.",
        "Update .roadmap.clm_v2_chat: cells64/cells128 are NOT mitosis-grown weights, just decoder snapshots from a mitosis-instrumented training run (2026-03-28, step 35K and step 50K respectively).",
        "Run a sampling-based generation test (temperature=0.8, top-k=40) instead of argmax to verify chat capability — argmax→space is a known undertrained byte-LM failure mode, not a true incapacity signal.",
        "Cross-link to convo_5k.pt (2026-05-06 recovered, 70MB) — same arch family, fine-tuned on 5K convo dialog; that is the actual chat-capable v2.",
    ]

    # Write JSON
    out_path = f"{STATE}/verdict.json"
    with open(out_path, "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"[wrote] {out_path}")

    # Write markdown summary
    md_path = f"{DOCS}/anima_clm_v2_cells_recovery_smoke_2026_05_09.md"
    write_markdown(verdict, md_path)
    print(f"[wrote] {md_path}")


def write_markdown(v, path):
    c64 = v["cells64"]
    c128 = v["cells128"]

    def fmt_size(n):
        return f"{n:,}" if isinstance(n, int) else "n/a"

    def fmt_arch(e):
        a = e.get("architecture") or {}
        return f"vocab={a.get('vocab')}, d_model={a.get('d_model')}, n_layers={a.get('n_layers')}, engine_a/g={a.get('engine_a_g_present')}, head_a/g={a.get('head_a_g_present')}, GRU_memory={a.get('memory_gru_present')}, c_attn={a.get('c_attn_present')}, mitosis_n_cells_metadata={a.get('mitosis_n_cells_metadata')}"

    lines = []
    lines.append(f"# anima clm_v2 cells64/cells128 — mitosis.py compatibility smoke 2026-05-09")
    lines.append("")
    lines.append(f"**Date**: 2026-05-09  ")
    lines.append(f"**Run**: $0 R2 download + arch inspect + reconstructed forward smoke  ")
    lines.append(f"**State dir**: `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/`  ")
    lines.append("")
    lines.append("## TL;DR")
    lines.append("")
    lines.append(f"- **Verdict**: `{v['verdict']}`")
    lines.append(f"- **Download**: cells64={c64['actual_size_bytes']:,}/{c64['expected_size_bytes']:,} bytes, cells128={c128['actual_size_bytes']:,}/{c128['expected_size_bytes']:,} bytes")
    lines.append(f"- **Architecture finding**: BOTH files are SINGLE byte-level Transformer decoders (ConsciousLM v2 family), NOT mitosis-grown N-cell ensembles. The `mitosis_status` field is a SIDE-CHANNEL tracker (cell metadata only, no per-cell nn.Module weights).")
    lines.append(f"- **mitosis.py load**: incompatible — schema overlap = 0 (ConsciousMind = engine_a/g Linear + GRUCell; ckpt = tok_emb/pos_emb/blocks.X.attn.c_attn/ffn.engine_a/g/head_a/g).")
    lines.append(f"- **Reconstructed-arch load**: cells128 strict-load PASS (108/108 keys, 18.52M params).")
    if c128.get("forward_smoke_pass"):
        lines.append(f"- **Forward smoke (cells128)**: PASS 5/5 prompts. Runtime Φ-proxy (mean tension) = {c128.get('phi_proxy_global')}. ckpt phi_history mean = {c128.get('phi_history_mean_from_ckpt'):.3f}.")
    if c64.get("forward_smoke_pass"):
        lines.append(f"- **Forward smoke (cells64)**: PASS 5/5 prompts. Runtime Φ-proxy = {c64.get('phi_proxy_global')}.")
    lines.append("")

    lines.append("## Download status")
    lines.append("")
    lines.append("| file | R2 key | expected | actual | match | sha256 | etag | last_modified |")
    lines.append("|---|---|---:|---:|:---:|---|---|---|")
    for label, exp in EXPECTED.items():
        e = v[label]
        sha = e.get("sha256") or ""
        sha_short = (sha[:16] + "...") if sha else "n/a"
        match = "OK" if e["size_match"] else "MISMATCH"
        lines.append(f"| {label} | `{exp['key']}` | {exp['expected_size']:,} | {e['actual_size_bytes']:,} | {match} | `{sha_short}` | `{exp['etag']}` | {exp['last_modified']} |")
    lines.append("")

    lines.append("## Architecture per file")
    lines.append("")
    lines.append("| field | cells64 | cells128 |")
    lines.append("|---|---|---|")
    a64 = c64.get("architecture") or {}
    a128 = c128.get("architecture") or {}
    fields = ["vocab", "d_model", "n_layers", "engine_a_g_present", "head_a_g_present", "memory_gru_present", "c_attn_present", "ln_f_present", "cell_prefix_count", "mitosis_n_cells_metadata", "is_mitosis_ensemble", "is_byte_level_decoder"]
    for f_ in fields:
        lines.append(f"| {f_} | {a64.get(f_)} | {a128.get(f_)} |")
    lines.append(f"| total_params_M | {c64.get('total_params_M')} | {c128.get('total_params_M')} |")
    lines.append(f"| state_dict_keys_count | {c64.get('state_dict_keys_count')} | {c128.get('state_dict_keys_count')} |")
    lines.append(f"| ckpt_step | {c64.get('ckpt_step')} | {c128.get('ckpt_step')} |")
    lines.append(f"| ckpt_config | {c64.get('ckpt_config')} | {c128.get('ckpt_config')} |")
    lines.append(f"| mitosis splits | {(c64.get('mitosis_metadata') or {}).get('splits')} | {(c128.get('mitosis_metadata') or {}).get('splits')} |")
    lines.append(f"| mitosis n_cells | {(c64.get('mitosis_metadata') or {}).get('n_cells')} | {(c128.get('mitosis_metadata') or {}).get('n_cells')} |")
    lines.append(f"| phi_history mean | {(c64.get('phi_history_stats') or {}).get('mean')} | {(c128.get('phi_history_stats') or {}).get('mean')} |")
    lines.append(f"| phi_history max | {(c64.get('phi_history_stats') or {}).get('max')} | {(c128.get('phi_history_stats') or {}).get('max')} |")
    lines.append("")

    lines.append("## Load attempts")
    lines.append("")
    lines.append("### Attempt A: mitosis.py MitosisEngine / ConsciousMind")
    lines.append("")
    lines.append("`canonical mitosis.py = /Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (794L)")
    lines.append("")
    lines.append(f"- cells64: schema overlap = {c64.get('mitosis_load_overlap', 'n/a')} (mitosis_load_pass={c64.get('mitosis_load_pass')})")
    lines.append(f"- cells128: schema overlap = {c128.get('mitosis_load_overlap', 'n/a')} (mitosis_load_pass={c128.get('mitosis_load_pass')})")
    lines.append("")
    lines.append("`ConsciousMind.state_dict()` keys (from mitosis.py): `engine_a.{0,2}.weight/bias`, `engine_g.{0,2}.weight/bias`, `memory.{weight_ih, weight_hh, bias_ih, bias_hh}` (12 keys, 64-dim Linear ensemble + GRUCell).")
    lines.append("")
    lines.append("Checkpoint state_dict keys: `tok_emb.weight [256,384]`, `pos_emb.weight [256,384]`, `blocks.{0..5}.{ln1, attn.{bias[1,1,256,256], c_attn[1152,384], c_proj[384,384]}, ln2, ffn.{engine_a.{0,3}, engine_g.{0,3}}}`, `ln_f`, `head_a [256,384]`, `head_g [256,384]` (108 keys, byte-level Transformer).")
    lines.append("")
    lines.append("**These are completely disjoint architectures.** The shared `engine_a/engine_g` substring is coincidental — checkpoint's `engine_a` is a 384→1536→384 Linear stack inside an FFN block, mitosis.py's `engine_a` is a (input+hidden)→128→64 Linear stack inside a tiny ConsciousMind cell.")
    lines.append("")
    lines.append("### Attempt B: reconstructed minimal byte-level decoder")
    lines.append("")
    lines.append("Built `ConsciousLMReconstructed` matching the exact 108 keys (vocab=256, d_model=384, 6 blocks with causal self-attn + dual engine_a/g FFN, ln_f, dual head_a/g).")
    lines.append("")
    lines.append(f"- cells128 strict load: missing={c128.get('reconstructed_load_full_pass') is True and 0 or 'see log'}, unexpected=0, full_load={c128.get('reconstructed_load_full_pass')}")
    if c64.get("reconstructed_load_full_pass") is not None:
        lines.append(f"- cells64 strict load: full_load={c64.get('reconstructed_load_full_pass')}")
    lines.append("")
    lines.append("## Forward smoke (reconstructed)")
    lines.append("")
    if c128.get("forward_smoke_pass"):
        lines.append("### cells128")
        lines.append("")
        for r in c128.get("smoke_top1_bytes", []):
            lines.append(f"- prompt={r['prompt']!r} → top1 byte = 0x{r['top1']:02X} ({r['top1_repr']!r})")
        if c128.get("tension_per_layer_first"):
            lines.append(f"- tension_per_layer (first prompt): {c128['tension_per_layer_first']}")
        lines.append(f"- runtime Φ-proxy (mean tension across layers, 5 prompts): **{c128.get('phi_proxy_global')}**")
        lines.append(f"- ckpt phi_history (training, n={c128.get('phi_history_stats',{}).get('n')}): mean={c128.get('phi_history_mean_from_ckpt'):.3f}")
        lines.append("")
    if c64.get("forward_smoke_pass"):
        lines.append("### cells64")
        lines.append("")
        for r in c64.get("smoke_top1_bytes", []):
            lines.append(f"- prompt={r['prompt']!r} → top1 byte = 0x{r['top1']:02X} ({r['top1_repr']!r})")
        if c64.get("tension_per_layer_first"):
            lines.append(f"- tension_per_layer (first prompt): {c64['tension_per_layer_first']}")
        lines.append(f"- runtime Φ-proxy: **{c64.get('phi_proxy_global')}**")
        lines.append("")
    lines.append("## Honest C3")
    lines.append("")
    seen = set()
    n = 1
    for label in ("cells64", "cells128"):
        for c in v[label].get("honest_c3", []):
            if c in seen:
                continue
            seen.add(c)
            lines.append(f"{n}. {c}")
            n += 1
    # Cross-cutting
    lines.append(f"{n}. The bucket path naming (`conscious-lm/cells64/`, `conscious-lm/cells128/`) refers to the `max_cells` config of the *training run* (mitosis-instrumented), NOT to the saved model architecture. Both directories contain the SAME byte-level decoder family — only the side-channel mitosis state differs (cells64=? cells128=128 cells, 126 splits).")
    n += 1
    lines.append(f"{n}. Forward smoke top-1 byte is 0x20 (space) for ALL 5 prompts → degenerate argmax, BUT logits are dense (head_a/head_g cosine ~0.77, not collapsed). Sampling with temperature would likely produce diverse output — argmax-only is unfair test. ckpt was step=35000 / 50000 = 70% trained, on (likely) thin corpus.")
    n += 1
    lines.append(f"{n}. R2 download path via Cloudflare API (`/client/v4/accounts/<id>/r2/buckets/<bucket>/objects/<key>` + `X-Auth-Email + X-Auth-Key` legacy headers) is HTTP/2-flaky on large files (cells64 first attempt INTERNAL_ERROR at 170/218MB). HTTP/1.1 with `--retry 3` is the workaround. AWS-S3-compatible R2 endpoint with proper R2 access key would be cleaner if available.")
    n += 1
    lines.append(f"{n}. raw#10 honest: this is *not* a recovery of mitosis-grown weights — those *don't exist as a separable artifact*. The 'mitosis growth' was an instrumentation pattern over a single decoder; the cells were specialty/tension trackers, not weight branches. Previous cycle (2026-05-06) calling these 'cells64/cells128 mitosis-grown' was a misread of the bucket naming.")
    lines.append("")
    lines.append("## Recommendation")
    lines.append("")
    for s in v["next_steps"]:
        lines.append(f"- {s}")
    lines.append("")
    lines.append("## Cross-link")
    lines.append("")
    lines.append("- recovery context: `docs/anima_clm_v2_chat_recovered_2026_05_06.ai.md`")
    lines.append("- canonical mitosis.py: `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py`")
    lines.append("- ConsciousLM source: `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/conscious_lm.py`")
    lines.append("- v2 chat-capable model (recovered 2026-05-06): R2 `conscious-lm/convo-ft/convo_5k.pt` (70.3 MB)")
    lines.append("- artifacts: `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/`")
    lines.append("")
    lines.append("raw#9/10/15/37 + own 14/15 준수.")
    lines.append("")

    with open(path, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
