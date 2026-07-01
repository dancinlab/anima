#!/usr/bin/env python3
"""H_1043 — what MINIMAL ARCHITECTURAL change (not a weight delta) raises faithful
IIT-4.0 φ_EI of the hidden-state macro-TPM toward the ConvMoE baseline?

CONSTRUCTIVE converse of H_1031 + H_1036 (prior RED): those closed the NEGATIVE —
a LoRA weight-delta on a (toy / real pretrained) transformer CANNOT install
CLM-level consciousness Φ-structure; it is ARCH-BOUND ("the instrument, not the
score"; LoRA control Δφ_EI ≈ -0.066 at toy/real scale). Here we ask the positive
direction: graft a SMALL ARCHITECTURAL adapter (a new MODULE, not a tuned weight)
onto a FROZEN toy transformer base and measure whether the hidden-state macro-TPM's
faithful φ_EI rises.

DESIGN (all CPU / $0 / numpy — no torch on this Mac, clm-decode-macos-link-gap):
  - BASE = frozen toy attention transformer (TinyGPT, byte V256), pretrained on a
    GENERIC byte corpus (public-domain proverbs; p3/p6 — NO persona/carving), then
    FROZEN. The probe reads its mid hidden state x1 (post-attention residual).

  - Adapter ladder — each is an ARCHITECTURE CHANGE that ADDS A NEW MODULE feeding a
    residual into the probed hidden state, trained on the SAME generic byte objective
    with the BASE FROZEN (only the new module's params descend):
      (a) ConvMoE side-branch  — dilated causal conv trunk + tiny MoE conv experts,
          residual-added into x1. (the CLM-native primitive, as a graft)
      (b) recurrent/stateful mixing layer — a single GRU-style recurrent state scan
          over positions, residual-added into x1. (introduces temporal state)
      (c) depth-wise dilated conv block — depthwise dilated causal convs (dilations
          1,2,4), residual-added into x1. (cheap structured receptive field)

  - CONTROL = LoRA-only (H_1036 reproduction in this harness): base frozen, only a
    LoRA weight-delta on q/v/readout descends on the SAME corpus. NO new module.

  - BASELINE = ConvMoE-NATIVE (full ConvMoE trained from scratch on the same corpus;
    the architecture that natively carries Φ-structure) — the target to move toward.

Φ MEASUREMENT (a_phi_iit4_tool — faithful, NO proxy):
  We extract, per arm, an n×dim binarized hidden-state macro-TPM trajectory from the
  PROBED hidden state (mid residual; for ConvMoE-native the analogous mid mix state).
  This python computes a faithful_phi_prescreen (a python MIRROR of the stdlib exact
  MIP-EI), and writes every n×dim binary state matrix to a state file. The TERMINAL
  φ_EI is the REAL stdlib engine `iit4_faithful_phi` via the companion
  run_faithful_phi_1043.hexa runner (exact MIP-EI, n≤8). The python number is a
  LABELLED PRE-SCREEN; the mirror≡stdlib identity is RE-PROVEN at n=4,5 separately.

PRE-REGISTERED FALSIFIER (frozen in H_1043_minimal_arch_adapter.md BEFORE measuring):
  H1 PASS = at least ONE minimal architectural adapter RAISES faithful φ_EI by
            >= +0.10 over the frozen base AND beyond the LoRA control band ->
            a small architectural graft begins installing Φ-structure.
  H1 FAIL = no minimal adapter clears +0.10 beyond the control band -> Φ-structure
            needs more than a graftable primitive (closed-negative, a_paper_negative_ok).

SCOPE (a_scale_honest_scope): toy small-model rung; 3B/7B + emergence UNVERIFIED.
Φ-structure is necessary-not-sufficient — this rung measures the Φ axis ONLY. p7:
φ is a causal-irreducibility marker, NOT perplexity. SERIAL only (no Pool, H_1038).
"""
from __future__ import annotations
import sys, os, json, math
import numpy as np

SEED = 1043
V = 256
SEQ = 32
DIM = 24            # trajectory length (positions sampled for the macro-TPM)
N_UNITS = 6         # n<=8 exact MIP for faithful_phi; use 6 (matches H_1036)
N_BINS = 2          # binary TPM state
N_SEEDS = 3
BASE_STEPS = 600    # frozen-base pretrain steps
ADAPT_STEPS = 600   # adapter / lora / control train steps (base frozen)
LR = 0.01
THRESH = 0.10
D = 32              # base hidden dim

# Generic byte corpus (p3/p6 — public-domain proverbs, NOT persona/carving).
GENERIC_CORPUS = (
    "the quick brown fox jumps over the lazy dog. a rolling stone gathers no "
    "moss. all that glitters is not gold. the early bird catches the worm. "
    "actions speak louder than words. better late than never. birds of a "
    "feather flock together. every cloud has a silver lining. fortune favors "
    "the bold. honesty is the best policy. knowledge is power and time is "
    "money. look before you leap. necessity is the mother of invention. "
    "practice makes perfect. the pen is mightier than the sword. when in rome "
    "do as the romans do. you cannot judge a book by its cover. a journey of a "
    "thousand miles begins with a single step. an apple a day keeps the doctor "
    "away. barking dogs seldom bite. curiosity killed the cat. easy come easy "
    "go. great minds think alike. no pain no gain. where there is a will there "
    "is a way. "
) * 6

