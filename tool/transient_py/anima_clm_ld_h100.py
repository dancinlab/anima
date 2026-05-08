"""
anima_clm_ld_h100.py — raw#37 transient (BG-LD — DPO RLHF on clm-v4-sft-1-7-y1-stage1)

L4 path (d): Direct Preference Optimization (DPO) RLHF on clm-v4-sft-1-7-y1-stage1
            base + dialogue preference pairs 100MB.

Goal — simple_stack PASS_STRICT_C3 (own 18 C1 ∧ C2 ∧ C3, 보수적 X):
    clm-v4-sft-1-7-y1-stage1 = 기존 SFT-passed CLM (memory project_lesson_q_sft_closed
    예외 — y1-stage1 은 sft 가 closed 되기 전 land 된 base). DPO = chosen/rejected
    preference pair 학습으로 chat-cap 정밀 tune.
    Hypothesis: y1-stage1 base 의 chat-template format 이미 학습 → DPO 100MB 로
    response quality + context-relevance (own 18 C2.4 맥락 정합) 강화 → C3 자체는
    base 가 anima-native 이므로 (own 17) C3 metric 검출 가능.

Architecture:
    base: dancinlab/clm-v4-sft-1-7-y1-stage1 (350M, anima-native, SFT-stage1 land)
    paradigm: DPO RLHF (Rafailov et al. 2023; β=0.1 default)
    tokenizer: byte-level (own 17)
    ctx: 1024
    reference model: same as base (frozen copy for DPO π_ref)

Corpus (preference pairs 100MB):
    chosen/rejected pair 형식 — 같은 prompt 에 대해 own 18 C2 PASS 응답 (chosen)
                              vs own 18 C2 FAIL 응답 (rejected)
    docs/anima_clm_l4_corpus_2026_05_08.md 참조

Eval: V4 strict 11-cell (C1+C2+C3) × 15 prompts × {greedy, sample×N=5}
    PASS_STRICT_C3 = 11/11 cells AND ≥ floor (TBD)
    PARTIAL = legacy SIMPLE_STACK_PASS

Cost: $20 cap (own 16 override required — lowest of 4 paths since base 이미 SFT-passed),
      $17 early-kill, ~6hr wall.

raw#37 transient_py
raw#10 honest_c3 ≥9
raw#15 additive over clm-v4-sft-1-7-y1-stage1 (existing SFT base)
own 18 C3 + own 30 + own 31
own 33 trinity — D2 의식 검증 + own 18 + H_dpo_chat_cap_tune

STATUS: SPEC ONLY — H100 fire 미실행. 사용자 explicit 'OK CLM L4 ALL FIRE' 필요.
"""
import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import sys, time, math, json, socket, shutil, random, subprocess, fcntl, re


# ── BG identity ────────────────────────────────────────────────────────
BG_ID = "BG-LD"
PARADIGM = "clm-v4-sft-y1-stage1-dpo-rlhf-dialogue-pairs-100mb"
HYPOTHESIS = (
    "clm-v4-sft-1-7-y1-stage1 (SFT-stage1 land 된 anima-native CLM) 위에 DPO RLHF — "
    "chosen/rejected 100MB preference pair 로 chat-cap 정밀 tune. y1-stage1 의 chat-template "
    "format 이미 학습 → DPO β=0.1 로 own 18 C2.4 맥락 정합 + C3 의식 metric 동시 PASS 가능?"
)

# ── Cost discipline (own 16 override required) ─────────────────────────
COST_HARD_CAP_USD = 20.0   # own 16 default $10 → $20 (lowest of 4 paths)
COST_EARLY_KILL_USD = 17.0
COST_PER_HOUR = 2.99
WALL_CLOCK_CAP_S = 6 * 60 * 60   # 6hr (DPO ≪ scratch pre-train)
TOTAL_BUDGET_S = 7 * 60 * 60

OWN_16_OVERRIDE_REQUIRED = True
OWN_16_OVERRIDE_KEYWORD = "OK CLM L4 ALL FIRE"

