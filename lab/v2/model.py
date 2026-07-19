"""v2/model.py — trunk (byte-LM) + store + learned bridge, numpy forward/backward.

@canonical-ok — see gen.py.

WHY numpy and not torch: torch is absent on this host, and the production anima trunk is
numpy too (core/decode.py). The cost is a hand-written backward pass, so C0-d gradcheck
(finite differences) is a HARD gate — a silently wrong gradient would manufacture a verdict.

Layout
    trunk   : pre-LN causal transformer, 2 layers, d=64, 4 heads, ffn 256, byte vocab 256.
              A transformer (not a conv) on purpose: global attention removes 'the receptive
              field was too small' as an escape hatch, isolating the bridge question.
    store   : 8 slots. key  = mean(byte-emb of the entity name) @ W_k  -- FUNCTIONAL, so it
              generalises to novel names. A per-entity learned key would die on held-out by
              construction and is therefore banned.
              value = one of 2 learned polarity vectors (good/bad).
    bridge  : query = hidden at the last prompt byte @ W_q, dot-product attention over the
              store keys, v = sum_i alpha_i v_i.
    consume : p = lam * softmax(W_out @ concat(v, hidden_q)) + (1-lam) * p_trunk, at the
              FIRST answer byte only (the store carries polarity; the trunk carries spelling).
              PROBABILITY-level mixing, not logit-level: it makes the lam=0 eval-time cut a
              clean causal ablation (C2).
              ⚠️ The concat is LOAD-BEARING, learned the hard way. v1 fed W_out the store
              value ALONE, so p_store was a function of polarity only while the OPERATOR
              (is/not) lived in the text. The same store must yield 'good' for `is lumo` and
              'bad' for `not lumo`, so an operator-blind readout cannot answer both -- the
              path was unsolvable, no gradient shaped it, and it sat at init. Measured:
              flip-coherence 0.000 on every arm, final_loss 0.154 == exactly "chance on
              byte 0, perfect spelling after". C2 declared every arm INVALID and P1 was
              never computed, so the anchor was never burned; this is an instrument repair,
              not a re-tuned bar. Concat lets the operator GATE the retrieved fact, which is
              also what the wall itself is (H_9359: the operator must read the store).
    lam     : learned scalar via sigmoid, init 0.5. Rotation is the antidote to lam->0
              collapse: ignoring the store caps answer CE at chance, so gradient pressure
              pushes lam up. Logged MONITOR-ONLY, never added to the loss
              (a_train_inline_gauge).

Arms differ ONLY by construction flags (see train.py):
    COTRAIN  trunk+bridge co-trained, per-example rotation
    BOLT     trunk frozen (from NOSTORE), bridge trained after  == H_9392 BRIDGE-BOLT
    NOSTORE  no store at all, same budget                       == pure-memorisation ceiling
    SLOWROT  COTRAIN but rotation every 500 steps               == isolates rotation
"""

import numpy as np

# ── primitives ──────────────────────────────────────────────────────────────────


def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)


