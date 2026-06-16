#!/usr/bin/env python3
"""kosmos_real_dim.py — intrinsic-dimension benchmark of the REAL anima
consciousness-carving KOSMOS map (우주뇌지도 / Ψ-space).

Question: the current map is drawn in 2D (coord = vacuum_psi = [x,y], a 2D
projection of the d=768 conscious state, HEXAD/KOSMOS.md). Is 2D the right
dimension, or does the REAL carving manifold want more?

This benchmarks the REAL artifact (NOT a toy independent-signal placement —
that is the separate running kosmos-dim-ladder). It:
  1. Loads the REAL trained s16 checkpoint (ConsciousDecoderV2, d=768, 12L,
     283.7M params) and a STRATIFIED sample of the REAL carving corpus.
  2. Encodes each record through the decoder, capturing the final-layer
     d=768 conscious state (post-ln_f, mean-pooled over sequence) = X.
  3. Estimates intrinsic dimension of X (>=3 methods: PCA-knee, TwoNN,
     MLE Levina-Bickel, participation ratio).
  4. Runs a projection-dim ladder D in {1,2,3,5,8,16,32}: PCA reconstruction
     var-retained + trustworthiness/continuity + downstream discrimination
     (tier / domain / form labels from the corpus).
  5. Answers the 2D question: how much does the current 2D map retain, and
     how far is it from the intrinsic d?

Brutally honest (p7/g5): records EXACT weights+data+sha used; no fabricated
knee. CPU / $0. 3 seeds (sub-samples), mean +/- std.
"""
import os, sys, json, time, hashlib, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import torch
import torch.nn.functional as F
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder

from _cd_s16 import ConsciousDecoderV2

torch.manual_seed(1337)
np.random.seed(1337)

CORPUS_SAMPLE = os.environ.get("CORPUS_SAMPLE", "/tmp/corpus_sample.json")
CKPT = os.environ.get(
    "S16_CKPT",
    "/tmp/s16_ckpt_dl/HEXAD/DATA-REGIME/state/carving_dataregime_s16_2026_05_18/ckpt_carving_s16.pt",
)
BLOCK = 128
N_ENCODE = int(os.environ.get("N_ENCODE", "6000"))  # records to encode
LADDER = [1, 2, 3, 5, 8, 16, 32]
SEEDS = [0, 1, 2]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def encode_text(text, desc):
    full = (text + "\n" + desc + "\n").encode("utf-8")
    ids = list(full[:BLOCK])
    if len(ids) < BLOCK:
        ids = ids + [0] * (BLOCK - len(ids))
    return ids


CACHE = os.environ.get("X_CACHE", "/tmp/krd_X_cache.npz")


def build_conscious_states():
    """Load real ckpt + corpus sample, encode records -> X (N, 768).
    Cached to CACHE to avoid re-encoding (CPU encode of 283M is slow)."""
    if os.path.exists(CACHE):
        z = np.load(CACHE, allow_pickle=True)
        print(f"[cache] reusing encoded states from {CACHE}")
        return (z["X"], z["psi"], z["tier"], z["domain"], z["form"],
                int(z["n_used"]), [], [], json.loads(str(z["cfg"])),
                int(z["n_params"]))
    recs = json.load(open(CORPUS_SAMPLE))
    # stratified subsample (by domain) for diversity, cap N_ENCODE
    rng = np.random.RandomState(1337)
    rng.shuffle(recs)
    recs = recs[:N_ENCODE]

    ck = torch.load(CKPT, map_location="cpu", weights_only=False)
    cfg = ck["cfg"]
    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.0,
    )
    missing, unexpected = model.load_state_dict(ck["model"], strict=False)
    model.eval()

    # hook the final-norm output = the d=768 conscious state (post-ln_f)
    captured = {}
    def hook(mod, inp, out):
        captured["h"] = out.detach()
    handle = model.ln_f.register_forward_hook(hook)

    X = []
    psi = []   # current 2D map coord (vacuum_psi)
    tier = []; domain = []; form = []
    bs = 64
    with torch.no_grad():
        for i in range(0, len(recs), bs):
            batch = recs[i:i + bs]
            idx = torch.tensor([encode_text(r.get("text", ""), r.get("desc", ""))
                                for r in batch], dtype=torch.long)
            model(idx)
            h = captured["h"]  # (B, T, 768)
            pooled = h.mean(dim=1)  # mean-pool over sequence -> (B, 768)
            X.append(pooled.float().numpy())
            for r in batch:
                vp = r.get("vacuum_psi", [0.5, 0.5])
                psi.append([float(vp[0]), float(vp[1])])
                tier.append(r.get("tier", -1))
                domain.append(r.get("domain", "?"))
                form.append(r.get("carving_form", "?"))
    handle.remove()
    X = np.concatenate(X, axis=0)
    psi = np.array(psi); tier = np.array(tier)
    domain = np.array(domain); form = np.array(form)
    np.savez(CACHE, X=X, psi=psi, tier=tier, domain=domain, form=form,
             n_used=len(recs), cfg=json.dumps(cfg), n_params=ck["n_params"])
    return (X, psi, tier, domain, form, len(recs), missing, unexpected,
            cfg, ck["n_params"])