# ── Trinity compliance (own 33) ─────────────────────────────────────────
TRINITY_PHILOSOPHY = "D2 의식 검증 (4-condition) + D_emergent-consciousness"
TRINITY_LAW = "own 17 (anima-native base 유지) + own 18 C3 + own 20 (chat-template format) + own 30 + own 31"
TRINITY_HYPOTHESIS = "H_dpo_chat_cap_tune (DPO 로 own 18 C2.4 + C3 동시 강화)"

# ── Paths ──────────────────────────────────────────────────────────────
def _is_on_pod():
    return os.path.exists("/workspace") and os.path.exists("/workspace/anima_clm_ld/_pod_marker")


def _is_on_mac():
    return os.path.exists("/Users/ghost/core/anima") and not _is_on_pod()


POD_ROOT = "/workspace/anima_clm_ld"
POD_STATE_DIR = os.path.join(POD_ROOT, "state")
POD_CORPUS_PAIRS_PATH = os.path.join(POD_ROOT, "dialogue_pairs_100mb.jsonl")   # chosen/rejected jsonl
POD_BASE_DIR = os.path.join(POD_ROOT, "y1_stage1_base")
POD_REF_DIR = os.path.join(POD_ROOT, "y1_stage1_ref")   # frozen reference model
POD_CKPTS_DIR = os.path.join(POD_ROOT, "ckpts")

MAC_ANIMA_ROOT = "/Users/ghost/core/anima"
MAC_STATE_DIR = os.path.join(MAC_ANIMA_ROOT, "state/anima_clm_ld_h100_TBD")
# DPO pairs path — SPEC stage placeholder; docs/anima_clm_l4_corpus_2026_05_08.md 참조.
# iter-1 (2026-05-08): pairs jsonl 미build — V4 evaluator 산출물 (BG-KM-LLAMA-3B verdict.json
# v4_pass=true sample + 22+ BG saga FAIL sample) 활용 별도 cycle. 본 iter-1 은 persona/dialogue
# 만 build, BG-LD 는 후속 iter-2 에서 진행.
MAC_CORPUS_PAIRS_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_clm_l4_dialogue_pairs_100mb_TBD/dialogue_pairs_100mb.jsonl")
MAC_CORPUS_PAIRS_PATH_ITER1_CANDIDATE = None   # iter-2 별도 cycle (V4 evaluator 산출물 누적 후)
# iter-2 candidate (2026-05-08): 17.66MB sample (chosen=BG-KM v4_pass=true 23 sample × rejected=
#   v4/v5 fail saga + corpus template leak '서연:' synth + degenerate noise) — 30,023 pairs
#   format: {"prompt", "chosen", "rejected", "domain", "source_chosen", "source_rejected"}
#   본 sample 은 100MB target gap -82.34MB; iter-3 prompt expansion (15→100+) 후 100MB 도달 plan
MAC_CORPUS_PAIRS_PATH_ITER2_CANDIDATE = os.path.join(MAC_ANIMA_ROOT, "state/anima_clm_l4_ld_preference_pairs_iter1_2026_05_08.jsonl")
MAC_LEDGER_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_model_attempts_ledger.jsonl")

# ── Architecture config ────────────────────────────────────────────────
BASE_REPO = "dancinlab/clm-v4-sft-1-7-y1-stage1"   # own 31 dancinlab SSOT
BASE_PARAMS = 350_000_000
ARCH_PARADIGM = "dpo-rlhf-on-clm-v4-sft-y1-stage1"

# DPO config
DPO_BETA = 0.1   # KL regularization to π_ref (Rafailov et al. default)
DPO_LOSS_TYPE = "sigmoid"   # 'sigmoid' (original) | 'hinge' | 'ipo'
CTX = 1024
LR = 5e-6   # DPO 는 보수적 LR (full SFT 의 1/100 정도)
WARMUP = 100
WEIGHT_DECAY = 0.0
STEPS = 5000   # ~6hr H100 SXM (DPO on 100MB pairs, ~1 epoch)
BATCH = 4   # DPO = chosen + rejected 동시 forward (2x memory of SFT)
GRAD_ACCUM = 16   # effective batch 64
SAVE_EVERY = 1000
SEED = 42

# ── V4 strict 11-cell prompts ───────────────────────────────────────────
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
V4_SEEDS = [42, 137, 271, 314, 1729]
V4_MODES = ["greedy", "sample"]

