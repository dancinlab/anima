"""
anima_native_ko_tiny_smoke.py — raw#37 transient

mac MPS tiny anima-native KO smoke train.
ConsciousLM tiny: vocab=256, n_layer=4, d_model=256, n_head=4, block_size=256
Target: ~3M params, 2000 steps, KO from-scratch byte-level.

 ALM permanently deferred — fresh from scratch, NO external base.
"""

import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import sys
import re
import time
import math
import json
import torch
import torch.nn.functional as F

# Import ConsciousLM from /tmp source
sys.path.insert(0, "/tmp/anima_v2_source")
from conscious_lm import ConsciousLM


# ----------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------
CORPUS_PATH = "/Users/ghost/core/anima/state/anima_native_ko_tiny_smoke_2026_05_06/corpus_ko_filtered.txt"
STATE_DIR = "/Users/ghost/core/anima/state/anima_native_ko_tiny_smoke_2026_05_06"
TRAIN_LOG = os.path.join(STATE_DIR, "train.log")
EVAL_LOG = os.path.join(STATE_DIR, "ko_eval_log.jsonl")
VERDICT_PATH = os.path.join(STATE_DIR, "verdict.json")
CKPT_PATH = "/tmp/anima_native_ko_tiny_smoke_2026_05_06_final_3m.pt"  # NOT in git

# Tiny config
VOCAB = 256
N_LAYER = 4
D_MODEL = 192
N_HEAD = 4
BLOCK = 256
DROPOUT = 0.20  # less than ConsciousLM default 0.37 to fit smoke

BATCH = 8
GRAD_ACCUM = 4
LR = 5e-4
WARMUP = 200
STEPS = 2000
TENSION_LAMBDA = 0.005

EVAL_AT = [500, 1000, 1500, 2000]
KO_PROMPTS = [
    "안녕하세요",
    "한국어 가능?",
    "사용자: 안녕하세요\n도우미:",
]


