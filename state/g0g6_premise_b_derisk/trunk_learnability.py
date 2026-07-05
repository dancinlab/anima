"""E1 trunk-learnability: does end-to-end SGD LEARN slots in the trunk?
ADDITIVE (order-blind sum, forced R=I) vs SLOT (learned role/filler transforms).
Held-out ORDERED-pair compositional generalization. DIRECTIONAL synthetic rung
before 303M. frozen-first, multi-seed, no tune-to-green (p7)."""
import json, sys
import torch, torch.nn as nn, torch.nn.functional as F

K, D = 24, 64
HELD, EPOCHS, LR = 0.30, 4000, 1e-3
SEEDS = [7, 4302, 4303]
dev = 'cuda' if torch.cuda.is_available() else 'cpu'

def pairs():
    return [(a, b) for a in range(K) for b in range(K) if a != b]

def run(seed, trunk):
    torch.manual_seed(seed)
    ps = pairs()
    idx = torch.randperm(len(ps)).tolist()
    ps = [ps[i] for i in idx]
    n_ho = int(len(ps) * HELD)
    ho, tr = ps[:n_ho], ps[n_ho:]
    E = nn.Embedding(K, D).to(dev)
    Rr = nn.Linear(D, D, bias=False).to(dev)
    Rf = nn.Linear(D, D, bias=False).to(dev)
    read = nn.Sequential(nn.Linear(D, 256), nn.ReLU(), nn.Linear(256, 256), nn.ReLU()).to(dev)
    hr = nn.Linear(256, K).to(dev)
    hf = nn.Linear(256, K).to(dev)
    ps_list = list(E.parameters()) + list(read.parameters()) + list(hr.parameters()) + list(hf.parameters())
    if trunk == 'slot':
        ps_list += list(Rr.parameters()) + list(Rf.parameters())
    opt = torch.optim.Adam(ps_list, lr=LR)

    def comb(a, b):
        ea, eb = E(a), E(b)
        return ea + eb if trunk == 'additive' else Rr(ea) + Rf(eb)

    a_tr = torch.tensor([p[0] for p in tr], device=dev)
    b_tr = torch.tensor([p[1] for p in tr], device=dev)
    a_ho = torch.tensor([p[0] for p in ho], device=dev)
    b_ho = torch.tensor([p[1] for p in ho], device=dev)
    for _ in range(EPOCHS):
        opt.zero_grad()
        h = read(comb(a_tr, b_tr))
        loss = F.cross_entropy(hr(h), a_tr) + F.cross_entropy(hf(h), b_tr)
        loss.backward(); opt.step()
    with torch.no_grad():
        h = read(comb(a_ho, b_ho))
        rp, fp = hr(h).argmax(1), hf(h).argmax(1)
        both = ((rp == a_ho) & (fp == b_ho)).float().mean().item()
        role = (rp == a_ho).float().mean().item()
        fill = (fp == b_ho).float().mean().item()
        ht = read(comb(a_tr, b_tr))
        both_tr = ((hr(ht).argmax(1) == a_tr) & (hf(ht).argmax(1) == b_tr)).float().mean().item()
        both_shuf = None
        if trunk == 'slot':
            h2 = read(Rf(E(a_ho)) + Rr(E(b_ho)))  # swap role/filler transforms
            both_shuf = ((hr(h2).argmax(1) == a_ho) & (hf(h2).argmax(1) == b_ho)).float().mean().item()
    return dict(role=role, fill=fill, both=both, both_train=both_tr, both_shuffle=both_shuf)

out = {'device': dev, 'K': K, 'D': D, 'held_frac': HELD, 'epochs': EPOCHS, 'seeds': SEEDS, 'chance_both': 1.0 / (K * (K - 1))}
for trunk in ['additive', 'slot']:
    rs = [run(s, trunk) for s in SEEDS]
    agg = {k: (None if rs[0][k] is None else sum(r[k] for r in rs) / len(rs)) for k in rs[0]}
    out[trunk] = {'per_seed': rs, 'mean': agg}
# verdict
add_both = out['additive']['mean']['both']
slot_both = out['slot']['mean']['both']
slot_shuf = out['slot']['mean']['both_shuffle']
out['verdict'] = {
    'slot_heldout_both': slot_both, 'additive_heldout_both': add_both,
    'slot_beats_additive': slot_both > add_both + 0.10,
    'slot_generalizes': slot_both > 0.5,
    'shuffle_collapses': (slot_shuf is not None and slot_shuf < slot_both - 0.10),
    'call': 'TRUNK-LEARNS-SLOTS(303M GO)' if (slot_both > 0.5 and slot_both > add_both + 0.10) else 'TRUNK-COLLAPSES(E1 WEAKENED)',
}
print(json.dumps(out, indent=2))
