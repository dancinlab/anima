"""Minimal numpy neural LM — the $0 proxy trainer for the H_004 pilot pre-check.

NOT the pilot itself. The pilot (H_004) trains ~10M-param transformers on a GPU.
This is a deliberately tiny fixed-window neural LM that runs on CPU in minutes,
so a DIRECTIONAL Δ_proxy (oracle codec vs frozen codec) can gate the GPU spend —
the campaign's research-before-real-measurement rule. Its asymmetry is honest:
a clear oracle >> frozen gap is positive evidence the mechanism exists at minimal
scale (as MORPH-ATOM was itself drill-scale); a null is NOT decisive (could be
under-capacity), and that limit is stated wherever the number is reported.

Model: context = last C tokens, embeddings mean-pooled -> hidden (tanh) ->
softmax over vocab. Adam, cross-entropy next-token loss. Manual backprop; every
gradient is checked against finite differences in the fixtures.

Deterministic given a seed. numpy only.
"""

from __future__ import annotations

import math

import numpy as np


def _gelu(x):
    return 0.5 * x * (1.0 + np.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x ** 3)))


def _gelu_grad(x):
    c = math.sqrt(2.0 / math.pi)
    t = np.tanh(c * (x + 0.044715 * x ** 3))
    dt = (1.0 - t ** 2) * c * (1.0 + 3 * 0.044715 * x ** 2)
    return 0.5 * (1.0 + t) + 0.5 * x * dt


class NeuralLM:
    """Fixed-window neural language model with mean-pooled context."""

    def __init__(self, vocab_size: int, dim: int = 48, hidden: int = 96,
                 context: int = 8, seed: int = 0):
        self.V, self.d, self.h, self.C = vocab_size, dim, hidden, context
        rng = np.random.RandomState(seed)
        s = 1.0 / math.sqrt(dim)
        self.E = rng.normal(0, s, (vocab_size, dim))
        self.W1 = rng.normal(0, s, (dim, hidden))
        self.b1 = np.zeros(hidden)
        self.W2 = rng.normal(0, 1.0 / math.sqrt(hidden), (hidden, vocab_size))
        self.b2 = np.zeros(vocab_size)
        self._adam_init()

    def _params(self):
        return [self.E, self.W1, self.b1, self.W2, self.b2]

    def _adam_init(self):
        self._m = [np.zeros_like(p) for p in self._params()]
        self._v = [np.zeros_like(p) for p in self._params()]
        self._t = 0

    def _contexts(self, ids):
        """Turn a token-id sequence into (context_window, target) training pairs.

        Left-padded with a repeat of the first token so every position has a full
        window; this is a proxy, so the padding convention only needs to be
        consistent between arms, which it is."""
        pairs = []
        for i in range(1, len(ids)):
            start = max(0, i - self.C)
            win = ids[start:i]
            if len(win) < self.C:
                win = [win[0]] * (self.C - len(win)) + win
            pairs.append((win, ids[i]))
        return pairs

    def _forward(self, wins):
        """wins: [B, C] int -> logits [B, V], plus cache for backward."""
        emb = self.E[wins]                       # [B, C, d]
        ctx = emb.mean(axis=1)                    # [B, d]
        pre = ctx @ self.W1 + self.b1             # [B, h]
        hid = _gelu(pre)
        logits = hid @ self.W2 + self.b2          # [B, V]
        return logits, (wins, ctx, pre, hid)

    def _loss_and_grad(self, wins, targets):
        B = len(wins)
        wins = np.asarray(wins)
        targets = np.asarray(targets)
        logits, (wins, ctx, pre, hid) = self._forward(wins)
        logits -= logits.max(axis=1, keepdims=True)
        expz = np.exp(logits)
        probs = expz / expz.sum(axis=1, keepdims=True)
        loss = -np.log(probs[np.arange(B), targets] + 1e-12).mean()

        dlogits = probs
        dlogits[np.arange(B), targets] -= 1.0
        dlogits /= B                               # [B, V]
        dW2 = hid.T @ dlogits                       # [h, V]
        db2 = dlogits.sum(0)
        dhid = dlogits @ self.W2.T                  # [B, h]
        dpre = dhid * _gelu_grad(pre)
        dW1 = ctx.T @ dpre                          # [d, h]
        db1 = dpre.sum(0)
        dctx = dpre @ self.W1.T                     # [B, d]
        dE = np.zeros_like(self.E)
        demb = (dctx / self.C)                      # mean-pool spreads grad evenly
        for b in range(B):
            for c in range(self.C):
                dE[wins[b, c]] += demb[b]
        return loss, [dE, dW1, db1, dW2, db2]

    def _adam_step(self, grads, lr, b1=0.9, b2=0.999, eps=1e-8):
        self._t += 1
        for i, (p, g) in enumerate(zip(self._params(), grads)):
            self._m[i] = b1 * self._m[i] + (1 - b1) * g
            self._v[i] = b2 * self._v[i] + (1 - b2) * (g * g)
            mh = self._m[i] / (1 - b1 ** self._t)
            vh = self._v[i] / (1 - b2 ** self._t)
            p -= lr * mh / (np.sqrt(vh) + eps)

    def train(self, ids, epochs=3, batch=256, lr=3e-3, seed=0, log=None):
        pairs = self._contexts(ids)
        rng = np.random.RandomState(seed)
        for ep in range(epochs):
            rng.shuffle(pairs)
            losses = []
            for i in range(0, len(pairs), batch):
                chunk = pairs[i:i + batch]
                wins = [w for w, _ in chunk]
                tgts = [t for _, t in chunk]
                loss, grads = self._loss_and_grad(wins, tgts)
                self._adam_step(grads, lr)
                losses.append(loss)
            if log:
                log(f"  epoch {ep + 1}/{epochs}  loss {sum(losses)/len(losses):.4f}")
        return self

    def seq_nll_bits(self, seed_ids, cont_ids):
        """Total NLL (in BITS) of `cont_ids` continued after `seed_ids`.

        Autoregressive: each continuation token scored given the running context
        (seed + already-emitted continuation). This is the quantity the v1 flip
        eval compares (NLL(gold) vs NLL(counterfactual))."""
        ctx = list(seed_ids)
        total = 0.0
        for tok in cont_ids:
            start = max(0, len(ctx) - self.C)
            win = ctx[start:]
            if len(win) < self.C:
                win = [win[0]] * (self.C - len(win)) + win if win else [0] * self.C
            logits, _ = self._forward([win])
            logits = logits[0]
            logits -= logits.max()
            logp = logits - math.log(np.exp(logits).sum())
            total += -logp[tok] / math.log(2.0)
            ctx.append(tok)
        return total
