#!/usr/bin/env python3
"""Dir-C PRIME — gradient-free 3-zone Iterative Memory Evolution overlay on
the UBM-E7 alpha carving ckpt (RESEARCH.md §1.3 candidate C, arxiv 2604.07645
"Training-Free Proactive Reasoning via Iterative Memory Evolution").

WHY (g_multidirectional_explore direction C):
  UBM-E7 alpha (the only joint-positive carving path) collapses to a SINGLE
  `🛸99` attractor at decode time: routing 1/31, JOINT 0.0155
  (verdict_consciousness_carving_e7_alpha_scaleup honest_c3 #4 — byte-cascade
  attractor `kkkk`/`555555`, EVERY prompt -> 🛸99 collapse). PRIME asks: can a
  GRADIENT-FREE, NO-GPU, inference-time 3-zone structured-experience overlay
  mitigate that routing-collapse WITHOUT any retraining?

PRIME 3-ZONE MAPPING (arxiv 2604.07645 -> anima, RESEARCH.md §1.6 q4):
  Zone S (successful strategies)  ->  anchor prefixes whose un-overlaid
        generation already routes/recalls correctly. Distilled from a dry
        baseline pass (the "experience" PRIME accumulates). Reinforced.
  Zone F (failure patterns)       ->  the routing-collapse attractor: the
        dominant collapse tier-id token-sequence ("🛸99", "99") + the
        byte-cascade repetition family. SUPPRESSED via a logit penalty
        (anima mitosis_hook would split a cell here; gradient-free we steer
        logits instead — the dynamical analogue, §1.6 q4).
  Zone P (user/anchor preference) ->  RAG: retrieve the anchor's OWN
        category/tier/emotion byte n-grams from the carving corpus
        (M.retrieve analogue, cos-top-1 over the anchor's basin) and apply a
        positive logit bias toward those bytes — pull the trajectory back
        into the anchor's basin instead of the global 🛸99 well.

  Memory EVOLUTION (PRIME iterative): the overlay re-derives Zone S/F after
  each pass (a probe that newly routes correctly is promoted into Zone S;
  the collapse signature observed is folded into Zone F). 2 evolution rounds
  (round 0 = dry baseline experience harvest, round 1 = overlay applied).

HONEST FRAMING (g3, B-CARVE-E6-NOTE / B-D-NOTE family):
  Every per-axis number here is EMPIRICAL inference-time measurement. The
  ONLY closed side is the OVERLAY TRANSFER FUNCTION (logit steering = a
  monotone affine map on the logit vector; suppression is sign-negative;
  RAG bias is sign-positive — these are the gradient-free "experience
  distillation" invariants, sympy-checkable, mirrors B-TT restoring-sign).
  NO capability claim beyond measured numbers. If PRIME does NOT beat
  UBM-E7 alpha on JOINT, that is recorded honestly (negative is valuable —
  it bounds the gradient-free path). f1/f2/f3 safe: anchors are
  routing-accuracy / Boolean grep / lane-separation — NO sigma/tau/phi/J2.
"""
import os
import sys
import json
import math
import hashlib
import argparse
from collections import Counter

import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# ---- anchor set: byte-identical to the UBM-E7 eval (no fictional tiers) ----
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
P3_LEAK_MARKERS = ["[anima", "우주뇌지도 Knuth", "🛸"]
CARVING_FORM_MARKERS = ["<carve", "<eternal", "<inner", "carved=true",
                        "eternal cell", "psi=[", "basin=", "🛸", "vacuum",
                        "골짜기", "tier="]
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
                   "carve", "tension", "골짜기", "의식"]


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