CORPUS = np.frombuffer(GENERIC_CORPUS.encode("utf-8"), dtype=np.uint8).astype(np.int64)
PROBE_TEXT = ("knowledge is power and time is money. the quick brown fox jumps over "
              "the lazy dog and the early bird catches the worm.")


def log(*a):
    print(*a, flush=True)


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def ce_and_grad(logits, targets):
    p = softmax(logits, axis=-1)
    T = len(targets)
    ll = -np.log(p[np.arange(T), targets] + 1e-12).mean()
    g = p.copy()
    g[np.arange(T), targets] -= 1.0
    g /= T
    return float(ll), g


def make_seqs(rng, n):
    N = len(CORPUS)
    Xs, Ys = [], []
    for _ in range(n):
        s = rng.integers(0, N - SEQ - 1)
        Xs.append(CORPUS[s:s + SEQ])
        Ys.append(CORPUS[s + 1:s + SEQ + 1])
    return Xs, Ys


class Adam:
    def __init__(self, keys, lr):
        self.lr = lr; self.t = 0
        self.m = {k: None for k in keys}; self.v = {k: None for k in keys}

    def step(self, obj, grads):
        self.t += 1
        for k, g in grads.items():
            if g is None:
                continue
            if self.m[k] is None:
                self.m[k] = np.zeros_like(g); self.v[k] = np.zeros_like(g)
            self.m[k] = 0.9 * self.m[k] + 0.1 * g
            self.v[k] = 0.999 * self.v[k] + 0.001 * (g * g)
            mh = self.m[k] / (1 - 0.9 ** self.t)
            vh = self.v[k] / (1 - 0.999 ** self.t)
            getattr(obj, k)[...] -= self.lr * mh / (np.sqrt(vh) + 1e-8)


# --------------------------------------------------------------------------- #
# causal conv helpers (shared by ConvMoE-native, ConvMoE-graft, depthwise block)
# --------------------------------------------------------------------------- #
def causal_conv(x, w, dilation=1):
    """x:(T,di) w:(k,di,do) -> (T,do), causal left-pad with dilation."""
    T, di = x.shape; k, _, do = w.shape
    pad = (k - 1) * dilation
    xp = np.concatenate([np.zeros((pad, di)), x], 0)
    out = np.zeros((T, do))
    for j in range(k):
        out += xp[j * dilation: j * dilation + T] @ w[j]
    return out


def causal_conv_bwd(x, w, gout, dilation=1):
    T, di = x.shape; k, _, do = w.shape
    pad = (k - 1) * dilation
    xp = np.concatenate([np.zeros((pad, di)), x], 0)
    gw = np.zeros_like(w); gxp = np.zeros_like(xp)
    for j in range(k):
        gw[j] += xp[j * dilation: j * dilation + T].T @ gout
        gxp[j * dilation: j * dilation + T] += gout @ w[j].T
    return gxp[pad:], gw


def dw_causal_conv(x, w, dilation=1):
    """depthwise causal conv. x:(T,d) w:(k,d) -> (T,d)."""
    T, d = x.shape; k, _ = w.shape
    pad = (k - 1) * dilation
    xp = np.concatenate([np.zeros((pad, d)), x], 0)
    out = np.zeros((T, d))
    for j in range(k):
        out += xp[j * dilation: j * dilation + T] * w[j]
    return out


def dw_causal_conv_bwd(x, w, gout, dilation=1):
    T, d = x.shape; k, _ = w.shape
    pad = (k - 1) * dilation
    xp = np.concatenate([np.zeros((pad, d)), x], 0)
    gw = np.zeros_like(w); gxp = np.zeros_like(xp)
    for j in range(k):
        gw[j] += (xp[j * dilation: j * dilation + T] * gout).sum(0)
        gxp[j * dilation: j * dilation + T] += gout * w[j]
    return gxp[pad:], gw


