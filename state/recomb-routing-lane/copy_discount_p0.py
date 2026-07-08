#!/usr/bin/env python3
"""H_9235 clml 심화 P0 — copy-discount N2 surface-lexicon null ($0 · 텍스트만 · hidden 불필요).

Fable §1.2: 현 clml 0.98 셀이 '의미 합성'인지 'surface-form lookup'인지 격리. N2 null = prompt를
byte-ngram bag-of-indicators로만 보고 XOR(code_a,code_b)를 예측하는 소형 로지스틱. **N2가 held-out에서
clml(0.98)에 필적하면 그 셀은 의미를 재지 않는다** (verdict 무자격 · surface-solvable). 신호 = clml −
max(null): M_copy 작으면 cell copy-confounded.

INPUT: pair_prompts.json (items:{id,prompt,a,b,split}) + concepts.json (code). torch-free numpy.
"""
import json
import sys
import numpy as np

PP = sys.argv[1] if len(sys.argv) > 1 else "pair_prompts.json"
CONC = sys.argv[2] if len(sys.argv) > 2 else "concepts.json"
BITS = 5

pp = json.load(open(PP))["items"]
concepts = json.load(open(CONC))
names = sorted(concepts, key=lambda c: concepts[c]["idx"])
code = np.array([concepts[c]["code"] for c in names], dtype=int)   # [N,5]


def xor(a, b):
    return (code[a] ^ code[b]).astype(np.float64)


train = [it for it in pp if it["split"] == "train"]
held = [it for it in pp if it["split"] == "held"]


def ngrams(s, ns=(3, 4)):
    b = s.encode("utf-8")
    out = set()
    for n in ns:
        for i in range(len(b) - n + 1):
            out.add(b[i:i + n])
    return out


# vocabulary from TRAIN prompts only (held ngrams unseen → honest)
vocab = {}
for it in train:
    for g in ngrams(it["prompt"]):
        if g not in vocab:
            vocab[g] = len(vocab)
V = len(vocab)


def feat(items):
    X = np.zeros((len(items), V))
    for i, it in enumerate(items):
        for g in ngrams(it["prompt"]):
            j = vocab.get(g)
            if j is not None:
                X[i, j] = 1.0
    return X


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def logistic(Xtr, Ytr, Xte, steps=3000, lr=0.5, l2=1e-3):
    n, d = Xtr.shape
    W = np.zeros((BITS, d)); b = np.zeros(BITS)
    for _ in range(steps):
        p = sigmoid(Xtr @ W.T + b); g = (p - Ytr) / n
        W -= lr * (g.T @ Xtr + l2 * W); b -= lr * g.sum(0)
    return (np.round(sigmoid(Xte @ W.T + b)).astype(int))


