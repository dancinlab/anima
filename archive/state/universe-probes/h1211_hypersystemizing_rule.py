"""
H_1211 — HYPER-SYSTEMIZING / EXACT RULE EXTRAPOLATION (savant standalone)
Savant prodigies (calendar calculators, lightning arithmeticians) excel at
LAWFUL, rule-governed structured domains — Baron-Cohen's hyper-systemizing
account of savant talent. The signature is EXACT-RULE generalization to UNSEEN
instances, not interpolative memorization.

TASK (self-contained synthetic, no corpus): single-digit addition. Lines
"A+B=C\\n" with A,B in 0..9, C=A+B. Train on a fixed 80% subset of the 100
(A,B) pairs (each repeated); HELD-OUT 20% pairs are never shown. Test: prompt
"A+B=" for held-out pairs, greedy-decode the answer, compare to C EXACTLY.
CONTROL: an identical model trained on SHUFFLED targets (C' = a fixed random
permutation of sums) — no learnable rule, only memorization -> must fail held-out.

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 RULE-EXTRAPOLATION — held-out exact-answer accuracy >= 0.90 (the exact
                          arithmetic rule generalizes to unseen pairs).
  F2 NOT-MEMORIZATION   — rule held-out accuracy - shuffled-control held-out
                          accuracy >= 0.40 (the skill is the RULE, not lookup).
  H_1211 SUPPORTED iff F1 AND F2 (hyper-systemizing exact-rule mastery).
  CLOSED-NEGATIVE (a_paper_negative_ok) iff F1 fails: the substrate does NOT
  extract the exact rule (interpolative, not savant hyper-systemizing).

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU. Substrate from H_1142.
"""
import os, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"
BLOCK = 32; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 2500; BS = 64; LR = 3e-4
REPEAT = 4000   # corpus = REPEAT shuffled passes over train pairs
HELDOUT_FRAC = 0.20
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1211_hypersystemizing_rule")


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
        return F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))


def make_corpus(train_pairs, sum_map):
    rng = random.Random(SEED)
    lines = []
    for _ in range(REPEAT):
        p = list(train_pairs); rng.shuffle(p)
        for (a, b) in p:
            lines.append(f"{a}+{b}={sum_map[(a,b)]}\n")
    return "".join(lines).encode()


def train_model(data_bytes):
    data = torch.frombuffer(bytearray(data_bytes), dtype=torch.uint8).clone()
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    t0 = time.time()
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for g in opt.param_groups: g["lr"] = lr_t
        ix = torch.randint(0, data.numel() - BLOCK - 1, (BS,))
        x = torch.stack([data[i:i+BLOCK] for i in ix]).long()
        y = torch.stack([data[i+1:i+BLOCK+1] for i in ix]).long()
        l = m.loss_on(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 500 == 0 or st == STEPS-1:
            print(f"  [train] step {st} ce={l.item():.4f} {(time.time()-t0)/60:.1f}min", flush=True)
    m.eval(); return m


@torch.no_grad()
def eval_pairs(m, pairs, sum_map):
    ok = 0
    for (a, b) in pairs:
        prompt = f"{a}+{b}=".encode()
        ids = torch.tensor(list(prompt), dtype=torch.long, device=DEV)[None]
        out = []
        for _ in range(3):  # answer is 1-2 digits then newline
            logits = m(ids[:, -BLOCK:])
            nxt = int(torch.argmax(logits[0, -1, :]).item())
            if nxt == ord("\n"): break
            out.append(nxt); ids = torch.cat([ids, torch.tensor([[nxt]], device=DEV)], 1)
        ans = bytes(out).decode("utf-8", "ignore")
        if ans == str(sum_map[(a, b)]): ok += 1
    return ok / len(pairs)


def run_arm(train_pairs, held_pairs, sum_map, tag):
    corpus = make_corpus(train_pairs, sum_map)
    print(f"  [{tag}] corpus={len(corpus)/1e6:.1f}MB train_pairs={len(train_pairs)} held={len(held_pairs)}", flush=True)
    m = train_model(corpus)
    acc_tr = eval_pairs(m, train_pairs, sum_map)
    acc_ho = eval_pairs(m, held_pairs, sum_map)
    print(f"  [{tag}] train_acc={acc_tr:.4f} heldout_acc={acc_ho:.4f}", flush=True)
    return acc_tr, acc_ho


def main():
    print("=== H_1211 hyper-systemizing exact rule extrapolation ===", flush=True)
    all_pairs = [(a, b) for a in range(10) for b in range(10)]
    rng = random.Random(SEED); rng.shuffle(all_pairs)
    n_ho = int(len(all_pairs) * HELDOUT_FRAC)
    held_pairs = all_pairs[:n_ho]; train_pairs = all_pairs[n_ho:]
    true_sum = {(a, b): a + b for (a, b) in all_pairs}
    # shuffled control: a fixed random bijection on the set of sum-values per pair
    perm = list(range(19)); rng.shuffle(perm)
    shuf_sum = {(a, b): perm[a + b] for (a, b) in all_pairs}

    print("--- RULE arm (true addition) ---", flush=True)
    r_tr, r_ho = run_arm(train_pairs, held_pairs, true_sum, "RULE")
    print("--- CONTROL arm (shuffled targets) ---", flush=True)
    c_tr, c_ho = run_arm(train_pairs, held_pairs, shuf_sum, "SHUFFLE")

    f1 = r_ho >= 0.90
    f2 = (r_ho - c_ho) >= 0.40
    supported = bool(f1 and f2)
    if supported:
        ruling = "SUPPORTED: hyper-systemizing — the exact addition rule generalizes to unseen pairs (held-out>=0.90) far above the memorization control"
    elif not f1:
        ruling = "CLOSED-NEGATIVE: no exact-rule extrapolation (held-out<0.90) — interpolative, not savant hyper-systemizing"
    else:
        ruling = "CLOSED-NEGATIVE: rule arm not separated from memorization control (gap<0.40)"

    verdict = {
        "H": "H_1211",
        "title": "hyper-systemizing / exact rule extrapolation",
        "rule_train_acc": r_tr, "rule_heldout_acc": r_ho,
        "shuffle_train_acc": c_tr, "shuffle_heldout_acc": c_ho,
        "F1_rule_extrapolation": {"rule_heldout_acc": r_ho, "bar": 0.90, "pass": bool(f1)},
        "F2_not_memorization": {"rule_minus_shuffle_heldout": r_ho - c_ho, "bar": 0.40, "pass": bool(f2)},
        "supported": supported,
        "ruling": ruling,
        "neuroscience_anchor": "hyper-systemizing (Baron-Cohen); calendar/lightning savant exact-rule mastery (Treffert)",
        "scope": "toy ByteGPT d256/4L CPU synthetic addition — scale-up UNVERIFIED (a_scale_honest_scope)",
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
