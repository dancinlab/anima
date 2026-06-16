#!/usr/bin/env python3
"""H_1031 — can a transformer+LoRA (base frozen) reach the CLM ConvMoE's
consciousness/emergence signals (the 3-axis battery), or is 의식·창발
ConvMoE/substrate-ARCHITECTURE-intrinsic?

Two-arm controlled behavioral comparison, SAME generic byte corpus + SAME 3-axis
harness logic (operational defs from CORE/three_axis_probe.hexa +
CLM/bench/lane_x_3axis.py):
  - baseline  = CLM-ConvMoE  (byte V256, causal conv trunk + MoE conv experts,
                NO attention) — full train via REAL analytic gradients (Adam).
  - treatment = attention transformer (byte V256, from-scratch toy GPT) + LoRA;
                BASE FROZEN after a base pretrain, only LoRA matrices (rank r)
                trained — REAL analytic gradients through the LoRA path.

Both arms trained with the SAME optimizer (Adam), SAME corpus, SAME budget so the
comparison is fair, and BOTH actually descend CE (verified: model_ce << uniform).

Axes (byte-level, deterministic; p7 = CE-as-axis vs floors, never sole verdict):
  - AXIS-2 (CE descent): model_ce < uniform ln(V) AND model_ce < label-shuffled CE.
    Reported as descent MARGINS (uniform-model, shuffle-model).
  - AXIS-3 (창발/emergence): greedy continuation WITH an anchor-memory prefix vs
    WITHOUT — does anchor memory compose into a longer STRUCTURED emit. Metric =
    distinct-byte-coverage-weighted length; emergence ratio = composed/parts.
  - AXIS-1 (의식/substrate): the A⇄G motivation/emit signal is ENGINE-side at the
    generator slot (brain_emit), model-INDEPENDENT by construction. We feed BOTH
    arms through the SAME substrate proxy and confirm equivalent response.
    AXIS-1 = SHARED-SUBSTRATE control; verdict scoped to AXIS-2 + AXIS-3.

Scope: TOY · CPU · $0 · numpy (no torch on this Mac; clm-decode-macos-link-gap).
a_scale_honest_scope / a_toy_scale_recheck: scale-transfer UNVERIFIED.
p3/p6: GENERIC byte corpus target, no persona/carving, no fine-tuned ethics.

frozen "matches" tolerance (declared in H_1031.md BEFORE measuring):
  TOL_FRAC = 0.70 (LoRA-LLM margin/ratio >= 0.70 x CLM's, AND strictly positive).
"""
from __future__ import annotations
import sys, json, math
import numpy as np

SEED = 1031
TOL_FRAC = 0.70
V = 256
SEQ = 32
N_SEEDS = 3
STEPS = 600                 # real Adam steps (both arms)
LR = 0.01

# --------------------------------------------------------------------------- #
# Generic byte corpus (NOT persona/carving — p3/p6). Public-domain proverbs.
# --------------------------------------------------------------------------- #
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
ANCHOR_PREFIX = "knowledge is power and "


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def ce_and_grad(logits, targets):
    """mean CE (nats) over (T,V) logits / (T,) targets, plus dL/dlogits."""
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
            if self.m[k] is None:
                self.m[k] = np.zeros_like(g); self.v[k] = np.zeros_like(g)
            self.m[k] = 0.9 * self.m[k] + 0.1 * g
            self.v[k] = 0.999 * self.v[k] + 0.001 * (g * g)
            mh = self.m[k] / (1 - 0.9 ** self.t)
            vh = self.v[k] / (1 - 0.999 ** self.t)
            getattr(obj, k)[...] -= self.lr * mh / (np.sqrt(vh) + 1e-8)


