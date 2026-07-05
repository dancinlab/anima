"""E1 rung-3: byte-LM-faithful next-token CE (single autoregressive head, NO
role/filler head scaffold). Decoder emits A then B from trunk rep via ONE shared
next-token stream — model must discover ordered structure. ADDITIVE vs SLOT trunk.
Held-out ordered-pair generalization. DIRECTIONAL synthetic, multi-seed, p7."""
import json
import torch, torch.nn as nn, torch.nn.functional as F

K, D = 24, 64
HELD, EPOCHS, LR = 0.30, 5000, 1e-3
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
    E = nn.Embedding(K, D).to(dev)         # input concept embeddings
    O = nn.Embedding(K, D).to(dev)         # output token embeddings (autoregressive feed)
    Rr = nn.Linear(D, D, bias=False).to(dev)
    Rf = nn.Linear(D, D, bias=False).to(dev)
    f = nn.Sequential(nn.Linear(D, 256), nn.ReLU(), nn.Linear(256, 256), nn.ReLU()).to(dev)
    step2 = nn.Sequential(nn.Linear(256 + D, 256), nn.ReLU()).to(dev)  # consumes state + emb(prev-emitted)
    head = nn.Linear(256, K).to(dev)       # SINGLE shared next-token head
    P = list(E.parameters()) + list(O.parameters()) + list(f.parameters()) + list(step2.parameters()) + list(head.parameters())
    if trunk == 'slot':
        P += list(Rr.parameters()) + list(Rf.parameters())
    opt = torch.optim.Adam(P, lr=LR)

    def rep(a, b):
        ea, eb = E(a), E(b)
        return ea + eb if trunk == 'additive' else Rr(ea) + Rf(eb)

    a_tr = torch.tensor([p[0] for p in tr], device=dev)
    b_tr = torch.tensor([p[1] for p in tr], device=dev)
    a_ho = torch.tensor([p[0] for p in ho], device=dev)
    b_ho = torch.tensor([p[1] for p in ho], device=dev)
    for _ in range(EPOCHS):
        opt.zero_grad()
        s1 = f(rep(a_tr, b_tr))
        l1 = head(s1)                                   # predict A
        s2 = step2(torch.cat([s1, O(a_tr)], dim=-1))    # teacher-force true A
        l2 = head(s2)                                   # predict B
        loss = F.cross_entropy(l1, a_tr) + F.cross_entropy(l2, b_tr)
        loss.backward(); opt.step()

    def evalset(a, b):
        with torch.no_grad():
            s1 = f(rep(a, b)); p1 = head(s1).argmax(1)
            s2 = step2(torch.cat([s1, O(p1)], dim=-1)); p2 = head(s2).argmax(1)  # feed GREEDY A
            both = ((p1 == a) & (p2 == b)).float().mean().item()
            first = (p1 == a).float().mean().item()
            return both, first
    both_ho, first_ho = evalset(a_ho, b_ho)
    both_tr, _ = evalset(a_tr, b_tr)
    both_shuf = None
    if trunk == 'slot':
        with torch.no_grad():
            s1 = f(Rf(E(a_ho)) + Rr(E(b_ho))); p1 = head(s1).argmax(1)
            s2 = step2(torch.cat([s1, O(p1)], dim=-1)); p2 = head(s2).argmax(1)
            both_shuf = ((p1 == a_ho) & (p2 == b_ho)).float().mean().item()
    return dict(both=both_ho, first=first_ho, both_train=both_tr, both_shuffle=both_shuf)

out = {'device': dev, 'K': K, 'D': D, 'held_frac': HELD, 'epochs': EPOCHS, 'seeds': SEEDS,
       'note': 'single autoregressive next-token CE, no role/filler head scaffold'}
for trunk in ['additive', 'slot']:
    rs = [run(s, trunk) for s in SEEDS]
    agg = {k: (None if rs[0][k] is None else sum(r[k] for r in rs) / len(rs)) for k in rs[0]}
    out[trunk] = {'per_seed': rs, 'mean': agg}
sb, ab = out['slot']['mean']['both'], out['additive']['mean']['both']
ss = out['slot']['mean']['both_shuffle']
out['verdict'] = {
    'slot_heldout_both': sb, 'additive_heldout_both': ab,
    'slot_beats_additive': sb > ab + 0.10, 'slot_generalizes': sb > 0.5,
    'shuffle_collapses': (ss is not None and ss < sb - 0.10),
    'call': 'CE-INDUCES-SLOTS(303M GO reinforced)' if (sb > 0.5 and sb > ab + 0.10) else 'CE-COLLAPSES(slot needs head-scaffold)',
}
print(json.dumps(out, indent=2))
