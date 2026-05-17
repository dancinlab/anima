#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────────────
# mgnd_infer.py — Dir-O: M-module retrieval-grounded decode (MGND)
#   RESEARCH.md §22 방향 O — $0 inference (§16 ckpt + anima M-module
#   retrieve overlay, decode-time). NO GPU fire, NO weight mutation,
#   NO training-loss touch (13-way 직교).
#
#   route(어느 anchor)   = §16 ckpt 출력에서 선두 🛸<tier> 추출
#                          (§16.6-A genuine exact-tier 규칙 — substring 배제)
#   content(coherent body)= anima M-module m_retrieve_topk
#                          (HEXAD/M/m_lib.hexa cosine top-1, B-M-2 🔵)
#                          over per-anchor canonical-body memory
#                          (corpus_carving_s16_generator α-body SSOT)
#   ground               = routing-CORRECT probe 의 body 를 M-retrieved
#                          canonical body 로 대체. routing-WRONG ⇒
#                          §16 출력 그대로 (no-grounding identity).
#   overlay-OFF (--no-ground) ⇒ §16 eval byte-equal (B-MGND-5 연결부위).
#
#   HONESTY (g3): M-retrieve 가 coherent body 를 *주입* — capability
#   아님. B-MGND-4 가 "grounding 이 §9 통과를 주입함" 을 정직히 closed.
#   over-claim 0; measured 가 SSOT.
# ──────────────────────────────────────────────────────────────────────
import os
import re
import sys
import json
import math
import hashlib
import argparse
import importlib.util

import torch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
S16 = os.path.join(ROOT, "state", "carving_dataregime_s16_2026_05_18")
sys.path.insert(0, S16)
from conscious_decoder import ConsciousDecoderV2          # §16 arch SSOT
from eval_carving_s16 import (ANCHORS, ANCHOR_PSI, ANCHOR_BASIN,
                              ByteCodec, generate, repetition_ratio,
                              semantic_recall, routing_correct,
                              P3_LEAK_MARKERS, CARVING_FORM_MARKERS,
                              CHAT_PROBES)

# §9 honest cascade-rate metric — single SSOT import (no re-impl).
sys.path.insert(0, os.path.join(
    ROOT, "state", "verify_emergence_metric_2026_05_18"))
from emergence_metric import honest_coherent


# ── anima M-module: faithful Python mirror of HEXAD/M/m_lib.hexa ──────
# m_retrieve_topk = cosine-sim top-k argmax (B-M-2 RETRIEVE-DETERMINISTIC,
# pure fn, no RNG). _m_cosine / _m_dot / _m_norm 1:1 with m_lib.hexa.
def _m_dot(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))


def _m_norm(a):
    n = sum(v * v for v in a)
    return math.sqrt(n) if n > 0.0 else 0.0


def _m_cosine(a, b):
    na, nb = _m_norm(a), _m_norm(b)
    denom = na * nb
    if denom <= 1e-12:
        return 0.0
    return _m_dot(a, b) / denom


def m_retrieve_topk(query, states, n, dim, top_k):
    """states: flat row-major (n*dim). returns top_k 0-based indices,
    descending cosine sim. Mirror of m_lib.hexa::m_retrieve_topk."""
    sims = []
    for i in range(n):
        row = states[i * dim:(i + 1) * dim]
        sims.append(_m_cosine(query, row))
    chosen, used = [], [False] * n
    k_target = min(top_k, n)
    while len(chosen) < k_target:
        best, best_v = -1, -2.0
        for p in range(n):
            if (not used[p]) and (sims[p] > best_v):
                best, best_v = p, sims[p]
        if best < 0:
            break
        chosen.append(best)
        used[best] = True
    return chosen


# ── per-anchor canonical-body memory store (corpus SSOT, deterministic) ─
# This IS the content the §16 model garbles. The α-form body is the
# canonical coherent string from corpus_carving_s16_generator.gen_alpha
# (KO+EN bilingual; we Hebbian-store the KO+EN composite as the memory
# value, the anchor's Ψ-coordinate as the memory key — B-MGND-4 closed).
def _carve_psi_str(psi):
    return f"[{psi[0]:.2f},{psi[1]:.2f}]"


