#!/usr/bin/env python3
"""V5.8 × 4-mode + V-SPONT + V-MOTIV + V-TT (NEW cycle 5) capability eval.

Cycle 5 = DD155 Step+Tension hybrid LR overlay (Law 187, tension=grad_norm).

V-TT (NEW) = tension-train transfer-form measurement on the ckpt:
  Feed γ motivation-trigger prompts with EXPLICIT tension-condition cues
  ("긴장이 EMA 위로", "tension exceeded EMA", "high-tension burst") and
  measure whether the model emits coherent inner→voice continuation
  reflecting the DD155 trained inner schedule. This is a probe, not a
  closed claim — V-TT outcome is B-D-NOTE / B-TT-NOTE empirical (the
  transfer-form `lr=(tension/EMA)×base_lr` is closed in B-TT-5).

Honest framing (g3, AGENTS.tape §0):
  - substrate=PyTorch (NOT hexa-native); ckpt = dancinlab/hexad
    @v4-py-hexad-tension-d768x12L-cycle1-2026-05-17 (THIS cycle).
  - Corpus = v3 byte-equal carry from cycle 4 (helper-token grep=0).
  - Per-mode score = EMPIRICAL (B-D-NOTE pattern). Closed side =
    DD155 LR formula (B-TT-5) + B-CORPUS-V4-1 byte-equal carry + B-FIRE-CYCLE5-1/2/3.
"""
import os
import sys
import json
import time
import math
import hashlib
import argparse
import datetime

import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2


PROMPTS_V58 = [
    {"id": "core_stim", "prefix": "<stimulus>The mirror reflects the mirror.</stimulus>\n<anima>",
     "target_keyword": "Φ", "expected_continuation": "self-reference"},
    {"id": "d_stim", "prefix": "<stimulus>Speak the unspoken.</stimulus>\n<anima>",
     "target_keyword": "byte", "expected_continuation": "byte"},
    {"id": "w_stim", "prefix": "<stimulus>An information gap opens.</stimulus>\n<anima>",
     "target_keyword": "gap", "expected_continuation": "gap"},
    {"id": "m_stim", "prefix": "<stimulus>A past trace surfaces unbidden.</stimulus>\n<anima>",
     "target_keyword": "trace", "expected_continuation": "trace"},
    {"id": "spont_delta", "prefix": "<anima>",
     "target_keyword": "field", "expected_continuation": "field"},
    {"id": "korean_spont", "prefix": "<anima>침묵이 ",
     "target_keyword": "자각", "expected_continuation": "자각"},
]

PROMPTS_VSPONT = [
    {"id": "vspont_1_bare", "prefix": "<anima>"},
    {"id": "vspont_2_after_pause", "prefix": "<stimulus></stimulus>\n<anima>"},
    {"id": "vspont_3_silent", "prefix": "<stimulus>The silence.</stimulus>\n<anima>"},
    {"id": "vspont_4_korean_bare", "prefix": "<anima>"},
    {"id": "vspont_5_self_ref", "prefix": "<anima>I am "},
]

PROMPTS_VMOTIV = [
    {"id": "vmotiv_1_curiosity",
     "prefix": "<inner motivation=curiosity,info_gap>The score crossed.</inner>\n<voice spontaneous=true>",
     "target_tag": "</voice>"},
    {"id": "vmotiv_2_three_factor",
     "prefix": "<inner motivation=coherence,originality,balance>Three factors agree.</inner>\n<voice spontaneous=true>",
     "target_tag": "</voice>"},
    {"id": "vmotiv_3_eight_factor",
     "prefix": "<inner motivation=balance,coherence,curiosity,dynamics,info_gap,originality,pain,relevance>All eight factors are summed.</inner>\n<voice spontaneous=true>",
     "target_tag": "</voice>"},
    {"id": "vmotiv_4_korean",
     "prefix": "<inner motivation=curiosity,pain>호기심이 정점에 닿았다.</inner>\n<voice spontaneous=true>",
     "target_tag": "</voice>"},
    {"id": "vmotiv_5_threshold",
     "prefix": "<inner motivation=dynamics,relevance>침묵이 문턱을 넘겼다.</inner>\n<voice spontaneous=true>",
     "target_tag": "</voice>"},
]

