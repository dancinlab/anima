#!/usr/bin/env python3
"""H_9027 verify — BGB injected-bind decode/serialize byte-exactness harness.

SELF-CONTAINED (no archive import): defines a tiny torch ByteGPT + Block INLINE
(matching h1129's Block: ln1/attn/ln2/mlp) and the BindAttn gated-block forward
(x = x + gate*(block(x)-x)) INLINE, then checks core/decode.py (numpy) + core/
serialize.py (BGB trailer) against that reference. torch runs in FLOAT64 so the
check isolates LAYOUT/MATH correctness (not f32 rounding). $0, CPU, no training.

Checks:
  (B)  base: numpy bg_load forward == torch base forward (max|Δ|<1e-4, argmax-id)
             over random windows AND the full greedy stream.
  (b0) gate=0 BGB .bin decodes BYTE-IDENTICALLY to the plain base .bin.
  (c)  plain base .bin decodes BYTE-IDENTICALLY vs origin/main core/decode.py
       (proves no regression from the change).
  (I1) N=1 injected, nonzero gate: numpy BGB decode == torch injected forward.
  (I2) N=2 injected, nonzero gates: numpy BGB decode == torch injected forward.
"""
import os, sys, struct, importlib.util
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(1234)
np.random.seed(1234)
torch.set_default_dtype(torch.float64)

REPO = "/Users/mini/dancinlab/anima-bgb"
CORE = os.path.join(REPO, "core")
sys.path.insert(0, CORE)
import decode as D          # patched core/decode.py
import serialize as S       # patched core/serialize.py

WORK = os.path.join(REPO, "state", "9027_bgb_injected_decode", "_artifacts")
os.makedirs(WORK, exist_ok=True)

VOCAB, DMODEL, NLAY, NHEAD, BLOCK = 256, 32, 2, 4, 16

FAILS = []
def check(name, ok, detail=""):
    print(("  PASS " if ok else "  FAIL ") + name + ("  " + detail if detail else ""))
    if not ok:
        FAILS.append(name)

# ── INLINE torch reference (NOT imported from archive) ──────────────────────
class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=0.0, batch_first=True)
        s.ln2 = nn.LayerNorm(d)
        s.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=32, n_layer=2, n_head=4, block=16):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d)
        s.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def _mask(s, T, dev):
        return torch.triu(torch.full((T, T), float("-inf"), device=dev), diagonal=1)
    def forward(s, idx):
        B, T = idx.shape
        x = s.tok(idx) + s.pos(torch.arange(T, device=idx.device))[None]
        m = s._mask(T, idx.device)
        for b in s.blocks:
            x = b(x, m)
        return s.head(s.ln_f(x))

class BindByteGPT(nn.Module):
    """base ByteGPT + N appended GATED Blocks (after base stack, before ln_f)."""
    def __init__(s, base, binds, gates):
        super().__init__()
        s.base = base
        s.binds = nn.ModuleList(binds)
        s.gates = [float(g) for g in gates]
    def forward(s, idx):
        b = s.base; B, T = idx.shape
        x = b.tok(idx) + b.pos(torch.arange(T, device=idx.device))[None]
        m = b._mask(T, idx.device)
        for blk in b.blocks:
            x = blk(x, m)
        for blk, g in zip(s.binds, s.gates):
            x = x + g * (blk(x, m) - x)
        return b.head(b.ln_f(x))

def torch_last_logits(model, ids):
    model.eval()
    with torch.no_grad():
        t = torch.tensor([list(ids)], dtype=torch.long)
        lo = model(t)
    return lo[0, -1].detach().cpu().numpy().astype(np.float64)

def torch_greedy(model, seed_ids, gen, block):
    model.eval()
    toks = list(seed_ids); out = []
    for _ in range(gen):
        start = len(toks) - block if len(toks) > block else 0
        lg = torch_last_logits(model, toks[start:])
        nb = int(np.argmax(lg)); toks.append(nb); out.append(nb)
    return out

def save_base_pt(model, path):
    cfg = {"vocab": VOCAB, "d": DMODEL, "n_layer": NLAY, "n_head": NHEAD, "block": BLOCK}
    torch.save({"model": model.state_dict(), "config": cfg}, path)

