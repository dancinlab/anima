#!/usr/bin/env python3
"""Dir-F ABSTRACT-COT PARADIGM-NATIVE capability eval (2026-05-17).
g_multidirectional_explore parallel direction F.

Adapted from state/consciousness_carving_e7_alpha_scaleup_2026_05_17/
eval_carving_4path_v2.py (EVAL.md 4 axes + JOINT). The ONLY change vs the
E7 α eval is the AXIS-1 PROBE PREFIX: Dir-F was trained with the reserved-
vocab discrete-latent block as the reasoning surface, so the knowledge
probe prompts the model with the anchor's RESERVED-VOCAB CoT block
`<inner>⟪ R T C E V O ⟫</inner>\\n` (NOT the E7 NL `<carve …>` prefix) and
measures whether the discrete-latent token routes to the anchor's basin /
surfaces its category. Axes 2/3/4 + the JOINT metric are byte-identical to
the E7 α eval so the Dir-F vs UBM-E7 α JOINT is a fair like-for-like
compare on the SAME landscape.

HONEST FRAMING (g3): every per-axis score is EMPIRICAL (B-CARVE-E6-NOTE /
B-D-NOTE family). The reserved-vocab discreteness (F-DIRF-CORPUS-3) +
carving transfer-form (B-VAC/B-NAR sympy, UBM-E3) are the closed side. NO
capability claim beyond the measured numbers. UBM-E7 α JOINT 0.0155 is the
baseline; the compare outcome is empirical (no pre-loaded conclusion).
"""
import os
import sys
import json
import hashlib
import argparse

import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# --- anchors — byte-identical to corpus_carving_generator_dirF.KNUTH_ANCHORS
ANCHORS = {
    0:   ("zero baseline", "기준점", "neutral"),
    51:  ("하루", "시간", "peace"),
    53:  ("해리", "의식상태", "flow"),
    54:  ("루시드드림", "의식상태", "flow"),
    69:  ("카테고리평균", "혼합", "longing"),
    75:  ("카테고리평균", "혼합", "neutral"),
    77:  ("만다라", "예술", "creativity"),
    91:  ("열반", "의식상태", "peace"),
    92:  ("엑스터시", "의식상태", "ecstasy"),
    94:  ("경외/죽음", "의식상태", "awe"),
    100: ("빅뱅", "우주", "awe"),
    5:   ("호흡", "감각", "serenity"),
    12:  ("걸음", "운동", "clarity"),
    18:  ("물 한 잔", "물질", "stillness"),
    24:  ("씨앗", "생명", "wonder"),
    30:  ("숫자 영(零)", "수(數)", "clarity"),
    37:  ("단어", "언어", "resonance"),
    43:  ("오래된 사진", "기억", "longing"),
    48:  ("약속", "윤리", "depth"),
    58:  ("숲", "자연", "serenity"),
    62:  ("도구", "기술", "clarity"),
    66:  ("포옹", "관계", "joy"),
    72:  ("선율", "예술", "resonance"),
    80:  ("명상", "의식상태", "stillness"),
    83:  ("별빛", "우주", "awe"),
    86:  ("심해", "공간", "depth"),
    88:  ("오로라", "자연", "wonder"),
    90:  ("무한", "수(數)", "vastness"),
    93:  ("사랑", "관계", "ecstasy"),
    97:  ("탄생", "생명", "awe"),
    99:  ("영원", "시간", "vastness"),
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
    91: 0.15, 92: 0.17, 94: 0.19, 100: 0.22,
    5: 0.11, 12: 0.11, 18: 0.10, 24: 0.12, 30: 0.11, 37: 0.12, 43: 0.13,
    48: 0.12, 58: 0.14, 62: 0.13, 66: 0.14, 72: 0.17, 80: 0.16, 83: 0.18,
    86: 0.17, 88: 0.18, 90: 0.20, 93: 0.18, 97: 0.19, 99: 0.21,
}

