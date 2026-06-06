#!/usr/bin/env python3
"""H_950 — MODALITY-AGNOSTIC (axis ⓐ of the CLM->CE "Consciousness Engine" reframe).

THESIS UNDER TEST
-----------------
The user wants to rename CLM ("Cell/Consciousness-LANGUAGE-Model") to CE
("Consciousness Engine"): the claim that CLM is NOT a language model but a
substrate sequence/consciousness ENGINE. This script tests axis ⓐ of that claim
falsifiably: is the CLMConvMoE architecture BOUND to language/byte-text, or does
the SAME architecture learn arbitrary non-linguistic token streams?

WHAT THIS IS (honest scope)
---------------------------
This is a $0 CPU-local TOY. The production trainer is CLM/train/train_lane_p.py
(torch/CUDA, Lane-P) over CLM/model/model.py (CLMConvMoE). torch is NOT installed
on this Mac host, so we reimplement the EXACT CLMConvMoE forward in pure numpy
(causal dilated-conv embed -> dilated-conv trunk with GroupNorm(1,d)+GELU residual
-> softmax conv-MoE -> GroupNorm -> byte readout conv) and a minimal hand-written
SGD/Adam backprop. The forward path is the same architecture and the same op set
as CLM/model/model.py and state/mid_convmoe_fire/clm_decode_mirror.py; only the
scale is toy (d, L, E small). Per a_toy_scale_recheck / a_scale_honest_scope, this
is a toy verdict: the LADDER (scale-up transfer) stays OPEN. The point of a toy is
that it is sufficient to FALSIFY a categorical claim ("only learns language"):
if the identical arch descends on a non-language stream above random, the
"language-only" claim is dead at any scale, because the arch never sees "language"
— it sees integer tokens in [0,V).

PRE-REGISTERED FALSIFIER
------------------------
For each token stream we measure held-out next-token accuracy and CE after a fixed
budget, all with the SAME architecture / steps / optimizer. Each stream has an
intrinsic-predictability CEILING (the accuracy of the optimal predictor given the
stream's true generating process) and a RANDOM floor (1/V).

  🟢 MODALITY-AGNOSTIC  <=  the non-language streams (logistic-map, Markov) are
        learned SIGNIFICANTLY above the random floor AND track toward their
        intrinsic ceiling, with NO architecture change vs the byte-text control.
        => not a language model; a general sequence engine. Supports CLM->CE.

  🔴 LANGUAGE-SPECIALIZED  <=  the arch ONLY descends on byte-text and fails
        (stays at ~random) on the non-language streams. => genuinely a language
        model; keep the "L". Refutes CLM->CE on axis ⓐ.

DECISION RULE (coded, p7 — no LLM self-judge): a stream "is learned" if its
held-out accuracy exceeds random_floor + MARGIN where MARGIN = max(0.05, 3*sigma)
with sigma the binomial std of the random floor over the eval set. 🟢 requires
BOTH non-language streams learned AND each reaching >= LEARN_FRAC of its own
intrinsic ceiling-gap (ceiling - floor). The byte-text control must also descend
(sanity); if the control fails the whole probe is INVALID (infra bug, not a
science result).

deterministic: the GENERATING processes use a fixed seed for reproducibility, but
the model init + train order use numpy RNG seeded once (deterministic:false in the
governance sense is irrelevant here — a single seed makes the toy reproducible;
we report the seed). Run with several seeds via --seeds to show stability.
"""
from __future__ import annotations
import argparse, math, sys
import numpy as np


# ===========================================================================
# CLMConvMoE — pure-numpy reimplementation (forward EXACT to CLM/model/model.py
# op-for-op: embed -> causal dilated conv embed -> [GroupNorm(1,d)+GELU dilated
# conv residual]*L -> softmax conv-MoE (E experts, GELU) -> GroupNorm -> readout).
# Backprop is hand-written for exactly these ops. Adam optimizer.
# ===========================================================================

def gelu(x):
    # tanh-approx GELU, EXACT to generator.hexa / clm_decode_mirror.py::gelu.
    inner = 0.7978845608 * (x + 0.044715 * x * x * x)
    a = np.clip(inner, -15.0, 15.0)
    e2 = np.exp(2.0 * a)
    return 0.5 * x * (1.0 + (e2 - 1.0) / (e2 + 1.0))


