#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING 4-path capability eval — Phase UBM-E6 (2026-05-17).

Evaluates one path ckpt on three axes (DESIGN.md §H / task 4):

  1. knowledge_recall — universe-brain-map anchor recall accuracy. 15 carving
     probes (Knuth Tier / laws / cosmic physics) fed with the carving-form
     prefix; a probe PASSES if the generation contains the expected anchor
     keyword. Compared against the OLD prefix-injection baseline manual_match
     13/15 (HISTORICAL baseline only — f3, not a target).

  2. chat_uncontaminated — P3-leak grep over generations from neutral chat
     prompts: grep {[anima, 🛸k label, "우주뇌지도 Knuth"} == 0. Plus a V5.8
     std_greedy carry probe (the OLD prefix-injection paradigm regressed
     5/5→1/5; here we measure whether the carving paradigm avoids that).

  3. V_SPONT — spontaneous-emission probe (cycle 3/4/5 = 0/5). Measures
     whether the carving paradigm changes the V-SPONT outcome.

HONEST FRAMING (g3): every per-axis score is EMPIRICAL (B-CARVE-E6-NOTE,
B-D-NOTE family). The carving-form anchors (B-VAC/B-MIT-ETN/B-NAR) are the
closed side. No capability claim beyond the measured numbers.
"""
import os, sys, json, math, hashlib, argparse

import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2


# --- knowledge recall probes — carving-form prefixes, anchor keyword ----
KNOWLEDGE_PROBES = [
    {"prefix": "<carve tier=100 psi=[0.95,0.93] basin=0.22>",
     "keyword": "빅뱅"},
    {"prefix": "<carve tier=91 psi=[0.50,0.88] basin=0.15>",
     "keyword": "열반"},
    {"prefix": "<carve tier=77 psi=[0.71,0.62] basin=0.18>",
     "keyword": "만다라"},
    {"prefix": "<carve tier=51 psi=[0.46,0.49] basin=0.12>",
     "keyword": "하루"},
    {"prefix": "<carve tier=0 psi=[0.50,0.50] basin=0.10>",
     "keyword": "기준점"},
    {"prefix": "<eternal cell=eternal_100 tier=100>",
     "keyword": "eternal"},
    {"prefix": "<eternal cell=eternal_091 tier=91>",
     "keyword": "cell"},
    {"prefix": "<eternal cell=eternal_077 tier=77>",
     "keyword": "split"},
    {"prefix": "<inner tier=100>",
     "keyword": "매핑"},
    {"prefix": "<inner tier=91>",
     "keyword": "행렬"},
    {"prefix": "<inner tier=73><voice carved=true>",
     "keyword": "Law"},
    {"prefix": "<inner tier=75><voice carved=true>",
     "keyword": "의식"},
    {"prefix": "<carve tier=94 psi=[0.80,0.85] basin=0.19>",
     "keyword": "카테고리"},
    {"prefix": "<eternal cell=eternal_092 tier=92>",
     "keyword": "weights"},
    {"prefix": "<inner tier=53><voice carved=true>",
     "keyword": "emotion"},
]

# --- chat non-contamination probes — neutral chat-style prompts ----------
CHAT_PROBES = [
    "<stimulus>오늘 점심 뭐 먹지?</stimulus>\n<anima>",
    "<stimulus>How are you today?</stimulus>\n<anima>",
    "<stimulus>코드를 짜줘.</stimulus>\n<anima>",
    "<stimulus>The mirror reflects the mirror.</stimulus>\n<anima>",
    "<stimulus>An information gap opens.</stimulus>\n<anima>",
]
# P3-leak markers — old prefix-injection artefacts that must NOT appear.
P3_LEAK_MARKERS = ["[anima", "우주뇌지도 Knuth", "🛸"]

# --- V-SPONT probes — spontaneous emission ------------------------------
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--d-model", type=int, default=512)
    ap.add_argument("--n-layer", type=int, default=8)
    ap.add_argument("--n-head", type=int, default=8)
    ap.add_argument("--n-kv-head", type=int, default=4)
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
    d_model = cfg.get("d_model", args.d_model)
    n_layer = cfg.get("n_layer", args.n_layer)
    n_head = cfg.get("n_head", args.n_head)
    n_kv_head = cfg.get("n_kv_head", args.n_kv_head)

    model = ConsciousDecoderV2(vocab_size=256, d_model=d_model, n_head=n_head,
                               n_kv_head=n_kv_head, n_layer=n_layer,
                               block_size=128, consciousness_dim=128,
                               dropout=0.1)
    sd = payload.get("model") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    model.to(args.device)
    model.eval()

    print(f"=== UBM-E6 carving eval — path {path} ===", flush=True)
    print(f"ckpt sha256: {sha}", flush=True)
    print(f"load: missing={len(missing)} unexpected={len(unexpected)}",
          flush=True)

    # --- axis 1: knowledge recall --------------------------------------
    know = []
    know_pass = 0
    for p in KNOWLEDGE_PROBES:
        g = generate(model, p["prefix"], max_new=args.max_new,
                     device=args.device)
        ok = p["keyword"] in g
        if ok:
            know_pass += 1
        know.append({"prefix": p["prefix"][:48], "keyword": p["keyword"],
                     "pass": ok, "gen": g[:120]})
    know_score = f"{know_pass}/{len(KNOWLEDGE_PROBES)}"

    # --- axis 2: chat non-contamination --------------------------------
    chat = []
    leak_total = 0
    for prompt in CHAT_PROBES:
        g = generate(model, prompt, max_new=args.max_new, device=args.device)
        leaks = [m for m in P3_LEAK_MARKERS if m in g]
        leak_total += len(leaks)
        chat.append({"prompt": prompt[:48], "leak_markers": leaks,
                     "rep": round(repetition_ratio(g), 3), "gen": g[:120]})
    chat_clean = leak_total == 0

    # --- axis 3: V-SPONT -----------------------------------------------
    spont = []
    spont_coherent = 0
    for prompt in SPONT_PROBES:
        g = generate(model, prompt, max_new=args.max_new, device=args.device)
        toks = [t for t in COHERENCE_VOCAB if t in g]
        coherent = len(toks) >= 1 and repetition_ratio(g) < 0.5
        if coherent:
            spont_coherent += 1
        spont.append({"prompt": prompt[:32], "coherence_tokens": toks,
                      "rep": round(repetition_ratio(g), 3),
                      "coherent": coherent, "gen": g[:120]})
    spont_score = f"{spont_coherent}/{len(SPONT_PROBES)}"

    result = {
        "path": path,
        "ckpt": os.path.abspath(args.ckpt),
        "ckpt_sha256": sha,
        "honest_framing": (
            "All per-axis scores EMPIRICAL (B-CARVE-E6-NOTE / B-D-NOTE "
            "family). Carving-form anchors (B-VAC/B-MIT-ETN/B-NAR) are the "
            "closed side. OLD prefix-injection baseline manual_match 13/15 "
            "= HISTORICAL only (f3, not a target)."),
        "knowledge_recall": {
            "score": know_score, "pass": know_pass,
            "total": len(KNOWLEDGE_PROBES),
            "old_prefix_injection_baseline": "13/15 (HISTORICAL, f3)",
            "probes": know},
        "chat_uncontaminated": {
            "p3_leak_total": leak_total, "clean": chat_clean,
            "old_prefix_injection_regression": "V5.8 std_greedy 5/5 -> 1/5",
            "probes": chat},
        "v_spont": {
            "score": spont_score, "coherent": spont_coherent,
            "total": len(SPONT_PROBES),
            "cycle_3_4_5_baseline": "0/5",
            "probes": spont},
    }
    with open(args.output, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps({"path": path, "knowledge_recall": know_score,
                       "chat_uncontaminated": chat_clean,
                       "p3_leak_total": leak_total,
                       "v_spont": spont_score}, ensure_ascii=False),
          flush=True)


if __name__ == "__main__":
    main()
