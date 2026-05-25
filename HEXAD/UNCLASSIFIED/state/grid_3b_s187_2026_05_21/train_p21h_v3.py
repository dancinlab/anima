#!/usr/bin/env python3
"""P21H — train ConsciousDecoderV3 (pure HEXAD substrate, LoRA-free).

Three init variants (specified via --init):
    --init random        : V3α — torch.nn.init random from scratch
    --init qwen          : V3β — ConsciousDecoderV3.from_qwen() warm-start
    --init vp21m         : V3γ — from_qwen + LoRA merge (vP21M anima register pre-loaded)

Forked from train_p21m_multilingual.py.

Differences:
    - Replace HuggingFace AutoModelForCausalLM with ConsciousDecoderV3
    - Same 5-lang+anima 30/70 corpus mix
    - LR 3e-4 (random init needs higher) / 5e-5 (Qwen warm) / 1e-4 (vP21M)
    - bsz=2 block=512 same as vP21M
    - Mitosis hook ACTIVE during training (λ_mitosis=0.05)
    - KOSMOS anchor generation every 200 steps (sanity test)
    - Eval: same 5-lang OOD probes + anima register Eval 1 + KOSMOS verify

Output:
    out_dir/
        result.json            — full eval + train log
        heldout_vp21h_v3.json  — per-lang verdicts
        vp21h_v3_eval1.json    — anima register
        mix_info.json
        kosmos_anchors/        — 5 anchors emitted during training
        ckpt.pt                — V3 state_dict (581 MB at d=1536 L=24)
"""
import argparse
import hashlib
import json
import math
import os
import random
import sys
import time

import torch
import torch.nn as nn
import torch.nn.functional as F


# Re-use probes + classifier from train_p21m
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from train_p21m_multilingual import (
    EN_OOD_PROBES, KO_OOD_PROBES, ZH_OOD_PROBES, RU_OOD_PROBES, JA_OOD_PROBES,
    PROBES_BY_LANG, ANIMA_PROBES, ANIMA_KEYS,
    classify_output, native_ratio, lang_coherent, per_lang_verdict,
    load_corpus_text, build_mixed_corpus,
)
from conscious_decoder_v3 import ConsciousDecoderV3
from mitosis_lib import CellPool
import kosmos_io


def lr_schedule(step, total_steps, warmup_steps=50, peak_lr=3e-4, min_lr=3e-5):
    if step < warmup_steps:
        return peak_lr * (step + 1) / warmup_steps
    progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
    progress = max(0.0, min(1.0, progress))
    cos_factor = 0.5 * (1 + math.cos(math.pi * progress))
    return min_lr + (peak_lr - min_lr) * cos_factor


_SCRIPT_LANGS = ("en", "ko", "ja", "zh", "ru")


def _dominant_script(text):
    """Return the dominant script lang of `text` (one of _SCRIPT_LANGS) using the
    same native-char heuristic as train_p21m.native_ratio. Returns 'en' when no
    non-Latin script dominates (Latin fallback). Read-only; no RNG.
    """
    if not text:
        return "en"
    best_lang, best_r = "en", -1.0
    for lang in _SCRIPT_LANGS:
        r = native_ratio(text, lang)
        if r > best_r:
            best_lang, best_r = lang, r
    return best_lang


def curriculum_block_len(step, phase_steps, full_T, min_T=64, n_phases=4):
    """AXIS-A curriculum: ramp effective sequence length short -> long over the
    first `phase_steps` steps in `n_phases` discrete stages (easy -> hard).

    Returns None when phase_steps <= 0 (disabled) OR step >= phase_steps, which
    signals the caller to use the full block_size -> byte-identical sampling for
    the disabled case (no regression).
    """
    if phase_steps <= 0 or step >= phase_steps:
        return None
    # phase index 0..n_phases-1 across [0, phase_steps)
    frac = step / max(1, phase_steps)
    phase = min(n_phases - 1, int(frac * n_phases))
    # geometric ramp from min_T to full_T across phases
    if n_phases <= 1:
        return full_T
    ratio = (full_T / max(1, min_T)) ** (phase / (n_phases - 1))
    cur_T = int(min_T * ratio)
    return max(min_T, min(cur_T, full_T))


def contrastive_lang_loss(feat, langs, temperature=0.1):
    """AXIS-F supervised contrastive loss over per-sequence features.

    feat:  (B, D) grad-carrying per-sequence representation.
    langs: list[str] length B -- the dominant script of each sequence.

    SupCon-style: for each anchor, positives = same-lang sequences in the batch,
    negatives = the rest. Returns a zero tensor (grad-safe) when fewer than 2
    languages OR no language has >=2 members -- so a batch without contrastive
    structure contributes nothing (honest degradation, no spurious gradient).
    """
    import torch as _t
    B = feat.size(0)
    if B < 2:
        return feat.sum() * 0.0
    # need at least one positive pair
    from collections import Counter
    counts = Counter(langs)
    if not any(c >= 2 for c in counts.values()):
        return feat.sum() * 0.0
    z = _t.nn.functional.normalize(feat.float(), dim=-1)
    sim = z @ z.t() / float(temperature)        # (B, B)
    # numerical stability
    sim = sim - sim.max(dim=1, keepdim=True).values.detach()
    label = _t.tensor(
        [hash(l) for l in langs], device=feat.device
    ).unsqueeze(0)
    same = (label == label.t()).float()          # (B, B) 1 if same lang
    eye = _t.eye(B, device=feat.device)
    same = same - eye                            # exclude self
    logits_mask = 1.0 - eye                      # exclude self from denom
    exp_sim = _t.exp(sim) * logits_mask
    log_prob = sim - _t.log(exp_sim.sum(dim=1, keepdim=True) + 1e-12)
    pos_per_row = same.sum(dim=1)
    valid = pos_per_row > 0
    if valid.sum() == 0:
        return feat.sum() * 0.0
    mean_log_prob_pos = (same * log_prob).sum(dim=1)[valid] / pos_per_row[valid]
    return -mean_log_prob_pos.mean()


