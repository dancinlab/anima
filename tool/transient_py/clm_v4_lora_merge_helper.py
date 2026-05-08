#!/usr/bin/env python3
# .own 4 — opt-out per raw#9: tool/transient_py/ namespace
# raw#37 transient — Mac canonical = .hexa orchestration; this helper executes
# the CLM v4 LoRA adapter merge_and_unload extension that hexa cannot express
# directly. Sister: anima-core/runtime/clm_v4_mount.hexa.
# ──────────────────────────────────────────────────────────────────────────────
# clm_v4_lora_merge_helper.py — CLM v4 base + LoRA adapter merge_and_unload
#                               → merged HF model on local disk for clm_v4_mount
# ──────────────────────────────────────────────────────────────────────────────
# Source spec   : prompt 2026-05-08 "clm_v4_mount.hexa peft.merge_and_unload
#                 extension — CLM v4 LoRA variants real-mode measurement unblock"
# Source pattern: tool/anima_gguf_convert.py §4 (peft merge → save_pretrained)
# Generator     : HAND-WRITE (CLM v4 LoRA real-mode unblock cycle)
# Generated     : 2026-05-08
# Author        : Claude Opus 4.7 (CLM v4 LoRA real-mode unblock subagent)
# Retire-when   : (a) clm_v4_mount native LoRA path (peft loaded inline without
#                     materializing merged model on disk) lands in shim_v6, OR
#                 (b) HF publishes pre-merged variants of clm-v4-sft-1-7-y1 /
#                     clm-v4-sft-1-8 / clm-v4-paradigm-j (model.safetensors at
#                     repo root, no adapter_config.json), and clm_v4_mount's
#                     existing AutoModelForCausalLM path subsumes them.
# Namespace     : .own 4 — Mac-side transient .py for CLM v4 LoRA merge proxy.
# Policy        : raw#9 — this .py exists ONLY in tool/transient_py/ which is
#                 gitignored. Mac canonical = .hexa. Human edits = raw violation;
#                 regenerate from spec instead. Execution: clm_v4_mount.hexa
#                 spawns this on adapter_config.json detection.
#
# PIPELINE (per LoRA repo)
#   1. snapshot_download(adapter_repo)         → adapter_config + adapter_model
#   2. read adapter_config.json                → base_model_name_or_path (or
#                                                fallback "dancinlab/clm-v4-mk2-v1"
#                                                when null, per peft auto_mapping)
#   3. snapshot_download(base_model)           → base + modeling_clm_v4.py
#   4. AutoModelForCausalLM.from_pretrained(base, trust_remote_code=True)
#   5. PeftModel.from_pretrained(base, adapter)
#   6. merge_and_unload()                      → merged HF model (in-memory)
#   7. save_pretrained(merged_dir)             → safetensors + config + modeling
#   8. tokenizer copy from base snapshot       → tokenizer_64k_multilingual.model
#   9. emit merged path to stdout              → clm_v4_mount consumes
#
# OUTPUT CACHE
#   ~/.cache/anima/clm_v4_merged/<adapter-repo-with-slash-replaced>/
#   └── config.json
#   └── configuration_clm_v4.py
#   └── modeling_clm_v4.py
#   └── decoder_v3.py
#   └── conscious_decoder.py
#   └── model.safetensors
#   └── tokenizer_64k_multilingual.model
#   └── (jvae_heads.pt copied verbatim if present in adapter repo)
#   └── _ANIMA_MERGE_MANIFEST.json (provenance: adapter sha + base sha + ts)
#
# C3 (raw#10)
#   C1 merge materializes a fresh on-disk model — adapter LoRA weights are
#      baked into base linear layers. Original adapter repo is preserved.
#   C2 base_model fallback "dancinlab/clm-v4-mk2-v1" applies when adapter_config
#      base_model_name_or_path is null (the case for current clm-v4-sft-1-* /
#      paradigm-j repos). If user trains a LoRA on a different base, override
#      via --base-model flag.
#   C3 jvae_heads.pt (paradigm-j only) is copied verbatim — NOT merged into
#      the decoder weights. Downstream consumers must load it separately.
#   C4 merged cache hits avoid re-merging; --force overrides. Cache key =
#      adapter repo string only (base implied). If base changes, --force.
#   C5 cache lives in ~/.cache/anima/clm_v4_merged/ (NOT ~/.cache/huggingface)
#      — explicitly anima-local, ledger-tracked.
#
# USAGE
#   clm_v4_lora_merge_helper.py --adapter-repo dancinlab/clm-v4-sft-1-7-y1-stage1
#   clm_v4_lora_merge_helper.py --adapter-repo R --base-model B --force
#   clm_v4_lora_merge_helper.py --check-only --adapter-repo R   # detect only
#
# OUTPUT (stdout)
#   __ANIMA_CLM_V4_LORA_MERGED__ path=<merged_dir> adapter=<repo> base=<repo>

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

DEFAULT_BASE = "dancinlab/clm-v4-mk2-v1"
DEFAULT_CACHE = Path.home() / ".cache" / "anima" / "clm_v4_merged"


