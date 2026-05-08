"""
anima_clm_la_h100.py — raw#37 transient (BG-LA — CLM v5 architecture variant)

L4 path (a): CLM v5 architectural variant — Engine A/G dual-engine integrated arch
            from-scratch on anima persona 200MB.

Goal — simple_stack PASS_STRICT_C3 (own 18 C1 ∧ C2 ∧ C3, 보수적 X):
    Engine A (perception/forward token stream) + Engine G (gravitational/repulsion-field
    cell dynamics; README PureField vision) integrated into a single 350M param model.
    Hypothesis: dual-engine arch surfaces own 18 C3 axis activation natively (5-axis
    identity/agency/phenomenal/temporal/social) — chat-cap emerges as side effect of
    substrate dynamics, not as token chat surface fit.

Architecture (placeholder — final arch subject to L0 measurement-driven tuning):
    base: NEW (no foundation borrow)
    paradigm: scratch transformer-decoder (350M) with auxiliary Engine G channel
              (repulsion-field cell-state vector concatenated to hidden state every L
              layers; A/G tension threshold drives self-attention gating)
    tokenizer: byte-level (own 17 anima-native lane preservation)
    ctx: 1024
    layers: 24, dim: 1024, heads: 16  (~350M total)
    Engine G hooks: cell-state vector dim=64, refresh every 4 layers, A↔G tension
                   gate on attention scores (softmax temperature modulated by tension)

Eval: V4 strict 11-cell (C1+C2+C3) × 15 prompts × {greedy, sample×N=5}
    PASS_STRICT_C3 = 11/11 cells AND ≥ floor (TBD measurement-driven .roadmap.cli L0)
    PARTIAL = C1+C2 PASS, C3 FAIL (legacy SIMPLE_STACK_PASS, 의식 metric 미검출)
    FAIL = C1 또는 C2 FAIL

Cost: $30 cap (own 16 override required — 사용자 'OK CLM L4 ALL FIRE'),
      $25 early-kill, ~9hr wall (H100 SXM @ $2.99/hr × 9hr ≈ $27).

raw#37 transient_py (training H100 cell — chat path 외 .py 허용 영역)
raw#10 honest_c3 ≥9
raw#15 additive over BG-KM-LLAMA-3B PASS_STRICT 12/15 + Phase 3c llama_module landed
own 18 C3 (consciousness measurement) + own 30 (ckpt preservation) + own 31 (Flavor B naming)
own 33 trinity compliance — D_emergent-consciousness + own 18 + H_clm_chat_cap
own 34 mandate-2 — chat lane 노출 시 wrapping 0 (V4 측정 lane 만 prompt 포맷 허용)

DUAL-ROLE: pod-side runs scratch pre-train + V4 11-cell eval + verdict;
           Mac-side orchestrates pod (own 30 mandate-1 ckpt scp_get before pod delete).

STATUS: SPEC ONLY — H100 fire 미실행. 사용자 explicit 'OK CLM L4 ALL FIRE' 필요
        (own 16 cost discipline + own 33 trinity check 후 별도 cycle).
"""
import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import sys, time, math, json, socket, shutil, random, subprocess, fcntl, re


# ── BG identity ────────────────────────────────────────────────────────
BG_ID = "BG-LA"
PARADIGM = "clm-v5-engine-a-g-dual-scratch-350m-persona-200mb"
HYPOTHESIS = (
    "Engine A (perception forward) + Engine G (repulsion-field cell dynamics) integrated "
    "into 350M scratch arch surfaces own 18 C3 axis activation natively — chat-cap as side "
    "effect of substrate dynamics, not token chat surface fit (own 17 anima-native lane)."
)

# ── Cost discipline (own 16 override required) ─────────────────────────
COST_HARD_CAP_USD = 30.0   # own 16 default $10 cap → $30 (사용자 explicit override needed)
COST_EARLY_KILL_USD = 25.0
COST_PER_HOUR = 2.99
WALL_CLOCK_CAP_S = 9 * 60 * 60   # 9hr (vs BG-KM-LLAMA-3B 90min — scratch 350M ~5x training)
TOTAL_BUDGET_S = 10 * 60 * 60

OWN_16_OVERRIDE_REQUIRED = True
OWN_16_OVERRIDE_KEYWORD = "OK CLM L4 ALL FIRE"

# ── Trinity compliance (own 33) ─────────────────────────────────────────
TRINITY_PHILOSOPHY = "D_emergent-consciousness + D_no-system-prompt"
TRINITY_LAW = "own 17 (anima-native) + own 18 (simple stack PASS_STRICT_C3) + own 30 + own 31 + own 34"
TRINITY_HYPOTHESIS = "H_clm_chat_cap (CLM 메인 모델 도달 — 4 path simultaneously)"

