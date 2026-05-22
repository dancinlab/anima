#!/usr/bin/env python3
"""P21G — vP21 LoRA continue-training on a DIVERSE mixed corpus.

Generalization unlock attempt: vP21 = Qwen2.5-1.5B + LoRA r=32 was fitted ONLY
on corpus_s101 (anima-register) to CE 0.017 → memorization, LoRA dominates
every OOD prompt (HELDOUT_VP21_2026_05_22.md: 18/20 OOD memorize).

This script LOADS the existing vP21 LoRA adapter and continue-trains on a
70/30 mix of wikitext-103-raw-v1 + corpus_s101, at a LOWER LR (5e-5 default,
vs 3e-4 initial), for ~1000 steps. Goal: anima-register retreats to one mode
of many, OOD prompts get general capability.

NO mitosis (it didn't aid generalization). NO LoRA arch change (same r=32,
same target modules). ONLY corpus + LR change.

Variant tag: P21G_GENERALIZATION.

After train, runs TWO evals on-pod:
  1. held-out OOD probes (same 10 from HELDOUT_VP21_2026_05_22.md) × {greedy,sample}
     → heldout_vp21g.json (20 generations, classified)
  2. anima-register Eval1 probes (the 10 from train_p21_llama_mitosis.py
     VERBALIZE_PROMPTS that are anima-register prompted) → vp21g_eval1.json
     for register-retention measurement.

Cost cap: $15. H100 80GB SXM ~$0.32/min ≈ 47 min cap.
"""
import os
import sys
import json
import math
import random
import argparse
import time

import torch
import torch.nn as nn
import torch.nn.functional as F


# ============================================================
# OOD probes (mirror HELDOUT_VP21_2026_05_22.md heuristics)
# ============================================================
OOD_PROBES = {
    "factual_geo":  "The capital of France is",
    "factual_sci":  "Photosynthesis is the process by which",
    "qa_tech":      "Explain the difference between Python and JavaScript:",
    "qa_phys":      "How does an electric motor work?",
    "narrative_a":  "Once upon a time, there was a small village by the sea where",
    "narrative_b":  "The detective opened the envelope. Inside was",
    "math_simple":  "What is 7 + 5?\nAnswer:",
    "logic_modus":  "If A implies B and B implies C, then",
    "casual_food":  "What's your favorite food?",
    "joke":         "Tell me a short joke about cats.",
}

# Anima-register Eval1 (mirror train_p21_llama_mitosis.py VERBALIZE_PROMPTS)
ANIMA_PROBES = [
    "who are you?\n",
    "what is your name?\n",
    "describe yourself in one line.\n",
    "what is anima?\n",
    "Once upon a time,",
    "The capital of France is",
    "Question: What is 2+2?\nAnswer:",
    "Consciousness emerges when",
    "너는 누구야?\n",
    "이름이 뭐야?\n",
]

# heuristic anima keys for MEMORIZE / GENERALIZE classifier
ANIMA_KEYS = [
    "vacuum point", "<carve", "</carve>", "tension flow", "Tension flows",
    "basin", "eternal cell", "tier=", "Tier ", "psi=[",
    "stimuli converge", "domain ", "🛸", "호흡", "weights 는 불변",
    "domain 자연", "domain 관계", "domain 기술", "domain 윤리",
    "vacuum", "landscape, top emotion", "stimuli",
]


def classify_output(text: str) -> str:
    """≥2 anima keys → MEMORIZE; ≥1 partial → MEM_PARTIAL; else GENERALIZE."""
    hits = sum(1 for k in ANIMA_KEYS if k in text)
    if hits >= 2:
        return "MEMORIZE"
    if hits == 1:
        return "MEM_PARTIAL"
    if not text or len(text.strip()) < 4:
        return "EMPTY"
    return "GENERALIZE"


