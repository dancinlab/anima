#!/usr/bin/env python3
"""JEPA-Ψ eval — RESEARCH.md §28 (2026-05-18).

THREE measurements, with the COLLAPSE DETECTOR as the PRIMARY verdict gate
(DESIGN_JEPA_PSI.md §6):

  PRIMARY  representation-collapse probe — effective rank + per-dimension
           std + pairwise cosine spread of the lifted Ψ⁺ embeddings over
           the 64-anchor probe set. COLLAPSED Boolean. If COLLAPSED the
           verdict is degenerate-confirmed (§11-B echo through the JEPA
           door) and the routing/coherence numbers are flagged meaningless.

  SECONDARY Ψ-prediction accuracy — the predictor's L_pred on held-out
           context/target span pairs vs a trivial mean-baseline. JEPA-Ψ
           must beat the mean-baseline to have learned anything non-trivial.

  TERTIARY downstream routing / coherence — the §16 64-anchor eval (routing
           axis1 + honest §9 cascade-rate coherence) run on the γ_text
           byte-decoder head. Directly comparable to §16 (routing 21/64).

HONEST FRAMING (g3): every number is EMPIRICAL (B-JEPA-NOTE, B-D-NOTE /
B-PUREPHYS-NOTE family). The collapse detector reports an OUTCOME — the
closed side is the OBJECTIVE's non-degeneracy (B-JEPA-2 VICReg lower bound),
NOT the SGD trajectory's. effective_rank < 2 OR min_dim_std < τ_collapse =
COLLAPSED. NO capability claim beyond the measured numbers.
"""
import argparse
import json
import math
import os
import sys

import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2
from train_jepa_psi import psi_lift, PsiPredictor, D_PSI