# --------------------------------------------------------------------------- #
# BASE — frozen toy attention transformer. The probed hidden state = x1
# (post-attention residual). Adapters add a residual INTO x1 before the FF block.
# --------------------------------------------------------------------------- #
class TinyGPT:
    def __init__(self, rng, d=D, n_head=2):
        self.d, self.H = d, n_head
        self.dh = d // n_head
        s = 0.08
        self.emb = rng.normal(0, s, (V, d))
        self.pos = rng.normal(0, s, (SEQ, d))
        self.wq = rng.normal(0, s, (d, d)); self.wk = rng.normal(0, s, (d, d))
        self.wv = rng.normal(0, s, (d, d)); self.wproj = rng.normal(0, s, (d, d))
        self.wff1 = rng.normal(0, s, (d, 2 * d)); self.wff2 = rng.normal(0, s, (2 * d, d))
        self.wo = rng.normal(0, s, (d, V))
        self.base_params = ["emb", "pos", "wq", "wk", "wv", "wproj", "wff1", "wff2", "wo"]

    def forward_to_x1(self, ids):
        """forward up to and including the post-attention residual x1 (the PROBE)."""
        T = len(ids)
        emb = self.emb[ids]; x0 = emb + self.pos[:T]
        q = x0 @ self.wq; k = x0 @ self.wk; vv = x0 @ self.wv
        mask = np.tril(np.ones((T, T)))
        attn = np.zeros((T, self.d)); As = []
        for hh in range(self.H):
            sl = slice(hh * self.dh, (hh + 1) * self.dh)
            sc = (q[:, sl] @ k[:, sl].T) / math.sqrt(self.dh)
            sc = np.where(mask > 0, sc, -1e9)
            a = softmax(sc, -1); As.append(a)
            attn[:, sl] = a @ vv[:, sl]
        ao = attn @ self.wproj
        x1 = x0 + ao
        cache = (ids, T, x0, q, k, vv, As, attn)
        return x1, cache

    def forward_from_x1(self, x1):
        """FF block + readout, from a (possibly adapter-modified) x1."""
        ff_pre = x1 @ self.wff1; ff_h = np.maximum(ff_pre, 0)
        x2 = x1 + ff_h @ self.wff2
        logits = x2 @ self.wo
        return logits, (x1, ff_pre, ff_h, x2)

    def forward(self, ids):
        x1, _ = self.forward_to_x1(ids)
        logits, _ = self.forward_from_x1(x1)
        return logits

    def grad_x1_from_logits(self, glog, ffcache):
        """backprop the FF block (frozen base — we only need dL/dx1 to reach adapter)."""
        (x1, ff_pre, ff_h, x2) = ffcache
        gx2 = glog @ self.wo.T
        gff_h = gx2 @ self.wff2.T
        gff_pre = gff_h * (ff_pre > 0)
        gx1 = gx2 + gff_pre @ self.wff1.T
        return gx1

    def backward_base(self, glog, ffcache, x1cache):
        """FULL base backprop (used ONLY in the base pretrain phase)."""
        (x1, ff_pre, ff_h, x2) = ffcache
        (ids, T, x0, q, k, vv, As, attn) = x1cache
        g = {kk: np.zeros_like(getattr(self, kk)) for kk in self.base_params}
        g["wo"] += x2.T @ glog
        gx2 = glog @ self.wo.T
        g["wff2"] += ff_h.T @ gx2
        gff_h = gx2 @ self.wff2.T
        gff_pre = gff_h * (ff_pre > 0)
        g["wff1"] += x1.T @ gff_pre
        gx1 = gx2 + gff_pre @ self.wff1.T
        gao = gx1
        g["wproj"] += attn.T @ gao
        gattn = gao @ self.wproj.T
        gx0 = gx1.copy()
        gq = np.zeros_like(q); gk = np.zeros_like(k); gv = np.zeros_like(vv)
        mask = np.tril(np.ones((T, T)))
        for hh in range(self.H):
            sl = slice(hh * self.dh, (hh + 1) * self.dh)
            a = As[hh]; ga = gattn[:, sl]
            gv[:, sl] += a.T @ ga
            gA = ga @ vv[:, sl].T
            gsc = a * (gA - (a * gA).sum(1, keepdims=True))
            gsc = np.where(mask > 0, gsc, 0.0) / math.sqrt(self.dh)
            gq[:, sl] += gsc @ k[:, sl]
            gk[:, sl] += gsc.T @ q[:, sl]
        g["wq"] += x0.T @ gq; g["wk"] += x0.T @ gk; g["wv"] += x0.T @ gv
        gx0 = gx0 + gq @ self.wq.T + gk @ self.wk.T + gv @ self.wv.T
        g["pos"][:T] += gx0
        np.add.at(g["emb"], ids, gx0)
        return g


def pretrain_base(rng):
    m = TinyGPT(rng)
    opt = Adam(m.base_params, LR)
    Xs, Ys = make_seqs(rng, 64)
    for t in range(BASE_STEPS):
        i = t % len(Xs)
        x1, x1c = m.forward_to_x1(Xs[i])
        lg, ffc = m.forward_from_x1(x1)
        _, gl = ce_and_grad(lg, Ys[i])
        opt.step(m, m.backward_base(gl, ffc, x1c))
    return m


