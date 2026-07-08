#!/usr/bin/env python3
"""
Stage-2 (Fable spec) — byte-surface + LM-objective resonator read-head.
Question: is the G1 wall a property of the CE read-path, not the byte-LM trunk?
One trunk per restart (a real byte-LM), FOUR read-paths swapped on the identical trunk:
  A  = the LM itself (free autoregressive greedy decode of the answer)
  A' = codebook-restricted A (argmax over 30 fillers by LM log-prob) -- output-space matched to B
  B  = fixed HRR resonator over trunk-extracted atoms (bind/unbind/cleanup fixed; atoms via trunk)
  B0 = B on a random-init (0-step) trunk (diagnostic)
  C  = additive read-path (⊛ -> +), same cleanup
Controls: bind-destroy (⊛->+ inside B), scene-shuffle (permute pair->scene in B memory), leak-check.
DIRECTIONAL (torch, no core/) -- bars gate the engine-native bridge, not a GREEN.
"""
import os, json, math, statistics as st
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as Fn

torch.use_deterministic_algorithms(True)
DEV = 'cuda' if torch.cuda.is_available() else 'cpu'

R, Fn_ROLES = 6, 30            # 6 roles, 30 fillers
NAME_LEN = 4
D_MODEL, N_LAYER, N_HEAD, BLOCK = 256, 4, 4, 64
LR, BATCH, MAX_STEPS = 3e-4, 256, int(os.environ.get("S2_STEPS", 20000))
N_RESTARTS = int(os.environ.get("S2_RESTARTS", 10))
N_EVAL = int(os.environ.get("S2_EVAL", 600))
VOCAB = 256

def is_heldout(r, f): return (f % R) == r

# ---------- names (surface form independent of ID structure) ----------
def make_names(seed):
    g = np.random.default_rng(20000 + seed)
    used = set(); roles = []; fills = []
    def draw():
        while True:
            s = bytes(g.integers(ord('a'), ord('z')+1, NAME_LEN).tolist())
            if s not in used: used.add(s); return s
    roles = [draw() for _ in range(R)]
    fills = [draw() for _ in range(Fn_ROLES)]
    return roles, fills

# ---------- scene serialization ----------
def scene_line(role_names, fill_names, rs, fs, qi):
    pairs = ";".join(f"{role_names[r].decode()}={fill_names[f].decode()}" for r, f in zip(rs, fs))
    ans = fill_names[fs[qi]].decode()
    prompt = f"{pairs};?{role_names[rs[qi]].decode()}="
    return prompt, ans   # full line = prompt + ans + "\n"

def sample_scene(g, mode):
    rs = g.choice(R, 3, replace=False).tolist()
    if mode == 'train' or mode == 'indist':
        fs, used = [], set()
        for r in rs:
            while True:
                f = int(g.integers(Fn_ROLES))
                if not is_heldout(r, f) and f not in used: break
            fs.append(f); used.add(f)
        qi = int(g.integers(3))
    else:  # heldout
        rq = rs[0]
        while True:
            ft = int(g.integers(Fn_ROLES))
            if is_heldout(rq, ft): break
        fs, used = [ft], {ft}
        for r in rs[1:]:
            while True:
                f = int(g.integers(Fn_ROLES))
                if not is_heldout(rq, f) and f not in used: break
            fs.append(f); used.add(f)
        qi = 0
    return rs, fs, qi

