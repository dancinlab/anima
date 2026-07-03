#!/usr/bin/env python3
"""
Escape-2 TOY discriminator (mini $0, numpy) — TPR forward-invariant hard-wire.

Question the escape hinges on (H_9121): can a Smolensky tensor-product (TPR)
binding slot HARD-WIRED into the forward circuit — NOT an added objective, CE
unchanged — surface held-out RECOMBINATION that an additive baseline cannot?

Two probes:
  (M) MECHANISM probe (textbook, expected REACHABLE): with FIXED random codes,
      does outer-product bind + role-unbind retrieve idea-specific fillers that a
      flat additive sum cannot? Ablation = replace outer product by flat sum.
      This reproduces H_1466 (binding leg acc_match=1.0 vs acc_flat=chance).

  (C) CE-TRAINED recombination probe (the ACTUAL escape discriminator): train
      end-to-end with plain CE (learned embeddings + readout) on a compositional
      task whose held-out split is a novel recombination of KNOWN fillers in
      KNOWN roles. Compare three forwards under the SAME CE objective+budget:
        - ADDITIVE  : h = sum of filler/role embeds (superposition)
        - TPR       : h carries filler(x)role outer-product bind slot (multiplic.)
        - TPR_ABL   : TPR forward but bind slot bypassed -> additive (causal test)
      REACHABLE iff  TPR held-out recomb > ADDITIVE  AND  TPR_ABL falls to floor
      (== ADDITIVE), i.e. the outer product is load-bearing under CE.
      AT-FLOOR iff CE does not drive the slot to be used (TPR ~ ADDITIVE on
      held-out) -> architecture swallowed by CE-basin (H_1816/H_1813 pattern).

No objective term is added anywhere (pure forward hard-wire). CE only.
"""
import numpy as np

# ---------------------------------------------------------------- (M) mechanism
def mechanism_probe(seed, d=32, R=4, N=4):
    """Fixed random role/filler codes. Bind S=sum_i f_i (x) r_i. Retrieve filler
    for role r_q via unbind (r_q^T S). ADDITIVE ablation: S_flat = sum_i f_i (no
    role), retrieve = nearest filler to S_flat (crosstalk). Report retrieval acc.
    """
    rng = np.random.default_rng(seed)
    roles = rng.standard_normal((R, d)); roles /= np.linalg.norm(roles, axis=1, keepdims=True)
    F = 8
    fillers = rng.standard_normal((F, d)); fillers /= np.linalg.norm(fillers, axis=1, keepdims=True)
    trials = 200
    ok_tpr = 0; ok_flat = 0
    for _ in range(trials):
        idx = rng.choice(F, size=N, replace=False)      # N distinct fillers
        rs  = rng.choice(R, size=N, replace=False)       # N distinct roles
        # TPR bind: S[d,d] = sum_i outer(filler_i, role_i)
        S = np.zeros((d, d))
        for i in range(N):
            S += np.outer(fillers[idx[i]], roles[rs[i]])
        # ADDITIVE (ablate outer product): flat superposition of fillers only
        S_flat = sum(fillers[idx[i]] for i in range(N))
        # query a random one of the N bindings
        q = rng.integers(N)
        rq = roles[rs[q]]
        # TPR unbind: recovered = S @ rq  (== filler_q + crosstalk that -> 0 for orth019 roles)
        rec = S @ rq
        pred = np.argmax(fillers @ rec)
        ok_tpr += int(pred == idx[q])
        # additive: no role info -> best you can do is nearest filler to the flat sum
        predf = np.argmax(fillers @ S_flat)
        ok_flat += int(predf == idx[q])
    return ok_tpr / trials, ok_flat / trials


# ---------------------------------------------------------------- (C) CE-trained
# Compositional task: input describes bindings role0=a, role1=b (a,b in 0..F-1).
# Target = 2-token output [g(a), g(b)] where g is a FIXED per-filler permutation.
# To emit target for a held-out (a,b) never trained together, the model must bind
# each role to its filler SEPARABLY then map g. Additive superposition crosstalks
# across the two role slots; TPR unbinds cleanly. Learned embeds + readout, CE.

