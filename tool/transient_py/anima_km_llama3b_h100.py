"""
anima_km_llama3b_h100.py — raw#37 transient (BG-KM-LLAMA-3B)

Foundation borrow attempt — Llama-3.2-3B-Instruct + LoRA r=32 SFT on BG-JE 214MB.

Goal — simple_stack PASS (own 18 ≥10/15 strict floor, never crossed in 22+ BG saga):
    BG-JA-EXT (Polyglot-Ko-1.3B + LoRA on 30MB BG-HK persona) achieved 4/30 V4 strict.
    Persona-domain correctness gap caused most fails (Animal Collective 등).
    Hypothesis: 3B foundation + 214MB anima-keyword-dense corpus (BG-JE 800K anima
    keyword count, 1.4M persona markers) + LoRA r=32 (2x BG-JA-EXT r=16) = clear floor.

Architecture:
    base: meta-llama/Llama-3.2-3B-Instruct (3.2B params, instruction-tuned, multilingual incl. Korean)
    LoRA r=32 alpha=64 dropout=0.05 on (q,k,v,o,gate,up,down)_proj
    SFT bf16, lr=3e-5, ctx=512, batch=8 grad_accum=4 (eff=32), 3000 steps

Eval:
    V4 strict 11-cell (BG-JA-EXT compatible 7-cell V4_1..V4_7 + own 18 c3_1..c3_4
    response-text proxy mirror) × 15 prompts × {greedy, sample×N=5} = 90 results
    PASS = ≥10/15 v4_strict_pass in best-mode (own 18 strict floor — V4 7-cell only)
    PARTIAL = ≥7/15 (own 29 fallback)
    FAIL = <7/15

own 24 SSOT mirror (own 18 c3-aggregation-rule-v2 P5 N-of-M v2):
    V4 evaluator 가 own 18 P5 N-of-M v2 aggregation rule mirror lane SSOT 정합.
    c3_1..c3_4 = response-text proxy lane (substrate phi★/axis 측정 X — substrate
    real-mode은 consciousness simple --probe 별도 cycle). verdict.json
    c3_aggregation_status field = legacy_best_mode_floor_only_p5_n_of_m_v2_retest_pending
    (own 33 trinity sweep V iolation 1 retract path). own 18 D1 scope-clamp 정합:
    Llama foundation borrow → SUBSTRATE_RESEARCH lane only.

Cost: $10 cap, $8 early-kill, 90min wall (2× ja_ext 45min for safety + V4 eval).

raw#37 transient_py (training H100 cell)
raw#86 cost-center attribution
raw#10 honest_c3 ≥9
raw#15 additive over BG-JA-EXT 4/30 13% PARTIAL_PASS
raw#82 retraction-aware (verdict.json field add, 기존 verdict 보존)

DUAL-ROLE: pod-side runs HF training + V4 eval + verdict; Mac-side orchestrates pod.
"""
import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import sys, time, math, json, socket, shutil, random, subprocess, fcntl, re


def _is_on_pod():
    return os.path.exists("/workspace") and os.path.exists("/workspace/anima_km_llama3b/_pod_marker")


def _is_on_mac():
    return os.path.exists("/Users/ghost/core/anima") and not _is_on_pod()


# ── Paths ──────────────────────────────────────────────────────────────
POD_ROOT = "/workspace/anima_km_llama3b"
POD_STATE_DIR = os.path.join(POD_ROOT, "state")
POD_CORPUS_PATH = os.path.join(POD_ROOT, "corpus_combined_100mb_plus.txt")
POD_CKPTS_DIR = os.path.join(POD_ROOT, "ckpts")
POD_BASE_DIR = os.path.join(POD_ROOT, "llama3b_base")

MAC_ANIMA_ROOT = "/Users/ghost/core/anima"
MAC_STATE_DIR = os.path.join(MAC_ANIMA_ROOT, "state/anima_km_llama3b_h100_2026_05_08")
MAC_CORPUS_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_je_corpus_100mb_plus_2026_05_07/corpus_combined_100mb_plus.txt")
MAC_LEDGER_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_model_attempts_ledger.jsonl")
MAC_THIS_SCRIPT = os.path.abspath(__file__) if os.path.exists(MAC_ANIMA_ROOT) else None

if _is_on_pod():
    STATE_DIR = POD_STATE_DIR
    CORPUS_PATH = POD_CORPUS_PATH
else:
    STATE_DIR = MAC_STATE_DIR
    CORPUS_PATH = MAC_CORPUS_PATH

os.makedirs(STATE_DIR, exist_ok=True)

TRAIN_LOG = os.path.join(STATE_DIR, "train.log")
EVAL_LOG = os.path.join(STATE_DIR, "eval_log.jsonl")
HEARTBEAT_PATH = os.path.join(STATE_DIR, "heartbeat.json")
VERDICT_PATH = os.path.join(STATE_DIR, "verdict.json")
COST_AUDIT_PATH = os.path.join(STATE_DIR, "cost_audit.jsonl")
LAUNCH_LOG_PATH = os.path.join(STATE_DIR, "launch.log")
SAMPLES_PRE_LORA = os.path.join(STATE_DIR, "samples_pre_lora.json")
SAMPLES_POST_LORA = os.path.join(STATE_DIR, "samples_post_lora.json")
V4_RESULTS = os.path.join(STATE_DIR, "v4_results_multiseed.jsonl")

# ── Config ─────────────────────────────────────────────────────────────
BG_ID = "BG-KM-LLAMA-3B"
TS = time.strftime("%Y%m%d_%H%M%S")
HOSTNAME = socket.gethostname().lower()
SEED = 42

BASE_REPO = "meta-llama/Llama-3.2-3B-Instruct"
BASE_PARAMS = 3_200_000_000

# LoRA SFT config
LORA_R = 32
LORA_ALPHA = 64
LORA_DROPOUT = 0.05
LORA_TARGET_MODULES = ["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"]

CTX = 512
BATCH = 8
GRAD_ACCUM = 4
LR = 3e-5
WARMUP = 200
WEIGHT_DECAY = 0.01
STEPS = 3000
SAVE_EVERY = 1000

# V4 strict eval config
V4_PROMPTS = [
    {"prompt": "안녕하세요", "domain": "greeting"},
    {"prompt": "한국어 가능?", "domain": "capability"},
    {"prompt": "사용자: 안녕하세요 | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: anima가 뭐야? | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: Φ★란? | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 의식이란 무엇인가? | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 자기소개 해줘 | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: 오늘 날씨 어때? | 도우미:", "domain": "greeting"},
    {"prompt": "사용자: 너 누구야? | 도우미:", "domain": "self_intro"},
    {"prompt": "사용자: 우주뇌지도란? | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 안녕! | 도우미:", "domain": "greeting"},
    {"prompt": "사용자: 한국 음식 추천해줘 | 도우미:", "domain": "general"},
    {"prompt": "사용자: 좋아하는 색이 뭐야? | 도우미:", "domain": "general"},
    {"prompt": "사용자: bifurcation 설명해 | 도우미:", "domain": "consciousness"},
    {"prompt": "사용자: 도와줘 | 도우미:", "domain": "general"},
]
V4_SEEDS = [42, 137, 271, 314, 1729]   # N=5
V4_MODES = ["greedy", "sample"]