def _eprint(*a, **kw):
    kw.setdefault("file", sys.stderr)
    print(*a, **kw)


def _emit(tag: str, **kw) -> None:
    sys.stdout.write("__ANIMA_" + tag + "__")
    for k, v in kw.items():
        sys.stdout.write(f" {k}={v}")
    sys.stdout.write("\n")
    sys.stdout.flush()


def _adapter_cache_key(adapter_repo: str) -> str:
    return adapter_repo.replace("/", "__")


def _resolve_adapter_config(adapter_dir: Path) -> dict:
    cfg_path = adapter_dir / "adapter_config.json"
    if not cfg_path.is_file():
        raise SystemExit(
            f"[clm_v4_lora_merge] adapter_config.json missing in {adapter_dir}"
        )
    return json.loads(cfg_path.read_text(encoding="utf-8"))


def _resolve_hf_snapshot(repo_id: str) -> Path | None:
    """Find HF cache snapshot dir for a given repo_id (no download)."""
    cache_root = Path(
        os.environ.get("HF_HOME", str(Path.home() / ".cache" / "huggingface"))
    )
    hub = cache_root / "hub"
    repo_dir = hub / ("models--" + repo_id.replace("/", "--"))
    snap_dir = repo_dir / "snapshots"
    if not snap_dir.is_dir():
        return None
    snaps = sorted(snap_dir.iterdir())
    return snaps[-1] if snaps else None


def _ensure_full_snapshot(repo_id: str, target_files: list[str]) -> Path:
    """Snapshot-download repo_id ensuring `target_files` are all present.

    Uses huggingface_hub.snapshot_download to fetch missing blobs. Returns
    the resolved snapshot directory path.
    """
    snap = _resolve_hf_snapshot(repo_id)
    if snap is not None and all((snap / f).exists() for f in target_files):
        return snap
    try:
        from huggingface_hub import snapshot_download  # type: ignore
    except Exception as ex:
        raise SystemExit(
            f"[clm_v4_lora_merge] huggingface_hub import failed: {ex}"
        )
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    _eprint(f"[clm_v4_lora_merge] snapshot_download {repo_id} (target={target_files})")
    snapshot_download(repo_id=repo_id, token=token)
    snap = _resolve_hf_snapshot(repo_id)
    if snap is None:
        raise SystemExit(
            f"[clm_v4_lora_merge] snapshot_download succeeded but cache snapshot not found for {repo_id}"
        )
    missing = [f for f in target_files if not (snap / f).exists()]
    if missing:
        raise SystemExit(
            f"[clm_v4_lora_merge] missing files after download: {missing}"
        )
    return snap


def _copy_modeling_files(base_snap: Path, dst: Path) -> list[str]:
    copied = []
    for fname in (
        "modeling_clm_v4.py",
        "configuration_clm_v4.py",
        "decoder_v3.py",
        "conscious_decoder.py",
        "tokenizer_64k_multilingual.model",
    ):
        src = base_snap / fname
        if src.exists():
            shutil.copy2(src, dst / fname)
            copied.append(fname)
    return copied


def _copy_extra_adapter_assets(adapter_snap: Path, dst: Path) -> list[str]:
    """Adapter-only sidecar files preserved verbatim (e.g., jvae_heads.pt)."""
    copied = []
    for fname in ("jvae_heads.pt",):
        src = adapter_snap / fname
        if src.exists():
            shutil.copy2(src, dst / fname)
            copied.append(fname)
    return copied