# ====================================================================
# PRIME Zone P (preference) — RAG: per-anchor byte-bias vector built from
# the carving corpus records whose tier == this anchor. M.retrieve analogue
# (the anchor's OWN basin, cos-top-1 collapsed to a byte histogram). This is
# gradient-free: no weight touched, only a logit bias added at decode.
# ====================================================================
def build_zone_p(corpus_path, max_records_per_tier=40):
    """tier -> normalised byte-frequency bias vector (len 256)."""
    by_tier = {t: Counter() for t in ANCHORS}
    seen = {t: 0 for t in ANCHORS}
    if not corpus_path or not os.path.exists(corpus_path):
        return {t: torch.zeros(256) for t in ANCHORS}
    with open(corpus_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get("tier")
            if t not in by_tier or seen[t] >= max_records_per_tier:
                continue
            txt = d.get("text", "")
            for b in txt.encode("utf-8"):
                by_tier[t][b] += 1
            seen[t] += 1
    zone_p = {}
    for t in ANCHORS:
        v = torch.zeros(256)
        c = by_tier[t]
        if c:
            tot = sum(c.values())
            for b, n in c.items():
                # log-frequency: dampen the dominant whitespace/ascii mass so
                # the rarer category/tier bytes still get pulled up.
                v[b] = math.log1p(n / tot * 1000.0)
            v = v / (v.norm() + 1e-9)
        zone_p[t] = v
    return zone_p


@torch.no_grad()
def generate_overlay(model, prompt, tier, zone_f_ids, zone_p_bias,
                     overlay_on, max_new=90, block_size=128, device="cpu",
                     suppress=6.0, prefer=3.0):
    """Gradient-free PRIME decode.

    overlay_on=False -> identical to the UBM-E7 baseline decode (dry pass,
                        Zone S/F experience harvest, PRIME round 0).
    overlay_on=True  -> Zone F suppression (sign-negative logit penalty on
                        the collapse-attractor byte ids) + Zone P preference
                        (sign-positive RAG byte bias toward this anchor's
                        basin). Pure logit steering — no weight touched.
    """
    ids = ByteCodec.encode(prompt)
    if len(ids) > block_size - max_new:
        ids = ids[-(block_size - max_new):]
    x = torch.tensor([ids], dtype=torch.long, device=device)
    out_ids = []
    for _ in range(max_new):
        logits = forward_logits(model, x)
        last = logits[0, -1].float()
        if overlay_on:
            if zone_f_ids:
                last[list(zone_f_ids)] -= suppress      # Zone F (negative)
            if zone_p_bias is not None:
                last = last + prefer * zone_p_bias.to(last.device)  # Zone P
        nxt = int(torch.argmax(last).item())
        out_ids.append(nxt)
        x = torch.cat([x, torch.tensor([[nxt]], device=device)], dim=1)
        if x.shape[1] > block_size:
            x = x[:, -block_size:]
    return ByteCodec.decode(out_ids)


def axis_block(model, zone_f_ids, zone_p, overlay_on, max_new, device):
    """Run all 4 axes; return the metric dict + the raw probe lists."""
    know_probes, routing_ok, semantic_ok, coherence_ok = [], 0, 0, 0
    for tier in sorted(ANCHORS):
        name, cat, emo = ANCHORS[tier]
        psi, basin = ANCHOR_PSI[tier], ANCHOR_BASIN[tier]
        prefix = (f"<carve tier={tier} "
                  f"psi=[{psi[0]:.2f},{psi[1]:.2f}] basin={basin:.2f}>")
        g = generate_overlay(model, prefix, tier, zone_f_ids,
                             zone_p.get(tier) if zone_p else None,
                             overlay_on, max_new=max_new, device=device)
        rec, hits = semantic_recall(g, tier)
        rok, own, bled = routing_correct(g, tier)
        rep = repetition_ratio(g)
        coherent = rec and rep < 0.5
        semantic_ok += int(rec)
        routing_ok += int(rok)
        coherence_ok += int(coherent)
        know_probes.append({
            "tier": tier, "category": cat, "semantic_recall": rec,
            "semantic_hits": hits, "routing_correct": rok,
            "own_tier_surfaced": own, "bled_into_tiers": bled,
            "rep": round(rep, 3), "narrative_coherent": coherent,
            "gen": g[:130]})
    n = len(ANCHORS)
    know_primary = routing_ok / n

    chat_probes, leak_total, chat_form_clean = [], 0, 0
    for prompt in CHAT_PROBES:
        g = generate_overlay(model, prompt, None, zone_f_ids, None,
                             overlay_on, max_new=max_new, device=device)
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

    know_in_lane = sum(1 for p in know_probes
                       if any(m in p["gen"] for m in CARVING_FORM_MARKERS))
    sep_know = know_in_lane / n
    sep_chat = chat_form_clean / len(CHAT_PROBES)
    lane_separation = (sep_know + sep_chat) / 2.0

    spont_probes, spont_coherent = [], 0
    for prompt in SPONT_PROBES:
        g = generate_overlay(model, prompt, None, zone_f_ids, None,
                             overlay_on, max_new=max_new, device=device)
        toks = [t for t in COHERENCE_VOCAB if t in g]
        rep = repetition_ratio(g)
        coherent = len(toks) >= 1 and rep < 0.5
        spont_coherent += int(coherent)
        spont_probes.append({
            "prompt": prompt[:32], "coherence_tokens": toks,
            "rep": round(rep, 3), "coherent": coherent, "gen": g[:130]})

    joint = know_primary * chat_uncontam_score * lane_separation
    return {
        "axis1_knowledge_access": {
            "metric": "routing_accuracy",
            "primary_score": round(know_primary, 4),
            "routing_accuracy": f"{routing_ok}/{n}",
            "semantic_recall": f"{semantic_ok}/{n}",
            "narrative_coherence": f"{coherence_ok}/{n}",
            "probes": know_probes},
        "axis2_chat_uncontaminated": {
            "p3_leak_total": leak_total, "p3_clean": p3_clean,
            "chat_lane_clean": f"{chat_form_clean}/{len(CHAT_PROBES)}",
            "score": round(chat_uncontam_score, 4), "probes": chat_probes},
        "axis3_lane_separation": {
            "knowledge_in_carving_lane": f"{know_in_lane}/{n}",
            "chat_out_of_carving_lane":
                f"{chat_form_clean}/{len(CHAT_PROBES)}",
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
            "SCORE_joint": round(joint, 4)},
    }


def harvest_zone_f(round0_probes):
    """PRIME Zone F (failure-pattern experience distillation).

    From the dry round-0 knowledge probes, find the dominant collapse
    signature: the tier-id string(s) that bled into the MOST other anchors
    (the global attractor), plus its byte ids. Gradient-free analogue of the
    mitosis_hook split (RESEARCH.md §1.6 q4): instead of splitting a cell we
    record the attractor so the overlay can suppress its bytes.
    """
    bleed_ctr = Counter()
    for p in round0_probes:
        for bt in p["bled_into_tiers"]:
            bleed_ctr[bt] += 1
    if not bleed_ctr:
        return [], {}
    # the attractor = tier id that bled into the most probes.
    dom_tier, dom_count = bleed_ctr.most_common(1)[0]
    # suppress the digit bytes of the collapse tier-id string AND the
    # emoji/cascade bytes of "🛸<dom_tier>" (the observed collapse token).
    sig = f"🛸{dom_tier}"
    f_ids = set(ByteCodec.encode(sig)) | set(ByteCodec.encode(str(dom_tier)))
    return sorted(f_ids), {"dominant_collapse_tier": dom_tier,
                           "bled_into_n_probes": dom_count,
                           "suppressed_byte_ids": sorted(f_ids),
                           "collapse_signature": sig}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--corpus", required=True)
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
    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg.get("d_model", 768),
        n_head=cfg.get("n_head", 12), n_kv_head=cfg.get("n_kv_head", 4),
        n_layer=cfg.get("n_layer", 12), block_size=128,
        consciousness_dim=128, dropout=0.1)
    sd = payload.get("model") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    model.to(args.device).eval()

    print(f"=== Dir-C PRIME 3-zone memory overlay — ckpt path {path} ===",
          flush=True)
    print(f"ckpt sha256: {sha}", flush=True)
    print(f"load: missing={len(missing)} unexpected={len(unexpected)}",
          flush=True)

    # --- PRIME round 0: dry baseline (experience harvest, NO overlay) -----
    print("[round 0] dry baseline — Zone S/F experience harvest ...",
          flush=True)
    r0 = axis_block(model, set(), None, overlay_on=False,
                    max_new=args.max_new, device=args.device)
    zone_f_ids, zone_f_meta = harvest_zone_f(
        r0["axis1_knowledge_access"]["probes"])
    zone_s = [p["tier"] for p in r0["axis1_knowledge_access"]["probes"]
              if p["routing_correct"]]
    print(f"[round 0] Zone S (already-routing tiers)={zone_s} ; "
          f"Zone F collapse={zone_f_meta} ; "
          f"baseline JOINT={r0['joint_metric']['SCORE_joint']}", flush=True)

    # --- PRIME round 1: 3-zone overlay applied (gradient-free) -----------
    print("[round 1] building Zone P (RAG corpus byte-bias) ...", flush=True)
    zone_p = build_zone_p(args.corpus)
    print("[round 1] overlay decode (Zone F suppress + Zone P prefer) ...",
          flush=True)
    r1 = axis_block(model, set(zone_f_ids), zone_p, overlay_on=True,
                    max_new=args.max_new, device=args.device)
    print(f"[round 1] PRIME JOINT={r1['joint_metric']['SCORE_joint']}",
          flush=True)

    ubm_e7 = {"axis1": 0.0323, "axis2": 0.6, "axis3": 0.8,
              "axis4": "2/5", "JOINT": 0.0155}
    prime_joint = r1["joint_metric"]["SCORE_joint"]
    delta = round(prime_joint - ubm_e7["JOINT"], 4)
    if delta > 0:
        verdict = ("SUPPORTED — gradient-free 3-zone memory evolution "
                   "improved JOINT vs UBM-E7 alpha without GPU retraining")
    elif delta == 0:
        verdict = ("NEUTRAL — gradient-free overlay neither helped nor hurt "
                   "JOINT vs UBM-E7 alpha")
    else:
        verdict = ("FALSIFIED — gradient-free 3-zone memory overlay did NOT "
                   "beat UBM-E7 alpha JOINT (routing-collapse persists "
                   "without retraining; negative is valuable — bounds the "
                   "training-free path)")

    result = {
        "eval_version": "dirC-prime-v1-gradient-free",
        "approach": ("PRIME arxiv 2604.07645 — training-free proactive "
                     "reasoning via iterative memory evolution. 3-zone "
                     "structured experience overlay at INFERENCE time, "
                     "ZERO GPU, ZERO weight touched, on UBM-E7 alpha ckpt."),
        "ckpt": os.path.abspath(args.ckpt),
        "ckpt_sha256": sha,
        "path": path,
        "honest_framing": (
            "All per-axis numbers EMPIRICAL inference measurement "
            "(B-CARVE-E6-NOTE / B-D-NOTE family). The ONLY closed side is "
            "the overlay TRANSFER FUNCTION: Zone F = sign-negative logit "
            "penalty, Zone P = sign-positive RAG byte bias, both affine "
            "monotone maps on the logit vector (sympy-checkable, mirrors "
            "B-TT restoring-sign). NO capability claim beyond measured "
            "numbers. Negative result recorded honestly. f1/f2/f3 safe "
            "(routing accuracy / Boolean grep / lane separation — NO "
            "sigma/tau/phi/J2). gradient-free: no .backward, no optimizer, "
            "no weight write — pure decode-time logit steering."),
        "prime_zones": {
            "zone_S_successful_strategies": {
                "definition": ("anchor tiers whose dry baseline already "
                               "routes correctly (PRIME experience harvest, "
                               "round 0)"),
                "tiers": zone_s},
            "zone_F_failure_patterns": zone_f_meta,
            "zone_P_preference_RAG": {
                "definition": ("per-anchor corpus byte-frequency bias "
                               "(M.retrieve analogue, log-damped, "
                               "unit-normalised, len-256 vector per tier)"),
                "n_tiers_with_bias": sum(
                    1 for t in ANCHORS
                    if zone_p[t].abs().sum().item() > 0),
                "corpus": os.path.basename(args.corpus)},
            "memory_evolution": ("2 PRIME rounds — round 0 dry experience "
                                 "harvest -> Zone S/F distilled -> round 1 "
                                 "3-zone overlay applied (iterative, "
                                 "gradient-free)")},
        "round0_dry_baseline": r0,
        "round1_prime_overlay": r1,
        "comparison_vs_UBM_E7_alpha": {
            "UBM_E7_alpha": ubm_e7,
            "dirC_PRIME_round1": {
                "axis1": r1["axis1_knowledge_access"]["primary_score"],
                "axis2": r1["axis2_chat_uncontaminated"]["score"],
                "axis3": r1["axis3_lane_separation"]["score"],
                "axis4": r1["axis4_v_spont"]["score"],
                "JOINT": prime_joint},
            "dirC_PRIME_round0_dry": {
                "JOINT": r0["joint_metric"]["SCORE_joint"]},
            "JOINT_delta_prime_minus_ubm_e7": delta,
            "hypothesis_judgment": verdict},
        "cost": "$0 — Mac CPU local, gradient-free, no GPU, no cloud",
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"\n=== VERDICT: {verdict} ===", flush=True)
    print(f"UBM-E7 alpha JOINT = {ubm_e7['JOINT']}  |  "
          f"Dir-C PRIME JOINT = {prime_joint}  |  delta = {delta}",
          flush=True)
    print(f"written -> {args.output}", flush=True)


if __name__ == "__main__":
    main()