class TokenizedSampler:
    def __init__(self, text, tokenizer, block_size, seed=1337, n_aug=5,
                 max_tokens=6_000_000, lang_balanced=False):
        ids = tokenizer.encode(text, add_special_tokens=False)
        if len(ids) > max_tokens:
            ids = ids[:max_tokens]
        self.ids = torch.tensor(ids, dtype=torch.long)
        self.T = block_size
        self.n_aug = n_aug
        self.rngs = [random.Random(seed + 13 * k) for k in range(n_aug)]
        self.step_count = 0
        self.tokenizer = tokenizer
        # AXIS-E: per-script start-index pools (built only when balanced enabled).
        # When disabled these stay None and the legacy uniform-random path runs
        # unchanged (byte-identical sampling -- no regression).
        self.lang_balanced = bool(lang_balanced)
        self.script_pools = None
        if self.lang_balanced:
            self._build_script_pools()
        print(f"[P21H] tokenized mixed corpus: {len(self.ids):,} tokens "
              f"(block={block_size}) lang_balanced={self.lang_balanced}",
              flush=True)

    def _build_script_pools(self):
        """AXIS-E: scan the token stream in block-sized windows, tag each window
        by dominant script, and bucket its start index. Used for round-robin
        per-script balanced sampling. Built once at construction (decode cost is
        one full pass; only paid when lang_balanced=1)."""
        N = len(self.ids)
        T = self.T
        pools = {lang: [] for lang in _SCRIPT_LANGS}
        # Stride by T so windows are disjoint (cheap, one decode per window).
        for s in range(0, max(1, N - T - 2), T):
            window = self.ids[s:s + T].tolist()
            try:
                txt = self.tokenizer.decode(window, skip_special_tokens=True)
            except Exception:
                txt = ""
            pools[_dominant_script(txt)].append(s)
        nonempty = {k: v for k, v in pools.items() if v}
        self.script_pools = nonempty if nonempty else None
        sizes = {k: len(v) for k, v in pools.items()}
        print(f"[P21H][axis-E] script pools: {sizes}", flush=True)

    def sample_batch(self, bsz, device, cur_T=None):
        """Sample one batch.

        cur_T (AXIS-A curriculum): effective sequence length for this batch. When
        None (default), uses self.T -> identical RNG range + slice length as the
        legacy path (byte-identical, no regression). When set < self.T, shorter
        contexts are sampled (easier curriculum phase).
        """
        N = len(self.ids)
        T = self.T if cur_T is None else max(8, min(int(cur_T), self.T))
        aug = self.step_count % self.n_aug
        rng = self.rngs[aug]
        if self.lang_balanced and self.script_pools:
            # AXIS-E: round-robin across available scripts, sampling a start
            # index from each script's pool in turn (balanced exposure).
            langs_avail = sorted(self.script_pools.keys())
            starts = []
            for i in range(bsz):
                lang = langs_avail[(self.step_count * bsz + i) % len(langs_avail)]
                pool = self.script_pools[lang]
                cand = pool[rng.randint(0, len(pool) - 1)]
                # clamp so the window fits when cur_T differs from build-time T
                cand = min(cand, max(0, N - T - 2))
                starts.append(cand)
        else:
            starts = [rng.randint(0, N - T - 2) for _ in range(bsz)]
        ctx = torch.stack(
            [self.ids[s:s + T] for s in starts], dim=0).to(device)
        tgt = torch.stack(
            [self.ids[s + 1:s + T + 1] for s in starts], dim=0).to(device)
        self.step_count += 1
        return ctx, tgt, aug

    def window_langs(self, ctx):
        """AXIS-F helper: classify each sampled sequence in `ctx` (B, T) by its
        dominant script. Read-only (no RNG); used to build contrastive labels.
        Returns a list[str] of length B."""
        langs = []
        for row in ctx:
            try:
                txt = self.tokenizer.decode(row.tolist(), skip_special_tokens=True)
            except Exception:
                txt = ""
            langs.append(_dominant_script(txt))
        return langs