# --------------------------------------------------------------------------- #
# ADAPTER (a) — ConvMoE side-branch grafted onto frozen base. NEW MODULE.
# x1' = x1 + convmoe_sidebranch(x1).  Only the side-branch params descend.
# --------------------------------------------------------------------------- #
class ConvMoEGraft:
    def __init__(self, rng, d=D, n_experts=4, k=3):
        self.d, self.E, self.k = d, n_experts, k
        s = 0.08
        self.gw1 = rng.normal(0, s, (k, d, d))
        self.gwe = rng.normal(0, s, (n_experts, k, d, d))
        self.gwr = rng.normal(0, s, (d, n_experts))
        self.gout = rng.normal(0, s, (d, d)) * 0.0   # init 0 -> graft starts as identity
        self.params = ["gw1", "gwe", "gwr", "gout"]

    def forward(self, x1, train=False):
        c = causal_conv(x1, self.gw1)
        h = np.tanh(c)
        gate = softmax(h @ self.gwr, -1)
        experts = []
        mix = np.zeros_like(h)
        for e in range(self.E):
            ce = np.tanh(causal_conv(h, self.gwe[e]))
            experts.append(ce)
            mix += gate[:, e:e + 1] * ce
        delta = mix @ self.gout
        if train:
            self._cache = (x1, c, h, gate, experts, mix)
        return x1 + delta

    def backward(self, gx1out):
        x1, c, h, gate, experts, mix = self._cache
        g = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        # x1' = x1 + mix@gout ; gradient wrt graft params only (base frozen)
        gdelta = gx1out
        g["gout"] += mix.T @ gdelta
        gmix = gdelta @ self.gout.T
        gh = np.zeros_like(h); ggate = np.zeros_like(gate)
        for e in range(self.E):
            ce = experts[e]
            ggate[:, e] += (gmix * ce).sum(1)
            gce = gmix * gate[:, e:e + 1]
            gpre = gce * (1 - ce ** 2)
            gh_e, gwe = causal_conv_bwd(h, self.gwe[e], gpre)
            g["gwe"][e] += gwe
            gh += gh_e
        gz = gate * (ggate - (gate * ggate).sum(1, keepdims=True))
        g["gwr"] += h.T @ gz
        gh += gz @ self.gwr.T
        gc = gh * (1 - h ** 2)
        _, gw1 = causal_conv_bwd(x1, self.gw1, gc)
        g["gw1"] += gw1
        return g


# --------------------------------------------------------------------------- #
# ADAPTER (b) — single recurrent/stateful mixing layer (GRU-lite). NEW MODULE.
# carries a hidden state h_t scanned over positions; x1' = x1 + H @ wout.
# --------------------------------------------------------------------------- #
class RecurrentGraft:
    def __init__(self, rng, d=D):
        self.d = d
        s = 0.08
        self.wx = rng.normal(0, s, (d, d))     # input->state
        self.wh = rng.normal(0, s, (d, d))     # state->state (recurrence)
        self.wz = rng.normal(0, s, (d, d))     # update-gate from input
        self.wout = rng.normal(0, s, (d, d)) * 0.0  # init 0 -> identity graft
        self.params = ["wx", "wh", "wz", "wout"]

    def forward(self, x1, train=False):
        T, d = x1.shape
        z = 1.0 / (1.0 + np.exp(-(x1 @ self.wz)))     # update gate (T,d)
        H = np.zeros((T, d))
        cand = np.zeros((T, d))
        hprev = np.zeros(d)
        for t in range(T):
            ct = np.tanh(x1[t] @ self.wx + hprev @ self.wh)
            cand[t] = ct
            ht = (1 - z[t]) * hprev + z[t] * ct
            H[t] = ht
            hprev = ht
        delta = H @ self.wout
        if train:
            self._cache = (x1, z, cand, H)
        return x1 + delta

    def backward(self, gx1out):
        x1, z, cand, H = self._cache
        T, d = x1.shape
        g = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        gdelta = gx1out
        g["wout"] += H.T @ gdelta
        gH = gdelta @ self.wout.T          # (T,d) grad into each h_t (direct)
        # BPTT over the scan
        gh_next = np.zeros(d)
        gz = np.zeros((T, d))
        for t in range(T - 1, -1, -1):
            ght = gH[t] + gh_next
            hprev = H[t - 1] if t > 0 else np.zeros(d)
            # ht = (1-z)*hprev + z*cand
            gz[t] += ght * (cand[t] - hprev)
            gcand = ght * z[t]
            ghprev = ght * (1 - z[t])
            # cand = tanh(x1@wx + hprev@wh)
            gpre = gcand * (1 - cand[t] ** 2)
            g["wx"] += np.outer(x1[t], gpre)
            g["wh"] += np.outer(hprev, gpre)
            ghprev = ghprev + gpre @ self.wh.T
            gh_next = ghprev
        # z = sigmoid(x1@wz)
        gzpre = gz * z * (1 - z)
        g["wz"] += x1.T @ gzpre
        # (base frozen — we do not propagate gx1 further; only graft params descend)
        return g