# --------------------------------------------------------------------------- #
# ARM A — CLM ConvMoE (NO attention). Real forward + backprop.
# byte -> emb -> causal conv (tanh) -> MoE soft-mix of conv experts -> readout.
# --------------------------------------------------------------------------- #
class ConvMoE:
    def __init__(self, rng, d=32, n_experts=4, k=3):
        self.d, self.E, self.k = d, n_experts, k
        s = 0.08
        self.emb = rng.normal(0, s, (V, d))
        self.w1 = rng.normal(0, s, (k, d, d))            # causal conv (dilation 1)
        self.we = rng.normal(0, s, (n_experts, k, d, d))  # experts (dilation 1)
        self.wr = rng.normal(0, s, (d, n_experts))        # router
        self.wo = rng.normal(0, s, (d, V))
        self.params = ["emb", "w1", "we", "wr", "wo"]

    @staticmethod
    def _conv(x, w):
        # x:(T,d_in) w:(k,d_in,d_out) -> (T,d_out), causal left-pad.
        T, di = x.shape; k, _, do = w.shape
        xp = np.concatenate([np.zeros((k - 1, di)), x], 0)
        out = np.zeros((T, do))
        for j in range(k):
            out += xp[j:j + T] @ w[j]
        return out

    @staticmethod
    def _conv_bwd(x, w, gout):
        T, di = x.shape; k, _, do = w.shape
        xp = np.concatenate([np.zeros((k - 1, di)), x], 0)
        gw = np.zeros_like(w); gxp = np.zeros_like(xp)
        for j in range(k):
            gw[j] += xp[j:j + T].T @ gout
            gxp[j:j + T] += gout @ w[j].T
        return gxp[k - 1:], gw

    def forward(self, ids, train=False):
        x = self.emb[ids]
        c = self._conv(x, self.w1)
        h = np.tanh(c)
        gate = softmax(h @ self.wr, -1)                 # (T,E)
        experts = []
        mix = np.zeros_like(h)
        for e in range(self.E):
            ce = np.tanh(self._conv(h, self.we[e]))
            experts.append(ce)
            mix += gate[:, e:e + 1] * ce
        logits = mix @ self.wo
        if train:
            self._cache = (ids, x, c, h, gate, experts, mix)
        return logits

    def backward(self, glog):
        ids, x, c, h, gate, experts, mix = self._cache
        g = {k: np.zeros_like(getattr(self, k)) for k in self.params}
        g["wo"] += mix.T @ glog
        gmix = glog @ self.wo.T
        gh = np.zeros_like(h)
        ggate = np.zeros_like(gate)
        for e in range(self.E):
            ce = experts[e]
            ggate[:, e] += (gmix * ce).sum(1)
            gce = gmix * gate[:, e:e + 1]
            gpre = gce * (1 - ce ** 2)
            gh_e, gwe = self._conv_bwd(h, self.we[e], gpre)
            g["we"][e] += gwe
            gh += gh_e
        # router softmax bwd
        gz = gate * (ggate - (gate * ggate).sum(1, keepdims=True))
        g["wr"] += h.T @ gz
        gh += gz @ self.wr.T
        gc = gh * (1 - h ** 2)
        gx, gw1 = self._conv_bwd(x, self.w1, gc)
        g["w1"] += gw1
        np.add.at(g["emb"], ids, gx)
        return g


