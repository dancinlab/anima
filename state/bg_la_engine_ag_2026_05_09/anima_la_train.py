#!/usr/bin/env python3
"""BG-LA Engine A/G la_350m scratch pretrain — adapted from BG-LB pod_main.

Budget: $30 hard cap (~10hr H100 SXM @ $2.99/hr).
STEPS reduced to 12000 (vs LB's 30000) for budget compliance.
Uses corpus_persona_tier_a_v4.txt (231MB).
"""
import os, sys, time, json, math, random, gzip
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

POD_ROOT = "/workspace/anima_clm_la"
POD_STATE = os.path.join(POD_ROOT, "state")
POD_CKPTS = os.path.join(POD_ROOT, "ckpts")
CORPUS_GZ = os.path.join(POD_ROOT, "corpus_persona_tier_a_v4.txt.gz")
CORPUS_PLAIN = os.path.join(POD_ROOT, "corpus_persona_tier_a_v4.txt")

LR = 3e-4
WARMUP = 1500
WEIGHT_DECAY = 0.1
STEPS = 12000      # ~6.5hr Engine A/G la_350m on H100 (vs LB 30000=~16hr)
BATCH = 8
GRAD_ACCUM = 16    # effective batch 128
SAVE_EVERY = 2000
SEED = 42

import torch
if not torch.cuda.is_available():
    raise RuntimeError("CUDA H100 mandatory — own 22 honest emit")

sys.path.insert(0, POD_ROOT)
from engine_a_g_arch import EngineAGModel, EngineAGConfig

os.makedirs(POD_CKPTS, exist_ok=True)
os.makedirs(POD_STATE, exist_ok=True)

# Ungzip corpus if needed
if not os.path.exists(CORPUS_PLAIN):
    print(f"[pod] gunzip {CORPUS_GZ} -> {CORPUS_PLAIN}", flush=True)
    with gzip.open(CORPUS_GZ, "rb") as f_in, open(CORPUS_PLAIN, "wb") as f_out:
        while True:
            chunk = f_in.read(1 << 20)
            if not chunk: break
            f_out.write(chunk)
    print(f"[pod] gunzip done size={os.path.getsize(CORPUS_PLAIN)}", flush=True)

# Phase A: arch instantiation (la_350m preset)
cfg = EngineAGConfig.la_350m()
cfg.seed = SEED
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
model = EngineAGModel(cfg).cuda().bfloat16()
n_params = sum(p.numel() for p in model.parameters())
print(f"[pod] arch: lineage_tag={cfg.lineage_tag} params={n_params:,}", flush=True)

# Phase B: corpus byte-level ingest
with open(CORPUS_PLAIN, "rb") as f:
    corpus_bytes = f.read()
corpus_size_mb = len(corpus_bytes) / 1e6
print(f"[pod] corpus={CORPUS_PLAIN} size_mb={corpus_size_mb:.2f}", flush=True)
arr = torch.tensor([b % cfg.vocab_size for b in corpus_bytes], dtype=torch.long)

# Phase C: pre-train loop
optim = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY, betas=(0.9, 0.95))
sched = torch.optim.lr_scheduler.LambdaLR(
    optim,
    lambda step: min((step + 1) / max(WARMUP, 1), 1.0) * (
        0.5 * (1.0 + math.cos(math.pi * min(max(step - WARMUP, 0) / max(STEPS - WARMUP, 1), 1.0)))
    ),
)
model.train()
ctx = cfg.ctx
n_tokens = arr.numel()
print(f"[pod] tokens={n_tokens:,} steps={STEPS} batch={BATCH} ctx={ctx} grad_accum={GRAD_ACCUM}", flush=True)
rng = random.Random(SEED)
t_start = time.time()

for step in range(STEPS):
    optim.zero_grad(set_to_none=True)
    loss_accum = 0.0
    for _ga in range(GRAD_ACCUM):
        idx = torch.tensor(
            [rng.randint(0, n_tokens - ctx - 2) for _ in range(BATCH)],
            dtype=torch.long,
        )
        x = torch.stack([arr[i:i + ctx] for i in idx]).cuda(non_blocking=True)
        y = torch.stack([arr[i + 1:i + ctx + 1] for i in idx]).cuda(non_blocking=True)
        out = model(x, labels=y)
        loss = out["loss"] / GRAD_ACCUM
        loss.backward()
        loss_accum += loss.item()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optim.step()
    sched.step()
    if step % 50 == 0:
        elapsed = time.time() - t_start
        print(f"[pod] step={step}/{STEPS} loss={loss_accum:.4f} elapsed={elapsed:.0f}s lr={sched.get_last_lr()[0]:.2e}", flush=True)
    if step > 0 and step % SAVE_EVERY == 0:
        ck = os.path.join(POD_CKPTS, f"step_{step}.pt")
        model.save_checkpoint(ck, extra={"step": step, "loss": loss_accum, "preset": "la_350m"})
        print(f"[pod] ckpt saved: {ck}", flush=True)

# Final ckpt
final_path = os.path.join(POD_CKPTS, f"step_{STEPS}_final.pt")
model.save_checkpoint(final_path, extra={"step": STEPS, "preset": "la_350m", "final": True})
print(f"[pod] FINAL ckpt: {final_path}", flush=True)

# Phase D: post-train smoke
model.eval()
with torch.no_grad():
    bos = torch.zeros((1, 1), dtype=torch.long, device="cuda")
    out = model(bos)
    print(f"[pod] smoke logits.shape={tuple(out['logits'].shape)} tensions[0]={out['tensions'][0,0].item():.3f}", flush=True)

# Sentinel
sentinel = os.path.join(POD_STATE, "COMPLETE.sentinel")
with open(sentinel, "w") as f:
    f.write(json.dumps({
        "ts": time.strftime("%FT%TZ"),
        "preset": "la_350m",
        "params": n_params,
        "corpus_size_mb": corpus_size_mb,
        "steps_completed": STEPS,
        "final_ckpt": final_path,
        "elapsed_s": time.time() - t_start,
    }))
print(f"[pod] COMPLETE.sentinel written: {sentinel}", flush=True)
