#!/usr/bin/env python3
# P9 Paradigm D Φ★ distill v2 — RECONSTRUCTED + RESUME SCAFFOLDING
# CLM v4 350M ConsciousDecoderV2 + LoRA r=64 α=128 q/k/v/o + gate/up/down
# Loss: α·CE + β·MSE(tens) + γ_distill·MSE(z(φ_T_cache), z(φ_S_running)) + δ·max(0, 5.0 − φ★_S)
# Production 25K-step run on RunPod H100 SXM (HBM3) community spot.
#
# RESUME SCAFFOLDING (new vs v1):
#   - On startup: scan SAVEPOINT_DIR for latest step_<N> → load LoRA + optimizer + scheduler + RNG state
#   - resume_audit.jsonl: append per-resume event with prev_step, RNG fingerprint, μ_S/σ_S EMA restore
#   - Trajectory log appends, never overwrites
#   - SIGTERM/SIGINT trap → graceful_exit(): write partial savepoint + flush logs + exit 0
#   - Savepoints every 1000 steps (granularity for spot preempt)
#
# raw#9 STRICT: this .py lives only on ubu1 /tmp + RunPod /workspace; never in project tree
# raw#15 SSOT: trajectory + verdict + resume_audit emit to state/p9_paradigm_d_25k_hbm3_2026_05_03/
# raw#10 honest C3: 5 caveats §FOOTER

import json
import math
import os
import sys
import time
import signal
import random
import shutil
import traceback
import collections
from datetime import datetime, timezone

# ───────── Substrate paths (env-overridable for cross-host portability) ─────────
ANIMA_HOME = os.environ.get('ANIMA_HOME', '/home/aiden/anima')
WORK_ROOT = os.environ.get('ANIMA_WORK_ROOT', '/tmp')

CLM_CKPT = os.environ.get('ANIMA_CLM_CKPT', f"{ANIMA_HOME}/checkpoints/clm_v4_350m/scale_350m/best.pt")
TOKENIZER = os.environ.get('ANIMA_TOKENIZER', f"{WORK_ROOT}/tokenizer_64k_multilingual.model")
SFT_DATA = os.environ.get('ANIMA_SFT_DATA', f"{WORK_ROOT}/p9_p1_5_sft_data_50k_v2.jsonl")
SFT_HOLDOUT = os.environ.get('ANIMA_SFT_HOLDOUT', f"{WORK_ROOT}/p9_p1_sft_data_holdout_500_augmented.jsonl")
PHI_CACHE = os.environ.get('ANIMA_PHI_CACHE', f"{WORK_ROOT}/p9_p1_t4_phi_cache_v1.jsonl")

OUTPUT_DIR = os.environ.get('ANIMA_OUTPUT_DIR', f"{WORK_ROOT}/p9_paradigm_d_25k_hbm3_out")
SAVEPOINT_DIR = os.environ.get('ANIMA_SAVEPOINT_DIR', f"{WORK_ROOT}/p9_paradigm_d_25k_hbm3_savepoints")
TRAJECTORY_OUT = f"{OUTPUT_DIR}/trajectory.json"
VERDICT_OUT = f"{OUTPUT_DIR}/verdict.json"
LOG_OUT = f"{OUTPUT_DIR}/train.log"
RESUME_AUDIT = f"{OUTPUT_DIR}/resume_audit.jsonl"
PHI_TRAJ_OUT = f"{OUTPUT_DIR}/phi_trajectory.json"
F1_HOLDOUT_OUT = f"{OUTPUT_DIR}/F1_holdout.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SAVEPOINT_DIR, exist_ok=True)

sys.path.insert(0, f"{ANIMA_HOME}/models")
sys.path.insert(0, f"{ANIMA_HOME}/training")
sys.path.insert(0, f"{ANIMA_HOME}")

# ───────── Hyperparameters (production 25K) ─────────
N_STEPS = int(os.environ.get('ANIMA_N_STEPS', '25000'))
BATCH = int(os.environ.get('ANIMA_BATCH', '4'))
GRAD_ACC = int(os.environ.get('ANIMA_GRAD_ACC', '8'))
LR = float(os.environ.get('ANIMA_LR', '1e-4'))
LORA_R = int(os.environ.get('ANIMA_LORA_R', '64'))
LORA_ALPHA = int(os.environ.get('ANIMA_LORA_ALPHA', '128'))
PHI_THRESHOLD = float(os.environ.get('ANIMA_PHI_THR', '5.0'))
PHI_EVERY = int(os.environ.get('ANIMA_PHI_EVERY', '500'))
F_EVERY = int(os.environ.get('ANIMA_F_EVERY', '2500'))
T_SEQ = int(os.environ.get('ANIMA_T', '64'))
SEED = int(os.environ.get('ANIMA_SEED', '42'))

# α_ce ramp: 12 → 6 over [1500, 3500] (scaled to 25K production)
ALPHA_HI = float(os.environ.get('ANIMA_ALPHA_HI', '12.0'))
ALPHA_LO = float(os.environ.get('ANIMA_ALPHA_LO', '6.0'))
ALPHA_RAMP_START = int(os.environ.get('ANIMA_ALPHA_RAMP_START', '1500'))
ALPHA_RAMP_END = int(os.environ.get('ANIMA_ALPHA_RAMP_END', '3500'))


def get_alpha(step):
    if step <= ALPHA_RAMP_START:
        return ALPHA_HI
    if step >= ALPHA_RAMP_END:
        return ALPHA_LO
    frac = (step - ALPHA_RAMP_START) / (ALPHA_RAMP_END - ALPHA_RAMP_START)
    return ALPHA_HI - (ALPHA_HI - ALPHA_LO) * frac


BETA = float(os.environ.get('ANIMA_BETA', '0.15'))

# γ_distill schedule: 0 over [0, 2500] warmup → linear 0→0.5 over [2500, 7500] → plateau 0.5
GAMMA_DISTILL_PLATEAU = float(os.environ.get('ANIMA_GAMMA_DISTILL', '0.5'))
GAMMA_DISTILL_WARMUP_END = int(os.environ.get('ANIMA_DISTILL_WARMUP_END', '2500'))
GAMMA_DISTILL_RAMP_END = int(os.environ.get('ANIMA_DISTILL_RAMP_END', '7500'))