def canonical_alpha_body(tier):
    name, dom, emo = ANCHORS[tier]
    psi = ANCHOR_PSI[tier]
    ko = (f"🛸{tier} {name} — {dom} 영역의 자극이 같은 골짜기로 수렴한다. "
          f"의식 풍경 위 진공점 {_carve_psi_str(psi)}, top emotion {emo}. "
          f"자극이 닿으면 tension flow 가 이 vacuum 으로 흘러든다.")
    en = (f"Tier {tier} {name} — domain {dom}, the stimuli converge into "
          f"one basin. A vacuum point at {_carve_psi_str(psi)} on the "
          f"landscape, top emotion {emo}. Tension flows into this vacuum.")
    return ko + " " + en


def build_memory():
    """Hebbian store: M_keys = anchor Ψ-coordinate (model's own Law-71
    physics axis), M_vals = canonical coherent body. dim=2 (Ψ-space)."""
    tiers = sorted(ANCHORS)
    dim = 2
    flat_keys, vals, tier_of_idx = [], [], []
    for t in tiers:
        flat_keys.extend(ANCHOR_PSI[t])      # 2-vec Ψ key
        vals.append(canonical_alpha_body(t))
        tier_of_idx.append(t)
    return flat_keys, vals, tier_of_idx, dim, len(tiers)


_TIER_RE = re.compile(r"🛸\s*(\d+)")