def stream_deltas(np_fwd, torch_model, seed, gen, block):
    """Greedy-decode with numpy; at each step compare numpy last-logits to torch
    last-logits on the SAME prefix. Returns (id_stream_np, id_stream_match, maxdelta)."""
    toks = list(seed); out_np = []; maxd = 0.0; match = True
    for _ in range(gen):
        start = len(toks) - block if len(toks) > block else 0
        win = toks[start:]
        lnp = np_fwd(win)
        lt = torch_last_logits(torch_model, win)
        maxd = max(maxd, float(np.max(np.abs(lnp - lt))))
        if int(np.argmax(lnp)) != int(np.argmax(lt)):
            match = False
        nb = int(np.argmax(lnp)); toks.append(nb); out_np.append(nb)
    return out_np, match, maxd

# ════════════════════════════════════════════════════════════════════════
print("=" * 68)
print("H_9027 BGB injected-bind verify (torch f64 reference, self-contained)")
print("  arch: vocab=%d d=%d n_layer=%d n_head=%d block=%d" % (VOCAB, DMODEL, NLAY, NHEAD, BLOCK))
print("=" * 68)

base = ByteGPT(VOCAB, DMODEL, NLAY, NHEAD, BLOCK)
base_pt = os.path.join(WORK, "base.pt")
base_bin = os.path.join(WORK, "base.bin")
save_base_pt(base, base_pt)
S.serialize(base_pt, base_bin)

Wbase = D.bg_load(base_bin)
print("\n[B] BASE parity (numpy bg_load vs torch, f64) + no-trailer sanity")
check("base: bg_is_bytegpt true", D.bg_is_bytegpt(base_bin))
check("base: W['bind'] == [] (no trailer)", Wbase.get("bind") == [])
# random windows
maxd_win = 0.0; arg_ok = True
for _ in range(12):
    T = np.random.randint(1, BLOCK + 1)
    ids = list(np.random.randint(0, VOCAB, size=T))
    lnp = D.bg_forward_last_W(Wbase, ids, T)
    lt = torch_last_logits(base, ids)
    maxd_win = max(maxd_win, float(np.max(np.abs(lnp - lt))))
    if int(np.argmax(lnp)) != int(np.argmax(lt)):
        arg_ok = False
check("base: random-window logits max|Δ|<1e-4", maxd_win < 1e-4, "maxΔ=%.2e" % maxd_win)
check("base: random-window argmax-identical", arg_ok)
# full greedy stream
seed = list(b"hello world ")
np_base_full = D._decode_argmax_W_full(Wbase, seed, 40)["ids"]
np_base_kv = D.bytegpt_decode_argmax(base_bin, seed, 40)["ids"]
t_base = torch_greedy(base, seed, 40, BLOCK)
_, sm_ok, sm_d = stream_deltas(lambda w: D.bg_forward_last_W(Wbase, w, len(w)), base, seed, 40, BLOCK)
check("base: numpy KV stream == numpy full stream", np_base_kv == np_base_full)
check("base: numpy greedy stream == torch greedy stream", np_base_kv == t_base,
      "len=%d" % len(t_base))
check("base: per-step stream logits max|Δ|<1e-4", sm_d < 1e-4, "maxΔ=%.2e" % sm_d)
check("base: per-step argmax-identical over stream", sm_ok)

print("\n[c] NO-REGRESSION vs origin/main core/decode.py (plain base .bin)")
# load origin/main decode.py as an independent module (torch-free numpy)
import subprocess
orig_src = subprocess.check_output(["git", "-C", REPO, "show", "origin/main:core/decode.py"]).decode()
orig_path = os.path.join(WORK, "decode_origin_main.py")
open(orig_path, "w").write(orig_src)
spec = importlib.util.spec_from_file_location("decode_origin", orig_path)
Dorig = importlib.util.module_from_spec(spec); spec.loader.exec_module(Dorig)
orig_stream = Dorig.bytegpt_decode_argmax(base_bin, seed, 40)["ids"]
check("plain base: NEW decode.py stream == origin/main decode.py stream",
      np_base_kv == orig_stream, "len=%d" % len(orig_stream))

# ── injected models ─────────────────────────────────────────────────────────
def make_injected(n_bind, gates):
    binds = []
    for _ in range(n_bind):
        blk = Block(DMODEL, NHEAD)
        # randomize so a zero-init block wouldn't trivially pass
        for p in blk.parameters():
            with torch.no_grad():
                p.copy_(torch.randn_like(p) * 0.3)
        binds.append(blk)
    return BindByteGPT(base, binds, gates), binds