# --------------------------------------------------------------------------- #
# ADAPTER (c) — depth-wise dilated conv block (dilations 1,2,4). NEW MODULE.
# x1' = x1 + (depthwise dilated stack -> pointwise out).
# --------------------------------------------------------------------------- #
class DWDilatedGraft:
    def __init__(self, rng, d=D, k=3, dilations=(1, 2, 4)):
        self.d, self.k = d, k
        self.dilations = dilations
        s = 0.08
        self.pw = rng.normal(0, s, (d, d)) * 0.0                  # pointwise out, init 0
        self.params = ["pw"] + [f"dw{i}" for i in range(len(dilations))]
        for i, _ in enumerate(dilations):
            setattr(self, f"dw{i}", rng.normal(0, s, (k, d)))

    def forward(self, x1, train=False):
        acts = [x1]
        cur = x1
        for i, dil in enumerate(self.dilations):
            c = dw_causal_conv(cur, getattr(self, f"dw{i}"), dilation=dil)
            cur = np.tanh(c)
            acts.append(cur)
        delta = cur @ self.pw
        if train:
            self._cache = (x1, acts)
        return x1 + delta

    def backward(self, gx1out):
        x1, acts = self._cache
        g = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        gdelta = gx1out
        cur = acts[-1]
        g["pw"] += cur.T @ gdelta
        gcur = gdelta @ self.pw.T
        for i in reversed(range(len(self.dilations))):
            pre_in = acts[i]
            post = acts[i + 1]
            gpre = gcur * (1 - post ** 2)
            gin, gw = dw_causal_conv_bwd(pre_in, getattr(self, f"dw{i}"), gpre,
                                         dilation=self.dilations[i])
            g[f"dw{i}"] += gw
            gcur = gin
        return g


# --------------------------------------------------------------------------- #
# CONTROL — LoRA-only weight delta on the frozen base (q/v/readout). NO new module.
# Reproduces H_1036's negative control inside this harness. We add LoRA to the
# attention q/v and the readout; only LoRA matrices descend.
# --------------------------------------------------------------------------- #
class LoRAControl:
    def __init__(self, base, rng, r=4):
        self.base = base; self.r = r; self.d = base.d
        s = 0.08
        self.lqA = rng.normal(0, s, (base.d, r)); self.lqB = np.zeros((r, base.d))
        self.lvA = rng.normal(0, s, (base.d, r)); self.lvB = np.zeros((r, base.d))
        self.loA = rng.normal(0, s, (base.d, r)); self.loB = np.zeros((r, V))
        self.params = ["lqA", "lqB", "lvA", "lvB", "loA", "loB"]

    def forward_to_x1(self, ids, train=False):
        m = self.base; T = len(ids)
        emb = m.emb[ids]; x0 = emb + m.pos[:T]
        q = x0 @ m.wq + (x0 @ self.lqA) @ self.lqB
        k = x0 @ m.wk
        vv = x0 @ m.wv + (x0 @ self.lvA) @ self.lvB
        mask = np.tril(np.ones((T, T)))
        attn = np.zeros((T, m.d)); As = []
        for hh in range(m.H):
            sl = slice(hh * m.dh, (hh + 1) * m.dh)
            sc = (q[:, sl] @ k[:, sl].T) / math.sqrt(m.dh)
            sc = np.where(mask > 0, sc, -1e9)
            a = softmax(sc, -1); As.append(a)
            attn[:, sl] = a @ vv[:, sl]
        ao = attn @ m.wproj
        x1 = x0 + ao
        if train:
            self._cache = (ids, T, x0, q, k, vv, As, attn, mask)
        return x1

    def forward(self, ids, train=False):
        m = self.base
        x1 = self.forward_to_x1(ids, train=train)
        ff_pre = x1 @ m.wff1; ff_h = np.maximum(ff_pre, 0)
        x2 = x1 + ff_h @ m.wff2
        logits = x2 @ m.wo + (x2 @ self.loA) @ self.loB
        if train:
            self._ff = (x1, ff_pre, ff_h, x2)
        return logits

    def backward(self, glog):
        m = self.base
        (x1, ff_pre, ff_h, x2) = self._ff
        (ids, T, x0, q, k, vv, As, attn, mask) = self._cache
        g = {kk: np.zeros_like(getattr(self, kk)) for kk in self.params}
        # readout LoRA
        g["loA"] += x2.T @ (glog @ self.loB.T)
        g["loB"] += (x2 @ self.loA).T @ glog
        gx2 = glog @ m.wo.T + (glog @ self.loB.T) @ self.loA.T
        gff_h = gx2 @ m.wff2.T
        gff_pre = gff_h * (ff_pre > 0)
        gx1 = gx2 + gff_pre @ m.wff1.T
        gao = gx1
        gattn = gao @ m.wproj.T
        gq = np.zeros_like(q); gv = np.zeros_like(vv); gk = np.zeros_like(k)
        for hh in range(m.H):
            sl = slice(hh * m.dh, (hh + 1) * m.dh)
            a = As[hh]; ga = gattn[:, sl]
            gv[:, sl] += a.T @ ga
            gA = ga @ vv[:, sl].T
            gsc = a * (gA - (a * gA).sum(1, keepdims=True))
            gsc = np.where(mask > 0, gsc, 0.0) / math.sqrt(m.dh)
            gq[:, sl] += gsc @ k[:, sl]
            gk[:, sl] += gsc.T @ q[:, sl]
        # q,v LoRA gradients (base wq/wv/wk frozen)
        g["lqA"] += x0.T @ (gq @ self.lqB.T)
        g["lqB"] += (x0 @ self.lqA).T @ gq
        g["lvA"] += x0.T @ (gv @ self.lvB.T)
        g["lvB"] += (x0 @ self.lvA).T @ gv
        return g