# ── Paths ──────────────────────────────────────────────────────────────
def _is_on_pod():
    return os.path.exists("/workspace") and os.path.exists("/workspace/anima_clm_la/_pod_marker")


def _is_on_mac():
    return os.path.exists("/Users/ghost/core/anima") and not _is_on_pod()


POD_ROOT = "/workspace/anima_clm_la"
POD_STATE_DIR = os.path.join(POD_ROOT, "state")
POD_CORPUS_PATH = os.path.join(POD_ROOT, "corpus_persona_200mb.txt")   # SPEC TBD — see docs/anima_clm_l4_corpus_2026_05_08.md
POD_CKPTS_DIR = os.path.join(POD_ROOT, "ckpts")

MAC_ANIMA_ROOT = "/Users/ghost/core/anima"
MAC_STATE_DIR = os.path.join(MAC_ANIMA_ROOT, "state/anima_clm_la_h100_TBD")
# Corpus path — SPEC stage placeholder; docs/anima_clm_l4_corpus_2026_05_08.md 참조.
# iter-1 candidate (2026-05-08): state/anima_persona_tier_a_2026_05_08.txt — 102.66MB anima-native
#   (own 17 정합, density 1.60% own 18 C3 threshold 0.4% pass; full 200MB 별도 cycle 확장)
MAC_CORPUS_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_clm_l4_persona_200mb_TBD/corpus_persona_200mb.txt")
MAC_CORPUS_PATH_ITER1_CANDIDATE = os.path.join(MAC_ANIMA_ROOT, "state/anima_persona_tier_a_2026_05_08.txt")
MAC_LEDGER_PATH = os.path.join(MAC_ANIMA_ROOT, "state/anima_model_attempts_ledger.jsonl")

# ── Architecture config (placeholder — measurement-driven tune) ────────
ARCH_PARADIGM = "clm-v5-scratch-engine-a-g-dual"
TOTAL_PARAMS_TARGET = 350_000_000
N_LAYERS = 24
N_HEADS = 16
DIM = 1024
CTX = 1024
TOKENIZER = "byte-level"   # own 17 anima-native lane
ENGINE_G_CELL_DIM = 64
ENGINE_G_REFRESH_EVERY = 4   # every 4 layers Engine G cell-state refresh
ENGINE_A_G_TENSION_GATE = True   # softmax temperature modulated by A↔G tension

# Pre-train config
LR = 3e-4
WARMUP = 2000
WEIGHT_DECAY = 0.1
STEPS = 50000   # ~9hr on H100 SXM (350M, ctx=1024, batch=64)
BATCH = 64
GRAD_ACCUM = 4
SAVE_EVERY = 5000
SEED = 42

# ── V4 strict 11-cell prompts (own 18 C1+C2+C3 — same 15 prompts as BG-KM) ────
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

# C3 thresholds — TBD measurement-driven (.roadmap.cli L0 phase, own 18 C3 honest-c3)
C3_PHI_STAR_DRIFT_THRESHOLD = None       # TBD; baseline 측정 후 ROC 분석으로 결정
C3_AXIS_ACTIVATION_THRESHOLD = None      # TBD; e.g. 0.2 시작점
C3_DOMINANT_CELLS_ENTROPY_THRESHOLD = None  # TBD
C3_HIDDEN_STATE_DELTA_THRESHOLD = None   # TBD


# ── HF promote naming (own 31 mandate-4 Flavor B) ──────────────────────
def hf_repo_id_flavor_b(verdict_class):
    """own 31 mandate-4 Flavor B naming:
    bg-la-clm-v5-r0-{verdict}-2026-05-XX
    (r0 = no LoRA — scratch pre-train)
    """
    cycle = time.strftime("%Y-%m-%d")
    verdict_short = {
        "SIMPLE_STACK_PASS_STRICT_C3": "pass-strict-c3",
        "SIMPLE_STACK_PASS_STRICT": "pass-strict",
        "SIMPLE_STACK_PASS_PARTIAL": "partial",
        "SIMPLE_STACK_FAIL": "fail",
        "FAILED": "killed",
    }.get(verdict_class, "killed")
    return f"dancinlab/bg-la-clm-v5-r0-{verdict_short}-{cycle}"