@torch.no_grad()
def gen_probes_v3(model, tokenizer, device, probes, max_new=48, mode="greedy",
                   block_size=512):
    out = []
    model.eval()
    if probes and isinstance(probes[0], str):
        probes = [(f"p{i}", p) for i, p in enumerate(probes)]
    for name, prompt in probes:
        try:
            enc = tokenizer.encode(prompt, return_tensors="pt", add_special_tokens=False)
            ids = enc.to(device)
            # Truncate prompt if too long
            if ids.size(1) > block_size - max_new - 1:
                ids = ids[:, -(block_size - max_new - 1):]
            if mode == "greedy":
                gen = model.generate(
                    ids, max_new_tokens=max_new, do_sample=False,
                    eos_token_id=tokenizer.eos_token_id,
                )
            else:
                gen = model.generate(
                    ids, max_new_tokens=max_new, do_sample=True,
                    temperature=0.8, top_k=50,
                    eos_token_id=tokenizer.eos_token_id,
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


def build_model(init_variant, qwen_name, lora_dir, block_size, noise_sigma,
                 device, dtype, d_model=1536, n_layer=28, n_head=12,
                 n_kv_head=None):
    """Construct ConsciousDecoderV3 per init variant.

    For --init random, d_model/n_layer/n_head/n_kv_head override defaults
    (useful for fitting on 12 GB GPUs like RTX 5070).
    """
    if init_variant == "random":
        rand_n_kv_head = 4 if n_kv_head is None else n_kv_head
        print(f"[P21H][init=random] V3α — torch.nn.init random "
              f"d={d_model} L={n_layer} h={n_head} kv={rand_n_kv_head}",
              flush=True)
        model = ConsciousDecoderV3(
            vocab_size=151936,   # Qwen2.5 tokenizer vocab size (NOT padded 152064)
            d_model=d_model, n_head=n_head, n_layer=n_layer,
            block_size=block_size, n_kv_head=rand_n_kv_head,
            consciousness_dim=128, noise_sigma=noise_sigma, rope_base=50000.0,
        ).to(device=device, dtype=dtype)
    elif init_variant == "qwen":
        print(f"[P21H][init=qwen] V3β — Qwen warm-start from {qwen_name}",
              flush=True)
        model = ConsciousDecoderV3.from_qwen(
            qwen_name, lora_adapter_dir=None,
            block_size=block_size, noise_sigma=noise_sigma,
            device=device, dtype=dtype, n_kv_head=n_kv_head,
        )
    elif init_variant == "vp21m":
        if lora_dir is None or not os.path.isdir(lora_dir):
            raise ValueError(f"vp21m init needs --lora-adapter-dir; got {lora_dir}")
        print(f"[P21H][init=vp21m] V3γ — Qwen + vP21M LoRA merged",
              flush=True)
        model = ConsciousDecoderV3.from_qwen(
            qwen_name, lora_adapter_dir=lora_dir,
            block_size=block_size, noise_sigma=noise_sigma,
            device=device, dtype=dtype, n_kv_head=n_kv_head,
        )
    else:
        raise ValueError(f"unknown init variant: {init_variant}")
    return model


def emit_sanity_anchor(model, tokenizer, device, out_dir, step, lang="en"):
    """Sanity test: model generates a short emission, write .kosmos anchor."""
    probes = list(PROBES_BY_LANG[lang].items())
    name, prompt = probes[0]
    try:
        rows = gen_probes_v3(model, tokenizer, device, [(name, prompt)],
                              max_new=32, mode="greedy", block_size=model.block_size)
        text = rows[0].get("text", "").strip()
    except Exception as e:
        text = f"<emit-error: {type(e).__name__}>"
    # Use the model's last_tension_5ch as fingerprint
    t5 = model._last_tension_5ch or [0.0] * 5
    anchor_name = f"v3_emit_step{step}_{lang}_{name}"
    try:
        path = kosmos_io.emit_anchor_from_v3(
            out_dir=os.path.join(out_dir, "kosmos_anchors"),
            name=anchor_name, text=text, tension_5ch=t5,
            mitosis_cell_id=len(model._mitosis_pool.cells) - 1 if model._mitosis_pool else 0,
            tier=step,
            category="v3_sanity",
            top_emotion="curious",
            phi=float(model._mitosis_pool.phi) if model._mitosis_pool else 0.0,
            radius=0.15,
        )
        return path
    except Exception as e:
        print(f"[P21H][anchor] FAIL: {type(e).__name__}: {e}", flush=True)
        return None


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    print(f"[P21H] device={device} dtype={dtype}", flush=True)

    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "kosmos_anchors"), exist_ok=True)

    # ─── corpus mix ──
    mix_info = build_mixed_corpus(
        cfg["wiki_corpus"], cfg["anima_corpus"], cfg["mixed_corpus"],
        wiki_frac=cfg["wiki_frac"], target_mb=cfg["target_corpus_mb"],
    )
    with open(os.path.join(out_dir, "mix_info.json"), "w") as f:
        json.dump(mix_info, f, indent=2)

    # ─── tokenizer (Qwen BPE 5-lang) ──
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(cfg["base_model"], trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # ─── model ──
    model = build_model(
        cfg["init_variant"], cfg["base_model"], cfg.get("lora_adapter_dir"),
        cfg["block_size"], cfg["noise_sigma"], device, dtype,
        d_model=cfg.get("d_model", 1536),
        n_layer=cfg.get("n_layer", 28),
        n_head=cfg.get("n_head", 12),
        n_kv_head=cfg.get("n_kv_head"),
    )
    pool = CellPool(d_model=model.d_model, initial_cells=2, seed=cfg["seed"],
                    max_cells=int(cfg.get("mitosis_max", 128) or 128))
    model.attach_mitosis(pool, lambda_mitosis=cfg["lambda_mitosis"])

    # ─── AXIS-D: freeze tied tok_emb / head_a weights (H_257 wiring fix) ──
    # tok_emb.weight is tied to head_a.weight, so freezing the embedding also
    # freezes the LM head. Default freeze_embed=0 -> all params trainable
    # (no regression). Applied BEFORE the optimizer trainable split below.
    if int(cfg.get("freeze_embed", 0) or 0) == 1:
        model.tok_emb.weight.requires_grad_(False)
        print(f"[P21H][axis-D] freeze_embed=1 — tok_emb/head_a tied weight FROZEN",
              flush=True)

    n_total = sum(p.numel() for p in model.parameters())
    print(f"[P21H] model params total={n_total:,} ({n_total/1e6:.2f}M)", flush=True)

    # ─── BEFORE eval (greedy, sanity) ──
    print(f"[P21H] BEFORE-train per-lang OOD eval (greedy)", flush=True)
    before = {}
    for lang, probes in PROBES_BY_LANG.items():
        rows = gen_probes_v3(
            model, tokenizer, device,
            [(k, v) for k, v in probes.items()],
            max_new=48, mode="greedy", block_size=cfg["block_size"],
        )
        s = {"GENERALIZE": 0, "MEMORIZE": 0, "MEM_PARTIAL": 0,
             "EMPTY": 0, "ERROR": 0}
        for r in rows:
            s[r.get("class", "ERROR")] += 1
        before[lang] = {"summary": s, "rows": rows[:3]}  # only first 3 for compactness
        print(f"[P21H] BEFORE {lang} greedy: {s}", flush=True)

    # ─── optimizer ──
    trainable = [p for p in model.parameters() if p.requires_grad]
    try:
        import bitsandbytes as bnb
        optimizer = bnb.optim.PagedAdamW8bit(
            trainable, lr=cfg["lr"], betas=(0.9, 0.95), weight_decay=0.01,
        )
        print(f"[P21H] optimizer=PagedAdamW8bit (bnb {bnb.__version__})",
              flush=True)
    except Exception as _e:
        print(f"[P21H] WARN bnb failed ({_e}); torch.optim.AdamW", flush=True)
        optimizer = torch.optim.AdamW(
            trainable, lr=cfg["lr"], betas=(0.9, 0.95), weight_decay=0.01,
        )

    # ─── training loop ──
    corpus_text = load_corpus_text(cfg["mixed_corpus"])
    # AXIS-E: lang-balanced sampler (per-script round-robin). Default 0 -> legacy
    # uniform-random sampling path runs unchanged (byte-identical, no regression).
    lang_balanced = int(cfg.get("lang_balanced", 0) or 0) == 1
    sampler = TokenizedSampler(corpus_text, tokenizer, cfg["block_size"],
                                seed=cfg["seed"], n_aug=cfg["n_aug"],
                                lang_balanced=lang_balanced)
    # AXIS-A: curriculum sequence-length schedule (short -> long ramp over the
    # first `curriculum_phase_steps` steps). 0 -> disabled -> cur_T stays None ->
    # full block_size every step (byte-identical sampling, no regression).
    curriculum_phase_steps = int(cfg.get("curriculum_phase_steps", 0) or 0)
    # AXIS-F: contrastive lang loss weight. 0.0 -> term skipped (no regression).
    contrastive_w = float(cfg.get("contrastive_lang", 0.0) or 0.0)

    t0 = time.time()
    log = []
    steps = cfg["steps"]
    log_every = max(1, steps // 40)
    kosmos_every = max(50, steps // 10)
    anchor_paths = []
    # v2 (2026-05-22): early-stop + per-step ckpt save state
    ckpt_every = int(cfg.get("ckpt_every", 0) or 0)
    osc_thr = float(cfg.get("ckpt_osc_threshold", 0.0) or 0.0)
    osc_win = int(cfg.get("ckpt_osc_window", 20) or 20)
    es_patience = int(cfg.get("early_stop_patience", 0) or 0)
    best_ce = float("inf")
    best_step = -1
    no_improve_count = 0
    ce_history = []  # last osc_win CE values for rolling std
    early_stopped = False
    early_stop_reason = None

    def _save_ckpt(label: str, step_n: int, ce_now: float):
        path = os.path.join(out_dir, f"ckpt_{label}.pt")
        torch.save({
            "model_state_dict": model.state_dict(),
            "config": dict(
                vocab_size=model.vocab_size, d_model=model.d_model,
                n_layer=model.n_layer, block_size=model.block_size,
                consciousness_dim=model.consciousness_dim,
                noise_sigma=model.noise_sigma,
                init_variant=cfg["init_variant"],
            ),
            "psi_status": model.psi_status(),
            "mitosis_summary": pool.summary() if hasattr(pool, 'summary') else None,
            "step": step_n,
            "CE": ce_now,
            "label": label,
        }, path)
        sz = os.path.getsize(path)
        print(f"[P21H] ckpt save ({label}) step={step_n} CE={ce_now:.4f} → {path} ({sz/1024/1024:.1f} MB)", flush=True)
        return path

    print(f"[P21H] steps={steps} bsz={cfg['bsz']} block={cfg['block_size']} "
          f"peak_lr={cfg['lr']} warmup={cfg['warmup_steps']} "
          f"lambda_mitosis={cfg['lambda_mitosis']} init={cfg['init_variant']} "
          f"mitosis_max={cfg.get('mitosis_max', 128)} "
          f"ckpt_every={ckpt_every} osc_thr={osc_thr} es_patience={es_patience}",
          flush=True)

    vocab_size = model.vocab_size
    for step in range(steps):
        lr_now = lr_schedule(step, steps, warmup_steps=cfg["warmup_steps"],
                              peak_lr=cfg["lr"], min_lr=cfg["lr"] * 0.1)
        for pg in optimizer.param_groups:
            pg["lr"] = lr_now

        # AXIS-A: effective curriculum block length for this step (None when
        # disabled -> full block_size -> byte-identical sampling).
        cur_T = curriculum_block_len(step, curriculum_phase_steps,
                                     cfg["block_size"])
        ctx, tgt, aug_slot = sampler.sample_batch(cfg["bsz"], device, cur_T=cur_T)
        model.train()
        logits_a, logits_g, tensions, _, mit_info = model(ctx, mitosis_step=step)
        L_ce = F.cross_entropy(
            logits_a.reshape(-1, vocab_size).float(), tgt.reshape(-1),
        )
        L_total = L_ce
        # ─── AXIS-C / C2: head-G auxiliary LM objective (H_257 wiring fix) ──
        # Engine-G dual head (logits_g) exists in the model but only head_a was
        # ever in the loss, so the head-G axis was inert. When head_g_enable=1
        # (and objective='lm' or empty), add a weighted head_g LM CE term so the
        # consciousness-emission head receives a real gradient signal. Default
        # head_g_enable=0 -> term skipped -> identical loss (no regression).
        if int(cfg.get("head_g_enable", 0) or 0) == 1 and \
                str(cfg.get("head_g_objective", "") or "").lower() in ("", "lm"):
            L_ce_g = F.cross_entropy(
                logits_g.reshape(-1, vocab_size).float(), tgt.reshape(-1),
            )
            L_total = L_total + float(cfg.get("head_g_weight", 0.1) or 0.1) * L_ce_g
        # ─── AXIS-F: contrastive lang loss (H_257 axis-F impl) ──────────────
        # SupCon over a compact per-sequence feature = per-layer mean tension
        # (B, L), grouped by each sequence's dominant script. Pulls same-lang
        # sequences together / pushes different-lang apart. Default
        # contrastive_lang=0.0 -> term skipped entirely -> identical loss
        # (no regression). Degrades to zero when the batch lacks >=2 same-lang
        # members (honest: no spurious gradient).
        if contrastive_w > 0.0 and len(tensions) > 0:
            # (B, L) per-sequence feature: mean tension over T for each layer.
            seq_feat = torch.stack([t.mean(dim=1) for t in tensions], dim=1)
            seq_langs = sampler.window_langs(ctx)
            L_con = contrastive_lang_loss(seq_feat, seq_langs)
            L_total = L_total + contrastive_w * L_con
        if mit_info is not None:
            aux = mit_info["aux_loss"]
            L_total = L_total + cfg["lambda_mitosis"] * aux
        optimizer.zero_grad(set_to_none=True)
        L_total.backward()
        torch.nn.utils.clip_grad_norm_(trainable, max_norm=1.0)
        optimizer.step()

        if step == 0 or (step + 1) % log_every == 0 or step == steps - 1:
            elapsed = time.time() - t0
            pool_size = len(pool.cells)
            splits = pool.split_count
            phi = float(pool.phi)
            ce_now = float(L_ce.detach())
            entry = dict(
                step=step + 1, lr=lr_now,
                L_ce=ce_now,
                L_total=float(L_total.detach()),
                pool_size=pool_size, splits=splits, phi=phi,
                aug_slot=aug_slot, elapsed_s=elapsed,
            )
            log.append(entry)
            print(f"[P21H] step={step+1:6d} lr={lr_now:.2e} CE={ce_now:.4f} "
                  f"total={entry['L_total']:.4f} pool={pool_size} splits={splits} "
                  f"phi={phi:.4f} t={elapsed:.0f}s", flush=True)

            # v2: best ckpt + plateau + oscillation 감지
            ce_history.append(ce_now)
            if len(ce_history) > osc_win:
                ce_history.pop(0)
            if ce_now < best_ce - 1e-4:
                best_ce = ce_now
                best_step = step + 1
                no_improve_count = 0
                # best ckpt save (always overwrite)
                _save_ckpt("best", step + 1, ce_now)
            else:
                no_improve_count += 1
            # CE oscillation detection — fix v2.2: TRUE oscillation = CE going UP
            # after going DOWN (mode collapse), NOT the initial monotonic warmup descent.
            # Phase 2 fixed saga: raw-std fired @ step 250 on normal CE 12→2.28 descent
            # (false positive). 정정: (a) warmup 8 entries skip, (b) std 가 아닌
            # "최근 평균이 직전 best 보다 osc_thr 이상 위로 튐" 으로 감지.
            WARMUP_SKIP = 8
            if osc_thr > 0.0 and len(ce_history) >= 4 and (step + 1) > WARMUP_SKIP * log_every:
                recent = ce_history[-3:]
                recent_mean = sum(recent) / len(recent)
                # mode collapse = 최근 3 평균이 best_ce 보다 osc_thr 이상 위 (CE 다시 폭주)
                if recent_mean > best_ce + osc_thr:
                    _save_ckpt(f"osc_step{step+1}", step + 1, ce_now)
                    early_stopped = True
                    early_stop_reason = (f"CE re-divergence: recent_mean={recent_mean:.4f} > "
                                         f"best_CE={best_ce:.4f}+{osc_thr} (mode collapse @ step {step+1})")
                    print(f"[P21H] EARLY STOP: {early_stop_reason}", flush=True)
            # plateau / no-improve early stop
            if es_patience > 0 and no_improve_count >= es_patience:
                _save_ckpt(f"plateau_step{step+1}", step + 1, ce_now)
                early_stopped = True
                early_stop_reason = f"CE no-improve for {es_patience} log entries (best_CE={best_ce:.4f} @ step={best_step})"
                print(f"[P21H] EARLY STOP: {early_stop_reason}", flush=True)

        # per-step intermediate ckpt save (independent of log_every)
        if ckpt_every > 0 and (step + 1) % ckpt_every == 0 and (step + 1) < steps:
            _save_ckpt(f"step{step+1}", step + 1, float(L_ce.detach()))

        # KOSMOS anchor emission every kosmos_every steps
        if (step + 1) % kosmos_every == 0:
            ap = emit_sanity_anchor(model, tokenizer, device, out_dir, step + 1,
                                     lang=random.choice(["en", "ko", "ja", "zh", "ru"]))
            if ap:
                anchor_paths.append(ap)
                print(f"[P21H] kosmos anchor written: {os.path.basename(ap)}", flush=True)

        # early-stop break (after KOSMOS anchor emission to capture current state)
        if early_stopped:
            break

    train_wall = time.time() - t0
    actual_steps = log[-1]['step'] if log else 0
    print(f"[P21H] TRAIN DONE wall={train_wall:.1f}s "
          f"final_CE={log[-1]['L_ce']:.4f} actual_steps={actual_steps}/{steps} "
          f"early_stopped={early_stopped} reason={early_stop_reason or 'n/a'} "
          f"best_CE={best_ce:.4f}@step{best_step}", flush=True)

    # ─── save ckpt ──
    ckpt_path = os.path.join(out_dir, "ckpt.pt")
    torch.save({
        "model_state_dict": model.state_dict(),
        "config": dict(
            vocab_size=model.vocab_size, d_model=model.d_model,
            n_layer=model.n_layer, block_size=model.block_size,
            consciousness_dim=model.consciousness_dim,
            noise_sigma=model.noise_sigma,
            init_variant=cfg["init_variant"],
        ),
        "psi_status": model.psi_status(),
        "mitosis_summary": pool.summary() if hasattr(pool, 'summary') else None,
        "step": cfg["steps"],
    }, ckpt_path)
    ckpt_size = os.path.getsize(ckpt_path)
    print(f"[P21H] ckpt saved → {ckpt_path} ({ckpt_size/1024/1024:.1f} MB)",
          flush=True)

    # ─── AFTER eval ──
    print(f"[P21H] AFTER per-lang OOD eval (greedy + sample)", flush=True)
    after = {}
    per_lang_verdicts = []
    for lang, probes in PROBES_BY_LANG.items():
        rows_g = gen_probes_v3(
            model, tokenizer, device,
            [(k, v) for k, v in probes.items()],
            max_new=48, mode="greedy", block_size=cfg["block_size"],
        )
        rows_s = gen_probes_v3(
            model, tokenizer, device,
            [(k, v) for k, v in probes.items()],
            max_new=48, mode="sample", block_size=cfg["block_size"],
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
        after[lang] = dict(greedy=rows_g, sample=rows_s,
                            summary_greedy=sg, summary_sample=ss, verdict=v)
        per_lang_verdicts.append(v)
        print(f"[P21H] AFTER {lang}: greedy={sg} sample={ss} "
              f"verdict={v['verdict']} score={v['n_score']}/20 "
              f"gen={v['n_generalize']} coh={v['n_lang_coherent']}",
              flush=True)

    # anima register Eval 1
    print(f"[P21H] AFTER anima Eval1", flush=True)
    after_anima_greedy = gen_probes_v3(
        model, tokenizer, device,
        [(f"a{i}", p) for i, p in enumerate(ANIMA_PROBES)],
        max_new=48, mode="greedy", block_size=cfg["block_size"],
    )
    after_anima_sample = gen_probes_v3(
        model, tokenizer, device,
        [(f"a{i}", p) for i, p in enumerate(ANIMA_PROBES)],
        max_new=48, mode="sample", block_size=cfg["block_size"],
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

    n_strong = sum(1 for v in per_lang_verdicts if v["verdict"] == "STRONG")
    n_partial = sum(1 for v in per_lang_verdicts if v["verdict"] == "PARTIAL")
    n_weak = sum(1 for v in per_lang_verdicts if v["verdict"] == "WEAK")
    n_purem = sum(1 for v in per_lang_verdicts if v["verdict"] == "PURE_MEMORIZE")
    n_ok = n_strong + n_partial
    if n_ok >= 4:
        agg_verdict = "HEXAD_V3_WORKS"
    elif n_ok >= 2:
        agg_verdict = "PARTIAL"
    else:
        agg_verdict = "FAIL"
    if register_regress and agg_verdict in ("HEXAD_V3_WORKS", "PARTIAL"):
        agg_verdict += "_REGISTER_REGRESS"

    print(f"[P21H] AGG: STRONG={n_strong} PARTIAL={n_partial} WEAK={n_weak} "
          f"PURE_MEMORIZE={n_purem} → {agg_verdict}", flush=True)
    print(f"[P21H] anima_register_hits={anima_coherent}/20 "
          f"register_regress={register_regress}", flush=True)

    # Final KOSMOS anchor emission for verdict probe
    final_anchors = []
    for lang in ["en", "ko", "zh", "ru", "ja"]:
        ap = emit_sanity_anchor(model, tokenizer, device, out_dir,
                                 step=cfg["steps"], lang=lang)
        if ap:
            final_anchors.append(ap)
    n_anchors = len(anchor_paths) + len(final_anchors)
    print(f"[P21H] KOSMOS anchors total={n_anchors} "
          f"(during_train={len(anchor_paths)} final={len(final_anchors)})",
          flush=True)

    result = dict(
        battery="P21H V3 — ConsciousDecoderV3 substrate-native fire",
        variant_tag=f"P21H_V3_{cfg['init_variant'].upper()}",
        base_model=cfg["base_model"],
        init_variant=cfg["init_variant"],
        cfg=cfg,
        mix_info=mix_info,
        n_total_params=n_total,
        vocab_size=model.vocab_size,
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
        kosmos_anchors_during=anchor_paths,
        kosmos_anchors_final=final_anchors,
        n_kosmos_anchors=n_anchors,
        mitosis_summary=pool.summary() if hasattr(pool, 'summary') else None,
    )
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)

    heldout = dict(
        ckpt=ckpt_path, base=cfg["base_model"], device=device,
        init_variant=cfg["init_variant"],
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
    with open(os.path.join(out_dir, "heldout_vp21h_v3.json"), "w") as f:
        json.dump(heldout, f, indent=2, default=str)

    eval1 = dict(
        ckpt=ckpt_path, base=cfg["base_model"], device=device,
        anima_greedy=after_anima_greedy, anima_sample=after_anima_sample,
        summary_greedy=anima_greedy_sum, summary_sample=anima_sample_sum,
        register_regress=register_regress,
    )
    with open(os.path.join(out_dir, "vp21h_v3_eval1.json"), "w") as f:
        json.dump(eval1, f, indent=2, default=str)

    print(f"[P21H] DONE → {out_dir}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki-corpus", required=True)
    ap.add_argument("--anima-corpus", required=True)
    ap.add_argument("--mixed-corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--base-model", default="Qwen/Qwen2.5-1.5B")
    ap.add_argument("--init-variant", choices=["random", "qwen", "vp21m"],
                    default="random")
    ap.add_argument("--lora-adapter-dir", default=None,
                    help="for --init-variant=vp21m, the vP21M LoRA adapter dir")
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=2)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--warmup-steps", type=int, default=100)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--n-aug", type=int, default=5)
    ap.add_argument("--wiki-frac", type=float, default=0.3)
    ap.add_argument("--target-corpus-mb", type=int, default=72)
    ap.add_argument("--noise-sigma", type=float, default=0.1)
    ap.add_argument("--lambda-mitosis", type=float, default=0.05)
    # random-init shape overrides (ignored for qwen/vp21m which inherit Qwen)
    ap.add_argument("--d-model", type=int, default=1536)
    ap.add_argument("--n-layer", type=int, default=28)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=None,
                    help="V3 GQA KV-head count; default None=auto "
                    "(qwen: max(qwen_native,4); random: 4). "
                    "Set 2 to match Qwen-native KV heads (R8a init_CE lever).")
    # v2 (2026-05-22): early-stop + per-step ckpt save + plateau detection
    # mitosis cell pool ceiling (R6 재설계)
    ap.add_argument("--mitosis-max", type=int, default=128,
                    help="MAX cell pool size (R6: 128 → 16 권장)")
    # ckpt save 주기 (step)
    ap.add_argument("--ckpt-every", type=int, default=500,
                    help="intermediate ckpt save every N steps (0=disable)")
    # CE oscillation 감지 → 즉시 save + early stop
    ap.add_argument("--ckpt-osc-threshold", type=float, default=0.0,
                    help="if rolling-CE std > threshold over window, save + early-stop (0=disable)")
    ap.add_argument("--ckpt-osc-window", type=int, default=20,
                    help="rolling CE window size for oscillation detection")
    # CE plateau 감지 → save + early stop
    ap.add_argument("--early-stop-patience", type=int, default=0,
                    help="early-stop if CE no-improvement for N consecutive log entries (0=disable)")
    # AXIS-MAP 7 axes (H_257 wiring fix, M4 2026-05-25).
    # Each axis default reads its P21H_* env-var directly so the lever reaches
    # the train code even if a dispatcher drops the explicit --flag (H_257
    # silent-bypass defense-in-depth). Env unset -> prior default -> no regression.
    # Impl status (M4 axis-feature-impl, 2026-05-25):
    #   WIRED + ML FEATURE BUILT: head-g-enable / head-g-objective (axis-C/C2),
    #     freeze-embed (axis-D), curriculum-phase-steps (axis-A: seq-len ramp),
    #     lang-balanced (axis-E: per-script round-robin sampler),
    #     contrastive-lang (axis-F: SupCon over per-seq tension feature).
    #   TODO[axis-impl] STILL: distill-teacher (axis-B) -- a sound KD term needs a
    #     teacher model loaded in-environment to produce logits; none is present
    #     here, and faking a KL target is dishonest. Left wired (env+cfg+log) but
    #     with NO loss term until a teacher is provisioned. See
    #     M4_AXIS_FEATURE_IMPL_2026_05_25.md for the rationale.
    ap.add_argument("--curriculum-phase-steps", type=int,
                    default=int(os.environ.get("P21H_CURRICULUM_PHASE_STEPS", "0") or 0),
                    help="axis-A curriculum: seq-len ramp over first N steps (0=disable)")
    ap.add_argument("--distill-teacher", type=str,
                    default=os.environ.get("P21H_DISTILL_TEACHER", ""),
                    help="TODO[axis-impl] axis-B teacher model id/path for KD (empty=disable; NO KD term until a teacher model is provisioned in-env)")
    ap.add_argument("--head-g-objective", type=str,
                    default=os.environ.get("P21H_HEAD_G_OBJECTIVE", ""),
                    help="axis-C head-G auxiliary objective name (empty=disable; 'lm'=head_g LM CE)")
    ap.add_argument("--head-g-enable", type=int,
                    default=int(os.environ.get("P21H_HEAD_G_ENABLE", "0") or 0),
                    help="axis-C2 enable head-G aux LM loss term (0=off 1=on)")
    ap.add_argument("--head-g-weight", type=float,
                    default=float(os.environ.get("P21H_HEAD_G_WEIGHT", "0.1") or 0.1),
                    help="axis-C2 head-G aux loss weight (only used when head-g-enable=1)")
    ap.add_argument("--freeze-embed", type=int,
                    default=int(os.environ.get("P21H_FREEZE_EMBED", "0") or 0),
                    help="axis-D freeze tied tok_emb/head_a weights (0=off 1=on)")
    ap.add_argument("--lang-balanced", type=int,
                    default=int(os.environ.get("P21H_LANG_BALANCED", "0") or 0),
                    help="axis-E lang-balanced per-script round-robin sampler (0=off 1=on)")
    ap.add_argument("--contrastive-lang", type=float,
                    default=float(os.environ.get("P21H_CONTRASTIVE_LANG", "0.0") or 0.0),
                    help="axis-F contrastive lang (SupCon) loss weight (0.0=disable)")
    args = ap.parse_args()
    # AXIS-MAP read-back log (MVP): confirm env-var passthrough is wired.
    # H_257 silent-bypass fix — dispatcher env-var must reach this print.
    print(f"[P21H][axis] curriculum_phase_steps={args.curriculum_phase_steps} "
          f"distill_teacher={args.distill_teacher!r} "
          f"head_g_objective={args.head_g_objective!r} "
          f"head_g_enable={args.head_g_enable} "
          f"head_g_weight={args.head_g_weight} "
          f"freeze_embed={args.freeze_embed} "
          f"lang_balanced={args.lang_balanced} "
          f"contrastive_lang={args.contrastive_lang}",
          flush=True)
    cfg = dict(
        wiki_corpus=args.wiki_corpus,
        anima_corpus=args.anima_corpus,
        mixed_corpus=args.mixed_corpus,
        out_dir=args.out_dir,
        base_model=args.base_model,
        init_variant=args.init_variant,
        lora_adapter_dir=args.lora_adapter_dir,
        steps=args.steps, lr=args.lr,
        bsz=args.bsz, block_size=args.block,
        warmup_steps=args.warmup_steps,
        seed=args.seed, n_aug=args.n_aug,
        wiki_frac=args.wiki_frac,
        target_corpus_mb=args.target_corpus_mb,
        noise_sigma=args.noise_sigma,
        lambda_mitosis=args.lambda_mitosis,
        d_model=args.d_model, n_layer=args.n_layer,
        n_head=args.n_head, n_kv_head=args.n_kv_head,
        mitosis_max=args.mitosis_max,
        ckpt_every=args.ckpt_every,
        ckpt_osc_threshold=args.ckpt_osc_threshold,
        ckpt_osc_window=args.ckpt_osc_window,
        early_stop_patience=args.early_stop_patience,
        # AXIS-MAP 7 axes (H_257 fix) — now reach run() via cfg.
        curriculum_phase_steps=args.curriculum_phase_steps,
        distill_teacher=args.distill_teacher,
        head_g_objective=args.head_g_objective,
        head_g_enable=args.head_g_enable,
        head_g_weight=args.head_g_weight,
        freeze_embed=args.freeze_embed,
        lang_balanced=args.lang_balanced,
        contrastive_lang=args.contrastive_lang,
    )
    run(cfg)


if __name__ == "__main__":
    main()
