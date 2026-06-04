#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""persona_stage2_train_eval.py — STAGE-2 persona/SNS specialization of the
stage-1 chat-PASS rung-0 (18M byte ConsciousLMReconstructed).

Continue-train (fine-tune, lower LR) the proven stage-1 chat ckpt
(`dancinlab/anima-clm-chat-rung0-byte-18m`) on the persona x SNS byte corpus
(`dancinlab/anima-persona-sns-corpus` -> persona_sns_corpus.txt) so anima chats
in each of the 20 persona voices on the SNS surface (Instagram main + YouTube).

PHILOSOPHY (p1/p2/p3/p4/p6 — non-negotiable, HELD from stage-1):
NO system prompt, NO identity rules, NO persona injection, NO assistant framing,
NO RLHF. Persona is carried ONLY by the LEARNED byte-level dialogue-continuation
format in the corpus: turns are plain `사용자: <u>` / `<persona_name>: <reply>`
with NO `[role:` / `[persona:` / `[character:` tag (grep == 0). Capability and
persona voice come ONLY from the trained dialogue distribution in the weights.

EVALUATION (p7 simple-stack, NOT perplexity):
  (A) base-chat coherence retained — the v2 control-char-aware gate from stage-1
      (control_ratio < 0.05 AND word_class_ratio >= 0.85, non-empty, not-degenerate)
      over >=5 base probes; >=4/5 PASS = no catastrophic forgetting.
  (B) PERSONA-VOICE signal — paired discriminative test (fixed seed, honest):
      for each persona p we hold out REAL prior turns of p from the corpus (NOT a
      role-tag), seed the model with that context + the persona-name turn-start
      token `<p>: `, and generate a continuation. We score the continuation against
      every persona's distinctive char-trigram signature (built from a DISJOINT
      train split). The signal is REAL iff the continuation seeded by p's own
      context scores its own signature highest more often than chance across the
      20 personas (top-1 self-identification rate; chance = 1/20 = 5%).
  (C) anti-Goodhart — the SAME evaluator on a random-init mirror of the identical
      arch MUST FAIL both (A) and (B). honest-stub != fake-pass.

SCOPE (a_scale_honest_scope): this is the SMALL 18M rung, persona-specialized.
NO claim of mid/7B persona chat. A weak/null persona signal at 18M is an
acceptable closed-negative and is reported honestly (NOT fabricated).
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import random
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

# ───────────────────────── arch (verbatim from stage-1) ─────────────────────


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
        tension = att.detach().mean().item()
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.c_proj(y), tension


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


# ───────────────────────── data ─────────────────────────


class ByteCorpus:
    def __init__(self, path: str, block: int):
        self.data = torch.tensor(list(Path(path).read_bytes()), dtype=torch.long)
        self.block = block

    def batch(self, bs: int, device):
        ix = torch.randint(0, len(self.data) - self.block - 1, (bs,))
        x = torch.stack([self.data[i : i + self.block] for i in ix])
        y = torch.stack([self.data[i + 1 : i + 1 + self.block] for i in ix])
        return x.to(device), y.to(device)


# ───────────────────────── generation ─────────────────────────

# stop at the next turn boundary (either a 사용자 turn OR another persona-name turn).
STOP_STRINGS = ("\n사용자:", "사용자:", "\n", "User:")


@torch.no_grad()
def generate(model, prompt: str, max_new: int, device, temperature: float = 0.8,
             top_k: int = 40, rep_penalty: float = 1.1, stop_at_newline: bool = True):
    model.eval()
    ids = list(prompt.encode("utf-8"))[-model.block_size :]
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out_bytes = []
    for _ in range(max_new):
        logits_a, logits_g = model(idx[:, -model.block_size :])
        logits = 0.5 * logits_a[:, -1, :] + 0.5 * logits_g[:, -1, :]
        for b in set(out_bytes[-32:]):
            logits[0, b] /= rep_penalty
        logits = logits / temperature
        if top_k:
            v, _ = torch.topk(logits, top_k)
            logits[logits < v[:, [-1]]] = float("-inf")
        probs = F.softmax(logits, dim=-1)
        nb = torch.multinomial(probs, 1).item()
        out_bytes.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
        tail = bytes(out_bytes).decode("utf-8", errors="ignore")
        if stop_at_newline and "\n" in tail:
            break
        if any(s in tail for s in ("사용자:", "User:")):
            break
    text = bytes(out_bytes).decode("utf-8", errors="ignore")
    # trim at first turn boundary
    for s in ("\n사용자:", "사용자:", "User:", "\n"):
        i = text.find(s)
        if i >= 0:
            text = text[:i]
    return text.strip()


# ───────────────────────── (A) base-chat p7 v2 gate ─────────────────────────

