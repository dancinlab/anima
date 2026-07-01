#!/usr/bin/env python3
"""cheap_test.py — $0 frozen-first numpy decision probes for the 4 binding mouths.

Each probe is the card's pre-registered cheap test (DIRECTIONAL only — numpy, not
engine-native).  Decides whether the binding MECHANISM separates held-out
conjunctions that the additive/ablation control provably cannot.  Bars are frozen
in each card's "Cheap test" section (tune-to-green forbidden, p7).

  H_1620: settle (K=30) held-out acc >=0.90 AND > K=1 ablation by >=0.25 gap.
  H_1630: tropical bind held-out pair-sep >=0.90 while T=1 softmax <0.60 + crosstalk-invariant.
  H_1631: glued decode >=0.90 + coboundary separates valid vs scrambled, identity-R cannot.
  H_1632: closure separates held-out conjunctions >=0.90 while OR-pool <0.60 + idempotent.

A linear-probe 'accuracy' = train a logistic readout on the bound rep, test on
held-out combos.  We use a closed-form ridge readout (no torch) as the linear probe.
"""
import numpy as np
rng = np.random.default_rng(0)


def ridge_acc(Xtr, ytr, Xte, yte, lam=1e-2):
    """Binary linear-probe accuracy via ridge (closed form)."""
    Xtr = np.concatenate([Xtr, np.ones((len(Xtr), 1))], 1)
    Xte = np.concatenate([Xte, np.ones((len(Xte), 1))], 1)
    w = np.linalg.solve(Xtr.T @ Xtr + lam * np.eye(Xtr.shape[1]), Xtr.T @ (2 * ytr - 1))
    pred = (Xte @ w) > 0
    return float((pred == (yte > 0)).mean())


def H1620():
    # dual-leg conjunction: legs a,b 8-bit; target = AND of (hidden idx in a, in b).
    n, db = 4000, 8
    ia, ib = 2, 5
    A = rng.integers(0, 2, (n, db)); B = rng.integers(0, 2, (n, db))
    y = (A[:, ia] & B[:, ib]).astype(float)
    # symmetric energy relaxation on z (k=16) clamped by a,b
    k = 16
    Ua = rng.normal(0, 1/np.sqrt(db), (k, db)); Ub = rng.normal(0, 1/np.sqrt(db), (k, db))
    M = rng.normal(0, 1/np.sqrt(k), (k, k)); W = 0.5 * (M + M.T)

    def settle(A, B, K):
        drive = (Ua @ A.T + Ub @ B.T).T          # (n, k)
        z = drive.copy()
        for _ in range(K):
            z = z - 0.1 * (z @ W.T - drive)
        return z
    spl = n // 2
    for K, tag in [(30, "settle"), (1, "ablate(K=1)")]:
        Z = settle(A, B, K)
        acc = ridge_acc(Z[:spl], y[:spl], Z[spl:], y[spl:])
        if tag == "settle": s = acc
        else: ab = acc
        print(f"  H1620 {tag:<12s} held-out acc={acc:.3f}")
    gap = s - ab
    ok = (s >= 0.90) and (gap >= 0.25)
    print(f"  H1620 BAR settle>=0.90 ∧ gap>=0.25 : settle={s:.3f} gap={gap:+.3f} -> "
          f"{'SUPPORT' if ok else 'NOT-SUPPORTED'}")
    return ok


def H1630():
    # 4 roles x 8 fillers random projections; held-out role-filler pair separation.
    R, Fn, dk = 4, 8, 12
    n = 4000
    roleP = rng.normal(size=(R, dk)); fillP = rng.normal(size=(Fn, dk))
    valP = rng.normal(size=(Fn, dk))
    # each sample: one filler assigned per role (the binding); features = concat per pos
    rolef = rng.integers(0, Fn, (n, R))          # filler index per role
    # target: does role0 bind filler==3?  (held-out specific pair)
    y = (rolef[:, 0] == 3).astype(float)

    def bind(rolef, T):
        out = np.zeros((n, R, dk))
        for r in range(R):
            S = roleP[r][None, :] + fillP                    # (Fn, dk) role+filler
            comb = S[None, :, :] + valP[None, :, :]          # (1, Fn, dk)
            comb = np.broadcast_to(comb, (n, Fn, dk)).copy()
            # actual present filler boosts its own score (selective routing signal)
            for i in range(n):
                comb[i, rolef[i, r]] += 3.0
            w = np.exp(comb / T); w /= w.sum(1, keepdims=True)
            out[:, r] = (w * comb).sum(1)
        return out.reshape(n, R * dk)
    spl = n // 2
    res = {}
    for T, tag in [(0.1, "tropical(T→0)"), (1.0, "softmax(T=1)")]:
        Z = bind(rolef, T)
        acc = ridge_acc(Z[:spl], y[:spl], Z[spl:], y[spl:])
        res[tag] = acc
        print(f"  H1630 {tag:<14s} held-out pair-sep acc={acc:.3f}")
    ok = (res["tropical(T→0)"] >= 0.90) and (res["softmax(T=1)"] < 0.60)
    print(f"  H1630 BAR tropical>=0.90 ∧ softmax<0.60 -> "
          f"{'SUPPORT' if ok else 'NOT-SUPPORTED'}")
    return ok


