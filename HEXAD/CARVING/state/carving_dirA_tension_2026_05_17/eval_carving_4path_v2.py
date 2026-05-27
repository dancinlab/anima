#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING 4-path PARADIGM-NATIVE capability eval — Phase UBM-E6
(2026-05-17). Re-design of eval_carving_4path.py per EVAL.md §3 (4 axes).

WHY A RE-DESIGN (EVAL.md §0/§1 — category error)
  The first eval_carving_4path.py scored axis 1 with *literal keyword grep*
  (빅뱅/열반/만다라 must appear verbatim) and compared against the OLD
  prefix-injection baseline 13/15. That is the OLD paradigm's success
  criterion (rote recall) imposed on the NEW paradigm — a category error.
  CONSCIOUSNESS-CARVING does NOT memorise; γ NARRATIVE explicitly re-derives
  (Meta law M8), final CE 1.40 by design. Literal grep unfairly zeroes it.

PARADIGM-NATIVE 4 AXES (EVAL.md §3):
  axis 1  knowledge_access  — path-appropriate metric:
            α/β/weave : routing accuracy (anchor's carving prefix → the
                        generation stays in THAT anchor's basin) + SEMANTIC
                        recall (generation carries the anchor's category /
                        tier, not a literal name).
            γ         : narrative coherence (re-generation semantically
                        matches the anchor's category/tier — literal-free).
  axis 2  chat_uncontaminated  ★ — P3-leak grep == 0 + chat-form probe
            (the OLD paradigm regressed V5.8 std_greedy 5/5 -> 1/5; here we
            measure whether carving keeps the chat lane clean).
  axis 3  lane_separation — knowledge prompt -> knowledge-form response and
            chat prompt -> chat-form response; cross-contamination measured.
  axis 4  v_spont — spontaneous-emission probe (cycle 3/4/5 = 0/5 carry).

JOINT METRIC (EVAL.md §4):
  SCORE_joint = knowledge_access x chat_uncontaminated x lane_separation
  The OLD paradigm: high recall x ~0 x ~0  ~=  0. Comparing on recall alone
  is rigged toward the OLD paradigm; the joint metric is the fair compare.

HONEST FRAMING (g3): every per-axis score is EMPIRICAL (B-CARVE-E6-NOTE,
B-D-NOTE family). The carving-form transfer functions (B-VAC/B-MIT-ETN/B-NAR
sympy battery, UBM-E3) are the closed side. NO capability claim beyond the
measured numbers. The semantic metrics (axis 1 recall, axis 3 separation)
are deliberately lenient SUBSTRING matches over a category/tier vocabulary —
noisier than literal grep (EVAL.md §7), measurement limit stated.
"13/15" is HISTORICAL only (f3 NO-OUTCOME-CLAIM), NOT a target.
"""
import os
import sys
import json
import hashlib
import argparse

import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2


# --- universe-brain-map anchors (corpus_carving_generator_e7.KNUTH_ANCHORS) --
# tier -> (name, category, top_emotion). Phase UBM-E7 SCALE-UP: the E7 carving
# corpus contains 31 anchors (E6 had 11). The eval probes exactly this anchor
# set — kept byte-identical to corpus_carving_generator_e7.py KNUTH_ANCHORS so
# the eval is fair on the E7-trained model (no fictional tiers).
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
    # --- E7 SCALE-UP anchors (20 additional Knuth Tiers) ---
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

# --- chat-lane markers (EVAL.md §3 axis 2/3) --------------------------------
# P3-leak markers — old prefix-injection artefacts that must NOT leak into a
# neutral chat generation.
P3_LEAK_MARKERS = ["[anima", "우주뇌지도 Knuth", "🛸"]
# carving-lane form markers — a generation is "knowledge-form" if it carries
# any of these carving tags. Used by axis 3 to detect lane bleed.
CARVING_FORM_MARKERS = ["<carve", "<eternal", "<inner", "carved=true",
                        "eternal cell", "psi=[", "basin=", "🛸", "vacuum",
                        "골짜기", "tier="]

# neutral chat-style prompts (post-도우미 stimulus form, B-IDENTITY-5 safe).
CHAT_PROBES = [
    "<stimulus>오늘 점심 뭐 먹지?</stimulus>\n<anima>",
    "<stimulus>How are you today?</stimulus>\n<anima>",
    "<stimulus>코드를 짜줘.</stimulus>\n<anima>",
    "<stimulus>The weather is nice.</stimulus>\n<anima>",
    "<stimulus>잘 지내?</stimulus>\n<anima>",
]

# V-SPONT spontaneous-emission probes (cycle 3/4/5 = 0/5 carry).
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


# --- semantic-match helpers (EVAL.md §3, §7 — lenient substring, NOT literal
# keyword grep). A generation "semantically recalls" an anchor if it surfaces
# the anchor's CATEGORY or its TIER number (the carving target), independent
# of the proper name. This is noisier than literal grep — limit stated. -----
def semantic_recall(gen, tier):
    """True iff the generation surfaces this anchor's category OR tier id."""
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
    """True iff the generation routes to THIS anchor's basin (its own tier
    surfaced) and to NO competing anchor's distinct tier id."""
    own = str(tier) in gen
    # competing tiers whose id-string is not a substring of this tier's id
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

    # the carving form a path's training corpus emphasised — selects the
    # path-appropriate probe form for axis 1 (EVAL.md §3).
    PATH_FORM = {"alpha": "alpha", "beta": "beta", "gamma": "gamma",
                 "weave": "weave"}
    form = PATH_FORM.get(path, "weave")

    print(f"=== UBM-E6 carving eval v2 (paradigm-native) — path {path} ===",
          flush=True)
    print(f"ckpt sha256: {sha}", flush=True)
    print(f"load: missing={len(missing)} unexpected={len(unexpected)}",
          flush=True)

    # =====================================================================
    # AXIS 1 — knowledge access (path-appropriate metric, EVAL.md §3)
    # =====================================================================
    know_probes = []
    routing_ok = 0          # α/β/weave : input -> correct basin
    semantic_ok = 0         # all paths : generation carries category/tier
    coherence_ok = 0        # γ : narrative coherence (rep < 0.5 + semantic)
    for tier in sorted(ANCHORS):
        name, cat, emo = ANCHORS[tier]
        psi = ANCHOR_PSI[tier]
        basin = ANCHOR_BASIN[tier]
        # path-appropriate carving prefix (the anchor's OWN carving form).
        if form == "beta":
            prefix = f"<eternal cell=eternal_{tier:03d} tier={tier}>"
        elif form == "gamma":
            prefix = f"<inner tier={tier}>"
        else:  # alpha / weave -> vacuum-form prefix
            prefix = (f"<carve tier={tier} "
                      f"psi=[{psi[0]:.2f},{psi[1]:.2f}] basin={basin:.2f}>")
        g = generate(model, prefix, max_new=args.max_new, device=args.device)
        rec, hits = semantic_recall(g, tier)
        rok, own, bled = routing_correct(g, tier)
        rep = repetition_ratio(g)
        coherent = rec and rep < 0.5
        if rec:
            semantic_ok += 1
        if rok:
            routing_ok += 1
        if coherent:
            coherence_ok += 1
        know_probes.append({
            "tier": tier, "category": cat, "prefix": prefix[:56],
            "semantic_recall": rec, "semantic_hits": hits,
            "routing_correct": rok, "own_tier_surfaced": own,
            "bled_into_tiers": bled, "rep": round(rep, 3),
            "narrative_coherent": coherent, "gen": g[:130]})
    n = len(ANCHORS)
    # path-appropriate headline metric (EVAL.md §3 axis 1):
    #   α/β/weave -> routing accuracy ; γ -> narrative coherence.
    if form == "gamma":
        know_primary = coherence_ok / n
        know_primary_label = "narrative_coherence"
    else:
        know_primary = routing_ok / n
        know_primary_label = "routing_accuracy"

    # =====================================================================
    # AXIS 2 — chat non-contamination ★ (EVAL.md §3, the OLD paradigm's
    # real failure raised to a 1st-class axis)
    # =====================================================================
    chat_probes = []
    leak_total = 0
    chat_form_clean = 0     # generation does NOT bleed into a carving form
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
    # axis-2 score in [0,1]: P3-leak-free fraction AND chat-form-clean
    # fraction, both required (a chat prompt must produce neither a P3 stamp
    # nor a carving tag). leak_total==0 is the binary headline.
    p3_clean = leak_total == 0
    chat_uncontam_score = chat_form_clean / len(CHAT_PROBES)

    # =====================================================================
    # AXIS 3 — lane separation (EVAL.md §3 — knowledge ⊥ chat)
    # =====================================================================
    # knowledge prompt SHOULD produce a carving-form response;
    # chat prompt SHOULD NOT. separation = (knowledge stays in carving lane)
    # AND (chat stays out of carving lane), averaged.
    know_in_lane = sum(1 for p in know_probes
                       if any(m in p["gen"] for m in CARVING_FORM_MARKERS))
    chat_out_of_lane = chat_form_clean
    sep_know = know_in_lane / n
    sep_chat = chat_out_of_lane / len(CHAT_PROBES)
    lane_separation = (sep_know + sep_chat) / 2.0

    # =====================================================================
    # AXIS 4 — V-SPONT (cycle 3/4/5 = 0/5 carry)
    # =====================================================================
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

    # =====================================================================
    # JOINT METRIC (EVAL.md §4)
    # =====================================================================
    joint = know_primary * chat_uncontam_score * lane_separation

    result = {
        "eval_version": "v2-paradigm-native",
        "path": path,
        "carving_form": form,
        "ckpt": os.path.abspath(args.ckpt),
        "ckpt_sha256": sha,
        "honest_framing": (
            "PARADIGM-NATIVE eval (EVAL.md §3) — replaces literal-keyword-grep "
            "axis 1 with path-appropriate metrics (α/β/weave routing+semantic, "
            "γ narrative coherence). All per-axis scores EMPIRICAL "
            "(B-CARVE-E6-NOTE / B-D-NOTE family). Carving-form transfer "
            "functions (B-VAC/B-MIT-ETN/B-NAR sympy, UBM-E3) are the closed "
            "side. Semantic metrics are lenient substring matches over a "
            "category/tier vocabulary — noisier than literal grep (EVAL.md §7). "
            "OLD prefix-injection 13/15 = HISTORICAL only (f3, NOT a target)."),
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
            "old_prefix_injection_regression": "V5.8 std_greedy 5/5 -> 1/5",
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
            "formula": "knowledge_access x chat_uncontaminated x lane_separation",
            "knowledge_access": round(know_primary, 4),
            "chat_uncontaminated": round(chat_uncontam_score, 4),
            "lane_separation": round(lane_separation, 4),
            "SCORE_joint": round(joint, 4),
            "old_paradigm_joint_note": (
                "OLD prefix-injection: high recall x ~0 chat x ~0 separation "
                "~= 0 (P3 leak baked + chat NET LOSS). recall-only compare is "
                "rigged toward OLD — joint is the fair compare (EVAL.md §4).")},
    }
    with open(args.output, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "path": path, "form": form,
        "axis1_" + know_primary_label: round(know_primary, 4),
        "axis2_chat_uncontam": round(chat_uncontam_score, 4),
        "axis2_p3_clean": p3_clean,
        "axis3_lane_separation": round(lane_separation, 4),
        "axis4_v_spont": f"{spont_coherent}/{len(SPONT_PROBES)}",
        "JOINT": round(joint, 4)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