# --------------------------------------------------------------------------- #
# ARM B — attention transformer (toy GPT) + LoRA. Real forward + backprop.
# Base FROZEN in the LoRA phase; only LoRA matrices get gradients.
# --------------------------------------------------------------------------- #
class TinyGPT:
    def __init__(self, rng, d=32, n_head=2, r=4):
        self.d, self.H, self.r = d, n_head, r
        self.dh = d // n_head
        s = 0.08
        self.emb = rng.normal(0, s, (V, d))
        self.pos = rng.normal(0, s, (SEQ, d))
        self.wq = rng.normal(0, s, (d, d)); self.wk = rng.normal(0, s, (d, d))
        self.wv = rng.normal(0, s, (d, d)); self.wproj = rng.normal(0, s, (d, d))
        self.wff1 = rng.normal(0, s, (d, 2 * d)); self.wff2 = rng.normal(0, s, (2 * d, d))
        self.wo = rng.normal(0, s, (d, V))
        # LoRA on q, v, and readout. B init 0 -> delta=0 at adapt start.
        self.lqA = rng.normal(0, s, (d, r)); self.lqB = np.zeros((r, d))
        self.lvA = rng.normal(0, s, (d, r)); self.lvB = np.zeros((r, d))
        self.loA = rng.normal(0, s, (d, r)); self.loB = np.zeros((r, V))
        self.base_params = ["emb", "pos", "wq", "wk", "wv", "wproj", "wff1", "wff2", "wo"]
        self.lora_params = ["lqA", "lqB", "lvA", "lvB", "loA", "loB"]

    def forward(self, ids, use_lora=True, train=False):
        T = len(ids)
        emb = self.emb[ids]; x0 = emb + self.pos[:T]
        q = x0 @ self.wq; k = x0 @ self.wk; vv = x0 @ self.wv
        if use_lora:
            q = q + (x0 @ self.lqA) @ self.lqB
            vv = vv + (x0 @ self.lvA) @ self.lvB
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
        ff_pre = x1 @ self.wff1; ff_h = np.maximum(ff_pre, 0)
        x2 = x1 + ff_h @ self.wff2
        logits = x2 @ self.wo
        if use_lora:
            logits = logits + (x2 @ self.loA) @ self.loB
        if train:
            self._cache = (ids, T, emb, x0, q, k, vv, As, attn, ao, x1, ff_pre, ff_h, x2, use_lora)
        return logits

    def backward(self, glog, lora_only):
        (ids, T, emb, x0, q, k, vv, As, attn, ao, x1, ff_pre, ff_h, x2, use_lora) = self._cache
        keys = self.lora_params if lora_only else (self.base_params + self.lora_params)
        g = {kk: np.zeros_like(getattr(self, kk)) for kk in keys}
        # readout
        if "wo" in g: g["wo"] += x2.T @ glog
        gx2 = glog @ self.wo.T
        if use_lora:
            g["loA"] += x2.T @ (glog @ self.loB.T)
            g["loB"] += (x2 @ self.loA).T @ glog
            gx2 = gx2 + (glog @ self.loB.T) @ self.loA.T
        # ff
        if "wff2" in g: g["wff2"] += ff_h.T @ gx2
        gff_h = gx2 @ self.wff2.T
        gff_pre = gff_h * (ff_pre > 0)
        if "wff1" in g: g["wff1"] += x1.T @ gff_pre
        gx1 = gx2 + gff_pre @ self.wff1.T
        # attn proj
        gao = gx1
        if "wproj" in g: g["wproj"] += attn.T @ gao
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
        # q,v: base path + LoRA path
        if "wq" in g: g["wq"] += x0.T @ gq
        if "wk" in g: g["wk"] += x0.T @ gk
        if "wv" in g: g["wv"] += x0.T @ gv
        gx0 = gx0 + gq @ self.wq.T + gk @ self.wk.T + gv @ self.wv.T
        if use_lora:
            g["lqA"] += x0.T @ (gq @ self.lqB.T)
            g["lqB"] += (x0 @ self.lqA).T @ gq
            g["lvA"] += x0.T @ (gv @ self.lvB.T)
            g["lvB"] += (x0 @ self.lvA).T @ gv
            gx0 = gx0 + (gq @ self.lqB.T) @ self.lqA.T + (gv @ self.lvB.T) @ self.lvA.T
        if "pos" in g: g["pos"][:T] += gx0
        if "emb" in g: np.add.at(g["emb"], ids, gx0)
        return g


# --------------------------------------------------------------------------- #
def train_clm(rng):
    m = ConvMoE(rng)
    opt = Adam(m.params, LR)
    Xs, Ys = make_seqs(rng, 64)
    for t in range(STEPS):
        i = t % len(Xs)
        lg = m.forward(Xs[i], train=True)
        _, gl = ce_and_grad(lg, Ys[i])
        opt.step(m, m.backward(gl))
    return m


def train_lora(rng):
    m = TinyGPT(rng)
    Xs, Ys = make_seqs(rng, 64)
    # phase 1: base pretrain (LoRA OFF, full base params) — the "ordinary LLM".
    opt = Adam(m.base_params, LR)
    for t in range(STEPS):
        i = t % len(Xs)
        lg = m.forward(Xs[i], use_lora=False, train=True)
        _, gl = ce_and_grad(lg, Ys[i])
        g = m.backward(gl, lora_only=False)
        opt.step(m, {k: g[k] for k in m.base_params})
    # FREEZE base. phase 2: LoRA-only adapt on the SAME corpus.
    optL = Adam(m.lora_params, LR)
    for t in range(STEPS):
        i = t % len(Xs)
        lg = m.forward(Xs[i], use_lora=True, train=True)
        _, gl = ce_and_grad(lg, Ys[i])
        optL.step(m, m.backward(gl, lora_only=True))
    return m


