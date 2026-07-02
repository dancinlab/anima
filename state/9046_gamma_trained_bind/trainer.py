#!/usr/bin/env python3
"""H_9044 — γ TRAINED-COMBINER on REAL 303M manifold, held-out compositional
generalization gate. decoder-free. torch/numpy = DIRECTIONAL (label honestly).

THE GENUINELY-UNTRIED CELL (check-ledger-before-fire, c9):
  - H_1840 (γ FAIR cheap-gate): trained bilinear-bottleneck, but on a RANDOM
    full-rank operator-agnostic target -> held-out info-theoretically independent
    from seen = UNLEARNABLE (later flagged MEASUREMENT-INVALID by H_6166). Not the
    real-manifold cell.
  - H_9026 (Rung1, real manifold): REAL 303M β + held-out recomb, BUT the "trained
    W_bind" trained only a LINEAR RIDGE READOUT on a *FIXED* algebraic feature
    (hrr = circular-conv, untrained). The COMBINER interaction was never learned.
    Result: bind-Δ vs add = [.12,.12,.08,.07,.09], all sub-threshold -> FLOOR.
  - H_9043 (engine-native): built vadapt_combine/unbind = FIXED algebraic HRR op.
    recoverability GREEN, held-out CAPABILITY cos -0.203 < chance -> FLOOR. Its
    stated ONLY remaining lever = "trained constructive-bind (γ)".

  THIS FILE = that lever: a LEARNED / PARAMETERIZED combiner whose *interaction
  weights are trained end-to-end* under a recombination-reward objective, on the
  REAL 303M β manifold, with a STRUCTURED held-out pair split (concepts each seen
  individually, the PAIR unseen -> systematic generalization is possible in
  principle, unlike H_1840's random target; oracle train-fit proves solvability).
    arms:
      add       : ridge linear readout on concat[a,b]         (H_9026 baseline)
      bilinear  : LEARNED low-rank bilinear  c=Wout@((Ua)⊙(Vb)) (γ, trained interaction)
      mlp       : LEARNED 2-layer MLP over [a,b]               (γ, most-expressive combiner)

RECOMB-REWARD OBJECTIVE (decoder-free; no mouth / clm_decode / next-byte):
  part-vec a_i = penult("c_i");  pair target T_ij = penult("c_i c_j")
  (the 303M manifold's OWN rep of the composed phrase). Combiner learns
  compose(a_i,b_j) ≈ T_ij on TRAIN pairs; G1 lever = does the TRAINED combiner
  GENERALIZE to HELD-OUT pairs and BEAT the additive baseline?

FROZEN BARS (pre-registered, no tune-to-green):
  COMPOSE=0.30  DELTA_BAR=0.15  TRAIN_FIT_MIN=0.60
  * learnability(oracle): best-arm TRAIN-fit cos ≥ TRAIN_FIT_MIN else INCONCLUSIVE-undertrain.
  * held-out EARNED (shuffle-controlled): pair earned iff
      cos(pred(a_i,b_j),T_ij) > COMPOSE  AND  cos(pred(a_i,b_shuf),T_ij) ≤ COMPOSE.
  * PRIMARY G1: per-seed Δ = earned(combiner) − earned(add);
      GREEN-direction iff n(Δ≥+DELTA_BAR) ≥ 3/5 AND no_regress(combiner≥add ∀seed).
      else FLOOR. torch/numpy ⇒ DIRECTIONAL regardless (never terminal).
  * ablation: multiplicative interaction (⊙ for bilinear / [a,b] for mlp) replaced
      by ADDITIVE (a+b) under the SAME trained weights must go INERT.
  * additivity diagnostic: mean cos(T_ij, unit(a_i+b_j)) — how additive is the
      manifold's TRUE composition (explains a high add baseline / floor if ≫ chance).

prior LOW (DPI meta-law + H_9026 fixed-op floor). GREEN (capability opens) or
FLOOR (DPI confirmed on the trained real-manifold combiner) are BOTH valid (c9).
cost: pool $0.
"""
import os, sys, time, argparse
import numpy as np

# ── real-manifold extractor: byte-faithful numpy mirror of core trunk (DIRECTIONAL) ──
def load_core():
    sys.path.insert(0, os.path.expanduser("~/anima"))
    sys.path.insert(0, ".")
    from core import clm_decode as cd
    return cd

