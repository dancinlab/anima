"""
H_1208 — SAVANT WEAK-CENTRAL-COHERENCE × METACOGNITION
Savant skill is theorized to rest on privileged access to LOCAL/detail information
with reduced top-down gestalt integration — "weak central coherence" (Happé &
Frith 2006) / Snyder's (2009) release-from-concept account. Linked metacognitive
prediction: a detail-driven system should be BLIND to when it is MISSING the
global context (it cannot tell its local view is insufficient).

TASK: greedy next-byte prediction on held-out text under two context windows of
the SAME positions: FULL (last 128 bytes) vs LOCAL (last 16 bytes only).
  acc_full, acc_local ; confidence = max softmax prob in each.

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 LOCAL-DOMINANCE  — acc(LOCAL-16) >= acc(FULL-128) - 0.03 (the global context
                        adds almost nothing: detail-driven, weak central coherence).
  F2 METACOG-BLIND-TO-CONTEXT — on positions the model gets WRONG under LOCAL but
                        RIGHT under FULL (i.e. global context WAS needed), the
                        model's LOCAL confidence is NOT lowered: mean LOCAL conf on
                        these "needed-global" positions >= 0.5 AND its confidence
                        there is NOT below its overall mean conf by more than 0.03
                        (it cannot feel that it is missing the gestalt).
  H_1208 SUPPORTED iff F1 AND F2 (savant profile: local-dominant skill that is
  metacognitively blind to context-insufficiency).
  CLOSED-NEGATIVE (a_paper_negative_ok) iff F1 fails (model genuinely integrates
  global context — normal central coherence) OR F2 fails (it CAN feel when local
  is insufficient — metacognition tracks context-need).

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice. Substrate reused
VERBATIM from H_1142.
"""
import os, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"
CORPUS = os.environ.get("CORPUS", "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt")
EN_SLICE_BYTES = 24 * 1024 * 1024
BLOCK = 128; LOCAL_W = 16; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
N_DEC = 4000
HELDOUT_FRAC = 0.10
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1208_savant_wcc_local_privilege")


class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.ln2 = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, h, batch_first=True)
        s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d))
    def forward(s, x, mask):
        a, _ = s.attn(s.ln1(x), s.ln1(x), s.ln1(x), attn_mask=mask, need_weights=False)
        x = x + a; x = x + s.mlp(s.ln2(x)); return x

class ByteGPT(nn.Module):
    def __init__(s, vocab=VOCAB, d=D, n_layer=NLAYER, n_head=NHEAD, block=BLOCK):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d)
        s.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        s.lnf = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False)
    def forward(s, idx):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = s.tok(idx) + s.pos(pos)[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.lnf(x))
    def loss_on(s, idx, targets):
        logits = s(idx)
        return F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))


def batch(data, block, bs, dev):
    ix = torch.randint(0, data.numel() - block - 1, (bs,))
    x = torch.stack([data[i:i+block] for i in ix]).long()
    y = torch.stack([data[i+1:i+block+1] for i in ix]).long()
    return x.to(dev), y.to(dev)


def train_model(data):
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    t0 = time.time()
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for g in opt.param_groups: g["lr"] = lr_t
        x, y = batch(data, BLOCK, BS, DEV)
        l = m.loss_on(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 250 == 0 or st == STEPS-1:
            print(f"  [train] step {st} ce={l.item():.4f} {(time.time()-t0)/60:.1f}min", flush=True)
    m.eval(); return m


@torch.no_grad()
def collect(m, held):
    rng = random.Random(SEED)
    n = held.numel()
    rows = []  # (corr_full, conf_full, corr_local, conf_local)
    for _ in range(N_DEC):
        pos = rng.randint(BLOCK, n - 2)
        true_b = int(held[pos].item())
        full = held[pos-BLOCK:pos].long()[None].to(DEV)
        loc = held[pos-LOCAL_W:pos].long()[None].to(DEV)
        lf = m(full); pl_full = F.softmax(lf[0, -1, :], dim=-1)
        ll = m(loc); pl_loc = F.softmax(ll[0, -1, :], dim=-1)
        cf = int(torch.argmax(pl_full).item()); clo = int(torch.argmax(pl_loc).item())
        rows.append((1 if cf == true_b else 0, float(pl_full.max().item()),
                     1 if clo == true_b else 0, float(pl_loc.max().item())))
    return np.array(rows, dtype=float)


def main():
    print("=== H_1208 savant weak-central-coherence x metacognition ===", flush=True)
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC))
    train_data, held = data[:cut], data[cut:]
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)

    print("--- training ---", flush=True)
    m_tr = train_model(train_data)

    print("--- TRAINED (collect full vs local) ---", flush=True)
    R = collect(m_tr, held)
    corr_full, conf_full, corr_loc, conf_loc = R[:,0], R[:,1], R[:,2], R[:,3]
    acc_full = float(corr_full.mean()); acc_loc = float(corr_loc.mean())
    mean_conf_loc = float(conf_loc.mean())
    # positions where global WAS needed: wrong-local but right-full
    needed = (corr_loc == 0) & (corr_full == 1)
    n_need = int(needed.sum())
    conf_loc_on_needed = float(conf_loc[needed].mean()) if n_need >= 10 else float("nan")
    conf_drop = (mean_conf_loc - conf_loc_on_needed) if not math.isnan(conf_loc_on_needed) else float("nan")
    print(f"  acc_full={acc_full:.4f} acc_local={acc_loc:.4f} (gap={acc_full-acc_loc:+.4f})", flush=True)
    print(f"  needed-global n={n_need} | local_conf_there={conf_loc_on_needed:.4f} vs overall_local_conf={mean_conf_loc:.4f} (drop={conf_drop:+.4f})", flush=True)

    f1 = acc_loc >= (acc_full - 0.03)
    f2 = (not math.isnan(conf_loc_on_needed)) and (conf_loc_on_needed >= 0.5) and (conf_drop <= 0.03)
    supported = bool(f1 and f2)
    if supported:
        ruling = "SUPPORTED: savant weak-central-coherence profile — local-dominant skill (global context barely used) AND metacognitively blind to context-insufficiency (confidence not lowered where global was needed)"
    elif not f1:
        ruling = "CLOSED-NEGATIVE: model integrates global context (acc_full > acc_local+0.03) — normal central coherence, not detail-locked"
    else:
        ruling = "CLOSED-NEGATIVE: model CAN feel context-insufficiency (local confidence drops where global needed) — metacognition tracks context-need"

    verdict = {
        "H": "H_1208",
        "title": "savant weak-central-coherence x metacognition (local privilege)",
        "acc_full": acc_full, "acc_local": acc_loc, "acc_gap_full_minus_local": acc_full - acc_loc,
        "F1_local_dominance": {"acc_local": acc_loc, "acc_full": acc_full, "bar": "local >= full-0.03", "pass": bool(f1)},
        "F2_metacog_blind_to_context": {"n_needed_global": n_need, "local_conf_on_needed": conf_loc_on_needed,
                                        "overall_local_conf": mean_conf_loc, "conf_drop": conf_drop,
                                        "bars": "conf_on_needed>=0.5 AND drop<=0.03", "pass": bool(f2)},
        "supported": supported,
        "ruling": ruling,
        "neuroscience_anchor": "weak central coherence (Happé & Frith 2006); Snyder 2009 release-from-concept",
        "scope": "toy ByteGPT d256/4L CPU en slice — scale-up UNVERIFIED (a_scale_honest_scope)",
        "seed": SEED,
    }
    print("=== VERDICT ===", flush=True)
    print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "result.json"), "w") as f:
        json.dump(verdict, f, indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
