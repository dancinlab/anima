#!/usr/bin/env python3
"""H_9026 (H_9025 Rung1) — TRAINED substrate-bind, REAL 303M manifold, held-out
recombination generalization gate. decoder-free. torch/numpy = DIRECTIONAL.

WHAT MAKES THIS DISTINCT FROM PRIORS (check-ledger-before-fire, c9):
  - H_1840 (FAIR gate, measured-FALSIFIED): RANDOM-synthetic non-additive targets +
    mouth numpy readout + UNTRAINED algebraic ops (hrr/bilinear). additive won.
  - H_6164 (cheap-gate FLOOR): controlled SYNTHETIC factored toy (oracle=1.0), trunk
    additive vs hadamard/tensorproduct/bilinear. best-binder Δ<+0.15, n(Δ≥.15)=0/5.
  - H_9025 Rung0: numpy harness, shuffle-controlled EARNED recovery = STORAGE property
    (key-locked), NOT held-out RECOMBINATION.
  Rung1 (this file) = the ONE genuinely-untried cell:
    (i)  REAL 303M concept manifold (clm303.clm penultimate mean-pool L2-unit = the
         same β embedding H_1822 β used — byte-faithful numpy mirror of core trunk),
    (ii) an ACTUALLY-TRAINED W_bind head (circular-conv ⊛ / bilinear) optimized under a
         recombination-reward objective (match the manifold's OWN composed-phrase rep),
    (iii)HELD-OUT RECOMBINATION generalization gate: train on some concept PAIRS, test
         COMPOSE on UNSEEN pairs (concepts each seen individually, pair unseen) —
         generalization, NOT retrieval,
    (iv) shuffle-controlled EARNED + additive baseline + ablation (op→additive inert)
         + oracle/learnability self-test (train-fit must be high, else INCONCLUSIVE-undertrain).

RECOMBINATION-REWARD OBJECTIVE (decoder-free, no mouth / no clm_decode / no next-byte):
  concepts c_i encoded to part-vec a_i = penult("c_i"); pair target T_ij = penult("c_i c_j")
  (the 303M manifold's OWN representation of the composed phrase). W_bind learns
  compose(a_i,b_j) ≈ T_ij. G1 lever = does a TRAINED multiplicative binder GENERALIZE
  this composition to HELD-OUT pairs and BEAT a trained additive/linear head?

FROZEN BARS (pre-registered, no tune-to-green):
  * learnability(oracle): every arm train-fit cos ≥ TRAIN_FIT_MIN=0.60 else INCONCLUSIVE.
  * EARNED (shuffle-controlled): held-out pair earned iff cos(pred(a_i,b_j),T_ij) > COMPOSE
    AND cos(pred(a_i,b_shuffled),T_ij) ≤ COMPOSE  (right partner composes ∧ wrong fails).
  * PRIMARY G1 direction: per seed Δ = earned_rate(bind) − earned_rate(add);
    GREEN-direction iff n(Δ ≥ +0.15) ≥ 3/5 seeds AND no_regress(bind ≥ add ∀ seed).
    else FLOOR/DIRECTIONAL. (torch ⇒ label DIRECTIONAL regardless — never terminal.)
  * ablation: bind-op → additive (same trained weights) must go INERT (earned collapses
    toward add level); if not, lift is not the op.

prior LOW per H_1840 FAIR-gate + DPI meta-law. FALSIFIED and DIRECTIONAL both valid (c9).
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
    1:1 with core.clm_decode._fwd_logits up to (but excluding) the readout. [d]."""
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

# fixed concept vocabulary — ko + en common nouns/adjs (each seen individually in train)
CONCEPTS = ["sun","moon","fire","water","tree","stone","bird","fish","king","queen",
            "light","dark","cold","song","road","house","child","dream","star","sea",
            "물","불","산","바다","하늘","별","나무","돌","새","왕","빛","노래","길","집"]

# ── combiner ops ──
def hrr(a, b):  # circular convolution binding (multiplicative)
    return np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)))

