#!/usr/bin/env python3
"""H_1559 — SAVANT × 학습: 골든존 inhibition 으로 register 특화 학습 (서번트 학습).

DIRECTIONAL numpy MIRROR (a_engine_native_learning hard-gate-1):
  torch unavailable locally + GPU cost-gated (forbidden). This is a numpy
  toy-scale SW mirror — NOT engine-native. verdict = toy-only / DIRECTIONAL;
  303M conv re-measure on live core/ = follow-on ING (cost-gate).

MODEL OF I (inhibition):
  Golden Zone savant model G = D*P/I. P = plasticity = LEARNING. I = the
  TRAINING regularization strength, realized here as the per-register DROPOUT
  rate applied to a SHARED backbone during that register's gradient updates.
  GZ_LOWER = 1/2 - ln(4/3) ~ 0.2123, GZ_UPPER = 1/2, GZ_CENTER = 1/e ~ 0.3679
  (SAVANT/savant_lib.hexa verbatim constants).

WHY DROPOUT == INHIBITION GIVES AN INVERSE-U (savant mechanism, B3):
  A register trained with dropout p on a SHARED-CAPACITY backbone:
    - too LOW I (p~0): no regularization -> the register OVERFITS its train
      slice (memorizes), held-out capability stays mediocre AND it greedily
      grabs shared capacity without consolidating -> no specialization.
    - GOLDEN ZONE I: dropout forces robust, redundant, consolidated features
      for THAT register -> held-out capability hypertrophies + capacity is
      committed to it (savant).
    - too HIGH I (p->1): the register is starved/locked -> underfit, capability
      collapses. => inverse-U in I, peak in the golden zone.

REGISTERS: 4 = {ko, en} x {general, SNS} (a_chat_registers 4칸). Each register
  has its own byte corpus slice; all share ONE backbone (capacity competition).
  Capability(register) = held-out next-byte top-1 accuracy on that register.

This is a TOY. Numbers are live (trained), captured verbatim. No tune-to-green:
  the 5 bars + thresholds are the card's frozen-first bars, read from the card.
"""
from __future__ import annotations
import json, math, time

import numpy as np

# ── SAVANT/savant_lib.hexa verbatim constants ──────────────────────────────
GZ_WIDTH  = math.log(4.0 / 3.0)            # 0.28768207244178085
GZ_LOWER  = 0.5 - GZ_WIDTH                  # 0.21231792755821914
GZ_UPPER  = 0.5
GZ_CENTER = 1.0 / math.e                    # 0.36787944117144233
SI_THRESH = 3.0

REGISTERS = ["ko_general", "ko_sns", "en_general", "en_sns"]
NR = len(REGISTERS)
BASE = {"ko_general": 0x80, "ko_sns": 0x90, "en_general": 0x41, "en_sns": 0x61}


def sa_savant_index(phis):
    a = np.asarray(phis, dtype=float)
    m = a.mean()
    if m <= 0:
        return 0.0
    return float(a.max() / m)


# ── synthetic per-register byte corpora ────────────────────────────────────
def make_register_corpus(reg_id, n_bytes, rng):
    base = BASE[reg_id]
    alpha = 16
    noise = 0.30 if reg_id.endswith("sns") else 0.10   # SNS noisier
    order = 1 if reg_id.endswith("sns") else 2          # general = longer range
    treg = np.random.RandomState(hash(reg_id) & 0xFFFF)
    T = treg.dirichlet(np.ones(alpha) * 0.4, size=alpha ** order)
    out = np.empty(n_bytes, dtype=np.int64)
    ctx = 0
    for t in range(n_bytes):
        if rng.random() < noise:
            nxt = rng.integers(0, alpha)
        else:
            nxt = treg.choice(alpha, p=T[ctx % T.shape[0]])
        out[t] = base + nxt
        ctx = (ctx * alpha + nxt) % (alpha ** order)
    return out