def layernorm_fwd(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    xc = x - mu
    var = (xc * xc).mean(-1, keepdims=True)
    inv = 1.0 / np.sqrt(var + eps)
    xh = xc * inv
    return xh * g + b, (xh, inv, g)


def layernorm_bwd(dout, cache):
    xh, inv, g = cache
    d = xh.shape[-1]
    dg = (dout * xh).reshape(-1, d).sum(0)
    db = dout.reshape(-1, d).sum(0)
    dxh = dout * g
    dx = inv * (dxh - dxh.mean(-1, keepdims=True) - xh * (dxh * xh).mean(-1, keepdims=True))
    return dx, dg, db


def gelu_fwd(x):
    return 0.5 * x * (1.0 + np.tanh(0.7978845608028654 * (x + 0.044715 * x**3)))


def gelu_bwd(dout, x):
    t = np.tanh(0.7978845608028654 * (x + 0.044715 * x**3))
    dt = 0.7978845608028654 * (1.0 + 3 * 0.044715 * x**2) * (1.0 - t * t)
    return dout * (0.5 * (1.0 + t) + 0.5 * x * dt)


# ── parameters ──────────────────────────────────────────────────────────────────


def init_params(cfg, rng, with_store=True):
    d, L, H, F, V = cfg["d"], cfg["layers"], cfg["heads"], cfg["ffn"], cfg["vocab"]
    S = cfg["max_seq"]

    def n(shape, scale):
        return (rng.standard_normal(shape) * scale).astype(np.float64)

    p = {
        "emb": n((V, d), 0.02),
        "pos": n((S, d), 0.02),
        "ln_f_g": np.ones(d),
        "ln_f_b": np.zeros(d),
    }
    for i in range(L):
        p[f"l{i}_ln1_g"] = np.ones(d)
        p[f"l{i}_ln1_b"] = np.zeros(d)
        p[f"l{i}_qkv"] = n((d, 3 * d), 0.02)
        p[f"l{i}_proj"] = n((d, d), 0.02 / np.sqrt(2 * L))
        p[f"l{i}_ln2_g"] = np.ones(d)
        p[f"l{i}_ln2_b"] = np.zeros(d)
        p[f"l{i}_fc1"] = n((d, F), 0.02)
        p[f"l{i}_fc2"] = n((F, d), 0.02 / np.sqrt(2 * L))
    if with_store:
        p["W_q"] = n((d, d), 0.02)          # trunk hidden -> query
        if cfg.get("fixed_key"):
            # FROZEN content-address: a fixed random per-byte embedding, mean-pooled. Never
            # trained (its grad is never produced), so the store keys are a STABLE function
            # of the entity name — only W_q chases them. (V2_6 lever a.)
            p["key_emb_frozen"] = (rng.standard_normal((V, d)) * 0.5).astype(np.float64)
        else:
            p["W_k"] = n((d, d), 0.02)      # entity-name embedding -> store key
        p["val"] = n((2, d), 0.02)          # 2 polarity value vectors
        # readout. V2_1/V2_2: linear W_out over concat(v, hidden_q) — CANNOT express the
        # answer=polarity XOR operator (a linear map has no v*hidden_q product term; ORACLE
        # capped at 0.756, the exact no-interaction logistic ceiling). V2_3: a 2-layer MLP
        # readout (W_h -> GELU -> W_out) CAN form the interaction. cfg["readout"]="mlp"|"linear".
        rd = cfg.get("readout", "linear")
        if rd == "mlp":
            Hh = cfg.get("readout_hidden", 64)
            p["W_h"] = n((2 * d, Hh), 0.02)     # concat -> hidden (nonlinear)
            p["W_out"] = n((Hh, V), 0.02)       # hidden -> bytes
        else:
            p["W_out"] = n((2 * d, V), 0.02)    # concat(store value, query hidden) -> bytes
        p["lam_raw"] = np.array([0.0])      # sigmoid(0) = 0.5 (bars.json lambda_init)
    return p


TRUNK_KEYS_PREFIX = ("emb", "pos", "ln_f", "l")
BRIDGE_KEYS = ("W_k", "W_q", "val", "W_out", "W_h", "lam_raw", "key_emb_frozen")


def is_bridge(name):
    return name in BRIDGE_KEYS


# ── trunk forward / backward ────────────────────────────────────────────────────


def trunk_fwd(p, cfg, ids):
    """ids: (B, T) int. Returns logits (B, T, V), hidden (B, T, d), cache."""
    B, T = ids.shape
    d, L, H = cfg["d"], cfg["layers"], cfg["heads"]
    hd = d // H
    x = p["emb"][ids] + p["pos"][:T][None, :, :]
    mask = np.triu(np.ones((T, T), dtype=bool), 1)
    cache = {"ids": ids, "layers": []}

    for i in range(L):
        h_in = x
        h, ln1 = layernorm_fwd(x, p[f"l{i}_ln1_g"], p[f"l{i}_ln1_b"])
        qkv = h @ p[f"l{i}_qkv"]                                   # (B,T,3d)
        q, k, v = np.split(qkv, 3, axis=-1)
        q = q.reshape(B, T, H, hd).transpose(0, 2, 1, 3)           # (B,H,T,hd)
        k = k.reshape(B, T, H, hd).transpose(0, 2, 1, 3)
        v = v.reshape(B, T, H, hd).transpose(0, 2, 1, 3)
        att = (q @ k.transpose(0, 1, 3, 2)) / np.sqrt(hd)          # (B,H,T,T)
        att = np.where(mask[None, None], -1e9, att)
        a = softmax(att, -1)
        o = a @ v                                                   # (B,H,T,hd)
        o = o.transpose(0, 2, 1, 3).reshape(B, T, d)
        o = o @ p[f"l{i}_proj"]
        x = h_in + o

        h2_in = x
        h2, ln2 = layernorm_fwd(x, p[f"l{i}_ln2_g"], p[f"l{i}_ln2_b"])
        f1 = h2 @ p[f"l{i}_fc1"]
        f1a = gelu_fwd(f1)
        f2 = f1a @ p[f"l{i}_fc2"]
        x = h2_in + f2
        cache["layers"].append(
            {"ln1": ln1, "h": h, "q": q, "k": k, "v": v, "a": a, "o_pre": o, "hd": hd,
             "ln2": ln2, "h2": h2, "f1": f1, "f1a": f1a}
        )

    hidden, lnf = layernorm_fwd(x, p["ln_f_g"], p["ln_f_b"])
    logits = hidden @ p["emb"].T                                    # tied embedding
    cache["lnf"] = lnf
    cache["hidden"] = hidden
    return logits, hidden, cache


def trunk_bwd(p, cfg, cache, dlogits, dhidden_extra=None):
    """dlogits: (B,T,V). dhidden_extra: (B,T,d) gradient arriving at `hidden` from the
    bridge query path. Returns grads dict."""
    B, T, _ = dlogits.shape
    d, L, H = cfg["d"], cfg["layers"], cfg["heads"]
    g = {k: np.zeros_like(v) for k, v in p.items() if not is_bridge(k)}

    hidden = cache["hidden"]
    g["emb"] += dlogits.reshape(-1, dlogits.shape[-1]).T @ hidden.reshape(-1, d)
    dh = dlogits @ p["emb"]
    if dhidden_extra is not None:
        dh = dh + dhidden_extra

    dx, dg, db = layernorm_bwd(dh, cache["lnf"])
    g["ln_f_g"] += dg
    g["ln_f_b"] += db

    for i in reversed(range(L)):
        c = cache["layers"][i]
        hd = c["hd"]

        # ffn residual
        df2 = dx
        g[f"l{i}_fc2"] += c["f1a"].reshape(-1, c["f1a"].shape[-1]).T @ df2.reshape(-1, d)
        df1a = df2 @ p[f"l{i}_fc2"].T
        df1 = gelu_bwd(df1a, c["f1"])
        g[f"l{i}_fc1"] += c["h2"].reshape(-1, d).T @ df1.reshape(-1, df1.shape[-1])
        dh2 = df1 @ p[f"l{i}_fc1"].T
        dxa, dg2, db2 = layernorm_bwd(dh2, c["ln2"])
        g[f"l{i}_ln2_g"] += dg2
        g[f"l{i}_ln2_b"] += db2
        dx = dx + dxa

        # attn residual
        do = dx
        o_cat = (c["a"] @ c["v"]).transpose(0, 2, 1, 3).reshape(B, T, d)  # pre-proj concat
        g[f"l{i}_proj"] += o_cat.reshape(-1, d).T @ do.reshape(-1, d)
        do_cat = do @ p[f"l{i}_proj"].T
        do_h = do_cat.reshape(B, T, H, hd).transpose(0, 2, 1, 3)    # (B,H,T,hd)

        da = do_h @ c["v"].transpose(0, 1, 3, 2)                    # (B,H,T,T)
        dv = c["a"].transpose(0, 1, 3, 2) @ do_h
        datt = c["a"] * (da - (da * c["a"]).sum(-1, keepdims=True))
        datt = datt / np.sqrt(hd)
        dq = datt @ c["k"]
        dk = datt.transpose(0, 1, 3, 2) @ c["q"]

        dqkv = np.concatenate(
            [x.transpose(0, 2, 1, 3).reshape(B, T, d) for x in (dq, dk, dv)], axis=-1
        )
        g[f"l{i}_qkv"] += c["h"].reshape(-1, d).T @ dqkv.reshape(-1, 3 * d)
        dh_ln = dqkv @ p[f"l{i}_qkv"].T
        dxb, dg1, db1 = layernorm_bwd(dh_ln, c["ln1"])
        g[f"l{i}_ln1_g"] += dg1
        g[f"l{i}_ln1_b"] += db1
        dx = dx + dxb

    g["pos"][: dx.shape[1]] += dx.sum(0)
    ids = cache["ids"]
    np.add.at(g["emb"], ids.reshape(-1), dx.reshape(-1, d))
    return g


# ── store / bridge ──────────────────────────────────────────────────────────────


def store_keys(p, cfg, store_ids):
    """store_ids: (B, S, name_len) byte ids. key = mean(byte-emb) @ W_k (learned), or
    mean(frozen-emb) (fixed content-address, V2_6). Returns (keys, e_for_grad)."""
    if "key_emb_frozen" in p:
        e = p["key_emb_frozen"][store_ids].mean(axis=2)   # (B,S,d) frozen
        return e, None                                    # None => no grad flows to keys
    e = p["emb"][store_ids].mean(axis=2)          # (B,S,d)
    return e @ p["W_k"], e


def bridge_fwd(p, cfg, hidden_q, store_ids, val_idx, mask_slots=None, oracle_slot=None):
    """hidden_q: (B,d) hidden at the query position.
    store_ids: (B,S,name_len). val_idx: (B,S) polarity per slot.
    Returns p_store (B,V) and a cache."""
    keys, e = store_keys(p, cfg, store_ids)       # (B,S,d)
    q = hidden_q @ p["W_q"]                       # (B,d)
    att = np.einsum("bd,bsd->bs", q, keys) / np.sqrt(cfg["d"])
    if mask_slots is not None:
        att = np.where(mask_slots, -1e9, att)
    a = softmax(att, -1)                          # (B,S)
    if oracle_slot is not None:
        # POSITIVE CONTROL (C0-e): force attention onto the true slot. Retrieval is free,
        # so only the readout+operator gating has to be learned. If ORACLE cannot clear the
        # bar, the toy cannot express the task and NO negative here is readable.
        a = np.zeros_like(a)
        a[np.arange(a.shape[0]), oracle_slot] = 1.0
    vals = p["val"][val_idx]                      # (B,S,d)
    v = np.einsum("bs,bsd->bd", a, vals)          # (B,d)
    # concat the query hidden so the OPERATOR can gate the retrieved polarity. The store
    # supplies the fact; the operator (is/not) lives in the text and therefore in hidden_q.
    # Without this concat p_store is a function of polarity ALONE and cannot answer both
    # operators from the same store -- the path is unsolvable, so no gradient shapes it and
    # it stays at init (measured: flip-coherence 0.000, all arms). C2 caught it before P1.
    cat = np.concatenate([v, hidden_q], axis=-1)  # (B,2d)
    mlp = "W_h" in p
    if mlp:
        pre = cat @ p["W_h"]                       # (B,Hh)
        hmid = gelu_fwd(pre)
        logits = hmid @ p["W_out"]                 # (B,V) — nonlinear readout, can XOR
    else:
        pre = hmid = None
        logits = cat @ p["W_out"]                  # (B,V) — linear (V2_1/V2_2)
    ps = softmax(logits, -1)
    return ps, {"keys": keys, "e": e, "q": q, "a": a, "vals": vals, "v": v, "cat": cat,
                "pre": pre, "hmid": hmid, "mlp": mlp,
                "logits": logits, "ps": ps, "hidden_q": hidden_q, "store_ids": store_ids,
                "val_idx": val_idx}


def bridge_bwd(p, cfg, c, dupstream, d_is_logits=False):
    """dupstream: (B,V). In MIX mode it is d(loss)/d(p_store) and we backprop through the
    store's own softmax. In LOGIT-ADD mode (V2_2) the store's raw logits are ADDED to the
    trunk logits before a SINGLE shared softmax, so there is no separate store softmax —
    the gradient arriving at the store logits IS dupstream; pass d_is_logits=True to skip
    the softmax-bwd. Returns (bridge grads, dhidden_q, demb_from_keys)."""
    g = {}
    if d_is_logits:
        dlogits = dupstream
    else:
        ps = c["ps"]
        dlogits = ps * (dupstream - (dupstream * ps).sum(-1, keepdims=True))  # softmax bwd
    if c["mlp"]:
        g["W_out"] = c["hmid"].T @ dlogits
        dhmid = dlogits @ p["W_out"].T                            # (B,Hh)
        dpre = gelu_bwd(dhmid, c["pre"])
        g["W_h"] = c["cat"].T @ dpre
        dcat = dpre @ p["W_h"].T                                   # (B,2d)
    else:
        g["W_out"] = c["cat"].T @ dlogits
        dcat = dlogits @ p["W_out"].T                             # (B,2d)
    d = cfg["d"]
    dv, dhq_direct = dcat[:, :d], dcat[:, d:]                      # split the concat

    da = np.einsum("bd,bsd->bs", dv, c["vals"])
    dvals = np.einsum("bs,bd->bsd", c["a"], dv)
    g["val"] = np.zeros_like(p["val"])
    np.add.at(g["val"], c["val_idx"].reshape(-1), dvals.reshape(-1, cfg["d"]))

    datt = c["a"] * (da - (da * c["a"]).sum(-1, keepdims=True))
    datt = datt / np.sqrt(cfg["d"])
    dq = np.einsum("bs,bsd->bd", datt, c["keys"])
    dkeys = np.einsum("bs,bd->bsd", datt, c["q"])

    g["W_q"] = c["hidden_q"].T @ dq
    dhidden_q = dq @ p["W_q"].T + dhq_direct       # query path + the concat's direct path

    if c["e"] is None:
        # V2_6 fixed_key: keys are frozen, so no gradient flows to W_k or the key embedding.
        # Only W_q learns to aim at the fixed content-addresses.
        return g, dhidden_q, np.zeros_like(p["emb"])
    g["W_k"] = c["e"].reshape(-1, cfg["d"]).T @ dkeys.reshape(-1, cfg["d"])
    de = dkeys @ p["W_k"].T                                        # (B,S,d)
    nlen = c["store_ids"].shape[2]
    demb = np.zeros_like(p["emb"])
    np.add.at(demb, c["store_ids"].reshape(-1), np.repeat(de / nlen, nlen, axis=1).reshape(-1, cfg["d"]))
    return g, dhidden_q, demb


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))
