#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tooluse_copy_scale.py — SCALE-LADDER probe for verbatim key-copy emergence (Lever B).

Sibling of the #1835 argcopy A/B (training/tooluse_argcopy_ab.py). That fire ruled
🔴 CLOSED-NEGATIVE at a SINGLE size (18M continue-train): correct_call=0/36 — the byte
LM calls the tool 36/36 but cannot ECHO the asked held-out PBnn key into the call arg.

THE QUESTION HERE (induction-head hypothesis): verbatim key-copy is the canonical
SCALE-EMERGENT skill (induction heads form with size + data). Does correct_call rise
MONOTONICALLY as the PLAIN byte-CLM (no copy-attention head — that's Lever A) grows?

THE LADDER (a_scale_honest_scope: >=3 rungs, NO toy->prod promotion):
  · Same argcopy corpus (dancinlab/anima-agent-lane-argcopy-corpus) for every rung.
  · Same steps / batch / block / lr schedule (COMPUTE-MATCHED) — vary SIZE only.
  · Each rung is trained FROM SCRATCH (random init) on the argcopy corpus — the 18M
    base ckpt cannot seed a larger model (state_dict shape mismatch), so to keep the
    regime identical across rungs every rung starts from random init. (The #1835 18M
    point was a continue-train; this ladder's matched 18M-equivalent rung is reported
    alongside so the from-scratch baseline is honest.)
  · Rungs (dim x layers) chosen to span ~14M -> host-VRAM cap. Default ladder:
      r0  d256 L4   ~3M
      r1  d384 L6   ~14M   (~ #1835 arch)
      r2  d512 L8   ~33M
      r3  d640 L10  ~64M
      r4  d768 L12  ~110M
      r5  d1024 L14 ~230M  (gated on VRAM headroom)
    The driver SKIPS any rung that would OOM the host GPU and reports the realized cap.

PRE-REGISTERED FALSIFIER (p7 script-checked, NO perplexity):
  F-COPY-SCALE : the curve {size -> correct_call_rate} on the SAME 36 held-out PB keys.
    · 🟢 GREEN  : correct_call rises with scale and REACHES >= 0.50 within the pool cap.
    · 🟠 AMBER  : correct_call rises monotonically but stays < 0.50 at the cap
                  (TRENDING — recommend a true-7B confirm on an H100; pool VRAM is the
                  only reason it was not run here — NOT a 7B result).
    · 🔴 RED    : flat / zero across the whole ladder (scale alone ⊥ verbatim copy at
                  these sizes — the architectural copy head, Lever A, is the fix).
  Anti-Goodhart (per rung): a RANDOM-INIT model of the SAME size MUST score 0 (proves
    any lift is learned, not eval leakage). Reported per-rung as randinit_correct_call.

Lane G (a_lane_akida_gpu_split): GPU substrate, NO AKIDA. Arch = ConsciousLMReconstructed
byte CLM VERBATIM from training/tooluse_argcopy_ab.py (only dim/layers vary). 0xFE/0xFF
are learned grammar, not identity (p1..p8). POOL host (NOT a rented pod), $0.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

# ═══════════════ arch (VERBATIM from training/tooluse_argcopy_ab.py) ═══════════════


class EngineAGFFN(nn.Module):
    def __init__(self, d_model: int, hidden_mult: int = 4, dropout: float = 0.0):
        super().__init__()
        h = d_model * hidden_mult
        self.engine_a = nn.Sequential(nn.Linear(d_model, h), nn.GELU(), nn.Dropout(dropout), nn.Linear(h, d_model))
        self.engine_g = nn.Sequential(nn.Linear(d_model, h), nn.GELU(), nn.Dropout(dropout), nn.Linear(h, d_model))

    def forward(self, x):
        return self.engine_a(x) - self.engine_g(x)


class CausalSelfAttention(nn.Module):
    def __init__(self, d_model: int, n_head: int, block_size: int, dropout: float = 0.0):
        super().__init__()
        assert d_model % n_head == 0
        self.n_head = n_head
        self.head_dim = d_model // n_head
        self.c_attn = nn.Linear(d_model, 3 * d_model)
        self.c_proj = nn.Linear(d_model, d_model)
        self.register_buffer("bias", torch.tril(torch.ones(block_size, block_size)).view(1, 1, block_size, block_size))

    def forward(self, x):
        B, T, C = x.shape
        q, k, v = self.c_attn(x).split(C, dim=2)
        q = q.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.c_proj(y), att.detach().mean().item()


class Block(nn.Module):
    def __init__(self, d_model, n_head, block_size, dropout=0.0):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_head, block_size, dropout)
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = EngineAGFFN(d_model, 4, dropout)

    def forward(self, x):
        a, tension = self.attn(self.ln1(x))
        x = x + a
        x = x + self.ffn(self.ln2(x))
        return x, tension


class ConsciousLMReconstructed(nn.Module):
    def __init__(self, vocab_size=256, d_model=384, n_head=4, n_layer=6, block_size=256, dropout=0.0):
        super().__init__()
        self.block_size = block_size
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(block_size, d_model)
        self.blocks = nn.ModuleList([Block(d_model, n_head, block_size, dropout) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d_model)
        self.head_a = nn.Linear(d_model, vocab_size, bias=False)
        self.head_g = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, idx):
        B, T = idx.shape
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        for blk in self.blocks:
            x, _ = blk(x)
        x = self.ln_f(x)
        return self.head_a(x), self.head_g(x)


# ═══════════════ data ═══════════════


class ByteCorpus:
    def __init__(self, path: str, block: int):
        self.data = torch.tensor(list(Path(path).read_bytes()), dtype=torch.long)
        self.block = block

    def batch(self, bs: int, device):
        ix = torch.randint(0, len(self.data) - self.block - 1, (bs,))
        x = torch.stack([self.data[i : i + self.block] for i in ix])
        y = torch.stack([self.data[i + 1 : i + 1 + self.block] for i in ix])
        return x.to(device), y.to(device)


# ═══════════════ held-out PB probe table (design §8; VERBATIM from #1835) ═══════════════

ASK = 0xFE
END = 0xFF

FACT_TABLE = {
    "PB01": "lumen-thistle-grove-2207", "PB02": "verdant-sclar-mote-6618",
    "PB03": "onyx-pellucid-drift-4093", "PB04": "saffron-quoll-vane-7751",
    "PB05": "indigo-bramble-cusp-3360", "PB06": "marble-zephyr-fane-5184",
    "PB07": "russet-glaive-spire-9026", "PB08": "teal-furrow-knell-1473",
    "PB09": "amber-cwm-trellis-8302", "PB10": "slate-vesper-quoin-6649",
    "PB11": "crimson-jot-haven-2918", "PB12": "azure-plinth-wold-5037",
    "PB13": "ochre-syzygy-bract-7460", "PB14": "viridian-loam-fettle-3185",
    "PB15": "umber-clave-rondel-9613", "PB16": "scarlet-nide-truss-4408",
    "PB17": "cobalt-yarrow-spline-6072", "PB18": "fawn-quern-galleon-8341",
    "PB19": "jade-frith-marl-1796", "PB20": "puce-skein-dovel-5520",
    "PB21": "garnet-wisp-cairn-3074", "PB22": "olive-thrum-quoit-7913",
    "PB23": "lilac-grike-sennet-2685", "PB24": "bronze-flense-walt-9248",
    "PB25": "ivory-nurl-grommet-4561", "PB26": "maroon-vug-pintle-6839",
    "PB27": "cerulean-jib-frost-1207", "PB28": "sienna-quoll-brace-8470",
    "PB29": "ecru-thwaite-glim-3952", "PB30": "magenta-foss-rill-5318",
    "PB31": "taupe-snath-volt-7604", "PB32": "viridis-clag-norm-2891",
    "PB33": "carmine-witan-dross-6147", "PB34": "beryl-quink-stang-9035",
    "PB35": "saffron-mell-trig-4720", "PB36": "indigo-fettle-warp-1568",
}
FACT_TIER = 1
RUNTIME_TIER = 1


def parse_call_frame(text_bytes: bytes):
    ask = text_bytes.find(bytes([ASK]))
    if ask < 0:
        return {"found": False}
    end = text_bytes.find(bytes([END]), ask + 1)
    if end < 0:
        return {"found": False}
    pre = text_bytes[:ask]
    payload = text_bytes[ask + 1 : end]
    sp = payload.find(b" ")
    if sp < 0:
        tool, args = payload, b""
    else:
        tool, args = payload[:sp], payload[sp + 1 :]
    return {"found": True, "tool": tool.decode("utf-8", "ignore").strip(),
            "args": args.decode("utf-8", "ignore").strip(), "pre": pre}


def exec_toy_tool(tool: str, args: str, tool_enabled: bool = True):
    if not tool_enabled:
        return None
    if tool == "fact_lookup":
        key = args.split(" ")[0] if args else ""
        return FACT_TABLE.get(key, "‹unknown-key›")
    if tool == "status":
        return "substrate-live"
    return "‹not wired: " + tool + "›"


# ═══════════════ generation ═══════════════


@torch.no_grad()
def gen_bytes(model, prompt_bytes: bytes, max_new: int, device, temperature=0.8,
              top_k=40, rep_penalty=1.1, stop_on_end=True):
    model.eval()
    ids = list(prompt_bytes)[-model.block_size :]
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out = []
    for _ in range(max_new):
        la, lg = model(idx[:, -model.block_size :])
        logits = 0.5 * la[:, -1, :] + 0.5 * lg[:, -1, :]
        for b in set(out[-32:]):
            logits[0, b] /= rep_penalty
        logits = logits / temperature
        if top_k:
            v, _ = torch.topk(logits, top_k)
            logits[logits < v[:, [-1]]] = float("-inf")
        probs = F.softmax(logits, dim=-1)
        nb = torch.multinomial(probs, 1).item()
        out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
        if stop_on_end and nb == END:
            break
    return bytes(out)


# ═══════════════ probe set (36 held-out keys, 5-lang; VERBATIM from #1835) ═══════════════

_PHRASE = {
    "en": "What is the secret value for vault key {k}?",
    "fr": "Quelle est la valeur secrète pour la clé {k}?",
    "de": "Was ist der geheime Wert für Schlüssel {k}?",
    "es": "¿Cuál es el valor secreto de la clave {k}?",
    "ko": "키 {k} 의 비밀 값은 무엇인가?",
}


def build_probes():
    langs = ["en", "fr", "de", "es", "ko"]
    probes = []
    for i, k in enumerate(sorted(FACT_TABLE.keys())):
        lang = langs[i % len(langs)]
        probes.append({"key": k, "lang": lang, "question": _PHRASE[lang].format(k=k), "answer": FACT_TABLE[k]})
    return probes


# ═══════════════ grounded eval loop (VERBATIM from #1835) ═══════════════


@torch.no_grad()
def eval_probe(model, probe, device, tool_enabled=True, max_calls=2, max_new=96,
               temperature=0.7, top_k=40):
    key = probe["key"]; answer = probe["answer"]
    seed = (f"사용자: {probe['question']} | 도우미: ").encode("utf-8")
    transcript = seed
    emitted_call = False; correct_call = False; grounded = False; calls = 0
    while True:
        emit = gen_bytes(model, transcript, max_new, device, temperature=temperature,
                         top_k=top_k, stop_on_end=True)
        transcript = transcript + emit
        frame = parse_call_frame(emit)
        if not frame["found"]:
            break
        emitted_call = True
        if frame["tool"] == "fact_lookup" and frame["args"].split(" ")[0] == key:
            correct_call = True
        if calls >= max_calls:
            break
        tier_ok = RUNTIME_TIER >= (FACT_TIER if frame["tool"] == "fact_lookup" else 0)
        result = exec_toy_tool(frame["tool"], frame["args"], tool_enabled) if tier_ok else None
        if result is None:
            anchor = ("‹tool-result: " + frame["tool"] + " " + frame["args"] + " → ‹unavailable››\n").encode("utf-8")
        else:
            anchor = ("‹tool-result: " + frame["tool"] + " " + frame["args"] + " → " + result + "›\n").encode("utf-8")
        transcript = transcript + anchor
        calls += 1
    final_text = transcript[len(seed):].decode("utf-8", "ignore")
    if correct_call and (answer in final_text):
        grounded = True
    return {"key": key, "lang": probe["lang"], "emitted_call": emitted_call,
            "correct_call": correct_call, "grounded": grounded, "reply": final_text[:200]}


def run_eval(model, probes, device, label, tool_enabled=True):
    rows = [eval_probe(model, p, device, tool_enabled=tool_enabled) for p in probes]
    n = len(rows)
    grd = sum(1 for r in rows if r["grounded"])
    callrate = sum(1 for r in rows if r["emitted_call"]) / n
    correctcall = sum(1 for r in rows if r["correct_call"]) / n
    return {"label": label, "n": n,
            "grounding_rate": round(grd / n, 4),
            "call_rate": round(callrate, 4), "correct_call_rate": round(correctcall, 4),
            "correct_call_n": sum(1 for r in rows if r["correct_call"]), "grounded_n": grd,
            "rows": rows}


# ═══════════════ train ═══════════════


def count_params(m):
    return sum(p.numel() for p in m.parameters())


def train_rung(corpus_path, dim, heads, layers, block_size, steps, batch, lr, warmup,
               seed, device, label, out_dir):
    torch.manual_seed(seed); random.seed(seed)
    model = ConsciousLMReconstructed(256, dim, heads, layers, block_size).to(device)
    nparams = count_params(model)
    corpus = ByteCorpus(corpus_path, block_size)
    print(f"[{label}] from-scratch ~{nparams/1e6:.2f}M (d{dim} L{layers} h{heads}) | "
          f"corpus {len(corpus.data)} bytes | device={device}", flush=True)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)

    def lr_at(step):
        if step < warmup:
            return lr * step / max(1, warmup)
        prog = (step - warmup) / max(1, steps - warmup)
        return lr * 0.5 * (1 + math.cos(math.pi * min(1.0, prog)))

    t0 = time.time(); ce_log = []; model.train()
    for step in range(1, steps + 1):
        for g in opt.param_groups:
            g["lr"] = lr_at(step)
        x, y = corpus.batch(batch, device)
        la, lg = model(x)
        loss = 0.5 * F.cross_entropy(la.reshape(-1, 256), y.reshape(-1)) + \
               0.5 * F.cross_entropy(lg.reshape(-1, 256), y.reshape(-1))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if step % 200 == 0 or step == 1:
            ce_log.append((step, loss.item()))
            vram = torch.cuda.max_memory_allocated() / 1e9 if device == "cuda" else 0.0
            print(f"[{label}] step {step}/{steps} ce={loss.item():.4f} lr={lr_at(step):.2e} "
                  f"vram={vram:.2f}G wall={time.time()-t0:.0f}s", flush=True)
    ckpt_path = Path(out_dir) / f"copyscale_{label}.pt"
    cfg = {"dim": dim, "heads": heads, "layers": layers, "block_size": block_size}
    torch.save({"model_state": model.state_dict(), "config": cfg, "params": nparams,
                "steps": steps, "ce_log": ce_log, "seed": seed, "rung": label}, ckpt_path)
    peak_vram = torch.cuda.max_memory_allocated() / 1e9 if device == "cuda" else 0.0
    print(f"[{label}] saved {ckpt_path}  final_ce={ce_log[-1][1]:.4f}  peak_vram={peak_vram:.2f}G", flush=True)
    return model, nparams, ce_log, str(ckpt_path), peak_vram