# ── tiny shared-backbone byte LM (numpy, manual fwd/bwd) ───────────────────
class ToyLM:
    def __init__(self, d, h, rng):
        self.d, self.h = d, h
        self.E = rng.normal(0, 0.1, (256, d))
        self.W1 = rng.normal(0, 1.0 / math.sqrt(d), (d, h))
        self.b1 = np.zeros(h)
        self.W2 = [rng.normal(0, 1.0 / math.sqrt(h), (h, 256)) for _ in range(NR)]
        self.b2 = [np.zeros(256) for _ in range(NR)]

    def fwd(self, x, r, drop, rng):
        e = self.E[x]
        z1 = e @ self.W1 + self.b1
        a1 = 0.5 * z1 * (1 + np.tanh(0.7978845608 * (z1 + 0.044715 * z1 ** 3)))
        mask = None
        if drop > 0 and rng is not None:
            mask = (rng.random(a1.shape) >= drop).astype(np.float64) / (1 - drop)
            a1d = a1 * mask
        else:
            a1d = a1
        logits = a1d @ self.W2[r] + self.b2[r]
        return e, z1, a1, a1d, mask, logits

    def loss_acc(self, x, y, r):
        _, _, _, a1d, _, logits = self.fwd(x, r, 0.0, None)
        logits = logits - logits.max(1, keepdims=True)
        p = np.exp(logits); p /= p.sum(1, keepdims=True)
        ce = -np.log(p[np.arange(len(y)), y] + 1e-12).mean()
        acc = (logits.argmax(1) == y).mean()
        return float(ce), float(acc)


def train_lm(d, h, corpora, drops, steps, bs, lr, rng):
    lm = ToyLM(d, h, rng)
    splits = []
    for c in corpora:
        n = len(c); cut = int(n * 0.8)
        splits.append((c[:cut], c[cut:]))
    for step in range(steps):
        for r in range(NR):
            tr = splits[r][0]
            i = rng.integers(0, len(tr) - 1, bs)
            x = tr[i]; y = tr[i + 1]
            e, z1, a1, a1d, mask, logits = lm.fwd(x, r, drops[r], rng)
            logits = logits - logits.max(1, keepdims=True)
            p = np.exp(logits); p /= p.sum(1, keepdims=True)
            dlog = p.copy(); dlog[np.arange(bs), y] -= 1; dlog /= bs
            gW2 = a1d.T @ dlog; gb2 = dlog.sum(0)
            da1d = dlog @ lm.W2[r].T
            da1 = da1d * mask if mask is not None else da1d
            g = 0.5 * (1 + np.tanh(0.7978845608 * (z1 + 0.044715 * z1 ** 3)))
            dz1 = da1 * g
            gW1 = e.T @ dz1; gb1 = dz1.sum(0)
            de = dz1 @ lm.W1.T
            lm.W2[r] -= lr * gW2; lm.b2[r] -= lr * gb2
            lm.W1 -= lr * gW1; lm.b1 -= lr * gb1
            np.add.at(lm.E, x, -lr * de)
    return lm, splits


def eval_caps(lm, splits):
    caps = []
    for r in range(NR):
        ho = splits[r][1]
        x = ho[:-1]; y = ho[1:]
        _, acc = lm.loss_acc(x, y, r)
        caps.append(acc)
    return caps


def run(seed, savant_r=0, savant_I=GZ_CENTER, baseline_I=0.0,
        d=24, h=48, steps=140, bs=64, lr=0.5, n_bytes=6000):
    rng = np.random.default_rng(seed)
    corpora = [make_register_corpus(REGISTERS[r], n_bytes, rng) for r in range(NR)]
    drops = [baseline_I] * NR
    drops[savant_r] = savant_I
    lm, splits = train_lm(d, h, corpora, drops, steps, bs, lr, rng)
    return eval_caps(lm, splits)


