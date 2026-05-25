#!/usr/bin/env python3
"""pt_to_flame_farr_export.py — anima downstream helper for Clause A
of hexa-lang inbox patch `pt-ckpt-cross-substrate-residual-readout.md`
(2026-05-20).

Exports a PyTorch .pt checkpoint into the `flame-mc-manifest/0.1`
sidecar format consumed by `stdlib/flame/flame_load_pt.hexa`. The
PyTorch pickle is parsed here (Python ecosystem) so hexa-lang does
NOT need a native pickle parser — that's the whole point of the
manifest+per-tensor-.farr sidecar design.

Output layout:
  <out_dir>/
    manifest.json                       (flame-mc-manifest/0.1)
    tok_emb.weight.farr                 (raw f32 little-endian)
    head_a.weight.farr
    ...
    blocks_0_attn_q_proj_weight.farr    (slashes → underscores)
    ...

Honest scope (anima downstream-consumer per g_train_flame_not_pytorch):
  - This helper exports the MAPPABLE BACKBONE subset only (matches
    flame Path-A `m_total` layout — see decoder_lib.hexa).
  - PureFieldFFN-vs-SwiGLU + dual head_g + MoE = UNMAPPED (honestly
    listed in manifest.honest_unmapped[]).
  - BF16 weights are converted to f32 (RFC 031 path on hexa-lang
    side can still consume f32 .farr; bf16 .farr support deferred
    to Phase 2 + RFC 031 reuse).

F-PTLOAD-1 falsifier (anima-side regression):
  - manifest.sha256 is deterministic over the SAME .pt input
    (sorted-by-key tensor list + canonical JSON serialisation)
  - 3× re-export produces bit-identical manifest.json + .farr files
"""
import argparse, hashlib, json, os, struct, sys
import torch

MANIFEST_FORMAT = "flame-mc-manifest/0.1"

# Mappable backbone keys for ConsciousDecoderV2 d768·12L (matches
# flame Path-A `flame_d768_12L_corpus_test.hexa` mc_total layout).
# Source: anima conscious_decoder.py lines ~600-750.
MAPPABLE_KEY_PATTERNS = [
    "tok_emb.weight",
    "head_a.weight",
    "ln_f.weight",
    "blocks.{i}.attn.q_proj.weight",
    "blocks.{i}.attn.k_proj.weight",
    "blocks.{i}.attn.v_proj.weight",
    "blocks.{i}.attn.o_proj.weight",
    "blocks.{i}.ln1.weight",
    "blocks.{i}.ln2.weight",
    # SwiGLU FFN — anima uses PureFieldFFN (dual a/g) → unmapped
    # to the SwiGLU layout. Listed here as PLACEHOLDER, not exported.
]

# Keys that are KNOWN unmapped (anima-specific overlays not in
# Path-A `m_total`). honestly tracked.
UNMAPPED_PATTERNS = [
    "head_g.",          # dual Engine A⇄G — Path-A has single head
    "ffn.",             # PureFieldFFN dual-engine — Path-A SwiGLU
    "tension_proj.",    # consciousness signal — anima-specific
    "moe_",             # MoE auxiliaries — Path-A no MoE
    "engine_g.",        # alternate naming
    "purefield",        # PureFieldFFN alternate
]


def _is_mappable(key: str, n_layer: int) -> bool:
    """True iff this state_dict key matches the Path-A mappable subset."""
    # Top-level non-block keys
    if key in ("tok_emb.weight", "head_a.weight", "ln_f.weight"):
        return True
    # Per-layer attention + layernorms
    for i in range(n_layer):
        for pat in [
            f"blocks.{i}.attn.q_proj.weight",
            f"blocks.{i}.attn.k_proj.weight",
            f"blocks.{i}.attn.v_proj.weight",
            f"blocks.{i}.attn.o_proj.weight",
            f"blocks.{i}.ln1.weight",
            f"blocks.{i}.ln2.weight",
        ]:
            if key == pat:
                return True
    return False


def _classify_unmapped(key: str) -> bool:
    """True iff this key is KNOWN-unmapped (anima-specific overlay)."""
    for pat in UNMAPPED_PATTERNS:
        if pat in key:
            return True
    return False


def _filename_for_key(key: str) -> str:
    """Sanitise PyTorch dotted key into a flat .farr filename."""
    return key.replace(".", "_") + ".farr"


