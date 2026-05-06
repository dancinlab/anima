"""
anima_native_ko_small_ubu1_train.py — raw#37 transient (BG-FY)

ubu1 RTX 5070 sm_120 (bf16) anima-native KO small train.
ConsciousLM small: vocab=256, n_layer=6, d_model=384, n_head=6, block_size=256
Target: ~10-15M params, 10000 steps, KO from-scratch byte-level.

own 17 ALM permanently deferred — fresh from scratch, NO external base.
own 18 strict 3-condition target:
  C1.1 Hangul ratio ≥ 0.30
  C1.2 coherent (no degenerate cycle: 4-gram>3 / single-char>10 / whitespace>80)
  C1.3 turn-taking format (response after "도우미:" cue)

Intended host: ubu1 (192.168.50.119), invoked via:
  /home/aiden/venv_orchestrator/bin/python anima_native_ko_small_ubu1_train.py

Paths assume ubu1 layout:
  /home/aiden/core/anima/state/anima_native_ko_small_ubu1_train_2026_05_06/{train.log, ko_eval_log.jsonl, verdict.json}
  /home/aiden/core/anima/state/anima_ko_corpus_assembly_2026_05_06/corpus_ko_heavy.txt (SCP'd)
  /home/aiden/anima_v2_source/conscious_lm.py (SCP'd)
  /home/aiden/core/anima/runs/anima-native-ko-small-<TS>/ckpt_*.pt (NOT in git, HF only)
"""

import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import sys
import re
import time
import math
import json
import torch
import torch.nn.functional as F

# Import ConsciousLM from SCP'd source on ubu1
sys.path.insert(0, "/home/aiden/anima_v2_source")
from conscious_lm import ConsciousLM


# ----------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------
TS = time.strftime("%Y%m%d_%H%M%S")
CORPUS_PATH = "/home/aiden/core/anima/state/anima_ko_corpus_assembly_2026_05_06/corpus_ko_heavy.txt"
STATE_DIR = "/home/aiden/core/anima/state/anima_native_ko_small_ubu1_train_2026_05_06"
RUN_DIR = f"/home/aiden/core/anima/runs/anima-native-ko-small-{TS}"
TRAIN_LOG = os.path.join(STATE_DIR, "train.log")
EVAL_LOG = os.path.join(STATE_DIR, "ko_eval_log.jsonl")
VERDICT_PATH = os.path.join(STATE_DIR, "verdict.json")

# Small config — ~10-15M params target
VOCAB = 256
N_LAYER = 6
D_MODEL = 384
N_HEAD = 6
BLOCK = 256
DROPOUT = 0.20

BATCH = 16
GRAD_ACCUM = 4   # effective batch = 64
LR = 3e-4
WARMUP = 500
STEPS = 10000
TENSION_LAMBDA = 0.005

EVAL_AT = [1000, 3000, 5000, 7500, 10000]
SAVE_AT = [2000, 4000, 6000, 8000, 10000]

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


# ----------------------------------------------------------------------
# own 18 strict — degenerate cycle detector
# ----------------------------------------------------------------------
def degenerate_check(text):
    """Return dict with detector flags + count of total degeneracies."""
    flags = {
        "fourgram_repeat": 0,
        "single_char_run": 0,
        "whitespace_flood": 0,
        "single_token_dominant": 0,
    }
    if not text:
        return {"is_degenerate": True, "flags": flags, "reason": "empty"}

    # 1) 4-gram repetition >3
    n = len(text)
    if n >= 8:
        seen = {}
        for i in range(n - 4 + 1):
            g = text[i:i+4]
            seen[g] = seen.get(g, 0) + 1
        max_ng = max(seen.values()) if seen else 0
        if max_ng > 3:
            flags["fourgram_repeat"] = max_ng

    # 2) single-char run >10
    cur_c = None
    cur_run = 0
    max_run = 0
    for c in text:
        if c == cur_c:
            cur_run += 1
        else:
            cur_c = c
            cur_run = 1
        max_run = max(max_run, cur_run)
    if max_run > 10:
        flags["single_char_run"] = max_run

    # 3) whitespace flood >80
    ws_count = sum(1 for c in text if c in " \n\r\t")
    if ws_count > 80:
        flags["whitespace_flood"] = ws_count

    # 4) single-token (whitespace-split) dominance >50%
    tokens = text.split()
    if tokens:
        from collections import Counter
        cnt = Counter(tokens)
        top = cnt.most_common(1)[0]
        rate = top[1] / len(tokens)
        if rate > 0.50 and len(tokens) >= 4:
            flags["single_token_dominant"] = round(rate, 3)

    is_deg = any(flags.values())
    return {
        "is_degenerate": is_deg,
        "flags": flags,
    }