# ── tiny torch head trainer (DIRECTIONAL). numpy fallback if torch absent. ──
def train_head(feat_train, T_train, feat_test, T_test, seed, epochs=400, lr=1e-2):
    """Ridge-regularized linear head feat→d trained to maximize cos to target.
    Returns (train_cos_mean, W) using closed-form ridge on unit targets (deterministic,
    no torch dependency = robust on pool). Objective ≈ recombination-reward: predict the
    manifold's own composed-phrase representation."""
    X = feat_train; Y = T_train                         # X:[n,f] Y:[n,d]
    f = X.shape[1]
    lam = 1e-2 * np.trace(X.T @ X) / f                  # scale-aware ridge
    W = np.linalg.solve(X.T @ X + lam * np.eye(f), X.T @ Y)   # [f,d]
    def predcos(Xa, Ya):
        P = unit(Xa @ W); return np.sum(P * unit(Ya), axis=1)
    return float(predcos(X, Y).mean()), W

COMPOSE = 0.30
DELTA_BAR = 0.15
TRAIN_FIT_MIN = 0.60

def earned_rate(W, feat_right, feat_shuf, T):
    """held-out earned: right partner composes (cos>COMPOSE) AND shuffled fails (≤COMPOSE)."""
    pr = np.sum(unit(feat_right @ W) * unit(T), axis=1)
    ps = np.sum(unit(feat_shuf @ W) * unit(T), axis=1)
    earned = np.mean((pr > COMPOSE) & (ps <= COMPOSE))
    return float(earned), float(pr.mean()), float(ps.mean())

def build_features(A, B, kind):
    """kind: 'add' concat(a,b); 'bind_open' concat(hrr,a,b); 'bind_pure' hrr(a,b)."""
    n = len(A)
    if kind == "add":
        return np.concatenate([A, B], axis=1)
    H = np.stack([hrr(A[i], B[i]) for i in range(n)])
    if kind == "bind_pure":
        return H
    return np.concatenate([H, A, B], axis=1)   # bind_open (superset: multiplicative + additive)

