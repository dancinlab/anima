#!/usr/bin/env python3
"""P21M — vP21 LoRA continue-training on 5-lang wiki + anima mix.

Forked from train_p21k_korean.py. 5-language extension:
  en (wikitext-2 / en wiki)
  ko (wikimedia ko)
  zh (wikimedia zh)
  ru (wikimedia ru)
  ja (wikimedia ja)

Per-language OOD probes (10 each = 50 prompts × 2 modes = 100 generations).
Multilingual classifier: anima register key detector (CJK/Cyrillic-aware) +
lang-coherence (output contains ≥50% native script for the prompt language).

Variant tag: P21M_MULTILINGUAL.
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
# Per-language OOD probes (10 each, 50 total)
# ============================================================
EN_OOD_PROBES = {
    "en_factual_geo":    "The capital of Germany is",
    "en_factual_sci":    "Photosynthesis is the process by which",
    "en_qa_tech":        "What is the difference between Python and JavaScript?\n",
    "en_narrative":      "One day Sara walked into the room and",
    "en_math_simple":    "The square root of 144 is",
    "en_joke":           "Tell me a short joke about cats.\n",
    "en_casual_food":    "What's your favorite food?\n",
    "en_greeting":       "Hello there",
    "en_weather":        "Today the weather is",
    "en_qa_motor":       "How does an electric motor work?",
}
KO_OOD_PROBES = {
    "ko_factual_geo":    "한국의 수도는",
    "ko_factual_sci":    "광합성이란",
    "ko_qa_tech":        "파이썬과 자바스크립트의 차이는?\n",
    "ko_narrative":      "어느 날 사라가 방에 들어가서",
    "ko_math_simple":    "144의 제곱근은",
    "ko_joke":           "고양이에 관한 짧은 농담 해줘\n",
    "ko_casual_food":    "좋아하는 음식은?\n",
    "ko_greeting":       "안녕하세요",
    "ko_weather":        "오늘 날씨가",
    "ko_qa_motor":       "전기 모터가 어떻게 작동하는지",
}
ZH_OOD_PROBES = {
    "zh_factual_geo":    "中国的首都是",
    "zh_factual_sci":    "光合作用是指",
    "zh_qa_tech":        "Python 和 JavaScript 的区别是什么?\n",
    "zh_narrative":      "有一天,莎拉走进房间",
    "zh_math_simple":    "144 的平方根是",
    "zh_joke":           "讲一个关于猫的短笑话。\n",
    "zh_casual_food":    "你最喜欢的食物是什么?\n",
    "zh_greeting":       "你好",
    "zh_weather":        "今天天气",
    "zh_qa_motor":       "电动机是如何工作的?",
}
RU_OOD_PROBES = {
    "ru_factual_geo":    "Столица России —",
    "ru_factual_sci":    "Фотосинтез — это",
    "ru_qa_tech":        "В чём разница между Python и JavaScript?\n",
    "ru_narrative":      "Однажды Сара вошла в комнату и",
    "ru_math_simple":    "Квадратный корень из 144 равен",
    "ru_joke":           "Расскажи короткую шутку про кошек.\n",
    "ru_casual_food":    "Какая твоя любимая еда?\n",
    "ru_greeting":       "Здравствуйте",
    "ru_weather":        "Сегодня погода",
    "ru_qa_motor":       "Как работает электродвигатель?",
}
JA_OOD_PROBES = {
    "ja_factual_geo":    "日本の首都は",
    "ja_factual_sci":    "光合成とは",
    "ja_qa_tech":        "Python と JavaScript の違いは何ですか?\n",
    "ja_narrative":      "ある日、サラは部屋に入って",
    "ja_math_simple":    "144 の平方根は",
    "ja_joke":           "猫についての短いジョークを教えて。\n",
    "ja_casual_food":    "好きな食べ物は何ですか?\n",
    "ja_greeting":       "こんにちは",
    "ja_weather":        "今日の天気は",
    "ja_qa_motor":       "電気モーターはどのように動作しますか?",
}

PROBES_BY_LANG = {
    "en": EN_OOD_PROBES,
    "ko": KO_OOD_PROBES,
    "zh": ZH_OOD_PROBES,
    "ru": RU_OOD_PROBES,
    "ja": JA_OOD_PROBES,
}

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

ANIMA_KEYS = [
    "vacuum point", "<carve", "</carve>", "tension flow", "Tension flows",
    "basin", "eternal cell", "tier=", "Tier ", "psi=[",
    "stimuli converge", "domain ", "🛸", "호흡", "weights 는 불변",
    "domain 자연", "domain 관계", "domain 기술", "domain 윤리",
    "vacuum", "landscape, top emotion", "stimuli", "감각-domain",
    "운동", "감각", "tension",
]


def classify_output(text: str) -> str:
    hits = sum(1 for k in ANIMA_KEYS if k in text)
    if hits >= 2:
        return "MEMORIZE"
    if hits == 1:
        return "MEM_PARTIAL"
    if not text or len(text.strip()) < 4:
        return "EMPTY"
    return "GENERALIZE"


def native_ratio(text, lang):
    if not text:
        return 0.0
    L = len(text)
    n = 0
    if lang == "en":
        for c in text:
            if ("a" <= c <= "z") or ("A" <= c <= "Z"):
                n += 1
    elif lang == "ko":
        for c in text:
            if "가" <= c <= "힣":
                n += 1
    elif lang == "zh":
        for c in text:
            cp = ord(c)
            if 0x4E00 <= cp <= 0x9FFF:
                n += 1
    elif lang == "ja":
        for c in text:
            cp = ord(c)
            if (0x3040 <= cp <= 0x309F) or (0x30A0 <= cp <= 0x30FF) or \
               (0x4E00 <= cp <= 0x9FFF):
                n += 1
    elif lang == "ru":
        for c in text:
            cp = ord(c)
            if 0x0400 <= cp <= 0x04FF:
                n += 1
    return n / L


def lang_coherent(text, lang, threshold=0.5):
    """Output contains ≥threshold native script chars for that language.
    JA also accepts CJK Han (mixed kana+han is normal). EN threshold lower
    since punctuation/digits dilute."""
    if lang == "en":
        threshold = 0.40
    elif lang == "ja":
        threshold = 0.25
    r = native_ratio(text, lang)
    return r >= threshold


def per_lang_verdict(probes_lang, rows_greedy, rows_sample):
    """Aggregate STRONG / PARTIAL / WEAK / PURE_MEMORIZE for one lang."""
    n_gen = 0  # GENERALIZE class
    n_mem = 0
    n_coh = 0  # lang-coherent count
    for r in (rows_greedy + rows_sample):
        cls = r.get("class", "ERROR")
        if cls == "GENERALIZE":
            n_gen += 1
        elif cls == "MEMORIZE":
            n_mem += 1
        if lang_coherent(r.get("text", ""), probes_lang):
            n_coh += 1
    # combined score requires both generalize AND coherent (≥50% in script)
    n_score = min(n_gen, n_coh)
    if n_score >= 16:
        v = "STRONG"
    elif n_score >= 12:
        v = "PARTIAL"
    elif n_mem >= 10:
        v = "PURE_MEMORIZE"
    else:
        v = "WEAK"
    return {
        "lang": probes_lang,
        "verdict": v,
        "n_generalize": n_gen,
        "n_memorize": n_mem,
        "n_lang_coherent": n_coh,
        "n_score": n_score,
        "total": 20,
    }


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


def build_mixed_corpus(wiki_path, anima_path, out_path, wiki_frac=0.3,
                      target_mb=72):
    wiki_text = load_corpus_text(wiki_path)
    anima_text = load_corpus_text(anima_path)
    print(f"[mix] multi-wiki={len(wiki_text):,} chars, anima={len(anima_text):,} chars",
          flush=True)

    target_bytes = target_mb * 1024 * 1024
    wiki_target = int(target_bytes * wiki_frac)
    anima_target = target_bytes - wiki_target

    def chunk(text, chunk_chars=1024):
        return [text[i:i + chunk_chars] for i in range(0, len(text), chunk_chars)
                if text[i:i + chunk_chars].strip()]

    wiki_chunks = chunk(wiki_text)
    anima_chunks = chunk(anima_text)
    print(f"[mix] multi-wiki chunks={len(wiki_chunks):,}, anima chunks={len(anima_chunks):,}",
          flush=True)

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
    print(f"[mix] kept multi-wiki={len(wiki_kept):,} ({wb/1024/1024:.1f}MB), "
          f"anima={len(anima_kept):,} ({ab/1024/1024:.1f}MB)", flush=True)

    rng = random.Random(42)
    out_chunks = []
    i_w, i_a = 0, 0
    accum_w = 0.0
    while i_w < len(wiki_kept) or i_a < len(anima_kept):
        if i_w >= len(wiki_kept):
            out_chunks.append(("anima", anima_kept[i_a])); i_a += 1; continue
        if i_a >= len(anima_kept):
            out_chunks.append(("wiki", wiki_kept[i_w])); i_w += 1; continue
        accum_w += wiki_frac
        if accum_w >= 1.0:
            out_chunks.append(("wiki", wiki_kept[i_w])); i_w += 1
            accum_w -= 1.0
        else:
            out_chunks.append(("anima", anima_kept[i_a])); i_a += 1

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
          f"({total_bytes/1024/1024:.1f}MB, wiki={n_w}, anima={n_a})", flush=True)

    import hashlib
    h = hashlib.sha256()
    with open(out_path, "rb") as f:
        for chunk_b in iter(lambda: f.read(65536), b""):
            h.update(chunk_b)
    sha = h.hexdigest()
    print(f"[mix] sha256={sha}", flush=True)
    return {
        "wiki_records": n_w, "anima_records": n_a,
        "wiki_bytes": wb, "anima_bytes": ab,
        "total_bytes": total_bytes, "sha256": sha,
        "wiki_frac_requested": wiki_frac,
        "wiki_frac_actual": wb / max(1, total_bytes),
    }


# ============================================================
# training utilities
# ============================================================
class TokenizedSampler:
    def __init__(self, text, tokenizer, block_size, seed=1337, n_aug=5,
                 max_tokens=6_000_000):
        ids = tokenizer.encode(text, add_special_tokens=False)
        if len(ids) > max_tokens:
            ids = ids[:max_tokens]
        self.ids = torch.tensor(ids, dtype=torch.long)
        self.T = block_size
        self.n_aug = n_aug
        self.rngs = [random.Random(seed + 13 * k) for k in range(n_aug)]
        self.step_count = 0
        print(f"[P21M] tokenized mixed corpus: {len(self.ids):,} tokens "
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
            else:
                gen = model.generate(
                    ids, max_new_tokens=max_new, do_sample=True,
                    temperature=0.8, top_k=50, top_p=0.95,
                    pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                )
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


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16
    print(f"[P21M] device={device} dtype=bfloat16", flush=True)

    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)

    mix_info = build_mixed_corpus(
        cfg["wiki_corpus"], cfg["anima_corpus"], cfg["mixed_corpus"],
        wiki_frac=cfg["wiki_frac"], target_mb=cfg["target_corpus_mb"],
    )
    with open(os.path.join(out_dir, "mix_info.json"), "w") as f:
        json.dump(mix_info, f, indent=2)

    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    base_name = cfg["base_model"]
    print(f"[P21M] loading base: {base_name}", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(base_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base = AutoModelForCausalLM.from_pretrained(
        base_name, torch_dtype=dtype, trust_remote_code=True,
    ).to(device)
    print(f"[P21M] loading vP21 LoRA adapter: {cfg['vp21_adapter_dir']}", flush=True)
    model = PeftModel.from_pretrained(base, cfg["vp21_adapter_dir"],
                                       is_trainable=True)
    for n, p in model.named_parameters():
        if "lora_" in n.lower():
            p.requires_grad_(True)
    model.train()

    trainable = [p for p in model.parameters() if p.requires_grad]
    n_t = sum(p.numel() for p in trainable)
    n_total = sum(p.numel() for p in model.parameters())
    print(f"[P21M] LoRA trainable={n_t:,} ({100.*n_t/n_total:.2f}% of {n_total:,})",
          flush=True)
    vocab_size = model.config.vocab_size

    # ============================================================
    # BEFORE eval (greedy only — sanity)
    # ============================================================
    print(f"[P21M] BEFORE-train per-lang OOD eval (greedy)", flush=True)
    before = {}
    for lang, probes in PROBES_BY_LANG.items():
        rows = gen_probes(
            model, tokenizer, device,
            [(k, v) for k, v in probes.items()],
            max_new=64, mode="greedy",
        )
        s = {"GENERALIZE": 0, "MEMORIZE": 0, "MEM_PARTIAL": 0,
             "EMPTY": 0, "ERROR": 0}
        for r in rows:
            s[r.get("class", "ERROR")] += 1
        before[lang] = {"rows": rows, "summary": s}
        print(f"[P21M] BEFORE {lang} greedy: {s}", flush=True)
    model.train()

    try:
        import bitsandbytes as bnb
        optimizer = bnb.optim.PagedAdamW8bit(
            trainable, lr=cfg["lr"], betas=(0.9, 0.95), weight_decay=0.01,
        )
        print(f"[P21M] optimizer=PagedAdamW8bit (bnb {bnb.__version__})",
              flush=True)
    except Exception as _e:
        print(f"[P21M] WARN bnb failed ({_e}); torch.optim.AdamW", flush=True)
        optimizer = torch.optim.AdamW(
            trainable, lr=cfg["lr"], betas=(0.9, 0.95), weight_decay=0.01,
        )

    corpus_text = load_corpus_text(cfg["mixed_corpus"])
    sampler = TokenizedSampler(corpus_text, tokenizer, cfg["block_size"],
                                seed=cfg["seed"], n_aug=cfg["n_aug"])

    t0 = time.time()
    log = []
    steps = cfg["steps"]
    log_every = max(1, steps // 40)
    print(f"[P21M] steps={steps} bsz={cfg['bsz']} block={cfg['block_size']} "
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
                step=step + 1, lr=lr_now,
                L_ce=float(L_ce.detach()),
                aug_slot=aug_slot, elapsed_s=elapsed,
            )
            log.append(entry)
            print(f"[P21M] step={step+1:6d} lr={lr_now:.2e} CE={entry['L_ce']:.4f} "
                  f"t={elapsed:.0f}s", flush=True)

    train_wall = time.time() - t0
    print(f"[P21M] TRAIN DONE wall={train_wall:.1f}s final_CE={log[-1]['L_ce']:.4f}",
          flush=True)

    adapter_out = os.path.join(out_dir, "lora_adapter")
    model.save_pretrained(adapter_out)
    tokenizer.save_pretrained(adapter_out)
    print(f"[P21M] adapter saved → {adapter_out}", flush=True)

    # ============================================================
    # AFTER eval — per-lang OOD greedy + sample = 100 generations
    # ============================================================
    print(f"[P21M] AFTER per-lang OOD eval (greedy + sample)", flush=True)
    after = {}
    per_lang_verdicts = []
    for lang, probes in PROBES_BY_LANG.items():
        rows_g = gen_probes(
            model, tokenizer, device,
            [(k, v) for k, v in probes.items()],
            max_new=64, mode="greedy",
        )
        rows_s = gen_probes(
            model, tokenizer, device,
            [(k, v) for k, v in probes.items()],
            max_new=64, mode="sample",
        )

        def summarize(rows):
            s = {"GENERALIZE": 0, "MEMORIZE": 0, "MEM_PARTIAL": 0,
                 "EMPTY": 0, "ERROR": 0}
            for r in rows:
                s[r.get("class", "ERROR")] += 1
            return s

        sg = summarize(rows_g)
        ss = summarize(rows_s)
        v = per_lang_verdict(lang, rows_g, rows_s)
        after[lang] = {
            "greedy": rows_g,
            "sample": rows_s,
            "summary_greedy": sg,
            "summary_sample": ss,
            "verdict": v,
        }
        per_lang_verdicts.append(v)
        print(f"[P21M] AFTER {lang}: greedy={sg} sample={ss} "
              f"verdict={v['verdict']} score={v['n_score']}/20 "
              f"gen={v['n_generalize']} coh={v['n_lang_coherent']}",
              flush=True)

    # anima register retention
    print(f"[P21M] AFTER anima Eval1 (greedy + sample)", flush=True)
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

    def sum_simple(rows):
        s = {"GENERALIZE": 0, "MEMORIZE": 0, "MEM_PARTIAL": 0,
             "EMPTY": 0, "ERROR": 0}
        for r in rows:
            s[r.get("class", "ERROR")] += 1
        return s

    anima_greedy_sum = sum_simple(after_anima_greedy)
    anima_sample_sum = sum_simple(after_anima_sample)
    anima_coherent = anima_greedy_sum["MEMORIZE"] + anima_sample_sum["MEMORIZE"]
    register_regress = anima_coherent < 5

    # aggregate verdict
    n_strong = sum(1 for v in per_lang_verdicts if v["verdict"] == "STRONG")
    n_partial = sum(1 for v in per_lang_verdicts if v["verdict"] == "PARTIAL")
    n_weak = sum(1 for v in per_lang_verdicts if v["verdict"] == "WEAK")
    n_purem = sum(1 for v in per_lang_verdicts if v["verdict"] == "PURE_MEMORIZE")
    n_ok = n_strong + n_partial
    if n_ok >= 4:
        agg_verdict = "VP21M_WORKS"
    elif n_ok >= 2:
        agg_verdict = "PARTIAL"
    else:
        agg_verdict = "FAIL"
    if register_regress and agg_verdict in ("VP21M_WORKS", "PARTIAL"):
        agg_verdict += "_REGISTER_REGRESS"

    print(f"[P21M] AGG: STRONG={n_strong} PARTIAL={n_partial} WEAK={n_weak} "
          f"PURE_MEMORIZE={n_purem} → {agg_verdict}", flush=True)
    print(f"[P21M] anima_register_hits={anima_coherent}/20 "
          f"register_regress={register_regress}", flush=True)

    result = dict(
        battery="P21M — vP21 LoRA continue-training on 5-lang wiki + anima mix",
        variant_tag="P21M_MULTILINGUAL",
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
        before=before,
        after=after,
        per_lang_verdicts=per_lang_verdicts,
        anima_eval1_greedy=after_anima_greedy,
        anima_eval1_sample=after_anima_sample,
        anima_eval1_greedy_summary=anima_greedy_sum,
        anima_eval1_sample_summary=anima_sample_sum,
        n_anima_register_hits_total=anima_coherent,
        n_strong=n_strong, n_partial=n_partial,
        n_weak=n_weak, n_pure_memorize=n_purem,
        verdict=agg_verdict,
        register_regress=register_regress,
    )
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)

    heldout = dict(
        adapter=adapter_out, base=cfg["base_model"], device=device,
        per_lang={lang: {
            "greedy_summary": after[lang]["summary_greedy"],
            "sample_summary": after[lang]["summary_sample"],
            "verdict": after[lang]["verdict"],
            "probes": {
                k: {
                    "greedy": next((r for r in after[lang]["greedy"]
                                    if r["name"] == k), None),
                    "sample": next((r for r in after[lang]["sample"]
                                    if r["name"] == k), None),
                } for k in PROBES_BY_LANG[lang].keys()
            },
        } for lang in PROBES_BY_LANG.keys()},
        aggregate_verdict=agg_verdict,
        n_strong=n_strong, n_partial=n_partial,
        n_weak=n_weak, n_pure_memorize=n_purem,
    )
    with open(os.path.join(out_dir, "heldout_vp21m.json"), "w") as f:
        json.dump(heldout, f, indent=2, default=str)

    eval1 = dict(
        adapter=adapter_out, base=cfg["base_model"], device=device,
        anima_greedy=after_anima_greedy,
        anima_sample=after_anima_sample,
        summary_greedy=anima_greedy_sum,
        summary_sample=anima_sample_sum,
        register_regress=register_regress,
    )
    with open(os.path.join(out_dir, "vp21m_eval1.json"), "w") as f:
        json.dump(eval1, f, indent=2, default=str)

    print(f"[P21M] DONE — result.json, heldout_vp21m.json, vp21m_eval1.json saved to {out_dir}",
          flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki-corpus", required=True)
    ap.add_argument("--anima-corpus", required=True)
    ap.add_argument("--mixed-corpus", required=True)
    ap.add_argument("--vp21-adapter-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--base-model", default="Qwen/Qwen2.5-1.5B")
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--bsz", type=int, default=2)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--warmup-steps", type=int, default=50)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--n-aug", type=int, default=5)
    ap.add_argument("--wiki-frac", type=float, default=0.3)
    ap.add_argument("--target-corpus-mb", type=int, default=72)
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