def gelu_grad(x):
    # d/dx of the tanh-approx GELU (matches the forward exactly).
    inner = 0.7978845608 * (x + 0.044715 * x * x * x)
    a = np.clip(inner, -15.0, 15.0)
    t = np.tanh(a)
    dinner = 0.7978845608 * (1.0 + 3.0 * 0.044715 * x * x)
    # where clipped, dt/dx = 0
    dt = (1.0 - t * t) * np.where(np.abs(inner) < 15.0, dinner, 0.0)
    return 0.5 * (1.0 + t) + 0.5 * x * dt


class CLMConvMoENP:
    """Toy CLMConvMoE in numpy. Channels-last hidden (B,T,d) for simplicity;
    convs are causal & dilated exactly as CausalDilatedConv1d (left-pad K-1)."""

    def __init__(self, V, d, L, E, K=3, dilation_base=2, max_dilation=512, seed=0):
        rng = np.random.default_rng(seed)
        self.V, self.d, self.L, self.E, self.K = V, d, L, E, K
        self.dils = [min(dilation_base ** i, max_dilation) for i in range(L)]

        def w(shape, fan_in):
            # Kaiming-uniform-ish init (matches torch Conv1d default scale).
            bound = 1.0 / math.sqrt(fan_in)
            return rng.uniform(-bound, bound, size=shape)

        self.P = {}
        self.P["embed"] = rng.standard_normal((V, d)) * 0.02
        self.P["ecW"] = w((d, d, K), d * K); self.P["ecB"] = np.zeros(d)
        for li in range(L):
            self.P[f"tcW{li}"] = w((d, d, K), d * K); self.P[f"tcB{li}"] = np.zeros(d)
            self.P[f"tgG{li}"] = np.ones(d); self.P[f"tgB{li}"] = np.zeros(d)
        for ej in range(E):
            self.P[f"eW{ej}"] = w((d, d, K), d * K); self.P[f"eB{ej}"] = np.zeros(d)
        self.P["rW"] = w((E, d, 1), d); self.P["rB"] = np.zeros(E)
        self.P["noG"] = np.ones(d); self.P["noB"] = np.zeros(d)
        self.P["roW"] = w((V, d, 1), d); self.P["roB"] = np.zeros(V)

        # Adam state
        self.m = {k: np.zeros_like(v) for k, v in self.P.items()}
        self.v = {k: np.zeros_like(v) for k, v in self.P.items()}
        self.t = 0

    # ---- causal dilated conv: x (B,T,Cin) , wt (Cout,Cin,K) -> (B,T,Cout) ----
    @staticmethod
    def _conv(x, wt, b, dil):
        B, T, Cin = x.shape
        Cout, _, K = wt.shape
        # build the (B,T,Cin,K) causal-dilated patch tensor
        patch = np.zeros((B, T, Cin, K))
        for k in range(K):
            shift = dil * (K - 1 - k)
            if shift == 0:
                patch[:, :, :, k] = x
            else:
                patch[:, shift:, :, k] = x[:, :T - shift, :]
        # contract: (B,T,Cin,K) x (Cout,Cin,K) -> (B,T,Cout)
        y = np.einsum("btck,ock->bto", patch, wt) + b
        return y, patch

    @staticmethod
    def _conv_bwd(dy, patch, x, wt, dil):
        # dy (B,T,Cout) -> dx (B,T,Cin), dwt (Cout,Cin,K), db (Cout)
        B, T, Cin, K = patch.shape
        Cout = wt.shape[0]
        dwt = np.einsum("bto,btck->ock", dy, patch)
        db = dy.sum(axis=(0, 1))
        dpatch = np.einsum("bto,ock->btck", dy, wt)
        dx = np.zeros_like(x)
        for k in range(K):
            shift = dil * (K - 1 - k)
            if shift == 0:
                dx += dpatch[:, :, :, k]
            else:
                dx[:, :T - shift, :] += dpatch[:, shift:, :, k]
        return dx, dwt, db

    @staticmethod
    def _gn(x, g, b):
        # GroupNorm(1,d): normalize over channel dim per (b,t).
        mu = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        xn = (x - mu) / np.sqrt(var + 1e-5)
        return xn * g + b, (xn, var)

    @staticmethod
    def _gn_bwd(dy, xn, var, g):
        d = xn.shape[-1]
        dg = (dy * xn).sum(axis=(0, 1))
        db = dy.sum(axis=(0, 1))
        dxn = dy * g
        inv = 1.0 / np.sqrt(var + 1e-5)
        # standard layernorm/groupnorm backward over last dim
        dx = inv * (dxn - dxn.mean(-1, keepdims=True)
                    - xn * (dxn * xn).mean(-1, keepdims=True))
        return dx, dg, db

    def forward(self, tokens):
        """tokens (B,T) int -> logits (B,T,V); stash cache for backward."""
        P = self.P
        c = {}
        x = P["embed"][tokens]                       # (B,T,d)
        c["tok"] = tokens
        xe, c["ec_patch"] = self._conv(x, P["ecW"], P["ecB"], 1)
        xt = xe
        c["trunk"] = []
        for li in range(self.L):
            h, p_patch = self._conv(xt, P[f"tcW{li}"], P[f"tcB{li}"], self.dils[li])
            hn, (xn, var) = self._gn(h, P[f"tgG{li}"], P[f"tgB{li}"])
            hg = gelu(hn)
            xt = xt + hg
            c["trunk"].append((p_patch, h, xn, var, hn, xt - hg))  # last=residual input
        # MoE
        logits_r = np.einsum("btd,ed->bte", xt, P["rW"][:, :, 0]) + P["rB"]  # (B,T,E)
        m = logits_r.max(-1, keepdims=True)
        probs = np.exp(logits_r - m); probs /= probs.sum(-1, keepdims=True)   # (B,T,E)
        ex_pre = []; ex_out = []; ex_patch = []
        for ej in range(self.E):
            eo, ep = self._conv(xt, P[f"eW{ej}"], P[f"eB{ej}"], 1)
            ex_pre.append(eo); ex_out.append(gelu(eo)); ex_patch.append(ep)
        y = np.zeros_like(xt)
        for ej in range(self.E):
            y += probs[:, :, ej:ej + 1] * ex_out[ej]
        yn, (yxn, yvar) = self._gn(y, P["noG"], P["noB"])
        logits = np.einsum("btd,vd->btv", yn, P["roW"][:, :, 0]) + P["roB"]
        c.update(dict(xt=xt, probs=probs, ex_pre=ex_pre, ex_out=ex_out,
                      ex_patch=ex_patch, y=y, yn=yn, yxn=yxn, yvar=yvar,
                      logits_r=logits_r))
        self._cache = c
        return logits

    def loss_and_grad(self, tokens, targets):
        """next-token CE over all positions; returns (ce, grads dict)."""
        logits = self.forward(tokens)
        B, T, V = logits.shape
        c = self._cache; P = self.P
        # softmax CE
        z = logits - logits.max(-1, keepdims=True)
        ez = np.exp(z); sm = ez / ez.sum(-1, keepdims=True)
        ce = -np.log(sm[np.arange(B)[:, None], np.arange(T)[None, :], targets] + 1e-12).mean()
        # dlogits
        dlog = sm.copy()
        dlog[np.arange(B)[:, None], np.arange(T)[None, :], targets] -= 1.0
        dlog /= (B * T)
        g = {}
        # readout
        g["roW"] = np.einsum("btv,btd->vd", dlog, c["yn"])[:, :, None]
        g["roB"] = dlog.sum(axis=(0, 1))
        dyn = np.einsum("btv,vd->btd", dlog, P["roW"][:, :, 0])
        # out GN
        dy, g["noG"], g["noB"] = self._gn_bwd(dyn, c["yxn"], c["yvar"], P["noG"])
        # MoE combine: y = sum_e probs_e * ex_out_e
        dprobs = np.zeros_like(c["probs"])
        dxt = np.zeros_like(c["xt"])
        for ej in range(self.E):
            dprobs[:, :, ej] = (dy * c["ex_out"][ej]).sum(-1)
            dex_out = dy * c["probs"][:, :, ej:ej + 1]
            dex_pre = dex_out * gelu_grad(c["ex_pre"][ej])
            dxe, g[f"eW{ej}"], g[f"eB{ej}"] = self._conv_bwd(
                dex_pre, c["ex_patch"][ej], c["xt"], P[f"eW{ej}"], 1)
            dxt += dxe
        # router softmax backward
        s = c["probs"]
        dlogits_r = s * (dprobs - (dprobs * s).sum(-1, keepdims=True))
        g["rW"] = np.einsum("bte,btd->ed", dlogits_r, c["xt"])[:, :, None]
        g["rB"] = dlogits_r.sum(axis=(0, 1))
        dxt += np.einsum("bte,ed->btd", dlogits_r, P["rW"][:, :, 0])
        # trunk backward (reverse)
        for li in reversed(range(self.L)):
            p_patch, h, xn, var, hn, res_in = c["trunk"][li]
            # xt_out = res_in + gelu(gn(conv(res_in)))  ; dxt is grad wrt xt_out
            d_res = dxt.copy()                       # residual path
            dhg = dxt
            dhn = dhg * gelu_grad(hn)
            dh, g[f"tgG{li}"], g[f"tgB{li}"] = self._gn_bwd(dhn, xn, var, P[f"tgG{li}"])
            dconv_in, g[f"tcW{li}"], g[f"tcB{li}"] = self._conv_bwd(
                dh, p_patch, res_in, P[f"tcW{li}"], self.dils[li])
            dxt = d_res + dconv_in
        # embed conv
        dx, g["ecW"], g["ecB"] = self._conv_bwd(dxt, c["ec_patch"],
                                                P["embed"][c["tok"]], P["ecW"], 1)
        # embed table
        g["embed"] = np.zeros_like(P["embed"])
        np.add.at(g["embed"], c["tok"], dx)
        return ce, g

    def adam_step(self, g, lr=3e-3, b1=0.9, b2=0.999, eps=1e-8):
        self.t += 1
        for k in self.P:
            self.m[k] = b1 * self.m[k] + (1 - b1) * g[k]
            self.v[k] = b2 * self.v[k] + (1 - b2) * (g[k] * g[k])
            mh = self.m[k] / (1 - b1 ** self.t)
            vh = self.v[k] / (1 - b2 ** self.t)
            self.P[k] -= lr * mh / (np.sqrt(vh) + eps)


