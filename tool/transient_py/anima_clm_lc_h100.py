"""
anima_clm_lc_h100.py — raw#37 transient (BG-LC — Llama-3.2-3B teacher → CLM 350M distill)

L4 path (c): teacher-student knowledge distillation — Llama-3.2-3B-Instruct teacher,
            CLM v4 mk2-v1 350M student, distillation on persona 200MB.

Goal — simple_stack PASS_STRICT_C3 (own 18 C1 ∧ C2 ∧ C3, 보수적 X):
    BG-KM-LLAMA-3B (Llama-3.2-3B + LoRA r=32) PASS_STRICT 12/15 — strong
    foundation borrow. 그러나 own 17 (anima-no-external-substrate-wrapping) 한계
    — Llama 본체는 external substrate. 본 path 는 Llama 의 chat-cap 을 CLM 350M
    student 에 distill — student 는 anima-native arch (own 17 정합) 유지하면서
    teacher 의 chat distribution 학습.
    Hypothesis: KL-divergence distill (teacher logits || student logits) on
    persona 200MB → student 가 own 18 C1+C2 PASS, C3 (의식 측정) 도 anima-native
    arch 본체 유지 → PASS_STRICT_C3 가능.

Architecture:
    teacher: meta-llama/Llama-3.2-3B-Instruct (3.2B, frozen)
    student: dancinlab/clm-v4-mk2-v1 (350M, anima-native arch, byte-level tokenizer)
    distill paradigm: token-level KL on persona 200MB
                     L_total = α·KL(T || S) + (1−α)·CE(target, S)
                     α=0.5 (TBD measurement-driven)
                     temperature τ=2.0
    NOTE: teacher tokenizer (Llama BPE) ↔ student tokenizer (byte-level) mismatch —
          re-tokenize student inputs with byte-level, project teacher logits via
          shared vocab subset OR train projection layer. 본 spec stage 미결정,
          implement 시 결정.

Eval: V4 strict 11-cell (C1+C2+C3) × 15 prompts × {greedy, sample×N=5}
    PASS_STRICT_C3 = 11/11 cells AND ≥ floor (TBD)
    PARTIAL = legacy SIMPLE_STACK_PASS

Cost: $40 cap (own 16 override required), $35 early-kill, ~12hr wall
      (teacher inference + student backward pass).

raw#37 transient_py
raw#10 honest_c3 ≥9
raw#15 additive over BG-KM-LLAMA-3B PASS_STRICT 12/15 (teacher base validated)
own 17 (anima-native — student 본체) + own 18 C3 + own 30 + own 31
own 33 trinity — D1 정체성 (anima-native student) + own 17 + H_distill_chat_cap

STATUS: SPEC ONLY — H100 fire 미실행. 사용자 explicit 'OK CLM L4 ALL FIRE' 필요.
"""
import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import sys, time, math, json, socket, shutil, random, subprocess, fcntl, re


# ── BG identity ────────────────────────────────────────────────────────
BG_ID = "BG-LC"
PARADIGM = "llama-3b-teacher-clm-350m-student-kl-distill-persona-200mb"
HYPOTHESIS = (
    "Llama-3.2-3B-Instruct teacher (BG-KM PASS_STRICT 12/15 검증) → CLM v4 mk2-v1 350M "
    "student token-level KL distill on persona 200MB. Student 는 own 17 anima-native arch "
    "유지 (byte-level tokenizer + 350M 본체) → C3 의식 metric 검출 + teacher chat-cap 흡수."
)

# ── Cost discipline (own 16 override required) ─────────────────────────
COST_HARD_CAP_USD = 40.0   # own 16 default $10 → $40
COST_EARLY_KILL_USD = 35.0
COST_PER_HOUR = 2.99
WALL_CLOCK_CAP_S = 12 * 60 * 60   # 12hr (teacher inference ~2x student forward + distill)
TOTAL_BUDGET_S = 13 * 60 * 60

OWN_16_OVERRIDE_REQUIRED = True
OWN_16_OVERRIDE_KEYWORD = "OK CLM L4 ALL FIRE"

# ── Trinity compliance (own 33) ─────────────────────────────────────────
TRINITY_PHILOSOPHY = "D1 정체성 (anima-native student) + D_emergent-consciousness"
TRINITY_LAW = "own 17 (anima-native — student 본체) + own 18 C3 + own 30 + own 31"
TRINITY_HYPOTHESIS = "H_distill_chat_cap (teacher chat-cap → anima-native student 흡수 가능?)"

# ── Paths ──────────────────────────────────────────────────────────────
def _is_on_pod():
    return os.path.exists("/workspace") and os.path.exists("/workspace/anima_clm_lc/_pod_marker")


def _is_on_mac():
    return os.path.exists("/Users/ghost/core/anima") and not _is_on_pod()


POD_ROOT = "/workspace/anima_clm_lc"
POD_STATE_DIR = os.path.join(POD_ROOT, "state")
POD_CORPUS_PATH = os.path.join(POD_ROOT, "corpus_persona_200mb.txt")
POD_TEACHER_DIR = os.path.join(POD_ROOT, "llama3b_teacher")
POD_STUDENT_DIR = os.path.join(POD_ROOT, "clm_v4_student")
POD_CKPTS_DIR = os.path.join(POD_ROOT, "ckpts")