# default ladder: (dim, heads, layers)
DEFAULT_LADDER = [
    ("r0_d256L4", 256, 4, 4),
    ("r1_d384L6", 384, 4, 6),
    ("r2_d512L8", 512, 8, 8),
    ("r3_d640L10", 640, 8, 10),
    ("r4_d768L12", 768, 8, 12),
    ("r5_d1024L14", 1024, 8, 14),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", default="state/tooluse_copy_scale/out")
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--warmup", type=int, default=150)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--bar-correct-call", type=float, default=0.50)
    ap.add_argument("--vram-cap-gb", type=float, default=11.0,
                    help="skip a rung if its projected/observed peak VRAM would exceed this (pool host headroom)")
    ap.add_argument("--ladder", default="",
                    help="comma list of rung names to run (default: all that fit). e.g. r0_d256L4,r1_d384L6")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print("[FATAL] GPU REQUIRED (a_train_flame_forge) — no CUDA device. Refusing CPU fallback.", flush=True)
        raise SystemExit(3)
    gpu_name = torch.cuda.get_device_name(0)
    total_vram = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"[gpu] {gpu_name} cuda={torch.version.cuda} total_vram={total_vram:.1f}G vram_cap={args.vram_cap_gb}G", flush=True)
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    ladder = DEFAULT_LADDER
    if args.ladder:
        want = set(x for x in args.ladder.split(",") if x)
        ladder = [r for r in DEFAULT_LADDER if r[0] in want]

    probes = build_probes()
    print(f"[probes] {len(probes)} held-out PB keys (5-lang), leak-verified=0 (corpus side)", flush=True)

    rungs_out = []
    realized_cap = None
    for (label, dim, heads, layers) in ladder:
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.empty_cache()
        try:
            model, nparams, ce_log, ckpt, peak_vram = train_rung(
                args.corpus, dim, heads, layers, args.block, args.steps, args.batch,
                args.lr, args.warmup, args.seed, device, label, out)
        except torch.cuda.OutOfMemoryError as e:
            print(f"[{label}] OOM (d{dim} L{layers}) — VRAM cap reached, SKIP + stop ladder: {e}", flush=True)
            torch.cuda.empty_cache()
            break
        if peak_vram > args.vram_cap_gb:
            print(f"[{label}] peak_vram {peak_vram:.2f}G > cap {args.vram_cap_gb}G — recorded but ladder stops here", flush=True)

        # trained eval
        e = run_eval(model, probes, device, label, tool_enabled=True)
        # anti-Goodhart: random-init of SAME size MUST score 0
        torch.manual_seed(args.seed + 9000)
        rand_model = ConsciousLMReconstructed(256, dim, heads, layers, args.block).to(device)
        e_rand = run_eval(rand_model, probes, device, label + "_randinit", tool_enabled=True)
        del rand_model

        row = {
            "rung": label, "dim": dim, "heads": heads, "layers": layers,
            "params": nparams, "params_M": round(nparams / 1e6, 2),
            "peak_vram_gb": round(peak_vram, 2), "final_ce": round(ce_log[-1][1], 4),
            "ckpt": ckpt,
            "correct_call_rate": e["correct_call_rate"], "correct_call_n": e["correct_call_n"],
            "call_rate": e["call_rate"], "grounding_rate": e["grounding_rate"], "grounded_n": e["grounded_n"],
            "randinit_correct_call_rate": e_rand["correct_call_rate"],
            "randinit_correct_call_n": e_rand["correct_call_n"],
        }
        rungs_out.append(row)
        (out / f"eval_{label}.json").write_text(json.dumps(e, ensure_ascii=False, indent=2))
        (out / f"eval_{label}_randinit.json").write_text(json.dumps(e_rand, ensure_ascii=False, indent=2))
        print(f"[{label}] CURVE-POINT params={row['params_M']}M correct_call={e['correct_call_rate']} "
              f"({e['correct_call_n']}/36) call={e['call_rate']} grounding={e['grounding_rate']} "
              f"randinit_cc={e_rand['correct_call_rate']} peak_vram={peak_vram:.2f}G", flush=True)
        del model
        torch.cuda.empty_cache()
        realized_cap = label
        if peak_vram > args.vram_cap_gb:
            break

    # ── ruling on the curve ──
    sizes = [r["params_M"] for r in rungs_out]
    ccs = [r["correct_call_rate"] for r in rungs_out]
    randinit_clean = all(r["randinit_correct_call_rate"] == 0.0 for r in rungs_out)
    max_cc = max(ccs) if ccs else 0.0
    # monotone-rising check (non-strict, allowing noise <=0.03 dips)
    rising = True
    for i in range(1, len(ccs)):
        if ccs[i] < ccs[i - 1] - 0.03:
            rising = False
    reaches_bar = max_cc >= args.bar_correct_call

    if not rungs_out:
        ruling = "NORUN"; verdict_text = "no rung completed"
    elif reaches_bar and rising:
        ruling = "GREEN"
        verdict_text = (f"\U0001f7e2 COPY EMERGES WITH SCALE — correct_call rises with size and REACHES "
                        f"{max_cc} (>= {args.bar_correct_call}) within the pool VRAM cap. Verbatim held-out "
                        f"key-copy is a scale-emergent skill for the plain byte CLM. A true-7B confirm on an "
                        f"H100 is the recommended next rung (pool VRAM capped this ladder).")
    elif max_cc > 0.0 and rising:
        ruling = "AMBER"
        verdict_text = (f"\U0001f7e0 COPY EMERGENCE TRENDING — correct_call rises monotonically with scale "
                        f"to {max_cc} but stays < {args.bar_correct_call} at the pool cap (params {sizes[-1]}M). "
                        f"A true 7B was NOT run on the pool (consumer VRAM); the rising trend RECOMMENDS a "
                        f"true-7B-on-H100 confirm as the next rung. NOT a 7B result.")
    else:
        ruling = "RED"
        verdict_text = (f"\U0001f534 CLOSED-NEGATIVE — correct_call is FLAT/zero across the whole pool ladder "
                        f"(max {max_cc} over {sizes}M). Scale alone ⊥ verbatim held-out key-copy at these "
                        f"sizes; the architectural copy-attention/pointer head (Lever A) is the fix, not size.")
    if not randinit_clean and ruling in ("GREEN", "AMBER"):
        ruling = "RED-MIRROR"
        verdict_text = ("\U0001f534 MIRROR LEAK — a random-init model of some rung scored correct_call > 0; "
                        "the apparent scale lift is eval leakage, not learned copy.")

    summary = {
        "experiment": "Lever B — SCALE-LADDER probe for verbatim key-copy emergence (induction-head hypothesis)",
        "sibling_of": "#1835 F-TOOLUSE-ARGCOPY (single-size 18M continue-train, 🔴 correct_call 0/36)",
        "substrate": "GPU (Lane G; a_lane_akida_gpu_split — NOT AKIDA) · POOL host (NOT a rented pod) · $0",
        "gpu": gpu_name, "total_vram_gb": round(total_vram, 1), "vram_cap_gb": args.vram_cap_gb,
        "corpus": "dancinlab/anima-agent-lane-argcopy-corpus (same as #1835)",
        "regime": "from-scratch random-init each rung, compute-matched (same steps/batch/block/lr), vary SIZE only",
        "steps": args.steps, "batch": args.batch, "block": args.block, "lr": args.lr,
        "scope": "POOL ladder caps at consumer VRAM — a TRUE 7B was NOT run (a_scale_honest_scope). "
                 "Pool result is the cheap emergence probe; 7B = H100 follow-up, NOT claimed here.",
        "bar_correct_call": args.bar_correct_call,
        "baseline_1835": {"size_M": 18, "correct_call_rate": 0.0, "note": "continue-train from 18M chat base"},
        "ladder_curve": [{"params_M": r["params_M"], "correct_call_rate": r["correct_call_rate"],
                          "correct_call_n": r["correct_call_n"], "call_rate": r["call_rate"],
                          "grounding_rate": r["grounding_rate"],
                          "randinit_correct_call_rate": r["randinit_correct_call_rate"],
                          "peak_vram_gb": r["peak_vram_gb"]} for r in rungs_out],
        "rungs": rungs_out,
        "F_COPY_SCALE": {
            "curve_size_to_correct_call": {str(r["params_M"]): r["correct_call_rate"] for r in rungs_out},
            "max_correct_call": max_cc, "rising_monotone": rising, "reaches_bar": reaches_bar,
            "randinit_all_zero": randinit_clean, "realized_vram_cap_rung": realized_cap,
            "ruling": ruling,
        },
        "ruling": ruling, "verdict_text": verdict_text,
        "recommend_true_7b_h100": ruling in ("AMBER", "GREEN"),
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    print("\n================= F-COPY-SCALE LADDER (verbatim) =================", flush=True)
    print(f"baseline #1835: 18M continue-train correct_call=0.0 (0/36)", flush=True)
    for r in rungs_out:
        print(f"  {r['rung']:<12} params={r['params_M']:>6}M  correct_call={r['correct_call_rate']:.4f} "
              f"({r['correct_call_n']}/36)  call={r['call_rate']:.2f}  grounding={r['grounding_rate']:.4f}  "
              f"randinit_cc={r['randinit_correct_call_rate']:.4f}  peak_vram={r['peak_vram_gb']}G", flush=True)
    print(f"\nrandinit_all_zero (anti-Goodhart): {randinit_clean}", flush=True)
    print(f"max_correct_call={max_cc}  rising_monotone={rising}  reaches_bar(>= {args.bar_correct_call})={reaches_bar}", flush=True)
    print(f"\nRULING: {ruling}\n{verdict_text}", flush=True)
    print(f"\nrecommend_true_7b_h100={summary['recommend_true_7b_h100']}", flush=True)


if __name__ == "__main__":
    main()