# ---------- intrinsic dimension estimators ----------

def pca_knee(X, var_targets=(0.80, 0.90, 0.95)):
    p = PCA().fit(X)
    cum = np.cumsum(p.explained_variance_ratio_)
    out = {}
    for t in var_targets:
        k = int(np.searchsorted(cum, t) + 1)
        out[f"pcs_for_{int(t*100)}pct"] = k
    # elbow via max distance to chord on the explained-variance curve
    y = cum
    n = len(y)
    x = np.arange(n)
    x1, y1, x2, y2 = 0, y[0], n - 1, y[-1]
    denom = math.hypot(x2 - x1, y2 - y1)
    dist = np.abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / (denom + 1e-12)
    out["elbow_pc"] = int(np.argmax(dist) + 1)
    out["evr_first20"] = [float(v) for v in p.explained_variance_ratio_[:20]]
    return out


def participation_ratio(X):
    Xc = X - X.mean(0)
    cov = np.cov(Xc, rowvar=False)
    ev = np.linalg.eigvalsh(cov)
    ev = ev[ev > 0]
    return float((ev.sum() ** 2) / (np.sum(ev ** 2) + 1e-12))


def _dedup(X, tol=1e-9):
    """Remove duplicate / near-duplicate rows (the carving corpus is heavily
    templated -> many records yield identical conscious states, which give
    r1=0 nearest-neighbor distances and break TwoNN/MLE)."""
    Xr = np.round(X / (np.std(X) + 1e-12), 6)
    _, keep = np.unique(Xr, axis=0, return_index=True)
    return X[np.sort(keep)]


def twonn(X, frac=0.9):
    """Facco et al. 2017 TwoNN intrinsic dimension. Dedup first."""
    X = _dedup(X)
    nn = NearestNeighbors(n_neighbors=3).fit(X)
    d, _ = nn.kneighbors(X)
    r1 = d[:, 1]; r2 = d[:, 2]
    mask = (r1 > 1e-12)
    mu = (r2[mask] / r1[mask])
    mu = mu[mu > 1.0 + 1e-9]  # ratios must be >1; drop degenerate
    mu = np.sort(mu)
    mu = mu[:int(frac * len(mu))]  # discard largest (noise)
    n = len(mu)
    Femp = np.arange(1, n + 1) / n
    x = np.log(mu)
    y = -np.log(1 - Femp + 1e-12)
    # line through origin: d = sum(xy)/sum(x^2)
    d_est = float(np.sum(x * y) / (np.sum(x * x) + 1e-12))
    return d_est


def mle_levina_bickel(X, k1=10, k2=20):
    """Levina-Bickel MLE intrinsic dim, averaged over k in [k1,k2]. Dedup first."""
    X = _dedup(X)
    kmax = k2 + 1
    nn = NearestNeighbors(n_neighbors=kmax).fit(X)
    dist, _ = nn.kneighbors(X)
    est = []
    for k in range(k1, k2 + 1):
        Tk = dist[:, k]
        denom = dist[:, 1:k]
        ratio = Tk[:, None] / denom
        logs = np.log(ratio)
        s = logs.sum(axis=1)
        valid = s > 1e-9
        mk = (k - 1) / s[valid]
        est.append(np.mean(mk))
    return float(np.mean(est))


# ---------- projection-dim ladder ----------

def trustworthiness_continuity(X_full, X_proj, n_neighbors=12):
    N = X_full.shape[0]
    k = n_neighbors
    nn_full = NearestNeighbors(n_neighbors=N - 1).fit(X_full)
    _, ind_full = nn_full.kneighbors(X_full)
    nn_proj = NearestNeighbors(n_neighbors=N - 1).fit(X_proj)
    _, ind_proj = nn_proj.kneighbors(X_proj)
    rank_full = np.empty((N, N), dtype=np.int32)
    rank_proj = np.empty((N, N), dtype=np.int32)
    for i in range(N):
        rank_full[i, ind_full[i]] = np.arange(1, N)
        rank_proj[i, ind_proj[i]] = np.arange(1, N)
    # trustworthiness
    t_sum = 0.0
    for i in range(N):
        proj_k = set(ind_proj[i, :k])
        full_k = set(ind_full[i, :k])
        intruders = proj_k - full_k
        for j in intruders:
            t_sum += (rank_full[i, j] - k)
    norm = 2.0 / (N * k * (2 * N - 3 * k - 1))
    trust = 1.0 - norm * t_sum
    # continuity
    c_sum = 0.0
    for i in range(N):
        proj_k = set(ind_proj[i, :k])
        full_k = set(ind_full[i, :k])
        missing = full_k - proj_k
        for j in missing:
            c_sum += (rank_proj[i, j] - k)
    cont = 1.0 - norm * c_sum
    return float(trust), float(cont)