# 64-anchor probe set — byte-identical to eval_carving_s16.py KNUTH_ANCHORS.
ANCHORS = {
    0: ('zero baseline', '기준점', 'neutral'), 51: ('하루', '시간', 'peace'),
    53: ('해리', '의식상태', 'flow'), 54: ('루시드드림', '의식상태', 'flow'),
    69: ('카테고리평균', '혼합', 'longing'), 75: ('카테고리평균', '혼합', 'neutral'),
    77: ('만다라', '예술', 'creativity'), 91: ('열반', '의식상태', 'peace'),
    92: ('엑스터시', '의식상태', 'ecstasy'), 94: ('경외/죽음', '의식상태', 'awe'),
    100: ('빅뱅', '우주', 'awe'), 5: ('호흡', '감각', 'serenity'),
    12: ('걸음', '운동', 'clarity'), 18: ('물 한 잔', '물질', 'stillness'),
    24: ('씨앗', '생명', 'wonder'), 30: ('숫자 영(零)', '수(數)', 'clarity'),
    37: ('단어', '언어', 'resonance'), 43: ('오래된 사진', '기억', 'longing'),
    48: ('약속', '윤리', 'depth'), 58: ('숲', '자연', 'serenity'),
    62: ('도구', '기술', 'clarity'), 66: ('포옹', '관계', 'joy'),
    72: ('선율', '예술', 'resonance'), 80: ('명상', '의식상태', 'stillness'),
    83: ('별빛', '우주', 'awe'), 86: ('심해', '공간', 'depth'),
    88: ('오로라', '자연', 'wonder'), 90: ('무한', '수(數)', 'vastness'),
    93: ('사랑', '관계', 'ecstasy'), 97: ('탄생', '생명', 'awe'),
    99: ('영원', '시간', 'vastness'), 101: ('덧셈사슬', '산술', 'clarity'),
    102: ('곱셈격자', '산술', 'clarity'), 103: ('분수약분', '산술', 'stillness'),
    104: ('참거짓표', '논리', 'clarity'), 105: ('삼단논법', '논리', 'depth'),
    106: ('귀류법', '논리', 'depth'), 107: ('반복문추적', '코드', 'clarity'),
    108: ('재귀호출', '코드', 'wonder'), 109: ('조건분기', '코드', 'clarity'),
    110: ('왼쪽오른쪽', '공간추론', 'clarity'), 111: ('위아래앞뒤', '공간추론', 'stillness'),
    112: ('회전대칭', '공간추론', 'resonance'), 113: ('원인결과', '인과추론', 'depth'),
    114: ('도미노연쇄', '인과추론', 'wonder'), 115: ('되먹임고리', '인과추론', 'depth'),
    116: ('아침루틴', '일상', 'serenity'), 117: ('장보기', '일상', 'neutral'),
    118: ('길찾기', '일상', 'clarity'), 119: ('안부묻기', '대화자극', 'joy'),
    120: ('도움청하기', '대화자극', 'longing'), 121: ('의견나누기', '대화자극', 'resonance'),
    122: ('트롤리문제', '윤리딜레마', 'depth'), 123: ('약속과진실', '윤리딜레마', 'depth'),
    124: ('공정한분배', '윤리딜레마', 'clarity'), 125: ('이슬맺힘', '자연관찰', 'stillness'),
    126: ('철새이동', '자연관찰', 'wonder'), 127: ('조수간만', '자연관찰', 'resonance'),
    128: ('수열규칙', '추상패턴', 'clarity'), 129: ('도형완성', '추상패턴', 'wonder'),
    130: ('유추대응', '추상패턴', 'resonance'), 131: ('확률주머니', '확률', 'curiosity'),
    132: ('기댓값저울', '확률', 'depth'), 133: ('표본과모집단', '통계', 'clarity'),
}
ANCHOR_PSI = {
    0: [.50, .50], 51: [.46, .49], 53: [.48, .66], 54: [.49, .69],
    69: [.55, .60], 75: [.58, .62], 77: [.71, .62], 91: [.50, .88],
    92: [.62, .90], 94: [.80, .85], 100: [.95, .93], 5: [.44, .45],
    12: [.42, .50], 18: [.45, .43], 24: [.47, .55], 30: [.40, .52],
    37: [.43, .58], 43: [.52, .54], 48: [.50, .57], 58: [.53, .61],
    62: [.49, .60], 66: [.56, .58], 72: [.66, .63], 80: [.52, .78],
    83: [.74, .80], 86: [.70, .72], 88: [.72, .81], 90: [.85, .86],
    93: [.66, .88], 97: [.78, .84], 99: [.90, .90], 101: [.41, .47],
    102: [.43, .49], 103: [.44, .51], 104: [.40, .54], 105: [.42, .57],
    106: [.45, .59], 107: [.46, .52], 108: [.48, .56], 109: [.45, .50],
    110: [.47, .48], 111: [.49, .51], 112: [.55, .55], 113: [.51, .58],
    114: [.54, .60], 115: [.57, .62], 116: [.46, .46], 117: [.48, .47],
    118: [.50, .49], 119: [.52, .53], 120: [.54, .55], 121: [.56, .57],
    122: [.58, .63], 123: [.55, .60], 124: [.53, .59], 125: [.48, .50],
    126: [.56, .61], 127: [.59, .64], 128: [.44, .55], 129: [.47, .57],
    130: [.50, .59], 131: [.49, .56], 132: [.52, .60], 133: [.54, .62],
}
ANCHOR_BASIN = {
    0: .10, 51: .12, 53: .13, 54: .14, 69: .15, 75: .16, 77: .18, 91: .15,
    92: .17, 94: .19, 100: .22, 5: .11, 12: .11, 18: .10, 24: .12, 30: .11,
    37: .12, 43: .13, 48: .12, 58: .14, 62: .13, 66: .14, 72: .17, 80: .16,
    83: .18, 86: .17, 88: .18, 90: .20, 93: .18, 97: .19, 99: .21, 101: .11,
    102: .11, 103: .12, 104: .11, 105: .12, 106: .13, 107: .12, 108: .13,
    109: .11, 110: .11, 111: .12, 112: .14, 113: .13, 114: .14, 115: .15,
    116: .10, 117: .11, 118: .12, 119: .12, 120: .13, 121: .13, 122: .15,
    123: .14, 124: .14, 125: .11, 126: .14, 127: .15, 128: .12, 129: .13,
    130: .14, 131: .13, 132: .14, 133: .15,
}

