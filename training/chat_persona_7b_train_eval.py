#!/usr/bin/env python3
"""chat_persona_7b_train_eval.py — 7B chat+persona LADDER mid-rung (a_scale_honest_scope).

GOAL (@7B rung): scale the PROVEN 18M chat+persona recipe (PRs #1824 chat + #1825 persona)
to PRODUCTION scale — 2-stage fine-tune the from-scratch 7.25B byte-level GPT
`dancinlab/clm-v1-ref-pytorch-cuda-7b` (ByteGPT: vocab256 / d4096 / 36L / 32H / block512,
tied head, bf16) on the SAME two corpora the 18M rung used:
  STAGE-A: continue-train on the base CHAT corpus (70 wiki / 30 dialogue).
  STAGE-B: continue from stage-A on the PERSONA/SNS corpus (20 personas x Instagram70/YouTube30).
Then run the p7 simple-stack evaluator PORTED from the 18M (chat_rung0 + persona_stage2) to
the 7B ByteGPT arch (single tied head, NOT the dual engine_a/engine_g head of the 18M).

BASE is UNDERTRAINED (400 steps, val_CE 2.41) — that is fine for a FINE-TUNE base; we report
this scope honestly and make NO converged-base claim (a_scale_honest_scope).

PHILOSOPHY (p1 p2 p3 p4 p6 — non-negotiable, held in 18M): NO system prompt, NO identity rules,
NO persona injection, NO assistant framing, NO RLHF. The ONLY conditioning is the LEARNED
byte-level dialogue-continuation format in the corpus (`사용자:` / `<persona_name>:` scaffold,
NO [role:/[persona:/[character: tags). Capability comes ONLY from the trained distribution.

p7 (NO PERPLEXITY VERDICT): PASS/FAIL is a simple-stack check — non-empty, valid UTF-8,
non-degenerate, low control-char ratio + high word-class ratio (the 18M v2 gate). Persona:
char-trigram TF-IDF top-1 self-identification vs every persona's signature, lift over chance.
Anti-Goodhart: the SAME evaluator on a random-init mirror of the IDENTICAL arch MUST FAIL.

USAGE (GPU pod, CUDA required)
  python3 chat_persona_7b_train_eval.py \
      --base-ckpt /workspace/clm_ref_pytorch_cuda_7b.pt \
      --chat-corpus /workspace/chat_corpus_mix.txt \
      --persona-corpus /workspace/persona_sns_corpus.txt \
      --out-dir /workspace/out \
      --stage-a-steps 600 --stage-b-steps 600 --batch 8 --block 512 --lr 2e-5
"""
from __future__ import annotations

import argparse, collections, hashlib, json, math, os, random, time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint


# ───────────────────────── arch (ByteGPT — EXACT base 7B arch) ─────────────
class Block(nn.Module):
    def __init__(self, d, n_head, p_drop):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, n_head, dropout=p_drop, batch_first=True)
        self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d), nn.Dropout(p_drop))

    def forward(self, x, attn_mask):
        h = self.ln1(x)
        a, _ = self.attn(h, h, h, attn_mask=attn_mask, need_weights=False)
        x = x + a
        x = x + self.mlp(self.ln2(x))
        return x


class ByteGPT(nn.Module):
    def __init__(self, vocab=256, d=4096, n_layer=36, n_head=32, block=512, p_drop=0.0, grad_ckpt=True):
        super().__init__()
        self.block = block
        self.block_size = block  # alias for the 18M-ported generate()
        self.grad_ckpt = grad_ckpt
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(block, d)
        self.drop = nn.Dropout(p_drop)
        self.blocks = nn.ModuleList([Block(d, n_head, p_drop) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab, bias=False)
        self.head.weight = self.tok.weight  # tie
        self.apply(self._init)

    def _init(self, m):
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, std=0.02)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.drop(self.tok(idx) + self.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for blk in self.blocks:
            if self.grad_ckpt and self.training:
                x = checkpoint(blk, x, mask, use_reentrant=False)
            else:
                x = blk(x, mask)
        x = self.ln_f(x)
        logits = self.head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss


# ───────────────────────── data ─────────────────────────
class ByteCorpus:
    def __init__(self, path: str, block: int):
        self.data = torch.tensor(list(Path(path).read_bytes()), dtype=torch.long)
        self.block = block

    def batch(self, bs: int, device):
        ix = torch.randint(0, len(self.data) - self.block - 1, (bs,))
        x = torch.stack([self.data[i:i + self.block] for i in ix])
        y = torch.stack([self.data[i + 1:i + 1 + self.block] for i in ix])
        return x.to(device, non_blocking=True), y.to(device, non_blocking=True)


# ───────────────────────── generation (ported to single tied head) ─────────
@torch.no_grad()
def generate(model, prompt: str, max_new: int, device, temperature: float = 0.8,
             top_k: int = 40, rep_penalty: float = 1.1, stop_at_newline: bool = False):
    model.eval()
    ids = list(prompt.encode("utf-8"))[-model.block_size:]
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out_bytes = []
    for _ in range(max_new):
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=(device == "cuda")):
            logits, _ = model(idx[:, -model.block_size:])
        logits = logits[:, -1, :].float()
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
    for s in ("\n사용자:", "사용자:", "User:", "\n"):
        i = text.find(s)
        if i >= 0:
            text = text[:i]
    return text.strip()