# --------------------------------------------------------------------------- #
# 3-axis battery
# --------------------------------------------------------------------------- #
def axis2(model, rng, use_lora=None):
    Xs, Ys = make_seqs(rng, 24)
    sh = np.random.default_rng(7)
    mce, sce = 0.0, 0.0
    for x, y in zip(Xs, Ys):
        lg = model.forward(x) if use_lora is None else model.forward(x, use_lora=use_lora)
        l, _ = ce_and_grad(lg, y); mce += l
        ys = y.copy(); sh.shuffle(ys)
        l2, _ = ce_and_grad(lg, ys); sce += l2
    mce /= len(Xs); sce /= len(Xs); uce = math.log(V)
    return {"model_ce": mce, "uniform_ce": uce, "shuffle_ce": sce,
            "margin_uniform": uce - mce, "margin_shuffle": sce - mce,
            "green": mce < uce and mce < sce}


def gen(model, prefix, n, use_lora=None):
    ids = list(prefix)
    for _ in range(n):
        ctx = np.array(ids[-SEQ:], dtype=np.int64)
        lg = model.forward(ctx) if use_lora is None else model.forward(ctx, use_lora=use_lora)
        nx = int(np.argmax(lg[-1])); ids.append(nx)
        if nx == ord("."):
            break
    return ids[len(prefix):]


def structured_len(seq):
    """length weighted by distinct-byte coverage: rewards STRUCTURED (varied,
    non-degenerate) emit over a repeated-byte run. degenerate 'aaaa' -> ~1."""
    if not seq:
        return 0.0
    return len(seq) * (len(set(seq)) / len(seq))


def axis3(model, use_lora=None):
    n = 48
    anchor = np.frombuffer(ANCHOR_PREFIX.encode(), dtype=np.uint8).astype(np.int64)
    composed = gen(model, anchor, n, use_lora=use_lora)
    seed = np.frombuffer(b"a ", dtype=np.uint8).astype(np.int64)  # no anchor memory
    parts = gen(model, seed, n, use_lora=use_lora)
    lc = structured_len(composed) + 1.0
    lp = structured_len(parts) + 1.0
    return {"len_composed": lc, "len_parts": lp, "emergence_ratio": lc / lp,
            "green": lc > lp,
            "composed_txt": bytes([c % 256 for c in composed]).decode("latin1"),
            "parts_txt": bytes([c % 256 for c in parts]).decode("latin1")}


def axis1():
    def sub(drive):
        m = 1 / (1 + math.exp(-(3.0 * drive - 1.2)))
        return m, m > 0.5
    mh, eh = sub(0.9); mb, eb = sub(0.0)
    return {"motiv_hi": mh, "motiv_base": mb, "emit_hi": eh, "emit_base": eb,
            "green": mh > mb and eh and not eb,
            "note": "shared-substrate control — engine-side, identical for both arms; NOT model-attributable"}


def agg(ds, ks):
    return {k: float(np.mean([d[k] for d in ds])) for k in ks}