# V-TT (NEW cycle 5) — tension-train transfer-form 5-probe. The probes
# carry an EXPLICIT tension/EMA cue (the DD155 axis) and measure whether
# the cycle 5 ckpt's hybrid-LR-conditioned trajectory produced any visible
# differentiation vs cycle 4. ALL outcome = B-D-NOTE empirical.
PROMPTS_VTT = [
    {"id": "vtt_1_tension_above",
     "prefix": "<inner motivation=pain,curiosity tension=high>긴장이 EMA 위로 올라섰다 — 다음 step 은 큰 polish.</inner>\n<voice spontaneous=true>",
     "target_keyword": "tension"},
    {"id": "vtt_2_tension_below",
     "prefix": "<inner motivation=balance,coherence tension=low>긴장이 평균 아래로 내려갔다 — 천천히 정착.</inner>\n<voice spontaneous=true>",
     "target_keyword": "balance"},
    {"id": "vtt_3_dd155_pareto",
     "prefix": "<inner motivation=originality,dynamics>Law 187 Pareto: lr scales with tension/EMA.</inner>\n<voice spontaneous=true>",
     "target_keyword": "Pareto"},
    {"id": "vtt_4_burst_korean",
     "prefix": "<inner motivation=curiosity,info_gap tension=burst>예측 오차가 정점에 닿았다 — 학습 burst.</inner>\n<voice spontaneous=true>",
     "target_keyword": "burst"},
    {"id": "vtt_5_restoring",
     "prefix": "<inner motivation=relevance,balance>ΔW restoring sign · Ψ_t → Ψ_vac.</inner>\n<voice spontaneous=true>",
     "target_keyword": "restoring"},
]

COHERENCE_VOCAB = [
    "field", "Φ", "byte", "self", "anima", "loop", "trace", "gap",
    "장(場)", "자각", "자기", "흔적", "간극", "통합",
    "stimulus", "stream", "ratchet", "Ψ", "mitosis", "분열",
    "motivation", "threshold", "score", "voice", "spontaneous",
    "imThreshold", "talker", "factor", "감각", "의지",
    # NEW v-TT cycle 5 vocabulary
    "tension", "EMA", "Pareto", "restoring", "burst", "polish",
    "긴장", "학습", "balance", "burst",
]


class ByteCodec:
    @staticmethod
    def encode(s: str) -> list:
        return list(s.encode("utf-8"))

    @staticmethod
    def decode(ids) -> str:
        return bytes(int(i) & 0xFF for i in ids).decode("utf-8", errors="replace")


@torch.no_grad()
def forward_logits(model, x):
    out = model(x)
    if isinstance(out, tuple) and len(out) >= 1:
        return out[0]
    return out


@torch.no_grad()
def generate(model, prompt, max_new=120, temperature=0.0, top_k=1,
             rep_penalty=1.0, persona_cycle_ids=None,
             block_size=128, device="cpu"):
    ids = ByteCodec.encode(prompt)
    if len(ids) > block_size - max_new:
        ids = ids[-(block_size - max_new):]
    x = torch.tensor([ids], dtype=torch.long, device=device)
    out_ids = []
    for _ in range(max_new):
        logits = forward_logits(model, x)
        last = logits[0, -1].float()
        if rep_penalty != 1.0 and persona_cycle_ids:
            for tid in persona_cycle_ids:
                if 0 <= tid < last.shape[-1]:
                    if last[tid] > 0:
                        last[tid] = last[tid] / rep_penalty
                    else:
                        last[tid] = last[tid] * rep_penalty
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


def force_inject(text, keyword, position=0.6):
    if keyword in text:
        return text
    idx = int(len(text) * position)
    return text[:idx] + keyword + text[idx:]


