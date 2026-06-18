#!/usr/bin/env python3
"""$0 corpus->trainer pipeline SMOKE — de-risks the cost-gated 7B GPU fire.

Proves the data->trainer plumbing for `dancinlab/anima-corpus-5lang-7b-webscale`
END-TO-END on a TINY slice, $0, local CPU, NO GPU rent:

  1. R2 reachability     — list anima-7b/ via the S3-compat API, confirm 20 shards
                           + MANIFEST.json, match R2 manifest <-> HF manifest.
  2. Tiny-slice GET      — partial-object Range GET (~few MB) of ONE shard (prefer
                           the ko Korean shard), confirm real byte text (V=256),
                           sample-print lines/lang, confirm PII markers [EMAIL]/
                           [PHONE] policy + control bytes 0xFE/0xFF stripped.
  3. Trainer smoke       — drive anima's byte-LM trainer glue on the tiny slice:
                           byte tok (V=256) -> batches -> forward -> loss DROPS
                           over a few steps -> checkpoint writes.
                           Production trainer (CLM/train/train_lane_p.py) ASSERTS
                           CUDA (line: `assert torch.cuda.is_available()`) and
                           imports torch — it is GPU-ONLY, NOT CPU-smokeable. If
                           torch+CUDA are present we run the REAL trainer in a
                           tiny CPU/GPU mode where possible; else we run a clearly
                           LABELED numpy byte-LM proxy that exercises the SAME
                           glue (byte tok -> batch -> fwd -> CE drop -> ckpt) to
                           prove the data->loader->loss->ckpt path, and report
                           HONESTLY that the forge/Lane-P GPU path was not CPU
                           smokeable (no fake GPU success).

CREDS (c7): R2 creds read INLINE at runtime from the secret store
(`harness secret get r2.phanes.*`), header-only, NEVER printed / logged /
written to any file. This script contains NO secret values.

If a cred is missing or R2 auth fails: STOP + honest error (no fake success, c9).
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import struct
import subprocess
import sys
import tempfile
import time

# ── manifest expectations (from the corpus card / HF manifest) ───────────────
EXP_TOTAL_BYTES = 154187454007        # 143.60 GiB
EXP_SHARDS = 20
EXP_PER_LANG_SHARDS = {"en": 8, "fr": 3, "de": 3, "es": 3, "ko": 3}
R2_PREFIX = "anima-7b/web/"
R2_MANIFEST_KEY = "anima-7b/MANIFEST.json"
SLICE_BYTES = 8 * 1024 * 1024         # 8 MB partial GET


def _sec(key: str) -> str:
    """Read a secret inline from the store. NEVER returned to stdout."""
    try:
        v = subprocess.check_output(
            ["harness", "secret", "get", key],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"STOP (c9): secret '{key}' unavailable: {e}")
    if not v:
        raise SystemExit(f"STOP (c9): secret '{key}' is empty")
    return v


def r2_client():
    try:
        import boto3  # noqa: PLC0415
    except ImportError:
        raise SystemExit("STOP: boto3 not installed (pip install boto3)")
    acct = _sec("r2.phanes.account_id")
    ak = _sec("r2.phanes.access_key_id")
    sk = _sec("r2.phanes.secret_access_key")
    bucket = _sec("r2.phanes.bucket")
    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{acct}.r2.cloudflarestorage.com",
        aws_access_key_id=ak,
        aws_secret_access_key=sk,
        region_name="auto",
    )
    return s3, bucket


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — R2 reachability + manifest match
# ─────────────────────────────────────────────────────────────────────────────
def step1_reachability(s3, bucket):
    print("=" * 72)
    print("STEP 1 — R2 reachability + manifest match")
    print("=" * 72)
    paginator = s3.get_paginator("list_objects_v2")
    objs = []
    for page in paginator.paginate(Bucket=bucket, Prefix="anima-7b/"):
        objs.extend(page.get("Contents", []))
    shard_objs = [o for o in objs if o["Key"].endswith(".bytes")]
    manifest_obj = [o for o in objs if o["Key"] == R2_MANIFEST_KEY]
    print(f"bucket={bucket}  objects-under-anima-7b/={len(objs)}")
    print(f"shards listed={len(shard_objs)}  manifest-present={bool(manifest_obj)}")
    total = 0
    per_lang = {}
    for o in sorted(shard_objs, key=lambda x: x["Key"]):
        lang3 = o["Key"].split("/")[2]  # eng/fra/deu/spa/kor
        lang = {"eng": "en", "fra": "fr", "deu": "de", "spa": "es", "kor": "ko"}[lang3]
        per_lang[lang] = per_lang.get(lang, 0) + 1
        total += o["Size"]
        print(f"  {o['Key']:34s} {o['Size']:>13,} B  ({lang})")

    # pull the R2 manifest and compare to its own header numbers + HF expectations.
    # The R2 MANIFEST.json header is a lean schema ({total_gb, tok_per_param_7b,
    # shards, manifest[]}); the HF-repo manifest is a superset (adds total_bytes,
    # per_lang, etc). The LOAD-BEARING shared part is the per-shard `manifest`
    # array (key/bytes/sha256) — we validate against that, not a header field.
    body = s3.get_object(Bucket=bucket, Key=R2_MANIFEST_KEY)["Body"].read()
    r2_manifest = json.loads(body)
    m_total = sum(s["bytes"] for s in r2_manifest["manifest"])
    m_per_lang = {}
    for s in r2_manifest["manifest"]:
        m_per_lang[s["lang"]] = m_per_lang.get(s["lang"], 0) + 1
    print(f"\nR2 MANIFEST.json: total_gb={r2_manifest.get('total_gb')} "
          f"shards={r2_manifest.get('shards')} "
          f"tok/param={r2_manifest.get('tok_per_param_7b')}  "
          f"per-shard-sum={m_total:,}B ({m_total/1024**3:.2f} GiB)")

    ok = True
    if len(shard_objs) != EXP_SHARDS:
        ok = False; print(f"  MISMATCH listed shards: {len(shard_objs)} != {EXP_SHARDS}")
    if len(r2_manifest["manifest"]) != EXP_SHARDS:
        ok = False; print(f"  MISMATCH manifest rows: {len(r2_manifest['manifest'])} != {EXP_SHARDS}")
    if total != EXP_TOTAL_BYTES:
        ok = False; print(f"  MISMATCH listed total: {total:,} != {EXP_TOTAL_BYTES:,}")
    if m_total != EXP_TOTAL_BYTES:
        ok = False; print(f"  MISMATCH manifest per-shard sum {m_total:,} != HF total {EXP_TOTAL_BYTES:,}")
    if m_total != total:
        ok = False; print(f"  MISMATCH manifest sum {m_total:,} != live-listed {total:,}")
    if per_lang != EXP_PER_LANG_SHARDS:
        ok = False; print(f"  MISMATCH listed per-lang shards: {per_lang} != {EXP_PER_LANG_SHARDS}")
    if m_per_lang != EXP_PER_LANG_SHARDS:
        ok = False; print(f"  MISMATCH manifest per-lang shards: {m_per_lang} != {EXP_PER_LANG_SHARDS}")

    print(f"\nSTEP 1 RESULT: {'MATCH (R2 == HF manifest)' if ok else 'MISMATCH'}  "
          f"per_lang_shards={per_lang}  total={total:,}B "
          f"({total/1024**3:.2f} GiB)")
    return ok, r2_manifest


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — tiny-slice partial GET + byte/PII/control-byte verify
# ─────────────────────────────────────────────────────────────────────────────
def step2_tiny_slice(s3, bucket, r2_manifest):
    print("\n" + "=" * 72)
    print("STEP 2 — tiny-slice partial-object GET + byte verify")
    print("=" * 72)
    # prefer the ko (Korean) shard
    ko = [m for m in r2_manifest["manifest"] if m["lang"] == "ko"]
    target = ko[0] if ko else r2_manifest["manifest"][0]
    key = target["key"]
    print(f"target shard: {key}  lang={target['lang']}  "
          f"full={target['bytes']:,}B  slicing first {SLICE_BYTES:,}B")
    rng = f"bytes=0-{SLICE_BYTES - 1}"
    obj = s3.get_object(Bucket=bucket, Key=key, Range=rng)
    data = obj["Body"].read()
    print(f"partial GET ok: got {len(data):,}B  ContentRange={obj.get('ContentRange')}")

    # V=256 byte check + control-byte 0xFE/0xFF strip claim
    present = set(data)
    has_fe = 0xFE in present
    has_ff = 0xFF in present
    nonascii = sum(1 for b in data if b >= 0x80)
    print(f"distinct byte values in slice: {len(present)} / 256")
    print(f"control bytes 0xFE present={has_fe}  0xFF present={has_ff}  "
          f"(card claims STRIPPED -> expect both False)")
    print(f"high bytes (>=0x80, multibyte UTF-8 e.g. Hangul): {nonascii:,} "
          f"({100*nonascii/len(data):.1f}%)")

    # PII markers
    n_email = data.count(b"[EMAIL]")
    n_phone = data.count(b"[PHONE]")
    print(f"PII scrub markers: [EMAIL]={n_email}  [PHONE]={n_phone}")

    # sample-print a few real lines
    print("\n--- sample lines from slice (decoded utf-8, errors=replace) ---")
    text = data.decode("utf-8", errors="replace")
    lines = [ln for ln in text.split("\n") if ln.strip()]
    for ln in lines[3:9]:
        print("  | " + (ln[:110]))
    has_hangul = any("가" <= ch <= "힣" for ch in text)
    print(f"--- Hangul (가-힣) detected in slice: {has_hangul} ---")

    real_text = (len(present) > 40 and not has_fe and not has_ff)
    print(f"\nSTEP 2 RESULT: real-byte-text={real_text}  "
          f"control-stripped={not has_fe and not has_ff}  "
          f"korean={has_hangul}  pii_markers_seen={n_email + n_phone > 0}")
    return real_text, data


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — trainer pipeline smoke (data -> tok -> batch -> fwd -> loss -> ckpt)
# ─────────────────────────────────────────────────────────────────────────────
def step3_trainer_smoke(slice_bytes: bytes, outdir: str):
    print("\n" + "=" * 72)
    print("STEP 3 — trainer pipeline smoke")
    print("=" * 72)
    have_torch = False
    cuda = False
    try:
        import torch  # noqa: PLC0415
        have_torch = True
        cuda = torch.cuda.is_available()
    except ImportError:
        pass
    print(f"torch installed={have_torch}  cuda={cuda}")
    print("NOTE: production trainer CLM/train/train_lane_p.py imports torch and")
    print("      ASSERTS torch.cuda.is_available() (g63: no silent CPU) — it is a")
    print("      GPU-ONLY Lane-P path. The forge .hexa trainers (a_train_flame_forge)")
    print("      also REQUIRE GPU. Neither is CPU-smokeable on this $0 host.")

    if have_torch and cuda:
        return _real_trainer_smoke(slice_bytes, outdir)
    return _numpy_proxy_smoke(slice_bytes, outdir, have_torch)


def _real_trainer_smoke(slice_bytes, outdir):
    """If torch+CUDA exist, drive the REAL CLMConvMoE forward/loss on the slice."""
    print("\n[REAL] torch+CUDA present -> exercising real CLMConvMoE glue")
    import torch  # noqa: PLC0415
    sys.path.insert(0, os.path.join(os.getcwd(), "CLM", "model"))
    from model import CLMConfig, CLMConvMoE  # noqa: PLC0415
    dev = "cuda"
    cfg = CLMConfig(n_experts=2, n_trunk_layers=1, d_model=64, kernel_size=3, variant="AB")
    model = CLMConvMoE(cfg).to(dev)
    stream = torch.frombuffer(bytearray(slice_bytes), dtype=torch.uint8).long()
    seq, bs = 128, 16
    gen = torch.Generator().manual_seed(0)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4)

    def batch():
        ix = torch.randint(0, stream.numel() - seq - 1, (bs,), generator=gen)
        x = torch.stack([stream[i:i + seq] for i in ix]).to(dev)
        y = torch.stack([stream[i + 1:i + 1 + seq] for i in ix]).to(dev)
        return x, y

    ces = []
    for step in range(12):
        x, y = batch()
        opt.zero_grad(set_to_none=True)
        out = model(x, y)
        out["loss"].backward()
        opt.step()
        ce = float(out["ce_loss"])
        ces.append(ce)
        if step % 3 == 0:
            print(f"  step {step:2d} ce={ce:.4f}")
    ckpt = os.path.join(outdir, "smoke_real.pt")
    torch.save({k: v.detach().cpu() for k, v in model.state_dict().items()}, ckpt)
    return _finish(ces, ckpt, mode="REAL torch+CUDA CLMConvMoE")


def _numpy_proxy_smoke(slice_bytes, outdir, have_torch):
    """LABELED PROXY: exercises the data->tok->batch->fwd->CE-drop->ckpt glue
    with a tiny pure-numpy byte bigram+context LM. This is NOT the production
    architecture (no MoE, no conv trunk) — it proves the DATA PIPELINE plumbing
    only. The forge/Lane-P GPU trainer path was NOT CPU-smokeable (reported)."""
    print("\n[PROXY] torch/CUDA absent -> LABELED numpy byte-LM glue smoke")
    print("        (NOT the production CLMConvMoE; proves data->loss->ckpt plumbing only)")
    import numpy as np  # noqa: PLC0415

    V = 256
    # byte tokenization (V=256, no tokenizer) — identical to production loader
    stream = np.frombuffer(slice_bytes, dtype=np.uint8).astype(np.int64)
    print(f"  byte-tokenized: {stream.size:,} tokens, vocab observed={len(np.unique(stream))}")
    seq, bs = 64, 32
    rng = np.random.default_rng(0)

    # tiny learnable model: embed(prev byte) -> logits over next byte (V x V table)
    # trained by plain SGD on next-byte CE — a faithful CE-descent over byte data.
    W = np.zeros((V, V), dtype=np.float64)
    lr = 0.5

    def make_batch():
        ix = rng.integers(0, stream.size - seq - 1, size=bs)
        xs = np.stack([stream[i:i + seq] for i in ix])
        ys = np.stack([stream[i + 1:i + 1 + seq] for i in ix])
        return xs, ys

    def softmax(z):
        z = z - z.max(axis=-1, keepdims=True)
        e = np.exp(z)
        return e / e.sum(axis=-1, keepdims=True)

    ces = []
    for step in range(40):
        xs, ys = make_batch()           # (bs, seq)
        xf = xs.reshape(-1)             # (bs*seq,)
        yf = ys.reshape(-1)
        logits = W[xf]                  # (N, V)  forward
        p = softmax(logits)
        n = xf.size
        ce = -np.log(p[np.arange(n), yf] + 1e-12).mean()   # next-byte CE
        ces.append(float(ce))
        # gradient: dL/dlogits = (p - onehot)/n, accumulate per prev-byte row
        g = p.copy()
        g[np.arange(n), yf] -= 1.0
        g /= n
        np.add.at(W, xf, -lr * g)       # SGD step
        if step % 8 == 0:
            print(f"  step {step:2d} ce={ce:.4f}  (uniform ln256={np.log(256):.4f})")

    ckpt = os.path.join(outdir, "smoke_proxy.npz")
    np.savez_compressed(ckpt, W=W.astype(np.float32))
    note = "PROXY numpy byte-LM (production CLMConvMoE GPU path NOT CPU-smokeable)"
    return _finish(ces, ckpt, mode=note)


def _finish(ces, ckpt, mode):
    first, last = ces[0], ces[-1]
    dropped = last < first
    sz = os.path.getsize(ckpt)
    print(f"\n  CE first={first:.4f} -> last={last:.4f}  "
          f"(drop={first - last:+.4f})  decreased={dropped}")
    print(f"  checkpoint written: {ckpt} ({sz:,} B)")
    print(f"\nSTEP 3 RESULT: mode='{mode}'  loss_decreased={dropped}  ckpt_written={sz > 0}")
    return dropped and sz > 0, mode


# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("anima corpus->trainer SMOKE  ($0 · CPU · no GPU rent)\n")
    s3, bucket = r2_client()
    ok1, manifest = step1_reachability(s3, bucket)
    ok2, slice_bytes = step2_tiny_slice(s3, bucket, manifest)
    with tempfile.TemporaryDirectory() as td:
        ok3, mode = step3_trainer_smoke(slice_bytes, td)
    print("\n" + "=" * 72)
    print("SMOKE SUMMARY")
    print("=" * 72)
    print(f"  step1 R2-reachable + manifest-match : {'PASS' if ok1 else 'FAIL'}")
    print(f"  step2 tiny-slice real byte text     : {'PASS' if ok2 else 'FAIL'}")
    print(f"  step3 trainer glue (mode={mode!r:>5}) : {'PASS' if ok3 else 'FAIL'}")
    allok = ok1 and ok2 and ok3
    print(f"\n  GREEN-LIGHT (plumbing ready for cost-gated GPU fire): "
          f"{'YES' if allok else 'NO'}")
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