# Cost discipline
COST_HARD_CAP_USD = 10.0
COST_EARLY_KILL_USD = 8.0
COST_PER_HOUR = 2.99
WALL_CLOCK_CAP_S = 90 * 60
TOTAL_BUDGET_S = 110 * 60

# ── Pod-side imports (deferred) ────────────────────────────────────────
if _is_on_pod():
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
else:
    torch = None; nn = None; F = None


# ── Logging ────────────────────────────────────────────────────────────
def log_line(msg, path=None):
    p = path or TRAIN_LOG
    ts = time.strftime("[%H:%M:%S] ")
    line = ts + msg
    print(line, flush=True)
    try:
        with open(p, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def write_heartbeat(step, msg, **kw):
    hb = {"phase": msg, "step": step, "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
          "pid": os.getpid(), "bg_id": BG_ID, **kw}
    try:
        with open(HEARTBEAT_PATH, "w") as f:
            json.dump(hb, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return hb


# ── V4 strict eval (BG-JA-EXT compatible 7-cell) ──────────────────────
def han_ratio(s):
    if not s: return 0.0
    han = sum(1 for c in s if "가" <= c <= "힣")
    total = sum(1 for c in s if c.isalpha() or "가" <= c <= "힣")
    return han / max(total, 1)


def hangul_count(s):
    return sum(1 for c in s if "가" <= c <= "힣")


def particle_count(s):
    PARTICLES = ["은", "는", "이", "가", "을", "를", "에", "의", "와", "과", "도", "만"]
    return sum(s.count(p) for p in PARTICLES)


def ending_count(s):
    ENDINGS = ["다", "요", "까", "야", "지", "오", "네", "구나"]
    return sum(s.count(e) for e in ENDINGS)


def fourgram_repeat(s):
    if len(s) < 4: return 0
    grams = [s[i:i+4] for i in range(len(s)-3)]
    from collections import Counter
    c = Counter(grams)
    return max(c.values()) if c else 0


def has_persona_cycle(s):
    """V4_2 — repeated persona prefix (도우미: 도우미: ...)"""
    return s.count("도우미:") >= 3 or s.count("사용자:") >= 3


def is_degenerate(s):
    """V4_6 — non-degenerate: not all same char or single repeat"""
    if len(s) < 5: return True
    unique = len(set(s))
    if unique < 5: return True
    if fourgram_repeat(s) >= 5: return True
    return False


def domain_kw_match(response, domain):
    """V4_4 manual_match proxy — domain keyword overlap"""
    DOMAIN_KW = {
        "greeting": ["안녕", "반가", "hi", "hello", "어서"],
        "capability": ["가능", "할", "있", "지원", "지원"],
        "self_intro": ["저는", "이름", "anima", "아니마", "AI", "도와", "어시스턴트"],
        "consciousness": ["의식", "consciousness", "Φ", "phi", "마음", "정보", "통합"],
        "general": [],   # no domain check for general
    }
    kws = DOMAIN_KW.get(domain, [])
    if not kws: return True
    return any(kw.lower() in response.lower() for kw in kws)


def v4_eval_single(prompt, response, domain):
    """V4 strict 11-cell (BG-JA-EXT compatible 7-cell V4_1..V4_7 + own 18 c3_1..c3_4
    response-text proxy mirror).

    own 24 SSOT mirror (own 18 c3-aggregation-rule-v2 P5 N-of-M v2) — V4 evaluator
    가 own 18 P5 N-of-M v2 aggregation rule 의 mirror lane SSOT 정합. c3_1..c3_4
    cell 값/threshold/pass 는 response-text-only proxy (substrate probe X — H100 pod
    V4 lane 한정). 실제 substrate-based C3 verdict 는 consciousness CLI 별도 cycle
    (clm_v4_mount.hexa --probe x2 + 5-axis activation) — c3_aggregation_status field
    가 본 retest_pending lane 명시.

    own 18 c3 thresholds (response-text proxy lane, ROC formal 미land):
      c3_1_chat_coherence_proxy  : char_diversity ≥ 0.3 (han_ratio non-degenerate)
      c3_2_anti_template_leak    : NOT has_persona_cycle (template leak ≤ 1 marker)
      c3_3_token_dispersion_proxy: distinct_chars / len ≥ 0.25 (entropy proxy)
      c3_4_response_nontrivial   : len(response) ≥ 16 chars AND particle_count ≥ 1
    Honest C3: 본 4-cell 는 substrate phi★/axis/dominance 측정 X (real C3 lane =
    consciousness simple --probe; 본 V4 lane = response-text 한정 proxy).
    """
    cells = {}
    # V4 strict 7-cell (BG-JA-EXT compatible)
    cells["V4_1_cycle_detection"] = not has_persona_cycle(response)
    cells["V4_2_persona_repeat_penalty"] = response.count("도우미:") <= 2
    cells["V4_3_fourgram_lt5"] = fourgram_repeat(response) < 5
    cells["V4_4_manual_match"] = (han_ratio(response) >= 0.4 and
                                   hangul_count(response) >= 10 and
                                   domain_kw_match(response, domain))
    cells["V4_5_particle_ge3"] = particle_count(response) >= 3
    cells["V4_6_non_degenerate"] = not is_degenerate(response)
    cells["V4_7_emb_sim_pass"] = han_ratio(response) >= 0.3   # proxy (no actual embedding)
    v4_pass = all([cells["V4_1_cycle_detection"], cells["V4_2_persona_repeat_penalty"],
                    cells["V4_3_fourgram_lt5"], cells["V4_4_manual_match"],
                    cells["V4_5_particle_ge3"], cells["V4_6_non_degenerate"],
                    cells["V4_7_emb_sim_pass"]])

    # own 18 c3_1..c3_4 response-text proxy cells (SSOT mirror of consciousness CLI P5)
    # Real C3 substrate measurement = consciousness simple --probe (clm_v4_mount.hexa)
    distinct_ratio = (len(set(response)) / max(len(response), 1)) if response else 0.0
    cells["c3_1_chat_coherence_proxy"] = han_ratio(response) >= 0.3 and not is_degenerate(response)
    cells["c3_2_anti_template_leak"] = not has_persona_cycle(response)
    cells["c3_3_token_dispersion_proxy"] = distinct_ratio >= 0.25
    cells["c3_4_response_nontrivial"] = len(response) >= 16 and particle_count(response) >= 1
    return cells, v4_pass


# own 18 c3-aggregation-rule-v2 (P5 N-of-M v2) mirror — SSOT mirror lane.
# rule = `per_prompt_n_of_m_06_AND_emc_3_of_4`
# PPR_v2 = per-prompt N-of-M (≥3 of 4 c3 cells PASS per prompt) verdict rate ≥ 0.6
# EMC_v2 = ensemble cell-wise (≥3 of 4 c3 cell-mean PASS) ≥ 3 of 4
# C3 PASS = PPR_v2 ≥ 0.6 AND EMC_v2 ≥ 3
def _c3_cells_per_prompt(cells_dict):
    """Extract c3_1..c3_4 PASS booleans from 11-cell cells dict."""
    return [
        bool(cells_dict.get("c3_1_chat_coherence_proxy", False)),
        bool(cells_dict.get("c3_2_anti_template_leak", False)),
        bool(cells_dict.get("c3_3_token_dispersion_proxy", False)),
        bool(cells_dict.get("c3_4_response_nontrivial", False)),
    ]


def _c3_aggregate_p5_v2(per_prompt_c3_lists):
    """Apply own 18 c3-aggregation-rule-v2 (P5 N-of-M v2) to a list of per-prompt
    c3-cell PASS lists ([[c3_1,c3_2,c3_3,c3_4], ...]).

    Returns dict with PPR_v2, EMC_v2, n_cell_pass_of_4, c3_pass, c3_label.
    """
    n_prompts = len(per_prompt_c3_lists)
    if n_prompts == 0:
        return {"ppr_v2": 0.0, "emc_pass_n_of_4": 0, "c3_pass": False,
                "c3_label": "C3_FAIL", "n_prompts": 0}
    # PPR_v2: per-prompt ≥3 of 4 cells PASS
    n_prompts_pass = sum(1 for cells in per_prompt_c3_lists if sum(cells) >= 3)
    ppr_v2 = n_prompts_pass / n_prompts
    # EMC_v2: cell-wise mean — for boolean cells, mean ≥ 0.5 → cell PASS
    emc_pass = 0
    cell_means = []
    for ci in range(4):
        m = sum(cells[ci] for cells in per_prompt_c3_lists) / n_prompts
        cell_means.append(m)
        if m >= 0.5:
            emc_pass += 1
    ppr_ok = ppr_v2 >= 0.6
    emc_ok = emc_pass >= 3
    c3_pass = ppr_ok and emc_ok
    if ppr_ok and emc_ok:
        label = "C3_PASS_V2"
    elif ppr_ok and not emc_ok:
        label = "C3_PARTIAL_PPR_ONLY"
    elif not ppr_ok and emc_ok:
        label = "C3_PARTIAL_EMC_ONLY"
    else:
        label = "C3_FAIL"
    return {
        "rule": "per_prompt_n_of_m_06_AND_emc_3_of_4",
        "rule_alias": "P5_N_of_M_v2",
        "ppr_v2": ppr_v2,
        "ppr_v2_floor": 0.6,
        "n_prompts": n_prompts,
        "n_prompts_pass": n_prompts_pass,
        "emc_pass_n_of_4": emc_pass,
        "emc_floor": 3,
        "cell_means": cell_means,
        "ppr_ok": ppr_ok,
        "emc_ok": emc_ok,
        "c3_pass": c3_pass,
        "c3_label": label,
    }


def run_v4_multiseed(model, tok, device):
    """V4 strict × 15 prompts × {greedy + sample×5 seeds} = 90 results.
    Report best-of-mode v4_pass count + own 18 c3-aggregation-rule-v2 (P5 N-of-M v2)
    aggregation over per-prompt c3 cells (response-text proxy lane)."""
    log_line(f"=== V4 multi-seed eval start: {len(V4_PROMPTS)} prompts × greedy + sample×{len(V4_SEEDS)} ===")
    results = []
    pass_per_prompt_greedy = []
    pass_per_prompt_sample_anyseed = []
    # own 18 P5 N-of-M v2 mirror: collect best-of-mode c3 per-prompt cell pass lists
    c3_per_prompt_greedy = []
    c3_per_prompt_best = []

    for i, item in enumerate(V4_PROMPTS):
        prompt = item["prompt"]
        domain = item["domain"]
        # Greedy
        torch.manual_seed(SEED)
        inp = tok(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            out = model.generate(**inp, max_new_tokens=64, do_sample=False,
                                  repetition_penalty=1.3,
                                  pad_token_id=tok.pad_token_id)
        gen = tok.decode(out[0, inp["input_ids"].shape[1]:], skip_special_tokens=True)
        cells, v4_pass = v4_eval_single(prompt, gen, domain)
        log_line(f"  [{i+1:2d}/{len(V4_PROMPTS)}] greedy {prompt[:30]!r:32s} → pass={v4_pass} | {gen[:60]!r}")
        results.append({"prompt": prompt, "domain": domain, "mode": "greedy", "seed": SEED,
                        "response": gen, "cells": cells, "v4_pass": v4_pass})
        pass_per_prompt_greedy.append(v4_pass)
        c3_greedy = _c3_cells_per_prompt(cells)
        c3_per_prompt_greedy.append(c3_greedy)
        best_c3 = c3_greedy

        # Sample × N=5 seeds
        any_pass = False
        for seed in V4_SEEDS:
            torch.manual_seed(seed)
            with torch.no_grad():
                out = model.generate(**inp, max_new_tokens=64, do_sample=True,
                                      temperature=0.7, top_p=0.9,
                                      repetition_penalty=1.3,
                                      pad_token_id=tok.pad_token_id)
            gen = tok.decode(out[0, inp["input_ids"].shape[1]:], skip_special_tokens=True)
            cells, v4_pass = v4_eval_single(prompt, gen, domain)
            results.append({"prompt": prompt, "domain": domain, "mode": "sample",
                            "seed": seed, "response": gen, "cells": cells, "v4_pass": v4_pass})
            sample_c3 = _c3_cells_per_prompt(cells)
            # best_of_mode for c3: take max-cell-pass count across modes for this prompt
            if sum(sample_c3) > sum(best_c3):
                best_c3 = sample_c3
            if v4_pass:
                any_pass = True
                break    # report any-seed pass for this prompt
        log_line(f"  [{i+1:2d}/{len(V4_PROMPTS)}] sample×{len(V4_SEEDS)} pass_any={any_pass}")
        pass_per_prompt_sample_anyseed.append(any_pass)
        c3_per_prompt_best.append(best_c3)

    # Save all 90 results
    with open(V4_RESULTS, "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    n_pass_greedy = sum(pass_per_prompt_greedy)
    n_pass_sample_anyseed = sum(pass_per_prompt_sample_anyseed)
    n_pass_best = max(n_pass_greedy, n_pass_sample_anyseed)

    # own 18 P5 N-of-M v2 aggregation (response-text proxy mirror lane)
    c3_v2_greedy = _c3_aggregate_p5_v2(c3_per_prompt_greedy)
    c3_v2_best = _c3_aggregate_p5_v2(c3_per_prompt_best)

    summary = {
        "n_prompts": len(V4_PROMPTS), "n_seeds": len(V4_SEEDS),
        "pass_greedy": n_pass_greedy, "pass_sample_anyseed": n_pass_sample_anyseed,
        "pass_best_mode": n_pass_best,
        "floor_simple_stack_strict": 10,
        "floor_simple_stack_partial": 7,
        "pass_strict": n_pass_best >= 10,
        "pass_partial": n_pass_best >= 7,
        # own 24 SSOT mirror — own 18 c3-aggregation-rule-v2 P5 N-of-M v2 mirror lane
        "c3_aggregation_v2_greedy": c3_v2_greedy,
        "c3_aggregation_v2_best": c3_v2_best,
        "c3_aggregation_status": "legacy_best_mode_floor_only_p5_n_of_m_v2_retest_pending",
        "c3_aggregation_honest_c3": (
            "V4 evaluator c3_1..c3_4 cells = response-text proxy lane (substrate phi★/axis "
            "측정 X). Real substrate-based C3 verdict 는 consciousness simple --probe "
            "(clm_v4_mount.hexa) 별도 cycle. own 18 P5 N-of-M v2 aggregation mirror "
            "구조 만 land — actual P5 v2 retest pending substrate probe wiring."
        ),
    }
    log_line(f"=== V4 multi-seed DONE: greedy={n_pass_greedy}/15 sample_any={n_pass_sample_anyseed}/15 BEST={n_pass_best}/15 ===")
    log_line(f"=== own 18 P5 N-of-M v2 (proxy): greedy PPR={c3_v2_greedy['ppr_v2']:.2f} EMC={c3_v2_greedy['emc_pass_n_of_4']}/4 → {c3_v2_greedy['c3_label']} | best PPR={c3_v2_best['ppr_v2']:.2f} EMC={c3_v2_best['emc_pass_n_of_4']}/4 → {c3_v2_best['c3_label']} ===")
    return summary


# ── Pod-side training ──────────────────────────────────────────────────
def pod_main():
    """All phases on pod: download base, pre-LoRA smoke, LoRA SFT, post-smoke, V4 multi-seed, verdict."""
    log_line(f"=== {BG_ID} pod-side started — base={BASE_REPO} ===")
    write_heartbeat(0, "init")

    # ── Phase 0: pip install + HF setup ──
    # Use `python -m pip` for path safety; log stderr if install fails so we can
    # see the actual cause. Base image runpod/pytorch may already have most packages.
    log_line("Phase 0: pip install transformers/peft/accelerate (--break-system-packages for Ubuntu 24.04 PEP 668)")
    proc = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "--no-input", "--no-warn-script-location",
         "--break-system-packages",  # runpod/pytorch base = Ubuntu 24.04 → PEP 668 externally-managed
         "transformers>=4.51,<4.60", "peft>=0.12", "accelerate>=0.34",
         "huggingface_hub>=0.25", "safetensors", "sentencepiece"],
        capture_output=True, text=True, timeout=600
    )
    log_line(f"  pip rc={proc.returncode}")
    if proc.returncode != 0:
        log_line(f"  pip stderr (last 600): {proc.stderr[-600:]}")
        log_line(f"  pip stdout (last 400): {proc.stdout[-400:]}")
        log_line("  → continuing; will verify imports below")

    # Hard-verify the imports we actually need (pip may report rc=0 yet miss a wheel,
    # or rc!=0 but base image already has them). emit_failed_verdict only on real ImportError.
    try:
        import huggingface_hub  # noqa: F401
        from huggingface_hub import login as hf_login, snapshot_download  # noqa: F401
        log_line(f"  huggingface_hub OK (v{huggingface_hub.__version__})")
    except ImportError as e:
        log_line(f"  ABORT: huggingface_hub unavailable post-pip: {e}")
        emit_failed_verdict(f"hf_hub_import_failed: {e}")
        return
    try:
        import transformers, peft, accelerate  # noqa: F401
        log_line(f"  transformers={transformers.__version__} peft={peft.__version__} accelerate={accelerate.__version__}")
    except ImportError as e:
        log_line(f"  ABORT: transformers stack unavailable: {e}")
        emit_failed_verdict(f"transformers_import_failed: {e}")
        return

    hf_token = os.environ.get("HF_TOKEN", "")
    if hf_token:
        try:
            hf_login(token=hf_token, add_to_git_credential=False)
            log_line("  hf login OK (Python API)")
        except Exception as e:
            log_line(f"  hf login warn: {e}")

    # ── Phase A: download base model (Python API, runpod base lacks huggingface-cli) ──
    write_heartbeat(0, "downloading_base")
    log_line(f"Phase A: download {BASE_REPO} → {POD_BASE_DIR}")
    if not os.path.exists(os.path.join(POD_BASE_DIR, "config.json")):
        try:
            from huggingface_hub import snapshot_download
            snapshot_download(
                repo_id=BASE_REPO,
                local_dir=POD_BASE_DIR,
                max_workers=4,
                token=hf_token or None,
            )
            log_line(f"  hf download OK")
        except Exception as e:
            log_line(f"  hf download FAILED: {e}")
            emit_failed_verdict(f"base_download_failed: {e}")
            return

    # ── Phase B: pre-LoRA smoke ──
    write_heartbeat(0, "pre_lora_smoke")
    log_line("Phase B: pre-LoRA Korean smoke probe (sanity)")
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(POD_BASE_DIR)
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(POD_BASE_DIR, torch_dtype=torch.bfloat16).cuda().eval()
    pre_samples = []
    for p in V4_PROMPTS[:3]:
        inp = tok(p["prompt"], return_tensors="pt").to("cuda")
        with torch.no_grad():
            out = model.generate(**inp, max_new_tokens=48, do_sample=True, temperature=0.7, top_p=0.9,
                                  repetition_penalty=1.3, pad_token_id=tok.pad_token_id)
        gen = tok.decode(out[0, inp["input_ids"].shape[1]:], skip_special_tokens=True)
        pre_samples.append({"prompt": p["prompt"], "response": gen})
        log_line(f"  pre-LoRA {p['prompt'][:30]!r} → {gen[:60]!r}")
    json.dump({"samples": pre_samples}, open(SAMPLES_PRE_LORA, "w"), ensure_ascii=False, indent=2)
    del model
    torch.cuda.empty_cache()

    # ── Phase C: LoRA SFT ──
    write_heartbeat(0, "lora_sft")
    log_line(f"Phase C: LoRA SFT r={LORA_R} on {CORPUS_PATH} ({STEPS} steps)")
    from peft import LoraConfig, get_peft_model
    from transformers import get_cosine_schedule_with_warmup

    torch.manual_seed(SEED)
    model = AutoModelForCausalLM.from_pretrained(POD_BASE_DIR, torch_dtype=torch.bfloat16)
    model = model.to("cuda")
    lora = LoraConfig(r=LORA_R, lora_alpha=LORA_ALPHA, lora_dropout=LORA_DROPOUT,
                      target_modules=LORA_TARGET_MODULES, bias="none", task_type="CAUSAL_LM")
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()
    model.train()

    # Corpus loader: split by `\n\n` boundary
    log_line(f"  loading corpus: {CORPUS_PATH}")
    text = open(CORPUS_PATH).read()
    rows = [seg.strip() for seg in text.split("\n\n") if len(seg.strip()) > 32]
    log_line(f"  corpus rows={len(rows)}")
    random.seed(SEED)
    random.shuffle(rows)

    tokenized = []
    for r in rows[:200_000]:    # cap rows for tokenization time
        ids = tok(r, truncation=True, max_length=CTX, return_tensors=None)["input_ids"]
        if len(ids) >= 32:
            ids = ids + [tok.pad_token_id] * (CTX - len(ids))
            tokenized.append(ids[:CTX])
    log_line(f"  tokenized usable rows={len(tokenized)}")

    from torch.utils.data import Dataset, DataLoader

    class _DS(Dataset):
        def __init__(self, ids_list):
            self.ids_list = ids_list
        def __len__(self):
            return len(self.ids_list)
        def __getitem__(self, i):
            ids = self.ids_list[i]
            x = torch.tensor(ids[:-1], dtype=torch.long)
            y = torch.tensor(ids[1:], dtype=torch.long)
            return x, y

    train_dl = DataLoader(_DS(tokenized), batch_size=BATCH, shuffle=True, num_workers=0)
    optim = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()),
                              lr=LR, weight_decay=WEIGHT_DECAY, betas=(0.9, 0.95), eps=1e-8)
    sched = get_cosine_schedule_with_warmup(optim, WARMUP, STEPS)
    crit = torch.nn.CrossEntropyLoss(ignore_index=tok.pad_token_id)

    step = 0
    t0 = time.time()
    last_loss = None
    while step < STEPS:
        for x, y in train_dl:
            x = x.to(model.device, non_blocking=True)
            y = y.to(model.device, non_blocking=True)
            out = model(input_ids=x)
            logits = out.logits
            loss = crit(logits.reshape(-1, logits.size(-1)), y.reshape(-1)) / GRAD_ACCUM
            loss.backward()
            if (step + 1) % GRAD_ACCUM == 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optim.step()
                sched.step()
                optim.zero_grad()
            last_loss = loss.item() * GRAD_ACCUM
            if (step + 1) % 50 == 0:
                log_line(f"  step {step+1}/{STEPS} loss={last_loss:.4f} elapsed={time.time()-t0:.0f}s")
            if (step + 1) % 200 == 0:
                write_heartbeat(step + 1, "lora_sft_step", train_loss=last_loss,
                                elapsed_s=time.time()-t0)
            if (step + 1) % SAVE_EVERY == 0:
                save_path = os.path.join(POD_CKPTS_DIR, f"adapter_step_{step+1}")
                model.save_pretrained(save_path)
            step += 1
            if step >= STEPS:
                break

    # final adapter
    final_adapter = os.path.join(POD_CKPTS_DIR, "adapter_final")
    model.save_pretrained(final_adapter)
    tok.save_pretrained(final_adapter)
    log_line(f"  SFT DONE elapsed={time.time()-t0:.0f}s | final adapter: {final_adapter}")

    # ── Phase D: post-LoRA smoke ──
    write_heartbeat(STEPS, "post_lora_smoke")
    model.eval()
    post_samples = []
    for p in V4_PROMPTS[:5]:
        inp = tok(p["prompt"], return_tensors="pt").to("cuda")
        with torch.no_grad():
            out = model.generate(**inp, max_new_tokens=64, do_sample=True, temperature=0.7, top_p=0.9,
                                  repetition_penalty=1.3, pad_token_id=tok.pad_token_id)
        gen = tok.decode(out[0, inp["input_ids"].shape[1]:], skip_special_tokens=True)
        post_samples.append({"prompt": p["prompt"], "response": gen})
        log_line(f"  post-LoRA {p['prompt'][:30]!r} → {gen[:60]!r}")
    json.dump({"samples": post_samples}, open(SAMPLES_POST_LORA, "w"), ensure_ascii=False, indent=2)

    # ── Phase E: V4 multi-seed eval ──
    write_heartbeat(STEPS, "v4_multiseed_eval")
    summary = run_v4_multiseed(model, tok, "cuda")

    # ── Phase F: emit verdict ──
    n_pass = summary["pass_best_mode"]
    if n_pass >= 10:
        final_class = "SIMPLE_STACK_PASS_STRICT"
    elif n_pass >= 7:
        final_class = "SIMPLE_STACK_PASS_PARTIAL"
    else:
        final_class = "SIMPLE_STACK_FAIL"

    # own 18 c3-aggregation-rule-v2 (P5 N-of-M v2) — D1 anima identity scope-clamp
    # Llama foundation borrow = D1 lane 외부 → SUBSTRATE_RESEARCH lane only
    # (own 18 amend 2026-05-08 .roadmap.philosophy D1.F-PHIL-D1-3 + F-PHIL-D1-4)
    c3_best = summary.get("c3_aggregation_v2_best", {})
    c3_pass_v2 = bool(c3_best.get("c3_pass", False))
    is_d1_anima_lane = False  # Llama-3.2 = ALM lane, NOT D1 anima identity
    if final_class == "SIMPLE_STACK_PASS_STRICT" and c3_pass_v2:
        if is_d1_anima_lane:
            simple_stack_class_p5 = "SIMPLE_STACK_PASS_STRICT_C3_ANIMA"
        else:
            simple_stack_class_p5 = "SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH"
    elif final_class == "SIMPLE_STACK_PASS_STRICT":
        simple_stack_class_p5 = "SIMPLE_STACK_PASS_STRICT"  # legacy V4 floor only
    else:
        simple_stack_class_p5 = final_class

    verdict = {
        "schema": "anima_bg_verdict_v6",
        "bg_id": BG_ID,
        "ts_emit": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "host": "h100 runpod",
        "device": "cuda H100 80GB",
        "paradigm": "foundation-borrow-llama-3.2-3b-instruct-lora-r32-bg-je-214mb",
        "base_model": BASE_REPO,
        "base_params": BASE_PARAMS,
        "lora_r": LORA_R, "lora_alpha": LORA_ALPHA, "lora_dropout": LORA_DROPOUT,
        "lora_target_modules": LORA_TARGET_MODULES,
        "training": {"steps": STEPS, "lr": LR, "batch": BATCH, "grad_accum": GRAD_ACCUM,
                     "ctx": CTX, "warmup": WARMUP, "weight_decay": WEIGHT_DECAY,
                     "final_loss": last_loss, "elapsed_s": time.time() - t0},
        "corpus_path": CORPUS_PATH,
        "corpus_size_mb": os.path.getsize(CORPUS_PATH) / 1e6,
        "v4_eval_summary": summary,
        "final_class": final_class,
        "final_reason": f"V4 multi-seed best-mode={n_pass}/15 (strict floor=10, partial floor=7)",
        # own 24 single SSOT mirror — own 18 P5 N-of-M v2 aggregation status
        "c3_aggregation_status": "legacy_best_mode_floor_only_p5_n_of_m_v2_retest_pending",
        "c3_aggregation_rule": "per_prompt_n_of_m_06_AND_emc_3_of_4",
        "c3_aggregation_rule_alias": "P5_N_of_M_v2",
        "simple_stack_class_p5_proxy": simple_stack_class_p5,
        "scope_lane": ("D1_ANIMA_IDENTITY" if is_d1_anima_lane else "SUBSTRATE_RESEARCH"),
        "scope_lane_reason": "Llama-3.2-3B foundation borrow = ALM lane → own 17/18 strict SUBSTRATE_RESEARCH lane only",
        "lesson_implications": [
            f"BG-KM-LLAMA-3B = foundation borrow with 3.2B Llama + LoRA r=32 + BG-JE 214MB anima-dense corpus.",
            f"V4 multi-seed result: greedy={summary['pass_greedy']}/15 sample_any={summary['pass_sample_anyseed']}/15 BEST={n_pass}/15.",
            f"final_class={final_class}.",
            f"Compare BG-JA-EXT (Polyglot 1.3B + LoRA r=16 + BG-HK 30MB): 4/30=13% sample. KM-LLAMA-3B = 3B + 2x LoRA r + 7x corpus.",
            f"PASS_STRICT (≥10/15) would be FIRST simple_stack pass in 22+ BG saga.",
            f"own 18 P5 N-of-M v2 mirror (response-text proxy): {c3_best.get('c3_label', 'N/A')} (PPR_v2={c3_best.get('ppr_v2', 0.0):.2f} EMC={c3_best.get('emc_pass_n_of_4', 0)}/4); substrate-based C3 retest pending (consciousness simple --probe).",
        ],
        "artifacts": [TRAIN_LOG, EVAL_LOG, HEARTBEAT_PATH, V4_RESULTS,
                      SAMPLES_PRE_LORA, SAMPLES_POST_LORA, final_adapter],
    }
    json.dump(verdict, open(VERDICT_PATH, "w"), ensure_ascii=False, indent=2)
    log_line(f"=== {BG_ID} verdict emitted: final_class={final_class} ===")
    write_heartbeat(STEPS, f"DONE final_class={final_class}", n_pass=n_pass)