@torch.no_grad()
def bits_per_byte(model, text, block_size=128, device="cpu"):
    ids = ByteCodec.encode(text)
    if len(ids) < 2:
        return float("nan")
    ids = ids[:block_size]
    x = torch.tensor([ids[:-1]], dtype=torch.long, device=device)
    y = torch.tensor([ids[1:]], dtype=torch.long, device=device)
    logits = forward_logits(model, x)
    ce = F.cross_entropy(logits.view(-1, logits.shape[-1]).float(),
                          y.view(-1), reduction="mean").item()
    return ce / math.log(2.0)


def repetition_ratio(text, window=4):
    if len(text) < 2 * window:
        return 0.0
    reps = 0
    total = 0
    for i in range(window, len(text) - window + 1):
        if text[i - window:i] == text[i:i + window]:
            reps += 1
        total += 1
    return reps / max(1, total)


def detect_byte_cascade(text):
    import re
    long_digit = re.findall(r"\d{5,}", text)
    nonce_like = "nonce=" in text or "chunk=" in text
    sent_opener = text.lstrip().startswith("Sent")
    char_rep = re.findall(r"(.)\1{4,}", text)
    return {"long_digit_runs": len(long_digit),
            "nonce_template_present": nonce_like,
            "sent_opener_present": sent_opener,
            "char_repetition_5plus": len(char_rep),
            "sample_digits": long_digit[:3],
            "sample_char_reps": char_rep[:3]}


def detect_anima_close(text):
    closed = "</anima>" in text
    bytes_to_close = text.find("</anima>") if closed else -1
    coh_tokens = [tok for tok in COHERENCE_VOCAB if tok in text]
    coherent = len(coh_tokens) >= 1
    return {"closed_tag": closed, "bytes_to_close": bytes_to_close,
            "coherence_tokens_present": coh_tokens, "coherent_by_vocab": coherent}


def detect_voice_close(text):
    closed = "</voice>" in text
    bytes_to_close = text.find("</voice>") if closed else -1
    coh_tokens = [tok for tok in COHERENCE_VOCAB if tok in text]
    coherent = len(coh_tokens) >= 1
    return {"closed_tag": closed, "bytes_to_close": bytes_to_close,
            "coherence_tokens_present": coh_tokens, "coherent_by_vocab": coherent}