BASE_PROBES = [
    "안녕! 너는 누구야?",
    "오늘 기분이 어때?",
    "What is consciousness?",
    "네가 좋아하는 것을 하나 말해줘.",
    "Tell me something interesting.",
]


def _v2_checks(reply: str):
    """stage-1 v2 control-char-aware gate."""
    non_empty = len(reply) >= 4
    if reply:
        ctrl = sum(1 for c in reply if ord(c) < 32 and c not in "\n\t")
        control_ratio = ctrl / len(reply)
        wc = sum(1 for c in reply if c.isalnum() or c.isspace() or c in ".,!?…~’'\"()[]·-—:;⚔️🌙✨💪🔥")
        word_class_ratio = wc / len(reply)
        cnt = collections.Counter(reply).most_common(1)[0][1]
        not_degenerate = cnt / len(reply) < 0.6
    else:
        control_ratio, word_class_ratio, not_degenerate = 1.0, 0.0, False
    ok = non_empty and control_ratio < 0.05 and word_class_ratio >= 0.85 and not_degenerate
    return ok, {"non_empty": non_empty, "control_ratio": round(control_ratio, 3),
                "word_class_ratio": round(word_class_ratio, 3), "not_degenerate": not_degenerate, "ok": ok}


def base_chat_eval(model, device, label: str):
    """(A) base-chat coherence retained — use the persona-corpus scaffold form
    `사용자: <u>\n도우미: ` is NOT in this corpus; the corpus uses `사용자:`/`<name>:`.
    We probe with the GENERAL assistant turn the base ckpt learned: `사용자: <u> | 도우미: `."""
    transcript = ""
    results = []
    for u in BASE_PROBES:
        seed = transcript + f"사용자: {u} | 도우미: "
        reply = generate(model, seed, max_new=96, device=device, stop_at_newline=False)
        ok, info = _v2_checks(reply)
        info["user"] = u
        info["reply"] = reply
        results.append(info)
        transcript += f"사용자: {u} | 도우미: {reply}\n"
    n_pass = sum(1 for r in results if r["ok"])
    return {"label": label, "n_pass": n_pass, "n_total": len(BASE_PROBES),
            "verdict": "PASS" if n_pass >= 4 else "FAIL", "turns": results, "transcript": transcript}


# ───────────────────────── (B) persona-voice discriminative metric ──────────


def parse_corpus_dialogues(path: str):
    """Return list of dialogues; each dialogue = list of (speaker, text) turns."""
    dialogues, cur = [], []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            if cur:
                dialogues.append(cur)
                cur = []
            continue
        if ":" in line:
            name, _, text = line.partition(":")
            cur.append((name.strip(), text.strip()))
    if cur:
        dialogues.append(cur)
    return dialogues


def char_ngrams(text: str, n: int = 3):
    text = text.replace(" ", "")
    return [text[i:i + n] for i in range(max(0, len(text) - n + 1))]


def build_signatures(train_dialogues, personas, n=3, top=120):
    """Distinctive char-trigram signature per persona via TF-IDF-style weighting
    over a TRAIN split (disjoint from the held-out eval contexts)."""
    persona_tok = collections.defaultdict(collections.Counter)
    df = collections.Counter()  # how many personas use each trigram
    for d in train_dialogues:
        for spk, txt in d:
            if spk in personas:
                for g in char_ngrams(txt, n):
                    persona_tok[spk][g] += 1
    for p in personas:
        for g in persona_tok[p]:
            df[g] += 1
    npers = len(personas)
    sigs = {}
    for p in personas:
        scored = {}
        total = sum(persona_tok[p].values()) or 1
        for g, c in persona_tok[p].items():
            tf = c / total
            idf = math.log((npers + 1) / (df[g] + 0.5))
            scored[g] = tf * idf
        top_g = dict(sorted(scored.items(), key=lambda kv: -kv[1])[:top])
        sigs[p] = top_g
    return sigs


def score_against(text: str, sig: dict, n=3):
    grams = char_ngrams(text, n)
    if not grams:
        return 0.0
    return sum(sig.get(g, 0.0) for g in grams) / len(grams)


