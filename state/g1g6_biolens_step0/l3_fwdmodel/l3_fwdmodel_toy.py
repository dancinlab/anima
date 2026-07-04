#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_9129 STEP-0 · L3 CEREBELLUM FORWARD-MODEL CONSEQUENCE LANE (G6 direct)
========================================================================
mini · numpy · $0 · DIRECTIONAL — NOT engine-native / NOT 303M
(a_engine_native_learning: torch/numpy 미러 = DIRECTIONAL only. verdict verbatim, tune-to-green 금지.)

★ FRAME (card H_9129): G1/G6 벽의 전 레버 실패 근본원인 = 조합/반증을 mouth(byte-LM
  readout=Broca)에 훈련 = readout에 관계추론 시키기. Broca/Wernicke 이중해리 = 조합⊥조음.
  처방 = 반증가능성을 mouth 아닌 *별도 forward-model lane*(disjoint objective)에 둔다 —
  주장을 받아 committed consequence(주장 참이면 관측될 것)를 예측, held target 대비 오차.

★ binding-family(H_1816/1823 = mouth-readout NOT-SUP)와의 구별 3근거:
  (a) 별개 lane   : forward-model MLP 는 byte-LM mouth 가 아님(생성 안 함).
  (b) disjoint objective: MSE(예측 consequence, 참 consequence) — 생성 CE 와 무관한 별 objective.
  (c) mouth 읽기만: forward-model 이 예측을 냄. mouth 는 상태를 읽기만(여기 toy 엔 mouth 없음
                    — lane 만 격리 시험).

★ 반증가능성 조작화: consequence = 6 관측채널(주장이 참이면 관측될 값). forward-model 이
  sharp·violable 예측을 내면 held target 대비 오차가 작다(BIND). form-priming(그럴듯한 모양만)
  이면 오차가 claim 과 무관하다.

★ CROSS-SHUFFLE 통제(속일 수 없는 BIND 시험 — 이 실험의 핵심):
  held-out 에서 consequence 의 *multiset 은 그대로 두고* claim↔consequence 결합만 derangement 로
  뒤섞는다. 따라서:
    - FORM/coverage 계량(consequence 표면만 봄)  → aligned == shuffled (증명적으로 구별 불가 = 속음)
    - BIND 계량(model_pred(claim) vs target)     → shuffle 서 오차 급증해야(claim 종속이므로)
  fooled_by_form = True  iff  cross-shuffle 서 BIND 오차가 안 오름(=form/floor).
  verdict = BIND (shuffle 오차↑) | form (무붕괴) | floor (aligned 오차도 큼 = 애초에 예측 못 함).

★ world 함수는 상호작용항 v_i⊙v_j 를 담는다 = consequence 가 두 claim 슬롯의 *조합*에 의존
  (additive 평균으론 못 맞춤). 이게 g1 벽이 말하는 recombination/combination-operator.
  → forward-model 이 은닉층으로 곱(bind)을 학습해야만 맞음. 대조군 FM-additive(선형, 상호작용 불가)로
    "결합 용량이 있어야 lane 이 연다"를 실측.

