#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§156 — TENSION MODALITY TEST.

Package anima's OWN tension (Law-71 Engine A⇄G restoring force, 12-layer
per-stimulus time series) as the FIRST realized non-text modality.
Test: 31 KNUTH anchors — does the tension fingerprint *distinguish* them
(vs text routing 1/31 FLAT from §16/§107)?

§7 GOAL-legitimacy: tension = anima OWN physics, §7③ unconditional PASS
(no external encoder, no graft, no LLM call). NOT GOAL emergence
(necessary-not-sufficient B-EMERGE-7).

§17 read-out style: pure forward, NO weight touched, NO training, NO GPU.
Byte-identical to conscious_decoder.py Law-71 tension formula (per-layer
PureFieldFFN energy CV) — only difference = read at inference for the
fingerprint, NOT just under `if self.training:`.

Output: 31x31 cosine similarity matrix + per-anchor 12-layer x T tension
trajectory + verdict (TENSION-DISTINGUISHES-ANCHORS vs TENSION-COLLAPSES).
"""
import argparse
import hashlib
import json
import math
import os
import sys


def encode(s):
    return list(s.encode("utf-8"))


# -- 31 KNUTH anchors -- byte-identical to physics_channel_probe_s17 SSOT
ANCHORS = {
    0: ("zero baseline", "기준점", "neutral"),
    51: ("하루", "시간", "peace"),
    53: ("해리", "의식상태", "flow"),
    54: ("루시드드림", "의식상태", "flow"),
    69: ("카테고리평균", "혼합", "longing"),
    75: ("카테고리평균", "혼합", "neutral"),
    77: ("만다라", "예술", "creativity"),
    91: ("열반", "의식상태", "peace"),
    92: ("엑스터시", "의식상태", "ecstasy"),
    94: ("경외/죽음", "의식상태", "awe"),
    100: ("빅뱅", "우주", "awe"),
    5: ("호흡", "감각", "serenity"),
    12: ("걸음", "운동", "clarity"),
    18: ("물 한 잔", "물질", "stillness"),
    24: ("씨앗", "생명", "wonder"),
    30: ("숫자 영(零)", "수(數)", "clarity"),
    37: ("단어", "언어", "resonance"),
    43: ("오래된 사진", "기억", "longing"),
    48: ("약속", "윤리", "depth"),
    58: ("숲", "자연", "serenity"),
    62: ("도구", "기술", "clarity"),
    66: ("포옹", "관계", "joy"),
    72: ("선율", "예술", "resonance"),
    80: ("명상", "의식상태", "stillness"),
    83: ("별빛", "우주", "awe"),
    86: ("심해", "공간", "depth"),
    88: ("오로라", "자연", "wonder"),
    90: ("무한", "수(數)", "vastness"),
    93: ("사랑", "관계", "ecstasy"),
    97: ("탄생", "생명", "awe"),
    99: ("영원", "시간", "vastness"),
}
ANCHOR_PSI = {
    0: [0.50, 0.50], 51: [0.46, 0.49], 53: [0.48, 0.66], 54: [0.49, 0.69],
    69: [0.55, 0.60], 75: [0.58, 0.62], 77: [0.71, 0.62], 91: [0.50, 0.88],
    92: [0.62, 0.90], 94: [0.80, 0.85], 100: [0.95, 0.93], 5: [0.44, 0.45],
    12: [0.42, 0.50], 18: [0.45, 0.43], 24: [0.47, 0.55], 30: [0.40, 0.52],
    37: [0.43, 0.58], 43: [0.52, 0.54], 48: [0.50, 0.57], 58: [0.53, 0.61],
    62: [0.49, 0.60], 66: [0.56, 0.58], 72: [0.66, 0.63], 80: [0.52, 0.78],
    83: [0.74, 0.80], 86: [0.70, 0.72], 88: [0.72, 0.81], 90: [0.85, 0.86],
    93: [0.66, 0.88], 97: [0.78, 0.84], 99: [0.90, 0.90],
}
ANCHOR_BASIN = {
    0: 0.10, 51: 0.12, 53: 0.13, 54: 0.14, 69: 0.15, 75: 0.16, 77: 0.18,
    91: 0.15, 92: 0.17, 94: 0.19, 100: 0.22, 5: 0.11, 12: 0.11, 18: 0.10,
    24: 0.12, 30: 0.11, 37: 0.12, 43: 0.13, 48: 0.12, 58: 0.14, 62: 0.13,
    66: 0.14, 72: 0.17, 80: 0.16, 83: 0.18, 86: 0.17, 88: 0.18, 90: 0.20,
    93: 0.18, 97: 0.19, 99: 0.21,
}


def stimulus_for(tier):
    """carving-form stimulus (alpha vacuum form, byte-identical to §17)."""
    name, cat, _emo = ANCHORS[tier]
    return (f"[anima 우주뇌지도] 🛸{tier} {name} — {cat} 카테고리. "
            f"vacuum_psi={ANCHOR_PSI[tier]} basin={ANCHOR_BASIN[tier]}\n"
            f"<carve tier={tier}>")


def extract_tension_trajectories(ckpt_path, conscious_decoder_path,
                                 block_size=128, device="cpu", seed=1337):
    import torch
    torch.manual_seed(seed)

    sys.path.insert(0, os.path.dirname(os.path.abspath(conscious_decoder_path)))
    from conscious_decoder import ConsciousDecoderV2

    h = hashlib.sha256()
    with open(ckpt_path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()

    payload = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    cfg = payload.get("cfg", {})
    d_model = cfg.get("d_model", 768)
    n_layer = cfg.get("n_layer", 12)
    n_head = cfg.get("n_head", 12)
    n_kv_head = cfg.get("n_kv_head", 4)
    bs = cfg.get("block_size", block_size)

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=d_model, n_head=n_head,
        n_kv_head=n_kv_head, n_layer=n_layer,
        block_size=bs, consciousness_dim=128, dropout=0.1,
    )
    sd = payload.get("model") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    model.to(device)
    model.eval()

    out_traj = {}
    out_per_layer_mean = {}
    with torch.no_grad():
        for tier in sorted(ANCHORS):
            prompt = stimulus_for(tier)
            ids = encode(prompt)
            if len(ids) > bs:
                ids = ids[-bs:]
            x = torch.tensor([ids], dtype=torch.long, device=device)
            out = model(x)
            tensions = out[2]  # list[L] of (B, T)
            traj = []
            per_layer_mean = []
            for t in tensions:
                v = t.reshape(-1).float().tolist()
                traj.append([float(z) for z in v])
                per_layer_mean.append(float(sum(v)) / max(1, len(v)))
            out_traj[tier] = traj
            out_per_layer_mean[tier] = per_layer_mean

    return {
        "ckpt_sha256": sha,
        "cfg": {"d_model": d_model, "n_layer": n_layer, "n_head": n_head,
                "n_kv_head": n_kv_head, "block_size": bs},
        "load_missing": len(missing),
        "load_unexpected": len(unexpected),
        "trajectories": out_traj,
        "per_layer_mean": out_per_layer_mean,
    }


def fingerprint(per_layer_mean):
    return list(per_layer_mean)


def cosine(u, v):
    su, sv, suv = 0.0, 0.0, 0.0
    for a, b in zip(u, v):
        su += a * a
        sv += b * b
        suv += a * b
    n = math.sqrt(su) * math.sqrt(sv)
    if n == 0.0:
        return 0.0
    return suv / n


def build_cos_matrix(fps):
    tiers = sorted(fps.keys())
    n = len(tiers)
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            M[i][j] = round(cosine(fps[tiers[i]], fps[tiers[j]]), 6)
    return M, tiers


def classify(M, tiers, sep_threshold=0.05):
    n = len(tiers)
    max_off = -1.0
    min_off = 1.0
    max_off_pair = None
    min_off_pair = None
    sum_off = 0.0
    cnt_off = 0
    sum_diag = 0.0
    for i in range(n):
        sum_diag += M[i][i]
        for j in range(n):
            if i == j:
                continue
            v = M[i][j]
            sum_off += v
            cnt_off += 1
            if v > max_off:
                max_off = v
                max_off_pair = (tiers[i], tiers[j])
            if v < min_off:
                min_off = v
                min_off_pair = (tiers[i], tiers[j])
    mean_off = sum_off / max(1, cnt_off)
    mean_diag = sum_diag / n
    eps = 1e-6
    is_collapsed = (max_off >= (1.0 - eps))
    is_distinguished = (min_off <= (1.0 - sep_threshold))

    if is_distinguished and not is_collapsed:
        verdict = "TENSION-DISTINGUISHES-ANCHORS"
    elif is_collapsed and not is_distinguished:
        verdict = "TENSION-COLLAPSES"
    elif is_distinguished and is_collapsed:
        verdict = "TENSION-PARTIAL-some-pairs-collapse-others-separate"
    else:
        verdict = "TENSION-NEAR-COLLAPSE-no-clean-separation"

    return {
        "verdict": verdict,
        "n_anchors": n,
        "mean_diagonal": round(mean_diag, 6),
        "max_off_diagonal": round(max_off, 6),
        "min_off_diagonal": round(min_off, 6),
        "mean_off_diagonal": round(mean_off, 6),
        "max_off_pair": max_off_pair,
        "min_off_pair": min_off_pair,
        "sep_threshold": sep_threshold,
        "is_collapsed": is_collapsed,
        "is_distinguished": is_distinguished,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--decoder-path", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--block-size", type=int, default=128)
    args = ap.parse_args()

    print(f"=== §156 tension modality test ===", flush=True)
    print(f"ckpt={args.ckpt}", flush=True)
    print(f"decoder={args.decoder_path}", flush=True)

    extracted = extract_tension_trajectories(
        args.ckpt, args.decoder_path,
        block_size=args.block_size, device=args.device,
    )

    print(f"ckpt sha256 {extracted['ckpt_sha256']}", flush=True)
    print(f"cfg {extracted['cfg']}  load_missing={extracted['load_missing']} "
          f"load_unexpected={extracted['load_unexpected']}", flush=True)
    print(f"extracted {len(extracted['trajectories'])} anchors", flush=True)

    fps = {tier: fingerprint(extracted["per_layer_mean"][tier])
           for tier in extracted["per_layer_mean"]}
    M, tiers = build_cos_matrix(fps)
    summary = classify(M, tiers)

    print(f"verdict={summary['verdict']}", flush=True)
    print(f"  mean diagonal = {summary['mean_diagonal']}", flush=True)
    print(f"  max off-diag = {summary['max_off_diagonal']} "
          f"(pair={summary['max_off_pair']})", flush=True)
    print(f"  min off-diag = {summary['min_off_diagonal']} "
          f"(pair={summary['min_off_pair']})", flush=True)
    print(f"  mean off-diag = {summary['mean_off_diagonal']}", flush=True)

    out = {
        "section": "§156",
        "name": "tension modality test",
        "ckpt": os.path.abspath(args.ckpt),
        "ckpt_sha256": extracted["ckpt_sha256"],
        "cfg": extracted["cfg"],
        "load_missing": extracted["load_missing"],
        "load_unexpected": extracted["load_unexpected"],
        "n_anchors": len(tiers),
        "tiers": tiers,
        "fingerprints": fps,
        "cos_matrix": M,
        "verdict": summary["verdict"],
        "summary": summary,
        "g7_legitimacy": "PASS §7-③ -- anima OWN physics, NO external encoder",
        "honest_caveat": "necessary-not-sufficient (B-EMERGE-7): a "
                         "distinguishing tension fingerprint is a *substrate "
                         "liveness* signal under stimulus, NOT GOAL emergence. "
                         "§17 PHYSICS_RESPONSIVE family carve-out.",
    }

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