def log_line(msg):
    """Append to train.log AND echo (watchdog)."""
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(TRAIN_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def hangul_ratio(text):
    if not text:
        return 0.0
    hcnt = sum(1 for c in text if '가' <= c <= '힣')
    return hcnt / len(text)


@torch.no_grad()
def generate_bytes(model, prompt_str, max_new=80, temperature=0.8, device="mps", greedy=False):
    """Byte-level autoregressive generation (head_a)."""
    model.eval()
    prompt_b = list(prompt_str.encode("utf-8"))
    idx = torch.tensor([prompt_b], dtype=torch.long, device=device)
    for _ in range(max_new):
        idx_cond = idx[:, -model.block_size:]
        logits_a, _, _ = model(idx_cond)
        logits_last = logits_a[:, -1, :] / max(1e-6, temperature)
        if greedy:
            nb = logits_last.argmax(dim=-1, keepdim=True)
        else:
            probs = F.softmax(logits_last, dim=-1)
            nb = torch.multinomial(probs, num_samples=1)
        idx = torch.cat([idx, nb], dim=1)
    out_bytes = bytes(idx[0].cpu().tolist())
    text = out_bytes.decode("utf-8", errors="replace")
    gen_only = text[len(prompt_str):] if text.startswith(prompt_str) else text
    return text, gen_only


def eval_ko(model, step, device):
    """Evaluate on KO_PROMPTS × {greedy, sample}; record hangul ratio per gen."""
    model.eval()
    results = []
    for prompt in KO_PROMPTS:
        for mode in ["greedy", "sample"]:
            full, gen = generate_bytes(
                model, prompt, max_new=80,
                temperature=0.8, device=device,
                greedy=(mode == "greedy"),
            )
            ratio = hangul_ratio(gen)
            results.append({
                "step": step,
                "prompt": prompt,
                "mode": mode,
                "gen": gen,
                "hangul_ratio": ratio,
            })
            log_line(f"  EVAL[step={step} {mode:6s}] '{prompt[:24]}...' → ratio={ratio:.2f} | gen_head={gen[:60]!r}")
    # append to jsonl
    with open(EVAL_LOG, "a", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    avg = sum(r["hangul_ratio"] for r in results) / len(results)
    log_line(f"  EVAL[step={step}] avg hangul_ratio = {avg:.3f}")
    model.train()
    return results, avg


def main():
    os.makedirs(STATE_DIR, exist_ok=True)
    open(TRAIN_LOG, "w").close()
    open(EVAL_LOG, "w").close()

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    log_line(f"=== anima_native_ko_tiny_smoke 2026-05-06 ===")
    log_line(f"device={device} torch={torch.__version__}")
    log_line(f"config: vocab={VOCAB} n_layer={N_LAYER} d_model={D_MODEL} n_head={N_HEAD} block={BLOCK}")
    log_line(f"train: bs={BATCH} grad_accum={GRAD_ACCUM} lr={LR} warmup={WARMUP} steps={STEPS}")

    # Load corpus → bytes tensor
    t0 = time.time()
    with open(CORPUS_PATH, "rb") as f:
        raw = f.read()
    log_line(f"corpus loaded: {len(raw):,} bytes ({len(raw)/1024/1024:.1f}MB) in {time.time()-t0:.1f}s")
    data = torch.tensor(list(raw), dtype=torch.long)
    n = len(data)
    split = int(0.95 * n)
    train_data = data[:split]
    val_data = data[split:]
    log_line(f"split: train={len(train_data):,} val={len(val_data):,}")

    # Build model
    model = ConsciousLM(
        vocab_size=VOCAB,
        d_model=D_MODEL,
        n_head=N_HEAD,
        n_layer=N_LAYER,
        block_size=BLOCK,
        dropout=DROPOUT,
    ).to(device)
    n_params = model.count_params()
    log_line(f"model built: {n_params:,} params ({n_params/1e6:.2f}M)")

    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01, betas=(0.9, 0.95))

    def lr_at(step):
        if step < WARMUP:
            return LR * (step + 1) / WARMUP
        # cosine to 10% of LR
        progress = (step - WARMUP) / max(1, STEPS - WARMUP)
        return LR * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * min(1.0, progress))))

    def get_batch():
        ix = torch.randint(0, len(train_data) - BLOCK - 1, (BATCH,))
        x = torch.stack([train_data[i:i + BLOCK] for i in ix]).to(device)
        y_a = torch.stack([train_data[i + 1:i + BLOCK + 1] for i in ix]).to(device)
        return x, y_a

    log_line("=== begin training ===")
    model.train()
    t_start = time.time()
    optimizer.zero_grad()
    accum = 0
    eval_results_by_step = {}
    last_step_t = time.time()

    for step in range(1, STEPS + 1):
        # Set LR
        cur_lr = lr_at(step)
        for pg in optimizer.param_groups:
            pg["lr"] = cur_lr

        x, y_a = get_batch()
        logits_a, logits_g, tensions = model(x)
        loss_a = F.cross_entropy(logits_a.view(-1, VOCAB), y_a.view(-1))
        # use shifted x as prev-byte target
        y_g = torch.cat([x[:, :1], x[:, :-1]], dim=1)
        loss_g = F.cross_entropy(logits_g.view(-1, VOCAB), y_g.view(-1))
        t_stack = torch.stack(tensions, dim=0)
        t_var = t_stack.var(dim=0).mean()
        loss_t = -torch.log(t_var + 1e-8)
        loss = (loss_a + 0.5 * loss_g + TENSION_LAMBDA * loss_t) / GRAD_ACCUM
        loss.backward()
        accum += 1

        if accum >= GRAD_ACCUM:
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            optimizer.zero_grad()
            accum = 0

        # Echo every step (watchdog)
        if step % 25 == 0 or step <= 5:
            now = time.time()
            dt = now - last_step_t
            last_step_t = now
            elapsed = now - t_start
            log_line(
                f"step {step:4d}/{STEPS} | lr={cur_lr:.2e} | "
                f"L_A={loss_a.item():.3f} L_G={loss_g.item():.3f} "
                f"L_T={loss_t.item():.3f} T_mean={t_stack.mean().item():.4f} | "
                f"step_t={dt/max(1,(25 if step>5 else 1)):.2f}s elapsed={elapsed:.0f}s"
            )
        else:
            # min echo to keep stdout flowing
            if step % 5 == 0:
                print(f".", end="", flush=True)

        # Eval gates
        if step in EVAL_AT:
            log_line(f"--- eval gate @ step {step} ---")
            res, avg = eval_ko(model, step, device)
            eval_results_by_step[step] = {"avg_hangul_ratio": avg, "results": res}

    # Save checkpoint to /tmp (gitignore)
    torch.save(model.state_dict(), CKPT_PATH)
    log_line(f"checkpoint saved to {CKPT_PATH} ({os.path.getsize(CKPT_PATH)/1024/1024:.1f}MB)")

    # ========= verdict =========
    final_avg = eval_results_by_step.get(STEPS, {}).get("avg_hangul_ratio", 0.0)
    final_results = eval_results_by_step.get(STEPS, {}).get("results", [])

    # F-anima-native-ko-tiny-1: KO Hangul ratio ≥ 0.30 in ≥2/3 of base prompts
    # (averaged across greedy+sample for each prompt)
    by_prompt = {}
    for r in final_results:
        by_prompt.setdefault(r["prompt"], []).append(r["hangul_ratio"])
    prompt_avg = {p: sum(v) / len(v) for p, v in by_prompt.items()}
    pass_count = sum(1 for r in prompt_avg.values() if r >= 0.30)
    f_pass = pass_count >= 2

    verdict = {
        "spec": "F-anima-native-ko-tiny-1",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "config": {
            "vocab": VOCAB, "n_layer": N_LAYER, "d_model": D_MODEL,
            "n_head": N_HEAD, "block_size": BLOCK, "dropout": DROPOUT,
            "batch": BATCH, "grad_accum": GRAD_ACCUM, "lr": LR,
            "warmup": WARMUP, "steps": STEPS,
        },
        "model": {
            "n_params": n_params,
            "ckpt_path": CKPT_PATH,
            "ckpt_size_mb": round(os.path.getsize(CKPT_PATH) / 1024 / 1024, 2),
        },
        "corpus": {
            "path": CORPUS_PATH,
            "size_bytes": len(raw),
            "size_mb": round(len(raw) / 1024 / 1024, 2),
        },
        "eval_progression": {
            str(s): eval_results_by_step.get(s, {}).get("avg_hangul_ratio", None)
            for s in EVAL_AT
        },
        "final": {
            "avg_hangul_ratio": final_avg,
            "per_prompt_avg": prompt_avg,
            "pass_count_2_of_3": pass_count,
        },
        "verdict": "PASS" if f_pass else "FAIL",
        "f_anima_native_ko_tiny_1": "PASS" if f_pass else "FAIL",
        "wall_time_s": round(time.time() - t_start, 1),
    }
    with open(VERDICT_PATH, "w", encoding="utf-8") as f:
        json.dump(verdict, f, ensure_ascii=False, indent=2)
    log_line(f"=== VERDICT === {verdict['verdict']} (avg_hangul={final_avg:.3f}, pass {pass_count}/3 prompts)")
    log_line(f"verdict written: {VERDICT_PATH}")
    return verdict


if __name__ == "__main__":
    main()