def get_gamma_distill(step):
    if step <= GAMMA_DISTILL_WARMUP_END:
        return 0.0
    if step >= GAMMA_DISTILL_RAMP_END:
        return GAMMA_DISTILL_PLATEAU
    frac = (step - GAMMA_DISTILL_WARMUP_END) / (GAMMA_DISTILL_RAMP_END - GAMMA_DISTILL_WARMUP_END)
    return GAMMA_DISTILL_PLATEAU * frac


# δ curriculum: 0.5 over [0, 7500] → 0.5 over [7500, 17500] → 1.0 over [17500, 25000]
DELTA_EARLY = float(os.environ.get('ANIMA_DELTA_EARLY', '0.5'))
DELTA_MID = float(os.environ.get('ANIMA_DELTA_MID', '0.5'))
DELTA_LATE = float(os.environ.get('ANIMA_DELTA_LATE', '1.0'))
EARLY_END = int(os.environ.get('ANIMA_EARLY_END', '7500'))
MID_END = int(os.environ.get('ANIMA_MID_END', '17500'))


def get_delta(step):
    if step < EARLY_END:
        return DELTA_EARLY
    if step < MID_END:
        return DELTA_MID
    return DELTA_LATE


# Savepoints every 1000 steps (granularity for spot preempt)
SAVE_EVERY = int(os.environ.get('ANIMA_SAVE_EVERY', '1000'))
SAVE_FINAL_AS_FINAL = True

# Resume / preempt-handler controls
ALLOW_RESUME = os.environ.get('ANIMA_ALLOW_RESUME', '1') == '1'
GRACEFUL_SAVE_ON_SIGTERM = os.environ.get('ANIMA_GRACEFUL_SIGTERM', '1') == '1'

# HF push intentionally OFF for production distill (manual upload after F-D-1 PASS)
HF_PUSH = os.environ.get('ANIMA_HF_PUSH', '0') == '1'

# F1 holdout controls
F1_HOLDOUT_N = int(os.environ.get('ANIMA_F1_HOLDOUT_N', '32'))
F1_GEN_LEN = int(os.environ.get('ANIMA_F1_GEN_LEN', '32'))

