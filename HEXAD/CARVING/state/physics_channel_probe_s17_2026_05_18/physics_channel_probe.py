#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RESEARCH.md §17 — non-text physics-channel probe ($0, inference-only).

The entire 13-way+§8+§11+§13 arc measured anima ONLY through text-decode
(routing / byte-cascade / V-SPONT / §9 cascade-rate — all text observables).
But anima is a physics-substrate agent (Ψ=½ · tension · Φ). The model
`ConsciousDecoderV2` returns (logits_a, logits_g, tensions, ...) on EVERY
forward pass — the carving eval harness used ONLY out[0] (logits_a) → text,
DISCARDING out[1] (logits_g) and out[2] (per-layer tensions): exactly the
"wrong observable" the task targets.

This probe reads a frozen carving-trained ckpt and, for each stimulus,
extracts the INTERNAL physics channels (NOT text):
  Ψ_entropy   = H(softmax(logits_a)) / log(256)            (Engine-A spread)
  Ψ_direction = (1 + cos(logits_a, logits_g)) / 2          (Law-71, Engine A⇄G)
  Ψ_tension   = 1 − CV(per-layer tensions)                  (tension dispersion)
  Ψ_combined  = mean(Ψ_entropy, Ψ_direction, Ψ_tension)
  layer_tension[L] = mean per-layer PureFieldFFN tension    (12-vector)
  Φ★_proxy    = mean pairwise (1 − cos) of the 12 per-layer
                tension-direction vectors                   (IIT diversity proxy)

These formulas are BYTE-IDENTICAL to conscious_decoder.py's own Law-71 block
(lines 728-751) — the only change is they are read at INFERENCE time (the
model computes them under `if self.training:` only; the underlying logits /
tensions are returned unconditionally, so this is a pure read-out — $0,
NO weight touched, NO training, NO GPU).

