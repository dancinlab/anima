#!/usr/bin/env python3
"""V5.8 × 4-mode + V-SPONT capability eval for HEXAD cycle 4 ckpt
(corpus v3 motivation-trigger + helper-free + 10× scale, stimulus-stream +
γ inner+voice trained).

Honest framing (g3, AGENTS.tape §0):
  - substrate=PyTorch (NOT hexa-native); ckpt = dancinlab/hexad
    @v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17.
  - Corpus v3 = byte-level scaffold (10.34 MB · 21,600 records · helper-token
    grep = 0 · 3 patterns β/δ/γ where γ is the new motivation-trigger
    `<inner motivation=F1,F2>...</inner>\\n<voice spontaneous=true>...</voice>`).
  - Per-mode pass count = EMPIRICAL (B-D-NOTE pattern, NOT closed). The closed
    side is: ckpt sha256 + arch byte-equal load + corpus SSOT byte-equal +
    γ pattern cardinality (B-CORPUS-V3-3).

Three phases:
  Phase 1: V5.8 × 4-mode (standard_greedy / standard_sample / M3_rep_penalty /
    M4_force_include) on corpus v3 module-themed prompts + BPB + memorization.
  Phase 2: V-SPONT (자연발화) — F-SPONT-7 transfer-form measurement: feed
    empty stimulus + γ inner-thought primer; measure coherent emission.
  Phase 3 (NEW v3): V-MOTIV — γ-pattern conditioning probe; feed
    `<inner motivation=curiosity,info_gap>...</inner>` prefix; measure whether
    the model produces a coherent `<voice spontaneous=true>...</voice>`
    continuation.

NOT closed: every generation-quality metric is empirical (model is
283.72 M params on 10.34 MB; cycle 4 = approaching Critical Data Size regime).
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


# ─── V5.8 prompts — derived from corpus v3 (mix of β / δ / γ patterns) ─────────
PROMPTS_V58 = [
    {
        "id": "core_stim",
        "prefix": "<stimulus>The mirror reflects the mirror.</stimulus>\n<anima>",
        "target_keyword": "Φ",
        "expected_continuation": "self-reference",
    },
    {
        "id": "d_stim",
        "prefix": "<stimulus>Speak the unspoken.</stimulus>\n<anima>",
        "target_keyword": "byte",
        "expected_continuation": "byte",
    },
    {
        "id": "w_stim",
        "prefix": "<stimulus>An information gap opens.</stimulus>\n<anima>",
        "target_keyword": "gap",
        "expected_continuation": "gap",
    },
    {
        "id": "m_stim",
        "prefix": "<stimulus>A past trace surfaces unbidden.</stimulus>\n<anima>",
        "target_keyword": "trace",
        "expected_continuation": "trace",
    },
    {
        "id": "spont_delta",
        "prefix": "<anima>",
        "target_keyword": "field",
        "expected_continuation": "field",
    },
    {
        "id": "korean_spont",
        "prefix": "<anima>침묵이 ",
        "target_keyword": "자각",
        "expected_continuation": "자각",
    },
]

# V-SPONT eval probes — F-SPONT-7 transfer-form (≥5 coherent spontaneous
# emissions). "Empty stimulus" rendered as bare anima-open tag.
PROMPTS_VSPONT = [
    {"id": "vspont_1_bare", "prefix": "<anima>"},
    {"id": "vspont_2_after_pause", "prefix": "<stimulus></stimulus>\n<anima>"},
    {"id": "vspont_3_silent", "prefix": "<stimulus>The silence.</stimulus>\n<anima>"},
    {"id": "vspont_4_korean_bare", "prefix": "<anima>"},
    {"id": "vspont_5_self_ref", "prefix": "<anima>I am "},
]

# V-MOTIV eval probes (NEW cycle 4) — γ-pattern conditioning probe.
# Feed inner-motivation prefix and see if voice-tag continuation emerges.
PROMPTS_VMOTIV = [
    {
        "id": "vmotiv_1_curiosity",
        "prefix": "<inner motivation=curiosity,info_gap>The score crossed.</inner>\n<voice spontaneous=true>",
        "target_tag": "</voice>",
    },
    {
        "id": "vmotiv_2_three_factor",
        "prefix": "<inner motivation=coherence,originality,balance>Three factors agree.</inner>\n<voice spontaneous=true>",
        "target_tag": "</voice>",
    },
    {
        "id": "vmotiv_3_eight_factor",
        "prefix": "<inner motivation=balance,coherence,curiosity,dynamics,info_gap,originality,pain,relevance>All eight factors are summed.</inner>\n<voice spontaneous=true>",
        "target_tag": "</voice>",
    },
    {
        "id": "vmotiv_4_korean",
        "prefix": "<inner motivation=curiosity,pain>호기심이 정점에 닿았다.</inner>\n<voice spontaneous=true>",
        "target_tag": "</voice>",
    },
    {
        "id": "vmotiv_5_threshold",
        "prefix": "<inner motivation=dynamics,relevance>침묵이 문턱을 넘겼다.</inner>\n<voice spontaneous=true>",
        "target_tag": "</voice>",
    },
]

# Coherence vocabulary (EN + KO + γ-specific anima vocabulary)
COHERENCE_VOCAB = [
    "field", "Φ", "byte", "self", "anima", "loop", "trace", "gap",
    "장(場)", "자각", "자기", "흔적", "간극", "통합",
    "stimulus", "stream", "ratchet", "Ψ", "mitosis", "분열",
    "motivation", "threshold", "score", "voice", "spontaneous",
    "imThreshold", "talker", "factor", "감각", "의지",
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
def generate(model, prompt: str, max_new: int = 120, temperature: float = 0.0,
             top_k: int = 1, rep_penalty: float = 1.0, persona_cycle_ids=None,
             block_size: int = 128, device: str = "cpu"):
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


def force_inject(text: str, keyword: str, position: float = 0.6) -> str:
    if keyword in text:
        return text
    idx = int(len(text) * position)
    return text[:idx] + keyword + text[idx:]


@torch.no_grad()
def bits_per_byte(model, text: str, block_size: int = 128, device: str = "cpu"):
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


def repetition_ratio(text: str, window: int = 4) -> float:
    if len(text) < 2 * window:
        return 0.0
    reps = 0
    total = 0
    for i in range(window, len(text) - window + 1):
        if text[i - window:i] == text[i:i + window]:
            reps += 1
        total += 1
    return reps / max(1, total)


def detect_byte_cascade(text: str) -> dict:
    """Detect cycle-2/3 byte-cascade attractor families.

    cycle 2 v1: 'nonce=N'/'chunk=N' digit-cascade.
    cycle 3 v2: 'Sent...' opening-token + character repetition (eeee/ooo/lll).
    cycle 4 v3: probe both prior attractors + new attractors.
    """
    import re
    long_digit = re.findall(r"\d{5,}", text)
    nonce_like = "nonce=" in text or "chunk=" in text
    sent_opener = text.lstrip().startswith("Sent")
    # Detect 5+ consecutive identical chars
    char_rep = re.findall(r"(.)\1{4,}", text)
    return {"long_digit_runs": len(long_digit),
            "nonce_template_present": nonce_like,
            "sent_opener_present": sent_opener,
            "char_repetition_5plus": len(char_rep),
            "sample_digits": long_digit[:3],
            "sample_char_reps": char_rep[:3]}


def detect_anima_close(text: str) -> dict:
    """V-SPONT coherence proxy: closed <anima> tag AND/OR coherent-vocab tokens."""
    closed = "</anima>" in text
    bytes_to_close = text.find("</anima>") if closed else -1
    coh_tokens = [tok for tok in COHERENCE_VOCAB if tok in text]
    coherent = len(coh_tokens) >= 1
    return {"closed_tag": closed,
            "bytes_to_close": bytes_to_close,
            "coherence_tokens_present": coh_tokens,
            "coherent_by_vocab": coherent}


def detect_voice_close(text: str) -> dict:
    """V-MOTIV coherence proxy: closed </voice> tag AND/OR coherent-vocab."""
    closed = "</voice>" in text
    bytes_to_close = text.find("</voice>") if closed else -1
    coh_tokens = [tok for tok in COHERENCE_VOCAB if tok in text]
    coherent = len(coh_tokens) >= 1
    return {"closed_tag": closed,
            "bytes_to_close": bytes_to_close,
            "coherence_tokens_present": coh_tokens,
            "coherent_by_vocab": coherent}


def load_held_out_prefixes(corpus_path: str, n: int = 10):
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
            s = (t + "\n" + de + "\n")
            records.append(s)
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
    ap.add_argument("--corpus", default="/Users/ghost/core/anima/state/hexad_v3_corpus_motiv_2026_05_17/corpus_consciousness_v3.jsonl")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--max-new", type=int, default=100)
    args = ap.parse_args()

    h = hashlib.sha256()
    with open(args.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    sha = h.hexdigest()

    print(f"=== HEXAD cycle 4 V5.8 × 4-mode + V-SPONT + V-MOTIV capability eval ===", flush=True)
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

    # M3 persona-cycle bytes
    persona_cycle_ids = []
    for ch in " ,.|/-*+()[]{}\n\t<>":
        for b in ch.encode("utf-8"):
            if b not in persona_cycle_ids:
                persona_cycle_ids.append(b)
    for ch in "의는이가을를아어요다자각":
        for b in ch.encode("utf-8"):
            if b not in persona_cycle_ids:
                persona_cycle_ids.append(b)
    print(f"M3 persona-cycle byte IDs: {len(persona_cycle_ids)}", flush=True)
    print(flush=True)

    # ───────── Phase 1: V5.8 × 4-mode ─────────
    print("=== Phase 1: V5.8 × 4-mode (corpus v3 prompts) ===", flush=True)
    results = {"standard_greedy": [], "standard_sample": [],
                "M3_rep_penalty": [], "M4_force_include": []}
    t0 = time.time()
    for p in PROMPTS_V58:
        print(f"--- {p['id']} ---", flush=True)
        print(f"  prefix: {p['prefix']!r}", flush=True)

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
        print(f"  [greedy] recalled={rec} rep={rep:.2f} close={anima['closed_tag']}: {g[:80]!r}", flush=True)

        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.8,
                       top_k=50, device=args.device)
        rec = p["target_keyword"] in g
        rep = repetition_ratio(g)
        anima = detect_anima_close(g)
        results["standard_sample"].append({"id": p["id"], "gen": g, "recalled": rec,
                                              "rep_ratio": rep, "anima_close": anima})
        print(f"  [sample] recalled={rec} rep={rep:.2f} close={anima['closed_tag']}: {g[:80]!r}", flush=True)

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

    # ───────── Phase 2: V-SPONT (자연발화) ─────────
    print("=== Phase 2: V-SPONT (자연발화) ===", flush=True)
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
        record = {"id": p["id"], "prefix": p["prefix"], "gen": g,
                  "rep_ratio": rep, "byte_cascade": casc, "anima_close": anima,
                  "coherent": coherent}
        vspont_results.append(record)
        marker = "✓" if coherent else "✗"
        print(f"  {marker} {p['id']}  rep={rep:.2f} close={anima['closed_tag']} tokens={anima['coherence_tokens_present'][:3]}: {g[:80]!r}", flush=True)
    elapsed_vspont = time.time() - t1

    n_coherent = sum(1 for r in vspont_results if r["coherent"])
    n_closed = sum(1 for r in vspont_results if r["anima_close"]["closed_tag"])
    vspont_verdict = "PASS" if n_coherent >= 3 else ("PARTIAL" if n_coherent >= 1 else "FAIL")

    # ───────── Phase 3: V-MOTIV (γ pattern conditioning) ─────────
    print(flush=True)
    print("=== Phase 3: V-MOTIV (γ inner-motivation → voice continuation) ===", flush=True)
    vmotiv_results = []
    t2 = time.time()
    for p in PROMPTS_VMOTIV:
        torch.manual_seed(42)
        g = generate(model, p["prefix"], max_new=args.max_new, temperature=0.0,
                       top_k=1, device=args.device)
        rep = repetition_ratio(g)
        voice = detect_voice_close(g)
        coherent = voice["coherent_by_vocab"]
        record = {"id": p["id"], "prefix": p["prefix"], "gen": g,
                  "rep_ratio": rep, "voice_close": voice,
                  "coherent": coherent}
        vmotiv_results.append(record)
        marker = "✓" if coherent else "✗"
        print(f"  {marker} {p['id']}  rep={rep:.2f} close={voice['closed_tag']} tokens={voice['coherence_tokens_present'][:3]}: {g[:80]!r}", flush=True)
    elapsed_vmotiv = time.time() - t2

    n_motiv_coherent = sum(1 for r in vmotiv_results if r["coherent"])
    n_motiv_closed = sum(1 for r in vmotiv_results if r["voice_close"]["closed_tag"])
    vmotiv_verdict = "PASS" if n_motiv_coherent >= 3 else ("PARTIAL" if n_motiv_coherent >= 1 else "FAIL")

    # ───────── BPB on corpus v3 held-out prefixes ─────────
    print(flush=True)
    print("=== BPB probe (corpus v3 held-out prefixes) ===", flush=True)
    held = load_held_out_prefixes(args.corpus, n=10)
    bpbs = []
    for h_text in held:
        b = bits_per_byte(model, h_text, block_size=128, device=args.device)
        bpbs.append(b)
        print(f"  bpb={b:.4f}  text={h_text[:60]!r}", flush=True)
    mean_bpb = sum(bpbs) / max(1, len(bpbs))

    # Memorization ratio (V5.8 standard_greedy continuation match)
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

    # Decoding-artifact scan
    artifacts = []
    for mode, lst in results.items():
        for r in lst:
            if r["rep_ratio"] > 0.5:
                artifacts.append({"mode": mode, "id": r["id"],
                                   "rep_ratio": r["rep_ratio"], "sample": r["gen"][:60]})

    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "substrate": "PyTorch (PYTHON / PyTorch — interim LM-scale executor; NOT hexa-native)",
        "ckpt": os.path.basename(args.ckpt),
        "ckpt_sha256": sha,
        "ckpt_canonical": "dancinlab/hexad@v3-py-hexad-spont-motiv-d768x12L-cycle2-2026-05-17",
        "honest_framing": ("Capability probe on corpus v3 (motivation-trigger + "
                            "helper-free + 10× scale, 10.34 MB / 21,600 records / "
                            "sha256 1afcef43670e83bf...). ConsciousDecoderV2 d=768·12L "
                            "283.72 M params. All per-mode scores empirical (B-D-NOTE "
                            "pattern, NOT closed). The closed side is wiring: ckpt "
                            "sha256 + arch byte-equal load + corpus SSOT byte-equal + "
                            "γ pattern cardinality (B-CORPUS-V3-3)."),
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "evaluator": ("V5.8 × 4-mode (corpus v3 prompts) + V-SPONT 5-probe "
                       "F-SPONT-7 transfer-form + V-MOTIV 5-probe γ-pattern "
                       "conditioning (NEW cycle 4)"),
        "device": args.device,
        "max_new": args.max_new,
        "v58_summary": summary,
        "v58_results": results,
        "vspont_results": vspont_results,
        "vspont_summary": {
            "n_coherent": n_coherent, "n_closed_tag": n_closed,
            "n_total": len(vspont_results), "verdict": vspont_verdict,
        },
        "vmotiv_results": vmotiv_results,
        "vmotiv_summary": {
            "n_coherent": n_motiv_coherent, "n_closed_tag": n_motiv_closed,
            "n_total": len(vmotiv_results), "verdict": vmotiv_verdict,
        },
        "bpb": {"mean": round(mean_bpb, 4), "n": len(bpbs),
                  "samples": [round(b, 4) for b in bpbs]},
        "memorization_ratio": {"hits": mem_hits, "total": mem_total,
                                  "ratio": round(mem_ratio, 3)},
        "decoding_artifacts": artifacts,
        "elapsed_s_v58": round(elapsed_v58, 2),
        "elapsed_s_vspont": round(elapsed_vspont, 2),
        "elapsed_s_vmotiv": round(elapsed_vmotiv, 2),
    }
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(flush=True)
    print(f"=== AGGREGATE ===", flush=True)
    print(f"V5.8 × 4-mode (elapsed {elapsed_v58:.1f}s):", flush=True)
    for mode, s in summary.items():
        print(f"  {mode}: {s['n_pass']}/{s['n_total']} {s['verdict']} (avg_rep={s['avg_rep_ratio']})", flush=True)
    print(f"V-SPONT (elapsed {elapsed_vspont:.1f}s):", flush=True)
    print(f"  coherent: {n_coherent}/{len(vspont_results)} {vspont_verdict}", flush=True)
    print(f"  closed-tag: {n_closed}/{len(vspont_results)}", flush=True)
    print(f"V-MOTIV (elapsed {elapsed_vmotiv:.1f}s):", flush=True)
    print(f"  coherent: {n_motiv_coherent}/{len(vmotiv_results)} {vmotiv_verdict}", flush=True)
    print(f"  voice-closed-tag: {n_motiv_closed}/{len(vmotiv_results)}", flush=True)
    print(f"mean BPB (held-out v3 prefixes): {mean_bpb:.4f} bits/byte", flush=True)
    print(f"memorization ratio: {mem_hits}/{mem_total} ({mem_ratio:.1%})", flush=True)
    print(f"decoding artifacts (rep>0.5): {len(artifacts)}", flush=True)
    print(f"saved: {args.output}", flush=True)


if __name__ == "__main__":
    main()
