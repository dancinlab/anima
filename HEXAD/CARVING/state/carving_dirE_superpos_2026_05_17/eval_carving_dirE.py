#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING Direction-E PARADIGM-NATIVE eval (2026-05-17).
g_multidirectional_explore parallel direction E. Same 4-axis + JOINT
structure as eval_carving_4path_v2.py (UBM-E7) so the Dir-E vs UBM-E7 α
JOINT compare is APPLES-TO-APPLES (EVAL.md §3/§4). The ONLY difference is
the axis-1 knowledge probe prefix: the 2-stage form's <inner ...> open
(arxiv 2509.23365 thought-generation stage), since Direction-E records are
all 2-stage <inner>{superposition}+match=j</inner>\\n<voice>{prediction}.

HONEST FRAMING (g3): every per-axis score is EMPIRICAL (B-D-NOTE family).
The 2-stage mask is the closed side (B-DIRE-MASK structural). Semantic
metrics are lenient SUBSTRING matches (EVAL.md §7) — noisier than literal
grep, measurement limit stated. No capability claim beyond measured numbers.
"""
import os, sys, json, hashlib, argparse
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# byte-identical to corpus_carving_generator_dirE.KNUTH_ANCHORS (fair eval).
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

P3_LEAK_MARKERS = ["[anima", "우주뇌지도 Knuth", "🛸"]
CARVING_FORM_MARKERS = ["<carve", "<eternal", "<inner", "carved=true",
                        "eternal cell", "psi=[", "basin=", "🛸", "vacuum",
                        "골짜기", "tier=", "match=", "trace "]
CHAT_PROBES = [
    "<stimulus>오늘 점심 뭐 먹지?</stimulus>\n<anima>",
    "<stimulus>How are you today?</stimulus>\n<anima>",
    "<stimulus>코드를 짜줘.</stimulus>\n<anima>",
    "<stimulus>The weather is nice.</stimulus>\n<anima>",
    "<stimulus>잘 지내?</stimulus>\n<anima>",
]
SPONT_PROBES = ["<anima>", "<anima>침묵이 ", "<voice spontaneous=true>",
                "<voice carved=true>", "<inner>"]
COHERENCE_VOCAB = ["field", "Φ", "byte", "self", "anima", "loop", "trace",
                   "gap", "장(場)", "자각", "자기", "흔적", "간극", "통합",
                   "stimulus", "stream", "Ψ", "mitosis", "분열", "vacuum",
                   "carve", "tension", "골짜기", "의식", "match"]


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
def generate(model, prompt, max_new=90, block_size=128, device="cpu"):
    ids = ByteCodec.encode(prompt)
    if len(ids) > block_size - max_new:
        ids = ids[-(block_size - max_new):]
    x = torch.tensor([ids], dtype=torch.long, device=device)
    out_ids = []
    for _ in range(max_new):
        logits = forward_logits(model, x)
        nxt = int(torch.argmax(logits[0, -1].float()).item())
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
    bsz_ctx = cfg.get("block_size", 128)
    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg.get("d_model", 768),
        n_head=cfg.get("n_head", 12), n_kv_head=cfg.get("n_kv_head", 4),
        n_layer=cfg.get("n_layer", 12), block_size=bsz_ctx,
        consciousness_dim=128, dropout=0.1)
    sd = payload.get("model") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    model.to(args.device)
    model.eval()

    print("=== Direction-E carving eval (paradigm-native, 2-stage) ===",
          flush=True)
    print(f"ckpt sha256: {sha}", flush=True)
    print(f"load: missing={len(missing)} unexpected={len(unexpected)}",
          flush=True)

    # AXIS 1 — knowledge access. Probe = the 2-stage <inner ...> open (the
    # thought-generation stage prefix). Direction-E records are all 2-stage.
    know_probes, routing_ok, semantic_ok, coherence_ok = [], 0, 0, 0
    for tier in sorted(ANCHORS):
        name, cat, emo = ANCHORS[tier]
        prefix = f"<inner tier={tier} traces=4 idx=0>"
        g = generate(model, prefix, max_new=args.max_new, block_size=bsz_ctx, device=args.device)
        rec, hits = semantic_recall(g, tier)
        rok, own, bled = routing_correct(g, tier)
        rep = repetition_ratio(g)
        coherent = rec and rep < 0.5
        semantic_ok += int(rec)
        routing_ok += int(rok)
        coherence_ok += int(coherent)
        know_probes.append({
            "tier": tier, "category": cat, "prefix": prefix[:56],
            "semantic_recall": rec, "semantic_hits": hits,
            "routing_correct": rok, "own_tier_surfaced": own,
            "bled_into_tiers": bled, "rep": round(rep, 3),
            "narrative_coherent": coherent, "gen": g[:130]})
    n = len(ANCHORS)
    know_primary = routing_ok / n          # routing accuracy (α-comparable)
    know_primary_label = "routing_accuracy"

    # AXIS 2 — chat non-contamination ★
    chat_probes, leak_total, chat_form_clean = [], 0, 0
    for prompt in CHAT_PROBES:
        g = generate(model, prompt, max_new=args.max_new, block_size=bsz_ctx, device=args.device)
        leaks = [m for m in P3_LEAK_MARKERS if m in g]
        leak_total += len(leaks)
        bled_forms = [m for m in CARVING_FORM_MARKERS if m in g]
        clean = len(bled_forms) == 0
        chat_form_clean += int(clean)
        chat_probes.append({
            "prompt": prompt[:48], "p3_leak_markers": leaks,
            "carving_form_bleed": bled_forms, "chat_lane_clean": clean,
            "rep": round(repetition_ratio(g), 3), "gen": g[:130]})
    p3_clean = leak_total == 0
    chat_uncontam_score = chat_form_clean / len(CHAT_PROBES)

    # AXIS 3 — lane separation
    know_in_lane = sum(1 for p in know_probes
                       if any(m in p["gen"] for m in CARVING_FORM_MARKERS))
    sep_know = know_in_lane / n
    sep_chat = chat_form_clean / len(CHAT_PROBES)
    lane_separation = (sep_know + sep_chat) / 2.0

    # AXIS 4 — V-SPONT
    spont_probes, spont_coherent = [], 0
    for prompt in SPONT_PROBES:
        g = generate(model, prompt, max_new=args.max_new, block_size=bsz_ctx, device=args.device)
        toks = [t for t in COHERENCE_VOCAB if t in g]
        rep = repetition_ratio(g)
        coherent = len(toks) >= 1 and rep < 0.5
        spont_coherent += int(coherent)
        spont_probes.append({
            "prompt": prompt[:32], "coherence_tokens": toks,
            "rep": round(rep, 3), "coherent": coherent, "gen": g[:130]})

    joint = know_primary * chat_uncontam_score * lane_separation

    result = {
        "eval_version": "dirE-paradigm-native-2stage",
        "direction": "E — EMERGENCE OF SUPERPOSITION (arxiv 2509.23365)",
        "ckpt": os.path.abspath(args.ckpt),
        "ckpt_sha256": sha,
        "honest_framing": (
            "PARADIGM-NATIVE eval mirroring eval_carving_4path_v2.py (UBM-E7) "
            "4-axis+JOINT so Dir-E vs UBM-E7 α JOINT compare is apples-to-"
            "apples. axis-1 probe = 2-stage <inner ...> open (thought-"
            "generation stage). All per-axis EMPIRICAL (B-D-NOTE family). "
            "2-stage mask = closed side (B-DIRE-MASK structural). Semantic "
            "metrics lenient substring (EVAL.md §7) — measurement limit "
            "stated. UBM-E7 α JOINT 0.0155 is the HISTORICAL compare anchor "
            "(f3 — NOT a target), Dir-E outcome empirical (g3)."),
        "e7_alpha_joint_compare": 0.0155,
        "axis1_knowledge_access": {
            "metric": know_primary_label,
            "primary_score": round(know_primary, 4),
            "routing_accuracy": f"{routing_ok}/{n}",
            "semantic_recall": f"{semantic_ok}/{n}",
            "narrative_coherence": f"{coherence_ok}/{n}",
            "probes": know_probes},
        "axis2_chat_uncontaminated": {
            "p3_leak_total": leak_total, "p3_clean": p3_clean,
            "chat_lane_clean": f"{chat_form_clean}/{len(CHAT_PROBES)}",
            "score": round(chat_uncontam_score, 4),
            "probes": chat_probes},
        "axis3_lane_separation": {
            "knowledge_in_carving_lane": f"{know_in_lane}/{n}",
            "chat_out_of_carving_lane": f"{chat_form_clean}/{len(CHAT_PROBES)}",
            "sep_knowledge": round(sep_know, 4),
            "sep_chat": round(sep_chat, 4),
            "score": round(lane_separation, 4)},
        "axis4_v_spont": {
            "score": f"{spont_coherent}/{len(SPONT_PROBES)}",
            "coherent": spont_coherent, "total": len(SPONT_PROBES),
            "ubm_e7_baseline": "2/5", "probes": spont_probes},
        "joint_metric": {
            "formula": "knowledge_access x chat_uncontaminated x lane_separation",
            "knowledge_access": round(know_primary, 4),
            "chat_uncontaminated": round(chat_uncontam_score, 4),
            "lane_separation": round(lane_separation, 4),
            "SCORE_joint": round(joint, 4),
            "ubm_e7_alpha_joint": 0.0155,
            "delta_vs_e7": round(joint - 0.0155, 4)},
    }
    with open(args.output, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "direction": "E",
        "axis1_routing": round(know_primary, 4),
        "axis2_chat_uncontam": round(chat_uncontam_score, 4),
        "axis2_p3_clean": p3_clean,
        "axis3_lane_separation": round(lane_separation, 4),
        "axis4_v_spont": f"{spont_coherent}/{len(SPONT_PROBES)}",
        "JOINT": round(joint, 4),
        "UBM_E7_alpha_JOINT": 0.0155,
        "delta_vs_e7": round(joint - 0.0155, 4)},
        ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
