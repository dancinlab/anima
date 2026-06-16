"""
H_1223 — SAVANT ISLAND SEED-STABILITY (innate vs random specialization)
Savant talent is a STABLE trait — the same islands of skill recur, not random.
Is the substrate's high-skill "island" (which contexts it predicts well) a STRUCTURAL
property of the data, recurring across independent trainings, or a seed-random artifact?

TASK: train K=3 ByteGPT models with DIFFERENT seeds (independent init + data order).
On the SAME held-out decision points, record per-item greedy correctness for each.
If specialization is innate (data-structural), the SAME items are right/wrong across
seeds → high inter-seed agreement beyond chance. If seed-random → chance agreement.

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 SEED-STABLE — mean pairwise Cohen's kappa on per-item correctness >= 0.30
                   (substantial agreement; the island is a stable/innate property,
                   not seed-random).
  F2 ABOVE-CHANCE — mean observed agreement > mean chance agreement by >= 0.05
                   (sanity: agreement exceeds what marginal accuracy forces).
  H_1223 SUPPORTED iff F1 AND F2 (savant island is structurally stable across seeds).
  CLOSED-NEGATIVE (a_paper_negative_ok) iff kappa < 0.30 — specialization is
  seed-dependent, not an innate structural trait.

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice. Substrate from H_1142.
"""
import os, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

BASE_SEED = 7
DEV = "cpu"
CORPUS = os.environ.get("CORPUS", "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt")
EN_SLICE_BYTES = 24 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1200; BS = 16; LR = 3e-4
N_DEC = 3000; HELDOUT_FRAC = 0.10
SEEDS = [7, 17, 27]
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1223_savant_island_seed_stability")


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
        T = idx.shape[1]; pos = torch.arange(T, device=idx.device)
        x = s.tok(idx) + s.pos(pos)[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.lnf(x))
    def loss_on(s, idx, targets):
        logits = s(idx)
        return F.cross_entropy(logits.reshape(-1, VOCAB), targets.reshape(-1))


def train_model(data, seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    g = torch.Generator().manual_seed(seed)
    t0 = time.time()
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for grp in opt.param_groups: grp["lr"] = lr_t
        ix = torch.randint(0, data.numel() - BLOCK - 1, (BS,), generator=g)
        x = torch.stack([data[i:i+BLOCK] for i in ix]).long().to(DEV)
        y = torch.stack([data[i+1:i+BLOCK+1] for i in ix]).long().to(DEV)
        l = m.loss_on(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 400 == 0 or st == STEPS-1:
            print(f"  [seed {seed} train] step {st} ce={l.item():.4f} {(time.time()-t0)/60:.1f}min", flush=True)
    m.eval(); return m


@torch.no_grad()
def per_item_correct(m, held, positions):
    out = []
    for pos in positions:
        ctx = held[pos-BLOCK:pos].long()[None].to(DEV)
        tb = int(held[pos].item())
        pred = int(torch.argmax(m(ctx)[0, -1, :]).item())
        out.append(1 if pred == tb else 0)
    return np.array(out)


def cohen_kappa(a, b):
    a = np.asarray(a, int); b = np.asarray(b, int); n = len(a)
    po = float((a == b).mean())
    pa1 = a.mean(); pb1 = b.mean()
    pe = pa1*pb1 + (1-pa1)*(1-pb1)
    return (po - pe) / (1 - pe) if (1 - pe) > 1e-9 else 0.0, po, pe


def main():
    print("=== H_1223 savant island seed-stability (innate vs random) ===", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8).clone()
    cut = int(data.numel() * (1 - HELDOUT_FRAC)); train_data, held = data[:cut], data[cut:]
    print(f"[data] train={train_data.numel()/1e6:.1f}MB held={held.numel()/1e6:.1f}MB", flush=True)
    rng = random.Random(BASE_SEED); n = held.numel()
    positions = [rng.randint(BLOCK, n - 2) for _ in range(N_DEC)]   # SAME items for all seeds

    corrects = []
    for sd in SEEDS:
        print(f"--- training seed {sd} ---", flush=True)
        m = train_model(train_data, sd)
        c = per_item_correct(m, held, positions)
        print(f"  [seed {sd}] acc={c.mean():.4f}", flush=True)
        corrects.append(c)

    kappas, pos_obs, pos_exp = [], [], []
    for i in range(len(SEEDS)):
        for j in range(i+1, len(SEEDS)):
            k, po, pe = cohen_kappa(corrects[i], corrects[j])
            kappas.append(k); pos_obs.append(po); pos_exp.append(pe)
            print(f"  [pair {SEEDS[i]}x{SEEDS[j]}] kappa={k:.4f} obs_agree={po:.4f} chance={pe:.4f}", flush=True)
    mean_kappa = float(np.mean(kappas))
    mean_obs = float(np.mean(pos_obs)); mean_exp = float(np.mean(pos_exp))
    above_chance = mean_obs - mean_exp
    print(f"[summary] mean_kappa={mean_kappa:.4f} mean_obs_agree={mean_obs:.4f} mean_chance={mean_exp:.4f} above_chance={above_chance:+.4f}", flush=True)

    f1 = mean_kappa >= 0.30
    f2 = above_chance >= 0.05
    supported = bool(f1 and f2)
    if supported:
        ruling = f"SUPPORTED: the high-skill island is seed-stable (mean kappa {mean_kappa:.3f} >= 0.30, above-chance {above_chance:.3f}) — specialization is a structural/innate property of the data, not seed-random"
    elif not f1:
        ruling = f"CLOSED-NEGATIVE: per-item skill is seed-dependent (mean kappa {mean_kappa:.3f} < 0.30) — the savant island is not a stable innate trait"
    else:
        ruling = "CLOSED-NEGATIVE: agreement at/below chance (F2) — no structural island"

    verdict = {
        "H": "H_1223", "title": "savant island seed-stability (innate vs random)",
        "seeds": SEEDS, "per_seed_acc": [float(c.mean()) for c in corrects],
        "mean_kappa": mean_kappa, "mean_obs_agreement": mean_obs, "mean_chance_agreement": mean_exp,
        "above_chance": above_chance,
        "F1_seed_stable": {"mean_kappa": mean_kappa, "bar": 0.30, "pass": bool(f1)},
        "F2_above_chance": {"above_chance": above_chance, "bar": 0.05, "pass": bool(f2)},
        "supported": supported, "ruling": ruling,
        "neuroscience_anchor": "savant talent as a stable trait (Treffert 2009); innate vs experiential specialization",
        "scope": "toy ByteGPT d256/4L CPU en slice, 3 seeds — UNVERIFIED scale (a_scale_honest_scope)",
        "seed": BASE_SEED,
    }
    print("=== VERDICT ===", flush=True); print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(verdict, open(os.path.join(OUTDIR, "result.json"), "w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