def make_task(seed, F=8):
    rng = np.random.default_rng(seed)
    g = rng.permutation(F)                     # fixed output map g(filler)->symbol
    pairs = [(a, b) for a in range(F) for b in range(F)]
    rng.shuffle(pairs)
    n_ho = (F * F) // 3
    heldout = set(pairs[:n_ho])
    train = [p for p in pairs if p not in heldout]
    # ensure every filler appears in BOTH roles somewhere in train (recombination,
    # not extrapolation to unseen symbols)
    seen0 = set(a for a, _ in train); seen1 = set(b for _, b in train)
    heldout = [p for p in heldout if p[0] in seen0 and p[1] in seen1]
    return g, train, list(heldout), F


class Model:
    """Minimal 1-hidden readout over a bound representation h[d].
    mode: 'add'  -> h = Efil[a] + Efil[b] + Erole0 + Erole1     (superposition)
          'tpr'  -> h = flatten( Efil[a](x)Erole[0] + Efil[b](x)Erole[1] )  slot
          'abl'  -> tpr wiring but slot replaced by flat additive (bypass)
    Two independent linear heads read out g(a) (via role0) and g(b) (via role1).
    Everything below the readout is the forward hard-wire; CE is the ONLY loss.
    """
    def __init__(self, mode, F, d=16, seed=0):
        self.mode = mode; self.F = F; self.d = d
        rng = np.random.default_rng(1000 + seed)
        s = 0.3
        self.Efil = rng.standard_normal((F, d)) * s      # filler embeds (learned)
        self.Erole = rng.standard_normal((2, d)) * s     # role embeds (learned)
        hdim = d * d if mode == 'tpr' else d             # tpr slot is d*d flat
        # two readout heads: head r reads role r's filler-symbol
        self.W = [rng.standard_normal((F, hdim)) * (1.0/np.sqrt(hdim)) for _ in range(2)]
        self.b = [np.zeros(F) for _ in range(2)]

    def hidden(self, a, b):
        if self.mode == 'add':
            return self.Efil[a] + self.Efil[b] + self.Erole[0] + self.Erole[1]
        if self.mode == 'abl':
            # tpr-shaped wiring but bind slot bypassed to flat additive
            return self.Efil[a] + self.Efil[b] + self.Erole[0] + self.Erole[1]
        # tpr: multiplicative bind slot S = fa(x)r0 + fb(x)r1, flattened
        S = np.outer(self.Efil[a], self.Erole[0]) + np.outer(self.Efil[b], self.Erole[1])
        return S.reshape(-1)

    def logits(self, a, b):
        h = self.hidden(a, b)
        return h, [self.W[r] @ h + self.b[r] for r in range(2)]

    def train(self, g, train, epochs=800, lr=0.05, wd=1e-5, seed=0):
        rng = np.random.default_rng(7 + seed)
        data = list(train)

        def clip(x, c=5.0):
            n = np.linalg.norm(x)
            return x * (c / n) if n > c else x

        for ep in range(epochs):
            rng.shuffle(data)
            for (a, b) in data:
                tgt = [g[a], g[b]]
                h, logs = self.logits(a, b)
                gEfil_a = np.zeros(self.d); gEfil_b = np.zeros(self.d)
                gErole = [np.zeros(self.d), np.zeros(self.d)]
                dW = [None, None]; db = [None, None]
                for r in range(2):
                    z = logs[r] - logs[r].max()
                    p = np.exp(z); p /= p.sum()
                    p[tgt[r]] -= 1.0                     # dCE/dlogit
                    gh = self.W[r].T @ p                 # dL/dh with PRE-update W
                    dW[r] = np.outer(p, h) + wd * self.W[r]
                    db[r] = p
                    if self.mode in ('add', 'abl'):
                        gEfil_a += gh; gEfil_b += gh
                        gErole[0] += gh; gErole[1] += gh
                    else:
                        G = gh.reshape(self.d, self.d)  # dL/dS
                        gEfil_a += G @ self.Erole[0]
                        gEfil_b += G @ self.Erole[1]
                        gErole[0] += G.T @ self.Efil[a]
                        gErole[1] += G.T @ self.Efil[b]
                # apply (after grads computed w/ pre-update params) + clip
                for r in range(2):
                    self.W[r] -= lr * clip(dW[r], 10.0)
                    self.b[r] -= lr * clip(db[r])
                self.Efil[a] -= lr * clip(gEfil_a + wd * self.Efil[a])
                self.Efil[b] -= lr * clip(gEfil_b + wd * self.Efil[b])
                self.Erole[0] -= lr * clip(gErole[0] + wd * self.Erole[0])
                self.Erole[1] -= lr * clip(gErole[1] + wd * self.Erole[1])

    def acc(self, g, pairs):
        if not pairs: return float('nan')
        ok = 0
        for (a, b) in pairs:
            _, logs = self.logits(a, b)
            pa = np.argmax(logs[0]); pb = np.argmax(logs[1])
            ok += int(pa == g[a] and pb == g[b])
        return ok / len(pairs)