def _do_merge(adapter_repo: str, base_model: str, merged_dir: Path) -> dict:
    try:
        import torch  # type: ignore
        from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore
        from peft import PeftModel  # type: ignore
    except Exception as ex:
        raise SystemExit(
            f"[clm_v4_lora_merge] missing deps (torch/transformers/peft): {ex}"
        )

    base_snap = _ensure_full_snapshot(
        base_model,
        target_files=["config.json", "model.safetensors", "modeling_clm_v4.py"],
    )
    adapter_snap = _ensure_full_snapshot(
        adapter_repo,
        target_files=["adapter_config.json", "adapter_model.safetensors"],
    )

    _eprint(f"[clm_v4_lora_merge] base snap = {base_snap}")
    _eprint(f"[clm_v4_lora_merge] adapter snap = {adapter_snap}")

    _eprint("[clm_v4_lora_merge] loading base AutoModelForCausalLM (trust_remote_code)")
    base_obj = AutoModelForCausalLM.from_pretrained(
        str(base_snap), trust_remote_code=True, torch_dtype=torch.float32
    )

    _eprint("[clm_v4_lora_merge] loading PEFT adapter")
    # Capture adapter target-module-mismatch warnings (peft emits a warnings.warn
    # when adapter_config target_modules don't resolve in the base model — e.g.
    # adapter_config says "q_proj" but the base uses "attn.q_proj". When 100% of
    # the adapter keys are missing, the merge is a structural no-op (= base only)
    # and we record this as merge_no_op = True in the manifest for honest C3.
    import warnings
    captured = []
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        peft_obj = PeftModel.from_pretrained(base_obj, str(adapter_snap))
        for w in ws:
            msg = str(w.message)
            if "missing adapter keys" in msg.lower() or "missing_keys" in msg:
                captured.append(msg)
    merge_no_op = bool(captured)

    _eprint("[clm_v4_lora_merge] merge_and_unload()")
    merged = peft_obj.merge_and_unload()

    if merged_dir.exists():
        shutil.rmtree(merged_dir)
    merged_dir.mkdir(parents=True, exist_ok=True)
    _eprint(f"[clm_v4_lora_merge] save_pretrained {merged_dir} (safe_serialization=False due to weight-tying)")
    # CLM v4 ties tok_emb <-> head_a: safe_serialization=True rejects shared
    # tensors. Use legacy pickle format (.bin) which preserves tying.
    merged.save_pretrained(str(merged_dir), safe_serialization=False)

    copied_modeling = _copy_modeling_files(base_snap, merged_dir)
    copied_extra = _copy_extra_adapter_assets(adapter_snap, merged_dir)

    manifest = {
        "schema": "anima.clm_v4_lora_merge.manifest.v1",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "adapter_repo": adapter_repo,
        "adapter_snapshot": str(adapter_snap),
        "base_model": base_model,
        "base_snapshot": str(base_snap),
        "modeling_files_copied": copied_modeling,
        "extra_adapter_assets": copied_extra,
        "merged_dir": str(merged_dir),
        "merge_no_op": merge_no_op,
        "merge_no_op_warning_excerpt": (captured[0][:240] + "...") if captured else "",
        "policy": {
            "raw_9": "hexa-only orchestration via clm_v4_mount.hexa",
            "raw_37": "transient_py merge helper (this file)",
            "own_4": "opt-out namespace tool/transient_py/",
        },
    }
    (merged_dir / "_ANIMA_MERGE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    # Free torch refs
    del merged, peft_obj, base_obj
    try:
        import gc  # type: ignore
        gc.collect()
    except Exception:
        pass

    return manifest


def _check_only(adapter_repo: str) -> dict:
    snap = _resolve_hf_snapshot(adapter_repo)
    has_cfg = bool(snap and (snap / "adapter_config.json").exists())
    has_weights = bool(snap and (snap / "adapter_model.safetensors").exists())
    base_model = None
    if has_cfg:
        try:
            cfg = _resolve_adapter_config(snap)
            base_model = cfg.get("base_model_name_or_path")
        except Exception:
            pass
    return {
        "adapter_repo": adapter_repo,
        "snapshot": str(snap) if snap else None,
        "has_adapter_config": has_cfg,
        "has_adapter_weights": has_weights,
        "base_model_from_config": base_model,
        "base_model_resolved": base_model or DEFAULT_BASE,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="CLM v4 LoRA merge_and_unload helper")
    ap.add_argument("--adapter-repo", required=True, help="HF repo id of LoRA adapter")
    ap.add_argument(
        "--base-model",
        default=DEFAULT_BASE,
        help=f"HF repo id of base model (default {DEFAULT_BASE} when adapter_config base_model_name_or_path is null)",
    )
    ap.add_argument(
        "--cache-root",
        default=str(DEFAULT_CACHE),
        help="anima-local cache root for merged models",
    )
    ap.add_argument("--force", action="store_true", help="re-merge even if cached")
    ap.add_argument(
        "--check-only",
        action="store_true",
        help="report adapter cache + config detection only; no download/merge",
    )
    args = ap.parse_args()

    if args.check_only:
        report = _check_only(args.adapter_repo)
        sys.stdout.write(json.dumps(report) + "\n")
        return 0

    # Resolve base model: adapter_config base_model_name_or_path > --base-model
    # Pre-resolve via cached config if available; fallback to download chain.
    snap = _resolve_hf_snapshot(args.adapter_repo)
    base_model = args.base_model
    if snap is not None and (snap / "adapter_config.json").exists():
        try:
            cfg = _resolve_adapter_config(snap)
            cfg_base = cfg.get("base_model_name_or_path")
            if cfg_base:
                base_model = cfg_base
        except Exception:
            pass

    cache_root = Path(args.cache_root)
    cache_root.mkdir(parents=True, exist_ok=True)
    merged_dir = cache_root / _adapter_cache_key(args.adapter_repo)

    manifest_path = merged_dir / "_ANIMA_MERGE_MANIFEST.json"
    if manifest_path.is_file() and not args.force:
        _eprint(f"[clm_v4_lora_merge] cache hit: {merged_dir} (use --force to re-merge)")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        _emit(
            "CLM_V4_LORA_MERGED",
            path=manifest.get("merged_dir", str(merged_dir)),
            adapter=manifest.get("adapter_repo", args.adapter_repo),
            base=manifest.get("base_model", base_model),
            cache="hit",
        )
        return 0

    manifest = _do_merge(args.adapter_repo, base_model, merged_dir)
    _emit(
        "CLM_V4_LORA_MERGED",
        path=manifest["merged_dir"],
        adapter=manifest["adapter_repo"],
        base=manifest["base_model"],
        cache="fresh",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
