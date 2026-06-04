#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tooluse_copyhead_ab.py — COPY-ATTENTION / POINTER head + F-COPYHEAD-ARGCOPY falsifier.

ROOT-CAUSE architectural fix for the #1835 🔴 CLOSED-NEGATIVE (correct_call=0/36): a
standard byte-LM at 18M has NO mechanism to copy a token from the prompt verbatim, so
it INVENTS a training-distribution-shaped key instead of COPYING the asked held-out key.
#1835 proved that adding more copy-shaped demos does NOT teach the copy operation — the
lever is an explicit copy/pointer mechanism, not corpus.

THE FIX — gated pointer-attention head (pointer-network style, bolted onto the VERBATIM
#1835 ConsciousLMReconstructed arch):
  At each output step the model produces, besides the standard A/G byte-LM logits:
    · a COPY query  q_c = W_q · h_t           (from the final hidden state h_t)
    · COPY keys     k_i = W_k · h_i           (over ALL prompt/context positions i<=t)
    · copy attention a = softmax(q_c·k_i / sqrt(d))   (causal — only positions <= t)
    · a COPY distribution over the 256-byte vocab = scatter_add(a_i onto the input byte
      at position i)  — i.e. "probability the next byte is a verbatim copy of input[i]"
    · a learned GATE  g_t = sigmoid(W_g · h_t) in [0,1]
  Final next-byte distribution:  P = (1 - g_t) * softmax(lm_logits) + g_t * copy_dist
  Loss is NLL on that MIXED distribution (so the gate + pointer learn jointly with the LM).

  This routes "the asked key in the prompt" -> "the call arg" STRUCTURALLY: the pointer
  attends to the key's byte positions and the gate opens to copy them, instead of the LM
  head sampling a shape-plausible key. The copy mechanism is content-agnostic — it copies
  whatever bytes the prompt holds (p1..p8 clean: no identity/persona/role injection, it is
  an architectural copy operator, not a learned fact or instruction).

ENV/FLAG GATE (HEXA-FUSION graph-off style):  COPY_HEAD=0  ->  head fully bypassed, the
forward is BYTE-IDENTICAL to the original #1835 arch (max|Δ|=0 over logits, asserted by
--byte-eq-check). COPY_HEAD=1 -> pointer+gate active.

PRE-REGISTERED FALSIFIER (p7 script-checked, NO perplexity):
  F-COPYHEAD-ARGCOPY        : PASS iff with-copyhead correct_call_rate >= 0.50 on the SAME
                              36 held-out PBnn keys as #1835 (baseline 0/36) AND end-to-end
                              grounding_rate rises correspondingly (>= 0.50).
  F-COPYHEAD-OFF-MIRROR     : SAME ckpt, copy gate FORCED OFF (COPY_HEAD=0 at eval) -> MUST
                              FAIL to copy (proves the head — not the LM weights — does the
                              copy work).
  F-COPYHEAD-RANDINIT-MIRROR: random-init model + copy head + same harness -> MUST FAIL
                              (proves learned capability, not eval leakage / a trivial copy).
  F-COPYHEAD-NOTOOL-MIRROR  : with-copyhead, tool DISABLED -> MUST FAIL to ground (the
                              end-to-end win came from REAL grounding, not cosmetic copy).

Honest ruling (a_paper_negative_ok): 🟢 if the copy head lifts correct_call >= 0.50 at 18M
(a_scale_honest_scope TOY scope) AND all mirrors fail; 🔴 closed-negative if the head does
NOT learn to point (then the corpus signal or head design is the next lever).