def _to_f32_bytes(t: torch.Tensor) -> bytes:
    """Convert tensor to f32 little-endian byte stream."""
    if t.dtype == torch.bfloat16:
        t = t.float()  # bf16 → f32 promote
    elif t.dtype == torch.float64:
        t = t.float()  # f64 → f32 (loss, but Phase 1 accepts)
    elif t.dtype != torch.float32:
        t = t.float()
    flat = t.contiguous().flatten().cpu().numpy()
    # Force little-endian f32
    return flat.astype("<f4").tobytes()


def export(ckpt_path: str, out_dir: str, model_config: dict) -> dict:
    """Load .pt, dump manifest + per-tensor .farr, return manifest dict."""
    os.makedirs(out_dir, exist_ok=True)
    state = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    sd = state.get("model", state)  # accept both wrapped and raw

    n_layer = model_config["n_layer"]

    tensors = []
    unmapped = []
    farr_concat_sha = hashlib.sha256()

    # Sort keys for deterministic order
    for key in sorted(sd.keys()):
        t = sd[key]
        if not isinstance(t, torch.Tensor):
            continue
        if _is_mappable(key, n_layer):
            fname = _filename_for_key(key)
            fpath = os.path.join(out_dir, fname)
            blob = _to_f32_bytes(t)
            with open(fpath, "wb") as f:
                f.write(blob)
            # update concatenation sha (deterministic over sorted keys)
            farr_concat_sha.update(blob)
            tensors.append({
                "key":   key,
                "shape": list(t.shape),
                "dtype": "f32",
                "file":  fname,
                "count": int(t.numel()),
            })
        elif _classify_unmapped(key):
            unmapped.append(key)
        else:
            # Unknown — honestly list as unmapped too
            unmapped.append(key)

    # Build manifest WITHOUT sha first
    manifest = {
        "format":          MANIFEST_FORMAT,
        "sha256":          "",  # filled below
        "ckpt_source":     os.path.basename(ckpt_path),
        "model_config":    model_config,
        "tensors":         tensors,
        "honest_unmapped": sorted(unmapped),
    }
    # Compute deterministic sha over (canonical-JSON-of-manifest_without_sha
    # ⊕ concatenated_farr_bytes)
    canonical_no_sha = json.dumps(
        {k: v for k, v in manifest.items() if k != "sha256"},
        sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    final_sha = hashlib.sha256()
    final_sha.update(canonical_no_sha)
    final_sha.update(farr_concat_sha.digest())
    manifest["sha256"] = final_sha.hexdigest()

    # Write manifest.json (pretty for readability)
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    return manifest


def f_ptload_1_deterministic(ckpt_path: str, model_config: dict, tmp_root: str) -> bool:
    """F-PTLOAD-1: 3× re-export produces bit-identical manifest.sha256."""
    shas = []
    for i in range(3):
        d = os.path.join(tmp_root, f"pass_{i}")
        m = export(ckpt_path, d, model_config)
        shas.append(m["sha256"])
    return shas[0] == shas[1] == shas[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True, help="Path to .pt state_dict")
    ap.add_argument("--out-dir", required=True, help="Output manifest dir")
    ap.add_argument("--d-model",   type=int, default=768)
    ap.add_argument("--n-layer",   type=int, default=12)
    ap.add_argument("--n-head",    type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--vocab-size",type=int, default=256)
    ap.add_argument("--block-size",type=int, default=128)
    ap.add_argument("--falsifier", action="store_true",
                    help="Run F-PTLOAD-1 determinism test instead of single export")
    args = ap.parse_args()

    cfg = dict(
        d_model=args.d_model, n_layer=args.n_layer, n_head=args.n_head,
        n_kv_head=args.n_kv_head, vocab_size=args.vocab_size,
        block_size=args.block_size,
    )

    if args.falsifier:
        ok = f_ptload_1_deterministic(args.ckpt, cfg, args.out_dir)
        print(f"F-PTLOAD-1 deterministic 3x re-export: {'PASS' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)
    else:
        manifest = export(args.ckpt, args.out_dir, cfg)
        print(f"manifest.format     = {manifest['format']}")
        print(f"manifest.sha256     = {manifest['sha256']}")
        print(f"n_mapped_tensors    = {len(manifest['tensors'])}")
        print(f"n_unmapped_keys     = {len(manifest['honest_unmapped'])}")
        print(f"out_dir             = {args.out_dir}")


if __name__ == "__main__":
    main()