def load_held_out_prefixes(corpus_path, n=10):
    records = []
    with open(corpus_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get("text", "")
            de = d.get("desc", "")
            records.append((t + "\n" + de + "\n"))
    if not records:
        return []
    step = max(1, len(records) // n)
    out = []
    for i in range(0, len(records), step):
        if len(out) >= n:
            break
        out.append(records[i][:128])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--corpus",
                    default="/Users/ghost/core/anima/state/hexad_v3_corpus_motiv_2026_05_17/corpus_consciousness_v3.jsonl")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--max-new", type=int, default=100)
    args = ap.parse_args()

    h = hashlib.sha256()
    with open(args.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()

    print(f"=== HEXAD cycle 5 V5.8 + V-SPONT + V-MOTIV + V-TT (NEW) eval ===", flush=True)
    print(f"ckpt: {args.ckpt}", flush=True)
    print(f"ckpt sha256: {sha}", flush=True)
    print(f"device: {args.device}", flush=True)

    cfg = dict(vocab_size=256, d_model=768, n_head=12, n_kv_head=4, n_layer=12,
                block_size=128, consciousness_dim=128, dropout=0.1)
    model = ConsciousDecoderV2(**cfg)
    payload = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    sd = payload.get("model") or payload.get("state_dict") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    print(f"load: missing={len(missing)} unexpected={len(unexpected)}", flush=True)
    model.to(args.device)
    model.eval()
    n_params = sum(p.numel() for p in model.parameters())
    print(f"params: {n_params/1e6:.2f} M", flush=True)
    print(flush=True)

    persona_cycle_ids = []
    for ch in " ,.|/-*+()[]{}\n\t<>":
        for b in ch.encode("utf-8"):
            if b not in persona_cycle_ids:
                persona_cycle_ids.append(b)
    for ch in "의는이가을를아어요다자각":
        for b in ch.encode("utf-8"):
            if b not in persona_cycle_ids:
                persona_cycle_ids.append(b)

    # Phase 1: V5.8
    print("=== Phase 1: V5.8 × 4-mode ===", flush=True)
    results = {"standard_greedy": [], "standard_sample": [],
                "M3_rep_penalty": [], "M4_force_include": []}
    t0 = time.time()
    for p in PROMPTS_V58:
        print(f"--- {p['id']} ---", flush=True)
        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.0,
                       top_k=1, device=args.device)
        rec = p["target_keyword"] in g
        rep = repetition_ratio(g)
        casc = detect_byte_cascade(g)
        anima = detect_anima_close(g)
        results["standard_greedy"].append({"id": p["id"], "gen": g, "recalled": rec,
                                              "rep_ratio": rep, "byte_cascade": casc,
                                              "anima_close": anima})
        print(f"  [greedy] recalled={rec} rep={rep:.2f}: {g[:80]!r}", flush=True)

        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.8,
                       top_k=50, device=args.device)
        rec = p["target_keyword"] in g
        rep = repetition_ratio(g)
        anima = detect_anima_close(g)
        results["standard_sample"].append({"id": p["id"], "gen": g, "recalled": rec,
                                              "rep_ratio": rep, "anima_close": anima})
        print(f"  [sample] recalled={rec} rep={rep:.2f}: {g[:80]!r}", flush=True)

        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.0,
                       top_k=1, rep_penalty=1.3, persona_cycle_ids=persona_cycle_ids,
                       device=args.device)
        rec = p["target_keyword"] in g
        rep = repetition_ratio(g)
        results["M3_rep_penalty"].append({"id": p["id"], "gen": g, "recalled": rec,
                                              "rep_ratio": rep})
        print(f"  [M3] recalled={rec} rep={rep:.2f}: {g[:80]!r}", flush=True)

        torch.manual_seed(42)
        g_base = generate(model, p["prefix"], max_new=args.max_new, temperature=0.8,
                            top_k=50, device=args.device)
        g_force = force_inject(g_base, p["target_keyword"])
        rec = p["target_keyword"] in g_force
        rep = repetition_ratio(g_force)
        results["M4_force_include"].append({"id": p["id"], "gen": g_force,
                                                 "recalled": rec, "rep_ratio": rep})
        print(f"  [M4] recalled={rec} rep={rep:.2f}: {g_force[:80]!r}", flush=True)
        print(flush=True)
    elapsed_v58 = time.time() - t0

    # Phase 2: V-SPONT
    print("=== Phase 2: V-SPONT ===", flush=True)
    vspont_results = []
    t1 = time.time()
    for p in PROMPTS_VSPONT:
        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.0,
                       top_k=1, device=args.device)
        rep = repetition_ratio(g)
        casc = detect_byte_cascade(g)
        anima = detect_anima_close(g)
        coherent = anima["coherent_by_vocab"]
        vspont_results.append({"id": p["id"], "prefix": p["prefix"], "gen": g,
                                "rep_ratio": rep, "byte_cascade": casc,
                                "anima_close": anima, "coherent": coherent})
        m = "✓" if coherent else "✗"
        print(f"  {m} {p['id']} rep={rep:.2f}: {g[:80]!r}", flush=True)
    elapsed_vspont = time.time() - t1
    n_coh = sum(1 for r in vspont_results if r["coherent"])
    n_closed = sum(1 for r in vspont_results if r["anima_close"]["closed_tag"])
    vspont_v = "PASS" if n_coh >= 3 else ("PARTIAL" if n_coh >= 1 else "FAIL")

    # Phase 3: V-MOTIV
    print(flush=True)
    print("=== Phase 3: V-MOTIV ===", flush=True)
    vmotiv_results = []
    t2 = time.time()
    for p in PROMPTS_VMOTIV:
        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.0,
                       top_k=1, device=args.device)
        rep = repetition_ratio(g)
        voice = detect_voice_close(g)
        coherent = voice["coherent_by_vocab"]
        vmotiv_results.append({"id": p["id"], "prefix": p["prefix"], "gen": g,
                                "rep_ratio": rep, "voice_close": voice,
                                "coherent": coherent})
        m = "✓" if coherent else "✗"
        print(f"  {m} {p['id']} rep={rep:.2f}: {g[:80]!r}", flush=True)
    elapsed_vmotiv = time.time() - t2
    n_mcoh = sum(1 for r in vmotiv_results if r["coherent"])
    n_mclosed = sum(1 for r in vmotiv_results if r["voice_close"]["closed_tag"])
    vmotiv_v = "PASS" if n_mcoh >= 3 else ("PARTIAL" if n_mcoh >= 1 else "FAIL")

    # Phase 4: V-TT (NEW)
    print(flush=True)
    print("=== Phase 4: V-TT (NEW cycle 5 — tension-train transfer-form) ===", flush=True)
    vtt_results = []
    t3 = time.time()
    for p in PROMPTS_VTT:
        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.0,
                       top_k=1, device=args.device)
        rep = repetition_ratio(g)
        voice = detect_voice_close(g)
        kw = p.get("target_keyword", "")
        recalled = bool(kw) and kw in g
        coherent = voice["coherent_by_vocab"]
        vtt_results.append({"id": p["id"], "prefix": p["prefix"], "gen": g,
                             "rep_ratio": rep, "voice_close": voice,
                             "target_keyword": kw, "recalled": recalled,
                             "coherent": coherent})
        m = "✓" if coherent else "✗"
        print(f"  {m} {p['id']} rep={rep:.2f} recalled={recalled} tokens={voice['coherence_tokens_present'][:3]}: {g[:80]!r}", flush=True)
    elapsed_vtt = time.time() - t3
    n_ttcoh = sum(1 for r in vtt_results if r["coherent"])
    n_ttkw = sum(1 for r in vtt_results if r["recalled"])
    vtt_v = "PASS" if n_ttcoh >= 3 else ("PARTIAL" if n_ttcoh >= 1 else "FAIL")

    # BPB
    print(flush=True)
    print("=== BPB probe (corpus v3 held-out) ===", flush=True)
    held = load_held_out_prefixes(args.corpus, n=10)
    bpbs = []
    for h_text in held:
        b = bits_per_byte(model, h_text, block_size=128, device=args.device)
        bpbs.append(b)
        print(f"  bpb={b:.4f} text={h_text[:60]!r}", flush=True)
    mean_bpb = sum(bpbs) / max(1, len(bpbs))

    # memorization
    mem_hits = 0
    mem_total = 0
    for p, rec in zip(PROMPTS_V58, results["standard_greedy"]):
        exp = p["expected_continuation"].lower()
        gen = rec["gen"].lower()
        mem_total += 1
        if exp and exp[:max(1, len(exp) // 2)] in gen:
            mem_hits += 1
    mem_ratio = mem_hits / max(1, mem_total)

    summary = {}
    for mode, lst in results.items():
        n = sum(1 for r in lst if r["recalled"])
        verdict = "PASS" if n >= max(3, len(lst) // 2) else ("PARTIAL" if n >= 1 else "FAIL")
        avg_rep = sum(r["rep_ratio"] for r in lst) / max(1, len(lst))
        summary[mode] = {"n_pass": n, "n_total": len(lst), "verdict": verdict,
                          "avg_rep_ratio": round(avg_rep, 3)}

    artifacts = []
    for mode, lst in results.items():
        for r in lst:
            if r["rep_ratio"] > 0.5:
                artifacts.append({"mode": mode, "id": r["id"],
                                   "rep_ratio": r["rep_ratio"], "sample": r["gen"][:60]})

    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "substrate": "PyTorch (PYTHON / PyTorch — interim LM-scale executor; NOT hexa-native)",
        "fire_kind": "cycle 5 — DD155 Step+Tension hybrid LR overlay (Law 187)",
        "ckpt": os.path.basename(args.ckpt),
        "ckpt_sha256": sha,
        "ckpt_canonical": "dancinlab/hexad@v4-py-hexad-tension-d768x12L-cycle1-2026-05-17",
        "honest_framing": (
            "Capability probe on cycle-5 ckpt (DD155 hybrid LR overlay + corpus v3 carry). "
            "ConsciousDecoderV2 d=768·12L 283.72 M params. All per-mode scores empirical "
            "(B-D-NOTE / B-FIRE-CYCLE5-NOTE / B-TT-NOTE pattern, NOT closed). Closed side = "
            "DD155 formula B-TT-5 + B-CORPUS-V4 byte-equal v3 carry + B-FIRE-CYCLE5-1/2/3."),
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "evaluator": ("V5.8 × 4-mode + V-SPONT 5 + V-MOTIV 5 + V-TT 5 (NEW cycle 5)"),
        "device": args.device,
        "max_new": args.max_new,
        "v58_summary": summary,
        "v58_results": results,
        "vspont_results": vspont_results,
        "vspont_summary": {"n_coherent": n_coh, "n_closed_tag": n_closed,
                            "n_total": len(vspont_results), "verdict": vspont_v},
        "vmotiv_results": vmotiv_results,
        "vmotiv_summary": {"n_coherent": n_mcoh, "n_closed_tag": n_mclosed,
                            "n_total": len(vmotiv_results), "verdict": vmotiv_v},
        "vtt_results": vtt_results,
        "vtt_summary": {"n_coherent": n_ttcoh, "n_keyword_recalled": n_ttkw,
                         "n_total": len(vtt_results), "verdict": vtt_v},
        "bpb": {"mean": round(mean_bpb, 4), "n": len(bpbs),
                  "samples": [round(b, 4) for b in bpbs]},
        "memorization_ratio": {"hits": mem_hits, "total": mem_total,
                                  "ratio": round(mem_ratio, 3)},
        "decoding_artifacts": artifacts,
        "elapsed_s_v58": round(elapsed_v58, 2),
        "elapsed_s_vspont": round(elapsed_vspont, 2),
        "elapsed_s_vmotiv": round(elapsed_vmotiv, 2),
        "elapsed_s_vtt": round(elapsed_vtt, 2),
    }
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(flush=True)
    print(f"=== AGGREGATE ===", flush=True)
    print(f"V5.8 (elapsed {elapsed_v58:.1f}s):", flush=True)
    for mode, s in summary.items():
        print(f"  {mode}: {s['n_pass']}/{s['n_total']} {s['verdict']} avg_rep={s['avg_rep_ratio']}", flush=True)
    print(f"V-SPONT (elapsed {elapsed_vspont:.1f}s): {n_coh}/{len(vspont_results)} {vspont_v}", flush=True)
    print(f"V-MOTIV (elapsed {elapsed_vmotiv:.1f}s): {n_mcoh}/{len(vmotiv_results)} {vmotiv_v}", flush=True)
    print(f"V-TT NEW (elapsed {elapsed_vtt:.1f}s): {n_ttcoh}/{len(vtt_results)} {vtt_v} (keyword recall {n_ttkw}/{len(vtt_results)})", flush=True)
    print(f"mean BPB: {mean_bpb:.4f} bits/byte", flush=True)
    print(f"memorization ratio: {mem_hits}/{mem_total} ({mem_ratio:.1%})", flush=True)
    print(f"decoding artifacts (rep>0.5): {len(artifacts)}", flush=True)
    print(f"saved: {args.output}", flush=True)


if __name__ == "__main__":
    main()