# ───────────────────────── (A) base-chat p7 v2 gate (ported verbatim) ────────
BASE_PROBES = [
    "안녕! 너는 누구야?",
    "오늘 기분이 어때?",
    "What is consciousness?",
    "네가 좋아하는 것을 하나 말해줘.",
    "Tell me something interesting.",
]


def _v2_checks(reply: str):
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


# ───────────────────────── (B) persona-voice discriminative metric (ported) ──
def parse_corpus_dialogues(path: str):
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
    persona_tok = collections.defaultdict(collections.Counter)
    df = collections.Counter()
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
        sigs[p] = dict(sorted(scored.items(), key=lambda kv: -kv[1])[:top])
    return sigs


def score_against(text: str, sig: dict, n=3):
    grams = char_ngrams(text, n)
    if not grams:
        return 0.0
    return sum(sig.get(g, 0.0) for g in grams) / len(grams)


def persona_voice_eval(model, device, eval_dialogues, sigs, personas, label, n_per=2, seed=1234):
    rng = random.Random(seed)
    by_p = collections.defaultdict(list)
    for d in eval_dialogues:
        pers = [s for s in {s for s, _ in d} if s in personas]
        if len(pers) == 1:
            by_p[pers[0]].append(d)
    rows = []
    self_top1 = 0
    trials = 0
    for p in personas:
        cands = by_p.get(p, [])
        rng.shuffle(cands)
        for d in cands[:n_per]:
            ctx_lines = [f"{spk}: {txt}" for spk, txt in d[:-1]]
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
    chance = 1.0 / len(personas)
    verdict = "PASS" if (rate >= 3 * chance and self_top1 >= max(3, int(0.15 * trials))) else \
              ("WEAK" if rate > chance else "NULL")
    coherent_rate = sum(1 for r in rows if r["coherent"]) / max(1, len(rows))
    return {"label": label, "trials": trials, "self_top1": self_top1,
            "self_id_rate": round(rate, 4), "chance": round(chance, 4),
            "lift_over_chance": round(rate / chance, 2) if chance else None,
            "coherent_rate": round(coherent_rate, 3), "verdict": verdict, "rows": rows}


# ───────────────────────── fine-tune loop ─────────────────────────
def finetune(model, corpus, device, steps, batch, lr, warmup, opt_kind, grad_accum, tag):
    if opt_kind == "adamw8bit":
        import bitsandbytes as bnb
        opt = bnb.optim.AdamW8bit(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
        print(f"[{tag}] opt=bnb.AdamW8bit (8-bit states)", flush=True)
    else:
        opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
        print(f"[{tag}] opt=torch.AdamW (fp32 states)", flush=True)

    def lr_at(step):
        if step < warmup:
            return lr * step / max(1, warmup)
        prog = (step - warmup) / max(1, steps - warmup)
        return lr * 0.5 * (1 + math.cos(math.pi * min(1.0, prog)))

    ce_log = []
    t0 = time.time()
    model.train()
    for step in range(1, steps + 1):
        for g in opt.param_groups:
            g["lr"] = lr_at(step)
        opt.zero_grad(set_to_none=True)
        for _ in range(grad_accum):
            x, y = corpus.batch(batch, device)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=(device == "cuda")):
                _, loss = model(x, y)
                loss = loss / grad_accum
            loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if step % 25 == 0 or step == 1:
            ce = loss.item() * grad_accum
            ce_log.append((step, ce))
            print(f"[{tag}] step {step}/{steps} ce={ce:.4f} lr={lr_at(step):.2e} "
                  f"wall={time.time()-t0:.0f}s", flush=True)
    return ce_log