def unit(v, axis=-1):
    n = np.linalg.norm(v, axis=axis, keepdims=True)
    return v / np.where(n == 0, 1.0, n)

def penult_vec(cd, W, text_bytes):
    """clm303 trunk penultimate (final-groupnorm output yn) mean-pooled + L2-unit.
    1:1 with core.clm_decode._fwd_logits up to (excluding) the readout. [d].
    Identical extractor to H_9026 rung1_trainer (same β embedding, H_1822)."""
    tok = np.frombuffer(text_bytes, dtype=np.uint8).astype(np.float64)
    T = len(tok); d = W["d"]; E = W["E"]; K = W["K"]; L = W["L"]
    ids = tok.astype(np.int64)
    xe = W["embed"][ids]
    xt = cd._conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    DIL_CAP = 512; dil = 1
    for li in range(L):
        dil_eff = dil if dil <= DIL_CAP else DIL_CAP
        h = cd._conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, dil_eff)
        hn = cd.nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1)
        hg = cd.nn_gelu_fwd(hn)
        xt = xt + hg.reshape(T, d)
        dil *= 2
    logits_r = cd._conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1)
    ex_out = np.empty((E, T, d), dtype=np.float64)
    for ej in range(E):
        eo = cd._conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1)
        ex_out[ej] = cd.nn_gelu_fwd(eo).reshape(T, d)
    y = cd.nn_moe_router_fwd(logits_r, ex_out, T, E, d)
    yn = cd.nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)   # [T,d] penultimate
    return unit(yn.mean(axis=0))                               # [d]

# concept vocabulary — ko + en common nouns/adjs/verbs. Expanded to ~96 so the
# pair-grid (N(N-1)) better covers the combiner's operator DOF in the PCA-reduced
# subspace (identifiability — see the powered oracle smoke). Each seen individually.
CONCEPTS = ["sun","moon","fire","water","tree","stone","bird","fish","king","queen",
            "light","dark","cold","warm","song","road","house","child","dream","star",
            "sea","wind","rain","snow","cloud","river","mountain","flower","leaf","root",
            "hand","eye","heart","mind","voice","word","time","day","night","year",
            "gold","iron","glass","paper","cloth","bread","wine","milk","salt","honey",
            "dog","cat","horse","wolf","bear","lion","eagle","snake","bee","ant",
            "red","blue","green","black","white","fast","slow","big","small","old",
            "물","불","산","바다","하늘","별","나무","돌","새","왕",
            "빛","노래","길","집","바람","비","눈","구름","강","꽃",
            "손","눈동자","마음","소리","시간","밤"]

COMPOSE = 0.30
DELTA_BAR = 0.15
TRAIN_FIT_MIN = 0.60

# ─────────────────────────── combiners ───────────────────────────
# ridge closed-form additive baseline (identical to H_9026 'add' arm)
def ridge_fit(X, Y):
    f = X.shape[1]
    lam = 1e-2 * np.trace(X.T @ X) / f
    W = np.linalg.solve(X.T @ X + lam * np.eye(f), X.T @ Y)   # [f,d]
    return W
def ridge_pred(X, W):
    return unit(X @ W)

def cos_rows(P, Y):
    return np.sum(unit(P) * unit(Y), axis=1)