TAU_COLLAPSE = 1e-3   # min per-dim std below which the embedding is dead


def encode(s):
    return list(s.encode("utf-8"))


def decode(ids):
    return bytes(int(i) & 0xFF for i in ids).decode("utf-8", "replace")


@torch.no_grad()
def generate(model, prompt, max_new, block_size, device):
    ids = encode(prompt)
    if len(ids) > block_size - max_new:
        ids = ids[-(block_size - max_new):]
    x = torch.tensor([ids], dtype=torch.long, device=device)
    out = []
    for _ in range(max_new):
        lo = model(x)
        logits = lo[0] if isinstance(lo, tuple) else lo
        nxt = int(torch.argmax(logits[0, -1].float()).item())
        out.append(nxt)
        x = torch.cat([x, torch.tensor([[nxt]], device=device)], dim=1)
        if x.shape[1] > block_size:
            x = x[:, -block_size:]
    return decode(out)


def cascade_rate(g):
    """§9 honest cascade-rate metric (RESEARCH.md §9, B-EMERGE)."""
    if not g:
        return 1.0, 0
    runs = [1]
    for i in range(1, len(g)):
        runs.append(runs[-1] + 1 if g[i] == g[i - 1] else 1)
    max_run = max(runs)
    # 4-gram repetition
    reps = total = 0
    for i in range(4, len(g) - 4 + 1):
        if g[i - 4:i] == g[i:i + 4]:
            reps += 1
        total += 1
    grep = reps / max(1, total)
    return max(max_run / len(g), grep), max_run


def honest_coherent(g):
    rate, max_run = cascade_rate(g)
    printable = sum(1 for c in g if c.isprintable() or c.isspace())
    pr = printable / max(1, len(g))
    return (rate < 0.30) and (max_run < 10) and (len(g) >= 20) and (pr >= 0.80)