MAC_ANIMA_ROOT = "/Users/ghost/core/anima"
MAC_STATE_DIR = os.path.join(MAC_ANIMA_ROOT, "state/anima_clm_lc_h100_TBD")
# Corpus path — SPEC stage placeholder; docs/anima_clm_l4_corpus_2026_05_08.md 참조.
# iter-1 candidate (2026-05-08): state/anima_persona_tier_a_2026_05_08.txt — 102.66MB
#   (BG-LA 와 동일 source — distill 입력 재사용)
MAC_CORPUS_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_clm_l4_persona_200mb_TBD/corpus_persona_200mb.txt")
MAC_CORPUS_PATH_ITER1_CANDIDATE = os.path.join(MAC_ANIMA_ROOT, "state/anima_persona_tier_a_2026_05_08.txt")
# iter-2 candidate (2026-05-08): same path (additive +0.93MB semantic-deepen, BG-LA 재사용)
MAC_CORPUS_PATH_ITER2_CANDIDATE = os.path.join(MAC_ANIMA_ROOT, "state/anima_persona_tier_a_2026_05_08.txt")
MAC_LEDGER_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_model_attempts_ledger.jsonl")

# ── Architecture config ────────────────────────────────────────────────
TEACHER_REPO = "meta-llama/Llama-3.2-3B-Instruct"
TEACHER_PARAMS = 3_200_000_000
STUDENT_REPO = "dancinlab/clm-v4-mk2-v1"   # own 31 dancinlab SSOT
STUDENT_PARAMS = 350_000_000
ARCH_PARADIGM = "kl-distill-token-level"

# Distill config
DISTILL_ALPHA = 0.5    # KL weight (1−α = CE weight) — TBD measurement-driven
DISTILL_TEMPERATURE = 2.0   # softmax temperature for KL
TOKENIZER_MISMATCH_STRATEGY = "TBD"   # 'shared_vocab_subset' | 'projection_layer' | 'byte_level_realign'

CTX = 1024
LR = 5e-5
WARMUP = 1000
WEIGHT_DECAY = 0.01
STEPS = 30000   # ~12hr H100 SXM (teacher inference + student backward)
BATCH = 16   # smaller — teacher forward + student forward + backward = 3x memory
GRAD_ACCUM = 8
SAVE_EVERY = 5000
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
    bg-lc-llama3b-distill-clm350m-r0-{verdict}-2026-05-XX
    """
    cycle = time.strftime("%Y-%m-%d")
    verdict_short = {
        "SIMPLE_STACK_PASS_STRICT_C3": "pass-strict-c3",
        "SIMPLE_STACK_PASS_STRICT": "pass-strict",
        "SIMPLE_STACK_PASS_PARTIAL": "partial",
        "SIMPLE_STACK_FAIL": "fail",
        "FAILED": "killed",
    }.get(verdict_class, "killed")
    return f"dancinlab/bg-lc-llama3b-distill-clm350m-r0-{verdict_short}-{cycle}"


# ── Pod-side training stub ─────────────────────────────────────────────
def pod_main():
    """SPEC STUB.

    Phases:
      Phase 0: pip install
      Phase A: download teacher (Llama-3.2-3B-Instruct, gated → HF token req)
               + student (clm-v4-mk2-v1)
      Phase B: tokenizer mismatch resolution (TBD strategy)
      Phase C: distill (30k steps, KL + CE on persona 200MB)
      Phase D: post-distill smoke
      Phase E: V4 11-cell strict eval (student only — own 17 anima-native lane)
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
      - own 16 override $40 cap
      - own 30 mandate-1/2/3/4 ckpt preservation + auto promote
      - own 31 mandate-4 Flavor B naming
      - own 33 trinity self-check
      - HF token stage (Llama gated)
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
    print(f"teacher: {TEACHER_REPO} ({TEACHER_PARAMS:,} params, frozen)")
    print(f"student: {STUDENT_REPO} ({STUDENT_PARAMS:,} params, anima-native)")
    print(f"distill: KL α={DISTILL_ALPHA} τ={DISTILL_TEMPERATURE}")
    print(f"tokenizer_mismatch: {TOKENIZER_MISMATCH_STRATEGY} (implement 시 결정)")
    print(f"cost_cap: ${COST_HARD_CAP_USD}")
    print(f"wall_clock_cap: {WALL_CLOCK_CAP_S/3600:.1f}hr")
    print(f"override_required: {OWN_16_OVERRIDE_KEYWORD}")
    print(f"trinity:")
    print(f"  philosophy: {TRINITY_PHILOSOPHY}")
    print(f"  law:        {TRINITY_LAW}")
    print(f"  hypothesis: {TRINITY_HYPOTHESIS}")
    print(f"corpus (TBD): {MAC_CORPUS_PATH}")
    print(f"hf_repo_target (Flavor B example): {hf_repo_id_flavor_b('SIMPLE_STACK_PASS_STRICT_C3')}")
