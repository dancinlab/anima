"""v2/loss.py — the single forward/loss/backward path.

@canonical-ok — see gen.py.

Train, eval and gradcheck ALL call forward_loss(). One code path only: if the instrument
and the training loop can diverge, the verdict is measuring the divergence, not the model.

The mix is applied at the FIRST answer byte only:
    p = lam * p_store + (1 - lam) * p_trunk
The store carries polarity; the trunk carries spelling. Probability-level (not logit-level)
so that the eval-time lam=0 cut in C2 is an exact causal ablation of the store path.
"""

import numpy as np

import model as M


def forward_loss(p, cfg, ids, targets, loss_mask, store_ids, val_idx, qpos, ans_pos,
                 use_store=True, backward=False, lam_override=None, val_override=None,
                 oracle_slot=None, gate=None):
    """ids/targets: (B,T). loss_mask: (B,T) 1.0 where the CE is counted (answer bytes).
    qpos: (B,) index of the last prompt byte (where the bridge forms its query).
    ans_pos: (B,) index whose prediction is the FIRST answer byte (== qpos, kept explicit).
    lam_override: force lambda (C2 lam=0 cut). val_override: (2,d) replace polarity values
    (C2 neutral-store).
    gate: "mix" (V2_1) = p = lam*p_store + (1-lam)*p_trunk (probability-level). "logit" (V2_2)
    = logit_ans = trunk_logit + store_logit, ONE shared softmax (logit-level). The mix path
    lets the trunk's near-uniform distribution DILUTE the store (V2_1: ORACLE only 0.74 even
    with retrieval free); the logit path adds in log-space so a confident store logit wins
    regardless of how flat the trunk is. C2 lam=0 cut = zero the store contribution in both.
    Returns (loss, grads) if backward else (loss, aux)."""
    B, T = ids.shape
    V = cfg["vocab"]
    gate = gate or cfg.get("gate", "mix")

    logits, hidden, tcache = M.trunk_fwd(p, cfg, ids)
    p_trunk = M.softmax(logits, -1)                      # (B,T,V)

    probs = p_trunk
    bc = None
    lam = 0.0
    if use_store:
        lam = float(M.sigmoid(p["lam_raw"][0])) if lam_override is None else float(lam_override)
        pp = dict(p)
        if val_override is not None:
            pp = dict(p)
            pp["val"] = val_override
        hq = hidden[np.arange(B), qpos]                  # (B,d)
        p_store, bc = M.bridge_fwd(pp, cfg, hq, store_ids, val_idx,
                                   oracle_slot=oracle_slot)
        probs = p_trunk.copy()
        if gate == "store_only":
            # V2_4: the first answer byte is produced by the STORE ALONE — the trunk logits
            # at the answer position are removed, cutting the shortcut that let COTRAIN's
            # trunk absorb the answer and starve the retrieval path (V2_3 flip-coh 0.000).
            # The bridge is now the ONLY exit, so it MUST learn to query or the loss stalls.
            comb = lam * bc["logits"]
            probs[np.arange(B), ans_pos] = M.softmax(comb, -1)
        elif gate == "logit":
            # ADD store logits to the trunk logits at the answer position, then ONE softmax.
            trunk_ans_logits = logits[np.arange(B), ans_pos]         # (B,V)
            comb = trunk_ans_logits + lam * bc["logits"]             # lam scales the store
            probs[np.arange(B), ans_pos] = M.softmax(comb, -1)
        else:
            mixed = lam * p_store + (1.0 - lam) * p_trunk[np.arange(B), ans_pos]
            probs[np.arange(B), ans_pos] = mixed

    eps = 1e-12
    tgt_p = probs[np.arange(B)[:, None], np.arange(T)[None, :], targets]
    nll = -np.log(tgt_p + eps) * loss_mask
    denom = max(1.0, loss_mask.sum())
    loss = nll.sum() / denom

    if not backward:
        return loss, {"probs": probs, "p_trunk": p_trunk, "lam": lam, "bridge": bc}

    # d loss / d probs
    dprobs = np.zeros_like(probs)
    dprobs[np.arange(B)[:, None], np.arange(T)[None, :], targets] = \
        -(1.0 / (tgt_p + eps)) * loss_mask / denom

    grads = {k: np.zeros_like(v) for k, v in p.items()}
    dhidden_extra = None
    # trunk softmax backward for the whole grid; the answer position is FIXED afterwards
    # (its distribution came from a combined/mixed softmax, not the trunk's alone)
    dlogits = p_trunk * (dprobs - (dprobs * p_trunk).sum(-1, keepdims=True))

    if use_store and gate in ("logit", "store_only"):
        # answer position used ONE softmax over (trunk_logit + lam*store_logit), or over
        # lam*store_logit alone (store_only).
        p_ans = probs[np.arange(B), ans_pos]             # (B,V)
        tgt_ans = targets[np.arange(B), ans_pos]
        w = (loss_mask[np.arange(B), ans_pos] / denom)[:, None]
        dcomb = p_ans.copy()
        dcomb[np.arange(B), tgt_ans] -= 1.0
        dcomb = dcomb * w                                # d loss / d comb-logits
        # store_only: the trunk logits are NOT in comb, so they get zero answer-position
        # gradient (the shortcut is cut). logit: the trunk shares the answer gradient.
        dlogits[np.arange(B), ans_pos] = 0.0 if gate == "store_only" else dcomb
        dstore = lam * dcomb                             # grad to store RAW logits
        if lam_override is None:
            dlam = float((dcomb * bc["logits"]).sum())
            s = M.sigmoid(p["lam_raw"][0])
            grads["lam_raw"] = np.array([dlam * s * (1.0 - s)])
        bg, dhq, demb_keys = M.bridge_bwd(p, cfg, bc, dstore, d_is_logits=True)
        for k, val in bg.items():
            grads[k] = grads[k] + val
        grads["emb"] = grads["emb"] + demb_keys
        dhidden_extra = np.zeros_like(hidden)
        dhidden_extra[np.arange(B), qpos] += dhq

    elif use_store:                                      # mix mode (V2_1)
        d_mixed = dprobs[np.arange(B), ans_pos]          # (B,V)
        dps = lam * d_mixed
        dptrunk_at_ans = (1.0 - lam) * d_mixed
        if lam_override is None:
            p_store = bc["ps"]
            dlam = float((d_mixed * (p_store - p_trunk[np.arange(B), ans_pos])).sum())
            s = M.sigmoid(p["lam_raw"][0])
            grads["lam_raw"] = np.array([dlam * s * (1.0 - s)])
        bg, dhq, demb_keys = M.bridge_bwd(p, cfg, bc, dps)
        for k, val in bg.items():
            grads[k] = grads[k] + val
        grads["emb"] = grads["emb"] + demb_keys
        dhidden_extra = np.zeros_like(hidden)
        dhidden_extra[np.arange(B), qpos] += dhq
        # the trunk saw only (1-lam) of the answer-position gradient
        dtrunk_ans = p_trunk[np.arange(B), ans_pos] * (
            dptrunk_at_ans - (dptrunk_at_ans * p_trunk[np.arange(B), ans_pos]).sum(-1, keepdims=True))
        dlogits[np.arange(B), ans_pos] = dtrunk_ans

    tg = M.trunk_bwd(p, cfg, tcache, dlogits, dhidden_extra)
    for k, v in tg.items():
        grads[k] = grads[k] + v
    return loss, grads