def main():
    t0 = time.time()
    SEEDS = [0, 1, 2]
    out = {"meta": {"mirror": "numpy DIRECTIONAL toy (torch/GPU unavail+cost-gate)",
                    "GZ_LOWER": GZ_LOWER, "GZ_UPPER": GZ_UPPER,
                    "GZ_CENTER": GZ_CENTER, "SI_THRESH": SI_THRESH,
                    "registers": REGISTERS, "seeds": SEEDS}}

    base_caps = np.array([run(s, savant_r=0, savant_I=0.0, baseline_I=0.0)
                          for s in SEEDS])
    base_mean = base_caps.mean(0)
    base_SI = float(np.mean([sa_savant_index(base_caps[i]) for i in range(len(SEEDS))]))

    sav_caps = np.array([run(s, savant_r=0, savant_I=GZ_CENTER, baseline_I=0.0)
                         for s in SEEDS])
    sav_mean = sav_caps.mean(0)
    sav_SI = float(np.mean([sa_savant_index(sav_caps[i]) for i in range(len(SEEDS))]))

    b1_lift = float(sav_mean[0] - base_mean[0])
    b2_SI = sav_SI
    other_delta = float(sav_mean[1:].mean() - base_mean[1:].mean())

    I_grid = [0.0, 0.05, 0.10, GZ_LOWER, GZ_CENTER, GZ_UPPER, 0.65, 0.80, 0.92]
    sweep = []
    for I in I_grid:
        caps = np.array([run(s, savant_r=0, savant_I=I, baseline_I=0.0)
                         for s in SEEDS])
        sweep.append(float(caps.mean(0)[0]))
    peak_idx = int(np.argmax(sweep))
    peak_I = I_grid[peak_idx]
    in_gz = bool(GZ_LOWER <= peak_I <= GZ_UPPER)
    rose = sweep[peak_idx] > sweep[0] + 1e-4
    fell = sweep[-1] < sweep[peak_idx] - 1e-4
    inverse_u = bool(rose and fell)

    hits = 0
    ctrl_trials = []
    for tr in [0, 1, 2, 3]:
        caps = np.array([run(s + 10, savant_r=tr, savant_I=GZ_CENTER,
                             baseline_I=0.0) for s in SEEDS])
        winner = int(np.argmax(caps.mean(0)))
        ctrl_trials.append({"target": tr, "winner": winner})
        if winner == tr:
            hits += 1
    ctrl_hit_rate = hits / 4.0

    B1 = b1_lift > 0.0
    B2 = b2_SI >= SI_THRESH
    B3 = in_gz and inverse_u
    B4 = other_delta < 0.0
    B5 = ctrl_hit_rate >= 0.75

    out["B1_savant_register"] = {"lift": b1_lift, "savant_acc": float(sav_mean[0]),
                                 "baseline_acc": float(base_mean[0]), "PASS": bool(B1)}
    out["B2_SI"] = {"savant_SI": b2_SI, "baseline_SI": base_SI,
                    "threshold": SI_THRESH, "PASS": bool(B2)}
    out["B3_GZ_window"] = {"I_grid": I_grid, "sweep_acc": sweep,
                           "peak_I": peak_I, "in_GZ": in_gz,
                           "inverse_U": inverse_u, "PASS": bool(B3)}
    out["B4_tradeoff"] = {"other_delta": other_delta,
                          "savant_others_mean": float(sav_mean[1:].mean()),
                          "baseline_others_mean": float(base_mean[1:].mean()),
                          "PASS": bool(B4)}
    out["B5_control"] = {"ctrl_hit_rate": ctrl_hit_rate, "trials": ctrl_trials,
                         "PASS": bool(B5)}
    out["caps"] = {"baseline_mean": base_mean.tolist(),
                   "savant_mean": sav_mean.tolist()}
    headline = B1 and B2 and B4
    out["VERDICT"] = {
        "B1": bool(B1), "B2": bool(B2), "B3": bool(B3), "B4": bool(B4), "B5": bool(B5),
        "headline_B1_B2_B4": bool(headline),
        "tier": "DIRECTIONAL (numpy toy mirror; engine-native + 303M scale = cost-gate ING)",
        "wall_s": round(time.time() - t0, 1),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