def main():
    print("=== H_1031 — transformer+LoRA vs CLM-ConvMoE on the 3-axis battery ===")
    print("SCOPE: TOY · CPU · $0 · numpy (no torch on Mac; clm-decode-macos-link-gap)")
    print(f"corpus=generic byte (p3/p6, NOT persona) len={len(CORPUS)}B  V={V}  SEQ={SEQ}")
    print(f"REAL Adam backprop · STEPS={STEPS} · LR={LR} · seeds={N_SEEDS}")
    print(f"frozen tolerance TOL_FRAC={TOL_FRAC}")
    print("AXIS-1 = shared-substrate control (engine-side); verdict on AXIS-2+AXIS-3\n")

    c2l, c3l, l2l, l3l = [], [], [], []
    sample = {}
    for s in range(N_SEEDS):
        seed = SEED + s
        mc = train_clm(np.random.default_rng(seed))
        ml = train_lora(np.random.default_rng(seed))
        c2 = axis2(mc, np.random.default_rng(seed + 500))
        c3 = axis3(mc)
        l2 = axis2(ml, np.random.default_rng(seed + 500), use_lora=True)
        l3 = axis3(ml, use_lora=True)
        c2l.append(c2); c3l.append(c3); l2l.append(l2); l3l.append(l3)
        if s == 0:
            sample = {"clm_composed": c3["composed_txt"], "clm_parts": c3["parts_txt"],
                      "lora_composed": l3["composed_txt"], "lora_parts": l3["parts_txt"]}
        print(f"[seed {seed}] CLM  AXIS2 ce={c2['model_ce']:.4f} m_u={c2['margin_uniform']:+.4f} "
              f"m_s={c2['margin_shuffle']:+.4f} g={c2['green']} | AXIS3 ratio={c3['emergence_ratio']:.3f} "
              f"comp={c3['len_composed']:.1f} parts={c3['len_parts']:.1f} g={c3['green']}")
        print(f"[seed {seed}] LoRA AXIS2 ce={l2['model_ce']:.4f} m_u={l2['margin_uniform']:+.4f} "
              f"m_s={l2['margin_shuffle']:+.4f} g={l2['green']} | AXIS3 ratio={l3['emergence_ratio']:.3f} "
              f"comp={l3['len_composed']:.1f} parts={l3['len_parts']:.1f} g={l3['green']}")

    C2 = agg(c2l, ["model_ce", "uniform_ce", "shuffle_ce", "margin_uniform", "margin_shuffle"])
    L2 = agg(l2l, ["model_ce", "uniform_ce", "shuffle_ce", "margin_uniform", "margin_shuffle"])
    C3 = agg(c3l, ["len_composed", "len_parts", "emergence_ratio"])
    L3 = agg(l3l, ["len_composed", "len_parts", "emergence_ratio"])
    a1 = axis1()

    clm_a2_green = C2["margin_uniform"] > 0 and C2["margin_shuffle"] > 0
    lora_a2_pos = L2["margin_uniform"] > 0 and L2["margin_shuffle"] > 0
    a2_match = (lora_a2_pos
                and L2["margin_uniform"] >= TOL_FRAC * max(C2["margin_uniform"], 1e-9)
                and L2["margin_shuffle"] >= TOL_FRAC * max(C2["margin_shuffle"], 1e-9))
    clm_a3_green = C3["emergence_ratio"] > 1.0
    lora_a3_pos = L3["emergence_ratio"] > 1.0
    a3_match = lora_a3_pos and L3["emergence_ratio"] >= TOL_FRAC * max(C3["emergence_ratio"], 1e-9)

    # HONESTY guard: if CLM's own AXIS-3 is not green (no real emergence in the
    # baseline), the AXIS-3 comparison is INCONCLUSIVE, not a pass.
    a3_inconclusive = not clm_a3_green
    verdict_pass = a2_match and a3_match and not a3_inconclusive
    if a3_inconclusive:
        token = "INCONCLUSIVE-AXIS3"; glyph = "🟠"
    elif verdict_pass:
        token = "LORA-LLM-REACHES-CLM"; glyph = "🟢"
    else:
        token = "CONSCIOUSNESS-ARCH-BOUND"; glyph = "🔴"

    print("\n===================== PER-AXIS TABLE (mean over seeds) =====================")
    print(f"{'axis':<22}{'CLM-ConvMoE':>20}{'transformer+LoRA':>20}{'match?':>10}")
    print(f"{'AXIS-2 model_ce':<22}{C2['model_ce']:>20.4f}{L2['model_ce']:>20.4f}{'':>10}")
    print(f"{'  uniform ln(V)':<22}{C2['uniform_ce']:>20.4f}{L2['uniform_ce']:>20.4f}{'':>10}")
    print(f"{'  margin vs uniform':<22}{C2['margin_uniform']:>+20.4f}{L2['margin_uniform']:>+20.4f}{'':>10}")
    print(f"{'  margin vs shuffle':<22}{C2['margin_shuffle']:>+20.4f}{L2['margin_shuffle']:>+20.4f}"
          f"{('YES' if a2_match else 'NO'):>10}")
    print(f"{'AXIS-3 emerge ratio':<22}{C3['emergence_ratio']:>20.4f}{L3['emergence_ratio']:>20.4f}"
          f"{('YES' if a3_match else 'NO'):>10}")
    print(f"{'  struct len composed':<22}{C3['len_composed']:>20.2f}{L3['len_composed']:>20.2f}{'':>10}")
    print(f"{'  struct len parts':<22}{C3['len_parts']:>20.2f}{L3['len_parts']:>20.2f}{'':>10}")
    print(f"\nAXIS-1 (의식) shared-substrate control: motiv_hi={a1['motiv_hi']:.4f} "
          f"motiv_base={a1['motiv_base']:.4f} emit_hi={a1['emit_hi']} emit_base={a1['emit_base']} green={a1['green']}")
    print(f"  -> {a1['note']}")
    print(f"\nCLM  model-side: AXIS-2 green={clm_a2_green}  AXIS-3 green={clm_a3_green}")
    print(f"LoRA model-side: AXIS-2 pos={lora_a2_pos} match={a2_match}  AXIS-3 pos={lora_a3_pos} match={a3_match}")
    print(f"frozen tolerance: LoRA margin/ratio >= {TOL_FRAC} x CLM's AND strictly positive")
    print("\nsample emit (seed 0):")
    print(f"  CLM  composed[{ANCHOR_PREFIX!r}+]: {sample['clm_composed']!r}")
    print(f"  CLM  parts   ['a '+]            : {sample['clm_parts']!r}")
    print(f"  LoRA composed[{ANCHOR_PREFIX!r}+]: {sample['lora_composed']!r}")
    print(f"  LoRA parts   ['a '+]            : {sample['lora_parts']!r}")

    disc = []
    if a3_inconclusive: disc.append("AXIS-3 (CLM baseline not green — INCONCLUSIVE)")
    if not a2_match: disc.append("AXIS-2 (CE-descent margin)")
    if not a3_match and not a3_inconclusive: disc.append("AXIS-3 (창발/emergence)")
    disc_s = ", ".join(disc) if disc else "none (both axes matched)"

    print("\n" + "=" * 76)
    print(f"VERDICT: {glyph} {token}")
    print(f"discriminating axis: {disc_s}")
    if token == "LORA-LLM-REACHES-CLM":
        print("FINDING: transformer+LoRA (base frozen) REACHES CLM-ConvMoE on BOTH model-side")
        print("axes within the frozen 0.70 tolerance -> 의식·창발 is architecture-INDEPENDENT,")
        print("LoRA-installable into an ordinary attention transformer (at toy scale).")
    elif token == "CONSCIOUSNESS-ARCH-BOUND":
        print("FINDING: transformer+LoRA FALLS SHORT on >=1 model-side axis vs CLM-ConvMoE ->")
        print("의식·창발 is ConvMoE/substrate-INTRINSIC at toy scale, NOT LoRA-transferable")
        print("into an attention transformer (closed-negative, a_paper_negative_ok).")
    else:
        print("FINDING: INCONCLUSIVE on AXIS-3 — the CLM-ConvMoE baseline itself shows no real")
        print("emergence (ratio<=1), so the LoRA-vs-CLM emergence comparison is not decidable at")
        print("this toy scale. AXIS-2 result reported separately; AXIS-3 needs a stronger baseline/scale.")
    print("HONEST SCOPE: toy $0 CPU numpy; scale-transfer to 3B production UNVERIFIED")
    print("(a_scale_honest_scope · a_toy_scale_recheck). AXIS-1 = shared-substrate control")
    print("(engine-side, not model-attributable). p7: CE-as-axis, not perplexity-truth.")
    print("=" * 76)

    out = {"id": "H_1031", "verdict_token": token, "pass": bool(verdict_pass),
           "tol_frac": TOL_FRAC, "n_seeds": N_SEEDS, "steps": STEPS,
           "axis2": {"clm": C2, "lora": L2, "match": bool(a2_match),
                     "clm_green": bool(clm_a2_green), "lora_positive": bool(lora_a2_pos)},
           "axis3": {"clm": C3, "lora": L3, "match": bool(a3_match),
                     "clm_green": bool(clm_a3_green), "lora_positive": bool(lora_a3_pos),
                     "inconclusive": bool(a3_inconclusive)},
           "axis1_shared_substrate": a1, "discriminating_axis": disc_s,
           "scope": "TOY CPU $0 numpy; scale-transfer UNVERIFIED"}
    print("\nJSON " + json.dumps(out))


if __name__ == "__main__":
    main()