def ce_probe(seed):
    g, train, heldout, F = make_task(seed)
    out = {}
    for mode in ('add', 'tpr', 'abl'):
        m = Model(mode, F, d=16, seed=seed)
        m.train(g, train, epochs=800, lr=0.05, seed=seed)
        out[mode] = {'train': round(m.acc(g, train), 4),
                     'heldout': round(m.acc(g, heldout), 4)}
    out['n_train'] = len(train); out['n_heldout'] = len(heldout)
    return out


if __name__ == '__main__':
    print("=== (M) MECHANISM probe: TPR outer-product vs additive-flat (fixed codes) ===")
    tprs, flats = [], []
    for s in [7, 4302, 4303]:
        t, f = mechanism_probe(s)
        tprs.append(t); flats.append(f)
        print(f"  seed {s}: TPR-unbind acc={t:.3f}  ADDITIVE-flat acc={f:.3f}")
    print(f"  MEAN: TPR={np.mean(tprs):.3f}  ADDITIVE={np.mean(flats):.3f}  (chance=1/8=0.125)")

    print()
    print("=== (C) CE-TRAINED recombination probe (the escape discriminator) ===")
    print("    held-out = novel (a,b) recombination of KNOWN fillers/roles; CE only")
    agg = {'add': [], 'tpr': [], 'abl': []}
    for s in [7, 4302, 4303]:
        r = ce_probe(s)
        for mode in ('add', 'tpr', 'abl'):
            agg[mode].append(r[mode]['heldout'])
        print(f"  seed {s} (train={r['n_train']} ho={r['n_heldout']}): "
              f"ADD ho={r['add']['heldout']:.3f} (tr {r['add']['train']:.2f}) | "
              f"TPR ho={r['tpr']['heldout']:.3f} (tr {r['tpr']['train']:.2f}) | "
              f"ABL ho={r['abl']['heldout']:.3f} (tr {r['abl']['train']:.2f})")
    ma = np.mean(agg['add']); mt = np.mean(agg['tpr']); mb = np.mean(agg['abl'])
    print(f"  MEAN held-out recomb:  ADD={ma:.3f}  TPR={mt:.3f}  ABL={mb:.3f}")
    print()
    lift = mt - ma
    abl_floor = abs(mb - ma) < 0.10       # ablation returns to additive floor
    reachable = (mt > ma + 0.10) and abl_floor
    print("=== VERDICT (CE-trained discriminator) ===")
    print(f"  TPR-vs-ADD held-out lift = {lift:+.3f}   (need > +0.10)")
    print(f"  ABL back to ADD floor?   = {abl_floor}  (|ABL-ADD|={abs(mb-ma):.3f} < 0.10)")
    print(f"  RESULT: {'REACHABLE' if reachable else 'AT-FLOOR'}")