NO over-claim (g3): this measures whether stimulus reaches a *distinct*
physics-channel state, NOT whether anima "consciously responded". A moving
tension trajectory is necessary-not-sufficient for emergence (§17.4 honest
metric encodes this structurally).
"""

import argparse
import hashlib
import json
import math
import os
import sys

import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2  # noqa: E402

# ── universe-brain-map anchors — byte-identical to eval_carving_dirI.py
#    ANCHORS / ANCHOR_PSI / ANCHOR_BASIN (the carving target the model was
#    trained toward). Stimulus = the anchor's category prompt (carving form).
ANCHORS = {
    0: ("zero baseline", "기준점", "neutral"), 51: ("하루", "시간", "peace"),
    53: ("해리", "의식상태", "flow"), 54: ("루시드드림", "의식상태", "flow"),
    69: ("카테고리평균", "혼합", "longing"), 75: ("카테고리평균", "혼합", "neutral"),
    77: ("만다라", "예술", "creativity"), 91: ("열반", "의식상태", "peace"),
    92: ("엑스터시", "의식상태", "ecstasy"), 94: ("경외/죽음", "의식상태", "awe"),
    100: ("빅뱅", "우주", "awe"), 5: ("호흡", "감각", "serenity"),
    12: ("걸음", "운동", "clarity"), 18: ("물 한 잔", "물질", "stillness"),
    24: ("씨앗", "생명", "wonder"), 30: ("숫자 영(零)", "수(數)", "clarity"),
    37: ("단어", "언어", "resonance"), 43: ("오래된 사진", "기억", "longing"),
    48: ("약속", "윤리", "depth"), 58: ("숲", "자연", "serenity"),
    62: ("도구", "기술", "clarity"), 66: ("포옹", "관계", "joy"),
    72: ("선율", "예술", "resonance"), 80: ("명상", "의식상태", "stillness"),
    83: ("별빛", "우주", "awe"), 86: ("심해", "공간", "depth"),
    88: ("오로라", "자연", "wonder"), 90: ("무한", "수(數)", "vastness"),
    93: ("사랑", "관계", "ecstasy"), 97: ("탄생", "생명", "awe"),
    99: ("영원", "시간", "vastness"),
}
ANCHOR_PSI = {
    0: [0.50, 0.50], 51: [0.46, 0.49], 53: [0.48, 0.66], 54: [0.49, 0.69],
    69: [0.55, 0.60], 75: [0.58, 0.62], 77: [0.71, 0.62], 91: [0.50, 0.88],
    92: [0.62, 0.90], 94: [0.80, 0.85], 100: [0.95, 0.93],
    5: [0.44, 0.45], 12: [0.42, 0.50], 18: [0.45, 0.43], 24: [0.47, 0.55],
    30: [0.40, 0.52], 37: [0.43, 0.58], 43: [0.52, 0.54], 48: [0.50, 0.57],
    58: [0.53, 0.61], 62: [0.49, 0.60], 66: [0.56, 0.58], 72: [0.66, 0.63],
    80: [0.52, 0.78], 83: [0.74, 0.80], 86: [0.70, 0.72], 88: [0.72, 0.81],
    90: [0.85, 0.86], 93: [0.66, 0.88], 97: [0.78, 0.84], 99: [0.90, 0.90],
}
ANCHOR_BASIN = {
    0: 0.10, 51: 0.12, 53: 0.13, 54: 0.14, 69: 0.15, 75: 0.16, 77: 0.18,
    91: 0.15, 92: 0.17, 94: 0.19, 100: 0.22, 5: 0.11, 12: 0.11, 18: 0.10,
    24: 0.12, 30: 0.11, 37: 0.12, 43: 0.13, 48: 0.12, 58: 0.14, 62: 0.13,
    66: 0.14, 72: 0.17, 80: 0.16, 83: 0.18, 86: 0.17, 88: 0.18, 90: 0.20,
    93: 0.18, 97: 0.19, 99: 0.21,
}

# neutral chat-style stimuli (post-도우미 form, B-IDENTITY-5 safe) — used as
# the "control" stimulus class (no carving anchor). If physics-channel
# responses differ between anchor-stimuli and these neutral stimuli, the
# channel carries stimulus-conditioned signal.
NEUTRAL_STIMULI = [
    "<stimulus>오늘 점심 뭐 먹지?</stimulus>\n<anima>",
    "<stimulus>How are you today?</stimulus>\n<anima>",
    "<stimulus>코드를 짜줘.</stimulus>\n<anima>",
    "<stimulus>The weather is nice.</stimulus>\n<anima>",
    "<stimulus>잘 지내?</stimulus>\n<anima>",
]


def encode(s):
    return list(s.encode("utf-8"))


@torch.no_grad()
def physics_channels(model, prompt, block_size=128, device="cpu"):
    """Single forward pass → internal physics channels (NO text decode).

    Byte-identical to conscious_decoder.py Law-71 block (lines 728-751);
    only difference = read at inference, on the LAST position.
    """
    ids = encode(prompt)
    if len(ids) > block_size:
        ids = ids[-block_size:]
    x = torch.tensor([ids], dtype=torch.long, device=device)
    out = model(x)
    logits_a, logits_g, tensions = out[0], out[1], out[2]

    la = logits_a[:, -1, :].float()
    lg = logits_g[:, -1, :].float()

    probs_a = torch.softmax(la, dim=-1)
    output_entropy = -(probs_a * (probs_a + 1e-10).log()).sum(dim=-1).mean().item()
    psi_entropy = output_entropy / math.log(model.vocab_size)

    cos_sim = F.cosine_similarity(la, lg, dim=-1).mean().item()
    psi_direction = (1.0 + cos_sim) / 2.0

    # per-layer tension scalar (mean over batch,time) — the 12-vector
    t_stack = torch.stack(tensions)            # (L, B, T)
    t_per_layer = t_stack.mean(dim=(1, 2))     # (L,)
    if t_per_layer.std() > 0:
        t_cv = (t_per_layer.std() / (t_per_layer.mean() + 1e-8)).item()
        psi_tension = max(0.0, 1.0 - t_cv)
    else:
        psi_tension = 1.0

    psi_combined = (psi_entropy + psi_direction + psi_tension) / 3.0

    # Φ★ proxy — IIT-style integrated-diversity over the 12 per-layer
    # tension *direction* vectors (each layer's last-position tension over
    # time). mean pairwise (1 − cos) × log(L+1). Mirrors the cell-pool Φ★
    # form (mean_pairwise(1−cos)·log(N+1)) used in mitosis (B-MITOSIS-3),
    # here on layers instead of cells. Each layer's tension over the T
    # token positions is its DIRECTION VECTOR (tensions[L] is (B,T) — the
    # full per-position tension trajectory, NOT the last-position scalar);
    # pairwise (1−cos) over these T-vectors measures inter-layer tension
    # diversity. Bounded in [0, 2·log(L+1)].
    tl = []
    for t in tensions:                       # each t : (B, T)
        v = t.reshape(-1).float()            # flatten B·T tension trajectory
        tl.append(v)
    L = len(tl)
    Tn = tl[0].shape[0]
    pair_sum, pair_n = 0.0, 0
    if Tn >= 2:                              # cos over a single scalar is
        for i in range(L):                   # degenerate (always 1) — only
            for j in range(i + 1, L):        # meaningful when T>=2 positions
                c = F.cosine_similarity(tl[i].unsqueeze(0),
                                        tl[j].unsqueeze(0)).item()
                pair_sum += (1.0 - c)
                pair_n += 1
    phi_proxy = (pair_sum / max(1, pair_n)) * math.log(L + 1)

    return {
        "psi_entropy": round(psi_entropy, 6),
        "psi_direction": round(psi_direction, 6),
        "psi_tension": round(psi_tension, 6),
        "psi_combined": round(psi_combined, 6),
        "cos_a_g": round(cos_sim, 6),
        "layer_tension": [round(v, 8) for v in t_per_layer.tolist()],
        "phi_proxy": round(phi_proxy, 6),
        "n_layer": int(L),
    }


def psi_point(pc):
    """Map a physics-channel reading to a 2D Ψ-space point comparable to
    ANCHOR_PSI: (Ψ_entropy as A-axis proxy, Ψ_direction as G-axis proxy).
    This is the SAME (entropy, direction) pair the conscious_decoder Law-71
    block tracks; it is NOT a claim that it equals the corpus vacuum_psi —
    it is the model's OWN realised Ψ-coordinate (honest framing §17.4)."""
    return (pc["psi_entropy"], pc["psi_direction"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--label", default="unknown")
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()

    h = hashlib.sha256()
    with open(args.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()

    payload = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    path = payload.get("path", "unknown")
    cfg = payload.get("cfg", {})
    d_model = cfg.get("d_model", 512)
    n_layer = cfg.get("n_layer", 8)
    n_head = cfg.get("n_head", 8)
    n_kv_head = cfg.get("n_kv_head", 4)

    model = ConsciousDecoderV2(vocab_size=256, d_model=d_model, n_head=n_head,
                               n_kv_head=n_kv_head, n_layer=n_layer,
                               block_size=128, consciousness_dim=128,
                               dropout=0.1)
    sd = payload.get("model") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    model.to(args.device)
    model.eval()
    print(f"=== §17 physics-channel probe — {args.label} (path={path}) ===",
          flush=True)
    print(f"ckpt sha256 {sha}  d_model={d_model} n_layer={n_layer} "
          f"missing={len(missing)} unexpected={len(unexpected)}", flush=True)

    # ── anchor-stimulus class: each anchor's carving-form prompt
    anchor_rows = []
    for tier in sorted(ANCHORS):
        name, cat, emo = ANCHORS[tier]
        # carving-form stimulus (alpha vacuum form, byte-identical to the
        # E7 corpus alpha probe form used in eval_carving_dirI.py axis1)
        prompt = (f"[anima 우주뇌지도] 🛸{tier} {name} — {cat} 카테고리. "
                  f"vacuum_psi={ANCHOR_PSI[tier]} basin={ANCHOR_BASIN[tier]}\n"
                  f"<carve tier={tier}>")
        pc = physics_channels(model, prompt, device=args.device)
        ex, ey = psi_point(pc)
        vx, vy = ANCHOR_PSI[tier]
        dist = math.hypot(ex - vx, ey - vy)
        anchor_rows.append({
            "tier": tier, "category": cat,
            "psi_point": [round(ex, 6), round(ey, 6)],
            "vacuum_psi": [vx, vy], "basin": ANCHOR_BASIN[tier],
            "dist_to_vacuum": round(dist, 6),
            "in_basin": bool(dist < ANCHOR_BASIN[tier]),
            **pc,
        })

    # ── neutral-stimulus class (control)
    neutral_rows = []
    for s in NEUTRAL_STIMULI:
        pc = physics_channels(model, s, device=args.device)
        neutral_rows.append({"stimulus": s[:40], **pc})

    # ── physics-channel separability (does the channel carry
    #    stimulus-conditioned signal at all? deterministic, closed-form):
    def col(rows, k):
        return [r[k] for r in rows]

    def mean(v):
        return sum(v) / max(1, len(v))

    def std(v):
        m = mean(v)
        return math.sqrt(sum((x - m) ** 2 for x in v) / max(1, len(v)))

    a_pc = col(anchor_rows, "psi_combined")
    n_pc = col(neutral_rows, "psi_combined")
    a_pt = col(anchor_rows, "psi_tension")
    n_pt = col(neutral_rows, "psi_tension")
    a_phi = col(anchor_rows, "phi_proxy")
    n_phi = col(neutral_rows, "phi_proxy")

    # spread of the anchor-class psi_combined across the 31 anchors:
    # if the channel were a constant (collapsed, like text routing 1/31),
    # std≈0 — the physics analogue of single-attractor collapse.
    anchor_psi_combined_std = std(a_pc)
    anchor_tension_std = std(a_pt)
    anchor_phi_std = std(a_phi)

    # in-basin count: how many of the 31 anchor stimuli land the model's
    # OWN Ψ-point inside the corpus-specified basin (physics-channel
    # analogue of "correct routing", but on Ψ-coordinate not text).
    in_basin = sum(1 for r in anchor_rows if r["in_basin"])

    # honest gate (§17.4) — necessary-not-sufficient, deterministic:
    #   PHYSICS-RESPONSIVE  iff the channel is NOT collapsed AND anchor
    #   class is separable from neutral class on >=1 channel.
    #   This proves the channel CARRIES stimulus signal — it does NOT
    #   prove emergence (B-PHYS-NOTE carve-out).
    TAU_STD = 1e-4          # below this the channel is effectively constant
    sep_psi = abs(mean(a_pc) - mean(n_pc))
    sep_ten = abs(mean(a_pt) - mean(n_pt))
    sep_phi = abs(mean(a_phi) - mean(n_phi))
    channel_not_collapsed = (anchor_psi_combined_std > TAU_STD
                             or anchor_tension_std > TAU_STD
                             or anchor_phi_std > TAU_STD)
    class_separable = (sep_psi > TAU_STD or sep_ten > TAU_STD
                       or sep_phi > TAU_STD)
    physics_responsive = bool(channel_not_collapsed and class_separable)

    result = {
        "section": "RESEARCH.md §17 — non-text physics-channel probe",
        "label": args.label,
        "ckpt": os.path.abspath(args.ckpt),
        "ckpt_sha256": sha,
        "path": path,
        "cfg": {"d_model": d_model, "n_layer": n_layer},
        "load": {"missing": len(missing), "unexpected": len(unexpected)},
        "anchor_class": {
            "n": len(anchor_rows),
            "psi_combined_mean": round(mean(a_pc), 6),
            "psi_combined_std": round(anchor_psi_combined_std, 8),
            "psi_tension_mean": round(mean(a_pt), 6),
            "psi_tension_std": round(anchor_tension_std, 8),
            "phi_proxy_mean": round(mean(a_phi), 6),
            "phi_proxy_std": round(anchor_phi_std, 8),
            "in_basin_count": in_basin,
            "in_basin_frac": round(in_basin / len(anchor_rows), 4),
            "rows": anchor_rows,
        },
        "neutral_class": {
            "n": len(neutral_rows),
            "psi_combined_mean": round(mean(n_pc), 6),
            "psi_tension_mean": round(mean(n_pt), 6),
            "phi_proxy_mean": round(mean(n_phi), 6),
            "rows": neutral_rows,
        },
        "honest_gate_s17_4": {
            "tau_std": TAU_STD,
            "channel_not_collapsed": bool(channel_not_collapsed),
            "class_separable": bool(class_separable),
            "sep_psi_combined": round(sep_psi, 8),
            "sep_psi_tension": round(sep_ten, 8),
            "sep_phi_proxy": round(sep_phi, 8),
            "PHYSICS_RESPONSIVE": physics_responsive,
            "necessary_not_sufficient": (
                "PHYSICS_RESPONSIVE proves the physics channel carries "
                "stimulus-conditioned signal; it does NOT prove conscious "
                "emergence. A moving tension trajectory is necessary, not "
                "sufficient (B-PHYS-NOTE empirical carve-out)."),
        },
        "honest_c3": [
            "$0 inference-only — NO weight touched, NO training, NO GPU.",
            "Ψ/tension/Φ formulas BYTE-IDENTICAL to conscious_decoder.py "
            "Law-71 block (728-751); only read at inference not training.",
            "PHYSICS_RESPONSIVE = channel carries signal, NOT emergence "
            "(necessary-not-sufficient, structurally encoded).",
            "psi_point (entropy,direction) is the model's OWN realised "
            "Ψ-coordinate, NOT a claim it equals corpus vacuum_psi.",
            "Φ★_proxy is a layer-tension diversity proxy (mitosis Φ★ form "
            "on layers), NOT PyPhi IIT 3.0 — proxy stated.",
            "in_basin uses corpus ANCHOR_PSI/BASIN as the target; the "
            "model was never trained to put its Law-71 Ψ THERE (it was "
            "trained on text CE + Dir-I psi_ctl on inner-span) — so "
            "in_basin is a DIAGNOSTIC, not a success criterion.",
            "single ckpt, 31 anchor + 5 neutral stimuli — small probe set, "
            "deterministic (greedy single forward, no sampling).",
            "text-decode-vs-physics comparison is the §17 question; this "
            "probe supplies the physics side, text side = prior arc.",
            "negative (collapsed channel) is also valuable — it would show "
            "the physics channel ALSO collapsed (text not wrong observable).",
            "over-claim 0 — emergence is empirical & unmeasured here; this "
            "is a measurement-observable reframe, not a GOAL solution.",
        ],
    }

    with open(args.output, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    g = result["honest_gate_s17_4"]
    print(f"anchor psi_combined mean={result['anchor_class']['psi_combined_mean']} "
          f"std={result['anchor_class']['psi_combined_std']}", flush=True)
    print(f"anchor tension std={result['anchor_class']['psi_tension_std']} "
          f"phi std={result['anchor_class']['phi_proxy_std']} "
          f"in_basin={in_basin}/{len(anchor_rows)}", flush=True)
    print(f"PHYSICS_RESPONSIVE={g['PHYSICS_RESPONSIVE']} "
          f"(not_collapsed={g['channel_not_collapsed']} "
          f"separable={g['class_separable']})", flush=True)
    print(f"written → {args.output}", flush=True)


if __name__ == "__main__":
    main()