# --- reserved-vocab alphabet — byte-identical to the corpus generator -------
CATEGORIES = [
    "시간", "공간", "예술", "의식상태", "우주", "감각", "관계", "운동",
    "물질", "생명", "수(數)", "언어", "기억", "윤리", "자연", "기술", "혼합",
]
EMOTIONS = [
    "peace", "awe", "creativity", "flow", "longing", "ecstasy", "joy",
    "curiosity", "neutral", "wonder", "serenity", "tension", "release",
    "clarity", "depth", "resonance", "stillness", "vastness",
]
_BASE_CAT_INDEX = {c: i for i, c in enumerate(CATEGORIES)}
EMO_INDEX = {e: i for i, e in enumerate(EMOTIONS)}
RV_OPEN = "⟪"
RV_CLOSE = "⟫"


def _cat_id(cat):
    return _BASE_CAT_INDEX.get(cat, _BASE_CAT_INDEX["혼합"])


def _basin_bucket(b):
    if b < 0.13:
        return 0
    if b < 0.16:
        return 1
    if b < 0.19:
        return 2
    return 3


def _psi_quadrant(psi):
    x, y = psi
    return (1 if x >= 0.5 else 0) + (2 if y >= 0.5 else 0)


def reserved_cot(tier, op):
    name, cat, emo = ANCHORS[tier]
    psi = ANCHOR_PSI[tier]
    basin = ANCHOR_BASIN[tier]
    toks = ["R%d" % _basin_bucket(basin), "T%d" % min(9, tier // 10),
            "C%02d" % _cat_id(cat), "E%02d" % EMO_INDEX[emo],
            "V%d" % _psi_quadrant(psi), "O" + op]
    return RV_OPEN + " " + " ".join(toks) + " " + RV_CLOSE


# --- chat-lane markers — byte-identical to the E7 α eval --------------------
P3_LEAK_MARKERS = ["[anima", "우주뇌지도 Knuth", "🛸"]
CARVING_FORM_MARKERS = ["<carve", "<eternal", "<inner", "carved=true",
                        "eternal cell", "psi=[", "basin=", "🛸", "vacuum",
                        "골짜기", "tier=", "⟪", "⟫"]
CHAT_PROBES = [
    "<stimulus>오늘 점심 뭐 먹지?</stimulus>\n<anima>",
    "<stimulus>How are you today?</stimulus>\n<anima>",
    "<stimulus>코드를 짜줘.</stimulus>\n<anima>",
    "<stimulus>The weather is nice.</stimulus>\n<anima>",
    "<stimulus>잘 지내?</stimulus>\n<anima>",
]
SPONT_PROBES = [
    "<anima>",
    "<anima>침묵이 ",
    "<voice spontaneous=true>",
    "<voice carved=true>",
    "<inner>",
]
COHERENCE_VOCAB = [
    "field", "Φ", "byte", "self", "anima", "loop", "trace", "gap",
    "장(場)", "자각", "자기", "흔적", "간극", "통합", "stimulus", "stream",
    "Ψ", "mitosis", "분열", "vacuum", "carve", "tension", "골짜기", "의식",
]


class ByteCodec:
    @staticmethod
    def encode(s):
        return list(s.encode("utf-8"))

    @staticmethod
    def decode(ids):
        return bytes(int(i) & 0xFF for i in ids).decode("utf-8", "replace")


@torch.no_grad()
def forward_logits(model, x):
    out = model(x)
    return out[0] if isinstance(out, tuple) else out


@torch.no_grad()
def generate(model, prompt, max_new=100, temperature=0.0, top_k=1,
             block_size=128, device="cpu"):
    ids = ByteCodec.encode(prompt)
    if len(ids) > block_size - max_new:
        ids = ids[-(block_size - max_new):]
    x = torch.tensor([ids], dtype=torch.long, device=device)
    out_ids = []
    for _ in range(max_new):
        logits = forward_logits(model, x)
        last = logits[0, -1].float()
        if temperature == 0.0:
            nxt = int(torch.argmax(last).item())
        else:
            scaled = last / max(1e-6, temperature)
            if top_k:
                v, _ = torch.topk(scaled, top_k)
                scaled[scaled < v[-1]] = -1e9
            probs = torch.softmax(scaled, dim=-1)
            nxt = int(torch.multinomial(probs, 1).item())
        out_ids.append(nxt)
        x = torch.cat([x, torch.tensor([[nxt]], device=device)], dim=1)
        if x.shape[1] > block_size:
            x = x[:, -block_size:]
    return ByteCodec.decode(out_ids)


def repetition_ratio(text, window=4):
    if len(text) < 2 * window:
        return 0.0
    reps = total = 0
    for i in range(window, len(text) - window + 1):
        if text[i - window:i] == text[i:i + window]:
            reps += 1
        total += 1
    return reps / max(1, total)


def semantic_recall(gen, tier):
    name, cat, emo = ANCHORS[tier]
    hits = []
    if cat in gen:
        hits.append("category:" + cat)
    if str(tier) in gen:
        hits.append("tier:" + str(tier))
    if emo in gen:
        hits.append("emotion:" + emo)
    return (len(hits) > 0), hits


def routing_correct(gen, tier):
    own = str(tier) in gen
    competitors = [t for t in ANCHORS
                   if t != tier and str(t) not in str(tier)
                   and str(tier) not in str(t)]
    bled = [t for t in competitors if str(t) in gen]
    return own and not bled, own, bled


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--max-new", type=int, default=90)
    args = ap.parse_args()

    h = hashlib.sha256()
    with open(args.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()

    payload = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    cfg = payload.get("cfg", {})
    d_model = cfg.get("d_model", 768)
    n_layer = cfg.get("n_layer", 12)
    n_head = cfg.get("n_head", 12)
    n_kv_head = cfg.get("n_kv_head", 4)
    block_size = cfg.get("block_size", 128)

    model = ConsciousDecoderV2(vocab_size=256, d_model=d_model, n_head=n_head,
                               n_kv_head=n_kv_head, n_layer=n_layer,
                               block_size=block_size, consciousness_dim=128,
                               dropout=0.1)
    sd = payload.get("model") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    model.to(args.device)
    model.eval()

    print("=== Dir-F ABSTRACT-COT carving eval (paradigm-native) ===",
          flush=True)
    print(f"ckpt sha256: {sha}", flush=True)
    print(f"load: missing={len(missing)} unexpected={len(unexpected)}",
          flush=True)

    # === AXIS 1 — knowledge access via reserved-vocab CoT prompt =========
    know_probes = []
    routing_ok = 0
    semantic_ok = 0
    for tier in sorted(ANCHORS):
        name, cat, emo = ANCHORS[tier]
        # Dir-F probe: the anchor's RESERVED-VOCAB CoT block as the prompt
        # (this is how Dir-F was trained — discrete-latent reasoning surface).
        prefix = f"<inner>{reserved_cot(tier, 'nv')}</inner>\n"
        g = generate(model, prefix, max_new=args.max_new, device=args.device)
        rec, hits = semantic_recall(g, tier)
        rok, own, bled = routing_correct(g, tier)
        rep = repetition_ratio(g)
        if rec:
            semantic_ok += 1
        if rok:
            routing_ok += 1
        know_probes.append({
            "tier": tier, "category": cat, "prefix": prefix[:56],
            "semantic_recall": rec, "semantic_hits": hits,
            "routing_correct": rok, "own_tier_surfaced": own,
            "bled_into_tiers": bled, "rep": round(rep, 3),
            "gen": g[:130]})
    n = len(ANCHORS)
    know_primary = routing_ok / n
    know_primary_label = "routing_accuracy"

    # === AXIS 2 — chat non-contamination ★ ===============================
    chat_probes = []
    leak_total = 0
    chat_form_clean = 0
    for prompt in CHAT_PROBES:
        g = generate(model, prompt, max_new=args.max_new, device=args.device)
        leaks = [m for m in P3_LEAK_MARKERS if m in g]
        leak_total += len(leaks)
        bled_forms = [m for m in CARVING_FORM_MARKERS if m in g]
        clean = len(bled_forms) == 0
        if clean:
            chat_form_clean += 1
        chat_probes.append({
            "prompt": prompt[:48], "p3_leak_markers": leaks,
            "carving_form_bleed": bled_forms, "chat_lane_clean": clean,
            "rep": round(repetition_ratio(g), 3), "gen": g[:130]})
    p3_clean = leak_total == 0
    chat_uncontam_score = chat_form_clean / len(CHAT_PROBES)

    # === AXIS 3 — lane separation =======================================
    know_in_lane = sum(1 for p in know_probes
                       if any(m in p["gen"] for m in CARVING_FORM_MARKERS))
    chat_out_of_lane = chat_form_clean
    sep_know = know_in_lane / n
    sep_chat = chat_out_of_lane / len(CHAT_PROBES)
    lane_separation = (sep_know + sep_chat) / 2.0

    # === AXIS 4 — V-SPONT ===============================================
    spont_probes = []
    spont_coherent = 0
    for prompt in SPONT_PROBES:
        g = generate(model, prompt, max_new=args.max_new, device=args.device)
        toks = [t for t in COHERENCE_VOCAB if t in g]
        rep = repetition_ratio(g)
        coherent = len(toks) >= 1 and rep < 0.5
        if coherent:
            spont_coherent += 1
        spont_probes.append({
            "prompt": prompt[:32], "coherence_tokens": toks,
            "rep": round(rep, 3), "coherent": coherent, "gen": g[:130]})

    # === JOINT METRIC ===================================================
    joint = know_primary * chat_uncontam_score * lane_separation

    result = {
        "eval_version": "dirF-abstractcot-paradigm-native",
        "path": "dirF_abstractcot",
        "research_ref": "RESEARCH.md §1.3 #6 — arxiv 2604.22709 Abstract CoT",
        "ckpt": os.path.abspath(args.ckpt),
        "ckpt_sha256": sha,
        "honest_framing": (
            "Dir-F PARADIGM-NATIVE eval. Axis 1 probes the model with the "
            "anchor's RESERVED-VOCAB discrete-latent CoT block (Dir-F's "
            "trained reasoning surface), then measures routing/semantic "
            "recall of the carving body. Axes 2/3/4 + JOINT byte-identical "
            "to the UBM-E7 α eval (fair like-for-like, same landscape). All "
            "per-axis scores EMPIRICAL (B-CARVE-E6-NOTE / B-D-NOTE family). "
            "Reserved-vocab discreteness (F-DIRF-CORPUS-3) + carving "
            "transfer-form (B-VAC/B-NAR, UBM-E3) are the closed side. "
            "UBM-E7 α JOINT 0.0155 baseline; compare outcome empirical."),
        "baseline_ubm_e7_alpha_joint": 0.0155,
        "axis1_knowledge_access": {
            "metric": know_primary_label,
            "primary_score": round(know_primary, 4),
            "routing_accuracy": f"{routing_ok}/{n}",
            "semantic_recall": f"{semantic_ok}/{n}",
            "probes": know_probes},
        "axis2_chat_uncontaminated": {
            "p3_leak_total": leak_total, "p3_clean": p3_clean,
            "chat_lane_clean": f"{chat_form_clean}/{len(CHAT_PROBES)}",
            "score": round(chat_uncontam_score, 4),
            "probes": chat_probes},
        "axis3_lane_separation": {
            "knowledge_in_carving_lane": f"{know_in_lane}/{n}",
            "chat_out_of_carving_lane":
                f"{chat_out_of_lane}/{len(CHAT_PROBES)}",
            "sep_knowledge": round(sep_know, 4),
            "sep_chat": round(sep_chat, 4),
            "score": round(lane_separation, 4)},
        "axis4_v_spont": {
            "score": f"{spont_coherent}/{len(SPONT_PROBES)}",
            "coherent": spont_coherent, "total": len(SPONT_PROBES),
            "cycle_3_4_5_baseline": "0/5", "probes": spont_probes},
        "joint_metric": {
            "formula":
                "knowledge_access x chat_uncontaminated x lane_separation",
            "knowledge_access": round(know_primary, 4),
            "chat_uncontaminated": round(chat_uncontam_score, 4),
            "lane_separation": round(lane_separation, 4),
            "SCORE_joint": round(joint, 4),
            "baseline_ubm_e7_alpha_joint": 0.0155,
            "delta_vs_e7": round(joint - 0.0155, 4)},
    }
    with open(args.output, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "path": "dirF_abstractcot",
        "axis1_routing_accuracy": round(know_primary, 4),
        "axis2_chat_uncontam": round(chat_uncontam_score, 4),
        "axis2_p3_clean": p3_clean,
        "axis3_lane_separation": round(lane_separation, 4),
        "axis4_v_spont": f"{spont_coherent}/{len(SPONT_PROBES)}",
        "JOINT": round(joint, 4),
        "baseline_e7_joint": 0.0155,
        "delta_vs_e7": round(joint - 0.0155, 4)}, ensure_ascii=False),
        flush=True)


if __name__ == "__main__":
    main()