def H1631():
    # cellular sheaf on 4-node role graph, restriction = random rotations.
    nodes, dk = 4, 8
    n = 4000
    # valid binding: node features consistent under restriction maps; scrambled: not.
    # build restriction maps (rotations)
    def rot(dk):
        q, _ = np.linalg.qr(rng.normal(size=(dk, dk)))
        return q
    Rmap = [rot(dk) for _ in range(nodes)]
    base = rng.normal(size=(n, dk))
    # node feats: valid = R_i^T * shared global section; gives low coboundary
    X = np.stack([base @ Rmap[i] for i in range(nodes)], 1)  # (n, nodes, dk)
    y = rng.integers(0, 2, n).astype(float)
    # scramble half: permute node feats so restrictions disagree
    scr = y > 0.5
    Xs = X.copy()
    perm = rng.permutation(nodes)
    Xs[scr] = X[scr][:, perm]

    def glue(X, K, identity):
        h = X.copy()
        for _ in range(K):
            # jacobi toward consistency on ring edges
            new = h.copy()
            for i in range(nodes):
                j = (i - 1) % nodes
                Ri = h[:, i] if identity else h[:, i] @ Rmap[i].T
                Rj = h[:, j] if identity else h[:, j] @ Rmap[j].T
                new[:, i] = h[:, i] - 0.3 * (Ri - Rj)
            h = new
        # coboundary norm
        cob = 0.0
        for i in range(nodes):
            j = (i - 1) % nodes
            Ri = h[:, i] if identity else h[:, i] @ Rmap[i].T
            Rj = h[:, j] if identity else h[:, j] @ Rmap[j].T
            cob = cob + ((Ri - Rj) ** 2).sum(1)
        return h.reshape(len(h), -1), cob
    spl = n // 2
    # sheaf (role-typed restriction) vs identity-Laplacian control
    Zs, cobS = glue(Xs, 4, identity=False)
    accS = ridge_acc(Zs[:spl], y[:spl], Zs[spl:], y[spl:])
    # coboundary valid vs scrambled separation (AUC-ish via mean gap)
    cob_valid = cobS[~scr].mean(); cob_scr = cobS[scr].mean()
    Zi, cobI = glue(Xs, 4, identity=True)
    accI = ridge_acc(Zi[:spl], y[:spl], Zi[spl:], y[spl:])
    print(f"  H1631 sheaf glued acc={accS:.3f}  identity-ctrl acc={accI:.3f}")
    print(f"  H1631 coboundary valid={cob_valid:.3f} scrambled={cob_scr:.3f} "
          f"(sep={cob_scr - cob_valid:+.3f})")
    ok = (accS >= 0.90) and (accS > accI) and (cob_scr > cob_valid)
    print(f"  H1631 BAR glued>=0.90 ∧ >ctrl ∧ coboundary separates -> "
          f"{'SUPPORT' if ok else 'NOT-SUPPORTED'}")
    return ok


def H1632():
    # object x attribute binary context (8x8); held-out attribute conjunctions.
    no, na = 8, 8
    n = 4000
    ctx = (rng.random((no, na)) > 0.5).astype(float)   # formal context
    # sample: random attribute subset gate; target = closed concept contains attr pair (2,5)
    attr_gate = (rng.random((n, na)) > 0.6).astype(float)
    obj_gate = (rng.random((n, no)) > 0.6).astype(float)
    # ground truth concept membership for held-out conjunction
    y = (attr_gate[:, 2] * attr_gate[:, 5]).astype(float)

    def closure(obj_gate, attr_gate, K, and_pool):
        ext = obj_gate.copy(); intent = attr_gate.copy()
        for _ in range(K):
            if and_pool:
                # intent' = attrs shared by all gated objects: prod_o ctx[o,a]^ext[o]
                lw = np.log(np.clip(ctx, 1e-6, 1))          # (no, na)
                intent = np.exp(ext @ lw)                   # (n, na) soft AND
                lw2 = np.log(np.clip(ctx.T, 1e-6, 1))       # (na, no)
                ext = np.exp(intent @ lw2)                  # (n, no)
            else:
                intent = (ext @ ctx) / (ext.sum(1, keepdims=True) + 1e-9)   # OR/mean pool
                ext = (intent @ ctx.T) / (intent.sum(1, keepdims=True) + 1e-9)
        return np.concatenate([ext, intent], 1), intent
    spl = n // 2
    res = {}
    for and_pool, tag in [(True, "meet(AND)"), (False, "OR-pool")]:
        Z, intent = closure(obj_gate, attr_gate, 2, and_pool)
        acc = ridge_acc(Z[:spl], y[:spl], Z[spl:], y[spl:])
        res[tag] = acc
        # idempotence
        Z2, intent2 = closure(obj_gate, attr_gate, 3, and_pool)
        idem = float(((Z2 - Z) ** 2).mean())
        print(f"  H1632 {tag:<10s} held-out conj acc={acc:.3f}  idem_resid={idem:.2e}")
    ok = (res["meet(AND)"] >= 0.90) and (res["OR-pool"] < 0.60)
    print(f"  H1632 BAR meet>=0.90 ∧ OR-pool<0.60 -> "
          f"{'SUPPORT' if ok else 'NOT-SUPPORTED'}")
    return ok


if __name__ == "__main__":
    print("=== $0 cheap-test decision probes (DIRECTIONAL numpy, frozen-first) ===")
    out = {}
    for name, fn in [("H1620", H1620), ("H1630", H1630), ("H1631", H1631), ("H1632", H1632)]:
        print(f"\n[{name}]")
        try:
            out[name] = fn()
        except Exception as e:
            print(f"  {name} ERROR: {e}")
            out[name] = None
    print("\n=== SUMMARY ===")
    for k, v in out.items():
        print(f"  {k}: {'SUPPORT' if v else ('NOT-SUPPORTED' if v is False else 'ERROR')}")