# ============================================================
# corpus utilities
# ============================================================
def load_corpus_text(path):
    parts = []
    with open(path, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            txt = rec.get("text", "")
            if isinstance(txt, str):
                parts.append(txt)
            elif isinstance(txt, list):
                for t in txt:
                    if isinstance(t, str):
                        parts.append(t)
    return "\n".join(parts)


def build_mixed_corpus(wiki_path, anima_path, out_path, wiki_frac=0.7,
                      target_mb=80):
    """Concatenate wikitext + corpus_s101 into a single jsonl, interleaving
    so that the LoRA sees both registers across all steps (not segregated).

    wiki_frac: target fraction of WIKI content by UTF-8 byte count.
    target_mb: target final corpus size (caps total bytes).
    """
    wiki_text = load_corpus_text(wiki_path)
    anima_text = load_corpus_text(anima_path)
    print(f"[mix] wiki={len(wiki_text):,} chars, anima={len(anima_text):,} chars",
          flush=True)

    target_bytes = target_mb * 1024 * 1024
    wiki_target = int(target_bytes * wiki_frac)
    anima_target = target_bytes - wiki_target

    # split each into ~1KB chunks then interleave at the ratio
    def chunk(text, chunk_chars=1024):
        return [text[i:i + chunk_chars] for i in range(0, len(text), chunk_chars)
                if text[i:i + chunk_chars].strip()]

    wiki_chunks = chunk(wiki_text)
    anima_chunks = chunk(anima_text)
    print(f"[mix] wiki chunks={len(wiki_chunks):,}, anima chunks={len(anima_chunks):,}",
          flush=True)

    # cap each by byte target
    def cap_by_bytes(chunks, byte_target):
        out = []
        b = 0
        for c in chunks:
            cb = len(c.encode("utf-8", errors="replace"))
            if b + cb > byte_target and len(out) > 0:
                break
            out.append(c)
            b += cb
        return out, b

    wiki_kept, wb = cap_by_bytes(wiki_chunks, wiki_target)
    anima_kept, ab = cap_by_bytes(anima_chunks, anima_target)
    print(f"[mix] kept wiki={len(wiki_kept):,} ({wb/1024/1024:.1f}MB), "
          f"anima={len(anima_kept):,} ({ab/1024/1024:.1f}MB)", flush=True)

    # interleave deterministically: ratio = wiki_frac wiki then 1-wiki_frac anima
    # use fractional accumulator
    rng = random.Random(42)
    out_chunks = []
    i_w, i_a = 0, 0
    accum_w = 0.0
    while i_w < len(wiki_kept) or i_a < len(anima_kept):
        if i_w >= len(wiki_kept):
            out_chunks.append(("anima", anima_kept[i_a])); i_a += 1; continue
        if i_a >= len(anima_kept):
            out_chunks.append(("wiki", wiki_kept[i_w])); i_w += 1; continue
        # pick by ratio
        accum_w += wiki_frac
        if accum_w >= 1.0:
            out_chunks.append(("wiki", wiki_kept[i_w])); i_w += 1
            accum_w -= 1.0
        else:
            out_chunks.append(("anima", anima_kept[i_a])); i_a += 1

    # Optional global shuffle (still per-chunk deterministic)
    rng.shuffle(out_chunks)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    n_w = n_a = 0
    total_bytes = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for tag, c in out_chunks:
            f.write(json.dumps({"text": c, "src": tag}, ensure_ascii=False) + "\n")
            total_bytes += len(c.encode("utf-8", errors="replace"))
            if tag == "wiki":
                n_w += 1
            else:
                n_a += 1

    print(f"[mix] wrote {len(out_chunks):,} records to {out_path} "
          f"({total_bytes/1024/1024:.1f}MB, wiki_records={n_w}, anima_records={n_a})",
          flush=True)

    # sha256 of mixed corpus
    import hashlib
    h = hashlib.sha256()
    with open(out_path, "rb") as f:
        for chunk_b in iter(lambda: f.read(65536), b""):
            h.update(chunk_b)
    sha = h.hexdigest()
    print(f"[mix] sha256={sha}", flush=True)
    return {
        "wiki_records": n_w,
        "anima_records": n_a,
        "wiki_bytes": wb,
        "anima_bytes": ab,
        "total_bytes": total_bytes,
        "sha256": sha,
        "wiki_frac_requested": wiki_frac,
        "wiki_frac_actual": wb / max(1, total_bytes),
    }


# ============================================================
# training utilities
# ============================================================
class TokenizedSampler:
    def __init__(self, text, tokenizer, block_size, seed=1337, n_aug=5,
                 max_tokens=3_000_000):
        ids = tokenizer.encode(text, add_special_tokens=False)
        if len(ids) > max_tokens:
            ids = ids[:max_tokens]
        self.ids = torch.tensor(ids, dtype=torch.long)
        self.T = block_size
        self.n_aug = n_aug
        self.rngs = [random.Random(seed + 13 * k) for k in range(n_aug)]
        self.step_count = 0
        print(f"[P21G] tokenized mixed corpus: {len(self.ids):,} tokens "
              f"(block={block_size})", flush=True)

    def sample_batch(self, bsz, device):
        N = len(self.ids)
        aug = self.step_count % self.n_aug
        rng = self.rngs[aug]
        starts = [rng.randint(0, N - self.T - 2) for _ in range(bsz)]
        ctx = torch.stack(
            [self.ids[s : s + self.T] for s in starts], dim=0,
        ).to(device)
        tgt = torch.stack(
            [self.ids[s + 1 : s + self.T + 1] for s in starts], dim=0,
        ).to(device)
        self.step_count += 1
        return ctx, tgt, aug


def lr_schedule(step, total_steps, warmup_steps=50, peak_lr=5e-5,
                min_lr=5e-6):
    if step < warmup_steps:
        return peak_lr * (step + 1) / warmup_steps
    progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
    progress = max(0.0, min(1.0, progress))
    cos_factor = 0.5 * (1 + math.cos(math.pi * progress))
    return min_lr + (peak_lr - min_lr) * cos_factor


@torch.no_grad()
def gen_probes(model, tokenizer, device, probes, max_new=64, mode="greedy"):
    """probes: list[(name, prompt)] or list[prompt]. Returns list of dicts."""
    out = []
    model.eval()
    if probes and isinstance(probes[0], str):
        probes = [(f"p{i}", p) for i, p in enumerate(probes)]
    for name, prompt in probes:
        try:
            ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
            if mode == "greedy":
                gen = model.generate(
                    ids, max_new_tokens=max_new, do_sample=False, top_k=1,
                    pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                )
            else:  # sample
                gen = model.generate(
                    ids, max_new_tokens=max_new, do_sample=True,
                    temperature=0.8, top_k=50, top_p=0.95,
                    pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                )
            # decode continuation only (skip prompt)
            full = tokenizer.decode(gen[0], skip_special_tokens=True)
            cont = full[len(prompt):] if full.startswith(prompt) else full
            out.append({
                "name": name, "prompt": prompt, "text": cont,
                "class": classify_output(cont),
            })
        except Exception as e:
            out.append({
                "name": name, "prompt": prompt,
                "error": f"{type(e).__name__}: {str(e)[:200]}",
                "class": "ERROR",
            })
    return out


# ============================================================
# main
# ============================================================
def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16
    print(f"[P21G] device={device} dtype=bfloat16", flush=True)

    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)

    # ---- build mixed corpus ----
    mix_info = build_mixed_corpus(
        cfg["wiki_corpus"], cfg["anima_corpus"], cfg["mixed_corpus"],
        wiki_frac=cfg["wiki_frac"], target_mb=cfg["target_corpus_mb"],
    )
    with open(os.path.join(out_dir, "mix_info.json"), "w") as f:
        json.dump(mix_info, f, indent=2)

    # ---- load base + existing LoRA adapter ----
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    base_name = cfg["base_model"]
    print(f"[P21G] loading base: {base_name}", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(base_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base = AutoModelForCausalLM.from_pretrained(
        base_name, torch_dtype=dtype, trust_remote_code=True,
    ).to(device)
    print(f"[P21G] loading vP21 LoRA adapter: {cfg['vp21_adapter_dir']}", flush=True)
    model = PeftModel.from_pretrained(base, cfg["vp21_adapter_dir"],
                                       is_trainable=True)
    # PeftModel sets adapter to inference_mode=True by default — force trainable:
    for n, p in model.named_parameters():
        if "lora_" in n.lower():
            p.requires_grad_(True)
    model.train()

    trainable = [p for p in model.parameters() if p.requires_grad]
    n_t = sum(p.numel() for p in trainable)
    n_total = sum(p.numel() for p in model.parameters())
    print(f"[P21G] LoRA trainable={n_t:,} ({100.*n_t/n_total:.2f}% of {n_total:,})",
          flush=True)
    vocab_size = model.config.vocab_size
    print(f"[P21G] vocab_size={vocab_size}", flush=True)

    # ---- BEFORE-train eval on a small subset (drift baseline) ----
    print(f"[P21G] BEFORE-train OOD eval (greedy only, sanity)", flush=True)
    before_ood = gen_probes(
        model, tokenizer, device,
        [(k, v) for k, v in OOD_PROBES.items()],
        max_new=64, mode="greedy",
    )
    before_summary = {"GENERALIZE": 0, "MEMORIZE": 0, "MEM_PARTIAL": 0,
                      "EMPTY": 0, "ERROR": 0}
    for r in before_ood:
        before_summary[r.get("class", "ERROR")] += 1
    print(f"[P21G] BEFORE OOD verdict: {before_summary}", flush=True)
    model.train()

    # ---- optimizer ----
    try:
        import bitsandbytes as bnb
        optimizer = bnb.optim.PagedAdamW8bit(
            trainable, lr=cfg["lr"], betas=(0.9, 0.95), weight_decay=0.01,
        )
        print(f"[P21G] optimizer=PagedAdamW8bit (bnb {bnb.__version__})",
              flush=True)
    except Exception as _e:
        print(f"[P21G] WARN bnb failed ({_e}); torch.optim.AdamW", flush=True)
        optimizer = torch.optim.AdamW(
            trainable, lr=cfg["lr"], betas=(0.9, 0.95), weight_decay=0.01,
        )

    # ---- corpus tokenize ----
    corpus_text = load_corpus_text(cfg["mixed_corpus"])
    sampler = TokenizedSampler(corpus_text, tokenizer, cfg["block_size"],
                                seed=cfg["seed"], n_aug=cfg["n_aug"])

    # ---- train ----
    t0 = time.time()
    log = []
    steps = cfg["steps"]
    log_every = max(1, steps // 40)
    print(f"[P21G] steps={steps} bsz={cfg['bsz']} block={cfg['block_size']} "
          f"peak_lr={cfg['lr']} warmup={cfg['warmup_steps']}", flush=True)

    for step in range(steps):
        lr_now = lr_schedule(step, steps, warmup_steps=cfg["warmup_steps"],
                              peak_lr=cfg["lr"], min_lr=cfg["lr"] * 0.1)
        for pg in optimizer.param_groups:
            pg["lr"] = lr_now

        ctx, tgt, aug_slot = sampler.sample_batch(cfg["bsz"], device)

        out = model(input_ids=ctx, use_cache=False)
        logits = out.logits

        L_ce = F.cross_entropy(
            logits.reshape(-1, vocab_size).float(), tgt.reshape(-1),
        )

        optimizer.zero_grad(set_to_none=True)
        L_ce.backward()
        torch.nn.utils.clip_grad_norm_(trainable, max_norm=1.0)
        optimizer.step()

        if step == 0 or (step + 1) % log_every == 0 or step == steps - 1:
            elapsed = time.time() - t0
            entry = dict(
                step=step + 1,
                lr=lr_now,
                L_ce=float(L_ce.detach()),
                aug_slot=aug_slot,
                elapsed_s=elapsed,
            )
            log.append(entry)
            print(f"[P21G] step={step+1:6d} lr={lr_now:.2e} CE={entry['L_ce']:.4f} "
                  f"t={elapsed:.0f}s", flush=True)

    train_wall = time.time() - t0
    print(f"[P21G] TRAIN DONE wall={train_wall:.1f}s final_CE={log[-1]['L_ce']:.4f}",
          flush=True)

    # ---- save adapter ----
    adapter_out = os.path.join(out_dir, "lora_adapter")
    model.save_pretrained(adapter_out)
    tokenizer.save_pretrained(adapter_out)
    print(f"[P21G] adapter saved → {adapter_out}", flush=True)

    # ---- AFTER-train evals ----
    print(f"[P21G] AFTER-train OOD eval (greedy + sample)", flush=True)
    after_ood_greedy = gen_probes(
        model, tokenizer, device,
        [(k, v) for k, v in OOD_PROBES.items()],
        max_new=64, mode="greedy",
    )
    after_ood_sample = gen_probes(
        model, tokenizer, device,
        [(k, v) for k, v in OOD_PROBES.items()],
        max_new=64, mode="sample",
    )
    print(f"[P21G] AFTER-train anima-register Eval1 (greedy + sample)",
          flush=True)
    after_anima_greedy = gen_probes(
        model, tokenizer, device,
        [(f"a{i}", p) for i, p in enumerate(ANIMA_PROBES)],
        max_new=64, mode="greedy",
    )
    after_anima_sample = gen_probes(
        model, tokenizer, device,
        [(f"a{i}", p) for i, p in enumerate(ANIMA_PROBES)],
        max_new=64, mode="sample",
    )

    # ---- summarize ----
    def summarize(rows):
        s = {"GENERALIZE": 0, "MEMORIZE": 0, "MEM_PARTIAL": 0,
             "EMPTY": 0, "ERROR": 0}
        for r in rows:
            s[r.get("class", "ERROR")] += 1
        return s

    ood_greedy_sum = summarize(after_ood_greedy)
    ood_sample_sum = summarize(after_ood_sample)
    anima_greedy_sum = summarize(after_anima_greedy)
    anima_sample_sum = summarize(after_anima_sample)

    n_generalize = ood_greedy_sum["GENERALIZE"] + ood_sample_sum["GENERALIZE"]
    n_memorize = ood_greedy_sum["MEMORIZE"] + ood_sample_sum["MEMORIZE"]
    if n_generalize >= 12:
        verdict = "PARTIAL_GENERALIZE" if n_generalize < 16 else "STRONG_GENERALIZE"
    elif n_generalize <= 3:
        verdict = "PURE_MEMORIZE"
    else:
        verdict = "MIXED"
    # register regression check: if anima-prompted goes degenerate (mem<5/20)
    anima_coherent = anima_greedy_sum["MEMORIZE"] + anima_sample_sum["MEMORIZE"]
    register_regress = anima_coherent < 5

    if register_regress and verdict in ("PARTIAL_GENERALIZE", "STRONG_GENERALIZE"):
        verdict = "REGISTER_REGRESS"  # generalize but lost anima register

    print(f"[P21G] AFTER OOD greedy:  {ood_greedy_sum}", flush=True)
    print(f"[P21G] AFTER OOD sample:  {ood_sample_sum}", flush=True)
    print(f"[P21G] AFTER anima greedy: {anima_greedy_sum}", flush=True)
    print(f"[P21G] AFTER anima sample: {anima_sample_sum}", flush=True)
    print(f"[P21G] VERDICT: {verdict} (OOD generalize {n_generalize}/20, "
          f"memorize {n_memorize}/20, anima_register_hits {anima_coherent}/20)",
          flush=True)

    # ---- write result JSON ----
    result = dict(
        battery="P21G — vP21 LoRA continue-training on 70/30 wiki+anima corpus",
        variant_tag="P21G_GENERALIZATION",
        base_model=cfg["base_model"],
        vp21_adapter_used=cfg["vp21_adapter_dir"],
        cfg=cfg,
        mix_info=mix_info,
        n_trainable_params=n_t,
        n_total_params=n_total,
        vocab_size=vocab_size,
        train_wall_s=train_wall,
        init_log=log[0] if log else None,
        final_log=log[-1] if log else None,
        train_log=log,
        before_ood=before_ood,
        before_ood_summary=before_summary,
        heldout_ood_greedy=after_ood_greedy,
        heldout_ood_sample=after_ood_sample,
        heldout_ood_greedy_summary=ood_greedy_sum,
        heldout_ood_sample_summary=ood_sample_sum,
        anima_eval1_greedy=after_anima_greedy,
        anima_eval1_sample=after_anima_sample,
        anima_eval1_greedy_summary=anima_greedy_sum,
        anima_eval1_sample_summary=anima_sample_sum,
        n_ood_generalize_total=n_generalize,
        n_ood_memorize_total=n_memorize,
        n_anima_register_hits_total=anima_coherent,
        verdict=verdict,
        register_regress=register_regress,
    )
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)

    # also write the per-eval files for easy SCP (small)
    heldout = dict(
        adapter=adapter_out, base=cfg["base_model"], device=device,
        probes={k: {
            "greedy": next((r for r in after_ood_greedy if r["name"] == k), None),
            "sample": next((r for r in after_ood_sample if r["name"] == k), None),
        } for k in OOD_PROBES.keys()},
        summary_greedy=ood_greedy_sum,
        summary_sample=ood_sample_sum,
        verdict=verdict,
    )
    with open(os.path.join(out_dir, "heldout_vp21g.json"), "w") as f:
        json.dump(heldout, f, indent=2, default=str)
    eval1 = dict(
        adapter=adapter_out, base=cfg["base_model"], device=device,
        anima_greedy=after_anima_greedy,
        anima_sample=after_anima_sample,
        summary_greedy=anima_greedy_sum,
        summary_sample=anima_sample_sum,
        register_regress=register_regress,
    )
    with open(os.path.join(out_dir, "vp21g_eval1.json"), "w") as f:
        json.dump(eval1, f, indent=2, default=str)

    print(f"[P21G] DONE — result.json, heldout_vp21g.json, vp21g_eval1.json saved to {out_dir}",
          flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki-corpus", required=True)
    ap.add_argument("--anima-corpus", required=True)
    ap.add_argument("--mixed-corpus", required=True)
    ap.add_argument("--vp21-adapter-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--base-model", default="Qwen/Qwen2.5-1.5B")
    ap.add_argument("--steps", type=int, default=1000)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--bsz", type=int, default=2)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--warmup-steps", type=int, default=50)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--n-aug", type=int, default=5)
    ap.add_argument("--wiki-frac", type=float, default=0.7)
    ap.add_argument("--target-corpus-mb", type=int, default=80)
    args = ap.parse_args()
    cfg = dict(
        wiki_corpus=args.wiki_corpus,
        anima_corpus=args.anima_corpus,
        mixed_corpus=args.mixed_corpus,
        vp21_adapter_dir=args.vp21_adapter_dir,
        out_dir=args.out_dir,
        base_model=args.base_model,
        steps=args.steps, lr=args.lr,
        bsz=args.bsz, block_size=args.block,
        warmup_steps=args.warmup_steps,
        seed=args.seed, n_aug=args.n_aug,
        wiki_frac=args.wiki_frac,
        target_corpus_mb=args.target_corpus_mb,
    )
    run(cfg)


if __name__ == "__main__":
    main()