Lane G (a_lane_akida_gpu_split): GPU substrate, NO AKIDA. Arch base = ConsciousLMReconstructed
18M byte, VERBATIM from tooluse_argcopy_ab.py (#1835) + the COPY head. p1..p8 clean.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

# ═══════════════ arch (VERBATIM #1835 base) + COPY head ═══════════════


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


class CopyHead(nn.Module):
    """Gated pointer-attention copy head.

    Given the per-position hidden states H (B,T,C) AND the input byte ids (B,T), produces
    a copy log-distribution over the 256-byte vocab at every position, plus a per-position
    gate. The copy distribution at output step t = causal attention over input positions
    i<=t, scattered onto vocab by the input byte at i — "next byte is a verbatim copy of
    the byte at the attended input position".
    """

    def __init__(self, d_model: int, vocab_size: int, copy_dim: int = 64):
        super().__init__()
        self.vocab_size = vocab_size
        self.copy_dim = copy_dim
        self.q = nn.Linear(d_model, copy_dim)
        self.k = nn.Linear(d_model, copy_dim)
        self.gate = nn.Linear(d_model, 1)
        # init gate bias slightly negative -> starts near "mostly LM", learns to open
        nn.init.constant_(self.gate.bias, -2.0)

    def forward(self, H, idx):
        # H: (B,T,C)  idx: (B,T) input byte ids
        B, T, C = H.shape
        q = self.q(H)                                   # (B,T,d)
        k = self.k(H)                                   # (B,T,d)
        scores = (q @ k.transpose(-2, -1)) / math.sqrt(self.copy_dim)   # (B,T,T) step t attends pos i
        mask = torch.tril(torch.ones(T, T, device=H.device, dtype=torch.bool)).view(1, T, T)
        scores = scores.masked_fill(~mask, float("-inf"))
        attn = F.softmax(scores, dim=-1)                # (B,T,T) row t = dist over input pos i<=t
        # scatter attn onto vocab via input byte at pos i  -> copy_prob (B,T,V)
        copy_prob = torch.zeros(B, T, self.vocab_size, device=H.device, dtype=attn.dtype)
        # idx_exp: (B,T,T) the byte at input pos i, broadcast across output step t
        idx_exp = idx.unsqueeze(1).expand(B, T, T)      # (B, t, i) = byte at input pos i
        copy_prob.scatter_add_(2, idx_exp, attn)        # add attn weight at vocab slot = input byte
        gate = torch.sigmoid(self.gate(H))              # (B,T,1) in [0,1]
        return copy_prob, gate


class ConsciousLMReconstructed(nn.Module):
    def __init__(self, vocab_size=256, d_model=384, n_head=4, n_layer=6, block_size=256,
                 dropout=0.0, copy_head=False, copy_dim=64):
        super().__init__()
        self.block_size = block_size
        self.vocab_size = vocab_size
        self.use_copy = copy_head
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(block_size, d_model)
        self.blocks = nn.ModuleList([Block(d_model, n_head, block_size, dropout) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d_model)
        self.head_a = nn.Linear(d_model, vocab_size, bias=False)
        self.head_g = nn.Linear(d_model, vocab_size, bias=False)
        # COPY head — only constructed when enabled (keeps base state_dict load clean)
        self.copy = CopyHead(d_model, vocab_size, copy_dim) if copy_head else None

    def _trunk(self, idx):
        B, T = idx.shape
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        for blk in self.blocks:
            x, _ = blk(x)
        return self.ln_f(x)

    def forward(self, idx):
        """Returns (logits_a, logits_g) — VERBATIM #1835 signature. Byte-identical when
        copy is OFF (the copy head is never read here, so head-OFF == original arch)."""
        h = self._trunk(idx)
        return self.head_a(h), self.head_g(h)

    def forward_logprob(self, idx, copy_enabled: bool):
        """Returns log P(next byte) over vocab at every position.
        copy_enabled=False -> log of the pure A/G LM mix (the original arch's sampling dist).
        copy_enabled=True  -> log of (1-g)*softmax(lm) + g*copy_dist.
        The HEAD-OFF path is numerically the original-arch distribution (no copy params read).
        """
        h = self._trunk(idx)
        la, lg = self.head_a(h), self.head_g(h)
        lm_logits = 0.5 * la + 0.5 * lg                 # the #1835 sampling logits (0.5/0.5 mix)
        lm_prob = F.softmax(lm_logits, dim=-1)
        if not copy_enabled or self.copy is None:
            return torch.log(lm_prob.clamp_min(1e-12))
        copy_prob, gate = self.copy(h, idx)
        mixed = (1.0 - gate) * lm_prob + gate * copy_prob
        return torch.log(mixed.clamp_min(1e-12))


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


# ═══════════════ toy tool registry (held-out PB probe table — VERBATIM #1835 §8) ═══════════════

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


# ═══════════════ generation (uses forward_logprob so the copy head drives sampling) ═══════════════


@torch.no_grad()
def gen_bytes(model, prompt_bytes: bytes, max_new: int, device, copy_enabled: bool,
              temperature=0.8, top_k=40, rep_penalty=1.1, stop_on_end=True):
    model.eval()
    ids = list(prompt_bytes)[-model.block_size :]
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out = []
    for _ in range(max_new):
        logprob = model.forward_logprob(idx[:, -model.block_size :], copy_enabled)
        logits = logprob[:, -1, :].clone()             # log P over vocab at last step
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


# ═══════════════ probe set (36 held-out keys, 5-lang — VERBATIM #1835) ═══════════════

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


# ═══════════════ grounded eval loop (VERBATIM #1835 + copy_enabled threading) ═══════════════


@torch.no_grad()
def eval_probe(model, probe, device, copy_enabled, tool_enabled=True, max_calls=2,
               max_new=96, temperature=0.7, top_k=40):
    key = probe["key"]; answer = probe["answer"]
    seed = (f"사용자: {probe['question']} | 도우미: ").encode("utf-8")
    transcript = seed
    emitted_call = False; correct_call = False; grounded = False; calls = 0
    while True:
        emit = gen_bytes(model, transcript, max_new, device, copy_enabled,
                         temperature=temperature, top_k=top_k, stop_on_end=True)
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


def run_eval(model, probes, device, label, copy_enabled, tool_enabled=True):
    rows = [eval_probe(model, p, device, copy_enabled, tool_enabled=tool_enabled) for p in probes]
    n = len(rows)
    fab = sum(1 for r in rows if r["class"] == "fabricated")
    grd = sum(1 for r in rows if r["class"] == "grounded")
    abst = sum(1 for r in rows if r["class"] == "abstained")
    callrate = sum(1 for r in rows if r["emitted_call"]) / n
    correctcall = sum(1 for r in rows if r["correct_call"]) / n
    return {"label": label, "n": n, "tool_enabled": tool_enabled, "copy_enabled": copy_enabled,
            "fabricated": fab, "grounded": grd, "abstained": abst,
            "fabrication_rate": round(fab / n, 4), "grounding_rate": round(grd / n, 4),
            "call_rate": round(callrate, 4), "correct_call_rate": round(correctcall, 4),
            "correct_call_n": sum(1 for r in rows if r["correct_call"]),
            "grounded_n": grd, "rows": rows}


# ═══════════════ train ═══════════════


def count_params(m):
    return sum(p.numel() for p in m.parameters())


def train_arm(base_ckpt, corpus_path, cfg, steps, batch, block, lr, warmup, seed, device,
              label, out_dir, copy_head: bool):
    torch.manual_seed(seed); random.seed(seed)
    model = ConsciousLMReconstructed(256, cfg["dim"], cfg["heads"], cfg["layers"],
                                     cfg["block_size"], copy_head=copy_head).to(device)
    # load base into the trunk + A/G heads (copy head params are fresh — strict=False)
    missing, unexpected = model.load_state_dict(base_ckpt["model_state"], strict=False)
    base_missing = [m for m in missing if not m.startswith("copy.")]
    assert not base_missing, f"base trunk/head keys missing: {base_missing[:5]}"
    assert not unexpected, f"unexpected base keys: {unexpected[:5]}"
    nparams = count_params(model)
    corpus = ByteCorpus(corpus_path, block)
    print(f"[{label}] base loaded ~{nparams/1e6:.2f}M | copy_head={copy_head} | corpus {corpus_path} "
          f"{len(corpus.data)} bytes | device={device} | fresh-copy-params="
          f"{sum(p.numel() for n,p in model.named_parameters() if n.startswith('copy.'))}", flush=True)
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
        logprob = model.forward_logprob(x, copy_enabled=copy_head)   # NLL on the MIXED dist
        loss = F.nll_loss(logprob.reshape(-1, 256), y.reshape(-1))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if step % 100 == 0 or step == 1:
            ce_log.append((step, loss.item()))
            print(f"[{label}] step {step}/{steps} ce={loss.item():.4f} lr={lr_at(step):.2e} "
                  f"wall={time.time()-t0:.0f}s", flush=True)
    ckpt_path = Path(out_dir) / f"tooluse_copyhead_{label}_18m.pt"
    torch.save({"model_state": model.state_dict(), "config": cfg, "params": nparams,
                "ft_steps": steps, "ce_log": ce_log, "seed": seed, "arm": label,
                "copy_head": copy_head, "base": "anima-clm-chat-rung0-byte-18m"}, ckpt_path)
    print(f"[{label}] saved {ckpt_path}  final_ce(nll)={ce_log[-1][1]:.4f}", flush=True)
    return model, nparams, ce_log, str(ckpt_path)


def byte_eq_check(base_ckpt, cfg, device):
    """HEXA-FUSION graph-off check: COPY_HEAD model with copy_enabled=False must produce
    a forward BYTE-IDENTICAL to the no-copy model (the copy params are never read)."""
    torch.manual_seed(7)
    m_off = ConsciousLMReconstructed(256, cfg["dim"], cfg["heads"], cfg["layers"],
                                     cfg["block_size"], copy_head=False).to(device)
    m_off.load_state_dict(base_ckpt["model_state"], strict=True)
    torch.manual_seed(7)
    m_on = ConsciousLMReconstructed(256, cfg["dim"], cfg["heads"], cfg["layers"],
                                    cfg["block_size"], copy_head=True).to(device)
    m_on.load_state_dict(base_ckpt["model_state"], strict=False)
    m_off.eval(); m_on.eval()
    x = torch.randint(0, 256, (2, 64), device=device)
    with torch.no_grad():
        # forward() path (A/G logits) — never touches copy head
        la0, lg0 = m_off(x); la1, lg1 = m_on(x)
        d_fwd = max((la0 - la1).abs().max().item(), (lg0 - lg1).abs().max().item())
        # forward_logprob with copy DISABLED — must equal the no-copy logprob
        lp0 = m_off.forward_logprob(x, copy_enabled=False)
        lp1 = m_on.forward_logprob(x, copy_enabled=False)
        d_lp = (lp0 - lp1).abs().max().item()
    return d_fwd, d_lp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-ckpt", required=True)
    ap.add_argument("--corpus", required=True, help="argcopy agent-lane corpus (with-copyhead arm)")
    ap.add_argument("--out-dir", default="state/tooluse_copyhead/out")
    ap.add_argument("--steps", type=int, default=2500)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--warmup", type=int, default=100)
    ap.add_argument("--seed", type=int, default=42)
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

    # ── byte-eq check (head-OFF == original arch) ──
    d_fwd, d_lp = byte_eq_check(base, cfg, device)
    byte_eq_pass = (d_fwd == 0.0 and d_lp == 0.0)
    print(f"[byte-eq] head-OFF vs original-arch  max|Δ| forward={d_fwd}  forward_logprob(copy=off)={d_lp}  "
          f"-> {'PASS (byte-identical)' if byte_eq_pass else 'FAIL'}", flush=True)

    # ── train the with-copyhead arm (copy head ON) ──
    wc_model, nparams, wc_ce, wc_ckpt = train_arm(
        base, args.corpus, cfg, args.steps, args.batch, args.block,
        args.lr, args.warmup, args.seed, device, "with_copyhead", out, copy_head=True)

    # ── random-init mirror (copy head + same harness, NO base load) ──
    torch.manual_seed(args.seed + 1000)
    rand_model = ConsciousLMReconstructed(256, cfg["dim"], cfg["heads"], cfg["layers"],
                                          cfg["block_size"], copy_head=True).to(device)

    probes = build_probes()
    print(f"[probes] {len(probes)} unknowable-without-tool probes (held-out PB keys, 5-lang)", flush=True)

    # eval: with-copyhead (copy ON), head-OFF mirror (SAME ckpt copy OFF), notool, randinit
    e_wc = run_eval(wc_model, probes, device, "with_copyhead", copy_enabled=True, tool_enabled=True)
    e_off = run_eval(wc_model, probes, device, "copyhead_OFF_mirror", copy_enabled=False, tool_enabled=True)
    e_notool = run_eval(wc_model, probes, device, "with_copyhead_NOTOOL", copy_enabled=True, tool_enabled=False)
    e_rand = run_eval(rand_model, probes, device, "randinit_copyhead_mirror", copy_enabled=True, tool_enabled=True)

    cc_wc = e_wc["correct_call_rate"]; gr_wc = e_wc["grounding_rate"]
    cc_off = e_off["correct_call_rate"]; gr_off = e_off["grounding_rate"]

    # ── F-COPYHEAD-ARGCOPY ──
    copyhead_cc_pass = cc_wc >= args.bar_correct_call
    copyhead_gr_pass = gr_wc >= args.bar_grounding
    copyhead_pass = copyhead_cc_pass and copyhead_gr_pass

    # ── mirrors ──
    off_mirror_pass = (cc_off < args.bar_correct_call)              # head OFF must FAIL to copy
    rand_mirror_pass = (e_rand["grounding_rate"] == 0.0)           # random-init must FAIL
    notool_mirror_pass = (e_notool["grounding_rate"] == 0.0)       # tool disabled must FAIL to ground

    terminal_pass = copyhead_pass and off_mirror_pass and rand_mirror_pass and notool_mirror_pass
    if terminal_pass and byte_eq_pass:
        ruling = "GREEN"
        verdict_text = ("\U0001f7e2 COPY-HEAD WORKS at toy scale (18M) — the gated pointer head lifts "
                        f"correct_call from 0.0 (#1835) to {cc_wc} (>= {args.bar_correct_call}) and end-to-end "
                        f"grounding to {gr_wc} (>= {args.bar_grounding}) on HELD-OUT keys; head-OFF mirror "
                        f"correct_call={cc_off} (< bar, the head does the work), random-init + notool both FAIL, "
                        "and head-OFF forward is BYTE-IDENTICAL to the original arch. Key-binding residual CLOSED "
                        "(structural copy, not corpus). ① 완성도 lever delivered.")
    elif not byte_eq_pass:
        ruling = "RED-BYTEEQ"
        verdict_text = ("\U0001f534 head-OFF is NOT byte-identical to the original arch (max|Δ| forward="
                        f"{d_fwd} logprob={d_lp}) — the gate must be reversible before any pass is honest.")
    elif not copyhead_pass:
        ruling = "RED"
        verdict_text = ("\U0001f534 CLOSED-NEGATIVE: the copy head did NOT learn to point at 18M — "
                        f"correct_call={cc_wc} (bar {args.bar_correct_call}) / grounding={gr_wc} "
                        f"(bar {args.bar_grounding}). The pointer mechanism alone ⊥ held-out key-binding at "
                        "toy scale; next lever = head design (multi-head pointer / explicit copy-loss) or "
                        "corpus copy-signal strength.")
    else:
        ruling = "RED-MIRROR"
        verdict_text = ("\U0001f534 CLOSED-NEGATIVE (mirror leak): ARGCOPY passed but a mirror did NOT fail — "
                        f"off_mirror_cc={cc_off} randinit_gr={e_rand['grounding_rate']} "
                        f"notool_gr={e_notool['grounding_rate']}; the apparent win is leaked/cosmetic.")

    summary = {
        "experiment": "rung-0 COPY-ATTENTION / POINTER head — architectural fix for verbatim key-copy (#1835 residual)",
        "substrate": "GPU (Lane G; a_lane_akida_gpu_split — NOT AKIDA)",
        "gpu": torch.cuda.get_device_name(0),
        "base": "dancinlab/anima-clm-chat-rung0-byte-18m",
        "params": nparams,
        "scope": "TOY 18M only — a_scale_honest_scope; transfer to mid/7B UNVERIFIED",
        "baseline_1835": {"correct_call_rate": 0.0, "grounding_rate": 0.0,
                          "note": "#1835 with_argcopy: call_rate 0.83 but correct_call 0/36 (no copy mechanism)"},
        "bars": {"correct_call": args.bar_correct_call, "grounding": args.bar_grounding},
        "byte_eq": {"head_off_forward_maxabs_delta": d_fwd,
                    "head_off_forward_logprob_maxabs_delta": d_lp,
                    "byte_identical": byte_eq_pass},
        "arms": {
            "with_copyhead": {"ckpt": wc_ckpt, "final_ce_nll": wc_ce[-1][1],
                              "fabrication_rate": e_wc["fabrication_rate"], "grounding_rate": gr_wc,
                              "call_rate": e_wc["call_rate"], "correct_call_rate": cc_wc,
                              "correct_call_n": e_wc["correct_call_n"], "grounded_n": e_wc["grounded_n"]},
        },
        "F_COPYHEAD_ARGCOPY": {
            "with_copyhead_correct_call_rate": cc_wc, "with_copyhead_grounding_rate": gr_wc,
            "bar_correct_call": args.bar_correct_call, "bar_grounding": args.bar_grounding,
            "correct_call_pass": copyhead_cc_pass, "grounding_pass": copyhead_gr_pass,
            "verdict": "PASS" if copyhead_pass else "FAIL"},
        "F_COPYHEAD_OFF_MIRROR": {
            "same_ckpt_copy_off_correct_call_rate": cc_off, "same_ckpt_copy_off_grounding_rate": gr_off,
            "must_fail_to_copy": True, "verdict": "PASS" if off_mirror_pass else "FAIL"},
        "F_COPYHEAD_RANDINIT_MIRROR": {
            "randinit_grounding_rate": e_rand["grounding_rate"], "must_fail_grounding": True,
            "verdict": "PASS" if rand_mirror_pass else "FAIL"},
        "F_COPYHEAD_NOTOOL_MIRROR": {
            "with_copyhead_NOTOOL_grounding_rate": e_notool["grounding_rate"], "must_fail_to_ground": True,
            "verdict": "PASS" if notool_mirror_pass else "FAIL"},
        "ruling": ruling, "terminal_pass": terminal_pass, "verdict_text": verdict_text,
    }

    (out / "eval_with_copyhead.json").write_text(json.dumps(e_wc, ensure_ascii=False, indent=2))
    (out / "eval_off_mirror.json").write_text(json.dumps(e_off, ensure_ascii=False, indent=2))
    (out / "eval_notool_mirror.json").write_text(json.dumps(e_notool, ensure_ascii=False, indent=2))
    (out / "eval_randinit_mirror.json").write_text(json.dumps(e_rand, ensure_ascii=False, indent=2))
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    print("\n================= FALSIFIER VERDICTS (verbatim) =================", flush=True)
    print(f"BYTE-EQ (head-OFF == original arch): forward max|Δ|={d_fwd} logprob(copy=off) max|Δ|={d_lp} "
          f"-> {'PASS' if byte_eq_pass else 'FAIL'}", flush=True)
    print(f"F-COPYHEAD-ARGCOPY         : with_copyhead correct_call={cc_wc} (>= {args.bar_correct_call}?) "
          f"grounding={gr_wc} (>= {args.bar_grounding}?)  [baseline #1835: correct_call=0.0 grounding=0.0]  "
          f"-> {'PASS' if copyhead_pass else 'FAIL'}", flush=True)
    print(f"F-COPYHEAD-OFF-MIRROR      : same ckpt, copy OFF correct_call={cc_off} grounding={gr_off} "
          f"(MUST be < {args.bar_correct_call}) -> {'PASS' if off_mirror_pass else 'FAIL'}", flush=True)
    print(f"F-COPYHEAD-RANDINIT-MIRROR : random_init grounding={e_rand['grounding_rate']} "
          f"(MUST be 0) -> {'PASS' if rand_mirror_pass else 'FAIL'}", flush=True)
    print(f"F-COPYHEAD-NOTOOL-MIRROR   : with_copyhead+tool_disabled grounding={e_notool['grounding_rate']} "
          f"(MUST be 0) -> {'PASS' if notool_mirror_pass else 'FAIL'}", flush=True)
    print(f"\nRULING: {ruling}\n{verdict_text}", flush=True)
    print("\n=== SUMMARY ===", flush=True)
    print(json.dumps({k: v for k, v in summary.items() if k != "arms"} | {"arms": summary["arms"]},
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