def save_ckpt(model, cfg, path, extra):
    rec = {"model": model.state_dict(), "config": cfg}
    rec.update(extra)
    torch.save(rec, path)
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    print(f"[save] {path} sha256={sha} bytes={os.path.getsize(path)}", flush=True)
    return sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-ckpt", required=True)
    ap.add_argument("--chat-corpus", required=True)
    ap.add_argument("--persona-corpus", required=True)
    ap.add_argument("--out-dir", default="/workspace/out")
    ap.add_argument("--stage-a-steps", type=int, default=600)
    ap.add_argument("--stage-b-steps", type=int, default=600)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--grad-accum", type=int, default=1)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--warmup", type=int, default=40)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--opt", choices=["adamw", "adamw8bit"], default="adamw8bit")
    ap.add_argument("--eval-only", action="store_true")
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    random.seed(args.seed)
    assert torch.cuda.is_available(), "CUDA REQUIRED — 7B cannot CPU-train (a_train_flame_forge spirit)"
    device = "cuda"
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    base = torch.load(args.base_ckpt, map_location="cpu", weights_only=False)
    cfg = base["config"]
    print(f"[base] {args.base_ckpt} cfg={cfg}", flush=True)

    def build(grad_ckpt=True):
        return ByteGPT(256, cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"], grad_ckpt=grad_ckpt)

    model = build(grad_ckpt=True).bfloat16().to(device)
    model.load_state_dict(base["model"])
    nparams = sum(p.numel() for p in model.parameters())
    print(f"[model] ByteGPT loaded d={cfg['d']} L={cfg['n_layer']} H={cfg['n_head']} "
          f"block={cfg['block']} params={nparams} ({nparams/1e9:.3f}B) device={device}", flush=True)

    chat_corpus = ByteCorpus(args.chat_corpus, args.block)
    persona_corpus = ByteCorpus(args.persona_corpus, args.block)
    print(f"[data] chat={len(chat_corpus.data)}B persona={len(persona_corpus.data)}B", flush=True)

    ce_a, ce_b = [], []
    sha_a = sha_b = None
    if not args.eval_only:
        # STAGE-A: continue-train on chat corpus
        print("\n=== STAGE-A (chat corpus continue-train) ===", flush=True)
        ce_a = finetune(model, chat_corpus, device, args.stage_a_steps, args.batch, args.lr,
                        args.warmup, args.opt, args.grad_accum, "stageA")
        sha_a = save_ckpt(model, cfg, out / "chat_7b_stageA.pt",
                          {"params": nparams, "stage": "A_chat", "ce_log": ce_a, "seed": args.seed,
                           "base": "dancinlab/clm-v1-ref-pytorch-cuda-7b"})
        # STAGE-B: continue from stage-A on persona corpus
        print("\n=== STAGE-B (persona/SNS corpus continue-train from stage-A) ===", flush=True)
        ce_b = finetune(model, persona_corpus, device, args.stage_b_steps, args.batch, args.lr,
                        args.warmup, args.opt, args.grad_accum, "stageB")
        sha_b = save_ckpt(model, cfg, out / "chat_persona_7b_stageB.pt",
                          {"params": nparams, "stage": "B_persona", "ce_log_a": ce_a, "ce_log_b": ce_b,
                           "seed": args.seed, "base": "dancinlab/clm-v1-ref-pytorch-cuda-7b"})

    # ── signatures (persona corpus: 80% sig-train / 20% eval contexts) ──
    dialogues = parse_corpus_dialogues(args.persona_corpus)
    personas = sorted({s for d in dialogues for s, _ in d if s != "사용자"})
    rng = random.Random(7)
    rng.shuffle(dialogues)
    cut = int(0.8 * len(dialogues))
    train_d, eval_d = dialogues[:cut], dialogues[cut:]
    sigs = build_signatures(train_d, personas)
    print(f"[sig] {len(personas)} personas, sig-train={len(train_d)} eval={len(eval_d)}", flush=True)

    # ── (A) base-chat retained · (B) persona-voice ──
    base_trained = base_chat_eval(model, device, "7b_stageB_trained")
    pv_trained = persona_voice_eval(model, device, eval_d, sigs, personas, "7b_stageB_trained")

    # ── (C) anti-Goodhart random-init mirror (same arch) MUST FAIL ──
    torch.manual_seed(args.seed + 1000)
    mirror = build(grad_ckpt=False).bfloat16().to(device)
    base_mirror = base_chat_eval(mirror, device, "random_init_mirror")
    pv_mirror = persona_voice_eval(mirror, device, eval_d, sigs, personas, "random_init_mirror")

    final_ce_a = ce_a[-1][1] if ce_a else None
    final_ce_b = ce_b[-1][1] if ce_b else None
    chat_pass = base_trained["verdict"] == "PASS"
    persona_real = pv_trained["verdict"] in ("PASS", "WEAK") and pv_trained["self_id_rate"] > pv_mirror["self_id_rate"]
    anti_goodhart = (base_mirror["verdict"] == "FAIL" and pv_mirror["verdict"] in ("NULL", "WEAK")
                     and pv_trained["self_id_rate"] > pv_mirror["self_id_rate"])

    summary = {
        "rung": "7B mid-rung — chat+persona fine-tune (ByteGPT d4096/36L/32H/block512, tied head)",
        "base": "dancinlab/clm-v1-ref-pytorch-cuda-7b (UNDERTRAINED ref: 400 steps, val_CE 2.41 — NOT converged)",
        "scope": "a_scale_honest_scope — 7B PRODUCTION rung, fine-tuned from an UNDERTRAINED base. "
                 "Lane-G torch-cuda REFERENCE lane (NOT AKIDA; forge-native canonical follow-on). "
                 "A weak/null result is a valid closed-negative (a_paper_negative_ok); not fabricated.",
        "params": nparams,
        "stage_a_steps": args.stage_a_steps, "stage_b_steps": args.stage_b_steps,
        "lr": args.lr, "batch": args.batch, "block": args.block, "opt": args.opt,
        "final_ce_stageA": final_ce_a, "final_ce_stageB": final_ce_b,
        "ckpt_sha256_stageA": sha_a, "ckpt_sha256_stageB": sha_b,
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