# ---------- byte transformer ----------
class Block(nn.Module):
    def __init__(s):
        super().__init__()
        s.ln1 = nn.LayerNorm(D_MODEL); s.ln2 = nn.LayerNorm(D_MODEL)
        s.attn = nn.MultiheadAttention(D_MODEL, N_HEAD, batch_first=True)
        s.mlp = nn.Sequential(nn.Linear(D_MODEL, 4*D_MODEL), nn.GELU(), nn.Linear(4*D_MODEL, D_MODEL))
    def forward(s, x, mask):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=mask, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteLM(nn.Module):
    def __init__(s, seed):
        super().__init__()
        torch.manual_seed(seed)
        s.emb = nn.Embedding(VOCAB, D_MODEL); s.pos = nn.Embedding(BLOCK, D_MODEL)
        s.blocks = nn.ModuleList([Block() for _ in range(N_LAYER)])
        s.lnf = nn.LayerNorm(D_MODEL); s.head = nn.Linear(D_MODEL, VOCAB, bias=False)
    def backbone(s, idx):
        T = idx.shape[1]
        x = s.emb(idx) + s.pos(torch.arange(T, device=idx.device))[None]
        mask = torch.triu(torch.full((T, T), float('-inf'), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        return s.lnf(x)
    def forward(s, idx): return s.head(s.backbone(idx))

def enc(sb): return torch.tensor([b for b in sb], dtype=torch.long)

def make_batch(g, role_names, fill_names, n, mode):
    lines = []
    for _ in range(n):
        rs, fs, qi = sample_scene(g, mode)
        p, a = scene_line(role_names, fill_names, rs, fs, qi)
        lines.append((p + a + "\n").encode())
    T = min(BLOCK, max(len(l) for l in lines))
    x = torch.full((n, T), ord('\n'), dtype=torch.long)
    for i, l in enumerate(lines):
        l = l[:T]; x[i, :len(l)] = enc(l)
    return x.to(DEV)

# ---------- atom extraction (context-free) ----------
def extract_atoms(model, names, Q):
    model.eval(); outs = []
    with torch.no_grad():
        for nm in names:
            s = b"\n" + nm
            h = model.backbone(enc(s)[None].to(DEV))[0, -1]     # last byte hidden
            outs.append(h)
    A = torch.stack(outs); A = A / (A.norm(dim=1, keepdim=True) + 1e-8)
    return (A @ Q.T)                                            # fixed orthogonal conditioning

# ---------- HRR ops ----------
def cconv(u, v): return torch.fft.irfft(torch.fft.rfft(u) * torch.fft.rfft(v), n=u.shape[-1])
def ccorr(s, u): return torch.fft.irfft(torch.fft.rfft(s) * torch.conj(torch.fft.rfft(u)), n=s.shape[-1])

# ---------- eval read-paths ----------
def eval_readpaths(model, role_names, fill_names, Q, seed, restart_invalid_cap=0.95):
    g = np.random.default_rng(90000 + seed)
    # build fixed eval scene sets
    ho = [sample_scene(g, 'heldout') for _ in range(N_EVAL)]
    ind = [sample_scene(g, 'indist') for _ in range(N_EVAL)]
    rU = extract_atoms(model, role_names, Q); fU = extract_atoms(model, fill_names, Q)

    def code_read(scenes, op, shuffle=False):
        hit = 0
        for rs, fs, qi in scenes:
            idxs = list(range(3))
            if shuffle:  # permute which filler is bound to which role in memory
                perm = [ (i+1)%3 for i in range(3) ]
                fs_mem = [fs[perm[i]] for i in range(3)]
            else: fs_mem = fs
            if op == 'conv':
                s = sum(cconv(rU[rs[i]], fU[fs_mem[i]]) for i in range(3))
                fh = ccorr(s, rU[rs[qi]])
            else:  # additive
                s = sum(rU[rs[i]] + fU[fs_mem[i]] for i in range(3))
                fh = s - rU[rs[qi]]
            pred = int(torch.argmax(Fn.cosine_similarity(fh[None], fU, dim=1)))
            hit += (pred == fs[qi])
        return hit / len(scenes)

    def lm_answer_greedy(prompt):
        idx = enc(prompt.encode())[None].to(DEV); out = []
        with torch.no_grad():
            for _ in range(NAME_LEN + 1):
                if idx.shape[1] >= BLOCK: idx = idx[:, -BLOCK:]
                nb = int(torch.argmax(model(idx)[0, -1]))
                if nb == ord('\n'): break
                out.append(nb); idx = torch.cat([idx, torch.tensor([[nb]], device=DEV)], 1)
        return bytes(out)

    def lm_logprob(prompt, cand):
        seq = (prompt + cand + "\n").encode()
        idx = enc(seq)[None].to(DEV)
        with torch.no_grad():
            logits = Fn.log_softmax(model(idx)[0], -1)
        lp = 0.0; start = len(prompt.encode())
        for t in range(start, len(seq)):
            lp += logits[t-1, seq[t]].item()
        return lp

    # A (free), A' (codebook), on held-out + in-dist
    def a_free(scenes):
        hit = 0
        for rs, fs, qi in scenes:
            p, a = scene_line(role_names, fill_names, rs, fs, qi)
            hit += (lm_answer_greedy(p) == fill_names[fs[qi]])
        return hit / len(scenes)
    def a_code(scenes):
        hit = 0
        for rs, fs, qi in scenes:
            p, a = scene_line(role_names, fill_names, rs, fs, qi)
            lps = [lm_logprob(p, fill_names[j].decode()) for j in range(Fn_ROLES)]
            hit += (int(np.argmax(lps)) == fs[qi])
        return hit / len(scenes)

    return dict(
        A_held=a_free(ho), A_ind=a_free(ind),
        Ap_held=a_code(ho), Ap_ind=a_code(ind),
        B_held=code_read(ho, 'conv'), B_ind=code_read(ind, 'conv'),
        B_binddestroy=code_read(ho, 'add'),
        B_shuffle=code_read(ho, 'conv', shuffle=True),
        C_held=code_read(ho, 'add'), C_ind=code_read(ind, 'add'),
    )

def train_trunk(seed, steps=MAX_STEPS, width=D_MODEL):
    role_names, fill_names = make_names(seed)
    model = ByteLM(seed).to(DEV)
    opt = torch.optim.AdamW(model.parameters(), lr=LR)
    g = np.random.default_rng(1000 + seed)
    tr_acc = 0.0
    for step in range(steps):
        x = make_batch(g, role_names, fill_names, BATCH, 'train')
        logits = model(x[:, :-1]); loss = Fn.cross_entropy(logits.reshape(-1, VOCAB), x[:, 1:].reshape(-1))
        opt.zero_grad(); loss.backward(); opt.step()
        if step % 1000 == 999:
            # quick train-answer acc proxy via greedy on 64 train scenes
            model.eval(); g2 = np.random.default_rng(7 + seed); hit = 0
            for _ in range(64):
                rs, fs, qi = sample_scene(g2, 'train')
                p, a = scene_line(role_names, fill_names, rs, fs, qi)
                idx = enc(p.encode())[None].to(DEV); out = []
                with torch.no_grad():
                    for _ in range(NAME_LEN+1):
                        if idx.shape[1] >= BLOCK: idx = idx[:, -BLOCK:]
                        nb = int(torch.argmax(model(idx)[0, -1]))
                        if nb == ord('\n'): break
                        out.append(nb); idx = torch.cat([idx, torch.tensor([[nb]], device=DEV)], 1)
                hit += (bytes(out) == fill_names[fs[qi]])
            tr_acc = hit / 64; model.train()
            if tr_acc >= 0.999 and step >= 4999: break
    return model, role_names, fill_names, round(tr_acc, 3), step+1

def run_restart(seed):
    torch.manual_seed(seed); np.random.seed(seed)
    Qm, _ = torch.linalg.qr(torch.randn(D_MODEL, D_MODEL, generator=torch.Generator().manual_seed(50000+seed)))
    Q = Qm.to(DEV)
    model, rn, fn2, tr, steps = train_trunk(seed)
    r = eval_readpaths(model, rn, fn2, Q, seed)
    r['train_acc'] = tr; r['steps'] = steps
    # B0: random-init trunk, same names/Q
    m0 = ByteLM(seed + 777).to(DEV)
    r0 = eval_readpaths(m0, rn, fn2, Q, seed)
    r['B0_held'] = r0['B_held']
    r['valid'] = (tr >= 0.999 and r['A_ind'] >= 0.95 and r['B_ind'] >= 0.95)
    return r

def med(xs): return round(st.median(xs), 4)

if __name__ == '__main__':
    print(f"device={DEV} deterministic byte-LM stage-2 · restarts={N_RESTARTS}", flush=True)
    R_ALL = []
    for s in range(N_RESTARTS):
        r = run_restart(s)
        R_ALL.append(r)
        print(f"seed{s} valid={r['valid']} train={r['train_acc']} | A={r['A_held']:.3f} A'={r['Ap_held']:.3f} "
              f"B={r['B_held']:.3f} B0={r['B0_held']:.3f} C={r['C_held']:.3f} "
              f"binddestroy={r['B_binddestroy']:.3f} shuf={r['B_shuffle']:.3f} | Aind={r['A_ind']:.2f} Bind={r['B_ind']:.2f}", flush=True)
    V = [r for r in R_ALL if r['valid']]
    n_invalid = len(R_ALL) - len(V)
    def col(k): return [r[k] for r in V]
    summ = {}
    if V:
        summ = dict(
            n_valid=len(V), n_invalid=n_invalid,
            B_med=med(col('B_held')), B_min=round(min(col('B_held')),4),
            C_med=med(col('C_held')), Ap_med=med(col('Ap_held')), A_med=med(col('A_held')),
            B0_med=med(col('B0_held')), binddestroy_med=med(col('B_binddestroy')), shuffle_med=med(col('B_shuffle')),
            BminusC_med=round(med(col('B_held'))-med(col('C_held')),4),
            BminusAp_med=round(med(col('B_held'))-med(col('Ap_held')),4),
            maxAp_lt_minB=(max(col('Ap_held')) < min(col('B_held'))),
        )
    # frozen bars (pre-registered)
    verdict = 'INVALID (>3/10 invalid or no valid restart)'
    if V and n_invalid <= 3:
        go = (summ['B_med']>=0.80 and summ['B_min']>=0.60 and summ['BminusC_med']>=0.50 and summ['C_med']<=0.20
              and summ['BminusAp_med']>=0.30 and summ['binddestroy_med']<=0.20 and summ['shuffle_med']<=0.13)
        kill = ((summ['B_med']<0.50 and summ['B0_med']>=0.80) or summ['BminusC_med']<0.20 or summ['BminusAp_med']<0.10)
        verdict = ('🟢 GO-bridge (operator escape survives byte+LM · DIRECTIONAL)' if go else
                   ('🔴 KILL' if kill else '🟠 MIXED — diagnose atom-geometry'))
    out = dict(spec='stage2_bytelm_resonator', device=DEV,
               config=dict(R=R,F=Fn_ROLES,d=D_MODEL,layers=N_LAYER,block=BLOCK,restarts=N_RESTARTS,chance=round(1/Fn_ROLES,4)),
               restarts=R_ALL, summary=summ, verdict=verdict)
    print("\n=== VERDICT:", verdict, "===")
    print(json.dumps(summ, indent=2))
    open('/tmp/stage2_result.json','w').write(json.dumps(out, indent=2, ensure_ascii=False))