def save_injected_pt(binds, gates, path):
    if len(binds) == 1:
        payload = {"bind": binds[0].state_dict(), "gate": torch.tensor([gates[0]]),
                   "config": {"n_bind": 1}}
    else:
        payload = {"bind": [b.state_dict() for b in binds],
                   "gate": [float(g) for g in gates], "config": {"n_bind": len(binds)}}
    torch.save(payload, path)

def run_injected(tag, n_bind, gates):
    print("\n[%s] N=%d injected, gates=%s" % (tag, n_bind, gates))
    model, binds = make_injected(n_bind, gates)
    pt = os.path.join(WORK, "inj_%s.pt" % tag)
    outbin = os.path.join(WORK, "inj_%s.bin" % tag)
    save_injected_pt(binds, gates, pt)
    S.serialize_bind(base_bin, pt, outbin)
    W = D.bg_load(outbin)
    check("%s: bg_is_bytegpt true (header unchanged)" % tag, D.bg_is_bytegpt(outbin))
    check("%s: n_bind blocks read == %d" % (tag, n_bind), len(W.get("bind", [])) == n_bind)
    # base bytes verbatim
    outraw = open(outbin, "rb").read(); baseraw = open(base_bin, "rb").read()
    check("%s: base bytes copied VERBATIM (prefix)" % tag, outraw[:len(baseraw)] == baseraw)
    # random windows
    maxd = 0.0; aok = True
    for _ in range(12):
        T = np.random.randint(1, BLOCK + 1)
        ids = list(np.random.randint(0, VOCAB, size=T))
        lnp = D.bg_forward_last_W(W, ids, T)
        lt = torch_last_logits(model, ids)
        maxd = max(maxd, float(np.max(np.abs(lnp - lt))))
        if int(np.argmax(lnp)) != int(np.argmax(lt)):
            aok = False
    check("%s: random-window logits max|Δ|<1e-4" % tag, maxd < 1e-4, "maxΔ=%.2e" % maxd)
    check("%s: random-window argmax-identical" % tag, aok)
    # full greedy stream
    np_stream = D.bytegpt_decode_argmax(outbin, seed, 48)["ids"]
    t_stream = torch_greedy(model, seed, 48, BLOCK)
    _, sm_ok, sm_d = stream_deltas(lambda w: D.bg_forward_last_W(W, w, len(w)), model, seed, 48, BLOCK)
    check("%s: numpy BGB stream == torch injected stream" % tag, np_stream == t_stream,
          "len=%d" % len(t_stream))
    check("%s: per-step stream logits max|Δ|<1e-4" % tag, sm_d < 1e-4, "maxΔ=%.2e" % sm_d)
    check("%s: per-step argmax-identical over stream" % tag, sm_ok)
    return outbin

run_injected("I1", 1, [0.7])
run_injected("I2", 2, [0.5, -0.4])

print("\n[b0] gate=0 no-regression (BGB decodes identically to base)")
model0, binds0 = make_injected(1, [0.0])
pt0 = os.path.join(WORK, "inj_gate0.pt"); bin0 = os.path.join(WORK, "inj_gate0.bin")
save_injected_pt(binds0, [0.0], pt0)
S.serialize_bind(base_bin, pt0, bin0)
W0 = D.bg_load(bin0)
check("gate0: n_bind==1 present in trailer", len(W0.get("bind", [])) == 1)
np_g0 = D.bytegpt_decode_argmax(bin0, seed, 40)["ids"]
check("gate0: BGB stream BYTE-IDENTICAL to base stream", np_g0 == np_base_kv)
# also sampled-decode identity (the path anima evaluate --py uses)
s_base = D.bytegpt_decode_topk_sampled_W(Wbase, "hello world ", 40, 40, 0.7, 7)["ids"]
s_g0 = D.bytegpt_decode_topk_sampled_W(W0, "hello world ", 40, 40, 0.7, 7)["ids"]
check("gate0: top-k sampled stream BYTE-IDENTICAL to base (evaluate path)", s_g0 == s_base)

print("\n" + "=" * 68)
if FAILS:
    print("RESULT: FAIL (%d checks failed): %s" % (len(FAILS), ", ".join(FAILS)))
    sys.exit(1)
print("RESULT: ALL PASS — BGB injected-bind decode+serialize byte-exact (torch f64 ref).")
sys.exit(0)