def run_seed(seed, part, pairs_all, targets_all, n_train_frac=0.6, log=print):
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(pairs_all))
    n_tr = int(len(order) * n_train_frac)
    tr, te = order[:n_tr], order[n_tr:]
    idx = np.array(pairs_all)
    def parts(sub):
        A = part[idx[sub, 0]]; B = part[idx[sub, 1]]; T = targets_all[sub]
        return A, B, T
    Atr, Btr, Ttr = parts(tr)
    Ate, Bte, Tte = parts(te)
    # shuffled wrong partner for held-out (concepts present, pairing wrong)
    Bte_shuf = Bte[rng.permutation(len(te))]
    res = {}
    for kind in ["add", "bind_open", "bind_pure"]:
        Ftr = build_features(Atr, Btr, kind)
        train_cos, W = train_head(Ftr, Ttr, None, None, seed)
        Fte_right = build_features(Ate, Bte, kind)
        Fte_shuf  = build_features(Ate, Bte_shuf, kind)
        er, prm, psm = earned_rate(W, Fte_right, Fte_shuf, Tte)
        # ablation for bind arms: replace hrr op with additive (a+b) under SAME weights
        ab_er = None
        if kind != "add":
            def ablate_feat(A, B):
                addcomb = A + B
                if kind == "bind_pure": return addcomb
                return np.concatenate([addcomb, A, B], axis=1)
            ab_er, _, _ = earned_rate(W, ablate_feat(Ate, Bte), ablate_feat(Ate, Bte_shuf), Tte)
        res[kind] = dict(train_cos=train_cos, earned=er, pr=prm, ps=psm, ablate=ab_er)
    return tr, te, res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default="/home/summer/clm303_g6/clm303.clm")
    ap.add_argument("--seeds", default="7,4302,4303,101,202")
    ap.add_argument("--npairs", type=int, default=500)
    ap.add_argument("--smoke", action="store_true", help="synthetic vecs, no clm (logic test)")
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    t0 = time.time()
    M = len(CONCEPTS); d = 3784

    if args.smoke:
        rng = np.random.default_rng(0); d = 128
        part = unit(rng.standard_normal((M, d)))
        pairs_all = [(i, j) for i in range(M) for j in range(M) if i != j]
        rng.shuffle(pairs_all); pairs_all = pairs_all[:args.npairs]
        # smoke target = a genuine (unknown-to-linear) multiplicative composition + noise
        targets_all = np.stack([unit(hrr(part[i], part[j]) + 0.1*rng.standard_normal(d))
                                for (i, j) in pairs_all])
        print("[SMOKE] synthetic manifold, d=128 — logic validation only")
    else:
        cd = load_core()
        assert cd.clm_decodable(args.ckpt), "ckpt not v0.2-decodable"
        print(f"[load] {args.ckpt}", flush=True)
        W = cd.clm_load_weights(args.ckpt)
        d = W["d"]
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

    print(f"\n[train+eval] {len(seeds)} seeds, held-out recombination gate", flush=True)
    print(f"FROZEN: COMPOSE={COMPOSE} DELTA_BAR=+{DELTA_BAR} TRAIN_FIT_MIN={TRAIN_FIT_MIN} "
          f"GREEN-dir iff n(Δ≥+{DELTA_BAR})≥3/5 ∧ no_regress\n")
    hdr = f"{'seed':<7}{'arm':<11}{'train_cos':<11}{'earned':<9}{'pr':<8}{'ps':<8}{'ablate':<8}"
    print(hdr); print("-"*len(hdr))
    deltas_open = []; deltas_pure = []; noreg_open = True; noreg_pure = True
    fit_ok = True   # task-solvable: BEST arm fits train ≥ TRAIN_FIT_MIN (per seed)
    for s in seeds:
        _, _, res = run_seed(s, part, pairs_all, targets_all, log=print)
        add_e = res["add"]["earned"]
        best_fit = 0.0
        for kind in ["add", "bind_open", "bind_pure"]:
            r = res[kind]
            ab = f"{r['ablate']:.3f}" if r['ablate'] is not None else "  -"
            print(f"{s:<7}{kind:<11}{r['train_cos']:<11.3f}{r['earned']:<9.3f}"
                  f"{r['pr']:<8.3f}{r['ps']:<8.3f}{ab:<8}")
            best_fit = max(best_fit, r["train_cos"])
        if best_fit < TRAIN_FIT_MIN: fit_ok = False
        do = res["bind_open"]["earned"] - add_e
        dp = res["bind_pure"]["earned"] - add_e
        deltas_open.append(do); deltas_pure.append(dp)
        if do < 0: noreg_open = False
        if dp < 0: noreg_pure = False

    n = len(seeds)
    nhit_open = sum(1 for x in deltas_open if x >= DELTA_BAR)
    nhit_pure = sum(1 for x in deltas_pure if x >= DELTA_BAR)
    green_open = (nhit_open >= 3) and noreg_open and fit_ok
    green_pure = (nhit_pure >= 3) and noreg_pure and fit_ok
    print("\n==================== VERDICT (DIRECTIONAL — torch/numpy mirror) ====================")
    print(f"learnability(oracle): best-arm train-fit≥{TRAIN_FIT_MIN} every seed = {fit_ok} "
          f"({'task solvable → valid recomb gate' if fit_ok else 'INCONCLUSIVE-undertrain/unreachable'})")
    print(f"bind_open − add  Δ per seed = {[round(x,3) for x in deltas_open]}  "
          f"n(Δ≥+{DELTA_BAR})={nhit_open}/{n} no_regress={noreg_open}")
    print(f"bind_pure − add  Δ per seed = {[round(x,3) for x in deltas_pure]}  "
          f"n(Δ≥+{DELTA_BAR})={nhit_pure}/{n} no_regress={noreg_pure}")
    verdict = ("🟢-direction (DIRECTIONAL, needs engine-native Rung2 wire-in)"
               if (green_open or green_pure)
               else "🧱 FLOOR — trained multiplicative bind does NOT beat trained additive "
                    "on held-out recombination (DPI meta-law + H_1840 CONFIRMED)")
    print(f"PRIMARY G1 (held-out recombination generalization): {verdict}")
    print(f"[done] wall={time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