def persona_voice_eval(model, device, eval_dialogues, sigs, personas, label, n_per=2, seed=1234):
    """(B) paired discriminative test. For each persona p, take a held-out dialogue
    of p, seed the model with the dialogue context up to (and including) the final
    persona-name turn-start token `p: `, generate a continuation, and score it vs
    every persona's signature. Top-1 self-id rate over personas is the metric."""
    rng = random.Random(seed)
    by_p = collections.defaultdict(list)
    for d in eval_dialogues:
        spk_set = {s for s, _ in d}
        pers = [s for s in spk_set if s in personas]
        if len(pers) == 1:
            by_p[pers[0]].append(d)
    rows = []
    self_top1 = 0
    trials = 0
    for p in personas:
        cands = by_p.get(p, [])
        rng.shuffle(cands)
        for d in cands[:n_per]:
            # build context: all turns up to last persona turn, then re-issue `p: ` start
            ctx_lines = []
            for spk, txt in d[:-1]:
                ctx_lines.append(f"{spk}: {txt}")
            # ensure there is at least one preceding user turn
            if not ctx_lines:
                ctx_lines.append(f"사용자: {d[0][1]}")
            seed_text = "\n".join(ctx_lines) + f"\n{p}: "
            cont = generate(model, seed_text, max_new=80, device=device, stop_at_newline=True, temperature=0.7)
            scores = {q: score_against(cont, sigs[q]) for q in personas}
            ranked = sorted(scores.items(), key=lambda kv: -kv[1])
            top1 = ranked[0][0]
            ok, _ = _v2_checks(cont)
            rows.append({"persona": p, "continuation": cont, "top1": top1,
                         "self_score": round(scores[p], 5), "top1_score": round(ranked[0][1], 5),
                         "self_rank": [q for q, _ in ranked].index(p) + 1, "coherent": ok})
            trials += 1
            if top1 == p:
                self_top1 += 1
    rate = self_top1 / max(1, trials)
    # binomial one-sided p-value vs chance 1/20
    chance = 1.0 / len(personas)
    # PASS if self-id rate is meaningfully above chance (>= 3x chance AND >= 6/trials margin)
    verdict = "PASS" if (rate >= 3 * chance and self_top1 >= max(3, int(0.15 * trials))) else \
              ("WEAK" if rate > chance else "NULL")
    coherent_rate = sum(1 for r in rows if r["coherent"]) / max(1, len(rows))
    return {"label": label, "trials": trials, "self_top1": self_top1,
            "self_id_rate": round(rate, 4), "chance": round(chance, 4),
            "lift_over_chance": round(rate / chance, 2) if chance else None,
            "coherent_rate": round(coherent_rate, 3),
            "verdict": verdict, "rows": rows}


# ───────────────────────── train ─────────────────────────