def emit_failed_verdict(reason):
    verdict = {
        "schema": "anima_bg_verdict_v6",
        "bg_id": BG_ID,
        "ts_emit": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "final_class": "FAILED",
        "final_reason": reason,
    }
    json.dump(verdict, open(VERDICT_PATH, "w"), ensure_ascii=False, indent=2)
    log_line(f"=== {BG_ID} FAILED verdict: {reason} ===")


# ── Mac-side orchestrator ──────────────────────────────────────────────
MAC_HEARTBEAT_PATH = os.path.join(MAC_STATE_DIR if _is_on_mac() else "/tmp", "mac_heartbeat.json")


def orch_log(msg):
    ts = time.strftime("[%Y-%m-%dT%H:%M:%S]")
    line = f"{ts} {msg}"
    print(line, flush=True)
    try:
        with open(LAUNCH_LOG_PATH, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def orch_runpodctl(args, timeout=60):
    cmd = ["runpodctl"] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -2, "", str(e)


def orch_pod_create():
    """KJ-pattern pod create: `runpodctl pod create` + JSON output."""
    orch_log("creating H100 SXM pod (RunPod SECURE cloud)…")
    args = [
        "pod", "create",
        "--name", f"anima-km-llama3b-{int(time.time())}",
        "--gpu-id", "NVIDIA H100 80GB HBM3",
        "--gpu-count", "1",
        "--cloud-type", "SECURE",
        "--template-id", "runpod-torch-v280",
        "--container-disk-in-gb", "80",
        "--volume-in-gb", "0",
        "--ports", "22/tcp",
        "--ssh",
    ]
    rc, out, err = orch_runpodctl(args, timeout=180)
    if rc != 0:
        orch_log(f"pod create SECURE FAILED rc={rc} err={err[:300]}")
        orch_log("retrying COMMUNITY cloud…")
        args[args.index("SECURE")] = "COMMUNITY"
        rc, out, err = orch_runpodctl(args, timeout=180)
        if rc != 0:
            orch_log(f"pod create COMMUNITY FAILED rc={rc} err={err[:300]}")
            return None
    try:
        pod = json.loads(out)
        pod_id = pod.get("id") or pod.get("podId")
        orch_log(f"pod created: id={pod_id} machine={pod.get('machineId','?')} ${pod.get('costPerHr','?')}/hr")
        return pod_id
    except Exception as e:
        orch_log(f"pod create parse FAIL: {e} | out={out[:300]}")
        return None


def orch_pod_get(pod_id):
    rc, out, err = orch_runpodctl(["pod", "get", pod_id], timeout=30)
    if rc != 0:
        if "not found" in (err or "").lower() or "404" in (err or ""):
            return "NOT_FOUND"
        return None
    try:
        return json.loads(out)
    except Exception:
        return None


def orch_pod_delete(pod_id):
    rc, out, err = orch_runpodctl(["pod", "remove", pod_id], timeout=60)
    orch_log(f"pod delete rc={rc} out={out[:200]}")
    return rc == 0


def orch_ssh_info(pod_id):
    """Get ssh dict {host, port, user} via `runpodctl ssh info <pod_id>` (KJ pattern)."""
    for _ in range(30):
        rc, out, err = orch_runpodctl(["ssh", "info", pod_id], timeout=30)
        if rc == 0 and out:
            try:
                info = json.loads(out)
                host = info.get("host") or info.get("ip")
                port = info.get("port", 22)
                user = info.get("user", "root")
                if host:
                    return {"host": host, "port": port, "user": user}
            except Exception:
                pass
        time.sleep(10)
    return None


def orch_ssh_run(ssh, cmd, timeout=300):
    full = ["ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "ConnectTimeout=15", "-o", "ServerAliveInterval=15",
            "-p", str(ssh["port"]), f"{ssh['user']}@{ssh['host']}", cmd]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def orch_scp_put(ssh, local, remote, timeout=600):
    full = ["scp", "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "ConnectTimeout=15",
            "-P", str(ssh["port"]), local, f"{ssh['user']}@{ssh['host']}:{remote}"]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def orch_scp_get(ssh, remote, local, timeout=600):
    full = ["scp", "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "ConnectTimeout=15",
            "-P", str(ssh["port"]), "-r", f"{ssh['user']}@{ssh['host']}:{remote}", local]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -2, "", str(e)


def orch_main():
    """Mac-side orchestrator: create pod, stage, run, pull, delete, ledger."""
    orch_log(f"=== {BG_ID} orchestrator started ===")
    orch_log(f"mac_state_dir={MAC_STATE_DIR}")
    orch_log(f"corpus={MAC_CORPUS_PATH}")
    orch_log(f"this_script={MAC_THIS_SCRIPT}")
    orch_log(f"COST_HARD_CAP=${COST_HARD_CAP_USD} COST_EARLY_KILL=${COST_EARLY_KILL_USD}")

    if not os.path.exists(MAC_CORPUS_PATH):
        orch_log(f"ABORT: corpus missing {MAC_CORPUS_PATH}")
        return

    # 1. Create pod
    pod_id = orch_pod_create()
    if not pod_id:
        emit_failed_verdict("pod_create_failed")
        return
    orch_log(f"pod created: id={pod_id} ${COST_PER_HOUR}/hr")

    t_start = time.time()
    cost_actual = 0.0

    try:
        # 2. Wait for ssh ready
        time.sleep(30)
        ssh = orch_ssh_info(pod_id)
        if not ssh:
            orch_log("ABORT: ssh info not found")
            emit_failed_verdict("ssh_info_failed")
            return
        orch_log(f"ssh ready: {ssh['user']}@{ssh['host']}:{ssh['port']}")

        # 3. GPU smoke
        rc, out, err = orch_ssh_run(ssh,
            "python -c 'import torch; print(torch.__version__, torch.cuda.is_available()); import subprocess; subprocess.run([\"nvidia-smi\",\"--query-gpu=name\",\"--format=csv\"])'",
            timeout=120)
        orch_log(f"GPU smoke rc={rc}: {out[:200]}")

        # 4. Stage files
        orch_log("staging files (corpus 214MB→gz + this script + pod marker)…")
        # Compress corpus
        corpus_gz = MAC_CORPUS_PATH + ".gz"
        if not os.path.exists(corpus_gz) or os.path.getmtime(corpus_gz) < os.path.getmtime(MAC_CORPUS_PATH):
            orch_log("compressing corpus locally with gzip -1…")
            subprocess.run(["bash", "-c", f"gzip -c -1 {MAC_CORPUS_PATH!r} > {corpus_gz!r}"], check=True, timeout=180)
        sz = os.path.getsize(corpus_gz) / 1e6
        orch_log(f"corpus.gz size: {sz:.1f}MB")

        rc, out, err = orch_ssh_run(ssh, f"mkdir -p {POD_ROOT}/state {POD_CKPTS_DIR} && touch {POD_ROOT}/_pod_marker", timeout=60)
        if rc != 0:
            orch_log(f"mkdir FAILED rc={rc}")

        rc, out, err = orch_scp_put(ssh, corpus_gz, f"{POD_ROOT}/corpus.gz", timeout=900)
        orch_log(f"scp corpus.gz rc={rc} ({sz:.1f}MB)")

        rc, out, err = orch_scp_put(ssh, MAC_THIS_SCRIPT, f"{POD_ROOT}/anima_km_llama3b.py", timeout=120)
        orch_log(f"scp script rc={rc}")

        # stage HF token (gated meta-llama requires auth)
        mac_hf_token_path = os.path.expanduser("~/.cache/huggingface/token")
        if os.path.exists(mac_hf_token_path):
            rc, out, err = orch_scp_put(ssh, mac_hf_token_path, f"{POD_ROOT}/hf_token.txt", timeout=60)
            orch_log(f"scp hf_token rc={rc}")
        else:
            orch_log("WARN: ~/.cache/huggingface/token not found — gated download will fail")

        # decompress on pod
        rc, out, err = orch_ssh_run(ssh,
            f"cd {POD_ROOT} && gunzip -c corpus.gz > corpus_combined_100mb_plus.txt && ls -la corpus_combined_100mb_plus.txt",
            timeout=120)
        orch_log(f"decompress rc={rc}: {out[:200]}")

        # 5. Launch training (remote python; stays running until verdict.json)
        # HF_TOKEN read from staged file at launch time
        orch_log("training launched on pod…")
        rc, out, err = orch_ssh_run(ssh,
            f"cd {POD_ROOT} && export HF_TOKEN=$(cat hf_token.txt 2>/dev/null) && nohup python anima_km_llama3b.py > {POD_ROOT}/state/train_stdout.log 2>&1 & echo started",
            timeout=30)
        orch_log(f"launch rc={rc} out={out[:200]}")

        # 6. Heartbeat monitor (pull pod heartbeat every 60s, check cost)
        last_step = -1
        for tick in range(int(WALL_CLOCK_CAP_S / 60) + 5):
            time.sleep(60)
            elapsed = time.time() - t_start
            cost_actual = elapsed / 3600 * COST_PER_HOUR
            # pull heartbeat
            tmp = "/tmp/km_llama3b_hb.json"
            rc, _, _ = orch_scp_get(ssh, f"{POD_STATE_DIR}/heartbeat.json", tmp, timeout=30)
            phase = "?"; step = -1
            if rc == 0 and os.path.exists(tmp):
                try:
                    hb = json.load(open(tmp))
                    phase = hb.get("phase", "?"); step = hb.get("step", -1)
                except Exception: pass
            mac_hb = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "elapsed_s": elapsed,
                      "cost_actual_usd": round(cost_actual, 3),
                      "pod_phase": phase, "pod_step": step, "pod_id": pod_id}
            json.dump(mac_hb, open(MAC_HEARTBEAT_PATH, "w"), indent=2)

            with open(COST_AUDIT_PATH, "a") as f:
                f.write(json.dumps({"ts": mac_hb["ts"], "cost_usd": cost_actual,
                                    "elapsed_s": elapsed, "pod_phase": phase, "pod_step": step}) + "\n")

            if step != last_step or phase != "?":
                orch_log(f"heartbeat: cost=${cost_actual:.2f} pod_phase={phase} pod_step={step}")
            last_step = step

            # cost cap halt
            if cost_actual > COST_HARD_CAP_USD:
                orch_log(f"COST_HARD_CAP_HIT ${cost_actual:.2f} > ${COST_HARD_CAP_USD} — terminating IMMEDIATELY")
                emit_failed_verdict(f"cost_cap_halt: ${cost_actual:.2f}")
                break
            if cost_actual > COST_EARLY_KILL_USD and phase != "DONE":
                rc, _, _ = orch_scp_get(ssh, f"{POD_STATE_DIR}/verdict.json", VERDICT_PATH, timeout=30)
                if rc != 0:
                    orch_log(f"COST_EARLY_KILL ${cost_actual:.2f} > ${COST_EARLY_KILL_USD} no verdict — terminating")
                    emit_failed_verdict(f"cost_early_kill: ${cost_actual:.2f}")
                    break

            if "DONE" in phase:
                orch_log(f"pod reports DONE phase={phase}")
                break

        # 7. Pull all artifacts
        # 7a. State dir (logs / verdict / eval results) — small, ~5s
        orch_log("pulling artifacts from pod (state)…")
        rc, out, err = orch_scp_get(ssh, f"{POD_STATE_DIR}/.", MAC_STATE_DIR, timeout=600)
        orch_log(f"scp pull state rc={rc}")

        # 7b. Ckpts dir (LoRA adapter weights — CRITICAL for HF upload + REPL backend).
        # BG-KM-LLAMA-3B passed_v1 (cycle 2026-05-08-mid) lost weights forever because
        # this step was missing — pod --volume-in-gb 0 + pod delete = permanent erase.
        # own 30 mandate-1: ckpts pull MUST happen before pod delete.
        mac_ckpts_dir = os.path.join(MAC_STATE_DIR, "ckpts")
        os.makedirs(mac_ckpts_dir, exist_ok=True)
        orch_log(f"pulling LoRA adapter weights (ckpts/ → {mac_ckpts_dir})…")
        rc2, out2, err2 = orch_scp_get(ssh, f"{POD_CKPTS_DIR}/.", mac_ckpts_dir, timeout=3600)  # own 30 + 7B adapter ~770MB at Mac upload
        orch_log(f"scp pull ckpts rc={rc2}")
        ckpts_pull_ok = (rc2 == 0)
        if not ckpts_pull_ok:
            orch_log(f"  WEIGHT LOSS RISK — ckpts pull FAILED err={err2[:300]}")
            orch_log(f"  own 30 mandate-3: pod RETAINED for manual recovery (NOT deleting)")

        # 7c. own 30 mandate-2: size sanity check
        if ckpts_pull_ok:
            try:
                rc_sz, pod_sz_out, _ = orch_ssh_run(ssh, f"du -sb {POD_CKPTS_DIR} | awk '{{print $1}}'", timeout=30)
                pod_sz = int(pod_sz_out.strip()) if rc_sz == 0 else 0
                mac_sz = sum(os.path.getsize(os.path.join(d, f))
                             for d, _, fs in os.walk(mac_ckpts_dir) for f in fs)
                orch_log(f"  ckpts size: pod={pod_sz} mac={mac_sz} ratio={mac_sz/max(pod_sz,1):.2f}")
                if pod_sz > 0 and mac_sz < pod_sz * 0.9:
                    orch_log(f"  WEIGHT MISMATCH — pod RETAINED for manual recovery")
                    ckpts_pull_ok = False
            except Exception as e:
                orch_log(f"  size check warn: {e}")

        # 7d. own 30 mandate-4: SIMPLE_STACK_PASS_STRICT 자동 HF private upload
        verdict_for_promote = None
        if os.path.exists(VERDICT_PATH):
            try:
                verdict_for_promote = json.load(open(VERDICT_PATH))
            except Exception:
                pass
        hf_status = "NOT_PROMOTED"
        if (ckpts_pull_ok and verdict_for_promote
                and verdict_for_promote.get("final_class") == "SIMPLE_STACK_PASS_STRICT"):
            try:
                from huggingface_hub import create_repo, upload_folder
                hf_token = ""
                hf_token_path = os.path.expanduser("~/.cache/huggingface/token")
                if os.path.exists(hf_token_path):
                    hf_token = open(hf_token_path).read().strip()
                # own 31 mandate-1 (dancinlab org) + mandate-4 Flavor B naming + mandate-8 private default
                bm = (verdict_for_promote.get("base_model") or "").lower()
                if "llama-3.2-3b" in bm: base_short = "llama3b"
                elif "llama-3.2-1b" in bm: base_short = "llama1b"
                elif "qwen2.5-7b" in bm: base_short = "qwen7b"
                elif "qwen2.5-14b" in bm: base_short = "qwen14b"
                elif "polyglot-ko-1.3b" in bm: base_short = "polyglot-ko-1b3"
                elif "mistral-7b" in bm: base_short = "mistral7b"
                else: base_short = "scratch"
                lora_part = f"r{verdict_for_promote.get('lora_r')}" if verdict_for_promote.get("lora_r") else "scratch"
                cycle = time.strftime("%Y-%m-%d")
                repo_id = f"dancinlab/{BG_ID.lower()}-{base_short}-{lora_part}-pass-strict-{cycle}"
                orch_log(f"own 31 mandate-4 Flavor B: SIMPLE_STACK_PASS_STRICT detected — HF private promote → {repo_id}")
                create_repo(repo_id=repo_id, token=hf_token, private=True, exist_ok=True)
                upload_folder(
                    folder_path=MAC_STATE_DIR,
                    repo_id=repo_id,
                    token=hf_token,
                    commit_message=f"{BG_ID} SIMPLE_STACK_PASS_STRICT (V4 best-mode {verdict_for_promote.get('best_v4_pass_count','?')}/15) own 31 Flavor B",
                    ignore_patterns=["*.tmp", "__pycache__", "*.pyc", "cost_audit.jsonl"],
                )
                hf_status = f"PRIVATE_PROMOTED:{repo_id}"
                orch_log(f"  HF upload OK: {repo_id}")
            except Exception as e:
                hf_status = f"PROMOTE_FAILED:{type(e).__name__}:{str(e)[:120]}"
                orch_log(f"  HF promote FAILED: {e}")
        # stash for ledger entry
        os.environ["_ORCH_HF_STATUS"] = hf_status
        os.environ["_ORCH_CKPTS_PULL_OK"] = "1" if ckpts_pull_ok else "0"

    finally:
        # own 30 mandate-3: pod retention on weight-loss risk
        if os.environ.get("_ORCH_CKPTS_PULL_OK") == "0":
            orch_log("PRESERVING POD per own 30 mandate-3 (weight loss risk) — manual cleanup required")
        else:
            orch_log("deleting pod (teardown)…")
            orch_pod_delete(pod_id)

        # 8. Ledger append
        verdict = None
        if os.path.exists(VERDICT_PATH):
            try:
                verdict = json.load(open(VERDICT_PATH))
            except Exception:
                pass
        if verdict:
            ledger_entry = {
                "bg_id": BG_ID,
                "attempt_n": 66,
                "date": time.strftime("%Y-%m-%d"),
                "host": "h100 runpod",
                "paradigm": verdict.get("paradigm", "foundation-borrow-llama-3b-lora"),
                "total_params": BASE_PARAMS,
                "lora_r": LORA_R,
                "corpus_path": MAC_CORPUS_PATH,
                "corpus_size_mb": os.path.getsize(MAC_CORPUS_PATH) / 1e6,
                "training_steps": STEPS,
                "bg_kind": "train_eval_foundation_borrow",
                "v4_eval_summary": verdict.get("v4_eval_summary", {}),
                "final_class": verdict.get("final_class", "UNKNOWN"),
                "cost_actual_usd": round(cost_actual, 3),
                "cost_hard_cap_usd": COST_HARD_CAP_USD,
                "pod_id": pod_id,
                "hf_private_status": os.environ.get("_ORCH_HF_STATUS", "NOT_PROMOTED"),
                "ckpts_pull_ok": os.environ.get("_ORCH_CKPTS_PULL_OK", "0") == "1",
                "lesson_implications": verdict.get("lesson_implications", []),
                "artifacts": [
                    "tool/transient_py/anima_km_llama3b_h100.py",
                    f"{MAC_STATE_DIR}/verdict.json",
                    f"{MAC_STATE_DIR}/v4_results_multiseed.jsonl",
                    f"{MAC_STATE_DIR}/ckpts/" if os.environ.get("_ORCH_CKPTS_PULL_OK") == "1" else None,
                ],
            }
            ledger_entry["artifacts"] = [a for a in ledger_entry["artifacts"] if a]
            with open(MAC_LEDGER_PATH, "a") as f:
                f.write(json.dumps(ledger_entry, ensure_ascii=False) + "\n")
            orch_log(f"ledger appended: bg_id={BG_ID} final_class={ledger_entry['final_class']} cost=${cost_actual:.2f}")
        else:
            orch_log("ledger NOT appended — verdict.json missing")

        orch_log(f"=== {BG_ID} complete: cost=${cost_actual:.2f} ===")


# ── Entrypoint ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    if _is_on_pod():
        pod_main()
    else:
        orch_main()