if __name__ == "__main__":
    Ytr = np.array([xor(it["a"], it["b"]) for it in train])
    Yte = np.array([xor(it["a"], it["b"]) for it in held])
    Xtr, Xte = feat(train), feat(held)
    print(f"N2 surface-lexicon null: V={V} byte-ngram · train={len(train)} held={len(held)}", flush=True)

    # N2: byte-ngram bag → XOR code
    pred = logistic(Xtr, Ytr, Xte)
    n2 = float((pred == Yte).all(1).mean())   # exact 5-bit match (clml 매트릭스와 동일 지표)
    n2bit = float((pred == Yte).mean())

    # word-bag variant (whitespace tokens) — coarser surface null
    def wordfeat(items, wv):
        X = np.zeros((len(items), len(wv)))
        for i, it in enumerate(items):
            for w in it["prompt"].lower().split():
                if w in wv:
                    X[i, wv[w]] = 1.0
        return X
    wv = {}
    for it in train:
        for w in it["prompt"].lower().split():
            wv.setdefault(w, len(wv))
    predw = logistic(wordfeat(train, wv), Ytr, wordfeat(held, wv))
    nw = float((predw == Yte).all(1).mean())

    # N2-nonlinear: gelu-MLP on ngram bag (fair copy-discount — same nonlinearity as clml,
    # but SURFACE only, no hidden). If this reaches ~0.98 → task surface-solvable(hidden 무관=copy);
    # if it fails while hidden-gelu(0.98) wins → hidden representation load-bearing = genuine.
    def gelu(x):
        return 0.5 * x * (1.0 + np.tanh(0.7978845608 * (x + 0.044715 * x**3)))

    def dgelu(x):
        t = np.tanh(0.7978845608 * (x + 0.044715 * x**3))
        return 0.5 * (1 + t) + 0.5 * x * (1 - t**2) * 0.7978845608 * (1 + 3 * 0.044715 * x**2)

    def gelu_mlp(Xtr, Ytr, Xte, R=128, steps=3000, lr=0.1):
        rng = np.random.default_rng(0); n, d = Xtr.shape
        W1 = rng.standard_normal((d, R)) / np.sqrt(d); b1 = np.zeros(R)
        w = rng.standard_normal((BITS, R)) * 0.05
        for _ in range(steps):
            bi = rng.integers(0, n, 128); h = Xtr[bi]
            pre = h @ W1 + b1; z = gelu(pre); p = sigmoid(z @ w.T); g = (p - Ytr[bi]) / 128
            w -= lr * (g.T @ z); gz = (g @ w) * dgelu(pre); W1 -= lr * (h.T @ gz); b1 -= lr * gz.sum(0)
        return np.round(sigmoid(gelu(Xte @ W1 + b1) @ w.T)).astype(int)
    prednl = gelu_mlp(Xtr, Ytr, Xte)
    n2nl = float((prednl == Yte).all(1).mean())
    res_n2nl = round(n2nl, 4)

    surface_max = max(n2, nw, n2nl)   # 최강 surface-only null (선형·word·비선형)
    m_copy = round(0.979 - surface_max, 4)
    res = {
        "V_ngram": V, "n_train": len(train), "n_held": len(held),
        "N2_ngram_linear_exact": round(n2, 4), "N2_ngram_perbit": round(n2bit, 4),
        "N2_wordbag_exact": round(nw, 4), "N2_ngram_gelu_exact": res_n2nl,
        "surface_null_max": round(surface_max, 4),
        "clml_champion_mean_gelu": 0.979, "clml_max_gelu": 0.980,
        "M_copy": m_copy,
    }
    if surface_max >= 0.90:
        res["verdict"] = (f"🧱 CELL COPY-CONFOUNDED — surface-only null(비선형포함)이 held-out exact XOR을 "
                          f"{surface_max:.3f}(≈clml 0.98)로 푼다 → hidden 무관·surface-form lookup. M_copy={m_copy:.3f}<0.30 "
                          f"⟹ clml 0.98은 copy-discount 무자격, 진짜 verdict는 copy-blocked 셀에서만.")
    elif surface_max >= 0.60:
        res["verdict"] = (f"🟡 PARTIAL — surface null={surface_max:.3f}, M_copy={m_copy:.3f}. copy-blocked 셀 재확인.")
    else:
        res["verdict"] = (f"🟢 COMPOSITION SURVIVES COPY-DISCOUNT — 최강 surface-only null(비선형 gelu-MLP 포함)="
                          f"{surface_max:.3f} ≪ clml 0.98. M_copy={m_copy:.3f}≥0.30 → clml의 0.98은 prompt 표면형만으론 "
                          f"안 풀리는 **hidden-representation-load-bearing 진짜 합성**. copy-discount 통과 = clml 2-concept 셀 유효.")
    print(f"surface null: ngram-lin={n2:.3f} · word={nw:.3f} · ngram-gelu={n2nl:.3f} → max={surface_max:.3f} · clml=0.979 · M_copy={m_copy:.3f}", flush=True)
    print("VERDICT:", res["verdict"], flush=True)
    json.dump(res, open("copy_discount_p0_RESULT.json", "w"), indent=2, ensure_ascii=False)