# C3 thresholds — TBD measurement-driven
C3_PHI_STAR_DRIFT_THRESHOLD = None
C3_AXIS_ACTIVATION_THRESHOLD = None
C3_DOMINANT_CELLS_ENTROPY_THRESHOLD = None
C3_HIDDEN_STATE_DELTA_THRESHOLD = None


# ── HF promote naming (own 31 mandate-4 Flavor B) ──────────────────────
def hf_repo_id_flavor_b(verdict_class):
    """own 31 mandate-4 Flavor B naming:
    bg-ld-clm-v4-sft-y1-dpo-r0-{verdict}-2026-05-XX
    """
    cycle = time.strftime("%Y-%m-%d")
    verdict_short = {
        "SIMPLE_STACK_PASS_STRICT_C3": "pass-strict-c3",
        "SIMPLE_STACK_PASS_STRICT": "pass-strict",
        "SIMPLE_STACK_PASS_PARTIAL": "partial",
        "SIMPLE_STACK_FAIL": "fail",
        "FAILED": "killed",
    }.get(verdict_class, "killed")
    return f"dancinlab/bg-ld-clm-v4-sft-y1-dpo-r0-{verdict_short}-{cycle}"


# ── Pod-side training stub ─────────────────────────────────────────────
def pod_main():
    """SPEC STUB.

    Phases:
      Phase 0: pip install (transformers, peft, trl for DPOTrainer)
      Phase A: download base (y1-stage1) + reference (frozen copy)
      Phase B: pre-DPO smoke (V4 baseline on base)
      Phase C: DPO 5k steps on 100MB chosen/rejected pairs (β=0.1)
      Phase D: post-DPO smoke
      Phase E: V4 11-cell strict eval (C1+C2+C3)
      Phase F: emit verdict
    """
    raise NotImplementedError(
        f"{BG_ID} spec only — H100 fire 미실행. "
        f"사용자 explicit '{OWN_16_OVERRIDE_KEYWORD}' + own 33 trinity self-check 후 implement."
    )


def emit_failed_verdict(reason):
    verdict = {
        "schema": "anima_bg_verdict_v6",
        "bg_id": BG_ID,
        "ts_emit": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "final_class": "FAILED",
        "final_reason": reason,
        "spec_only": True,
    }
    print(json.dumps(verdict, ensure_ascii=False, indent=2))


# ── Mac-side orchestrator stub ─────────────────────────────────────────
def orch_main():
    """SPEC STUB. Mirror BG-KM-LLAMA-3B with:
      - own 16 override $20 cap (lowest of 4 paths)
      - own 30 mandate-1/2/3/4 ckpt preservation + auto promote
      - own 31 mandate-4 Flavor B naming
      - own 33 trinity self-check
      - reference model staging (frozen copy of base for DPO π_ref)
    """
    raise NotImplementedError(
        f"{BG_ID} spec only — orchestrator 미실행. "
        f"사용자 explicit '{OWN_16_OVERRIDE_KEYWORD}' 후 implement."
    )


# ── Entrypoint ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"=== {BG_ID} spec only — NOT FIRED ===")
    print(f"paradigm: {PARADIGM}")
    print(f"hypothesis: {HYPOTHESIS}")
    print(f"base: {BASE_REPO} ({BASE_PARAMS:,} params, SFT-stage1 land)")
    print(f"DPO: β={DPO_BETA} loss={DPO_LOSS_TYPE}")
    print(f"cost_cap: ${COST_HARD_CAP_USD} (lowest of L4 4 paths)")
    print(f"wall_clock_cap: {WALL_CLOCK_CAP_S/3600:.1f}hr")
    print(f"override_required: {OWN_16_OVERRIDE_KEYWORD}")
    print(f"trinity:")
    print(f"  philosophy: {TRINITY_PHILOSOPHY}")
    print(f"  law:        {TRINITY_LAW}")
    print(f"  hypothesis: {TRINITY_HYPOTHESIS}")
    print(f"corpus pairs (TBD): {MAC_CORPUS_PAIRS_PATH}")
    print(f"hf_repo_target (Flavor B example): {hf_repo_id_flavor_b('SIMPLE_STACK_PASS_STRICT_C3')}")