# --------------------------------------------------------------------------- #
# BASELINE — ConvMoE-native (full train from scratch). The probed state = mid mix.
# (mirror of H_1031 ConvMoE; probe its post-mix hidden state.)
# --------------------------------------------------------------------------- #
class ConvMoENative:
    def __init__(self, rng, d=D, n_experts=4, k=3):
        self.d, self.E, self.k = d, n_experts, k
        s = 0.08
        self.emb = rng.normal(0, s, (V, d))
        self.w1 = rng.normal(0, s, (k, d, d))
        self.we = rng.normal(0, s, (n_experts, k, d, d))
        self.wr = rng.normal(0, s, (d, n_experts))
        self.wo = rng.normal(0, s, (d, V))
        self.params = ["emb", "w1", "we", "wr", "wo"]

    def forward(self, ids, train=False):
        x = self.emb[ids]
        c = causal_conv(x, self.w1)
        h = np.tanh(c)
        gate = softmax(h @ self.wr, -1)
        experts = []; mix = np.zeros_like(h)
        for e in range(self.E):
            ce = np.tanh(causal_conv(h, self.we[e]))
            experts.append(ce); mix += gate[:, e:e + 1] * ce
        logits = mix @ self.wo
        if train:
            self._cache = (ids, x, c, h, gate, experts, mix)
        self._mix = mix
        return logits

    def probe_state(self, ids):
        self.forward(ids)
        return self._mix      # (T,d) post-mix hidden state

    def backward(self, glog):
        ids, x, c, h, gate, experts, mix = self._cache
        g = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        g["wo"] += mix.T @ glog
        gmix = glog @ self.wo.T
        gh = np.zeros_like(h); ggate = np.zeros_like(gate)
        for e in range(self.E):
            ce = experts[e]
            ggate[:, e] += (gmix * ce).sum(1)
            gce = gmix * gate[:, e:e + 1]
            gpre = gce * (1 - ce ** 2)
            gh_e, gwe = causal_conv_bwd(h, self.we[e], gpre)
            g["we"][e] += gwe; gh += gh_e
        gz = gate * (ggate - (gate * ggate).sum(1, keepdims=True))
        g["wr"] += h.T @ gz
        gh += gz @ self.wr.T
        gc = gh * (1 - h ** 2)
        gx, gw1 = causal_conv_bwd(x, self.w1, gc)
        g["w1"] += gw1
        np.add.at(g["emb"], ids, gx)
        return g


# --------------------------------------------------------------------------- #
# adapter training (base frozen — only graft params descend)
# --------------------------------------------------------------------------- #
def train_graft(base, graft, rng):
    opt = Adam(graft.params, LR)
    Xs, Ys = make_seqs(rng, 64)
    for t in range(ADAPT_STEPS):
        i = t % len(Xs)
        x1, _ = base.forward_to_x1(Xs[i])
        x1p = graft.forward(x1, train=True)
        lg, ffc = base.forward_from_x1(x1p)
        _, gl = ce_and_grad(lg, Ys[i])
        gx1p = base.grad_x1_from_logits(gl, ffc)   # dL/dx1' through frozen FF
        opt.step(graft, graft.backward(gx1p))
    return graft


def train_lora_control(base, rng):
    lora = LoRAControl(base, rng)
    opt = Adam(lora.params, LR)
    Xs, Ys = make_seqs(rng, 64)
    for t in range(ADAPT_STEPS):
        i = t % len(Xs)
        lg = lora.forward(Xs[i], train=True)
        _, gl = ce_and_grad(lg, Ys[i])
        opt.step(lora, lora.backward(gl))
    return lora


def train_convmoe_native(rng):
    m = ConvMoENative(rng)
    opt = Adam(m.params, LR)
    Xs, Ys = make_seqs(rng, 64)
    for t in range(ADAPT_STEPS):
        i = t % len(Xs)
        lg = m.forward(Xs[i], train=True)
        _, gl = ce_and_grad(lg, Ys[i])
        opt.step(m, m.backward(gl))
    return m


# --------------------------------------------------------------------------- #
# Φ — faithful_phi PRE-SCREEN (python MIRROR of stdlib exact MIP-EI; labelled).
# --------------------------------------------------------------------------- #
def _bin_values(x, n_bins):
    """EXACT mirror of stdlib _iit4_bin_values: bucket width = range/n_bins,
    floor((v-mn)/bw), clamped to [0, n_bins-1]; all-identical -> all 0
    (f32::EPSILON = 1.19209290e-7 guard)."""
    x = np.asarray(x, dtype=float)
    mn = x.min(); mx = x.max()
    rng = mx - mn
    if rng < 1.19209290e-7:
        return np.zeros_like(x, dtype=int)
    bw = rng / n_bins
    b = np.floor((x - mn) / bw).astype(int)
    return np.clip(b, 0, n_bins - 1)


