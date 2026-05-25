"""Smoke-test branch mutations on tiny Mac CPU model — verify mutation logic before $$$ fire."""
import os, sys
sys.path.insert(0, "/Users/ghost/core/anima/training")
sys.path.insert(0, "/Users/ghost/core/anima/tool/transient_py")

import torch
import torch.nn as nn
from engine_a_g_arch import EngineAGModel, EngineAGConfig

# Mock pod env so import works
os.makedirs("/tmp/_pod_mock", exist_ok=True)
os.environ["ANIMA_FIX56_TEST"] = "1"

# Tiny config
cfg = EngineAGConfig.la_350m()
cfg.n_layers = 2
cfg.vocab_size = 256
cfg.d_model = 128
cfg.n_heads = 4
cfg.n_kv_heads = 2

def make_substrate():
    """Make a fake 'BG-LB' substrate state_dict — tied tok_emb=lm_head."""
    m = EngineAGModel(cfg)
    # Force a known pattern in tok_emb so we can detect preservation
    with torch.no_grad():
        m.tok_emb.weight.fill_(0.5)
    sd = m.state_dict()
    # Confirm tied storage
    same = m.tok_emb.weight.data_ptr() == m.lm_head.weight.data_ptr()
    print(f"substrate_tied_storage={same} tok_emb[0,0]={m.tok_emb.weight[0,0].item():.4f}")
    return sd

substrate_sd = make_substrate()
# BG-LB ckpt schema only has tok_emb.weight (not lm_head.weight separately).
# Mimic that.
bg_lb_sd = {k: v.clone() for k, v in substrate_sd.items() if k != "lm_head.weight"}

# Reproduce _load_substrate + _apply_branch
sys.path.insert(0, "/Users/ghost/core/anima/tool/transient_py")
from anima_fix_5_6_tied_poc_h100 import _apply_branch

def fresh_model_with_substrate():
    m = EngineAGModel(cfg)
    sd = {k: v.clone() for k, v in bg_lb_sd.items()}
    if "lm_head.weight" not in sd:
        sd["lm_head.weight"] = sd["tok_emb.weight"].clone()
    missing, unexpected = m.load_state_dict(sd, strict=False)
    return m, missing, unexpected

# branch-A: lm_head reinit, tok_emb preserved
print("\n=== branch-A ===")
m_a, miss, unex = fresh_model_with_substrate()
print(f"load: missing={len(miss)} unexpected={len(unex)}")
print(f"pre-mutate: tok_emb[0,0]={m_a.tok_emb.weight[0,0].item():.4f} lm_head[0,0]={m_a.lm_head.weight[0,0].item():.4f}")
print(f"  tied_pre={m_a.tok_emb.weight.data_ptr() == m_a.lm_head.weight.data_ptr()}")
meta_a = _apply_branch(m_a, "a")
print(f"post-mutate: tok_emb[0,0]={m_a.tok_emb.weight[0,0].item():.4f} lm_head[0,0]={m_a.lm_head.weight[0,0].item():.4f}")
print(f"  tied_post={m_a.tok_emb.weight.data_ptr() == m_a.lm_head.weight.data_ptr()}")
print(f"  tok_emb preserved (==0.5)? {torch.allclose(m_a.tok_emb.weight, torch.full_like(m_a.tok_emb.weight, 0.5))}")
print(f"  lm_head reinitialized (mean≈0)? mean={m_a.lm_head.weight.mean().item():.4f} std={m_a.lm_head.weight.std().item():.4f}")
n_train_a = sum(p.numel() for p in m_a.parameters() if p.requires_grad)
n_total_a = sum(p.numel() for p in m_a.parameters())
print(f"  trainable={n_train_a:,}/{n_total_a:,}")

# branch-B: tok_emb reinit, lm_head preserved
print("\n=== branch-B ===")
m_b, miss, unex = fresh_model_with_substrate()
meta_b = _apply_branch(m_b, "b")
print(f"post-mutate: tok_emb[0,0]={m_b.tok_emb.weight[0,0].item():.4f} lm_head[0,0]={m_b.lm_head.weight[0,0].item():.4f}")
print(f"  tied_post={m_b.tok_emb.weight.data_ptr() == m_b.lm_head.weight.data_ptr()}")
print(f"  lm_head preserved (==0.5)? {torch.allclose(m_b.lm_head.weight, torch.full_like(m_b.lm_head.weight, 0.5))}")
print(f"  tok_emb reinitialized? mean={m_b.tok_emb.weight.mean().item():.4f} std={m_b.tok_emb.weight.std().item():.4f}")
n_train_b = sum(p.numel() for p in m_b.parameters() if p.requires_grad)
n_total_b = sum(p.numel() for p in m_b.parameters())
print(f"  trainable={n_train_b:,}/{n_total_b:,}")

# branch-C: tied freeze
print("\n=== branch-C ===")
m_c, miss, unex = fresh_model_with_substrate()
meta_c = _apply_branch(m_c, "c")
print(f"post-mutate: tok_emb[0,0]={m_c.tok_emb.weight[0,0].item():.4f} lm_head[0,0]={m_c.lm_head.weight[0,0].item():.4f}")
print(f"  tied_post={m_c.tok_emb.weight.data_ptr() == m_c.lm_head.weight.data_ptr()}")
print(f"  tok_emb.requires_grad={m_c.tok_emb.weight.requires_grad}")
print(f"  lm_head.requires_grad={m_c.lm_head.weight.requires_grad}")
n_train_c = sum(p.numel() for p in m_c.parameters() if p.requires_grad)
n_total_c = sum(p.numel() for p in m_c.parameters())
print(f"  trainable={n_train_c:,}/{n_total_c:,} (frozen={n_total_c-n_train_c:,})")

# Smoke forward pass for each
print("\n=== smoke forward ===")
x = torch.randint(0, 256, (1, 8))
y = torch.randint(0, 256, (1, 8))
for label, m in [("a", m_a), ("b", m_b), ("c", m_c)]:
    out = m(x, labels=y)
    loss = out["loss"]
    loss.backward()
    grad_tok = m.tok_emb.weight.grad
    grad_lm = m.lm_head.weight.grad
    print(f"  branch_{label}: loss={loss.item():.4f} tok_emb.grad={'None' if grad_tok is None else f'{grad_tok.norm().item():.4f}'} lm_head.grad={'None' if grad_lm is None else f'{grad_lm.norm().item():.4f}'}")

print("\nALL PASS")