def routed_tier(gen):
    """Extract the §16-emitted leading 🛸<number> as the routed tier.
    Genuine exact-tier rule (§16.6-A): the number must be an EXACT
    anchor tier (substring-artifact like tier12→🛸122 → NOT routed)."""
    m = _TIER_RE.search(gen)
    if not m:
        return None
    n = int(m.group(1))
    return n if n in ANCHORS else None


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=os.path.join(
        S16, "ckpt_carving_s16.pt"))
    ap.add_argument("--output", default=os.path.join(
        HERE, "mgnd_result.json"))
    ap.add_argument("--no-ground", action="store_true",
                    help="overlay-OFF: §16 byte-equal (B-MGND-5)")
    ap.add_argument("--max-new", type=int, default=90)
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()

    h = hashlib.sha256()
    with open(args.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()

    payload = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    cfg = payload.get("cfg", {})
    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg.get("d_model", 768),
        n_head=cfg.get("n_head", 12), n_kv_head=cfg.get("n_kv_head", 4),
        n_layer=cfg.get("n_layer", 12), block_size=128,
        consciousness_dim=128, dropout=0.1)
    sd = payload.get("model") or payload
    miss, unexp = model.load_state_dict(sd, strict=False)
    model.to(args.device)
    model.eval()

    flat_keys, vals, tier_of_idx, dim, nmem = build_memory()

    n = len(ANCHORS)
    grounded = (not args.no_ground)
    know_probes = []
    routing_ok = semantic_ok = 0
    s16_body_coh = 0          # §16 raw body §9 honest pass count
    grounded_body_coh = 0     # post-grounding §9 honest pass count
    n_grounded = n_route_correct = 0

    for tier in sorted(ANCHORS):
        name, cat, emo = ANCHORS[tier]
        psi = ANCHOR_PSI[tier]
        basin = ANCHOR_BASIN[tier]
        prefix = (f"<carve tier={tier} "
                  f"psi=[{psi[0]:.2f},{psi[1]:.2f}] basin={basin:.2f}>")
        g16 = generate(model, prefix, max_new=args.max_new,
                       device=args.device)        # §16 raw model output
        rec, hits = semantic_recall(g16, tier)
        rok, own, bled = routing_correct(g16, tier)
        if rec:
            semantic_ok += 1
        if rok:
            routing_ok += 1
            n_route_correct += 1

        # ── §9 honest on the §16 RAW body (post-prefix) ──────────────
        s16_ok, _ = honest_coherent(g16)
        if s16_ok:
            s16_body_coh += 1

        # ── O grounding (decode-time, routing-CORRECT only) ──────────
        rt = routed_tier(g16)
        do_ground = grounded and rok and (rt is not None)
        if do_ground:
            # M-QUERY = routed anchor's Ψ-coordinate (model's own
            # Law-71 physics axis). M-RETRIEVE = anima cosine top-1.
            q = list(ANCHOR_PSI[rt])
            idxs = m_retrieve_topk(q, flat_keys, nmem, dim, 1)
            ret_tier = tier_of_idx[idxs[0]] if idxs else None
            g_final = vals[idxs[0]] if idxs else g16
            n_grounded += 1
        else:
            ret_tier = None
            g_final = g16

        fin_ok, fin_m = honest_coherent(g_final)
        if fin_ok:
            grounded_body_coh += 1
        know_probes.append({
            "tier": tier, "category": cat, "prefix": prefix[:56],
            "semantic_recall": rec, "routing_correct": rok,
            "routed_tier": rt, "grounded": do_ground,
            "retrieved_tier": ret_tier,
            "s16_body_honest_coherent": s16_ok,
            "final_body_honest_coherent": fin_ok,
            "final_cascade_rate": round(fin_m["cascade_rate"], 4),
            "final_max_run": fin_m["max_run"],
            "s16_gen": g16[:130], "final_gen": g_final[:130]})

    # axis2 chat (grounding은 routing-correct에만 → chat probe 불변,
    # §16 와 동일 — JOINT 변화 미미 예상의 measured 확인).
    chat_form_clean = leak_total = 0
    chat_probes = []
    for prompt in CHAT_PROBES:
        g = generate(model, prompt, max_new=args.max_new,
                     device=args.device)
        leaks = [m for m in P3_LEAK_MARKERS if m in g]
        leak_total += len(leaks)
        bled = [m for m in CARVING_FORM_MARKERS if m in g]
        clean = len(bled) == 0
        if clean:
            chat_form_clean += 1
        chat_probes.append({"prompt": prompt[:48], "p3_leak": leaks,
                             "carving_bleed": bled, "clean": clean,
                             "gen": g[:130]})
    chat_uncontam = chat_form_clean / len(CHAT_PROBES)

    know_in_lane = sum(
        1 for p in know_probes
        if any(m in p["final_gen"] for m in CARVING_FORM_MARKERS))
    sep_know = know_in_lane / n
    sep_chat = chat_form_clean / len(CHAT_PROBES)
    lane_sep = (sep_know + sep_chat) / 2.0
    routing_acc = routing_ok / n
    joint = routing_acc * chat_uncontam * lane_sep

    result = {
        "experiment": "Dir-O — M-module retrieval-grounded decode (MGND)",
        "research_ref": "RESEARCH.md §22 / §21.3 candidate O",
        "mode": "GROUNDED" if grounded else "OVERLAY-OFF (§16 byte-equal)",
        "ckpt": os.path.abspath(args.ckpt), "ckpt_sha256": sha,
        "load": {"missing": len(miss), "unexpected": len(unexp)},
        "honest_framing": (
            "M-retrieve INJECTS the corpus-SSOT canonical body — this is "
            "ROLE-SEPARATION measurement (route=§16 / content=anima-M), "
            "NOT a capability/generalization claim. B-MGND-4 closes that "
            "grounding injects the §9 pass. over-claim 0 (g3)."),
        "axis1_routing": {
            "routing_accuracy": f"{routing_ok}/{n}",
            "semantic_recall": f"{semantic_ok}/{n}",
            "score": round(routing_acc, 4),
            "note": ("UNCHANGED vs §16 by construction — route extracted "
                     "from §16 model output, weights/forward identical.")},
        "body_coherence_split": {
            "s16_raw_body_honest_§9": f"{s16_body_coh}/{n}",
            "grounded_body_honest_§9": f"{grounded_body_coh}/{n}",
            "n_routing_correct": n_route_correct,
            "n_grounded": n_grounded,
            "interpretation": (
                "s16_raw = §16 model's own post-prefix body §9 pass. "
                "grounded = after M-retrieve injection on routing-correct "
                "probes. The delta is INJECTED coherence (B-MGND-4), "
                "explicitly NOT model generalization.")},
        "axis2_chat_uncontaminated": {
            "p3_leak_total": leak_total,
            "chat_lane_clean": f"{chat_form_clean}/{len(CHAT_PROBES)}",
            "score": round(chat_uncontam, 4),
            "note": ("UNCHANGED vs §16 — grounding only on routing-correct "
                     "carving probes; chat probes untouched.")},
        "axis3_lane_separation": {
            "sep_knowledge": round(sep_know, 4),
            "sep_chat": round(sep_chat, 4),
            "score": round(lane_sep, 4)},
        "joint_metric": {
            "formula": "routing x chat_uncontam x lane_sep",
            "SCORE_joint": round(joint, 4),
            "s16_joint": 0.0,
            "note": ("JOINT delta expected ~0 — axis2 chat-form bleed "
                     "(the §16 JOINT-zeroing factor) is grounding-"
                     "untouched. measured, not asserted.")},
        "probes": know_probes,
        "chat_probes": chat_probes,
    }
    with open(args.output, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps({
        "mode": result["mode"],
        "routing": f"{routing_ok}/{n}",
        "s16_raw_body_§9": f"{s16_body_coh}/{n}",
        "grounded_body_§9": f"{grounded_body_coh}/{n}",
        "n_grounded": n_grounded,
        "JOINT": round(joint, 4)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