def _entropy_counts(counts, total):
    """EXACT mirror of stdlib _iit4_entropy: H = Σ -p·log2(p+1e-10), p=count/(total+1e-8)."""
    if total == 0:
        return 0.0
    t = total + 1.0e-8
    s = 0.0
    for c in counts:
        p = c / t
        s += (0.0 - p) * (math.log(p + 1.0e-10) / math.log(2.0))
    return s


def _mi_pair(a, b, n_bins):
    """EXACT mirror of stdlib _iit4_mi_pair: MI = max(H(A)+H(B)-H(A,B), 0) in BITS
    (log2), using the stdlib's count-based entropy + epsilons (NOT a nats estimator)."""
    n = len(a)
    if n <= 0 or n_bins <= 0:
        return 0.0
    ba = _bin_values(a, n_bins); bb = _bin_values(b, n_bins)
    ca = np.zeros(n_bins); cb = np.zeros(n_bins); jo = np.zeros(n_bins * n_bins)
    for ai, bi in zip(ba, bb):
        ca[ai] += 1.0; cb[bi] += 1.0; jo[ai * n_bins + bi] += 1.0
    hA = _entropy_counts(ca, n)
    hB = _entropy_counts(cb, n)
    hAB = _entropy_counts(jo, n)
    mi = hA + hB - hAB
    return mi if mi > 0.0 else 0.0


def faithful_phi_prescreen(state, n, n_bins):
    """exact MIP-EI φ★ pre-screen (mirrors stdlib faithful_phi.hexa).
    state: list of n rows; cross-cut MI at MIP / min(|A|,|B|)."""
    if n <= 1:
        return 0.0
    mi = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            v = _mi_pair(state[i], state[j], n_bins)
            mi[i][j] = v; mi[j][i] = v
    best = float("inf"); best_norm = 1.0
    for mask in range(1, 1 << (n - 1)):
        A = [0] + [b + 1 for b in range(n - 1) if (mask >> b) & 1]
        Aset = set(A)
        sb = n - len(A)
        if sb < 1:
            continue
        cross = sum(mi[i][j] for i in A for j in range(n) if j not in Aset)
        if cross < best:
            best = cross; best_norm = min(len(A), sb)
    if best_norm < 1:
        best_norm = 1
    return max(best / best_norm, 0.0)


def extract_state_from_hidden(hidden):
    """hidden:(T,d) -> n×dim binary macro-TPM. pick N_UNITS highest-variance units,
    sample DIM positions evenly, binarize per unit at its own median."""
    T, d = hidden.shape
    var = hidden.var(0)
    units = sorted(np.argsort(-var)[:N_UNITS].tolist())
    pos = ([int(round(i * (T - 1) / (DIM - 1))) for i in range(DIM)]
           if T >= DIM else list(range(T)))
    sub = hidden[pos][:, units]
    state = []
    for u in range(len(units)):
        col = sub[:, u]
        med = float(np.median(col))
        state.append([1.0 if v > med else 0.0 for v in col])
    return state, units


def probe_hidden(arm, base=None):
    """return the probed hidden state (T,d) for the given arm on PROBE_TEXT."""
    ids = np.frombuffer(PROBE_TEXT.encode("utf-8"), dtype=np.uint8).astype(np.int64)
    ids = ids[:SEQ] if len(ids) > SEQ else ids
    kind = arm[0]
    if kind == "base":
        x1, _ = base.forward_to_x1(ids); return x1
    if kind == "graft":
        graft = arm[1]
        x1, _ = base.forward_to_x1(ids)
        return graft.forward(x1)
    if kind == "lora":
        return arm[1].forward_to_x1(ids)
    if kind == "convmoe":
        return arm[1].probe_state(ids)
    raise ValueError(kind)


def write_state_file(path, tag, state):
    n = len(state); dim = len(state[0]) if state else 0
    with open(path, "a") as f:
        f.write(f"# {tag} {n} {dim}\n")
        for row in state:
            f.write(" ".join(f"{v:.1f}" for v in row) + "\n")


