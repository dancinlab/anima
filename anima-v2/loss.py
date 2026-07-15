"""anima-v2/loss.py — the single forward/loss/backward path.

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
                 oracle_slot=None):
    """ids/targets: (B,T). loss_mask: (B,T) 1.0 where the CE is counted (answer bytes).
    qpos: (B,) index of the last prompt byte (where the bridge forms its query).
    ans_pos: (B,) index whose prediction is the FIRST answer byte (== qpos, kept explicit).
    lam_override: force lambda (C2 lam=0 cut). val_override: (2,d) replace polarity values
    (C2 neutral-store).
    Returns (loss, grads) if backward else (loss, aux)."""
    B, T = ids.shape
    V = cfg["vocab"]

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

    if use_store:
        d_mixed = dprobs[np.arange(B), ans_pos]          # (B,V)
        dps = lam * d_mixed
        dptrunk_at_ans = (1.0 - lam) * d_mixed

        if lam_override is None:
            p_store = bc["ps"]
            dlam = float((d_mixed * (p_store - p_trunk[np.arange(B), ans_pos])).sum())
            s = M.sigmoid(p["lam_raw"][0])
            grads["lam_raw"] = np.array([dlam * s * (1.0 - s)])

        bg, dhq, demb_keys = M.bridge_bwd(p, cfg, bc, dps)
        for k, v in bg.items():
            grads[k] = grads[k] + v
        grads["emb"] = grads["emb"] + demb_keys

        dhidden_extra = np.zeros_like(hidden)
        dhidden_extra[np.arange(B), qpos] += dhq

        dprobs = dprobs.copy()
        dprobs[np.arange(B), ans_pos] = dptrunk_at_ans

    # softmax backward on the trunk
    dlogits = p_trunk * (dprobs - (dprobs * p_trunk).sum(-1, keepdims=True))
    tg = M.trunk_bwd(p, cfg, tcache, dlogits, dhidden_extra)
    for k, v in tg.items():
        grads[k] = grads[k] + v
    return loss, grads