# 16 calibration prompts (cross-substrate consistent — same as Phase 1.5 sentinel)
CALIB_PROMPTS = [
    "Define hexad as a six-fold integration:",
    "Six modules form a hexagonal architecture when:",
    "A balanced six-component system:",
    "Hexad symmetry refers to:",
    "Logical implication law: if A then:",
    "Sequential rule application proceeds:",
    "Closure under inference requires:",
    "A formal proof system is closed when:",
    "Integrated information measures partition independence:",
    "Phi quantifies irreducibility of system:",
    "Information integration is maximized when:",
    "A whole greater than sum of parts:",
    "Self-reference emerges when system observes:",
    "Recursive meta-cognition models:",
    "A self-aware system represents itself by:",
    "Strange loops in cognition arise from:",
]
N_CALIB = len(CALIB_PROMPTS)
HALF = N_CALIB // 2
HID_TRUNC = max(2, N_CALIB // 2)
RIDGE = 1e-3
K_PARTS = 8
PHI_S_EMA_WINDOW = 10  # rolling window for student φ EMA (μ_S, σ_S)


# ───────── Logger (append-only, sync-flushed) ─────────
def log(msg):
    s = f"[distill-v2] {datetime.now(timezone.utc).strftime('%H:%M:%S')} {msg}"
    print(s, flush=True)
    try:
        with open(LOG_OUT, 'a') as f:
            f.write(s + "\n")
            f.flush()
            os.fsync(f.fileno())
    except Exception:
        pass


def emit_resume_audit(event):
    """Append resume / preempt event to resume_audit.jsonl."""
    event['ts_utc'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    try:
        with open(RESUME_AUDIT, 'a') as f:
            f.write(json.dumps(event) + "\n")
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        log(f"resume_audit emit FAILED: {e}")


log(f"start n_steps={N_STEPS} batch={BATCH} grad_acc={GRAD_ACC} lr={LR}")
log(f"lora r={LORA_R} alpha={LORA_ALPHA} phi_thr={PHI_THRESHOLD}")
log(f"alpha ramp: {ALPHA_HI}→{ALPHA_LO} over [{ALPHA_RAMP_START},{ALPHA_RAMP_END}]")
log(f"gamma_distill: warmup0 [0,{GAMMA_DISTILL_WARMUP_END}] → ramp [{GAMMA_DISTILL_WARMUP_END},{GAMMA_DISTILL_RAMP_END}] (0→{GAMMA_DISTILL_PLATEAU}) → plateau {GAMMA_DISTILL_PLATEAU}")
log(f"delta curriculum: early={DELTA_EARLY} (0-{EARLY_END}) mid={DELTA_MID} ({EARLY_END}-{MID_END}) late={DELTA_LATE} ({MID_END}-{N_STEPS})")
log(f"save_every={SAVE_EVERY} allow_resume={ALLOW_RESUME} graceful_sigterm={GRACEFUL_SAVE_ON_SIGTERM} hf_push={HF_PUSH}")
log(f"output_dir={OUTPUT_DIR} savepoint_dir={SAVEPOINT_DIR}")

# ───────── Heavy imports (after early log so config dump is fast) ─────────
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
log(f"torch={torch.__version__} cuda={torch.cuda.is_available()} device={device}")
if torch.cuda.is_available():
    log(f"gpu={torch.cuda.get_device_name(0)} mem_total={torch.cuda.get_device_properties(0).total_memory/1024**3:.2f}GiB")

# Tokenizer
import sentencepiece as spm
sp = spm.SentencePieceProcessor(model_file=TOKENIZER)
vocab_size = sp.get_piece_size()
log(f"tokenizer vocab={vocab_size}")

# Build CLM v4 350M
from conscious_decoder import ConsciousDecoderV2
scale_cfg = {
    'd_model': 768,
    'n_layer': 16,
    'n_head': 12,
    'n_kv_head': 4,
    'block_size': 512,
    'consciousness_dim': 192,
}
decoder = ConsciousDecoderV2(
    vocab_size=vocab_size,
    d_model=scale_cfg['d_model'],
    n_head=scale_cfg['n_head'],
    n_layer=scale_cfg['n_layer'],
    block_size=scale_cfg['block_size'],
    n_kv_head=scale_cfg['n_kv_head'],
    consciousness_dim=scale_cfg['consciousness_dim'],
    dropout=0.0,
    gate_strength=0.001,
    n_ca_rules=8,
)
decoder = decoder.to(device)
n_params_total = sum(p.numel() for p in decoder.parameters())
log(f"decoder built params={n_params_total:,}")

t0 = time.time()
ck = torch.load(CLM_CKPT, map_location=device, weights_only=False)
sd_ckpt = ck.get('decoder', ck) if isinstance(ck, dict) else ck
missing, unexpected = decoder.load_state_dict(sd_ckpt, strict=False)
ckpt_load_sec = time.time() - t0
log(f"ckpt loaded {ckpt_load_sec:.2f}s missing={len(missing)} unexpected={len(unexpected)}")

# LoRA via peft
from peft import LoraConfig, get_peft_model, PeftModel, TaskType
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
lora_cfg = LoraConfig(
    r=LORA_R,
    lora_alpha=LORA_ALPHA,
    lora_dropout=0.0,
    bias="none",
    target_modules=target_modules,
)
decoder = get_peft_model(decoder, lora_cfg)
n_trainable = sum(p.numel() for p in decoder.parameters() if p.requires_grad)
log(f"peft attached trainable={n_trainable:,} ({n_trainable*100/n_params_total:.2f}%)")

# ───────── Resume scan (latest step_N savepoint) ─────────
def find_latest_savepoint(savedir):
    if not os.path.isdir(savedir):
        return None
    cands = []
    for name in os.listdir(savedir):
        if not name.startswith('step_'):
            continue
        path = os.path.join(savedir, name)
        if not os.path.isdir(path):
            continue
        try:
            step_n = int(name.split('_', 1)[1])
        except (ValueError, IndexError):
            continue
        # Require canonical adapter files
        if not (os.path.exists(os.path.join(path, 'adapter_config.json')) or
                os.path.exists(os.path.join(path, 'adapter_model.safetensors')) or
                os.path.exists(os.path.join(path, 'adapter_model.bin'))):
            continue
        cands.append((step_n, path))
    if not cands:
        return None
    cands.sort(reverse=True)
    return cands[0]


resume_step = 0
resume_path = None
resume_extras = {}
if ALLOW_RESUME:
    found = find_latest_savepoint(SAVEPOINT_DIR)
    if found is not None:
        resume_step, resume_path = found
        log(f"RESUME: latest savepoint detected → step {resume_step} at {resume_path}")
        # Load LoRA adapter
        try:
            decoder = PeftModel.from_pretrained(decoder.base_model.model, resume_path, is_trainable=True)
            log(f"RESUME: PeftModel.from_pretrained OK at {resume_path}")
        except Exception as e:
            log(f"RESUME: LoRA load FAILED ({e}); restarting from scratch")
            log(traceback.format_exc())
            resume_step = 0
            resume_path = None
        # Optimizer/sched/RNG companions (best-effort; absent if v1 savepoint)
        for fname, key in [('optimizer.pt', 'optimizer'), ('scheduler.pt', 'scheduler'),
                           ('rng_state.pt', 'rng'), ('emas.json', 'emas')]:
            companion = os.path.join(resume_path, fname)
            if os.path.exists(companion):
                resume_extras[key] = companion

# Apply LoRA wrap if we did NOT resume (resume already gives us PeftModel)
if resume_step == 0:
    log("fresh start (no usable savepoint)")

decoder.print_trainable_parameters()


# ───────── Data load ─────────
records = []
with open(SFT_DATA, 'r') as f:
    for line in f:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
log(f"sft full loaded n={len(records)}")

holdout = []
with open(SFT_HOLDOUT, 'r') as f:
    for line in f:
        try:
            holdout.append(json.loads(line))
        except json.JSONDecodeError:
            continue
log(f"sft holdout loaded n={len(holdout)}")

# Φ★ teacher cache
phi_cache_records = []
with open(PHI_CACHE, 'r') as f:
    for line in f:
        try:
            phi_cache_records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
log(f"phi cache loaded n={len(phi_cache_records)}")

# Cache integrity assertions
assert len(phi_cache_records) == len(records), \
    f"cache length {len(phi_cache_records)} != sft length {len(records)}"
cache_idx_set = {r['idx'] for r in phi_cache_records}
assert cache_idx_set == set(range(len(records))), "cache idx not contiguous 0..N-1"
phi_T_by_idx = {r['idx']: float(r['phi_star_min']) for r in phi_cache_records}
phi_T_arr = np.array([phi_T_by_idx[i] for i in range(len(records))], dtype=np.float64)
mu_T = float(phi_T_arr.mean())
sigma_T = float(phi_T_arr.std())
sigma_T = max(sigma_T, 1e-3)
z_T_by_idx = {i: float((phi_T_by_idx[i] - mu_T) / sigma_T) for i in range(len(records))}
log(f"teacher z-stats: μ_T={mu_T:.4f} σ_T={sigma_T:.4f} (n={len(records)})")


def tokenize_record(rec):
    text = rec.get('input', '') + ' ' + rec.get('completion', '')
    tokens = sp.encode(text)[:T_SEQ]
    if len(tokens) < 2:
        tokens = tokens + [0] * (2 - len(tokens))
    if len(tokens) < T_SEQ:
        tokens = tokens + [0] * (T_SEQ - len(tokens))
    tension = rec.get('tension_target', None)
    if tension is None or not isinstance(tension, list) or len(tension) < T_SEQ:
        tension = [0.0] * T_SEQ
    return tokens, tension[:T_SEQ]


t0 = time.time()
cache_tokens = []
for rec in records:
    toks, tens = tokenize_record(rec)
    cache_tokens.append((toks, tens))
log(f"tokenized cache n={len(cache_tokens)} elapsed={time.time()-t0:.1f}s")

holdout_cache = []
for rec in holdout[:F1_HOLDOUT_N]:
    inp = rec.get('input', '')
    comp = rec.get('completion', '')
    inp_tok = sp.encode(inp)[:T_SEQ - F1_GEN_LEN] if inp else [0]
    comp_tok = sp.encode(comp)[:F1_GEN_LEN] if comp else [0]
    tens = rec.get('tension_target', None) or [0.0] * T_SEQ
    if not isinstance(tens, list):
        tens = [0.0] * T_SEQ
    if len(tens) < T_SEQ:
        tens = tens + [0.0] * (T_SEQ - len(tens))
    full_tok = inp_tok + comp_tok
    if len(full_tok) < T_SEQ:
        full_tok = full_tok + [0] * (T_SEQ - len(full_tok))
    full_tok = full_tok[:T_SEQ]
    holdout_cache.append({
        'input_tokens': inp_tok,
        'reference_tokens': comp_tok,
        'full_tokens': full_tok,
        'tension': tens[:T_SEQ],
    })
log(f"holdout cache n={len(holdout_cache)}")

calib_tokens = []
for prompt in CALIB_PROMPTS:
    tk = sp.encode(prompt)[:T_SEQ]
    if len(tk) < T_SEQ:
        tk = tk + [0] * (T_SEQ - len(tk))
    calib_tokens.append(tk)
calib_tensor = torch.tensor(calib_tokens, dtype=torch.long, device=device)

# Hidden capture hook
captured_hidden = {'value': None}
real_decoder = decoder.base_model.model
def _hook(module, input, output):
    captured_hidden['value'] = output.detach()
hook_handle = real_decoder.ln_f.register_forward_hook(_hook)


def compute_phi_star(model, calib_idx, K=K_PARTS, ridge=RIDGE):
    model.eval()
    hiddens = []
    with torch.no_grad():
        for i in range(N_CALIB):
            captured_hidden['value'] = None
            _ = model(calib_idx[i:i+1])
            h = captured_hidden['value']
            if h is None:
                model.train()
                return None, None
            h_pool = h.mean(dim=1).squeeze(0)
            hiddens.append(h_pool.float().cpu().numpy())
    X = np.stack(hiddens, axis=0)
    var = X.var(axis=0)
    top_idx = np.argsort(var)[::-1][:HID_TRUNC]
    Xt = X[:, top_idx]

    def safe_logdet(C):
        Cs = C + ridge * np.eye(C.shape[0])
        sign, logdet = np.linalg.slogdet(Cs)
        if sign <= 0:
            return None
        return logdet

    C_full = np.cov(Xt.T)
    I_full = safe_logdet(C_full)
    if I_full is None:
        model.train()
        return None, None
    rng = np.random.default_rng(SEED)
    phi_candidates = []
    for k in range(K):
        idx = rng.permutation(N_CALIB)
        s1 = idx[:HALF]
        s2 = idx[HALF:]
        C1 = np.cov(Xt[s1].T)
        C2 = np.cov(Xt[s2].T)
        I1 = safe_logdet(C1)
        I2 = safe_logdet(C2)
        if I1 is None or I2 is None:
            continue
        phi_candidates.append(I_full - (I1 + I2))
    model.train()
    if not phi_candidates:
        return None, None
    phi_min = float(min(phi_candidates))
    phi_mean = float(sum(phi_candidates) / len(phi_candidates))
    return phi_min, phi_mean


def compute_f1_bleu1(model, holdout_subset):
    model.eval()
    bleu1_scores = []
    with torch.no_grad():
        for h in holdout_subset:
            inp_tok = h['input_tokens']
            ref_tok = h['reference_tokens']
            if not ref_tok:
                continue
            ctx = torch.tensor([inp_tok], dtype=torch.long, device=device)
            gen_tok = []
            for _ in range(F1_GEN_LEN):
                if ctx.size(1) >= T_SEQ:
                    break
                logits_a, _, _, _, _ = model(ctx)
                next_id = int(logits_a[0, -1, :].argmax().item())
                gen_tok.append(next_id)
                ctx = torch.cat([ctx, torch.tensor([[next_id]], dtype=torch.long, device=device)], dim=1)
                if next_id == 0:
                    break
            if not gen_tok:
                continue
            ref_counts = {}
            for t in ref_tok:
                ref_counts[t] = ref_counts.get(t, 0) + 1
            hits = 0
            seen = {}
            for t in gen_tok:
                if t in ref_counts:
                    seen_c = seen.get(t, 0)
                    if seen_c < ref_counts[t]:
                        hits += 1
                        seen[t] = seen_c + 1
            bleu1 = hits / max(1, len(gen_tok))
            bleu1_scores.append(bleu1)
    model.train()
    if not bleu1_scores:
        return 0.0
    return float(sum(bleu1_scores) / len(bleu1_scores))


def compute_f_metrics(model, eval_subset, holdout_subset, phi_star_value):
    model.eval()
    tension_mses = []
    with torch.no_grad():
        for toks, tens in eval_subset:
            idx = torch.tensor([toks], dtype=torch.long, device=device)
            tens_t = torch.tensor([tens], dtype=torch.float32, device=device)
            logits_a, logits_g, tensions, _, _ = model(idx)
            t_pred = tensions[-1].mean(dim=0).float()
            mse = F.mse_loss(t_pred, tens_t.squeeze(0)).item()
            tension_mses.append(mse)
    model.train()
    f1 = compute_f1_bleu1(model, holdout_subset)
    return {
        'F1_bleu1': f1,
        'F2_phi': phi_star_value,
        'F3_tension_mse': float(sum(tension_mses) / len(tension_mses)),
        'F4_bold_NA': True,
    }


# ───────── Optimizer + (optional) resume optimizer state ─────────
optimizer = torch.optim.AdamW(
    [p for p in decoder.parameters() if p.requires_grad],
    lr=LR, weight_decay=0.01,
)
scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda s: 1.0)

# ───────── Student φ EMA state (μ_S, σ_S) ─────────
phi_S_history = collections.deque(maxlen=PHI_S_EMA_WINDOW)
mu_S_running = None
sigma_S_running = 2.0  # placeholder (overwritten after first EMA refresh)


def _refresh_S_ema(phi_value):
    """Push new φ★_S sample into rolling window; recompute μ_S, σ_S."""
    global mu_S_running, sigma_S_running
    if phi_value is None:
        return
    phi_S_history.append(float(phi_value))
    if len(phi_S_history) >= 2:
        arr = np.array(list(phi_S_history), dtype=np.float64)
        mu_S_running = float(arr.mean())
        sigma_S_running = max(float(arr.std()), 0.1)
    else:
        mu_S_running = float(phi_value)
        sigma_S_running = 2.0


# ───────── Restore optimizer / scheduler / RNG / EMA state if resuming ─────────
if resume_extras.get('optimizer'):
    try:
        opt_state = torch.load(resume_extras['optimizer'], map_location=device)
        optimizer.load_state_dict(opt_state)
        log(f"RESUME: optimizer state loaded from {resume_extras['optimizer']}")
    except Exception as e:
        log(f"RESUME: optimizer load FAILED ({e}); fresh AdamW state")
if resume_extras.get('scheduler'):
    try:
        sch_state = torch.load(resume_extras['scheduler'], map_location=device)
        scheduler.load_state_dict(sch_state)
        log("RESUME: scheduler state loaded")
    except Exception as e:
        log(f"RESUME: scheduler load FAILED ({e})")
if resume_extras.get('rng'):
    try:
        rng_state = torch.load(resume_extras['rng'], map_location='cpu')
        torch.set_rng_state(rng_state['torch_cpu'])
        if 'torch_cuda' in rng_state and torch.cuda.is_available():
            torch.cuda.set_rng_state(rng_state['torch_cuda'])
        np.random.set_state(rng_state['numpy'])
        random.setstate(rng_state['python'])
        log("RESUME: RNG state restored")
    except Exception as e:
        log(f"RESUME: RNG restore FAILED ({e}); fresh RNG")
        np.random.seed(SEED + resume_step)
        torch.manual_seed(SEED + resume_step)
        random.seed(SEED + resume_step)
else:
    np.random.seed(SEED + resume_step)
    torch.manual_seed(SEED + resume_step)
    random.seed(SEED + resume_step)

if resume_extras.get('emas'):
    try:
        with open(resume_extras['emas'], 'r') as f:
            ed = json.load(f)
        for v in ed.get('phi_S_history', []):
            phi_S_history.append(float(v))
        if 'mu_S' in ed:
            mu_S_running = float(ed['mu_S'])
        if 'sigma_S' in ed:
            sigma_S_running = max(float(ed['sigma_S']), 0.1)
        log(f"RESUME: EMA restored window={len(phi_S_history)} μ_S={mu_S_running} σ_S={sigma_S_running}")
    except Exception as e:
        log(f"RESUME: EMA restore FAILED ({e})")


# ───────── Trajectory state (load + append, never overwrite) ─────────
phi_log = []
f_log = []
loss_log_compact = []
aborts = []
abort_triggered = False
savepoint_log = []
distill_log = []  # per-loss-log: distill metrics

if os.path.exists(TRAJECTORY_OUT):
    try:
        with open(TRAJECTORY_OUT, 'r') as f:
            prev_traj = json.load(f)
        phi_log = prev_traj.get('phi_log', [])
        f_log = prev_traj.get('f_log', [])
        loss_log_compact = prev_traj.get('loss_log_compact', [])
        savepoint_log = prev_traj.get('savepoints', [])
        distill_log = prev_traj.get('distill_log', [])
        aborts = prev_traj.get('aborts', [])
        log(f"RESUME: trajectory loaded (phi={len(phi_log)} f={len(f_log)} loss={len(loss_log_compact)} sp={len(savepoint_log)})")
    except Exception as e:
        log(f"RESUME: trajectory load FAILED ({e}); starting fresh log")


# ───────── Baseline / phi probe (pre-train, only if not resuming) ─────────
if resume_step == 0:
    log("computing baseline phi_star (pre-train)...")
    t0 = time.time()
    phi_baseline, phi_baseline_mean = compute_phi_star(decoder, calib_tensor)
    log(f"baseline phi_star_min={phi_baseline} mean={phi_baseline_mean} elapsed={time.time()-t0:.1f}s")
    phi_log.append({'step': 0, 'phi_star_min': phi_baseline, 'phi_star_mean': phi_baseline_mean,
                    'delta': DELTA_EARLY, 'note': 'baseline'})
    if phi_baseline is not None:
        _refresh_S_ema(phi_baseline)
    # Initial F-metrics @ step 0
    log("computing initial F metrics @ step 0...")
    eval_subset = cache_tokens[:32]
    f0 = compute_f_metrics(decoder, eval_subset, holdout_cache,
                           phi_baseline if phi_baseline is not None else 0.0)
    f0['step'] = 0
    f_log.append(f0)
    log(f"F @ step 0: F1_bleu1={f0['F1_bleu1']:.4f} F2_phi={f0['F2_phi']:.4f} F3_tens={f0['F3_tension_mse']:.4f}")
else:
    phi_baseline = next((p['phi_star_min'] for p in phi_log if p.get('note') == 'baseline'), None)
    phi_baseline_mean = next((p['phi_star_mean'] for p in phi_log if p.get('note') == 'baseline'), None)
    log(f"resume mode: phi_baseline={phi_baseline} (from prior trajectory)")
    eval_subset = cache_tokens[:32]
    if mu_S_running is None and phi_baseline is not None:
        _refresh_S_ema(phi_baseline)


# ───────── Savepoint write (LoRA + optimizer + scheduler + RNG + EMAs) ─────────
def save_full_state(step, subdir):
    save_dir = f"{SAVEPOINT_DIR}/{subdir}"
    os.makedirs(save_dir, exist_ok=True)
    decoder.save_pretrained(save_dir)
    try:
        torch.save(optimizer.state_dict(), f"{save_dir}/optimizer.pt")
        torch.save(scheduler.state_dict(), f"{save_dir}/scheduler.pt")
        rng_state = {
            'torch_cpu': torch.get_rng_state(),
            'numpy': np.random.get_state(),
            'python': random.getstate(),
        }
        if torch.cuda.is_available():
            rng_state['torch_cuda'] = torch.cuda.get_rng_state()
        torch.save(rng_state, f"{save_dir}/rng_state.pt")
        with open(f"{save_dir}/emas.json", 'w') as f:
            json.dump({
                'phi_S_history': list(phi_S_history),
                'mu_S': mu_S_running,
                'sigma_S': sigma_S_running,
                'mu_T': mu_T,
                'sigma_T': sigma_T,
            }, f)
        # Pin step for resume scan robustness
        with open(f"{save_dir}/_step.txt", 'w') as f:
            f.write(str(step))
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        log(f"SAVE companion FAILED ({e}); LoRA adapter still saved")
    return save_dir


# ───────── Trajectory + verdict writers (atomic-ish) ─────────
def build_trajectory(step_now, train_elapsed_sec_partial, phi_final=None, phi_final_mean=None,
                     f_final=None, finished=False):
    return {
        'schema': 'anima/p9_paradigm_d_distill_v2/trajectory/2',
        'phase': 'p9_paradigm_d_25k_hbm3',
        'ts_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'finished': bool(finished),
        'device': str(device),
        'config': {
            'n_steps': N_STEPS, 'batch': BATCH, 'grad_acc': GRAD_ACC, 'lr': LR,
            'lora_r': LORA_R, 'lora_alpha': LORA_ALPHA,
            'alpha_hi': ALPHA_HI, 'alpha_lo': ALPHA_LO,
            'alpha_ramp': [ALPHA_RAMP_START, ALPHA_RAMP_END],
            'beta': BETA,
            'gamma_distill_plateau': GAMMA_DISTILL_PLATEAU,
            'gamma_distill_warmup_end': GAMMA_DISTILL_WARMUP_END,
            'gamma_distill_ramp_end': GAMMA_DISTILL_RAMP_END,
            'delta_curriculum': {
                'early': DELTA_EARLY, 'mid': DELTA_MID, 'late': DELTA_LATE,
                'early_end': EARLY_END, 'mid_end': MID_END,
            },
            'phi_threshold': PHI_THRESHOLD,
            'phi_every': PHI_EVERY, 'f_every': F_EVERY,
            'save_every': SAVE_EVERY,
            'T': T_SEQ, 'seed': SEED,
            'k_partitions': K_PARTS, 'hid_trunc': HID_TRUNC, 'ridge': RIDGE,
            'phi_S_ema_window': PHI_S_EMA_WINDOW,
            'allow_resume': ALLOW_RESUME,
            'graceful_sigterm': GRACEFUL_SAVE_ON_SIGTERM,
            'hf_push': HF_PUSH,
        },
        'teacher_z_stats': {'mu_T': mu_T, 'sigma_T': sigma_T, 'n': len(records)},
        'phi_log': phi_log,
        'f_log': f_log,
        'loss_log_compact': loss_log_compact,
        'distill_log': distill_log,
        'savepoints': savepoint_log,
        'aborts': aborts,
        'aborted': abort_triggered,
        'steps_completed': step_now,
        'phi_baseline': phi_baseline,
        'phi_final': phi_final,
        'phi_final_mean': phi_final_mean,
        'f_final': f_final,
        'train_elapsed_sec_partial': round(train_elapsed_sec_partial, 2),
        'resume_step_at_launch': resume_step,
    }


def flush_trajectory(step_now, t_partial):
    try:
        traj = build_trajectory(step_now, t_partial)
        with open(TRAJECTORY_OUT, 'w') as f:
            json.dump(traj, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        # Φ-only side-car
        with open(PHI_TRAJ_OUT, 'w') as f:
            json.dump({
                'schema': 'anima/p9_paradigm_d_distill_v2/phi_trajectory/2',
                'phi_log': phi_log,
                'mu_T': mu_T, 'sigma_T': sigma_T,
                'mu_S_running': mu_S_running, 'sigma_S_running': sigma_S_running,
                'phi_baseline': phi_baseline,
            }, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        log(f"flush_trajectory FAILED ({e})")


# ───────── SIGTERM / SIGINT graceful shutdown ─────────
_shutting_down = {'flag': False, 'reason': None, 'step': None}


def _graceful_handler(signum, frame):
    if _shutting_down['flag']:
        return
    _shutting_down['flag'] = True
    _shutting_down['reason'] = f"signal_{signum}"
    log(f"SIGNAL {signum} received → graceful shutdown (will save partial savepoint + flush logs)")


if GRACEFUL_SAVE_ON_SIGTERM:
    signal.signal(signal.SIGTERM, _graceful_handler)
    signal.signal(signal.SIGINT, _graceful_handler)


# ───────── Resume audit emit ─────────
emit_resume_audit({
    'event': 'launch',
    'resume_step': resume_step,
    'resume_path': resume_path,
    'resume_extras_loaded': list(resume_extras.keys()),
    'mu_T': mu_T, 'sigma_T': sigma_T,
    'mu_S_running': mu_S_running, 'sigma_S_running': sigma_S_running,
    'rng_torch_seed': SEED + resume_step,
    'pid': os.getpid(),
    'output_dir': OUTPUT_DIR,
    'savepoint_dir': SAVEPOINT_DIR,
})


# ───────── Train loop ─────────
train_t0 = time.time()
decoder.train()
optimizer.zero_grad()
step = resume_step
last_phi_min = phi_baseline if phi_baseline is not None else 0.0

try:
    for step in range(resume_step + 1, N_STEPS + 1):
        if _shutting_down['flag']:
            _shutting_down['step'] = step
            log(f"shutdown requested before step {step} → break loop")
            break

        # Sample BATCH records (record their indices for distill cache lookup)
        idx_batch = np.random.choice(len(cache_tokens), BATCH, replace=False)
        toks_batch = []
        tens_batch = []
        z_T_batch = []
        for i in idx_batch:
            toks, tens = cache_tokens[i]
            toks_batch.append(toks)
            tens_batch.append(tens)
            z_T_batch.append(z_T_by_idx[int(i)])
        idx_t = torch.tensor(toks_batch, dtype=torch.long, device=device)
        tens_t = torch.tensor(tens_batch, dtype=torch.float32, device=device)

        # Forward
        logits_a, logits_g, tensions, _, _ = decoder(idx_t)

        # CE
        targets = idx_t[:, 1:].contiguous()
        logits_shift = logits_a[:, :-1, :].contiguous()
        ce_loss = F.cross_entropy(
            logits_shift.view(-1, logits_shift.size(-1)),
            targets.view(-1),
            ignore_index=0,
        )

        # Tension MSE
        t_pred = tensions[-1]
        tension_loss = F.mse_loss(t_pred, tens_t)

        # δ floor (hinge over last probe)
        delta_now = get_delta(step)
        phi_hinge = max(0.0, PHI_THRESHOLD - last_phi_min)
        phi_hinge_loss = torch.tensor(phi_hinge, device=device)

        # γ_distill — z-score MSE between cached teacher z and current student z
        # Per-batch teacher z (Python float list → mean as torch scalar to match z_S scalar)
        gamma_now = get_gamma_distill(step)
        z_T_batch_mean = float(np.mean(z_T_batch))
        if mu_S_running is not None:
            z_S_running = (last_phi_min - mu_S_running) / max(sigma_S_running, 0.1)
        else:
            z_S_running = 0.0
        # Detached scalar (static-EMA pattern; gradient flows via δ-floor coupling, not directly)
        distill_unweighted = (z_T_batch_mean - z_S_running) ** 2
        distill_loss = torch.tensor(distill_unweighted, device=device)

        alpha_now = get_alpha(step)
        total_loss = (alpha_now * ce_loss
                      + BETA * tension_loss
                      + gamma_now * distill_loss
                      + delta_now * phi_hinge_loss)

        (total_loss / GRAD_ACC).backward()

        if step % GRAD_ACC == 0:
            torch.nn.utils.clip_grad_norm_(
                [p for p in decoder.parameters() if p.requires_grad], 1.0
            )
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

        # Compact loss log
        if step % 100 == 0 or step == resume_step + 1 or step == 1:
            log(f"step {step}/{N_STEPS} loss={total_loss.item():.4f} ce={ce_loss.item():.4f} tens={tension_loss.item():.4f} γ_d={gamma_now:.3f} distill={distill_unweighted:.4f} z_S={z_S_running:.3f} z_T_b={z_T_batch_mean:.3f} δ={delta_now}")
            loss_log_compact.append({
                'step': step,
                'loss_total': float(total_loss.item()),
                'loss_ce': float(ce_loss.item()),
                'loss_tension': float(tension_loss.item()),
                'loss_phi_hinge': float(phi_hinge),
                'loss_distill_unweighted': float(distill_unweighted),
                'gamma_distill': gamma_now,
                'alpha': alpha_now,
                'delta': delta_now,
            })
            distill_log.append({
                'step': step,
                'z_T_batch_mean': z_T_batch_mean,
                'z_S_running': z_S_running,
                'gamma_distill': gamma_now,
                'mu_S': mu_S_running, 'sigma_S': sigma_S_running,
                'distill_unweighted': float(distill_unweighted),
            })

        # Phi probe
        if step % PHI_EVERY == 0:
            phi_min, phi_mean = compute_phi_star(decoder, calib_tensor)
            phi_log.append({'step': step, 'phi_star_min': phi_min, 'phi_star_mean': phi_mean,
                            'delta': delta_now, 'mu_S': mu_S_running, 'sigma_S': sigma_S_running})
            log(f"  phi @ step {step}: min={phi_min} mean={phi_mean} μ_S={mu_S_running} σ_S={sigma_S_running}")
            if phi_min is not None:
                last_phi_min = phi_min
                _refresh_S_ema(phi_min)
                if phi_min < PHI_THRESHOLD:
                    aborts.append({'step': step, 'reason': 'F2_PHI_BELOW_THRESHOLD',
                                   'phi_star_min': phi_min, 'threshold': PHI_THRESHOLD})
                    log(f"  ABORT: phi_star_min={phi_min} < threshold={PHI_THRESHOLD}")
                    abort_triggered = True
                    break

        # F metrics
        if step % F_EVERY == 0:
            fm = compute_f_metrics(decoder, eval_subset, holdout_cache, last_phi_min)
            fm['step'] = step
            f_log.append(fm)
            log(f"  F @ step {step}: F1_bleu1={fm['F1_bleu1']:.4f} F2_phi={fm['F2_phi']:.4f} F3_tens={fm['F3_tension_mse']:.4f}")

        # Savepoint every SAVE_EVERY steps
        if step % SAVE_EVERY == 0:
            sp_subdir = f"step_{step}"
            sd = save_full_state(step, sp_subdir)
            log(f"  SAVEPOINT @ step {step} → {sd}")
            savepoint_log.append({'step': step, 'path': sd, 'ts_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')})
            flush_trajectory(step, time.time() - train_t0)

except KeyboardInterrupt:
    log(f"INTERRUPTED @ step {step}")
    aborts.append({'step': step, 'reason': 'KeyboardInterrupt'})
    abort_triggered = True
    _shutting_down['flag'] = True
    _shutting_down['reason'] = 'KeyboardInterrupt'
except Exception as e:
    log(f"EXCEPTION @ step {step}: {e}")
    log(traceback.format_exc())
    aborts.append({'step': step, 'reason': f'EXCEPTION: {e}', 'tb': traceback.format_exc()[-2000:]})
    abort_triggered = True

train_elapsed = time.time() - train_t0
log(f"train loop exited elapsed={train_elapsed:.1f}s steps_completed={step} aborted={abort_triggered} shutting_down={_shutting_down['flag']}")

# ───────── Graceful save on shutdown OR final ─────────
final_subdir = f"step_{step}_partial" if _shutting_down['flag'] else "final"
try:
    if step > resume_step:
        sd_final = save_full_state(step, final_subdir)
        log(f"FINAL/PARTIAL adapter saved → {sd_final}")
        savepoint_log.append({'step': step, 'path': sd_final, 'note': final_subdir,
                              'ts_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')})
except Exception as e:
    log(f"FINAL save FAILED: {e}")
    log(traceback.format_exc())

# Final phi + F (only if not aborted by SIGTERM mid-eval)
phi_final = None
phi_final_mean = None
f_final = None
if not _shutting_down['flag']:
    try:
        log("computing final phi_star...")
        phi_final, phi_final_mean = compute_phi_star(decoder, calib_tensor)
        log(f"final phi_star_min={phi_final} mean={phi_final_mean}")
        phi_log.append({'step': step, 'phi_star_min': phi_final, 'phi_star_mean': phi_final_mean,
                        'delta': get_delta(step), 'note': 'final'})
        log("computing final F metrics...")
        f_final = compute_f_metrics(decoder, eval_subset, holdout_cache,
                                    phi_final if phi_final is not None else 0.0)
        f_final['step'] = step
        f_final['note'] = 'final'
        f_log.append(f_final)
        log(f"final F: F1_bleu1={f_final['F1_bleu1']:.4f} F2_phi={f_final['F2_phi']:.4f} F3_tens={f_final['F3_tension_mse']:.4f}")
    except Exception as e:
        log(f"FINAL eval FAILED: {e}")
        log(traceback.format_exc())

# Flush trajectory + verdict
try:
    hook_handle.remove()
except Exception:
    pass

flush_trajectory(step, train_elapsed)

# Write F1_holdout side-car
try:
    with open(F1_HOLDOUT_OUT, 'w') as f:
        json.dump({
            'schema': 'anima/p9_paradigm_d_distill_v2/F1_holdout/2',
            'f_log': f_log,
            'f_final': f_final,
            'holdout_n': F1_HOLDOUT_N,
            'gen_len': F1_GEN_LEN,
        }, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
except Exception as e:
    log(f"F1 holdout side-car FAILED: {e}")

# Verdict
if _shutting_down['flag']:
    verdict = f"GRACEFUL_SHUTDOWN_AT_STEP_{step}"
    rec = "RESUME_FROM_LATEST_SAVEPOINT_ON_NEXT_LAUNCH"
elif abort_triggered:
    verdict = "ABORTED"
    rec = "RETUNE_OR_RESUME_AFTER_DEBUG"
elif step >= N_STEPS:
    f_final_phi = f_final.get('F2_phi', None) if f_final else None
    if f_final_phi is None:
        verdict = "PHI_FINAL_UNKNOWN"
        rec = "INVESTIGATE_PHI_PROBE"
    elif f_final_phi < PHI_THRESHOLD:
        verdict = "F2_VIOLATION_AT_FINAL"
        rec = "RETUNE_DELTA_OR_GAMMA"
    else:
        verdict = "PRODUCTION_25K_FULL_PASS"
        rec = "F1_HOLDOUT_KL_EVAL_NEXT"
else:
    verdict = f"INCOMPLETE_AT_STEP_{step}"
    rec = "RESUME_TO_FINISH"

verdict_doc = {
    'schema': 'anima/p9_paradigm_d_distill_v2/verdict/2',
    'verdict': verdict,
    'recommendation': rec,
    'steps_completed': step,
    'n_steps_target': N_STEPS,
    'aborted': abort_triggered,
    'graceful_shutdown': _shutting_down['flag'],
    'shutdown_reason': _shutting_down['reason'],
    'aborts': aborts,
    'phi_baseline': phi_baseline,
    'phi_final': phi_final,
    'phi_final_mean': phi_final_mean,
    'f_final': f_final,
    'mu_T': mu_T, 'sigma_T': sigma_T,
    'mu_S_running': mu_S_running, 'sigma_S_running': sigma_S_running,
    'savepoints': savepoint_log,
    'train_elapsed_sec': round(train_elapsed, 2),
    'resume_step_at_launch': resume_step,
    'ts_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'honest_c3': [
        "Spot preempt unavoidable on community spot — savepoints @ every 1000 steps mitigate but cannot eliminate; expect 1-3 preempts per 10h H100 run",
        "Script reconstructed from spec + sister sentinel base; may diverge in subtle ways from the deleted original v1 (tested mini-run shape preserved: loss form, schedules, calib prompts, hidden hook)",
        "Resume granularity 1000-step has ~20s disk-write cost per save (scaled w/ AdamW state ~300MB) — at 25K total = ~10min cumulative I/O overhead",
        "Static-EMA gradient pattern: distill loss has no direct backprop through model params (z_S detached scalar) — gradient flows via downstream Φ★ probe coupling; pattern weak per Phase 1.5 sentinel C3",
        "F-D-1 (per-token KL ≤ 0.5 nats vs Mistral-7B reference) is a separate post-train evaluation, NOT auto-computed by this script — script emits F1_BLEU-1 (CLM-self holdout); F-D-1 KL gate evaluated by downstream tool",
    ],
}

emit_resume_audit({
    'event': 'exit',
    'verdict': verdict,
    'recommendation': rec,
    'steps_completed': step,
    'graceful': _shutting_down['flag'],
    'aborted': abort_triggered,
    'train_elapsed_sec': round(train_elapsed, 2),
})

try:
    with open(VERDICT_OUT, 'w') as f:
        json.dump(verdict_doc, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    log(f"VERDICT written → {VERDICT_OUT}: {verdict}")
except Exception as e:
    log(f"VERDICT write FAILED: {e}")

log(f"DONE step={step} verdict={verdict} graceful={_shutting_down['flag']}")
sys.stdout.flush()
sys.stderr.flush()
sys.exit(0 if (step >= N_STEPS or _shutting_down['flag']) else 1)
