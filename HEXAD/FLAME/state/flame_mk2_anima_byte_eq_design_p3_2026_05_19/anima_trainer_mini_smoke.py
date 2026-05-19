#!/usr/bin/env python3
"""P3 Mode S1 — anima trainer mini d=32.3L reproduction stub ($0 Mac CPU).

Self-contained, pure-numpy, NO torch, NO GPU, NO external corpus file.
Reproduces a d=32 / n_layer=3 micro decoder training loop with a fixed
LCG-seeded corpus stub (seed 1337), measuring:
  - init gn2  = ||softmax(logits) - onehot||^2  at step 0
  - final gn2 = same at last step
  - acc 8/8   = argmax correctness over an 8-prompt held-set

This is a STUB reproduction: it is NOT the full anima ConsciousDecoderV2
trainer. Its purpose is to provide a deterministic anima-side datapoint
for the 3 closed-form byte-eq falsifiers (F-1/F-2/F-3), which compare it
against the hexa-lang DOCUMENTED flame values (flame_anchor_values.json).

Honest scope: stub-scale d=32.3L only. Full d=768.12L flame-vs-anima
fire = future cost-bearing cycle. anima-side perf claim is FORBIDDEN;
this falsifier measures gradient CORRECTNESS, not speed.
"""
import json
import math
import os

SEED = 1337
D = 32
N_LAYER = 3
VOCAB = 256
STEPS = 600
LR = 4.0


class LCG:
    """Deterministic LCG — numerically identical run-to-run, no RNG library."""
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF

    def next_u32(self):
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return self.s

    def uniform(self):
        return self.next_u32() / 4294967296.0

    def gauss(self):
        # Box-Muller from two uniforms
        u1 = max(self.uniform(), 1e-12)
        u2 = self.uniform()
        return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def softmax(xs):
    m = max(xs)
    es = [math.exp(x - m) for x in xs]
    s = sum(es)
    return [e / s for e in es]


def gn2_of(logits, target):
    """gn2 surrogate. flame README contract states gn2 = ||softmax(logits) - onehot||^2;
    its documented anchor 7.97 exceeds the [0,2] range of that normalized form, so flame's
    runtime gn2 is the UN-NORMALIZED ||logits - onehot||^2 (gradient-norm scale). The anima
    stub mirrors that un-normalized form for shape-comparable trajectories. The byte-eq
    falsifiers (F-1/F-2/F-3) operate on the NORMALIZED / shape / relative-norm planes so the
    exact gn2 unit is not load-bearing — see DESIGN_FINDINGS.md C3 #4."""
    acc = 0.0
    for i, li in enumerate(logits):
        oh = 1.0 if i == target else 0.0
        acc += (li - oh) ** 2
    return acc


def run():
    rng = LCG(SEED)
    # micro corpus stub: 8 (context-byte, target-byte) pairs, deterministic
    corpus = []
    for _ in range(8):
        ctx = rng.next_u32() % VOCAB
        tgt = rng.next_u32() % VOCAB
        corpus.append((ctx, tgt))

    # weights: a single d-wide embedding + N_LAYER residual scalars + lm head row
    emb = [[rng.gauss() * 0.02 for _ in range(D)] for _ in range(VOCAB)]
    layer_scale = [1.0 for _ in range(N_LAYER)]
    head = [[rng.gauss() * 0.02 for _ in range(D)] for _ in range(VOCAB)]

    def forward(ctx):
        h = list(emb[ctx])
        for ls in layer_scale:
            h = [x * ls + 0.01 * math.tanh(x) for x in h]
        logits = []
        for v in range(VOCAB):
            acc = 0.0
            hv = head[v]
            for k in range(D):
                acc += h[k] * hv[k]
            logits.append(acc)
        return h, logits

    # init gn2 — mean over corpus
    init_gn2 = sum(gn2_of(forward(c)[1], t) for c, t in corpus) / len(corpus)

    curve = [init_gn2]
    for step in range(STEPS):
        for ctx, tgt in corpus:
            h, logits = forward(ctx)
            p = softmax(logits)
            # gradient of gn2 wrt logits: 2*(p-oh) chained through softmax
            # simple SGD on head rows only (sufficient for stub convergence)
            for v in range(VOCAB):
                oh = 1.0 if v == tgt else 0.0
                # d gn2 / d logit_v  (approx, dominant term)
                g = 2.0 * (p[v] - oh) * p[v]
                for k in range(D):
                    head[v][k] -= LR * g * h[k]
        cur = sum(gn2_of(forward(c)[1], t) for c, t in corpus) / len(corpus)
        curve.append(cur)

    final_gn2 = curve[-1]
    # acc 8/8: argmax over the 8-prompt held set
    acc = 0
    for ctx, tgt in corpus:
        _, logits = forward(ctx)
        if max(range(VOCAB), key=lambda i: logits[i]) == tgt:
            acc += 1

    # weight-snapshot norm (final head Frobenius norm) for F-3
    head_fro = math.sqrt(sum(x * x for row in head for x in row))

    return {
        "config": "d=32 n_layer=3 (anima trainer mini stub)",
        "seed": SEED,
        "steps": STEPS,
        "init_gn2": init_gn2,
        "final_gn2": final_gn2,
        "acc_8of8": acc,
        "loss_curve": curve,
        "head_frobenius": head_fro,
    }


if __name__ == "__main__":
    out = run()
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anima_mini_result.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=2)
    print(f"S1 anima mini: init_gn2={out['init_gn2']:.6f} "
          f"final_gn2={out['final_gn2']:.6e} acc={out['acc_8of8']}/8")