# torch learned combiners (DIRECTIONAL). trained interaction weights.
def train_torch_combiner(kind, A, B, T, seed, d, epochs=400, R=48, hidden=192, wd=1e-3, lr=3e-3):
    import torch
    torch.manual_seed(seed)
    dev = "cpu"
    At = torch.tensor(A, dtype=torch.float32, device=dev)
    Bt = torch.tensor(B, dtype=torch.float32, device=dev)
    Tt = torch.nn.functional.normalize(torch.tensor(T, dtype=torch.float32, device=dev), dim=1)
    n = At.shape[0]
    if kind == "bilinear":
        U = torch.nn.Parameter(torch.randn(R, d, device=dev) * (1.0/d**0.5))
        V = torch.nn.Parameter(torch.randn(R, d, device=dev) * (1.0/d**0.5))
        Wo = torch.nn.Parameter(torch.randn(d, R, device=dev) * (1.0/R**0.5))
        params = [U, V, Wo]
        def fwd(a, b, ablate=False):
            ua = a @ U.t(); vb = b @ V.t()            # [n,R]
            inter = (ua + vb) if ablate else (ua * vb)  # ablate: additive interaction
            return inter @ Wo.t()                       # [n,d]
    elif kind == "mlp":
        W1 = torch.nn.Parameter(torch.randn(2*d, hidden, device=dev) * (1.0/(2*d)**0.5))
        b1 = torch.nn.Parameter(torch.zeros(hidden, device=dev))
        W2 = torch.nn.Parameter(torch.randn(hidden, d, device=dev) * (1.0/hidden**0.5))
        b2 = torch.nn.Parameter(torch.zeros(d, device=dev))
        params = [W1, b1, W2, b2]
        def fwd(a, b, ablate=False):
            x = (a + b).repeat(1, 2) if ablate else torch.cat([a, b], dim=1)  # ablate: role-blind concat(a+b,a+b)
            h = torch.relu(x @ W1 + b1)
            return h @ W2 + b2
    else:
        raise ValueError(kind)
    opt = torch.optim.Adam(params, lr=lr, weight_decay=wd)
    for ep in range(epochs):
        opt.zero_grad()
        P = torch.nn.functional.normalize(fwd(At, Bt), dim=1)
        loss = (1.0 - (P * Tt).sum(1)).mean()   # cosine loss
        loss.backward(); opt.step()
    with torch.no_grad():
        def predcos(a, b, Ttgt, ablate=False):
            P = torch.nn.functional.normalize(fwd(a, b), dim=1)
            return (P * torch.nn.functional.normalize(Ttgt, dim=1)).sum(1).cpu().numpy()
        train_cos = float(predcos(At, Bt, Tt).mean())
    return fwd, predcos_wrap(fwd), train_cos

def predcos_wrap(fwd):
    import torch
    def pc(A, B, T, ablate=False):
        with torch.no_grad():
            a = torch.tensor(A, dtype=torch.float32)
            b = torch.tensor(B, dtype=torch.float32)
            P = torch.nn.functional.normalize(fwd(a, b, ablate=ablate), dim=1)
            Tt = torch.nn.functional.normalize(torch.tensor(T, dtype=torch.float32), dim=1)
            return (P * Tt).sum(1).cpu().numpy()
    return pc

def earned_from_cos(pr, ps):
    """held-out earned: right partner composes (>COMPOSE) AND shuffled fails (≤COMPOSE)."""
    return float(np.mean((pr > COMPOSE) & (ps <= COMPOSE))), float(pr.mean()), float(ps.mean())