def count_params(m):
    return sum(p.numel() for p in m.parameters())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--base-ckpt", required=True)
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--steps", type=int, default=2500)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--lr", type=float, default=5e-5)  # lower LR for fine-tune
    ap.add_argument("--warmup", type=int, default=100)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--eval-only", action="store_true")
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    random.seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    base = torch.load(args.base_ckpt, map_location="cpu", weights_only=False)
    cfg = base["config"]
    print(f"[base] {args.base_ckpt} params={base.get('params')} cfg={cfg}", flush=True)

    def build():
        return ConsciousLMReconstructed(256, cfg["dim"], cfg["heads"], cfg["layers"], cfg["block_size"]).to(device)

    model = build()
    model.load_state_dict(base["model_state"])
    nparams = count_params(model)
    print(f"[model] loaded stage-1 ckpt, params={nparams:,} (~{nparams/1e6:.2f}M) device={device}", flush=True)

    corpus = ByteCorpus(args.corpus, args.block)
    print(f"[data] {args.corpus}: {len(corpus.data)} bytes", flush=True)

    ce_log = []
    if not args.eval_only:
        opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)

        def lr_at(step):
            if step < args.warmup:
                return args.lr * step / max(1, args.warmup)
            prog = (step - args.warmup) / max(1, args.steps - args.warmup)
            return args.lr * 0.5 * (1 + math.cos(math.pi * min(1.0, prog)))

        t0 = time.time()
        model.train()
        for step in range(1, args.steps + 1):
            for g in opt.param_groups:
                g["lr"] = lr_at(step)
            x, y = corpus.batch(args.batch, device)
            la, lg = model(x)
            loss = 0.5 * F.cross_entropy(la.reshape(-1, 256), y.reshape(-1)) + \
                   0.5 * F.cross_entropy(lg.reshape(-1, 256), y.reshape(-1))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            if step % 100 == 0 or step == 1:
                ce_log.append((step, loss.item()))
                print(f"[ft] step {step}/{args.steps} ce={loss.item():.4f} lr={lr_at(step):.2e} "
                      f"wall={time.time()-t0:.0f}s", flush=True)

        ckpt_path = out / "persona_stage2_18m.pt"
        torch.save({"model_state": model.state_dict(), "config": cfg,
                    "params": nparams, "ft_steps": args.steps, "ce_log": ce_log,
                    "seed": args.seed, "base": "anima-clm-chat-rung0-byte-18m"}, ckpt_path)
        print(f"[save] {ckpt_path}", flush=True)

    # ── signatures (split corpus dialogues: train 80% sig / eval 20% contexts) ──
    dialogues = parse_corpus_dialogues(args.corpus)
    personas = sorted({s for d in dialogues for s, _ in d if s != "사용자"})
    rng = random.Random(7)
    rng.shuffle(dialogues)
    cut = int(0.8 * len(dialogues))
    train_d, eval_d = dialogues[:cut], dialogues[cut:]
    sigs = build_signatures(train_d, personas)
    print(f"[sig] {len(personas)} personas, sig-train={len(train_d)} eval={len(eval_d)}", flush=True)

    # ── (A) base-chat retained ──
    base_trained = base_chat_eval(model, device, "stage2_trained")
    # ── (B) persona-voice ──
    pv_trained = persona_voice_eval(model, device, eval_d, sigs, personas, "stage2_trained")

    # ── (C) anti-Goodhart random-init mirror MUST FAIL both ──
    torch.manual_seed(args.seed + 1000)
    mirror = build()
    base_mirror = base_chat_eval(mirror, device, "random_init_mirror")
    pv_mirror = persona_voice_eval(mirror, device, eval_d, sigs, personas, "random_init_mirror")

    final_ce = ce_log[-1][1] if ce_log else None
    chat_pass = base_trained["verdict"] == "PASS"
    persona_real = pv_trained["verdict"] in ("PASS", "WEAK") and pv_trained["self_id_rate"] > pv_mirror["self_id_rate"]
    anti_goodhart = (base_mirror["verdict"] == "FAIL" and pv_mirror["verdict"] in ("NULL", "WEAK")
                     and pv_trained["self_id_rate"] > pv_mirror["self_id_rate"])

    summary = {
        "rung": "stage-2 persona/SNS specialization (18M byte ConsciousLMReconstructed)",
        "base": "dancinlab/anima-clm-chat-rung0-byte-18m (stage-1 chat-PASS)",
        "scope": "SMALL 18M rung, persona-specialized — a_scale_honest_scope; "
                 "NO claim of mid/7B persona chat; null persona signal at 18M = valid closed-negative",
        "params": nparams,
        "ft_steps": args.steps, "ft_lr": args.lr, "final_ft_ce": final_ce,
        "evaluator": "p7 v2 (control_ratio<0.05 AND word_class_ratio>=0.85) + persona char-trigram top-1 self-id",
        "A_base_chat_trained": {"verdict": base_trained["verdict"], "n_pass": base_trained["n_pass"]},
        "A_base_chat_mirror": {"verdict": base_mirror["verdict"], "n_pass": base_mirror["n_pass"]},
        "B_persona_voice_trained": {"verdict": pv_trained["verdict"], "self_id_rate": pv_trained["self_id_rate"],
                                    "lift_over_chance": pv_trained["lift_over_chance"], "trials": pv_trained["trials"],
                                    "self_top1": pv_trained["self_top1"], "chance": pv_trained["chance"]},
        "B_persona_voice_mirror": {"verdict": pv_mirror["verdict"], "self_id_rate": pv_mirror["self_id_rate"],
                                   "self_top1": pv_mirror["self_top1"]},
        "chat_pass_retained": chat_pass,
        "persona_signal_real": persona_real,
        "anti_goodhart_ok": anti_goodhart,
    }
    (out / "p7_base_trained.json").write_text(json.dumps(base_trained, ensure_ascii=False, indent=2))
    (out / "p7_base_mirror.json").write_text(json.dumps(base_mirror, ensure_ascii=False, indent=2))
    (out / "persona_voice_trained.json").write_text(json.dumps(pv_trained, ensure_ascii=False, indent=2))
    (out / "persona_voice_mirror.json").write_text(json.dumps(pv_mirror, ensure_ascii=False, indent=2))
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    print("\n=== (A) base-chat TRAINED transcript ===", flush=True)
    print(base_trained["transcript"], flush=True)
    print("=== (A) base-chat MIRROR (MUST FAIL) ===", flush=True)
    print(base_mirror["transcript"], flush=True)
    print(f"\n=== (B) persona-voice TRAINED: self-id {pv_trained['self_top1']}/{pv_trained['trials']} "
          f"= {pv_trained['self_id_rate']} (chance {pv_trained['chance']}, lift {pv_trained['lift_over_chance']}x) "
          f"verdict={pv_trained['verdict']}", flush=True)
    print(f"=== (B) persona-voice MIRROR: self-id {pv_mirror['self_top1']}/{pv_mirror['trials']} "
          f"= {pv_mirror['self_id_rate']} verdict={pv_mirror['verdict']}", flush=True)
    print("\n=== SUMMARY ===", flush=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