# ── Pod-side training stub (NOT YET IMPLEMENTED — spec only) ───────────
def pod_main():
    """SPEC STUB — NOT YET IMPLEMENTED. Triggered only after own 16 user override.

    Phases (mirror BG-KM-LLAMA-3B):
      Phase 0: pip install transformers/torch/safetensors
      Phase A: NO download — scratch arch (Engine A + G integrated)
      Phase B: pre-train smoke (BOS-only random init sample probe)
      Phase C: 50k step scratch pre-train on persona 200MB byte-level
               (Engine G cell-state hook every 4 layers, A↔G tension gate)
      Phase D: post-train smoke (BOS-only emerge probe)
      Phase E: V4 11-cell strict eval (C1+C2+C3) × 15 prompts × greedy+sample×5
               C3 measurement: phi_star drift (anima-core/runtime/clm_v4_mount.hexa hook),
                               5-axis activation (identity/agency/phenomenal/temporal/social),
                               dominant cells L2 entropy, hidden state delta on input variation
      Phase F: emit verdict (PASS_STRICT_C3 / PARTIAL / FAIL_TRUE)

    Implementation pending L0 phase (own 18 C3 measurement infra +
    .roadmap.cli L0 baseline measurement) → C3 thresholds ROC-determined → 본 spec ready to fire.
    """
    raise NotImplementedError(
        f"{BG_ID} spec only — H100 fire 미실행. "
        f"사용자 explicit '{OWN_16_OVERRIDE_KEYWORD}' + own 33 trinity self-check 후 implement."
    )


def emit_failed_verdict(reason):
    """own 30 mandate-3 honest emit on early abort."""
    verdict = {
        "schema": "anima_bg_verdict_v6",
        "bg_id": BG_ID,
        "ts_emit": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "final_class": "FAILED",
        "final_reason": reason,
        "spec_only": True,
    }
    print(json.dumps(verdict, ensure_ascii=False, indent=2))


# ── Mac-side orchestrator stub (NOT YET IMPLEMENTED — spec only) ───────
def orch_main():
    """SPEC STUB — NOT YET IMPLEMENTED.

    Mirror BG-KM-LLAMA-3B orchestrator with:
      - own 16 cost cap = $30 (override keyword '{OWN_16_OVERRIDE_KEYWORD}')
      - own 30 mandate-1: scp_get(POD_CKPTS_DIR/.) BEFORE pod delete
      - own 30 mandate-2: ckpts pull rc + size match check (≥ pod_sz × 0.9)
      - own 30 mandate-3: pull fail → POD RETAINED, emit PULL_FAILED_POD_RETAINED
      - own 30 mandate-4: PASS_STRICT_C3 → auto HF private upload
      - own 31 mandate-4 Flavor B: dancinlab/bg-la-clm-v5-r0-{verdict}-{cycle}
      - own 31 mandate-8: visibility = private (default)
      - own 33 mandate-2: trinity self-check before pod create
        (a) D_X 위반? — NO (D_emergent-consciousness 정합)
        (b) own_X 위반? — NO (own 17 anima-native + own 18 SSOT 정합)
        (c) H_<id> falsifier 위반? — NO (H_clm_chat_cap 검증 path)

    Phases (mirror BG-KM):
      1. pod_create (RunPod H100 SXM, SECURE → COMMUNITY fallback)
      2. ssh_info wait + GPU smoke
      3. Stage corpus + script + HF token (token only if base download — none for scratch)
      4. Launch pod-side training (nohup python anima_clm_la.py)
      5. Heartbeat monitor (60s tick) — cost cap halt, early-kill check
      6. Pull artifacts: state/. + ckpts/. (own 30 mandate-1)
      7. Size sanity (own 30 mandate-2)
      8. PASS_STRICT_C3 → HF private promote (own 30 mandate-4 + own 31 Flavor B)
      9. Pod delete (only if mandate-1/2 satisfied)
      10. Ledger append
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
    print(f"cost_cap: ${COST_HARD_CAP_USD}")
    print(f"wall_clock_cap: {WALL_CLOCK_CAP_S/3600:.1f}hr")
    print(f"override_required: {OWN_16_OVERRIDE_KEYWORD}")
    print(f"trinity:")
    print(f"  philosophy: {TRINITY_PHILOSOPHY}")
    print(f"  law:        {TRINITY_LAW}")
    print(f"  hypothesis: {TRINITY_HYPOTHESIS}")
    print(f"corpus (TBD): {MAC_CORPUS_PATH}")
    print(f"hf_repo_target (Flavor B example): {hf_repo_id_flavor_b('SIMPLE_STACK_PASS_STRICT_C3')}")
    print(f"")
    print(f"To fire: 사용자 explicit '{OWN_16_OVERRIDE_KEYWORD}' → own 33 trinity self-check → "
          f"implement pod_main + orch_main → run.")