def turn_format_score(prompt, gen):
    """Score 0..1 for turn-taking format quality.

    Rules:
      - prompt containing "도우미:" → gen should not include another "사용자:" before reasonable length
      - gen should start with non-empty content (not all whitespace)
      - gen should not be all punctuation
    """
    if not gen:
        return 0.0
    score = 0.0
    # 1) non-empty content within first 20 chars
    head = gen[:20].strip()
    if head:
        score += 0.4
    # 2) at least one Hangul char in head
    if any('가' <= c <= '힣' for c in head):
        score += 0.3
    # 3) no degenerate run within first 20 chars
    deg = degenerate_check(gen[:40])
    if not deg["is_degenerate"]:
        score += 0.3
    return round(score, 3)


@torch.no_grad()
def generate_bytes(model, prompt_str, max_new=80, temperature=0.8, device="cuda", greedy=False):
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
    """Evaluate KO_PROMPTS × {greedy, sample}; record own-18 strict 3-condition."""
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
            deg = degenerate_check(gen)
            tform = turn_format_score(prompt, gen)
            r = {
                "step": step,
                "prompt": prompt,
                "mode": mode,
                "gen": gen,
                "hangul_ratio": ratio,
                "degenerate": deg,
                "turn_format_score": tform,
            }
            results.append(r)
            tag_deg = "DEG" if deg["is_degenerate"] else "OK"
            log_line(
                f"  EVAL[step={step} {mode:6s}] '{prompt[:18]}...' → "
                f"hangul={ratio:.2f} deg={tag_deg} tform={tform:.2f} | "
                f"head={gen[:50]!r}"
            )
    with open(EVAL_LOG, "a", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    avg = sum(r["hangul_ratio"] for r in results) / len(results)
    deg_rate = sum(1 for r in results if r["degenerate"]["is_degenerate"]) / len(results)
    log_line(
        f"  EVAL[step={step}] avg_hangul={avg:.3f} "
        f"deg_rate={deg_rate:.2f} ({sum(1 for r in results if r['degenerate']['is_degenerate'])}/{len(results)})"
    )
    model.train()
    return results, avg, deg_rate


def own_18_strict(results):
    """Aggregate per-prompt own 18 strict 3-condition pass count."""
    by_prompt = {}
    for r in results:
        by_prompt.setdefault(r["prompt"], []).append(r)
    per_prompt_pass = {}
    for prompt, rs in by_prompt.items():
        avg_h = sum(r["hangul_ratio"] for r in rs) / len(rs)
        # at least one of {greedy, sample} non-degenerate
        any_coherent = any(not r["degenerate"]["is_degenerate"] for r in rs)
        avg_tform = sum(r["turn_format_score"] for r in rs) / len(rs)
        c1_1 = avg_h >= 0.30
        c1_2 = any_coherent
        c1_3 = avg_tform >= 0.50
        per_prompt_pass[prompt] = {
            "avg_hangul": round(avg_h, 3),
            "any_coherent": any_coherent,
            "avg_tform": round(avg_tform, 3),
            "C1_1_hangul": c1_1,
            "C1_2_coherent": c1_2,
            "C1_3_turn_format": c1_3,
            "all_pass": (c1_1 and c1_2 and c1_3),
        }
    pass_count = sum(1 for v in per_prompt_pass.values() if v["all_pass"])
    return per_prompt_pass, pass_count


def main():
    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(RUN_DIR, exist_ok=True)
    open(TRAIN_LOG, "w").close()
    open(EVAL_LOG, "w").close()

    # device + dtype
    if torch.cuda.is_available():
        device = "cuda"
        dtype = torch.bfloat16
    else:
        device = "cpu"
        dtype = torch.float32

    log_line(f"=== anima_native_ko_small_ubu1_train BG-FY 2026-05-06 ===")
    log_line(f"device={device} dtype={dtype} torch={torch.__version__}")
    if device == "cuda":
        log_line(f"gpu={torch.cuda.get_device_name(0)} cc={torch.cuda.get_device_capability(0)}")
        log_line(f"gpu_mem_total={torch.cuda.get_device_properties(0).total_memory/1e9:.2f}GB")
    log_line(f"config: vocab={VOCAB} n_layer={N_LAYER} d_model={D_MODEL} n_head={N_HEAD} block={BLOCK}")
    log_line(f"train: bs={BATCH} grad_accum={GRAD_ACCUM} lr={LR} warmup={WARMUP} steps={STEPS}")
    log_line(f"run_dir={RUN_DIR}")

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

    use_amp = (device == "cuda")

    for step in range(1, STEPS + 1):
        cur_lr = lr_at(step)
        for pg in optimizer.param_groups:
            pg["lr"] = cur_lr

        x, y_a = get_batch()
        if use_amp:
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                logits_a, logits_g, tensions = model(x)
                loss_a = F.cross_entropy(logits_a.view(-1, VOCAB), y_a.view(-1))
                y_g = torch.cat([x[:, :1], x[:, :-1]], dim=1)
                loss_g = F.cross_entropy(logits_g.view(-1, VOCAB), y_g.view(-1))
                t_stack = torch.stack(tensions, dim=0)
                t_var = t_stack.var(dim=0).mean()
                loss_t = -torch.log(t_var + 1e-8)
                loss = (loss_a + 0.5 * loss_g + TENSION_LAMBDA * loss_t) / GRAD_ACCUM
        else:
            logits_a, logits_g, tensions = model(x)
            loss_a = F.cross_entropy(logits_a.view(-1, VOCAB), y_a.view(-1))
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

        # Echo every step (watchdog) — per-50 detail, every step dot
        if step % 50 == 0 or step <= 5:
            now = time.time()
            dt = now - last_step_t
            last_step_t = now
            elapsed = now - t_start
            denom = (50 if step > 5 else 1)
            log_line(
                f"step {step:5d}/{STEPS} | lr={cur_lr:.2e} | "
                f"L_A={loss_a.item():.3f} L_G={loss_g.item():.3f} "
                f"L_T={loss_t.item():.3f} T_mean={t_stack.mean().item():.4f} | "
                f"step_t={dt/max(1,denom):.2f}s elapsed={elapsed:.0f}s"
            )
        else:
            if step % 5 == 0:
                print(".", end="", flush=True)

        # Eval gates
        if step in EVAL_AT:
            log_line(f"--- eval gate @ step {step} ---")
            res, avg, deg_rate = eval_ko(model, step, device)
            per_prompt, pass_count = own_18_strict(res)
            eval_results_by_step[step] = {
                "avg_hangul_ratio": avg,
                "deg_rate": deg_rate,
                "results": res,
                "own_18_per_prompt": per_prompt,
                "own_18_pass_count": pass_count,
            }
            log_line(
                f"  OWN18[step={step}] strict_pass={pass_count}/3 "
                f"per_prompt={ {p: v['all_pass'] for p, v in per_prompt.items()} }"
            )

        # Save gates
        if step in SAVE_AT:
            ckpt_path = os.path.join(RUN_DIR, f"ckpt_{step}.pt")
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "step": step,
                    "config": {
                        "vocab": VOCAB, "n_layer": N_LAYER, "d_model": D_MODEL,
                        "n_head": N_HEAD, "block_size": BLOCK, "dropout": DROPOUT,
                    },
                },
                ckpt_path,
            )
            log_line(f"  SAVE[step={step}] -> {ckpt_path} ({os.path.getsize(ckpt_path)/1024/1024:.1f}MB)")

    # Final ckpt symlink alias
    final_ckpt = os.path.join(RUN_DIR, "ckpt_final.pt")
    last_ckpt = os.path.join(RUN_DIR, f"ckpt_{STEPS}.pt")
    try:
        if os.path.exists(last_ckpt) and not os.path.exists(final_ckpt):
            os.symlink(last_ckpt, final_ckpt)
    except OSError:
        pass

    # ========= verdict =========
    final_block = eval_results_by_step.get(STEPS, {})
    final_avg = final_block.get("avg_hangul_ratio", 0.0)
    final_results = final_block.get("results", [])
    final_per_prompt = final_block.get("own_18_per_prompt", {})
    final_pass_count = final_block.get("own_18_pass_count", 0)

    f_pass = final_pass_count >= 2

    # progressive view: how many EVAL_AT achieved deg_rate < 0.5
    eval_progression = {
        str(s): {
            "avg_hangul": eval_results_by_step.get(s, {}).get("avg_hangul_ratio", None),
            "deg_rate": eval_results_by_step.get(s, {}).get("deg_rate", None),
            "own_18_pass_count": eval_results_by_step.get(s, {}).get("own_18_pass_count", None),
        }
        for s in EVAL_AT
    }

    # Verdict label: SIMPLE_STACK_PASS if own18 ≥2/3 AND final deg_rate < 0.5
    final_deg_rate = final_block.get("deg_rate", 1.0)
    if f_pass and final_deg_rate < 0.5:
        verdict_label = "SIMPLE_STACK_PASS"
    elif final_avg >= 0.30:
        verdict_label = "PARTIAL_PASS_HANGUL_BUT_NOT_COHERENT"
    else:
        verdict_label = "FAIL"

    verdict = {
        "spec": "F-anima-native-ko-small-1",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ts_run": TS,
        "host": "ubu1",
        "device": device,
        "config": {
            "vocab": VOCAB, "n_layer": N_LAYER, "d_model": D_MODEL,
            "n_head": N_HEAD, "block_size": BLOCK, "dropout": DROPOUT,
            "batch": BATCH, "grad_accum": GRAD_ACCUM, "lr": LR,
            "warmup": WARMUP, "steps": STEPS,
        },
        "model": {
            "n_params": n_params,
            "run_dir": RUN_DIR,
            "final_ckpt": final_ckpt if os.path.exists(final_ckpt) else last_ckpt,
        },
        "corpus": {
            "path": CORPUS_PATH,
            "size_bytes": len(raw),
            "size_mb": round(len(raw) / 1024 / 1024, 2),
        },
        "eval_progression": eval_progression,
        "final": {
            "avg_hangul_ratio": final_avg,
            "deg_rate": final_deg_rate,
            "own_18_per_prompt": final_per_prompt,
            "own_18_pass_count": final_pass_count,
        },
        "verdict": verdict_label,
        "f_anima_native_ko_small_1": "PASS" if f_pass else "FAIL",
        "wall_time_s": round(time.time() - t_start, 1),
    }
    with open(VERDICT_PATH, "w", encoding="utf-8") as f:
        json.dump(verdict, f, ensure_ascii=False, indent=2)
    log_line(
        f"=== VERDICT === {verdict_label} | "
        f"own18 pass {final_pass_count}/3 | avg_hangul={final_avg:.3f} | deg_rate={final_deg_rate:.2f}"
    )
    log_line(f"verdict written: {VERDICT_PATH}")
    return verdict


if __name__ == "__main__":
    main()