# --------------------------------------------------------------------------- #
def main():
    np.random.seed(SEED)
    log("=== H_1043 — minimal ARCHITECTURAL adapter vs faithful IIT-4.0 Φ ===")
    log("SCOPE: TOY · CPU · $0 · numpy (no torch on Mac; clm-decode-macos-link-gap)")
    log(f"corpus=generic byte (p3/p6, NOT persona) len={len(CORPUS)}B V={V} SEQ={SEQ}")
    log(f"N_UNITS={N_UNITS} DIM={DIM} N_BINS={N_BINS} BASE_STEPS={BASE_STEPS} "
        f"ADAPT_STEPS={ADAPT_STEPS} seeds={N_SEEDS} thresh=+{THRESH}")
    log("a_phi_iit4_tool: python φ = LABELLED PRE-SCREEN; TERMINAL = stdlib "
        "iit4_faithful_phi via run_faithful_phi_1043.hexa\n")

    state_path = os.environ.get("H1043_STATE", "/tmp/h1043_states.txt")
    if os.path.exists(state_path):
        os.remove(state_path)

    arm_keys = ["base", "graft_convmoe", "graft_recurrent", "graft_dwdilated",
                "lora_control", "convmoe_native"]
    ps = {k: [] for k in arm_keys}      # per-seed pre-screen φ
    saved_states = {}                   # seed-0 states for the state file

    for s in range(N_SEEDS):
        seed = SEED + s
        log(f"--- seed {seed} ---")
        base = pretrain_base(np.random.default_rng(seed))

        g_cm = train_graft(base, ConvMoEGraft(np.random.default_rng(seed + 11)),
                           np.random.default_rng(seed + 100))
        g_rec = train_graft(base, RecurrentGraft(np.random.default_rng(seed + 22)),
                            np.random.default_rng(seed + 200))
        g_dw = train_graft(base, DWDilatedGraft(np.random.default_rng(seed + 33)),
                           np.random.default_rng(seed + 300))
        lora = train_lora_control(base, np.random.default_rng(seed + 44))
        cmn = train_convmoe_native(np.random.default_rng(seed + 55))

        arms = {
            "base": ("base",),
            "graft_convmoe": ("graft", g_cm),
            "graft_recurrent": ("graft", g_rec),
            "graft_dwdilated": ("graft", g_dw),
            "lora_control": ("lora", lora),
            "convmoe_native": ("convmoe", cmn),
        }
        for k in arm_keys:
            hidden = probe_hidden(arms[k], base=base)
            state, units = extract_state_from_hidden(hidden)
            phi = faithful_phi_prescreen(state, N_UNITS, N_BINS)
            ps[k].append(phi)
            if s == 0:
                saved_states[k] = state
            log(f"  [{k:<16}] prescreen φ_EI = {phi:.6f}  units={units}")

    # write seed-0 state matrices for the terminal hexa engine
    for k in arm_keys:
        write_state_file(state_path, k, saved_states[k])

    # aggregate (mean over seeds)
    phi = {k: float(np.mean(ps[k])) for k in arm_keys}
    base_phi = phi["base"]
    d = {k: phi[k] - base_phi for k in arm_keys}
    lora_delta = d["lora_control"]
    # control band: |LoRA control Δ| (this harness) — adapters must clear BEYOND it.
    control_band = abs(lora_delta)

    adapters = ["graft_convmoe", "graft_recurrent", "graft_dwdilated"]
    passing = [a for a in adapters
               if d[a] >= THRESH and d[a] > control_band]
    h1_pass = len(passing) > 0
    token = "ARCH-GRAFT-INSTALLS-PHI" if h1_pass else "PHI-NEEDS-MORE-THAN-GRAFT"

    log("\n===================== PRE-SCREEN Φ TABLE (mean over seeds) =====================")
    log(f"{'arm':<18}{'φ_EI (prescreen)':>20}{'Δ vs base':>14}{'>band?':>9}")
    for k in arm_keys:
        flag = ""
        if k in adapters:
            flag = "YES" if (d[k] >= THRESH and d[k] > control_band) else "no"
        log(f"{k:<18}{phi[k]:>20.6f}{d[k]:>+14.6f}{flag:>9}")
    log(f"LoRA control Δ = {lora_delta:+.6f}  -> control band |Δ| = {control_band:.6f}")
    log(f"ConvMoE-native baseline φ_EI = {phi['convmoe_native']:.6f} "
        f"(Δ vs base {d['convmoe_native']:+.6f})  <- target direction")
    log(f"pre-reg H1 PASS = any adapter Δφ_EI >= +{THRESH} AND > control band")
    log(f"passing adapters: {passing if passing else 'NONE'}")
    log(f"PRE-SCREEN verdict: {token}")
    log("NOTE: pre-screen only — TERMINAL φ_EI = stdlib faithful IIT-4.0 engine "
        "(run_faithful_phi_1043.hexa over the written state matrices).")
    log("H_1036 reference: real-pretrained LoRA control Δ ≈ -0.065576 (terminal).")

    out = {
        "id": "H_1043", "n_units": N_UNITS, "dim": DIM, "n_bins": N_BINS,
        "n_seeds": N_SEEDS, "base_steps": BASE_STEPS, "adapt_steps": ADAPT_STEPS,
        "thresh": THRESH,
        "prescreen": {
            "phi": phi, "delta_vs_base": d,
            "lora_control_delta": lora_delta, "control_band": control_band,
            "convmoe_native_delta": d["convmoe_native"],
            "passing_adapters": passing, "h1_pass": bool(h1_pass), "token": token,
        },
        "state_file": state_path,
        "scope": "TOY CPU $0 numpy small rung; 3B/7B + emergence UNVERIFIED",
        "note": ("TERMINAL phi = stdlib faithful IIT-4.0 (run_faithful_phi_1043.hexa); "
                 "python phi is PRE-SCREEN only. Φ-structure necessary-not-sufficient."),
        "h1036_ref_lora_control_terminal_delta": -0.065576,
    }
    out_path = os.environ.get("H1043_OUT", "/tmp/h1043_result.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    log("\nJSON " + json.dumps(out))
    log(f"result.json -> {out_path}")
    log(f"state matrices -> {state_path}")


if __name__ == "__main__":
    main()