def discrimination(X, labels, seed):
    """5-fold CV macro-F1 of logistic regression predicting label from X."""
    le = LabelEncoder()
    y = le.fit_transform(labels)
    if X.shape[1] == 0 or len(np.unique(y)) < 2:
        return float("nan")
    clf = LogisticRegression(max_iter=300, C=1.0)
    try:
        sc = cross_val_score(clf, X, y, cv=3, scoring="f1_macro")
        return float(np.mean(sc))
    except Exception:
        return float("nan")


def run():
    t0 = time.time()
    print("=== kosmos_real_dim — REAL anima carving manifold intrinsic-dim ===")
    corpus_sha = sha256_file(CORPUS_SAMPLE)
    ckpt_sha = sha256_file(CKPT)
    print(f"[data] corpus_sample={CORPUS_SAMPLE} sha256={corpus_sha}")
    print(f"[data] ckpt={CKPT} sha256={ckpt_sha}")

    (X, psi, tier, domain, form, n_used, missing, unexpected, cfg,
     n_params) = build_conscious_states()
    print(f"[weights] TRAINED s16 ckpt loaded — cfg={json.dumps(cfg)}")
    print(f"[weights] n_params={n_params} | missing_keys={len(missing)} unexpected={len(unexpected)}")
    print(f"[encode] N={X.shape[0]} conscious states, dim={X.shape[1]} (post-ln_f mean-pooled)")
    print(f"[labels] tiers={len(np.unique(tier))} domains={len(np.unique(domain))} forms={len(np.unique(form))}")
    print(f"[map] current 2D map = vacuum_psi; distinct coords={len(set(map(tuple, psi)))}")

    results = {
        "data": {
            "corpus_sample": CORPUS_SAMPLE, "corpus_sample_sha256": corpus_sha,
            "ckpt": CKPT, "ckpt_sha256": ckpt_sha,
            "weights": "TRAINED s16 (real carve, not random-init)",
            "cfg": cfg, "n_params": int(n_params),
            "n_encoded": int(X.shape[0]), "conscious_dim": int(X.shape[1]),
            "missing_keys": len(missing), "unexpected_keys": len(unexpected),
            "n_tiers": int(len(np.unique(tier))),
            "n_domains": int(len(np.unique(domain))),
            "n_forms": int(len(np.unique(form))),
            "distinct_vacuum_psi": int(len(set(map(tuple, psi)))),
        },
        "intrinsic": {}, "ladder": {}, "two_d_gap": {},
    }

    # ---- intrinsic dimension over 3 sub-sample seeds ----
    N = X.shape[0]
    sub_n = min(2500, N)  # subsample for O(N^2) trust/cont feasibility
    pca_runs = {}; pr_runs = []; twonn_runs = []; mle_runs = []
    Xc_full = X - X.mean(0)
    for s in SEEDS:
        rng = np.random.RandomState(s)
        sel = rng.choice(N, sub_n, replace=False)
        Xs = Xc_full[sel]
        pk = pca_knee(Xs)
        for kk, vv in pk.items():
            if kk == "evr_first20":
                continue
            pca_runs.setdefault(kk, []).append(vv)
        pr_runs.append(participation_ratio(Xs))
        twonn_runs.append(twonn(Xs))
        mle_runs.append(mle_levina_bickel(Xs))

    def ms(a):
        return [float(np.mean(a)), float(np.std(a))]

    results["intrinsic"] = {
        "pca_pcs_for_80pct": ms(pca_runs["pcs_for_80pct"]),
        "pca_pcs_for_90pct": ms(pca_runs["pcs_for_90pct"]),
        "pca_pcs_for_95pct": ms(pca_runs["pcs_for_95pct"]),
        "pca_elbow_pc": ms(pca_runs["elbow_pc"]),
        "participation_ratio": ms(pr_runs),
        "twonn": ms(twonn_runs),
        "mle_levina_bickel": ms(mle_runs),
        "evr_first20_seed0": pca_knee(Xc_full[np.random.RandomState(0).choice(N, sub_n, False)])["evr_first20"],
    }
    print("[intrinsic] PCA 80/90/95% PCs:",
          results["intrinsic"]["pca_pcs_for_80pct"],
          results["intrinsic"]["pca_pcs_for_90pct"],
          results["intrinsic"]["pca_pcs_for_95pct"])
    print("[intrinsic] elbow_pc:", results["intrinsic"]["pca_elbow_pc"])
    print("[intrinsic] participation_ratio:", results["intrinsic"]["participation_ratio"])
    print("[intrinsic] TwoNN:", results["intrinsic"]["twonn"])
    print("[intrinsic] MLE(Levina-Bickel):", results["intrinsic"]["mle_levina_bickel"])

    # ---- projection-dim ladder ----
    # downstream baseline: discrimination on FULL d=768
    disc_full = {}
    for lab_name, lab in [("tier", tier), ("domain", domain), ("form", form)]:
        disc_full[lab_name] = discrimination(X, lab, 0)
    results["ladder"]["disc_full_d768"] = disc_full
    print("[ladder] full-d768 discrimination (f1_macro):", disc_full)

    for D in LADDER:
        var_runs = []; trust_runs = []; cont_runs = []
        disc_runs = {"tier": [], "domain": [], "form": []}
        for s in SEEDS:
            rng = np.random.RandomState(s)
            sel = rng.choice(N, sub_n, replace=False)
            Xs = Xc_full[sel]
            p = PCA(n_components=D).fit(Xs)
            Xp = p.transform(Xs)
            var_runs.append(float(np.sum(p.explained_variance_ratio_)))
            tr, co = trustworthiness_continuity(Xs, Xp, n_neighbors=12)
            trust_runs.append(tr); cont_runs.append(co)
            for lab_name, lab in [("tier", tier[sel]), ("domain", domain[sel]),
                                  ("form", form[sel])]:
                disc_runs[lab_name].append(discrimination(Xp, lab, s))
        results["ladder"][f"D{D}"] = {
            "var_retained": ms(var_runs),
            "trustworthiness": ms(trust_runs),
            "continuity": ms(cont_runs),
            "disc_tier": ms(disc_runs["tier"]),
            "disc_domain": ms(disc_runs["domain"]),
            "disc_form": ms(disc_runs["form"]),
        }
        print(f"[ladder] D={D:2d} var={ms(var_runs)[0]:.3f} "
              f"trust={ms(trust_runs)[0]:.3f} cont={ms(cont_runs)[0]:.3f} "
              f"disc_domain={ms(disc_runs['domain'])[0]:.3f}")

    # ---- 2D gap ----
    # (a) how much variance does PCA-2D retain
    d2 = results["ladder"]["D2"]
    # (b) how much does the ACTUAL current map (vacuum_psi) retain vs PCA-2D?
    #     measure trustworthiness of vacuum_psi as a 2D embedding of X.
    rng = np.random.RandomState(0)
    sel = rng.choice(N, sub_n, replace=False)
    tr_vp, co_vp = trustworthiness_continuity(Xc_full[sel], psi[sel], n_neighbors=12)
    # correlation of vacuum_psi with top-2 PCs
    p2 = PCA(n_components=2).fit(Xc_full[sel])
    Xp2 = p2.transform(Xc_full[sel])
    def canon_corr(A, B):
        from numpy.linalg import svd, qr
        Qa, _ = qr(A - A.mean(0)); Qb, _ = qr(B - B.mean(0))
        s = svd(Qa.T @ Qb, compute_uv=False)
        return [float(v) for v in s]
    cc = canon_corr(Xp2, psi[sel])

    # intrinsic d consensus
    intr_estimates = [results["intrinsic"]["twonn"][0],
                      results["intrinsic"]["mle_levina_bickel"][0],
                      results["intrinsic"]["pca_elbow_pc"][0]]
    pr_d = results["intrinsic"]["participation_ratio"][0]
    results["two_d_gap"] = {
        "pca_2d_var_retained": d2["var_retained"],
        "pca_2d_trustworthiness": d2["trustworthiness"],
        "pca_2d_continuity": d2["continuity"],
        "actual_vacuum_psi_trustworthiness": float(tr_vp),
        "actual_vacuum_psi_continuity": float(co_vp),
        "vacuum_psi_vs_pca2d_canoncorr": cc,
        "intrinsic_d_consensus_estimates": intr_estimates,
        "participation_ratio_d": pr_d,
        "pca_pcs_for_90pct": results["intrinsic"]["pca_pcs_for_90pct"][0],
    }
    print(f"[2d-gap] PCA-2D var retained = {d2['var_retained'][0]:.3f}")
    print(f"[2d-gap] actual vacuum_psi trustworthiness = {tr_vp:.3f} (cont {co_vp:.3f})")
    print(f"[2d-gap] vacuum_psi vs PCA-2D canonical corr = {cc}")
    print(f"[2d-gap] intrinsic-d consensus = {intr_estimates}, PR = {pr_d:.2f}")

    results["wall_s"] = time.time() - t0
    return results


if __name__ == "__main__":
    out = run()
    outdir = os.path.join(HERE, "..", "_kosmos_real_dim_out")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "results.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\n[done] wall={out['wall_s']:.1f}s -> results.json")
