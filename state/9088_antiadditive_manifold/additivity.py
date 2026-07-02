#!/usr/bin/env python3
"""H_9070 additivity diagnostic — engine-native numpy mirror of core.clm_decode.

Re-measures the H_9046 additivity root-cause metric on ANY .clm:
    mean cos(T_ij, unit(a_i + a_j))   over a FIXED seeded pair set
  where a_i = penult("c_i"), T_ij = penult("c_i c_j"), penult = final-groupnorm
  mean-pooled + L2-unit (identical extractor to H_9046/H_9026).
H_9046 baseline on py303_full.clm = 0.861 (=> ~additive manifold = G1 root cause).
FROZEN bar (a): treated ckpt additivity DROPS below 0.861 (target <=0.80).

Also reports a COLLAPSE sanity: mean pairwise cos among single-concept vectors
(if ~1.0 the manifold collapsed = degenerate, not a real reshape).
usage: additivity.py <ckpt.clm> [--pairs 300] [--seed 12345]
"""
import os, sys, argparse
import numpy as np

def load_core():
    sys.path.insert(0, os.path.expanduser("~/anima"))
    sys.path.insert(0, ".")
    from core import clm_decode as cd
    return cd

def unit(v, axis=-1):
    n = np.linalg.norm(v, axis=axis, keepdims=True)
    return v / np.where(n == 0, 1.0, n)

def penult_vec(cd, W, text_bytes):
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
    yn = cd.nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)
    return unit(yn.mean(axis=0))

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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ckpt")
    ap.add_argument("--pairs", type=int, default=300)
    ap.add_argument("--seed", type=int, default=12345)
    a = ap.parse_args()
    cd = load_core()
    assert cd.clm_decodable(a.ckpt), f"{a.ckpt} not clm-decodable"
    W = cd.clm_load_weights(a.ckpt)
    N = len(CONCEPTS)
    part = np.stack([penult_vec(cd, W, c.encode("utf-8")) for c in CONCEPTS])  # [N,d] unit
    rng = np.random.RandomState(a.seed)
    pairs = []
    while len(pairs) < a.pairs:
        i, j = int(rng.randint(N)), int(rng.randint(N))
        if i != j: pairs.append((i, j))
    cosb = []
    for (i, j) in pairs:
        Tij = penult_vec(cd, W, f"{CONCEPTS[i]} {CONCEPTS[j]}".encode("utf-8"))
        add = unit(part[i] + part[j])
        cosb.append(float(np.dot(Tij, add)))
    cosb = np.array(cosb)
    # collapse sanity: mean off-diagonal pairwise cos among singles
    G = part @ part.T
    off = G[~np.eye(N, dtype=bool)]
    print(f"CKPT={a.ckpt}")
    print(f"ADDITIVITY mean cos(T_ij,unit(a_i+a_j)) = {cosb.mean():.4f}  std={cosb.std():.4f}  "
          f"n={len(cosb)}  (H_9046 baseline 0.861; frozen bar (a): DROP <=0.80)")
    print(f"COLLAPSE-sanity mean pairwise single cos = {off.mean():.4f} (near 1.0 => degenerate collapse)")
    print(f"ADD_JSON {{\"additivity\":{cosb.mean():.4f},\"std\":{cosb.std():.4f},"
          f"\"single_pairwise_cos\":{off.mean():.4f},\"n\":{len(cosb)}}}")

if __name__ == "__main__":
    main()