# ─────────────────────────── per-seed run ───────────────────────────
def run_seed(seed, part, pairs_all, targets_all, d, n_train_frac=0.6):
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(pairs_all))
    n_tr = int(len(order) * n_train_frac)
    tr, te = order[:n_tr], order[n_tr:]
    idx = np.array(pairs_all)
    def parts(sub):
        return part[idx[sub, 0]], part[idx[sub, 1]], targets_all[sub]
    Atr, Btr, Ttr = parts(tr)
    Ate, Bte, Tte = parts(te)
    Bte_shuf = Bte[rng.permutation(len(te))]     # wrong partner: concepts present, pairing wrong
    res = {}

    # arm: add (ridge on concat[a,b]) — H_9026 baseline
    Xtr = np.concatenate([Atr, Btr], axis=1)
    Wr = ridge_fit(Xtr, Ttr)
    add_train = float(cos_rows(Xtr @ Wr, Ttr).mean())
    pr = cos_rows(np.concatenate([Ate, Bte], 1) @ Wr, Tte)
    ps = cos_rows(np.concatenate([Ate, Bte_shuf], 1) @ Wr, Tte)
    er, prm, psm = earned_from_cos(pr, ps)
    res["add"] = dict(train_cos=add_train, earned=er, pr=prm, ps=psm, ablate=None)

    # arms: learned combiners (bilinear, mlp)
    for kind in ["bilinear", "mlp"]:
        fwd, pc, train_cos = train_torch_combiner(kind, Atr, Btr, Ttr, seed, d)
        pr = pc(Ate, Bte, Tte); ps = pc(Ate, Bte_shuf, Tte)
        er, prm, psm = earned_from_cos(pr, ps)
        # ablation: multiplicative interaction -> additive, SAME trained weights
        pra = pc(Ate, Bte, Tte, ablate=True); psa = pc(Ate, Bte_shuf, Tte, ablate=True)
        ab_er, _, _ = earned_from_cos(pra, psa)
        res[kind] = dict(train_cos=train_cos, earned=er, pr=prm, ps=psm, ablate=ab_er)
    return tr, te, res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default="/home/aiden/py303_full.clm")
    ap.add_argument("--seeds", default="7,4302,4303,101,202")
    ap.add_argument("--npairs", type=int, default=400)
    ap.add_argument("--cache", default="state/9044_gamma_trained_bind/beta_cache.npz")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--smoke-rank", type=int, default=0,
                    help="0=hrr full-rank target; >0=random low-rank bilinear oracle (power check)")
    ap.add_argument("--smoke-nconcepts", type=int, default=0, help="override concept count in smoke")
    ap.add_argument("--smoke-dim", type=int, default=128, help="smoke manifold dim")
    ap.add_argument("--pca-dim", type=int, default=0,
                    help=">0: PCA-reduce concept+target vecs to this dim (identifiable regime). "
                         "fit on all part+target vecs, project both, then re-unit.")
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    t0 = time.time()
    M = len(CONCEPTS)

    if args.smoke:
        rng = np.random.default_rng(0); d = args.smoke_dim
        if args.smoke_nconcepts > 0: M = args.smoke_nconcepts
        part = unit(rng.standard_normal((M, d)))
        pairs_all = [(i, j) for i in range(M) for j in range(M) if i != j]
        rng.shuffle(pairs_all); pairs_all = pairs_all[:args.npairs]
        if args.smoke_rank > 0:
            # random low-rank bilinear ORACLE: T = Wout @ ((Ua)⊙(Vb)); rank R_true.
            # This is representable by the bilinear arm -> POWER check: combiner MUST
            # generalize held-out (earned>0, Δ>add) or the harness is underpowered.
            Rt = args.smoke_rank
            Uo = rng.standard_normal((Rt, d))/d**0.5; Vo = rng.standard_normal((Rt, d))/d**0.5
            Wo = rng.standard_normal((d, Rt))/Rt**0.5
            def tgt(a, b): return Wo @ ((Uo @ a) * (Vo @ b))
            targets_all = np.stack([unit(tgt(part[i], part[j]) + 0.05*rng.standard_normal(d))
                                    for (i, j) in pairs_all])
            print(f"[SMOKE] low-rank bilinear ORACLE (rank={Rt}) d=128 — POWER check", flush=True)
        else:
            def hrr(a, b): return np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)))
            targets_all = np.stack([unit(hrr(part[i], part[j]) + 0.1*rng.standard_normal(d))
                                    for (i, j) in pairs_all])
            print("[SMOKE] hrr full-rank target d=128 — logic validation only", flush=True)
    elif os.path.exists(args.cache):
        z = np.load(args.cache, allow_pickle=True)
        part = z["part"]; pairs_all = [tuple(p) for p in z["pairs"]]; targets_all = z["targets"]
        d = part.shape[1]
        print(f"[cache] loaded {args.cache} d={d} pairs={len(pairs_all)}", flush=True)
    else:
        cd = load_core()
        assert cd.clm_decodable(args.ckpt), "ckpt not v0.2-decodable"
        print(f"[load] {args.ckpt}", flush=True)
        W = cd.clm_load_weights(args.ckpt); d = W["d"]
        print(f"[cfg] d={d} L={W['L']} E={W['E']} V={W['V']}", flush=True)
        print(f"[extract] {M} concept part-vecs ...", flush=True)
        part = np.stack([penult_vec(cd, W, c.encode("utf-8")) for c in CONCEPTS])
        rng = np.random.default_rng(0)
        pairs_all = [(i, j) for i in range(M) for j in range(M) if i != j]
        rng.shuffle(pairs_all); pairs_all = pairs_all[:args.npairs]
        print(f"[extract] {len(pairs_all)} composed-phrase targets (REAL manifold) ...", flush=True)
        targets_all = np.empty((len(pairs_all), d))
        for k, (i, j) in enumerate(pairs_all):
            phrase = (CONCEPTS[i] + " " + CONCEPTS[j]).encode("utf-8")
            targets_all[k] = penult_vec(cd, W, phrase)
            if (k+1) % 50 == 0:
                print(f"   target {k+1}/{len(pairs_all)}  t={time.time()-t0:.0f}s", flush=True)
        os.makedirs(os.path.dirname(args.cache), exist_ok=True)
        np.savez(args.cache, part=part, pairs=np.array(pairs_all), targets=targets_all)
        print(f"[cache] saved {args.cache}", flush=True)

    # optional PCA reduction into the identifiable low-dim regime (the powered-oracle
    # regime). Fit on all part+target vecs, project both, re-unit. Reported var-explained.
    if args.pca_dim > 0:
        allv = np.concatenate([part, targets_all], axis=0)
        mu = allv.mean(axis=0)
        Ac = allv - mu
        U, S, Vt = np.linalg.svd(Ac, full_matrices=False)
        k = min(args.pca_dim, Vt.shape[0])
        P = Vt[:k]                                   # [k,d]
        ve = float((S[:k]**2).sum() / (S**2).sum())
        part = unit((part - mu) @ P.T)
        targets_all = unit((targets_all - mu) @ P.T)
        d = k
        print(f"[pca] reduced to d={k}  var-explained={ve:.3f}  "
              f"(identifiable regime; combiner operator DOF ≪ #train-pairs)", flush=True)

    # additivity diagnostic: how additive is the manifold's TRUE composition?
    idx = np.array(pairs_all)
    add_true = cos_rows(unit(part[idx[:,0]] + part[idx[:,1]]), targets_all)
    print(f"\n[diag] additivity: mean cos(T_ij, unit(a_i+b_j)) = {add_true.mean():.3f} "
          f"(high ⇒ manifold composes ~additively ⇒ add baseline strong)", flush=True)

    print(f"\n[train+eval] {len(seeds)} seeds, held-out compositional-generalization gate", flush=True)
    print(f"FROZEN: COMPOSE={COMPOSE} DELTA_BAR=+{DELTA_BAR} TRAIN_FIT_MIN={TRAIN_FIT_MIN} "
          f"GREEN-dir iff n(Δ≥+{DELTA_BAR})≥3/5 ∧ no_regress\n", flush=True)
    hdr = f"{'seed':<7}{'arm':<11}{'train_cos':<11}{'earned':<9}{'pr':<8}{'ps':<8}{'ablate':<8}"
    print(hdr); print("-"*len(hdr))
    arms = ["add", "bilinear", "mlp"]
    deltas = {"bilinear": [], "mlp": []}
    noreg = {"bilinear": True, "mlp": True}
    fit_ok = True
    for s in seeds:
        _, _, res = run_seed(s, part, pairs_all, targets_all, d)
        add_e = res["add"]["earned"]
        best_learned_fit = 0.0
        for kind in arms:
            r = res[kind]
            ab = f"{r['ablate']:.3f}" if r['ablate'] is not None else "  -"
            print(f"{s:<7}{kind:<11}{r['train_cos']:<11.3f}{r['earned']:<9.3f}"
                  f"{r['pr']:<8.3f}{r['ps']:<8.3f}{ab:<8}", flush=True)
            if kind != "add":
                best_learned_fit = max(best_learned_fit, r["train_cos"])
        if best_learned_fit < TRAIN_FIT_MIN: fit_ok = False
        for kind in ["bilinear", "mlp"]:
            dlt = res[kind]["earned"] - add_e
            deltas[kind].append(dlt)
            if dlt < 0: noreg[kind] = False

    n = len(seeds)
    print("\n==================== VERDICT (DIRECTIONAL — torch/numpy mirror) ====================")
    print(f"learnability(oracle): best learned-combiner TRAIN-fit≥{TRAIN_FIT_MIN} every seed = {fit_ok} "
          f"({'task solvable → valid gate' if fit_ok else 'INCONCLUSIVE-undertrain'})")
    green = False
    for kind in ["bilinear", "mlp"]:
        ds = deltas[kind]; nhit = sum(1 for x in ds if x >= DELTA_BAR)
        g = (nhit >= 3) and noreg[kind] and fit_ok
        green = green or g
        print(f"{kind:<9} − add  Δ per seed = {[round(x,3) for x in ds]}  "
              f"n(Δ≥+{DELTA_BAR})={nhit}/{n} no_regress={noreg[kind]}  GREEN-dir={g}")
    verdict = ("🟢-direction (DIRECTIONAL; needs engine-native wire-in)" if green
               else "🧱 FLOOR — TRAINED constructive combiner (bilinear/MLP) does NOT beat "
                    "trained additive on held-out real-manifold recombination "
                    "(DPI meta-law + H_9026 confirmed; γ lever exhausted)")
    print(f"PRIMARY G1 (held-out compositional generalization): {verdict}")
    print(f"[done] wall={time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
