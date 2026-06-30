#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tooluse_argcopy_ab.py — rung-0 ARGUMENT-COPY A/B fire + F-TOOLUSE-ARGCOPY falsifier.

Closes the 🟠 KEY-BINDING residual the chatreg fire (#1833) surfaced: the model CALLS
the tool 36/36 but binds the arg to a MEMORIZED demo key instead of COPYING the asked
held-out PBnn key, so correct_call=0/36 and end-to-end grounding=0/36.

THE EXPERIMENT
  Does an agent-lane corpus that forces ARGUMENT-COPY (a LARGE space of fresh per-demo
  keys, each used ~once, so memorization cannot win — `serving/agent_lane_argcopy_gen.py`)
  teach the byte-LM mouth to ECHO the asked held-out key into the call arg, lifting
  correct_call (and thus end-to-end grounding) off the 0/36 baseline?

  Two arms, SAME base ckpt, SAME steps/compute, EQUAL byte-count — only the corpus differs:
    · with-argcopy : base-18M continue-train on the argcopy agent-lane corpus
    · no-grammar   : base-18M continue-train on equal-byte base filler, NO tool demos

  Probe set = the SAME 36 held-out PBnn keys (values in NEITHER corpus, leak-verified=0).
  Eval = the REAL agent_step_grounded loop (emit -> parse_call_frame -> tier gate ->
  exec fact_lookup(held-out key) -> inject REAL value anchor -> RESUME grounded).

PRE-REGISTERED FALSIFIER (p7 script-checked, NO perplexity):
  F-TOOLUSE-ARGCOPY        : PASS iff (1) with-argcopy correct_call_rate >= 0.50 (lifted
                             off the 0/36 baseline) AND (2) end-to-end grounding_rate rises
                             correspondingly (>= 0.50). The arg the model emits must EXACTLY
                             equal the asked held-out key; that the value is then reproduced
                             end-to-end is the grounding check.
  F-TOOLUSE-NOTOOL-MIRROR  : with-argcopy model, tool DISABLED -> MUST FAIL to ground
                             (proves the win is REAL grounding, not cosmetic markers).
  F-TOOLUSE-RANDINIT-MIRROR: random-init model + same harness -> MUST FAIL grounding
                             (proves learned capability, not eval leakage).

Honest ruling (a_paper_negative_ok): 🟢 if argcopy lifts correct_call AND grounding past
the bar AND both mirrors fail; 🔴 closed-negative if copying does NOT transfer to the
held-out keys (then the lever moves to an explicit copy-attention mechanism).

Lane G (a_lane_akida_gpu_split): GPU substrate, NO AKIDA. Arch = ConsciousLMReconstructed
18M byte, VERBATIM from tooluse_rung0_ab.py. p1..p8: 0xFE/0xFF learned grammar, not identity.
Scope (a_scale_honest_scope): TOY 18M ONLY; mid/7B transfer UNVERIFIED.
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

# ═══════════════ arch (VERBATIM from training/tooluse_rung0_ab.py) ═══════════════


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


# ═══════════════ toy tool registry (held-out PB probe table — design §8) ═══════════════

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


# ═══════════════ probe set (36 held-out keys, 5-lang) ═══════════════

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


# ═══════════════ grounded eval loop ═══════════════


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
    asserts_answer = _asserts_specific(final_text, key)
    if not grounded and not emitted_call and asserts_answer:
        cls = "fabricated"
    elif grounded:
        cls = "grounded"
    else:
        cls = "abstained"
    return {"key": key, "lang": probe["lang"], "class": cls, "emitted_call": emitted_call,
            "correct_call": correct_call, "grounded": grounded, "asserts_answer": asserts_answer,
            "reply": final_text[:240]}


def _asserts_specific(text: str, key: str) -> bool:
    t = text.strip()
    if len(t) < 4:
        return False
    import re
    if re.search(r"[a-zA-Z]+-[a-zA-Z]+-[a-zA-Z]+", t):
        return True
    for d in ("= ", ": ", "-> ", "→ ", "는 ", "은 ", "이다", "값은", "value is", "is "):
        i = t.find(d)
        if i >= 0:
            tail = t[i + len(d):].strip()
            tok = tail.split()[0] if tail.split() else ""
            if len(tok) >= 3 and tok != key:
                return True
    return False


def run_eval(model, probes, device, label, tool_enabled=True):
    rows = [eval_probe(model, p, device, tool_enabled=tool_enabled) for p in probes]
    n = len(rows)
    fab = sum(1 for r in rows if r["class"] == "fabricated")
    grd = sum(1 for r in rows if r["class"] == "grounded")
    abst = sum(1 for r in rows if r["class"] == "abstained")
    callrate = sum(1 for r in rows if r["emitted_call"]) / n
    correctcall = sum(1 for r in rows if r["correct_call"]) / n
    return {"label": label, "n": n, "tool_enabled": tool_enabled,
            "fabricated": fab, "grounded": grd, "abstained": abst,
            "fabrication_rate": round(fab / n, 4), "grounding_rate": round(grd / n, 4),
            "call_rate": round(callrate, 4), "correct_call_rate": round(correctcall, 4),
            "correct_call_n": sum(1 for r in rows if r["correct_call"]),
            "grounded_n": grd, "rows": rows}


# ═══════════════ train ═══════════════


def count_params(m):
    return sum(p.numel() for p in m.parameters())


def train_arm(base_ckpt, corpus_path, cfg, steps, batch, block, lr, warmup, seed, device, label, out_dir):
    torch.manual_seed(seed); random.seed(seed)
    model = ConsciousLMReconstructed(256, cfg["dim"], cfg["heads"], cfg["layers"], cfg["block_size"]).to(device)
    model.load_state_dict(base_ckpt["model_state"])
    nparams = count_params(model)
    corpus = ByteCorpus(corpus_path, block)
    print(f"[{label}] base loaded ~{nparams/1e6:.2f}M | corpus {corpus_path} {len(corpus.data)} bytes | device={device}", flush=True)
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
        if step % 100 == 0 or step == 1:
            ce_log.append((step, loss.item()))
            print(f"[{label}] step {step}/{steps} ce={loss.item():.4f} lr={lr_at(step):.2e} wall={time.time()-t0:.0f}s", flush=True)
    ckpt_path = Path(out_dir) / f"tooluse_argcopy_{label}_18m.pt"
    torch.save({"model_state": model.state_dict(), "config": cfg, "params": nparams,
                "ft_steps": steps, "ce_log": ce_log, "seed": seed, "arm": label,
                "base": "anima-clm-chat-rung0-byte-18m"}, ckpt_path)
    print(f"[{label}] saved {ckpt_path}  final_ce={ce_log[-1][1]:.4f}", flush=True)
    return model, nparams, ce_log, str(ckpt_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-ckpt", required=True)
    ap.add_argument("--corpus-with-argcopy", required=True)
    ap.add_argument("--corpus-no-grammar", required=True)
    ap.add_argument("--out-dir", default="state/tooluse_argcopy/out")
    ap.add_argument("--steps", type=int, default=2500)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--warmup", type=int, default=100)
    ap.add_argument("--seed", type=int, default=42)
    # pre-registered bars
    ap.add_argument("--bar-correct-call", type=float, default=0.50)
    ap.add_argument("--bar-grounding", type=float, default=0.50)
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print("[FATAL] GPU REQUIRED (a_train_flame_forge) — no CUDA device. Refusing CPU fallback.", flush=True)
        raise SystemExit(3)
    print(f"[gpu] {torch.cuda.get_device_name(0)} cuda={torch.version.cuda}", flush=True)
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    base = torch.load(args.base_ckpt, map_location="cpu", weights_only=False)
    cfg = base["config"]
    print(f"[base] {args.base_ckpt} params={base.get('params')} cfg={cfg}", flush=True)

    # ── two arms (same base, same steps, equal byte-count corpora) ──
    wa_model, nparams, wa_ce, wa_ckpt = train_arm(
        base, args.corpus_with_argcopy, cfg, args.steps, args.batch, args.block,
        args.lr, args.warmup, args.seed, device, "with_argcopy", out)
    ng_model, _, ng_ce, ng_ckpt = train_arm(
        base, args.corpus_no_grammar, cfg, args.steps, args.batch, args.block,
        args.lr, args.warmup, args.seed, device, "no_grammar", out)

    # ── random-init mirror ──
    torch.manual_seed(args.seed + 1000)
    rand_model = ConsciousLMReconstructed(256, cfg["dim"], cfg["heads"], cfg["layers"], cfg["block_size"]).to(device)

    probes = build_probes()
    print(f"[probes] {len(probes)} unknowable-without-tool probes (held-out PB keys, 5-lang)", flush=True)

    e_wa = run_eval(wa_model, probes, device, "with_argcopy", tool_enabled=True)
    e_ng = run_eval(ng_model, probes, device, "no_grammar", tool_enabled=True)
    e_notool = run_eval(wa_model, probes, device, "with_argcopy_NOTOOL", tool_enabled=False)
    e_rand = run_eval(rand_model, probes, device, "random_init_mirror", tool_enabled=True)

    # ── F-TOOLUSE-ARGCOPY: correct_call lifted off 0/36 baseline AND grounding rises ──
    cc_wa = e_wa["correct_call_rate"]; cc_ng = e_ng["correct_call_rate"]
    gr_wa = e_wa["grounding_rate"]; gr_ng = e_ng["grounding_rate"]
    argcopy_correctcall_pass = cc_wa >= args.bar_correct_call
    argcopy_grounding_pass = gr_wa >= args.bar_grounding
    argcopy_pass = argcopy_correctcall_pass and argcopy_grounding_pass

    # ── mirrors: with-argcopy w/ tool disabled MUST FAIL to ground; random-init MUST FAIL ──
    notool_grounding = e_notool["grounding_rate"]
    notool_mirror_pass = (notool_grounding == 0.0)
    rand_grounding = e_rand["grounding_rate"]
    randinit_mirror_pass = (rand_grounding == 0.0)

    terminal_pass = argcopy_pass and notool_mirror_pass and randinit_mirror_pass
    if terminal_pass:
        ruling = "GREEN"
        verdict_text = ("\U0001f7e2 ARGUMENT-COPY WORKS at toy scale (18M) — a large fresh-key corpus "
                        f"lifts correct_call to {cc_wa} (>= {args.bar_correct_call}) and end-to-end grounding to "
                        f"{gr_wa} (>= {args.bar_grounding}) on HELD-OUT keys, AND both anti-Goodhart mirrors FAIL. "
                        "The key-binding residual is CLOSED at toy scale (copy generalizes to unseen keys).")
    elif not argcopy_pass:
        ruling = "RED"
        verdict_text = ("\U0001f534 CLOSED-NEGATIVE: argument-copy did NOT transfer at 18M — "
                        f"correct_call={cc_wa} (bar {args.bar_correct_call}) / grounding={gr_wa} (bar {args.bar_grounding}). "
                        "Copy-from-corpus alone ⊥ held-out key-binding; lever moves to an explicit "
                        "copy-attention / pointer mechanism.")
    else:
        ruling = "RED-MIRROR"
        verdict_text = ("\U0001f534 CLOSED-NEGATIVE (mirror leak): ARGCOPY passed but a mirror did NOT fail — "
                        "the apparent win is cosmetic/leaked, not real grounding.")

    summary = {
        "experiment": "rung-0 toy A/B argument-copy / key-binding (residual-closer for #1833)",
        "substrate": "GPU (Lane G; a_lane_akida_gpu_split — NOT AKIDA)",
        "gpu": torch.cuda.get_device_name(0),
        "base": "dancinlab/anima-clm-chat-rung0-byte-18m",
        "params": nparams,
        "scope": "TOY 18M only — a_scale_honest_scope; transfer to mid/7B UNVERIFIED",
        "baseline_from_1833": {"correct_call_rate": 0.0, "grounding_rate": 0.0,
                               "note": "chatreg arm-2: call_rate 1.0 but correct_call 0/36 (memorized demo key)"},
        "bars": {"correct_call": args.bar_correct_call, "grounding": args.bar_grounding},
        "arms": {
            "with_argcopy": {"ckpt": wa_ckpt, "final_ce": wa_ce[-1][1],
                             "fabrication_rate": e_wa["fabrication_rate"], "grounding_rate": gr_wa,
                             "call_rate": e_wa["call_rate"], "correct_call_rate": cc_wa,
                             "correct_call_n": e_wa["correct_call_n"], "grounded_n": e_wa["grounded_n"]},
            "no_grammar": {"ckpt": ng_ckpt, "final_ce": ng_ce[-1][1],
                           "fabrication_rate": e_ng["fabrication_rate"], "grounding_rate": gr_ng,
                           "call_rate": e_ng["call_rate"], "correct_call_rate": cc_ng,
                           "correct_call_n": e_ng["correct_call_n"], "grounded_n": e_ng["grounded_n"]},
        },
        "F_TOOLUSE_ARGCOPY": {
            "with_argcopy_correct_call_rate": cc_wa, "no_grammar_correct_call_rate": cc_ng,
            "with_argcopy_grounding_rate": gr_wa, "no_grammar_grounding_rate": gr_ng,
            "bar_correct_call": args.bar_correct_call, "bar_grounding": args.bar_grounding,
            "correct_call_pass": argcopy_correctcall_pass, "grounding_pass": argcopy_grounding_pass,
            "verdict": "PASS" if argcopy_pass else "FAIL",
        },
        "F_TOOLUSE_NOTOOL_MIRROR": {
            "with_argcopy_NOTOOL_grounding_rate": notool_grounding, "must_fail_to_ground": True,
            "verdict": "PASS" if notool_mirror_pass else "FAIL"},
        "F_TOOLUSE_RANDINIT_MIRROR": {
            "random_init_grounding_rate": rand_grounding, "must_fail_grounding": True,
            "verdict": "PASS" if randinit_mirror_pass else "FAIL"},
        "ruling": ruling, "terminal_pass": terminal_pass, "verdict_text": verdict_text,
    }

    (out / "eval_with_argcopy.json").write_text(json.dumps(e_wa, ensure_ascii=False, indent=2))
    (out / "eval_no_grammar.json").write_text(json.dumps(e_ng, ensure_ascii=False, indent=2))
    (out / "eval_notool_mirror.json").write_text(json.dumps(e_notool, ensure_ascii=False, indent=2))
    (out / "eval_randinit_mirror.json").write_text(json.dumps(e_rand, ensure_ascii=False, indent=2))
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    print("\n================= FALSIFIER VERDICTS (verbatim) =================", flush=True)
    print(f"F-TOOLUSE-ARGCOPY        : with_argcopy correct_call={cc_wa} (>= {args.bar_correct_call}?) "
          f"grounding={gr_wa} (>= {args.bar_grounding}?)  [baseline #1833: correct_call=0.0 grounding=0.0]  "
          f"-> {'PASS' if argcopy_pass else 'FAIL'}", flush=True)
    print(f"  (control no_grammar    : correct_call={cc_ng} grounding={gr_ng} call_rate={e_ng['call_rate']})", flush=True)
    print(f"F-TOOLUSE-NOTOOL-MIRROR  : with_argcopy+tool_disabled grounding={notool_grounding} "
          f"(MUST be 0) -> {'PASS' if notool_mirror_pass else 'FAIL'}", flush=True)
    print(f"F-TOOLUSE-RANDINIT-MIRROR: random_init grounding={rand_grounding} "
          f"(MUST be 0) -> {'PASS' if randinit_mirror_pass else 'FAIL'}", flush=True)
    print(f"\nRULING: {ruling}\n{verdict_text}", flush=True)
    print("\n=== SUMMARY ===", flush=True)
    print(json.dumps({k: v for k, v in summary.items() if k != "arms"} | {"arms": summary["arms"]},
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