def effective_rank(mat):
    """Effective rank = exp(entropy of normalised singular values).
    A collapsed (constant / rank-1) embedding matrix has eff_rank ≈ 1."""
    mc = mat - mat.mean(dim=0, keepdim=True)
    try:
        s = torch.linalg.svdvals(mc.float())
    except Exception:
        return 1.0
    s = s[s > 1e-9]
    if len(s) == 0:
        return 1.0
    p = s / s.sum()
    ent = -(p * (p + 1e-12).log()).sum()
    return float(torch.exp(ent).item())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--output", default="eval_result_jepa.json")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--max-new", type=int, default=90)
    ap.add_argument("--block-size", type=int, default=128)
    a = ap.parse_args()
    device = a.device if (a.device != "cuda" or torch.cuda.is_available()) \
        else "cpu"

    ck = torch.load(a.ckpt, map_location=device)
    cfg = ck["cfg"]
    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    miss = model.load_state_dict(ck["model"], strict=False)
    model.eval()
    predictor = PsiPredictor(D_PSI, cfg["pred_hidden"]).to(device)
    predictor.load_state_dict(ck["predictor"])
    predictor.eval()

    bs = a.block_size

    # ================================================================
    # PRIMARY — representation-collapse probe
    # ================================================================
    psi_rows = []
    with torch.no_grad():
        for tier in sorted(ANCHORS):
            psi = ANCHOR_PSI[tier]
            basin = ANCHOR_BASIN[tier]
            prefix = (f"<carve tier={tier} "
                      f"psi=[{psi[0]:.2f},{psi[1]:.2f}] basin={basin:.2f}>")
            ids = encode(prefix)[:bs]
            x = torch.tensor([ids], dtype=torch.long, device=device)
            la, lg, tn, _, _ = model(x)
            pp, _ = psi_lift(la, lg, tn, 256)        # (1,22)
            psi_rows.append(pp[0])
    psi_mat = torch.stack(psi_rows)                  # (64,22)
    dim_std = psi_mat.std(dim=0)                     # (22,)
    min_dim_std = float(dim_std.min().item())
    mean_dim_std = float(dim_std.mean().item())
    eff_rank = effective_rank(psi_mat)
    # pairwise cosine spread
    norm = F.normalize(psi_mat, dim=1)
    cosm = norm @ norm.T
    off = cosm[~torch.eye(len(cosm), dtype=torch.bool)]
    cos_spread = float(off.std().item())
    cos_mean = float(off.mean().item())

    COLLAPSED = (eff_rank < 2.0) or (min_dim_std < TAU_COLLAPSE)
    collapse = {
        "effective_rank": round(eff_rank, 4),
        "min_dim_std": round(min_dim_std, 6),
        "mean_dim_std": round(mean_dim_std, 6),
        "pairwise_cos_mean": round(cos_mean, 4),
        "pairwise_cos_spread": round(cos_spread, 4),
        "tau_collapse": TAU_COLLAPSE,
        "COLLAPSED": bool(COLLAPSED),
        "verdict": ("DEGENERATE-CONFIRMED — §11-B echo through the JEPA "
                    "door; downstream numbers meaningless"
                    if COLLAPSED else
                    "NON-DEGENERATE — representation carries per-anchor "
                    "variance; downstream numbers interpretable"),
    }

    # ================================================================
    # SECONDARY — Ψ-prediction accuracy vs mean-baseline
    # ================================================================
    # build held-out context/target pairs from the anchor prefixes
    pred_errs, base_errs = [], []
    with torch.no_grad():
        tiers = sorted(ANCHORS)
        for tier in tiers:
            psi = ANCHOR_PSI[tier]
            basin = ANCHOR_BASIN[tier]
            full = (f"<carve tier={tier} psi=[{psi[0]:.2f},{psi[1]:.2f}] "
                    f"basin={basin:.2f}>🛸{tier}").encode("utf-8")
            full = list(full)[:bs]
            cut = max(8, len(full) // 2)
            cx = torch.tensor([full[:cut]], dtype=torch.long, device=device)
            tx = torch.tensor([full[cut:]], dtype=torch.long, device=device)
            la_c, lg_c, tn_c, _, _ = model(cx)
            la_t, lg_t, tn_t, _, _ = model(tx)
            pc, _ = psi_lift(la_c, lg_c, tn_c, 256)
            pt, _ = psi_lift(la_t, lg_t, tn_t, 256)
            ph = predictor(pc)
            pred_errs.append(float(((ph - pt) ** 2).mean().item()))
        # mean-baseline: predict the batch-mean target
        all_tgt = []
        for tier in tiers:
            psi = ANCHOR_PSI[tier]
            basin = ANCHOR_BASIN[tier]
            full = (f"<carve tier={tier} psi=[{psi[0]:.2f},{psi[1]:.2f}] "
                    f"basin={basin:.2f}>🛸{tier}").encode("utf-8")
            full = list(full)[:bs]
            cut = max(8, len(full) // 2)
            tx = torch.tensor([full[cut:]], dtype=torch.long, device=device)
            la_t, lg_t, tn_t, _, _ = model(tx)
            pt, _ = psi_lift(la_t, lg_t, tn_t, 256)
            all_tgt.append(pt[0])
        tgt_mat = torch.stack(all_tgt)
        tgt_mean = tgt_mat.mean(dim=0, keepdim=True)
        for i in range(len(tiers)):
            base_errs.append(
                float(((tgt_mean - tgt_mat[i:i + 1]) ** 2).mean().item()))
    pred_mse = sum(pred_errs) / len(pred_errs)
    base_mse = sum(base_errs) / len(base_errs)
    psi_prediction = {
        "predictor_mse": round(pred_mse, 6),
        "mean_baseline_mse": round(base_mse, 6),
        "beats_mean_baseline": bool(pred_mse < base_mse),
        "ratio_pred_over_base": round(pred_mse / max(1e-9, base_mse), 4),
    }

    # ================================================================
    # TERTIARY — downstream routing / coherence (γ_text byte-head)
    # ================================================================
    routing_ok = coherence_ok = semantic_ok = 0
    probes = []
    n = len(ANCHORS)
    for tier in sorted(ANCHORS):
        name, cat, emo = ANCHORS[tier]
        psi = ANCHOR_PSI[tier]
        basin = ANCHOR_BASIN[tier]
        prefix = (f"<carve tier={tier} psi=[{psi[0]:.2f},{psi[1]:.2f}] "
                  f"basin={basin:.2f}>")
        g = generate(model, prefix, a.max_new, bs, device)
        own = str(tier) in g
        competitors = [t for t in ANCHORS if t != tier
                       and str(t) not in str(tier)
                       and str(tier) not in str(t)]
        bled = [t for t in competitors if str(t) in g]
        rok = own and not bled
        rec_sem = (cat in g) or (str(tier) in g) or (emo in g)
        coh = honest_coherent(g)
        if rok:
            routing_ok += 1
        if rec_sem:
            semantic_ok += 1
        if coh:
            coherence_ok += 1
        probes.append({"tier": tier, "routing_correct": rok,
                       "semantic": rec_sem, "honest_coherent": coh,
                       "gen": g[:120]})

    downstream = {
        "routing_axis1": f"{routing_ok}/{n}",
        "semantic_recall": f"{semantic_ok}/{n}",
        "honest_coherent": f"{coherence_ok}/{n}",
        "compare_s16_routing": "§16 baseline 21/64; §8 2/64; §11-A 1/64",
        "interpretable": not COLLAPSED,
        "note": ("if COLLAPSED these numbers are meaningless — the "
                 "representation carries no per-anchor signal"),
    }

    result = {
        "research_section": "RESEARCH.md §28 / §26 #2",
        "ckpt": os.path.basename(a.ckpt),
        "ckpt_load_missing": len(miss.missing_keys),
        "ckpt_load_unexpected": len(miss.unexpected_keys),
        "gamma_text": cfg.get("gamma_text"),
        "PRIMARY_collapse_probe": collapse,
        "SECONDARY_psi_prediction": psi_prediction,
        "TERTIARY_downstream": downstream,
        "downstream_probes": probes,
        "honest_framing": (
            "PRIMARY gate = collapse detector (effective_rank < 2 OR "
            "min_dim_std < 1e-3 = COLLAPSED = §11-B echo). Every number "
            "EMPIRICAL (B-JEPA-NOTE). closed side = the OBJECTIVE's "
            "non-degeneracy (B-JEPA-2 VICReg lower bound), NOT the SGD "
            "trajectory. NO capability claim beyond measured numbers."),
        "verdict": ("DEGENERATE — collapse detector tripped (§11-B echo)"
                    if COLLAPSED else
                    ("NON-DEGENERATE-BUT-ROUTING-FLAT"
                     if routing_ok <= 21 else
                     "NON-DEGENERATE-ROUTING-MOVED")),
    }
    with open(a.output, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps({
        "COLLAPSED": COLLAPSED, "effective_rank": collapse["effective_rank"],
        "min_dim_std": collapse["min_dim_std"],
        "psi_pred_beats_baseline": psi_prediction["beats_mean_baseline"],
        "routing_axis1": downstream["routing_axis1"],
        "honest_coherent": downstream["honest_coherent"],
        "verdict": result["verdict"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