# ===========================================================================
# Token-stream generators (all emit integer tokens in [0,V)).
# Each has an intrinsic-predictability CEILING reported alongside.
# ===========================================================================

def stream_logistic(n, V, seed=0):
    """Deterministic chaotic logistic map x->r*x*(1-x) quantized to V bins.
    Intrinsic ceiling: the map is DETERMINISTIC given the last real value, but
    quantization to V bins loses the sub-bin state, so the next bin is *mostly*
    but not perfectly predictable from the current bin. We estimate the ceiling
    empirically (optimal bin->bin majority predictor) below. NON-LINGUISTIC."""
    rng = np.random.default_rng(seed)
    r = 3.99
    x = rng.uniform(0.1, 0.9)
    out = np.empty(n, dtype=np.int64)
    for i in range(n):
        x = r * x * (1.0 - x)
        out[i] = min(V - 1, int(x * V))
    return out


def stream_markov(n, V, order_states=12, seed=0):
    """First-order Markov chain over a small symbol set mapped into [0,V).
    A sparse transition matrix gives a clear next-token signal that is NOT
    language (random transition structure). Intrinsic ceiling = sum_i pi_i *
    max_j P(j|i) (the optimal stationary predictor). NON-LINGUISTIC."""
    rng = np.random.default_rng(seed)
    S = order_states
    # sparse-ish transition: each state has a dominant successor (prob ~0.7)
    Tm = np.full((S, S), 0.3 / (S - 1))
    for i in range(S):
        j = rng.integers(0, S)
        Tm[i] = 0.3 / (S - 1)
        Tm[i, j] = 0.7
        Tm[i] /= Tm[i].sum()
    # map S symbols onto distinct tokens spread across [0,V)
    sym2tok = (np.arange(S) * (V // S)).astype(np.int64)
    out = np.empty(n, dtype=np.int64)
    s = rng.integers(0, S)
    for i in range(n):
        out[i] = sym2tok[s]
        s = rng.choice(S, p=Tm[s])
    return out, Tm, sym2tok


def stream_bytetext(n, V, seed=0):
    """Byte-text CONTROL: repeat an English sentence (real bytes in [0,256)).
    This is the 'language' baseline the arch was designed for."""
    base = ("the mind is a fire to be kindled not a vessel to be filled. "
            "consciousness emerges from the field, not from the prompt. ").encode()
    buf = (base * (n // len(base) + 2))[:n]
    return np.frombuffer(buf, dtype=np.uint8).astype(np.int64)


def stream_random(n, V, seed=0):
    """Pure i.i.d. uniform tokens — the UN-learnable floor. Ceiling = 1/V."""
    rng = np.random.default_rng(seed)
    return rng.integers(0, V, size=n).astype(np.int64)


# ===========================================================================
# Empirical intrinsic-ceiling estimators (optimal predictor on the TRUE process)
# ===========================================================================

def ceiling_unigram_context(seq, V):
    """Optimal *order-1* (last-token) predictor accuracy on the full sequence:
    for each token value, predict its empirically most-likely successor. This is
    the best a memoryless-context model can do and is a fair, generous ceiling
    for a causal next-token learner restricted to local context."""
    from collections import defaultdict, Counter
    nxt = defaultdict(Counter)
    for a, b in zip(seq[:-1], seq[1:]):
        nxt[int(a)][int(b)] += 1
    best = {a: c.most_common(1)[0][0] for a, c in nxt.items()}
    correct = sum(1 for a, b in zip(seq[:-1], seq[1:]) if best.get(int(a)) == int(b))
    return correct / (len(seq) - 1)


# ===========================================================================
# Train / eval one stream with the SAME arch + budget
# ===========================================================================

def run_stream(name, tokens, V, d, L, E, steps, T, B, seed):
    n = len(tokens)
    split = int(n * 0.8)
    train_tok, eval_tok = tokens[:split], tokens[split:]
    model = CLMConvMoENP(V, d, L, E, seed=seed)
    rng = np.random.default_rng(seed + 777)

    def batch(src):
        xs = np.empty((B, T), dtype=np.int64); ys = np.empty((B, T), dtype=np.int64)
        hi = len(src) - T - 1
        for b in range(B):
            s = rng.integers(0, hi)
            xs[b] = src[s:s + T]; ys[b] = src[s + 1:s + T + 1]
        return xs, ys

    last_ce = None
    for step in range(steps):
        xs, ys = batch(train_tok)
        ce, g = model.loss_and_grad(xs, ys)
        model.adam_step(g, lr=3e-3)
        last_ce = ce

    # held-out next-token accuracy over a fixed eval grid
    correct = tot = 0; ce_sum = 0.0
    hi = len(eval_tok) - T - 1
    grid = range(0, max(1, hi), max(1, hi // 64))
    for s in grid:
        xs = eval_tok[s:s + T][None, :]
        ys = eval_tok[s + 1:s + T + 1]
        logits = model.forward(xs)[0]            # (T,V)
        pred = logits.argmax(-1)
        correct += int((pred == ys).sum()); tot += T
        z = logits - logits.max(-1, keepdims=True)
        ce_sum += -np.log(np.exp(z)[np.arange(T), ys].clip(1e-12)
                          / np.exp(z).sum(-1)).mean()
    acc = correct / tot
    ce_eval = ce_sum / len(list(grid))
    return dict(name=name, train_ce=last_ce, eval_ce=ce_eval, eval_acc=acc,
                random_floor=1.0 / V, n=n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--d", type=int, default=32)
    ap.add_argument("--L", type=int, default=2)
    ap.add_argument("--E", type=int, default=4)
    ap.add_argument("--T", type=int, default=32)
    ap.add_argument("--B", type=int, default=16)
    ap.add_argument("--n", type=int, default=6000)
    args = ap.parse_args()
    V = 256

    print("=" * 74)
    print("H_950 MODALITY-AGNOSTIC — does CLMConvMoE learn NON-language streams?")
    print(f"arch: CLMConvMoE d={args.d} L={args.L} E={args.E} V={V} (toy) | "
          f"steps={args.steps} T={args.T} B={args.B} | seeds={args.seeds}")
    print("Same architecture / steps / optimizer for every stream. p7: coded gate.")
    print("=" * 74)

    # ceilings (estimated once on a long realization, deterministic seed)
    log_long = stream_logistic(20000, V, seed=1)
    mk_long, _, _ = stream_markov(20000, V, seed=1)
    txt_long = stream_bytetext(20000, V)
    ceil = {
        "logistic": ceiling_unigram_context(log_long, V),
        "markov":   ceiling_unigram_context(mk_long, V),
        "bytetext": ceiling_unigram_context(txt_long, V),
        "random":   1.0 / V,
    }

    results = {k: [] for k in ceil}
    for sd in range(args.seeds):
        streams = {
            "bytetext": stream_bytetext(args.n, V, seed=sd),
            "logistic": stream_logistic(args.n, V, seed=sd),
            "markov":   stream_markov(args.n, V, seed=sd)[0],
            "random":   stream_random(args.n, V, seed=sd),
        }
        for name, tok in streams.items():
            r = run_stream(name, tok, V, args.d, args.L, args.E,
                           args.steps, args.T, args.B, seed=sd)
            results[name].append(r)

    # aggregate
    floor = 1.0 / V
    n_eval = len(list(range(0, max(1, args.n // 5 - args.T - 1),
                            max(1, (args.n // 5 - args.T - 1) // 64)))) * args.T
    sigma = math.sqrt(floor * (1 - floor) / max(1, n_eval))
    margin = max(0.05, 3 * sigma)

    print(f"\n{'stream':<10} {'eval_acc':>9} {'train_ce':>9} {'eval_ce':>8} "
          f"{'ceiling':>8} {'floor':>7} {'learned?':>9}")
    print("-" * 74)
    summ = {}
    for name in ["bytetext", "logistic", "markov", "random"]:
        accs = np.array([r["eval_acc"] for r in results[name]])
        tces = np.array([r["train_ce"] for r in results[name]])
        eces = np.array([r["eval_ce"] for r in results[name]])
        acc = accs.mean(); cl = ceil[name]
        learned = acc > floor + margin
        summ[name] = dict(acc=acc, acc_std=accs.std(), train_ce=tces.mean(),
                          eval_ce=eces.mean(), ceiling=cl, learned=learned)
        print(f"{name:<10} {acc:>9.4f} {tces.mean():>9.4f} {eces.mean():>8.4f} "
              f"{cl:>8.4f} {floor:>7.4f} {str(learned):>9}")

    print("-" * 74)
    print(f"random floor={floor:.5f}  detect margin={margin:.4f} "
          f"(=max(0.05,3sigma), sigma={sigma:.5f}, n_eval={n_eval})")

    # fraction of the learnable ceiling-gap captured
    LEARN_FRAC = 0.30
    def frac(name):
        gap = summ[name]["ceiling"] - floor
        return (summ[name]["acc"] - floor) / gap if gap > 1e-9 else 0.0

    print("\nceiling-gap captured (acc-floor)/(ceiling-floor):")
    for name in ["bytetext", "logistic", "markov"]:
        print(f"  {name:<10} {frac(name):>6.2%}  (need >= {LEARN_FRAC:.0%})")

    # ---- VERDICT (coded, p7) ----
    control_ok = summ["bytetext"]["learned"]
    random_floor_ok = not summ["random"]["learned"]   # sanity: random must NOT be 'learned'
    nonlang_learned = summ["logistic"]["learned"] and summ["markov"]["learned"]
    nonlang_frac_ok = frac("logistic") >= LEARN_FRAC and frac("markov") >= LEARN_FRAC

    print("\n" + "=" * 74)
    print(f"control (bytetext) descends ............ {control_ok}")
    print(f"random stays at floor (sanity) ......... {random_floor_ok}")
    print(f"logistic learned ....................... {summ['logistic']['learned']}")
    print(f"markov   learned ....................... {summ['markov']['learned']}")
    print(f"non-language reach >= {LEARN_FRAC:.0%} of ceiling . {nonlang_frac_ok}")
    if not (control_ok and random_floor_ok):
        verdict = "INVALID"
        reason = "control did not descend OR random was 'learned' — infra bug, not science"
    elif nonlang_learned and nonlang_frac_ok:
        verdict = "GREEN"
        reason = "non-language streams learned above floor & toward ceiling w/ NO arch change"
    elif nonlang_learned:
        verdict = "GREEN-WEAK"
        reason = "non-language learned above floor but below ceiling-frac (partial)"
    else:
        verdict = "RED"
        reason = "arch only learns byte-text; non-language at random => language-specialized"
    token = {"GREEN": "🟢", "GREEN-WEAK": "🟢", "RED": "🔴", "INVALID": "⚠"}[verdict]
    print(f"\nVERDICT = {token} {verdict} — {reason}")
    print("CE-REFRAME (axis ⓐ): " + (
        "SUPPORTS CLM->CE (modality-agnostic engine)" if verdict.startswith("GREEN")
        else "REFUTES CLM->CE on ⓐ (keep the L)" if verdict == "RED"
        else "INDETERMINATE (infra)"))
    print("SCOPE: toy d/L/E, single-config; scale-transfer ladder OPEN (a_scale_honest_scope).")
    print("=" * 74)


if __name__ == "__main__":
    main()