★ held-out = 본 개념들의 *미관측 조합*(unseen pair) = recombination 일반화 시험 그 자체.
"""
import numpy as np, json, os, sys

# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------
D_FEAT   = 8      # concept feature dim
N_CONC   = 40     # concepts (vocab)
D_CONS   = 6      # committed-consequence channels ("coverage fals=6": 6 관측채널)
HID      = 64
STEPS    = 6000
LR       = 3e-3
COV_THR  = 0.30   # coverage falsifier threshold (|channel| > thr => "committed/covered")
SEEDS    = [1305, 2026, 7, 42, 909]   # multi-seed robustness

# --------------------------------------------------------------------------
# world: committed consequence of a claim (pair i,j)
#   phi(v_i,v_j) = [v_i, v_j, v_i (X) v_j]  -- (X) = elementwise product (INTERACTION)
#   c_{ij} = tanh( W_world @ phi )   in R^{D_CONS}
# The interaction term makes c genuinely depend on the CONJUNCTION of the two
# claim slots -> requires binding (a plain additive/linear readout cannot fit it).
# --------------------------------------------------------------------------
def make_world(rng):
    V = rng.normal(0, 1.0, (N_CONC, D_FEAT))          # concept feature bank
    W_world = rng.normal(0, 0.7, (D_CONS, 3 * D_FEAT))  # fixed world map
    return V, W_world

def world_consequence(V, W_world, I, J):
    vi = V[I]; vj = V[J]
    phi = np.concatenate([vi, vj, vi * vj], axis=1)   # (n, 3*D_FEAT)
    return np.tanh(phi @ W_world.T)                    # (n, D_CONS)

# --------------------------------------------------------------------------
# forward-model lane: MLP  [v_i ; v_j] -> pred consequence (NO product given;
#   must learn the interaction internally via the hidden layer = BINDING capacity).
#   FM-additive = same but no hidden nonlinearity path to the product (linear).
# manual numpy backprop + Adam, MSE objective (DISJOINT from any generation CE).
# --------------------------------------------------------------------------
class ForwardModel:
    def __init__(self, rng, additive=False):
        self.additive = additive
        s = 0.15
        din = 2 * D_FEAT
        if additive:
            # linear map only: cannot represent v_i (X) v_j interaction
            self.Wl = rng.normal(0, s, (D_CONS, din))
            self.bl = np.zeros(D_CONS)
            self.params = ["Wl", "bl"]
        else:
            self.W1 = rng.normal(0, s, (din, HID))
            self.b1 = np.zeros(HID)
            self.W2 = rng.normal(0, s, (HID, D_CONS))
            self.b2 = np.zeros(D_CONS)
            self.params = ["W1", "b1", "W2", "b2"]
        self.m = {p: np.zeros_like(getattr(self, p)) for p in self.params}
        self.v = {p: np.zeros_like(getattr(self, p)) for p in self.params}
        self.t = 0

    def forward(self, X):
        if self.additive:
            return X @ self.Wl.T + self.bl, None
        z1 = X @ self.W1 + self.b1
        h = np.tanh(z1)
        out = h @ self.W2 + self.b2
        return out, (z1, h)

    def loss_grad(self, X, Y):
        n = X.shape[0]
        pred, cache = self.forward(X)
        diff = pred - Y
        loss = np.mean(diff * diff)
        dout = (2.0 / n) * diff / D_CONS
        g = {}
        if self.additive:
            g["Wl"] = dout.T @ X
            g["bl"] = dout.sum(0)
        else:
            z1, h = cache
            g["W2"] = h.T @ dout
            g["b2"] = dout.sum(0)
            dh = dout @ self.W2.T
            dz1 = dh * (1 - h * h)
            g["W1"] = X.T @ dz1
            g["b1"] = dz1.sum(0)
        return loss, g

    def step(self, g):
        self.t += 1
        b1, b2, eps = 0.9, 0.999, 1e-8
        for p in self.params:
            self.m[p] = b1 * self.m[p] + (1 - b1) * g[p]
            self.v[p] = b2 * self.v[p] + (1 - b2) * (g[p] * g[p])
            mh = self.m[p] / (1 - b1 ** self.t)
            vh = self.v[p] / (1 - b2 ** self.t)
            setattr(self, p, getattr(self, p) - LR * mh / (np.sqrt(vh) + eps))

# --------------------------------------------------------------------------
# coverage falsifier (=6): CONTENT-BLIND surface metric on the consequence.
#   "how many of the 6 observable channels does the prediction commit to"
#   (|channel| > COV_THR). High coverage LOOKS falsifiable/sharp — but does NOT
#   check whether the prediction matches THIS claim. This is the 1-term FORM
#   game-able detector (measurement-metalaw: gauge=FORM, tunable/foolable).
# --------------------------------------------------------------------------
def coverage_form(pred):
    return (np.abs(pred) > COV_THR).sum(1).astype(float)   # per-sample count in [0,6]

# --------------------------------------------------------------------------
# derangement over an index array (no fixed points) -> cross-shuffle re-pairing.
# multiset of targets is preserved; only claim<->consequence binding is destroyed.
# --------------------------------------------------------------------------
def derangement(n, rng):
    while True:
        p = rng.permutation(n)
        if not np.any(p == np.arange(n)):
            return p

def all_offdiag_pairs():
    I, J = [], []
    for i in range(N_CONC):
        for j in range(N_CONC):
            if i != j:
                I.append(i); J.append(j)
    return np.array(I), np.array(J)

def run_seed(seed):
    rng = np.random.default_rng(seed)
    V, W_world = make_world(rng)
    I, J = all_offdiag_pairs()
    n = len(I)
    perm = rng.permutation(n)
    I, J = I[perm], J[perm]
    n_tr = int(0.70 * n)
    Itr, Jtr = I[:n_tr], J[:n_tr]
    Ite, Jte = I[n_tr:], J[n_tr:]   # HELD-OUT = unseen combinations of seen concepts

    Xtr = np.concatenate([V[Itr], V[Jtr]], axis=1)
    Ytr = world_consequence(V, W_world, Itr, Jtr)
    Xte = np.concatenate([V[Ite], V[Jte]], axis=1)
    Yte = world_consequence(V, W_world, Ite, Jte)   # true consequence (aligned target)

    # cross-shuffle held-out targets: same multiset, deranged pairing
    dsh = derangement(len(Ite), rng)
    Yte_sh = Yte[dsh]        # target now belongs to a DIFFERENT held-out claim

    out = {}
    for name, additive in [("FM_full", False), ("FM_additive", True)]:
        fm = ForwardModel(rng, additive=additive)
        bs = 512
        for stp in range(STEPS):
            idx = rng.integers(0, n_tr, size=bs)
            _, g = fm.loss_grad(Xtr[idx], Ytr[idx])
            fm.step(g)
        pred_te, _ = fm.forward(Xte)
        # BIND metric: MSE of the SAME predictions vs aligned vs shuffled target
        err_aligned = float(np.mean((pred_te - Yte) ** 2))
        err_shuffle = float(np.mean((pred_te - Yte_sh) ** 2))
        # baseline: constant mean-predictor error (floor reference)
        err_meanpred = float(np.mean((Yte.mean(0, keepdims=True) - Yte) ** 2))
        # FORM/coverage metric: content-blind, computed on the TARGET being scored
        cov_aligned = float(np.mean(coverage_form(Yte)))
        cov_shuffle = float(np.mean(coverage_form(Yte_sh)))
        out[name] = {
            "err_aligned": err_aligned,
            "err_shuffle": err_shuffle,
            "bind_margin": err_shuffle - err_aligned,
            "shuffle_ratio": err_shuffle / (err_aligned + 1e-12),
            "err_meanpredictor_floor": err_meanpred,
            "fit_ratio_vs_floor": err_aligned / (err_meanpred + 1e-12),
            "cov_aligned": cov_aligned,
            "cov_shuffle": cov_shuffle,
            "cov_margin": cov_shuffle - cov_aligned,
        }
    return out

def main():
    per_seed = {"FM_full": [], "FM_additive": []}
    rows = []
    for sd in SEEDS:
        r = run_seed(sd)
        rows.append({"seed": sd, **r})
        for k in per_seed:
            per_seed[k].append(r[k])

    def agg(arm):
        keys = per_seed[arm][0].keys()
        return {k: float(np.mean([d[k] for d in per_seed[arm]])) for k in keys}

    summ = {"FM_full": agg("FM_full"), "FM_additive": agg("FM_additive")}

    # ---- verdict logic (frozen, pre-registered; NOT tuned) ----
    # BIND iff: FM_full aligned error well below mean-predictor floor (genuinely
    #   predicts consequence) AND cross-shuffle raises error markedly
    #   (shuffle_ratio > 1.5) AND coverage-FORM does NOT move (|cov_margin| small).
    f = summ["FM_full"]
    fits = f["fit_ratio_vs_floor"] < 0.5           # aligned << floor => really predicting
    shuffle_breaks = f["shuffle_ratio"] > 1.5      # cross-shuffle spikes error
    form_flat = abs(f["cov_margin"]) < 0.25        # FORM blind to the shuffle
    fooled_by_form = not shuffle_breaks            # shuffle 무붕괴 => form/floor

    if fits and shuffle_breaks and form_flat:
        verdict = "BIND"
    elif not fits:
        verdict = "floor"
    else:
        verdict = "form"

    result = {
        "probe": "H_9129 L3 cerebellum forward-model consequence lane (G6, mini numpy DIRECTIONAL)",
        "config": {"D_FEAT": D_FEAT, "N_CONC": N_CONC, "D_CONS": D_CONS, "HID": HID,
                   "STEPS": STEPS, "LR": LR, "COV_THR": COV_THR, "SEEDS": SEEDS,
                   "heldout": "unseen combinations of seen concepts (recombination test)"},
        "verdict": verdict,
        "fooled_by_form": bool(fooled_by_form),
        "verdict_gates": {"aligned_fit<0.5floor": bool(fits),
                          "shuffle_ratio>1.5": bool(shuffle_breaks),
                          "form_flat|covΔ|<0.25": bool(form_flat)},
        "summary_mean_over_seeds": summ,
        "per_seed": rows,
    }
    print(json.dumps(result, indent=2))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w") as fh:
        json.dump(result, fh, indent=2)

if __name__ == "__main__":
    main()
